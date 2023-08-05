from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
import json
import traceback
from typing import Dict, List, Optional, Tuple

from aporia.as_code.resources.base import BaseResource, CompareStatus, NonDeletableResourceException
from aporia.as_code.resources.custom_metrics import CustomMetric
from aporia.as_code.resources.data_source import DataSource
from aporia.as_code.resources.dataset import Dataset
from aporia.as_code.resources.model import Model
from aporia.as_code.resources.monitor import Monitor
from aporia.as_code.resources.segment import Segment
from aporia.as_code.resources.version import Version
from aporia.sdk.client import Client


class StackAction(Enum):
    CREATE = "create"
    DELETE = "delete"
    PREVIEW = "preview"
    REFRESH = "refresh"


class ResourceStatus(Enum):
    CREATED = "created"  # Found in config file
    MISSING = "missing"  # Not found in config file, create
    DEPRECATED = "deprecated"  # Found in config file, definition changed
    # TODO: Support that
    # UNWANTED = "unwanted"  # Found in config file, not in resources


@dataclass
class Resource:
    resource: BaseResource
    depth: int
    status: ResourceStatus
    id: Optional[str] = None


RESOURCE_TYPE_TO_RESOURCE_CLASS = {
    CustomMetric.__name__: CustomMetric,
    DataSource.__name__: DataSource,
    Dataset.__name__: Dataset,
    Model.__name__: Model,
    Monitor.__name__: Monitor,
    Segment.__name__: Segment,
    Version.__name__: Version,
}


class Stack:
    def __init__(
        self,
        token: str,
        account: str,
        workspace: str = "default-workspace",
        base_url: str = "https://platform.aporia.com",
    ):
        self._resources: OrderedDict[str, Resource] = OrderedDict()
        self._output = None
        self._client = Client(base_url=f"{base_url}/api/v1/{account}/{workspace}", token=token)
        self._delete_resources: OrderedDict[str, BaseResource] = OrderedDict()

    def add(self, resource: BaseResource, depth=0, prefix=None):
        unique_id = (prefix or "") + resource.name

        if unique_id in self._resources.keys():
            raise Exception(f"Found duplicate resource name: {unique_id}")

        self._resources[unique_id] = Resource(
            resource=resource, depth=depth, status=ResourceStatus.MISSING
        )
        if hasattr(resource, "sub_resources"):
            for sub_resource, _ in resource.sub_resources:
                self.add(sub_resource, depth=depth + 1, prefix=f"{prefix or ''}{resource.name}/")

    def _call_argsetters(self, resource, resource_data):
        if hasattr(resource, "sub_resources"):
            sub_resources = resource.sub_resources
            for sub_resource, argsetter in sub_resources:
                argsetter(resource_data, sub_resource)
        if hasattr(resource, "dependants"):
            dependants = resource.dependants
            for sub_resource, argsetter in dependants:
                argsetter(resource_data, sub_resource)

    def _preview(self, delete: bool = False):
        if delete:
            RESOURCE_STATUS_TO_PREVIEW_ACTION = {
                ResourceStatus.CREATED: "delete",
                ResourceStatus.MISSING: "create",
                ResourceStatus.DEPRECATED: "delete",
            }
            for resource_entry in self._resources.values():
                if resource_entry.status is ResourceStatus.MISSING:
                    continue
                print(
                    f"|-{'----' * resource_entry.depth}{resource_entry.resource.name} - {RESOURCE_STATUS_TO_PREVIEW_ACTION[resource_entry.status]}"
                )
        else:
            RESOURCE_STATUS_TO_PREVIEW_ACTION = {
                ResourceStatus.CREATED: "pass",
                ResourceStatus.MISSING: "create",
                ResourceStatus.DEPRECATED: "update",
            }
            for resource_entry in self._resources.values():
                print(
                    f"|-{'----' * resource_entry.depth}{resource_entry.resource.name} - {RESOURCE_STATUS_TO_PREVIEW_ACTION[resource_entry.status]}"
                )
        if len(self._delete_resources) > 0:
            print("Removed resources:")
        for unique_id in self._delete_resources.keys():
            resource_parts = unique_id.split("/")
            depth = len(resource_parts) - 1
            name = resource_parts[-1]
            print(f"|-{'----' * depth}{name} - delete")

    def __pop_deleted_sub_resources(self, non_deleteable_resources: List[str], unique_id):
        resource_entry = self._resources[unique_id]
        if hasattr(resource_entry.resource, "sub_resources"):
            for resource, _ in resource_entry.resource.sub_resources:
                sub_resource_unique_id = f"{unique_id}/{resource.name}"
                if sub_resource_unique_id in non_deleteable_resources:
                    self.__pop_deleted_sub_resources(
                        non_deleteable_resources=non_deleteable_resources,
                        unique_id=sub_resource_unique_id,
                    )
                    self._output.pop(sub_resource_unique_id)
                elif sub_resource_unique_id in self._output.keys():
                    raise RuntimeError(
                        f"Resource deletion missed for {sub_resource_unique_id}. Stack potentially corrupted."
                    )

    def _create(self) -> Tuple[Dict, Optional[Exception]]:
        output = self._output or {}
        error = None
        try:
            # Create/update resources
            for (
                unique_id,
                resource_entry,
            ) in self._resources.items():
                if resource_entry.status is ResourceStatus.CREATED:
                    continue
                if hasattr(resource_entry.resource, "deferred_load"):
                    resource_entry.resource.deferred_load(self._client, resource_entry.resource)

                if resource_entry.status is ResourceStatus.MISSING:
                    _, resource_data = resource_entry.resource.create(client=self._client)
                elif resource_entry.status is ResourceStatus.DEPRECATED:
                    resource_data = resource_entry.resource.update(
                        client=self._client, id=self._output[unique_id]["id"]
                    )
                else:
                    raise Exception("Unexpected resource status")
                self._call_argsetters(resource_entry.resource, resource_data)
                output[unique_id] = resource_data
                output[unique_id]["_resource_type"] = type(resource_entry.resource).__name__
                resource_entry.status = ResourceStatus.CREATED

            # Delete resources
            non_deleteable_resources = []
            for unique_id, resource_class in list(self._delete_resources.items())[::-1]:
                resource_data = self._output[unique_id]
                try:
                    resource_class.delete(client=self._client, id=resource_data["id"])
                except NonDeletableResourceException:
                    non_deleteable_resources.append(unique_id)
                    continue
                for non_deleteable_resource in [*non_deleteable_resources]:
                    if non_deleteable_resource.startswith(f"{unique_id}/"):
                        self._output.pop(non_deleteable_resource)
                        non_deleteable_resources.remove(non_deleteable_resource)
                self._output.pop(unique_id)
        except Exception as e:
            error = e

        return output, error

    def _destroy(self):
        # Read from storage
        # Destroy all resources
        # TODO: Consider adding all this logic into _create, just with setting resource.action to delete
        error = None
        if self._output is None:
            raise Exception("Stack not created")
        try:
            non_deleteable_resources = []
            for unique_id, resource_entry in list(self._resources.items())[::-1]:
                if unique_id in self._output.keys():
                    resource_data = self._output[unique_id]
                    try:
                        resource_entry.resource.delete(client=self._client, id=resource_data["id"])
                    except NonDeletableResourceException:
                        non_deleteable_resources.append(unique_id)
                        continue
                    self.__pop_deleted_sub_resources(non_deleteable_resources, unique_id)
                    self._output.pop(unique_id)
            for unique_id, resource_class in list(self._delete_resources.items())[::-1]:
                resource_data = self._output[unique_id]
                try:
                    resource_class.delete(client=self._client, id=resource_data["id"])
                except NonDeletableResourceException:
                    non_deleteable_resources.append(unique_id)
                    continue
                self.__pop_deleted_sub_resources(non_deleteable_resources, unique_id)
                self._output.pop(unique_id)
        except Exception as e:
            error = e

        return error

    def _diff(self):
        for unique_id, resource_entry in self._resources.items():
            if unique_id in self._output.keys():
                # Resource already exists. Call argsetters
                # TODO: Add support for edit
                resource_data = self._output[unique_id]
                self._call_argsetters(resource_entry.resource, resource_data)
                compare_status = self._resources[unique_id].resource.compare(
                    resource_data=resource_data
                )
                if compare_status is CompareStatus.SAME:
                    self._resources[unique_id].status = ResourceStatus.CREATED
                elif compare_status is CompareStatus.UPDATEABLE:
                    self._resources[unique_id].status = ResourceStatus.DEPRECATED
                else:
                    raise Exception(
                        f"Configuration for {unique_id} was edited but can't be updated!"
                    )
                continue

        for unique_id, resource_data in self._output.items():
            if unique_id not in self._resources.keys():
                self._delete_resources[unique_id] = RESOURCE_TYPE_TO_RESOURCE_CLASS[
                    resource_data["_resource_type"]
                ]

    def apply(
        self,
        action: StackAction = StackAction.CREATE,
        skip_preview: bool = False,
        yes: bool = False,
        rollback=True,
        yes_rollback=False,
        config_path: Optional[str] = None,
    ):
        action = StackAction(action)
        # TODO: Read config_path, and apply diffs. Then write to config_path
        if config_path is not None:
            try:
                with open(config_path, "r") as f:
                    self._output = json.loads(f.read())
                    self._diff()
            except FileNotFoundError:
                # It's OK if the file wasn't found. It's probably the first run
                pass

        if action is StackAction.CREATE:
            if not skip_preview:
                self._preview()
            if not yes:
                if "y" != input("Do create? [Y/N] ").lower():
                    print("Cancelling...")
                    return
            self._output, error = self._create()

            if error is not None:
                traceback.print_exception(error)
                if rollback:
                    if not yes_rollback:
                        if "y" == input("Delete created resources? [Y/N] ").lower():
                            print("Deleting...")
                            error = self._destroy()
                            if error is not None:
                                traceback.print_exception(error)
        elif action is StackAction.PREVIEW:
            self._preview()
            return
        elif action is StackAction.DELETE:
            if not skip_preview:
                self._preview(delete=True)
            # TODO: Change the way you use ResourceAction to support deletes, edits etc all at once, and previews for all
            if not yes:
                if "y" != input("Do delete? [Y/N] ").lower():
                    print("Cancelling...")
                    return
            error = self._destroy()
            if error is not None:
                traceback.print_exception(error)
        else:
            raise ValueError("Unknown action")

        if config_path is not None:
            with open(config_path, "w") as f:
                f.write(json.dumps(self._output))

    def get_resource_id(self, unique_id: str) -> str:
        return self._output[unique_id]["id"]

from typing import Any, Dict, Optional, Tuple

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.sdk.client import Client
from aporia.sdk.monitors import Monitor as _Monitor


class Monitor(BaseResource):
    def __init__(self, resource_name: str, /, *, name: Optional[str] = None):
        raise NotImplementedError()
        self.name = resource_name
        if name is None:
            name = resource_name

        self._args = {"name": name}

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def compare(self, resource_data: Dict) -> CompareStatus:
        if all([self._args[k] == resource_data[k] for k in self._args.keys()]):
            return CompareStatus.SAME
        return CompareStatus.UPDATEABLE

    def create(self, client: Client) -> Tuple[str, Dict]:
        monitor = _Monitor.create(client=client, **self._args)
        return monitor.id, monitor.raw_data

    def read(self, client: Client, id: str) -> Dict:
        return _Monitor.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        monitor = _Monitor.read(client=client, id=id)
        monitor.update(**self._args)
        return monitor.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Monitor.delete_by_id(client=client, id=id)

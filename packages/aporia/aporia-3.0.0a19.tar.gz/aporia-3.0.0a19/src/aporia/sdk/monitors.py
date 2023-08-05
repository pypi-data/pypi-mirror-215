from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, root_validator, validator

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client

SEGMENT_ID_ALL_DATA = "ALLDATA"


class MonitorType(Enum):
    MODEL_ACTIVITY = "model_activity"
    DATA_DRIFT = "data_drift"
    PREDICTION_DRIFT = "prediction_drift"
    MISSING_VALUES = "missing_values"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    MODEL_STALENESS = "model_staleness"
    METRIC_CHANGE = "metric_change"
    CUSTOM_METRIC_MONITOR = "custom_metric"
    VALUE_RANGE = "notimplemented1"
    NEW_VALUES = "notimplemented2"


class DetectionMethod(Enum):
    ANOMALY = "anomaly"
    PERCENTAGE = "percentage"
    ABSOLUTE = "absolute"
    COMPARED_TO_SEGMENT = "segment"
    COMPARED_TO_TRAINING = "training"


class SourceType(Enum):
    SERVING = "SERVING"
    TRAINING = "TRAINING"


class PeriodType(Enum):
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"
    MONTHS = "M"


class TimePeriod(BaseModel):
    count: int
    type: PeriodType

    def to_string(self) -> str:
        return f"{self.count}{self.type.value}"


# TODO: Rename stuff to match Python conventions
class FocalConfiguration(BaseModel):
    source: SourceType = SourceType.SERVING
    timePeriod: Optional[TimePeriod] = None  # Missing for staleness
    skipPeriod: Optional[TimePeriod] = None
    alignBinsWithBaseline: Optional[bool] = None  # Needed (as True) for drift/histogram

    @validator("source")
    def _validate_source(cls, value):
        if value is not SourceType.SERVING:
            raise ValueError("For focal, source must always be serving")
        return value

    @validator("alignBinsWithBaseline")
    def _validate_align_bins_with_baseline(cls, value):
        if value is not True:
            raise ValueError("If alignBinsWithBaseline appears, it must be True")
        return value

    def to_dict(self):
        result = {
            "source": self.source.value,
        }
        if self.timePeriod is not None:
            result["timePeriod"] = self.timePeriod.to_string()
        if self.skipPeriod is not None:
            result["skipPeriod"] = self.skipPeriod.to_string()
        if self.alignBinsWithBaseline is not None:
            result["alignBinsWithBaseline"] = self.alignBinsWithBaseline

        return result


class BaselineConfiguration(BaseModel):
    source: SourceType
    timePeriod: TimePeriod  # Actual time to compare to
    skipPeriod: Optional[TimePeriod] = None  # By default, equal to Focal. Doesn't exist on training
    aggregationPeriod: Optional[TimePeriod] = None  # Does't exist on drift/histogram
    segmentValue: Optional[Union[str, int, float]] = None
    segmentGroupId: Optional[str] = None

    @validator("skipPeriod", always=True)
    def _validate_skip_period(cls, value, values):
        if values["source"] is SourceType.TRAINING:
            if value is not None:
                raise ValueError("For training baseline, skipPeriod must not appear")
        # TODO: This is basically defaulted in the global monitor validator
        # elif values["source"] is SourceType.SERVING:
        #     if value is None:
        #         raise ValueError("For serving baseline, skipPeriod must appear")
        return value

    def to_dict(self):
        result = {"source": self.source.value, "timePeriod": self.timePeriod.to_string()}
        if self.skipPeriod is not None:
            result["skipPeriod"] = self.skipPeriod.to_string()
        if self.aggregationPeriod is not None:
            result["aggregationPeriod"] = self.aggregationPeriod.to_string()
        # TODO: Validate these fields
        if self.segmentGroupId is not None:
            if self.segmentGroupId == SEGMENT_ID_ALL_DATA:
                result["segmentGroupId"] = None
            else:
                result["segmentGroupId"] = self.segmentGroupId
        if self.segmentValue is not None:
            result["segmentValue"] = self.segmentValue

        return result


class MetricType(Enum):
    COUNT = "count"
    MISSING_RATIO = "missing_ratio"
    LAST_VERSION_CREATION = "last_version_creation"
    HISTOGRAM = "histogram"
    CUSTOM_METRIC = "custom_metric"
    # TODO: These are probably just all generic metrics
    ACCURACY = "accuracy"
    MEAN = "mean"


class MetricConfiguration(BaseModel):
    type: MetricType
    # Necessary for custom metrics
    id: Optional[str] = None
    # Necessary for general metrics
    metricAtK: Optional[int] = None  # TODO: Almost always 3 -.- Gubkin
    threshold: Optional[float] = None
    # TODO: Check if more things exist for other metrics
    # TODO: Maybe add class for Aporia metrics

    @validator("id", always=True)
    def _validate_id(cls, value, values):
        if values["type"] is MetricType.CUSTOM_METRIC:
            if value is None:
                raise ValueError("For custom metrics, id must appear")
        else:
            if value is not None:
                raise ValueError("id must only appear for custom metrics")
        return value

    def to_dict(self):
        result = {"type": self.type.value}
        if self.id is not None:
            result["id"] = self.id
        if self.metricAtK is not None:
            result["metricAtK"] = self.metricAtK
        if self.threshold is not None:
            result["threshold"] = self.threshold

        return result


class LogicEvaluationType(Enum):
    RATIO = "RATIO"
    RANGE = "RANGE"
    TIME_SERIES_ANOMALY = "TIME_SERIES_ANOMALY"
    APORIA_DRIFT_SCORE = "APORIA_DRIFT_SCORE"
    MODEL_STALENESS = "MODEL_STALENESS"


class ThresholdConfiguration(BaseModel):
    numeric: Optional[float] = None
    categorical: Optional[float] = None

    def to_dict(self):
        result = {}

        if self.numeric is not None:
            result["numeric"] = self.numeric
        if self.categorical is not None:
            result["categorical"] = self.categorical

        return result


class LogicEvaluationConfiguration(BaseModel):
    name: LogicEvaluationType
    # Needed for range (Both must exist, if one isn't used, it should be null)
    min: Optional[float] = None
    # Also needed for ratio (float) and staleness (TimePeriod)
    max: Optional[Union[float, TimePeriod]] = None
    # Needed for timeseries anomaly
    sensitivity: Optional[float] = None
    # Needed for Aporia drift score
    thresholds: Optional[ThresholdConfiguration] = None

    @root_validator()
    def _validate_logic_evaluation(cls, values):
        if values["name"] is LogicEvaluationType.RANGE:
            if isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a float or None for Range logic evaluation")
            if values["sensitivity"] is not None or values["thresholds"] is not None:
                raise ValueError("Only min and max can appear for Range logic evaluation")

        if values["name"] is LogicEvaluationType.RATIO:
            if not isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a TimePeriod for Ratio logic evaluation")
            if (
                values["min"] is not None
                or values["sensitivity"] is not None
                or values["thresholds"] is not None
            ):
                raise ValueError("Only max can appear for Ratio logic evaluation")

        if values["name"] is LogicEvaluationType.TIME_SERIES_ANOMALY:
            if values["sensitivity"] is None:
                raise ValueError("sensitivity must appear for Timeseries Anomaly Logic Evaluation")
            if (
                values["max"] is not None
                or values["min"] is not None
                or values["thresholds"] is not None
            ):
                raise ValueError(
                    "Only sensitivity can appear for Timeseries Anomaly logic evaluation"
                )

        if values["name"] is LogicEvaluationType.APORIA_DRIFT_SCORE:
            if values["thresholds"] is None:
                raise ValueError("thresholds must appear for Aporia Drift Score Logic Evaluation")
            if (
                values["max"] is not None
                or values["min"] is not None
                or values["sensitivity"] is not None
            ):
                raise ValueError(
                    "Only thresholds can appear for Aporia Drift Score logic evaluation"
                )

        return values

    def to_dict(self):
        result = {"name": self.name.value}

        if self.min is not None:
            result["min"] = self.min
        if self.max is not None:
            if isinstance(self.max, TimePeriod):
                result["max"] = self.max.to_string()
            else:
                result["max"] = self.max
        if self.sensitivity is not None:
            result["sensitivity"] = self.sensitivity
        if self.thresholds is not None:
            result["thresholds"] = self.thresholds.to_dict()

        return result


class PreConditionType(Enum):
    # TODO: Check for MAX_BASELINE_DATA_POINTS
    MIN_BASELINE_DATA_POINTS = "MIN_BASELINE_DATA_POINTS"
    FOCAL_DATA_VALUE_IN_RANGE = "FOCAL_DATA_VALUE_IN_RANGE"


class PreConditionConfiguration(BaseModel):
    name: PreConditionType
    # Needed for MIN_BASELINE_DATA_POINTS
    value: Optional[int] = None
    # Needed for FOCAL_DATA_VALUE_IN_RANGE
    min: Optional[float] = None

    @root_validator()
    def _validate_pre_condition(cls, values):
        if values["name"] is PreConditionType.MIN_BASELINE_DATA_POINTS:
            if values["value"] is None:
                raise ValueError("value must appear for MIN_BASELINE_DATA_POINTS PreCondition")
            if values["min"] is not None:
                raise ValueError("Only value can appear for MIN_BASELINE_DATA_POINTS PreCondition")
        if values["name"] is PreConditionType.FOCAL_DATA_VALUE_IN_RANGE:
            if values["min"] is None:
                raise ValueError("min must appear for MIN_BASELINE_DATA_POINTS PreCondition")
            if values["values"] is not None:
                raise ValueError("Only min can appear for MIN_BASELINE_DATA_POINTS PreCondition")

        return values

    def to_dict(self):
        result = {"name": self.name.value}

        if self.min is not None:
            result["min"] = self.min
        if self.value is not None:
            result["value"] = self.value

        return result


class ActionType(Enum):
    ALERT = "ALERT"


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AlertType(Enum):
    MODEL_STALENESS = "model_staleness"
    PREDICTION_DRIFT_ANOMALY = "prediction_drift_anomaly"
    PREDICTION_DRIFT_SEGMENT_CHANGE = (
        "prediction_drift_segment_change"  # TODO: Add more segment-specific stuff
    )
    DATA_DRIFT_ANOMALY = "data_drift_anomaly"
    DATA_DRIFT_TRAINING = "data_drift_training"
    METRIC_CHANGE = "metric_change"
    FEATURE_MISSING_VALUES_CHANGE = "feature_missing_values_change"
    FEATURE_MISSING_VALUES_ANOMALY = "feature_missing_values_anomaly"
    FEATURE_MISSING_VALUES_THRESHOLD = "feature_missing_values_threshold"
    FEATURE_MISSING_VALUES_SEGMENT_CHANGE = "feature_missing_values_segment_change"
    MODEL_ACTIVITY_THRESHOLD = "model_activity_threshold"
    MODEL_ACTIVITY_ANOMALY = "model_activity_anomaly"
    MODEL_ACTIVITY_CHANGE = "model_activity_change"


class VisualizationType(Enum):
    DISTRIBUTION_COMPARE_CHART = "distribution_compare_chart"
    RANGE_LINE_CHART = "range_line_chart"
    VALUE_OVER_TIME = "value_over_time"


class ActionConfiguration(BaseModel):
    type: ActionType
    severity: Severity
    alertType: AlertType
    description: str  # TODO: Enumize
    notification: List  # TODO: Look deeper into that
    action_schema: str = "v1"  # TODO: Realize what to do with it
    maxAlertsPerDay: Optional[int] = None
    visualization: Optional[VisualizationType] = None

    def to_dict(self):
        result = {
            "type": self.type.value,
            "severity": self.severity.value,
            "alertType": self.alertType.value,
            "description": self.description,
            "notification": self.notification,
            "schema": self.action_schema,
        }

        if self.maxAlertsPerDay is not None:
            result["maxAlertsPerDay"] = self.maxAlertsPerDay
        if self.visualization is not None:
            result["visualization"] = self.visualization.value

        return result


class ModelIdentification(BaseModel):
    id: str
    version: Optional[
        str
    ] = None  # None indicates all versions # TODO: Saw one saying "all_versions" as well?? Validate that

    def to_dict(self):
        return self.dict()


class SegmentIdentification(BaseModel):
    group: Optional[str] = None
    value: Optional[Union[str, int, float]] = None  # None indicates all segment values

    def to_dict(self):
        return self.dict()


class Identification(BaseModel):
    models: ModelIdentification
    segment: SegmentIdentification
    # TODO: Check for raw inputs and actuals
    features: Optional[List[str]] = None
    predictions: Optional[List[str]] = None

    def to_dict(self):
        result = {
            "models": self.models.to_dict(),
            "segment": self.segment.to_dict(),
        }
        if self.features is not None:
            result["features"] = self.features
        if self.predictions is not None:
            result["predictions"] = self.predictions

        return result


class MonitorConfiguration(BaseModel):
    identification: Identification
    focal: FocalConfiguration
    metric: MetricConfiguration
    actions: List[ActionConfiguration]
    baseline: Optional[BaselineConfiguration] = None
    logicEvaluations: Optional[List[LogicEvaluationConfiguration]] = None
    preConditions: Optional[List[PreConditionConfiguration]] = None
    # TODO: Add cross-configuration validators

    @root_validator()
    def _validate_monitor_configuration(cls, values):
        if values["baseline"] is not None:
            # For non-training monitors, skipPeriod defaults to the focal timePeriod, unless it's per segment
            if values["baseline"].source is SourceType.SERVING:
                if values["identification"].segment.group is None:
                    if values["baseline"].skipPeriod is None:
                        values["baseline"].skipPeriod = values["focal"].timePeriod

            # For non-histogram monitors, aggregationPeriod defaults to timePeriod
            if values["metric"].type is not MetricType.HISTOGRAM:
                if values["baseline"].aggregationPeriod is None:
                    values["baseline"].aggregationPeriod = values["baseline"].timePeriod

        return values

    def to_dict(self):
        result = {
            "identification": self.identification.to_dict(),
            "configuration": {
                "focal": self.focal.to_dict(),
                "metric": self.metric.to_dict(),
                "actions": [action.to_dict() for action in self.actions],
            },
        }
        if self.baseline is not None:
            result["configuration"]["baseline"] = self.baseline.to_dict()
        if self.logicEvaluations is not None:
            result["configuration"]["logicEvaluations"] = [
                logic_evaluation.to_dict() for logic_evaluation in self.logicEvaluations
            ]
        if self.preConditions is not None:
            result["configuration"]["preConditions"] = [
                precondition.to_dict() for precondition in self.preConditions
            ]

        return result


class Monitor(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        # TODO: Enum-ize
        self.type = data["type"]

    @classmethod
    def get_all(cls, client: Client) -> List["Monitor"]:
        response = client.send_request("/monitors", "GET")

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        model_id: str,
        name: str,
        monitor_type: MonitorType,
        scheduling: str,  # TODO: Optionally infer from configuration
        configuration: MonitorConfiguration,
        comment: Optional[str] = None,
        creator: Optional[str] = None,
        is_active: bool = True,
    ) -> "Monitor":
        monitor_type = MonitorType(monitor_type)

        # TODO: Justify these values
        if scheduling is None:
            if configuration.focal.timePeriod is None:
                scheduling = "0 * * * *"
            else:
                # if configuration.focal.timePeriod.count == 1:
                if configuration.focal.timePeriod.type is PeriodType.HOURS:
                    scheduling = "*/5 * * * *"  # Every 5 minutes
                elif configuration.focal.timePeriod.type is PeriodType.DAYS:
                    scheduling = "0 */4 * * *"  # Every 4 hours
                elif configuration.focal.timePeriod.type is PeriodType.WEEKS:
                    scheduling = "0 */12 * * *"  # Every 12 hours

        configuration.identification.models.id = model_id

        if scheduling is None:
            raise ValueError("Scheduling must be defined")

        response = client.send_request(
            "/monitors",
            "POST",
            {
                "name": name,
                "type": monitor_type.value,
                "scheduling": scheduling,
                "configuration": configuration.to_dict(),
                "comment": comment,
                "creator_id": creator,
                "is_active": is_active,
            },
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Monitor":
        response = client.send_request(f"/monitors/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self):
        response = self.client.send_request(f"/monitors/{self.id}", "PUT")
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/monitors/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/monitors/{id}", "DELETE")
        client.assert_response(response)

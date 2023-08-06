import typing, abc
from TransformsAI.Animo.Learning.Sensors import SensorConfig, GridSensorShape, SensorSpec
from System import Array_1, Span_1
from TransformsAI.Animo.Objects.Character import CharacterObject
from TransformsAI.Animo.Learning.Sensors.CellSensors import CellSensor
from TransformsAI.Animo.Learning.Sensors.EntitySensors import EntitySensor

class GridSensor(Sensor):
    sensorConfig : SensorConfig
    @property
    def GridShape(self) -> GridSensorShape: ...
    @property
    def OptionKeys(self) -> Array_1[str]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetGridObservations(self, character: CharacterObject, xzdObservations: Array_1[float]) -> None: ...


class RecyclingGridSensor(GridSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    recycledCellSensor : CellSensor
    sensorConfig : SensorConfig
    @property
    def GridShape(self) -> GridSensorShape: ...
    @property
    def OptionKeys(self) -> Array_1[str]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...


class Sensor(abc.ABC):
    sensorConfig : SensorConfig
    @property
    def OptionKeys(self) -> Array_1[str]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...


class VariableLengthSensor(Sensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    reusedEntitySensor : EntitySensor
    sensorConfig : SensorConfig
    @property
    def EntitySize(self) -> int: ...
    @property
    def NumEntities(self) -> int: ...
    @property
    def OptionKeys(self) -> Array_1[str]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetEntitiesObservations(self, character: CharacterObject, outEPObservations: Array_1[float], offset: int = ...) -> None: ...


class VectorSensor(Sensor):
    sensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def OptionKeys(self) -> Array_1[str]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    # Skipped GetObservations due to it being static, abstract and generic.

    GetObservations : GetObservations_MethodGroup
    class GetObservations_MethodGroup:
        @typing.overload
        def __call__(self, character: CharacterObject, values: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, character: CharacterObject, observations: Array_1[float], offset: int = ...) -> None:...



import typing
from System.Collections.Generic import List_1, Dictionary_2
from System import MulticastDelegate, IAsyncResult, AsyncCallback
from System.Reflection import MethodInfo
from TransformsAI.Animo.Learning.Sensors.Primitives import Sensor
from TransformsAI.Animo.Numerics import Vec3Int

class GridSensorShape:
    def __init__(self, xLength: int, zLength: int, depth: int) -> None: ...
    Depth : int
    XLength : int
    ZLength : int


class SensorConfig:
    def __init__(self) -> None: ...
    childSensorConfigs : List_1[SensorConfig]
    sensorName : str
    sensorSpec : SensorSpec
    sensorType : str


class SensorFactory(MulticastDelegate):
    def __init__(self, object: typing.Any, method: int) -> None: ...
    @property
    def Method(self) -> MethodInfo: ...
    @property
    def Target(self) -> typing.Any: ...
    def BeginInvoke(self, config: SensorConfig, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
    def EndInvoke(self, result: IAsyncResult) -> Sensor: ...
    def Invoke(self, config: SensorConfig) -> Sensor: ...


class SensorRegistry:
    Instance : SensorRegistry
    numTypeIds : int
    registry : Dictionary_2[str, SensorFactory]
    def CreateSensor(self, sensorConfig: SensorConfig) -> Sensor: ...
    @staticmethod
    def GetSensorConfigs(characterId: int) -> List_1[SensorConfig]: ...


class SensorSpec:
    @property
    def GridShape(self) -> GridSensorShape: ...
    @property
    def SensorType(self) -> SensorTypes: ...
    @SensorType.setter
    def SensorType(self, value: SensorTypes) -> SensorTypes: ...
    @property
    def Shape(self) -> Vec3Int: ...
    @Shape.setter
    def Shape(self, value: Vec3Int) -> Vec3Int: ...
    @property
    def VariableLenShape(self) -> VariableLenSensorShape: ...
    @property
    def VectorLength(self) -> int: ...
    @staticmethod
    def Grid(width: int, height: int, depth: int) -> SensorSpec: ...
    @staticmethod
    def VariableLength(entities: int, properties: int) -> SensorSpec: ...
    @staticmethod
    def Vector(length: int) -> SensorSpec: ...


class SensorTypes(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Vector : SensorTypes # 0
    VariableLen : SensorTypes # 1
    Grid : SensorTypes # 2


class VariableLenSensorShape:
    def __init__(self, entities: int, properties: int) -> None: ...
    Entities : int
    Properties : int


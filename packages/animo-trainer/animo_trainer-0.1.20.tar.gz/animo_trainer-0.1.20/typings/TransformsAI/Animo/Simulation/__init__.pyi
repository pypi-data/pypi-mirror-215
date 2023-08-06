import typing
from System.Collections.Generic import HashSet_1
from TransformsAI.Animo.Objects import TypeIds
from TransformsAI.Animo.Grid import VoxelGrid

class EndCondition:
    def __init__(self) -> None: ...
    NeedsCharacters : bool
    RequiredItems : HashSet_1[TypeIds]
    StepLimit : typing.Optional[int]
    def IsMet(self, grid: VoxelGrid, stepCount: int) -> bool: ...
    def Validate(self, grid: VoxelGrid) -> None: ...


class SimulationRunner:
    def __init__(self, grid: VoxelGrid) -> None: ...
    def Simulate(self) -> None: ...


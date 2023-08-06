import abc
from System import Span_1

class ObservationSpanExtensions(abc.ABC):
    @staticmethod
    def AddOneHot(span: Span_1[float], hotIndex: int) -> None: ...
    @staticmethod
    def SetOneHot(span: Span_1[float], hotIndex: int) -> None: ...


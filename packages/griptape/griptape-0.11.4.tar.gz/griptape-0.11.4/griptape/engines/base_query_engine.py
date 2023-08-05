from abc import ABC, abstractmethod
from attr import define
from griptape.artifacts import TextArtifact


@define
class BaseQueryEngine(ABC):
    @abstractmethod
    def query(self, query: str, *args, **kwargs) -> TextArtifact:
        ...

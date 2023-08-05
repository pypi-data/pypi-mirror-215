from __future__ import annotations
import logging
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from attr import define, field
from griptape.tokenizers import BaseTokenizer

if TYPE_CHECKING:
    from griptape.artifacts import TextArtifact


@define
class BasePromptDriver(ABC):
    max_retries: int = field(default=8, kw_only=True)
    retry_delay: float = field(default=1, kw_only=True)
    temperature: float = field(default=0.1, kw_only=True)
    model: str
    tokenizer: BaseTokenizer

    def run(self, **kwargs) -> TextArtifact:
        for attempt in range(0, self.max_retries + 1):
            try:
                return self.try_run(**kwargs)
            except Exception as e:
                logging.error(f"PromptDriver.run attempt {attempt} failed: {e}\nRetrying in {self.retry_delay} seconds")

                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise e

    @abstractmethod
    def try_run(self, **kwargs) -> TextArtifact:
        ...

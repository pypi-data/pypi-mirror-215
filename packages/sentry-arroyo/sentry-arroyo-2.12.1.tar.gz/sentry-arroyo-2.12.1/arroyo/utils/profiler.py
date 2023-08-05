import logging
import time
from cProfile import Profile
from pathlib import Path
from typing import Mapping, Optional

from arroyo.processing.strategies.abstract import (
    ProcessingStrategy,
    ProcessingStrategyFactory,
)
from arroyo.types import Commit, Message, Partition, TStrategyPayload

logger = logging.getLogger(__name__)


class ProcessingStrategyProfilerWrapper(ProcessingStrategy[TStrategyPayload]):
    def __init__(
        self,
        strategy: ProcessingStrategy[TStrategyPayload],
        profiler: Profile,
        output_path: str,
    ) -> None:
        self.__strategy = strategy
        self.__profiler = profiler
        self.__output_path = output_path

    def poll(self) -> None:
        self.__strategy.poll()

    def submit(self, message: Message[TStrategyPayload]) -> None:
        self.__strategy.submit(message)

    def close(self) -> None:
        self.__strategy.close()

    def terminate(self) -> None:
        self.__strategy.terminate()
        self.__profiler.disable()  # not sure if necessary
        logger.info(
            "Writing profile data from %r to %r...", self.__profiler, self.__output_path
        )
        self.__profiler.dump_stats(self.__output_path)

    def join(self, timeout: Optional[float] = None) -> None:
        self.__strategy.join(timeout)
        self.__profiler.disable()  # not sure if necessary
        logger.info(
            "Writing profile data from %r to %r...", self.__profiler, self.__output_path
        )
        self.__profiler.dump_stats(self.__output_path)


class ProcessingStrategyProfilerWrapperFactory(
    ProcessingStrategyFactory[TStrategyPayload]
):
    def __init__(
        self,
        strategy_factory: ProcessingStrategyFactory[TStrategyPayload],
        output_directory: str,
    ) -> None:
        self.__strategy_factory = strategy_factory
        self.__output_directory = Path(output_directory)
        assert self.__output_directory.exists() and self.__output_directory.is_dir()

    def create_with_partitions(
        self,
        commit: Commit,
        partitions: Mapping[Partition, int],
    ) -> ProcessingStrategy[TStrategyPayload]:
        profiler = Profile()
        profiler.enable()
        return ProcessingStrategyProfilerWrapper(
            self.__strategy_factory.create_with_partitions(commit, partitions),
            profiler,
            str(self.__output_directory / f"{int(time.time() * 1000)}.prof"),
        )

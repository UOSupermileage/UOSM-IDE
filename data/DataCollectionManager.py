from threading import Thread
from time import sleep
from typing import Protocol
from uuid import UUID
from data.DataCollector import DataCollector
from drivers.SerialDriver import SerialDriver


class CollectorManager(Protocol):
    def RegisterCollector(self, t: type[DataCollector], *args, **kwargs) -> UUID:
        """Register a collector"""

    def UnregisterCollector(self, id: UUID) -> bool:
        """Unregister a collector"""


class DataCollectionManager:
    """Manage data collectors and orchestrate data collection"""

    serialDriver: SerialDriver = SerialDriver()
    collectors: list[DataCollector] = []
    frequency: float = 0.1

    thread: Thread = None

    def RegisterCollector(self, t: type[DataCollector], *args, **kwargs) -> UUID:
        collector = t(self.serialDriver, *args, **kwargs)
        self.collectors.append(collector)

        if self.thread is None:
            self.thread = Thread(target=self.__ProcessCollectors)
            self.thread.start()

    def UnregisterCollector(self, id: UUID) -> bool:
        for collector in [
            collector for collector in self.collector if collector.id == id
        ]:
            self.collectors.remove(collector)

    def __ProcessCollectors(self) -> None:
        while len(self.collectors) > 0:
            for collector in self.collectors:
                collector.UpdateTimeTillCollection(self.frequency)

                if collector.ShouldCollect():
                    collector.CollectData()

            sleep(self.frequency)

        self.thread = None

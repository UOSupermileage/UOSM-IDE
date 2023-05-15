from abc import ABC
from dataclasses import dataclass
import time

from components.DataSources import DataSource, ObservableData
import random

import threading


class DataCollector(ABC):
    def __init__(self, dataSource: DataSource, type: ObservableData) -> None:
        self.dataSource = dataSource
        self.type = type

    def Collect(self) -> None:
        pass


class MockValueDataCollector(DataCollector):
    def __init__(
        self, dataSource: DataSource, type: ObservableData, min=-2000, max=2000
    ) -> None:
        super().__init__(dataSource, type)

        self.min = min
        self.max = max

    def Collect(self) -> None:
        self.dataSource.ReceiveData(self.type, random.randrange(self.min, self.max, 1))


@dataclass
class DataCollectorManagerItem:
    collector: DataCollector
    frequency: float
    recuring: bool
    timeUntilExecution: float = 0


class DataCollectorManager:
    collectorItems: list[DataCollectorManagerItem] = []
    frequency: float = 0.5

    def __init__(self) -> None:
        x = threading.Thread(target=self.Loop)
        x.start()

    def Register(
        self, collector: DataCollector, frequency: float = 1, recuring: bool = True
    ):
        print("Adding collector")
        for i in range(len(self.collectorItems)):
            if self.collectorItems[i].collector == collector:
                self.collectorItems[i] = DataCollectorManagerItem(
                    collector, frequency, recuring
                )
                return

        self.collectorItems.append(
            DataCollectorManagerItem(collector, frequency, recuring)
        )

    def Loop(self, *args, **kwargs) -> None:
        """Current implementation can be affected by a long .Collect() function."""
        while True:
            print(
                f"Looping through collectors. There are {len(self.collectorItems)} of them."
            )

            for item in self.collectorItems:
                if item.timeUntilExecution <= 0:
                    item.collector.Collect()
                    item.timeUntilExecution = item.frequency
                else:
                    item.timeUntilExecution -= self.frequency

            time.sleep(self.frequency)

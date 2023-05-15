from enum import Enum
from typing import Protocol


class ObservableData(Enum):
    ACTUAL_TORQUE = 1
    TARGET_TORQUE = 2
    ACTUAL_VELOCITY = 3
    TARGET_VELOCITY = 4
    ACTUAL_POSITION = 5
    TARGET_POSITION = 6


class DataObserver(Protocol):
    def OnReceiveData(data: list) -> None:
        pass


class DataObservable(Protocol):
    def Register(self, key: ObservableData, observer: DataObserver) -> None:
        pass


class DataSource:
    observers: dict[ObservableData, list[DataObserver]]

    def __init__(self) -> None:
        self.observers = []

    def RegisterForData(self, key: ObservableData, observer: DataObserver) -> None:
        if observer not in self.observers[key]:
            self.observers[key].append(observer)

from enum import Enum
from typing import Protocol


class StorageCategory(Enum):
    LIST = (1,)
    VALUE = 2


class ObservableData(Enum):
    ACTUAL_TORQUE = 1
    TARGET_TORQUE = 2
    ACTUAL_VELOCITY = 3
    TARGET_VELOCITY = 4
    ACTUAL_POSITION = 5
    TARGET_POSITION = 6

    def GetStorageCategory(self) -> StorageCategory:
        match self:
            case self.ACTUAL_TORQUE | self.ACTUAL_VELOCITY | self.ACTUAL_POSITION | self.TARGET_TORQUE | self.TARGET_VELOCITY | self.TARGET_POSITION:
                return StorageCategory.LIST


class DataObserver(Protocol):
    def OnReceiveData(data: any) -> None:
        pass


class DataObservable(Protocol):
    def Register(self, key: ObservableData, observer: DataObserver) -> None:
        pass

    def ReceiveData(self, key: ObservableData, data: any) -> None:
        pass


class DataSource:
    """Holds data for the IDE. It is the source of truth for the application."""

    maxDataLength: int = 1000
    cache: dict[ObservableData, list[any]]
    observers: dict[ObservableData, list[DataObserver]]

    def __init__(self) -> None:
        self.cache = {}
        self.observers = {}

    def Register(self, key: ObservableData, observer: DataObserver) -> None:
        if observer not in self.observers[key]:
            self.observers[key].append(observer)

    def ReceiveData(self, key: ObservableData, data: any) -> None:
        match key.GetStorageCategory():
            case StorageCategory.LIST:
                if key not in self.cache.keys():
                    self.cache[key] = []

                if len(self.cache[key]) > self.maxDataLength:
                    self.cache[key].pop(0)

                self.cache[key].append(data)
            case StorageCategory.VALUE:
                self.cache[key] = data

        if key in self.observers.keys():
            for observer in self.observers[key]:
                observer.OnReceiveData(self.cache[key])

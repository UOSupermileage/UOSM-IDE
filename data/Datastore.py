from abc import ABC, abstractmethod
from typing import Optional, Protocol, Union
from uuid import UUID
from data.Data import DataKey, DataPoint, DataPointCache
from data.DataCollectionManager import DataCollectionManager
from data.DataCollector import SerialDataCollector


class DataObserver(Protocol):
    def OnDataChanged(key: DataKey) -> None:
        """Called whenever data for key changes"""


class DataObservable(Protocol):
    def NotifyObservers(self, key: DataKey) -> None:
        """Notify Observers"""

    def RegisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        """Register Observer"""

    def UnregisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        """Unregister Observer"""


class DataContainer(Protocol):
    def GetDataValue(key: DataKey) -> Optional[DataPoint]:
        """Get a single data point from storage"""

    def GetDataList(key: DataKey, size: int = 0) -> list[DataKey]:
        """Get multiple data points from storage"""


class Datastore(ABC):
    """Source of truth for the application"""

    @abstractmethod
    def ReceiveData(self, point: DataPoint) -> None:
        """Set data in the store"""

    @abstractmethod
    def GetDataValue(self, key: DataKey) -> Optional[DataPoint]:
        """Get single value from the store"""

    @abstractmethod
    def GetDataList(self, key: DataKey, size: int = 0):
        """Get list from the store"""

    @abstractmethod
    def GetDataState(self, key: DataKey) -> Optional[UUID]:
        """Get state from the store"""

    @abstractmethod
    def NotifyObservers(self, key: DataKey) -> None:
        """Notify observers of change"""

    @abstractmethod
    def RegisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        """Register a new observer"""

    @abstractmethod
    def RegisterObserverWithKeys(
        self, keys: list[DataKey], observer: DataObserver
    ) -> None:
        """Register a new observer"""

    @abstractmethod
    def UnregisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        """Unregister an observer"""


class AppDatastore(Datastore):
    """Source of truth for the application"""

    collectionManager: DataCollectionManager = DataCollectionManager()
    data: dict[DataKey, DataPointCache] = {}
    observers: dict[DataKey, list[DataObserver]] = {}

    def __init__(self) -> None:
        for key in DataKey:
            self.data[key] = DataPointCache(key.GetDefaultCacheSize())

        self.collectionManager.RegisterCollector(
            SerialDataCollector, recipient=self, keys=[DataKey.TorqueP]
        )

    def ReceiveData(self, point: DataPoint) -> None:
        self.data[point.key].Append(point)
        self.NotifyObservers(point.key)

    def GetDataValue(self, key: DataKey) -> Optional[DataPoint]:
        if key in self.data.keys():
            return self.data[key].GetLatest()

        return None

    def GetDataList(self, key: DataKey, size: int = 0):
        if key in self.data.keys():
            return self.data[key].Get(size)

        return None

    def GetDataState(self, key: DataKey) -> Optional[UUID]:
        if key in self.data.keys():
            return self.data[key].GetState()

        return None

    def NotifyObservers(self, key: DataKey) -> None:
        if key not in self.observers.keys():
            return

        for observer in self.observers[key]:
            observer.OnDataChanged(key)

    def RegisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        if key not in self.observers.keys():
            self.observers[key] = []

        if observer in self.observers[key]:
            return

        self.observers[key].append(observer)

    def RegisterObserverWithKeys(
        self, keys: list[DataKey], observer: DataObserver
    ) -> None:
        for key in keys:
            self.RegisterObserver(key, observer)

    def UnregisterObserver(self, key: DataKey, observer: DataObserver) -> None:
        if key not in self.observers.keys():
            return

        if observer in self.observers[key]:
            self.observers[key].remove(observer)

        if len(self.observers[key]) == 0:
            self.observers.pop(key)

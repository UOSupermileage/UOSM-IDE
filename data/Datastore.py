from typing import Protocol
from data.Data import DataKey, DataPoint, DataPointCache
from data.DataCollectionManager import DataCollectionManager


class DataRecipient(Protocol):
    """Represents a class that can receive data"""

    def ReceiveData(point: DataPoint):
        pass


class Datastore:
    """Source of truth for the application"""

    collectionManager: DataCollectionManager = DataCollectionManager()
    data: dict[DataKey, DataPointCache] = {}

    def __init__(self) -> None:
        for key in DataKey:
            self.data[key] = DataPointCache(key.GetDefaultCacheSize())

    def ReceiveData(self, point: DataPoint) -> None:
        self.data[point.key].append(point)

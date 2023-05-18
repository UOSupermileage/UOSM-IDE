from data.DataCollector import DataCollector
from drivers.SerialDriver import SerialDriver


class DataCollectionManager:
    """Manage data collectors and orchestrate data collection"""

    serialDriver: SerialDriver = SerialDriver()

    def CreateCollector(self) -> DataCollector:
        return DataCollector()

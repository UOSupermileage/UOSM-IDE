from abc import ABC
from uuid import UUID, uuid4
from data.Data import DataKey, DataPoint
from data.DataRecipient import DataRecipient

from drivers.SerialDriver import SerialDriver

DEFAULT_FREQUENCY = 0.5
DEFAULT_SHOULD_LOOP = True


class DataCollector(ABC):
    """Collect data"""

    id: UUID
    frequency: float
    timeTillCollection: float = 0
    loop: bool
    recipient: DataRecipient

    def __init__(
        self,
        recipient: DataRecipient,
        frequency: float = DEFAULT_FREQUENCY,
        loop: bool = DEFAULT_SHOULD_LOOP,
        id: UUID = uuid4(),
    ) -> None:
        super().__init__()

        self.recipient = recipient
        self.frequency = frequency
        self.loop = loop
        self.id = id

    def CollectData(self) -> None:
        """Trigger data collection in colelctor"""
        self.timeTillCollection = self.frequency

    def ShouldCollect(self) -> bool:
        return self.timeTillCollection <= 0

    def UpdateTimeTillCollection(self, delta: float):
        self.timeTillCollection -= delta


class SerialDataCollector(DataCollector):
    # How often to collect data

    driver: SerialDriver
    keys: list[DataKey]

    def __init__(
        self,
        driver: SerialDriver,
        recipient: DataRecipient,
        keys: list[DataKey],
        frequency: float = DEFAULT_FREQUENCY,
        loop=DEFAULT_SHOULD_LOOP,
        *args,
        **kwargs
    ) -> None:
        super().__init__(recipient, frequency, loop)
        self.driver = driver
        self.keys = keys

    def CollectData(self) -> None:
        super().CollectData()
        self.driver.EnqueueReadRequest(self.keys, self.recipient)

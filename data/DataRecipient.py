from typing import Protocol

from data.Data import DataPoint


class DataRecipient(Protocol):
    """Represents a class that can receive data"""

    def ReceiveData(point: DataPoint):
        pass

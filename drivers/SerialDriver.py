from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from queue import PriorityQueue
from threading import Thread
from typing import Callable, Protocol

from data.Data import DataKey, DataPoint
from data.DataRecipient import DataRecipient


class RequestPriority(Enum):
    """Lower priority number means it's a higher priority"""

    Action = 0
    Write = 1
    Read = 2


@dataclass
class SerialDriverResponse:
    pass


@dataclass
class SerialDriverReadResponse(SerialDriverResponse):
    data: list[DataPoint] = field(default_factory=list)


@dataclass(order=True)
class SerialDriverRequest:
    priority: RequestPriority = field(compare=True)
    command: str = field(compare=False)
    onCollection: Callable[[SerialDriverResponse, DataRecipient], None] = field(
        compare=False
    )


class Driver(ABC):
    def EnqueueReadRequest(self, keys: list[DataKey], recipient: DataRecipient) -> None:
        """Read keys and give data to recipient"""


class SerialDriver(Driver):
    """Interface with serial devices"""

    queue: PriorityQueue[SerialDriverRequest]
    thread: Thread = None

    def __init__(self, queueSize=0) -> None:
        self.queue = PriorityQueue(queueSize)

    def EnqueueReadRequest(self, keys: list[DataKey], recipient: DataRecipient) -> None:
        self.EnqueueRequest(
            RequestPriority.Read,
            self.CreateReadCommand(keys),
            lambda response, r=recipient: [
                r.ReceiveData(point) for point in response.data
            ],
        )

    def EnqueueRequest(
        self,
        priority: RequestPriority,
        command: str,
        onCollection: Callable[[SerialDriverResponse], None],
    ) -> None:
        self.queue.put(SerialDriverRequest(priority, command, onCollection))

        if self.thread is None:
            self.thread = Thread(target=self.__ProcessQueue)
            self.thread.start()

    def __ProcessQueue(self, *args, **kwargs) -> None:
        while self.queue.not_empty:
            request = self.queue.get()
            self.ProcessRequest(request)

        self.thread = None

    def ProcessRequest(self, request: SerialDriverRequest):
        request.onCollection(
            SerialDriverReadResponse([DataPoint(DataKey.TorqueP, datetime.now(), 10)])
        )

    def CreateReadCommand(self, keys: list[DataKey]) -> str:
        return NotImplementedError()

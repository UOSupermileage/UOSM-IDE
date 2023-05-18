from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from threading import Thread

from data.Data import DataPoint


class RequestPriority(Enum):
    """Lower priority number means it's a higher priority"""

    Action = 0
    Write = 1
    Read = 2


@dataclass
class SerialDriverResponse:
    pass


@dataclass(order=True)
class SerialDriverRequest:
    priority: RequestPriority = field(compare=True)
    command: str = field(compare=False)
    onCollection: callable[[SerialDriverResponse], None] = field(compare=False)


class SerialDriver:
    """Interface with serial devices"""

    queue: PriorityQueue[SerialDriverRequest]
    thread: Thread

    def __init__(self, queueSize=0) -> None:
        self.queue = PriorityQueue(queueSize)

    def EnqueueRequest(
        self,
        priority: RequestPriority,
        command: str,
        onCollection: callable[[SerialDriverResponse], None],
    ) -> None:
        self.queue.put(SerialDriverRequest(priority, command, onCollection))

        if self.thread is None:
            self.thread = Thread(target=self.ProcessQueue)
            self.thread.start()

    def ProcessQueue(self, *args, **kwargs) -> None:
        while self.queue.not_empty:
            request = self.queue.get()
            self.ProcessRequest(request)

        self.thread = None

    def ProcessRequest(self, request: SerialDriverRequest):
        request.onCollection(SerialDriverResponse())

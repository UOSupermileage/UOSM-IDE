from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional
from uuid import UUID, uuid4

DEFAULT_CACHE_SIZE = 1


class DataKey(Enum):
    MotorMode = auto()  # Motor Mode defines if motor is idle, rtmi, standalone
    TorqueP = auto()
    TorqueI = auto()
    VelocityP = auto()
    VelocityI = auto()
    PositionP = auto()
    PositionI = auto()
    MaxCurrent = auto()  # Max current that the motor can draw
    MaxTorque = auto()  # Max Torque for throttle when driving in torque mode
    MaxVelocity = auto()  # Max Velocity for throttle when driving in velocity mode
    MaxAcceleration = auto()  # Max Acceleration when driving in velocity mode

    def GetDefaultCacheSize(self) -> int:
        match self:
            case default:
                return DEFAULT_CACHE_SIZE


@dataclass
class DataPoint:
    key: DataKey
    value: int
    timestamp: datetime = datetime.now()


class DataPointCache:
    data: list[DataPoint] = []
    state: UUID = uuid4()

    maxLength: int

    def __init__(self, maxLength: int) -> None:
        self.maxLength = maxLength

    def Append(self, point: DataPoint) -> None:
        self.data.append(point)

        if len(self.data) > self.maxLength:
            self.data.pop(0)

        self.__UpdateState()

    def GetLatest(self) -> Optional[DataPoint]:
        length = len(self.data)

        if length > 0:
            return self.data[length - 1]

        return None

    def Get(self, size: int = 0) -> list[DataPoint]:
        if size <= 0 or size >= len(self.data):
            return self.data

        # Return ending slice of the data
        return self.data[len(self.data) - size :]

    def __UpdateState(self):
        self.state = uuid4()

    def GetState(self) -> UUID:
        return self.state

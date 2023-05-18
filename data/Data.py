from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

DEFAULT_CACHE_SIZE = 1000


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
        return DEFAULT_CACHE_SIZE


@dataclass
class DataPoint:
    key: DataKey
    timestamp: datetime
    value: int


class DataPointCache:
    data: list[DataPoint]
    maxLength: int

    def __init__(self, maxLength: int) -> None:
        self.maxLength = maxLength

    def append(self, point: DataPoint) -> None:
        self.data.append(point)

        if len(self.data) > self.maxLength:
            self.data.pop(0)

from enum import IntEnum, auto
from dataclasses import dataclass


class Phase(IntEnum):
    STANDBY = auto()
    PRESSURIZATION = auto()
    COUNTDOWN = auto()
    ENGINE_STARTUP = auto()
    ENGINE_FIRING = auto()
    ENGINE_SHUTDOWN = auto()
    FUEL_TANK_VENT = auto()
    ENGINE_RAPID_SHUTDOWN = auto()
    POSTBURN = auto()
    TESTING = auto()
    LOG_DOWNLINK = auto()

    def in_mission(self) -> bool:
        return self not in [Phase.STANDBY, Phase.TESTING, Phase.LOG_DOWNLINK]


@dataclass
class SystemState:
    class Clock:
        mission_time: float = 0
        time: float = 0

    phase: Phase = Phase.STANDBY
    clock: Clock = Clock()

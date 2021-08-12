from enum import IntEnum, auto
from dataclasses import dataclass
import time
from modules.mcl.config import Config


class State(IntEnum):
    STANDBY = auto()
    PRESSURIZATION = auto()
    COUNTDOWN = auto()
    ENGINE_STARTUP = auto()
    ENGINE_FIRING = auto()
    ENGINE_SHUTDOWN = auto()
    FUEL_TANK_VENT = auto()
    ENGINE_RAPID_SHUTDOWN = auto()
    ENGINE_VENT = auto()


class Clock:
    '''class to handle the mission clock'''

    def __init__(self):
        self._mission_tzero = None  # stays None until start() called
        self._countdown = Config.autosequence.COUNTDOWN_DURATION

    @property
    def time(self):
        return time.time()

    @property
    def mission_time(self):
        '''returns -(countdown) if mission clock not started yet'''
        if self.mission_tzero is None:
            return -self._countdown
        else:
            return self.time - self._mission_tzero

    def start_mission_clock(self):
        '''sets the mission's t=0 point to a countdown length ahead of now'''
        self.mission_tzero = self.time + self._countdown


class SystemState:
    def __init__(self):
        self.clock = Clock()
        self.state = State.STANDBY

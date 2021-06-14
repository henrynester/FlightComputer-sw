from abc import ABC, abstractmethod
from modules.mcl.system_state import SystemState


class Task(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def initialize(self, state):
        pass

    @abstractmethod
    def sense(self, state: SystemState):
        pass

    @abstractmethod
    def control(self, state: SystemState):
        pass

    @abstractmethod
    def actuate(self, state: SystemState):
        pass

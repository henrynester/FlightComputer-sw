from modules.mcl.system_state import SystemState


class Task:
    def __init__(self, name: str):
        self.name = name

    def initialize(self, state):
        pass

    def sense(self, state: SystemState):
        pass

    def control(self, state: SystemState):
        pass

    def actuate(self, state: SystemState):
        pass

    def deinitialize(self):
        pass

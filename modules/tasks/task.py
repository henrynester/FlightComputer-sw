from modules.mcl.system_state import SystemState


class Task:
    def __init__(self, name: str, state: SystemState):
        self.name = name
        self.state = state

    def sense(self):
        pass

    def control(self):
        pass

    def actuate(self):
        pass

    def deinitialize(self):
        pass

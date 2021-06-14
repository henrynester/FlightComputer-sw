from modules.mcl.system_state import SystemState, Phase
from modules.mcl.config import Config
from modules.tasks.task import Task

import time


class PhaseTask(Task):
    def __init__(self):
        self.vent_start_time: float
        self.time_mission_tzero: float
        super().__init__('Phase')

    def initialize(self, state: SystemState):
        state.phase = Phase.STANDBY

    def sense(self, state):
        pass

    def actuate(self, state):
        pass

    def control(self, state: SystemState):
        # first, update the various clocks on the computer:
        # mission_time: time delta between now and t=0 ignition
        # time: epoch time of Pi (seconds since 1970).
        #       syncs over network, lost with power cycle
        # may have issues from clock jumping around due to network sync
        # if this happens during a burn, interesting things could happen
        state.clock.time = time.time()
        if not state.phase.in_mission():
            # when we're not in the countdown or burn, keep the mission
            # t=0 point ahead of now by the countdown length
            self.time_mission_tzero = state.clock.time + 10
        # mission_time is the delta between now and the t=0 point for the
        # mission, when the ignitor lights
        state.clock.mission_time = state.clock.time - self.time_mission_tzero

        if state.phase not in [
                Phase.ENGINE_SHUTDOWN, Phase.ENGINE_RAPID_SHUTDOWN,
                Phase.FUEL_TANK_VENT
        ]:
            self.vent_start_time = state.clock.time

        # transition to the next phase in the autosequence
        # if the time for this one has elapsed
        if state.phase == Phase.COUNTDOWN and state.clock.mission_time > 0:
            state.phase = Phase.ENGINE_STARTUP

        elif state.phase == Phase.ENGINE_STARTUP and \
                state.clock.mission_time > Config.autosequence.BURN_START_TIME:
            state.phase = Phase.ENGINE_FIRING

        elif state.phase == Phase.ENGINE_FIRING and \
                state.clock.mission_time > \
                Config.autosequence.SHUTDOWN_START_TIME:
            state.phase = Phase.ENGINE_SHUTDOWN

        elif (state.phase == Phase.ENGINE_RAPID_SHUTDOWN or
                state.phase == Phase.ENGINE_SHUTDOWN) and \
                (state.clock.time - self.vent_start_time) > \
                Config.autosequence.ENGINE_VENT_DURATION:
            state.phase = Phase.POSTBURN

        elif state.phase == Phase.FUEL_TANK_VENT and \
                state.clock.time - self.vent_start_time > \
                Config.autosequence.FUEL_TANK_VENT_DURATION:
            state.phase = Phase.STANDBY

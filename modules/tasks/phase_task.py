from modules.mcl.system_state import SystemState, Phase
from modules.mcl.config import Config
from modules.tasks.task import Task

import time


class PhaseTask(Task):
    def __init__(self, state: SystemState):
        self.vent_start_time: float
        self.time_mission_tzero: float
        state.phase = Phase.STANDBY
        super().__init__("Phase", state)

    def control(self):
        # first, update the various clocks on the computer:
        # mission_time: time delta between now and t=0 ignition
        # time: epoch time of Pi (seconds since 1970).
        #       syncs over network, lost with power cycle
        # may have issues from clock jumping around due to network sync
        # if this happens during a burn, interesting things could happen
        self.state.clock.time = time.time()
        if not self.state.phase.in_mission():
            # when we're not in the countdown or burn, keep the mission
            # t=0 point ahead of now by the countdown length
            self.time_mission_tzero = self.state.clock.time + 10
        # mission_time is the delta between now and the t=0 point for the
        # mission, when the ignitor lights
        self.state.clock.mission_time = \
            self.state.clock.time - self.time_mission_tzero

        if self.state.phase not in [
            Phase.ENGINE_SHUTDOWN,
            Phase.ENGINE_RAPID_SHUTDOWN,
            Phase.FUEL_TANK_VENT,
        ]:
            self.vent_start_time = self.state.clock.time

        # transition to the next phase in the autosequence
        # if the time for this one has elapsed
        if self.state.phase == Phase.COUNTDOWN and \
                self.state.clock.mission_time > 0:
            self.state.phase = Phase.ENGINE_STARTUP

        elif (
            self.state.phase == Phase.ENGINE_STARTUP
            and self.state.clock.mission_time >
                Config.autosequence.BURN_START_TIME
        ):
            self.state.phase = Phase.ENGINE_FIRING

        elif (
            self.state.phase == Phase.ENGINE_FIRING
            and self.state.clock.mission_time >
                Config.autosequence.SHUTDOWN_START_TIME
        ):
            self.state.phase = Phase.ENGINE_SHUTDOWN

        elif (
            self.state.phase == Phase.ENGINE_RAPID_SHUTDOWN
            or self.state.phase == Phase.ENGINE_SHUTDOWN
        ) and (
            self.state.clock.time - self.vent_start_time
        ) > Config.autosequence.ENGINE_VENT_DURATION:
            self.state.phase = Phase.POSTBURN

        elif (
            self.state.phase == Phase.FUEL_TANK_VENT
            and self.state.clock.time - self.vent_start_time
            > Config.autosequence.FUEL_TANK_VENT_DURATION
        ):
            self.state.phase = Phase.STANDBY

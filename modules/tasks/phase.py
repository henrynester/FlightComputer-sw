from modules.mcl.system_state import SystemState, State
from modules.mcl.config import Config
from modules.tasks.task import Task

import time

import transitions
import logging

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
logging.getLogger('transitions').setLevel(logging.INFO)


class StateMachineTask(Task):
    def __init__(self, state: SystemState):
        self.vent_start_time = 0

        self.clock = Clock()

        # finite state machine controls propulsion state
        # possible fsm transitions (trigger, source, dest)
        state_transitions = [  # oops
            # normal sequence of transitions for an engine fire
            {'trigger': 'manual_proceed',
             'source': State.STANDBY,
             'dest': State.PRESSURIZATION},
            {'trigger': 'manual_proceed',
             'source': State.STANDBY,
             'dest': State.COUNTDOWN},
            {'trigger': 'auto_proceed',
             'source': State.COUNTDOWN,
             'dest': State.ENGINE_STARTUP,
             'conditions': [lambda: self.clock.mt > 0]},
            {'trigger': 'auto_proceed',
             'source': State.ENGINE_STARTUP,
             'dest': State.ENGINE_FIRING,
             'conditions': [lambda: self.clock.mt > Config.autosequence.BURN_START_TIME]},
            {'trigger': 'auto_proceed',
             'source': State.ENGINE_FIRING,
             'dest': State.ENGINE_SHUTDOWN,
             'conditions': [lambda: self.clock.mt > Config.autosequence.SHUTDOWN_START_TIME]},
            {'trigger': 'auto_proceed',
             'source': State.ENGINE_SHUTDOWN,
             'dest': State.ENGINE_VENT,
             'conditions': []},
            {'trigger': 'auto_proceed',
                'source': State.ENGINE_VENT,
                'dest': State.FUEL_TANK_VENT,
                'conditions': [lambda: self.clock.t - self.vent_start_time >
                               Config.autosequence.ENGINE_VENT_DURATION,
                               self.check_engine_depressurized]},
            {'trigger': 'auto_proceed',
                'source': State.FUEL_TANK_VENT,
                'dest': State.STANDBY,
                'conditions': [lambda: self.clock.t - self.vent_start_time >
                               Config.autosequence.FUEL_TANK_VENT_DURATION,
                               self.check_fuel_tank_depressurized]},
            # "unusual" transitions (aborts, etc.)
            # issuing a manual proceed during burn initiates the soft shutdown early
            {'trigger': 'manual_proceed',
             'source': State.ENGINE_FIRING,
             'dest': State.ENGINE_SHUTDOWN},
            # abort once engine has lit causes a hard shutdown
            {'trigger': 'abort',
             'source': [State.ENGINE_STARTUP, State.ENGINE_FIRING, State.ENGINE_SHUTDOWN],
             'dest': State.ENGINE_RAPID_SHUTDOWN},
            # ...which leads to an engine vent, then a fuel tank vent, and finally back to standby
            {'trigger': 'auto_proceed',
                'source': State.ENGINE_RAPID_SHUTDOWN,
                'dest': State.ENGINE_VENT},
            # abort during countdown returns to pressurization
            {'trigger': 'abort', 'source': State.COUNTDOWN,
                'dest': State.PRESSURIZATION},
            # abort during pressurization returns vents the fuel tank, then returns to standby
            {'trigger': 'abort', 'source': State.PRESSURIZATION,
                'dest': State.FUEL_TANK_VENT}
        ]

        self.fsm = transitions.Machine(model=self, states=State, transitions=state_transitions,
                                       initial=State.STANDBY)

        self.to_COUNTDOWN()

        # state.state = State.STANDBY
        super().__init__("StateMachine", state)

    def on_enter_COUNTDOWN(self):
        self.clock.start_mt()

    def is_countdown_complete(self):
        return self.clock.mt >= 0

    def is_startup_complete(self):
        pass

    def check_engine_depressurized(self):
        return True

    def check_fuel_tank_depressurized(self):
        return True

    def control(self):
        # self.update_clocks()
        # if 'auto_proceed' in self.fsm.get_triggers(self.state):
        #     self.auto_proceed()

        if 'auto_proceed' in self.fsm.get_triggers(self.state):
            self.auto_proceed()

        # if self._state.phase not in [
        #     State.ENGINE_SHUTDOWN,
        #     State.ENGINE_RAPID_SHUTDOWN,
        #     State.FUEL_TANK_VENT,
        # ]:
        #     self.vent_start_time = self._state.clock.time

        # # transition to the next phase in the autosequence
        # # if the time for this one has elapsed
        # if self._state.phase == State.COUNTDOWN and \
        #         self._state.clock.mission_time > 0:
        #     self._state.phase = State.ENGINE_STARTUP

        # elif (
        #     self._state.phase == State.ENGINE_STARTUP
        #     and self._state.clock.mission_time >
        #         Config.autosequence.BURN_START_TIME
        # ):
        #     self._state.phase = State.ENGINE_FIRING

        # elif (
        #     self._state.phase == State.ENGINE_FIRING
        #     and self._state.clock.mission_time >
        #         Config.autosequence.SHUTDOWN_START_TIME
        # ):
        #     self._state.phase = State.ENGINE_SHUTDOWN

        # elif (
        #     self._state.phase == State.ENGINE_RAPID_SHUTDOWN
        #     or self._state.phase == State.ENGINE_SHUTDOWN
        # ) and (
        #     self._state.clock.time - self.vent_start_time
        # ) > Config.autosequence.ENGINE_VENT_DURATION:
        #     self._state.phase = State.POSTBURN

        # elif (
        #     self._state.phase == State.FUEL_TANK_VENT
        #     and self._state.clock.time - self.vent_start_time
        #     > Config.autosequence.FUEL_TANK_VENT_DURATION
        # ):
        #     self._state.phase = State.STANDBY


class Clock:
    '''class to handle the mission clock'''

    def __init__(self):
        self._mt_zero = None  # stays None until start() called
        self._countdown = Config.autosequence.COUNTDOWN_DURATION

    @ property
    def t(self):
        return time.time()

    @ property
    def mt(self):
        '''mission time: returns -(countdown) if mission clock not started yet'''
        if self._mt_zero is None:
            return -self._countdown
        else:
            return self.t - self._mt_zero

    def start_mt(self):
        '''sets the mission's t=0 point to a countdown length ahead of now'''
        self._mt_zero = self.t + self._countdown

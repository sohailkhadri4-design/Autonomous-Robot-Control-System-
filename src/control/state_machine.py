from enum import Enum


class RobotState(Enum):
    """Five supported robot motion/control states."""

    IDLE = "idle"
    FORWARD = "forward"
    REVERSE = "reverse"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"


class RobotStateMachine:
    """Small deterministic state machine for robot motion commands."""

    def __init__(self) -> None:
        self._state = RobotState.IDLE

    @property
    def state(self) -> RobotState:
        return self._state

    def set_state(self, state: RobotState) -> RobotState:
        if not isinstance(state, RobotState):
            raise ValueError("state must be a RobotState")
        self._state = state
        return self._state

    def reset(self) -> RobotState:
        self._state = RobotState.IDLE
        return self._state

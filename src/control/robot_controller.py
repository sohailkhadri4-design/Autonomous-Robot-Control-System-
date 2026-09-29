from src.control.state_machine import RobotState, RobotStateMachine
from src.motors.motor_controller import MotorController


class RobotController:
    """Coordinates high-level states with low-level motor commands."""
    def __init__(self, motors: MotorController) -> None:
        self.motors = motors
        self.state_machine = RobotStateMachine()
        self.motors.stop()

    @property
    def state(self) -> RobotState:
        return self.state_machine.state

    def set_state(self, state: RobotState, speed: float = 50) -> RobotState:
        self.state_machine.set_state(state)
        if state is RobotState.IDLE:
            self.motors.stop()
        elif state is RobotState.FORWARD:
            self.motors.forward(speed)
        elif state is RobotState.REVERSE:
            self.motors.reverse(speed)
        elif state is RobotState.TURN_LEFT:
            self.motors.turn_left(speed)
        elif state is RobotState.TURN_RIGHT:
            self.motors.turn_right(speed)
        return self.state

    def stop(self) -> RobotState:
        return self.set_state(RobotState.IDLE)

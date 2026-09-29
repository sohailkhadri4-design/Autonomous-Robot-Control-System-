from src.control.robot_controller import RobotController
from src.control.state_machine import RobotState
from src.gpio.gpio_interface import SimulatedGPIO
from src.motors.motor_controller import MotorController, MotorPins


def test_controller_drives_all_operating_states():
    gpio = SimulatedGPIO()
    motors = MotorController(gpio, MotorPins(5, 6, 12, 20, 21, 13))
    robot = RobotController(motors)
    for state in RobotState:
        assert robot.set_state(state) is state
    robot.stop()
    assert robot.state is RobotState.IDLE

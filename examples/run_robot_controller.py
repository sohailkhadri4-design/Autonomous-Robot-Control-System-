from src.control.robot_controller import RobotController
from src.control.state_machine import RobotState
from src.gpio.gpio_interface import SimulatedGPIO
from src.motors.motor_controller import MotorController, MotorPins


def main() -> None:
    gpio = SimulatedGPIO()
    pins = MotorPins(5, 6, 12, 20, 21, 13)
    robot = RobotController(MotorController(gpio, pins))
    for state in RobotState:
        robot.set_state(state)
        print(f"State: {state.value}")
    robot.stop()
    print("Returned to idle state.")


if __name__ == "__main__":
    main()

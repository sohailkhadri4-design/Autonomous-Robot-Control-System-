from src.gpio.gpio_interface import SimulatedGPIO
from src.motors.motor_controller import MotorController, MotorPins


def controller():
    gpio = SimulatedGPIO()
    return gpio, MotorController(gpio, MotorPins(5, 6, 12, 20, 21, 13))


def test_forward_sets_both_motors_forward():
    gpio, motors = controller()
    motors.forward(60)
    assert gpio.pin_values[5] == 1 and gpio.pin_values[6] == 0
    assert gpio.pin_values[20] == 1 and gpio.pin_values[21] == 0
    assert gpio.pwm_channels[12].duty_cycle == 60
    assert gpio.pwm_channels[13].duty_cycle == 60


def test_reverse_sets_both_motors_reverse():
    gpio, motors = controller()
    motors.reverse(40)
    assert gpio.pin_values[5] == 0 and gpio.pin_values[6] == 1
    assert gpio.pin_values[20] == 0 and gpio.pin_values[21] == 1


def test_stop_removes_motor_drive():
    gpio, motors = controller()
    motors.forward()
    motors.stop()
    assert gpio.pwm_channels[12].duty_cycle == 0
    assert gpio.pwm_channels[13].duty_cycle == 0


def test_invalid_speed_is_rejected():
    _, motors = controller()
    try:
        motors.forward(101)
    except ValueError:
        pass
    else:
        raise AssertionError("speed above 100 should raise ValueError")

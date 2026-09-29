from __future__ import annotations

from dataclasses import dataclass
from src.gpio.gpio_interface import GPIOInterface


@dataclass(frozen=True)
class MotorPins:
    left_in1: int
    left_in2: int
    left_pwm: int
    right_in1: int
    right_in2: int
    right_pwm: int


class MotorController:
    """Dual-motor driver abstraction for a typical H-bridge interface."""
    def __init__(self, gpio: GPIOInterface, pins: MotorPins) -> None:
        self.gpio = gpio
        self.pins = pins
        for pin in (pins.left_in1, pins.left_in2, pins.left_pwm, pins.right_in1, pins.right_in2, pins.right_pwm):
            gpio.setup_output(pin)
        gpio.pwm_start(pins.left_pwm, 0)
        gpio.pwm_start(pins.right_pwm, 0)

    @staticmethod
    def _validate_speed(speed: float) -> float:
        if not 0 <= speed <= 100:
            raise ValueError("speed must be between 0 and 100")
        return float(speed)

    def _set_motor(self, in1: int, in2: int, pwm: int, direction: int, speed: float) -> None:
        speed = self._validate_speed(speed)
        self.gpio.write(in1, 1 if direction > 0 else 0)
        self.gpio.write(in2, 1 if direction < 0 else 0)
        self.gpio.pwm_change_duty_cycle(pwm, speed)

    def drive(self, left_direction: int, right_direction: int, left_speed: float, right_speed: float) -> None:
        self._set_motor(self.pins.left_in1, self.pins.left_in2, self.pins.left_pwm, left_direction, left_speed)
        self._set_motor(self.pins.right_in1, self.pins.right_in2, self.pins.right_pwm, right_direction, right_speed)

    def stop(self) -> None:
        for pin in (self.pins.left_in1, self.pins.left_in2, self.pins.right_in1, self.pins.right_in2):
            self.gpio.write(pin, 0)
        self.gpio.pwm_change_duty_cycle(self.pins.left_pwm, 0)
        self.gpio.pwm_change_duty_cycle(self.pins.right_pwm, 0)

    def forward(self, speed: float = 50) -> None:
        self.drive(1, 1, speed, speed)

    def reverse(self, speed: float = 50) -> None:
        self.drive(-1, -1, speed, speed)

    def turn_left(self, speed: float = 40) -> None:
        self.drive(-1, 1, speed, speed)

    def turn_right(self, speed: float = 40) -> None:
        self.drive(1, -1, speed, speed)

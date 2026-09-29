from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class GPIOInterface(Protocol):
    """Minimal interface required by the motor controller."""
    def setup_output(self, pin: int) -> None: ...
    def write(self, pin: int, value: int) -> None: ...
    def pwm_start(self, pin: int, duty_cycle: float) -> None: ...
    def pwm_change_duty_cycle(self, pin: int, duty_cycle: float) -> None: ...
    def cleanup(self) -> None: ...


@dataclass
class PWMChannel:
    pin: int
    duty_cycle: float = 0.0


class SimulatedGPIO:
    """Deterministic GPIO backend for development and automated tests."""
    def __init__(self) -> None:
        self.pin_values: dict[int, int] = {}
        self.pwm_channels: dict[int, PWMChannel] = {}

    def setup_output(self, pin: int) -> None:
        self.pin_values[pin] = 0

    def write(self, pin: int, value: int) -> None:
        if pin not in self.pin_values:
            self.setup_output(pin)
        self.pin_values[pin] = 1 if value else 0

    def pwm_start(self, pin: int, duty_cycle: float) -> None:
        self.pwm_channels[pin] = PWMChannel(pin, float(duty_cycle))

    def pwm_change_duty_cycle(self, pin: int, duty_cycle: float) -> None:
        if pin not in self.pwm_channels:
            self.pwm_start(pin, duty_cycle)
        else:
            self.pwm_channels[pin].duty_cycle = float(duty_cycle)

    def cleanup(self) -> None:
        self.pin_values.clear()
        self.pwm_channels.clear()


class RaspberryPiGPIO:
    """Optional Raspberry Pi GPIO backend using RPi.GPIO."""
    def __init__(self) -> None:
        try:
            import RPi.GPIO as GPIO
        except ImportError as exc:
            raise RuntimeError("RPi.GPIO is required for physical Raspberry Pi operation.") from exc
        self._gpio = GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def setup_output(self, pin: int) -> None:
        self._gpio.setup(pin, self._gpio.OUT, initial=self._gpio.LOW)

    def write(self, pin: int, value: int) -> None:
        self._gpio.output(pin, self._gpio.HIGH if value else self._gpio.LOW)

    def pwm_start(self, pin: int, duty_cycle: float) -> None:
        pwm = self._gpio.PWM(pin, 1000)
        pwm.start(float(duty_cycle))
        setattr(self, f"_pwm_{pin}", pwm)

    def pwm_change_duty_cycle(self, pin: int, duty_cycle: float) -> None:
        pwm = getattr(self, f"_pwm_{pin}", None)
        if pwm is None:
            self.pwm_start(pin, duty_cycle)
        else:
            pwm.ChangeDutyCycle(float(duty_cycle))

    def cleanup(self) -> None:
        self._gpio.cleanup()

# Autonomous Robot Control System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CI](https://github.com/sohailkhadri4-design/Autonomous-Robot-Control-System-/actions/workflows/tests.yml/badge.svg)](https://github.com/sohailkhadri4-design/Autonomous-Robot-Control-System-/actions/workflows/tests.yml)

A Python-based real-time robot control project using Raspberry Pi GPIO, motor-driver control, and a deterministic five-state motion controller.

## Project Overview

This project demonstrates the software control layer between a Raspberry Pi, GPIO interfaces, a motor driver, and a two-motor robot platform.

The controller implements five operating states:

- **IDLE**: both motors stopped
- **FORWARD**: both motors drive forward
- **REVERSE**: both motors drive in reverse
- **TURN_LEFT**: left motor reverses while the right motor moves forward
- **TURN_RIGHT**: left motor moves forward while the right motor reverses

The design separates high-level state logic from low-level GPIO access so the control software can be developed and tested without requiring a Raspberry Pi in CI.

## Key Features

- Five-state deterministic robot control
- Dual DC motor direction control
- PWM-based motor speed control from 0 to 100%
- Raspberry Pi GPIO adapter using `RPi.GPIO`
- Simulated GPIO backend for development and automated tests
- Safe-stop behavior through the IDLE state
- Unit and integration tests with pytest
- GitHub Actions continuous integration
- System architecture and operating-state documentation

## System Architecture

![System Architecture](docs/system_architecture.svg)

**Control command → State Machine → Robot Controller → Motor Controller → GPIO Interface → Motor Driver → Motors**

See [system architecture](docs/system_architecture.md) for details.

## Repository Structure

```text
Autonomous-Robot-Control-System-/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── .github/workflows/tests.yml
├── src/
│   ├── control/
│   │   ├── robot_controller.py
│   │   └── state_machine.py
│   ├── gpio/gpio_interface.py
│   └── motors/motor_controller.py
├── examples/run_robot_controller.py
├── tests/
│   ├── test_state_machine.py
│   ├── test_motor_control.py
│   └── test_integration.py
└── docs/
    ├── operating_states.md
    ├── system_architecture.md
    └── system_architecture.svg
```

## Setup

Create a virtual environment and install the development dependencies.

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

Linux/Raspberry Pi:

```bash
python -m venv .venv
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## Run the Simulation

The included example uses the simulated GPIO backend, so it does not require physical hardware:

```bash
python examples/run_robot_controller.py
```

## Run Tests

```bash
pytest -q
```

GitHub Actions runs the test suite automatically for pushes and pull requests targeting `main`.

## Raspberry Pi Hardware Integration

The hardware adapter is implemented in `src/gpio/gpio_interface.py` using `RPi.GPIO`.

Before connecting a real robot:

1. Install the Raspberry Pi GPIO library appropriate for your Raspberry Pi OS/Python environment.
2. Select GPIO pins based on your actual motor-driver wiring.
3. Pass those pins through the `MotorPins` configuration.
4. Verify motor-driver logic levels and power wiring against the driver's datasheet.
5. Test with the wheels lifted from the ground before normal operation.

The pin numbers shown in the simulation example are **example values only** and are not presented as your actual hardware wiring.

## Testing Approach

The automated tests cover:

- State initialization and transitions
- All five operating states
- Forward and reverse motor direction logic
- Left and right turning logic
- PWM speed limits
- Stop behavior
- State-to-motor integration

The CI tests use `SimulatedGPIO`, making the software control path deterministic and hardware-independent.

## Project Scope

The repository focuses on the robot control and motor-interface layer. It does not claim autonomous navigation, obstacle avoidance, localization, or sensor-based path planning unless those features are added and documented separately.

This repository contains a reference implementation for the described control architecture. Physical robot validation should be documented with the actual hardware configuration and test results.

## Author

**Syed Sohel Khadri**

Embedded Firmware | STM32 | ARM Cortex-M | Embedded C

GitHub: https://github.com/sohailkhadri4-design

# System Architecture

Control flow:

High-Level Decision/User Command -> RobotController -> RobotStateMachine -> MotorController -> GPIOInterface -> Motor Driver -> DC Motors

GPIOInterface has two backends: SimulatedGPIO for development/CI and RaspberryPiGPIO for optional physical Raspberry Pi integration.

The architecture separates control logic from hardware access, allowing state transitions and motor-control behavior to be tested without a Raspberry Pi or connected motors.

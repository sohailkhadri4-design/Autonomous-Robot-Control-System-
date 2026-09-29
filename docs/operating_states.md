# Operating States

The controller exposes five explicit operating states:

| State | Behavior |
|---|---|
| IDLE | Motors stopped; safe default state |
| FORWARD | Both motors drive forward |
| REVERSE | Both motors drive in reverse |
| TURN_LEFT | Left motor reverses while right motor moves forward |
| TURN_RIGHT | Left motor moves forward while right motor reverses |

The state machine is deterministic and can be driven by a higher-level decision layer such as sensors, commands, or navigation logic.

The example application uses simulated GPIO. Actual motor-driver direction and PWM pins must be mapped to the user's physical Raspberry Pi wiring before hardware operation.

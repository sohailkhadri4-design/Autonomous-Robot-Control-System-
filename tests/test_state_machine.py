from src.control.state_machine import RobotState, RobotStateMachine


def test_initial_state_is_idle():
    assert RobotStateMachine().state is RobotState.IDLE


def test_all_five_states_are_supported():
    machine = RobotStateMachine()
    for state in RobotState:
        assert machine.set_state(state) is state


def test_invalid_state_is_rejected():
    machine = RobotStateMachine()
    try:
        machine.set_state("forward")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid state should raise ValueError")

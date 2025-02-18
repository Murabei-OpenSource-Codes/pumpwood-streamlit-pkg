"""Class to help to manager app states get/set triggers."""
import streamlit as st
import inspect
from typing import Any, Callable, List
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitConfigException, PumpwoodStreamlitStateNotFoundException)
from abc import ABC


class StateTrigger(ABC):
    """Abstract class for setting triggers."""

    _trigger_fun: Callable
    """Function that will be called at action triggered."""

    _change_states: List[str]
    """Informational fields that describe which states will be changed with
       the triggered function."""

    def __init__(self, fun: Callable, change_states: list):
        """__init__.

        Args:
            fun (Callable):
                Callable function that will be ran when trigger is fired.
            change_states (List[str]):
                Informational description of the states that will be updated
                at `fun` function.
        """
        self._trigger_fun = fun
        self._change_states = change_states

    def run(self, **kwargs):
        """Run function associated with trigger passing kwargs."""
        return self._trigger_fun(**kwargs)

    def to_dict(self):
        """Serialize trigger."""
        function_path = inspect.getfile(self._trigger_fun)
        function_name = self._trigger_fun.__name__
        return {
            'trigger_type': type(self).__name__,
            'trigger_fun_path': function_path,
            'trigger_fun_name': function_name,
            'trigger_change_states': self._change_states
        }


class StateBeforeGetTrigger(StateTrigger):
    """Class for setting Before Get triggers at Streamlit states."""


class StateAfterGetTrigger(StateTrigger):
    """Class for setting After Get triggers at Streamlit states."""


class StateBeforeSetTrigger(StateTrigger):
    """Class for setting Before Set triggers at Streamlit states."""


class StateAfterSetTrigger(StateTrigger):
    """Class for setting After Set triggers at Streamlit states."""


class StateManager:
    """Class to help managing streamlit session states.

    StateManager must be deffined at `PUMPWOOD_DASHBOARD__STATEMANAGER` path
    and defaults for `integration.state_manager.StateManager` as an
    uninstanciated class.
    """

    TRIGGERS = {
    }
    """Triggers for get/set state operations at streamlit states.

    It is deffined with state key and a list of triggers associated with it. It
    will be run according to definition order, using StateGetTrigger for
    get operations and StateSetTrigger for set operations.

    Example:
    ```python
    TRIGGERS = {
        'state_variable_1': [
            StateGetTrigger(function=function_get_1),
            StateSetTrigger(function=function_set_1),
            StateGetTrigger(function=function_get_2),
        ]
    }
    ```
    """
    @classmethod
    def does_state_exists(cls, state: str,
                          raise_if_not_found: bool = True) -> bool:
        """Check if state exists at `st.session_state`."""
        if state not in st.session_state:
            if raise_if_not_found:
                msg = (
                    "State [{state}] was not found at Streamlit "
                    "`session_state`. Check if state was initiated.")
                raise PumpwoodStreamlitStateNotFoundException(
                    message=msg, payload={"state": state})
            else:
                return False
        return True

    @classmethod
    def init(cls, state: str, init_value: Any = None,
             force_value: bool = False) -> str:
        """Initiate state using value.

        It will not update state value, unless force_value is set as `True`.
        For setting data use set method instead, this is should be used to
        initiate state variables.

        It will add `pumpwood_st__` to the beggining of the state variable
        to help identify them at states.

        Args:
            state (str):
                Name of the state that will be initiated.
            init_value (Any):
                Value that will be set as initial value for state.
            force_value (bool):
                Default value will not change states that are already present
                at streamlit states. Setting `force_value (bool) = True` will
                reverse this behaivor.
        """
        if (state not in st.session_state) or force_value:
            st.session_state[state] = init_value
        return state

    @classmethod
    def get_state(cls, state: str) -> Any:
        """Get state from Streamlit state."""
        cls.does_state_exists(state=state)
        return st.session_state[state]

    @classmethod
    def get_value(cls, state: str, default_value: Any = "__empty_value__",
                  **kwargs) -> Any:
        """Get value from streamlit `session_state`.

        It will run the triggers associated with get operation.
        StateBeforeGetTrigger will run before get and StateAfterGetTrigger
        will run after the get.

        Args:
            state (str):
                Name of the state that will be fetched. Get using this
                class will prefix this value with `pumpwood_st__` to help
                diferentiate from other non maneged states.
            default_value (Any):
                Return a default value if state is not found on Streamlit
                states.
            **kwargs (dict):
                Other arguments will be passed as kwargs to function associated
                with the triggers.

        Returns:
            Return value of `pumpwood_st__{state}` state found on Streamlit
            state.
        """
        is_val_state_present = (
            (state in st.session_state) or
            (default_value != "__empty_value__"))
        if not is_val_state_present:
            msg = (
                "State [{state}] was not found at Streamlit "
                "`session_state`. Check if state was initiated or set a "
                "default_value on get function.")
            raise PumpwoodStreamlitStateNotFoundException(
                message=msg, payload={"state": state})

        state_name_triggers = cls.TRIGGERS.get(state, [])
        is_type_validation_ok = (
            isinstance(state_name_triggers, list))
        if not is_type_validation_ok:
            msg = (
                'StateManager.TRIGGERS entry for state [{state}] if not a ' +
                'list or not set. Check dashboard StateManager.TRIGGERS ' +
                'definition')
            raise PumpwoodStreamlitConfigException(
                message=msg, payload={'state': state})

        # Run all trigger of before get before fetching state information
        for trigger in state_name_triggers:
            if isinstance(trigger, StateBeforeGetTrigger):
                trigger.run(**kwargs)

        # Get state value or return the default_value
        state_value = st.session_state.get(state, default_value)

        # Run all trigger of after get after fetching state information
        for trigger in state_name_triggers:
            if isinstance(trigger, StateAfterGetTrigger):
                trigger.run(**kwargs)
        return state_value

    @classmethod
    def set_value(cls, state: str, value: Any, ignore_init_error: bool = False,
                  **kwargs):
        """Set state at streamlit `session_state`.

        It will run the triggers associated with set operation.
        StateBeforeSetTrigger will run before get and StateAfterSetTrigger
        will run after the get.

        Args:
            state (str):
                Name of the state that will be setted. Get using this
                class will prefix this value with `pumpwood_st__` to help
                diferentiate from other non maneged states.
            value (Any):
                Value that will be setted at `pumpwood_st__{state}` on
                Streamlit state.
            ignore_init_error (bool):
                Ignore error if state is not init before set.
            **kwargs (dict):
                Other arguments will be passed as kwargs to function associated
                with the triggers.

        Returns:
            Return value of `pumpwood_st__{state}` state found on Streamlit
            state.
        """
        is_val_state_present = (
            (state in st.session_state) or
            ignore_init_error)
        if not is_val_state_present:
            msg = (
                "State [{state}] was not found at Streamlit "
                "`session_state`. Check if state was initiated or set "
                "argument `ignore_init_error=True`.")
            raise PumpwoodStreamlitStateNotFoundException(
                message=msg, payload={"state": state})

        state_name_triggers = cls.TRIGGERS.get(state, [])
        is_type_validation_ok = (
            isinstance(state_name_triggers, list))
        if not is_type_validation_ok:
            msg = (
                'StateManager.TRIGGERS entry for state [{state}] if not a ' +
                'list or not set. Check dashboard StateManager.TRIGGERS ' +
                'definition')
            raise PumpwoodStreamlitConfigException(
                message=msg, payload={'state': state})

        # Run all trigger of before get before fetching state information
        for trigger in state_name_triggers:
            if isinstance(trigger, StateBeforeSetTrigger):
                trigger.run(**kwargs)

        # Get state value or return the default_value
        st.session_state[state] = value

        # Run all trigger of after get after fetching state information
        for trigger in state_name_triggers:
            if isinstance(trigger, StateAfterSetTrigger):
                trigger.run(**kwargs)
        return True

    @classmethod
    def get_states(cls) -> dict:
        """Get Streamlit states and associated triggers.

        Return:
            Return a dictionary with mananeged states and its triggers.
        """
        return_dict = {}
        for key, item in st.session_state.items:
            is_managed = key.startswith('pumpwood_st__')
            state = key
            if is_managed:
                state = key.lstrip('pumpwood_st__')

            trigger_list = cls.TRIGGERS.get(state, [])
            list_trigger = []
            for t in trigger_list:
                list_trigger.append(t.to_dict())
            return_dict[state] = {
                "is_managed": True, "streamlit_state": key,
                "manager": state, "triggers": list_trigger}
        return return_dict

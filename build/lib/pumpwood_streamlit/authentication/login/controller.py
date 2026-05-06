"""Class to help fetching Authentication headers from Streamlit."""
import os
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_streamlit.state_manager import StateManager
from pumpwood_streamlit.authentication.abc.controller import (
    StreamlitAuthenticationABC)
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitUnauthorizedException,
    PumpwoodStreamlitConfigException)


class StreamlitUserAuthentication(StreamlitAuthenticationABC):
    """Create a authentication based on user login.

    Authentication that can be used with user login at streamlit. Auth header
    token is read from states.
    """

    AUTH_TOKEN_STATE = "PumpwoodAuthorizationToken" # NOQA

    def __init__(self, microservice: PumpWoodMicroService):
        """__init__."""
        self.debug_auth_header = None
        self.microservice = microservice

        # If env variable DEBUG_AUTHORIZATION_TOKEN is set then set
        # header for local development
        DEBUG_AUTHORIZATION_TOKEN = \
            os.getenv("DEBUG_AUTHORIZATION_TOKEN")

        # Use deploy variable to not deploy dashboards with
        # DEBUG_AUTHORIZATION_TOKEN
        DEPLOY = os.getenv("DEPLOY", "FALSE") == "TRUE"
        if DEBUG_AUTHORIZATION_TOKEN:
            if DEPLOY:
                msg = (
                    "Should not use 'DEBUG_AUTHORIZATION_TOKEN' env " +
                    "variable on production.")
                raise PumpwoodStreamlitConfigException(msg)

    def get_auth_header(self) -> dict:
        """Get auth header from streamlit state."""
        DEBUG_AUTHORIZATION_TOKEN = \
            os.getenv("DEBUG_AUTHORIZATION_TOKEN")
        if DEBUG_AUTHORIZATION_TOKEN is not None:
            return {"Authorization": DEBUG_AUTHORIZATION_TOKEN}

        # Retrieve token from states
        auth_header = StateManager.get_value(
            state=self.AUTH_TOKEN_STATE, default_value={})
        return auth_header

    def set_auth_header(self, auth_header: dict):
        """Set auth token on streamlit state.

        Args:
            auth_header (str):
                Token used to login on Pumpwood.
        """
        return StateManager.set_value(
            state=self.AUTH_TOKEN_STATE, value=auth_header,
            ignore_init_error=True)

    def logout(self):
        """Logout from dashboard."""
        StateManager.set_value(
            state=self.AUTH_TOKEN_STATE, value=None,
            ignore_init_error=True)

    def check_if_logged(self, raise_error: bool = True):
        """Check if auth_header if logged.

        Args:
            raise_error (bool):
                If user is not autorized will raise error if true and
                return false if `raise_error=False`.
        """
        auth_header = self.get_auth_header()
        is_logged = self.microservice.check_if_logged(
            auth_header=auth_header)
        if not is_logged and raise_error:
            msg = (
                "Authentication header is not valid, try to login again on "
                "application.")
            raise PumpwoodStreamlitUnauthorizedException(message=msg)
        return is_logged

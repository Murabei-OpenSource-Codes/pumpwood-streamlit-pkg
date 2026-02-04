"""Class to help fetching Authentication headers from Streamlit."""
import os
import copy
import streamlit as st
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_streamlit.authentication.abc.controller import (
    StreamlitAuthenticationABC)
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitUnauthorizedException,
    PumpwoodStreamlitConfigException)


class StreamlitPumpwoodAuthentication(StreamlitAuthenticationABC):
    """Class for auth validation using Pumpwood end-points."""

    microservice: PumpWoodMicroService
    """PumpWoodMicroService object to validate if auth_header is correct."""

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

    def get_auth_header(self):
        """Get auth header from cookies token."""
        DEBUG_AUTHORIZATION_TOKEN = \
            os.getenv("DEBUG_AUTHORIZATION_TOKEN")
        if DEBUG_AUTHORIZATION_TOKEN is not None:
            return {"Authorization": DEBUG_AUTHORIZATION_TOKEN}

        context_cookies = copy.deepcopy(dict(st.context.cookies))
        cookieauth_header = context_cookies.get("PumpwoodAuthorization")
        if cookieauth_header is not None:
            return {"Authorization": 'Token ' + cookieauth_header}
        else:
            return None

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

"""Class to help fetching authetication headers from Streamlit."""
import os
import streamlit as st
from abc import ABC, abstractmethod
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitUnauthorizedException,
    PumpwoodStreamlitConfigException)


class StreamlitAutheticationABC(ABC):
    """Abstract class to implement Autentication on Streamlit."""

    auth_header: dict
    """Auth header asssociated with session."""

    @abstractmethod
    def get_auth_header(self, refetch: bool = False):
        """Get auth header from cookies token."""
        pass

    @abstractmethod
    def check_if_logged(self, raise_error: bool = True):
        """
        Check if auth_header if logged.

        Args:
            raise_error (bool) = True:
                If user is not autorized will raise error if true and
                return false if `raise_error=False`.
        """
        pass


class StreamlitPumpwoodAuthetication(StreamlitAutheticationABC):
    """Class for auth validation using Pumpwood end-points."""

    auth_header: dict
    """Auth header asssociated with session."""

    microservice: PumpWoodMicroService
    """PumpWoodMicroService object to validate if auth_header is correct."""

    def __init__(self, microservice: PumpWoodMicroService):
        """__init__."""
        self.auth_header = None
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
            else:
                self.auth_header = {
                    "Authorization": DEBUG_AUTHORIZATION_TOKEN}

    def get_auth_header(self):
        """Get auth header from cookies token."""
        if self.auth_header is None:
            context_cookies = dict(st.context.cookies)
            cookieauth_header = context_cookies.get("PumpwoodAuthorization")
            if cookieauth_header is not None:
                self.auth_header = {
                    "Authorization": 'Token ' + cookieauth_header}
        return self.auth_header

    def check_if_logged(self, raise_error: bool = True):
        """
        Check if auth_header if logged.

        Args:
            raise_error (bool) = True:
                If user is not autorized will raise error if true and
                return false if `raise_error=False`.
        """
        auth_header = self.get_auth_header()
        is_logged = self.microservice.check_if_logged(
            auth_header=auth_header)
        if not is_logged and raise_error:
            msg = (
                "Authetication header is not valid, try to login again on "
                "application.")
            raise PumpwoodStreamlitUnauthorizedException(
                message=msg)
        return is_logged

"""Dashboard class to use as base from Pumpwood Streamlit Dashboards."""
import os
import streamlit as st
import extra_streamlit_components as stx
from abc import ABC, abstractmethod
from pumpwood_communication.microservices import PumpWoodMicroService


def _get_cookie_manager():
    """Retrieve Cookie Manager."""
    return stx.CookieManager()


class PumpwoodStreamlitDashboard(ABC):
    """Abstract Class to facilitate criation of Streamlit Dashboards."""

    def __init__(self, microservice: PumpWoodMicroService = None):
        """
        __init__.

        It is possible to init object with a microservice to help
        building dashboard.

        Kwargs:
            microservice [PumpWoodMicroService]: An microservice can
                be passed to object for developing and debug.
        """
        # Set auth_header to None, this will permit dev microservice to
        # use credencials and prod get auth header from cookie
        self._auth_token = None
        if microservice is not None:
            self._microservice = microservice
        else:
            MICROSERVICE_URL = os.getenv("MICROSERVICE_URL")
            if MICROSERVICE_URL is not None:
                self._microservice = PumpWoodMicroService(
                    name="dashboard-microservice",
                    server_url=MICROSERVICE_URL)
            else:
                msg = (
                    "'microservice' is not set as argument and " +
                    "'MICROSERVICE_URL' not set as enviroment variable")
                raise Exception(msg)

    def validate_authentication(self) -> bool:
        """
        Validate authentication using cookie with PumpwoodAuthorization.

        Return [bool]:
            Return True if user is logged on Pumpwood and False if token
            set at PumpwoodAuthorization is invalid.
        """
        cookie_manager = _get_cookie_manager()
        cookie_auth_token = cookie_manager.get('PumpwoodAuthorization')
        if cookie_auth_token is not None:
            self._auth_token = {"Authorization": 'Token ' + cookie_auth_token}

        is_logged = self._microservice.check_if_logged(
            auth_header=self._auth_token)
        return is_logged

    def authentication_error_page(self) -> None:
        """
        Set the authentication error page.

        This function is called if self.validate_login() return False.

        Example:
            st.title('User token is invalid, log in again to refresh token.')
        """
        st.title('User token is invalid, log in again to refresh token.')

    def run(self) -> None:
        """
        Render the dashboard.

        This function is used as an entry point for app.py Streamlit
        dashboard.

        Example of an app.py:
        >> from dashboard import Dashboard
        >> dash_obj = Dashboard()
        >> dash_obj.run()
        """
        # Set page configuration
        self.set_page_config()

        # Validate auth_header
        is_logged = self.validate_authentication()
        if not is_logged:
            # Authorization error
            self.authentication_error_page()
        else:
            # Render main Dashboard View
            self.main_view()

    @abstractmethod
    def set_page_config(self) -> None:
        """
        Set page config, must be implemented.

        Exemple:
        st.set_page_config(
            page_title="US Population Dashboard",
            page_icon="🏂",
            layout="wide",
            initial_sidebar_state="expanded")
        """
        msg = "'set_page_config' function must be implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def main_view(self):
        """
        Render main dashboard view.

        Exemple:
        st.set_page_config(
            page_title="US Population Dashboard",
            page_icon="🏂",
            layout="wide",
            initial_sidebar_state="expanded")
        """
        msg = "'main_view' function must be implemented"
        raise NotImplementedError(msg)

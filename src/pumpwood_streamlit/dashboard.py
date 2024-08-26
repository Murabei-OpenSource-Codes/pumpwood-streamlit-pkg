"""Dashboard class to use as base from Pumpwood Streamlit Dashboards."""
import os
import traceback
import streamlit as st
from abc import ABC, abstractmethod
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_communication.exceptions import PumpWoodException
from pumpwood_streamlit.exceptions import PumpwoodStreamlitException


class PumpwoodStreamlitDashboard(ABC):
    """Abstract Class to facilitate criation of Streamlit Dashboards."""

    def __init__(self, debug_microservice: PumpWoodMicroService = None):
        """__init__.

        It is possible to init object with a microservice to help
        building dashboard.

        If microservice=None (production deploy), `__init__` will create an
        unlogged microservice object using `MICROSERVICE_URL` from enviroment
        variable. Authentication validation function will set attribute
        `_auth_token` with `PumpwoodAuthorization` token that can be used
        to user impersonation.

        Args:
            debug_microservice:
                 An microservice can be passed to object for developing
                 and debug.
        """
        # Set auth_header to None, this will permit dev microservice to
        # use credencials and prod get auth header from cookie
        self._auth_token = None

        # Set 'TRUE' if streamlit was deployed, this will prevent
        # deploying Dashboard with logged microservice (disable auth)
        # on production and local docker-compose
        is_PUMPWOODSTREAMLIT__DEPLOY = os.getenv(
            "PUMPWOOD_STREAMLIT__DEPLOY", "FALSE") == "TRUE"
        if debug_microservice is not None:
            if is_PUMPWOODSTREAMLIT__DEPLOY:
                msg = (
                    "PUMPWOOD_STREAMLIT__DEPLOY env variable is set as "
                    "'TRUE', but a debug_microservice object was passed "
                    "as argument.")
                raise PumpwoodStreamlitException(msg)
            self._microservice = debug_microservice

        # If a debug microservice is not set, them create one using
        # `MICROSERVICE_URL`, microservice will use auth_header to
        # loging on backend.
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
        """Validate authentication using cookie with PumpwoodAuthorization.

        Returns:
            Return True if user is logged on Pumpwood and False if token
            set at PumpwoodAuthorization is invalid.
        """
        context_cookies = dict(st.context.cookies)
        cookie_auth_token = context_cookies.get("PumpwoodAuthorization")
        if cookie_auth_token is not None:
            self._auth_token = {"Authorization": "Token " + cookie_auth_token}

        is_logged = self._microservice.check_if_logged(
            auth_header=self._auth_token)
        return is_logged

    def authentication_error_page(self) -> None:
        """Set the authentication error page.

        This function is called if self.validate_login() return False.

        Example:
        ```python
        st.title('User token is invalid, log in again to refresh token.')
        ```
        """
        st.title("User token is invalid, log in again to refresh token.")

    def error_handler(self, exception: PumpWoodException) -> bool:
        """
        Handle PumpwoodStreamlitException errors.

        Render a default page for PumpwoodStreamlitException.
        """
        exception_dict = exception.to_dict()
        tb = traceback.format_exc()
        with st.container():
            st.header("Error when running dashboard")
            st.text(exception_dict['message'])

        with st.container():
            with st.expander("Debug traceback"):
                st.write(tb)

    def run(self) -> None:
        """Render Streamlit dashboard.

        This function is used as an entry point for app.py Streamlit
        dashboard.

        Most of the cases should not be reimplemented. It is important
        that if reimplemented `is_logged = self.validate_authentication()`
        function must be called at the beggin to assure that user is
        authenticated on Pumpwood.

        Example of an app.py:
        ```
        import os
        from dashboard import Dashboard
        from pumpwood_communication.microservices import PumpWoodMicroService

        ###############################################################
        # Read env variables to be used on local test of the dashboard.
        # Passing a logged microservice to dashboard will disable
        # authentication
        # !!! DO NOT USE AUTHENTICATED MICROSERVICE IN PRODUCTION
        # DASHBOARDS !!! #
        MICROSERVICE_URL = os.getenv('MICROSERVICE_URL')
        MICROSERVICE_DASHBOARD_USERNAME = os.getenv(
            'MICROSERVICE_DASHBOARD_USERNAME')
        MICROSERVICE_DASHBOARD_PASSWORD = os.getenv(
            'MICROSERVICE_DASHBOARD_PASSWORD')

        microservice = None
        if MICROSERVICE_DASHBOARD_USERNAME is not None:
            microservice = PumpWoodMicroService(
                name="dashboard-microservice",
                server_url=MICROSERVICE_URL,
                username=MICROSERVICE_DASHBOARD_USERNAME,
                password=MICROSERVICE_DASHBOARD_PASSWORD,)
            microservice.login()

        dash_obj = Dashboard(microservice=microservice)
        dash_obj.run()
        ```

        Implemented run function:
        ```python
        def run(self) -> None:
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
        ```
        """
        # Set page configuration
        self.set_page_config()

        # Validate auth_header
        is_logged = self.validate_authentication()
        if not is_logged:
            # Authorization error
            self.authentication_error_page()
        else:
            # Render main Dashboard View, if any PumpwoodStreamlitException
            # errors were raised, them treat them and return a default
            # error page.
            try:
                self.main_view()
            except PumpWoodException as e:
                self.error_handler(exception=e)

    @abstractmethod
    def set_page_config(self) -> None:
        """Set page config, must be implemented.

        Exemple:
        ```python
        st.set_page_config(
            page_title="US Population Dashboard",
            page_icon="🏂",
            layout="wide",
            initial_sidebar_state="expanded")
        ```
        """
        msg = "'set_page_config' function must be implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def main_view(self) -> None:
        """Render main dashboard view.

        Exemple:
        ```python
        st.set_page_config(
            page_title="US Population Dashboard",
            page_icon="🏂",
            layout="wide",
            initial_sidebar_state="expanded")
        ```
        """
        msg = "'main_view' function must be implemented"
        raise NotImplementedError(msg)

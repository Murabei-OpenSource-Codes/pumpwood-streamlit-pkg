"""Dashboard class to use as base from Pumpwood Streamlit Dashboards."""
import os
import traceback
import streamlit as st
from abc import ABC, abstractmethod
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_communication.exceptions import PumpWoodException
from pumpwood_streamlit.authentication import StreamlitAuthenticationABC
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitUnauthorizedException)


class PumpwoodStreamlitDashboard(ABC):
    """Abstract Class to facilitate criation of Streamlit Dashboards."""

    @property
    @abstractmethod
    def streamlit_auth(self) -> StreamlitAuthenticationABC:
        """Object of sub-class StreamlitAuthenticationABC."""
        pass

    @property
    @abstractmethod
    def microservice(self) -> PumpWoodMicroService:
        """Object of PumpWoodMicroService."""
        pass

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
        """Handle PumpwoodStreamlitException errors.

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

        dash_obj = Dashboard()
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
        self.set_style()

        # Render main Dashboard View, if any PumpwoodStreamlitException
        # errors were raised, them treat them and return a default
        # error page.
        try:
            self.streamlit_auth.check_if_logged()
            self.main_view()
        except PumpwoodStreamlitUnauthorizedException:
            self.authentication_error_page()
        except PumpWoodException as e:
            self.error_handler(exception=e)
        except Exception as e:
            raise e

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

    def set_style(self) -> None:
        """Set style associated with dashboard.

        Read all css files at a style folder and add them to dashboard.
        Styles folder is set using `PUMPWOOD_DASHBOARD__STYLES_DIR`
        enviroment variable, it default as `styles`.
        """
        PUMPWOOD_DASHBOARD__STYLES_DIR = \
            os.getenv("PUMPWOOD_DASHBOARD__STYLES_DIR", "static/styles")
        all_styles = []
        for file in os.listdir(PUMPWOOD_DASHBOARD__STYLES_DIR):
            if file.endswith(".css"):
                file_path = os.path.join(PUMPWOOD_DASHBOARD__STYLES_DIR, file)
                file_break = (
                    "\n/* ### Styles from file [{file}] ### */").format(
                        file=file)
                all_styles.append(file_break)
                with open(file_path, "r") as file:
                    all_styles.append(file.read())
        css = '\n'.join(all_styles)
        st.markdown(
            "<style> {css} </style>".format(css=css),
            unsafe_allow_html=True)

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

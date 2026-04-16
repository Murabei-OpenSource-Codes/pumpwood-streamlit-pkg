"""Dashboard class to use as base from Pumpwood Streamlit Dashboards."""

import os
import traceback
import streamlit as st
from abc import ABC, abstractmethod
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_communication.exceptions import PumpWoodException
from pumpwood_streamlit.authentication import StreamlitAuthenticationABC
from pumpwood_streamlit.query_params import decode_url_params
from pumpwood_streamlit.exceptions import (
    PumpwoodStreamlitUnauthorizedException,
)


class PumpwoodStreamlitDashboard(ABC):
    """Abstract Class to facilitate criation of Streamlit Dashboards.

    Attributes:
        URL_PARAMS (dict):
            Dictionary defining expected URL query parameters.
            Each key is a parameter name and value is a dict
            with configuration:
                - required (bool): If True, the parameter must
                  be present for `has_url_params()` to return
                  True. If False, the parameter is optional.
                - default (str): Default value when param is
                  not present. Only used for optional params.

            When all required params are present in the URL,
            `has_url_params()` returns True and filters should
            be hidden.

            Example:
            ```python
            URL_PARAMS = {
                "code": {"required": True},
                "variable": {"required": True},
                "date_init": {
                    "required": False, "default": None},
                "date_end": {
                    "required": False, "default": None},
            }
            ```
    """

    URL_PARAMS = {}
    """URL query parameters configuration dictionary."""

    @classmethod
    def get_url_params(cls):
        """Extract and validate query params from URL.

        Checks if all required parameters (required=True) are
        present in `st.query_params`. If they are, returns a
        dictionary with all parameter values as raw strings.
        If any required parameter is missing, returns None.

        Returns:
            dict or None:
                Dictionary with parameter values as strings,
                or None if required params are missing.

        Example:
            ```python
            # URL: ?code=ABC&variable=potencia-ativa
            params = Dashboard.get_url_params()
            # params = {
            #     "code": "ABC",
            #     "variable": "potencia-ativa",
            #     "date_init": None,
            #     "date_end": None,
            # }

            # URL sem params obrigatórios:
            params = Dashboard.get_url_params()
            # params = None
            ```
        """
        params = {}
        for param_name, config in cls.URL_PARAMS.items():
            is_required = config.get("required", False)
            default = config.get("default", None)
            value = st.query_params.get(param_name, None)

            if value is None and is_required:
                return None
            params[param_name] = value or default
        return params

    @classmethod
    def has_url_params(cls):
        """Check if all required URL query params are present.

        Returns:
            bool:
                True if all required parameters defined in
                URL_PARAMS are present in the URL.

        Example:
            ```python
            def main_view(self):
                if self.has_url_params():
                    params = self.get_url_params()
                    # Render URL header, hide filters
                else:
                    # Render filter bar
            ```
        """
        return cls.get_url_params() is not None

    @classmethod
    def render_filters_section(cls, render_grid, filter_keys=None, **kwargs):
        """Organize the filter section depending on the mode.

        If valid parameters are found in the URL (URL mode), the manual
        filter grid is omitted. Otherwise, the grid rendering function
        is executed.

        Workflow:
            Start -> Normal Mode
              |
            Has URL?
              |
            Yes -> Evaluate filters
              |
            Values valid? -> URL Mode (grid hidden)
              |
            Else -> Normal Mode (grid shown)

        Args:
            render_grid (callable): Function that renders the
                dashboard's manual filter grid.
            filter_keys (list, optional): List of keys that, if present
                in the decoded JSON, activate URL mode. If None, any
                content in the JSON activates the mode.
            **kwargs: Arguments passed to the grid function.

        Example:
            >>> def my_filters(plant_id):
            ...     st.selectbox("Select Plant", [1, 2], key="plant_id")
            >>> dashboard.render_filters_section(
            ...     render_grid=my_filters,
            ...     filter_keys=["plant_id"],
            ...     plant_id=1
            ... )
        """
        is_url_mode = False
        if cls.has_url_params():
            raw = cls.get_url_params()
            url_params = decode_url_params(raw)

            if filter_keys:
                # If any of the specified keys are present
                is_url_mode = any(
                    url_params.get(k) is not None for k in filter_keys
                )
            else:
                # If there is anything in the dictionary
                is_url_mode = len(url_params) > 0

        if not is_url_mode:
            with st.container():
                render_grid(**kwargs)

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
            st.text(exception_dict["message"])

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
        PUMPWOOD_DASHBOARD__STYLES_DIR = os.getenv(
            "PUMPWOOD_DASHBOARD__STYLES_DIR", "static/styles"
        )
        all_styles = []
        for file in os.listdir(PUMPWOOD_DASHBOARD__STYLES_DIR):
            if file.endswith(".css"):
                file_path = os.path.join(PUMPWOOD_DASHBOARD__STYLES_DIR, file)
                file_break = (
                    "\n/* ### Styles from file [{file}] ### */"
                ).format(file=file)
                all_styles.append(file_break)
                with open(file_path, "r") as file:
                    all_styles.append(file.read())
        css = "\n".join(all_styles)
        st.markdown(
            "<style> {css} </style>".format(css=css), unsafe_allow_html=True
        )

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

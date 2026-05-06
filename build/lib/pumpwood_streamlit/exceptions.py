"""Define custom exceptions from Streamlit dashboards."""
from pumpwood_communication.exceptions import PumpWoodException


class PumpwoodStreamlitException(PumpWoodException):
    """Class for General exceptions at Streamlit Dashboards."""

    pass


class PumpwoodStreamlitUnauthorizedException(PumpWoodException):
    """Class for Unauthorized exceptions at Streamlit Dashboards."""

    status_code = 401


class PumpwoodStreamlitStateNotFoundException(PumpWoodException):
    """Class for Not Found exceptions at Streamlit Dashboards."""

    status_code = 404


class PumpwoodStreamlitConfigException(PumpwoodStreamlitException):
    """Configuration error of streamlit dashboard."""

    status_code = 500

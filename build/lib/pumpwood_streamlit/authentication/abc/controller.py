"""Module to define the struture of Streamlit Authentication class."""
from abc import ABC, abstractmethod


class StreamlitAuthenticationABC(ABC):
    """Abstract class to implement Autentication on Streamlit."""

    auth_header: dict
    """Auth header asssociated with session."""

    @abstractmethod
    def get_auth_header(self, refetch: bool = False):
        """Get auth header from cookies token."""
        pass

    @abstractmethod
    def check_if_logged(self, raise_error: bool = True):
        """Check if auth_header if logged.

        Args:
            raise_error (bool):
                If user is not autorized will raise error if true and
                return false if `raise_error=False`.
        """
        pass

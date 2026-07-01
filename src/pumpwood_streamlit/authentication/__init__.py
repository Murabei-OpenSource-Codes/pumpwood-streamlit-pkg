"""Authentication backends for Streamlit dashboards.

Exports:

- ``StreamlitAuthenticationABC``: abstract base class.
- ``StreamlitPumpwoodAuthentication``: cookie-based auth via
  ``PumpwoodAuthorization``.
- ``StreamlitUserAuthentication``: username/password login form.
- ``StreamlitUserAuthenticationLoginView``: login page view.
"""
# Controlers
from pumpwood_streamlit.authentication.abc.controller import (
    StreamlitAuthenticationABC, )
from pumpwood_streamlit.authentication.login.controller import (
    StreamlitUserAuthentication)
from pumpwood_streamlit.authentication.pumpwood.controller import (
    StreamlitPumpwoodAuthentication)

# Views
from pumpwood_streamlit.authentication.login.view import (
    StreamlitUserAuthenticationLoginView)


__init__ = [
    StreamlitAuthenticationABC,
    StreamlitUserAuthentication,
    StreamlitUserAuthenticationLoginView,
    StreamlitPumpwoodAuthentication]

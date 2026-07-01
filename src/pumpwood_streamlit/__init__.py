"""Pumpwood Streamlit package.

This package helps build Streamlit dashboards with authentication
integrated with Pumpwood Auth and tools for Kong route registration,
session state management, and URL-driven filter hiding.

## Quick start

Create the ``app.py`` entry point called by Streamlit:

```python
from dashboard import Dashboard

dash_obj = Dashboard()
dash_obj.run()
```

Create the dashboard subclass:

```python
import streamlit as st
from pumpwood_streamlit.dashboard import PumpwoodStreamlitDashboard
from pumpwood_streamlit.authentication import StreamlitPumpwoodAuthentication
from singletons import microservice


class Dashboard(PumpwoodStreamlitDashboard):
    microservice = microservice
    streamlit_auth = StreamlitPumpwoodAuthentication(microservice)

    def set_page_config(self):
        st.set_page_config(page_title="My Dashboard", layout="wide")

    def main_view(self):
        st.title("Dashboard content")
```

## Authentication

Two authentication backends are available:

- ``StreamlitPumpwoodAuthentication``: reads the
  ``PumpwoodAuthorization`` cookie set by the Pumpwood web app.
- ``StreamlitUserAuthentication``: renders a login form and stores
  the token in Streamlit session state via ``StateManager``.

Assign the chosen backend to the ``streamlit_auth`` class attribute.
``PumpwoodStreamlitDashboard.run()`` calls
``streamlit_auth.check_if_logged()`` before rendering ``main_view()``.

## URL parameters

``URLParams`` is a utility class — do not subclass it. Set
``URLParams.URL_PARAMS`` and call its class methods from the
dashboard. When all required params are present,
``URLParams.has_url_params()`` returns ``True`` and
``URLParams.render_filters_section()`` can skip the manual filter
grid. Encoded filter values use URL-safe base64 JSON via the
``params`` query key.

```python
from pumpwood_streamlit.query_params import URLParams

URLParams.URL_PARAMS = {"params": {"required": True}}

# inside main_view():
URLParams.render_filters_section(
    render_grid=render_filters,
    filter_keys=["plant_id"],
)
```

## Kong registration

Call ``PumpwoodStreamlitRegister.run()`` at deploy time to register
the Streamlit service and route. See ``register.py`` for required
environment variables.

## Environment variables

- **DEBUG_FILES_PATH:** Path to save state debug files. Files are
  written under ``{debug_path}/{state_name}/`` as
  ``{state_name}__{type}__{time}.{extension}``.
- **DEBUG_AUTHORIZATION_TOKEN:** Bypass authentication during local
  development.
- **DEPLOY:** Defaults to ``TRUE`` on Docker images. Raises an error
  when ``DEBUG_AUTHORIZATION_TOKEN`` is set and ``DEPLOY`` is ``TRUE``.
- **PUMPWOOD_DASHBOARD__STYLES_DIR:** Folder with CSS files loaded
  by ``set_style()`` (default: ``static/styles``).
- **PUMPWOOD_DASHBOARD__STATEMANAGER:** Import path for the
  ``StateManager`` class (default:
  ``integration.state_manager.StateManager``).
"""

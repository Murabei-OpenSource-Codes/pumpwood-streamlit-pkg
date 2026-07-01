# pumpwood-streamlit-pkg

Python package to deploy Streamlit dashboards at Pumpwood Systems.

<p align="center" width="60%">
  <img src="static_doc/sitelogo-horizontal.png" /> <br>

  <a href="https://en.wikipedia.org/wiki/Cecropia">
    Pumpwood is a native Brazilian tree
  </a> which has a symbiotic relation with ants (Murabei)
</p>

This package helps deploy Streamlit dashboards integrated with Pumpwood
systems. It registers routes at Kong so all microservices share a single
endpoint, and provides a base dashboard class with authentication,
state management, and optional URL-driven filter hiding.

## Features

- **Authentication:** Cookie-based (`PumpwoodAuthorization`) or
  username/password login via `StreamlitUserAuthentication`.
- **Dashboard base class:** `PumpwoodStreamlitDashboard` with
  `run()`, error handling, and custom CSS loading.
- **URL parameters:** ``URLParams`` utility class to hide manual
  filters when a dashboard is opened from a deep link.
- **Kong registration:** `PumpwoodStreamlitRegister` to register the
  service and route at deploy time.
- **State management:** `StateManager` with triggers for session
  state get/set operations.

## Documentation

API reference (pdoc):
[https://murabei-opensource-codes.github.io/pumpwood-streamlit-pkg/pumpwood_streamlit.html](https://murabei-opensource-codes.github.io/pumpwood-streamlit-pkg/pumpwood_streamlit.html)

## Quick start

### app.py

```python
from dashboard import Dashboard

dash_obj = Dashboard()
dash_obj.run()
```

### dashboard.py

```python
import streamlit as st
from pumpwood_streamlit.dashboard import PumpwoodStreamlitDashboard
from pumpwood_streamlit.query_params import URLParams
from pumpwood_streamlit.authentication import StreamlitPumpwoodAuthentication
from singletons import microservice

URLParams.URL_PARAMS = {
    "params": {"required": True},
}


class Dashboard(PumpwoodStreamlitDashboard):
    microservice = microservice
    streamlit_auth = StreamlitPumpwoodAuthentication(microservice)

    def set_page_config(self):
        st.set_page_config(
            page_title="My Dashboard",
            page_icon="📊",
            layout="wide",
        )

    def main_view(self):
        def render_filters():
            st.selectbox("Plant", [1, 2, 3], key="plant_id")

        URLParams.render_filters_section(
            render_grid=render_filters,
            filter_keys=["plant_id"],
        )
        st.title("Dashboard content")
```

### Authentication modes

| Class | Token source | Use case |
|-------|-------------|----------|
| `StreamlitPumpwoodAuthentication` | `PumpwoodAuthorization` cookie | Embedded in Pumpwood app |
| `StreamlitUserAuthentication` | Streamlit session state | Standalone login form |

When authentication fails, `run()` calls `authentication_error_page()`.

### URL parameters

Configure ``URLParams.URL_PARAMS`` and call ``URLParams`` methods
directly from ``main_view()``. When all required params are present,
``URLParams.has_url_params()`` returns ``True``. Use
``URLParams.render_filters_section()`` to skip the manual filter grid
in that mode. Filter values are passed as a URL-safe base64 JSON blob
via the ``params`` query key; decode with
``URLParams.decode_url_params()``.

### Kong registration

Call `PumpwoodStreamlitRegister.run()` at deploy time. Required
environment variables:

- `MICROSERVICE_NAME`, `MICROSERVICE_URL`, `MICROSERVICE_USERNAME`,
  `MICROSERVICE_PASSWORD`
- `SERVICE_URL`, `DASHBOARD_NAME`

### Environment variables

| Variable | Description |
|----------|-------------|
| `DEBUG_FILES_PATH` | Save state debug files under `{path}/{state_name}/`. |
| `DEBUG_AUTHORIZATION_TOKEN` | Bypass auth for local development. |
| `DEPLOY` | When `TRUE`, blocks `DEBUG_AUTHORIZATION_TOKEN` in prod. |
| `PUMPWOOD_DASHBOARD__STYLES_DIR` | CSS folder (default: `static/styles`). |
| `PUMPWOOD_DASHBOARD__STATEMANAGER` | Import path for `StateManager` class. |

## Example

A full Streamlit population dashboard example is available in the
[Streamlit gallery](https://docs.streamlit.io/develop/tutorials/execution-and-deployment).
Adapt it by subclassing `PumpwoodStreamlitDashboard` as shown above.

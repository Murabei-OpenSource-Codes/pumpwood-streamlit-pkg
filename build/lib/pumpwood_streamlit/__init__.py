"""
# Pumpwood Streamlit Package.

This package helps to build Streamlit dashboard with authentication
integrated with Pumpwood Auth authentication.

## Example of use in aplications:
Creation of the app.py called by streamlit:
```python
import os
from dashboard import Dashboard
from pumpwood_communication.microservices import PumpWoodMicroService

dash_obj = Dashboard()
dash_obj.run()
```

Creation of the dashboard:
```python
import os
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from pumpwood_streamlit.dashboard import PumpwoodStreamlitDashboard
from singletons import microservice, streamlit_auth


class Dashboard(PumpwoodStreamlitDashboard):
    microservice = microservice
    streamlit_auth = streamlit_auth

    def set_page_config(self):
        #######################
        # Page configuration
        st.set_page_config(
            page_title="US Population Dashboard",
            page_icon="🏂",
            layout="wide",
            initial_sidebar_state="expanded")

    def main_view(self):
        alt.themes.enable("dark")

        #######################
        # Load data
        st.title('O dash mudou!')
```

## Enviroment variables:
Some enviroment can be used to debug and modify behaivor of the package
functions. Here are they description:
- **DEBUG_FILES_PATH:** Set the path to save data that is
    init and set at states using `StateManager`. This may help to debug
    dashboard, files will be saved at folder `{debug_path}/{state_name}` and
    file name `{state_name}__{type}__{time}.{extension}`.
- **DEBUG_AUTHORIZATION_TOKEN:** This variable can be set to by pass defautl
    authentication. This will help at the development reducing the time
    of authentication at each local test.
- **DEPLOY:** If by default will be set as `TRUE` on docker images,
    this is a safe lock to throw error will `DEBUG_AUTHORIZATION_TOKEN` is
    not None and DEPLOY is `TRUE`
"""

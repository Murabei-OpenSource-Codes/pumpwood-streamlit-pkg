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

##########################################################################
# Read env variables to be used on local test of the dashboard.          #
# Passing a logged microservice to dashboard will disable authentication #
# !!! DO NOT USE AUTHENTICATED MICROSERVICE IN PRODUCTION DASHBOARDS !!! #
MICROSERVICE_URL = os.getenv('MICROSERVICE_URL')
MICROSERVICE_DASHBOARD_USERNAME = os.getenv('MICROSERVICE_DASHBOARD_USERNAME')
MICROSERVICE_DASHBOARD_PASSWORD = os.getenv('MICROSERVICE_DASHBOARD_PASSWORD')

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

Creation of the dashboard:
```python
import os
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from pumpwood_streamlit.dashboard import PumpwoodStreamlitDashboard


class Dashboard(PumpwoodStreamlitDashboard):
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
"""

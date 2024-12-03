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
"""

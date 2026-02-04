"""Script para criação da tela de Login da aplicação."""
import os
import streamlit as st
from singletons import streamlit_auth
from pumpwood_streamlit.state_manager import StateManager
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_communication.exceptions import PumpWoodUnauthorized


LOGO_URL = os.getenv("LOGO_URL")
"""URL for login logo."""

_MICROSERVICE_URL = os.getenv("MICROSERVICE_URL")
"""Fetch the microservice URL."""


class StreamlitUserAuthenticationLoginView:
    """View to perform login on dashboard."""

    STATE_USERNAME = "loginview__username"
    STATE_PASSWORD = "loginview__password" # NOQA
    STATE_ERROR_MSG = "loginview__error_msg"
    STATE_LOGIN_BUTTON__ON_CHANGE = "loginview__login_button__on_change"

    @classmethod
    def render(cls):
        """Função para definição de login."""
        logo_markdown = (
            '<div class="centered-image">'
            '<img src="{src}" alt="Logo"></div>')\
            .format(src=LOGO_URL)
        st.markdown(logo_markdown, unsafe_allow_html=True)

        with st.container():
            _, form, _ = st.columns([0.33, 0.33, 0.33])
            with form:
                st.text_input("Usuário", key=cls.STATE_USERNAME)
                st.text_input("Senha", type="password", key=cls.STATE_PASSWORD)
                error_msg = StateManager.get_value(
                    state=cls.STATE_ERROR_MSG, default_value=None)
                if error_msg is not None:
                    st.markdown(error_msg, unsafe_allow_html=False)
                st.button("Entrar", on_click=cls.login_on_click)

    @classmethod
    def login_on_click(cls):
        """Run when login button is pressed."""
        username = StateManager.get_value(
            state=cls.STATE_USERNAME)
        password = StateManager.get_value(
            state=cls.STATE_PASSWORD)
        microservice_obj = PumpWoodMicroService(
            name="dashboard-microservice-login",
            server_url=_MICROSERVICE_URL,
            username=username, password=password)
        try:
            microservice_obj.login()
            auth_header = microservice_obj.get_auth_header()\
                .get('auth_header')
            streamlit_auth.set_auth_header(auth_header=auth_header)
            StateManager.set_value(
                state=cls.STATE_ERROR_MSG, value=None,
                ignore_init_error=True)
        except PumpWoodUnauthorized:
            msg = "Erro ao executar o login"
            StateManager.set_value(
                state=cls.STATE_ERROR_MSG, value=msg,
                ignore_init_error=True)
        except Exception as e:
            raise e

    @classmethod
    def logout_on_click(cls):
        """Run when login button is pressed."""
        streamlit_auth.set_auth_header(auth_header=None)

"""Register Dashboard on Auth App."""
import os
from loguru import logger
from pumpwood_communication.microservices import PumpWoodMicroService


class PumpwoodStreamlitRegister:
    """Class to help register dashboard on pumpwood routes."""

    @classmethod
    def run(cls):
        """Run Dashboard registering on Pumpwood routes."""
        # Microservice
        MICROSERVICE_NAME = os.getenv("MICROSERVICE_NAME")
        MICROSERVICE_URL = os.getenv("MICROSERVICE_URL")
        MICROSERVICE_USERNAME = os.getenv("MICROSERVICE_USERNAME")
        MICROSERVICE_PASSWORD = os.getenv("MICROSERVICE_PASSWORD")

        # Kong and Streamlit configs
        SERVICE_URL = os.getenv("SERVICE_URL")
        DASHBOARD_NAME = os.getenv("DASHBOARD_NAME")

        # Creating Microservice
        print("## Log in PumpWoodMicroService")
        try:
            microservice = PumpWoodMicroService(
                name=MICROSERVICE_NAME, server_url=MICROSERVICE_URL,
                username=MICROSERVICE_USERNAME, password=MICROSERVICE_PASSWORD)
            microservice.login()
        except Exception as e:
            msg = (
                "I was not possible to login at auth using "
                "'{microservice_username}' service user")\
                .format(microservice_username=MICROSERVICE_USERNAME)
            logger.error(msg)
            raise e

        # Register Service
        print("## Registering streamlit dashboard: [{}]".format(
            DASHBOARD_NAME))
        try:
            service_object = microservice.save({
                "model_class": "KongService",
                'service_url': SERVICE_URL,
                'service_name': "streamlit-" + DASHBOARD_NAME,
                'description': "Streamlit Dashboard | " + DASHBOARD_NAME,
                'notes': (
                    "Service to serve streamlit Dashboard" + DASHBOARD_NAME),
                'dimensions': {
                    "microservice": "pumpwood-streamlit-dashboard",
                    "dashboard_name": DASHBOARD_NAME}})
        except Exception as e:
            msg = ("Error when registering service: {service_url}")\
                .format(service_url=SERVICE_URL)
            logger.error(msg)
            raise e

        route_url = "/streamlit/" + DASHBOARD_NAME
        try:
            route_object = {
                "model_class": "KongRoute",
                "service_id": service_object["pk"],
                "route_url": route_url,
                "route_name": "streamlit-" + DASHBOARD_NAME,
                "route_type": "datavis",
                "description": (
                    "Streamlit dashboard end-point: " + DASHBOARD_NAME),
                "notes": (
                    "Streamlit dashboard end-point: " + DASHBOARD_NAME),
                "dimensions": {
                    "microservice": "pumpwood-streamlit-dashboard",
                    "dashboard_name": DASHBOARD_NAME},
                "icon": None,
                "extra_info": {}}
            microservice.save(route_object)
        except Exception as e:
            msg = ("Error when registering route: {route_url}")\
                .format(route_url=route_url)
            logger.error(msg)
            raise e

import os
from typing import Tuple
from autobahn.asyncio.component import Component
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth


CB_REALM = "userapps"

DATAPODS_WS_URI = "wss://cbw.datapods.io/ws-ua-usr"
STUDIO_WS_URI = "wss://cbw.record-evolution.com/ws-ua-usr"
LOCALHOST_WS_URI = "ws://crossbar_node1/ws-ua-usr"

socketURIMap = {
    "https://studio.datapods.io": DATAPODS_WS_URI,
    "https://studio.record-evolution.com": STUDIO_WS_URI,
    "http://localhost:8085": LOCALHOST_WS_URI,
}


def getWebSocketURI():
    reswarm_url = os.environ.get("RESWARM_URL")
    if not reswarm_url:
        return STUDIO_WS_URI
    return socketURIMap.get(reswarm_url)


def getSerialNumber(serial_number: str = None) -> str:
    if serial_number is None:
        s_num = os.environ.get("DEVICE_SERIAL_NUMBER")
        if s_num is None:
            raise Exception("ENV Variable 'DEVICE_SERIAL_NUMBER' is not set!")
    else:
        s_num = serial_number
    return s_num


class AppSession(ApplicationSession):
    serial_number: str = None

    def onConnect(self):
        if self.serial_number is None:
            raise Exception("serial_number missing on AppSession")

        self.join(CB_REALM, ["wampcra"], self.serial_number)

    def onChallenge(self, challenge):
        if challenge.method == "wampcra":
            if self.serial_number is None:
                raise Exception("serial_number missing on AppSession")

            signature = auth.compute_wcs(
                self.serial_number, challenge.extra["challenge"]
            )
            return signature

        raise Exception("Invalid authmethod {}".format(challenge.method))


def create_application_session(
    serial_number: str = None,
) -> Tuple[ApplicationSession, ApplicationRunner]:
    """Creates an Autobahn ApplicationSession and ApplicationRunner, which connects to the RE Platform

    Args:
        serial_number (str, optional): serial_number of device.
        Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.

    Returns:
        Tuple[ApplicationSession, ApplicationRunner]
    """
    AppSession.serial_number = getSerialNumber(serial_number)

    runner = ApplicationRunner(
        url=getWebSocketURI(),
        realm=CB_REALM,
    )

    return AppSession, runner


def create_application_component(serial_number: str = None) -> Component:
    """Creates an Autobahn Component, which connects to the RE Platform

    Args:
        serial_number (str, optional): serial_number of device.
        Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.

    Returns:
        Component
    """
    appSession, _ = create_application_session(serial_number)

    return Component(
        transports=getWebSocketURI(),
        realm=CB_REALM,
        session_factory=appSession,
    )

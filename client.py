"""
This is the part of piCamTrap, copyright @ Wenlong Liu.
Created on July 15,2017

This script will publish data to MQTT sever.  For now, it is a local sever.

Platform: Raspberry Pi 3 Model B.
"""

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


class publish():
    def __init__(self, topic, payload=None, qos=0, retain=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311):

        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.retain = retain
        self.hostname = hostname
        self.port = port
        self.client_id = client_id
        self.keepalive = keepalive
        self.will = will
        self.auth = auth
        self.tls = tls
        self.protocol = protocol


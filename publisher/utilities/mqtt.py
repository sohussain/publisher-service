"""
@author: abdullahrkw
"""
import logging
import paho.mqtt.client as mqtt


def is_mqtt_running(mqtt_address, mqtt_port):
    """Test if mqtt server(broker) is accessible.
    
    If yes, then disconnects the client.
    Returns:
        [boolean] -- True if running, else false
    """
    address = mqtt_address
    port = int(mqtt_port)

    try:
        client = mqtt.Client()
        client.connect(address, port=port, keepalive=60)
    except Exception as e:
        logging.error(f"Can't connect to the mqtt broker at {address}:{port}.")
        logging.error(f"{e}")
        return False
    client.disconnect()
    return True

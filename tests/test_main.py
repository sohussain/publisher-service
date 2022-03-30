"""
@discription: tests methods defined in main.py
"""

from unittest.mock import MagicMock
from unittest.mock import patch

from config.utils import get_config
from publisher.main import package_receiver
from publisher.main import package_publisher
from publisher.utilities.mqtt import is_mqtt_running


@patch('publisher.queue.queue.mqtt.Client')
def test_package_receiver_client_connect_with_correct_params(mock_client):
    """ Test mqtt client calls subscribe with the correct method """
    client = mock_client.return_value  # creating instance of mock client
    client.subscribe = MagicMock(return_value=[0, 0])
    is_mqtt_running = MagicMock(return_value=True)
    config = get_config()
    package_receiver(config)

    client.connect.assert_called_with(
        config["edge_mqtt_address"],
        port=int(config["edge_mqtt_port"]),
        keepalive=int(config["package_receive_queue_keep_alive"]))

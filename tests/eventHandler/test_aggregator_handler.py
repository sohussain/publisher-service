"""
@discription: test aggregator service handler
Note: ASH use mqtt queue to subscribe to mqtt
broker.
@author: abdullahrkw
"""

import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from publisher.queue.queue import MessageQueue
from publisher.eventHandler.aggregator_handler import AggregatorServiceHandler
from config.utils import get_config


@patch('publisher.queue.queue.mqtt.Client')
def test_connect_call_has_correct_params(mock_client):
    """ Test mqtt client calls subscribe with the correct method """
    client = mock_client.return_value  # creating instance of mock client
    client.subscribe = MagicMock(return_value=[0, 0])

    config = get_config()
    aggregator_handler_config = {
        "topic": config["package_receive_topic"],
        "queue_address": config["edge_mqtt_address"],
        "queue_port": int(config["edge_mqtt_port"]),
        "queue_keep_alive": int(config["package_receive_queue_keep_alive"]),
        "queue_qos": int(config["package_receive_queue_qos"]),
    }
    aggregatorServiceHandler = AggregatorServiceHandler(
        aggregator_handler_config)

    client.connect.assert_called_with(
        config["edge_mqtt_address"],
        port=int(config["edge_mqtt_port"]),
        keepalive=int(config["package_receive_queue_keep_alive"]))

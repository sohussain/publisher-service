"""
@discription: test queue which is a wrapper over paho
mqtt queue
@author: Bazarovey
"""

import pytest
from unittest.mock import create_autospec
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from publisher.queue.queue import MessageQueue

argument_list = [
    "address", "port", "keep_alive", "qos", "user_data", "clean_session",
    "client_id"
]
argument_dict = {key: None for key in argument_list}


@pytest.mark.parametrize("args", [argument_dict])
def test_exception_is_thrown_when_arguments_not_passed(args):
    """Tests exception is thrown when key is empty or none
    @TODO add all permutations"""
    with pytest.raises(ValueError):
        _ = MessageQueue(**args)


@patch('publisher.queue.queue.mqtt.Client')
def test_mqtt_client_is_instantiated(mock_client):
    """ Test mqtt client class is instantiated """
    _ = MessageQueue(address="some_address",
                     port="some_port",
                     keep_alive="some_keep_time",
                     qos=1)
    mock_client.assert_called_once(
    )  # check instance was created in the function


@patch('publisher.queue.queue.mqtt.Client')
def test_publish_call_has_correct_params(mock_client):
    """ Test mqtt client calls publish with the correct method """
    client = mock_client.return_value  # creating instance of mock client
    client.publish = MagicMock(return_value=[0, 0])

    message_queue = MessageQueue(address="some_address",
                                 port="some_port",
                                 keep_alive="some_keep_time",
                                 qos=1)
    message_queue.publish("some_topic", "some_message")

    client.publish.assert_called_with("some_topic",
                                      payload="some_message",
                                      qos=1,
                                      retain=False)

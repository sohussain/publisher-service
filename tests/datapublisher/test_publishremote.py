"""
@description: test publisher service handler 
Note: PSH uses mqtt queue to publish to mqtt 
broker.
@author: abdullahrkw
"""
import os
import pytest
import ssl
from unittest.mock import MagicMock
from unittest.mock import patch

from publisher.queue.queue import MessageQueue
from publisher.dataPublisher.publishRemote import CloudPublisher
from config.utils import get_config

@patch.dict(os.environ, {'PUBLISHER_ID':'publisher_testing'})
@patch('publisher.queue.queue.mqtt.Client')
def test_publish_call_has_correct_params(mock_client):
    """ Test mqtt client calls publish with the correct method """
    client = mock_client.return_value  # creating instance of mock client
    client.publish = MagicMock(return_value=[0, 0])

    config = get_config()
    cloud_publisher_config = {
        "topic": config["cloud_publish_topic"],
        "queue_address": config["cloud_mqtt_address"],
        "queue_port": int(config["cloud_mqtt_port"]),
        "queue_keep_alive": int(config["cloud_queue_keep_alive"]),
        "queue_qos": int(config["cloud_queue_qos"]),
        "enable_ssl": bool(int(config["remote_publisher_enable_ssl"])),
        "ca_certs": config["ca_certs"],
        "certfile": config["client_cert"],
        "keyfile": config["client_key"]

    }
    cloud_publisher = CloudPublisher(cloud_publisher_config)
    cloud_publisher.publish("some_message")

    client.publish.assert_called_with(config["cloud_publish_topic"],
                                      payload="some_message",
                                      qos=int(config["cloud_queue_qos"]),
                                      retain=False)


@patch.dict(os.environ, {'PUBLISHER_ID':'publisher_testing'})
@patch('publisher.queue.queue.mqtt.Client')
def test_tls_has_correct_params(mock_client):
    """ Test mqtt client has correct tls params (specified in config) """
    client = mock_client.return_value  # creating instance of mock client
    client.publish = MagicMock(return_value=[0, 0])

    config = get_config()
    ca_certs = "mosq-ca.crt"
    certfile = "mosq-client.crt"
    keyfile = "mosq-ca.key"
    cloud_publisher_config = {
        "topic": config["cloud_publish_topic"],
        "queue_address": config["cloud_mqtt_address"],
        "queue_port": int(config["cloud_mqtt_port"]),
        "queue_keep_alive": int(config["cloud_queue_keep_alive"]),
        "queue_qos": int(config["cloud_queue_qos"]),
        "enable_ssl": int("1"),
        "ca_certs": ca_certs,
        "certfile": certfile,
        "keyfile": keyfile

    }
    _ = CloudPublisher(cloud_publisher_config)

    client.tls_set.assert_called_with(ca_certs=ca_certs, 
                                    certfile=certfile, 
                                    keyfile=keyfile, 
                                    cert_reqs=ssl.CERT_REQUIRED,
                                    tls_version=ssl.PROTOCOL_TLSv1_2, 
                                    ciphers=None)

@patch.dict(os.environ, {'PUBLISHER_ID':'publisher_testing'})
@patch('publisher.queue.queue.mqtt.Client')
def test_tls_not_called_if_ssl_disabled(mock_client):
    """ Test mqtt client does not call tls_set if enable_tls is "0" (specified in config) """
    client = mock_client.return_value  # creating instance of mock client
    client.publish = MagicMock(return_value=[0, 0])

    config = get_config()
    cloud_publisher_config = {
        "topic": config["cloud_publish_topic"],
        "queue_address": config["cloud_mqtt_address"],
        "queue_port": int(config["cloud_mqtt_port"]),
        "queue_keep_alive": int(config["cloud_queue_keep_alive"]),
        "queue_qos": int(config["cloud_queue_qos"]),
        "enable_ssl": int("0"),
        "ca_certs": "mosq-ca.crt",
        "certfile": "mosq-client.crt",
        "keyfile": "mosq-ca.key"

    }
    _ = CloudPublisher(cloud_publisher_config)

    assert not client.tls_set.called

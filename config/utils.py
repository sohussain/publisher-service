"""
@discription: some utility functions related to config
"""

import logging
import os

from config.config_reader.config_factory import ConfigFactory

ini_parser = ConfigFactory.get_config(file_format='ini')
file_path = os.path.abspath('config/config_files/config.ini')
config = ini_parser.get_config(path=file_path)

expected_keys = [
    "edge_mqtt_address",
    "edge_mqtt_port",
    "package_receive_topic",
    "package_receive_queue_keep_alive",
    "package_receive_queue_qos",
    "container_storage",
    "cloud_mqtt_address",
    "cloud_mqtt_port",
    "cloud_publish_topic",
    "cloud_queue_qos",
    "cloud_queue_keep_alive",
    "log_level",
    "remote_publisher_enable_ssl",
    "ca_certs",
    "client_cert",
    "client_key",
    "redis_host",
    "redis_port"
]

config_keys = config.keys()


def is_config_valid():
    for key in expected_keys:
        if key not in config_keys:
            logging.error(f"[{key}] required in config but not present")
            return False

    logging.info("config validated ...")
    return True

def get_config():
    return config

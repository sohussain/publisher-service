import json
import multiprocessing
import os
import pytest
import shlex
import subprocess
import time
from unittest import mock
from unittest.mock import patch

from config.config_reader.config_factory import ConfigFactory
from publisher.queue.queue import MessageQueue
from publisher.main import package_receiver
from publisher.main import package_publisher


def publish_sample_package_to_queue(topic, sample_package):
    sample_queue = MessageQueue(
                        address="localhost",
                        port=1883,
                        keep_alive=60,
                        qos=1,
                        client_id="test_client",
                        clean_session=False,
                    )
    sample_queue.publish(topic, sample_package)

def start_mosquitto():
    subprocess.run(["mosquitto", "-v"])

def start_redis_server():
    subprocess.run(["redis-server"])

############################# Pytest Fixtures ###################
@pytest.fixture
@mock.patch.dict(os.environ, {"MODE": "TESTING"}, clear=True)
def sample_config():
    ini_parser = ConfigFactory.get_config(file_format='ini')
    file_path = os.path.abspath('tests/acceptance_test/test_config.ini')
    config = ini_parser.get_config(path=file_path)
    return config

@pytest.fixture
def sample_package():
    package = "test_package_123"
    package_dir = os.path.join("tests/acceptance_test/test_packages", package)
    if not os.path.exists(package_dir):
        os.mkdir(package_dir)
    txt_file = os.path.join(package_dir, f"{package}.txt")
    with open(txt_file, 'w+') as tfile:
        tfile.write("")
    create_tar_cmd = f"tar -czvf {package_dir}/{package}.tar.gz {package_dir}/{package}"
    subprocess.run(shlex.split(create_tar_cmd))
    return json.dumps({"package_path": f"{package}/{package}.tar.gz"})

############################    Tests   ##########################
def test_config_load(sample_config):
    assert "cloud_mqtt_address" in sample_config
    assert sample_config["cloud_mqtt_address"] == "localhost"

def test_publisher_e2e(sample_package, sample_config):
    with pytest.raises(Exception):
        topic = sample_config["package_receive_topic"]
        mosquitto = multiprocessing.Process(target=start_mosquitto, daemon=True)
        mosquitto.start()
        time.sleep(1)
        redis_server = multiprocessing.Process(target=start_redis_server, daemon=True)
        redis_server.start()
        time.sleep(1)
        receiver = multiprocessing.Process(target=package_receiver, args=(sample_config,), daemon=True)
        receiver.start()
        time.sleep(1)
        publish_sample_package_to_queue(topic, sample_package)
        time.sleep(5)
        publisher = multiprocessing.Process(target=package_publisher, args=(sample_config,), daemon=True)
        publisher.start()
        time.sleep(10)
        raise AssertionError

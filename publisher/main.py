import json
import logging
import os
import sys
import shutil
import time
import threading

from config.config_reader.config_factory import ConfigFactory
from config.utils import is_config_valid
from config.utils import get_config
from publisher.eventHandler.aggregator_handler import AggregatorServiceHandler
from publisher.utilities.mqtt import is_mqtt_running
from publisher.dataPublisher.publishRemote import CloudPublisher
from publisher.logger.logging import set_logging
from publisher.package_queue import PackageQueue
from publisher.utilities.encoder import Encoder
from publisher.dataPublisher.publishRemote import UnableToPublish

ini_parser = ConfigFactory.get_config(file_format='ini')
file_path = os.path.abspath('config/config_files/config.ini')
config = ini_parser.get_config(path=file_path)

def load_package_and_encode(package, storage_dir=None):
    """ receive a package(str) of format {package_path: "ts/ts.tar.gz"}
    deserialize the package (json.load) and encode (base64) the tar package
    and return the binary encoded string so that mqtt can publish it.
    """
    encoder = Encoder()
    package_json = json.loads(package)
    file_ = package_json["package_path"]
    binary_data = encoder.download_package_binary(
    os.path.join(storage_dir, file_))
    base64_encoded_string = encoder.encode_b64(binary_data)
    return (file_, base64_encoded_string)

def remove_package_directory_from_storage(package_path, storage_dir=None):
    """remove package from shared storage. package is usually
    removed after it is published.
    Format of package_path: "ts/ts.tar.gz"
    """
    package_dir = package_path.split('/')[0]
    dir_path = os.path.join(storage_dir, package_dir)
    shutil.rmtree(dir_path)
    logging.debug(f"This package content removed from disk {package_dir}")

def is_recording_package(package):
    check_str = "_recording"
    package_json = json.loads(package)
    pkg_path = package_json["package_path"]
    if check_str in pkg_path:
        return True
    else:
        return False

def discard_recording_package():
    if config['discard_recording_package'] == 'True':
        return True
    else:
        return False

def package_receiver(config):
    aggregator_handler_config = {
        "topic": config["package_receive_topic"],
        "queue_address": config["edge_mqtt_address"],
        "queue_port": int(config["edge_mqtt_port"]),
        "queue_keep_alive": int(config["package_receive_queue_keep_alive"]),
        "queue_qos": int(config["package_receive_queue_qos"]),
    }

    package_receiver = AggregatorServiceHandler(aggregator_handler_config)
    package_receiver.loop_forever()


def package_publisher(config):
    while not is_mqtt_running(config["cloud_mqtt_address"],
                              config["cloud_mqtt_port"]):
        time.sleep(10)
    cloud_publisher_config = {
        "topic": config["cloud_publish_topic"],
        "queue_address": config["cloud_mqtt_address"],
        "queue_port": int(config["cloud_mqtt_port"]),
        "queue_keep_alive": int(config["cloud_queue_keep_alive"]),
        "queue_qos": int(config["cloud_queue_qos"]),
        "enable_ssl": int(config["remote_publisher_enable_ssl"]),
        "ca_certs": config["ca_certs"],
        "certfile": config["client_cert"],
        "keyfile": config["client_key"]
    }
    cloud_publisher = CloudPublisher(cloud_publisher_config)
    publish_incremental_wait = config['publish_incremental_wait'].split()
    package_queue = PackageQueue()
    cloud_publisher.start_listening()
    while True:
        if  not package_queue.isEmpty():
                package = package_queue.head()
                if is_recording_package(package) and discard_recording_package():
                    logging.debug(f"Discarding following recording package: {package}")
                    package_json = json.loads(package)
                    pkg_path = package_json["package_path"]
                    package_queue.dequeue()
                    if config['delete_published_package'] == 'True':
                        remove_package_directory_from_storage(pkg_path)
                    continue

                try:
                    (file_, base64_encoded_string) = load_package_and_encode(package, storage_dir=config["container_storage"])
                    logging.debug(f"going to publish following package {file_}")
                    message_info = cloud_publisher.publish(base64_encoded_string)
                    if message_info is not None:
                        for wait in publish_incremental_wait:
                            start_time = time.time()
                            logging.debug(f"Starting to wait for server ack for {wait} seconds")
                            while not message_info.is_published():
                                time.sleep(1)
                                if time.time() > start_time + int(wait):
                                    break
                            if message_info.is_published():
                                break
                        if message_info.is_published():
                            logging.info(f"following package is published. {file_}")
                            # if published, then remove package from queue and storage
                            if config['delete_published_package'] == 'True':
                                remove_package_directory_from_storage(file_, storage_dir=config["container_storage"])
                            package_queue.dequeue()
                            logging.debug(f"PackageQueue size now is {package_queue.size()}")
                        else:
                            logging.debug(f"package {file_} could not be published. Enqueing again.")
                            package_queue.dequeue()
                            package_queue.enqueue(package)
                except UnableToPublish as e:
                    """ this happens generally when cloud mqtt broker is down,
                    or network error.
                    The package is re-enqueued into package queue.
                    """
                    logging.error(f"{e}")
                    time.sleep(0.5) #extra sleep to avoid cpu consumption in while loop if server is down
                except FileNotFoundError as e:
                    logging.error(f"{e}")
                    package_queue.dequeue()
                    logging.debug(f"No file for package {file_}. Removed from Queue")
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    config = get_config()
    set_logging(level=config["log_level"])
    # check if publisher id set in env, unique id required
    # to connect with broker.
    if 'PUBLISHER_ID' not in os.environ or not bool(os.environ['PUBLISHER_ID']):
        sys.exit("PUBLISHER_ID is not set in env or set to falsy values")
    if not is_config_valid():
        sys.exit("Config is not valid (missing some key)")
    try:
        t1 = threading.Thread(target=package_receiver, args=(config, ), daemon=True)
        t2 = threading.Thread(target=package_publisher, args=(config, ), daemon=False)
        # starting t1
        t1.start()
        # starting t2
        t2.start()
    except Exception as e:
        sys.exit(f"Exiting. Following Exception happened -> {e}")

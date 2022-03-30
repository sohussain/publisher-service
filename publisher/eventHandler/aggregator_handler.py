"""
@discription: aggregatorServiceHandler creates a queue which
subscribes to aggregator_service_topic and start listening
to incoming messages.
@author: abdullahrkw
"""
import logging
import threading 

from publisher.queue.queue import MessageQueue
from config.config_reader.config_factory import ConfigFactory
from config.utils import get_config
from publisher.package_queue import PackageQueue


def add_package_to_package_queue(package):
    packageQueue = PackageQueue()
    lock = threading.Lock()
    # this if-else is to avoid duplicate msg
    if (packageQueue.isEmpty()):
        lock.acquire()
        packageQueue.enqueue(package)
        lock.release()
    elif (package != packageQueue.peek()):
        lock.acquire()
        packageQueue.enqueue(package)
        lock.release()
    logging.info(f"PackageQueue size is {packageQueue.size()}")


# callback (called whenever violation_service_handler receives a message)
def read_for_violation_package(client, usrdata, msg):
    """ Callback called when an event(message) is read by the handler
    @note: Run on the client thread, and is blocking
    """
    try:
        decoded_message = str(msg.payload.decode("utf-8", "ignore"))
        logging.info(
            f"{usrdata} received message {decoded_message} with mid = {msg.mid}\
              on topic {msg.topic} with qos = {msg.qos}")
        add_package_to_package_queue(decoded_message)
    except Exception as e:
        logging.error(
            f"unexpected error occurred in {usrdata} while receiving message")
        logging.error(f"{e}")

def on_connect(client, userdata, flags, rc):
    """Callback function called after mqtt connection/reconnection
    
    Arguments:
        client {paho.mqtt.client.Client} -- [description]
        userdata {EdgeDataQueue} -- [description]
        flags {dict} -- [description]
        rc {int} -- Result code on connection
    """
    try:
        logging.debug(f"{userdata} Connected with result code {rc}")
        config = get_config()
        topic = config["package_receive_topic"]
        client.subscribe(topic=topic)
    except Exception as e:
        logging.error(f"Error handle before subscribing on_connect callback:{e}")


class AggregatorServiceHandler:
    def __init__(self, config):
        self.__queue = MessageQueue(
            address=config["queue_address"],
            port=int(config["queue_port"]),
            keep_alive=int(config["queue_keep_alive"]),
            qos=int(config["queue_qos"]),
            on_message=read_for_violation_package,
            on_connect=on_connect,
            client_id="aggregator_service_handler",
            user_data=self,
        )

    def __str__(self):
        return self.__queue.client_id

    def start_listening(self):
        self.__queue.start_loop()

    def loop_forever(self):
        self.__queue.loop_forever()

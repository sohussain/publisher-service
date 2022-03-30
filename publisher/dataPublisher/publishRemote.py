"""
@description: Creates a queue which publish aggregated
package to queue on cloud based mqtt.
@author: abdullahrkw
"""
import logging
import os

from publisher.queue.queue import MessageQueue


class UnableToPublish(Exception):
    pass

# callback function (called after a message has been published)
def after_publishing_package(client, userdata, mid):
    pass

class CloudPublisher(object):
    def __init__(self, config):
        self.cloud_publish_topic = config["topic"]
        self.address = config["queue_address"]
        self.port = int(config["queue_port"])
        self.keepalive = int(config["queue_keep_alive"])
        self.__queue = MessageQueue(
            address=config["queue_address"],
            port=int(config["queue_port"]),
            keep_alive=int(config["queue_keep_alive"]),
            qos=int(config["queue_qos"]),
            clean_session=True,
            on_publish=after_publishing_package,
            client_id=os.environ["PUBLISHER_ID"],
            user_data=self,
            enable_ssl=bool(config["enable_ssl"]),
            ca_certs=config["ca_certs"],
            certfile=config["certfile"],
            keyfile=config["keyfile"]
        )

    def __str__(self):
        return self.__queue.client_id

    def start_listening(self):
        self.__queue.start_loop()

    def publish(self, message):
        try:
            message_info = self.__queue.publish(self.cloud_publish_topic,
                                                message)
            return message_info
        except RuntimeError:
            raise UnableToPublish(f"{self.__queue.client_id} Unable to publish the msg")

    def reconnect(self):
        self.__queue.connect(address=self.address, port=self.port, keepalive=self.keepalive)

    def disconnect(self):
        self.__queue.disconnect()

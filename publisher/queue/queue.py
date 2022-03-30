"""
@description: Handle queue connection and messages
@original_author: @Bazarovey
@modified_by: abdullahrkw
"""
import paho.mqtt.client as mqtt
import logging
import ssl


def on_connect(client, userdata, flags, rc):
    """Callback function called after mqtt connection
    
    Arguments:
        client {[type]} -- [description]
        userdata {[type]} -- [description]
        flags {[type]} -- [description]
        rc {[type]} -- Result code on connection
    """
    logging.info(f"{userdata} Connected with result code {rc}")


def on_publish(client, userdata, mid):
    """Callback function called after publish ack recvd
    
    Arguments:
        client {[type]} -- [description]
        userdata {[type]} -- [description]
        mid {[type]} -- message id for the publish request
    """
    logging.info(f"Publish id {mid} ACK received")


def on_message(client, userdata, msg):
    """ Callback function called when message read """
    logging.info(f"{userdata} received Message : {msg}")


class Result:
    """Data structure to read client response"""

    state = 0
    message_id = 1


class State:
    """ Data structure to read state """

    success = 0
    fail = 1


class MessageQueue:
    def __init__(
        self,
        address=None,
        port=None,
        keep_alive=None,
        qos=None,
        on_connect=on_connect,
        on_publish=on_publish,
        on_message=on_message,
        user_data={},
        clean_session=False,
        client_id=None,
        enable_ssl=False,
        ca_certs=None,
        certfile=None,
        keyfile=None
    ):
        """Initialize queue client
        
        Quality of service 1 ensures
        that the message is delivered at least
        once. It is faster than QoS 2
        
        Keyword Arguments:
            address {[string]} -- [description] (default: {None})
            port {[int]} -- [description] (default: {None})
            keepalive {[int]} -- [description] (default: {None})
            qos {[int]} -- [Quality of service for the queue] (default: {None})
            on_connect {[string]} -- function to call on on connect
            on_publish {[string]} -- function to call on message publish
            on_message {[string]} -- function to call on message receive
            user_data {[string]} --  data which will be passed to callback functions
            clean_session {[boolean]} -- Persisting data. If false ensures that messages are
                                        presisted even when the client is dead 
            client_id {[string]} -- id of the client subscribing. Allows for persistance
        """
        self.quality_of_service = qos
        self.client_id = client_id
        self.client = mqtt.Client(client_id=client_id,
                                  clean_session=False,
                                  userdata=user_data)
        if enable_ssl == True:
            self.client.tls_set(ca_certs=ca_certs, 
                                certfile=certfile, 
                                keyfile=keyfile, 
                                cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLSv1_2, 
                                ciphers=None)
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.client.on_message = on_message
        self.client.connect(address, port=port, keepalive=keep_alive)
        logging.info(f"Client connection request made for {client_id}...")

    def __str__(self):
        return self.client_id

    def connect(self, address=None, port=None, keepalive=0):
        """ Start client connection
        """
        self.client.connect(address, port=port, keepalive=keepalive)
    
    def start_loop(self):
        """Start the client loop, non-blocking
        """
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_stop()

    def loop_forever(self):
        """Start the client loop, blocking
        """
        self.client.loop_forever()

    def publish(self, topic, message):
        """Publish message to a topic
        publish returns (response as (state, message id)) 
        Arguments:
            topic {[string]} -- [Topic to publish to]
            message {[type]} -- [Message to publish]
        """
        message_info = self.client.publish(topic,
                                           payload=message,
                                           qos=self.quality_of_service,
                                           retain=False)
        if message_info[
                Result.state] != State.success:  # 0 -> successful publish
            raise RuntimeError("Unable to publish message")
        return message_info

    def subscribe(self, topic):
        """ Subscribe to a particular topic
        @TODO should allow for a callback """
        self.client.subscribe(topic=topic, qos=self.quality_of_service)

    def disconnect(self):
        logging.info(
            f"Client disconnection request made for {self.client_id}...")
        self.client.disconnect()

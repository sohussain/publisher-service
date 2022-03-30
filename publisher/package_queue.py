"""
@description: class responsible for implementing
and maintaining a queue for received packages
@author: abdullahrkw
"""
import logging

from config.utils import get_config
from publisher.utilities.redis_queue import RedisQueue
from publisher.utilities.singleton_meta import Singleton


class PackageQueue(metaclass=Singleton):
    def __init__(self):
        """ Initialize RedisQueue and get current state of list copied
        """
        config = get_config()
        redis_host = config["redis_host"]
        redis_port = int(config["redis_port"])
        self.redis_queue = RedisQueue(redis_host, redis_port, key='packages')
        self._queue = self.redis_queue.get_current_list()

    def enqueue(self, element):
        """ Enqueue element in the program queue and make a copy in redis queue
        as well as backeup
        """
        self._queue.append(element)
        logging.debug(f"following package entered queue {element}")
        self.redis_queue.enqueue(element)

    def dequeue(self):
        """ Dequeue element from the program queue and from the backup queue
        stored on redis
        """
        popped_ele = self._queue.pop(0)
        logging.debug(f"following package left queue {popped_ele}")
        _ = self.redis_queue.dequeue()
        return popped_ele

    def peek(self):
        """ See last enetered element without removing
        """
        return self._queue[-1]

    def head(self):
        """ See the most first enetered element without removing
        """
        return self._queue[0]
        
    def isEmpty(self):
        return True if self.size() == 0 else False

    def size(self):
        return len(self._queue)

    def __str__(self):
        return "PackageQueue class(Singleton)"

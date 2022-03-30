"""
@description: class responsible for implementing
and maintaining a redis based queue for received packages
@author: abdullahrkw
"""
import logging

import redis

from publisher.utilities.singleton_meta import Singleton


class RedisQueue(metaclass=Singleton):
    def __init__(self, host, port, password=None, key='packages', db=1):
        """ Initialize redis connection
        raises ConnectionError - if redis server is not accessible
        """
        self.host = host
        self.port = port
        self.password = password
        self.key = key
        self.db = db
        self.connect()
    
    def connect(self):
        while True:
            if RedisQueue.redis_server_is_running(self.host, self.port, password=self.password):
                self.redis_client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
                break
            else:
                logging.warn(f"Couldn't connect with redis server at {self.host}:{self.port}")
                time.sleep(0.5)

    def enqueue(self, element):
        try:
            self.redis_client.rpush(self.key, element)
            logging.debug(f"following package entered redis queue {element}")
        except ConnectionError as e:
            self.connect()
            self.redis_client.rpush(self.key, element)

    def dequeue(self):
        try:
            popped_ele = self.redis_client.lpop(self.key)
            logging.debug(f"following package left redis queue {popped_ele}")
        except ConnectionError as e:
            self.connect()
            popped_ele = self.redis_client.lpop(self.key)
        finally:
            return popped_ele

    def peek(self):
        return self.redis_client.lindex(name=self.key, index=-1)

    def head(self):
        return self.redis_client.lindex(name=self.key, index=0)
        
    def isEmpty(self):
        return True if self.size() == 0 else False
    
    def get_current_list(self):
        return self.redis_client.lrange(name=self.key, start=0, end=-1)

    def size(self):
        return self.redis_client.llen(self.key)

    @staticmethod
    def redis_server_is_running(host, port, password=None):
        """Test if redis server is accessible.
        Returns:
            [boolean] -- True if running, else false
        """
        try:
            r = redis.StrictRedis(host=host, port=port, password=password)
            r.ping()
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Can't connect to the redis-server at {host}:{port}.")
            logging.error(e)
            return False
        return True

    def __str__(self):
        return "Redis based PackageQueue class(Singleton)"

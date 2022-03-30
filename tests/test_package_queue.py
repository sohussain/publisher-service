"""
@description: tests package_queue, package_queue is being accessed by two different threads.
One thread enqueue data, other dequeue data
@author: abdullahrkw
"""
import pytest
from redis import StrictRedis

from publisher.package_queue import PackageQueue
from publisher.utilities.redis_queue import RedisQueue

# @TODO make this monkeypatching work to avoid redis external calls and 
# then remove pytest test skipping decorator
@pytest.fixture(autouse=True)
def no_request_to_redis_queue(monkeypatch):
    monkeypatch.setitem(StrictRedis,'rpush', None)
    monkeypatch.setitem(StrictRedis,'lpop', None)    
    monkeypatch.setitem(RedisQueue,'get_current_list',[])


@pytest.fixture
def queue():
    queue = PackageQueue()
    return queue

@pytest.mark.skip
def test_package_queue_is_singleton():
    q1 = PackageQueue()
    q2 = PackageQueue()
    assert q1 is q2

@pytest.mark.skip
def test_package_queue_is_fifo(queue):
    """
    Yes, it looks like code smell but Reason for putting all assert here.
    PackageQueue is singleton, so, if i test one method, i need to clean the queue
    to test the other method. So, it's better to put all assert at one place.
    Don't you agree?
    Notify me at @abdullahrkw
    """
    queue.enqueue("abc")
    queue.enqueue("def")
    queue.enqueue("ghi")
    assert queue.peek() == "ghi"
    assert queue.dequeue() == "abc"
    assert queue.dequeue() == "def"
    assert queue.dequeue() == "ghi"
    assert queue.isEmpty()

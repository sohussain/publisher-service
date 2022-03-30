"""
@discription: this tests singleton meta
class which creates Singletons
@author: abdullahrkw
"""
from publisher.utilities.singleton_meta import Singleton


def test_if_singleton_meta_class_creates_singletns():
    class A(metaclass=Singleton):
        def __init__(self):
            pass

    a_obj = A()
    b_obj = A()
    assert a_obj is b_obj

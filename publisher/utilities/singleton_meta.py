"""
@discription metaclass to create singleton: a metaclass is a class whose instances are also classes
@author abdullahrkw
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ metaclass for creating singlaton
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]

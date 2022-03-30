"""
@discription: abstract class implementation in python
to create config interface so child classes can implement
all sort of config files, ini, toml, yaml, etc
@author: abdullahrkw
"""
from abc import ABC, abstractmethod


class IConfig(ABC):
    @abstractmethod
    def get_config(self, path):
        pass

"""
@description: test config_factory
@author: abdullahrkw
"""

from config.config_reader.config_factory import ConfigFactory
from config.config_reader.iconfig import IConfig


def test_configreader_factory():
    ini_parser = ConfigFactory.get_config(file_format='ini', )
    assert isinstance(ini_parser, IConfig)

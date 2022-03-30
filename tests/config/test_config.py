"""
@discription: test ini and yaml config
files by reading from them
@author: abdullahrkw
"""

import os
import pytest
from unittest.mock import patch

from config.config_reader.config_factory import ConfigFactory
from config.utils import is_config_valid


@patch.dict('os.environ', {'MODE': 'TESTING'})
def test_ini_parser():
    ini_parser = ConfigFactory.get_config(file_format='ini', )
    file_path = os.path.abspath("tests/config/test_config.ini")
    config = ini_parser.get_config(file_path)
    assert isinstance(config, dict)


def test_if_config_file_being_parsed_accurately():
    ini_parser = ConfigFactory.get_config(file_format='ini', )
    file_path = os.path.abspath("tests/config/test_config.ini")
    with patch.dict('os.environ', {'MODE': 'TESTING'}):
        config = ini_parser.get_config(file_path)
        assert config["address"] == '0.0.0.0'
        assert int(config["port"]) == 1883

    with patch.dict('os.environ', {'MODE': 'STAGING'}):
        config = ini_parser.get_config(file_path)
        assert config["address"] == 'https://pypo.com'


@patch.dict('os.environ', {'MODE': 'TESTING'})
def test_if_exception_raised_if_no_key_found():
    with pytest.raises(KeyError):
        ini_parser = ConfigFactory.get_config(file_format='ini', )
        file_path = os.path.abspath("tests/config/test_config.ini")
        config = ini_parser.get_config(file_path)
        _ = config["abc"]


def test_if_config_valid():
    assert is_config_valid()

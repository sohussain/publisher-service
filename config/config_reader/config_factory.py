"""
@discription: factory method to get desired config parser
@author: abdullahrkw
"""
from config.config_reader.ini_parser import IniParser


class ConfigFactory:
    @staticmethod
    def get_config(file_format=None):
        if (file_format == 'ini'):
            ini_parser = IniParser()
            return ini_parser
        else:
            raise ValueError(f"{file_format} is not supported yet")

"""
@discription: Implements ICONFIG by parsing ini 
files
@auther: abdullahrkw
"""
import configparser
import errno
import logging
import os

from config.config_reader.iconfig import IConfig


class IniParser(IConfig):
    def __init__(self):
        pass

    def is_file_exists(self, path):
        return os.path.isfile(path)

    def get_config(self, path):
        config = configparser.ConfigParser()
        # config.read(path)
        if (self.is_file_exists(path)):
            config.read(path)
        else:
            logging.error(f"file at path {path} doesn't exist")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    path)
        return dict(config[os.getenv('MODE')])

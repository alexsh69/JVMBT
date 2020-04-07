from flask_api import status
import requests
import yaml
import os


class ConfigManager(object):
    def __init__(self):
        self._config_path = os.getenv("CONFIG_PATH", os.path.join(os.getcwd(), "config.yml"))
        self.config = self.__parse_config()

    def __parse_config(self):
        with open(self._config_path) as _config_file:
            return yaml.load(_config_file, Loader=yaml.Loader)

    @property
    def get_builds(self):
        return self.config['build']

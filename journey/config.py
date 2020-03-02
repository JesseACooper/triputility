from configparser import ConfigParser

import os

class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.paths = [os.path.join(os.path.expanduser("~"), ".journey-cli.ini"), "config.ini"]
        self.config.read(self.paths)

    def persist(self):
        with open(self.path, "w") as f:
            self.config.write(f)

    def set(self, configuration, value):
        self.config["DEFAULT"][configuration] = value
        self.persist()

    def get(self, configuration):
        try:
            return self.config["DEFAULT"][configuration]
        except KeyError as error:
            return None

    @property
    def redash_api_key(self):
        return self.get("redash_api_key")

from configparser import ConfigParser


class Config:
    def __init__(self, path=None):
        self.config = ConfigParser()
        self.path = path
        self.config.read(self.path)

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

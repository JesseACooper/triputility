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
        return self.config["DEFAULT"][configuration]

    @property
    def aws_access_key_id(self):
        return self.get("aws_access_key_id")

    @property
    def aws_secret_access_key(self):
        return self.get("aws_secret_access_key")

    @property
    def aws_session_token(self):
        return self.get("aws_session_token")

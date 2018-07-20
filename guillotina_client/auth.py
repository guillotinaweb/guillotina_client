from base64 import b64encode


class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def token(self):
        return b64encode(f'{self.username}:{self.password}'.encode()).decode()

    @property
    def authorization(self):
        return f'Basic {self.token}'

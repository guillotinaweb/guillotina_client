from guillotina.glogging import Logger

logger = Logger(__name__)


class BaseException(Exception):
    def __init__(self, message=''):
        logger.error(message)


class AlreadyExistsException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)


class NotExistsException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)


class UnauthorizedException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)
    pass


class RetriableAPIException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)
    pass


class LoginFailedException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)
    pass


class RefreshTokenFailedException(BaseException):
    def __init__(self, message=''):
        super().__init__(message)

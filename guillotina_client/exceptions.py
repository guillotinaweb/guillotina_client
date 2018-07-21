class AlreadyExistsException(Exception):
    pass


class NotExistsException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class RetriableAPIException(Exception):
    pass


class LoginFailedException(Exception):
    pass


class RefreshTokenFailedException(Exception):
    pass

class AlreadyExistsException(Exception):
    pass


class NotExistsException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class RetriableAPIException(Exception):
    pass

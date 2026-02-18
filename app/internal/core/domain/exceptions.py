"""domain exceptions"""


class DomainException(Exception):
    pass


class DuplicateEmailError(DomainException):
    pass


class UserNotFoundError(DomainException):
    pass


class ValidationError(DomainException):
    pass

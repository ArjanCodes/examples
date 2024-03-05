class BaseError(Exception):
    """base exception class"""

    def __init__(self, message: str = "An error occurred", name: str = "SkyPulse"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(BaseError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class EntityDoesNotExistError(BaseError):
    """database returns nothing"""

    pass


class EntityAlreadyExistsError(BaseError):
    """conflict detected, like trying to create a resource that already exists"""

    pass


class InvalidOperationError(BaseError):
    """invalid operations like trying to delete a non-existing entity, etc."""

    pass


class AuthenticationFailed(BaseError):
    """invalid authentication credentials"""

    pass


class InvalidTokenError(BaseError):
    """invalid token"""

    pass

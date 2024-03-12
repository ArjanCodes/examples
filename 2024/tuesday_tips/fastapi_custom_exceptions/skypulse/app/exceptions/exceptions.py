class SkyPulseApiError(Exception):
    """base exception class"""

    def __init__(self, message: str = "An error occurred", name: str = "SkyPulse"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(SkyPulseApiError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class EntityDoesNotExistError(SkyPulseApiError):
    """database returns nothing"""

    pass


class EntityAlreadyExistsError(SkyPulseApiError):
    """conflict detected, like trying to create a resource that already exists"""

    pass


class InvalidOperationError(SkyPulseApiError):
    """invalid operations like trying to delete a non-existing entity, etc."""

    pass


class AuthenticationFailed(SkyPulseApiError):
    """invalid authentication credentials"""

    pass


class InvalidTokenError(SkyPulseApiError):
    """invalid token"""

    pass

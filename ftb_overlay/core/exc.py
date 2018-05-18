"""ftb-overlay exception classes."""


class ftboError(Exception):
    """Generic errors."""

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class ftboConfigError(ftboError):
    """Config related errors."""
    pass


class ftboRuntimeError(ftboError):
    """Generic runtime errors."""
    pass


class ftboArgumentError(ftboError):
    """Argument related errors."""
    pass

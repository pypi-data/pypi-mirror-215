class InvalidJWT(Exception):
    """Invalid JWT Token"""


class NodeUnhealthy(ConnectionError):
    """IOTA node health check returns non-200 status code"""


class NodeInternalServerError(Exception):
    """IOTA node internal error"""


class MessageNotFound(Exception):
    """Message not found"""


class UnknownError(Exception):
    """Unexpected errors"""


class MessageVerificationFailed(Exception):
    """Failed to verify message"""

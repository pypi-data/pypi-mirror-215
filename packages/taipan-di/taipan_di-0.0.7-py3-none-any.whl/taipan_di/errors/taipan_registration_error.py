from taipan_di.errors.taipan_error import TaipanError

__all__ = ["TaipanRegistrationError"]


class TaipanRegistrationError(TaipanError):
    """
    Exception indicating an error occurred during the registration process.
    """

    pass

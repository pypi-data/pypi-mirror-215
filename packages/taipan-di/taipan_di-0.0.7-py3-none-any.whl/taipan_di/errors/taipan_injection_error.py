from taipan_di.errors.taipan_error import TaipanError

__all__ = ["TaipanInjectionError"]


class TaipanInjectionError(TaipanError):
    """
    Exception indicating an error occurred during the service injection process.
    """

    pass

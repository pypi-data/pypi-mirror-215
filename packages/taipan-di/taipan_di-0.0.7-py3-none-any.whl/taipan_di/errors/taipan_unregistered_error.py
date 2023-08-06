from taipan_di.errors.taipan_error import TaipanError

__all__ = ["TaipanUnregisteredError"]


class TaipanUnregisteredError(TaipanError):
    """
    Exception indicating that you tried to resolved a service that wasn't registered
    """

    pass

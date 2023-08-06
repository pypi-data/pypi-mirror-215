from .data import EventType


class AppEvent:
    """Module with which you can define aws events like cognito, sqs, sns etc."""

    def __init__(self):
        self.triggers: dict[str, tuple[callable, str]] = dict()

    def event(self, _type: EventType, subtype: str = None, qualifier: str = None):
        def _event(func: callable):
            self.triggers[f"{_type.value}::{subtype}" if subtype else str(_type.value)] = func, qualifier
            return func

        return _event

    def cognito(self, trigger_source: str = None):
        return self.event(EventType.cognito, trigger_source)

    def sqs(self):
        return self.event(EventType.sqs)

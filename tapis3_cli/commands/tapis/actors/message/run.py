from .base import ActorsMessage

__all__ = ["ActorsRun"]


class ActorsRun(ActorsMessage):
    """Send a message an Actor and await response."""

    SYNCHRONOUS_EXECUTION = True

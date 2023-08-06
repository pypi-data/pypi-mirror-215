"""Payload tagger errors."""
from __future__ import annotations

from typing import Any


class NotIdentifiedPayloadError(Exception):
    """Raised when payload cannot be identified."""

    def __init__(self, payload: dict[str, Any]) -> None:  # noqa: D107
        super().__init__(f"payload {payload} couldn't be identified.")

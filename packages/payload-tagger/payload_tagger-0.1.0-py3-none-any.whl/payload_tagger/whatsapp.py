"""Whatsapp payload tagger."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from result import Err, Ok
from typing_extensions import Literal, TypeAlias

from payload_tagger import errors

if TYPE_CHECKING:
    from result import Result


SupportedWebhooks: TypeAlias = Literal[
    "text-message",
    "reaction-message",
    "media-message",
    "location-message",
    "contact-message",
    "received-callback-from-quick-reply-button",
    "received-answer-from-list-message",
    "received-answer-to-reply-button",
]


def _has_messages(payload_changes: dict[str, Any]) -> bool:
    return (
        "value" in payload_changes and "messages" in payload_changes["value"]
    )


def _has_type(payload_changes: dict[str, Any]) -> bool:
    return "type" in payload_changes["value"]["messages"][0]


def _is_text_message(payload_changes: dict[str, Any]) -> bool:
    if (
        "referral" not in payload_changes["value"]["messages"][0]
        and "context" not in payload_changes["value"]["messages"][0]
        and payload_changes["value"]["messages"][0]["type"] == "text"
    ):
        return True
    return False


def _is_reaction_message(payload_changes: dict[str, Any]) -> bool:
    if payload_changes["value"]["messages"][0]["type"] == "reaction":
        return True
    return False


def _is_media_message(payload_changes: dict[str, Any]) -> bool:
    if payload_changes["value"]["messages"][0]["type"] in ["image", "sticker"]:
        return True
    return False


def _is_location_message(payload_changes: dict[str, Any]) -> bool:
    if "location" in payload_changes["value"]["messages"][0]:
        return True
    return False


def _is_contact_message(payload_changes: dict[str, Any]) -> bool:
    if "contacts" in payload_changes["value"]["messages"][0]:
        return True
    return False


def _is_received_callback_from_quick_reply_button(
    payload_changes: dict[str, Any],
) -> bool:
    if payload_changes["value"]["messages"][0]["type"] == "button":
        return True
    return False


def _is_received_answer_from_list_message(
    payload_changes: dict[str, Any],
) -> bool:
    if (
        payload_changes["value"]["messages"][0]["type"] == "interactive"
        and payload_changes["value"]["messages"][0]["interactive"]["type"]
        == "list_reply"
    ):
        return True
    return False


def _is_received_answer_to_reply_button(
    payload_changes: dict[str, Any],
) -> bool:
    if (
        payload_changes["value"]["messages"][0]["type"] == "interactive"
        and payload_changes["value"]["messages"][0]["interactive"]["type"]
        == "button_reply"
    ):
        return True
    return False


def _message_changes(
    payload: dict[str, Any],
) -> Result[dict[str, Any], errors.NotIdentifiedPayloadError]:
    payload_entry: list[dict[str, Any]] | None = payload.get("entry", None)
    if not payload_entry:
        return Err(errors.NotIdentifiedPayloadError(payload=payload))
    changes: list[dict[str, Any]] | None = payload_entry[0].get(
        "changes",
        None,
    )
    if not changes:
        return Err(errors.NotIdentifiedPayloadError(payload=payload))
    return Ok(changes[0])


def identify_payload(  # noqa: C901, PLR0912
    payload: dict[str, Any],
) -> Result[SupportedWebhooks, errors.NotIdentifiedPayloadError]:
    """Identify Whatsapp payload."""
    identified: SupportedWebhooks

    changes_retrieved = _message_changes(payload=payload)
    if not isinstance(changes_retrieved, Ok):
        return changes_retrieved

    changes = changes_retrieved.unwrap()

    if not _has_messages(payload_changes=changes):
        return Err(errors.NotIdentifiedPayloadError(payload=payload))

    if not _has_type(payload_changes=changes):
        if _is_location_message(payload_changes=changes):
            identified = "location-message"
        elif _is_contact_message(payload_changes=changes):
            identified = "contact-message"
        else:
            return Err(errors.NotIdentifiedPayloadError(payload=payload))
        return Ok(identified)

    if _is_text_message(payload_changes=changes):
        identified = "text-message"
    elif _is_reaction_message(payload_changes=changes):
        identified = "reaction-message"
    elif _is_media_message(payload_changes=changes):
        identified = "media-message"
    elif _is_received_callback_from_quick_reply_button(
        payload_changes=changes,
    ):
        identified = "received-callback-from-quick-reply-button"
    elif _is_received_answer_from_list_message(
        payload_changes=changes,
    ):
        identified = "received-answer-from-list-message"
    elif _is_received_answer_to_reply_button(payload_changes=changes):
        identified = "received-answer-to-reply-button"
    else:
        return Err(errors.NotIdentifiedPayloadError(payload=payload))

    return Ok(identified)

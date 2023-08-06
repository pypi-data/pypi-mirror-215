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
    msgs: dict[str, Any] = payload_changes["value"]["messages"][0]
    if (
        "referral" not in msgs
        and "context" not in msgs
        and msgs["type"] == "text"
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
    msgs: dict[str, Any] = payload_changes["value"]["messages"][0]
    if (
        msgs["type"] == "interactive"
        and msgs["interactive"]["type"] == "list_reply"
    ):
        return True
    return False


def _is_received_answer_to_reply_button(
    payload_changes: dict[str, Any],
) -> bool:
    msgs: dict[str, Any] = payload_changes["value"]["messages"][0]
    if (
        msgs["type"] == "interactive"
        and msgs["interactive"]["type"] == "button_reply"
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


def _identify_payload_no_type(
    payload_changes: dict[str, Any],
) -> SupportedWebhooks | None:
    identified: SupportedWebhooks

    if _is_location_message(payload_changes=payload_changes):
        identified = "location-message"
    elif _is_contact_message(payload_changes=payload_changes):
        identified = "contact-message"
    else:
        return None
    return identified


def _identify_core_msgs(
    payload_changes: dict[str, Any],
) -> SupportedWebhooks | None:
    identified: SupportedWebhooks
    if _is_text_message(payload_changes=payload_changes):
        identified = "text-message"
    elif _is_reaction_message(payload_changes=payload_changes):
        identified = "reaction-message"
    elif _is_media_message(payload_changes=payload_changes):
        identified = "media-message"
    elif _is_received_callback_from_quick_reply_button(
        payload_changes=payload_changes,
    ):
        identified = "received-callback-from-quick-reply-button"
    elif _is_received_answer_from_list_message(
        payload_changes=payload_changes,
    ):
        identified = "received-answer-from-list-message"
    elif _is_received_answer_to_reply_button(payload_changes=payload_changes):
        identified = "received-answer-to-reply-button"
    else:
        return None
    return identified


def identify_payload(
    payload: dict[str, Any],
) -> Result[SupportedWebhooks, errors.NotIdentifiedPayloadError]:
    """Identify Whatsapp payload."""
    changes_retrieved = _message_changes(payload=payload)
    if not isinstance(changes_retrieved, Ok):
        return changes_retrieved

    changes = changes_retrieved.unwrap()

    if not _has_messages(payload_changes=changes):
        return Err(errors.NotIdentifiedPayloadError(payload=payload))

    if not _has_type(payload_changes=changes):
        identity = _identify_payload_no_type(payload_changes=changes)
        if identity:
            return Ok(identity)
        return Err(errors.NotIdentifiedPayloadError(payload=payload))

    identity = _identify_core_msgs(payload_changes=changes)
    if identity:
        return Ok(identity)
    return Err(errors.NotIdentifiedPayloadError(payload=payload))

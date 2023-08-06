"""Test whatsapp."""
from __future__ import annotations

from typing import Any

import pytest

from payload_tagger import errors, whatsapp


@pytest.mark.unit()
@pytest.mark.parametrize(
    argnames=["payload", "expected"],
    argvalues=[
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "PHONE_NUMBER",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "text": {
                                                "body": "MESSAGE_BODY",
                                            },
                                            "type": "text",
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "text-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "PHONE_NUMBER",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "reaction": {
                                                "message_id": "MESSAGE_ID",
                                                "emoji": "EMOJI",
                                            },
                                            "type": "reaction",
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "reaction-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "WHATSAPP_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "type": "image",
                                            "image": {
                                                "caption": "CAPTION",
                                                "mime_type": "image/jpeg",
                                                "sha256": "IMAGE_HASH",
                                                "id": "ID",
                                            },
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "media-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "WHATSAPP_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "location": {
                                                "latitude": "LOCATION_LATITUDE",  # noqa: E501
                                                "longitude": "LOCATION_LONGITUDE",  # noqa: E501
                                                "name": "LOCATION_NAME",
                                                "address": "LOCATION_ADDRESS",
                                            },
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "location-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "WHATSAPP_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "contacts": [
                                                {
                                                    "addresses": [
                                                        {
                                                            "city": "CONTACT_CITY",  # noqa: E501
                                                            "country": "CONTACT_COUNTRY",  # noqa: E501
                                                            "country_code": "CONTACT_COUNTRY_CODE",  # noqa: E501
                                                            "state": "CONTACT_STATE",  # noqa: E501
                                                            "street": "CONTACT_STREET",  # noqa: E501
                                                            "type": "HOME or WORK",  # noqa: E501
                                                            "zip": "CONTACT_ZIP",  # noqa: E501
                                                        },
                                                    ],
                                                    "birthday": "CONTACT_BIRTHDAY",  # noqa: E501
                                                    "emails": [
                                                        {
                                                            "email": "CONTACT_EMAIL",  # noqa: E501
                                                            "type": "WORK or HOME",  # noqa: E501
                                                        },
                                                    ],
                                                    "name": {
                                                        "formatted_name": "CONTACT_FORMATTED_NAME",  # noqa: E501
                                                        "first_name": "CONTACT_FIRST_NAME",  # noqa: E501
                                                        "last_name": "CONTACT_LAST_NAME",  # noqa: E501
                                                        "middle_name": "CONTACT_MIDDLE_NAME",  # noqa: E501
                                                        "suffix": "CONTACT_SUFFIX",  # noqa: E501
                                                        "prefix": "CONTACT_PREFIX",  # noqa: E501
                                                    },
                                                    "org": {
                                                        "company": "CONTACT_ORG_COMPANY",  # noqa: E501
                                                        "department": "CONTACT_ORG_DEPARTMENT",  # noqa: E501
                                                        "title": "CONTACT_ORG_TITLE",  # noqa: E501
                                                    },
                                                    "phones": [
                                                        {
                                                            "phone": "CONTACT_PHONE",  # noqa: E501
                                                            "wa_id": "CONTACT_WA_ID",  # noqa: E501
                                                            "type": "HOME or WORK>",  # noqa: E501
                                                        },
                                                    ],
                                                    "urls": [
                                                        {
                                                            "url": "CONTACT_URL",  # noqa: E501
                                                            "type": "HOME or WORK",  # noqa: E501
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "contact-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "WHATSAPP_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "context": {
                                                "from": "PHONE_NUMBER",
                                                "id": "wamid.ID",
                                            },
                                            "from": "16315551234",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "type": "button",
                                            "button": {
                                                "text": "No",
                                                "payload": "No-Button-Payload",
                                            },
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "received-callback-from-quick-reply-button",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "PHONE_NUMBER_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER_ID",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "interactive": {
                                                "list_reply": {
                                                    "id": "list_reply_id",
                                                    "title": "list_reply_title",  # noqa: E501
                                                    "description": "list_reply_description",  # noqa: E501
                                                },
                                                "type": "list_reply",
                                            },
                                            "type": "interactive",
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "received-answer-from-list-message",
        ),
        (
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                        "changes": [
                            {
                                "value": {
                                    "messaging_product": "whatsapp",
                                    "metadata": {
                                        "display_phone_number": "PHONE_NUMBER",
                                        "phone_number_id": "PHONE_NUMBER_ID",
                                    },
                                    "contacts": [
                                        {
                                            "profile": {
                                                "name": "NAME",
                                            },
                                            "wa_id": "PHONE_NUMBER_ID",
                                        },
                                    ],
                                    "messages": [
                                        {
                                            "from": "PHONE_NUMBER_ID",
                                            "id": "wamid.ID",
                                            "timestamp": "TIMESTAMP",
                                            "interactive": {
                                                "button_reply": {
                                                    "id": "unique-button-identifier-here",  # noqa: E501
                                                    "title": "button-text",
                                                },
                                                "type": "button_reply",
                                            },
                                            "type": "interactive",
                                        },
                                    ],
                                },
                                "field": "messages",
                            },
                        ],
                    },
                ],
            },
            "received-answer-to-reply-button",
        ),
    ],
)
def test_identify_payload(
    payload: dict[str, Any],
    expected: whatsapp.SupportedWebhooks,
) -> None:
    """Test identify payload works."""
    assert whatsapp.identify_payload(payload=payload).unwrap() == expected


@pytest.mark.unit()
@pytest.mark.parametrize(
    argnames="payload",
    argvalues=[
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "BUSINESS_DISPLAY_PHONE_NUMBER",  # noqa: E501
                                    "phone_number_id": "BUSINESS_PHONE_NUMBER_ID",  # noqa: E501
                                },
                                "statuses": [
                                    {
                                        "id": "WHATSAPP_MESSAGE_ID",
                                        "status": "sent",
                                        "timestamp": "TIMESTAMP",
                                        "recipient_id": "CUSTOMER_PHONE_NUMBER",  # noqa: E501
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "CONVERSATION_EXPIRATION_TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "user_initiated",
                                            },
                                        },
                                        "pricing": {
                                            "billable": "true",
                                            "pricing_model": "CBP",
                                            "category": "user_initiated",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {},
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "recipient_id": "PHONE_NUMBER",
                                        "status": "sent",
                                        "timestamp": "TIMESTAMP",
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "business_initated",
                                            },
                                        },
                                        "pricing": {
                                            "pricing_model": "CBP",
                                            "billable": "true",
                                            "category": "business_initated",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "status": "sent",
                                        "timestamp": "TIMESTAMP",
                                        "recipient_id": "PHONE_NUMBER",
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "referral_conversion",
                                            },
                                        },
                                        "pricing": {
                                            "billable": "false",
                                            "pricing_model": "CBP",
                                            "category": "referral_conversion",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "recipient_id": "PHONE_NUMBER",
                                        "status": "delivered",
                                        "timestamp": "TIMESTAMP",
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "user_initiated",
                                            },
                                        },
                                        "pricing": {
                                            "pricing_model": "CBP",
                                            "billable": "true",
                                            "category": "user_initiated",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "recipient_id": "PHONE_NUMBER",
                                        "status": "delivered",
                                        "timestamp": "TIMESTAMP",
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "user_initiated",
                                            },
                                        },
                                        "pricing": {
                                            "pricing_model": "CBP",
                                            "billable": "true",
                                            "category": "user_initiated",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "status": "sent",
                                        "timestamp": "TIMESTAMP",
                                        "recipient_id": "PHONE_NUMBER",
                                        "conversation": {
                                            "id": "CONVERSATION_ID",
                                            "expiration_timestamp": "TIMESTAMP",  # noqa: E501
                                            "origin": {
                                                "type": "referral_conversion",
                                            },
                                        },
                                        "pricing": {
                                            "billable": "false",
                                            "pricing_model": "CBP",
                                            "category": "referral_conversion",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "BUSINESS_DISPLAY_PHONE_NUMBER",  # noqa: E501
                                    "phone_number_id": "BUSINESS_PHONE_NUMBER_ID",  # noqa: E501
                                },
                                "statuses": [
                                    {
                                        "id": "WHATSAPP_MESSAGE_ID",
                                        "status": "read",
                                        "timestamp": "TIMESTAMP",
                                        "recipient_id": "CUSTOMER_PHONE_NUMBER",  # noqa: E501
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER",
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "NAME",
                                        },
                                        "wa_id": "PHONE_NUMBER",
                                    },
                                ],
                                "messages": [
                                    {
                                        "from": "PHONE_NUMBER",
                                        "id": "wamid.ID",
                                        "timestamp": "TIMESTAMP",
                                        "errors": [
                                            {
                                                "code": 131051,
                                                "details": "Message type is not currently supported",  # noqa: E501
                                                "title": "Unsupported message type",  # noqa: E501
                                            },
                                        ],
                                        "type": "unsupported",
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "statuses": [
                                    {
                                        "id": "wamid.ID",
                                        "status": "failed",
                                        "timestamp": "TIMESTAMP",
                                        "recipient_id": "PHONE_NUMBER",
                                        "errors": [
                                            {
                                                "code": 131014,
                                                "title": "Request for url https://URL.jpg failed with error: 404 (Not Found)",  # noqa: E501
                                            },
                                        ],
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "NAME",
                                        },
                                        "wa_id": "ID",
                                    },
                                ],
                                "messages": [
                                    {
                                        "referral": {
                                            "source_url": "AD_OR_POST_FB_URL",
                                            "source_id": "ADID",
                                            "source_type": "ad or post",
                                            "headline": "AD_TITLE",
                                            "body": "AD_DESCRIPTION",
                                            "media_type": "image or video",
                                            "image_url": "RAW_IMAGE_URL",
                                            "video_url": "RAW_VIDEO_URL",
                                            "thumbnail_url": "RAW_THUMBNAIL_URL",  # noqa: E501
                                        },
                                        "from": "SENDER_PHONE_NUMBERID",
                                        "id": "wamid.ID",
                                        "timestamp": "TIMESTAMP",
                                        "type": "text",
                                        "text": {
                                            "body": "BODY",
                                        },
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "NAME",
                                        },
                                        "wa_id": "PHONE_NUMBER_ID",
                                    },
                                ],
                                "messages": [
                                    {
                                        "from": "PHONE_NUMBER",
                                        "id": "wamid.ID",
                                        "text": {
                                            "body": "MESSAGE_TEXT",
                                        },
                                        "context": {
                                            "from": "PHONE_NUMBER",
                                            "id": "wamid.ID",
                                            "referred_product": {
                                                "catalog_id": "CATALOG_ID",
                                                "product_retailer_id": "PRODUCT_ID",  # noqa: E501
                                            },
                                        },
                                        "timestamp": "TIMESTAMP",
                                        "type": "text",
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "8856996819413533",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "16505553333",
                                    "phone_number_id": "phone-number-id",
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "Kerry Fisher",
                                        },
                                        "wa_id": "16315551234",
                                    },
                                ],
                                "messages": [
                                    {
                                        "from": "16315551234",
                                        "id": "wamid.ABGGFlCGg0cvAgo6cHbBhfK5760V",  # noqa: E501
                                        "order": {
                                            "catalog_id": "the-catalog_id",
                                            "product_items": [
                                                {
                                                    "product_retailer_id": "the-product-SKU-identifier",  # noqa: E501
                                                    "quantity": "number-of-item",  # noqa: E501
                                                    "item_price": "unitary-price-of-item",  # noqa: E501
                                                    "currency": "price-currency",  # noqa: E501
                                                },
                                                ...,
                                            ],
                                            "text": "text-message-sent-along-with-the-order",  # noqa: E501
                                        },
                                        "context": {
                                            "from": "16315551234",
                                            "id": "wamid.gBGGFlaCGg0xcvAdgmZ9plHrf2Mh-o",  # noqa: E501
                                        },
                                        "timestamp": "1603069091",
                                        "type": "order",
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
        {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE_NUMBER",
                                    "phone_number_id": "PHONE_NUMBER_ID",
                                },
                                "messages": [
                                    {
                                        "from": "PHONE_NUMBER",
                                        "id": "wamid.ID",
                                        "system": {
                                            "body": "NAME changed from PHONE_NUMBER to PHONE_NUMBER",  # noqa: E501
                                            "new_wa_id": "NEW_PHONE_NUMBER",
                                            "type": "user_changed_number",
                                        },
                                        "timestamp": "TIMESTAMP",
                                        "type": "system",
                                    },
                                ],
                            },
                            "field": "messages",
                        },
                    ],
                },
            ],
        },
    ],
)
def test_not_identify_payload(
    payload: dict[str, Any],
) -> None:
    """Test failure to identify payload."""
    assert isinstance(
        whatsapp.identify_payload(payload=payload).err(),
        errors.NotIdentifiedPayloadError,
    )

"""Base skeleton for Slack section elements."""

from typing import Type, TypeVar, Union

from pydantic import BaseModel, Field, validator

from ..core import (
    _Button,
    _ChannelsSelect,
    _Checkboxes,
    _ConversationsSelect,
    _Datepicker,
    _Image,
    _LinkButton,
    _MarkdownText,
    _MultiConversationsSelect,
    _MultiStaticSelect,
    _Overflow,
    _PlainText,
    _RadioButtons,
    _StaticSelect,
    _Timepicker,
    _UsersSelect,
    _valid_text,
)

SelectType = TypeVar("SelectType", _Checkboxes, _MultiStaticSelect, _Overflow, _RadioButtons, _StaticSelect)


ElementType = Union[
    _Button,
    _ChannelsSelect,
    _ConversationsSelect,
    _Datepicker,
    _Image,
    _LinkButton,
    _MarkdownText,
    _MultiConversationsSelect,
    _Overflow,
    _PlainText,
    _RadioButtons,
    _Timepicker,
    _UsersSelect,
]


def _valid_accessory(accessory: dict | Type[ElementType], element_type: Type[ElementType]):  # noqa: ANN202
    """Format accessory in valid format."""
    if isinstance(accessory, dict):
        return element_type(**accessory)
    return accessory


def _valid_select_accessory(accessory: list | dict | Type[SelectType], element_type: Type[SelectType]):  # noqa: ANN202
    """Format accessory and return valid accessory object."""
    if isinstance(accessory, dict):
        return element_type(**accessory)
    if isinstance(accessory, list):
        return element_type(options=accessory)
    return accessory


class _SectionBaseElement(BaseModel):
    """Skeleton for section elements with accessories."""

    type: str = Field("section", const=True)
    text: str | dict | _PlainText | _MarkdownText

    @validator("text")
    def format_text_field(cls, text: str) -> _MarkdownText | _PlainText:
        """Format text field as either Markdown or Plain Text."""
        return _valid_text(text)


class _SectionSelect(_SectionBaseElement):
    """Slack base section select object."""

    accessory: list[dict] | dict | _Checkboxes | _StaticSelect | _MultiStaticSelect

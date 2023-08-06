"""Slack action element.

isort: skip_file
"""
import re

from pydantic import BaseModel, Field, validator

from .core import (
    _Button,
    _ChannelsSelect,
    _Checkboxes,
    _ConversationsSelect,
    _Datepicker,
    _LinkButton,
    _MultiConversationsSelect,
    _MultiStaticSelect,
    _Overflow,
    _RadioButtons,
    _StaticSelect,
    _Timepicker,
    _UsersSelect,
)
from ..maps import ACTION_MAP
from ..utils import snakecase_to_pascalcase

ActionElementType = (  # noqa: ECE001
    _Button
    | _ChannelsSelect
    | _Checkboxes
    | _ConversationsSelect
    | _Datepicker
    | _LinkButton
    | _MultiConversationsSelect
    | _MultiStaticSelect
    | _Overflow
    | _RadioButtons
    | _StaticSelect
    | _Timepicker
    | _UsersSelect
)


class ActionsElement(BaseModel):
    """Slack action element.

    Args:
        type (str): Constant field, set to "actions".
        elements (dict | list[ActionElementType]): Action blocks listed as elements of this action element.
            Action blocks can be a button, channels select, checkboxes, conversations select, date picker, link button,
            multi-conversations select, multi-static select, overflow, radio buttons, static select, time picker or
            users select.
    """

    type: str = Field("actions", const=True)
    elements: dict | list[ActionElementType]

    @validator("elements")
    def valid_elements(cls, elements: dict | list[ActionElementType]) -> list[object]:
        """Return list of valid action elements."""
        blocks = []
        if isinstance(elements, dict):
            for key, value in elements.items():
                key = re.split(r"_(?=\d)", key)[0]
                block = ACTION_MAP[f"_{snakecase_to_pascalcase(key)}"]
                blocks.append(block(**value))
        return blocks

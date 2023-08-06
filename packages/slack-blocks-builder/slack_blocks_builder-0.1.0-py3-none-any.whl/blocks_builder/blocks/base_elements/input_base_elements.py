"""Base skeleton for Slack input elements.

isort: skip_file
"""

from typing import Type

from pydantic import BaseModel, Field, validator

from ..core import (
    _ChannelsSelect,
    _Checkboxes,
    _ConversationsSelect,
    _Datepicker,
    _MultiLinePlainTextInput,
    _MultiStaticSelect,
    _MultiUsersSelect,
    _PlainText,
    _PlainTextCustomActionInput,
    _PlainTextInput,
    _RadioButtons,
    _StaticSelect,
    _Timepicker,
    _UsersSelect,
    _text_as_plain_text,
)

InputType = (  # noqa: ECE001
    _ChannelsSelect
    | _Checkboxes
    | _ConversationsSelect
    | _Datepicker
    | _MultiLinePlainTextInput
    | _MultiStaticSelect
    | _MultiUsersSelect
    | _PlainTextCustomActionInput
    | _PlainTextInput
    | _RadioButtons
    | _StaticSelect
    | _Timepicker
    | _UsersSelect
)


def _valid_element(element: str | dict | Type[InputType], element_type: Type[InputType]):  # noqa: ANN202
    """Format element and return valid model object."""
    if isinstance(element, str):
        element = element_type(action_id=element)
    elif isinstance(element, dict):
        element = element_type(**element)
    return element


class _InputBaseElement(BaseModel):
    """Base element for input blocks.

    Args:
        type (str): Constant field, set to "input".
        element (str | dict | InputType): Input blocks listed as elements of this input element.
            Input blocks can be a channels select, checkboxes, conversations select, date picker,
            multi-line plain text input, multi-static select, multi-users select, plain text with custom action input,
            plain text input, radio buttons, static select, time picker or users select.
        label (str | dict | _PlainText}: Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    type: str = Field("input", const=True)
    element: str | dict | InputType
    label: str | dict | _PlainText

    @validator("label", allow_reuse=True)
    def format_text(cls, label: str | dict | _PlainText) -> _PlainText:
        """Format label as plain text element."""
        return _text_as_plain_text(label)

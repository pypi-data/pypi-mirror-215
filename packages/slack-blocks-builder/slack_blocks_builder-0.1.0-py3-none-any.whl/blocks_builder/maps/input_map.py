"""Map input classes to class names."""

from typing import Type

from ..blocks.input import (
    ChannelsSelect,
    Checkboxes,
    Datepicker,
    DispatchesActionsInput,
    DispatchesCustomActionsInput,
    MultiLinePlainTextInput,
    MultiStaticSelect,
    MultiUsersSelect,
    PlainTextInput,
    RadioButtons,
    StaticSelect,
    Timepicker,
)

_INPUT_BLOCKS = (
    ChannelsSelect,
    Checkboxes,
    Datepicker,
    DispatchesActionsInput,
    DispatchesCustomActionsInput,
    MultiLinePlainTextInput,
    MultiStaticSelect,
    MultiUsersSelect,
    PlainTextInput,
    RadioButtons,
    StaticSelect,
    Timepicker,
)

INPUT_MAP: dict[str, Type] = {block.__name__: block for block in _INPUT_BLOCKS}

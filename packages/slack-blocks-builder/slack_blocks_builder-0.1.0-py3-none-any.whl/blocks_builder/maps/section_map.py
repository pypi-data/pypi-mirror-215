"""Map section classes to class names."""

from typing import Type

from ..blocks.section import (
    Button,
    ChannelsSelect,
    Checkboxes,
    ConversationsSelect,
    DatePicker,
    Image,
    LinkButton,
    MultiConversationsSelect,
    MultiStaticSelect,
    Overflow,
    RadioButtons,
    StaticSelect,
    Text,
    TextFields,
    TimePicker,
    UsersSelect,
)

_SECTION_BLOCKS = (
    Button,
    ChannelsSelect,
    Checkboxes,
    ConversationsSelect,
    DatePicker,
    Image,
    LinkButton,
    MultiConversationsSelect,
    MultiStaticSelect,
    Overflow,
    RadioButtons,
    StaticSelect,
    Text,
    TextFields,
    TimePicker,
    UsersSelect,
)

SECTION_MAP: dict[str, Type] = {block.__name__: block for block in _SECTION_BLOCKS}

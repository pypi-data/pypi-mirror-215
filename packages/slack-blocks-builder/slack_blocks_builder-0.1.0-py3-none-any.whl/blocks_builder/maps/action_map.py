"""Map action classes to class names."""

from ..blocks.core import (
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

_ACTION_BLOCKS = (
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

ACTION_MAP = {block.__name__: block for block in _ACTION_BLOCKS}

"""Slack input blocks."""

from pydantic import Field, validator

from .base_elements import _InputBaseElement, _valid_element
from .core import (
    _ChannelsSelect,
    _Checkboxes,
    _ConversationsSelect,
    _Datepicker,
    _MultiLinePlainTextInput,
    _MultiStaticSelect,
    _MultiUsersSelect,
    _PlainTextCustomActionInput,
    _PlainTextInput,
    _RadioButtons,
    _StaticSelect,
    _Timepicker,
    _UsersSelect,
)


class ChannelsSelect(_InputBaseElement):
    """Slack channels select input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _ChannelsSelect): Channels select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select a channel".
                initial_channel (str | None): ID of the channel to appear as the default in the select.
                    Defaults to None.
                action_id (str): Action ID parameter. Defaults to "channels_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: dict | _ChannelsSelect = _ChannelsSelect()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _ChannelsSelect) -> _ChannelsSelect:
        """Format element as a channels select input object."""
        return _valid_element(element, _ChannelsSelect)


class Checkboxes(_InputBaseElement):
    """Slack checkboxes input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _Checkboxes): Checkboxes parameters. If provided as dictionary, the following
            parameters are accepted:
                options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                    dictionaries, the following parameters are accepted:
                        text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                            the "type" parameter should be provided.
                        value (str): Individual value associated with each option.
                        description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                            desired, the "type" parameter should be provided.
                action_id (str): Action ID parameter. Defaults to "checkboxes-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _Checkboxes) -> _Checkboxes:
        """Format element as a checkbox input object."""
        return _valid_element(element, _Checkboxes)


class ConversationsSelect(_InputBaseElement):
    """Slack channels select input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _ConversationsSelect): Conversations select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select a conversation".
                initial_conversation (str | None): ID of the conversation to appear as the default in the select.
                    Defaults to None.
                filter (dict[str, list] | None): Filters to apply to the conversations select. Defaults to None.
                action_id (str): Action ID parameter. Defaults to "conversations_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: dict | _ConversationsSelect = _ConversationsSelect()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _ConversationsSelect) -> _ConversationsSelect:
        """Format element as a conversations select input object."""
        return _valid_element(element, _ConversationsSelect)


class Datepicker(_InputBaseElement):
    """Slack date picker input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _Datepicker): Date picker parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select a date".
                initial_date (str | None): Date to appear as the default in the select. Defaults to None.
                action_id (str): Action ID parameter. Defaults to "datepicker-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: dict | _Datepicker = _Datepicker()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _Datepicker) -> _Datepicker:
        """Format element as a date picker input object."""
        return _valid_element(element, _Datepicker)


class MultiLinePlainTextInput(_InputBaseElement):
    """Slack multi-line plain text input.

    Args:
        type (str): Constant field, set to "input".
        element (str | dict | _MultiLinePlainTextInput): Multi-line plain text parameters. Works by default.
            If parameters provided:
                action_id (str): Defaults to "plain_text_input-action",
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: str | dict | _MultiLinePlainTextInput = _MultiLinePlainTextInput()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: str | dict | _MultiLinePlainTextInput) -> _MultiLinePlainTextInput:
        """Format element as a multi-line plain text input object."""
        return _valid_element(element, _MultiLinePlainTextInput)


class MultiStaticSelect(_InputBaseElement):
    """Slack multi-static select input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _MultiStaticSelect): Multi-static select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Text element. Defaults to "Select options". Can be provided as
                    the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
                options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                    dictionaries, the following parameters are accepted:
                        text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                            the "type" parameter should be provided.
                        value (str): Individual value associated with each option.
                action_id (str): Action ID parameter. Defaults to "multi_static_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    @validator("element", allow_reuse=True)
    def format_element(cls, element: str | dict | _MultiStaticSelect) -> _MultiStaticSelect:
        """Format element as a multi-select input input object."""
        return _valid_element(element, _MultiStaticSelect)


class MultiUsersSelect(_InputBaseElement):
    """Slack multi-user select.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _MultiUsersSelect): Multi-users select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select users".
                action_id (str): Action ID parameter. Defaults to "multi_users_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: str | dict | _MultiUsersSelect = _MultiUsersSelect()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: str | dict | _MultiUsersSelect) -> _MultiUsersSelect:
        """Format element as a multi-user select input object."""
        return _valid_element(element, _MultiUsersSelect)


class PlainTextInput(_InputBaseElement):
    """Simple Slack plain text input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _PlainTextInput): Plain text input parameters. If provided as dictionary, the following
            parameters are accepted:
                action_id (str): Action ID parameter. Defaults to "plain_text_input-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: str | dict | _PlainTextInput = _PlainTextInput()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: str | dict | _PlainTextInput) -> _PlainTextInput:
        """Format element as a plain text input block."""
        return _valid_element(element, _PlainTextInput)


class DispatchesActionsInput(PlainTextInput):
    """Slack plain text input with action dispatch.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _PlainTextInput): Plain text input parameters. If provided as dictionary, the following
            parameters are accepted:
                action_id (str): Action ID parameter. Defaults to "plain_text_input-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    dispatch_action: bool = Field(True, const=True)


class DispatchesCustomActionsInput(DispatchesActionsInput):
    """Slack plain text input with custom action dispatch.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _PlainTextCustomActionInput): Plain text input parameters. If provided as dictionary, the
            following parameters are accepted:
                dispatch_action_config (dict[str, list]): Dispatch action configuration.
                action_id (str): Action ID parameter. Defaults to "plain_text_input-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: dict | _PlainTextCustomActionInput

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _PlainTextCustomActionInput) -> _PlainTextCustomActionInput:
        """Format element as a plain text custom action input object."""
        if isinstance(element, dict):
            element = _PlainTextCustomActionInput(**element)
        return element


class RadioButtons(_InputBaseElement):
    """Slack radio buttons input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _RadioButtons): Radio button parameters. If provided as dictionary, the following
            parameters are accepted:
                options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                    dictionaries, the following parameters are accepted:
                        text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                            the "type" parameter should be provided.
                        value (str): Individual value associated with each option.
                        description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                            desired, the "type" parameter should be provided.
                action_id (str): Action ID parameter. Defaults to "channels_select-action".
        label (str | dict | _PlainText}: Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _RadioButtons) -> _RadioButtons:
        """Format element as a radio button input object."""
        return _valid_element(element, _RadioButtons)


class StaticSelect(_InputBaseElement):
    """Slack static select input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _StaticSelect): Static select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Text element. Defaults to "Select an item". Can be provided as
                    the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
                options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                    dictionaries, the following parameters are accepted:
                        text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                            the "type" parameter should be provided.
                        value (str): Individual value associated with each option.
                action_id (str): Action ID parameter. Defaults to "static_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    @validator("element", allow_reuse=True)
    def format_element(cls, element: str | dict | _StaticSelect) -> _StaticSelect:
        """Format element as a static select input object."""
        return _valid_element(element, _StaticSelect)


class Timepicker(_InputBaseElement):
    """Slack time picker input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _Timepicker): Time picker parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select time".
                initial_time (str | None): Time to appear as the default in the select. Defaults to None.
                action_id (str): Action ID parameter. Defaults to "timepicker-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _Timepicker) -> _Timepicker:
        """Format element as a time picker input object."""
        return _valid_element(element, _Timepicker)


class UsersSelect(_InputBaseElement):
    """Slack channels select input.

    Args:
        type (str): Constant field, set to "input".
        element (dict | _UsersSelect): Users select parameters. If provided as dictionary, the following
            parameters are accepted:
                placeholder (str | dict | _PlainText): Defaults to "Select a user".
                initial_user (str | None): ID of the user to appear as the default in the select. Defaults to None.
                action_id (str): Action ID parameter. Defaults to "users_select-action".
        label (str | dict | _PlainText): Field label content. Can be a string with the label text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    element: dict | _UsersSelect = _UsersSelect()

    @validator("element", allow_reuse=True)
    def format_element(cls, element: dict | _UsersSelect) -> _UsersSelect:
        """Format element as a users select input object."""
        return _valid_element(element, _UsersSelect)

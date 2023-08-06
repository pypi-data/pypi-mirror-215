"""Slack elements of type section.

isort: skip_file
"""
# mypy: disable-error-code=assignment
from pydantic import BaseModel, Field, validator

from .base_elements import (
    _SectionBaseElement,
    _SectionSelect,
    _valid_accessory,
    _valid_select_accessory,
)
from .core import (
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

SectionElement = (  # noqa: ECE001
    _Button
    | _ChannelsSelect
    | _Checkboxes
    | _ConversationsSelect
    | _Datepicker
    | _Image
    | _LinkButton
    | _MarkdownText
    | _MultiConversationsSelect
    | _MultiStaticSelect
    | _Overflow
    | _PlainText
    | _RadioButtons
    | _StaticSelect
    | _Timepicker
    | _UsersSelect
)


class Button(_SectionBaseElement):
    """Slack button with message.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _Button): Button parameters. Accepts the following:
            text (str | dict | _PlainText): Text to display in the button.
            value (str): Value associated with the button.
            action_id (str): Action ID parameter. Defaults to "button-action".
    """

    accessory: dict | _Button

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _Button) -> _Button:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _Button)


class ChannelsSelect(_SectionBaseElement):
    """Slack channel select with message.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _ChannelsSelect): Channels select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select a channel".
            initial_channel (str | None): ID of the channel to appear as the default in the select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "channels_select-action".
    """

    accessory: dict | _ChannelsSelect = _ChannelsSelect()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _ChannelsSelect) -> _ChannelsSelect:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _ChannelsSelect)


class Checkboxes(_SectionSelect):
    """Slack message with checkboxes.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (list[dict] | dict | _Checkboxes): Checkboxes parameters. Accepts the following:
            options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                dictionaries, the following parameters are accepted:
                    text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                        the "type" parameter should be provided.
                    value (str): Individual value associated with each option.
                    description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                        desired, the "type" parameter should be provided.
            action_id (str): Action ID parameter. Defaults to "checkboxes-action".
    """

    accessory: list[dict] | dict | _Checkboxes

    @validator("accessory")
    def format_accessory(cls, accessory: list[dict] | dict | _Checkboxes) -> _Checkboxes:
        """Format accessory as a checkbox element."""
        return _valid_select_accessory(accessory, _Checkboxes)


class ConversationsSelect(_SectionBaseElement):
    """Slack channel select with message.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _ConversationsSelect): Conversations select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select a conversation".
            initial_conversation (str | None): ID of the conversation to appear as the default in the select.
                Defaults to None.
            filter (dict[str, list] | None): Filters to apply to the conversations select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "conversations_select-action".
    """

    accessory: dict | _ConversationsSelect = _ConversationsSelect()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _ConversationsSelect) -> _ConversationsSelect:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _ConversationsSelect)


class DatePicker(_SectionBaseElement):
    """Slack message with date picker.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _Datepicker): Date picker parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select a date".
            initial_date (str | None): Date to appear as the default in the select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "datepicker-action".
    """

    accessory: dict | _Datepicker = _Datepicker()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _Datepicker) -> _Datepicker:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _Datepicker)


class Image(_SectionBaseElement):
    """Slack message with image.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _Image): Image parameters. Accepts the following:
            image_url (str): The URL of the image.
            alt_text (str): The alt text for the image. Set to an empty string by default.
    """

    accessory: dict | _Image

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _Image) -> _Image:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _Image)


class LinkButton(_SectionBaseElement):
    """Slack link button with message.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _LinkButton): Link button parameters. Accepts the following:
            text (str | dict | _PlainText): Text to display in the button.
            value (str): Value associated with the button.
            action_id (str): Action ID parameter. Defaults to "button-action".
            url (str): URl the button will lead to.
    """

    accessory: dict | _LinkButton

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _LinkButton) -> _LinkButton:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _LinkButton)


class MultiConversationsSelect(_SectionBaseElement):
    """Slack multi-conversation select object.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _MultiConversationsSelect): Multi-conversations select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select conversations".
            initial_conversation (str | None): ID of the conversation to appear as the default in the select.
                Defaults to None.
            filter (dict[str, list] | None): Filters to apply to the conversations select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "multi_conversations_select-action".
    """

    accessory: dict | _MultiConversationsSelect = _MultiConversationsSelect()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _MultiConversationsSelect) -> _MultiConversationsSelect:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _MultiConversationsSelect)


class MultiStaticSelect(_SectionSelect):
    """Slack multi-static select object.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _MultiStaticSelect): Multi-static select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Text element. Defaults to "Select options". Can be provided as
                    the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
            options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                dictionaries, the following parameters are accepted:
                    text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                        the "type" parameter should be provided.
                    value (str): Individual value associated with each option.
            action_id (str): Action ID parameter. Defaults to "multi_static_select-action".
    """

    accessory: dict | _MultiStaticSelect

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _MultiStaticSelect) -> _MultiStaticSelect:
        """Format accessory as a button."""
        return _valid_select_accessory(accessory, _MultiStaticSelect)


class Overflow(_SectionSelect):
    """Slack message with overflow meny.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _Overflow): Overflow menu parameters. Accepts the following:
            options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                dictionaries, the following parameters are accepted:
                    text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                        the "type" parameter should be provided.
                    value (str): Individual value associated with each option.
            action_id (str): Action ID parameter. Defaults to "overflow-action".
    """

    accessory: dict | _Overflow

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _Overflow) -> _Overflow:
        """Format accessory as a button."""
        return _valid_select_accessory(accessory, _Overflow)


class RadioButtons(_SectionSelect):
    """Slack message with radio buttons.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (list[dict] | dict | _RadioButtons): Radio buttons parameters. Accepts the following:
            options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                dictionaries, the following parameters are accepted:
                    text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                        the "type" parameter should be provided.
                    value (str): Individual value associated with each option.
                    description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                        desired, the "type" parameter should be provided.
            action_id (str): Action ID parameter. Defaults to "radio_buttons-action".
    """

    accessory: list[dict] | dict | _RadioButtons

    @validator("accessory")
    def format_accessory(cls, accessory: list[dict] | dict | _RadioButtons) -> _RadioButtons:
        """Format accessory as a checkbox element."""
        return _valid_select_accessory(accessory, _RadioButtons)


class StaticSelect(_SectionSelect):
    """Slack static select object.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (list[dict] | dict | _StaticSelect): Static select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Text element. Defaults to "Select an item". Can be provided as
                    the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
            options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
                dictionaries, the following parameters are accepted:
                    text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                        the "type" parameter should be provided.
                    value (str): Individual value associated with each option.
            action_id (str): Action ID parameter. Defaults to "static_select-action".
    """

    accessory: list[dict] | dict | _StaticSelect

    @validator("accessory")
    def format_accessory(cls, accessory: list[dict] | dict | _StaticSelect) -> _StaticSelect:
        """Format accessory as a checkbox element."""
        return _valid_select_accessory(accessory, _StaticSelect)


class Text(BaseModel):
    """Slack markdown or plain text message. Defaults to markdown.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
    """

    type: str = Field("section", const=True)
    text: str | _MarkdownText | _PlainText

    @validator("text")
    def format_text(cls, text: str | _MarkdownText | _PlainText) -> _MarkdownText | _PlainText:
        """Format text into either a plain text or a markdown text element."""
        return _valid_text(text)


class TextFields(BaseModel):
    """Slack text fields.

    Args:
        type (str): Constant field, set to "section".
        fields (list[str | dict | _PlainText | _MarkdownText]): Text fields for the section. Each individual field
            defaults to markdown. If plain text is desired, a dictionary with type defined is required.
            Emoji defaults to True.
    """

    type: str = Field("section", const=True)
    fields: list[str | dict | _PlainText | _MarkdownText]

    @validator("fields")
    def format_text_fields(cls, fields: list) -> list[_PlainText] | list[_MarkdownText]:
        """Check that each individual field is valid and can be converted to the desired format."""
        validated_fields = [_valid_text(field) for field in fields]
        return validated_fields


class TimePicker(_SectionBaseElement):
    """Slack message with time picker.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (dict | _Timepicker): Time picker parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select time".
            initial_time (str | None): Time to appear as the default in the select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "timepicker-action".
    """

    accessory: dict | _Timepicker = _Timepicker()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _Timepicker) -> _Timepicker:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _Timepicker)


class UsersSelect(_SectionBaseElement):
    """Slack users select object.

    Args:
        type (str): Constant field, set to "section".
        text (str | dict | _PlainText | _MarkdownText): Text parameter for the section. Defaults to markdown. If
            plain text is desired, dictionary with type defined is required. Emoji defaults to True.
        accessory (str | _UsersSelect): Users select parameters. Accepts the following:
            placeholder (str | dict | _PlainText): Defaults to "Select a user".
            initial_user (str | None): ID of the user to appear as the default in the select. Defaults to None.
            action_id (str): Action ID parameter. Defaults to "users_select-action".
    """

    accessory: dict | _UsersSelect = _UsersSelect()

    @validator("accessory", allow_reuse=True)
    def format_accessory(cls, accessory: dict | _UsersSelect) -> _UsersSelect:
        """Format accessory as a button."""
        return _valid_accessory(accessory, _UsersSelect)

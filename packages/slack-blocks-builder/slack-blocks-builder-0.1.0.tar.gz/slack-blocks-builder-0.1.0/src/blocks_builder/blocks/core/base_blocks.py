"""Basic Slack blocks used to compose elements.

isort: skip_file
"""

from pydantic import BaseModel, Field, validator

from ...utils import is_real_url, is_valid_date, is_valid_time
from .select import _ElementSelect, _Select, _Selector  # noqa: AZ100
from .text import _PlainText, _text_as_plain_text


class _Button(BaseModel):
    """Single button.

    Args:
        text (str | dict | _PlainText): Text to be displayed in the button. Accepts a simple string or plain text
            element with text and emoji. Emoji defaults to True.
        value (str): Value associated with the button.
        action_id (str): Action ID of the button element. Defaults to "button-action".
    """

    type: str = Field("button", const=True)
    text: str | dict | _PlainText
    value: str
    action_id: str = "button-action"

    @validator("text")
    def format_text_element(cls, text: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(text)


class _ChannelsSelect(_ElementSelect):
    """Channels select accessory.

    Args:
        placeholder (str | dict | _PlainText): Placeholder for the select. Defaults to "Select a channel". Accepts a
            simple string or plain text element with text and emoji. Emoji defaults to True.
        initial_channel (str | None): ID of the channel to display as the initial option. Defaults to None.
        action_id (str): Action ID of the button element. Defaults to "channels_select-action".
    """

    type: str = Field("channels_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select a channel", alias="text")
    initial_channel: str | None = None
    action_id: str = "channels_select-action"


class _Checkboxes(_Selector):
    """Checkboxes accessory.

    Args:
        options (list[dict | _SelectorOption | _SelectorOptionWithDescription]): If provided as a list of dictionaries,
            the following parameters are accepted:
                text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                    the "type" parameter should be provided.
                value (str): Individual value associated with each option.
                description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                    desired, the "type" parameter should be provided.
        action_id (str): Action ID of the button element. Defaults to "checkboxes-action".
    """

    type: str = Field("checkboxes", const=True)
    action_id: str = "checkboxes-action"


class _ConversationsSelect(_ElementSelect):
    """Simple conversation select accessory.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select a conversation".
        initial_conversation (str | None): ID of the conversation to appear as the default in the select.
            Defaults to None.
        filter (dict[str, list] | None): Filters to apply to the conversations select. Defaults to None.
        action_id (str): Action ID parameter. Defaults to "conversations_select-action".
    """

    type: str = Field("conversations_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select a conversation", alias="text")
    initial_conversation: str | None = None
    filter: dict[str, list] | None = None
    action_id: str = "conversations_select-action"


class _Datepicker(BaseModel):
    """Simple date picker component.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select a date".
        initial_date (str | None): Date to appear as the default in the select. Defaults to None.
        action_id (str): Action ID parameter. Defaults to "datepicker-action".
    """

    type: str = Field("datepicker", const=True)
    initial_date: str | None = None
    placeholder: str | dict | _PlainText = Field("Select a date", alias="text")
    action_id: str = "datepicker-action"

    @validator("placeholder")
    def format_placeholder_element(cls, placeholder: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(placeholder)

    @validator("initial_date")
    def is_valid_date(cls, initial_date: str) -> str | None:
        """Check that the date provided is valid."""
        if initial_date is None:
            return
        if not is_valid_date(initial_date):
            raise ValueError("Invalid date. Please provide a valid date string.")
        return initial_date


class _Image(BaseModel):
    """Simple image component.

    Args:
        type (str): Constant field, set to "image"
        image_url (str): The URL of the image.
        alt_text (str): The alt text for the image. Set to an empty string by default.
    """

    type: str = Field("image", const=True)
    image_url: str
    alt_text: str = ""

    @validator("image_url")
    def validate_url(cls, image_url: str) -> str:
        """Check that the provided URL is a real URL, i.e., can be opened."""
        if not is_real_url(image_url):
            raise ValueError("Invalid URL. Please provide a valid URL.")
        return image_url


class _LinkButton(_Button):
    """Single link button.

    Args:
        text (str | dict | _PlainText): Text to be displayed in the button. Accepts a simple string or plain text
            element with text and emoji. Emoji defaults to True.
        value (str): Value associated with the button.
        action_id (str): Action ID of the button element. Defaults to "button-action".
        url (str): The URL the button will link to.
    """

    url: str


class _MultiConversationsSelect(_ElementSelect):
    """Multi-conversations select accessory.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select conversations".
        action_id (str): Action ID parameter. Defaults to "multi_conversations_select-action".
    """

    type: str = Field("multi_conversations_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select conversations", alias="text")
    action_id: str = "multi_conversations_select-action"


class _MultiStaticSelect(_Select):
    """Multi static select accessory.

    Args:
        placeholder (str | dict | _PlainText): Text element. Defaults to "Select options". Can be provided as
            the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
        options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
            dictionaries, the following parameters are accepted:
                text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                    the "type" parameter should be provided.
                value (str): Individual value associated with each option.
        action_id (str): Action ID parameter. Defaults to "multi_static_select-action".
    """

    type: str = Field("multi_static_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select options", alias="text")
    action_id: str = "multi_static_select-action"

    @validator("placeholder", allow_reuse=True)
    def format_placeholder_element(cls, placeholder: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(placeholder)


class _MultiUsersSelect(_ElementSelect):
    """Multi-users select element.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select users".
        action_id (str): Action ID parameter. Defaults to "multi_users_select-action".
    """

    type: str = Field("multi_users_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select users", alias="text")
    action_id: str = "multi_users_select-action"


class _Overflow(_Select):
    """Overflow select accessory.

    Args:
        options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
            dictionaries, the following parameters are accepted:
                text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                    the "type" parameter should be provided.
                value (str): Individual value associated with each option.
        action_id (str): Action ID parameter. Defaults to "overflow-action".
    """

    type: str = Field("overflow", const=True)
    action_id: str = "overflow-action"


class _PlainTextInput(BaseModel):
    """Simple plain text input.

    Args:
        action_id (str): Action ID of the plain text input. Default to "plain_text_input-action".
    """

    type: str = Field("plain_text_input", const=True)
    action_id: str = "plain_text_input-action"


class _PlainTextCustomActionInput(_PlainTextInput):
    """Simple plain text input with custom action dispatched.

    Args:
        action_id (str): Action ID of the plain text input. Default to "plain_text_input-action".
        dispatch_action_config (dict[str, list]): Configuration for the custom dispatch action.
    """

    dispatch_action_config: dict[str, list]


class _MultiLinePlainTextInput(_PlainTextInput):
    """Simple multi-line plain text input.

    Args:
        action_id (str): Action ID of the plain text input. Default to "plain_text_input-action".
    """

    multiline: bool = Field(True, const=True)


class _RadioButtons(_Selector):
    """Radio buttons accessory.

    Args:
        options (list[dict | _SelectorOption | _SelectorOptionWithDescription]): If provided as a list of dictionaries,
            the following parameters are accepted:
                text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                    the "type" parameter should be provided.
                value (str): Individual value associated with each option.
                description (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is
                    desired, the "type" parameter should be provided.
        action_id (str): Action ID of the button element. Defaults to "radio_buttons-action".
    """

    type: str = Field("radio_buttons", const=True)
    action_id: str = "radio_buttons-action"


class _StaticSelect(_Select):
    """Static select accessory.

    Args:
        placeholder (str | dict | _PlainText): Text element. Defaults to "Select an item". Can be provided as
            the placeholder string or a dictionary with "text" and "emoji". Emoji is set to True by default.
        options (list[dict | _SelectorOption | _SelectorOptionWithDescription): If provided as a list of
            dictionaries, the following parameters are accepted:
                text (str | dict | _MarkdownText | _PlainText): Defaults to markdown. If plain text is desired,
                    the "type" parameter should be provided.
                value (str): Individual value associated with each option.
        action_id (str): Action ID parameter. Defaults to "static_select-action".
    """

    type: str = Field("static_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select an item", alias="text")
    action_id: str = "static_select-action"

    @validator("placeholder", allow_reuse=True)
    def format_placeholder_element(cls, placeholder: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(placeholder)


class _Timepicker(BaseModel):
    """Simple time picker component.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select time".
        initial_time (str | None): Time to appear as the default in the select. Defaults to None.
        action_id (str): Action ID parameter. Defaults to "timepicker-action".
    """

    type: str = Field("timepicker", const=True)
    initial_time: str | None = None
    placeholder: str | dict | _PlainText = Field("Select time", alias="text")
    action_id: str = "timepicker-action"

    @validator("placeholder")
    def format_placeholder_element(cls, placeholder: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(placeholder)

    @validator("initial_time")
    def is_valid_time(cls, initial_time: str) -> str | None:
        """Check that the time provided if valid."""
        if initial_time is None:
            return
        if not is_valid_time(initial_time):
            raise ValueError("Invalid time. Please provide a valid time string. Use a 24hr format.")
        return initial_time


class _UsersSelect(_ElementSelect):
    """Users select accessory.

    Args:
        placeholder (str | dict | _PlainText): Defaults to "Select a user".
        initial_user (str | None): ID of the user to appear as the default in the select. Defaults to None.
        action_id (str): Action ID parameter. Defaults to "users_select-action".
    """

    type: str = Field("users_select", const=True)
    placeholder: str | dict | _PlainText = Field("Select a user", alias="text")
    initial_user: str | None = None
    action_id: str = "users_select-action"

"""Base select elements."""

from pydantic import BaseModel, validator

from .text import _MarkdownText, _PlainText, _text_as_plain_text, _valid_text


class _SelectOption(BaseModel):
    """Individual option items for static selects."""

    text: str | dict | _PlainText
    value: str

    @validator("text", allow_reuse=True)
    def format_text_element(cls, text: str | dict | _PlainText) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(text)


class _SelectorOption(BaseModel):
    """Individual option items for checkboxes and radio buttons."""

    text: str | dict | _MarkdownText | _PlainText
    value: str

    @validator("text", allow_reuse=True)
    def format_text_element(cls, text: str | dict | _MarkdownText | _PlainText) -> _MarkdownText | _PlainText:
        """Return valid formatted text element."""
        return _valid_text(text)


class _SelectorOptionWithDescription(_SelectorOption):
    """Individual option items for checkboxes and radio buttons with a description."""

    description: str | dict | _MarkdownText | _PlainText

    @validator("text", "description", allow_reuse=True)
    def format_text_element(cls, text: str | dict | _MarkdownText | _PlainText) -> _MarkdownText | _PlainText:
        """Return valid formatted text element."""
        return _valid_text(text)


class _ElementSelect(BaseModel):
    """Accessory for pre-populated element selects."""

    type: str
    placeholder: str | dict | _PlainText
    action_id: str

    @validator("placeholder", allow_reuse=True)
    def format_placeholder_element(cls, placeholder: str) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(placeholder)


class _Select(BaseModel):
    """Base select accessory."""

    type: str
    options: list[dict | _SelectOption]
    action_id: str

    @validator("options", allow_reuse=True)
    def valid_options(cls, options: list[_SelectOption]) -> list[_SelectOption]:
        """Format and return valid select options."""
        valid_options = []
        for option in options:
            if not isinstance(option, dict):
                raise ValueError("Invalid select option. Provide a dictionary with, at least, text and value.")
            option = _SelectOption(**option)
            valid_options.append(option)
        return valid_options


class _Selector(BaseModel):
    """Base selector accessory."""

    type: str
    options: list[dict | _SelectorOption | _SelectorOptionWithDescription]
    action_id: str

    @validator("options", allow_reuse=True)
    def valid_options(
        cls, options: list[_SelectOption | _SelectorOptionWithDescription]
    ) -> list[_SelectOption | _SelectorOptionWithDescription]:
        """Format and return valid selector options."""
        valid_options = []
        for option in options:
            if not isinstance(option, dict):
                raise ValueError("Invalid select option. Provide a dictionary with, at least, text and value.")
            if option.get("description"):
                option = _SelectorOptionWithDescription(**option)
                valid_options.append(option)
            else:
                option = _SelectorOption(**option)
                valid_options.append(option)
        return valid_options

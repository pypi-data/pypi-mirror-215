"""Slack header elements."""

from pydantic import BaseModel, Field, validator

from .core import _PlainText, _text_as_plain_text


class Header(BaseModel):
    """Slack header block.

    Args:
        type (str): Constant field, set to "header"
        text (str | dict | _PlainText): Header content. Can be a string with the header text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
    """

    type: str = Field("header", const=True)
    text: str | dict | _PlainText

    @validator("text")
    def format_text(cls, text: str | dict | _PlainText) -> _PlainText:
        """Format text as a plain text element."""
        return _text_as_plain_text(text)

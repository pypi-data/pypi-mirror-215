"""Base text elements."""

from pydantic import BaseModel, Field


class _PlainText(BaseModel):
    """Basic plain text element."""

    type: str = Field("plain_text", const=True)
    text: str
    emoji: bool = True


class _MarkdownText(BaseModel):
    """Basic markdown test element."""

    type: str = Field("mrkdwn", const=True)
    text: str


def _text_as_plain_text(text: str | dict | _PlainText) -> _PlainText:
    """If text is a string, convert to PlainText."""
    if isinstance(text, str):
        text = _PlainText(text=text)
    elif isinstance(text, dict):
        text = _PlainText(**text)
    return text


def _valid_text(text: str | dict | _MarkdownText | _PlainText) -> _PlainText | _MarkdownText:
    """If text is a string, convert to MarkdownText or PlainText."""
    if isinstance(text, str):
        text = _MarkdownText(text=text)
    elif isinstance(text, dict):
        if text.get("type") and text["type"] == "plain_text":
            text = _PlainText(**text)
        else:
            text = _MarkdownText(**text)
    return text

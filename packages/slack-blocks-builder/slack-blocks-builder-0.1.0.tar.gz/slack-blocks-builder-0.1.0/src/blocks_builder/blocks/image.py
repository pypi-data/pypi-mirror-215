"""Slack image elements."""

from pydantic import validator

from .core import _Image, _PlainText, _text_as_plain_text

Image = _Image  # Image block with no title


class ImageWithTitle(_Image):
    """Simple image component with a title.

    Args:
        type (str): Constant field, set to "image"
        title (str | dict | _PlainText): Image title. Can be a string with the title text or a dictionary with
            text and emoji parameters. By default, emoji is set to True.
        image_url (str): The URL of the image.
        alt_text (str): The alt text for the image. Set to an empty string by default.
    """

    title: str | dict | _PlainText

    @validator("title")
    def format_title_element(cls, title: str | dict | _PlainText) -> _PlainText:
        """Return valid formatted text element."""
        return _text_as_plain_text(title)

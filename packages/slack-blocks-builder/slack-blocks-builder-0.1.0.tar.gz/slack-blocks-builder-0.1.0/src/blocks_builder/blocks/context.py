"""Slack context element."""

from pydantic import BaseModel, Field, validator

from .core import _Image, _MarkdownText, _PlainText

ContextElementType = _Image | _MarkdownText | _PlainText


class ContextElement(BaseModel):
    """Slack context element.

    Args:
        type (str): Constant field, set to "context".
        elements (dict | list[ContextElementType]): Context blocks listed as elements of this context element.
            Context blocks can be aa image, a markdown text block or a plan text block.
    """

    type: str = Field("context", const=True)
    elements: dict | list[ContextElementType]

    @validator("elements")
    def valid_elements(cls, elements: dict | list[ContextElementType]) -> list[ContextElementType]:
        """Return list of valid context elements."""
        blocks: list[ContextElementType] = []
        if isinstance(elements, dict):
            for key, value in elements.items():
                if "text" in key:
                    if isinstance(value, (str, dict)):
                        blocks.append(_MarkdownText(text=value) if isinstance(value, str) else _PlainText(**value))
                elif key == "image" and isinstance(value, (str, dict)):
                    blocks.append(_Image(image_url=value) if isinstance(value, str) else _Image(**value))
        return blocks

"""Slack divider elements."""

from pydantic import BaseModel, Field


class Divider(BaseModel):
    """Simple Slack message divider.

    Args:
        type (str): Constant field, set to "divider".
    """

    type: str = Field("divider", const=True)

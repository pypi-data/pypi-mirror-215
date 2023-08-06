"""Slack block kit payload builder."""

import os

from .blocks.actions import ActionsElement  # noqa: AZ100
from .blocks.context import ContextElement
from .blocks.divider import Divider
from .blocks.header import Header
from .blocks.image import Image, ImageWithTitle
from .maps import INPUT_MAP, SECTION_MAP
from .utils import open_json, open_yaml, snakecase_to_pascalcase


class Builder:
    """Build Slack block kit payload."""

    def build_from_file(self, file_path: str) -> dict:
        """Build Slack blocks payload from a JSON or YAML file.

        Args:
            file_path (str): The path to the file to build from.
        """
        file_type = self._get_file_type(file_path)
        data = open_yaml(file_path) if file_type == "yaml" else open_json(file_path)
        return self._block_map(data)

    def build_from_dict(self, data: dict) -> dict:
        """Build slack blocks payload from a dictionary.

        Args:
            data (dict): Data to be converted in dictionary form.
        """
        return self._block_map(data)

    # private

    def _block_map(self, data: dict) -> dict:
        # Map individual blocks to respective models
        blocks = []
        for block in data.keys():
            if "actions" in block:
                blocks.append(ActionsElement(elements=data["actions"]).dict(exclude_none=True))
            elif "context" in block:
                blocks.append(ContextElement(elements=data["context"]).dict(exclude_none=True))
            elif "divider" in block:
                blocks.append(Divider().dict())
            elif "header" in block:
                blocks.append(Header(**data["header"]).dict(exclude_none=True))
            elif "image" in block:
                blocks.append(self._image_map(data["image"]))
            elif "input" in block:
                blocks.append(self._input_map(data["input"]))
            elif "section" in block:
                blocks.append(self._section_map(data["section"]))
        return {"blocks": blocks}

    @staticmethod
    def _section_map(data: dict) -> dict:
        # Map section blocks
        if len(data) == 1:
            key = next(iter(data.keys()))
        else:
            key = next(key for key in data.keys() if key != "text")
        block = SECTION_MAP[snakecase_to_pascalcase(key)]
        return block(**data).dict(exclude_none=True)

    @staticmethod
    def _image_map(data: dict) -> dict:
        # Map image blocks
        if data.get("title"):
            return ImageWithTitle(**data).dict(exclude_none=True)
        return Image(**data).dict(exclude_none=True)

    @staticmethod
    def _input_map(data: dict) -> dict:
        # Map input blocks
        if len(data) == 1:
            key = next(iter(data.keys()))
        elif data.get("dispatch_action_config"):
            key = "DispatchesCustomActionsInput"
        elif data.get("dispatch_action"):
            key = "DispatchesActionsInput"
        elif data.get("multiline"):
            key = "MultiLinePlainTextInput"
        else:
            key = next(key for key in data.keys() if key != "text")
        block = INPUT_MAP[snakecase_to_pascalcase(key)]
        return block(**data[key]).dict(exclude_none=True)

    @staticmethod
    def _get_file_type(file_path: str) -> str:
        # Get file type from file path
        _, extension = os.path.splitext(file_path)
        file_type = extension.lstrip(".").lower()
        return "yaml" if file_type in ("yaml", "yml") else "json"

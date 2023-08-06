"""Generate sample files."""

import json

import yaml


def generate_sample_files() -> None:
    """Generate a sample YAML and a sample JSON configuration files for the block kit schema."""
    data: dict = {
        "header": {"text": "My header", "emoji": True},
        "section": {"text": "Simple test"},
        "divider": True,
        "context": {
            "text": {"text": "This is a test", "emoji": True},
            "text_2": "Another text",
            "image": {"image_url": "https://www.google.com", "alt_text": "This is a test"},
        },
        "actions": {
            "button": {"text": "Button 1", "value": "button_1", "url": "google.com"},
            "checkboxes": {
                "text": "This is an option",
                "options": [{"text": "option 1", "value": "option-1"}, {"text": "option 2", "value": "option-2"}],
            },
        },
        "input": {"channels_select": {"label": "Channel select test", "element": {"initial_channel": "TEST1234"}}},
    }
    with open("sample.yaml", "w") as yaml_file:
        yaml.safe_dump(data, yaml_file, sort_keys=False)

    with open("sample.json", "w") as json_file:
        json.dump(data, json_file)

"""Common utilities."""

import json
import re
from datetime import datetime
from urllib.request import urlopen

import yaml


def open_json(file_path: str, mode: str = "r") -> dict:
    """Read a JSON file into a dictionary."""
    with open(file_path, mode) as file:
        data = json.load(file)
    return data


def open_yaml(file_path: str, mode: str = "r") -> dict:
    """Read a YAML file into a dictionary."""
    with open(file_path, mode) as file:
        data = yaml.safe_load(file)
    return data


def is_real_url(url: str) -> bool:
    """Check that the provided URL is a real URL, i.e., can be opened."""
    try:
        urlopen(url)
    except IOError:
        return False
    return True


def is_valid_date(date: str) -> bool:
    """Check that a provided string is a valid ISO date ("YYYY-MM-DD")."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def is_valid_string(text: str, regex: str) -> bool:
    """Check if a particular string matches a specific regex pattern."""
    return bool(re.match(regex, text))


def is_valid_time(time: str, seconds: bool = False) -> bool:
    """Check if string is a valid 24ht time representation ("HH:MM:SS"). Optionally check for seconds."""
    try:
        datetime.strptime(time, "%H:%M:%S" if seconds else "%H:%M")
    except ValueError:
        return False
    return True


def snakecase_to_pascalcase(string: str) -> str:
    """Convert an underscore-separated string to camel case."""
    return "".join(x.title() for x in string.split("_"))

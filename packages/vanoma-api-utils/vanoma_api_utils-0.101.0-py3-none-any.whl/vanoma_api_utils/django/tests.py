import json
from typing import Any, Dict, Union
from django.apps import apps
from django.core.files.base import ContentFile
from pathlib import Path


def load_fixture_as_json(name: Union[str, None]) -> Union[Dict[str, Any], None]:
    if name is None:
        return None

    for app_config in apps.get_app_configs():
        file_path = f"{app_config.path}/fixtures/{name}"
        if Path(file_path).exists():
            with open(file_path, "r") as rfile:
                return json.load(rfile)

    raise Exception(f"Fixuture {name} not found.")


def load_fixture_as_binary(name: Union[str, None]) -> Union[bytes, None]:
    if name is None:
        return None

    for app_config in apps.get_app_configs():
        file_path = f"{app_config.path}/fixtures/{name}"
        if Path(file_path).exists():
            with open(file_path, "rb") as rfile:
                return rfile.read()

    raise Exception(f"Fixture file {name} not found.")


def load_fixture_as_content_file(name: Union[str, None]) -> Union[ContentFile, None]:
    _bytes = load_fixture_as_binary(name)
    if _bytes is None:
        return None

    return ContentFile(_bytes, name=name)

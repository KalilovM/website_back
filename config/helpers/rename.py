import os
import uuid
from typing import Any

from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename:
    """
    Class to rename given file into uuid4
    """

    def __init__(self, sub_path: str) -> None:
        self.path = sub_path

    def __call__(self, instance: Any, filename: str) -> str:
        file_ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{file_ext}"
        return os.path.join(self.path, filename)

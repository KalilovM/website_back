from django.conf import settings
from django.http import HttpRequest
import pydenticon
import hashlib
import uuid
import os


def generate_avatar(username: str, sub_path: str, request: "HttpRequest", file_ext: str = "png"):
    """
    Generating avatar using pydenticon library
    (Inspired by GitHub's Identicon)
    """

    hashed_value = hashlib.md5(username.encode("utf-8")).hexdigest()
    foreground = ["rgb(45,79,255)",
                  "rgb(254,180,44)",
                  "rgb(226,121,234)",
                  "rgb(30,179,253)",
                  "rgb(232,77,65)",
                  "rgb(49,203,115)",
                  "rgb(141,69,170)"]

    background = "rgb(224,224,224)"

    identicon = pydenticon.Generator(5, 5, background=background, foreground=foreground).generate(hashed_value, 250,
                                                                                                  250)
    filename = f"{uuid.uuid4().hex}.{file_ext}"
    file_path = os.path.join(sub_path, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(full_path)
    with open(full_path, "wb") as f:
        f.write(identicon)
    return file_path

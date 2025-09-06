from typing import TypedDict


class Data(TypedDict):
  allow_photo_message: bool
  pending_custom_rejects: set[int]

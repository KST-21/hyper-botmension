from typing import TypedDict


class Data(TypedDict):
  allow_photo_message: set[int]
  pending_custom_rejects: set[int]

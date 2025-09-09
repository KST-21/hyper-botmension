from typing import TypedDict


class Data(TypedDict):
  allow_photo_message: set[int]
  pending_custom_rejects: set[int]


class PrivateChannel(TypedDict):
  id: int


class PremiumChannel(TypedDict):
  id: int
  price: int


class Channels(TypedDict):
  hyper_space: int
  private_channels: dict[str, PrivateChannel]
  premium_channels: dict[str, PremiumChannel]
  fake_public_channel_id: int
  fake_premium_channel_id: int
  fake_private_channels: dict[str, PrivateChannel]


class BOT_INFO_TYPE(TypedDict):
  name: str | None
  username: str | None
  is_beta: bool | None

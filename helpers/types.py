from typing import TypedDict

from telegram import ChatFullInfo


class Data(TypedDict):
  allow_photo_message: set[int]
  pending_custom_rejects: set[int]


class PrivateChannel(TypedDict):
  id: int
  invite_link: str


class PremiumChannel(TypedDict):
  id: int
  price: int


class BotResourceChannel(TypedDict):
  id: int
  how_to_subscribe: tuple[int, int, int]


class Channels(TypedDict):
  hyper_space: int
  private_channels: dict[str, PrivateChannel]
  premium_channels: dict[str, PremiumChannel]
  fake_public_channel_id: int
  fake_premium_channel_id: int
  fake_private_channels: dict[str, PrivateChannel]
  bot_resource_channel: BotResourceChannel


class BOT_INFO_TYPE(TypedDict):
  name: str | None
  username: str | None
  is_beta: bool | None
  public_channel: ChatFullInfo | None

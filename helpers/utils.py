import re
from telegram import InlineKeyboardButton, Message, Update
from telegram.ext import ContextTypes
from constants import *
from config import BOT_RECEPTION_CHANNEL_ID
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def is_private_chat(update: Update):
  return update.message and update.message.chat.type == "private"


async def forward_message(
  update_message: Message, context: ContextTypes.DEFAULT_TYPE
):
  if not BOT_RECEPTION_CHANNEL_ID:
    return
  await context.bot.forward_message(
    chat_id=BOT_RECEPTION_CHANNEL_ID,
    from_chat_id=update_message.chat_id,
    message_id=update_message.message_id
  )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message:
    return
  update_message = update.message

  if not is_private_chat(update):
    await update_message.reply_text(not_private_chat_warning_message)
    return

  await update_message.reply_text(sending_message_warning_1)
  await update_message.reply_text(sending_message_warning_2)

  await forward_message(update_message, context)


def extract_user_id_from_caption(caption: str) -> str:
  """Extract the user id from a caption string containing 'id='."""
  parts = str(caption).split("id=")
  return parts[1] if len(parts) > 1 else ""


def clean_caption(caption: str) -> str:
  """Remove the last line of a caption (used when rejecting receipts)."""
  return "\n".join(str(caption).split("\n")[:-1])


def create_receipt_confirm_markup():
  return [
    [InlineKeyboardButton("Approve", callback_data="approve_join")],
    [InlineKeyboardButton("Custom Reject", callback_data="custom_reject")],
    [InlineKeyboardButton("Reject", callback_data="reject_join")],
  ]


def escape_md(text: str) -> str:
  return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


def get_channel_internal_id(id: int) -> str:
  return str(id).replace("-100", "", 1)


def get_public_channel_id() -> int:
  if BOT_INFO["is_beta"]:
    return channels["fake_public_channel_id"]
  return channels["hyper_space"]


def get_private_channel_ids(data_type: Callable[[Iterable[int]], T]) -> T:
  if BOT_INFO["is_beta"]:
    return data_type(
      data["id"] for data in channels["fake_private_channels"].values()
    )
  return data_type(
    data["id"] for data in channels["private_channels"].values()
  )

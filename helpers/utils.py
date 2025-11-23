import re
import logging
from telegram import Bot, InlineKeyboardButton, Update, User
from telegram.ext import ContextTypes
from telegram.error import Forbidden, NetworkError, TimedOut
from constants import *
from config import BOT_ERROR_LOGGING_CHANNEL_ID
from typing import Any, Awaitable, Callable, Iterable, TypeVar
import asyncio

T = TypeVar("T")


def get_welcome_message() -> str:
  name = BOT_INFO["name"] or "Bot"
  # commented out the feature that won't support yet
  return (
    f"ဟယ်လိုပါ {name} ကနေ ကြိုဆိုပါတယ်ဗျ\n\n"
    # "ဇာတ်ကားဝယ်မှာလား Premium ရက်၃၀ ဝင်မှာလားဆိုတာ ရွေးပေးပါခင်ဗျ"
  )


async def create_private_invite_link_with_message(
  context: ContextTypes.DEFAULT_TYPE
) -> str | None:
  public_channel = BOT_INFO["public_channel"]
  if not public_channel:
    return
  public_channel_reference = get_channel_reference(
    public_channel.id, public_channel.title
  )
  private_channel_id = get_private_channel_ids(tuple)[0]
  private_channel = await context.bot.get_chat(private_channel_id)

  invite_link = get_private_channel_invite_links(tuple)[0]
  return (
    f"'{private_channel.title or "Private channel"}' ထဲကို ဝင်လိုလျှင်\n"
    f"{public_channel_reference} ကို အရင် Subscribe ပြီးမှ\n"
    f"ဒီ link {escape_md(invite_link)} ကို နှိပ်ပြီး ဝင်ခွင့်တောင်းပါ"
  )


def is_private_chat(update: Update):
  return update.message and update.message.chat.type == "private"


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


def is_beta():
  return BOT_INFO["is_beta"]


def get_public_channel_id() -> int:
  if is_beta():
    return channels["fake_public_channel_id"]
  return channels["hyper_space"]


def get_private_channel_ids(data_type: Callable[[Iterable[int]], T]) -> T:
  if is_beta():
    return data_type(
      data["id"] for data in channels["fake_private_channels"].values()
    )
  return data_type(
    data["id"] for data in channels["private_channels"].values()
  )


def get_private_channel_invite_links(
  data_type: Callable[[Iterable[str]], T]
) -> T:
  if is_beta():
    return data_type(
      data["invite_link"]
      for data in channels["fake_private_channels"].values()
    )
  return data_type(
    data["invite_link"] for data in channels["private_channels"].values()
  )


def get_user_reference(user: User):
  if user.username:
    return f"[{escape_md(user.full_name)}](https://t.me/{escape_md(user.username)})"
  return f"[{escape_md(user.full_name)}]({escape_md(f'tg://user?id={user.id}')}) {escape_md('(')}[Backup Web Link]({escape_md(f'https://web.telegram.org/a/#{user.id}')}){escape_md(')')}"


def get_channel_reference(channel_id: int, channel_title: str | None):
  internal_id = get_channel_internal_id(channel_id)
  return f"[{escape_md(channel_title or '')}]({escape_md(f'https://t.me/c/{internal_id}/1')})"


async def safe_send_message(
  send_message: Callable[[], Awaitable[Any]],
  bot: Bot,
  original_message: str,
  user_reference: str | None = None,
  retries: int = 3
):
  if not BOT_ERROR_LOGGING_CHANNEL_ID:
    return

  logger = logging.getLogger(__name__)

  for _ in range(0, retries):
    try:
      await send_message()
      return

    except Forbidden:
      message_to_send = (
        f"🚨 **BLOCKED** 🚨\n\n"
        f"{user_reference} ဆိုတဲ့ကောင် bot ကို block ထားလို့ ပို့မရ\n"
        f"Original Message:\n"
        f"{original_message}"
      )
      await safe_send_message(
        lambda: bot.send_message(
          str(BOT_ERROR_LOGGING_CHANNEL_ID),
          message_to_send,
          parse_mode="MarkdownV2",
          disable_web_page_preview=True
        ),
        bot,
        original_message=message_to_send
      )
      return

    except (TimedOut, NetworkError) as e:
      logger.exception(
        "Error when sending this message.\n"
        f"{original_message}"
      )
      await asyncio.sleep(2)

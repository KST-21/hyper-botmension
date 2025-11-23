from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import data
from helpers.utils import create_private_invite_link_with_message
from constants import how_to_subscribe


async def handle_invite_private(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()

  keyboard = [
    [InlineKeyboardButton(how_to_subscribe, callback_data="how_to_subscribe")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  private_invite_link_message = await create_private_invite_link_with_message(
    context
  )
  if not private_invite_link_message:
    return

  await query.edit_message_text(
    text=private_invite_link_message,
    parse_mode="MarkdownV2",
    reply_markup=reply_markup
  )

  user_id = query.from_user.id
  if user_id in data["allow_photo_message"]:
    data["allow_photo_message"].remove(user_id)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from constants import get_welcome_message, not_private_chat_warning_message, premium_prompt_message, buy_something_prompt_message
from config import data
from helpers.utils import is_private_chat


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message:
    return
  if not is_private_chat(update):
    await update.message.reply_text(not_private_chat_warning_message)
    return

  keyboard = [
    [InlineKeyboardButton(premium_prompt_message, callback_data="premium")],
    [InlineKeyboardButton(buy_something_prompt_message, callback_data="buy")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  welcome_message = get_welcome_message()
  await update.message.reply_text(welcome_message, reply_markup=reply_markup)

  user = update.message.from_user
  if user and user.id in data["allow_photo_message"]:
    data["allow_photo_message"].remove(user.id)

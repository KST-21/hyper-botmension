from telegram import Message, Update
from telegram.ext import ContextTypes
from constants import *
from config import BOT_RECEPTION_CHANNEL_ID
from helpers.utils import is_private_chat


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

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import BOT_ADMISSION_CHANNEL_ID, data
from constants import receipt_receive
from handlers.messages import forward_message, message_handler
from helpers.utils import create_receipt_confirm_markup


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not (update.message and BOT_ADMISSION_CHANNEL_ID):
    return
  update_message = update.message

  user = update_message.from_user
  if not user:
    return

  if not user.id in data["allow_photo_message"]:
    await message_handler(update, context)
    return

  photo = update_message.photo[-1].file_id
  keyboard = create_receipt_confirm_markup()

  await context.bot.send_photo(
    chat_id=BOT_ADMISSION_CHANNEL_ID,
    photo=photo,
    caption=f"Photo from @{user.username or user.first_name}\nid={user.id}",
    reply_markup=InlineKeyboardMarkup(keyboard)
  )

  await forward_message(update_message, context)

  await update_message.reply_text(receipt_receive)
  data["allow_photo_message"].remove(user.id)

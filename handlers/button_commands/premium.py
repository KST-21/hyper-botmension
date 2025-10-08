from telegram import CallbackQuery
from telegram.ext import ContextTypes
from config import data
from constants import premium_invoice


async def handle_premium(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()
  await query.edit_message_text(premium_invoice)
  user_id = query.from_user.id
  data["allow_photo_message"].add(user_id)

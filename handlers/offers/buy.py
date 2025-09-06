from telegram import CallbackQuery
from telegram.ext import ContextTypes
from config import data


async def handle_buy(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
  await query.answer()
  await query.edit_message_text("ရော့ လိုချင်တဲ့ ဇာတ်ကား")
  data["allow_photo_message"] = False

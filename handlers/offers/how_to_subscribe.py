from telegram import CallbackQuery
from telegram.ext import ContextTypes
from config import data
from constants import channels


async def handle_how_to_subscribe(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()
  await query.delete_message()
  user_id = query.from_user.id

  bot_resource_channel = channels["bot_resource_channel"]
  from_chat_id = bot_resource_channel["id"]
  message_ids = bot_resource_channel["how_to_subscribe"]

  for msg_id in message_ids:
    await context.bot.copy_message(
      chat_id=user_id,
      from_chat_id=from_chat_id,
      message_id=msg_id,
      protect_content=True
    )

  if user_id in data["allow_photo_message"]:
    data["allow_photo_message"].remove(user_id)

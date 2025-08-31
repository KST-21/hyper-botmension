import os
from dotenv import load_dotenv
from typing import Final
from telegram import ChatInviteLink, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from constants import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

load_dotenv()

# Access variables
TOKEN: Final = os.getenv("TOKEN")
BOT_ADMISSION_CHANNEL_ID: Final = os.getenv("BOT_ADMISSION_CHANNEL_ID")
BOT_RECEPTION_CHANNEL_ID: Final = os.getenv("BOT_RECEPTION_CHANNEL_ID")
PORT = int(os.environ.get("PORT", 10000))

data: dict[str, bool] = {"allow_photo_message": False}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not is_private_chat(update):
    await update.message.reply_text(not_private_chat_warning_message)
    return

  global data
  keyboard = [
    [InlineKeyboardButton(premium_prompt_message, callback_data="premium")],
    [InlineKeyboardButton(buy_something_prompt_message, callback_data="buy")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text(welcome_message, reply_markup=reply_markup)
  data["allow_photo_message"] = False


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global data
  query = update.callback_query
  if not query:
    return
  await query.answer()
  if query.data == "premium":
    await query.edit_message_text(premium_invoice)
    data["allow_photo_message"] = True
    return
  elif query.data == "buy":
    await query.edit_message_text("ရော့ လိုချင်တဲ့ ဇာတ်ကား")
    data["allow_photo_message"] = False
    return

  original_user_id = str(query.message.caption).split("id=")[1]
  if query.data == "approve_join":
    await query.edit_message_caption(
      f"Photo from @{query.from_user.username or query.from_user.first_name}\nJoin Approved"
    )

    invite_link: ChatInviteLink = await context.bot.create_chat_invite_link(
      chat_id=channel_ids["fake_premium_channel_id"],
      member_limit=1,
      creates_join_request=False
    )
    await context.bot.send_message(
      chat_id=original_user_id,
      text=f"Premium Channel link\n{invite_link.invite_link}"
    )
    return

  elif query.data == "reject_join":
    await query.edit_message_caption(
      f"Photo from @{query.from_user.username or query.from_user.first_name}\nJoin Rejected"
    )
    await context.bot.send_message(
      chat_id=original_user_id,
      text="လက်ခံရရှိသော ပြေစာပယ်ချခံရပါသည်\nပြေစာပြန်လည် ပေးပို့ပေးပါ"
    )
    data["allow_photo_message"] = True
    return


def is_private_chat(update: Update):
  return update.message and update.message.chat.type == "private"


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not is_private_chat(update):
    if update.message:
      await update.message.reply_text(not_private_chat_warning_message)
    return

  await update.message.reply_text(sending_message_warning_1)
  await update.message.reply_text(sending_message_warning_2)

  await context.bot.forward_message(
    chat_id=BOT_RECEPTION_CHANNEL_ID,
    from_chat_id=update.message.chat_id,
    message_id=update.message.message_id
  )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global data
  if not data["allow_photo_message"]:
    await message_handler(update, context)
    return
  user = update.message.from_user
  photo = update.message.photo[-1].file_id  # last = best quality

  # Forward photo to admin group/channel for review
  keyboard = [
    [InlineKeyboardButton("Approve", callback_data="approve_join")],
    [InlineKeyboardButton("Reject", callback_data="reject_join")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await context.bot.send_photo(
    chat_id=BOT_ADMISSION_CHANNEL_ID,
    photo=photo,
    caption=
    f"Photo from @{user.username or user.first_name+user.last_name}\nid={user.id}",
    reply_markup=reply_markup
  )
  await context.bot.forward_message(
    chat_id=BOT_RECEPTION_CHANNEL_ID,
    from_chat_id=update.message.chat_id,
    message_id=update.message.message_id
  )

  await update.message.reply_text(receipt_receive)
  data["allow_photo_message"] = False


class Handler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is running!")

  def do_HEAD(self):
    self.send_response(200)
    self.end_headers()


if __name__ == "__main__":
  print("Starting bot...")
  server = HTTPServer(("", PORT), Handler)
  threading.Thread(target=server.serve_forever, daemon=True).start()
  app = Application.builder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button))
  app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
  app.add_handler(MessageHandler(filters.ALL, message_handler))

  print("Polling...")
  app.run_polling()

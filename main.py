import os
from dotenv import load_dotenv
from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from constants import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


load_dotenv()

# Access variables
TOKEN: Final = os.getenv("TOKEN")
BOT_ADMISSION_CHANNEL_ID: Final = os.getenv("BOT_ADMISSION_CHANNEL_ID")
PORT = int(os.environ.get("PORT", 10000))


data: dict[str,bool] = {
  "allow_photo_message": False
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if is_group_chat(update):
    await update.message.reply_text(group_chat_warning_message)
    return

  global data
  keyboard = [
    [InlineKeyboardButton(premium_prompt_message, callback_data="opt1")],
    [InlineKeyboardButton(buy_something_prompt_message, callback_data="opt2")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text(welcome_message, reply_markup=reply_markup)
  data["allow_photo_message"] = False

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global data
  query = update.callback_query
  await query.answer()
  if query.data == "opt1":
    await query.edit_message_text(premium_invoice)
    data["allow_photo_message"] = True
  elif query.data == "opt2":
    await query.edit_message_text("ရော့ လိုချင်တဲ့ ဇာတ်ကား")
    data["allow_photo_message"] = False

def is_group_chat(update: Update):
  message_type = update.message.chat.type
  return message_type == "group"

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if is_group_chat(update):
    await update.message.reply_text(group_chat_warning_message)
    return
  await update.message.reply_text(sending_message_warning_1)
  await update.message.reply_text(sending_message_warning_2)

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global data
  if not data["allow_photo_message"]:
    await message_handler(update, context)
    return
  user = update.message.from_user
  photo = update.message.photo[-1].file_id  # last = best quality

  # Forward photo to admin group/channel for review
  await context.bot.send_photo(
    chat_id=BOT_ADMISSION_CHANNEL_ID,
    photo=photo,
    caption=f"Photo from @{user.username or user.first_name}\nဘာလုပ်ချင်လဲဗျ\nApprove? Reject? Cancel? Custom..."
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

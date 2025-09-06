import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from handlers.messages import message_handler
from helpers.http_server import start_http_server
from handlers.start import start
from handlers.buttons import button
from handlers.photos import photo_handler
from handlers.receipt import handle_custom_reject_message


def main():
  if not TOKEN:
    raise RuntimeError("❌ BOT TOKEN is missing from environment variables")

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  logger.info("Starting bot...")
  start_http_server()

  app = Application.builder().token(TOKEN).build()

  handlers = [
    CommandHandler("start", start),
    CallbackQueryHandler(button),
    MessageHandler(filters.PHOTO, photo_handler),
    MessageHandler(filters.REPLY, handle_custom_reject_message),
    MessageHandler(filters.ALL, message_handler),
  ]

  for h in handlers:
    app.add_handler(h)

  logger.info("Polling...")
  app.run_polling()


if __name__ == "__main__":
  main()

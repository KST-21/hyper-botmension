import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ChatMemberHandler, ChatJoinRequestHandler
from config import TOKEN
from handlers.membership import handle_user_left, join_request
from helpers.utils import message_handler
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
    ChatMemberHandler(handle_user_left, ChatMemberHandler.CHAT_MEMBER),
    ChatJoinRequestHandler(join_request),
  ]

  for h in handlers:
    app.add_handler(h)

  logger.info("Polling...")
  app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  main()

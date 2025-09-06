from telegram import Update
from telegram.ext import ContextTypes
from handlers.messages import handle_buy, handle_premium
from handlers.receipt import handle_approve_join, handle_reject_join, handle_custom_reject, handle_cancel_custom_reject


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  if not query or not query.data:
    return

  dispatch = {
    "premium": handle_premium,
    "buy": handle_buy,
    "approve_join": handle_approve_join,
    "reject_join": handle_reject_join,
    "custom_reject": handle_custom_reject,
    "cancel_custom_reject": handle_cancel_custom_reject,
  }

  handler = dispatch.get(query.data)
  if handler:
    await handler(query, context)

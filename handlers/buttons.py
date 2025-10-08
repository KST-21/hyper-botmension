from telegram import Update
from telegram.ext import ContextTypes
from handlers.button_commands.buy import handle_buy
from handlers.button_commands.how_to_subscribe import handle_how_to_subscribe
from handlers.button_commands.invite_private import handle_invite_private
from handlers.button_commands.premium import handle_premium
from handlers.receipt import handle_approve_join, handle_reject_join, handle_custom_reject, handle_cancel_custom_reject


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  if not query or not query.data:
    return

  dispatch = {
    "premium": handle_premium,
    "buy": handle_buy,
    "invite_private": handle_invite_private,
    "how_to_subscribe": handle_how_to_subscribe,
    "approve_join": handle_approve_join,
    "reject_join": handle_reject_join,
    "custom_reject": handle_custom_reject,
    "cancel_custom_reject": handle_cancel_custom_reject,
  }

  handler = dispatch.get(query.data)
  if handler:
    await handler(query, context)

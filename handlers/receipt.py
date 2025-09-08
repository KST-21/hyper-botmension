from telegram import ChatInviteLink, InlineKeyboardButton, Message, Update, CallbackQuery, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.messages import message_handler
from helpers.utils import clean_caption, extract_user_id_from_caption, create_receipt_confirm_markup
from config import BOT_ADMISSION_CHANNEL_ID, data
from constants import channels, receipt_rejected


async def handle_approve_join(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()
  if not isinstance(query.message, Message):
    return

  caption = query.message.caption
  original_user_id = str(caption).split("id=")[1]
  await query.edit_message_caption(f"{caption}\nJoin Approved")

  invite_link: ChatInviteLink = await context.bot.create_chat_invite_link(
    chat_id=channels["fake_premium_channel_id"],
    member_limit=1,
    creates_join_request=False
  )
  await context.bot.send_message(
    chat_id=original_user_id,
    text=f"Premium Channel link\n{invite_link.invite_link}"
  )


async def handle_reject_join(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()
  if not isinstance(query.message, Message):
    return

  caption = query.message.caption
  original_user_id = str(caption).split("id=")[1]
  await query.edit_message_caption(
    f"{caption}\nJoin Rejected\nSent '''{receipt_rejected}''' to user"
  )
  await context.bot.send_message(
    chat_id=original_user_id, text=receipt_rejected
  )
  data["allow_photo_message"].add(int(original_user_id))


async def handle_custom_reject(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  if not isinstance(query.message, Message):
    return

  caption = query.message.caption
  keyboard = [
    [
      InlineKeyboardButton(
        "❌ Cancel Custom Reject", callback_data="cancel_custom_reject"
      )
    ]
  ]
  await query.edit_message_caption(
    f"{caption}\nPlease reply to this message with your custom reject text.",
    reply_markup=InlineKeyboardMarkup(keyboard),
  )
  data["pending_custom_rejects"].add(query.message.message_id)


async def handle_custom_reject_message(
  update: Update, context: ContextTypes.DEFAULT_TYPE
):
  if not update.channel_post:
    await message_handler(update, context)
    return
  receipt_message = update.channel_post.reply_to_message
  if not receipt_message:
    return

  receipt_message_id = receipt_message.message_id

  if receipt_message_id in data["pending_custom_rejects"]:
    reason = update.channel_post.text
    caption = receipt_message.caption
    if not caption:
      return

    original_user_id = extract_user_id_from_caption(caption)
    cleaned_caption = clean_caption(caption)

    await context.bot.send_message(
      chat_id=original_user_id,
      text=f"Admin မှ ယခုလို အကြောင်းပြန်ပါတယ်\n\n{reason}"
    )
    await context.bot.edit_message_caption(
      chat_id=BOT_ADMISSION_CHANNEL_ID,
      message_id=receipt_message_id,
      caption=f"{cleaned_caption}\nSent '''{reason}''' to user."
    )
    data["pending_custom_rejects"].remove(receipt_message_id)


async def handle_cancel_custom_reject(
  query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
  await query.answer()
  if not isinstance(query.message, Message):
    return

  caption = query.message.caption
  if not caption:
    return

  cleaned_caption = clean_caption(caption)
  keyboard = create_receipt_confirm_markup()

  await query.edit_message_caption(
    caption=cleaned_caption, reply_markup=InlineKeyboardMarkup(keyboard)
  )
  data["pending_custom_rejects"].remove(query.message.message_id)

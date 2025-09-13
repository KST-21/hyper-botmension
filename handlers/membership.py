from telegram import ChatMember, Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from config import BOT_RECEPTION_CHANNEL_ID, JOIN_LEAVE_NOTIFICATION_CHANNEL_ID
from helpers.utils import escape_md, get_channel_internal_id, get_channel_reference, get_private_channel_ids, get_public_channel_id, get_user_reference, safe_send_message


async def check_subscription(
  user_id: int, channel_id: int, context: ContextTypes.DEFAULT_TYPE
) -> bool:
  try:
    member = await context.bot.get_chat_member(channel_id, user_id)
    return member.status in (
      ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER
    )
  except:
    return False


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not (update.chat_join_request and BOT_RECEPTION_CHANNEL_ID):
    return

  user = update.chat_join_request.from_user
  user_reference = get_user_reference(user)

  private_channel_ids = get_private_channel_ids(set)

  requested_channel = update.chat_join_request.chat
  if requested_channel.id not in private_channel_ids:
    return

  requested_channel_reference = get_channel_reference(
    requested_channel.id, requested_channel.title
  )

  public_channel = await context.bot.get_chat(get_public_channel_id())
  public_channel_reference = get_channel_reference(
    public_channel.id, public_channel.title
  )

  if await check_subscription(user.id, public_channel.id, context):
    await update.chat_join_request.approve()

    message_to_send = f"{requested_channel_reference} ထဲ ဝင်ခွင့်ပေးလိုက်ပါပြီ"
    await safe_send_message(
      lambda: context.bot.
      send_message(user.id, message_to_send, parse_mode="MarkdownV2"),
      context.bot,
      original_message=message_to_send,
      user_reference=user_reference
    )

    message_to_send = (
      f"{user_reference} ဆိုတဲ့ကောင် {requested_channel_reference} channel ထဲကို ဝင်လာပြီ\n"
      f"{public_channel_reference} channel ကို subscribe လုပ်ထား"
    )
    await safe_send_message(
      lambda: context.bot.send_message(
        chat_id=str(BOT_RECEPTION_CHANNEL_ID),
        text=message_to_send,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
      ),
      context.bot,
      original_message=message_to_send
    )

  else:
    await update.chat_join_request.decline()

    message_to_send = f"{public_channel_reference} ကို အရင် subscribe လုပ်ပြီးမှ ပြန်ဝင်ပါ"
    await safe_send_message(
      lambda: context.bot.
      send_message(user.id, message_to_send, parse_mode="MarkdownV2"),
      context.bot,
      original_message=message_to_send,
      user_reference=user_reference
    )

    message_to_send = (
      f"🚨 **REJECT** 🚨\n\n"
      f"{user_reference} ဆိုတဲ့ကောင် {requested_channel_reference} channel ထဲကို\n"
      f"{public_channel_reference} channel subscribe မလုပ်ဘဲ ဝင်လာလို့\n"
      f"reject လိုက်ပြီ"
    )
    await safe_send_message(
      lambda: context.bot.send_message(
        chat_id=str(BOT_RECEPTION_CHANNEL_ID),
        text=message_to_send,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
      ),
      context.bot,
      original_message=message_to_send
    )


async def handle_user_membership(
  update: Update, context: ContextTypes.DEFAULT_TYPE
):
  result = update.chat_member
  if not (
    result and BOT_RECEPTION_CHANNEL_ID and JOIN_LEAVE_NOTIFICATION_CHANNEL_ID
  ):
    return

  if result.old_chat_member is None:
    return

  user = result.from_user
  user_reference = get_user_reference(user)
  chat = result.chat
  public_channel_id = get_public_channel_id()

  if chat.id != public_channel_id:
    return

  public_channel = await context.bot.get_chat(get_public_channel_id())
  public_channel_reference = get_channel_reference(
    public_channel.id, public_channel.title
  )

  old_status = result.old_chat_member.status
  new_status = result.new_chat_member.status

  if old_status in (
    ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.OWNER
  ) and new_status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
    message_to_send = f"{user_reference} left {public_channel_reference}"
    await safe_send_message(
      lambda: context.bot.send_message(
        chat_id=str(JOIN_LEAVE_NOTIFICATION_CHANNEL_ID),
        text=message_to_send,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
      ),
      context.bot,
      original_message=message_to_send
    )

    private_channel_ids = get_private_channel_ids(tuple)
    for private_channel_id in private_channel_ids:
      if not await check_subscription(user.id, private_channel_id, context):
        continue
      private_channel = await context.bot.get_chat(private_channel_id)
      private_channel_reference = get_channel_reference(
        private_channel.id, private_channel.title
      )

      await context.bot.ban_chat_member(private_channel_id, user.id)
      await context.bot.unban_chat_member(private_channel_id, user.id)

      message_to_send = (
        f"{public_channel_reference} ကို subscribe ဖြုတ်လိုက်လို့\n"
        f"'{private_channel.title}' ကနေ ထုတ်လိုက်ပါတယ်\n"
        f"{public_channel_reference} ကို အရင် subscribe လုပ်ပြီးမှ ပြန်ဝင်ပါ"
      )
      await safe_send_message(
        lambda: context.bot.send_message(
          chat_id=user.id, text=message_to_send, parse_mode="MarkdownV2"
        ),
        context.bot,
        original_message=message_to_send,
        user_reference=user_reference
      )

      message_to_send = (
        f"🚨 **KICK** 🚨\n\n"
        f"{user_reference} ဆိုတဲ့ကောင် {public_channel_reference} channel ကို\n"
        f"subscribe လာဖြုတ်လို့ {private_channel_reference} channel ကနေ\n"
        f"Kick လိုက်ပြီ"
      )
      await safe_send_message(
        lambda: context.bot.send_message(
          chat_id=str(BOT_RECEPTION_CHANNEL_ID),
          text=message_to_send,
          parse_mode="MarkdownV2",
          disable_web_page_preview=True
        ),
        context.bot,
        original_message=message_to_send
      )

  elif old_status in (
    ChatMemberStatus.LEFT, ChatMemberStatus.BANNED
  ) and new_status == ChatMemberStatus.MEMBER:
    message_to_send = f"{user_reference} joined {public_channel_reference}"
    await safe_send_message(
      lambda: context.bot.send_message(
        chat_id=str(JOIN_LEAVE_NOTIFICATION_CHANNEL_ID),
        text=message_to_send,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
      ),
      context.bot,
      original_message=message_to_send
    )

from telegram import ChatMember, Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from config import BOT_RECEPTION_CHANNEL_ID
from helpers.utils import escape_md, get_channel_internal_id, get_private_channel_ids, get_public_channel_id


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
  user_reference = f"[{escape_md(user.full_name)}]({escape_md(f'tg://user?id={user.id}')})"

  private_channel_ids = get_private_channel_ids(set)

  requested_channel = update.chat_join_request.chat
  if requested_channel.id not in private_channel_ids:
    return

  requested_channel_internal_id = get_channel_internal_id(requested_channel.id)
  requested_channel_reference = f"[{escape_md(requested_channel.title or '')}]({escape_md(f'https://t.me/c/{requested_channel_internal_id}/1')})"

  public_channel = await context.bot.get_chat(get_public_channel_id())
  public_channel_internal_id = get_channel_internal_id(public_channel.id)
  public_channel_reference = f"[{escape_md(public_channel.title or '')}]({escape_md(f'https://t.me/c/{public_channel_internal_id}/1')})"

  if await check_subscription(user.id, public_channel.id, context):
    await update.chat_join_request.approve()
    await context.bot.send_message(
      user.id,
      f"{requested_channel_reference} ထဲ ဝင်ခွင့်ပေးလိုက်ပါပြီ",
      parse_mode="MarkdownV2"
    )

    await context.bot.send_message(
      chat_id=BOT_RECEPTION_CHANNEL_ID,
      text=
      f"{user_reference} ဆိုတဲ့ကောင် {requested_channel_reference} channel ထဲကို ဝင်လာပြီ\n{public_channel_reference} channel ကို subscribe လုပ်ထား",
      parse_mode="MarkdownV2"
    )

  else:
    await update.chat_join_request.decline()

    await context.bot.send_message(
      user.id,
      f"{public_channel_reference} ကို အရင် subscribe လုပ်ပြီးမှ ပြန်ဝင်ပါ",
      parse_mode="MarkdownV2"
    )

    await context.bot.send_message(
      chat_id=BOT_RECEPTION_CHANNEL_ID,
      text=
      f"{user_reference} ဆိုတဲ့ကောင် {requested_channel_reference} channel ထဲကို {public_channel_reference} channel subscribe မလုပ်ဘဲ ဝင်လာလို့ reject လိုက်ပြီ",
      parse_mode="MarkdownV2"
    )


async def handle_user_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
  result = update.chat_member
  if not (result and BOT_RECEPTION_CHANNEL_ID):
    return

  if result.old_chat_member is None:
    return

  old_status = result.old_chat_member.status
  new_status = result.new_chat_member.status

  if old_status in (
    ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.OWNER
  ) and new_status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
    user = result.from_user
    user_reference = f"[{escape_md(user.full_name)}]({escape_md(f'tg://user?id={user.id}')})"
    chat = result.chat
    public_channel_id = get_public_channel_id()

    if chat.id != public_channel_id:
      return

    public_channel = await context.bot.get_chat(public_channel_id)
    public_channel_internal_id = get_channel_internal_id(public_channel.id)
    public_channel_reference = f"[{escape_md(public_channel.title or '')}]({escape_md(f'https://t.me/c/{public_channel_internal_id}/1')})"

    private_channel_ids = get_private_channel_ids(tuple)
    for private_channel_id in private_channel_ids:
      if not await check_subscription(user.id, private_channel_id, context):
        continue
      private_channel = await context.bot.get_chat(private_channel_id)
      private_channel_internal_id = get_channel_internal_id(private_channel.id)
      private_channel_reference = f"[{escape_md(private_channel.title or '')}]({escape_md(f'https://t.me/c/{private_channel_internal_id}/1')})"

      await context.bot.ban_chat_member(private_channel_id, user.id)
      await context.bot.unban_chat_member(private_channel_id, user.id)

      await context.bot.send_message(
        chat_id=user.id,
        text=
        f"{public_channel_reference} ကို subscribe ဖြုတ်လိုက်လို့ '{private_channel.title}' ကနေ ထုတ်လိုက်ပါတယ်\n{public_channel_reference} ကို အရင် subscribe လုပ်ပြီးမှ ပြန်ဝင်ပါ",
        parse_mode="MarkdownV2"
      )

      await context.bot.send_message(
        chat_id=BOT_RECEPTION_CHANNEL_ID,
        text=
        f"{user_reference} ဆိုတဲ့ကောင် {public_channel_reference} channel ကို subscribe လာဖြုတ်လို့ {private_channel_reference} channel ကနေ Kick လိုက်ပြီ",
        parse_mode="MarkdownV2"
      )

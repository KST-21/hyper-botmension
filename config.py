import os
from dotenv import load_dotenv
from typing import Final

from helpers.types import Data

load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_ADMISSION_CHANNEL_ID: Final = os.getenv("BOT_ADMISSION_CHANNEL_ID")
BOT_RECEPTION_CHANNEL_ID: Final = os.getenv("BOT_RECEPTION_CHANNEL_ID")
PORT: int = int(os.environ.get("PORT", 10000))

# runtime state (could move to Redis/DB later)
data: Data = {
  "allow_photo_message": False,
  "pending_custom_rejects": set(),
}

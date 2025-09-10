import os
from dotenv import load_dotenv
from typing import Final

from helpers.types import Data

load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_ADMISSION_CHANNEL_ID: Final = os.getenv("BOT_ADMISSION_CHANNEL_ID")
BOT_RECEPTION_CHANNEL_ID: Final = os.getenv("BOT_RECEPTION_CHANNEL_ID")
PORT: int = int(os.environ.get("PORT", 10000))
BETA_BOT_USERNAME: Final = os.getenv("BETA_BOT_USERNAME")
JOIN_LEAVE_NOTIFICATION_CHANNEL_ID: Final = os.getenv(
  "JOIN_LEAVE_NOTIFICATION_CHANNEL_ID"
)

# runtime state (could move to Redis/DB later)
data: Data = {
  "allow_photo_message": set(),
  "pending_custom_rejects": set(),
}

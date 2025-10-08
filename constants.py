from helpers.types import BOT_INFO_TYPE, Channels

BOT_INFO: BOT_INFO_TYPE = {"name": None, "username": None, "is_beta": None}

not_private_chat_warning_message = "You cannot use me in the group chat\nGroup chat တွင် အသုံးပြုခြင်း သည်းခံပါ"
premium_prompt_message = "Premium ရက် ၃၀ ဝင်မယ်"
buy_something_prompt_message = "ဇာတ်ကား ဝယ်မယ်"
request_private_join = "Private Channel ထဲ ဝင်မယ်"
how_to_subscribe = "ဘယ်လို Subscribe လုပ်ရမှာလဲ"
premium_invoice = "KPay number ဘာညာကွိကွကို ပိုက်ဆံ ၃၀၀၀ လွှဲ၍ screenshot ပြန်ပို့ပေးပါ\nscreenshot ကို Admin တစ်ယောက် စစ်ဆေးပြီးပါက Channel ထဲဝင်ဖို့ link ပို့ပေးပါလိမ့်မယ်"
sending_message_warning_1 = "ရွေးချယ်နိုင်သော ခလုတ်များကို နှိပ်၍သာ bot ကို အသုံးပြုပါ"
sending_message_warning_2 = "bot ကို /start ဟု ပို့၍သော်လည်းကောင်း နှိပ်၍သော်လည်းကောင်း ဆက်သွယ်နိုင်ပါသည်\n\nstart မဟုတ်ပါ /start ပါ\nမျဉ်းစောင်းပါပါတယ်\nပြာနေတာကိုပဲ နှိပ်လိုက်လည်း ရပါတယ်\nပို့စရာမလိုပါ"
receipt_receive = "ပြေစာလက်ခံရရှိပါသည်\nအိပ်ချိန်ကလွဲ၍ ကျန်တဲ့အချိန်များတွင် ၃နာရီအတွင်း Admin တစ်ယောက် စစ်ဆေးပြီးလျှင် ဒီကနေ Link ပို့ပေးပါမယ်"
receipt_rejected = "ပြေစာ မှားရွင်းနေပါသည်\nပြေစာပြန်လည် ပေးပို့ပေးပါ"

channels: Channels = {
  "fake_premium_channel_id": -1002917136045,
  "fake_public_channel_id": -1002764951583,
  "fake_private_channels": {
    "testing_private_channel_for_beta": {
      "id": -1002906977198,
      "invite_link": "https://t.me/+3ZP9JUrat30xN2M1"
    }
  },
  "hyper_space": -1002315991423,
  "private_channels": {
    "hyper_space_domain": {
      "id": -1002968318914,
      "invite_link": "https://t.me/+PJDDFRsJyQAwYWFl",
    },
  },
  "premium_channels": {
    "name1": {
      "id": 1234,
      "price": 12345,
    },
    "name2": {
      "id": 5678,
      "price": 67890,
    }
  },
  "bot_resource_channel": {
    "id": -1003142321222,
    "how_to_subscribe": (5, 6, 7)
  }
}

#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from typing import Union
from datetime import datetime, timedelta
from Yukki import cleanmode, app, botname
from Yukki.database import is_cleanmode_on
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=5),
    }
    cleanmode[chat_id].append(put)


async def auto_clean():
    while not await asyncio.sleep(30):
        try:
            for chat_id in cleanmode:
                if not await is_cleanmode_on(chat_id):
                    continue
                for x in cleanmode[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
                    else:
                        continue
        except:
            continue


asyncio.create_task(auto_clean())


RANDOM = [
    "https://telegra.ph/file/52e152c4f036384c84ae1.jpg",
    "https://telegra.ph/file/eb497a972df5836c1ebb9.jpg",
    "https://telegra.ph/file/3bf367b3ca7ccaadf339e.jpg",
    "https://telegra.ph/file/2b372cacca849f487039b.jpg",
    "https://telegra.ph/file/34d55f43d38e55ae001e9.jpg",
    "https://telegra.ph/file/8ff6b3dfbb3abb476c6d4.jpg",
    "https://telegra.ph/file/ec190771212ca366f2cbd.jpg",
    "https://telegra.ph/file/12549f809c7533e6c4197.jpg",
    "https://telegra.ph/file/a8cf5423ea950d28998c0.jpg",
    "https://telegra.ph/file/144551776656b05682d42.jpg",
    "https://telegra.ph/file/a2ea5c6d1099be896d79f.jpg"
]


HELP_TEXT = f"""Welcome to {botname}'s Help Section.

- When someone mentions you in a chat, the user will be notified you are AFK. You can even provide a reason for going AFK, which will be provided to the user as well.


/afk - This will set you offline.

/afk [Reason] - This will set you offline with a reason.

/afk [Replied to a Sticker/Photo] - This will set you offline with an image or sticker.

/afk [Replied to a Sticker/Photo] [Reason] - This will set you afk with an image and reason both.


/settings - To change or edit basic settings of AFK Bot.
"""

def settings_markup(status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Clean Mode", callback_data="cleanmode_answer"),
            InlineKeyboardButton(
                text="✅ Enabled" if status == True else "❌ Disabled",
                callback_data="CLEANMODE",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 Close Menu", callback_data="close"),
        ],
    ]
    return buttons

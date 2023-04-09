#
# Copyright (C) 2021-2022 by Vir99@Github, < https://github.com/Vir99 >.
#
# This file is part of < https://github.com/Vir99/Afk-Robot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Vir99/Afk-Robot/blob/master/LICENSE >
#
# All rights reserved.

import re
import time

from pyrogram import filters
from pyrogram.types import Message

from Afk-Robot import app, botid, botname, botusername
from Afk-Robot.database import add_served_chat, is_afk, remove_afk
from Afk-Robot.helpers import get_readable_time, put_cleanmode

chat_watcher_group = 1

@app.on_message(
    ~filters.edited & ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    if message.entities:
        possible = ["/afk", f"/afk@{botusername}"]
        message_text = message.text or message.caption
        for entity in message.entities:
            if entity.type == "bot_command":
                if (message_text[0 : 0 + entity.length]).lower() in possible:
                    return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\n"
            if afktype == "text_reason":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n"
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
        except:
            msg += f"**{user_name}** is back online\n\n"
        
    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = (
                message.reply_to_message.from_user.first_name
            )
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time(
                        (int(time.time() - timeafk))
                    )
                    if afktype == "text":
                        msg += f"**{replied_first_name}** is AFK since {seenago}\n\n"
                    if afktype == "text_reason":
                        msg += f"**{replied_first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name}** is AFK since {seenago}\n\n",
                            )
                        else:
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name}** is AFK since {seenago}\n\n",
                            )
                        else:
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                except Exception as e:
                    msg += f"**{replied_first_name}** is AFK\n\n"
        except:
            pass

    # If username or mentioned user is AFK
    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == "mention":
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{user.first_name}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{user.first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except:
                        msg += (
                            f"**{user.first_name}** is AFK\n\n"
                        )
            elif (entity[j].type) == "text_mention":
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{first_name}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except:
                        msg += f"**{first_name}** is AFK\n\n"
            j += 1
    if msg != "":
        try:
            send =  await message.reply_text(
                msg, disable_web_page_preview=True
            )
        except:
            return
    try:
        await put_cleanmode(message.chat.id, send.message_id)
    except:
        return


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == botid:
                send =  await message.reply_text(
                    f"[🧸](https://telegra.ph/file/9862778047d4e4e2ad1fa.jpg) Tʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ 😝\n\n {message.chat.title} 🌹\n\n ◍━━•━━•●●•━━•━━◍\n\n🧸 𝘉𝘖𝘛 𝘜𝘚𝘈𝘎𝘌 ⚙️\n\n○ Mᴀᴋᴇ ᴍᴇ Aᴅᴍɪɴ Fɪʀsᴛ 🖇\n\n○ /afk Yᴏᴜʀ ᴀғᴋ ʀᴇᴀsᴏɴ\n\nEɴᴊᴏʏ Aғᴋ Rᴏʙᴏᴛ 🤖 🎶\n\n ◍━━•━━•●●•━━•━━◍\n\n  {botname}\n\n**Bᴏᴛ's Oᴡɴᴇʀ ☆ [Vɪʀ](https://t.me/ITZVIR99)**\n**Pᴏᴡᴇʀᴇᴅ Bʏ ☆ [Rᴏᴄᴋs](https://t.me/rocks_official)**\n"
                ) 

                await put_cleanmode(message.chat.id, send.message_id)
        except:
            return

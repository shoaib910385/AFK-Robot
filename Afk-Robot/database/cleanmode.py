#
# Copyright (C) 2021-2022 by Vir99@Github, < https://github.com/Vir99 >.
#
# This file is part of < https://github.com/Vir99/Afk-Robot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Vir99/Afk-Robot/blob/master/LICENSE >
#
# All rights reserved.
#

from Afk-Robot import db

cleandb = db.cleanmode
cleanmode = {}


async def is_cleanmode_on(chat_id: int) -> bool:
    mode = cleanmode.get(chat_id)
    if not mode:
        user = await cleandb.find_one({"chat_id": chat_id})
        if not user:
            cleanmode[chat_id] = True
            return True
        cleanmode[chat_id] = False
        return False
    return mode


async def cleanmode_on(chat_id: int):
    cleanmode[chat_id] = True
    user = await cleandb.find_one({"chat_id": chat_id})
    if user:
        return await cleandb.delete_one({"chat_id": chat_id})


async def cleanmode_off(chat_id: int):
    cleanmode[chat_id] = False
    user = await cleandb.find_one({"chat_id": chat_id})
    if not user:
        return await cleandb.insert_one({"chat_id": chat_id})


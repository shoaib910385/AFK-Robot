#
# Copyright (C) 2021-2022 by Vir99@Github, < https://github.com/Vir99 >.
#
# This file is part of < https://github.com/Vir99/Afk-Robot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Vir99/Afk-Robot/blob/master/LICENSE >
#
# All rights reserved.


import asyncio
import importlib

from pyrogram import idle

from Afk-Robot.modules import ALL_MODULES

loop = asyncio.get_event_loop()


async def initiate_bot():
    for all_module in ALL_MODULES:
        importlib.import_module("Afk-Robot.modules." + all_module)
    print("Started TheAFKRobot.")
    await idle()
    print("GoodBye! Stopping Bot")


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())

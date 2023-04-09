#
# Copyright (C) 2021-2022 by Vir99@Github, < https://github.com/Vir99 >.
#
# This file is part of < https://github.com/Vir99/Afk-Robot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Vir99/Afk-Robot/blob/master/LICENSE >
#
# All rights reserved.
#

from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Get it from my.telegram.org
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

## Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Database to save your chats and stats... Get MongoDB:-  https://notreallyshikhar.gitbook.io/Afk-Robotmusicbot/deployment/mongodb#4.-youll-see-a-deploy-cloud-database-option.-please-select-shared-hosting-under-free-plan-here
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# SUDO USERS
SUDO_USER = list(
    map(int, getenv("SUDO_USER", "").split())
)  # Input type must be interger

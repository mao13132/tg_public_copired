# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import os

from src.sql.bot_connector import BotDB
from src.telegram.sheduler_scrap_chanels import ShedulerScrapChanels


async def main():
    path_dir_project = os.path.dirname(__file__)

    res_job = await ShedulerScrapChanels(path_dir_project, BotDB).start_job()


if __name__ == '__main__':

    try:
        asyncio.run(main())

    finally:

        print(f'Бот остановлен')

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

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import TIMER_POSTS, TIME_ONE_POST, TIME_TWO_POST, TIME_THREE_POST
from src.sql.bot_connector import BotDB
from src.telegram.bot_core import Core
from src.telegram.handlers.users import register_user
from src.telegram.sheduler_add_post_in_channel import ShedulerAddPostInChannels
from src.telegram.sheduler_scrap_chanels import ShedulerScrapChanels


def registration_all_handlers(dp):
    register_user(dp)


async def main():
    path_dir_project = os.path.dirname(__file__)

    bot_start = Core()

    registration_all_handlers(bot_start.dp)

    scheduler = AsyncIOScheduler()

    # scheduler.add_job(ShedulerAddPostInChannels(bot_start, BotDB).start_add_post, 'interval', seconds=2,
    #                   misfire_grace_time=300)

    _time_one_post = TIME_ONE_POST.split(':')

    scheduler.add_job(ShedulerAddPostInChannels(bot_start, BotDB).start_add_post, 'cron', hour=int(_time_one_post[0]),
                      minute=int(_time_one_post[1]), misfire_grace_time=300)

    _time_two_post = TIME_TWO_POST.split(':')

    scheduler.add_job(ShedulerAddPostInChannels(bot_start, BotDB).start_add_post, 'cron', hour=int(_time_two_post[0]),
                      minute=int(_time_two_post[1]), misfire_grace_time=300)

    _time_three_post = TIME_THREE_POST.split(':')

    scheduler.add_job(ShedulerAddPostInChannels(bot_start, BotDB).start_add_post, 'cron', hour=int(_time_three_post[0]),
                      minute=int(_time_three_post[1]), misfire_grace_time=300)

    scheduler.add_job(ShedulerScrapChanels(path_dir_project, BotDB).start_job, 'interval', misfire_grace_time=300,
                      seconds=TIMER_POSTS)

    scheduler.start()

    try:
        await bot_start.dp.start_polling()
    finally:
        await bot_start.dp.storage.close()
        await bot_start.dp.storage.wait_closed()
        await bot_start.bot.session.close()


if __name__ == '__main__':

    try:
        asyncio.run(main())

    finally:

        print(f'Бот остановлен')

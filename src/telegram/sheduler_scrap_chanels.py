# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

import os

from src.telegram.tg_auth_module import TgAuthModule
from src.telegram.tg_clear_old_posts import TgClearOldPosts
from src.telegram.tg_module_scrap import TgModuleScrap


class ShedulerScrapChanels:
    def __init__(self, path_dir_project, BotDB):
        self.path_dir_project = path_dir_project
        self.BotDB = BotDB

    async def start_job(self):
        sessions_path = os.path.join(self.path_dir_project, 'src', 'sessions')

        bot_core = TgAuthModule(sessions_path, self.BotDB)

        telegram_core = await bot_core.start_tg()

        if not telegram_core:
            return False

        print(f'Успешно авторизовался в user bote')

        posts_list = await TgModuleScrap(telegram_core, self.BotDB, self.path_dir_project).start_scrap_channels()

        print(f'Собрал {len(posts_list["posts"])} постов')

        res_clear = TgClearOldPosts(self.BotDB).start_clear_old_posts()

        print()

# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime

from settings import ADMIN_ID, ID_MY_CHANEL
from src.telegram.delete_media import delete_media


class ShedulerAddPostInChannels:
    def __init__(self, bot_start, BotDB):
        self.bot = bot_start.bot

        self.BotDB = BotDB

    async def posting_post(self, post):
        msg_id = post[3]

        post_text = post[4]

        source = post[5]

        media_list = self.BotDB.get_list_media(msg_id, source)

        media_file = media_list[0][2]

        try:
            with open(media_file, 'rb') as file:
                await self.bot.send_video(ID_MY_CHANEL, file, caption=post_text)
        except:
            return False

        res_del_media = delete_media(self.BotDB, media_list)

        return True

    async def start_add_post(self):
        posts_list = self.BotDB.get_active_post()

        if posts_list == []:
            self.bot.send_message(ADMIN_ID, 'База данных пуста. Нет новых постов для публикации в канал')

            return True

        posts_list = sorted(posts_list, key=lambda tup: datetime.strptime(tup[2], '%Y-%m-%d %H:%M:%S'))

        post = posts_list[0]

        post_id_pk = post[0]

        res_add_post = await self.posting_post(post)

        if res_add_post:
            self.BotDB.publisher_post(post_id_pk)

            return True

        return False

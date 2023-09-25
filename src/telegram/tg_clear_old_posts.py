# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os
from datetime import datetime

from settings import MAX_POSTS_BASE


class TgClearOldPosts:
    def __init__(self, BotDB):
        self.BotDB = BotDB

    def delete_media(self, list_media):

        for _media in list_media:

            id_pk = _media[0]

            media_patch = _media[2]

            try:
                os.remove(media_patch)
            except:
                pass

            self.BotDB.delete_media_from_pk(id_pk)

        return True

    def delete_sql_rows(self, posts_list):

        posts_list = sorted(posts_list, key=lambda tup: datetime.strptime(tup[2], '%Y-%m-%d %H:%M:%S'))

        count_delete = len(posts_list) - MAX_POSTS_BASE

        for ind_post in range(count_delete):

            row_post = posts_list[ind_post]

            id_pk = row_post[0]

            msg_id = row_post[3]

            source = row_post[5]

            media_list = self.BotDB.get_list_media(msg_id, source)

            res_del_media = self.delete_media(media_list)

            self.BotDB.delete_post(id_pk)

            print()

        return True

    def start_clear_old_posts(self):
        count_posts = self.BotDB.get_count_posts()

        if count_posts > MAX_POSTS_BASE:
            posts_list = self.BotDB.get_active_post()

            res_clear = self.delete_sql_rows(posts_list)

        return True

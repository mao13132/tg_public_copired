# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import MAX_POSTS_BASE


class TgClearOldPosts:
    def __init__(self, BotDB):
        self.BotDB = BotDB

    def delete_sql_rows(self, posts_list):

        for post in posts_list:
            print()

        return True

    def start_clear_old_posts(self):
        count_posts = self.BotDB.get_count_posts()

        if count_posts > MAX_POSTS_BASE:
            posts_list = self.BotDB.get_active_post()

            res_clear = self.delete_sql_rows(posts_list)

        print()

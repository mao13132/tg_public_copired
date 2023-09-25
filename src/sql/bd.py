import datetime
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"posts (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_chat TEXT, date DATETIME, message_id TEXT, text TEXT, "
                                f"source TEXT, title TEXT, active BOOLEAN DEFAULT 1, "
                                f"publish BOOLEAN DEFAULT 0, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table posts {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"media (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"message_id TEXT, path TEXT, source TEXT, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table media {es}')

    def exist_post(self, id_chat, title, date_post):
        try:
            result = self.cursor.execute(f"SELECT * FROM posts WHERE id_chat='{id_chat}' AND date='{date_post}' "
                                         f"AND title='{title}' AND active='1'")

            response = result.fetchall()

        except Exception as es:
            print(f'Ошибка при проверки существования записи из TG канала "{es}"')
            return False

        if response == []:
            return False

        return True

    def add_message(self, id_chat, message_id, title, text, source, date_post):

        result = self.cursor.execute(f"SELECT * FROM posts WHERE id_chat='{id_chat}' AND title='{title}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute("INSERT OR IGNORE INTO posts ('id_chat', 'message_id', 'title', 'text', 'source', "
                                "'date') VALUES (?,?,?,?,?,?)",
                                (id_chat, message_id, title, text, source,
                                 date_post,))

            self.conn.commit()
            return True

        return False

    def save_media(self, message_id, path, source):

        result = self.cursor.execute(f"SELECT * FROM media WHERE path='{path}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute("INSERT OR IGNORE INTO media ('message_id', 'path', 'source') VALUES (?,?,?)",
                                (message_id, path, source,))

            self.conn.commit()
            return True

        return False

    def get_count_posts(self):

        result = self.cursor.execute(f"SELECT count(*) FROM posts WHERE active='1' and publish='0'")

        response = result.fetchall()

        try:
            response = response[0][0]
        except:
            return False

        return response

    def get_active_post(self):

        result = self.cursor.execute(f"SELECT * FROM posts WHERE active='1' and publish='0'")

        response = result.fetchall()

        return response

    def get_list_media(self, message_id, source):

        result = self.cursor.execute(f"SELECT * FROM media WHERE message_id='{message_id}' AND source='{source}'")

        response = result.fetchall()

        return response

    def delete_media_from_pk(self, id_pk):

        result = self.cursor.execute(f"DELETE FROM media WHERE id_pk = '{id_pk}'")

        self.conn.commit()

        return True

    def delete_post(self, id_pk):

        result = self.cursor.execute(f"DELETE FROM posts WHERE id_pk = '{id_pk}'")

        self.conn.commit()

        return True

    def publisher_post(self, id_pk):

        self.cursor.execute(f"UPDATE posts SET publish='1' WHERE id_pk = '{id_pk}'")

        self.conn.commit()

        return True

    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')

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
from datetime import datetime

from settings import TELEGRAM_CHANNELS, count_message_new_chat
from src.telegram.formated_title import get_title


class TgModuleScrap:
    def __init__(self, telegram_core, BotDB, path_dir_project):
        """@developer_telegrams"""
        self.telegram_core = telegram_core
        self.BotDB = BotDB
        self.app = telegram_core.app
        self.path_dir_project = path_dir_project
        self.black_list = ['http']

    async def get_id_chat(self, name_link):
        try:

            name_chat = name_link.replace('https://t.me/', '')

        except Exception as es:
            print(f'Не могу получить вырезать имя чата "{name_link}" "{es}"')

            return False

        while True:

            try:

                res_chat = await self.app.get_chat(name_chat)

            except Exception as es:
                print(f'Исключения при получение ID чат {es}')
                return False

            id_chat = res_chat.id

            return id_chat

    async def download_media(self, list_rows_media):
        good_media_list = []

        text_message = ''

        for row in list_rows_media:
            if row.caption:
                text_message = row.caption

            good_media = await self.app.download_media(row)

            good_media_list.append(good_media)

        return good_media_list, text_message

    async def delete_media(self, list_media):

        for _media in list_media:
            try:
                os.remove(_media)
            except:
                pass

        return True

    async def check_black_word(self, text):
        for _bl_word in self.black_list:
            if _bl_word in text:
                return True

        return False

    async def start_monitoring_chat(self, chat_id, link_chat):

        stop_title_list = []

        id_media_list = []

        good_post = []

        count = 1

        async for message in self.app.get_chat_history(chat_id):

            date_post = message.date

            test_msg = message.caption if message.text is None else message.text

            if test_msg is None:
                continue

            check_black = await self.check_black_word(test_msg)

            if check_black:
                continue

            count += 1

            _title = get_title(test_msg)

            # TODO проверка на ссылку
            if _title in stop_title_list:
                continue

            stop_title_list.append(_title)

            sql_res = self.BotDB.exist_message(chat_id, _title)

            if sql_res:
                # await self.delete_media(good_media_list)
                continue

            one_post = {}

            media_group_id = message.media_group_id

            if media_group_id:

                if media_group_id in id_media_list:
                    continue

                id_media_list.append(media_group_id)

                media_ = await message.get_media_group()

                good_media_list, text_msg = await self.download_media(media_)

            else:
                try:
                    good_media_list = [await self.app.download_media(message)]
                except:
                    good_media_list = []

                text_msg = message.caption

                if not text_msg:
                    text_msg = message.text

            if not text_msg and good_media_list == []:
                continue

            one_post['text'] = text_msg
            one_post['media'] = good_media_list
            one_post['source'] = link_chat
            one_post['chat_id'] = chat_id
            one_post['message_id'] = message.id

            sql_res = self.BotDB.add_message(chat_id, message.id, _title, text_msg, link_chat, date_post)

            for _media in good_media_list:
                self.BotDB.save_media(message.id, _media, link_chat)

            good_post.append(one_post)

            print(f'{datetime.now().strftime("%H:%M:%S")} #{count} '
                  f'Получаю сообщение ID: {message.id} от {date_post}')

            if count > count_message_new_chat:
                msg = f'Достиг лимит на сообщения в чате {link_chat}. Останавливаюсь'

                print(msg)

                return good_post

        return good_post

    async def start_scrap_channels(self):

        job = {'posts': []}

        for link_chat in TELEGRAM_CHANNELS:

            id_chat = await self.get_id_chat(link_chat)

            if not id_chat:
                return False

            print(f'\n{datetime.now().strftime("%H:%M:%S")} Получаю сообщения из чата: {link_chat}\n')

            dict_post = await self.start_monitoring_chat(id_chat, link_chat)

            job['posts'].extend(dict_post)

        return job

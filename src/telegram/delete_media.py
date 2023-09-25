# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os


def delete_media(BotDB, list_media):
    for _media in list_media:

        id_pk = _media[0]

        media_patch = _media[2]

        try:
            os.remove(media_patch)
        except:
            pass

        BotDB.delete_media_from_pk(id_pk)

    return True

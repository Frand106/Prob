from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import os
import shutil

from userbot.config import (API_ID, API_HASH, SESSION_STRING,
                            SOURCE_CHANNEL, TARGET_CHANNEL, DICT_OF_PARS)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

bd_of_bds = {}


def replace_parametrs_in_bd(to_replace: dict, path_to_bd: str):
    with open(path_to_bd, 'r') as file:
        lines = file.read().split('\n')
        for lineid, line in enumerate(lines):
            if line != '':
                line_list = line.split(',')
                for key, value in to_replace.items():
                    try:
                        a = value
                        b = DICT_OF_PARS[key]
                        temp = line_list[b]
                        line_list[b] = line_list[a]
                        line_list[a] = temp
                    except IndexError:
                        pass
                    lines.pop(lineid)
                    lines.insert(lineid, ','.join(line_list))
                    print(line_list)
        for i in range(100):
            print()
        with open(path_to_bd, 'w') as file_w:
            file_w.write('\n'.join(lines))


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler_new_message(event):
    async for message in client.iter_messages(TARGET_CHANNEL, reverse=True):
        if message.id != 1:
            if not not message.media:
                name_of_downloaded_file = await client.download_media(message=message.media)
                if name_of_downloaded_file not in os.listdir('BDs/'):
                    shutil.move(name_of_downloaded_file, 'BDs/' + name_of_downloaded_file)
                    pars_of_file = message.text.split(':')[1].split(';')
                    to_replace = {}
                    for iid, i in enumerate(pars_of_file):
                        try:
                            if DICT_OF_PARS[i] != iid:
                                to_replace[i] = iid
                        except KeyError:
                            pass
                    print(to_replace)
                    replace_parametrs_in_bd(to_replace, 'BDs/' + name_of_downloaded_file)
                else:
                    os.remove(name_of_downloaded_file)


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()

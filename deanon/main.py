import csv

from aiogram import Bot, executor
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import IDFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os

from basicbot import config


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())


def format_phone_number(number):
    list_number = list(number)
    assert list_number[0] == '7' or list_number[0] == '8'
    list_number.pop(0)
    if list_number[0] == '7':
        list_number.insert(0, 8)
    elif list_number[0] == '8':
        list_number.insert(0, 7)
    return ''.join(list_number)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Пошёл ты нахуй, антоша ёбанный')


@dp.message_handler(commands=['number'])
async def number_command(message: types.Message):
    if not not message.get_args():
        print(message.text)
        a = {}
        for file_name in os.listdir('BDs/'):
            with open('BDs/' + file_name, encoding='utf-8') as r_file:
                file_reader = csv.DictReader(r_file, delimiter=",")
                for line in file_reader:
                    if line['ph_number'] == message.get_args() or \
                            line['ph_number'] == format_phone_number(message.get_args()):
                        for key, value in config.DICT_OF_PARS.items():
                            try:
                                a[key] = line[key]
                            except KeyError:
                                pass
        if not not a:
            await message.answer('Вот что мне удалось найти:')
            for key, value in config.DICT_OF_PARS_MESSAGES.items():
                if key != 'govn':
                    try:
                        await message.answer(value + a[key])
                    except KeyError:
                        pass
        else:
            await message.answer('К сожалению, мне не удалось ничего найти о человеке с этим номером')
    else:
        await message.answer('Вы неправильно используете бота.\n'
                             'Напишите ему /number номер_телефона')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import generate_languages
from googletrans import Translator
from configs import LANGUAGES
from database import create_history_table, insert_into_history


bot = TeleBot('6900479217:AAEdtixKM2DvkcEzFjxcJOdKJbksNu2lQ8w')


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    create_history_table()
    chat_id = message.chat.id
    text = "Привет. Это бот переводчик."
    bot.send_message(chat_id, text)
    get_lang(message)


def get_lang(message: Message):
    chat_id = message.chat.id
    text = 'Выберите язык для перевода: '
    msg = bot.send_message(chat_id, text, reply_markup=generate_languages())
    bot.register_next_step_handler(msg, get_lang_ask_text)


def get_lang_ask_text(message: Message):
    chat_id = message.chat.id
    lang = message.text
    bot.send_message(chat_id, f'Вы выбрали язык {lang}')
    msg = bot.send_message(chat_id, 'Введите текст для перевода: ', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_text_start_translate, lang)


def get_text_start_translate(message: Message, lang):
    chat_id = message.chat.id
    text = message.text
    rifkat = Translator()
    translated_text = rifkat.translate(text=text, src='ru', dest=get_key(lang)).text
    bot.send_message(chat_id, translated_text)
    insert_into_history(chat_id=chat_id, original_text=text, translated_text=translated_text, lang=lang)
    get_lang(message)


def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k


bot.polling(non_stop=True)

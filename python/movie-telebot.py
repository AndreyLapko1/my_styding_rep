import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import app


bot = telebot.TeleBot('7855375894:AAE8jf5q-RgYlhIZRGDqwapMZiNinjpqAP0')


@bot.message_handler(commands=['start'])
def start_message(message):

    keyboard = InlineKeyboardMarkup(row_width=2)


    button1 = InlineKeyboardButton('Поиск по году', callback_data='btn1')
    button2 = InlineKeyboardButton('Поиск по жанру', callback_data='btn2')
    button3 = InlineKeyboardButton('Поиск по ключевому слову', callback_data='btn3')
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'btn1':
        bot.send_message(call.message.chat.id, "Введите год: ")
        bot.register_next_step_handler(call.message, handle_year)
    elif call.data == 'btn2':
        bot.send_message(call.message.chat.id, "Введите жанр")
    elif call.data == 'btn3':
        bot.send_message(call.message.chat.id, "Введите ключевое слово")

    elif call.data.startswith('add_year:'):
        bot.answer_callback_query(call.id)
        year = call.data.split(':')[1]
        bot.send_message(call.message.chat.id, f'Фильтр по году {year} добавлен!')

    elif call.data == f'No':
        year = user_states.get(call.message.chat.id)
        bot.send_message(call.message.chat.id, f'{year}')
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Фильмы по выбранному вами году: ')
        app = main_.App()
        app.search_year(int(year), join_category='n')


user_states = {}

def handle_year(message):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        year = int(message.text)
        user_states[message.chat.id] = year
        button1 = InlineKeyboardButton('Да', callback_data=f'add_year:{year}')
        button2 = InlineKeyboardButton('Нет', callback_data=f'No')
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id, f'Год {year} принят. Хотите добавить фильтр жанра?', reply_markup=keyboard)

    except ValueError:
        bot.send_message(message.chat.id, "Введите корректный год (число).")
        bot.register_next_step_handler(message, handle_year)




bot.polling(none_stop=True)







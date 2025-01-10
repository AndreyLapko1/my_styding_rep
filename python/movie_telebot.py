import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from app import App
from app import Database, QueryDatabase



token = '7855375894:AAE8jf5q-RgYlhIZRGDqwapMZiNinjpqAP0'
bot = telebot.TeleBot(token)
app = App(bot)


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

    elif call.data.startswith('add_category:'):
        bot.answer_callback_query(call.id)
        year = call.data.split(':')[1]
        bot.send_message(call.message.chat.id, f'Выберите категорию')
        app.search_year(call.message.chat.id, year, join_category='y')

    elif call.data == f'No':
        year = user_states.get(call.message.chat.id)
        bot.send_message(call.message.chat.id, f'{year}')
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Фильмы по выбранному вами году: ')
        app.search_year(call.message.chat.id, year, join_category='n')

    elif call.data.startswith('category_'):
        category_index = int(call.data.split('_')[1])
        categories = app.db.show_categories()
        if category_index < len(categories):
            selected_category = categories[category_index][1]
            bot.send_message(call.message.chat.id, f'Selected: {selected_category}')
        else:
            bot.send_message(call.message.chat.id, "Invalid category selected.")




user_states = {}

def handle_year(message):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        year = int(message.text)
        user_states[message.chat.id] = year
        button1 = InlineKeyboardButton('Да', callback_data=f'add_category:{year}')
        button2 = InlineKeyboardButton('Нет', callback_data=f'No')
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id, f'Год {year} принят. Хотите добавить фильтр жанра?', reply_markup=keyboard)

    except ValueError:
        bot.send_message(message.chat.id, "Введите корректный год (число).")
        bot.register_next_step_handler(message, handle_year)




bot.polling(none_stop=True)







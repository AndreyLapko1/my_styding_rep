import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from app import App
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token")
bot = telebot.TeleBot(token)
app = App(bot)
user_states = {}


@bot.message_handler(commands=['start'])
def start_message(message):

    inline_keyboard = InlineKeyboardMarkup(row_width=2)

    button1 = InlineKeyboardButton('Поиск по году', callback_data='btn1')
    button2 = InlineKeyboardButton('Поиск по жанру', callback_data='btn2')
    button3 = InlineKeyboardButton('Поиск по ключевому слову', callback_data='btn3')
    button4 = InlineKeyboardButton('Просмотр 5 самых популярных запросов', callback_data='btn4')
    exit_button = InlineKeyboardButton('Выход', callback_data='exit_button')
    inline_keyboard.add(button1, button2, button3, button4, exit_button)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=inline_keyboard)

def close_resources():
    app.db.close()
    app.tracker.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'exit_button':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f'Bye!')
        close_resources()
        bot.stop_polling()
        os._exit(0)

    elif call.data == 'btn1':
        bot.send_message(call.message.chat.id, "Введите год: ")
        bot.register_next_step_handler(call.message, handle_year)
    elif call.data == 'btn2':
        app.search_only_by_ctg(call.message.chat.id)

    elif call.data == 'btn3':
        bot.send_message(call.message.chat.id, "Введите ключевое слово")
        bot.register_next_step_handler(call.message, handle_keyword)
    elif call.data == 'btn4':
        app.most_common_queries(call.message.chat.id)

    elif call.data.startswith('add_category:'):
        bot.answer_callback_query(call.id)
        year = call.data.split(':')[1]
        bot.send_message(call.message.chat.id, f'Выберите категорию')
        app.search_by_year(call.message.chat.id, year, join_category='y')

    elif call.data == 'No':
        year = user_states.get(call.message.chat.id)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f'Фильмы по {year} году: ')
        app.search_by_year(call.message.chat.id, year, join_category='n')

    elif call.data == 'return':
        start_message(call.message)

    elif call.data.startswith('onlyctg_'):
        category_index = int(call.data.split('_')[1])
        categories = app.db.show_categories()
        if category_index < len(categories):
            selected_category = categories[category_index][1]
            app.search_by_category_year(call.message.chat.id, selected_category)
        else:
            bot.send_message(call.message.chat.id, "Invalid category selected.")

    elif call.data.startswith('category_'):
        category_index = int(call.data.split('_')[1])
        categories = app.db.show_categories()
        year = user_states.get(call.message.chat.id)
        if category_index < len(categories):
            if year:
                selected_category = categories[category_index][1]
                bot.send_message(call.message.chat.id, f'Selected: {selected_category}')
                app.search_by_category_year(call.message.chat.id, category=selected_category, year=year)
            else:
                selected_category = categories[category_index][1]
                app.search_by_category_year(call.message.chat.id, selected_category)

        else:
            bot.send_message(call.message.chat.id, "Invalid category selected.")

    elif call.data.startswith('film_'):
        film = call.data.split('_')[1]
        result = app.db.search_info(film)
        if result:
            app.show_film_info(call.message.chat.id,result)
        print(film)


    elif call.data.startswith('mcommon_'):
        pattern = call.data.split('_')[1]
        if ', ' in pattern:
            func = app.db.search_by_category_year.__name__
            pattern = pattern.split(', ')
            result = app.db.search_by_category_year(pattern[1], pattern[0])
            app.display(call.message.chat.id, results=result, func=func)
            app.tracker.tracker('Category and Year', pattern[0] + ', ' + pattern[1])
        else:
            try:
                if isinstance(int(pattern), int):
                    func = app.db.search_by_year.__name__
                    result = app.db.search_by_year(pattern)
                    app.display(call.message.chat.id, pattern=pattern,results=result, func=func)
                    app.tracker.tracker('Year', pattern)
            except ValueError:
                if isinstance(pattern, str):
                    func = app.db.search_by_category_year.__name__
                    result = app.db.search_by_category_year(pattern)
                    app.display(call.message.chat.id, pattern=pattern, results=result, func=func)
                    app.tracker.tracker('Category', pattern)

    elif call.data.startswith('s/'):
        pattern = call.data.split('/')[1]
        func = call.data.split('/')[2]
        offset = int(call.data.split('/')[3]) + 10
        print(offset,'in another file')
        app.display(call.message.chat.id, pattern=pattern, more=True, func=func, offset=offset)

    elif call.data == 'dontshow':
        start_message(call.message)



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


def handle_keyword(message):
        keyword = message.text
        user_states[message.chat.id] = keyword
        if not any(char.isdigit() for char in keyword):
            bot.send_message(message.chat.id, f'Слово \'{keyword}\' принято!')
            app.search_by_keyword(message.chat.id, keyword)
        else:
            bot.send_message(message.chat.id, 'Вы ввели число. Введите слово: ')
            bot.register_next_step_handler(message, handle_keyword)



if __name__ == '__main__':
    bot.polling()




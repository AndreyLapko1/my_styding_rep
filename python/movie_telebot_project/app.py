from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import QueryDatabaseWrite, FilmDatabase
from images import genre_images
import random

class App:
    def __init__(self, bot):
        self.bot = bot
        self.db = FilmDatabase()
        self.tracker = QueryDatabaseWrite()

    def display(self, chat_id, results=None, pattern=None,  offset=0, more=False, func=None):
        keyboard = InlineKeyboardMarkup()
        if more:
            method = getattr(self.db, func)
            new_results = method(pattern, offset=offset)

            if new_results:
                self.display(chat_id, results=new_results, pattern=pattern, func=method.__name__, offset=offset)
                return
            else:
                keyboard.add(InlineKeyboardButton(text=f'Return', callback_data=f'return'))
                self.bot.send_message(chat_id, "No more results.", reply_markup=keyboard)
                return

        if isinstance(results, list) or isinstance(results, tuple):
            films_by_page = 10
            print(results[:10])

            for row in results[:films_by_page]:
                print(row[0])
                keyboard.add(InlineKeyboardButton(text=f'{row[0].capitalize()}', callback_data=f'film_{row[0]}'))

            if len(results) < films_by_page or len(results) == 0:
                keyboard.add(InlineKeyboardButton(text=f'Return', callback_data=f'return'))
                if len(results) == 0:
                    self.bot.send_message(chat_id, "Нет таких фильмов :(", reply_markup=keyboard)
                    return


            self.bot.send_message(chat_id, "Selected films:", reply_markup=keyboard)

            if len(results) >= films_by_page:
                show_more_keyboard = InlineKeyboardMarkup()
                print(offset)
                show_more_keyboard.add(InlineKeyboardButton(text="Yes", callback_data=f"s/{pattern}/{func}/{offset}"))
                show_more_keyboard.add(InlineKeyboardButton(text="No", callback_data="dontshow"))
                self.bot.send_message(chat_id, "Show more? :", reply_markup=show_more_keyboard)
                return
        else:
            print("Results is not a list:", results)
            self.bot.send_message(chat_id, "Error: Results are not in the correct format.")


    def show_film_info(self,chat_id, film):
        print(film)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Return", callback_data="return"))

        film_genre = film[0][1]
        if film_genre in genre_images and isinstance(genre_images[film_genre], list):
            image_path = random.choice(genre_images[film_genre])
        else:
            image_path = genre_images.get(film_genre, "C:/Users/andre/Desktop/img/default.jpg")

        film_dict = {"name": film[0][0], "genre": film[0][1], "descrip": film[0][2], "year": film[0][3], "language": film[0][4], "rate": film[0][5],}
        with open(image_path, 'rb') as img_file:
            self.bot.send_photo(
                chat_id,
                img_file,
                caption=f'''<b>🎬 Film Information</b>
        🌟 <b>Name:</b> {film_dict["name"]}
        🎭 <b>Genre:</b> {film_dict["genre"]}
        📝 <b>Description:</b> {film_dict["descrip"]}
        📅 <b>Release Year:</b> {film_dict["year"]}
        🌐 <b>Language:</b> {film_dict["language"]}
        ⭐ <b>Rate:</b> {film_dict["rate"]}''',
                reply_markup=keyboard,
                parse_mode='HTML'
            )




    def search_by_keyword(self, chat_id, keyword):
        if keyword.isdigit():
            print('Invalid input')
            return
        keyword = f'%{keyword}%'
        func = self.db.search_by_keyword.__name__
        result = self.db.search_by_keyword(keyword)
        self.tracker.tracker('Keyword', keyword)
        self.display(chat_id, results=result, pattern=keyword, func=func)


    def search_by_category_year(self, chat_id, category=None, year=None):
        if year and category:
            result= self.db.search_by_category_year(year, category)
            func = self.db.search_by_category.__name__
            self.display(chat_id, results=result, func=func, pattern=category)
            self.tracker.tracker('Category and Year', category + ', ' + str(year))
            return

        if category:
            result = self.db.search_by_category(category)
            func = self.db.search_by_category.__name__
            self.display(chat_id, results=result, pattern=category, func=func)
            return

        if year:
            categories = self.db.show_categories()
            keyboard = InlineKeyboardMarkup()
            for index, category in enumerate(categories):
                keyboard.add(InlineKeyboardButton(text=f'{category[1]}', callback_data=f'category_{index}'))
            self.bot.send_message(chat_id, "Select category:", reply_markup=keyboard)
            return


    def search_only_by_ctg(self, chat_id):
        categories = self.db.show_categories()
        keyboard = InlineKeyboardMarkup()
        for index, category in enumerate(categories):
            keyboard.add(InlineKeyboardButton(text=f'{category[1]}', callback_data=f'onlyctg_{index}'))
        self.bot.send_message(chat_id, "Select a category:", reply_markup=keyboard)


    def search_by_year(self, chat_id, year, join_category=None):
            if join_category == 'y':
                self.search_by_category_year(chat_id, year=year)
            elif join_category == 'n':
                result= self.db.search_by_year(year)
                func = self.db.search_by_year.__name__
                self.tracker.tracker('Year', f'{year}')
                self.display(chat_id, results=result, pattern=year, func=func)
            else:
                print('Invalid input')


    def out_common(self, chat_id, result):
        keyboard = InlineKeyboardMarkup()
        if result:
                for index, row in enumerate(result):
                    keyboard.add(InlineKeyboardButton(text=f'Search by {row[0]}, Times: {row[1]}', callback_data=f'mcommon_{row[0]}'))
                keyboard.add(InlineKeyboardButton(text=f'Return', callback_data=f'return'))
                self.bot.send_message(chat_id, "Most common: ", reply_markup=keyboard)



    def most_common_queries(self,chat_id):
        result = self.tracker.show_most_common()
        self.out_common(chat_id, result)


    def close(self):
        self.db.connection.close()
















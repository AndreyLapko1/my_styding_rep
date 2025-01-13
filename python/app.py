import mysql.connector
import os
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import re




class QueryDatabase:
    def __init__(self):
        load_dotenv()
        self.connection = mysql.connector.connect(
            host=os.getenv("host_write"),
            user=os.getenv("user_write"),
            password=os.getenv("password_write"),
            database=os.getenv("db_write"),
        )
        self.cursor = self.connection.cursor()


    def tracker(self, filter_, pattern):
        try:
            self.cursor.execute(f'insert into requests (search_by, title) values (%s, %s)', (filter_, pattern))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)


    def show_most_common(self):
        query = '''
                        SELECT title, COUNT(*) AS counter FROM `290724-ptm_fd_Andrey_Lapko`.requests
                        GROUP BY title
                        ORDER BY counter DESC
                        LIMIT 5'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()



#sakila
class Database:
    def __init__(self):
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("host"),
                user=os.getenv("user"),
                password=os.getenv("password"),
                database=os.getenv("database"),
            )
            self.cursor = self.connection.cursor()
            print("Connection established")
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)

    def show_categories(self):
        query = 'select * from category'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword, limit=10, offset=0):
        try:
            base_query = f'''
                            SELECT distinct f.title
                            FROM sakila.film f
                            join film_actor a
                            on f.film_id = a.film_id
                            join actor act
                            on a.actor_id = act.actor_id
                            where lower(act.first_name) LIKE %s
                            or lower(act.last_name) like %s
                            or lower(f.title) like %s
                            LIMIT {limit} OFFSET {offset}
                '''
            self.cursor.execute(base_query, (keyword, keyword, keyword))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)


    def search_by_category_year(self, year, category):
        base_query = '''
                         SELECT f.title, cat.name FROM sakila.film_category fcat
                         inner join category cat
                         on fcat.category_id = cat.category_id
                         inner join film f
                         on f.film_id = fcat.film_id
                         where f.release_year = %s and cat.name = %s

                                            '''
        self.cursor.execute(base_query, (year, category))
        return self.cursor.fetchall()

    def search_by_category(self, genre_name, limit=10, offset=0):
        try:
            base_query = f'''  
                                            select f.title FROM sakila.film_category fc
                                                    inner join category c
                                                    on c.category_id = fc.category_id
                                                    inner join film f
                                                    on f.film_id = fc.film_id
                                                    where c.name = %s
                                                    LIMIT {limit} OFFSET {offset}
                                                '''
            self.cursor.execute(base_query, (genre_name,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)



    def search_by_year(self, year, limit=10, offset=0):
        try:
            base_query = f'''
            SELECT title FROM sakila.film
            where release_year = %s
            LIMIT {limit} OFFSET {offset}
                                            '''
            self.cursor.execute(base_query, (year,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)


    def search_info(self, film_name):
        try:
            base_query = '''
            SELECT f.title, c.name, description, release_year, lng.name, rental_rate FROM sakila.film f
            inner join film_category fc
            on f.film_id = fc.film_id
            inner join category c
            on fc.category_id = c.category_id
            inner join language lng
            on f.language_id = lng.language_id
            where f.title = %s
            '''
            self.cursor.execute(base_query, (film_name,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)



    def close(self):
        self.connection.close()

class App:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.tracker = QueryDatabase()
        self.query = None



    def display(self, chat_id, results=None, pattern=None,  offset=0, more=False, func=None):
        # if query:
        #     if re.findall(pattern_regex, query, flags=re.DOTALL):
        #         print(self.query)
        #         match = re.findall(pattern_regex, query, re.DOTALL)
        #         cleaned_query = match[0]
        #         self.query = cleaned_query
        #     else:
        #         self.query = query


        if more:
            method = getattr(self.db, func)
            new_results = method(pattern, offset=offset)

            if new_results:
                self.display(chat_id, results=new_results, pattern=pattern, func=method.__name__, offset=offset)
                return
            else:
                self.bot.send_message(chat_id, "No more results.")
                return

        if isinstance(results, list) or isinstance(results, tuple):
            print(results[:10])
            keyboard = InlineKeyboardMarkup()
            for row in results[:10]:
                print(row[0])
                keyboard.add(InlineKeyboardButton(text=f'{row[0].capitalize()}', callback_data=f'film_{row[0]}'))


            if len(results) < 10 or len(results) == 0:
                keyboard.add(InlineKeyboardButton(text=f'Return', callback_data=f'return'))
                if len(results) == 0:
                    self.bot.send_message(chat_id, "Нет таких фильмов :(", reply_markup=keyboard)
                    return


            self.bot.send_message(chat_id, "Selected films:", reply_markup=keyboard)

            if len(results) >= 10:
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
        self.bot.send_message(chat_id, f'''---------------------\nName: {film[0][0]}\n\nGenre: {film[0][1]}\n\nDescription: \n{film[0][2]}\n
Release year: {film[0][3]}\n\nLanguage: {film[0][4]}\nRate: {film[0][5]}\n---------------------''', reply_markup=keyboard)




    def search_by_keyword(self, chat_id, keyword):
        if keyword.isdigit():
            print('Invalid input')
            return
        keyword = f'%{keyword}%'
        func = self.db.search_by_keyword.__name__
        result = self.db.search_by_keyword(keyword)
        self.tracker.tracker('Keyword', keyword)
        self.display(chat_id, results=result, pattern=keyword, func=func)


    def search_category(self, chat_id, category=None, year=None):
        if year and category:

            result= self.db.search_by_category_year(year, category)
            func = self.db.search_by_category.__name__
            self.display(chat_id, results=result, func=func, pattern=category)
            self.tracker.tracker('Category and Year', category + ', ' + str(year))
            return

        if category:
            result= self.db.search_by_category(category)
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

        else:
            categories = self.db.show_categories()
            keyboard = InlineKeyboardMarkup()
            for index, category in enumerate(categories):
                keyboard.add(InlineKeyboardButton(text=f'{category[1]}', callback_data=f'onlyctg_{index}'))
            self.bot.send_message(chat_id, "Select a category:", reply_markup=keyboard)

    def search_year(self, chat_id, year, join=False, join_category=None):
        if join:
            return year
        else:
            if join_category == 'y':
                self.search_category(chat_id, year=year)
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
















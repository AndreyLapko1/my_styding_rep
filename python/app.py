import mysql.connector
import os
from dotenv import load_dotenv
import telebot
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


    def tracker(self, filter, pattern):
        try:
            self.cursor.execute(f'insert into requests (search_by, title) values (%s, %s)', (filter, pattern))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)


    def show_history(self):
        query = 'select * from requests'
        self.cursor.execute(query)
        return  self.cursor.fetchall()

    def show_most_common(self):
        query = '''
                        SELECT title, COUNT(*) AS counter FROM `290724-ptm_fd_Andrey_Lapko`.requests
                        GROUP BY title
                        ORDER BY counter DESC
                        LIMIT 3'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()




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

    def search_by_actor(self, actor_name):
        try:
            base_query = '''
                            select flm.title from film_actor fct
                                                inner join film flm
                                                on flm.film_id = fct.film_id
                                                inner join actor act
                                                on act.actor_id = fct.actor_id
                                                where act.first_name = %s
                '''
            self.cursor.execute(base_query, (actor_name,))
            return self.cursor.fetchall(), base_query
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
        return self.cursor.fetchall(), base_query

    def search_by_category(self, genre_name):
        try:
            base_query = '''  
                                            select f.title FROM sakila.film_category fc
                                                    inner join category c
                                                    on c.category_id = fc.category_id
                                                    inner join film f
                                                    on f.film_id = fc.film_id
                                                    where c.name = %s
                                                '''
            self.cursor.execute(base_query, (genre_name,))
            return self.cursor.fetchall(), base_query
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)

    def search_by_year(self, year):
        try:
            base_query = '''
                                                            SELECT title FROM sakila.film
                                                            where release_year = %s
                                            '''
            self.cursor.execute(base_query, (year,))
            return self.cursor.fetchall(), base_query
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



    def display(self, chat_id, results=None, pattern=None, query=None, offset=10, limit=10, more=False):
        pattern_regex = r"^\s*SELECT.*%s\s*$"
        if query:
            if re.findall(pattern_regex, query, flags=re.DOTALL):
                match = re.findall(pattern_regex, query, re.DOTALL)
                cleaned_query = match[0]
                self.query = cleaned_query
                print(cleaned_query, 'это из очистки')
            else:
                self.query = query
                print(self.query, 'это из else')

        if more:
            offset_query = f'{self.query} LIMIT {limit} OFFSET {offset}'
            print(offset_query)
            self.db.cursor.execute(offset_query, (pattern,))
            new_results = self.db.cursor.fetchall()

            if new_results:

                self.display(chat_id, results=new_results, pattern=pattern, query=self.query, offset=offset + 10,limit=limit)
                print(new_results)
                return
            else:
                self.bot.send_message(chat_id, "No more results.")
                return



        if isinstance(results, list):

            keyboard = InlineKeyboardMarkup(row_width=2)
            for row in results[:10]:
                keyboard.add(InlineKeyboardButton(text=f'{row[0].capitalize()}', callback_data=f'film_{row[0]}'))


            self.bot.send_message(chat_id, "Selected films:", reply_markup=keyboard)

            if len(results) >= 10:
                show_more_keyboard = InlineKeyboardMarkup(row_width=2)
                show_more_keyboard.add(InlineKeyboardButton(text="Yes", callback_data=f"show_{pattern}"))
                show_more_keyboard.add(InlineKeyboardButton(text="No", callback_data="dontshow"))
                self.bot.send_message(chat_id, "Show more? :", reply_markup=show_more_keyboard)
                return
        else:
            print("Results is not a list:", results)
            self.bot.send_message(chat_id, "Error: Results are not in the correct format.")


    def search_actor(self):
        actor = input('Select actor: ')
        if actor.isdigit():
            print('Invalid input')
            return
        result, query = self.db.search_by_actor(actor)
        self.tracker.tracker('Actor', actor)
        self.display(results=result, query=query, pattern=actor)


    def search_category(self, chat_id, category=None, year=None):
        if year and category:
            kboard = InlineKeyboardMarkup(row_width=2)
            result, query = self.db.search_by_category_year(year,category)
            if result:
                for row in result:
                    kboard.add(InlineKeyboardButton(text=f'{row[0].capitalize()}', callback_data=f'film_{row[0]}'))
                self.bot.send_message(chat_id, "Select a category:", reply_markup=kboard)
            else:
                self.bot.send_message(chat_id, "No results found")
        else:
            categories = self.db.show_categories()
            keyboard = InlineKeyboardMarkup(row_width=2)
            for index, category in enumerate(categories):
                keyboard.add(InlineKeyboardButton(text=f'{category[1]}', callback_data=f'category_{index}'))
            self.bot.send_message(chat_id, "Select a category:", reply_markup=keyboard)

        # else:
        #     join_year = input('Do you want to join year? (y/n): ')
        #     if join_year == 'y':
        #         year = self.search_year(join=True)
        #         result = self.db.search_by_category_year(year, categories[select_category - 1][1])
        #         self.tracker.tracker('Category and Year', f'{categories[select_category - 1][1]}, {year}')
        #         self.display(*result)
        #     elif join_year == 'n':
        #             result, query = self.db.search_by_category(categories[select_category - 1][1])
        #             self.tracker.tracker('Category', f'{categories[select_category - 1][1]}')
        #             self.display(result, query=query, pattern=categories[select_category - 1][1])
        #     else:
        #         print('Invalid input')


    def search_year(self, chat_id, year, join=False, join_category=None):
        if join:
            return year
        else:
            if join_category == 'y':
                category = self.search_category(chat_id)
                result, query = self.db.search_by_category_year(year, category)
                self.tracker.tracker('Category and Year', f'{category}, {year}')
                # self.display(chat_id,*result)
            elif join_category == 'n':
                result, query = self.db.search_by_year(year)
                self.tracker.tracker('Year', f'{year}')
                self.display(chat_id, results=result, query=query, pattern=year)
            else:
                print('Invalid input')

    def most_common_queries(self):
        result = self.tracker.show_most_common()
        if result:
            for index, row in enumerate(result):
                print(f'{index + 1}. Search by {row[0].capitalize()}: {row[1]} times')

    def show_history(self):
        result = self.tracker.show_history()
        if result:
            for index, row in enumerate(result):
                print(f'\t{index + 1}. Search by {row[1]}: {row[2].capitalize()}')
    def close(self):
        self.db.connection.close()


    def main(self):
        print('Welcome!')
        while True:
            print('''
\t1. search actor       - Search for movies by actor
\t2. search year        - Search for movies by year
\t3. search category    - Search for movies by category
\t4. popular queries    - Show the most popular search queries
\t5. show history       - Show search history
\t6. quit               - Exit the application

                            ''')
            choise = int(input('Select command: '))
            if choise == 1:
                self.search_actor()
            elif choise == 2:
                self.search_year()
            elif choise == 3:
                self.search_category()
            elif choise == 4:
                self.most_common_queries()
            elif choise == 5:
                self.show_history()
            elif choise == 6:
                self.db.close()
                self.tracker.close()
                break
            else:
                print('Invalid input')


# if __name__ == '__main__':
#     app = App()
#     try:
#         app.main()
#     finally:
#         app.close()















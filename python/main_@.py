import mysql.connector
import os
from dotenv import load_dotenv


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
            self.connection.close()
        except mysql.connector.Error as err:
            print(f'Something went wrong ', err)


    def show_history(self):
        query = 'select * from requests'
        self.cursor.execute(query)
        return  self.cursor.fetchall()

    def show_most_common(self):
        query = '''
                        SELECT search_by, title, COUNT(*) AS counter FROM `290724-ptm_fd_Andrey_Lapko`.requests
                        GROUP BY title
                        ORDER BY counter DESC
                        LIMIT 3'''
        self.cursor.execute(query)
        return self.cursor.fetchall()




class Database:
    def __init__(self):
        load_dotenv()
        self.connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database"),
        )
        self.cursor = self.connection.cursor()

    def show_categories(self):
        query = 'select * from category'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_by_actor(self, actor_name):
        base_query = '''
                        select flm.title from film_actor fct
                                            inner join film flm
                                            on flm.film_id = fct.film_id
                                            inner join actor act
                                            on act.actor_id = fct.actor_id
                                            where act.first_name = %s
            '''
        self.cursor.execute(base_query, (actor_name,))
        return self.cursor.fetchall()

    def search_by_category(self, genre_name):
        base_query = '''  
                                        select f.title FROM sakila.film_category fc
                                                inner join category c
                                                on c.category_id = fc.category_id
                                                inner join film f
                                                on f.film_id = fc.film_id
                                                where c.name = %s
                                            '''
        self.cursor.execute(base_query, (genre_name,))
        return self.cursor.fetchall()

    def serach_by_year(self, year):
        base_query = '''
                                                        SELECT title FROM sakila.film
                                                        where release_year = %s
                                        '''
        self.cursor.execute(base_query, (year,))
        return self.cursor.fetchall()


    def close(self):
        self.connection.close()




class App:
    def __init__(self):
        self.db = Database()
        self.tracker = QueryDatabase()

    def display(self, results):
        if not results:
            print('No results')
        else:
            for result in results:
                print(result)

    def search_actor(self):
        actor = input('Select actor: ')
        result = self.db.search_by_actor(actor)
        self.tracker.tracker('Actor', actor)
        self.display(result)

    def search_category(self):
        categories = self.db.show_categories()
        print('Genres: \n')
        for index, category in enumerate(categories):
            print(f'{index}. {category[1]}', end=' \t')
        select_category = int(input('Select genre: ')) - 1
        result = self.db.search_by_category(select_category)
        self.display(result)


    def search_year(self):
        year = input('Select year: ')
        result = self.db.serach_by_year(year)
        self.display(result)

    def most_common_queries(self):
        result = self.tracker.show_most_common()
        if result:
            for row in result:
                print(row)


    def show_history(self):
        result = self.tracker.show_history()
        if result:
            for row in result:
                print(row)

    def close(self):
        self.db.connection.close()



    def main(self):
        print('Welcome!')
        choise = input('Input \'help\' to see available commands').strip().lower()
        while True:
            if choise == 'help':
                print('Available commands: \n')
                print('''
                    search keyword     - Search for movies by a keyword
                    search year        - Search for movies by genre and year
                    search actor       - Search for movies by actor
                    popular queries    - Show the most popular search queries
                    show history       - Show search history
                    quit               - Exit the application
                
                ''')
            elif choise == "search year":
                self.search_year()
            elif choise == "search actor":
                self.search_actor()
            elif choise == "search category":
                self.search_category()
            elif choise == "popular queries":
                self.most_common_queries()
            elif choise == "show history":
                self.show_history()
            elif choise == "quit":
                self.show_history()


if __name__ == '__main__':
    app = App()
    def run():
        try:
            app.main()
        finally:
            app.close()















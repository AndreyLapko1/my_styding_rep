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
        return self.cursor.fetchall(), base_query

    def serach_by_year(self, year):
        base_query = '''
                                                        SELECT title FROM sakila.film
                                                        where release_year = %s
                                        '''
        self.cursor.execute(base_query, (year,))
        return self.cursor.fetchall(), base_query


    def close(self):
        self.connection.close()




class App:
    def __init__(self):
        self.db = Database()
        self.tracker = QueryDatabase()

    def display(self, results, pattern=None, query=None, i=0, offset=10, limit=10, count=1):
        offset_query = f'{query} LIMIT {limit} OFFSET {offset}'
        if not results:
            print('No results')
        else:
            for row in results:
                if i < 10:
                    print(f'\t{count}. {row[0].capitalize()}')
                    i += 1
                    count += 1
                    if i == 10:
                        while True:
                            more = input('Show more? (y/n): ')
                            if more == 'y':
                                self.db.cursor.execute(offset_query, (pattern,))
                                self.display(self.db.cursor.fetchall(), pattern=pattern, query=query, limit=limit, count=count+10, offset=offset + 10)
                                break
                            elif more == 'n':
                                break
                            else:
                                print('Invalid input')


    def search_actor(self):
        actor = input('Select actor: ')
        result, query = self.db.search_by_actor(actor)
        self.tracker.tracker('Actor', actor)
        self.display(result, query=query, pattern=actor)

    def search_category(self):
        categories = self.db.show_categories()
        print('Genres: \n')
        for index, category in enumerate(categories):
            print(f'{index + 1}. {category[1]}', end=' \t')
        select_category = int(input('\nSelect genre: '))
        result, query = self.db.search_by_category(categories[select_category - 1][1])
        self.display(result, query=query, pattern=categories[select_category - 1][1])


    def search_year(self):
        year = input('Select year: ')
        result, query = self.db.serach_by_year(year)
        self.display(result, query=query, pattern=year)

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
        while True:
            print('''
                                1. search actor       - Search for movies by actor
                                2. search year        - Search for movies by year
                                3. search category    - Search for movies by category
                                4. popular queries    - Show the most popular search queries
                                5. show history       - Show search history
                                6. quit               - Exit the application

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
                break
            else:
                print('Invalid input')


if __name__ == '__main__':
    app = App()
    try:
        app.main()
    finally:
        app.close()















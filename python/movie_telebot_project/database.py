import mysql.connector
import os
from dotenv import load_dotenv

class QueryDatabaseWrite:
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

class FilmDatabase:
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
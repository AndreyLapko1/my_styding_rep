import mysql.connector
import os
from dotenv import load_dotenv
from collections import Counter



# class History:
#     def __init__(self):
#         self.history = []
#
#     def append_to(self, id: int, filter: str, pattern: str):
#         self.history.append([id, filter, pattern])
#
#
#     def show_history(self):
#         if self.history:
#             for row in self.history:
#                 print(row)
#         else:
#             print('History is not exist')
#         print(self.history)


def most_common(self):
    if self.history:
        elements_id = [el[0] for el in self.history]
        counter = Counter(elements_id)
        most_common_element = counter.most_common(1)[0][0]
        for item in self.history:
            if item[0] == most_common_element:
                print(f'{item[1]}: {item[2].capitalize()}')
                break

# history = History()


load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=os.getenv("database"),
    )
    cursor = conn.cursor()
    print('Connected to database')

except mysql.connector.Error as err:
    print(f'Something went wrong ', err)





def show_categories():
    cursor.execute('select * from category')
    categories = cursor.fetchall()
    print('Generes: ')
    for index, category in enumerate(categories, start=1):
        print(f'{index}. {category[1]}', end=' \t')
    return categories


def output(cursor,pattern=None,query=None, i=0, offset=10, limit=10, count=1):
    offset_query = f'{query} LIMIT {limit} OFFSET {offset}'
    results = cursor.fetchall()
    if not results:
        print(f'\tNot found')
    else:
        for row in results:
            if i < 10:
                print(f'\t{count}. {row[0].capitalize()}')
                count += 1
                i += 1

        show_more = input('Show more? (y/n): ')
        if show_more == 'y':

            cursor.execute(offset_query, (pattern,))

            output(cursor,pattern=pattern, query=query,offset=offset+10, count=count)


def history_write(cursor, number_of, filter, pattern):
    cursor.execute(f'insert queries values ({number_of}, {filter}, {pattern})')





def find_by_actor(cursor, name_find=None, send_to_out=True):
    if name_find is None:
        name_find = input('Enter the actor\'s name: ').upper()


    base_query = '''
                select flm.title from film_actor fct
                                    inner join film flm
                                    on flm.film_id = fct.film_id
                                    inner join actor act
                                    on act.actor_id = fct.actor_id
                                    where act.first_name = %s
    '''
    cursor.execute(base_query, (name_find,))

    if send_to_out:
        output(cursor, pattern=name_find, query=base_query)
    else:
        return cursor, base_query




def find_by_genre(cursor, genre_find=None, send_to_out=True, year=None):
    categories = show_categories()
    base_query = '''  
                                select f.title FROM sakila.film_category fc
                                        inner join category c
                                        on c.category_id = fc.category_id
                                        inner join film f
                                        on f.film_id = fc.film_id
                                        where c.name = %s
                                    '''
    if genre_find is None:
        try:
            genre_find = int(input('\nEnter the genre number: '))
            if genre_find < 1 or genre_find > len(categories):
                raise ValueError('Expected number within acceptable values')
            join_year = input('Do you want to join year filter?: (y/n): ')
            if join_year == 'y':
                year = find_by_year(cursor, join=True)
                print(year)
                base_query = '''
                            SELECT f.title, cat.name FROM sakila.film_category fcat
                            inner join category cat
                            on fcat.category_id = cat.category_id
                            inner join film f
                            on f.film_id = fcat.film_id
                            where f.release_year = %s and cat.name = %s
                
                '''
                cursor.execute(base_query, (year, categories[genre_find - 1][1], ))
                output(cursor)


            else:
                cursor.execute(base_query, (categories[genre_find - 1][1],))
        except (TypeError, ValueError) as e:
            raise Exception(f'Fail. {e}')


    if send_to_out:
        output(cursor, pattern=categories[genre_find - 1][1], query=base_query)
    else:
        return cursor, base_query



def find_by_year(cursor,selected_year=None, send_to_out=True, join=False):
    if selected_year is None:
        selected_year = int(input('Enter the year of release: '))
        if join:
            return selected_year
    base_query = '''
                    SELECT title FROM sakila.film
                    where release_year = %s
    '''
    cursor.execute(base_query, (selected_year,))

    if send_to_out:
        output(cursor, pattern=selected_year, query=base_query)
    else:
        return cursor, base_query



def sampling_filter():
    sampling_options = ['Actor name', 'Genre', 'Year of release', 'Check history', 'Most common queries', "Exit"]
    for index, samp_opt in enumerate(sampling_options, start=1):
        print(f'{index}. {samp_opt}', end='\t')
    try:
        choise_select = int(input('\nSelect sampling option: '))
        if choise_select < 1 or choise_select > len(sampling_options):
            raise ValueError('Expected number within acceptable values')


        if choise_select == 1:
            find_by_actor(cursor)
            return True

        if choise_select == 2:
            find_by_genre(cursor)
            return True


        if choise_select == 3:
            find_by_year(cursor)
            return True


        if choise_select == 4:
            # show_history()
            return True

        if choise_select == 5:
            return True
            # most_common()

        if choise_select == 6:
            print('Bye')
            return False

    except (TypeError, ValueError) as e:
        print(f'Fail. {e}')



def main():
    running = True
    while running:
        running = sampling_filter()


if __name__ == "__main__":
    main()

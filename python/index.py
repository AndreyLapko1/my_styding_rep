
import time
import re

# class History:
#     def __init__(self):
#         self.history = []
#
#     def append(self, text):
#         self.history.append(text)
#






# def hello():
#     print('func work')
#
# def choise():
#     a = int(input("Введите число (введите 5 для выхода): "))
#     if a == 5:
#         return False
#     hello()
#     return True
#
#
#
# while choise:
#     choise()
#
# import mysql.connector
#
# conn = mysql.connector.connect(
#         host='ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#         user='ich1',
#         password='password',
#         database='sakila'
# )
# cursor = conn.cursor()


# from collections import Counter
#
# # Исходный список списков
# data = [
#     [1, 'search by actor', 'NICK'],
#     [1, 'search by actor', 'NICK'],
#     [3, 'search by year', '2003'],
#     [2, 'search by genre', 'Children']
# ]
#
# # Извлекаем первые элементы каждого внутреннего списка
# first_elements = [item[0] for item in data]
#
# # Подсчитываем количество вхождений каждого элемента
# counter = Counter(first_elements)
#
# # Находим наиболее частый элемент
# most_common_element, count = counter.most_common(1)[0]
#
# print(f'Наиболее частый первый элемент: {most_common_element}, встречается {count} раз(а).')


import re

# Строка с двумя запросами
query = """
SELECT title FROM sakila.film
where release_year = %s

SELECT title FROM sakila.film
where release_year = %s
"""

# Регулярное выражение для захвата первого запроса
pattern = r"SELECT.*?%s"

# Ищем первый запрос
match = re.search(pattern, query, re.DOTALL)

if match:
    # Извлекаем первый запрос
    extracted_query = match.group(0)
    print("Вырванный запрос:", extracted_query)
else:
    print("Запрос не найден")


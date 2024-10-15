import psycopg2
from prettytable import PrettyTable

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="cinema",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Функція для виконання SQL-запитів і виведення результатів
def execute_query(query, params=None):
    cursor.execute(query, params)
    return cursor.fetchall()

# Функція для виведення даних в табличному форматі
def print_table(headers, data):
    table = PrettyTable(headers)
    for row in data:
        table.add_row(row)
    print(table)

# 1. Відобразити всі комедії, відсортовані по рейтингу
print("\n1. Всі комедії, відсортовані по рейтингу:")
query = """
    SELECT title, genre, duration, rating
    FROM films
    WHERE genre = 'Комедія'
    ORDER BY rating DESC;
"""
data = execute_query(query)
print_table(["Назва", "Жанр", "Тривалість", "Рейтинг"], data)

# 2. Остання дата показу фільму для кожного транслювання
print("\n2. Остання дата показу фільму для кожного транслювання:")
query = """
    SELECT f.title, c.name, s.start_date, s.duration_days, 
           (s.start_date + s.duration_days * INTERVAL '1 day') AS end_date
    FROM screenings s
    JOIN films f ON s.film_id = f.film_id
    JOIN cinemas c ON s.cinema_id = c.cinema_id;
"""
data = execute_query(query)
print_table(["Фільм", "Кінотеатр", "Початок", "Тривалість", "Кінець"], data)

# 3. Максимальний прибуток для кожного кінотеатру
print("\n3. Максимальний прибуток для кожного кінотеатру:")
query = """
    SELECT c.name, MAX(c.ticket_price * c.seats) AS max_profit
    FROM cinemas c
    JOIN screenings s ON c.cinema_id = s.cinema_id
    GROUP BY c.name;
"""
data = execute_query(query)
print_table(["Кінотеатр", "Максимальний прибуток"], data)

# 4. Відобразити всі фільми заданого жанру (запит з параметром)
print("\n4. Всі фільми заданого жанру:")
genre = input("Введіть жанр (Мелодрама, Комедія, Бойовик): ")
query = """
    SELECT title, genre, duration, rating
    FROM films
    WHERE genre = %s;
"""
data = execute_query(query, (genre,))
print_table(["Назва", "Жанр", "Тривалість", "Рейтинг"], data)

# 5. Кількість фільмів кожного жанру
print("\n5. Кількість фільмів кожного жанру:")
query = """
    SELECT genre, COUNT(*) AS film_count
    FROM films
    GROUP BY genre;
"""
data = execute_query(query)
print_table(["Жанр", "Кількість"], data)

# 6. Кількість фільмів кожного жанру, які транслюються в кожному кінотеатрі
print("\n6. Кількість фільмів кожного жанру в кожному кінотеатрі:")
query = """
    SELECT c.name, f.genre, COUNT(*) AS film_count
    FROM screenings s
    JOIN films f ON s.film_id = f.film_id
    JOIN cinemas c ON s.cinema_id = c.cinema_id
    GROUP BY c.name, f.genre;
"""
data = execute_query(query)
print_table(["Кінотеатр", "Жанр", "Кількість"], data)

# Закриття з'єднання
cursor.close()
conn.close()

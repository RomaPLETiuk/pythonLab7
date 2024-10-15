import psycopg2
from psycopg2 import sql

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="cinema",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor()

# Створення таблиці "Фільми"
cursor.execute("""
CREATE TABLE IF NOT EXISTS films (
    film_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(50) CHECK (genre IN ('Мелодрама', 'Комедія', 'Бойовик')),
    duration INTEGER CHECK (duration > 0),
    rating NUMERIC(3, 1) CHECK (rating >= 0 AND rating <= 10)
);
""")

# Створення таблиці "Кінотеатри"
cursor.execute("""
CREATE TABLE IF NOT EXISTS cinemas (
    cinema_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ticket_price NUMERIC(5, 2),
    seats INTEGER CHECK (seats > 0),
    address VARCHAR(255),
    phone CHAR(10) CHECK (phone ~ '^\d{10}$')
);
""")

# Створення таблиці "Транслювання фільмів"
cursor.execute("""
CREATE TABLE IF NOT EXISTS screenings (
    screening_id SERIAL PRIMARY KEY,
    film_id INTEGER REFERENCES films(film_id) ON DELETE CASCADE,
    cinema_id INTEGER REFERENCES cinemas(cinema_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    duration_days INTEGER CHECK (duration_days > 0)
);
""")

# Наповнення таблиці "Фільми" даними
cursor.execute("""
INSERT INTO films (title, genre, duration, rating)
VALUES
    ('Фільм 1', 'Комедія', 120, 7.5),
    ('Фільм 2', 'Бойовик', 140, 8.2),
    ('Фільм 3', 'Мелодрама', 90, 6.8),
    ('Фільм 4', 'Комедія', 110, 7.0),
    ('Фільм 5', 'Бойовик', 150, 8.0),
    ('Фільм 6', 'Мелодрама', 100, 6.5),
    ('Фільм 7', 'Бойовик', 130, 7.8),
    ('Фільм 8', 'Комедія', 95, 7.1),
    ('Фільм 9', 'Мелодрама', 105, 6.9),
    ('Фільм 10', 'Бойовик', 160, 8.5),
    ('Фільм 11', 'Комедія', 85, 7.3);
""")

# Наповнення таблиці "Кінотеатри" даними
cursor.execute("""
INSERT INTO cinemas (name, ticket_price, seats, address, phone)
VALUES
    ('Кінотеатр 1', 150.00, 200, 'вул. Шевченка 12', '0931234567'),
    ('Кінотеатр 2', 120.00, 150, 'вул. Грушевського 23', '0937654321'),
    ('Кінотеатр 3', 180.00, 250, 'пр. Перемоги 45', '0931112223');
""")

# Наповнення таблиці "Транслювання фільмів" даними
cursor.execute("""
INSERT INTO screenings (film_id, cinema_id, start_date, duration_days)
VALUES
    (1, 1, '2024-10-01', 7),
    (2, 1, '2024-10-08', 5),
    (3, 2, '2024-10-02', 10),
    (4, 2, '2024-10-12', 7),
    (5, 3, '2024-10-05', 4),
    (6, 3, '2024-10-09', 6),
    (7, 1, '2024-10-13', 9),
    (8, 2, '2024-10-17', 3),
    (9, 3, '2024-10-19', 8),
    (10, 1, '2024-10-24', 6),
    (11, 2, '2024-10-30', 5);
""")

# Збереження змін та закриття з'єднання
conn.commit()
cursor.close()
conn.close()

print("Таблиці створені та дані успішно додані.")

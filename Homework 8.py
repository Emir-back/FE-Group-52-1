import sqlite3


def create_tables():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area REAL DEFAULT 0,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO countries (title) VALUES (?)", [
        ("Киргизия",),
        ("Германия",),
        ("Китай",)
    ])

    conn.commit()

    cursor.execute("SELECT id FROM countries WHERE title='Киргизия'")
    kyrgyzstan_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM countries WHERE title='Германия'")
    germany_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM countries WHERE title='Китай'")
    china_id = cursor.fetchone()[0]

    cursor.executemany("INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)", [
        ("Бишкек", 160, kyrgyzstan_id),
        ("Ош", 182, kyrgyzstan_id),
        ("Берлин", 891, germany_id),
        ("Мюнхен", 310, germany_id),
        ("Пекин", 16410, china_id),
        ("Шанхай", 6340, china_id),
        ("Гуанчжоу", 7434, china_id)
    ])

    conn.commit()

    cursor.execute("SELECT id FROM cities")
    city_ids = [row[0] for row in cursor.fetchall()]

    students = [
        ("Иван", "Иванов", city_ids[0]),
        ("Петр", "Петров", city_ids[1]),
        ("Анна", "Сидорова", city_ids[2]),
        ("Максим", "Смирнов", city_ids[3]),
        ("Елена", "Козлова", city_ids[4]),
        ("Дмитрий", "Соколов", city_ids[5]),
        ("Ольга", "Морозова", city_ids[6]),
        ("Алексей", "Федоров", city_ids[0]),
        ("Мария", "Волкова", city_ids[1]),
        ("Сергей", "Зайцев", city_ids[2]),
        ("Наталья", "Беляева", city_ids[3]),
        ("Тимур", "Григорьев", city_ids[4]),
        ("Карина", "Романова", city_ids[5]),
        ("Виктор", "Мельников", city_ids[6]),
        ("Артем", "Николаев", city_ids[0])
    ]
    cursor.executemany("INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)", students)

    conn.commit()
    conn.close()


def show_students_by_city():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM cities")
    cities = cursor.fetchall()

    print(
        "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    while True:
        city_id = input("Введите ID города: ")
        if city_id == "0":
            break

        cursor.execute('''
            SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area 
            FROM students 
            JOIN cities ON students.city_id = cities.id 
            JOIN countries ON cities.country_id = countries.id 
            WHERE students.city_id = ?
        ''', (city_id,))

        students = cursor.fetchall()
        if students:
            print("Ученики, проживающие в выбранном городе:")
            for student in students:
                print(f"{student[0]} {student[1]}, {student[2]}, {student[3]}, площадь: {student[4]} км²")
        else:
            print("В этом городе пока нет учеников.")

    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_data()
    show_students_by_city()

import sqlite3

conn = sqlite3.connect("hw.db")

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_title TEXT NOT NULL CHECK(length(product_title) <= 200),
        price REAL(10,2) NOT NULL DEFAULT 0.0,
        quantity INTEGER NOT NULL DEFAULT 0
    )
''')

def add_products():
    products = [
        ("Мыло детское", 50.0, 10),
        ("Жидкое мыло с запахом ванили", 75.0, 15),
        ("Шампунь", 150.0, 20),
        ("Зубная паста", 120.0, 30),
        ("Гель для душа", 200.0, 25),
        ("Крем для рук", 180.0, 18),
        ("Лосьон для тела", 250.0, 12),
        ("Детская присыпка", 80.0, 22),
        ("Пена для бритья", 175.0, 17),
        ("Крем после бритья", 190.0, 19),
        ("Шампунь от перхоти", 210.0, 14),
        ("Гель для укладки волос", 160.0, 16),
        ("Одеколон", 300.0, 10),
        ("Духи", 500.0, 5),
        ("Дезодорант", 220.0, 20)
    ]
    cursor.executemany("INSERT INTO products (product_title, price, quantity) VALUES (?, ?, ?)", products)
    conn.commit()

def update_quantity(product_id, new_quantity):
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
    conn.commit()

def update_price(product_id, new_price):
    cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
    conn.commit()

def delete_product(product_id):
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

def get_all_products():
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(row)

def get_filtered_products(price_limit, quantity_limit):
    cursor.execute("SELECT * FROM products WHERE price < ? AND quantity > ?", (price_limit, quantity_limit))
    for row in cursor.fetchall():
        print(row)

def search_products(keyword):
    cursor.execute("SELECT * FROM products WHERE product_title LIKE ?", ('%' + keyword + '%',))
    for row in cursor.fetchall():
        print(row)

add_products()
get_all_products()
update_quantity(1, 50)
update_price(2, 65.0)
delete_product(3)
get_filtered_products(100, 5)
search_products("мыло")

conn.close()

print("База данных hw.db создана, таблица products добавлена, функции протестированы.")

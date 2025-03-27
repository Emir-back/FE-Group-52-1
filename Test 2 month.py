import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS categories (
        code VARCHAR(2) PRIMARY KEY,
        title VARCHAR(150) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS stores (
        store_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(250) NOT NULL,
        category_code VARCHAR(2) NOT NULL,
        unit_price FLOAT NOT NULL DEFAULT 0,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        store_id INTEGER NOT NULL,
        FOREIGN KEY (category_code) REFERENCES categories(code),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    );
''')

cursor.executescript('''
    INSERT OR IGNORE INTO categories (code, title) VALUES 
        ('FD', 'Food products'), 
        ('EL', 'Electronics'), 
        ('CL', 'Clothes');

    INSERT OR IGNORE INTO stores (store_id, title) VALUES 
        (1, 'Asia'), 
        (2, 'Globus'), 
        (3, 'Spar');

    INSERT OR IGNORE INTO products (title, category_code, unit_price, stock_quantity, store_id) VALUES 
        ('Chocolate', 'FD', 10.5, 129, 1),
        ('Jeans', 'CL', 20.0, 15, 2),
        ('TV', 'EL', 300.0, 5, 3),
        ('Bread', 'FD', 2.0, 50, 1),
        ('Laptop', 'EL', 800.0, 7, 2);
''')

conn.commit()


def show_stores():
    cursor.execute("SELECT store_id, title FROM stores")
    stores = cursor.fetchall()
    print(
        "\nВы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже,"
        " для выхода из программы введите 0:")
    for store in stores:
        print(f"{store[0]}. {store[1]}")


def show_products(store_id):
    cursor.execute("""
        SELECT p.title, c.title, p.unit_price, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_code = c.code
        WHERE p.store_id = ?
    """, (store_id,))

    products = cursor.fetchall()

    if not products:
        print("В этом магазине нет продуктов.")
        return

    print("\n Список продуктов в магазине:")
    for product in products:
        print(
            f" Название: {product[0]}\n   Категория: {product[1]}\n   Цена: {product[2]}\n   Количество на складе: {product[3]}\n")

while True:
    show_stores()
    store_id = input("\nВведите ID магазина: ")

    if store_id == "0":
        print("Выход")
        break

    if store_id.isdigit():
        show_products(int(store_id))
    else:
        print(" Введите корректный ID магазина!")

conn.close()

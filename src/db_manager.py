from src.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        category TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        products = [
            ("Товар 1", 100.0, "10 users included, 2 GB of storage, Email support, Help center access", "Электроника"),
            ("Товар 2", 100.0, "10 users included, 2 GB of storage, Email support, Help center access", "Электроника"),
            ("Товар 3", 150.0, "15 users included, 5 GB of storage, Priority support, Help center access",
             "Электроника"),
        ]
        cur.executemany("INSERT INTO products (name, price, description, category) VALUES (?, ?, ?, ?)", products)

    conn.commit()
    conn.close()


def save_contact(name: str, email: str, message: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()


def get_products(category=None):
    conn = get_connection()
    cur = conn.cursor()

    if category:
        cur.execute("SELECT * FROM products WHERE category = ?", (category,))
    else:
        cur.execute("SELECT * FROM products")

    products = cur.fetchall()
    conn.close()
    return products


def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM products")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories

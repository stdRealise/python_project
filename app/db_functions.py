import sqlite3


def conn_db():
    conn = sqlite3.connect('dbase.db')
    return conn


def create_db():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            price MONEY NOT NULL,
            time INTEGER NOT NULL,
            gamers1 INTEGER NOT NULL,
            gamers2 INTEGER NOT NULL,
            age INTEGER NOT NULL,
            ref VARCHAR(255) NOT NULL,
            UNIQUE(name)
        );
    ''')
    cursor.close()
    conn.close()


def add_item(conn, cursor, name, price, time, gamers1, gamers2, age, ref):
    cursor.execute('''
        INSERT INTO items (name, price, time, gamers1, gamers2, age, ref)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (name) DO UPDATE
        SET price = EXCLUDED.price,
            time = EXCLUDED.time,
            gamers1 = EXCLUDED.gamers1,
            gamers2 = EXCLUDED.gamers2,
            age = EXCLUDED.age,
            ref = EXCLUDED.ref;
        ''', (name, price, time, gamers1, gamers2, age, ref))


def select_db():
    return 'SELECT name, price, time, gamers1, gamers2, age, ref FROM items'


def sort_db():
    return f'''SELECT name, price, time, gamers1, gamers2, age, ref FROM items
               ORDER BY price'''


def select_between_db(col, x, y):
    return f'''SELECT name, price, time, gamers1, gamers2, age, ref FROM items
               WHERE {col} >= {x} AND {col} <= {y}'''


def select_age(col, x):
    return f'''SELECT name, price, time, gamers1, gamers2, age, ref FROM items
               WHERE age <= {x}'''


def select_name(x):
    return f'''SELECT name, price, time, gamers1, gamers2, age, ref FROM items
               WHERE name LIKE "%{x}%"'''


def execute_db(query):
    conn = conn_db()
    cursor = conn.cursor()
    res = list(cursor.execute(query))
    cursor.close()
    conn.close()
    return res


def res_db(data):
    query = ''
    if (data['price1'] and data['price2']) and (data['price1'].isnumeric() and \
        data['price2'].isnumeric()) and int(data['price1']) <= int(
        data['price2']
    ):
        query += (
            select_between_db('price', data['price1'], data['price2'])
            + ' INTERSECT '
        )
    if data['time1'] and data['time2'] and (data['time1'].isnumeric() and \
        data['time2'].isnumeric()) and int(data['time1']) <= int(
        data['time2']
    ):
        query += (
            select_between_db('time', data['time1'], data['time2'])
            + ' INTERSECT '
        )
    if data['gamers1'] and data['gamers2'] and (data['gamers1'].isnumeric() and \
        data['gamers2'].isnumeric()) and int(data['gamers1']) <= int(
        data['gamers2']
    ):
        query += (
            select_between_db('gamers2', data['gamers1'], data['gamers2'])
            + ' INTERSECT '
        )
    if data['age'] and data['age'].isnumeric():
        query += (
            select_age('age', data['age'])
            + ' UNION '
            + select_age('age', data['age'])
            + ' INTERSECT '
        )
    if data['name']:
        query += select_name(data['name']) + ' INTERSECT '
    query += sort_db()
    return execute_db(query)[:20]


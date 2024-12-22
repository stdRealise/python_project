import psycopg2


def conn_db():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='123', host='postgres', port='5432')
    return conn
    
    
def create_db():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postgres (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price MONEY NOT NULL
        );
    ''')
    cursor.close()
    conn.close()

    
def add_item(conn, cursor, name, price):
    cursor.execute('''
        INSERT INTO postgres (name, price) VALUES (%s, %s)
        ON CONFLICT (name) DO UPDATE 
        SET price = EXCLUDED.price;
        ''', (name, price))
            
            
def select_db():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM items;')
    res = list(cursor)
    cursor.close()
    conn.close()
    return res
          
            
def sort_db(col):
    cursor.execute(f'''
        SELECT * FROM items ORDER BY {col};''')


def select_between_db(x, y):
    cursor.execute(f'''select_price(x, y):
    SELECT * FROM items WHERE price BETWEEN x AND y;''')


def select_gamers(x, y):
    cursor.execute(f'''SELECT * FROM items WHERE price BETWEEN x AND y;''')


def select_name(x, y):
    cursor.execute(f'''FROM items WHERE name LIKE 'A%';''')

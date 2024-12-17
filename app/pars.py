import requests
from bs4 import BeautifulSoup
import lxml
import psycopg2


def create_table(conn, cursor):
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            price INTEGER
        )
    ''')
def conn_db():
    conn = psycopg2.connect(dbname='projectdb', user='user', password='123', host='postgres', port='5432')
    return conn
    
def add_item(conn, cursor, name, price):
    cursor.execute(f'''
        INSERT INTO items (name, price) VALUES
            ({name}, {price})''')
            

if __name__ == '__main__':
    #'https://ipc.susu.ru/4318.html'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0'}
    conn = conn_db()
    cursor = conn.cursor()
    create_table(conn, cursor)
    
    for page in range(1, 2):
        url = f'https://playland-group.ru/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3/page/{page}/'

        response = requests.get(url, headers=headers)
        #print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='item-content') #vertical-item overflow-hidden text-center')

        for card in items:
            name = card.find('h2', class_='woocommerce-loop-product__title').string
            ref = card.find('a', class_='woocommerce-loop-product__link').get('href')
            #response2 = requests.get(ref, headers=headers)
            print(name)
            add_item(conn, cursor, name, price)

    print(cursor.fetchall())
    cursor.close()
    conn.close()


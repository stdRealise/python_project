import requests
from bs4 import BeautifulSoup
from db_functions import conn_db, add_item


def get_digits(s):
    res = []
    i = 0
    while i < len(s):
        el = ''
        while i < len(s) and '0' <= s[i] <= '9':
            el += s[i]
            i += 1
        if el != '':
            res.append(int(el))
            el = ''
        i += 1
    return res


def scrap():
    conn = conn_db()
    cursor = conn.cursor()
    for page in range(1, 12):
        url = f'https://playland-group.ru/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3/page/{page}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='item-content')
        for card in items:
            name_ref = card.find('a', class_='woocommerce-loop-product__link')
            name = name_ref.text
            ref = name_ref.get('href')
            price = card.find(
                'span', class_='woocommerce-Price-amount amount'
            ).text.replace(',', '')[1:]
            lst = card.find_all('p')
            time = get_digits(lst[0].text)[0]
            gamers = get_digits(lst[1].text)
            gamers1 = gamers[0]
            if len(gamers) == 2:
                gamers2 = gamers[1]
            else:
                gamers2 = 20
            age = get_digits(lst[2].text)[0]
            add_item(
                conn, cursor, name, price, time, gamers1, gamers2, age, ref
            )
            conn.commit()
    cursor.close()
    conn.close()


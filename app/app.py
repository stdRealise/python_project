from flask import Flask, render_template, request, session, redirect, url_for
from db_functions import (
    create_db,
    select_db,
    execute_db,
    res_db,
    add_item
)
from scrap import scrap


app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def games():
    db_items = execute_db(select_db())
    return render_template(
        'index.html', count=len(db_items), query='Введите запрос', items=db_items
    )


@app.route('/show', methods=['GET', 'POST'])
def show():
    data = request.form
    db_items = res_db(data)
    count = len(db_items)
    curr_query = f'''Название: {data['name']};
                     цена: {data['price1']}-{data['price2']};
                     продолжительность: {data['time1']}-{data['time2']};
                     количество игроков: {data['gamers1']}-{data['gamers2']};
                     возраст: {data['age']}'''
    return render_template(
        'index.html', count=count, query=curr_query, items=db_items
    )


if __name__ == '__main__':
    create_db()
    scrap()
    app.run(host="0.0.0.0", port=5000)


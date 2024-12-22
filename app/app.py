from flask import Flask, render_template, request
from db_f import create_db, select_db, select_between_db, sort_db, select_age, select_name, execute_db
from scrap import scrap


app = Flask(__name__)


@app.route('/games')
def games():
    db_items = execute_db(select_db())[:20]
    return render_template('index.html', count=20, query='Введите запрос', items=db_items)


@app.route('/show', methods=['GET', 'POST'])
def show():
    data = request.form
    query = ''
    if data['price1'] and data['price2'] and int(data['price1']) <= int(data['price2']):
        query = query + select_between_db('price', data['price1'], data['price2']) + ' INTERSECT '
    if data['time1'] and data['time2'] and int(data['time1']) <= int(data['time2']):
        query = query + select_between_db('time', data['time1'], data['time2']) + ' INTERSECT '
    if data['gamers1'] and data['gamers2'] and int(data['gamers1']) <= int(data['gamers2']):
        query = query + select_between_db('gamers2', data['gamers1'], data['gamers2']) + ' INTERSECT '
    if data['age']:
        query = query + select_age('age', data['age']) + ' UNION ' + select_age('age', data['age']) + ' INTERSECT '
    if data['name']:
        query = query + select_name(data['name']) + ' INTERSECT '
    query += sort_db()
    db_items = execute_db(query)[:20]
    count = len(db_items)
    curr_query = f'''Название: {data['name']};
                     цена: {data['price1']}-{data['price2']};
                     продолжительность: {data['time1']}-{data['time2']};
                     количество игроков: {data['gamers1']}-{data['gamers2']};
                     возраст: {data['age']}'''
    return render_template('index.html', count=count, query=curr_query, items=db_items) 


if __name__ == '__main__':
    create_db()
    scrap()
    app.run(host="0.0.0.0", port=5000)


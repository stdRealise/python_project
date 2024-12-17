from flask import Flask, render_template, redirect
from pars import *

app = Flask(__name__)

@app.route('/')
def hello():
    
    return '<h1>Hello!</h1>'
    
@app.route('/t')
def page():
    try:
        conn = conn_db()
    except:
        print("Cannot connect to DB, check connection.")
        return '<h1>Helloff!</h1>'
    #conn = conn_db()
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    return '<h1>ok!</h1>'
    create_table(conn, cursor)
    pars()
    db_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',  items=db_items)
    
if __name__ == '__main__':
    
    app.run(port=8080,host='127.0.0.1',debug=True)
    

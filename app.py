from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Zaq12wsxcde345@localhost:5432/amur.db'
db = SQLAlchemy(app)


class House(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    address = db.Column(db.String(255), nullable = False)
    text = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return '<Article %r>' % self.id 


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/main')
def main():
    return 'Welcome to the Main page'


db_config = {
    'dbname': 'amur',
    'user': 'postgres',
    'password': 'Zaq12wsxcde345',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

@app.route('/main/items/', methods = ['GET'])
def get_data():
    houses = request.args.get('houses', 'houses')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        #sql запрос для получения данных из таблицы
        query = f'SELECT * FROM {houses}' #уязвимость для sql иньекций
        cur.execute(query)

        #извлекаем данные и преобразуем в словарь
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        cur.close()
        conn.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run()
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

db_user = os.getenv("MYSQLUSER")
db_password = os.getenv("MYSQLPASSWORD")
db_host = os.getenv("MYSQLHOST")
db_port = os.getenv("MYSQLPORT", 3306)
db_name = os.getenv("MYSQLDATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Item, User, UserData

@app.route('/')
def index():
    return "Flask + Railway + MySQL is working!"

################
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = Item(name=data['name'], value=data.get('value', 0))
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name, 'value': item.value})

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': i.id, 'name': i.name, 'value': i.value} for i in items])
################


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    # Создаём User
    user = User(id_email=data['id_email'])

    # Создаём связанные UserData
    user_data = UserData(
        user_email=data['id_email'],  # связка по ключу
        purpose=data.get('purpose'),
        gender=data.get('gender'),
        level=data.get('level'),
        frequency=data.get('frequency'),
        trauma=data.get('trauma'),
        muscles=data.get('muscles'),
        age=data.get('age')
    )

    # Устанавливаем связь (можно и user.user_data = user_data)
    user.user_data = user_data 
    # Сохраняем в БД
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id_email': user.id_email,
        'user_data': {
            'purpose': user_data.purpose
        }
    }), 201











if __name__ == '__main__':
    app.run(debug=True)

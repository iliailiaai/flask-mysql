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

from models import Item

@app.route('/')
def index():
    return "Flask + Railway + MySQL is working!"

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

if __name__ == '__main__':
    app.run(debug=True)

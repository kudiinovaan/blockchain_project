# Программа на Python для создания блокчейна
# Для временной метки
import datetime
# Вычисление хэша для добавления цифровой подписи к блокам
import hashlib
# Для хранения данных в блокчейне
import json
# Flask предназначен для создания веб-приложения, а jsonify - для
# отображения блокчейнаn
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from salon_clients_dump.sql import db, Client
class Blockchain:
# Эта функция ниже создана для создания самого первого блока и установки его хэша равным "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
# Эта функция ниже создана для добавления дополнительных блоков в цепочку
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 'client_hash': self.hash_data(client_data)}
        self.chain.append(block)
        return block
    
# Эта функция ниже создана для отображения предыдущего блока
    def print_previous_block(self):
        return self.chain[-1]
# Это функция для проверки работы и используется для успешного майнинга блока
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def hash_data(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True
# Создание веб-приложения с использованием flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/salon-clients'
db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

if __name__ == '__main__':
    app.run(debug=True)

 # Создание всех таблиц, определенных в модели
    db.create_all()

    # Заполнение таблицы данными
    clients_data = [
        {'first_name': 'Анна', 'last_name': 'Иванова', 'age': 32, 'gender': 'Женский', 'address': 'ул. Ленина, 14', 'email': 'anna@example.com'},
        {'first_name': 'Иван', 'last_name': 'Петров', 'age': 45, 'gender': 'Мужской', 'address': 'проспект Свободы, 7', 'email': 'ivan@example.com'},
        {'first_name': 'Ольга', 'last_name': 'Сидорова', 'age': 28, 'gender': 'Женский', 'address': 'ул. Пушкина, 23', 'email': 'olga@example.com'},
        {'first_name': 'Павел', 'last_name': 'Смирнов', 'age': 38, 'gender': 'Мужской', 'address': 'проспект Мира, 55', 'email': 'pavel@example.com'},
        {'first_name': 'Мария', 'last_name': 'Козлова', 'age': 41, 'gender': 'Женский', 'address': 'ул. Гагарина, 8', 'email': 'maria@example.com'},
        {'first_name': 'Александр', 'last_name': 'Иванов', 'age': 52, 'gender': 'Мужской', 'address': 'проспект Ленина, 3', 'email': 'alexander@example.com'},
        {'first_name': 'Елена', 'last_name': 'Федорова', 'age': 36, 'gender': 'Женский', 'address': 'ул. Московская, 12', 'email': 'elena@example.com'}
    ]

    # Добавление данных в таблицу
    for client_data in clients_data:
        client = Client(**client_data)
        db.session.add(client)

    # Сохранение изменений в базе данных
    db.session.commit()

# Применяем изменения к базе данных
db.session.commit()

def hash_data(self, client_data):
    # Преобразуйте данные о клиенте в строку для хэширования
    client_data_string = json.dumps(client_data, sort_keys=True)
    # Примените хэш-функцию SHA256 к строке данных о клиенте
    hashed_data = hashlib.sha256(client_data_string.encode()).hexdigest()
    return hashed_data

# Создаем объект класса blockchain
blockchain = Blockchain()
# Майнинг нового блока
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'client_hash': block["client_hash"]}
    return jsonify(response), 200
# Отобразить блокчейн в формате json
@app.route('/display_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
# Проверка валидности блокчейна
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
app.run(host='0.0.0.0', port=8000)

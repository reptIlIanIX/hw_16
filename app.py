import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


def users_data():
    with open('data/users.json', 'r') as file:
        user = json.load(file)
        return user


def offer_data():
    with open('data/offers.json', 'r') as file:
        offer = json.load(file)
        return offer


def orders_data():
    with open('data/orders.json', 'r', encoding='utf8') as file:
        order = json.load(file)
        return order


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship('Order')
    user = db.relationship('User')


db.drop_all()
db.create_all()

for item in users_data():
    user_add = db.session.add(
        User(id=item['id'], first_name=item['first_name'], last_name=item['last_name'], age=item['age'],
             email=item['email'], role=item['role'], phone=item['phone']))

for item in orders_data():
    db.session.add(
        Order(id=item['id'], name=item['name'], description=item['description'], start_date=item['start_date'],
              end_date=item['end_date'], address=item['address'], price=item['price'],
              customer_id=item['customer_id'],
              executor_id=item['executor_id']))

for item in offer_data():
    db.session.add(Offer(id=item['id'], order_id=item['order_id'], executor_id=item['executor_id']))

db.session.commit()
db.session.close()


def return_user_data(self):
    return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "age": self.age,
        "email": self.email,
        "role": self.role,
        "phone": self.phone,
    }


def return_order_data(self):
    return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "start_date": self.start_date,
        "end_date": self.end_date,
        "address": self.address,
        "price": self.price,
        "customer_id": self.customer_id,
        "executor_id": self.executor_id,

    }


def return_offer_data(self):
    return {
        "id": self.id,
        "order_id": self.order_id,
        "executor_id": self.executor_id,
    }


@app.route('/users', methods=['GET', 'POST'])
def all_users():
    if request.method == 'POST':
        data = request.json
        user = User(id=data.get('id'), first_name=data.get('first_name'), last_name=data.get('last_name'),
                    age=data.get('age'),
                    email=data.get('email'), role=data.get('role'), phone=data.get('phone'))
        db.session.add(user)
        db.session.commit()
        return jsonify(return_user_data(user))
    else:
        users = User.query.all()
        all_users = []
        for user in users:
            all_users.append(return_user_data(user))
        return jsonify(all_users)


@app.route('/orders')
def all_orders():
    orders = Order.query.all()
    all_orders = []
    for order in orders:
        all_orders.append(return_order_data(order))
    return jsonify(all_orders)


@app.route('/offers')
def all_offers():
    offers = Offer.query.all()
    all_offers = []
    for offer in offers:
        all_offers.append(return_offer_data(offer))
    return jsonify(all_offers)


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def by_id_users(id: int):
    if request.method == 'GET':
        users = User.query.all()
        for user in users:
            if user.id == id:
                user_id = jsonify(return_user_data(user))
                return user_id
    elif request.method == 'PUT':
        data = request.json
        user = db.session.query(User).get(id)
        user.id = data.get("id")
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.age = data.get('age')
        user.email = data.get('email')
        user.role = data.get('role')
        user.phone = data.get('phone')
        db.session.commit()
        return jsonify(return_user_data(user))
    elif request.method == 'DELETE':
        db.session.query(User).filter(User.id == id).delete()
        db.session.commit()
        return "Пользователь удален"


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def by_id_orders(id: int):
    if request.method == 'GET':
        orders = Order.query.all()
        for order in orders:
            if order.id == id:
                order_id = jsonify(return_order_data(order))
                return order_id
    elif request.method == 'PUT':
        data = request.json
        order = db.session.query(Order).get(id)
        order.id = data.get("id")
        order.name = data.get('name')
        order.description = data.get('description')
        order.start_date = data.get('start_date')
        order.end_date = data.get('end_date')
        order.address = data.get('address')
        order.price = data.get('price')
        order.customer_id = data.get('customer_id')
        order.executor_id = data.get('executor_id')
        db.session.commit()
        return jsonify(return_order_data(order))
    elif request.method == 'DELETE':
        db.session.query(Order).filter(Order.id == id).delete()
        db.session.commit()
        return "Заказ удален"


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def by_id_offers(id: int):
    if request.method == 'GET':
        offers = Offer.query.all()
        for offer in offers:
            if offer.id == id:
                offer_id = jsonify(return_offer_data(offer))
                return offer_id
    elif request.method == 'PUT':
        data = request.json
        offer = db.session.query(Offer).get(id)
        offer.id = data.get("id")
        offer.order_id = data.get('order_id')
        offer.executor_id = data.get('executor_id')
        db.session.commit()
        return jsonify(return_offer_data(offer))
    elif request.method == 'DELETE':
        db.session.query(Offer).filter(Offer.id == id).delete()
        db.session.commit()
        return "Предложение удалено"


if __name__ == '__main__':
    app.run()

from flask_sqlalchemy_rest.db import db


class Product(db.Model):
    """Product contains the model for a product insance"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('products', lazy=True))

    def __init__(self, name, description, price, quantity, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

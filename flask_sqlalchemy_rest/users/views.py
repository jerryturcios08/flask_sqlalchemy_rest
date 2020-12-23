from flask import Blueprint, jsonify, request

from flask_sqlalchemy_rest.db import db
from flask_sqlalchemy_rest.products.model import Product
from flask_sqlalchemy_rest.products.schema import products_schema

from .model import User
from .schema import user_schema

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/', methods=('POST',))
def create_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    error = None

    if not first_name:
        error = 'First name is required.'
    elif not last_name:
        error = 'Last name is required.'
    elif not email:
        error = 'Email is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    else:
        return jsonify({'error': error})


@blueprint.route('/<int:id>/', methods=('GET',))
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@blueprint.route('/<int:id>/products/', methods=('GET',))
def get_products_by_user(id):
    products = Product.query.filter_by(user_id=id).all()
    return products_schema.jsonify(products)

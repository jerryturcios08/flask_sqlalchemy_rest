from flask import Blueprint, jsonify, request

from flask_sqlalchemy_rest.auth.views import token_required
from flask_sqlalchemy_rest.db import db

from .model import Product
from .schema import product_schema, products_schema

blueprint = Blueprint('products', __name__, url_prefix='/products')


# Create a Product
@blueprint.route('/', methods=('POST',))
@token_required
def add_product(current_user):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    user_id = request.json['user_id']
    error = None

    if not name:
        error = 'Name is required.'
    elif not description:
        error = 'Description is required.'
    elif not price:
        error = 'Price is required.'
    elif not quantity:
        error = 'Quantity is required.'
    elif not user_id:
        error = 'User ID is required.'
    elif user_id != current_user.id:
        error = 'Current user token not verified'

    if error is None:
        new_product = Product(name, description, price, quantity, user_id)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)
    else:
        return jsonify({'error': error})


# Get all products
@blueprint.route('/', methods=('GET',))
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get product
@blueprint.route('/<int:id>/', methods=('GET',))
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update products
@blueprint.route('/<int:id>/', methods=('PUT',))
@token_required
def update_product(current_user, id):
    product = Product.query.get(id)

    if product.user_id != current_user.id:
        return jsonify({'error': 'Current user token not verified'})

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()
    return product_schema.jsonify(product)


# Delete products
@blueprint.route('/<int:id>/', methods=('DELETE',))
@token_required
def delete_product(current_user, id):
    product = Product.query.get(id)

    if product.user_id != current_user.id:
        return jsonify({'error': 'Current user token not verified'})

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

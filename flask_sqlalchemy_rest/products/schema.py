from flask_sqlalchemy_rest.db import ma


class ProductSchema(ma.Schema):
    """ProductSchema defines the schema for serialization of the products model"""
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity', 'user_id')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

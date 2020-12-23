from flask_sqlalchemy_rest.db import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


user_schema = UserSchema()

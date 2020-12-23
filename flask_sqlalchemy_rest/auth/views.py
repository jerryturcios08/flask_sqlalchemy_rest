from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, current_app, jsonify, make_response, request
from jwt import decode, encode, DecodeError
from werkzeug.security import check_password_hash

from flask_sqlalchemy_rest.users.model import User

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/login/', methods=('GET', 'POST'))
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(email=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = encode(
            {'id': user.id, 'exp': datetime.utcnow() + timedelta(days=12)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'A valid token is missing.'})

        try:
            data = decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except DecodeError:
            return jsonify({'message': 'Token is invalid.'})

        return func(current_user, *args, **kwargs)
    return decorator

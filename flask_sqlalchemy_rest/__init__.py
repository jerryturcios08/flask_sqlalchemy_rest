import os

from flask import Flask
from flask_migrate import Migrate

from flask_sqlalchemy_rest import products, users
from flask_sqlalchemy_rest.auth import views
from flask_sqlalchemy_rest.db import db

# App configuration
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy configuration
app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth.views.blueprint)
app.register_blueprint(products.views.blueprint)
app.register_blueprint(users.views.blueprint)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, 
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object(Config)
data_base = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    username = data_base.Column(data_base.String(200), unique=True, nullable=False)
    email = data_base.Column(data_base.String(250), unique=True, nullable=False)
    password = data_base.Column(data_base.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password, password)
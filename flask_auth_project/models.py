from app import data_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    username = data_base.Column(data_base.String(200), unique=True, nullable=False)
    email = data_base.Column(data_base.String(250), unique=True, nullable=False)
    password = data_base.Column(data_base.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
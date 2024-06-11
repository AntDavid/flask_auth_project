from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
data_base = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm


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
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('login.html'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        data_base.session.add(new_user)
        data_base.session.commit()
        flash('Account created successfully.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile')    
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
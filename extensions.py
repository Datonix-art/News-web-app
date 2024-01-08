import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from admin_views import AdminModelView


app = Flask(__name__ , template_folder='templates')
app.config["SECRET_KEY"] = os.urandom(20)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["FLASK_ADMIN_SWATCH"] = 'Slate'

db = SQLAlchemy(app)

admin = Admin(app, index_view=AdminModelView())

login_manager = LoginManager(app)
login_manager.login_view = "signUp"

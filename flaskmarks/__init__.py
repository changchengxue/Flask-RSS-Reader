from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
config = app.config
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from flaskmarks import views
from flaskmarks import models
from flaskmarks import filters

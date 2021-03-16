from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import MetaData

from data.DatabaseConfig import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

meta = MetaData()
meta.bind = db

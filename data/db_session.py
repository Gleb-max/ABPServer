from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import MetaData

from data.DatabaseConfig import Config

app = Flask(__name__, static_folder="static")
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
db.create_all()
db.session.commit()


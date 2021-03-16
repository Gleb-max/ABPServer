from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import MetaData

from data.DatabaseConfig import Config
import sqlalchemy as sa



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

meta = MetaData()
meta.bind = db

sa.ForeignKey('IndividualAchievement.id')
association_table = sa.Table('association', meta,
                             sa.Column('enrollee_id', sa.Integer, sa.ForeignKey('enrollee.id')),
                             sa.Column('achievement_id', sa.Integer, sa.ForeignKey('IndividualAchievement.id'))
                             )




import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask import Flask

from data.DatabaseConfig import Config

SqlAlchemyBase = dec.declarative_base()
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

# __factory = None
#
#
# def global_init(db_file):
#     global __factory
#
#     if __factory:
#         return
#
#     if not db_file or not db_file.strip():
#         raise Exception("Необходимо указать файл базы данных.")
#
#     # для heroku (там бесплатные плагины только с postgres):
#     if db_file.startswith("postgres://"):
#         conn_str = db_file
#         print("POSTGRES selected")
#     else:
#         conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
#     print(f"Подключение к базе данных по адресу {conn_str} ...")
#     print(conn_str)
#     engine = sa.create_engine(conn_str, echo=False)
#     print('Подключено')
#     __factory = orm.sessionmaker(bind=engine)
#
#     from . import __all_models
#     SqlAlchemyBase.metadata.drop_all(engine)
#     print('tables was dropped')
#     SqlAlchemyBase.metadata.create_all(engine)
#
#
# def create_session() -> Session:
#     global __factory
#     return __factory()

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from data.db_session import app, db

db.drop_all()
print('Drop tables...')
db.session.commit()
db.create_all()
print('Create tables...')
db.session.commit()

# migrate = Migrate(app, db)
# manager = Manager(app)
#
# manager.add_command('db', MigrateCommand)
#
#
# if __name__ == '__main__':
#     manager.run()
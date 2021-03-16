from flask_admin.contrib.sqla import ModelView
from data.__all_models import *
from blueprints import client
from flask import Flask, render_template, redirect, abort, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_admin import Admin
from data.db_session import app, db
from config import *
from flask_restful import Api
import logging

from data.enrollee import Enrollee
from data.exam_info import ExamInfo
from data.study_direction import StudyDirection
from data.user import User


def initAdmin():
    app.secret_key = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(user.User, db.session))
    admin.add_view(ModelView(enrollee.Enrollee, db.session))
    admin.add_view(ModelView(passport.Passport, db.session))
    admin.add_view(ModelView(school_certificate.SchoolCertificate, db.session))
    admin.add_view(ModelView(study_direction.StudyDirection, db.session))
    admin.add_view(ModelView(exam_info.ExamInfo, db.session))
    admin.add_view(ModelView(individual_achievements.IndividualAchievement, db.session))


@app.route("/")
def index():
    return "SGU API"


# for favicon
@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="img/favicon.ico"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/policy")
def policy():
    return render_template("policy.html", title="Политика конфиденциальности")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# register blueprint for mobile and desktop clients
app.register_blueprint(client.blueprint)

print('Creating tables...')
db.create_all()
db.session.commit()
print('Initializing admin panel...')
initAdmin()

# add resources
api = Api(app)
# api.add_resource(ReceiptsListResource, "/api/v2/receipts")


if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    db.session.commit()
    print('DB was created')
    host = PRODUCTION_HOST if PRODUCTION else LOCAL_HOST
    app.run(host=host, port=PORT)

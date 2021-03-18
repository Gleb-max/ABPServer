import json

from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func, and_, case

from admin.admin import ViewWithPK
from data import faculty, enrollee_statuses, student, dean
from data.__all_models import *
from blueprints import client
from flask import Flask, render_template, redirect, abort, url_for, send_from_directory, request, make_response
from flask_login import LoginManager, login_required, logout_user
from flask_admin import Admin
from data.db_session import app, db
from config import *
from flask_restful import Api
import logging
import sys

from data.enrollee import Enrollee
from data.exam_info import ExamInfo
from data.student import Student
from data.study_direction import StudyDirection
from data.user import User
from document_creator import create_student_personal_profile, create_student_record_book, create_student_card
from resources.receipts import EnrollsList, StudentsList


def initAdmin():
    app.secret_key = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewWithPK(user.User, db.session))
    admin.add_view(ViewWithPK(enrollee.Enrollee, db.session))
    admin.add_view(ViewWithPK(student.Student, db.session))
    admin.add_view(ViewWithPK(dean.Dean, db.session))
    admin.add_view(ModelView(passport.Passport, db.session))
    admin.add_view(ModelView(school_certificate.SchoolCertificate, db.session))
    admin.add_view(ModelView(study_direction.StudyDirection, db.session))
    admin.add_view(ModelView(faculty.Faculty, db.session))
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


@app.route('/get_file/<path:path>', methods=['GET'])
def download(path):
    return send_from_directory(filename=path, directory=os.path.abspath(os.getcwd()), cache_timeout=None)


@app.route('/confirm_form', methods=['GET'])
def enrollee_form_confirm(path):
    return send_from_directory(filename=path, directory=os.path.abspath(os.getcwd()))


@app.route('/get_rating_table', methods=['POST'])
def get_rating_table():
    direction_id = request.form.get('direction_id')
    need_hostel = request.form.get('need_hostel')

    enrolls = []
    print(direction_id, need_hostel, file=sys.stderr)

    if need_hostel == None:
        pass
    elif need_hostel.lower() == 'true':
        need_hostel = True
    elif need_hostel.lower() == 'false':
        need_hostel = False
    else:
        need_hostel = None

    if int(direction_id) < 0:  # Весь ВУЗ
        enrolls = Enrollee.query.filter(
            and_(
                # прошедшие проверку
                Enrollee.consideration_stage == enrollee_statuses.STAGE_RECEIVED,
                # нужно ли общежитие
                Enrollee.need_hostel == need_hostel if (need_hostel != None) else True
            )
        ).all()
    elif int(direction_id) > 0:  # По Факультетам
        enrolls = Enrollee.query.filter(
            and_(
                # прошедшие проверку
                Enrollee.consideration_stage == enrollee_statuses.STAGE_RECEIVED,
                # факультет
                Enrollee.study_direction_id == direction_id,
                # нужно ли общежитие
                Enrollee.need_hostel == need_hostel if (need_hostel != None) else True
            )
        ).all()
    else:
        return make_response({'result': 'Incorrect request params'}, 400)

    enrolls.sort(key=lambda x: x.get_exam_total_grade(), reverse=True)
    ans = []
    for enr in enrolls:
        ans.append({
            'user': enr.user.to_dict(),
            'exam_total_grade': enr.get_exam_total_grade(),
            'individual_grade': enr.get_individual_grade(),
            'is_original': enr.original_or_copy
        })
    return make_response(json.dumps({'table': ans}), 200)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# register blueprint for mobile and desktop clients
app.register_blueprint(client.blueprint)

# db init
print('Creating tables...')
db.create_all()
db.session.commit()

print('Initializing admin panel...')
initAdmin()

# add resources
api = Api(app)
api.add_resource(EnrollsList, "/api/v2/enrolls")
api.add_resource(StudentsList, "/api/v2/students")

if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    db.session.commit()

    user = User.query.first()
    try:
        ans = create_student_card('test', user)
        # ans = create_student_record_book('test', user)
        print(ans)
    except Exception as e:
        print(e)

    host = PRODUCTION_HOST if PRODUCTION else LOCAL_HOST
    app.run(host=host, port=PORT, debug=True)

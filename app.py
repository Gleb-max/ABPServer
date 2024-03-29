import json

import flask
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func, and_, case

from admin.admin import ViewWithPK
from data import faculty, enrollee_statuses, student, dean, subject, teacher
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
from data.generate_subjects_by_direction import fill_teachers, fill_subjects
from data.student import Student
from data.study_direction import StudyDirection
from data.user import User
from document_creator import create_student_personal_profile, create_student_record_book, create_student_card
from resources.api import *


def initAdmin():
    app.secret_key = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewWithPK(user.User, db.session))
    admin.add_view(ViewWithPK(enrollee.Enrollee, db.session))
    admin.add_view(ViewWithPK(student.Student, db.session))
    admin.add_view(ViewWithPK(dean.Dean, db.session))
    admin.add_view(ViewWithPK(students_group.StudentsGroup, db.session))
    admin.add_view(ModelView(passport.Passport, db.session))
    admin.add_view(ModelView(school_certificate.SchoolCertificate, db.session))
    admin.add_view(ViewWithPK(study_direction.StudyDirection, db.session))
    admin.add_view(ModelView(faculty.Faculty, db.session))
    admin.add_view(ModelView(exam_info.ExamInfo, db.session))
    admin.add_view(ModelView(individual_achievements.IndividualAchievement, db.session))
    admin.add_view(ViewWithPK(subject.Subject, db.session))
    admin.add_view(ViewWithPK(teacher.Teacher, db.session))


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
    return send_from_directory(filename=path, directory=os.path.abspath(os.getcwd()), as_attachment=True,
                               cache_timeout=0)


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


# no file cache
app.get_send_file_max_age = lambda x: 0

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
api.add_resource(ChangeStudentInfo, "/api/v2/change_student_info")
api.add_resource(StudentPersonalDossier, "/api/v2/get_student_dossier")
api.add_resource(StudentCard, "/api/v2/get_student_cards")
api.add_resource(StudentRecordBook, "/api/v2/get_record_books")
api.add_resource(InstructTable, "/api/v2/get_instruct_table")
api.add_resource(AttendanceTable, "/api/v2/get_attendance_table")
api.add_resource(StudentSubjectsInfo, "/api/v2/get_group_subjects")

# db filling if can
try:
    fill_teachers()
    fill_subjects()
except Exception as e:
    print(e)

if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    db.session.commit()
    fill_teachers()

    # user = User.query.first()
    # ans = create_instruct_table('test', User.query.all(), 'name')
    create_attendance_log('test', User.query.all(), StudentsGroup.query.first())
    try:
        pass
        # ans = create_student_card('test1', user)
        # ans = create_student_record_book('test2', user)
        # ans = create_student_personal_profile('test3', user)

    except Exception as e:
        print(e)

    host = PRODUCTION_HOST if PRODUCTION else LOCAL_HOST
    app.run(host=host, port=PORT, debug=True)

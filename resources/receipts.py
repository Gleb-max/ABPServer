from datetime import datetime

from flask import make_response
from flask_restful import abort, Resource
from sqlalchemy import and_

from data.db_session import db
from data.enrollee import Enrollee
import json

from data.student import Student
from data.students_group import StudentsGroup
from data.study_direction import StudyDirection
from data.user import User
from parsers.receipts import parser_get_enrolles, parser_student_info


class EnrollsList(Resource):
    def get(self):
        answer = []

        args = parser_get_enrolles.parse_args()
        direction_id = args["direction_id"]

        if direction_id:
            direction_id = int(direction_id)
            enrollee_list = Enrollee.query.filter_by(study_direction_id=direction_id).all()
        else:
            enrollee_list = Enrollee.query.all()

        for enrollee in enrollee_list:
            user_dict = {}
            if enrollee.user:
                user_dict = enrollee.user.to_dict()
            if enrollee:
                combined_dict = enrollee.to_dict()
                combined_dict.update(user_dict)

                combined_dict['enrollee_pk'] = enrollee.id

                answer.append(combined_dict)

        return json.dumps({'enrolls': answer})


class ChangeStudentInfo(Resource):
    def post(self):
        answer = []

        args = parser_student_info.parse_args()
        user_id = args["user_id"]
        email = args['email']
        registration_address = args['registration_address']
        residence_address = args['residence_address']
        group_name = args['group_name']
        library_card_number = args['library_card_number']
        series = args['series']
        number = args['number']
        who_issued = args['who_issued']
        department_code = args['department_code']
        when_issued = args['when_issued']

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response({'result': 'user not found'}, 404)

        if email:
            user.email = email

        if registration_address:
            user.enrollee.passport.registration_address = registration_address

        if residence_address:
            user.enrollee.passport.residence_address = residence_address

        if group_name:
            students_group = StudentsGroup.query.filter_by(name=group_name).first()
            if not students_group:
                return make_response({'result': 'student group not found'})

            user.student.student_group = students_group
            user.enrollee.study_direction = students_group.direction

        if library_card_number:
            user.student.library_card_number = library_card_number

        if series:
            user.passport.series = series

        if number:
            user.passport.number = number

        if who_issued:
            user.passport.who_issued = who_issued

        if department_code:
            user.passport.department_code = who_issued

        if when_issued:
            who_issued = datetime.strptime(when_issued, '%Y-%m-%d')
            user.passport.when_issued = who_issued

        db.session.commit()

        return make_response({'result': 'success'}, 200)


class StudentsList(Resource):
    def get(self):
        answer = []

        args = parser_get_enrolles.parse_args()
        direction_id = args["direction_id"]

        if direction_id:
            direction_id = int(direction_id)
            data = db.session.query(User).join(Student).join(Enrollee).filter(
                Enrollee.study_direction_id == direction_id).all()
        else:
            data = db.session.query(User).join(Student).join(Enrollee).all()

        for user in data:
            enrollee_dict = user.enrollee.to_dict()
            user_dict = user.to_dict()
            user_dict.update(enrollee_dict)
            answer.append(user_dict)

        return json.dumps({'students': answer})

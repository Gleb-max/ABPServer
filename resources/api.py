import os
from datetime import datetime

from flask import make_response, send_from_directory
from flask_restful import abort, Resource
from sqlalchemy import and_

from data.db_session import db
from data.enrollee import Enrollee
import json

from data.student import Student
from data.students_group import StudentsGroup
from data.study_direction import StudyDirection
from data.user import User
from parsers.receipts import parser_get_enrolles, parser_student_info, parser_get_student_dossier, \
    parser_get_student_card
from document_creator import *

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
        phone = args['phone']
        print(phone, user_id, email, residence_address, series, number)

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response({'result': 'user not found'}, 404)

        if email:
            user.email = email
            print(email)
            db.session.commit()
            print(user.email, email)

        if registration_address:
            user.enrollee.passport.registration_address = registration_address
            db.session.commit()

        if residence_address:
            user.enrollee.passport.residence_address = residence_address
            db.session.commit()

        if group_name:
            students_group = StudentsGroup.query.filter_by(name=group_name).first()
            if not students_group:
                return make_response({'result': 'student group not found'})

            user.student.student_group = students_group
            user.enrollee.study_direction = students_group.direction
            db.session.commit()

        if library_card_number:
            user.student.library_card_number = library_card_number
            db.session.commit()

        if phone:
            user.enrollee.phone = phone
            db.session.commit()

        if series:
            user.enrollee.passport.series = series
            db.session.commit()

        if number:
            user.enrollee.passport.number = number
            db.session.commit()

        if who_issued:
            user.enrollee.passport.who_issued = who_issued
            db.session.commit()

        if department_code:
            print(department_code)
            user.enrollee.passport.department_code = department_code
            print(user.enrollee.passport)
            db.session.commit()

        if when_issued:
            who_issued = datetime.strptime(when_issued, '%Y-%m-%d')
            user.enrollee.passport.when_issued = who_issued
            db.session.commit()

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


class StudentPersonalDossier(Resource):
    def get(self):
        args = parser_get_student_dossier.parse_args()
        user_id = args["user_id"]
        user = User.query.filter_by(id=user_id).first()

        if not user or not user.student:
            return make_response({'result': 'student not found'}, 404)

        path = f'media/dossiers/{user.id}_report'
        file_path = create_student_personal_profile(path, user, need_pdf=True)
        print(file_path)
        return file_path
        # return send_from_directory(filename=file_path, directory=os.path.abspath(os.getcwd()),as_attachment=True, cache_timeout=0)


class StudentRecordBook(Resource):
    def get(self):
        args = parser_get_student_card.parse_args()
        user_id = args["user_id"]
        direction_id = args['direction_id']
        file_name = ''
        users_data = []

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            users_data = [user]
            file_name = f'user_{user_id}'
        elif direction_id:
            users_data = db.session.query(User).join(Student).join(Enrollee).filter(
                Enrollee.study_direction_id == direction_id).all()
            file_name = f'direction_{direction_id}'

        path = f'media/student_record_books/{file_name}_report'
        file_path = create_student_record_book(path, users_data, need_pdf=True)
        print(file_path)
        return file_path


class StudentCard(Resource):
    def get(self):
        args = parser_get_student_card.parse_args()
        user_id = args["user_id"]
        direction_id = args['direction_id']
        file_name = ''
        users_data = []

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            users_data = [user]
            file_name = f'user_{user_id}'
        elif direction_id:
            users_data = db.session.query(User).join(Student).join(Enrollee).filter(
                Enrollee.study_direction_id == direction_id).all()
            file_name = f'direction_{direction_id}'

        path = f'media/student_cards/{file_name}_report'
        file_path = create_student_card(path, users_data, need_pdf=True)
        print(file_path)
        return file_path


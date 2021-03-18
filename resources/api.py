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
    parser_get_student_card, parser_instruct_table
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

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response({'result': 'user not found'}, 404)

        passport = user.enrollee.passport

        if email:
            user.email = email
            db.session.commit()

        if registration_address:
            passport.registration_address = registration_address
            db.session.commit()

        if residence_address:
            passport.residence_address = residence_address
            db.session.commit()

        if library_card_number:
            user.student.library_card_number = library_card_number
            db.session.commit()

        if phone != None:
            user.enrollee.phone = phone
            db.session.commit()

        if series != None:
            passport.series = series
            db.session.commit()

        if number != None:
            passport.number = number
            db.session.commit()

        if who_issued != None:
            passport.who_issued = who_issued
            db.session.commit()

        if department_code != None:
            passport.department_code = department_code
            db.session.commit()

        print(when_issued)
        if when_issued != None:
            when_issued = datetime.strptime(when_issued, '%Y-%m-%d')
            passport.when_issued = when_issued
            db.session.commit()

        db.session.commit()

        if group_name:
            students_group = StudentsGroup.query.filter_by(name=group_name).first()
            if not students_group:
                return make_response({'result': 'student group not found'})

            user.student.student_group = students_group
            user.enrollee.study_direction = students_group.direction
            db.session.commit()

        print('data was changed successfully')
        return make_response({'result': 'success'}, 200)


class StudentsList(Resource):
    def get(self):
        answer = []

        args = parser_get_enrolles.parse_args()
        direction_id = args["direction_id"]
        print(direction_id)
        if direction_id:
            direction_id = int(direction_id)
            direction = StudyDirection.query.filter_by(id=direction_id).first()
            groups = direction.groups
            data = []
            for g in groups:
                studs = g.students
                for s in studs:
                    data.append(s.user)
            # data = db.session.query(User).join(Student).join(Enrollee).filter(
            #     Enrollee.study_direction_id == direction_id).all()
        else:
            data = db.session.query(User).join(Student).join(Enrollee).all()

        for user in data:
            enrollee_dict = user.enrollee.to_dict()
            print(user.name, user.enrollee.study_direction.id)
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
        file_path = create_student_personal_profile(path, user, need_pdf=False)
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
        file_path = create_student_record_book(path, users_data, need_pdf=False)
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
        file_path = create_student_card(path, users_data, need_pdf=False)
        print(file_path)
        return file_path


class InstructTable(Resource):
    def get(self):
        args = parser_instruct_table.parse_args()
        group_id = args['group_id']

        file_name = ''
        print(group_id)
        convert_gleb_to_api = {
            'ИТ': 3,
            'ЗСИС': 2,
            'ПМ': 5,
            'ИИВТ': 1,
            'АУВТС': 4,
        }

        student_group = StudentsGroup.query.filter_by(id=group_id).first()
        print("group id:", group_id, "name:", student_group.name, "group_direction:", student_group.direction.name)

        if not student_group:
            return make_response({'result': 'group not found'}, 404)

        subject_name = "Физика"
        users = []

        # взять юзеров по имени группы
        # students = Student.query.filter(Student.student_group.name == student_group.name).all()
        student_group = StudentsGroup.query.filter_by(name=student_group.name).first()

        for st in student_group.students:
            users.append(st.user)
            print(st.user.name, st.student_group.direction.name)

        file_name = f'instruct_table_{student_group.id}'

        path = f'media/instruct_tables/{file_name}_report'
        file_path = create_instruct_table(path, users, subject_name, need_pdf=False)

        return file_path


class AttendanceTable(Resource):
    def get(self):
        args = parser_instruct_table.parse_args()
        group_id = args['group_id']

        file_name = ''

        student_group = StudentsGroup.query.filter_by(id=group_id).first()
        if not student_group:
            return make_response({'result': 'group not found'}, 404)

        subject_name = student_group.direction.name
        users = []
        for st in student_group.students:
            users.append(st.user)

        file_name = f'attendence_table_{student_group.id}'

        path = f'media/instruct_tables/{file_name}_report'
        file_path = create_attendance_log(path, users, student_group)

        return file_path

from flask_restful import abort, Resource
from sqlalchemy import and_

from data.db_session import db
from data.enrollee import Enrollee
import json

from data.student import Student
from data.user import User
from parsers.receipts import parser_get_enrolles


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


class StudentsList(Resource):
    def get(self):
        answer = []

        args = parser_get_enrolles.parse_args()
        direction_id = args["direction_id"]

        if direction_id:
            direction_id = int(direction_id)
            data = db.session.query(User).join(Student).join(Enrollee).filter(
                Enrollee.study_direction_id == direction_id).all()
            # data = Student.query.filter(and_(
            #     (not Student.user.enrollee),
            #     Student.user.enrollee.direction_id == direction_id)
            # ).all()
        else:
            data = db.session.query(User).join(Student).join(Enrollee).all()

        for user in data:
            user_dict = user.to_dict()
            answer.append(user_dict)

        return json.dumps({'students': answer})

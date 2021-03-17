from flask_restful import abort, Resource

from data.enrollee import Enrollee
import json

from parsers.receipts import parser_get_enrolles


class EnrollsList(Resource):
    def get(self):
        answer = []

        args = parser_get_enrolles.parse_args()
        direction_id = args["direction_id"]

        if direction_id and direction_id.isdigit():
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

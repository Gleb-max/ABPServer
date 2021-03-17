from flask_restful import abort, Resource

from data.enrollee import Enrollee
import json

from parsers.receipts import parser_get_enrolles


class EnrollsList(Resource):
    def get(self):
        answer = []

        for enrollee in Enrollee.query.all():
            user_dict = {}
            if enrollee.user:
                user_dict = enrollee.user.to_dict()
            if enrollee:
                combined_dict = enrollee.to_dict()
                combined_dict.update(user_dict)

                combined_dict['enrollee_pk'] = enrollee.id

                answer.append(combined_dict)

        return json.dumps({'enrolls': answer})




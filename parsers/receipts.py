import datetime

from flask_restful import reqparse, inputs

parser_get_all = reqparse.RequestParser()
parser_get_all.add_argument("phone", required=True, type=str)
parser_get_all.add_argument("period", required=True, type=str)

parser_receipt = reqparse.RequestParser()
parser_receipt.add_argument("phone", required=True, type=str)

parser_create = reqparse.RequestParser()
parser_create.add_argument("phone", required=True, type=str)
parser_create.add_argument("password", required=True, type=str)
parser_create.add_argument("scan_result", required=True, type=str)

parser_get_enrolles = reqparse.RequestParser()
parser_get_enrolles.add_argument("direction_id", required=False, type=int)

parser_student_info = reqparse.RequestParser()
parser_student_info.add_argument("user_id", required=True, type=int)
parser_student_info.add_argument("email", required=False, type=str)
parser_student_info.add_argument("registration_address", required=False, type=str)
parser_student_info.add_argument("residence_address", required=False, type=str)
parser_student_info.add_argument("group_name", required=False, type=str)
parser_student_info.add_argument("library_card_number", required=False, type=int)
# passport
parser_student_info.add_argument("series", required=False, type=int)
parser_student_info.add_argument("number", required=False, type=int)
parser_student_info.add_argument("who_issued", required=False, type=str)
parser_student_info.add_argument("department_code", required=False, type=int)
parser_student_info.add_argument("when_issued", required=False, type=str)


parser_get_student_dossier = reqparse.RequestParser()
parser_get_student_dossier.add_argument("user_id", required=True, type=int)


from flask_restful import reqparse


parser_get_all = reqparse.RequestParser()
parser_get_all.add_argument("phone", required=True, type=str)
parser_get_all.add_argument("period", required=True, type=str)

parser_receipt = reqparse.RequestParser()
parser_receipt.add_argument("phone", required=True, type=str)

parser_create = reqparse.RequestParser()
parser_create.add_argument("phone", required=True, type=str)
parser_create.add_argument("password", required=True, type=str)
parser_create.add_argument("scan_result", required=True, type=str)

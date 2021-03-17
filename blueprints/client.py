import re
import json

from transliterate import slugify

from config import MAIL_PASSWORD, MAIL_LOGIN
from data import account_types
from data.enrollee import Enrollee
from data.exam_info import ExamInfo
from data.individual_achievements import IndividualAchievement
from data.passport import Passport
from data.school_certificate import SchoolCertificate
from data.study_direction import StudyDirection
from data.user import User
from blueprints.constants import *
# from data.db_session import create_session
from flask import jsonify, Blueprint, make_response, request

from document_creator import create_order_of_admission
from utils import filling_all
from data.db_session import db
from datetime import datetime
from data import enrollee_statuses
import smtplib as smtp
from email.mime.text import MIMEText

blueprint = Blueprint("clients_api", __name__, template_folder="templates")


@blueprint.route("/error/", methods=["GET", 'POST'])
def show_errors():
    if request.method == 'POST':
        with open('errors.txt', 'a') as f:
            f.write(request.form.get('error') + '<br>\n')
        return make_response(RESULT_SUCCESS, 200)

    with open('errors.txt', 'r') as f:
        return f.read()


@blueprint.route("/error/clean", methods=["GET", 'POST'])
def clean_error_page():
    with open('errors.txt', 'w') as f:
        f.write('')
    return make_response(RESULT_SUCCESS, 200)


@blueprint.route("/client/registration/", methods=["POST"])
def user_registration():
    name = request.form.get("name")
    surname = request.form.get("surname")
    last_name = request.form.get("last_name")

    is_male = request.form.get("is_male")
    email = request.form.get("email")
    password = request.form.get("password")

    if not filling_all(name, surname, last_name, is_male, email, password):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    name = name.capitalize()
    surname = surname.capitalize()
    last_name = last_name.capitalize()
    is_male = convert_bool_str_to_bool(is_male)

    email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    pattern = re.compile(email_pattern)
    if not re.match(pattern, email):
        return make_response(EMAIL_INCORRECT, 400)

    if User.query.filter_by(email=email).first():
        return make_response(USER_ALREADY_CREATED, 409)

    user = User(
        name, surname, last_name,
        is_male, email, password
    )

    try:
        db.session.add(user)
        db.session.commit()
        db.session.close()
    except Exception as e:
        print(f"Register user error: {e}")
        return make_response(INTERNAL_ERROR, 500)

    return make_response(RESULT_SUCCESS, 200)


def check_field_and_set(field, model, value):
    if value not in [None, ""]:
        setattr(model, field, value)
        db.session.commit()


def convert_bool_str_to_bool(string):
    return string == 'true'


def convert_str_to_datetime(string):
    # date_time_example = '29.06.2020'
    return datetime.strptime(string, '%d.%m.%Y')


def update_enrollee_state(e: Enrollee):
    need_employee_data = [e.photo, e.exam_data_list, e.study_direction, e.individual_achievement_list,
                          e.exam_data_list, e.birthday, e.phone, e.birth_place,
                          e.need_hostel, e.photo, e.agreement_scan, e.is_budgetary,
                          e.original_or_copy,
                          e.enrollment_consent
                          ]

    need_passport_data = [
        e.passport.series, e.passport.number, e.passport.who_issued, e.passport.department_code,
        e.passport.when_issued, e.passport.passport_scan, e.passport.registration_address
    ]

    need_certification_data = [e.school_certificate.certificate_scan, e.school_certificate.certificate_number]
    need_data = need_certification_data + need_passport_data + need_employee_data
    without_original_need = need_data.copy()
    without_original_need.remove(e.enrollment_consent)
    without_original_need.remove(e.original_or_copy)

    if not any(need_data):  # данные не внесены
        e.status = enrollee_statuses.NEW
        e.consideration_stage = enrollee_statuses.STAGE_NEW

    elif all(without_original_need) and (not e.enrollment_consent or not e.original_or_copy):
        e.status = enrollee_statuses.WITHOUT_ORIGINAL
        e.consideration_stage = enrollee_statuses.STAGE_NEW

    elif all(need_data):
        e.status = enrollee_statuses.WITH_ORIGINAL
        e.consideration_stage = enrollee_statuses.STAGE_UNDER_OBSERVE
    else:
        e.status = enrollee_statuses.IN_PROCESS
        e.consideration_stage = enrollee_statuses.STAGE_NEW

    db.session.commit()


@blueprint.route("/client/add/enrolleeData/", methods=["POST"])
def add_enrollee_data():
    user_id = request.form.get("user_id")

    # personal info
    name = request.form.get("name")
    surname = request.form.get("surname")
    last_name = request.form.get("last_name")
    is_male = request.form.get("is_male")
    email = request.form.get("email")
    birthday = request.form.get("birthday")
    phone = request.form.get("phone")
    birth_place = request.form.get("birth_place")
    need_hostel = request.form.get("need_hostel")
    photo = request.files.get('photo')
    agreement_scan = request.files.get('agreement_scan')

    # passport
    passport_series = request.form.get("passport_series")
    passport_number = request.form.get("passport_number")
    who_issued = request.form.get("who_issued")
    when_issued = request.form.get("when_issued")
    department_code = request.form.get("department_code")
    passport_scan = request.files.get("passport_scan")
    registration_address = request.form.get("registration_address")

    # Education
    certificate_number = request.form.get("certificate_number")
    certificate_scan = request.files.get("certificate_scan")
    is_budgetary = request.form.get("is_budgetary")
    study_direction_id = request.form.get("study_direction_id")

    exams = request.form.get("exams")
    individual_achievements = request.form.get("individual_achievements")

    enrollment_consent = request.files.get("enrollment_consent")
    original_or_copy = request.form.get("original_or_copy")

    if not user_id:
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    if is_male:
        is_male = convert_bool_str_to_bool(is_male)

    if email:
        email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        pattern = re.compile(email_pattern)
        if not re.match(pattern, email):
            return make_response(EMAIL_INCORRECT, 400)

    user = User.query.filter_by(id=int(user_id)).first()
    if not user:
        print('user not found')
        return make_response(USER_NOT_FOUND, 401)

    try:
        # User model
        check_field_and_set("name", user, name)
        check_field_and_set("surname", user, surname)
        check_field_and_set("last_name", user, last_name)
        check_field_and_set("is_male", user, is_male)
        check_field_and_set("email", user, email)

        # Enrollee base info
        if user.enrollee == None:
            enrollee = Enrollee()
            db.session.add(enrollee)
            db.session.commit()
        else:
            enrollee = user.enrollee

        if need_hostel:
            need_hostel = convert_bool_str_to_bool(need_hostel)

        if is_budgetary:
            is_budgetary = convert_bool_str_to_bool(is_budgetary)

        if original_or_copy:
            original_or_copy = convert_bool_str_to_bool(original_or_copy)

        if birthday:
            birthday = convert_str_to_datetime(birthday)

        check_field_and_set("birthday", enrollee, birthday)
        check_field_and_set("phone", enrollee, phone)
        check_field_and_set("birth_place", enrollee, birth_place)
        check_field_and_set("need_hostel", enrollee, need_hostel)
        check_field_and_set("is_budgetary", enrollee, is_budgetary)
        check_field_and_set("original_or_copy", enrollee, original_or_copy)
        if photo:
            path = 'media/photos/' + str(user_id) + photo.filename
            a = photo.save(path)
            print(a, "photo was saved", path)
            check_field_and_set("photo", enrollee, path)

        if agreement_scan:
            path = 'media/agreement_scans/' + str(user_id) + agreement_scan.filename
            agreement_scan.save(path)
            check_field_and_set("agreement_scan", enrollee, path)

        if enrollment_consent:
            path = 'media/consents/' + str(user_id) + enrollment_consent.filename
            enrollment_consent.save(path)
            check_field_and_set("enrollment_consent", enrollee, path)

        if study_direction_id:
            direction = StudyDirection.query.filter_by(id=int(study_direction_id)).first()
            if not direction:
                return make_response(DIRECTION_NOT_FOUND, 400)

            enrollee.study_direction = direction

        if exams:
            exams = json.loads(exams)
            enrollee.exam_data_list = []
            for item in exams.get('items'):
                for sub_name, grade in item.items():
                    exam_info = ExamInfo(sub_name, int(grade))
                    db.session.add(exam_info)
                    enrollee.exam_data_list.append(exam_info)
                    db.session.commit()
        enrollee.user = user
        db.session.commit()
        user.enrollee = enrollee
        db.session.commit()

        # Passport
        if passport_series:
            passport_series = int(passport_series)

        if passport_number:
            passport_number = int(passport_number)

        if when_issued:
            when_issued = convert_str_to_datetime(when_issued)

        if department_code:
            department_code = int(department_code)

        if user.enrollee.passport == None:
            passport = Passport()
            db.session.add(passport)
            db.session.commit()
        else:
            passport = user.enrollee.passport

        check_field_and_set("series", passport, passport_series)
        check_field_and_set("number", passport, passport_number)
        check_field_and_set("who_issued", passport, who_issued)
        check_field_and_set("department_code", passport, department_code)
        check_field_and_set("when_issued", passport, when_issued)
        check_field_and_set("registration_address", passport, registration_address)
        if passport_scan:
            path = 'media/passports/' + str(user_id) + passport_scan.filename
            passport_scan.save(path)
            check_field_and_set("passport_scan", passport, path)

        user.enrollee.passport = passport
        db.session.commit()

        # School certificate
        if user.enrollee.school_certificate == None:
            school_certificate = SchoolCertificate()
            db.session.add(school_certificate)
            db.session.commit()
        else:
            school_certificate = user.enrollee.school_certificate

        if certificate_number:
            certificate_number = int(certificate_number)
        check_field_and_set("certificate_number", school_certificate, certificate_number)

        if certificate_scan:
            path = 'media/certificate_scans/' + str(user_id) + certificate_scan.filename
            certificate_scan.save(path)
            check_field_and_set("certificate_scan", school_certificate, path)

        user.enrollee.school_certificate = school_certificate
        db.session.commit()

        if individual_achievements:
            ach_indexes = json.loads(individual_achievements)['indexes']
            for i in ach_indexes:
                ach = IndividualAchievement.query.filter_by(id=i).first()
                if ach != None:
                    user.enrollee.individual_achievement_list.append(ach)
                    db.session.commit()

        update_enrollee_state(user.enrollee)

    except Exception as e:
        print(f"Register user error: {e}")
        return make_response(INTERNAL_ERROR, 500)

    return make_response(RESULT_SUCCESS, 200)


@blueprint.route("/client/login/", methods=["POST"])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not filling_all(email, password):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    # email as login and not enrollee
    user = User.query.filter_by(login=email).first()
    if user and user.account_type != account_types.ENROLL:
        if user.password == password:
            info = user.to_dict(rules=("-enrollee",))
            return make_response(json.dumps(info), 200)
        else:
            return make_response(FORM_INCORRECT, 401)

    user = db.session.query(User).filter(User.email == email).first()

    if user == None:
        print('user not found')
        return make_response(USER_NOT_FOUND, 401)

    if user.password == password:
        info = user.to_dict(rules=("-enrollee",))

        if user.account_type == account_types.ENROLL and user.enrollee:
            info.update(user.enrollee.to_dict())

        return make_response(json.dumps(info), 200)
    else:
        db.session.close()
        return make_response(FORM_INCORRECT, 401)


def send_mail(receiver, header, text):
    msg = MIMEText(text)
    msg['Subject'] = header
    msg['From'] = MAIL_LOGIN
    msg['To'] = receiver

    # Yandex mail
    server = smtp.SMTP_SSL('smtp.yandex.com', port=465)
    server.set_debuglevel(1)
    server.ehlo(MAIL_LOGIN)
    server.login(MAIL_LOGIN, MAIL_PASSWORD)
    server.auth_plain()
    print('sending...')
    server.sendmail(MAIL_LOGIN, [receiver], msg.as_string())
    server.quit()

    # Google mail
    # smtp_server = 'smtp.gmail.com'
    # s = smtp.SMTP(smtp_server)
    # s.starttls()
    # s.login(MAIL_LOGIN, MAIL_PASSWORD)
    # s.sendmail(MAIL_LOGIN, receiver, msg.as_string())
    # s.quit()
    print(f'mail to {receiver} sended')


@blueprint.route('/client/revision_form', methods=['POST'])
def enrollee_revision_form():
    enrollee_id = request.form.get('enrollee_id')
    incorrect_fields = request.form.getlist('incorrect_fields')
    print(incorrect_fields, enrollee_id)
    # incorrect_fields = json.loads(incorrect_fields).get('fields')
    # {asdadas: 123123, saddas: [] }
    if enrollee_id.isdigit():
        enrollee = Enrollee.query.filter_by(id=int(enrollee_id)).first()
        if enrollee:
            enrollee.consideration_stage = enrollee_statuses.STAGE_FOR_REVISION
            db.session.commit()
            user = enrollee.user
            new_line = '\n'
            send_mail(enrollee.user.email, 'СГУ им. Лимонадова',
                      f'Добрый день, {user.surname} {user.name} {user.last_name}!\n\n'
                      f'Уведомляем вас, что при подаче документов в '
                      f'Сызранский государственный университет имени Филиппа Лимонадова '
                      f'вы допустили ошибки.\n\n'
                      f'Просим исправить указанные поля в ближайшее время.\n'
                      f'  {new_line.join(incorrect_fields)}\n\n'
                      f'С уважением,\n'
                      f'приемная комиссия СГУ им. Ф.Лимонадова'
                      )

            return make_response(RESULT_SUCCESS, 200)
        else:
            return make_response(ENROLLEE_NOT_FOUND, 404)

    return make_response(FORM_INCORRECT, 400)


@blueprint.route('/client/confirm_form', methods=['POST'])
def enrollee_confirm_form():
    enrollee_id = request.form.get('enrollee_id')
    if enrollee_id.isdigit():
        enrollee = Enrollee.query.filter_by(id=int(enrollee_id)).first()
        if enrollee:
            enrollee.consideration_stage = enrollee_statuses.STAGE_RECEIVED
            db.session.commit()
            user = enrollee.user
            print('Trying to send mail...')
            send_mail(enrollee.user.email, 'СГУ им. Лимонадова',
                      f'Добрый день, {user.surname} {user.name} {user.last_name}!\n\n' + \
                      f'Уведомляем вас, что вы успешно подали документы в ' + \
                      f'Сызранский государственный университет имени Филиппа Лимонадова. ' + \
                      f'С этого момента вы участвуете в конкурсе на зачисление.\n\nС уважением,\n' + \
                      f'приемная комиссия СГУ им. Ф.Лимонадова.'
                      )
            return make_response(RESULT_SUCCESS, 200)
        else:
            return make_response(ENROLLEE_NOT_FOUND, 404)

    return make_response(FORM_INCORRECT, 400)


def enroll_student(enrollee: Enrollee, is_budget=False):
    enrollee.consideration_stage = enrollee_statuses.STAGE_RECEIVED
    db.session.commit()
    user = enrollee.user
    budget_text = 'бюджет' if is_budget else 'платно'
    send_mail(enrollee.user.email, 'СГУ им. Лимонадова',
              f'Добрый день, {user.surname} {user.name} {user.last_name}!\n\n ' + \
              f'Поздравляем!!!\n\n' + \
              f'Вы поступили в Сызранский государственный университет имени Филиппа Лимонадова.\n' + \
              f'Направление: {enrollee.study_direction.name}.\n' + \
              f'Форма: {budget_text}.\n\n' + \
              f'С уважением,\n' + \
              f'приемная комиссия СГУ им. Ф.Лимонадова'
              )


@blueprint.route('/client/enroll_users', methods=['POST'])
def enroll_users():
    # Формирование списков на зачисление
    need_original = request.form.get('need_original')
    direction_id = request.form.get('direction_id')
    direction = StudyDirection.query.filter_by(id=int(direction_id)).first()
    print(direction, "Для формирования документов о зачислении")
    if not direction:
        return make_response(FORM_INCORRECT, 400)

    # if need_original == None:
    #     pass
    # elif need_original.lower() == 'true':
    #     need_original = True
    # else:
    #     need_original = False
    need_original = True  # По критериям

    from sqlalchemy import and_
    enrolls = Enrollee.query.filter(
        and_(
            # прошедшие проверку
            Enrollee.consideration_stage == enrollee_statuses.STAGE_RECEIVED,
            Enrollee.study_direction_id == direction_id,
            (True if (need_original == None) else Enrollee.original_or_copy == need_original)
        )
    ).all()
    enrolls.sort(key=lambda x: x.get_exam_total_grade(), reverse=True)
    print('to table:', enrolls)
    i = 0
    enrolled_users = []
    # Зачислить бюджетников
    while i < direction.budget_count:
        if i < len(enrolls):
            enroll_student(enrolls[i], is_budget=True)
            enrolled_users.append(enrolls[i])
        print(i)
        i += 1

    # Зачислить платников
    for j in range(i, len(enrolls)):
        enroll_student(enrolls[j], is_budget=False)
        enrolled_users.append(enrolls[i])

    print('Generating report...')
    file_path = create_order_of_admission(f'media/commands/{slugify(direction.name)}', enrolled_users, direction)

    return make_response(json.dumps({'file_url': file_path}), 200)


@blueprint.route('/client/enroll', methods=['POST'])
def enroll_user():
    enrollee_id = request.form.get('enrollee_id')
    if enrollee_id.isdigit():
        enrollee = Enrollee.query.filter_by(id=int(enrollee_id)).first()
        if enrollee:
            enroll_student(enrollee, enrollee.is_budgetary)
            return make_response(RESULT_SUCCESS, 200)
        else:
            return make_response(ENROLLEE_NOT_FOUND, 404)

    return make_response(FORM_INCORRECT, 400)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

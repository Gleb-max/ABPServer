from config import MAIL_PASSWORD, MAIL_LOGIN
import smtplib as smtp
from email.mime.text import MIMEText

from data import enrollee_statuses
from data.db_session import db
from data.enrollee import Enrollee
from data.student import Student


def get_abbreviation(word_string):
    arr = word_string.split()
    arr = map(lambda x: x[0], arr)
    return (''.join(arr)).upper()


def send_mail(receiver, header, text):
    msg = MIMEText(text)
    msg['Subject'] = header
    msg['From'] = MAIL_LOGIN
    msg['To'] = receiver

    # Yandex mail
    # server = smtp.SMTP_SSL('smtp.yandex.com', port=465)
    # server.set_debuglevel(1)
    # server.ehlo(MAIL_LOGIN)
    # server.login(MAIL_LOGIN, MAIL_PASSWORD)
    # server.auth_plain()
    # print('sending...')
    # server.sendmail(MAIL_LOGIN, [receiver], msg.as_string())
    # server.quit()

    # Google mail
    smtp_server = 'smtp.gmail.com'
    s = smtp.SMTP(smtp_server)
    s.starttls()
    s.login(MAIL_LOGIN, MAIL_PASSWORD)
    s.sendmail(MAIL_LOGIN, receiver, msg.as_string())
    s.quit()
    print(f'mail to {receiver} sended')


def enroll_student(enrollee: Enrollee, is_budget=False):
    enrollee.consideration_stage = enrollee_statuses.STAGE_RECEIVED
    enrollee.is_budgetary = is_budget
    db.session.commit()
    user = enrollee.user

    student = Student()
    db.session.add(student)
    db.session.commit()

    student.user = user
    db.session.commit()

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


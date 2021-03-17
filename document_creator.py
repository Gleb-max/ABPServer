from typing import List

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
from data.enrollee import Enrollee
from data.study_direction import StudyDirection
from datetime import datetime


def create_order_of_admission(filename, enrolls: List[Enrollee], direction: StudyDirection, group_number):
    document = Document()

    upper = document.add_paragraph('Федеральное государственное бюджетное образовательное учреждение\n'
                                   'высшего образования\n'
                                   'Сызранский государственный университет имени Филиппа Лимонадова\n\n')
    upper.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    header = document.add_paragraph()
    header.add_run('Приказ').bold = True
    header.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(
        'На основании решения приемной комиссии зачислить на 1 курс очной формы обучения с 01.09.2021 г.\n\n')

    paragraph = document.add_paragraph(f'Факультет “{direction.faculty.name}”\n '
                                       f'Направление “{direction.name}”\n'
                                       f'Номер группы присвоить “{group_number}”\n')
    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = document.add_table(rows=len(enrolls) + 1, cols=4, style='Table Grid')
    table.cell(0, 0).text = '№'
    table.cell(0, 1).text = 'ФИО'
    table.cell(0, 2).text = 'Основа'
    table.cell(0, 3).text = 'Баллы'

    for row_num, enroll in enumerate(enrolls, 1):
        print(f'{enroll.user.name} was written to table')
        table.cell(row_num, 0).text = str(row_num)
        table.cell(row_num, 1).text = f'{enroll.user.name} {enroll.user.surname} {enroll.user.last_name}'
        table.cell(row_num, 2).text = 'бюджет' if enroll.is_budgetary else 'платная'
        table.cell(row_num, 3).text = str(enroll.get_total_grade)

    document.add_paragraph('\n\n\nРектор\t\t\t\t\t\t\t\t\t Иванов М.Ю.')

    full_file_name = f'{filename}.docx'.replace(' ', '_')
    document.save(full_file_name)
    return full_file_name

#
# enrolls = Enrollee.query.filter_by(birth_place='here').all()
# create_order_of_admission('test', enrolls, StudyDirection.query.first())

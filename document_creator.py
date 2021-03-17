from typing import List

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Inches, Cm
from data.enrollee import Enrollee
from data.study_direction import StudyDirection
from datetime import datetime

from data.user import User


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


def create_student_personal_profile(filename, user: User):
    document = Document()

    section = document.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    # crutch to rotate
    new_width, new_height = section.page_height, section.page_width
    section.page_width = new_width
    section.page_height = new_height
    print(section.orientation)

    upper = document.add_paragraph('Федеральное государственное бюджетное образовательное учреждение '
                                   'высшего образования\n'
                                   'Сызранский государственный университет имени Филиппа Лимонадова\n')
    upper.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    personal_debt = User.student.card_number

    delo = document.add_paragraph(f'Личное дело №')
    delo.add_run(f'{personal_debt}').underline = True
    delo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    big_line = '\t\t\t\t\t\t\t\t\t\t\t'
    small_line = '\t\t\t\t\t\t\t'
    par = document.add_paragraph()
    par.add_run('Факультет')
    par.add_run(big_line + '\n').underline = True
    par.add_run('Специальность')
    par.add_run(big_line[:-1] + '\n').underline = True
    par.add_run('Группа')
    par.add_run(small_line).underline = True

    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    header = document.add_paragraph('Учебная карточка студента\n(очная форма)')
    header.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


    tab = document.add_table(rows=1, cols=2)
    tab.autofit = False
    tab.allow_autofit = False
    line_len = 108
    # par = document.add_paragraph()
    cur_cell = tab.cell(0, 0)
    cur_cell.width = Inches(6.5)
    par = cur_cell.add_paragraph()
    par.add_run('Основа')
    par.add_run(small_line).underline = True
    par.add_run(', личное дело №')
    par.add_run(f'{personal_debt}\n').underline = True
    par.add_run('ФИО')
    fio = f'{user.name} {user.surname} {user.last_name}'
    par.add_run(fio + (line_len - len('ФИО') - len(fio))//10 * '\t' + '\n').underline = True
    par.add_run('Дата рождения')
    par.add_run((line_len - len('Дата рождения') - len(''))//10 * '\t' + '\n').underline = True
    par.add_run('Место рождения')
    par.add_run((line_len - len('Место рождения') - len(''))//10 * '\t' + '\n').underline = True
    par.add_run('Паспорт')
    par.add_run('1212 646464').underline = True
    par.add_run(' выдан')
    par.add_run((line_len - len('Паспортвыдан1212646464'))//10 * '\t' + '\n').underline = True

    small_line_len = 70
    par.add_run('\n\nКонтакты\n').bold = True
    par.add_run('Телефон')
    par.add_run((small_line_len - len('Телефон') - len(''))//10 * '\t' + '\n').underline = True
    par.add_run('E-mail')
    par.add_run((small_line_len - len('E-mail') - len(''))//10 * '\t' + '\n').underline = True
    par.add_run('Адрес по прописке')
    par.add_run((line_len - len('Адрес по прописке') - len(''))//10 * '\t' + '\n').underline = True
    par.add_run((line_len - len(''))//10 * '\t' + '\n').underline = True
    par.add_run((line_len - len(''))//10 * '\t' + '\n').underline = True

    with open('test_img.jpg', 'rb') as img:
        cur_cell = tab.cell(0, 1)
        paragraph = cur_cell.paragraphs[0]
        run = paragraph.add_run()
        picture = run.add_picture(img, width=Inches(2.3), height=Inches(3))
        cur_cell.width = Cm(10)

    document.save(f'{filename}.docx')

# user = User.query.first()
# create_student_personal_profile('test', user)
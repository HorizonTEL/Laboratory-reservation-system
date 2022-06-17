from models.model import *


class Student(db.Model):
    __tablename__ = "student"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    student_id = db.Column(db.String(64), primary_key=True)
    student_name = db.Column(db.String(256), nullable=False)
    student_password = db.Column(db.String(256), nullable=False)
    student_phone = db.Column(db.String(32), nullable=False)
    if_admin = db.Column(db.Boolean, default=False)


def initial_stu():
    students = [
        Student(student_id='202083290327', student_name='yjz', student_password='123456', student_phone='15305171970'),
        Student(student_id='202083290333', student_name='ljl', student_password='135790', student_phone='13037302381'),
        Student(student_id='202083290447', student_name='lrq', student_password='234572', student_phone='13749274203')
    ]
    db.session.add_all(students)

    admin = Student(student_id='admin', student_name='admin', student_password='admin', student_phone='', if_admin=True)
    db.session.add(admin)
    db.session.commit()
    db.session.commit()


def valid_login(student_id, password):
    student = Student.query.filter(Student.student_id == student_id).first()
    if student:
        if student.student_password == password:
            if student.if_admin:
                return 2
            return 1
    return 0


def stu_exist(student_id):
    student = Student.query.filter(Student.student_id == student_id).first()
    if student:
        return True
    return False


def change_password(student_id, password):
    student = Student.query.filter(Student.student_id == student_id).first()
    student.student_password = password
    db.session.commit()


def show_all_stu():
    students = Student.query.filter(Student.if_admin == False).all()
    re = []
    for student in students:
        re.append([student.student_id, student.student_name])
    return re

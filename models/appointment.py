from models.seat import *
from utils import *


class Appointment(db.Model):
    __tablename__ = "appointment"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    if_sign = db.Column(db.Boolean, default=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    laboratory_id = db.Column(db.Integer, db.ForeignKey('laboratory.laboratory_id'))
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.seat_id'))
    student_id = db.Column(db.String(64), db.ForeignKey('student.student_id'))
    '''
    laboratory = db.relationship('Laboratory', backref='appointments')  # 反向查询
    student = db.relationship('Laboratory', backref='appointments')  # 反向查询
    seat = db.relationship('Laboratory', backref='appointments')  # 反向查询
    '''


def initial_appointment():
    appointment = Appointment(appointment_time=getNowDataTime(), laboratory_id=9, seat_id=80, student_id='202083290447')
    db.session.add(appointment)
    db.session.commit()

    change_seat(9, 80, True)


def appointment_detail(student_id, name):
    laboratories_id = db.session.query(Laboratory.laboratory_id).filter(Laboratory.laboratory_name.like("%" + name+"%")).all()
    # print(laboratories_id)
    re = []
    for laboratory_id in laboratories_id:
        laboratory = Laboratory.query.filter(Laboratory.laboratory_id == laboratory_id[0]).first()
        appo = Appointment.query.filter(Appointment.student_id == student_id, Appointment.laboratory_id == laboratory_id[0]).first()
        if appo:
            if appo.if_sign:
                re.append([laboratory.laboratory_id, laboratory.laboratory_name, laboratory.laboratory_loc, laboratory.laboratory_left, 2])    # 已有预约且已经签到
            else:
                re.append([laboratory.laboratory_id, laboratory.laboratory_name, laboratory.laboratory_loc, laboratory.laboratory_left, 1])  # 已有预约
        else:
            re.append([laboratory.laboratory_id, laboratory.laboratory_name, laboratory.laboratory_loc, laboratory.laboratory_left, 0])  # 没有预约
    return re


def set_appointment(student_id, laboratory_id):
    appointment = Appointment.query.filter(Appointment.student_id == student_id, Appointment.laboratory_id == laboratory_id).first()
    if appointment:
        # 取消预约
        change_seat(laboratory_id, appointment.seat_id, False)
        db.session.delete(appointment)
    else:
        seat = Seat.query.filter(Seat.laboratory_id == laboratory_id, Seat.if_appointment == False).first()
        print(seat)
        print(laboratory_id)
        db.session.add(Appointment(appointment_time=getNowDataTime(),  laboratory_id=laboratory_id, seat_id=seat.seat_id, student_id=student_id))
        change_seat(laboratory_id, seat.seat_id, True)
    db.session.commit()


def mine_appoint(student_id):
    appointments = Appointment.query.filter(Appointment.student_id == student_id).all()
    re = []
    for appointment in appointments:
        laboratory = Laboratory.query.filter(Laboratory.laboratory_id == appointment.laboratory_id).first()
        re.append([appointment.appointment_id, laboratory.laboratory_name, laboratory.laboratory_loc, appointment.seat_id, appointment.appointment_time, appointment.if_sign])
    return re


def show_stu_detail(student_id):
    appointments = Appointment.query.filter(Appointment.student_id == student_id).all()
    re = []
    for appointment in appointments:
        laboratory = Laboratory.query.filter(Laboratory.laboratory_id == appointment.laboratory_id).first()
        re.append([appointment.appointment_id, laboratory.laboratory_name, laboratory.laboratory_loc, appointment.seat_id, appointment.appointment_time, appointment.if_sign])
    return re

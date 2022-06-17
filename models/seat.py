from models.laboratory import *


class Seat(db.Model):
    __tablename__ = "seat"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    seat_id = db.Column(db.Integer, primary_key=True)
    if_appointment = db.Column(db.Boolean, default=False)
    laboratory_id = db.Column(db.Integer, db.ForeignKey('laboratory.laboratory_id'))
    '''
    laboratory = db.relationship('Laboratory', backref='seats')  # 反向查询
    '''


def initial_seat():
    seats = []
    for i in range(1, 13):
        for j in range(40):
            seats.append(Seat(laboratory_id=i))

    db.session.add_all(seats)
    db.session.commit()


def change_seat(laboratory_id, seat_id, if_appointment):
    change_left(laboratory_id, if_appointment)
    seat = db.session.query(Seat).filter_by(seat_id=seat_id).first()
    seat.if_appointment = if_appointment
    db.session.commit()

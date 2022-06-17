from models.model import *


class Laboratory(db.Model):
    __tablename__ = "laboratory"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    laboratory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    laboratory_loc = db.Column(db.String(64), nullable=False)
    laboratory_name = db.Column(db.String(32), nullable=False)
    laboratory_left = db.Column(db.Integer, default=40)


def initial_lab():
    laboratories = [
        Laboratory(laboratory_loc='中美中心', laboratory_name='生物实验室1'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='生物实验室2'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='生物实验室3'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='化学实验室1'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='化学实验室2'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='化学实验室3'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='物理实验室1'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='物理实验室2'),
        Laboratory(laboratory_loc='中美中心', laboratory_name='物理实验室3'),
        Laboratory(laboratory_loc='长望楼', laboratory_name='机房1'),
        Laboratory(laboratory_loc='长望楼', laboratory_name='机房2'),
        Laboratory(laboratory_loc='长望楼', laboratory_name='机房3')
    ]
    db.session.add_all(laboratories)

    db.session.commit()


def change_left(laboratory_id, if_appointment):
    laboratory = db.session.query(Laboratory).filter_by(laboratory_id=laboratory_id).first()
    if if_appointment:
        if laboratory.laboratory_left == 0:
            return False
        laboratory.laboratory_left -= 1
    else:
        laboratory.laboratory_left += 1

    db.session.commit()


def show_all_lab(name):
    left_all = db.session.query(Laboratory.laboratory_left).filter(Laboratory.laboratory_name.like(name+"%")).all()
    numbers = 0
    for i in left_all:
        numbers += i[0]
    # print(numbers)
    return numbers


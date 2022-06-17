from flask import Flask
from flask import request
import flask
from settings import *
from models.student import *
from models.appointment import *


app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
            )
app.config.from_object(MySQLConfig)


# @app.before_first_request
def create_db():
    db.drop_all()  # 每次运行，先删除再创建
    db.create_all()
    initial_stu()
    initial_lab()
    initial_seat()
    initial_appointment()


with app.app_context():
    db.init_app(app)
    create_db()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        password = request.form.get('password')
        # print(user_id)
        # print(password)
        '''
        此处得添加一些防火墙
        '''
        if valid_login(user_id, password) == 2:
            response = flask.redirect('admin_stu')
            response.delete_cookie("user_id")
            response.set_cookie('admin_id', user_id)
            response.set_cookie('password', password)
            return response
        elif valid_login(user_id, password) == 1:
            response = flask.redirect('index')
            response.set_cookie('user_id', user_id)
            response.set_cookie('password', password)
            return response
        else:
            return flask.render_template('login.html', wrong='用户名或密码错误')
    elif request.method == 'GET':
        return flask.render_template('login.html')


@app.route('/logout')
def logout():
    response = flask.redirect('login')
    response.delete_cookie("user_id")
    response.delete_cookie("admin_id")
    response.delete_cookie("password")
    return response


@app.route('/index')
def index():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        numbers = [show_all_lab('生物实验室'), show_all_lab('化学实验室'), show_all_lab('物理实验室'), show_all_lab('机房')]
        return flask.render_template('index.html', user_id=user_id, numbers=numbers)
    else:
        return flask.redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        _id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        password_true = request.form.get('password_true')
        # print(password)
        # print(password_true)
        phone_number = request.form.get('phone')
        if _id == "" or name == "" or password == "" or phone_number == "":
            return flask.render_template('register.html', wrong="请将个人信息全部填写")
        if password != password_true:
            return flask.render_template('register.html', wrong="请保证两次输入的密码一致")
        if stu_exist(_id):
            return flask.render_template('register.html', wrong="账号已注册")
        stu = Student(student_id=_id, student_name=name, student_password=password, student_phone=phone_number)
        db.session.add(stu)
        db.session.commit()
        return flask.redirect('login')
    elif request.method == 'GET':
        return flask.render_template('register.html')


@app.route('/appoint', methods=['POST', 'GET'])
def appoint():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            laboratory = request.form.get('appointment')   # 实验室大类名称
            # print(appointment)
        elif request.method == "GET":
            laboratory = request.cookies.get('laboratory')
        return flask.render_template('appoint.html', name=laboratory, appoint_detail=appointment_detail(user_id, laboratory))

    else:
        return flask.redirect('login')


@app.route('/appointment', methods=['POST'])
def appointment():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            response = flask.redirect('appoint')
            laboratory_id = request.form.get('appoint')   # 实验室id
            laboratory = Laboratory.query.filter(Laboratory.laboratory_id == laboratory_id).first()
            response.set_cookie('laboratory', laboratory.laboratory_name[:-1])
            set_appointment(user_id, laboratory_id)
            return response
    else:
        return flask.redirect('login')


@app.route('/search', methods=['GET', 'POST'])
def search():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            sea = request.form.get('sea')
        else:
            sea = ""
        return flask.render_template('search.html', appointments=appointment_detail(user_id, sea))
    else:
        return flask.redirect('login')


@app.route('/search_appoint', methods=['POST'])
def search_appoint():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            laboratory_id = request.form.get('laboratory_id')  # 实验室id
            set_appointment(user_id, laboratory_id)
            return flask.redirect('search')
    else:
        return flask.redirect('login')


@app.route('/mine',  methods=['GET', 'POST'])
def mine():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        student = Student.query.filter(Student.student_id == user_id).first()
        wrong = ""
        if request.method == "POST":
            response = flask.redirect('login')
            old_password = request.form.get('old_password')
            print(old_password)
            new_password = request.form.get('new_password')
            sure_password = request.form.get('sure_password')
            if new_password == "":
                wrong = "密码不能为空"
            elif old_password == password and new_password == sure_password:
                response.set_cookie('password', new_password)
                change_password(user_id, new_password)
                return response
            elif new_password != sure_password:
                wrong = "请确保两次输入的密码一致"
            elif old_password != password:
                wrong = "原密码输入错误"
        return flask.render_template('mine.html', user_id=user_id, username=student.student_name, mine_appointment=mine_appoint(user_id), wrong=wrong)
    else:
        return flask.redirect('login')


@app.route('/sign',  methods=['POST'])
def sign():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            appointment_id = request.form.get('mine_sign')
            appointment = Appointment.query.filter(Appointment.appointment_id == appointment_id).first()
            appointment.if_sign = True
            db.session.commit()
            return flask.redirect('mine')
    else:
        return flask.redirect('login')


@app.route('/regulation',  methods=['GET'])
def regulation():
    user_id = request.cookies.get('user_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "GET":
            return flask.render_template('regulation.html')
    else:
        return flask.redirect('login')


@app.route('/admin_stu',  methods=['GET'])
def admin_stu():
    user_id = request.cookies.get('admin_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "GET":
            return flask.render_template('admin_app_stu.html', students=show_all_stu())
    else:
        return flask.redirect('login')


@app.route('/student_detail',  methods=['POST'])
def student_detail():
    user_id = request.cookies.get('admin_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            student_id = request.form.get('stu_de')
            return flask.render_template('stuinfo.html', students=show_stu_detail(student_id))
    else:
        return flask.redirect('login')


@app.route('/admin_del',  methods=['POST'])
def admin_del():
    user_id = request.cookies.get('admin_id')
    password = request.cookies.get('password')
    if valid_login(user_id, password):
        if request.method == "POST":
            response = flask.redirect('admin_stu')
            appoint_id = request.form.get('appoint_id')  # 预约id
            appointment = Appointment.query.filter(Appointment.appointment_id == appoint_id).first()
            set_appointment(appointment.student_id, appointment.laboratory_id)
            return response
    else:
        return flask.redirect('login')


if __name__ == '__main__':
    app.run()

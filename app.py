from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.user_form import BuildingForm, UsersForm, LessonForm, BuildingForm1, UsersForm1, LessonForm1, NeuronForm, \
    FloorForm, FloorForm1
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer, MaxAbsScaler
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly
import json
from math import fabs

import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/test2'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://ahxvfvvoydcbjj:5fc3a7c4a195cfa9cd767df048db74305dbeb5970880e3570319128f6ab19fab@ec2-174-129-33-107.compute-1.amazonaws.com:5432/d91cnp1pfnluo0'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormBuilding(db.Model):
    __tablename__ = 'Building'

    build_number = db.Column(db.String(50), primary_key=True)
    build_address = db.Column(db.String(50), nullable=False)

    Lesson_ = db.relationship('ormLesson')
    Floor_ = db.relationship('ormFloor')


class ormFloor(db.Model):
    __tablename__ = 'Floor'

    floors_number = db.Column(db.String(50), primary_key=True)
    build_number = db.Column(db.String(50), db.ForeignKey('Building.build_number'), nullable=True)
    floor_type = db.Column(db.String(50), nullable=False)
    floor_status = db.Column(db.String(50), nullable=False)

    Lesson_ = db.relationship('ormLesson')


class ormUsers(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), nullable=False)
    user_surname = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(30), nullable=False)
    user_groupe = db.Column(db.String(40), nullable=False)
    user_faculty = db.Column(db.String(40), nullable=False)
    user_course = db.Column(db.Integer, nullable=False)
    # lesson_name = db.Column(db.String(20), db.ForeignKey('Lesson.lesson_name'))

    lesson_id = db.relationship('ormLesson', secondary='user_has_lesson')


class ormLesson(db.Model):
    __tablename__ = 'Lesson'

    lesson_id = db.Column(db.Integer, primary_key=True)
    build_number = db.Column(db.String(50), db.ForeignKey('Building.build_number'), nullable=True)
    lesson_name = db.Column(db.String(20), nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)
    teacher = db.Column(db.String(20), nullable=False)
    floors_number = db.Column(db.String(50), db.ForeignKey('Floor.floors_number'), nullable=True)

    user_id = db.relationship('ormUsers', secondary='user_has_lesson')


class userHasLesson(db.Model):
    __tablename__ = 'user_has_lesson'

    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('Lesson.lesson_id'), primary_key=True)

# db.session.query(ormUsers).delete()
# db.session.query(ormLesson).delete()
# db.session.query(ormFloor).delete()
# db.session.query(ormBuilding).delete()
# db.session.commit()
# db.session.query(userHasLesson).delete()

db.create_all()



# User1 = ormUsers(user_id = 1, user_name ='Andriy', user_surname ='Hladkiy', user_email ='andriyha98@gmail.com', user_groupe ='KM-63', user_faculty ='FMA', user_course =3)
# User2 = ormUsers(user_id = 2, user_name ='Ihor', user_surname ='Riasik', user_email ='riasik99@gmail.com', user_groupe ='KM-63', user_faculty ='FMA', user_course =4)
# User3 = ormUsers(user_id = 3, user_name ='Alex', user_surname ='Buc', user_email ='buc99@gmail.com', user_groupe ='KM-63', user_faculty ='FMA', user_course =4)
# Building1 =ormBuilding(build_number = '14', build_address='politehnichna 14')
# Building2 =ormBuilding(build_number = '7', build_address='politehnichna 21')
# Building3 =ormBuilding(build_number = '15', build_address='politehnichna 16')
# Lesson1 = ormLesson(lesson_id = '1', build_number = '14', lesson_name = 'matan', lesson_number = '1', teacher = 'teacher1', floors_number = '95')
# Lesson2 = ormLesson(lesson_id = '2', build_number = '7', lesson_name = 'db', lesson_number = '3', teacher = 'teacher1',floors_number = '72')
# Lesson3 = ormLesson(lesson_id = '3', build_number = '14', lesson_name = 'ekonomika', lesson_number = '4', teacher = 'teacher1', floors_number = '302')
# Floor1 = ormFloor(floors_number = '95', build_number = '14', floor_type = 'Lection', floor_status = 'Occupied')
# Floor2 = ormFloor(floors_number = '72', build_number = '7', floor_type = 'Practise', floor_status = 'Occupied')
# Floor3 = ormFloor(floors_number = '302', build_number = '14', floor_type = 'Lection', floor_status = 'Occupied')
# 
# # Lesson1.Users__.append(User1)
# # Lesson1.Users__.append(User3)
# # Lesson1.Users__.append(User2)
# # Building3.Lesson_.append(Lesson1)
# # Building1.Lesson_.append(Lesson2)
# # Building2.Lesson_.append(Lesson3)
# db.session.add_all([User1,User2,User3])
# db.session.add_all([Building1,Building2,Building3])
# db.session.add_all([Lesson1,Lesson2,Lesson3])
# db.session.add_all([Floor1,Floor2,Floor3])
# db.session.commit()


# main page
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


# user pages
@app.route('/user', methods=['GET'])
def users():
    result = db.session.query(ormUsers).all()

    return render_template('users.html', users=result)


@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    form = UsersForm()

    if request.method == 'POST':
        if form.validate() == True:
            ok = ormUsers(
                user_id=form.user_id.data,
                user_name=form.user_name.data,
                user_surname=form.user_surname.data,
                user_email=form.user_email.data,
                user_groupe=form.user_groupe.data,
                user_faculty=form.user_faculty.data,
                user_course=form.user_course.data
            )

            try:
                db.session.add(ok)
                db.session.commit()
                return redirect('/user')
            except:
                form.user_id.errors = ['This name already exists!']
                return render_template('user_form.html', form=form, form_name="user form")

            return redirect(url_for('users'))
        else:

            return render_template('ok.html', form=form, form_name="ok")

    elif request.method == 'GET':
        return render_template('user_form.html', form=form, form_name="user form")


@app.route('/edit_user/<string:x>', methods=['GET', 'POST'])
def edit_user(x):
    form = UsersForm1()
    user = db.session.query(ormUsers).filter(ormUsers.user_id == x).one()

    if request.method == 'GET':

        # fill form and send to user
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.user_surname.data = user.user_surname
        form.user_email.data = user.user_email
        form.user_groupe.data = user.user_groupe
        form.user_faculty.data = user.user_faculty
        form.user_course.data = user.user_course

        return render_template('user_form1.html', form=form, form_name="Edit user")

    else:

        if form.validate() == True:
            user.user_name = form.user_name.data
            user.user_surname = form.user_surname.data
            user.user_email = form.user_email.data
            user.user_groupe = form.user_groupe.data
            user.user_faculty = form.user_faculty.data
            user.user_course = form.user_course.data

            db.session.commit()

            # return redirect('/user')
            return render_template('OK.html')
        else:
            return render_template('user_form1.html', form=form, form_name="Edit user")


@app.route('/delete_user/<string:x>', methods=['GET'])
def delete_user(x):
    result = db.session.query(ormUsers).filter(ormUsers.user_id == x).one()
    db.session.delete(result)
    db.session.commit()

    return render_template('OK.html')


# Building
@app.route('/building', methods=['GET'])
def building():
    result = db.session.query(ormBuilding).all()

    return render_template('building.html', building=result)


@app.route('/new_building', methods=['GET', 'POST'])
def new_building():
    form = BuildingForm()

    if request.method == 'POST':
        if form.validate() == True:
            ok = ormBuilding(
                build_number=form.build_number.data,
                build_address=form.build_address.data,

            )
            try:
                db.session.add(ok)
                db.session.commit()
                return redirect('/building')
            except:
                form.build_number.errors = ['This name already exists!']
                return render_template('building_form.html', form=form, form_name="building form")

            # return redirect(url_for('building'))

        else:
            return render_template('building_form.html', form=form, form_name="building form")

    elif request.method == 'GET':

        return render_template('building_form.html', form=form, form_name="building form")


@app.route('/edit_building/<string:x>', methods=['GET', 'POST'])
def edit_building(x):
    form = BuildingForm1()

    user = db.session.query(ormBuilding).filter(ormBuilding.build_number == x).one()

    if request.method == 'GET':

        form.build_address.data = user.build_address

        return render_template('building_form1.html', form=form, form_name="Edit building")


    else:

        if form.validate() == True:
            # find user

            # update fields from form data
            user.build_address = form.build_address.data

            db.session.commit()

            return redirect(url_for('building'))


        else:

            return render_template('building_form1.html', form=form, form_name="Edit building")


@app.route('/delete_building/<string:x>', methods=['GET'])
def delete_building(x):
    result = db.session.query(ormBuilding).filter(ormBuilding.build_number == x).one()
    result1 = db.session.query(ormFloor).filter(ormFloor.build_number == x).all()

    result2 = db.session.query(ormLesson).filter(ormLesson.build_number == x).all()
    for i in result1:
        db.session.delete(i)

    for i in result2:
        db.session.delete(i)


    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')

    # result = db.session.query(ormBuilding).filter(ormBuilding.build_number == x).one()

    # db.session.delete(result)
    # db.session.commit()

    # return render_template('OK.html')


# lessons pages
@app.route('/lesson', methods=['GET'])
def lesson():
    result = db.session.query(ormLesson).all()

    return render_template('lessons.html', lesson=result)


@app.route('/new_lesson', methods=['GET', 'POST'])
def new_lesson():
    form = LessonForm()

    if request.method == 'POST':
        if form.validate() == True:
            ok = ormLesson(
                lesson_id=form.lesson_id.data,
                build_number=form.build_number.data,
                lesson_name=form.lesson_name.data,
                lesson_number=form.lesson_number.data,
                teacher=form.teacher.data,
                floors_number=form.floors_number.data,

            )

            try:
                db.session.add(ok)
                db.session.commit()
                return redirect('/lesson')
            except:
                form.lesson_name.errors = ['This name already exists!']
                return render_template('lessons_form.html', form=form, form_name="New lesson", action="new_lesson")

            # return redirect(url_for('lesson'))


        else:
            return render_template('lessons_form.html', form=form, form_name="New lesson", action="new_lesson")

    return render_template('lessons_form.html', form=form, form_name="New lesson", action="new_lesson")


@app.route('/edit_lesson/<string:x>', methods=['GET', 'POST'])
def edit_lesson(x):
    form = LessonForm1()
    user = db.session.query(ormLesson).filter(ormLesson.lesson_id == x).one()

    if request.method == 'GET':

        # fill form and send to user
        form.lesson_id.data = user.lesson_name
        form.build_number.data = user.build_number
        form.lesson_name.data = user.lesson_name
        form.lesson_number.data = user.lesson_number
        form.teacher.data = user.teacher
        form.floors_number.data = user.floors_number

        return render_template('lessons_form1.html', form=form, form_name="Edit lesson")


    elif request.method == 'POST':

        if form.validate() == False:
            # update fields from form data
            form.build_number.data = user.build_number
            form.lesson_name.data = user.lesson_name
            form.lesson_number.data = user.lesson_number
            form.teacher.data = user.teacher
            form.floors_number.data = user.floors_number

            db.session.commit()

            return render_template('ok.html')


        else:
            return render_template('lessons_form1.html', form=form, form_name="Edit lesson")


@app.route('/delete_lesson/<string:x>', methods=['GET'])
def delete_lesson(x):
    result = db.session.query(ormLesson).filter(ormLesson.lesson_id == x).one()



    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


@app.route('/floor', methods=['GET'])
def Floor():
    result = db.session.query(ormFloor).all()

    return render_template('floor.html', floor=result)


@app.route('/new_floor', methods=['POST', 'GET'])
def new_floor():
    form = FloorForm()

    if request.method == 'POST':
        if form.validate() == True:
            ok = ormFloor(
                floors_number=form.floors_number.data,
                build_number=form.build_number.data,
                floor_type=form.floor_type.data,
                floor_status=form.floor_status.data,
            )

            try:
                db.session.add(ok)
                db.session.commit()
                return redirect('/floor')
            except:
                form.floors_number.errors = ['This name already exists!']
                return render_template('floor_form.html', form=form, form_name="floor form")

            return redirect(url_for('floor'))
        else:

            return render_template('ok.html', form=form, form_name="ok")

    elif request.method == 'GET':
        return render_template('floor_form.html', form=form, form_name="floor form")


@app.route('/edit_floor/<string:x>', methods=['GET', 'POST'])
def edit_floor(x):
    form = FloorForm1()
    user = db.session.query(ormFloor).filter(ormFloor.floors_number == x).one()

    if request.method == 'GET':

        # fill form and send to user
        form.floors_number.data = user.floors_number
        form.build_number.data = user.build_number
        form.floor_type.data = user.floor_type
        form.floor_status.data = user.floor_status

        return render_template('floor_form1.html', form=form, form_name="Edit floor")

    else:

        if form.validate() == False:
            user.build_number = form.build_number.data
            user.floor_type = form.floor_type.data
            user.floor_status = form.floor_status.data

            db.session.commit()

            # return redirect('/user')
            return render_template('OK.html')
        else:
            return render_template('floor_form1.html', form=form, form_name="Edit floor")


@app.route('/delete_floor/<string:x>', methods=['GET'])
def delete_floor(x):
    result = db.session.query(ormFloor).filter(ormFloor.floors_number == x).one()
    result1 = db.session.query(ormLesson).filter(ormLesson.floors_number == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)



    db.session.commit()

    return render_template('OK.html')


@app.route('/NeuralForm', methods=['GET', 'POST'])
def NeuralForm():
    form = NeuronForm()

    #Sample = db.session.query(ormUsers).join(ormLesson)

    # Sample = db.session.query(ormUsers).join(ormLesson).filter(ormLesson.lesson_number == 4)
    # for row in Sample:
    #     for inv in row.invoices:
    #         print(row.id, row.name, inv.invno, inv.amount)



    Sample = db.session.query(ormUsers).all()
    X = []
    y = []
    for i in Sample:
        X.append([i.user_groupe, i.user_faculty])
        y.append(i.user_course)

    Coder1 = ColumnTransformer(transformers=[('code1', OneHotEncoder(), [0,1])])

    Coder2 = MaxAbsScaler()

    Model = MLPClassifier(hidden_layer_sizes=(5, 4))

    Model = Pipeline(steps=[('code1', Coder1), ('code2', Coder2), ('neur', Model)])
    Model.fit(X, y)

    if request.method == 'POST':
        if form.validate() == True:
            return render_template('AI_form.html', form=form)

        new_user = [
            [form.user_groupe.data, form.user_faculty.data]]
        y_ = Model.predict(new_user)
        # print(y_)
        return render_template('oko.html', result=y_[0])
    elif request.method == 'GET':
        return render_template('AI_form.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            ormUsers.user_faculty,
            func.count(ormUsers.user_id).label('faculty')
        ).
            group_by(ormUsers.user_faculty)
    ).all()

    query2 = (
        db.session.query(
            ormUsers.user_groupe,
            func.avg(ormUsers.user_id).label('lesson_name')
        ).
            group_by(ormUsers.user_groupe)
    ).all()

    names, skill_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )

    skills, user_count = zip(*query2)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )

    names, skill_counts = zip(*query1)
    scat = go.Scatter(
        x=names,
        y=skill_counts,
        mode='markers'
    )

    data = {
        "bar": [bar],
        "pie": [pie],
        "scat": [scat]
    }

    x = []
    y = []

    query_for_cor = db.session.query(
            ormUsers.user_course,
            func.count(ormUsers.user_id).label('lesson_name')
        ).group_by(ormUsers.user_course).all()
    print(query_for_cor)
    for i in query_for_cor:
        x.append(int(i[0]))
        y.append(i[1])
    corr_coef = np.corrcoef(x, y)[0][1]

    massage = None

    if fabs(corr_coef) < 0.33:
        massage = 'weak dependence'
    else:
        massage = 'perceptible dependence'

    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON,corr_coef =corr_coef, massage = massage)


@app.route('/dash', methods=['GET', 'POST'])
def dash():
    query1 = (
        db.session.query(
            ormUsers.user_faculty,
            func.count(ormUsers.user_id).label('faculty')
        ).
            group_by(ormUsers.user_faculty)
    ).all()

    names, skill_counts = zip(*query1)
    bar = go.Scatter(
        x=names,
        y=skill_counts,
        mode='lines+markers',
        name='lines+markers'

    )

    data = [bar]

    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dash.html', graphsJSON=graphsJSON,corr_coef =corr_coef, massage = massage)


#     =================================================================================================

if __name__ == '__main__':
    app.run(debug=True)

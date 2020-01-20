from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, ValidationError
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange, Length, Email


def valid_status(form, field):
    if (field.data) not in ['Free','Occupied']:
        raise ValidationError("input Free or Occupied")

def valid_type(form, field):
    if (field.data) not in ['Lection','Practise']:
        raise ValidationError("input Lection or Practise")


def valid_minus(form, field):
    if int(field.data) < 0:
        raise ValidationError("more 0")

def valid_user_course(form, field):
    if 0 < int(field.data) < 6:
        raise ValidationError("more 0")

def valid_lesson_number(form, field):
    if 0 < int(field.data) > 6:
        raise ValidationError("more 0")

class BuildingForm(Form):
    build_number = StringField("build number: ", [valid_minus,
        validators.DataRequired("Please enter build number."),
        validators.Length(1, 20, "Name should be from 5 to 20 symbols")
    ])

    build_address = StringField("build adress: ", [
        validators.DataRequired("Please enter build adress."),
        validators.Length(1, 20, "Name should be from 5 to 20 symbols")
    ])

    submit = SubmitField("Save")


class BuildingForm1(Form):
    # build_number = StringField("build number: ", [
    #     validators.DataRequired("Please enter build number."),
    #     validators.Length(1, 20, "Name should be from 5 to 20 symbols")
    # ])

    build_address = StringField("build adress: ", [
        validators.DataRequired("Please enter build adress."),
        validators.Length(1, 20, "Name should be from 5 to 20 symbols")
    ])

    submit = SubmitField("Save")


class UsersForm(Form):
    user_id = IntegerField("user id: ", [valid_minus,
                                         validators.DataRequired("Please enter user id.")
                                         ])

    user_name = StringField("user name: ", [
        validators.DataRequired("Please enter user name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    user_surname = StringField("user surname: ", [
        validators.DataRequired("Please enter user surname."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")])

    user_email = StringField("user email: ", [
        validators.Email("Please enter user_email."),
        validators.Length(1, 40, "Name should be from 5 to 40 symbols")])

    user_groupe = StringField("user groupe: ", [
        validators.DataRequired("Please enter your user_groupe."),
        validators.Length(1, 30, "Name should be from 10 to 30 symbols")])

    user_faculty = StringField("user faculty: ", [
        validators.DataRequired("Please enter user faculty.")])

    user_course = IntegerField("user course: ", [valid_user_course,
        validators.DataRequired("Please enter user course."),
        validators.Length(1, 40, "Name should be from 10 to 40 symbols")
    ])

    # lesson_name = StringField("lesson name: ", [
    #     validators.DataRequired("Please enter lesson name."),
    #     validators.Length(1, 40, "Name should be from 10 to 40 symbols")
    # ])

    submit = SubmitField("Save")


class UsersForm1(Form):
    user_id = IntegerField("user id: ", [valid_minus,
        validators.DataRequired("Please enter user id.")
    ])

    user_name = StringField("user name: ", [
        validators.DataRequired("Please enter user name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    user_surname = StringField("user surname: ", [
        validators.DataRequired("Please enter user surname."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")])

    user_email = StringField("user email: ", [
        validators.Email("Please enter user_email."),
        validators.Length(1, 40, "Name should be from 5 to 40 symbols")])

    user_groupe = StringField("user groupe: ", [
        validators.DataRequired("Please enter your user_groupe."),
        validators.Length(1, 30, "Name should be from 10 to 30 symbols")])

    user_faculty = StringField("user faculty: ", [
        validators.DataRequired("Please enter user faculty.")])

    user_course = IntegerField("user course: ", [valid_user_course,
        validators.DataRequired("Please enter user course."),
        validators.Length(1, 40, "Name should be from 10 to 40 symbols")
    ])

    # lesson_name = StringField("lesson name: ", [
    #     validators.DataRequired("Please enter lesson name."),
    #     validators.Length(1, 40, "Name should be from 10 to 40 symbols")
    # ])

    submit = SubmitField("Save")


class LessonForm(Form):
    lesson_id = IntegerField("lesson id: ", [valid_minus,
        validators.DataRequired("Please enter lesson id.")
    ])

    build_number = StringField("build number: ", [valid_minus,
                                                  validators.DataRequired("Please enter build_number.")
                                                  ])

    lesson_name = StringField("lesson name: ", [
        validators.DataRequired("Please enter lesson name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    lesson_number = IntegerField("lesson number: ", [valid_lesson_number,
                                                     validators.DataRequired("Please enter lesson id.")
                                                     ])

    teacher = StringField("teacher name: ", [
        validators.DataRequired("Please enter lesson name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    floors_number = StringField("classroom number: ", [valid_minus,
        validators.DataRequired("Please enter count items.")
    ])



    submit = SubmitField("Save")


class LessonForm1(Form):
    lesson_id = IntegerField("lesson id: ", [valid_minus,
        validators.DataRequired("Please enter lesson id.")
    ])

    build_number = StringField("build number: ", [valid_minus,
        validators.DataRequired("Please enter build_number.")
    ])

    lesson_name = StringField("lesson name: ", [
        validators.DataRequired("Please enter lesson name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    lesson_number = IntegerField("lesson number: ", [valid_lesson_number,
        validators.DataRequired("Please enter lesson id.")
    ])

    teacher = StringField("teacher name: ", [
        validators.DataRequired("Please enter lesson name."),
        validators.Length(1, 20, "Name should be from 3 to 20 symbols")
    ])

    floors_number = StringField("classroom number: ", [valid_minus,
                                                       validators.DataRequired("Please enter count items.")
                                                       ])

    submit = SubmitField("Save")


class NeuronForm(Form):


    user_groupe = StringField("user groupe: ", [
        validators.DataRequired("Please enter your user_groupe."),
        validators.Length(1, 30, "Name should be from 10 to 30 symbols")])

    user_faculty = StringField("user faculty: ", [
        validators.DataRequired("Please enter user faculty.")])


    submit = SubmitField("Save")


class FloorForm(Form):
    floors_number = StringField("floors number: ", [valid_minus,
        validators.DataRequired("Please enter floors number."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    build_number = StringField("build number: ", [valid_minus,
        validators.DataRequired("Please enter build number.")
    ])

    floor_type = StringField("floors type: ", [valid_type,
        validators.DataRequired("Please enter floors number."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    floor_status = StringField("floor status: ", [valid_status,
        validators.DataRequired("Please enter floor status."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    submit = SubmitField("Save")


class FloorForm1(Form):
    floors_number = StringField("floors number: ", [valid_minus,
        validators.DataRequired("Please enter floors number."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    build_number = StringField("build number: ", [valid_minus,
        validators.DataRequired("Please enter build number.")
    ])

    floor_type = StringField("floors type: ", [valid_type,
        validators.DataRequired("Please enter floors number."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    floor_status = StringField("floor status: ", [valid_status,
        validators.DataRequired("Please enter floor status."),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    submit = SubmitField("Save")



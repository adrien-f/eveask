from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from eveask.models import User


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class RegisterApiForm(Form):
    key_id = TextField('key_id', validators=[DataRequired()])
    vcode = TextField('vcode', validators=[DataRequired(), Length(min=64, max=64)])


class RegisterAccountForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    character_id = SelectField('Character name', coerce=int, validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        Length(min=8),
        DataRequired(),
        EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired(), Email()])

    def validate_username(form, field):
        username = field.data
        users = User.query.filter_by(username=username).first()
        if users is not None:
            raise ValidationError('This username is already in use')

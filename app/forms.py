from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app import db
from app.models import Client
from sqlalchemy import select

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Create account')

    def validate_username(self, login):
        client = db.session.execute(select(Client).where(Client.login == login.data)).scalar_one_or_none()
        if client is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        client = db.session.execute(select(Client).where(Client.email == email.data)).scalar_one_or_none()
        if client is not None:
            raise ValidationError('Please use a different email address.')

class TaskForm(FlaskForm):
    task_name = StringField(label='Name', validators=[DataRequired()])
    task_description = StringField(label='Description', validators=[DataRequired()])
    worker = SelectField(label='Worker', validators=[DataRequired()])
    submit = SubmitField('Create task')

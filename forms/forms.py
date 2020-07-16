
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    FileField, TextField, validators, RadioField, SelectMultipleField
from wtforms.widgets import TextArea
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_components import DateTimeField, DateRange
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from flask import session
from wtforms.validators import NumberRange


class search(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(min=3, max=30)])


class recordSelection(FlaskForm):
    recordSelection = SelectField('Select Item', choices=[('Skater','Skater'), ('Skateboards','Skateboards'), ('Shoes','Shoes'), ('Trucks','Trucks'), ('Wheels','Wheels'), ('Tricks','Tricks')])

class contactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    emailAddress = StringField('Email', validators=[DataRequired(), Email()])
    message = TextField('Write your message here...', validators=[DataRequired(), Length(min=20, max=250)])
    submit = SubmitField('Send!')


class loginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('login')

class registration(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

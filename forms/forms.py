
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


class newSkater(FlaskForm):
    skaterName = StringField('Skater Name', validators=[DataRequired(), Length(min=2, max=30)])
    skaterAge = IntegerField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    skaterSex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    skateboardSponsor = StringField('Skateboard Company', validators=[DataRequired(), Length(min=2, max=30)])
    shoeSponsor = StringField('Shoe Sponsor', validators=(DataRequired(), Length(min=2, max=30)))
    truckSponsor = StringField('Truck Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    wheelSponsor = StringField('Wheel  Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Propose new skater')

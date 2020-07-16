from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    FileField, TextField, validators, RadioField, SelectMultipleField
from wtforms.widgets import TextArea
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class newSkater(FlaskForm):
    name = StringField('Skater Name', validators=[DataRequired(), Length(min=2, max=30)])
    DOB = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])
    gender = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    skateboard = StringField('Skateboard Company', validators=[DataRequired(), Length(min=2, max=30)])
    shoes = StringField('Shoe Sponsor', validators=(DataRequired(), Length(min=2, max=30)))
    trucks = StringField('Truck Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    wheels = StringField('Wheel  Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Propose new skater')

class newSkateboards(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    est = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Propose new skateboard')

class newShoes(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    est = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Propose new shoes')

class newTricks(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    creator = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    difficulty = SelectField('Difficulty', choices=[('Easy', 'Easy'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')]) 
    submit = SubmitField('Propose new trick')

class newTrucks(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    est = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])    
    submit = SubmitField('Propose new trucks')

class newWheels(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    est = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])  
    submit = SubmitField('Propose new wheels')
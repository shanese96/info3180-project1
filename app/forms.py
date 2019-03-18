from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email

class ProfileForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    location = StringField('location', validators=[DataRequired()])
    gender = SelectField('gender', validators=[DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')])
    biography = TextAreaField('biography', validators=[DataRequired()])
    photo = FileField('image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
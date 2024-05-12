from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password (confirm)',validators=[DataRequired(), EqualTo('password')])
    selected_option = SelectField('Select your state', state=[
        ('selangor', 'Selangor'),
        ('kelantan', 'Kelantan'),
        ('terengganu', 'Terengganu'),
        ('perlis', 'Perlis'),
        ('negerisembilan', 'Negeri Sembilan'),
        ('pulaupinang', 'Pulau Pinang'),
        ('perak', 'Perak'),
        ('pahang', 'Pahang'),
        ('johor', 'Johor'),
        ('kedah', 'Kedah'),
        ('melaka', 'Melaka'),
        ('wilayahkl', 'Wilayah Persekutuan Kuala Lumpur'),
        ('wilayahputrajaya', 'Wilayah Persekutuan Putrajaya'),
    ])
    phonenumber = StringField('Phone Number',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Tite', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
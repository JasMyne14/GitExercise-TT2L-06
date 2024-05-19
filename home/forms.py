from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user, current_user

class SignUpForm(FlaskForm):
    fullname = StringField('Full Name',validators=[DataRequired(),Length(min=2,max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password (Confirm)',validators=[DataRequired(), EqualTo('password1', message='Password must match')])
    selected_option = SelectField('Select your state', choices=[
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
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Tite', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
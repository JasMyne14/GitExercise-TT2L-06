from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class SignUpForm(FlaskForm):
    fullname = StringField('Full Name',validators=[DataRequired(),Length(min=2,max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password (Confirm)', validators=[DataRequired(), EqualTo('password1', message='Password must match')])
    selected_option = SelectField('Select your state', choices=[
        ('', 'Select your state'),
        ('Selangor', 'Selangor'),
        ('Kelantan', 'Kelantan'),
        ('Terengganu', 'Terengganu'),
        ('Perlis', 'Perlis'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Perak', 'Perak'),
        ('Pahang', 'Pahang'),
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Melaka', 'Melaka'),
        ('Wilayah Persekutuan Kuala Lumpur', 'Wilayah Persekutuan Kuala Lumpur'),
        ('Wilayah Persekutuan Putrajaya', 'Wilayah Persekutuan Putrajaya'),
    ])    
    phonenumber = StringField('Phone Number',validators=[DataRequired(),Length(min=10,max=12)])
    profile_pic = FileField("Profile Pic", validators=[FileAllowed(['jpg','png','jpeg','JPG'])])
    submit = SubmitField('Submit')


class UpdateProfileForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    selected_option = SelectField('Select your state', choices=[
        ('Selangor', 'Selangor'),
        ('Kelantan', 'Kelantan'),
        ('Terengganu', 'Terengganu'),
        ('Perlis', 'Perlis'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Perak', 'Perak'),
        ('Pahang', 'Pahang'),
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Melaka', 'Melaka'),
        ('Wilayah Persekutuan Kuala Lumpur', 'Wilayah Persekutuan Kuala Lumpur'),
        ('Wilayah Persekutuan Putrajaya', 'Wilayah Persekutuan Putrajaya')
    ])
    phonenumber = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20)])
    profile_pic = FileField("Profile Pic", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'JPG'])])
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        if 'obj' in kwargs and kwargs['obj'] is not None:
            self.selected_option.data = kwargs['obj'].state
            
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Tite', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    file= FileField('File', validators=[FileAllowed(['jpg','jpeg','png','pdf','gif','mov','mp4'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    text = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

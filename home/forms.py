from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])

class PostForm(FlaskForm):
    title = StringField('Tite', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
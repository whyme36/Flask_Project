from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskcsvdb.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
#żeby nie powtarzali się użytkownicu
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
          raise ValidationError('Użytkownik o tym nicku istnieje!')
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
          raise ValidationError('Email już jest użyty!')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])]) #pomyśl o rozmiarach zdjęcia
    submit = SubmitField('Update')
#żeby nie powtarzali się użytkownicu
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    csv = FileField('Add csv', validators=[FileAllowed(['csv']),DataRequired()])
    submit=SubmitField('Post')

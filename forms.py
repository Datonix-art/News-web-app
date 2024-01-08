from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, EqualTo



class SignupForm(FlaskForm):
  username = StringField('Enter Username:', validators=[DataRequired(), Length(min=3, max=15)])
  password = PasswordField('Enter Password:', validators=[DataRequired(), Length(min=8, max=25)])
  birthDate = DateField('When were you born?', format='%Y-%m-%d', validators=[DataRequired()])
  submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
  username = StringField('Enter your username', validators=[DataRequired(), Length(min=3, max=15)]) 
  password = PasswordField('Enter your password', validators=[DataRequired(), Length(min=8, max=25)]) 
  submit = SubmitField('Log in')

class PasswordChangeForm(FlaskForm):
  password = PasswordField('Current password', validators=[DataRequired()])
  newPassword = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=25)])
  confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('newPassword', message='Passwords must match')])
  submit = SubmitField('Apply')

class UsernameChangeForm(FlaskForm):
  username = StringField('Enter username', validators=[DataRequired()])
  password = PasswordField('Enter your current password to save changes', validators=[DataRequired()])
  submit = SubmitField('Apply')



class PostArticleForm(FlaskForm):
  image = FileField('add photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')])
  title = StringField('add title', validators=[DataRequired(), Length(min=2, max=12)])
  description = StringField('add some information about the article', validators=[DataRequired(), Length(min=10, max=75)])
  add = SubmitField('Register')

class ChangePostForm(FlaskForm):
  image = FileField('add photo', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')])
  title = StringField('add title', validators=[DataRequired(), Length(min=2, max=12)])
  description = StringField('add some information about the article', validators=[DataRequired(), Length(min=10, max=75)])
  add = SubmitField('Register')

class PostCommentForm(FlaskForm):
  message = StringField('write a comment', validators=[Optional()])
  submit_comment = SubmitField('comment')
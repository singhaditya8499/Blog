from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import TextAreaField,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Length,Email,ValidationError
from blog.models import User

class RegForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=10)])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),Length(min=2,max=10),EqualTo('password')])
	submit=SubmitField('Sign Up')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is taken. Please choose a different one.')

	def validate_email(self,email):
		email=User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('Email already exist!')

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=10)])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','jpeg','png'])])
	submit=SubmitField('Update')

	def validate_username(self,username):
		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is taken. Please choose a different one.')

	def validate_email(self,email):
		if email.data!=current_user.email:
			email=User.query.filter_by(email=email.data).first()
			if email:
				raise ValidationError('Email already exist!')


class PostForm(FlaskForm):
	title=StringField('Title',validators=[DataRequired()])
	content=TextAreaField('Content',validators=[DataRequired()])
	submit=SubmitField('Post')






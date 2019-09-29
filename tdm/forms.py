from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length,EqualTo,ValidationError
from tdm.models import Admin

class LoginForm(FlaskForm):
	username=StringField('Username',
		validators=[DataRequired(),Length(min=2,max=20)])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=20)])
	remember=BooleanField('Remember me')
	submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
	username=StringField('Username',
		validators=[DataRequired(),Length(min=2,max=20)])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=20)])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Sign Up')
	def validate_username(self,username):
		admin=Admin.query.filter_by(username=username.data).first()
		if admin:
			raise ValidationError('Username already exists. Choose another one.')
# class SearchForm(FlaskForm):
# 	searchterm=StringField('query',validators=[Length(max=21)])
# 	qType='n'
# 	def validate_type(self):
# 		result=Entry.query.filter_by(username=searchterm.strip()).first()
# 		if(result):
# 			try:
# 				result=Entry.query.filter_by(int(searchterm.strip())).first()
# 				if(result):
# 					self.qType='t'
# 				# else:
# 					# raise ValidationError("No such entry")
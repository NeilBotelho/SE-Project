from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired, Length,EqualTo,ValidationError
from tdm.models import Admin, Entry
from tdm import db
# from flask import flash
class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
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
class SearchForm(FlaskForm):
	searchTerm=StringField('Search',validators=[Length(max=21)])
	submit=SubmitField('Add Entry')

class DeleteForm(FlaskForm):
	ID=IntegerField('ID of entry to be deleted')
	moreThanOneEntry=BooleanField('Delete More Than One Entry')
	submit=SubmitField('Delete Entry')

class NewEntryForm(FlaskForm):
	ID=IntegerField("phone_num")
	phone_num=IntegerField("Phone Number",validators=[DataRequired()])
	name=StringField("Name",validators=[DataRequired(),Length(min=2,max=50)])
	address=StringField("Address",validators=[DataRequired(),Length(min=2,max=50)])
	moreThanOneEntry=BooleanField('More Than One New Entry')
	submit=SubmitField('Add Entry')
	def validate_phone_num(self,phone_num):
		phone_len=len(str(phone_num.data))
		if(phone_len>14 or phone_len <8):
			raise ValidationError('Invalid Phone number')
		entry=db.session.query(Entry.phone_num).filter_by(phone_num=phone_num.data).first()
		if(entry):
			raise ValidationError('Phone Number already exists in directory. \nPlease ask an admin to edit the entry if necessary.')
class EditEntryForm(FlaskForm):
	ID=IntegerField("ID of Entry to be edited",validators=[DataRequired()])
	phone_num=IntegerField("Phone Number",validators=[DataRequired()])
	name=StringField("Name",validators=[DataRequired(),Length(min=2,max=50)])
	address=StringField("Address",validators=[DataRequired(),Length(min=2,max=50)])
	moreThanOneEntry=BooleanField('More Than One New Entry')
	submit=SubmitField('Write Changes')
	def validate_phone_num(self,phone_num):
		phone_len=len(str(phone_num.data))
		if(phone_len>14 or phone_len <8):
			raise ValidationError('Invalid Phone number')
		def validate_ID(self,ID):
			entry=db.session.query(Entry.ID).filter_by(ID=ID.data)
			if(type(entry)!=type([1])):
				raise ValidationError("No such ID exists in directory")

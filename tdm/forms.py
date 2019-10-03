from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired, Length,EqualTo,ValidationError
from tdm.models import Admin, Medicine
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



class SearchForm(FlaskForm):
	searchTerm=StringField('Search',validators=[Length(max=21)])
	submit=SubmitField('Add Entry')

class NewEntryForm(FlaskForm):
	ID=IntegerField("ID")
	name=StringField("Name",validators=[DataRequired(),Length(min=2,max=50)])
	MFD=StringField("Manufacture Date",validators=[DataRequired(),Length(min=2,max=10)])
	EXP=StringField("Expiry Date",validators=[DataRequired(),Length(min=2,max=10)])
	units=IntegerField("Number of Units in Stock",validators=[DataRequired()])
	price=IntegerField("Price",validators=[DataRequired()])
	moreThanOneEntry=BooleanField('More Than One New Entry')
	submit=SubmitField('Add to Database')

class EditEntryForm(FlaskForm):
	ID=IntegerField("ID of entry to be edited",validators=[DataRequired()])
	name=StringField("Name",validators=[DataRequired(),Length(min=2,max=50)])
	MFD=StringField("Manufacture Date",validators=[DataRequired(),Length(min=2,max=10)])
	EXP=StringField("Expiry Date",validators=[DataRequired(),Length(min=2,max=10)])
	units=IntegerField("Number of Units in Stock",validators=[DataRequired()])
	price=IntegerField("Price",validators=[DataRequired()])
	submit=SubmitField('Write changes to database')
	def validate_ID(self,ID):
		entry=db.session.query(Medicine.ID).filter_by(ID=ID.data)
		if(type(entry)!=type([1])):
			raise ValidationError("No such ID exists in directory")

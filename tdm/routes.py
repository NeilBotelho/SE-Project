from flask import Flask, redirect, url_for, flash, request, render_template,session
from tdm.forms import LoginForm, RegistrationForm, NewEntryForm, SearchForm, EditEntryForm, DeleteForm
from tdm.models import Admin, Entry
from tdm import app, db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required

@app.route('/',methods=['POST','GET'])
def home():
	rows=Entry.query.all()
	form=SearchForm()
	if form.validate_on_submit():
		if form.searchTerm.data=="":
			return render_template('home.html',title='Welcome',rows=rows,form=form)
		rows=[]
		NameRows=Entry.query.filter_by(name=form.searchTerm.data.strip())
		AddressRows=Entry.query.filter_by(address=form.searchTerm.data.strip())
		PhoneRows=[]
		try:
			PhoneRows=Entry.query.filter_by(phone_num=int(form.searchTerm.data.strip()))
		except:
			pass
		for field in (NameRows,AddressRows, PhoneRows):
			for data in field:
				rows.append(data)
	return render_template('home.html',title='Welcome',rows=rows,form=form)

@app.route('/about')
def about():
	return "About"

@app.route('/register',methods=['GET','POST'])
def register():
	if(not current_user.is_authenticated):
		flash("Only admins can register new users","danger")
		return redirect(url_for('home'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_admin=Admin(username=form.username.data.lower(),password=hashed_password)
		db.session.add(new_admin)
		db.session.commit()
		flash("Account created for "+str(form.username.data)+"!. You can now log in" ,"success")
		return redirect(url_for('login'))
	return render_template('register.html',title='Sign Up',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	if(current_user.is_authenticated):
		flash("You are already logged in","success")
		return redirect(url_for("home"))
	form=LoginForm()
	if form.validate_on_submit():
		admin=Admin.query.filter_by(username=form.username.data.lower()).first()
		if(admin and bcrypt.check_password_hash(admin.password,form.password.data)):
			login_user(admin,remember=form.remember.data)
			return redirect(url_for("home"))
		else:
			flash("Login Unsuccessful. Please check username and password","danger")
	return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
	if(current_user.is_authenticated):
		logout_user()
		flash("Successfully logged out","success")
		return redirect(url_for('home'))
	else:
		flash("You are not logged in","danger")
		return redirect(url_for('home'))



@app.route('/admin/newentry',methods=['GET','POST'])
@login_required
def newEntry():
	form=NewEntryForm()
	if form.validate_on_submit():
		entry=Entry(phone_num=form.phone_num.data,name=form.name.data.lower(),address=form.address.data.lower())
		db.session.add(entry)
		db.session.commit()
		flash("Entry has been added","success")
		if(not form.moreThanOneEntry.data):
			return redirect(url_for('home'))
		else:
			return redirect(url_for('newEntry'))
	rows=Entry.query.all()
	# flash(form.ID.data)
	return render_template('newEntry.html',title="new",form=form,rows=rows)

@app.route('/admin/editentry',methods=['POST','GET'])
@login_required
def editEntry():
	form=EditEntryForm()
	if form.validate_on_submit():
		entry=Entry.query.filter_by(ID=form.ID.data).first()
		entry.phone_num=form.phone_num.data
		entry.name=form.name.data.lower()
		entry.address=form.address.data.lower()
		db.session.commit()
		flash("The entry has been updated","success")
		return redirect(url_for('home'))
	rows=Entry.query.all()
	return render_template('update.html',title="Update entry",form=form,rows=rows)

@app.route('/admin/deleteentry',methods=['POST','GET'])
@login_required
def deleteEntry():
	rows=Entry.query.all()
	deleteForm=DeleteForm()
	if deleteForm.validate_on_submit():
		entry=Entry.query.filter_by(ID=int(deleteForm.ID.data)).first()
		if(not entry):
			flash("Given id does not exist","danger")
			return redirect(url_for('home'))
		db.session.delete(entry)
		db.session.commit()

		flash("Entry "+str(deleteForm.ID.data)+" has been deleted","success")
		if(not deleteForm.moreThanOneEntry.data):
			return redirect(url_for('deleteEntry'))
		else:
			return redirect(url_for('deleteEntry'))
	return render_template('deleteEntry.html',title="Delete entry",deleteForm=deleteForm,rows=rows)

	# 	db.session.add(entry)
	# 	db.session.commit()
	# 	flash("Entry has been added","success")
	# 	if(not deleteForm.moreThanOneEntry.data):
	# 		return redirect(url_for('home'))
	# 	else:
	# 		return redirect(url_for('newEntry'))
	# rows=Entry.query.all()
	# # flash(deleteForm.ID.data)
	# return render_template('newEntry.html',title="new",form=deleteForm,rows=rows)

	# return render_template('home.html',title='Welcome',rows=rows,form=form)

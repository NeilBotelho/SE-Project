from flask import Flask, redirect, url_for, flash, request, render_template,session
from psm.forms import LoginForm, RegistrationForm, NewEntryForm, SearchForm, EditEntryForm
from psm.models import Admin, Medicine
from psm import app, db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required
tempadmin='bitchboy'
@app.route('/',methods=['POST','GET'])
def home():
	rows=Medicine.query.all()
	form=SearchForm()
	if form.validate_on_submit():
		if form.searchTerm.data=="":
			return render_template('home.html',title='Welcome',rows=rows,form=form)
		rows=[]
		NameRows=Medicine.query.filter_by(name=form.searchTerm.data.strip())
		MfdRows=Medicine.query.filter_by(MFD=form.searchTerm.data.strip())
		ExpRows=Medicine.query.filter_by(EXP=form.searchTerm.data.strip())
		UnitsRows=[]
		PriceRows=[]
		try:
			UnitsRows=Medicine.query.filter_by(units=int(form.searchTerm.data.strip()))
			PriceRows=Medicine.query.filter_by(price=int(form.searchTerm.data.strip()))
		except:
			pass
		for field in (NameRows,MfdRows,ExpRows,UnitsRows,PriceRows):
			for data in field:
				rows.append(data)
	return render_template('home.html',title='Welcome to the phramacy',rows=rows,form=form) 

@app.route('/about')
def about():
	return render_template('about.html',title='About') 

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
		flash("Account created for "+str(form.username.data)+"!" ,"success")
		return redirect(url_for('home'))
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
		medicine=Medicine(MFD=form.MFD.data,EXP=form.EXP.data,name=form.name.data.lower(),units=form.units.data,price=form.price.data)
		db.session.add(medicine)
		db.session.commit()
		flash("Medicine has been added","success")
		if(not form.moreThanOneEntry.data):
			return redirect(url_for('home'))
		else:
			return redirect(url_for('newEntry'))
	rows=Medicine.query.all()
	# flash(form.ID.data)
	return render_template('newEntry.html',title="new",form=form,rows=rows)

@app.route('/admin/editentry',methods=['POST','GET'])
@login_required
def editEntry():
	form=EditEntryForm()
	if form.validate_on_submit():
		medicine=Medicine.query.filter_by(ID=form.ID.data).first()
		medicine.phone_num=form.phone_num.data
		medicine.name=form.name.data.lower()
		medicine.address=form.address.data.lower()
		db.session.commit()
		flash("The entry has been updated","success")
		return redirect(url_for('home'))
	rows=Medicine.query.all()
	return render_template('update.html',title="Update entry",form=form,rows=rows)		


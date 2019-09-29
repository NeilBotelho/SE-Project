from flask import Flask, redirect, url_for, flash, request, render_template,session
from tdm.forms import LoginForm, RegistrationForm
from tdm.models import Admin, Entry, EntryTable,SortableTable
from tdm import app, db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required

@app.route('/')
def home():
	rows=Entry.query.all()

	return render_template('home.html',title='Welcome',rows=rows) 

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
		new_admin=Admin(username=form.username.data,password=hashed_password)
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
		admin=Admin.query.filter_by(username=form.username.data).first()
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

@app.route('/result',methods=['POST','GET'])
def result():
	return  request.args.get('Search', '')
	return str(request.form)
	# return request.form['tableSearch']
	# return render_template('results.html',title=%seach)
@app.route('/addentry')
@login_required
def add():
	return render_template('new_entry.html',title="new")
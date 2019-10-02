from datetime import datetime
from tdm import db, login_manager
from flask_login import UserMixin
from flask_table import Table, Col

# from flask
@login_manager.user_loader
def load_admin(admin_id):
	return Admin.query.get(int(admin_id))


class Admin(db.Model,UserMixin):
	ID=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True,nullable=False)
	password=db.Column(db.String(20),nullable=False)
	def __repre__(self):
		return f'Admin("{self.username}")'
	def get_id(self):
		return self.ID

class Medicine(db.Model):
	ID=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),unique=False,nullable=False)
	MFD=db.Column(db.String(50),unique=False,nullable=False)
	EXP=db.Column(db.String(50),unique=False,nullable=False)
	units=db.Column(db.Integer)
	price=db.Column(db.Integer)
	last_edited=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
	def __repre__(self):
		return f'Entry("{self.ID}",{self.name})'



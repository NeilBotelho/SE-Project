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

class Entry(db.Model):
	ID=db.Column(db.Integer,primary_key=True)
	phone_num=db.Column(db.Integer,unique=True,nullable=False)
	name=db.Column(db.String(50),unique=False,nullable=False)
	address=db.Column(db.String(50),unique=False,nullable=False)
	last_edited=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
	def __repre__(self):
		return f'Entry("{self.ID}",{self.name})'


# Declare your table
class EntryTable(Table):
    ID=Col('ID')
    name = Col('name')
    address = Col('address')
    phone_num=Col('phone_num')

# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
class SortableTable(Table):
    name = Col('Name')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction =  'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)
# items = [Item('Name1', 'Description1'),
#          Item('Name2', 'Description2'),
#          Item('Name3', 'Description3')]
# # Or, equivalently, some dicts
# items = [dict(name='Name1', description='Description1'),
#          dict(name='Name2', description='Description2'),
#          dict(name='Name3', description='Description3')]

# # Or, more likely, load items from your database with something like
# items = .query.all()

# # Populate the table
# table = ItemTable(items)

# # Print the html
# print(table.__html__())
# # or just {{ table }} from within a Jinja template

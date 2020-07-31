from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from docker_wae import db,app,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except:
		return None
		
class User(db.Model,UserMixin):
	__bind_key__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True,nullable=False)
	email = db.Column(db.String(120),unique=True,nullable=False)
	password = db.Column(db.String(60),nullable=False)
	password_decrypted = db.Column(db.String(60),nullable=False)
	
	def __repr__(self):
		return f"User('{self.username}')"
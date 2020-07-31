from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session,jsonify
from docker_wae import app,db,bcrypt,login_manager
from docker_wae.user_management.forms import LoginForm,RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from docker_wae.models import User

blue = Blueprint('user_management',__name__,template_folder='templates')

@blue.route('/',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			print("HELLO")
			return redirect(next_page) if next_page else redirect(url_for('home.home'))
		else:
			flash('Login Unsuccessful. Please check email or password','danger')

	return render_template('user_management/login.html',form=form)

@blue.route('/register',methods=['GET','POST'])
def register():
	
	if current_user.is_authenticated:
		return redirect(url_for('user_management.login'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password,password_decrypted=form.password.data)
		db.session.add(user)
		db.session.commit()
		
		flash(f'Your Account has been created! You are now able to login','success')
		return redirect(url_for('user_management.login'))

	return render_template('user_management/register.html',form=form)



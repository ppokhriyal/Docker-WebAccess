from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session,jsonify
from docker_wae import app,db,bcrypt,login_manager
from flask_login import login_user, current_user, logout_user, login_required
from docker_wae.models import User
import docker


blue = Blueprint('home',__name__,template_folder='templates')
client = docker.APIClient(base_url='unix://var/run/docker.sock')

#Dashboard
@blue.route('/home')
@login_required
def home():
	running = 0
	stop = 0
	
	for i in range(len(client.containers(all=True))):

		if client.containers(all=True)[i]['State'] == 'created' or client.containers(all=True)[i]['State'] == 'exited':
			stop = stop + 1

		elif client.containers(all=True)[i]['State'] == 'running':
			running = running + 1

	return render_template('home/home.html',title="Docker WAE : Home",client=client,running=running,stop=stop)

#Image Template
@blue.route('/images')
@login_required
def images():
	return render_template('home/images.html',title="Docker WAE : Images",client=client)

#Inspect image template
@blue.route('/inspect/image_template/<image_id>')
@login_required
def inspect_image_template(image_id):

	inspect_image = client.inspect_image(image_id)
	return render_template('home/inspect_image_template.html',title='Docker WAE : Inspect Image Template',inspect_image=inspect_image)

#Download image from Docker Hub
@blue.route('/image_template/download')
@login_required
def download_image_template():

	return render_template('home/download_image_template.html',title='Docker WAE : Download Image Template')

#Search Image in Docker Hub
@blue.route('/image_template/search',methods=['GET','POST'])
@login_required
def search_img_hub():
	if request.method == 'POST':

		if request.form['searchimagetag'] != '':
			searchimage = client.search(request.form['searchimagename']+':'+request.form['searchimagetag'])
			len_searchimage = len(client.search(request.form['searchimagename']+':'+request.form['searchimagetag']))
		else:
			searchimage = client.search(request.form['searchimagename']+':latest')
			len_searchimage = len(client.search(request.form['searchimagename']+':latest'))

	return render_template('home/download_image_template.html',title='Docker WAE : Download Image Template',searchimage=searchimage,len_searchimage=len_searchimage,result=request.form['searchimagename']+':'+request.form['searchimagetag'])



#User Logout
@blue.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_management.login'))
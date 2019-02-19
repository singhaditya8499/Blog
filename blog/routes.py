import os
from PIL import Image
from flask import request,render_template,flash,redirect,url_for,abort
from blog.forms import RegForm, LoginForm,UpdateAccountForm,PostForm
from blog import app,db,bcrypt
from blog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required


@app.route("/")
def hello():
	post=Post.query.all()
	return render_template('home.html',posts=post)

@app.route("/about")
def about():
    return render_template('about.html',title="About with title")

@app.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('hello'))
	form=RegForm()
	if form.validate_on_submit():
		hashed_password=str(bcrypt.generate_password_hash(form.password.data))
		hashed_password=str(hashed_password)
		print(type(hashed_password))
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created. You can now login!','success')
		return redirect(url_for('login'))
	return render_template('register.html',form=form,title='Register')

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('hello'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('hello'))
		else:
			flash('Login unsuccessful! Please check username and password.','danger')
	return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('hello'))


def save_picture(form_picture,id):
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=str(id)+f_ext
	picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
	output_size=(125, 125)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn



@app.route('/account',methods=['GET','POST'])
@login_required
def account():
	form=UpdateAccountForm()
	x=current_user
	print(x.user_image)
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data,current_user.id)
			print(picture_file)
			current_user.user_image=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your account has been updated!','success')
		return redirect(url_for('account'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	image_file=url_for('static',filename='profile_pics/'+current_user.user_image)
	return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data,content=form.content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!','success')
		return redirect(url_for('hello'))
	return render_template('create_post.html',form=form,title='New Post',legend='New Post')



@app.route('/post/<int:post_id>')
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template('post.html',title=post.title,post=post)


@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def updatepost(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash('Your post has been updated!','success')
		return redirect(url_for('post',post_id=post.id))
	elif request.method=='GET':
		form.title.data=post.title
		form.content.data=post.content
	return render_template('create_post.html',form=form,title='Update Post',legend='Update Post')


@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!','success')
	return redirect(url_for('hello'))

























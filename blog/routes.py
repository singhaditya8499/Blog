from flask import request,render_template,flash,redirect,url_for
from blog.forms import RegForm, LoginForm
from blog import app,db,bcrypt
from blog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required


post=[
	{
		"author":"Aditya singh",
		"date":"15 Feb 2019",
		"title":"Hello World",
		"content":"Hello I am Aditya singh"
	},
	{
		"author":"Bulbul singh",
		"date":"19 Feb 2019",
		"title":"Hello Girl",
		"content":"Hello I am Bulbul singh"
	}
]
@app.route("/")
def hello():
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


@app.route('/account')
@login_required
def account():
	return render_template('account.html',title='Account')



import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from datetime import datetime
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "cdtydvaerbtyuytnurdvcs"
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)

class ComplaintForm(Form):
	name = StringField("Full Name")
	address = StringField("Address")
	email = StringField("Email") 
	phone = StringField("Phone")
	body = TextAreaField("What's your complaint?", validators=[Required()])
	submit = SubmitField('Submit')

class Role(Form):
    username = StringField("Name", validators = [Required()])
    password = PasswordField("Password", validators = [Required()])
    submit = SubmitField('Submit')

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.role


class Post(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    address = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(64), unique=False)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.timestamp

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    form = ComplaintForm()
    role = 'unknown'
    if form.validate_on_submit():
        post = Post(name=form.name.data,address=form.address.data,email=form.email.data,phone=form.phone.data,body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Your complaint is submitted!')
    return render_template('complaint.html', form = form, role=role)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = Role()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        if name == 'admin' and password == '1234':
            role = 'admin'
        else:
            role = 'unknown'
        return redirect(url_for('.display', role = role))
    return render_template('login.html', form = form)

@app.route('/display/<role>', methods = ['GET', 'POST'])
def display(role):
    form = ComplaintForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data,address=form.address.data,email=form.email.data,phone=form.phone.data,body=form.body.data)
        db.session.add(post)
        db.session.commit()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('display.html', posts = posts, form=form, role=role)



@app.route('/<role>/delete/<int:id>', methods=['GET', 'POST'])
def delete(role,id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.display',role=role))

# Assigning task to the police man
# initial number of policeman in stations
def assign_task():
    police_man=10
    complaints = db.session.execute('select count(*) from complaints').scalar()
    new_police_man = complaints-police_man
    print("\n","\n","************CONFIDENTIAL-DETAIL******************","\n","\n")
    if(new_police_man<0):
        complaints=0
        police_man=abs(new_police_man)
        print("Number of complaints left to be Solve:- ",complaints)
        print("Number of Police-man available- ",police_man)
    
    elif(new_police_man>0):
        police_man=0
        complaints=new_police_man
        print("Number of complaints left to be Solve:- ",complaints)
        print("Number of Police-man available- ",0)
    
    elif(new_police_man==0):
        complaints=0
        police_man=0
        print("Number of complaints left to be Solve:- ",complaints)
        print("Number of Police-man available- ",police_man)
    print("\n","\n","*************************************************")

    
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=assign_task, trigger="interval", seconds=20)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    app.run(host="0.0.0.0",port=5000,debug = True,use_reloader=False)

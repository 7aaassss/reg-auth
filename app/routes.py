from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from app import app, db, login
from app.forms import LoginForm, RegForm, TaskForm
from app.models import Client
import sqlalchemy as sa
from urllib.parse import urlsplit
import requests

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        client = db.session.scalar(
            sa.select(Client).where(Client.login == form.login.data))
        if client is None or not client.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(client, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        client = Client(login=form.login.data, email=form.email.data)
        client.set_password(form.password.data)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/all_users', methods=['GET'])
def all_users():
    all_users = db.session.query(Client)
    response = [user.login for user in all_users]
    return jsonify(response)


@app.route('/task-create')
def task_create():
    form = TaskForm()
    all_users = db.session.query(Client).where(Client.login != current_user.login)
    response = [user.login for user in all_users]
    form.worker.choices = response
    return render_template('taskCreate.html', form=form)
from flask_app import app
from flask import flash
from flask import render_template, session, redirect, request
from flask_app.models import user, sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def show_form():
    return render_template('login.html')


@app.route('/register', methods=['post'])
def register():
    if not user.User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = user.User.create_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=['post'])
def login():
    if not user.User.validate_login(request.form):
        return redirect('/')

    data = {
        'email': request.form['email']
    }
    user1 = user.User.get_user_email(data)
    if not user1:
        flash('invalid email/password')
        return redirect('/')
    if not bcrypt.check_password_hash(user1.password, request.form['password']):
        flash(' invalid password')
        return redirect('/')

    session['user_id'] = user1.id

    return redirect('/dashboard')


@app.route('/logout', methods=['post'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user_info = {
        'id': session["user_id"]
    }
    logged_user = user.User.get_user_id(user_info)
    sightings = sighting.Sighting.get_all()
    return render_template('dashboard.html', logged_user=logged_user, sightings=sightings)

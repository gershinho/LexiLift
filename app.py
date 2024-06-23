from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import json
from db_funcs import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "gersh"





@app.route("/", methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get("email")
        psw = request.form.get("password")
        
        if check_user_exist(email, psw):
            user = find_user(email, psw)
            session['user'] = json.dumps(user)
            increment_login_count(user[0])  
            return redirect(url_for('dashboard'))
            
        
        flash('Email or password is incorrect', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        psw = request.form.get("password")
        
        if get_user_by_email(email):
            flash("Email already registered. Please log in.", 'error')
            return redirect(url_for('register'))
        
        insertUser(email, name, psw)
        user = find_user(email, psw)
        increment_login_count(user[0])
        session['user'] = json.dumps(user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        return render_template('dashboard.html', user=user)
    else:
        # Redirect to login if no user found in session
        return redirect(url_for('login'))
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/exercise")
def exercise():
    return render_template('exercise.html')
@app.route("/profile")
def profile():
    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        return render_template('profile.html', user=user)
    else:
        flash('You must be logged in to view your profile.', 'error')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

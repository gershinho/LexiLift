from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
import sqlite3
import json
from db_funcs import *
from dic import *
import re
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "gersh"

def filter_words(word_list):
    filtered_words = []
    for word in word_list:
        details = fetch_word_details(word)
        if details:
            filtered_words.append(word)
    return filtered_words

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
        return redirect(url_for('login'))

@app.route("/profile")
def profile():

    user_json = session.get('user')
    if user_json:
        user = json.loads(user_json)
        return render_template('profile.html', user=user)
    else:
        flash('You must be logged in to view your profile.', 'error')
        return redirect(url_for('login'))



@app.route("/practice", methods=['GET', 'POST'])
def practice():
    if 'user' in session:
        if isinstance(session['user'], str):
            user = json.loads(session['user'])
        else:
            user = session['user']
        
        user_id = user[0]
    else:
        return redirect(url_for('login'))

    if request.method == 'POST':
        chosen_word = request.form.get('chosen_word')
        correct_word = session.get('correct_word')

        # Fetch the current points, correct count, level, and question number from the database
        points = get_user_points(user_id)
        correct_count = get_user_correc(user_id)
        level = get_user_lvl(user_id)
        num = get_user_num(user_id)

        if chosen_word == correct_word:
            points_change = 20
            correct_count += 1
            result_message = {"message": "Correct!", "category": "success"}
        else:
            points_change = -10
            correct_count = 0
            result_message = {"message": f"Sorry, the correct answer is '{correct_word}'.", "category": "error"}

        # Update the level and reset question number if the correct count conditions are met
        if level == 'easy' and correct_count >= 10 and points >= 400:
            level = 'medium'
            correct_count = 0
            num = 1
        elif level == 'medium' and correct_count >= 7 and points >= 1200:
            level = 'hard'
            correct_count = 0
            num = 1
        else:
            num += 1

        # Update points, count, level, and question number in the database
        update_points(user_id, points_change)
        update_count(user_id, correct_count)
        update_level(user_id, level)
        update_num(user_id, num)

        return jsonify(result_message)

    return generate_question(user_id)

def generate_question(user_id):
    level = get_user_lvl(user_id)
    num = get_user_num(user_id)
    
    if level == 'easy':
        word_list = easy
    elif level == 'medium':
        word_list = medium
    else:
        word_list = hard

    if random.choice([True, False]):
        return best_word(word_list, user_id, num, level)
    else:
        return fill_in_blank(word_list, user_id, num, level)

def fill_in_blank(word_list, user_id, num, level):
    all_words = easy + medium + hard
    word = random.choice(word_list)
    details = fetch_word_details(word)

    while details is None or details.get('example', '') == '':
        word = random.choice(word_list)
        details = fetch_word_details(word)

    options = random.sample(word_list, 3)
    if details['word_id'] in options:
        options.remove(details['word_id'])
    options.append(details['word_id'])
    random.shuffle(options)

    session['correct_word'] = details['word_id']

    points = get_user_points(user_id)
    return render_template('exercise.html', options=options, example=details['example'], points=points, num=num, level=level)

def best_word(word_list, user_id, num, level):
    word = random.choice(word_list)
    details = fetch_word_details(word)
    
    while details is None:
        word = random.choice(word_list)
        details = fetch_word_details(word)
    
    options = random.sample(word_list, 3)
    if details['word_id'] in options:
        options.remove(details['word_id'])
    options.append(details['word_id'])
    random.shuffle(options)
    session['correct_word'] = details['word_id']
    
    defi = details['definitions']
    if defi[0].strip("[]").strip("'"):
        new_defi = defi[0].strip("[]").strip("'")
    else:
        new_defi = defi[1].strip("[]").strip("'")
    
    if word.lower() in new_defi.lower():
        new_defi = re.sub(r'\b{}\b'.format(re.escape(word)), '___', new_defi, flags=re.IGNORECASE)

    points = get_user_points(user_id)
    return render_template('exercise.html', defi=new_defi, options=options, correct_word=word, points=points, num=num, level=level)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

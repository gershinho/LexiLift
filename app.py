from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
import sqlite3
import json
from db_funcs import *
from dictionary import *
import re 
import random


#some words have diff amoutn of defintions so might make conditonal that makes sure if def[0] doesnt have anything use def[1]
#make it so you can see other defintions of word
#if word in defintion replace with blank even if its a best word question

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
        # Redirect to login if no user found in session
        return redirect(url_for('login'))
    



@app.route("/practice", methods=['GET', 'POST'])
def practice():
    if 'question_level' not in session:
        session['question_level'] = 'easy'
        session['correct_count'] = 0

    if request.method == 'POST':
        chosen_word = request.form.get('chosen_word')
        correct_word = session.get('correct_word')

        if chosen_word == correct_word:
            session['correct_count'] += 1
            result_message = {"message": "Correct!", "category": "success"}
        else:
            session['correct_count'] = 0  # Reset count if wrong
            result_message = {"message": f"Sorry, the correct answer is '{correct_word}'.", "category": "error"}

        if session['question_level'] == 'easy' and session['correct_count'] == 5:
            session['question_level'] = 'medium'
            session['correct_count'] = 0
        elif session['question_level'] == 'medium' and session['correct_count'] == 5:
            session['question_level'] = 'hard'
            session['correct_count'] = 0

        return jsonify(result_message)

    return generate_question()



def generate_question():
    
    if session['question_level'] == 'easy':
        word_list = easy
    elif session['question_level'] == 'medium':
        word_list = medium
    else:
        word_list = hard
    
    if random.choice([True, False]):
        return best_word(word_list)
    else:
        return fill_in_blank(word_list)

def fill_in_blank(word_list):
    all_words = easy + medium + hard
    word = random.choice(word_list)
    details = fetch_word_details(word)

    while details['example'] == '':
        word = random.choice(word_list)
        details = fetch_word_details(word)

    options = random.sample(all_words, 3)
    options.append(details['word_id'])
    random.shuffle(options)

    session['correct_word'] = details['word_id']

    return render_template('exercise.html', options=options, example=details['example'])

def best_word(word_list):
    word = random.choice(word_list)
    details = fetch_word_details(word)
    options = random.sample(word_list, 3)
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

    return render_template('exercise.html', defi=new_defi, options=options, correct_word=word)


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

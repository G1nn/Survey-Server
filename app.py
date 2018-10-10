import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
import psycopg2
import json
import db

app = Flask(__name__)

'''------------------food survey data------------------'''

survey_data = {
    #0. survey title
    'title' : 'Food Survey',
    #0.5 survey description
    'description' : 'This is a survey on your food choices. No hard questions.',
    #1.text input question
    'q1' : 'What is your comfort food?',
    #2.radio button question
    'q2' : 'Do you eat offal dishes? (e.g. foie gras, chicken feet, chitterlings, etc.)',
    'options' : ['Yes, yummy!', 'Hmm, I do eat some but find others offputting.', 'No, but I would like to try.', 'No, eww!'],
    #3.select box question
    'q3' : 'Which fast-food chain do you dislike the most?',
    'selections' : ['Select restaurant', 'Panda Express', 'Subway', 'Dunkin\' Donuts', 'Burger King', 'McDonald\'s', 'Pizza Hut', 'Taco Bell', 'Starbucks'],
    #4.checkbox question
    'q4' : 'Do you have any dietary restrictions?',
    'checkbox' : 'Yes.',
    #5.conditional text input question
    'q5' : 'What is it?'
}

'''------------------end of survey------------------'''


@app.before_first_request
def initialize():
    db.setup()

@app.route('/')
def home():
    return render_template("home.html", data = survey_data)

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', data = survey_data)

@app.route('/decline')
def decline():
    return render_template('decline.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        q1 = request.form.get('q1', False)
        q2 = request.form.get('q2', False)
        q3 = request.form.get('q3', False)
        q4 = request.form.get('q4', False)
        q5 = request.form.get('q5', False)
        with db.get_db_cursor(commit=True) as cur:
            cur.execute("insert into survey_data (q1, q2, q3, q4, q5) values (%s, %s, %s, %s, %s)", (q1, q2, q3, q4, q5))
        return render_template('thanks.html', data = survey_data)
    else:
        return render_template("survey.html", data = survey_data)

@app.route('/api/results')
def api_results():
    with db.get_db_cursor(commit=True) as cur:
        reverse = request.args.get('reverse')
        if reverse is None:
            cur.execute("SELECT * FROM survey_data")
        else:
            cur.execute("SELECT * FROM survey_data ORDER BY ts DESC")
        rec = cur.fetchall()
    return json.dumps(rec, indent=2)

if __name__ == '__main__':
    pass

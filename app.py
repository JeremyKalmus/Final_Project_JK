from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import quiz_script
import pandas as pd
from bson.json_util import dumps

# Create an instance of Flask
app = Flask(__name__)

client = pymongo.MongoClient(f"mongodb+srv://Jkalmus:KJeremy@cluster0.wecta.mongodb.net/Project-2?retryWrites=true&w=majority")
db = client.The_office
games_played = db.games_played


# Route to render index.html template using data from Mongo
@app.route('/')
def home():
    cursor = games_played.find().sort('_id',-1).limit(1)
    current_game = list(cursor)
    real_lines = current_game[0]['Real_dialouge'] 
    quiz_lines = current_game[0]['Quiz_Script']


    return render_template('index.html', current_game=current_game, real_lines=real_lines, quiz_lines=quiz_lines)

@app.route("/MICHAEL")
def run_quiz_michael():
    user_selection = "MICHAEL"
    quiz = quiz_script.get_quiz(user_selection)

    games_played.insert_one(quiz)

    return redirect("/")

@app.route("/DWIGHT")
def run_quiz_dwight():
    user_selection = "DWIGHT"
    quiz = quiz_script.get_quiz(user_selection)

    games_played.insert_one(quiz)

    return redirect("/")

@app.route("/JIM")
def run_quiz_jim():
    user_selection = "JIM"
    quiz = quiz_script.get_quiz(user_selection)

    games_played.insert_one(quiz)

    return redirect("/")

@app.route("/PAM")
def run_quiz_pam():
    user_selection = "PAM"
    quiz = quiz_script.get_quiz(user_selection)

    games_played.insert_one(quiz)

    return redirect("/")

@app.route("/ANDY")
def run_quiz_andy():
    user_selection = "ANDY"
    quiz = quiz_script.get_quiz(user_selection)

    games_played.insert_one(quiz)

    return redirect("/")

@app.route("/Guess_real")
def update_guess_real():
    user_guess = 'Real'
    cursor = games_played.find().sort('_id',-1).limit(1)
    current_game = list(cursor)
    current_game_id = current_game[0]["_id"]
    right_answer = current_game[0]['Real_or_Fake']
    user_correct = ''

    if user_guess == right_answer:
        user_correct = 'True'
    else: 
        user_correct = 'False'

    games_played.update({"_id": current_game_id}, {"$set" : {'User_guess': user_guess, 'User_correct': user_correct}})


    

    return redirect("/")

@app.route("/Guess_fake")
def update_guess_fake():
    user_guess = 'Fake'
    cursor = games_played.find().sort('_id',-1).limit(1)
    current_game = list(cursor)
    current_game_id = current_game[0]["_id"]
    right_answer = current_game[0]['Real_or_Fake']
    user_correct = ''

    if user_guess == right_answer:
        user_correct = 'True'
    else: 
        user_correct = 'False'

    games_played.update({"_id": current_game_id}, {"$set" : {'User_guess': user_guess, 'User_correct': user_correct}})

    

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, threaded=False)

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, Question

app = Flask(__name__)
app.config['SECRET_KEY']='oh-so-secret'
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def go_home():
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions/<int:index>')
def get_question(index):

    if len(responses) == len(satisfaction_survey.questions):
        flash("You've already completed the survey!", 'success')
        return redirect('/thanks')
    elif index != len(responses):
        index = len(responses)
        flash('You cannot access that page!', 'error')
        return redirect(f'/questions/{index}')

    question = satisfaction_survey.questions[index]
    return render_template('questions.html', survey=satisfaction_survey, question=question, index=index)

@app.route('/answer', methods=['POST'])
def handle_post():
  
    answer = request.form['question']
    responses.append(answer)
    i = len(responses)

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{i}')
    else:
        return redirect('/thanks')

@app.route('/thanks')
def handle_thanks():
    return render_template('thanks.html',responses=responses)

# do an if len(response) less than list of questions, redirect to next q page, else redirect to thanks page
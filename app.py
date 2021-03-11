from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, surveys,  Question

app = Flask(__name__)
app.config['SECRET_KEY']='oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
# responses = []

@app.route('/')
def pick_survey():
    '''page displaying user the survey options'''
    return render_template('surveys.html', surveys=surveys)

@app.route('/survey', methods=['POST'])
def handle_survey():
    '''route handling the chosen survey'''
    survey_pick = request.form['survey']
    
    session['survey'] = survey_pick
    return redirect('/home')

@app.route('/home')
def go_home():
    '''renders the survey form, home page'''
    return render_template('home.html', survey=surveys[session['survey']])

@app.route('/session', methods=["POST"])
def start_survey():
    session['responses'] = []
    # responses[::] = []
    return redirect('/questions/0')

@app.route('/questions/<int:index>')
def get_question(index):
    '''directs user to next question, and handles any attempts at visiting pages user are not supposed to access'''
    responses = session['responses']
    if len(responses) == len(surveys[session['survey']].questions):
        session.pop('_flashes', None)
        flash("You've already completed the survey!", 'success')
        return redirect('/thanks')
    elif index != len(responses):
        index = len(responses)
        session.pop('_flashes', None)
        flash('You cannot access that page!', 'error')
        return redirect(f'/questions/{index}')

    question = surveys[session['survey']].questions[index]
    return render_template('questions.html', survey=surveys[session['survey']], question=question, index=index)


@app.route('/answer', methods=['POST'])
def handle_post():
    '''append answer given to responses, and redirect to next question, or thanks page'''
    answer = request.form['question']
    response_list = session['responses']
    response_list.append(answer)
    session['responses'] = response_list
    # responses.append(answer)
    i = len(response_list)

    if i < len(surveys[session['survey']].questions):
        return redirect(f'/questions/{i}')
    else:
        return redirect('/thanks')


@app.route('/thanks')
def handle_thanks():
    '''renders the thanks page'''
    return render_template('thanks.html', survey=surveys[session['survey']])

# do an if len(response) less than list of questions, redirect to next q page, else redirect to thanks page
from flask import Flask, request, render_template, redirect, flash, jsonify
from surveys import Question, Survey, surveys
from flask import session, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretsecret"


@app.route('/')
def home():
    my_surveys = surveys
    return render_template('home.html', surveys = my_surveys)


@app.route('/survey/<name>/setting-response', methods=['POST'])
def setting_responses(name):
    session['responses'] = []
    return redirect(f'/survey/{name}/questions/0')

@app.route('/survey/<name>/questions/<int:number>')
def questions(name, number):
    if  len(surveys[name].questions) == len(session.get('responses')):
        flash("Your survey has already been submitted, thank you!")
        return redirect(f'/survey/{name}/thanks')
    elif len(session.get('responses')) != number:
        flash("Please answer the questions in the assign sequence")
        return redirect (f'/survey/{name}/questions/{len(session.get('responses'))}')
    else: 
        title = surveys[name].title 
        instructions = surveys[name].instructions
        question = surveys[name].questions[number].question
        choices = surveys[name].questions[number].choices
        text = surveys[name].questions[number].allow_text
        return render_template('question.html', name=name, question= question, title = title, choices = choices, text=text, number=number)
    
@app.route('/survey/<name>/questions/<int:number>/answer', methods=['POST'])
def add_response(name, number):
    response = request.form['choice']
    responses = session['responses']
    responses.append(response)
    session['responses'] = responses
    if number == len(surveys[name].questions)-1:
        return redirect(f'/survey/{name}/thanks')
    else:
        return redirect(f'/survey/{name}/questions/{number+1}')

@app.route('/survey/<name>/thanks')
def thanks(name):
    title = surveys[name].title
    questions = list(surveys[name].questions)
    return render_template('thanks.html', title = title, questions = questions)


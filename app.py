from sys import meta_path
from flask import Flask, request, render_template, redirect, flash
from flask.wrappers import Response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

user_responses = []

@app.route("/")
def show_survey():
    """Show the survey question and instructions"""
    user_responses.clear()
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("survey.html", title=title, inst=instructions)


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def show_questions(num):
    """show the question according to the question number"""

    """if the number exceeds the number of the questions, 
    redirect the user to the home page"""
    if(num >= len(satisfaction_survey.questions)):
        flash(
            f"""Invalid question number. There are only 
            {len(satisfaction_survey.questions)} 
            questions for this survey"""
            )
        return redirect("/")

    """check if the user has completed all the questions in the survey"""
    if(len(user_responses) == len(satisfaction_survey.questions)):
        flash(f"You have completed all the questions")
        return redirect('/complete')

    question = satisfaction_survey.questions[int(num)].question
    choices = satisfaction_survey.questions[int(num)].choices

    return render_template(
        "questions.html",
        question=question,
        choices=choices)


@app.route("/answer", methods=["POST"])
def answer():
    """store answers"""
    ans = request.form["answer"]
    user_responses.append(ans)
    return redirect(f"/questions/{len(user_responses)}")


@app.route('/complete')
def complete():
    """show the complete page once the user finished the survey"""
    return render_template('complete.html')

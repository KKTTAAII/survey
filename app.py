from flask import Flask, request, render_template, redirect, flash
from flask.globals import session
from flask.wrappers import Response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/", methods=["GET", "POST"])
def select_survey():
    """the user can select a survey"""
    all_surveys = [survey for survey in surveys.keys()]
    return render_template("homepage.html", surveys=all_surveys)


@app.route("/session", methods = ["POST"])
def empty_session():
    session["responses"] = []
    session["current_survey"] = request.form["survey"]
    return redirect('/survey')


@app.route("/survey", methods=["GET", "POST"])
def show_survey():
    """Show the survey question and instructions"""
    selected_survey = session["current_survey"]
    title = surveys[selected_survey].title
    instructions = surveys[selected_survey].instructions
    return render_template("survey.html", title=title, inst=instructions, selected_survey=selected_survey)


@app.route("/answer", methods=["POST"])
def answer():
    """store answers"""
    ans = request.form["answer"]
    # session["responses"].append(ans)
    responses = session["responses"]
    responses.append(ans)
    session["responses"] = responses
    length = len(session["responses"])
    return redirect(f"/questions/{length}")


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def show_questions(num):
    """show the question according to the question number"""

    responses_length = len(session["responses"])

    """if the number exceeds the number of the questions, 
    redirect the user to the home page"""
    if(num > len(surveys[session["current_survey"]].questions)):
        flash(
            f"""Invalid question number. There are only 
            {len(surveys[session["current_survey"]].questions)} 
            questions for this survey"""
            , "error")
        return redirect("/")

    """prevent user from trying to answer the question
    in wrong order"""
    if(responses_length != num):
        return redirect(f"/questions/{responses_length}")

    """check if the user has completed all the questions in the survey"""
    if(responses_length == len(surveys[session["current_survey"]].questions)):
        flash("You have completed all the questions", "finished")
        return redirect('/complete')

    question = surveys[session["current_survey"]].questions[int(num)].question
    choices = surveys[session["current_survey"]].questions[int(num)].choices
    text_box = surveys[session["current_survey"]].questions[int(num)].allow_text
    
    if(responses_length == num):
        return render_template(
        "questions.html",
        question=question,
        choices=choices, text_box=text_box)


@app.route('/complete')
def complete():
    """show the complete page once the user finished the survey"""
    return render_template('complete.html')

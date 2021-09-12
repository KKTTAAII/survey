from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

user_responses = []
current_survey = []

@app.route("/")
def select_survey():
    """the user can select a survey"""
    all_surveys = [survey for survey in surveys.keys()]
    return render_template("homepage.html", surveys=all_surveys)

@app.route("/survey", methods=["GET", "POST"])
def show_survey():
    """Show the survey question and instructions"""
    user_responses.clear()
    current_survey.clear()
    selected_survey = request.args["survey"]
    current_survey.append(selected_survey)
    title = surveys[selected_survey].title
    instructions = surveys[selected_survey].instructions
    return render_template("survey.html", title=title, inst=instructions, selected_survey=selected_survey)


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def show_questions(num):
    """show the question according to the question number"""

    """if the number exceeds the number of the questions, 
    redirect the user to the home page"""
    if(num > len(surveys[current_survey[0]].questions)):
        flash(
            f"""Invalid question number. There are only 
            {len(surveys[current_survey[0]].questions)} 
            questions for this survey"""
            , "error")
        return redirect("/")

    """prevent user from trying to answer the question
    in wrong order"""
    if(len(user_responses) != num):
        return redirect(f"/questions/{len(user_responses)}")

    """check if the user has completed all the questions in the survey"""
    if(len(user_responses) == len(surveys[current_survey[0]].questions)):
        flash("You have completed all the questions", "finished")
        return redirect('/complete')

    question = surveys[current_survey[0]].questions[int(num)].question
    choices = surveys[current_survey[0]].questions[int(num)].choices
    text_box = surveys[current_survey[0]].questions[int(num)].allow_text

    return render_template(
        "questions.html",
        question=question,
        choices=choices, text_box=text_box)


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

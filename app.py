from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "SUPERSECRETKEY"



debug = DebugToolbarExtension(app)

@app.route("/")
def start_page():
    return render_template("start-survey.html")

@app.route("/begin")
def begin_servey():
    session["Responses"] = []
    session["ResponseCount"] = 0
    return redirect("/questions/0")


@app.route("/questions/<int:id>")
def show_questions(id):
    if (session["ResponseCount"] != id):
        flash(f"Invalid question id: {id}")    
        return redirect(f"/questions/{session['ResponseCount']}")
    else:
        return render_template("show_question", survey.questions[responsecount])


@app.route("/answer", methods=["POST"])
def answer_picked():

    session["ResponseCount"] += 1

    responses = session["Responses"]
    responses.append(request.form["answers"])
    session["Responses"] = responses
    if (session["SessionCount"] >= len(survey.questions)):
        redirect("/complete")
    else:
        redirect(f"/questions/{session['ResponseCount']}")

@app.route("/complete")
def complete():
    return render_template("complete_template.html")


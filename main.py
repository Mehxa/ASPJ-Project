from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import Forms

db = mysql.connector.connect(
    host="localhost",
    user="ASPJuser",
    password="P@55w0rD",
    database="blogdb"
)

mycursor =db.cursor()
mycursor.execute("SHOW TABLES")
print(mycursor)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    return redirect("/home")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html", currentPage="home")

@app.route("/feedback")
def feedback():
    feedbackForm = Forms.FeedbackForm(request.form)
    return render_template("feedback.html", currentPage="feedback",feedbackForm = feedbackForm)

if __name__ == "__main__":
    app.run(debug=True)

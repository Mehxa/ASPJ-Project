from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import Forms

db = mysql.connector.connect(
    host="localhost",
    user="ASPJuser",
    password="P@55w0rD",
    database="blogdb"
)

mycursor = db.cursor()
mycursor.execute("SHOW TABLES")
print(mycursor)

app = Flask(__name__)

tempPosts = {

}

@app.route('/')
def main():
    return redirect("/home")

@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html', currentPage='home')

@app.route('/viewPost')
def viewPost():
    return render_template('viewPost.html', currentPage='viewPost')

@app.route('/addPost', methods=["GET", "POST"])
def addPost():
    return render_template('addPost.html', currentPage='home')

@app.route('/feedback')
def feedback():
    feedbackForm = Forms.FeedbackForm(request.form)
    return render_template('feedback.html', currentPage='feedback', feedbackForm = feedbackForm)

@app.route('/login')
def login():
    loginForm = Forms.LoginForm(request.form)
    return render_template('login.html', currentPage='login', loginForm = loginForm)

@app.route('/signup')
def signUp():
    signUpForm = Forms.SignUpForm(request.form)
    return render_template('signup.html', currentPage='signUp', signUpForm = signUpForm)

if __name__ == "__main__":
    app.run(debug=True)

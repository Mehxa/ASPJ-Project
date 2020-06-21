from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, re
import Forms
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="ASPJuser",
    password="P@55w0rD",
    database="blogdb"
)

mycursor = db.cursor(buffered=True)
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

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    feedbackForm = Forms.FeedbackForm(request.form)

    if request.method == 'POST' and feedbackForm.validate():
        mycursor.execute('SELECT FeedbackID FROM feedback WHERE FeedbackID=(SELECT max(FeedbackID) FROM feedback)')
        lastIdRegistered = mycursor.fetchall()
        availId = lastIdRegistered[0][0] + 1
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO feedback (FeedbackID, UserID, Reason, Content, DateTimePosted) VALUES (%s, %s, %s, %s, %s)'
        # Need to link to current userID to work
        val = (availId, 1, feedbackForm.reason.data, feedbackForm.comment.data, dateTime)
        mycursor.execute(sql, val)
        db.commit()

    return render_template('feedback.html', currentPage='feedback', feedbackForm = feedbackForm)

@app.route('/login', methods=["GET", "POST"])
def login():
    loginForm = Forms.LoginForm(request.form)

    return render_template('login.html', currentPage='login', loginForm = loginForm)

@app.route('/signup', methods=["GET", "POST"])
def signUp():
    signUpForm = Forms.SignUpForm(request.form)

    if request.method == 'POST' and signUpForm.validate():
        if not(re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', signUpForm.email.data)):
            signUpForm.email.errors.append('Invalid email address.')
            pass

        mycursor.execute('SELECT UserID FROM user WHERE UserID=(SELECT max(UserID) FROM user)')
        lastIdRegistered = mycursor.fetchall()
        availId = lastIdRegistered[0][0] + 1
        sql = 'INSERT INTO user (UserID, Name, Email, Username, Password, isAdmin) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (availId, signUpForm.name.data, signUpForm.email.data, signUpForm.username.data, signUpForm.password.data, 0)
        try:
            mycursor.execute(sql, val)
            db.commit()

        except mysql.connector.errors.IntegrityError as errorMsg:
            errorMsg = str(errorMsg)
            if 'email' in errorMsg.lower():
                signUpForm.email.errors.append('The email has already been linked to another account. Please use a different email.')
            elif 'username' in errorMsg.lower():
                signUpForm.username.errors.append('This username is already taken.')

    return render_template('signup.html', currentPage='signUp', signUpForm = signUpForm)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

sessionInfo = {'login': False, 'currentUserID': 0, 'username': ''}
# sessionInfo = {'login': True, 'currentUserID': 7, 'username': 'johnnyjohnny'}

@app.route('/')
def main():
    return redirect("/home")

@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html', currentPage='home', **sessionInfo)

@app.route('/viewPost')
def viewPost():
    return render_template('viewPost.html', currentPage='viewPost', **sessionInfo)

@app.route('/addPost', methods=["GET", "POST"])
def addPost():
    if not sessionInfo['login']:
        return redirect('/login')

    sql = "SELECT TopicID, Content FROM topic ORDER BY Content"
    mycursor.execute(sql)
    listOfTopics = mycursor.fetchall()

    postForm = Forms.PostForm(request.form)
    postForm.topic.choices = listOfTopics

    if request.method == 'POST' and postForm.validate():
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO post (TopicID, UserID, DateTimePosted, Title, Content, Upvotes, Downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (postForm.topic.data, sessionInfo['currentUserID'], dateTime, postForm.title.data, postForm.content.data, 0, 0)
        mycursor.execute(sql, val)
        db.commit()
        flash('Post successfully created!', 'success')
        return redirect('/home')

    return render_template('addPost.html', currentPage='addPost', **sessionInfo, postForm=postForm)

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if not sessionInfo['login']:
        return redirect('/login')
    feedbackForm = Forms.FeedbackForm(request.form)

    if request.method == 'POST' and feedbackForm.validate():
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO feedback (UserID, Reason, Content, DateTimePosted) VALUES (%s, %s, %s, %s)'
        val = (sessionInfo['currentUserID'], feedbackForm.reason.data, feedbackForm.comment.data, dateTime)
        mycursor.execute(sql, val)
        db.commit()
        flash('Feedback sent!', 'success')
        return redirect('/feedback')

    return render_template('feedback.html', currentPage='feedback', **sessionInfo, feedbackForm = feedbackForm)

@app.route('/login', methods=["GET", "POST"])
def login():
    loginForm = Forms.LoginForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        sql = "SELECT UserID, Username FROM user WHERE Username=%s AND Password=%s"
        val = (loginForm.username.data, loginForm.password.data)
        mycursor.execute(sql, val)
        findUser = mycursor.fetchone()
        if findUser==None:
            loginForm.password.errors.append('Wrong email or password.')
        else:
            sessionInfo['login'] = True
            sessionInfo['currentUserID'] = int(findUser[0])
            sessionInfo['username'] = findUser[1]
            flash('Welcome! You are now logged in as %s.' %(sessionInfo['username']), 'success')
            return redirect('/home') # Change this later to redirect to profile page

    return render_template('login.html', currentPage='login', **sessionInfo, loginForm = loginForm)

@app.route('/logout')
def logout():
    sessionInfo['login'] = False
    sessionInfo['currentUser'] = 0
    sessionInfo['username'] = ''
    return redirect('/home')

@app.route('/signup', methods=["GET", "POST"])
def signUp():
    signUpForm = Forms.SignUpForm(request.form)

    if request.method == 'POST' and signUpForm.validate():
        if not(re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', signUpForm.email.data)):
            signUpForm.email.errors.append('Invalid email address.')

        sql = 'INSERT INTO user (Name, Email, Username, Password, isAdmin) VALUES (%s, %s, %s, %s, %s)'
        val = (signUpForm.name.data, signUpForm.email.data, signUpForm.username.data, signUpForm.password.data, 0)
        try:
            mycursor.execute(sql, val)
            db.commit()

        except mysql.connector.errors.IntegrityError as errorMsg:
            errorMsg = str(errorMsg)
            if 'email' in errorMsg.lower():
                signUpForm.email.errors.append('The email has already been linked to another account. Please use a different email.')
            elif 'username' in errorMsg.lower():
                signUpForm.username.errors.append('This username is already taken.')

        else:
            sql = "SELECT UserID, Username FROM user WHERE Username=%s AND Password=%s"
            val = (signUpForm.username.data, signUpForm.password.data)
            mycursor.execute(sql, val)
            findUser = mycursor.fetchone()
            sessionInfo['login'] = True
            sessionInfo['currentUserID'] = int(findUser[0])
            sessionInfo['username'] = findUser[1]

            flash('Account successfully created! You are now logged in as %s.' %(sessionInfo['username']), 'success')
            return redirect('/home')

    return render_template('signup.html', currentPage='signUp', **sessionInfo, signUpForm = signUpForm)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html', currentPage='myProfile', **sessionInfo)

if __name__ == "__main__":
    app.run(debug=True)

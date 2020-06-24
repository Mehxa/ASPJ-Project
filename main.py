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

tupleCursor = db.cursor(buffered=True)
dictCursor = db.cursor(buffered=True, dictionary=True)
tupleCursor.execute("SHOW TABLES")
print(tupleCursor)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

""" For testing purposes only. To make it convenient cause I can't remember all the account names.
Uncomment the account that you would like to use. To run the program as not logged in, run the first one."""
sessionInfo = {'login': False, 'currentUserID': 0, 'username': '', 'isAdmin': 0}
# sessionInfo = {'login': True, 'currentUserID': 1, 'username': 'NotABot', 'isAdmin': 1}
# sessionInfo = {'login': True, 'currentUserID': 2, 'username': 'CoffeeGirl', 'isAdmin': 1}
# sessionInfo = {'login': True, 'currentUserID': 3, 'username': 'Mexha', 'isAdmin': 1}
# sessionInfo = {'login': True, 'currentUserID': 4, 'username': 'Kobot', 'isAdmin': 1}
# sessionInfo = {'login': True, 'currentUserID': 5, 'username': 'MarySinceBirthButStillSingle', 'isAdmin': 0}
# sessionInfo = {'login': True, 'currentUserID': 6, 'username': 'theauthenticcoconut', 'isAdmin': 0}
# sessionInfo = {'login': True, 'currentUserID': 7, 'username': 'johnnyjohnny', 'isAdmin': 0}
# sessionInfo = {'login': True, 'currentUserID': 8, 'username': 'iamjeff', 'isAdmin': 0}
sessionInfo = {'login': True, 'currentUserID': 9, 'username': 'hanbaobao', 'isAdmin': 0}

@app.route('/')
def main():
    return redirect("/home")

@app.route('/home', methods=["GET"])
def home():
    sql = "SELECT post.PostID, post.Title, post.Content, post.Upvotes, post.Downvotes, post.DatetimePosted, user.Username, topic.Content AS Topic FROM post"
    sql += " INNER JOIN user ON post.UserID=user.UserID"
    sql += " INNER JOIN topic ON post.TopicID=topic.TopicID"
    sql += " ORDER BY post.PostID DESC LIMIT 6"

    dictCursor.execute(sql)
    recentPosts = dictCursor.fetchall()
    for post in recentPosts:
        post['TotalVotes'] = post['Upvotes'] - post['Downvotes']
        post['Content'] = post['Content'][:200]

    return render_template('home.html', currentPage='home', **sessionInfo, recentPosts = recentPosts)

@app.route('/viewPost/<int:postID>', methods=["GET", "POST"])
def viewPost(postID):
    if not sessionInfo['login']:
        return redirect('/login')

    sql = "SELECT post.Title, post.Content, post.Upvotes, post.Downvotes, post.DatetimePosted, user.Username, topic.Content AS Topic FROM post"
    sql += " INNER JOIN user ON post.UserID=user.UserID"
    sql += " INNER JOIN topic ON post.TopicID=topic.TopicID"
    sql += " WHERE PostID=" + str(postID)
    dictCursor.execute(sql)
    post = dictCursor.fetchone()
    post['TotalVotes'] = post['Upvotes'] - post['Downvotes']

    sql = "SELECT comment.CommentID, comment.Content, comment.DatetimePosted, comment.Upvotes, comment.Downvotes, comment.DatetimePosted, user.Username FROM comment"
    sql += " INNER JOIN user ON comment.UserID=user.UserID"
    sql += " WHERE comment.PostID=" + str(postID)
    dictCursor.execute(sql)
    commentList = dictCursor.fetchall()
    for comment in commentList:
        comment['TotalVotes'] = comment['Upvotes'] - comment['Downvotes']

        sql = "SELECT reply.Content, reply.DatetimePosted, reply.DatetimePosted, user.Username FROM reply"
        sql += " INNER JOIN user ON reply.UserID=user.UserID"
        sql += " WHERE reply.CommentID=" + str(comment['CommentID'])
        dictCursor.execute(sql)
        replyList = dictCursor.fetchall()
        comment['ReplyList'] = replyList

    commentForm = Forms.CommentForm(request.form)
    replyForm = Forms.ReplyForm(request.form)

    if request.method == 'POST' and commentForm.validate():
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO comment (PostID, UserID, RepliedID, Content, DateTimePosted, Upvotes, Downvotes) VALUES"
        sql += " ('" + str(postID) + "'"
        sql += " , '" + str(sessionInfo['currentUserID']) + "'"
        sql += " , '" + None + "'"
        sql += " , '" + commentForm.comment.data + "'"
        sql += " , '" + dateTime + "'"
        sql += " , 0, 0)"
        tupleCursor.execute(sql, val)
        db.commit()
        flash('Comment posted!', 'success')
        return redirect('/viewPost/%d' %postID)

    if request.method == 'POST' and replyForm.validate():
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO reply (UserID, CommentID, Content, DateTimePosted) VALUES"
        sql += " ('" + str(sessionInfo['currentUserID']) + "'"
        sql += " , '" + replyForm.repliedID.data + "'"
        sql += " , '" + replyForm.reply.data + "'"
        sql += " , '" + dateTime + "')"
        tupleCursor.execute(sql)
        db.commit()
        flash('Comment posted!', 'success')
        return redirect('/viewPost/%d' %postID)

    return render_template('viewPost.html', currentPage='viewPost', **sessionInfo, commentForm = commentForm, replyForm = replyForm, post = post, commentList = commentList)

@app.route('/addPost', methods=["GET", "POST"])
def addPost():
    if not sessionInfo['login']:
        return redirect('/login')

    sql = "SELECT TopicID, Content FROM topic ORDER BY Content"
    tupleCursor.execute(sql)
    listOfTopics = tupleCursor.fetchall()

    postForm = Forms.PostForm(request.form)
    postForm.topic.choices = listOfTopics

    if request.method == 'POST' and postForm.validate():
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO post (TopicID, UserID, DateTimePosted, Title, Content, Upvotes, Downvotes) VALUES'
        sql += " ('" + str(postForm.topic.data) + "'"
        sql += " , '" + str(sessionInfo['currentUserID']) + "'"
        sql += " , '" + dateTime + "'"
        sql += " , '" + postForm.title.data + "'"
        sql += " , '" + postForm.content.data + "'"
        sql += " , 0, 0)"
        tupleCursor.execute(sql)
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
        sql = 'INSERT INTO feedback (UserID, Reason, Content, DateTimePosted) VALUES'
        sql += " ('" + str(sessionInfo['currentUserID']) + "'"
        sql += " , '" + feedbackForm.reason.data + "'"
        sql += " , '" + feedbackForm.comment.data + "'"
        sql += " , '" + dateTime + "')"
        tupleCursor.execute(sql)
        db.commit()
        flash('Feedback sent!', 'success')
        return redirect('/feedback')

    return render_template('feedback.html', currentPage='feedback', **sessionInfo, feedbackForm = feedbackForm)

@app.route('/login', methods=["GET", "POST"])
def login():
    loginForm = Forms.LoginForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        sql = "SELECT UserID, Username, isAdmin FROM user WHERE"
        sql += " Username='" + loginForm.username.data + "'"
        sql += " AND Password='" + loginForm.password.data + "'"
        dictCursor.execute(sql)
        findUser = dictCursor.fetchone()
        if findUser==None:
            loginForm.password.errors.append('Wrong email or password.')
        else:
            sessionInfo['login'] = True
            sessionInfo['currentUserID'] = int(findUser['UserID'])
            sessionInfo['username'] = findUser['Username']
            sessionInfo['isAdmin'] = findUser['isAdmin']
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
        sql = "INSERT INTO user (Email, Username, Name, Birthday, Password, isAdmin) VALUES"
        sql += " ('" + signUpForm.email.data + "'"
        sql += " , '" + signUpForm.username.data + "'"
        sql += " , '" + signUpForm.name.data + "'"
        sql += " , '" + str(signUpForm.dob.data) + "'"
        sql += " , '" + signUpForm.password.data + "'"
        sql += " , '0')"
        try:
            tupleCursor.execute(sql)
            db.commit()

        except mysql.connector.errors.IntegrityError as errorMsg:
            errorMsg = str(errorMsg)
            if 'email' in errorMsg.lower():
                signUpForm.email.errors.append('The email has already been linked to another account. Please use a different email.')
            elif 'username' in errorMsg.lower():
                signUpForm.username.errors.append('This username is already taken.')

        else:
            sql = "SELECT UserID, Username FROM user WHERE"
            sql += " Username='" + signUpForm.username.data + "'"
            sql += " AND Password='" + signUpForm.password.data + "'"
            tupleCursor.execute(sql)
            findUser = tupleCursor.fetchone()
            sessionInfo['login'] = True
            sessionInfo['currentUserID'] = int(findUser[0])
            sessionInfo['username'] = findUser[1]

            flash('Account successfully created! You are now logged in as %s.' %(sessionInfo['username']), 'success')
            return redirect('/home')

    return render_template('signup.html', currentPage='signUp', **sessionInfo, signUpForm = signUpForm)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html', currentPage='myProfile', **sessionInfo)

@app.route('/adminHome')
def adminHome():
    return render_template('adminHome.html', currentPage='adminHome', **sessionInfo)

@app.route('/adminTopics')
def adminTopics():
    # uncomment from here
    # sql = "SELECT TopicID, Content FROM topic ORDER BY Content"
    # tupleCursor.execute(sql)
    # listOfTopics = tupleCursor.fetchall()
    return render_template('adminTopics.html', currentPage='adminTopics', **sessionInfo, listOfTopics=listOfTopics)

@app.route('/addTopic', methods=["GET", "POST"])
def addTopic():
    # uncomment here
    # if not sessionInfo['login']:
        # return redirect('/login')
    # til here
    # sql = "SELECT TopicID, Content FROM topic ORDER BY Content"
    # tupleCursor.execute(sql)
    # listOfTopics = tupleCursor.fetchall()

    # uncomment here topicForm = Forms.TopicForm(request.form)
    # topicForm.topic.choices = listOfTopics
    # uncomment here
    # if request.method == 'POST' and postForm.validate():
    #     dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    #     sql = 'INSERT INTO topic (TopicID, UserID, Content, DateTimePosted) VALUES (%s, %s, %s, %s)'
    #     val = ("need to generate?", sessionInfo['currentUserID'],topicForm.topic.data, dateTime)
    #     tupleCursor.execute(sql, val)
    #     db.commit()
    #     flash('Topic successfully created!', 'success')
    #     return redirect('/adminHome')
        # till here


    return render_template('addTopic.html', currentPage='addTopic', **sessionInfo, topicForm=topicForm)

@app.route('/adminUsers')
def adminUsers():
    return render_template('adminUsers.html', currentPage='adminUsers', **sessionInfo)
if __name__ == "__main__":
    app.run(debug=True)

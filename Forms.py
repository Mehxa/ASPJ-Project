from wtforms import Form, validators, StringField, TextAreaField, PasswordField

class FeedbackForm(Form):
    firstName = StringField("First Name", [validators.DataRequired()], render_kw={"placeholder": "Alice"})
    lastName = StringField("Last Name", [validators.DataRequired()], render_kw={"placeholder": "Tan"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"placeholder": "alicetan@email.com"})
    comment = TextAreaField('Comment', [validators.DataRequired()], render_kw={"rows": 5, "placeholder": "Enter comment here..."})

class LoginForm(Form):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class SignUpForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"placeholder": "alicetan@email.com"})
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmPassword', message='Passwords do not match.')
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired()])

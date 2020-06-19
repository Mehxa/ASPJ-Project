from wtforms import Form, validators, StringField, TextAreaField

class FeedbackForm(Form):
    firstName = StringField("First Name", [validators.DataRequired()], render_kw={"placeholder": "Alice"})
    lastName = StringField("Last Name", [validators.DataRequired()], render_kw={"placeholder": "Tan"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"placeholder": "alicetan@email.com"})
    comment = TextAreaField('Comment', [validators.DataRequired()], render_kw={"rows": 5, "placeholder": "Enter comment here..."})

from flask_wtf import FlaskForm, csrf
from wtforms import HiddenField, StringField, TextAreaField, SelectField, PasswordField, RadioField, BooleanField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Email, Length

# feedback form just based around email, title and message
class FeedbackForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    title = SelectField('Your Title', choices=[
        ('Dr', 'Dr.'),
        ('Professor', 'Prof.'),
        ('Mr', 'Mr.'),
        ('Ms', 'Miss'),
        ('Mrs', 'Mrs.')
    ], validators=[DataRequired()])
    service_preference = RadioField('Preference for Services:', choices=[
        ('online', 'Online/Digital'),
        ('offline', 'Face 2 Face'),
        ('hybrid', 'Hybrid')
    ], validators=[DataRequired()])
    area_interest_1 = BooleanField('Mobile Dev')
    area_interest_2 = BooleanField('Software Dev')
    area_interest_3 = BooleanField('Web App Dev')
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=100)])
    message = TextAreaField('Your Feedback', validators=[DataRequired(), Length(min=10, max=600)])
    submit = SubmitField('Send Feedback')

# log in form for authentication purposes
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')

# a special form for collecting ratings on staff members using the drag+drop and hidden field technique
class StaffRateForm(FlaskForm):
    staff_rating = HiddenField('Staff Rating')
    submit = SubmitField('Send My Ratings')

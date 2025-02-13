from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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
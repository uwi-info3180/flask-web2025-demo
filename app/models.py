from . import db

class Feedbacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(280), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    service_preference = db.Column(db.String(120), nullable=True)
    area_interest = db.Column(db.String(320), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, email, title, srv, interest, subj, msg):
        self.email = email
        self.title = title
        self.service_preference = srv
        self.area_interest = interest
        self.subject = subj
        self.message = msg

    def __repr__(self):
        return f'<Feedback from {self.email}>'

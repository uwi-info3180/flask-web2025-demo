from . import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

class StaffRating(db.Model):
    # Uncomment the line below if you want to set your own table name
    __tablename__ = "staff_ratings"

    id = db.Column(db.Integer, primary_key=True)
    rater_fk = db.Column(db.Integer, nullable=False)
    rated_name = db.Column(db.String(110), nullable=False)
    rated_value = db.Column(db.Integer, nullable=False)
    rated_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def __init__(self, rater_fk, rated_name, rated_value):
        self.rater_fk = rater_fk
        self.rated_name = rated_name
        self.rated_value = rated_value

    def __repr__(self):
        return f'<Rating from {self.rater_fk} on {self.rated_name}>'

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

class User(db.Model):
    # Uncomment the line below if you want to set your own table name
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(280), unique=True, nullable=False)
    alias = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(255))

    def __init__(self, username, email, alias, password):
        self.username = username
        self.email = email
        self.alias = alias
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return f'<User {self.username}>'


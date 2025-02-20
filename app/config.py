import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SHOW_FOOTER_DATE = os.environ.get('SHOW_FOOTER_DATE', False)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed

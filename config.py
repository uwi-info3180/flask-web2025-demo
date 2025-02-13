import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SHOW_FOOTER_DATE = os.environ.get('SHOW_FOOTER_DATE', False)

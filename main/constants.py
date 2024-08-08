from dotenv import load_dotenv
import os

load_dotenv()

SMS_ACTIVATE_KEY = os.getenv("SMS_ACTIVATE_KEY")
RUCAPTCHA_KEY = os.getenv("RUCAPTCHA_KEY")
PROXY = os.getenv("PROXY")
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True
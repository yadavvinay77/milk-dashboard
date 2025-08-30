import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "milk_dashboard.db")
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    DEFAULT_MILK_RATE = 190.0
    DEFAULT_KHOYA_RATE = 310.0
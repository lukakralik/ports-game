import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    DB_URI = os.environ.get('DATABASE_URI')

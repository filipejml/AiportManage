import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_muito_segura'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456789@localhost/airport_manager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    #Any other existing configurations

from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['UPLOAD_FOLDER'] = 'app/static/profiles'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://info3180proj1:project1@104.154.72.189:5432/info3180proj1?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from app import views
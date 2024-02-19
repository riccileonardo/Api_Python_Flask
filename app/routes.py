from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token
from . import db
from .models import User, TrilhaAprendizado, Curso, Aula, Comentario, Avaliacao, engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'yjDoz89830-6062uNjeWkAfHu7s3NAlI'
jwt = JWTManager(app)

bp = Blueprint('bp', __name__)
Session = sessionmaker(bind=engine)
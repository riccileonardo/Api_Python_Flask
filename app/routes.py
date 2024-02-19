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

# User
@bp.route('/api/users/registro', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing data'}), 400

    try:
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User with this username or email already exists'}), 409

@bp.route('/api/users/login', methods=['POST'])
def login_usuario():
    pass

@bp.route('/api/users/<int:id_user>', methods=['PUT'])
def editar_usuario(id_user):
    pass

@bp.route('/api/users/<int:id_user>', methods=['DELETE'])
def deletar_usuario(id_user):
    pass

@bp.route('/api/users', methods=['GET'])
def visualizar_todos_usuarios():
    pass

@bp.route('/api/users/<int:id_user>', methods=['GET'])
def visualizar_usuario_especifico(id_user):
    pass

# Curso
@bp.route('/api/cursos', methods=['POST'])
def cadastro_curso():
    pass

@bp.route('/api/cursos/<int:id_curso>', methods=['PUT'])
def editar_curso(id_curso):
    pass

@bp.route('/api/cursos', methods=['GET'])
def visualizar_todos_cursos():
    pass

@bp.route('/api/cursos/<int:id_curso>', methods=['GET'])
def visualizar_curso_especifico(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>', methods=['DELETE'])
def deletar_curso(id_curso):
    pass

# Aula
@bp.route('/api/cursos/<int:id_curso>/aulas', methods=['POST'])
def cadastrar_aula(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['PUT'])
def atualizar_aula(id_curso, id_aula):
    pass

@bp.route('/api/cursos/<int:id_curso>/aulas', methods=['GET'])
def visualizar_todas_aulas(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['GET'])
def visualizar_aula_especifica(id_curso, id_aula):
    pass

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['DELETE'])
def deletar_aula(id_curso, id_aula):
    pass

# Comentário
@bp.route('/api/cursos/<int:id_curso>/comentarios', methods=['POST'])
def cadastrar_comentario(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/comentarios/<int:id_comentario>', methods=['PUT'])
def editar_comentario(id_curso, id_comentario):
    pass

@bp.route('/api/cursos/<int:id_curso>/comentarios', methods=['GET'])
def visualizar_todos_comentarios(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/comentarios/<int:id_comentario>', methods=['DELETE'])
def deletar_comentario(id_curso, id_comentario):
    pass

# Avaliação
@bp.route('/api/cursos/<int:id_curso>/avaliacoes', methods=['POST'])
def cadastrar_avaliacao(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['PUT'])
def atualizar_avaliacao(id_curso, id_avaliacao):
    pass

@bp.route('/api/cursos/<int:id_curso>/avaliacoes', methods=['GET'])
def visualizar_todas_avaliacoes(id_curso):
    pass

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['GET'])
def visualizar_avaliacao_especifica(id_curso, id_avaliacao):
    pass

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['DELETE'])
def deletar_avaliacao(id_curso, id_avaliacao):
    pass

# Trilha de Aprendizado
@bp.route('/api/trilhas-aprendizado', methods=['POST'])
def cadastrar_trilha():
    pass

@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['PUT'])
def atualizar_trilha(id_trilha):
    pass

@bp.route('/api/trilhas-aprendizado', methods=['GET'])
def visualizar_todas_trilhas():
    pass

@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['GET'])
def visualizar_trilha_especifica(id_trilha):
    pass

@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['DELETE'])
def deletar_trilha(id_trilha):
    pass
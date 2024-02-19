from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

#IMPORTANTE
#VERFICAR COMO FAZER O LOGOUT

@bp.route('/api/users/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    session = Session()
    data = request.get_json()

    try:
        user = session.query(User).get(id_user)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        session.commit()

        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar o usuário', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    session = Session()

    try:
        user = session.query(User).get(id_user)

        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        session.delete(user)
        session.commit()

        return jsonify({'message': 'Usuário deletado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao deletar o usuário', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/users', methods=['GET'])
def visualizar_todos_usuarios():
    session = Session()

    try:
        users = session.query(User).all()
        return jsonify([user.serialize() for user in users]), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar os usuários', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/users/<int:id_user>', methods=['GET'])
def visualizar_usuario_especifico(id_user):
    session = Session()

    try:
        user = session.query(User).get(id_user)

        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return jsonify(user.serialize()), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar o usuário', 'message': str(e)}), 500
    finally:
        session.close()

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
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
        serialized_users = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify(serialized_users), 200

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
def criar_curso():
    session = Session()
    data = request.get_json()
    
    if not data or 'nome' not in data or 'descricao' not in data:
        session.close()
        return jsonify({'error': 'Dados necessários para a criação do curso estão faltando.'}), 400
    
    try:
        curso = Curso(nome=data['nome'], descricao=data['descricao'])
        
        session.add(curso)
        session.commit()
        
        return jsonify({'message': 'Curso criado com sucesso', 'curso_id': curso.id}), 201
    except IntegrityError as e:

        session.rollback()
        return jsonify({'error': 'Erro ao criar o curso', 'message': str(e)}), 500
    finally:

        session.close()

@bp.route('/api/cursos/<int:id_curso>', methods=['PUT'])
def atualizar_curso(id_curso):
    session = Session()
    data = request.get_json()

    try:
        curso = session.query(Curso).get(id_curso)

        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        for key, value in data.items():
            setattr(curso, key, value)
        session.commit()

        return jsonify({'message': 'Curso atualizado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar o curso', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos', methods=['GET'])
def visualizar_todos_cursos():
    session = Session()

    try:
        cursos = session.query(Curso).all()
        return jsonify([curso.serialize() for curso in cursos]), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar os cursos', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>', methods=['GET'])
def visualizar_curso_especifico(id_curso):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)

        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        return jsonify(curso.serialize()), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar o curso', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>', methods=['DELETE'])
def deletar_curso(id_curso):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)

        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        session.delete(curso)
        session.commit()

        return jsonify({'message': 'Curso deletado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao deletar o curso', 'message': str(e)}), 500
    finally:
        session.close()


@bp.route('/api/cursos/<int:id_curso>/aulas', methods=['POST'])
def add_aula_to_curso(id_curso):
    session = Session()
    data = request.get_json()

    curso = session.query(Curso).get(id_curso)
    if not curso:
        session.close()
        return jsonify({'error': 'Curso não encontrado'}), 404

    nova_aula = Aula(
        nome=data.get('nome'),
        descricao=data.get('descricao'),
        curso_id=id_curso  
    )

    try:
        session.add(nova_aula)
        session.commit()
        return jsonify({'message': 'Aula adicionada com sucesso ao curso', 'aula_id': nova_aula.id}), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao adicionar a aula ao curso', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['PUT'])
def atualizar_aula(id_curso, id_aula):
    session = Session()
    data = request.get_json()

    try:
        aula = session.query(Aula).get(id_aula)

        if not aula:
            return jsonify({'error': 'Aula não encontrada'}), 404

        for key, value in data.items():
            setattr(aula, key, value)
        session.commit()

        return jsonify({'message': 'Aula atualizada com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar a aula', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/aulas', methods=['GET'])
def visualizar_todas_aulas(id_curso):
    session = Session()

    try:
        aulas = session.query(Aula).filter_by(curso_id=id_curso).all()
        return jsonify([aula.serialize() for aula in aulas]), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar as aulas', 'message': str(e)}), 500
    finally:
        session.close()


@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['GET'])
def obter_aula(id_curso, id_aula):
    session = Session()

    curso = session.query(Curso).filter_by(id=id_curso).first()
    if curso is None:
        return jsonify({'error': 'Curso não encontrado'}), 404

    aula = session.query(Aula).filter_by(id=id_aula, curso_id=id_curso).first()
    if aula is None:
        return jsonify({'error': 'Aula não encontrada neste curso'}), 404

    return jsonify({
        'id': aula.id,
        'nome': aula.nome,
        'descricao': aula.descricao,
        'curso_id': aula.curso_id
    }), 200


@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['DELETE'])
def deletar_aula(id_curso, id_aula):
    session = Session()

    try:
        aula = session.query(Aula).get(id_aula)

        if not aula:
            return jsonify({'error': 'Aula não encontrada'}), 404

        session.delete(aula)
        session.commit()

        return jsonify({'message': 'Aula deletada com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao deletar a aula', 'message': str(e)}), 500
    finally:
        session.close()

# Comentário
@bp.route('/api/cursos/<int:id_curso>/comentarios', methods=['POST'])
def add_comentario_to_curso(id_curso):
    session = Session()
    data = request.get_json()

    curso = session.query(Curso).get(id_curso)
    if not curso:
        session.close()
        return jsonify({'error': 'Curso não encontrado'}), 404

    novo_comentario = Comentario(
        descricao=data.get('descricao'),
        curso_id=id_curso,
        user_id=data.get('user_id')
    )

    try:
        session.add(novo_comentario)
        session.commit()
        return jsonify({'message': 'Comentário adicionado com sucesso ao curso', 'comentario_id': novo_comentario.id}), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao adicionar o comentário ao curso', 'message': str(e)}), 500
    finally:
        session.close()


@bp.route('/api/cursos/<int:id_curso>/comentarios/<int:id_comentario>', methods=['PUT'])
def atualizar_comentario(id_curso, id_comentario):
    session = Session()
    data = request.get_json()

    try:
        
        comentario = session.query(Comentario).filter(Comentario.id == id_comentario, Comentario.curso_id == id_curso).first()
        
        if not comentario:
            session.close()
            return jsonify({'error': 'Comentário não encontrado ou não pertence ao curso especificado.'}), 404

        
        if 'descricao' in data:
            comentario.descricao = data['descricao']
        
        session.commit()
        return jsonify({'message': 'Comentário atualizado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar o comentário', 'message': str(e)}), 500
    finally:
        session.close()


@bp.route('/api/cursos/<int:id_curso>/comentarios', methods=['GET'])
def listar_comentarios_curso(id_curso):
    session = Session()

    try:
        # Verifica se o curso existe
        curso = session.query(Curso).get(id_curso)
        if not curso:
            session.close()
            return jsonify({'error': 'Curso não encontrado'}), 404

        # Busca todos os comentários associados ao curso
        comentarios = session.query(Comentario).filter(Comentario.curso_id == id_curso).all()
        
        # Converte a lista de comentários para um formato JSON
        comentarios_json = [{'id': comentario.id, 'descricao': comentario.descricao, 'user_id': comentario.user_id} for comentario in comentarios]
        
        return jsonify(comentarios_json), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao listar comentários', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/comentarios/<int:id_comentario>', methods=['DELETE'])
def deletar_comentario_curso(id_curso, id_comentario):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        comentario = session.query(Comentario).filter(Comentario.id == id_comentario, Comentario.curso_id == id_curso).first()
        if not comentario:
            return jsonify({'error': 'Comentário não encontrado'}), 404

        session.delete(comentario)
        session.commit()

        return jsonify({'message': 'Comentário deletado com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao deletar o comentário', 'message': str(e)}), 500
    finally:
        session.close()

# Avaliação
@bp.route('/api/cursos/<int:id_curso>/avaliacoes', methods=['POST'])
def adicionar_avaliacao(id_curso):
    session = Session()
    data = request.get_json()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        nova_avaliacao = Avaliacao(curso_id=id_curso, **data)
        
        session.add(nova_avaliacao)
        session.commit()

        return jsonify({'message': 'Avaliação adicionada com sucesso', 'avaliacao_id': nova_avaliacao.id}), 201

    except IntegrityError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao adicionar avaliação', 'message': str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Erro ao processar sua solicitação', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['PUT'])
def atualizar_avaliacao(id_curso, id_avaliacao):
    session = Session()
    data = request.get_json()

    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, curso_id=id_curso).first()
        if not avaliacao:
            return jsonify({'error': 'Avaliação ou Curso não encontrado'}), 404

        for chave, valor in data.items():
            if hasattr(avaliacao, chave):
                setattr(avaliacao, chave, valor)

        session.commit()
        return jsonify({'message': 'Avaliação atualizada com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar avaliação', 'message': str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Erro ao processar sua solicitação', 'message': str(e)}), 500
    finally:
        session.close()


@bp.route('/api/cursos/<int:id_curso>/avaliacoes', methods=['GET'])
def listar_avaliacoes(id_curso):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        avaliacoes = session.query(Avaliacao).filter_by(curso_id=id_curso).all()
        
        avaliacoes_data = [{'id': avaliacao.id, 'nota': avaliacao.nota, 'comentario': avaliacao.comentario} for avaliacao in avaliacoes]

        return jsonify(avaliacoes_data), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao processar sua solicitação', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['GET'])
def buscar_avaliacao_especifica(id_curso, id_avaliacao):
    session = Session()
    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, curso_id=id_curso).first()
        if avaliacao:
            return jsonify(avaliacao.to_dict()), 200
        else:
            return jsonify({'message': 'Avaliação não encontrada'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar a avaliação', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['DELETE'])
def deletar_avaliacao(id_curso, id_avaliacao):
    session = Session()
    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, curso_id=id_curso).first()
        if avaliacao:
            session.delete(avaliacao)
            session.commit()
            return jsonify({'message': 'Avaliação deletada com sucesso'}), 200
        else:
            return jsonify({'error': 'Avaliação não encontrada'}), 404
    except SQLAlchemyError as e:

        session.rollback()  
        return jsonify({'error': 'Erro ao deletar a avaliação', 'message': str(e)}), 500
    finally:

        session.close()

# Trilha de Aprendizado
@bp.route('/api/trilhas-aprendizado', methods=['POST'])
def adicionar_trilha_aprendizado():
    session = Session()
    data = request.get_json()

    if 'nome' not in data or 'descricao' not in data:
        return jsonify({'error': 'Dados incompletos para a criação da trilha de aprendizado.'}), 400

    try:
        nova_trilha = TrilhaAprendizado(nome=data['nome'], descricao=data['descricao'])
        session.add(nova_trilha)
        session.commit()  
        return jsonify({
            'message': 'Trilha de aprendizado criada com sucesso',
            'trilha_id': nova_trilha.id
        }), 201

    except SQLAlchemyError as e:
        session.rollback()  
        return jsonify({'error': 'Erro ao criar a trilha de aprendizado', 'message': str(e)}), 500

    finally:
        session.close() 

@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['PUT'])
def atualizar_trilha_aprendizado(id_trilha):
    session = Session()
    data = request.get_json()

    trilha = session.query(TrilhaAprendizado).get(id_trilha)
    if not trilha:
        return jsonify({'error': 'Trilha de aprendizado não encontrada.'}), 404

    if 'nome' in data:
        trilha.nome = data['nome']
    if 'descricao' in data:
        trilha.descricao = data['descricao']

    try:
        session.commit() 
        return jsonify({
            'message': 'Trilha de aprendizado atualizada com sucesso',
            'trilha_id': trilha.id
        }), 200

    except SQLAlchemyError as e:
        session.rollback() 
        return jsonify({'error': 'Erro ao atualizar a trilha de aprendizado', 'message': str(e)}), 500

    finally:
        session.close()


@bp.route('/api/trilhas-aprendizado', methods=['GET'])
def listar_trilhas_aprendizado():
    session = Session()
    try:
        trilhas = session.query(TrilhaAprendizado).all()

        trilhas_lista = [{'id': trilha.id, 'nome': trilha.nome, 'descricao': trilha.descricao} for trilha in trilhas]
        
        return jsonify(trilhas_lista), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar trilhas de aprendizado', 'message': str(e)}), 500

    finally:
        session.close()


@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['GET'])
def obter_trilha_aprendizado(id_trilha):
    session = Session()
    try:
        trilha = session.query(TrilhaAprendizado).filter_by(id=id_trilha).first()

        if trilha is None:
            return jsonify({'error': 'Trilha de aprendizado não encontrada'}), 404
        
        trilha_data = {
            'id': trilha.id,
            'nome': trilha.nome,
            'descricao': trilha.descricao
        }
        
        return jsonify(trilha_data), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar trilha de aprendizado', 'message': str(e)}), 500

    finally:
        session.close()

@bp.route('/api/trilhas-aprendizado/<int:id_trilha>', methods=['DELETE'])
def deletar_trilha_aprendizado(id_trilha):
    session = Session()
    try:
        trilha = session.query(TrilhaAprendizado).filter_by(id=id_trilha).first()

        if trilha is None:
            return jsonify({'error': 'Trilha de aprendizado não encontrada'}), 404

        session.delete(trilha)
        session.commit()
        
        return jsonify({'message': 'Trilha de aprendizado deletada com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback() 
        return jsonify({'error': 'Erro ao deletar trilha de aprendizado', 'message': str(e)}), 500

    finally:
        session.close()
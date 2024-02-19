from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
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
    session = Session()
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        session.close()
        return jsonify({'error': 'Missing data'}), 400

    try:
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        session.add(new_user)
        session.commit()
        access_token = create_access_token(identity=new_user.id)
        session.close()
        return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201

    except IntegrityError:
        session.rollback()
        session.close()
        return jsonify({'error': 'User with this username or email already exists'}), 409

@bp.route('/api/users/login', methods=['POST'])
def login():
    session = Session()
    data = request.get_json()
    user = session.query(User).filter_by(username=data.get('username')).first()

    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user.id)
        session.close()
        return jsonify(access_token=access_token), 200
    else:
        session.close()
        return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/api/users/<int:id_user>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def add_aula_to_curso(id_curso):
    session = Session()
    data = request.get_json()

    curso = session.query(Curso).get(id_curso)
    if not curso:
        session.close()
        return jsonify({'error': 'Curso não encontrado'}), 404

    nova_aula = Aula(
        titulo=data.get('titulo'),
        descricao=data.get('descricao'),
        id_curso=id_curso,
        duracao=data.get('duracao')  
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
@jwt_required()
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
@jwt_required()
def visualizar_todas_aulas(id_curso):

    session = Session()

    try:
        aulas = session.query(Aula).filter_by(id_curso=id_curso).all()
        return jsonify([aula.serialize() for aula in aulas]), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar as aulas', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['GET'])
@jwt_required()
def obter_aula(id_curso, id_aula):
    session = Session()

    curso = session.query(Curso).filter_by(id=id_curso).first()
    if curso is None:
        return jsonify({'error': 'Curso não encontrado'}), 404

    aula = session.query(Aula).filter_by(id=id_aula, id_curso=id_curso).first()
    if aula is None:
        return jsonify({'error': 'Aula não encontrada neste curso'}), 404

    return jsonify({
        'id': aula.id,
        'titulo': aula.titulo,
        'descricao': aula.descricao,
        'id_curso': aula.id_curso
    }), 200

@bp.route('/api/cursos/<int:id_curso>/aulas/<int:id_aula>', methods=['DELETE'])
@jwt_required()
def deletar_aula(id_curso, id_aula):
    session = Session()

    curso = session.query(Curso).filter_by(id=id_curso).first()
    if curso is None:
        return jsonify({'error': 'Curso não encontrado'}), 404

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
@jwt_required()
def add_comentario_to_curso(id_curso):
    session = Session()
    data = request.get_json()

    curso = session.query(Curso).get(id_curso)
    if not curso:
        session.close()
        return jsonify({'error': 'Curso não encontrado'}), 404

    novo_comentario = Comentario(
        descricao=data.get('descricao'),
        id_curso=id_curso,
        id_user=data.get('id_user')
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
@jwt_required()
def atualizar_comentario(id_curso, id_comentario):
    session = Session()
    data = request.get_json()

    try:
        
        comentario = session.query(Comentario).filter(Comentario.id == id_comentario, Comentario.id_curso == id_curso).first()
        
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
@jwt_required()
def listar_comentarios_curso(id_curso):
    session = Session()

    try:
        # Verifica se o curso existe
        curso = session.query(Curso).get(id_curso)
        if not curso:
            session.close()
            return jsonify({'error': 'Curso não encontrado'}), 404

        # Busca todos os comentários associados ao curso
        comentarios = session.query(Comentario).filter(Comentario.id_curso == id_curso).all()
        
        # Converte a lista de comentários para um formato JSON
        comentarios_json = [{'id': comentario.id, 'descricao': comentario.descricao, 'id_user': comentario.id_user} for comentario in comentarios]
        
        return jsonify(comentarios_json), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao listar comentários', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/comentarios/<int:id_comentario>', methods=['DELETE'])
@jwt_required()
def deletar_comentario_curso(id_curso, id_comentario):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        comentario = session.query(Comentario).filter(Comentario.id == id_comentario, Comentario.id_curso == id_curso).first()
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
@jwt_required()
def adicionar_avaliacao(id_curso):
    session = Session()
    data = request.get_json()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        nova_avaliacao = Avaliacao(id_curso=id_curso, **data)
        
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
@jwt_required()
def atualizar_avaliacao(id_curso, id_avaliacao):
    session = Session()
    data = request.get_json()

    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, id_curso=id_curso).first()
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
@jwt_required()
def listar_avaliacoes(id_curso):
    session = Session()

    try:
        curso = session.query(Curso).get(id_curso)
        if not curso:
            return jsonify({'error': 'Curso não encontrado'}), 404

        avaliacoes = session.query(Avaliacao).filter_by(id_curso=id_curso).all()
        
        avaliacoes_data = [{'id': avaliacao.id, 'avaliacao': avaliacao.avaliacao, 'comentario': avaliacao.comentario} for avaliacao in avaliacoes]

        return jsonify(avaliacoes_data), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao processar sua solicitação', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['GET'])
@jwt_required()
def buscar_avaliacao_especifica(id_curso, id_avaliacao):
    session = Session()
    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, id_curso=id_curso).first()
        if avaliacao:
            return jsonify(avaliacao.serialize()), 200
        else:
            return jsonify({'message': 'Avaliação não encontrada'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar a avaliação', 'message': str(e)}), 500
    finally:
        session.close()

@bp.route('/api/cursos/<int:id_curso>/avaliacoes/<int:id_avaliacao>', methods=['DELETE'])
@jwt_required()
def deletar_avaliacao(id_curso, id_avaliacao):
    session = Session()
    try:
        avaliacao = session.query(Avaliacao).filter_by(id=id_avaliacao, id_curso=id_curso).first()
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
@jwt_required()
def adicionar_trilha_aprendizado():
    session = Session()
    data = request.get_json()

    if 'nome' not in data or 'descricao' not in data:
        return jsonify({'error': 'Dados incompletos para a criação da trilha de aprendizado.'}), 400

    try:
        nova_trilha = TrilhaAprendizado(nome=data['nome'], descricao=data['descricao'])
        for id_curso in data['cursos']:
            curso = session.query(Curso).get(id_curso)
            if curso:
                nova_trilha.cursos.append(curso)
            else:
                return jsonify({'error': f'Curso com ID {id_curso} não encontrado.'}), 400

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

@bp.route('/api/trilhas-aprendizado/<int:trilha_id>', methods=['PUT'])
@jwt_required()
def atualizar_trilha_aprendizado(trilha_id):
    session = Session()
    data = request.get_json()

    if 'nome' not in data and 'descricao' not in data and 'cursos' not in data:
        return jsonify({'error': 'Nenhum dado fornecido para atualização.'}), 400

    trilha = session.query(TrilhaAprendizado).get(trilha_id)
    if trilha is None:
        return jsonify({'error': 'Trilha de aprendizado não encontrada.'}), 404

    try:
        if 'nome' in data:
            trilha.nome = data['nome']
        if 'descricao' in data:
            trilha.descricao = data['descricao']
        
        if 'cursos' in data:
            trilha.cursos = [] 
            for id_curso in data['cursos']:
                curso = session.query(Curso).get(id_curso)
                if curso:
                    trilha.cursos.append(curso)
                else:
                    session.rollback() 
                    return jsonify({'error': f'Curso com ID {id_curso} não encontrado.'}), 400
        
        session.commit()
        return jsonify({'message': 'Trilha de aprendizado atualizada com sucesso'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar a trilha de aprendizado', 'message': str(e)}), 500

    finally:
        session.close()

@bp.route('/api/trilhas-aprendizado', methods=['GET'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
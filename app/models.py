from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from . import db


Base = declarative_base()

curso_trilha_association = Table('Curso_Trilha', Base.metadata,
    Column('Cursos_id', Integer, ForeignKey('Cursos.id')),
    Column('Trilha_apredizado_id', Integer, ForeignKey('Trilhas_apredizado.id'))
)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class TrilhaAprendizado(Base):
    __tablename__ = 'Trilhas_apredizado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    cursos = relationship("Curso", secondary=curso_trilha_association, back_populates="trilhas")

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
        }

class Curso(Base):
    __tablename__ = 'Cursos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    trilhas = relationship("TrilhaAprendizado", secondary=curso_trilha_association, back_populates="cursos")
    aulas = relationship("Aula", back_populates="curso")
    comentarios = relationship("Comentario", back_populates="curso")
    avaliacoes = relationship("Avaliacao", back_populates="curso")

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'trilhas': [trilha.serialize() for trilha in self.trilhas],
            'aulas': [aula.serialize() for aula in self.aulas],
            'comentarios': [comentario.serialize() for comentario in self.comentarios],
            'avaliacoes': [avaliacao.serialize() for avaliacao in self.avaliacoes]
        }

class Aula(Base):
    __tablename__ = 'Aulas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255))
    descricao = Column(String(255))
    duracao = Column(Integer)
    id_curso = Column(Integer, ForeignKey('Cursos.id'))
    curso = relationship("Curso", back_populates="aulas")

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'duracao': self.duracao,
            'id_curso': self.id_curso,
        }

class Comentario(Base):
    __tablename__ = 'Comentarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255))
    id_user = Column(Integer, ForeignKey('User.id'))
    id_curso = Column(Integer, ForeignKey('Cursos.id'))
    user = relationship("User")
    curso = relationship("Curso", back_populates="comentarios")

    def serialize(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'id_user': self.id_user,
            'id_curso': self.id_curso
        }

class Avaliacao(Base):
    __tablename__ = 'Avaliacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    avaliacao = Column(Integer)
    comentario = Column(String(255))
    id_user = Column(Integer, ForeignKey('User.id'))
    id_curso = Column(Integer, ForeignKey('Cursos.id'))
    user = relationship("User")
    curso = relationship("Curso", back_populates="avaliacoes")

    def serialize(self):
        return {
            'id': self.id,
            'avaliacao': self.avaliacao,
            'comentario': self.comentario,
            'id_user': self.id_user,
            'id_curso': self.id_curso
        }

# Conectar ao banco de dados e criar as tabelas
engine = create_engine('mysql+pymysql://root:root@localhost/Cursos', echo=True)
Base.metadata.create_all(engine)
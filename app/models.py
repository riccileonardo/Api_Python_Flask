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
    cargahoraria = Column(Integer)  # Adicionado, assumindo que você atualize seu banco de dados
    trilhas = relationship("TrilhaAprendizado", secondary=curso_trilha_association, back_populates="cursos")
    aulas = relationship("Aula", back_populates="curso")
    comentarios = relationship("Comentario", back_populates="curso")
    avaliacoes = relationship("Avaliacao", back_populates="curso")

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'cargahoraria': float(self.cargahoraria),
            'trilhas': [trilha.serialize() for trilha in self.trilhas],
            'aulas': [aula.serialize() for aula in self.aulas],
            'comentarios': [comentario.serialize() for comentario in self.comentarios],
            'avaliacoes': [avaliacao.serialize() for avaliacao in self.avaliacoes]
        }

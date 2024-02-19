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
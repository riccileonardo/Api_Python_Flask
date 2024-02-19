from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from . import db

Base = declarative_base()

curso_trilha_association = Table('Curso_Trilha', Base.metadata,
    Column('Cursos_id', Integer, ForeignKey('Cursos.id')),
    Column('Trilha_apredizado_id', Integer, ForeignKey('Trilhas_apredizado.id'))
)
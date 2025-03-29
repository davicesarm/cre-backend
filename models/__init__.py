from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .Curso import Curso
from .Materia import Materia
from .CursoMateria import CursoMateria
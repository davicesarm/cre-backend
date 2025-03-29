from . import db

class Materia(db.Model):
    __tablename__ = "materia"
    idMateria = db.Column(db.Integer, primary_key=True)
    nomeMateria = db.Column(db.String(255), nullable=False, unique=True)
from . import db

class Curso(db.Model):
    __tablename__ = "curso"
    idCurso = db.Column(db.Integer, primary_key=True)
    nomeCurso = db.Column(db.String(255), nullable=False)
from . import db

class Curso(db.Model):
    __tablename__ = "curso"
    idCurso = db.Column(db.Integer, primary_key=True)
    nomeCurso = db.Column(db.String(255), nullable=False)
    turno = db.Column(db.String(100))
    formacao = db.Column(db.String(100))
    fk_idCampus = db.Column(db.Integer, db.ForeignKey("campus.idCampus"), nullable=False)
    
    campus = db.relationship("Campus", backref="curso")
    
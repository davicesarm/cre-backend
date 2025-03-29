from . import db

class CursoMateria(db.Model):
    __tablename__ = "cursoMateria"
    peso = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    fk_idCurso = db.Column(db.Integer, db.ForeignKey("curso.idCurso"), nullable=False)
    fk_idMateria = db.Column(db.Integer, db.ForeignKey("materia.idMateria"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("fk_idCurso", "fk_idMateria"),
    )

    curso = db.relationship("Curso", backref="cursoMateria")
    materia = db.relationship("Materia", backref="cursoMateria")
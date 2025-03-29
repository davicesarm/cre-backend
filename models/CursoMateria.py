from . import db

class CursoMateria(db.Model):
    __tablename__ = "curso_materia"
    peso = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey("materia.id"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("id_curso", "id_materia"),
    )

    curso = db.relationship("Curso", backref="curso_materia")
    materia = db.relationship("Materia", backref="curso_materia")
from . import db

class Campus(db.Model):
    __tablename__ = "campus"
    idCampus = db.Column(db.Integer, primary_key=True)
    nomeCampus = db.Column(db.String(255), nullable=False, unique=True)
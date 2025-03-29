from flask import Flask, jsonify
from config import Config
from models import *
from utils import formatar_curso

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/cursos")
def get_cursos():
    cursos = Curso.query.all()
    cursos_dict = {
        "cursos": [
            {
                "id": curso.idCurso,
                "nome": curso.nomeCurso
            }
            for curso in cursos
        ] 
    }
    return jsonify(cursos_dict)
    

@app.route("/curso/id/<int:id>")
def get_curso(id: int):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 400
    
    curso_dict = formatar_curso(curso)
    
    return jsonify(curso_dict)
    
    
@app.route("/curso/nome/<string:nome>")
def find_curso(nome: str):
    curso = Curso.query.filter(Curso.nomeCurso.ilike(nome)).first()
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 400
    
    curso_dict = formatar_curso(curso)
    
    return jsonify(curso_dict)
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
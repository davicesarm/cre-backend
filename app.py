from flask_migrate import Migrate
from flask import Flask, jsonify, request
from config import Config
from models import *
from utils import formatar_curso
from flask_cors import CORS
from seed import *
import threading
import time

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

@app.route("/cursos")
def get_cursos():
    cursos = Curso.query.all()
    cursos_dict = {
        "cursos": [
            {
                "id_curso": curso.idCurso,
                "nome_curso": curso.nomeCurso,
                "turno": curso.turno,
                "formacao": curso.formacao,
                "campus": curso.campus.nomeCampus,
            }
            for curso in cursos
        ] 
    }
    return jsonify(cursos_dict)
    

@app.route("/curso/id/<int:id>")
def get_curso(id: int):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 404
    
    curso_dict = formatar_curso(curso)
    
    return jsonify(curso_dict)
    

@app.route("/curso/nome/<string:nome>")
def find_cursos(nome: str):
    turno = request.args.get('turno')
    formacao = request.args.get('formacao')
    campus = request.args.get('campus')
    
    cursos = Curso.query.filter(Curso.nomeCurso.ilike(nome))
    
    if turno:
        cursos = cursos.filter(Curso.turno.ilike(f"%{turno}"))
    if formacao:
        cursos = cursos.filter(Curso.formacao.ilike(formacao))
    if campus:
        cursos = cursos.filter(Campus.nomeCampus.ilike(f"%{campus}"))
    
    if not cursos.all():
        return jsonify({"error": "Curso não encontrado"}), 404
    
    cursos_dict = {
        "cursos": [
            formatar_curso(curso)
            for curso in cursos
        ] 
    }
    
    return jsonify(cursos_dict)
    

def popular_banco():
    while True:
        with app.app_context():
            links = pegar_links_cursos_disponiveis()
            for curso in links:
                extrair_e_inserir_dados_url(curso)

        time.sleep(7 * 24 * 60 * 60)
    """ 
    OBS: Talvez seja necessário mudar essa implementeçao,
    usar algo mais robusto...
    Deixarei assim por enquanto porque funciona.
    """
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
   
    threading.Thread(target=popular_banco, daemon=True).start()
        
    app.run(debug=True)
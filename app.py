from flask import Flask, jsonify, request
from config import Config
from models import *
from seed import *
from utils import formatar_curso
from flask_cors import CORS
import threading
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app)

UPDATE_SECRET = os.getenv("UPDATE_SECRET")

def tarefa_atualizacao():
    print("[DADOS] Iniciando atualização dos dados...")
    with app.app_context():
        links = pegar_links_cursos_disponiveis()
        for curso in links:
            extrair_e_inserir_dados_url(curso)
    print("[DADOS] Dados atualizados com sucesso!")

@app.route("/atualizar", methods=["POST"])
def atualizar_manual():
    token = request.headers.get("Authorization")
    if token != f"Bearer {UPDATE_SECRET}":
        return jsonify({"error": "Não autorizado"}), 403

    threading.Thread(target=tarefa_atualizacao, daemon=True).start()

    return jsonify({"message": "Dados atualizados com sucesso!"})


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
    curso = db.session.get(Curso, id)
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
        cursos = cursos.filter(Curso.turno.ilike(f"%{turno}%"))
    if formacao:
        cursos = cursos.filter(Curso.formacao.ilike(f"%{formacao}%"))
    if campus:
        cursos = cursos.join(Campus).filter(Campus.nomeCampus.ilike(f"%{campus}%"))
    
    if not cursos.all():
        return jsonify({"error": "Curso não encontrado"}), 404
    
    cursos_dict = {
        "cursos": [
            formatar_curso(curso)
            for curso in cursos
        ] 
    }
    
    return jsonify(cursos_dict)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
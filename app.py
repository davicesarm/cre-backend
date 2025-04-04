from flask import Flask, jsonify, request
from config import Config
from models import *
from utils import formatar_curso
from flask_cors import CORS
from seed import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

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



class AtualizadorBanco:
    def __init__(self, intervalo_dias=7):
        self.intervalo = timedelta(days=intervalo_dias)
        self.proxima_atualizacao = datetime.now() + self.intervalo
        self.scheduler = BackgroundScheduler()

    def atualizar_dados(self):
        print("[DADOS] Iniciando atualização dos dados...")
        with app.app_context():
            links = pegar_links_cursos_disponiveis()
            for curso in links:
                extrair_e_inserir_dados_url(curso)
        self.proxima_atualizacao = datetime.now() + self.intervalo
        print("[DADOS] Dados atualizados com sucesso!")

    def mensagem_diaria(self):
        dias = (self.proxima_atualizacao - datetime.now()).days
        if dias > 0:
            print(f"[DADOS] Próxima atualização em {dias} dias.")
        else:
            print("[DADOS] A atualização ocorre hoje!")

    def iniciar_scheduler(self):
        self.scheduler.add_job(self.atualizar_dados, 'interval', seconds=self.intervalo.total_seconds(), misfire_grace_time=60)
        self.scheduler.add_job(self.mensagem_diaria, 'cron', hour=12, minute=0, misfire_grace_time=60)
        self.scheduler.start()

    
with app.app_context():
    db.create_all()

atualizador = AtualizadorBanco()
atualizador.atualizar_dados()
atualizador.iniciar_scheduler()

if __name__ == '__main__':
    app.run(debug=True)
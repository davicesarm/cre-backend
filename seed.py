from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app import app
from utils import pegar_links_cursos_disponiveis, extrair_e_inserir_dados_url

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
        
atualizador = AtualizadorBanco()
atualizador.atualizar_dados()
atualizador.iniciar_scheduler()
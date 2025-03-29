from bs4 import BeautifulSoup
import requests
from bs4.element import NavigableString
from models import *
from app import app

def extrair_e_inserir_dados_url(url):
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.text, 'html.parser')
    
    curso_tag = soup.select_one(
        'html body.tema-verde div.content div.container div.row div#conteudo.col-sm-12.col-md-10.conteudo h2.titulo.azul-petroleo'
    )
    if not curso_tag:
        return
    
    curso_nome = curso_tag.get_text(strip=True)
    
    curso_obj = Curso.query.filter_by(nome=curso_nome).first()
    if not curso_obj:
        curso_obj = Curso(nome=curso_nome)
        db.session.add(curso_obj)
        db.session.commit()
    
    
    semestres = soup.select_one('div.corpo:nth-child(3) > div:nth-child(2)')
    if not semestres:
        return
    
    periodo_num = 1
    for semestre in semestres:
        if isinstance(semestre, NavigableString):
            continue
        
        tbody = semestre.find_next('tbody')
        if not tbody:
            continue
        
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:
                continue
            
            materia_nome = cols[0].get_text(strip=True)
            ch = cols[1].get_text(strip=True)
            try:
                peso = int(ch)
            except ValueError:
                peso = 0
            
            materia_obj = Materia.query.filter_by(nome=materia_nome).first()
            if not materia_obj:
                materia_obj = Materia(nome=materia_nome)
                db.session.add(materia_obj)
                db.session.commit()
            
            curso_materia_obj = CursoMateria(
                peso=peso,
                periodo=periodo_num,
                id_curso=curso_obj.id,
                id_materia=materia_obj.id
            )
            db.session.add(curso_materia_obj)
        periodo_num += 1
    
    db.session.commit()

with app.app_context():
    extrair_e_inserir_dados_url("https://estudante.ifpb.edu.br/cursos/39/")
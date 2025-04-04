from bs4 import BeautifulSoup
import requests
from bs4.element import NavigableString
from models import *


def formatar_curso(curso: Curso) -> dict:
    periodos = {}

    for cm in curso.cursoMateria:
        periodo = cm.periodo

        if periodo not in periodos:
            periodos[periodo] = []

        periodos[periodo].append({
            "id_materia": cm.materia.idMateria,
            "nome_materia": cm.materia.nomeMateria,
            "ch": cm.ch
        })
    
    curso_dict = {
        "id_curso": curso.idCurso,
        "nome_curso": curso.nomeCurso,
        "turno": curso.turno,
        "formacao": curso.formacao,
        "campus": curso.campus.nomeCampus,
        "periodos": [
            {
                "periodo": periodo,
                "materias": materias
            }
            for periodo, materias in sorted(periodos.items())
        ]
    }
    
    return curso_dict


def extrair_e_inserir_dados_url(url):
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.text, 'html.parser')
    
    curso_tag = soup.select_one(
        'html body.tema-verde div.content div.container div.row div#conteudo.col-sm-12.col-md-10.conteudo h2.titulo.azul-petroleo'
    )
    curso_nome = curso_tag.get_text(strip=True)
    
    turno_tag = soup.select_one('div.row:nth-child(3) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4)')
    turno_nome = turno_tag.get_text(strip=True)
    
    formacao_tag = soup.select_one('div.row:nth-child(3) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(2)')
    formacao_nome = formacao_tag.get_text(strip=True)
    
    campus_tag = soup.select_one('html body.tema-verde div.content div.container div.row div#conteudo.col-sm-12.col-md-10.conteudo div.row div.col-xs-12 ul.list-unstyled.list-inline li a')
    campus_nome = campus_tag.get_text(strip=True)
    
    campus_obj = Campus.query.filter_by(nomeCampus=campus_nome).first()
    if not campus_obj:
        campus_obj = Campus(nomeCampus=campus_nome)
        db.session.add(campus_obj)
        db.session.commit()
    
    curso_obj = Curso.query.filter_by(
        nomeCurso=curso_nome,
        turno=turno_nome,
        formacao=formacao_nome,
        fk_idCampus=campus_obj.idCampus,
    ).first()
    
    if not curso_obj:
        curso_obj = Curso(
            nomeCurso=curso_nome,
            turno=turno_nome,
            formacao=formacao_nome,
            fk_idCampus=campus_obj.idCampus
        )
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
                ch = int(ch)
            except ValueError:
                ch = 0
            
            materia_obj = Materia.query.filter_by(nomeMateria=materia_nome).first()
            if not materia_obj:
                materia_obj = Materia(nomeMateria=materia_nome)
                db.session.add(materia_obj)
                db.session.commit()
            
            curso_materia_obj = CursoMateria.query.filter_by(
                fk_idCurso=curso_obj.idCurso,
                fk_idMateria=materia_obj.idMateria
            ).first()
            if not curso_materia_obj:
                curso_materia_obj = CursoMateria(
                    ch=ch,
                    periodo=periodo_num,
                    fk_idCurso=curso_obj.idCurso,
                    fk_idMateria=materia_obj.idMateria
                )
                db.session.add(curso_materia_obj)
            else:
                curso_materia_obj.ch = ch
                curso_materia_obj.periodo = periodo_num
        
        periodo_num += 1
    db.session.commit()


def pegar_links_cursos_disponiveis() -> list[str]:
    pagina = requests.get("https://estudante.ifpb.edu.br/cursos/")
    soup = BeautifulSoup(pagina.text, "html.parser")
    content = soup.select_one('#conteudo')
    elementos = content.find_all(recursive=False)

    links = set()

    for elemento in elementos[3:]:
        for link in elemento.find_all('a'):
            href = link.get("href")
            if href:
                links.add(f"https://estudante.ifpb.edu.br{href}")

    return list(links)

from models import *
from app import app 
from sqlalchemy.exc import IntegrityError

with app.app_context():
    try:
        # Criando cursos
        curso1 = Curso(nome="Sistemas para Internet")
        curso2 = Curso(nome="Engenharia de Software")
        db.session.add_all([curso1, curso2])
        db.session.commit()  
        print("Cursos inseridos com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao inserir cursos")

    try:
        # Criando matérias p1
        subjects_p1 = [
            Materia(nome="Algoritmo e Programação Estruturada"),
            Materia(nome="Fundamentos da Computação"),
            Materia(nome="Fundamentos de Redes de Computadores"),
            Materia(nome="Linguagens de Marcação"),
            Materia(nome="Língua Portuguesa"),
            Materia(nome="Matemática Aplicada a Sistemas para Internet")
        ]
        db.session.add_all(subjects_p1)
        db.session.commit()  
        print("Matérias P1 inseridas com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao inserir matérias P1")

    try:
        # Criando matérias p2
        subjects_p2 = [
            Materia(nome="Banco de Dados I"),
            Materia(nome="Ciência, Tecnologia e Meio Ambiente"),
            Materia(nome="Estrutura de Dados"),
            Materia(nome="Fundamentos da Metodologia"),
            Materia(nome="Linguagens de Script"),
            Materia(nome="Protocolos de Interconexão de Redes de Computadores"),
            Materia(nome="Sistemas Operacionais")
        ]
        db.session.add_all(subjects_p2)
        db.session.commit()  
        print("Matérias P2 inseridas com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao inserir matérias P2")

    try:
        curso1 = Curso.query.filter_by(nome="Sistemas para Internet").first()
        if not curso1:
            raise ValueError("Curso 'Sistemas para Internet' não encontrado!")

        subjects = {s.nome: s.id for s in Materia.query.all()}

        relations_p1 = [
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Algoritmo e Programação Estruturada"], peso=100, periodo=1),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Fundamentos da Computação"], peso=60, periodo=1),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Fundamentos de Redes de Computadores"], peso=80, periodo=1),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Linguagens de Marcação"], peso=80, periodo=1),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Língua Portuguesa"], peso=60, periodo=1),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Matemática Aplicada a Sistemas para Internet"], peso=100, periodo=1)
        ]
        db.session.add_all(relations_p1)
        db.session.commit()
        print("Relações curso-matéria (P1) inseridas com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao inserir relações P1")
    except ValueError as e:
        print("Erro:", e)

    try:
        relations_p2 = [
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Banco de Dados I"], peso=80, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Ciência, Tecnologia e Meio Ambiente"], peso=40, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Estrutura de Dados"], peso=80, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Fundamentos da Metodologia"], peso=40, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Linguagens de Script"], peso=80, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Protocolos de Interconexão de Redes de Computadores"], peso=80, periodo=2),
            CursoMateria(id_curso=curso1.id, id_materia=subjects["Sistemas Operacionais"], peso=100, periodo=2)
        ]
        db.session.add_all(relations_p2)
        db.session.commit()
        print("Relações curso-matéria (P2) inseridas com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao inserir relações P2")

    print("Dados inseridos com sucesso!")

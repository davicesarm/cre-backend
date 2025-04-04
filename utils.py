from models import Curso


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
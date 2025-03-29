from models import Curso

def formatar_curso(curso: Curso) -> dict:
    periodos = {}

    for cm in curso.curso_materia:
        periodo = cm.periodo

        if periodo not in periodos:
            periodos[periodo] = []

        periodos[periodo].append({
            "id": cm.materia.id,
            "nome": cm.materia.nome,
            "peso": cm.peso
        })
    
    curso_dict = {
        "id": curso.id,
        "nome": curso.nome,
        "periodos": [
            {
                "periodo": periodo,
                "materias": materias
            }
            for periodo, materias in sorted(periodos.items())
        ]
    }
    
    return curso_dict
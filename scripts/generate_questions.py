#!/usr/bin/env python3
"""Gera questions.js com 28 Natural + 28 Adaptado."""
from pathlib import Path

# 28 itens naturais (revisados, sem temas duplicados na seleção)
NATURAL = [
    ("Decisão", "Em situações novas, prefiro definir o próximo passo rapidamente", "D",
     "Costumo ouvir diferentes pontos de vista antes de me posicionar", "S",
     "Sinto-me à vontade ao trocar perspectivas em grupo", "I",
     "Analiso cuidadosamente as alternativas antes de escolher", "C"),
    ("Relações", "Construo relações de confiança de forma gradual", "S",
     "Sou aberto ao conhecer novas pessoas", "I",
     "Prefiro interações diretas e objetivas", "D",
     "Valorizo conversas com pauta clara e organizada", "C"),
    ("Ritmo", "Trabalho melhor com ritmo constante e previsível", "S",
     "Gosto de ambientes com variedade de estímulos", "I",
     "Busco agir com rapidez para alcançar metas", "D",
     "Prefiro planejar cada etapa antes de executar", "C"),
    ("Problemas", "Diante de problemas, busco soluções práticas e imediatas", "D",
     "Procuro envolver outras pessoas na solução", "I",
     "Reservo tempo para processar antes de agir", "S",
     "Analiso dados e sigo métodos testados", "C"),
    ("Mudança", "Mudanças me motivam a buscar novos resultados", "D",
     "Adapto-me bem quando vejo o lado positivo das mudanças", "I",
     "Prefiro mudanças planejadas com tempo para me ajustar", "S",
     "Aceito mudanças quando são bem fundamentadas", "C"),
    ("Comunicação", "Expresso opiniões de forma direta", "D",
     "Uso exemplos e histórias para me comunicar", "I",
     "Comunico-me de forma calma e ponderada", "S",
     "Estruturo minha comunicação de forma lógica", "C"),
    ("Equipe", "Gosto de coordenar esforços do grupo", "D",
     "Trago energia e entusiasmo para o time", "I",
     "Contribuo para harmonia e cooperação", "S",
     "Ajudo a equipe a seguir processos e prazos", "C"),
    ("Aprendizado", "Aprendo melhor fazendo e enfrentando desafios", "D",
     "Aprendo melhor discutindo ideias com outros", "I",
     "Aprendo melhor com prática repetida", "S",
     "Aprendo melhor estudando materiais estruturados", "C"),
    ("Pressão", "Sob pressão, assumo controle e busco soluções rápidas", "D",
     "Sob pressão, busco apoio e troco ideias", "I",
     "Sob pressão, mantenho calma e rotina", "S",
     "Sob pressão, busco mais informações antes de agir", "C"),
    ("Organização", "Organizo meu espaço de forma funcional", "D",
     "Meu ambiente reflete criatividade e dinamismo", "I",
     "Mantenho organização consistente e previsível", "S",
     "Sou meticuloso com organização e detalhes", "C"),
    ("Metas", "Estabeleço metas ambiciosas e trabalho para alcançá-las", "D",
     "Compartilho metas para me manter motivado", "I",
     "Prefiro metas realistas com prazos confortáveis", "S",
     "Defino metas com critérios claros de medição", "C"),
    ("Conflito", "Enfrento conflitos de frente para resolvê-los", "D",
     "Busco mediar conflitos de forma construtiva", "I",
     "Evito conflitos e prefiro ambiente pacífico", "S",
     "Abordo conflitos com argumentos lógicos", "C"),
    ("Energia", "Minha energia vem de superar obstáculos", "D",
     "Minha energia vem da interação e reconhecimento", "I",
     "Minha energia vem de ambientes estáveis", "S",
     "Minha energia vem de fazer as coisas com qualidade", "C"),
    ("Planejamento", "Planejo focando no resultado final", "D",
     "Planejo deixando espaço para adaptações", "I",
     "Planejo com cuidado e sigo o plano", "S",
     "Planejo detalhadamente cada etapa", "C"),
    ("Iniciativa", "Tomar a frente em projetos novos me motiva", "D",
     "Sugiro ideias com entusiasmo para engajar", "I",
     "Contribuo de forma constante sem precisar de destaque", "S",
     "Contribuo quando tenho clareza de processos", "C"),
    ("Relacionamento", "Valorizo mais resultados do que agradar", "D",
     "Invisto tempo em relacionamentos positivos", "I",
     "Prezo por relações longas e de confiança", "S",
     "Mantenho relações com limites claros", "C"),
    ("Qualidade", "Foco em entregar resultados com impacto", "D",
     "Foco em criar experiências positivas", "I",
     "Foco em trabalhos consistentes e confiáveis", "S",
     "Foco em padrões elevados de qualidade", "C"),
    ("Prioridade", "Priorizo resultados rápidos e concretos", "D",
     "Priorizo boas relações e clima positivo", "I",
     "Priorizo estabilidade e previsibilidade", "S",
     "Priorizo fazer bem feito da primeira vez", "C"),
    ("Feedback", "Recebo bem feedbacks diretos e objetivos", "D",
     "Aprecio feedback que reconheça meu esforço", "I",
     "Prefiro feedback em particular e cuidadoso", "S",
     "Valorizo feedback específico baseado em fatos", "C"),
    ("Autonomia", "Gosto de autonomia para decidir como agir", "D",
     "Gosto de liberdade para expressar ideias", "I",
     "Gosto de saber exatamente o que se espera", "S",
     "Gosto de diretrizes e procedimentos claros", "C"),
    ("Desafio", "Desafios difíceis me motivam", "D",
     "Desafios criativos com pessoas me interessam", "I",
     "Desafios previsíveis me trazem segurança", "S",
     "Desafios analíticos me atraem", "C"),
    ("Rotina", "Prefiro variedade a rotinas previsíveis", "D",
     "Gosto quando cada dia traz situações diferentes", "I",
     "Rotinas estabelecidas me trazem conforto", "S",
     "Processos padronizados ajudam minha qualidade", "C"),
    ("Influência", "Influencio pela determinação e convicção", "D",
     "Influencio pelo entusiasmo e motivação", "I",
     "Influencio pela confiabilidade e consistência", "S",
     "Influencio pelo conhecimento técnico", "C"),
    ("Crise", "Em crise, ajo rápido para retomar controle", "D",
     "Em crise, busco unir as pessoas", "I",
     "Em crise, mantenho calma e rotina possível", "S",
     "Em crise, busco compreender causas antes de agir", "C"),
    ("Social", "Em grupos, costumo liderar a conversa", "D",
     "Em grupos, sou expansivo e me conecto fácil", "I",
     "Em grupos, observo antes de interagir", "S",
     "Em grupos, prefiro conversas com propósito", "C"),
    ("Liderança", "Lidero com metas claras e cobrança de resultados", "D",
     "Lidero inspirando e motivando", "I",
     "Lidero apoiando e garantindo bem-estar", "S",
     "Lidero definindo padrões e qualidade", "C"),
    ("Motivação", "Sou motivado por superação e conquistas", "D",
     "Sou motivado por reconhecimento e pertencimento", "I",
     "Sou motivado por segurança e estabilidade", "S",
     "Sou motivado por excelência técnica", "C"),
    ("Foco", "Meu foco está no resultado e meta final", "D",
     "Meu foco está nas pessoas e relacionamentos", "I",
     "Meu foco está no processo e consistência", "S",
     "Meu foco está nos detalhes e qualidade", "C"),
]

ADAPTED_PREFIX = {
    "Decisão": "No trabalho, ",
    "Relações": "No ambiente profissional, ",
    "Ritmo": "Na rotina de trabalho, ",
    "Problemas": "Ao resolver problemas no trabalho, ",
    "Mudança": "Diante de mudanças organizacionais, ",
    "Comunicação": "Na comunicação profissional, ",
    "Equipe": "Na equipe, ",
    "Aprendizado": "Para aprender no trabalho, ",
    "Pressão": "Sob pressão no trabalho, ",
    "Organização": "No meu espaço de trabalho, ",
    "Metas": "Em relação às metas do trabalho, ",
    "Conflito": "Em conflitos no trabalho, ",
    "Energia": "No trabalho, minha energia vem de ",
    "Planejamento": "No planejamento de tarefas, ",
    "Iniciativa": "No trabalho, ",
    "Relacionamento": "Nas relações profissionais, ",
    "Qualidade": "Na entrega de trabalho, ",
    "Prioridade": "No trabalho, ",
    "Feedback": "Ao receber feedback profissional, ",
    "Autonomia": "No trabalho, ",
    "Desafio": "Nos desafios profissionais, ",
    "Rotina": "Na rotina profissional, ",
    "Influência": "Para influenciar no trabalho, ",
    "Crise": "Em crises no trabalho, ",
    "Social": "Em interações profissionais, ",
    "Liderança": "Ao liderar ou ser liderado, ",
    "Motivação": "No trabalho, sou motivado por ",
    "Foco": "No trabalho, ",
}


def adapt_text(tema: str, text: str) -> str:
    prefix = ADAPTED_PREFIX.get(tema, "No trabalho, ")
    t = text[0].lower() + text[1:] if text else text
    if tema == "Energia":
        return prefix + t.replace("Minha energia vem de ", "").replace("minha energia vem de ", "")
    if tema == "Motivação":
        return prefix + t.replace("Sou motivado por ", "").replace("sou motivado por ", "")
    if tema == "Influência":
        return prefix + t.replace("Influencio ", "costumo ").replace("influencio ", "costumo ")
    return prefix + t


def rotate_opts(opts: list, offset: int) -> list:
    """Rotaciona posição dos fatores para evitar padrão fixo D/I/S/C por slot."""
    n = len(opts)
    return opts[offset % n:] + opts[: offset % n]


def fmt_q(idx: str, tema: str, opts: list, bloco: str, rot: int = 0) -> str:
    rotated = rotate_opts(opts, rot)
    parts = ", ".join(f"{{t:'{t}',f:'{f}'}}" for t, f in rotated)
    return f"{{id:'{idx}',bloco:'{bloco}',tema:'{tema}',opts:[{parts}]}}"


def main():
    out = Path(__file__).resolve().parent.parent / "src" / "js" / "questions.js"
    lines = ["// Gerado por scripts/generate_questions.py", "const PERGUNTAS_NATURAL = ["]
    for i, row in enumerate(NATURAL, 1):
        tema = row[0]
        opts = [(row[j], row[j+1]) for j in range(1, 9, 2)]
        lines.append("  " + fmt_q(f"n{i:02d}", tema, opts, "natural", (i * 3 + 1) % 4) + ",")
    lines.append("];")
    lines.append("")
    lines.append("const PERGUNTAS_ADAPTADO = [")
    for i, row in enumerate(NATURAL, 1):
        tema = row[0]
        opts = [(adapt_text(tema, row[j]), row[j+1]) for j in range(1, 9, 2)]
        lines.append("  " + fmt_q(f"a{i:02d}", tema, opts, "adaptado", (i * 5 + 2) % 4) + ",")
    lines.append("];")
    lines.append("")
    lines.append("const PERGUNTAS = [...PERGUNTAS_NATURAL, ...PERGUNTAS_ADAPTADO];")
    lines.append(f"const TOTAL_POR_BLOCO = {len(NATURAL)};")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ {out} — {len(NATURAL)} natural + {len(NATURAL)} adaptado")


if __name__ == "__main__":
    main()
# TESTEDISC V2 — Perfil Comportamental DISC

Teste psicométrico completo com perfil **Natural + Adaptado**, devolutiva profissional estruturada (base: 66 relatórios Thomas) e API de inferência.

**Versão:** 2.1.0

## Funcionalidades

- **56 afirmações** (28 Natural + 28 Adaptado) — ordem randomizada, sem revelar etapa
- **3 gráficos DISC** (Autoimagem · Pressão · Adaptado)
- **12 seções de devolutiva** no formato dos relatórios Thomas International
- **Base de conhecimento** extraída de 66 PDFs modelo
- **55 regras de inferência** via API
- Modo escuro, PWA offline, compartilhamento por link
- Coleta anônima para analytics (`/responses`)
- Painel admin em `admin/index.html`

## Desenvolvimento

```bash
# Pipeline completo
python build_all.py

# Ou manualmente:
python scripts/extract_knowledge.py
python scripts/build_devolutiva_templates.py
python scripts/generate_questions.py
python scripts/generate_rules.py
python build_complete.py
python run_tests.py
```

## API

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Endpoints: `POST /infer`, `POST /responses`, `GET /analytics`, `GET /result/{hash}`

## Estrutura

```
src/js/          — módulos frontend (app, scoring, devolutiva, templates)
scripts/         — pipeline de geração (questões, regras, knowledge)
artifacts/       — knowledge engine (phrases, rules, devolutiva_templates)
api/             — FastAPI + inferência
docs/            — GitHub Pages (deploy automático)
```

## Deploy

- **Repositório:** https://github.com/CENTRALSP3/TESTEDISC
- **Branch principal:** `enhanced-platform`
- **GitHub Pages:** https://centralsp3.github.io/TESTEDISC/
- Workflow `.github/workflows/pages.yml` publica `docs/` automaticamente

## Licença

Perfil Comportamental DISC — CENTRAL SP3
# TESTEDISC V2 — Perfil Comportamental DISC

Teste psicométrico completo com perfil **Natural + Adaptado**, devolutiva profissional em 12 seções e API de inferência.

**Versão:** 2.0.0

## Funcionalidades

- **56 questões** (28 Natural + 28 Adaptado) forced-choice
- **3 gráficos DISC** (Autoimagem · Pressão · Adaptado)
- **Análise de discrepância** Natural vs Adaptado
- **12 seções de devolutiva** inspiradas em relatórios profissionais
- **55 regras de inferência** via API
- Modo escuro, PWA offline, compartilhamento por link
- Coleta anônima para analytics (`/responses`)
- Painel admin em `admin/index.html`

## Desenvolvimento

```bash
# Pipeline completo (na raiz do projeto)
python build_all.py

# Ou manualmente:
python ../scripts/generate_questions.py
python ../scripts/generate_rules.py
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
src/js/
├── constants.js, questions.js, scoring.js
├── charts.js, devolutiva.js, features.js, app.js
api/
├── main.py, inference.py, database.py
admin/index.html
manifest.json, sw.js
```

## Deploy

GitHub Pages publica `docs/`. Branch `enhanced-platform`.

## Licença

TeclaPonto — Análise Comportamental DISC
# Perfil DISC - Análise Comportamental TeclaPonto

Teste psicométrico inspirado no modelo DISC (Dominância, Influência, Estabilidade, Conformidade). Pronto para deploy no GitHub Pages.

**Versão do instrumento:** 0.9.0 (Fase 0 concluída)

## Funcionalidades

- **40 questões forced-choice** com opções randomizadas
- **Scoring -10 a +10** por fator (normalizado de -40 a +40)
- **Gráfico interativo** Chart.js com zona cinzenta (|score| > 8)
- **Devolutiva em 10 seções** com palavras descritivas extraídas de 66 perfis profissionais
- **Devolutiva multi-fator** (comunicação, pressão, percepção ponderadas)
- Design responsivo, impressão/PDF via navegador

## Desenvolvimento

### Estrutura modular

```
TESTEDISC/
├── index.html              # gerado — não editar diretamente
├── build_complete.py       # gera index.html a partir dos módulos
├── run_tests.py            # executa todos os testes
├── src/js/
│   ├── constants.js        # fatores, cores, versão
│   ├── questions.js        # 40 questões
│   ├── palavras-data.js    # palavras dos 66 PDFs
│   ├── scoring.js          # scoring, blend, validação
│   ├── charts.js           # gráfico Chart.js
│   ├── devolutiva.js       # textos e renderização
│   └── app.js              # UI do quiz
├── artifacts/
│   ├── phrases.json        # biblioteca extraída dos PDFs
│   ├── palavras_por_fator.json
│   └── rules.yaml          # regras da API
└── tests/
    ├── test_scoring.py
    └── test_extraction.py
```

### Workflow

```bash
# 1. Editar módulos em src/js/
# 2. Regenerar index.html
python build_complete.py

# 3. Rodar testes
python run_tests.py
```

### Extrair dados dos PDFs (projeto pai)

```bash
cd ..
python scripts/extract_knowledge.py
python TESTEDISC/build_complete.py
```

## Deploy no GitHub Pages

1. Push para o GitHub
2. **Settings > Pages** → branch `main`, pasta `/`
3. Site em `https://SEU_USUARIO.github.io/TESTEDISC/`

## API (opcional)

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## Limitações

- Instrumento de autoconhecimento — não substitui avaliação psicológica profissional
- Sem normas populacionais validadas (previsto na Fase 3)
- Versão Natural vs Adaptado em desenvolvimento (Fase 1)

## Roadmap

Ver `../PLANEJAMENTO_V2.md` para o plano completo de evolução.

## Licença

TeclaPonto — Análise Comportamental DISC
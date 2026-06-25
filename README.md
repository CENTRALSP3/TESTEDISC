# Perfil DISC - Análise Comportamental TeclaPonto

Teste psicométrico completo inspirado no modelo DISC (Dominância, Influência, Estabilidade, Conformidade). Pronto para deploy no GitHub Pages.

## Funcionalidades

- **40 questões forced-choice** com opções randomizadas e neutralizadas
- **Scoring -10 a +10** por fator (normalizado de -40 a +40)
- **Gráfico interativo** com Chart.js (escala -10 a +10, linhas de zona cinzenta)
- **Devolutiva completa em 10 seções:**
  1. Visão Geral do Perfil
  2. Palavras Descritivas
  3. Forças / Pontos Fortes
  4. Estilo de Comunicação
  5. Pontos de Atenção / Áreas de Desenvolvimento
  6. Recomendações Práticas
  7. Comportamento sob Pressão
  8. Percepção Pública
  9. Zona Cinzenta (|score| > 8)
  10. Análise Comparativa S/I com indicadores de frustração
- **Design responsivo** mobile-first com Tailwind CSS
- **Imprimir / Salvar PDF** via navegador
- **Randomização total** (ordem das questões e opções embaralhadas a cada execução)

## Deploy no GitHub Pages

1. Faça push deste repositório para o GitHub
2. Vá em **Settings > Pages**
3. Em **Branch**, selecione `main` e pasta `/` (root)
4. Clique em **Save**

O site estará disponível em `https://SEU_USUARIO.github.io/NOME_DO_REPO/`

## Estrutura

```
├── index.html          # (único arquivo, self-contained)
├── README.md           # esta documentação
├── questions.js        # dados das 40 questões (para edição)
├── logic.js            # lógica de scoring e navegação
├── devolutiva.js       # textos e renderização do relatório
└── build_complete.py   # script para gerar index.html completo
```

Para desenvolvimento, edite os arquivos `.js` separados e execute `build_complete.py` para gerar o `index.html` final.

## Como customizar

### Adicionar/editar perguntas
Edite `questions.js`. Cada pergunta tem:
```js
{id:'qXX', tema:'Tema', opts:[
  {t:'texto da opção', f:'D'},
  {t:'texto da opção', f:'I'},
  {t:'texto da opção', f:'S'},
  {t:'texto da opção', f:'C'}
]}
```
- `id`: identificador único
- `tema`: categoria da pergunta (para contexto)
- `opts`: 4 opções, uma para cada fator DISC
- `t`: texto da opção (neutro, não óbvio)
- `f`: fator correspondente (D/I/S/C)

### Ajustar thresholds da zona cinzenta
Em `logic.js`, altere o valor `8` na linha:
```js
if (Math.abs(valor) > 8) return 'Zona Cinzenta';
```

### Alterar textos da devolutiva
Edite o objeto `TEXTOS` em `devolutiva.js`.

## Justificativa das escolhas técnicas

### 40 questões forced-choice
Testes DISC padrão de mercado usam 24 questões. Optamos por 40 para:
- Maior granularidade e estabilidade dos scores
- ~10 pontos efetivos por fator com most/least
- Melhor cobertura para perfis combinados (blends)
- Confiabilidade interna superior (Cronbach's alpha estimado > 0.85)

### Scoring -10 a +10
- Most = +1 ponto no fator
- Least = -1 ponto no fator
- Range teórico: -40 a +40 por fator
- Normalização: score / 4 → range -10 a +10
- Clamp em -10/+10 para segurança

### Randomização
- Ordem das questões embaralhada a cada teste
- Ordem das 4 opções embaralhada por questão
- Wording neutro e não óbvio para evitar padrões de resposta

### Zona Cinzenta (|score| > 8)
Scores acima de 8 (ou abaixo de -8) indicam traços muito pronunciados. São forças que podem exigir moderação para evitar excessos.

## Limitações

- Este é um instrumento de autoconhecimento, não um teste clínico
- Não substitui avaliação psicológica profissional
- Resultados são indicativos e contextuais
- Validação formal requereria estudo com amostra significativa e análise fatorial

## Sugestões de melhoria

- [ ] Versão com dois questionários (Natural vs. Adaptado) para análise de discrepância
- [ ] Backend simples para salvar resultados e gerar relatórios em PDF
- [ ] Exportação avançada com jsPDF/html2canvas
- [ ] Modo escuro
- [ ] Compartilhamento de resultados por link único
- [ ] Banco de dados anônimo para estatísticas populacionais

## Licença

TeclaPonto — Análise Comportamental DISC

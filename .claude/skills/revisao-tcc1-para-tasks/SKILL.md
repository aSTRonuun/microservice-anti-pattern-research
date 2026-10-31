---
name: revisao-tcc1-para-tasks
description: Converte a avaliação gerada pela skill revisor-tcc1 (parecer de projeto de TCC I com nota por critério) em uma lista de tasks acionáveis, cada uma com título, descrição, tipo de problema, severidade, critério da rubrica, localização, evidência, como resolver, critério de aceite, esforço e dependências. Use sempre que o usuário pedir para transformar a revisão/parecer/avaliação de um TCC em tarefas, tasks, pendências, checklist de correções, backlog, plano de correção ou issues (Jira, Linear, Trello), mesmo que não cite o revisor-tcc1 pelo nome.
---

# Revisão de TCC I → tasks

Transforma cada perda de pontos e cada incoerência apontada pela revisão em uma task que o autor do projeto consiga executar sem reler a revisão inteira. Responder em português (pt-BR).

## Princípio central: rastreabilidade

Toda task nasce de uma observação da revisão. Não crie tasks para problemas que a revisão não apontou, não aumente a gravidade de um problema e não invente trechos do projeto. Se perceber algo relevante que a revisão não cobriu, liste à parte em "Fora da revisão (não convertido)", em uma linha cada, sem gerar task.

O motivo: a revisão é o documento avaliado e justificado; a lista de tasks é um derivado dela. Se a lista disser mais do que a revisão, o autor corrige coisas que ninguém cobrou e o avaliador perde controle do que foi pedido.

## Fluxo

1. **Obter a revisão.** Use a saída do `revisor-tcc1` presente na conversa, ou o texto/arquivo enviado (skill `file-reading` se não estiver visível). Se não houver revisão, peça-a; não faça a revisão por conta própria. Se o projeto original também estiver disponível, use-o só para localizar trechos com mais precisão.
2. **Mapear observações.** Liste todo critério com veredito **Parcial** ou **Não atende**, a falta de cronograma (se apontada), cada incoerência da seção "Coerência interna" e cada referência "não localizada". Critérios **Atende** e a **Defesa** não geram task.
3. **Converter em tasks** com os campos abaixo.
4. **Agrupar e dividir:**
   - Mesma causa raiz em vários critérios (ex.: objetivo vago que afeta Objetivos e Metodologia) → uma task, listando todos os critérios afetados.
   - Uma observação com correções independentes (ex.: citação fora da norma e referência faltando) → tasks separadas.
5. **Ordenar:** severidade, depois pontos em jogo. Tasks de coerência e de objetivos vêm antes das que dependem deles (metodologia, cronograma, fundamentação), porque mudar o objetivo invalida correções feitas antes.
6. **Passada de verificação** antes de entregar:
   - Todo critério Parcial/Não atende está coberto por ao menos uma task.
   - Soma dos pontos em jogo = total perdido na revisão (sem dupla contagem em tasks agrupadas; cada perda é atribuída a uma única task).
   - Toda evidência citada existe na revisão (ou no projeto, se disponível).
   - Todo critério de aceite é verificável por outra pessoa.
7. **Entregar** no formato abaixo, no chat. Gere arquivo (CSV, JSON, .md) ou crie issues em ferramenta externa (Jira, Linear etc.) só se o usuário pedir; antes de criar issues, mostre a lista e peça confirmação.

## Campos de cada task

| Campo | Conteúdo |
|---|---|
| ID | T01, T02… na ordem de execução |
| Título | Verbo no infinitivo + objeto, até ~10 palavras ("Reescrever objetivo geral com objeto e campo de aplicação") |
| Tipo | Uma categoria da taxonomia abaixo |
| Severidade | Crítica / Alta / Média / Baixa (regras abaixo) |
| Critério(s) da rubrica | Parte + critério, como na revisão |
| Pontos em jogo | Perda atribuída pela revisão (ex.: −0,25); "0" se a perda não for pontuada |
| Localização | Seção/página/parágrafo do projeto; "não informada na revisão" se não houver |
| Evidência | Trecho curto ou paráfrase da revisão que justifica a task |
| Problema | O que está errado e por que importa, em até 2 frases |
| Como resolver | 1 a 4 passos concretos; partir da "Correção" sugerida pela revisão |
| Critério de aceite | Condição verificável de "feito" ("objetivo geral contém verbo, objeto e campo de aplicação; cada objetivo específico tem etapa correspondente na metodologia") |
| Esforço | P (< 1 h), M (algumas horas), G (exige pesquisa, coleta ou reescrita de seção). É estimativa; declare assim |
| Depende de | IDs de tasks que precisam ser feitas antes, ou "—" |

## Taxonomia de tipo

Escolha o tipo pela natureza do problema, não pela seção em que aparece.

- **Coerência interna:** desalinhamento entre problema, objetivos, referencial e metodologia.
- **Coesão/argumentação:** ligação fraca entre ideias, saltos lógicos, justificativa que não sustenta a conclusão.
- **Clareza/precisão:** termo vago, ambíguo ou não definido; objetivo sem objeto ou escopo.
- **Conteúdo ausente:** elemento exigido pela rubrica não existe (ex.: público-alvo, cronograma, critério de análise de dados).
- **Conteúdo insuficiente:** elemento existe, mas raso ou incompleto.
- **Método:** etapa, instrumento ou técnica inadequada ao objetivo, ou sem detalhamento suficiente para ser replicada.
- **Referência:** fonte ausente, desatualizada, de baixa qualidade, não localizada, ou citação sem entrada na lista (e vice-versa).
- **Formatação:** norma ABNT, template, numeração, figuras/tabelas.
- **Redação:** ortografia, gramática, pontuação, registro informal.

## Regras de severidade

Derive da revisão, nesta ordem (vale a primeira que se aplicar):

1. **Crítica:** causa ou contribui para "não apto à defesa" (coerência interna), ou falta de cronograma.
2. **Alta:** critério com veredito **Não atende**, ou perda ≥ 0,25 ponto.
3. **Média:** critério **Parcial** com perda entre 0,10 e 0,24, ou referência central "não localizada".
4. **Baixa:** perda < 0,10, ou problema apontado sem perda de pontos.

Se a revisão usou pesos próprios, aplique as regras sobre os pontos dela e diga isso nas premissas.

## Formato de saída

```
# Tasks de correção — [projeto avaliado]
Origem: revisão de [avaliador], nota estimada X,XX/10 | Parecer: apto/não apto
Total: N tasks (C críticas, A altas, M médias, B baixas) | Pontos recuperáveis: X,XX

## Visão geral
| ID | Título | Tipo | Severidade | Pontos | Esforço | Depende de |

## Detalhamento
### T01 — [Título]
**Tipo:** … | **Severidade:** … | **Critério:** … | **Pontos:** … | **Esforço:** …
**Localização:** …
**Evidência:** …
**Problema:** …
**Como resolver:**
1. …
**Critério de aceite:** …
**Depende de:** …

(repita para cada task)

## Fora da revisão (não convertido)
(opcional; uma linha por item, ou omita a seção)

Premissas: severidade derivada das regras da skill; esforço estimado; pontos conforme a revisão.
```

"Pontos recuperáveis" é a soma dos pontos em jogo. Não prometa nota final após as correções: a nova nota depende de nova avaliação.

## Exemplo de task

Observação na revisão: *Objetivos — Objetivo geral: **Parcial** (−0,25). Evidência: "desenvolver uma ferramenta para auxiliar alunos". Motivo: não define o que a ferramenta faz nem o contexto. Correção: especificar função e campo de aplicação.*

```
### T02 — Reescrever objetivo geral com função e contexto da ferramenta
**Tipo:** Clareza/precisão | **Severidade:** Alta | **Critério:** Objetivos — objetivo geral | **Pontos:** −0,25 | **Esforço:** P
**Localização:** Seção Objetivos, objetivo geral
**Evidência:** revisão cita "desenvolver uma ferramenta para auxiliar alunos" e aponta ausência de função e contexto.
**Problema:** O objetivo não diz o que a ferramenta faz nem para quem/onde, o que impede avaliar se a metodologia o atende.
**Como resolver:**
1. Definir a função principal da ferramenta (o que ela faz).
2. Delimitar público e contexto (curso, disciplina, instituição).
3. Reescrever no formato verbo + objeto + campo de aplicação.
**Critério de aceite:** objetivo geral contém verbo no infinitivo, função da ferramenta e contexto de aplicação explícitos.
**Depende de:** —
```

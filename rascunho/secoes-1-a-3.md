# Reuso e Perda de Autonomia em Microsserviços: Uma Análise do Acoplamento Induzido por Componentes Compartilhados

> Rascunho v1 (seções 1 a 3). Citações autor-data (ABNT). Referências em `referencias.bib`, todas com DOI conferido no Crossref.
> Marcadores `[REFERÊNCIA NECESSÁRIA]` e `[A CONFIRMAR]` indicam pontos a resolver (ver notas ao final).

---

## 1 Introdução

A arquitetura de microsserviços organiza um sistema como um conjunto de serviços pequenos e independentes, que se comunicam por mensagens (DRAGONI et al., 2017). A promessa central dessa abordagem é a autonomia: cada serviço deve poder ser alterado e implantado sem depender dos demais, o que facilitaria sua mudança e substituição (BOGNER et al., 2021).

Ao mesmo tempo, o reuso de software é uma prática consolidada para reduzir esforço e aumentar a qualidade (KRUEGER, 1992; FRAKES; KANG, 2005). Em microsserviços, o reuso aparece na forma de bibliotecas e componentes internos usados por vários serviços. Aqui está a tensão: quando um componente é compartilhado, uma mudança nele pode obrigar todos os serviços que o utilizam a serem modificados, testados e implantados juntos. A literatura já registra esse risco. Taibi e Lenarduzzi (2018) catalogam o uso de bibliotecas compartilhadas como *bad smell* de microsserviços, e de Toledo, Martini e Sjøberg (2020) relatam que elas acoplam equipes e atrasam correções. Badampudi, Usman e Chen (2025) observam conflito semelhante entre reuso e autonomia dos times em um contexto industrial.

Grande parte dessa evidência vem de entrevistas, ou seja, da percepção de quem desenvolve. Estudos que mineram repositórios mostram que os serviços raramente evoluem isolados (ASSUNÇÃO et al., 2023) e que há acoplamento lógico, medido pela co-mudança nos commits, em todos os sistemas analisados (AMOROSO D'ARAGONA et al., 2023). Esses estudos, porém, não separam quanto desse acoplamento vem de componentes compartilhados. Até onde foi possível verificar nas bases consultadas, falta, portanto, evidência extraída do código e do histórico sobre se o compartilhamento de fato reduz a independência entre serviços e em que condições isso ocorre. Essa lacuna importa na prática: se o reuso corrói a autonomia sem que a equipe perceba, o sistema paga o custo de ser distribuído sem obter o benefício da independência.

O **objetivo geral** deste trabalho é analisar como o compartilhamento de componentes afeta a autonomia de evolução e implantação de microsserviços, com base em indicadores de acoplamento extraídos de repositórios de sistemas reais. Os **objetivos específicos** são: (i) mapear os componentes compartilhados e o número de serviços que dependem de cada um; (ii) levantar, no histórico de commits, a co-mudança entre serviços associada a esses componentes; e (iii) caracterizar as condições em que o compartilhamento se associa à perda de autonomia, considerando o conteúdo do componente e sua abrangência. Esses objetivos orientam três questões de pesquisa:

- **RQ1:** Em que medida os serviços dependem de componentes compartilhados, considerando quantos serviços usam cada componente?
- **RQ2:** Que indícios de perda de autonomia, como mudanças coordenadas entre serviços, estão associados a esses componentes?
- **RQ3:** Em que condições o reuso de um componente compromete a autonomia dos serviços que dependem dele?

A contribuição esperada é uma caracterização, baseada em dados, das situações em que reutilizar um componente custa autonomia aos serviços, além de indicadores observáveis no repositório que permitam às equipes avaliar seus componentes compartilhados antes que o problema se instale. O restante do texto está organizado assim: a Seção 2 apresenta os trabalhos relacionados, a Seção 3 apresenta a fundamentação teórica, e as demais seções descrevem o método e os resultados esperados `[A DEFINIR]`.

---

## 2 Trabalhos Relacionados

Os trabalhos mais próximos desta proposta se dividem pelo tipo de evidência. Um grupo minera repositórios para medir co-evolução entre serviços. O outro parte da experiência de praticantes para descrever o que o compartilhamento causa.

**Mineração de repositórios.** Assunção et al. (2023) analisam 11 sistemas de código aberto, com 7.319 commits e 99.804 mudanças atômicas, e concluem que os serviços raramente mudam de forma isolada. Entre as causas que apontam estão a refatoração de APIs compartilhadas e as dependências de bibliotecas externas. É o trabalho mais próximo desta proposta, pois também usa o histórico de repositórios para observar a independência entre serviços. Diferencia-se, porém, em dois pontos: as mudanças foram rotuladas pelos próprios autores, e as bibliotecas aparecem como uma causa entre várias, sem que se isole o efeito dos componentes internos compartilhados, que é o foco deste estudo.

Amoroso d'Aragona et al. (2023) propõem uma métrica de acoplamento lógico entre microsserviços, calculada a partir dos commits e sem depender de dados de execução. Em 145 projetos, encontram acoplamento lógico em todos os sistemas, crescendo com o tempo. Este trabalho adota a mesma ideia, tomando a co-mudança como indicador de acoplamento (base da RQ2). A diferença é que a métrica original não investiga o que causa o acoplamento, e aqui ela é cruzada com a dependência de componentes compartilhados. Um estudo posterior dos mesmos autores, Amoroso d'Aragona, Li e Janes (2024), trata do chamado acoplamento aparente e das possibilidades de excluí-lo da medição `[A CONFIRMAR: ler o texto completo, pois só o resumo foi consultado]`. Ele não aborda componentes compartilhados como causa, mas alerta para um cuidado metodológico que este estudo deve incorporar ao medir co-mudança.

**Estudos com praticantes.** Taibi e Lenarduzzi (2018) catalogam 11 *bad smells* a partir de entrevistas com 72 desenvolvedores. O *smell* "Shared Libraries" aparece em 11,7% das 265 más práticas relatadas, e os entrevistados dizem que ele acopla serviços e obriga equipes a se coordenarem. Os próprios autores indicam que a nocividade, baseada em percepção, precisa de validação empírica. Este trabalho responde parcialmente a esse pedido, ao medir o efeito no código e no histórico, e não na opinião.

De Toledo, Martini e Sjøberg (2020) entrevistaram seis arquitetos de quatro empresas e relatam que bibliotecas compartilhadas acoplam times, sobrecarregam quem as mantém e exigem várias versões em paralelo. Compartilham com esta proposta a preocupação com a perda de agilidade causada por componentes compartilhados. Diferenciam-se por usar evidência qualitativa e amostra pequena, enquanto aqui se busca evidência quantitativa em sistemas abertos. Já Badampudi, Usman e Chen (2025) estudam o reuso de microsserviços em larga escala na Ericsson, com entrevistas e análise temática. Encontram ganhos de qualidade e velocidade, mas também times centrais que viram gargalo e ciclos de release em conflito. Tratam da mesma tensão entre reuso e autonomia, porém no nível de serviços reutilizados por vários times e em uma única empresa. Este estudo observa a tensão no nível do código.

**Síntese.** Há acordo de que compartilhar cria dependência entre serviços e entre equipes. A diferença está na evidência: a mineração mede o acoplamento sem identificar a causa, e os estudos sobre bibliotecas apontam uma causa provável, mas só com relatos. O Quadro 1 compara os trabalhos com a proposta.

**Quadro 1 – Comparação entre os trabalhos relacionados e a pesquisa proposta**

| Trabalho | Tipo de evidência | Objeto | Mede co-mudança? | Isola componentes compartilhados? |
|---|---|---|---|---|
| Assunção et al. (2023) | Mineração de repositórios | 11 sistemas abertos | Sim | Não (bibliotecas como uma causa entre várias) |
| Amoroso d'Aragona et al. (2023) | Mineração de repositórios | 145 projetos abertos | Sim (acoplamento lógico) | Não |
| Amoroso d'Aragona, Li e Janes (2024) | Não informado `[A CONFIRMAR]` | Acoplamento aparente | Não informado | Não |
| Taibi e Lenarduzzi (2018) | Entrevistas | 72 desenvolvedores, 61 organizações | Não | Parcial (smell "Shared Libraries") |
| de Toledo, Martini e Sjøberg (2020) | Entrevistas | 6 arquitetos, 4 empresas | Não | Sim (bibliotecas), sem medição |
| Badampudi, Usman e Chen (2025) | Estudo de caso | Ericsson, serviços reutilizados | Não | Parcial (nível de serviço) |
| **Proposta deste trabalho** | Mineração de repositórios | Sistemas abertos (oito, conforme Marco 3) | Sim | Sim (cruza co-mudança com dependência de componentes) |

Fonte: elaborado pelos autores.

**Lacuna de pesquisa.** Os estudos de mineração medem o acoplamento entre microsserviços pela co-mudança no histórico de commits (AMOROSO D'ARAGONA et al., 2023; ASSUNÇÃO et al., 2023), sem separar a parcela que vem de componentes compartilhados. Já o efeito do compartilhamento sobre a autonomia foi descrito a partir de entrevistas e estudos de caso (TAIBI; LENARDUZZI, 2018; DE TOLEDO; MARTINI; SJØBERG, 2020; BADAMPUDI; USMAN; CHEN, 2025), e Taibi e Lenarduzzi reconhecem que a nocividade apontada pelos entrevistados ainda precisa de validação empírica. Nas bases consultadas (ACM Digital Library, IEEE Xplore e Google Scholar, com as strings descritas na Seção `[A DEFINIR: seção de método]`), não identificamos estudo que relacione a co-mudança entre serviços a componentes internos compartilhados, extraindo a evidência do código e do histórico `[A CONFIRMAR: leitura integral de Amoroso d'Aragona, Li e Janes (2024)]`. Este trabalho busca preencher essa lacuna ao estimar quanto da co-mudança acompanha esses componentes e em que situações o compartilhamento impede a evolução independente dos serviços.

---

## 3 Fundamentação Teórica

Esta seção apresenta os conceitos que sustentam as decisões do estudo: o que é autonomia em microsserviços, o que se entende por reuso e componente compartilhado, como o acoplamento é definido e medido, e quais cuidados a mineração de repositórios exige.

### 3.1 Microsserviços e autonomia

Um microsserviço é, em linhas gerais, um processo independente que interage com os demais por troca de mensagens, e uma arquitetura de microsserviços é um sistema distribuído formado só por esses serviços (DRAGONI et al., 2017). A pesquisa sobre como arquitetar sistemas com microsserviços já foi sistematizada em mapeamentos da literatura (DI FRANCESCO; LAGO; MALAVOLTA, 2019). A implantação independente é considerada um princípio central em grande parte das definições de microsserviços (NERI et al., 2019). O ganho esperado está em ter serviços de granularidade fina, fracamente acoplados e implantáveis de forma independente, que deveriam ser fáceis de alterar e substituir (BOGNER et al., 2021). Trata-se de uma promessa de projeto, e a literatura registra desafios para mantê-la na prática (JAMSHIDI et al., 2018). Neste trabalho, **autonomia** é a capacidade de um serviço mudar e ser implantado sem exigir mudança simultânea em outros serviços. É essa propriedade que se quer verificar, e a co-mudança entre serviços será o indício observável de sua perda.

### 3.2 Reuso de software e componentes compartilhados

Reuso é a criação de sistemas a partir de artefatos já existentes, em vez de construí-los do zero (KRUEGER, 1992), prática que a pesquisa em engenharia de software associa a ganhos de produtividade e qualidade (FRAKES; KANG, 2005). Em um sistema de microsserviços, o reuso pode ocorrer de formas distintas: um serviço pode ser reutilizado por outros por meio de sua interface, ou o código pode ser reutilizado por meio de bibliotecas e componentes incorporados a cada serviço. Este estudo trata da segunda forma, em que um **componente compartilhado** é um módulo de código interno ao sistema usado por mais de um serviço. Essa distinção importa porque, no reuso por incorporação de código, uma alteração no componente atinge diretamente o código dos serviços que o usam. Os dois eixos de análise do estudo derivam daí: **quantos serviços** dependem do componente (abrangência, RQ1) e **o que ele contém**, código técnico ou regra de domínio (conteúdo, RQ3).

### 3.3 Acoplamento e acoplamento lógico

O acoplamento mede o grau de interdependência entre módulos (STEVENS; MYERS; CONSTANTINE, 1974), e a ocultação de informação é o critério clássico para decompor sistemas de modo que mudanças em um módulo não se propaguem aos demais (PARNAS, 1972). Há, contudo, duas formas de observá-lo. O acoplamento estrutural vem das dependências declaradas no código. O **acoplamento lógico** vem da evolução: dois elementos são logicamente acoplados quando mudam juntos repetidamente no histórico (GALL; HAJEK; JAZAYERI, 1998), o que pode ser identificado minerando o histórico de versões (ZIMMERMANN et al., 2005). As duas visões se relacionam, mas não coincidem (AJIENKA; CAPILUPPI, 2017). Para microsserviços, Amoroso d'Aragona et al. (2023) adaptam o acoplamento lógico aos commits que alteram mais de um serviço.

Aqui adota-se o acoplamento lógico, por duas razões. Primeiro, ele mede o que importa para a autonomia, que é a necessidade de mudar serviços juntos, e não apenas a existência de uma dependência. Segundo, os sistemas estudados referenciam os componentes compartilhados diretamente pelo código-fonte, sem pacotes versionados, o que inviabiliza indicadores baseados em versões. A dependência estrutural, por sua vez, será usada para mapear os componentes compartilhados (RQ1), e o cruzamento entre as duas visões responde à RQ2.

### 3.4 Mineração de repositórios

A mineração de repositórios extrai de sistemas de controle de versão e plataformas de hospedagem os dados necessários para estudar a evolução do software. Seu uso exige cuidado com a validade dos dados: Kalliamvakou et al. (2014) alertam, para repositórios do GitHub, que há riscos de interpretação, como projetos que não refletem desenvolvimento real de software. Neste trabalho, esse cuidado orienta a seleção de sistemas de código aberto e a leitura dos commits como indício, e não como prova, de coordenação entre serviços.

---

## Notas para a revisão da equipe

1. **Lacuna a revalidar.** O trabalho de Amoroso d'Aragona, Li e Janes (2024) é posterior à busca descrita no Marco 3? Ele não consta nos estudos selecionados. Só o resumo foi lido: vale ler o texto completo para confirmar que não trata de componentes compartilhados como causa. Há também uma tese de doutorado (Tampere, 2026) do primeiro autor sobre causas do acoplamento lógico, que não incluí por não ser artigo revisado por pares, mas que vale consultar para ver se afeta a lacuna.
2. **Dados dos estudos S1 a S5** (tamanho de amostra, resultados, limitações) vêm das fichas do Marco 3. Conferi autoria, título, veículo, volume, páginas e DOI no Crossref, mas **não li os textos completos**. Antes da entrega, conferir os números no PDF.
3. **Badampudi et al.**: publicado online em dez/2024 e no volume 30 (2025). Mantive 2025, como no Marco 3. A ABNT admite qualquer uma, mas convém padronizar.
3b. **Di Francesco et al. (2019)**: citado só como panorama da área (Seção 3.1), com base no título e no veículo. Não li o texto. Se quiser usá-lo para algo mais específico, leia-o antes e ajuste a frase.
4. **Implantação independente**: usei Neri et al. (2019, *SICS Software-Intensive Cyber-Physical Systems*), que a trata como princípio central das definições de microsserviços, e Bogner et al. (2021, *Empirical Software Engineering*), que descreve a ideia. Ambos têm DOI conferido. Neri et al. é uma revisão multivocal (inclui literatura cinzenta), mas o artigo em si é revisado por pares. Li o trecho em versão HTML do preprint, então vale conferir no PDF publicado. O artigo de 2024 (nota 1) é acesso aberto pelo DOI, mas os repositórios bloqueiam download automático, então a leitura fica com a equipe.
5. **Seções 3.3 e 3.4** podem ganhar uma figura (exemplo de commit que altera dois serviços via componente compartilhado), a criar pela equipe.
6. A Seção 3.4 está enxuta. Se o método usar outras técnicas (ex.: detecção de dependências, classificação do conteúdo do componente), faltam seções para elas.

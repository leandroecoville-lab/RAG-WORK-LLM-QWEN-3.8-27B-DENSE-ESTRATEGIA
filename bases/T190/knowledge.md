# T190 — Verifier Loop

**Nome canônico:** Verifier Loop  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T190  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ciclo de verificação

## T190:C01 — conceito

Ciclo de produzir, verificar e corrigir até satisfazer um critério ou atingir limite. O verificador pode ser teste executável, validação de dados, checagem de fonte ou modelo com rubrica. É essencial separar evidência de correção de uma simples declaração do gerador de que revisou a resposta.

Como funciona:
- Produzir candidato e associar requisitos verificáveis.
- Executar verificador e registrar falhas específicas.
- Corrigir apenas problemas identificados e repetir dentro de um orçamento.

## T190:C02 — aplicacao

Quando usar:
- Geração de código, objetos estruturados ou respostas com fontes.
- Erros podem ser localizados e corrigidos de forma objetiva.

Quando não usar:
- Verificador não observa o resultado real ou aprova qualquer justificativa textual.

Implementação proposta:
- Definir estados aprovado, rejeitado e inconclusivo.
- Detectar oscilação e repetição de tentativas equivalentes.
- Preservar melhor candidato e não perder teste anteriormente aprovado.

Aplicação LAI proposta:
Proposta: a Helena validar artefatos e recibos antes de declarar conclusão, guardando resultados de cada correção para auditoria.

## T190:C03 — riscos_validacao

Armadilhas:
- Gerador pode adaptar-se ao teste sem resolver o requisito real.
- Loop sem condição de parada consome recursos indefinidamente.

Métricas sugeridas:
- Correções aceitas por tentativa e regressões.
- Falsos positivos do verificador e custo por resultado aprovado.

Testes propostos:
- Introduzir falha conhecida e verificar que o ciclo a detecta e corrige.
- Usar tarefa impossível com recursos disponíveis e exigir término inconclusivo explícito.

## T190:C04 — perguntas_proveniencia

Pergunta: O mesmo modelo pode verificar?
Resposta: Pode, mas isso reduz independência e exige medir falsos positivos.

Pergunta: Passar no verificador prova tudo?
Resposta: Prova apenas os critérios cobertos e a confiabilidade daquele verificador.

Pergunta: Passou uma vez, está resolvido para sempre?
Resposta: Não. Mudança de conteúdo, dependências ou ambiente pode invalidar o resultado anterior.

Pergunta: O próprio gerador pode verificar?
Resposta: Pode contribuir com crítica, mas seus erros podem ser correlacionados; critérios objetivos e fontes independentes fortalecem a evidência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T190:C05 — mecanismo_avancado

Cada veredito deve vincular-se à revisão exata do artefato inspecionado. Uma correção posterior pode invalidar testes anteriores, inclusive quando tenta resolver outro problema. Como proposta de controle, mantenha hash ou revisão, lista de falhas e critérios de progresso; repetições sem melhoria e ciclos entre duas versões precisam encerrar com diagnóstico. Um timeout do verificador é desconhecimento, não aprovação.

Condição de contorno:
O ciclo pode nunca convergir quando requisitos são inconsistentes, o gerador não tem capacidade ou o verificador produz falsos negativos.

Contrato proposto:
- Entradas: Artefato versionado, critérios executáveis ou rubrica, orçamento e evidências anteriores.
- Saídas: Versão aprovada para critérios definidos ou relatório explícito de pendências.
- Estado: Histórico de revisões, vereditos, falhas e consumo de tentativas.
- Invariante: Aprovação sempre referencia o mesmo conteúdo que será entregue ou executado.

Compromissos de projeto:
- Mais iterações oferecem correções e ampliam custo e risco de regressão.
- Verificador estrito pode rejeitar alternativas válidas quando o contrato é incompleto.

## T190:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aprovar uma versão, modificá-la e reutilizar deliberadamente o veredito antigo. Esperar invalidação; injetar também alternância entre duas correções para testar parada por ciclo.

Plano de avaliação proposto:
Plano proposto: comparar geração única e loop limitado em casos com defeitos conhecidos. Medir taxa de correção, regressões, falsos aceites, custo e não convergência; aprovar apenas se o ganho externo justificar o esforço adicional.

Comparações:
- T195 (complements): Execução pode fornecer evidência objetiva para alguns critérios do loop, sem cobrir toda a especificação.

Afirmação rastreável:
Verificadores treinados podem classificar soluções e orientar seleção de candidatos, como no estudo de problemas matemáticos.
Suporte: related; fontes: C-S043
Limite: O protocolo de revisão, progresso e parada desta ficha é proposta de engenharia; o paper não o padroniza.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T190:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculou vereditos a revisões. O aprofundamento acrescenta classificação das falhas, reparos mínimos e condições de parada que preservam progresso sem transformar o loop em geração ilimitada.

Falha acionável
O verificador deve devolver critério, evidência e localização do defeito. Separe erro do artefato, requisito ambíguo e falha do executor. Cada classe pede ação distinta: corrigir, esclarecer ou repetir infraestrutura. Passar a mesma mensagem genérica ao gerador tende a criar mudanças grandes e pouco controladas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

Reparo com escopo
Uma correção deve declarar quais partes pode alterar e quais propriedades precisam ser preservadas. Reexecute testes afetados e barreiras obrigatórias na revisão final. O AutoClean descreve fixers e verificações por propriedade; a proposta transferível é reduzir superfície de mudança e manter evidência ligada ao conteúdo entregue.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

Progresso e encerramento
Use uma medida explícita de falhas remanescentes e detecte ciclos de revisões. Se a correção de uma propriedade quebra outra repetidamente, a hipótese ou o escopo pode estar errado. Encerre com pendências verificáveis quando o orçamento acabar, sem converter exaustão em aprovação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

USO AVANÇADO — Correção de código localizada
Cenário: Um teste falha num conjunto pequeno de arquivos.
Estratégia: Forneça ao modelo o erro mínimo e o contrato, gere patch restrito e valide. Amplie o contexto somente quando a falha indicar dependência externa ao escopo.
Papel do modelo pequeno: Um 3–7B pode reparar padrões simples; um 8–14B pode tratar relações maiores, conforme teste.
Aceite proposto: Entregar revisão que passa critérios e preserva invariantes, com custo e tentativas registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

USO AVANÇADO — Objeto estruturado com regras
Cenário: A saída viola formato ou uma regra de negócio.
Estratégia: Corrija apenas campos apontados e revalide o objeto completo. Se a regra depende de fato ausente, busque evidência em vez de inventar um valor para satisfazer o schema.
Papel do modelo pequeno: Um pequeno modelo funciona como proponente, não como autoridade de aceitação.
Aceite proposto: Nenhuma alteração silenciosa em campos já verificados; resultado final consistente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Loops curtos e critérios estreitos favorecem modelos pequenos sem prometer reparo geral.
8–14B: Use contexto incremental e ferramentas para reduzir adivinhação em dependências.
15–30B: Um 15–30B pode justificar problemas mais difíceis, mas continua sujeito ao orçamento e ao mesmo verificador.
Requisitos de treino/runtime: Runtime de geração, checagem e revisão; não implica aprendizagem persistente do modelo.
Não aplicar quando: Não considerar timeout, erro de teste ou ausência de feedback como aprovação.

## T190:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Candidatos recebem avaliação e alimentam novas propostas.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Verificadores avaliam propriedades após geração e CI.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Há geração e crítica por ferramentas; isso não implica refinamento livre multiagente.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T190:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T190 → T195 [requires]
Como combinar: AutoClean combina propostas e verificações executáveis antes de prosseguir.
Interface: Revisão, resultados e falhas localizadas.
Condição: Verificação ligada ao conteúdo que será entregue.
Aceite proposto: Introduzir defeitos conhecidos e confirmar bloqueio.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T190 → T200 [complements]
Como combinar: Revisores por propriedade acrescentam checagem antes de revisão humana no AutoClean.
Interface: Artefato e relatórios separados.
Condição: Critérios e limites da revisão são explícitos.
Aceite proposto: Medir falhas detectadas e discordâncias.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Preservar última versão válida e rejeitar regressões.
- Registrar conclusão inconclusiva quando o orçamento ou infraestrutura impede verificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de tarefas concluídas corretamente e custo do loop com uma chamada de fronteira. Verificação pode amplificar utilidade de um modelo pequeno, desde que o critério cubra a falha relevante.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T189, T192, T195, T200

## Fontes primárias associadas

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S051 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback verbal e memória episódica podem melhorar tentativas posteriores sem atualizar pesos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

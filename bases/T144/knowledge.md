# T144 — ReAct Pattern

**Nome canônico:** ReAct Pattern  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T144  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reasoning and acting

## T144:C01 — conceito

Padrão de agente que intercala deliberação operacional, ação de ferramenta e observação. A observação atualiza o próximo passo, permitindo adaptar a execução a informação externa. A existência do ciclo não demonstra que o modelo sabe verificar tudo o que encontra.

Como funciona:
- Identificar a próxima lacuna de informação ou ação útil.
- Emitir chamada de ferramenta e obter observação do ambiente.
- Atualizar estado e escolher nova ação ou término com evidência.

## T144:C02 — aplicacao

Quando usar:
- Tarefas exploratórias com dependências descobertas durante execução.
- Consultas que exigem ferramentas e correção de percurso.

Quando não usar:
- Processo determinístico já conhecido em que chamadas de LLM em cada passo só aumentam custo.

Implementação proposta:
- Limitar número de passos, tempo e repetição da mesma ação.
- Registrar observações como dados, separadas das instruções do agente.
- Exigir condição de término observável e preservar referências aos resultados.

Aplicação LAI proposta:
Proposta: usar ciclos ReAct limitados para investigação da Helena, com estado resumido e evidências externas persistidas.

## T144:C03 — riscos_validacao

Armadilhas:
- Loop pode repetir buscas sem acumular informação nova.
- Texto retornado por ferramenta pode tentar introduzir instruções indevidas.

Métricas sugeridas:
- Passos por tarefa resolvida e chamadas redundantes.
- Correção final com e sem ferramentas em conjunto de avaliação.

Testes propostos:
- Produzir resultado de ferramenta vazio e conferir adaptação ou abstenção.
- Injetar instrução estranha em documento recuperado e verificar que não altera a política do runtime.

## T144:C04 — perguntas_proveniencia

Pergunta: ReAct exige mostrar pensamentos privados?
Resposta: Não. O sistema pode registrar decisões operacionais curtas, ações e observações.

Pergunta: Mais ciclos significam mais inteligência?
Resposta: Não. Sem informação nova ou verificação, podem apenas repetir o erro.

Pergunta: Reagir a toda observação é sempre mais inteligente?
Resposta: Não. Algumas observações apenas confirmam passos previsíveis; a chamada adicional pode não mudar nenhuma decisão.

Pergunta: Como distinguir retry útil de loop?
Resposta: Pela categoria do erro, mudança de condições e evidência de progresso; igualdade de texto sozinha não decide todos os casos.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T144:C05 — mecanismo_avancado

A vantagem do ciclo observação–ação aparece quando a informação recém-obtida muda a próxima escolha. Seu custo cresce se cada rodada reenviar grandes resultados anteriores ou repetir uma consulta porque o estado de conclusão não está explícito. Um controle proposto identifica observações pelo conteúdo e pela origem, registra o que elas mudaram e diferencia investigação adicional de repetição sem informação nova.

Condição de contorno:
Em tarefas com dependências já conhecidas e ferramentas independentes, o ciclo estritamente serial pode introduzir latência evitável.

Contrato proposto:
- Entradas: Estado da tarefa, última observação, catálogo de ações e orçamento.
- Saídas: Próxima ação justificada por evidência operacional ou término verificável.
- Estado: Chamadas anteriores, observações referenciadas e hipóteses atualizadas.
- Invariante: Repetir uma ação exige nova finalidade, mudança de entrada ou política explícita de recuperação.

Compromissos de projeto:
- Reagir a cada resultado aumenta adaptação e também número de interações com o modelo.
- Agrupar observações economiza chamadas e pode retardar a percepção de um resultado decisivo.

## T144:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma ferramenta devolve repetidamente o mesmo resultado sem avanço; exigir identificação da repetição e mudança de estratégia ou encerramento com limitação.

Plano de avaliação proposto:
Comparar ReAct serial, planejamento antecipado e execução de grupos independentes. Fixar informação disponível e critérios de sucesso. Medir observações úteis por chamada, repetições, latência e conclusão; usar cenários onde resultados realmente alterem decisões.

Comparações:
- T143 (alternative): O plano antecipado evita algumas rodadas, mas depende mais de premissas estáveis.
- T218 (complements): Um detector de repetição pode limitar ciclos sem informação adicional.

Afirmação rastreável:
LLMCompiler identifica custos da chamada sequencial e propõe planejamento, despacho e execução paralela de funções.
Suporte: direct; fontes: V3C-S002
Limite: A comparação apoia um limite do serialismo, não a superioridade de paralelismo em tarefas com dependências desconhecidas.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T144:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou ganho informacional por observação. A camada nova delimita episódios de exploração, separa hipótese de fato e usa memória de decisões para impedir que cada turno reabra problemas já resolvidos.

Observação com pergunta associada
Cada chamada deve responder a uma lacuna explícita: localizar arquivo, verificar hipótese ou obter dado necessário. Ao retornar, registre se a lacuna foi resolvida e qual evidência mudou. Isso permite avaliar o ciclo por decisões melhoradas, sem depender da extensão de deliberação ou da quantidade bruta de ferramentas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

Subciclo dentro de contrato
Um executor reativo pode explorar livremente dentro de uma micro-missão, mas não alterar silenciosamente seu critério de término. Quando descobrir que o objetivo é impossível ou que falta autorização, devolva esse estado ao supervisor. A flexibilidade local fica separada da responsabilidade por redefinir o trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

Hipóteses com validade
Mantenha hipóteses descartadas e a evidência usada, associadas à revisão observada. Uma mudança de código pode reabrir uma hipótese legitimamente; repetição sem mudança não. Essa distinção evita tanto a perseveração quanto o bloqueio indevido de caminhos que se tornaram relevantes após nova informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

USO AVANÇADO — Investigação de teste intermitente
Cenário: O mesmo teste falha apenas em algumas condições.
Estratégia: Comece por reproduzir e registrar ambiente; escolha próxima ferramenta conforme a hipótese ainda não testada. Se a falha não se repetir, preserve a incerteza e busque evidência adicional. Não aplique correção apenas porque um novo run passou.
Papel do modelo pequeno: 8–14B organiza hipóteses locais; 15–30B relaciona concorrência e dependências.
Aceite proposto: Proposta: medir hipóteses eliminadas, chamadas redundantes e correções confirmadas sob repetição controlada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

USO AVANÇADO — Navegação de catálogo de ferramentas
Cenário: A primeira ferramenta encontrada não possui os campos necessários.
Estratégia: Inspecione o schema, reformule a busca por capacidade e teste a compatibilidade antes de invocar. Guarde candidatos rejeitados e motivo para não redescobrir repetidamente o mesmo contrato inadequado.
Papel do modelo pequeno: 3–7B executa escolhas entre poucos candidatos e estados tipados.
Aceite proposto: Proposta: usar consultas ambíguas e contratos próximos; aceitar seleção correta ou impedimento explícito dentro do orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: ciclos curtos de seleção e leitura, com pequena lista de ações e resultado verificável.
8–14B: Proposta: diagnóstico local com memória de hipóteses e evidências estruturadas.
15–30B: Proposta: exploração mais ampla dentro de uma missão delimitada, com supervisão do objetivo.
Requisitos de treino/runtime: O runtime precisa conservar estado factual separado do texto gerado e limitar tempo, ferramentas e repetição.
Não aplicar quando: Evitar ciclos abertos quando uma função determinística ou um plano estável já resolve a tarefa com menos chamadas.

## T144:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: O executor utiliza ReAct dentro do plano.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Hiring Assistant usa ReAct localmente; isso não prova que um loop genérico sem estados e verificadores seja apropriado a qualquer modelo pequeno.
Consultas registradas: V4C-Q006, V4C-Q009, V4C-Q010.

## T144:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T144 → T218 [feeds]
Como combinar: Mudanças de hipótese e observações fornecem sinais para detectar estagnação.
Interface: Estado semântico, evidências novas e ação realizada.
Condição: O detector distingue repetição legítima após mudança de entrada.
Aceite proposto: Injetar respostas idênticas de ferramentas e exigir parada ou mudança fundamentada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T144 → T208 [complements]
Como combinar: O supervisor delega exploração local e recebe resultado ou impedimento.
Interface: Missão, fatos confirmados e próximo requisito não satisfeito.
Condição: Escopo e término são definidos antes da delegação.
Aceite proposto: Comparar retorno do executor com o plano vigente, detectando desvio de objetivo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

CONTROLES DE FALHA
- Não promover uma sugestão do modelo a observação da ferramenta.
- Proibir que o loop esconda falha mudando o requisito que pretendia satisfazer.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de diagnóstico correto e custo por resolução com fronteira sob mesmas ferramentas. Loops adicionais podem ampliar erros de um modelo pequeno quando os verificadores são fracos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T190, T199

## Fontes primárias associadas

### C-S011 — ReAct: Synergizing Reasoning and Acting in Language Models

[https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alternância entre deliberação explícita, ações e observações externas em tarefas de agentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T142 — Agent Frameworks com Planning

**Nome canônico:** Agent Frameworks com Planning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T142  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** frameworks de agentes com planejamento

## T142:C01 — conceito

Família de frameworks que coordena estado, ferramentas e planejamento de agentes. O plano pode ser produzido pela LLM ou por código, enquanto o framework executa transições. Adotar uma biblioteca não garante qualidade do plano, recuperação após falhas nem respeito às regras da aplicação.

Como funciona:
- Representar estado da missão e etapas de execução.
- Converter decisões de planejamento em transições observáveis.
- Executar nós, persistir resultados e decidir término ou replanejamento.

## T142:C02 — aplicacao

Quando usar:
- Missões com várias etapas e ferramentas.
- Necessidade de inspeção, retomada e controle de fluxo explícito.

Quando não usar:
- Fluxo simples e fixo em que um serviço convencional resolve com menor complexidade.

Implementação proposta:
- Escolher framework pela necessidade de estado e replay, não pelo número de abstrações.
- Separar planejador, executor e verificador por contratos.
- Definir critérios de término e testes para transições ilegais.

Aplicação LAI proposta:
Proposta: comparar o runtime atual da Helena com uma implementação mínima de grafo antes de decidir incorporar outro framework.

## T142:C03 — riscos_validacao

Armadilhas:
- Plano bonito sem precondições gera ações inexequíveis.
- Estado apenas em memória desaparece quando o processo cai.

Métricas sugeridas:
- Conclusão correta por missão e número de replanejamentos.
- Esforço de operação, replay e diagnóstico de falhas.

Testes propostos:
- Interromper missão entre duas etapas e conferir retomada sem repetir efeitos.
- Apresentar plano com dependência ausente e exigir rejeição antes da execução.

## T142:C04 — perguntas_proveniencia

Pergunta: Framework com planning pensa melhor sozinho?
Resposta: Não. Ele organiza execução; a qualidade depende de modelos, ferramentas e validação.

Pergunta: LangGraph impõe um planejador?
Resposta: Não. Seu runtime permite definir arquitetura e controle de fluxo.

Pergunta: Um reducer que concatena listas é idempotente?
Resposta: Em geral, não: aplicar duas vezes a mesma atualização duplica elementos, salvo deduplicação por identidade.

Pergunta: Compilação do grafo prova que o plano resolve a tarefa?
Resposta: Não. Ela verifica aspectos estruturais do grafo, enquanto viabilidade e suficiência do plano exigem critérios da tarefa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T142:C05 — mecanismo_avancado

Em um runtime de grafos, a composição do estado é tão importante quanto o plano. Nós paralelos podem produzir atualizações para a mesma chave; sem regra de combinação, ocorre conflito ou sobrescrita conforme o runtime. Reducers com concatenação também podem duplicar resultados quando há reexecução. Definir identidade dos itens e semântica de merge permite distinguir repetir processamento de registrar nova evidência.

Condição de contorno:
Um grafo que compila corretamente ainda pode conter ciclos sem progresso, dependências semânticas omitidas ou reducers inadequados.

Contrato proposto:
- Entradas: Estado tipado, nós, transições, políticas de merge e plano corrente.
- Saídas: Atualizações do estado, tarefas prontas e motivo de término ou interrupção.
- Estado: Versões do grafo, checkpoint, reducers e itens já confirmados.
- Invariante: Atualizações concorrentes preservam identidade e não descartam silenciosamente resultados de outro nó.

Compromissos de projeto:
- Estado compartilhado simplifica coordenação e torna conflitos mais frequentes.
- Subgrafos isolados reduzem acoplamento, exigindo contratos explícitos na junção.

## T142:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois nós escrevem na mesma lista e um é reexecutado após falha; verificar que a política escolhida não perde nem duplica resultados lógicos.

Plano de avaliação proposto:
Comparar fluxo simples e grafo com paralelismo na mesma tarefa. Fixar modelos e ferramentas. Medir repetição de nós, coerência do estado, tempo e conclusão por objetivo. Escolher a abstração quando sua vantagem compensar custo de estado e depuração.

Comparações:
- R008 (distinct_from): LangGraph é um runtime concreto; a família de frameworks com planejamento inclui decisões que o aplicativo ainda precisa definir.
- T208 (complements): Planner–Executor define responsabilidades que podem ser representadas em nós separados.

Afirmação rastreável:
LangGraph define canais de estado e reducers para combinar atualizações dos nós.
Suporte: direct; fontes: V3C-S006
Limite: As regras exatas dependem da versão; requisitos de deduplicação do domínio não são fornecidos automaticamente.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T142:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou estado e reducers. A nova camada trata o framework como interpretador de uma linguagem operacional restrita, com separação entre plano proposto, validação e comandos efetivamente executados.

Representação intermediária
Defina um conjunto pequeno de operações, condições e dependências que o agente pode propor. Compile esse plano para o runtime somente após checar referências e caminhos de término. Isso reduz o espaço de ações de um modelo pequeno e permite rejeitar planos inválidos sem executar ferramentas para descobrir o erro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S006.

Estado de controle separado
Mensagens do modelo não devem ser a única fonte de status. Mantenha no controlador etapas elegíveis, leases, resultados e prazos; o texto contém interpretação e evidência. Assim, uma compactação ou mudança de prompt não apaga a informação de que uma ação já foi confirmada ou continua ambígua.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V4C-S015.

Evolução por compatibilidade
Uma missão em andamento precisa conhecer a versão do plano e do interpretador. Ao atualizar ferramentas ou nós, decida se ela continua na versão anterior, migra com conversão explícita ou é interrompida. Um deploy que compila corretamente ainda pode modificar o significado de comandos de históricos existentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

USO AVANÇADO — Agente de atendimento técnico delimitado
Cenário: O processo sempre coleta diagnóstico, consulta documentos e prepara ação.
Estratégia: Modele etapas recorrentes em código e permita ao modelo selecionar perguntas e evidências dentro delas. Só abra planejamento livre quando o fluxo conhecido não cobrir a solicitação, preservando o estado e o motivo da saída.
Papel do modelo pequeno: 3–7B preenche operações locais; 8–14B escolhe caminhos entre poucas alternativas.
Aceite proposto: Proposta: comparar conclusão, passos inúteis e falhas de contrato com um loop inteiramente livre.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

USO AVANÇADO — Workflow de migração de código
Cenário: Várias bibliotecas precisam ser atualizadas com dependências.
Estratégia: Gere um plano por módulo, valide a ordem e execute em checkpoints. Quando build falhar, replaneje somente o subgrafo afetado; resultados anteriores são reutilizados apenas se suas entradas continuarem válidas.
Papel do modelo pequeno: 15–30B propõe dependências e reparos; o framework conserva execução e verificação.
Aceite proposto: Proposta: interromper, atualizar um módulo e retomar; medir trabalho reutilizado corretamente e testes invalidados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: executor de uma linguagem pequena de tarefas com esquemas curtos e respostas verificáveis.
8–14B: Proposta: planejamento de workflows de domínio conhecido, com compilação e testes do plano.
15–30B: Proposta: supervisão de subgrafos e tratamento de exceções, sem substituir o interpretador determinístico.
Requisitos de treino/runtime: Exige schemas, controle de versão e persistência do runtime; instalar uma biblioteca não produz essas políticas.
Não aplicar quando: Evitar framework complexo para uma chamada isolada ou quando o domínio não possui estados e critérios de término definidos.

## T142:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor, Cadence e Hiring Assistant sustentam princípios diferentes; não se atribui um framework específico ao operador sem identificação explícita.
Consultas registradas: V4C-Q002, V4C-Q003, V4C-Q010.

## T142:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T142 → T143 [feeds]
Como combinar: O planejador emite a representação que o framework valida e executa.
Interface: Plano versionado com entradas, dependências e resultados exigidos.
Condição: As operações pertencem ao catálogo permitido.
Aceite proposto: Gerar planos adversos e conferir rejeição antes de qualquer efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T142 → T159 [complements]
Como combinar: Persistência conserva as fronteiras confirmadas do plano ao longo de falhas.
Interface: Histórico de comandos, resultados e versão do interpretador.
Condição: Operações externas são separadas da reconstrução.
Aceite proposto: Retomar uma missão interrompida e comparar efeitos com a execução sem falha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não deixar o modelo sobrescrever estados confirmados por texto de planejamento.
- Exigir migração explícita quando nomes de etapas ou significado de argumentos mudarem.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare framework restrito com modelo de fronteira usando o mesmo catálogo e verificadores. Uma arquitetura melhor pode reduzir erros de execução sem ampliar conhecimento geral do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T159, T160, R008

## Fontes primárias associadas

### C-S009 — LangGraph overview

[https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime de grafos com estado, controle de fluxo e integração de operações determinísticas e de LLM.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

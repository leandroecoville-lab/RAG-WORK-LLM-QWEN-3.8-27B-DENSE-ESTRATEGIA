# R008 — LangGraph

**Nome canônico:** LangGraph  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** LangGraph runtime

## R008:C01 — conceito

Runtime e framework de orquestração para agentes com estado e fluxos em grafo. Permite combinar nós determinísticos e chamadas de modelos, controlar transições e integrar persistência. Não é uma LLM, um RAG pronto nem um planejador universal; essas partes precisam ser projetadas pela aplicação.

Como funciona:
- Definir estado, nós e arestas do workflow.
- Executar transições segundo condições e resultados.
- Usar checkpointers e stores apropriados quando continuidade e memória forem necessárias.

## R008:C02 — aplicacao

Quando usar:
- Aplicação precisa de controle explícito de estado e fluxo.
- Missões exigem interrupção, retomada e observabilidade.

Quando não usar:
- Adotar framework apenas para uma única chamada simples sem necessidade de estado.

Implementação proposta:
- Fixar versão e consultar documentação correspondente antes de integrar.
- Construir prova pequena com modelo local ou remoto por adaptador.
- Escolher persistência durável e política de migração do estado para uso real.

Aplicação LAI proposta:
Proposta: avaliar LangGraph como componente possível da Helena somente após comparar requisitos e capacidades já existentes.

## R008:C03 — riscos_validacao

Armadilhas:
- Exemplo com backend em memória não demonstra retomada após reinício.
- Misturar side effects no replay pode duplicar ações se o fluxo não foi projetado para isso.

Métricas sugeridas:
- Conclusão correta de workflow e retomada após falha.
- Custo operacional e complexidade comparados ao runtime existente.

Testes propostos:
- Interromper o processo e retomar usando armazenamento persistente.
- Atualizar schema de estado e testar compatibilidade com missões já iniciadas.

## R008:C04 — perguntas_proveniencia

Pergunta: Precisa usar LangChain para usar LangGraph?
Resposta: A documentação consultada informa que não, embora exemplos frequentemente usem suas integrações.

Pergunta: Instalar LangGraph dá memória factual correta?
Resposta: Não. É preciso definir conteúdo, proveniência e recuperação.

Pergunta: O redutor padrão concatena mensagens concorrentes?
Resposta: Não. É necessário escolher uma regra adequada ao canal e testar conflitos e repetição.

Pergunta: O store substitui o checkpointer da conversa?
Resposta: Não. O store compartilha dados entre threads; a retomada do estado da thread exige persistência apropriada.

Escopo das fontes:
Documentação oficial consultada descreve grafo, persistência e ausência de arquitetura de agente prescrita. O roteiro de integração e avaliação é proposta editorial.

## R008:C05 — mecanismo_avancado

No LangGraph, nós devolvem atualizações parciais e cada canal de estado define como combiná-las. O redutor padrão substitui o valor; acumulação precisa de regra explícita. Isso torna o merge parte da semântica, especialmente quando vários nós executam no mesmo superpasso. Separar schemas de entrada, saída e estado interno organiza a interface, mas não filtra automaticamente o streaming. Assim, um canal omitido da resposta de invoke ainda pode aparecer em eventos transmitidos se a aplicação não selecionar a projeção adequada. Checkpointer por thread e store entre threads também representam escopos diferentes.

Condição de contorno:
Persistir estado não torna o redutor correto nem converte um canal privado em fronteira de acesso. Compatibilidade depende das versões do grafo e do backend.

Contrato proposto:
- Entradas: Atualizações tipadas, identificação da thread, versão do grafo e projeção permitida para streaming.
- Saídas: Estado consolidado e eventos filtrados para cada consumidor.
- Estado: Canais, redutores, checkpoints e namespace do store explicitamente separados.
- Invariante: Cada atualização preserva a identidade dos fatos; nenhuma saída pública inclui canais excluídos pelo contrato.

Compromissos de projeto:
- Redutor acumulativo conserva contribuições, mas pode duplicar mensagens sem identidade estável.
- Streaming melhora acompanhamento, porém amplia as superfícies que precisam de projeção e validação.

## R008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois nós escrevem no mesmo canal e um inclui dado interno. Variar ordem de conclusão, inspecionar invoke e stream; exigir merge previsto e ausência do dado no consumidor público.

Plano de avaliação proposto:
Comparar execução serial com paralela, fixando entradas e resultados dos nós. Medir equivalência do estado, duplicações, eventos indevidos e latência; adotar concorrência somente preservando as invariantes definidas.

Comparações:
- R017 (distinct_from): LangChain compõe agentes em nível mais alto; LangGraph expõe diretamente estado, transições e fusão de atualizações.
- T142 (distinct_from): Framework com planejamento é uma família; configurar LangGraph não acrescenta um planejador automaticamente.

Afirmação rastreável:
Schemas de entrada e saída restringem invoke, mas não ocultam canais do streaming por padrão.
Suporte: direct; fontes: V3C-S006
Limite: Comportamento documentado da Graph API consultada; mecanismos concretos devem corresponder à versão integrada.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R008:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o merge e a persistência anteriores com evolução de grafos em execução, testes algébricos de junção e isolamento de resultados que chegam depois da mudança de intenção.

Evolução com conversas abertas
Proposta: versionar grafo, schema e política junto do checkpoint. Classificar migrações em leitura compatível, transformação explícita ou encerramento controlado. Manter o executor antigo enquanto houver estados incompatíveis evita reinterpretar um nó pendente com significado novo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

Junção sob reentrega
Testar redutores com permutações, duplicatas e resultados tardios. Associatividade ou idempotência só devem ser exigidas quando o domínio permite; uma sequência de decisões pode exigir ordem. Registrar revisão da intenção em cada ramo permite rejeitar uma resposta correta para uma pergunta já cancelada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

Estado público por projeção
Construir uma projeção de saída a partir do estado validado, separada do estado de trabalho. O fluxo de eventos recebe a mesma revisão e política de exposição. A proposta trata vazamento de eventos e resposta final como superfícies distintas, com testes próprios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

USO AVANÇADO — Atendimento com mudança de solicitação
Cenário: Cliente altera o pedido enquanto duas consultas executam.
Estratégia: Incrementar revisão da intenção, preservar resultados auditáveis e impedir que ramos antigos atualizem a resposta atual.
Papel do modelo pequeno: Classificar a alteração e extrair campos; a decisão de validade pertence ao controlador.
Aceite proposto: Reproduzir chegada fora de ordem e confirmar ausência de resposta ou efeito da revisão cancelada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

USO AVANÇADO — Migração de workflow vivo
Cenário: Novo contrato de ferramenta precisa coexistir com sessões antigas.
Estratégia: Roteá-las pela versão persistida e migrar somente estados com transformação testada.
Papel do modelo pequeno: Produzir estado tipado sem escolher silenciosamente a versão de execução.
Aceite proposto: Retomar amostras históricas e conferir transições, efeitos e projeção final por versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: nós de extração ou classificação com estados pequenos e ramos explícitos.
8–14B: 8–14B: decisões locais com poucas ferramentas, limitadas por critérios externos.
15–30B: 15–30B: síntese de ramos quando a avaliação mostrar ganho sobre agregação determinística.
Requisitos de treino/runtime: Persistência, versões e redutores pertencem à aplicação; não exigem treino da LLM.
Não aplicar quando: Não adotar grafo complexo quando uma função determinística e uma chamada resolvem a tarefa.

## R008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Fonte nomeia LangGraph na arquitetura.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Klarna é relato de cliente pelo fornecedor e permanece produto/uso documentado com limites. A busca LinkedIn não confirmou LangGraph; sem atribuição por semelhança arquitetural.
Consultas registradas: V4C-Q021, V4C-Q026.

## R008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R008 → T060 [complements]
Como combinar: Vincular retomada à versão do grafo e à revisão da intenção.
Interface: Checkpoint, graph_version, intent_revision e próximo nó.
Condição: Sessões atravessam deploys ou falhas.
Aceite proposto: Um checkpoint incompatível é recusado ou migrado por regra registrada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006, V3D-S016, V4C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R008 → T148 [complements]
Como combinar: Resolver elegibilidade do ramo antes de publicar seu resultado.
Interface: Predicado tipado e revisão do estado de origem.
Condição: Existem ramos paralelos ou decisões atrasadas.
Aceite proposto: Resultado de ramo obsoleto não altera o estado vigente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006, V3D-S016, V4C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não inferir independência apenas porque nós executam em paralelo.
- Não usar memória entre threads sem namespace e política de visibilidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar o mesmo grafo e ferramentas com modelos diferentes; depois ablar a estrutura. Contabilizar ramos descartados e efeitos incorretos, não apenas respostas finais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T154, T159, T160

## Fontes primárias associadas

### C-S009 — LangGraph overview

[https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime de grafos com estado, controle de fluxo e integração de operações determinísticas e de LLM.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S019 — Persistence — LangGraph

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers mantêm estado de threads; stores preservam informação definida pela aplicação entre threads.

Limite: A URL durable-execution redirecionou para persistence na consulta; exemplos InMemory não demonstram durabilidade após queda de processo.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T148 — Conditional Branching

**Nome canônico:** Conditional Branching  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T148  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ramificação condicional

## T148:C01 — conceito

Controle de fluxo que escolhe próximos passos segundo condições do estado. A condição pode ser determinística ou uma classificação produzida por modelo, desde que validada. Ramificação cria caminhos distintos e exige que cada caminho tenha saída, dependências e término definidos.

Como funciona:
- Ler um estado consistente e os campos exigidos pela condição.
- Avaliar regra ou classificador e converter resultado em rota conhecida.
- Executar somente o ramo autorizado e registrar a transição.

## T148:C02 — aplicacao

Quando usar:
- Fluxos com tratamento distinto para sucesso, falha e falta de informação.
- Triagem entre capacidades ou tipos de documento.

Quando não usar:
- Condição crítica é texto livre não validado ou pode selecionar código arbitrário.

Implementação proposta:
- Usar enum de rotas permitidas e tratar estado desconhecido.
- Separar decisão de domínio de controles obrigatórios de autorização.
- Testar cada aresta, inclusive erro e caminho sem correspondência.

Aplicação LAI proposta:
Proposta: a Helena ter ramos claros para evidência suficiente, busca adicional, correção e impossibilidade, evitando loops implícitos.

## T148:C03 — riscos_validacao

Armadilhas:
- Ramo padrão pode transformar incerteza em uma decisão silenciosa.
- Mudança de schema pode invalidar condições sem erro evidente.

Métricas sugeridas:
- Cobertura das transições em testes.
- Frequência de rota desconhecida e retrabalho por classificação incorreta.

Testes propostos:
- Fornecer enum inesperado e exigir falha explícita ou recuperação definida.
- Alterar um campo de estado e verificar que somente a rota correspondente é executada.

## T148:C04 — perguntas_proveniencia

Pergunta: Uma LLM pode escolher o ramo?
Resposta: Sim, mas sua saída deve pertencer ao conjunto permitido e respeitar controles externos.

Pergunta: Branching exige DAG?
Resposta: Não. Pode existir em máquina de estados com ciclos limitados.

Pergunta: Desconhecido deve virar false automaticamente?
Resposta: Não. A política precisa decidir se busca dados, espera ou termina inconclusiva; ausência e negação têm significados distintos.

Pergunta: Como tornar uma decisão reproduzível?
Resposta: Persistir versão do estado, versão da regra e valor observado, em vez de recalcular a partir de um estado posterior.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T148:C05 — mecanismo_avancado

Condições de fluxo devem diferenciar falso, desconhecido e erro de avaliação. Tratar ausência de evidência como falso pode enviar o workflow para uma ação prematura. Quando a condição vem de uma LLM, o valor precisa ser validado contra um conjunto fechado de rotas, e o estado utilizado na decisão deve ser registrado. Atualizações concorrentes podem tornar a decisão obsoleta entre avaliação e execução.

Condição de contorno:
Uma guarda baseada em estado mutável precisa de revalidação ou vínculo de versão antes de efeitos dependentes daquela condição.

Contrato proposto:
- Entradas: Estado versionado, expressão da guarda ou classificação validada e mapa de destinos.
- Saídas: Destino permitido ou estado de decisão inconclusiva.
- Estado: Valor observado, regra aplicada e revisão do estado.
- Invariante: Toda saída da guarda pertence ao mapa de rotas e possui caminho de término.

Compromissos de projeto:
- Condições determinísticas são auditáveis, mas exigem dados formalizados.
- Classificação por modelo lida com linguagem ambígua e introduz variabilidade e custo de validação.

## T148:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover um campo necessário à guarda e alterar o estado após sua avaliação; exigir inconclusão no primeiro caso e rejeição ou reavaliação da decisão obsoleta no segundo.

Plano de avaliação proposto:
Comparar regras, classificador e combinação dos dois usando estados com rótulos conhecidos. Medir rotas indevidas, ambiguidades corretamente preservadas e ciclos introduzidos. Escolher por erro de encaminhamento e custo, não apenas por acerto médio.

Comparações:
- T134 (complements): Roteamento semântico pode produzir um sinal, mas o grafo deve validar a transição.
- T142 (complements): O framework fornece transições e estado; a guarda pertence ao contrato da tarefa.

Afirmação rastreável:
LangGraph permite transições condicionais e atualização de estado associada ao encaminhamento por Command.
Suporte: direct; fontes: V3C-S006
Limite: Um destino válido estruturalmente não demonstra que a condição semântica foi bem avaliada.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T148:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu falso, desconhecido e erro. A camada nova valida exaustividade de caminhos, precedência entre guardas e estabilidade das decisões diante de eventos fora de ordem.

Tabela de decisão verificável
Escreva combinações relevantes de condições e o destino correspondente antes de codificar o grafo. Guardas sobrepostas precisam de prioridade explícita; condições não cobertas precisam de uma saída definida. Isso evita que a ordem acidental de ifs determine decisões diferentes após uma refatoração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S032.

Versão da guarda e do estado
Uma decisão deve registrar qual estado observou e qual regra a produziu. Se houver evento concorrente relevante, reavalie antes do efeito ou use uma pré-condição atômica. O modelo pode sugerir uma categoria, mas a transição confirmada pertence ao controlador e ao contrato vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S002.

Estados terminais protegidos
Mensagens atrasadas não devem reabrir trabalho concluído por uma simples sobrescrita. Defina quais transições podem corrigir um estado terminal e exija um evento explícito para elas. Reabertura de tarefa é mudança de domínio distinta de retransmissão de uma atualização antiga.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004.

USO AVANÇADO — Promoção de uma alteração de código
Cenário: Um patch precisa passar build, testes e revisão antes de avançar.
Estratégia: Use guardas por evidência versionada, com estados aprovado, reprovado e ainda não avaliado. Quando o patch mudar, invalide os resultados dependentes. Uma mensagem tardia de sucesso da versão anterior não libera a nova alteração.
Papel do modelo pequeno: 3–30B pode explicar diagnóstico; regras de promoção continuam determinísticas.
Aceite proposto: Proposta: permutar ordem dos eventos de testes e exigir decisões idênticas para o mesmo conjunto de fatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S032.

USO AVANÇADO — Fluxo conversacional com informação incompleta
Cenário: O usuário alterna entre consultar dados e preparar uma ação.
Estratégia: Classifique intenção, resolva entidades e mantenha uma rota para informação insuficiente. Antes de escrever, confirme requisitos no estado atual. Se a consulta mudou, encerre ou substitua o plano antigo explicitamente, preservando o histórico.
Papel do modelo pequeno: 3–7B classifica; 8–14B extrai entidades; 15–30B propõe decomposição complexa.
Aceite proposto: Proposta: testar pedidos ambíguos, mudanças de objetivo e eventos duplicados, medindo ações incorretas e esclarecimentos úteis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: produzir enums de condição entre poucos caminhos com suporte explícito a desconhecido.
8–14B: Proposta: extrair fatos para guardas compostas, sem decidir o efeito sozinho.
15–30B: Proposta: propor novos caminhos para revisão, conservando a máquina de estados como autoridade operacional.
Requisitos de treino/runtime: Exige testes de tabela de decisão, versões de regras e pré-condições no backend que executa mutações.
Não aplicar quando: Não deixar transições críticas dependerem somente de texto livre ou de confiança não calibrada do modelo.

## T148:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: O DSL representa condicionais e outras transições.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Gates condicionam a transição entre estágios de deployment.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor e Up CD sustentam coordenação por condições. A tabela de decisão e seus testes são propostas para a integração local.
Consultas registradas: V4C-Q003, V4C-Q002, V4C-Q010.

## T148:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T148 → T141 [feeds]
Como combinar: Enums e evidências estruturadas tornam a classificação consumível pela guarda.
Interface: Condição, origem, versão e estado de validação.
Condição: O parser distingue desconhecido de falso.
Aceite proposto: Fornecer valores inválidos e exigir rota de erro explícita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T148 → T241 [complements]
Como combinar: Replay deve reproduzir a interpretação de decisões usando versões compatíveis.
Interface: Eventos ordenados e versão do avaliador de guardas.
Condição: Regras históricas continuam disponíveis ou têm migração definida.
Aceite proposto: Reprocessar eventos permutáveis e conferir invariantes de estado terminal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S004, V3C-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não liberar ação com base em evidência de artefato diferente.
- Detectar guardas contraditórias e caminhos sem término antes de publicar o workflow.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos na classificação de entradas que alimentam as guardas, mantendo controlador igual. Desempenho do workflow não pode ser atribuído inteiro à LLM.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T134, T143, T160

## Fontes primárias associadas

### C-S013 — Workflows and agents

[https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento e arestas condicionais selecionam fluxos conforme estado ou classificação da entrada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

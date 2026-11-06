# T147 — Parallel Fan-Out

**Nome canônico:** Parallel Fan-Out  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T147  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** distribuição paralela em ramos

## T147:C01 — conceito

Decomposição de uma etapa em vários ramos independentes executados concorrentemente, seguida de agregação. Pode envolver ferramentas, trabalhadores ou agentes. O coordenador precisa definir o que constitui conjunto completo, resultado parcial aceitável e falha impeditiva.

Como funciona:
- Criar unidades de trabalho com escopo e identificadores exclusivos.
- Distribuir unidades para executores com limite de concorrência.
- Agregar resultados verificando cobertura, duplicatas e inconsistências.

## T147:C02 — aplicacao

Quando usar:
- Busca em fontes independentes.
- Processamento de documentos que podem ser analisados separadamente.

Quando não usar:
- Cada ramo precisa conhecer continuamente todos os resultados dos demais.

Implementação proposta:
- Fixar contrato de entrada e saída para cada ramo.
- Declarar política de timeout, cancelamento e resultados parciais.
- Persistir manifest com unidades esperadas e concluídas antes da síntese.
- Reservar prazo para a agregação depois do encerramento dos ramos.

Aplicação LAI proposta:
Proposta: separar auditorias por módulos com especialistas consultivos e consolidar por um decisor, usando artefatos como interface.

## T147:C03 — riscos_validacao

Armadilhas:
- Agregador pode esconder ausência de um ramo importante.
- Aumentar fan-out sem capacidade disponível só aumenta filas.

Métricas sugeridas:
- Cobertura das unidades e tempo de cauda.
- Custo de coordenação e fração de resultados duplicados.

Testes propostos:
- Perder um ramo e exigir que o consolidado sinalize cobertura incompleta.
- Entregar respostas fora de ordem e confirmar reconstrução determinística do conjunto.

## T147:C04 — perguntas_proveniencia

Pergunta: Fan-out é sinônimo de multiagente?
Resposta: Não. Os ramos podem ser funções comuns sem LLM.

Pergunta: O consolidado pode assumir que todos responderam?
Resposta: Não. Deve comparar os resultados recebidos com o manifest esperado.

Pergunta: Quando todos os ramos existentes terminaram, o fan-out acabou?
Resposta: Somente se a fase que pode criar novos ramos também estiver encerrada.

Pergunta: Uma lista de resultados em ordem de chegada é reproduzível?
Resposta: Não necessariamente; preservar IDs e aplicar ordenação estável quando o consumidor depende da sequência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T147:C05 — mecanismo_avancado

A junção de um fan-out precisa saber quando o conjunto esperado está completo. Em expansão dinâmica, terminar a criação dos ramos é um evento diferente de terminar os ramos existentes. Uma política pode exigir todos, quorum ou melhor resultado até o deadline, mas cada escolha muda o significado da entrega. Agregações sensíveis à ordem devem usar uma chave lógica, pois ordem de término depende de latência e não de relevância.

Condição de contorno:
Ramos que editam o mesmo artefato ou dependem da saída uns dos outros não são independentes apenas porque foram delegados separadamente.

Contrato proposto:
- Entradas: Unidades de trabalho identificadas, cardinalidade ou condição de fechamento e regra de junção.
- Saídas: Agregado, cobertura dos ramos e ausências explicitadas.
- Estado: Ramos previstos, criados, concluídos, falhos e cancelados.
- Invariante: A junção não declara completude antes do fechamento da expansão.

Compromissos de projeto:
- Esperar todos preserva cobertura e fica sujeito ao ramo mais lento.
- Aceitar quorum reduz cauda de latência e exige provar que o requisito tolera resultados ausentes.

## T147:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar a descoberta do último ramo e concluir rapidamente os demais; impedir que o agregador feche a tarefa antes de conhecer a cardinalidade final.

Plano de avaliação proposto:
Comparar junção completa e parcial com distribuição de latências controlada. Medir cobertura, tempo do ramo crítico, consumo e qualidade do agregado. Adotar entrega parcial apenas quando o critério da tarefa a distinguir de conclusão integral.

Comparações:
- T139 (complements): Concorrência de chamadas é um mecanismo de execução dos ramos.
- T160 (complements): Um DAG representa dependências e a condição de prontidão da junção.

Afirmação rastreável:
LangGraph oferece Send para fan-out dinâmico e reducers para agregar atualizações de estado.
Suporte: direct; fontes: V3C-S006
Limite: A biblioteca não determina o quorum de negócio nem garante independência dos efeitos de cada ramo.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T147:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu completude de ramos e políticas de junção. O novo desenho acrescenta contratos de diversidade, tratamento de atrasos e limitação hierárquica para impedir explosão de subagentes.

Partição por pergunta diferente
Delegue ramos que respondam aspectos distintos ou usem evidências independentes. Dividir a mesma pergunta sem mudar fontes tende a gerar duplicação e erro correlacionado. O coordenador precisa registrar qual lacuna cada ramo cobre e reconhecer quando dois resultados são apenas paráfrases do mesmo documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Capacidade compartilhada na árvore
Cada subagente pode gerar novas chamadas, portanto limitar apenas o número de filhos diretos não limita a carga total. Passe orçamento residual e contador global pela árvore. Expansão exige reservar capacidade, evitando que um worker reinicie cotas ao criar outro worker.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S009.

Atraso com significado
Um ramo lento pode ser o único responsável por um requisito obrigatório. Encerrar por quorum sem olhar a cobertura pode entregar uma resposta incompleta com aparência de consenso. Diferencie requisito indispensável, redundância e exploração opcional; prazo expirado deve produzir uma lacuna identificada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S007.

USO AVANÇADO — Verificação de patch por propriedades
Cenário: O mesmo diff precisa preservar comportamento, escopo e ausência de resíduos.
Estratégia: Distribua propriedades independentes a revisores delimitados, incluindo ferramentas determinísticas. Agregue por critério, não por votação global. Se uma propriedade obrigatória falhar ou não for avaliada, mantenha o candidato sem aceite.
Papel do modelo pequeno: 3–14B revisa critérios estreitos; 15–30B integra conflitos com evidências.
Aceite proposto: Proposta: medir bugs detectados, falso bloqueio e custo de revisão em patches com defeitos introduzidos conhecidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

USO AVANÇADO — Inventário técnico de vários módulos
Cenário: Uma migração exige mapear dependências de dezenas de componentes.
Estratégia: Particione por módulo com entradas versionadas e formato comum. Reserve um ramo de integração para detectar dependências entre módulos; alterações compartilhadas voltam a uma fila serial, evitando duas correções concorrentes do mesmo arquivo.
Papel do modelo pequeno: 3–7B extrai símbolos e versões; 8–30B interpreta relações e exceções.
Aceite proposto: Proposta: conferir cobertura do inventário, conflitos e tempo de integração contra processamento sequencial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: workers com uma pergunta objetiva e saída curta, evitando autonomia recursiva.
8–14B: Proposta: revisores ou executores especializados em um módulo com contrato explícito.
15–30B: Proposta: coordenador de conjunto limitado, com integração obrigatória e memória de cobertura.
Requisitos de treino/runtime: Necessita orçamento compartilhado, identidade dos ramos e agregador que trate ausência, erro e duplicação.
Não aplicar quando: Não usar quando os ramos dependem fortemente do mesmo estado mutável ou quando integração domina todo o trabalho.

## T147:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O líder cria subagentes em paralelo e agrega suas saídas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Workflows incluem forks paralelos e junções.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: CodeCourt executa revisores por propriedade em paralelo e agrega todos os resultados antes de encaminhar o diff.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: O sistema limita paralelismo onde ele violaria estado; não é fan-out de ferramentas LLM.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e AutoClean documentam fan-out em funções diferentes. Cada deployment aparece uma vez, independentemente do número de ramos.
Consultas registradas: V4C-Q003, V4C-Q006, V4C-Q010.

## T147:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T147 → T237 [feeds]
Como combinar: A decomposição fornece tarefas delimitadas aos subagentes e recebe resultados por objetivo.
Interface: Objetivo, fontes, escopo, formato e estado de cada ramo.
Condição: A delegação possui lacunas identificáveis e resultados comparáveis.
Aceite proposto: Proposta: medir cobertura real sem contar respostas duplicadas como contribuição nova.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T147 → T200 [complements]
Como combinar: CodeCourt usa revisores paralelos por propriedade e agrega seus vereditos.
Interface: Diff e critérios separados para cada revisor.
Condição: Cada propriedade obrigatória precisa passar.
Aceite proposto: Proposta: semear violações distintas e conferir qual revisor as identifica.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Impedir fan-out recursivo sem consumo do orçamento comum.
- Conservar resultado tardio como evidência adicional, sem alterar silenciosamente uma entrega já publicada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare equipes pequenas com fronteira individual e com fronteira paralela, igualando custo e ferramentas. Mais agentes não garantem independência nem melhor resposta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T001, T139, T169

## Fontes primárias associadas

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

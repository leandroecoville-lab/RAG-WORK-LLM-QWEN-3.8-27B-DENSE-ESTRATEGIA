# T060 — Agent Checkpointing / Checkpoint & Resume — incluindo checkpoints transacionais

**Nome canônico:** Agent Checkpointing com retomada e checkpoint transacional  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T060  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Checkpointing; ponto de retomada; snapshot de execução; Agent Checkpointing; Checkpoint & Resume; checkpoint transacional

## T060:C01 — conceito

Agent Checkpointing salva estado suficiente para retomar uma execução após pausa ou falha. Um checkpoint transacional grava conjuntamente os elementos que precisam representar o mesmo avanço, como estado, cursor de eventos e intenções pendentes, dentro de uma transação. A garantia cobre esse limite de atomicidade; uma chamada externa não se torna atômica apenas por existir um snapshot local.

Como funciona:
- Escolher uma fronteira consistente: tarefas concluídas, tarefas pendentes, versões e resultados duráveis conhecidos.
- Persistir estado e cursor associados em uma única confirmação; falhas antes do commit não devem publicar um avanço parcial.
- Ao retomar, validar compatibilidade e reconciliar efeitos com resultado desconhecido antes de repetir operações.

## T060:C02 — aplicacao

Quando usar:
- Workflows longos, aprovações humanas e execuções sujeitas a reinício nas quais recomputar tudo é caro ou perigoso.

Quando não usar:
- Como substituto de idempotência, backup completo ou transação distribuída entre serviços independentes.

Implementação proposta:
- Proposta: definir mission_id, checkpoint_id, schema_version, state_version, event_cursor, artefatos referenciados e operações com chave de idempotência.
- Quando houver publicação de eventos, gravar a intenção em outbox na mesma transação do estado; um publicador posterior confirma o envio.
- Manter último checkpoint íntegro e testar migração de schema. Armazenamento apenas em RAM não permite retomada após perda do processo.
- Tratar resposta perdida depois de uma ação externa como resultado incerto: consultar recibo ou estado remoto antes de reexecutar.

Aplicação LAI proposta:
Proposta LAI: consolidar checkpoint, cursor e outbox no mesmo armazenamento transacional e deixar a reconciliação explícita no controlador de execução.

## T060:C03 — riscos_validacao

Armadilhas:
- Salvar o cursor antes dos resultados pode fazer a retomada pular trabalho que nunca foi concluído.
- Replay de código com efeitos não controlados pode duplicar alterações mesmo quando o checkpoint está íntegro.

Métricas sugeridas:
- Tempo de recuperação, trabalho repetido, checkpoints inválidos e efeitos duplicados nos cenários de falha.

Testes propostos:
- Teste proposto: interromper antes e depois do commit; estado e cursor devem reaparecer juntos ou nenhum deles.
- Interromper após efeito externo e antes do recibo local; a retomada deve reconciliar a mesma operação, sem criar outra intenção.

## T060:C04 — perguntas_proveniencia

Pergunta: Um arquivo JSON salvo é checkpoint transacional?
Resposta: Pode ser um snapshot, mas o nome transacional exige atomicidade definida para todos os elementos associados e uma estratégia verificável de recuperação.

Pergunta: Commit local garante exatamente uma chamada externa?
Resposta: Não. Outbox, idempotência e reconciliação tratam a fronteira externa; o commit protege somente os dados participantes da transação.

Pergunta: Salvar todas as variáveis garante retomada?
Resposta: Não. Também são necessários fluxo de controle, identidade de operações, compatibilidade do código e acesso aos artefatos referenciados.

Pergunta: Retornar a um checkpoint desfaz uma publicação externa?
Resposta: Não. Isso altera a execução local. É necessário observar o serviço externo e, se apropriado, executar uma compensação explicitamente autorizada.

Escopo das fontes:
LangGraph fundamenta checkpoints; PostgreSQL, atomicidade local; AWS, outbox e idempotência. O contrato de checkpoint LAI e seus testes são propostos.

## T060:C05 — mecanismo_avancado

É útil distinguir snapshot de dados, checkpoint de execução e gravações parciais de tarefas concluídas. Um snapshot mostra valores; a retomada também precisa saber o que executar depois. No LangGraph, checkpoints completos ficam em fronteiras de super-step, enquanto pending writes preservam resultados de nós concluídos quando outro nó falha. Essas gravações intermediárias não são, por si, checkpoints completos para qualquer ponto de retorno.

Condição de contorno:
Um ponto persistido não restaura arquivos temporários, credenciais expiradas ou serviços externos ao mesmo instante; a execução precisa verificar suas dependências ao retomar.

Contrato proposto:
- Entradas: Estado, agenda de execução, resultados duráveis de tarefas e referências a artefatos necessários.
- Saídas: Checkpoint validado com ponto de retomada e operações externas cujo resultado ainda é incerto.
- Estado: Identidade da thread, revisão de schema, tarefas pendentes e mecanismo de durabilidade.
- Invariante: Retomar trabalho computacional nunca implica que efeitos externos ocorridos depois do checkpoint foram desfeitos.

Compromissos de projeto:
- Salvar mais frequentemente reduz recomputação e aumenta escrita e sincronização.
- Persistir resultados por tarefa evita repetir trabalho concluído e exige distinguir recuperação parcial de retorno a um snapshot integral.

## T060:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar dois nós paralelos, concluir um e falhar no outro. A retomada deve reutilizar o resultado persistido do primeiro conforme o contrato; uma chamada externa sem recibo deve permanecer desconhecida.

Plano de avaliação proposto:
Avaliação proposta: comparar reinício integral e recuperação por checkpoint em falhas entre fronteiras. Medir trabalho repetido, perda de resultados, validade da agenda e efeitos duplicados; testar queda do processo, não apenas exceção capturada.

Comparações:
- T059 (distinct_from): Snapshot de projeção acelera reconstrução de domínio; checkpoint inclui informações para continuar a execução.
- T075 (complements): Reconciliação determina efeitos externos incertos que o checkpoint local não consegue comprovar.

Afirmação rastreável:
LangGraph distingue checkpoints por super-step e pending writes de tarefas concluídas para recuperação após falhas parciais.
Suporte: direct; fontes: V3A-S031
Limite: Durabilidade depende do saver e configuração; referências no estado não tornam seus recursos externos duráveis automaticamente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T060:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu snapshot, checkpoint e efeitos incertos. Aqui retomada inclui compatibilidade do executável e migração do contrato de estado.

Projeto e decomposição
Um checkpoint precisa identificar código, modelo, schema e referências necessárias à próxima etapa. Estado serializado válido pode ser incompatível com nova versão do executor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

Controle adaptativo
Restaure em modo de inspeção antes de liberar efeitos quando houve mudança de ambiente. Migração deve preservar operações pendentes e seus identificadores, sem convertê-las em novas tentativas automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

Validação contrafactual
Compare retomada na mesma versão e após atualização controlada. Meça etapas refeitas, operações duplicadas e estados bloqueados corretamente; snapshot isolado não prova capacidade de continuar o fluxo. Unidade de avaliação: ponto de retomada durável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

USO AVANÇADO — Atualização do agente
Cenário: Runtime muda enquanto tarefas estão pausadas.
Estratégia: Validar schema, migrar campos conhecidos e marcar operação externa incerta para reconciliação antes de continuar.
Papel do modelo pequeno: 3–7B explica incompatibilidade; código migra.
Aceite proposto: Nenhuma operação pendente pode ganhar novo identificador sem decisão explícita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

USO AVANÇADO — Falha durante coleta
Cenário: Alguns resultados já estão persistidos.
Estratégia: Restaurar fronteira confirmada e reexecutar somente trabalho sem confirmação, usando os mesmos contratos de deduplicação.
Papel do modelo pequeno: 8–14B retoma tarefa.
Aceite proposto: Artefatos confirmados devem ser reutilizados e resultados ausentes identificados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de etapa curta após checkpoint validado por código.
8–14B: Leitor de estado migrado com testes de pré-condição.
15–30B: Replanejador quando ambiente mudou e continuidade direta deixou de ser válida.
Requisitos de treino/runtime: Backend durável, manifestos de versão e protocolo de efeitos; checkpoint em memória não cobre reinício do processo.
Não aplicar quando: Referências essenciais expiraram ou não é possível determinar status das operações externas.

## T060:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O sistema utiliza checkpoints regulares e retomada após erros.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Estado e offsets/checkpoints sustentam retomada de tarefas.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Tolerância a falhas de fluxo é relacionada à retomada, mas não prova checkpoint LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008.

## T060:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T060 → T243 [requires]
Como combinar: Reconciliar efeitos sem confirmação antes de retomar.
Interface: operation_id, intenção, tentativa e recibo observado.
Condição: Serviço permitir consulta ou resolução explícita.
Aceite proposto: Simular sucesso externo com ACK perdido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V3A-S031, A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T060 → T064 [complements]
Como combinar: Serializar estado portátil e dependências.
Interface: Checkpoint, schema, código e referências duráveis.
Condição: Objetos não dependerem de handles efêmeros.
Aceite proposto: Restaurar em processo novo sem sessão original.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V3A-S031, A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir salvar um arquivo com checkpoint transacional completo.
- Não repetir efeitos para descobrir se a primeira tentativa funcionou.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade correta após falha; LLM maior não resolve ausência de protocolo de confirmação.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T162, T240, T242, P011, P015

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S001 — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gravação de estado e evento de outbox na mesma transação; publicação posterior; duplicatas exigem consumidores idempotentes.

Limite: Fundamenta princípios de consistência. Não prova implementação, exatamente-uma-vez ponta a ponta ou resultado de desempenho na LAI.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3A-S031 — LangGraph Checkpointers

[https://docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints por super-step, StateSnapshot e pending writes de tarefas concluídas; estado de execução e retomada.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4C-S024 — Open sourcing Brooklin: Near real-time data streaming at scale

[https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso operacional de Brooklin na LinkedIn para replicação e streaming, incluindo CDC; arquitetura técnica detalhada em fonte separada.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

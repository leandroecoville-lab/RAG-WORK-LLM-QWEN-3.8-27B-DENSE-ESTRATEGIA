# P008 — Event Store / Event Log

**Nome canônico:** Event Store / Event Log  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** armazenamento proposto de eventos; log proposto de eventos de estado

## P008:C01 — conceito

Event Store / Event Log é aqui o nome editorial de um componente arquitetural proposto. Armazenaria eventos duráveis usados para reconstruir estado e rastrear transições. Event sourcing é um padrão documentado, mas este componente LAI não foi verificado. Um log de diagnóstico só serve como origem de reconstrução se contiver todos os eventos e contratos necessários.

Como funciona:
- Representar cada mudança por evento com ID único, agregado, sequência, versão de schema e referências à causa e aos artefatos.
- Acrescentar eventos preservando o histórico lógico; correções de domínio entram como novos eventos que explicam a mudança.
- Reconstruir projeções por aplicação ordenada e usar snapshots vinculados a uma posição conhecida para acelerar a recuperação.

## P008:C02 — aplicacao

Quando usar:
- Fluxos que exigem retomada, explicação de decisões ou reconstrução do estado em pontos históricos.

Quando não usar:
- Quando apenas métricas agregadas são necessárias e o custo de evolução, retenção e replay não se justifica.

Implementação proposta:
- Proposta: estabelecer ordenação por agregado e controle de versão esperada; não assumir uma ordem global entre fontes independentes.
- Gravar estado local e evento de saída na mesma transação quando necessário, usando outbox para publicação posterior.
- Deduplicar consumidores por evento e testar migração de schemas; distinguir reprocessar projeções de reenviar efeitos externos.

Aplicação LAI proposta:
Proposta LAI: registrar transições do executor e versões de memória, oferecendo histórico e snapshots verificáveis aos componentes de continuidade.

## P008:C03 — riscos_validacao

Armadilhas:
- Entrega repetida pode duplicar projeções se o consumidor não for idempotente.
- Um snapshot sem sequência verificável pode pular eventos ou aplicá-los duas vezes.
- Append-only lógico não é, sozinho, garantia de proteção física contra alteração do armazenamento.

Métricas sugeridas:
- Atraso de consumo, eventos duplicados, lacunas de sequência e tempo de reconstrução por volume de histórico.

Testes propostos:
- Aceite proposto: reproduzir eventos até um cursor conhecido e comparar o estado com uma referência esperada.
- Entregar um evento duas vezes e interromper a publicação após o commit; a recuperação deve preservar uma única mudança lógica.

## P008:C04 — perguntas_proveniencia

Pergunta: Um arquivo de logs já é um event store suficiente?
Resposta: Somente se seus registros forem completos, duráveis, ordenáveis e interpretáveis para reconstruir o estado definido.

Pergunta: Replay deve executar novamente uma transferência externa?
Resposta: Não por padrão. Deve reconstruir o estado usando o resultado registrado; reexecutar efeitos requer protocolo próprio de reconciliação e idempotência.

Pergunta: Todo log permite replay?
Resposta: Não. Ele precisa conter os fatos necessários, sua ordem relevante e schemas interpretáveis.

Pergunta: O que torna a projeção recuperável?
Resposta: Eventos preservados, cursor consistente, projetor versionado e processamento repetível com deduplicação.

Escopo das fontes:
Fontes documentam eventos, replay e outbox; o componente e os requisitos LAI são propostos.

## P008:C05 — mecanismo_avancado

Event Store / Event Log é proposto como registro ordenado de fatos de execução, com ID do evento, entidade, sequência e versão de schema. Projeções devem guardar o último ponto aplicado e tolerar reentrega. Quando uma transação altera estado e precisa notificar outro sistema, uma outbox pode vincular a alteração ao evento pendente. A publicação posterior continua sujeita a duplicatas, portanto o consumidor precisa reconhecer eventos já processados.

Condição de contorno:
Um log de observabilidade não é automaticamente um histórico suficiente para reconstruir estado. Campos omitidos, eventos perdidos e mudanças de schema podem inviabilizar replay.

Contrato proposto:
- Entradas: Evento identificado, versão de schema, sequência por entidade, payload autorizado e revisão esperada.
- Saídas: Confirmação de gravação, posição no log e notificações ou projeções derivadas com seu próprio status.
- Estado: Eventos, offsets por consumidor, versões de projetores e chaves de deduplicação.
- Invariante: Uma projeção só avança o cursor quando aplica o evento de forma consistente; repetir o mesmo evento não deve duplicar seu efeito lógico.

Compromissos de projeto:
- Histórico completo facilita reconstrução e auditoria, mas aumenta custo e exige política de retenção compatível.
- Projeções assíncronas desacoplam consumidores e introduzem atraso que precisa ser exposto ao leitor.

## P008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: publicar o mesmo evento duas vezes, interromper consumidor após aplicar e antes de confirmar, e reaplicar desde snapshot; verificar estado final e cursor sem efeito duplicado.

Plano de avaliação proposto:
Comparar reconstrução integral e snapshot mais replay em sequência conhecida. Medir tempo de recuperação, atraso de projeções, divergências e compatibilidade após evolução de schema. Não afirmar exatamente uma vez para efeitos externos sem contrato adicional.

Comparações:
- T059 (complements): Event Sourcing utiliza eventos como fonte de reconstrução.
- T241 (complements): Replay consome o histórico com regras determinísticas e versionadas.

Afirmação rastreável:
A outbox grava alteração local e evento na mesma transação; consumidores ainda precisam tratar duplicatas.
Suporte: related; fontes: V3D-S018
Limite: O registro proposto exige decisões próprias de ordenação, retenção e evolução de schema.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P008:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a proposta Event Store com fronteira entre intenção e fato, causalidade parcial e replay sem repetir efeitos de negócio.

Envelope causal mínimo
Proposta: além da sequência por entidade, registrar causation_id, correlation_id e revisão observada. Esses campos permitem reconstruir dependências sem fingir uma ordem global de eventos simultâneos. Uma resposta de ferramenta pertence à intenção original mesmo se chegar em outra sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

Fato versus intenção
Usar tipos distintos para ação solicitada, envio iniciado, confirmação recebida e resultado reconciliado. A ausência de confirmação não é fato de falha. Esse desenho impede que um replay transforme um comando antigo em nova autorização para produzir efeito externo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

Projeções reexecutáveis
Versionar transformação e manter posição aplicada. Ensaiar reconstrução numa projeção separada antes de trocar consumidores. Eventos com dados sensíveis podem carregar referência e hash, preservando uma política explícita de retenção sem prometer apagar cópias fora do domínio controlado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

USO AVANÇADO — Memória de decisões do agente
Cenário: O sistema precisa explicar por que executou uma ação.
Estratégia: Persistir evidência e versão da política junto da transição; gerar resumo como projeção derivada.
Papel do modelo pequeno: 3–7B pode resumir a cadeia causal sem substituir o registro original.
Aceite proposto: Toda afirmação de ação concluída aponta para confirmação ou reconciliação registrada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

USO AVANÇADO — Reconstrução após bug de projeção
Cenário: Um extrator produziu estado derivado incorreto.
Estratégia: Corrigir a projeção, reproduzir eventos numa cópia e comparar diferenças antes de promover.
Papel do modelo pequeno: LLM revisa divergências sem criar novos fatos no histórico.
Aceite proposto: Replay não chama APIs mutantes e reconstrói estado segundo versão declarada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: produzir eventos candidatos tipados; validação confirma o que pode ser persistido.
8–14B: 8–14B: interpretar cadeias curtas para diagnóstico e resumo com referências.
15–30B: 15–30B: análise de incidentes complexos, sem poder de reescrever o histórico factual.
Requisitos de treino/runtime: Persistência, schema e idempotência pertencem ao serviço; não dependem de parâmetros do modelo.
Não aplicar quando: Não usar texto de log livre como único contrato para reconstrução e auditoria.

## P008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Histórico e posições ilustram requisitos do event store editorial.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P008 é componente editorial. Brooklin e padrões de outbox sustentam analogias e partes do desenho, sem adoção de um produto LAI com esse nome.
Consultas registradas: V4C-Q002, V4C-Q020, V4C-Q019.

## P008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P008 → T059 [complements]
Como combinar: Definir quais eventos são fonte de verdade e quais são projeções.
Interface: Envelope versionado, sequência e identidade causal.
Condição: Estado precisa ser reconstruído.
Aceite proposto: Uma reconstrução completa tem critérios explícitos de equivalência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S018, V4C-S024, V4C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P008 → T241 [feeds]
Como combinar: Entregar eventos para reprodução em modo sem efeitos externos.
Interface: Histórico, cursor e versão da projeção.
Condição: Há recuperação ou correção de projeção.
Aceite proposto: Reexecução preserva fatos sem duplicar operações.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S018, V4C-S024, V4C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir offset de transporte com confirmação de negócio.
- Não afirmar ordem causal total a partir apenas de timestamps.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas pela reconstrução correta e completude da evidência sob falhas. Mais memória textual não substitui eventos identificáveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T162, T240, T241, T242, P011

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

### V3D-S018 — AWS — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alteração local e evento pendente na mesma transação; publicação posterior pode duplicar mensagens.

Limite: Outbox não torna toda chamada externa exatamente uma vez; consumidores precisam de idempotência.

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

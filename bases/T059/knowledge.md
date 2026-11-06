# T059 — Event Sourcing

**Nome canônico:** Event Sourcing  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T059  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** estado derivado de eventos

## T059:C01 — conceito

Mantém a sequência de eventos de domínio como registro de referência e deriva o estado atual por projeções. Permite reconstrução e auditoria, ao custo de lidar com ordem, versões e reprocessamento. Um arquivo de logs arbitrários não constitui automaticamente event sourcing.

Como funciona:
- Registrar eventos com identidade e semântica de domínio.
- Aplicar eventos a projeções de estado.
- Reconstruir projeções a partir do histórico autorizado.

## T059:C02 — aplicacao

Quando usar:
- Fluxos em que reconstruir decisões e estado é requisito central.
- Sistemas com múltiplas projeções do mesmo histórico.

Quando não usar:
- Evitar complexidade desnecessária quando CRUD com trilha de auditoria já satisfaz o problema.

Implementação proposta:
- Proposta: definir aggregate_id, sequência, event_id e schema_version.
- Tornar projeções idempotentes e separar replay de efeitos externos.
- Evoluir schemas com migrações explícitas, preservando interpretação de eventos antigos.

Aplicação LAI proposta:
Proposta LAI: usar eventos para ações relevantes e evidências da Helena; geração de mensagem ou chamada externa precisa de controle próprio de idempotência.

## T059:C03 — riscos_validacao

Armadilhas:
- Reexecutar um evento pode disparar novamente um efeito externo.
- Mudanças de significado em schemas tornam replays inconsistentes.

Métricas sugeridas:
- Tempo de reconstrução e atraso das projeções.
- Divergência entre estado materializado e replay.

Testes propostos:
- Reaplicar o mesmo evento e exigir estado final igual.
- Reconstruir uma missão do zero e comparar com o snapshot persistido.

## T059:C04 — perguntas_proveniencia

Pergunta: Event sourcing garante exatamente uma execução?
Resposta: Não. Entrega, processamento e efeitos externos precisam de estratégias explícitas de idempotência e reconciliação.

Pergunta: Todo log é evento de domínio?
Resposta: Não. Um evento precisa ter significado, identidade e contrato suficientes para reconstruir estado.

Pergunta: Replay deve usar o relógio atual?
Resposta: Somente se a projeção foi definida assim. Reconstrução determinística costuma precisar do tempo do evento ou de valores persistidos, evitando depender de agora.

Pergunta: Como corrigir um evento já registrado?
Resposta: Use eventos corretivos ou interpretação versionada conforme o domínio. Sobrescrever o passado silenciosamente destrói a explicação do estado anteriormente conhecido.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T059:C05 — mecanismo_avancado

Reconstrução por eventos depende tanto da sequência persistida quanto da versão do projetor que interpreta essa sequência. Uma mudança de regra pode produzir outro estado a partir dos mesmos eventos, mesmo sem corrupção. Snapshots aceleram reidratação e precisam declarar posição do stream e compatibilidade do projetor. Eles são derivados substituíveis; o histórico continua necessário para reconstruir e diagnosticar diferenças entre projeções.

Condição de contorno:
Um broker com retenção limitada e ordenação parcial não oferece automaticamente todas as garantias de um event store por entidade.

Contrato proposto:
- Entradas: Eventos identificados, ordem por agregado, versões de schema e regra de projeção.
- Saídas: Estado materializado com posição consumida, revisão do projetor e erros de interpretação explícitos.
- Estado: Stream autoritativo, checkpoints de projeção, snapshots e registros de deduplicação.
- Invariante: Reproduzir eventos para reconstruir estado não reenvia mensagens nem repete efeitos de negócio por padrão.

Compromissos de projeto:
- Eventos permitem novas projeções e tornam evolução semântica mais trabalhosa.
- Snapshots reduzem tempo de reconstrução e exigem política de compatibilidade para não ocultar erros do projetor atual.

## T059:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar a interpretação de um evento antigo e tentar usar snapshot produzido pelo projetor anterior. A reconstrução deve detectar incompatibilidade ou aplicar migração conhecida, sem combinar silenciosamente duas semânticas.

Plano de avaliação proposto:
Avaliação proposta: comparar projeção incremental, replay integral e replay após snapshot no mesmo stream. Medir equivalência de estado, tempo, eventos duplicados ignorados e tratamento de versões antigas; executar a avaliação com efeitos externos desabilitados.

Comparações:
- T060 (complements): Um checkpoint pode registrar posição e estado do consumidor; event sourcing define o histórico autoritativo do domínio.
- T072 (complements): Versionar projetores e schemas permite explicar por que a mesma sequência produz representações diferentes.

Afirmação rastreável:
A documentação Microsoft descreve snapshots como otimização de reconstrução, mantendo o eventstream como fonte de referência.
Suporte: direct; fontes: A-S027
Limite: Adotar esse padrão exige contratos de ordenação, concorrência e evolução; um log genérico não os fornece automaticamente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T059:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou replay e efeitos. Aqui Event Sourcing sustenta evolução de esquema e reconstrução de memórias com projetores alternativos.

Projeto e decomposição
Eventos devem representar fatos de domínio, não frases livres do agente. Campos de intenção, tentativa e confirmação precisam ser distintos para reconstruir estado sem inventar sucesso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

Controle adaptativo
Versione schema e projetor. Upcasting pode adaptar formato antigo, mas não deve criar informação que nunca existiu; marcar ausência preserva honestidade da reconstrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

Validação contrafactual
Compare projeção atual e nova sobre o mesmo log, sem emitir efeitos externos. Meça divergências por tipo de evento e decisões afetadas; verificar eventos desconhecidos e fora de ordem. Unidade de avaliação: stream de eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

USO AVANÇADO — Migração de memória
Cenário: Novo schema separa hipóteses de decisões.
Estratégia: Reprocessar eventos em projeção paralela, comparar consultas e publicar somente após explicar diferenças materiais.
Papel do modelo pequeno: 3–7B classifica candidatos; código projeta.
Aceite proposto: Nenhum evento ambíguo pode ser reinterpretado silenciosamente como confirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

USO AVANÇADO — Auditoria de tarefa
Cenário: É necessário explicar sequência de ações.
Estratégia: Reconstruir estado com versão histórica do projetor e separar reavaliação atual em outro artefato.
Papel do modelo pequeno: 8–14B explica sequência.
Aceite proposto: Explicação deve apontar eventos que realmente ocorreram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de campos para propostas de evento, com validação externa.
8–14B: Leitor e explicador de projeção determinística.
15–30B: Analista de divergências entre projetores, sem controlar aplicação irrestrita de eventos.
Requisitos de treino/runtime: Log append-only, esquema versionado, ordenação definida e projetores determinísticos quando possível.
Não aplicar quando: Operações externas são repetidas no replay ou o histórico mistura intenção e confirmação.

## T059:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008.

## T059:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T059 → T072 [complements]
Como combinar: Versionar projetor e schema como parte da memória.
Interface: Stream, projector_version e migration_id.
Condição: Reconstrução declarar interpretação usada.
Aceite proposto: Reprocessar evento antigo com campo ausente e preservar desconhecido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S027, V4A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T059 → T075 [feeds]
Como combinar: Enviar divergências de projeção para reconciliação.
Interface: Estado anterior, novo estado e eventos causadores.
Condição: Reconciliação não apagar log de origem.
Aceite proposto: Detectar diferença material antes de trocar projeção ativa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S027, V4A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não executar novamente pagamentos, mensagens ou gravações externas no replay.
- Não usar timestamp de chegada como ordem causal universal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar explicações sobre log idêntico; reconstrução determinística deve ficar em código, não depender do porte do LLM.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T064, T162

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

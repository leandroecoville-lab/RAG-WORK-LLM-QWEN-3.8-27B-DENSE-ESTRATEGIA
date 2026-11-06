# T241 — Event Replay

**Nome canônico:** Event Replay  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T241  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** event replay; reprodução de eventos

## T241:C01 — conceito

Reconstrução de estado pela aplicação ordenada de eventos previamente registrados. Em Event Sourcing, replay permite refazer uma projeção ou investigar uma versão histórica. Reaplicar fatos a uma função de estado não significa reenviar mensagens, pagamentos, deploys ou outras ações que os eventos descrevem.

Como funciona:
- O log fornece identidade, ordem e versão dos eventos.
- Um processador aplica cada fato à projeção segundo regras conhecidas.
- A recuperação registra a fronteira processada e evita contar duplicatas como novos acontecimentos.

## T241:C02 — aplicacao

Quando usar:
- Reconstrução de índices e projeções, diagnóstico histórico e comparação entre versões de lógica de domínio.

Quando não usar:
- Usar o mesmo caminho de execução para replay e efeitos externos sem uma separação explícita e verificável.

Implementação proposta:
- Proposta: separar decisões e efeitos de funções que apenas aplicam fatos ao estado.
- Preservar eventos originais e definir migração ou interpretação compatível para versões antigas.
- Ordenar pela sequência apropriada ao agregado ou partição, sem presumir que timestamp global fornece ordem causal.
- Reproduzir em ambiente de projeção com efeitos externos desabilitados por construção.
- Comparar resultados e registrar a última sequência aplicada; deduplicar pela identidade do evento quando necessário.

Aplicação LAI proposta:
Proposta LAI: reconstruir estado de missões a partir de eventos confirmados, preservando efeitos externos em registros próprios e mantendo a reconstrução livre de novas mutações.

## T241:C03 — riscos_validacao

Armadilhas:
- Código não determinístico produz projeções diferentes.
- Um evento antigo pode não conter dados exigidos pela lógica nova.
- Reexecutar efeitos transforma uma recuperação de estado em uma segunda operação de negócio.

Métricas sugeridas:
- Eventos processados por segundo; divergência de projeção; duplicatas; falhas por esquema; tempo para reconstruir uma fronteira.

Testes propostos:
- Reprocessar o mesmo histórico e comparar o estado final.
- Incluir eventos duplicados e fora de ordem e verificar a política declarada.
- Substituir clientes externos por observadores que falham em qualquer chamada e demonstrar que replay não os aciona.

## T241:C04 — perguntas_proveniencia

Pergunta: Replay pode reproduzir uma resposta antiga de ferramenta?
Resposta: Pode usar o resultado registrado como evidência histórica, desde que a identidade e o conteúdo estejam preservados. Isso não exige chamar novamente a ferramenta.

Pergunta: Reexecutar uma ação externa durante recuperação é sempre proibido?
Resposta: Não, mas é uma decisão separada, dependente de autorização, idempotência e reconciliação. Não deve ocorrer implicitamente por leitura do histórico.

Pergunta: Mesmo log sempre produz o mesmo estado?
Resposta: Somente sob regras, ordem e entradas auxiliares compatíveis; trocar o processador pode mudar a projeção.

Pergunta: Posso usar a data atual para completar um evento antigo?
Resposta: Não como se fosse um fato original. Isso introduz dependência externa e altera o significado histórico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T241:C05 — mecanismo_avancado

Replay de eventos históricos exige compatibilidade de representação e significado. Um upcaster pode converter o schema antigo para o atual durante a leitura, mas não deve inventar informação que nunca foi registrada. Mudança de regra de projeção também pode produzir estado diferente a partir dos mesmos fatos; nesse caso, reconstrução atual e reprodução histórica são objetivos distintos. O contrato precisa declarar qual versão do processador será utilizada.

Condição de contorno:
Eventos incompletos, ordem incorreta ou transformações dependentes do relógio atual impedem reconstrução reproduzível.

Contrato proposto:
- Entradas: Eventos ordenados, cursor inicial, versão do reducer e conversões de schema.
- Saídas: Projeção reconstruída, cursor final e eventos não interpretáveis.
- Estado: Versões de processamento, IDs já aplicados e falhas de conversão.
- Invariante: Reconstrução da projeção não reenvia efeitos externos apenas porque encontra eventos antigos.

Compromissos de projeto:
- Upcasting evita regravar o histórico e aumenta trabalho de leitura e manutenção.
- Preservar processadores antigos permite reprodução histórica e amplia carga de compatibilidade.

## T241:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir evento antigo sem campo recém-exigido e converter usando um default que altera significado; exigir tratamento explícito da ausência, sem simular fato histórico inexistente.

Plano de avaliação proposto:
Comparar projeção antiga reproduzida e projeção nova reconstruída sobre o mesmo log. Medir divergências explicáveis, eventos rejeitados, tempo e efeitos externos indevidos. Separar regressão de mudança intencional de regra.

Comparações:
- T170 (complements): Evolução de schema também precisa de compatibilidade entre versões de eventos.
- T242 (complements): Replay a partir de snapshot aplica somente o sufixo ainda não incorporado.

Afirmação rastreável:
Marten descreve upcasting como transformação do schema antigo durante a leitura do evento.
Suporte: direct; fontes: V3C-S041
Limite: Conversão estrutural não prova preservação semântica; fatos ausentes continuam ausentes.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T241:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava reprodução histórica e projeção atual. A expansão define fronteiras de replay para agentes, bloqueia efeitos durante reconstrução e valida migrações com históricos representativos de falhas.

Decisões observadas versus geração nova
Uma chamada LLM gravada como decisão deve ser reproduzida pelo resultado registrado quando o objetivo é reconstruir a execução. Consultar novamente o modelo cria uma nova decisão, mesmo com temperatura baixa. Se a intenção é reavaliar com modelo novo, trate como experimento ou nova projeção, preservando o histórico original para comparação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

Reconstrução sem efeitos
Aplicadores de eventos devem atualizar projeções ou emitir comandos controlados, sem reenviar automaticamente efeitos já ocorridos. Separe modo de reconstrução e modo ativo, e teste fronteiras onde uma atividade foi enviada mas a confirmação local não chegou. Reconstruir intenção desconhecida não autoriza concluir que o efeito está ausente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S018.

Compatibilidade exercitada
Use históricos com timeout, cancelamento, concorrência e versão antiga, não apenas sucessos curtos. Upcasters preservam significado do que foi registrado; campos novos obrigatórios sem origem exigem migração explícita ou representação de ausência. A ordem causal e a identidade dos eventos precisam ser preservadas mesmo quando índices são reconstruídos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S001.

USO AVANÇADO — Atualização de runtime
Cenário: Uma nova versão deve retomar missões antigas.
Estratégia: Reproduza históricos selecionados em ambiente sem efeitos e compare comandos ou estados esperados conforme o contrato do runtime. Divergências legítimas precisam de plano de migração; divergências acidentais bloqueiam a publicação. Manter worker antigo pode ser necessário enquanto execuções anteriores terminam.
Papel do modelo pequeno: 3–30B continua em atividades externas ao replay determinístico; código controla reprodução.
Aceite proposto: Proposta: históricos compatíveis retomam e os incompatíveis falham de forma explícita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

USO AVANÇADO — Auditoria de decisão
Cenário: É necessário explicar como um agente chegou a um resultado.
Estratégia: Reconstrua observações, versões de ferramenta e decisões confirmadas, distinguindo dados disponíveis naquele momento dos atuais. Não preencher lacunas com uma narrativa nova da LLM. Quando o log não contém uma informação, a conclusão correta é limite de reconstrução.
Papel do modelo pequeno: 8–14B organiza evidência; 15–30B explica causalidade com referências ao log.
Aceite proposto: Proposta: cada explicação operacional aponta a evento ou artefato existente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atividades pequenas registradas facilitam replay porque a decisão fica delimitada.
8–14B: Interpretar logs reconstruídos e classificar falhas sem executar efeitos.
15–30B: Comparar versões e sugerir migração, preservando prova histórica independente.
Requisitos de treino/runtime: Log ordenado, schemas e processadores versionados, bloqueio de efeitos e artefatos externos disponíveis.
Não aplicar quando: Não chamar nova execução probabilística de replay fiel nem inventar fatos ausentes em upcast.

## T241:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: A fonte descreve replay/shadowing de históricos para detectar incompatibilidades.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Releitura de streams a partir de posições é relacionada a replay, sem provar reconstrução integral de estado de agente.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cadence oferece caso operacional de replay. Transporte de eventos Brooklin não foi considerado equivalente à reprodução determinística de decisões do agente.
Consultas registradas: V4C-Q002, V4C-Q020.

## T241:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T241 → T159 [complements]
Como combinar: Cadence utiliza histórico e replay para execução durável e validação de evolução.
Interface: Histórico, comandos e versão compatível.
Condição: Operações externas seguem a fronteira adequada do runtime.
Aceite proposto: Reconstrução não gera nova observação para explicar o passado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S001. Casos: V4C-C003.

2. T241 → T242 [complements]
Como combinar: Aplicar apenas eventos posteriores ao snapshot compatível, preservando a mesma semântica de redução.
Interface: Cursor, versão e sufixo do log.
Condição: Todos os eventos necessários continuam disponíveis.
Aceite proposto: Estado recuperado coincide com replay de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S041. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Replay que acessa relógio atual ou fonte mutável pode divergir sem erro de parsing.
- Deduplicar eventos requer identidade; textos parecidos podem representar intenções distintas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fidelidade e tempo de reconstrução entre arquiteturas, não entre capacidades linguísticas. O modelo pode explicar o replay, mas a correção depende do registro e do processador.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T240, T242, T243

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S041 — Marten — Events Versioning

[https://martendb.io/events/versioning.html](https://martendb.io/events/versioning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evolução de schemas e upcasting permitem interpretar eventos históricos sem tratar mudança de representação como novo fato.

Limite: Mecanismos específicos do framework; conversão deve preservar semântica e não inventar informação histórica ausente.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

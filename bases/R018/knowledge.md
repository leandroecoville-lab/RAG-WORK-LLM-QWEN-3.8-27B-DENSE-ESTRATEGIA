# R018 — Temporal

**Nome canônico:** Temporal  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Temporal durable execution; Temporal Workflows

## R018:C01 — conceito

Temporal é uma plataforma de execução durável de workflows. Ela registra histórico de eventos e reconstrói o estado por replay do código de orquestração. Operações externas ficam em Activities executadas por workers. O mecanismo ajuda a retomar processos após falhas; não conserva automaticamente a memória arbitrária de um processo nem garante efeitos externos exatamente uma vez.

Como funciona:
- O workflow deve tomar decisões compatíveis com o histórico registrado; valores não determinísticos exigem tratamento apropriado.
- Chamadas de LLM, rede e banco ficam em Activities, cujos resultados confirmados são reutilizados durante o replay.
- Uma Activity pode executar mais de uma vez por retries, inclusive depois de realizar parcialmente seu efeito.

Nota de nomenclatura: A garantia sobre o histórico não deve ser apresentada como exactly-once de qualquer serviço externo.

## R018:C02 — aplicacao

Quando usar:
- Missões longas com espera, múltiplas dependências e necessidade de recuperação operacional.

Quando não usar:
- Como substituto de memória semântica, cache KV ou validador da resposta produzida pela LLM.

Implementação proposta:
- Proposta: modelar etapas e condições de término; separar decisões determinísticas de integrações com efeitos externos.
- Definir timeouts, política de retry e chave de idempotência estável para cada operação de negócio.
- Guardar referências de artefatos grandes, registrar resultados de Activities e testar compatibilidade do replay ao evoluir o código.

Aplicação LAI proposta:
Proposta LAI: avaliar Temporal para coordenar tarefas extensas de programação e integrações da Helena, mantendo verificadores de conteúdo e evidências em etapas explícitas.

## R018:C03 — riscos_validacao

Armadilhas:
- Reexecutar uma escrita sem chave idempotente pode duplicar o efeito quando a confirmação anterior se perde.
- Persistência do workflow não confirma que uma ferramenta cumpriu o objetivo; sucesso operacional e qualidade são verificações distintas.

Métricas sugeridas:
- Workflows concluídos, tempo de retomada, retries por Activity, backlog de trabalho e efeitos duplicados.

Testes propostos:
- Proposta: interromper um worker depois do efeito externo e antes da confirmação; exigir reconciliação sem duplicação.
- Reproduzir históricos guardados com a nova definição do workflow e detectar incompatibilidades antes de substituir workers.

## R018:C04 — perguntas_proveniencia

Pergunta: Replay chama novamente toda LLM anterior?
Resposta: Resultados de Activities já confirmadas são reutilizados pelo histórico; atividades sem conclusão confirmada podem precisar de nova execução.

Pergunta: Temporal elimina a necessidade de idempotência?
Resposta: Não. Activities podem executar mais de uma vez, portanto os efeitos externos precisam tolerar repetição ou ser reconciliados.

Pergunta: Schedule-to-Start resolve uma fila sem workers com retry?
Resposta: Esse timeout é não repetível por desenho; reenfileirar na mesma fila não resolveria a ausência de capacidade.

Pergunta: Heartbeat local garante progresso recuperável?
Resposta: Não necessariamente. É preciso considerar throttling e o último detalhe efetivamente recebido pelo serviço.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R018:C05 — mecanismo_avancado

Os timeouts do Temporal delimitam fases diferentes. Schedule-to-Start mede espera de uma tarefa na fila; Start-to-Close limita uma tentativa; Schedule-to-Close delimita a execução lógica inteira, incluindo tentativas e esperas. Heartbeat informa atividade e progresso, mas o SDK pode agrupar transmissões: progresso registrado localmente antes da queda pode não ter chegado ao serviço. O workflow precisa reproduzir comandos compatíveis com o histórico; chamadas de modelo e integrações ficam em Activities, cujos efeitos precisam suportar repetição. Essa separação permite diagnosticar fila saturada sem confundi-la com worker travado.

Condição de contorno:
Timeout não confirma que um serviço externo parou de trabalhar. Uma tentativa anterior pode continuar e produzir efeito após o início de outra.

Contrato proposto:
- Entradas: Workflow ID, Activity ID, limites por fase, política de retry e chave da operação externa.
- Saídas: Resultado confirmado ou falha classificada por fase, com referência ao efeito observado.
- Estado: Histórico de comandos, tentativas, último heartbeat transmitido e versão do código.
- Invariante: Repetições conservam identidade lógica; resultado tardio é reconciliado antes de criar outro efeito.

Compromissos de projeto:
- Timeout curto acelera detecção, mas aumenta tentativas concorrentes quando o serviço apenas está lento.
- Heartbeat frequente melhora observabilidade, porém transmissão e persistência têm custo e atraso.

## R018:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover workers da fila e, separadamente, travar um worker após começar. Exigir diagnósticos distintos; interromper após efeito externo e confirmar reconciliação pela mesma chave.

Plano de avaliação proposto:
Comparar políticas com cargas e falhas idênticas. Medir espera de fila, tempo por tentativa, duração total, efeitos duplicados e atraso de recuperação; escolher limites a partir da distribuição operacional.

Comparações:
- T159 (specializes): Temporal oferece implementação concreta de execução durável, com regras próprias de histórico e workers.
- T162 (complements): Idempotência protege efeitos de Activities que podem repetir, fora da reconstrução determinística do workflow.

Afirmação rastreável:
Start-to-Close limita uma tentativa, enquanto Schedule-to-Close limita a execução da Activity ao longo das tentativas.
Suporte: direct; fontes: V2A-S010
Limite: Esses limites não equivalem a interromper atomicamente uma transação em serviço externo.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R018:C07 — estrategia_3_30b

NOVA CAMADA v4 — Avança dos timeouts para controle do crescimento do histórico, continuidade de identidade entre unidades de execução e tratamento de respostas externas tardias.

Histórico com orçamento
Proposta: medir crescimento do histórico por etapa, especialmente em polling e loops de agente. Guardar grandes documentos em armazenamento versionado e conservar referências verificáveis no estado. Planejar fronteiras de renovação ou subdivisão sem apagar a identidade lógica da tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

Resultado tardio
Tratar deadline local e estado remoto separadamente. Uma Activity interrompida pode deixar trabalho externo ativo. O resultado posterior deve ser associado à operação original e conciliado com a decisão vigente, sem iniciar outra operação por interpretar silêncio como falha definitiva.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

Upgrade com replay controlado
Usar históricos representativos para verificar compatibilidade antes de trocar workers. Chamadas a modelos permanecem fora da lógica determinística de workflow. A migração precisa preservar decisões já tomadas; reexecutar a LLM para preencher um resultado antigo muda o processo histórico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

USO AVANÇADO — Pesquisa longa em documentos versionados
Cenário: A tarefa atravessa falhas de worker e várias consultas.
Estratégia: Persistir decisões pequenas e referências imutáveis; dividir etapas por resultado verificável.
Papel do modelo pequeno: Extrair evidências e redigir sínteses dentro de Activities com prazo e resultado registrado.
Aceite proposto: Retomar após falha entre etapas sem consultar novamente fontes já congeladas por necessidade de replay.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

USO AVANÇADO — Operação externa com resposta ambígua
Cenário: Fornecedor responde depois do timeout da Activity.
Estratégia: Conservar operation_id e consultar status antes de repetir; registrar compensação somente quando definida pelo domínio.
Papel do modelo pequeno: Classificar evidência textual, sem decidir sozinho se um efeito remoto ocorreu.
Aceite proposto: Injetar resposta tardia e comprovar ausência de duplicação ou reconciliação explicitamente pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: ações semânticas pequenas; o workflow assume duração e persistência.
8–14B: 8–14B: microplanos com saídas tipadas e limites por Activity.
15–30B: 15–30B: reservar a interpretação mais difícil; tamanho não muda a semântica durável.
Requisitos de treino/runtime: Runtime, backend e políticas duráveis precisam de implantação própria; persistência não é aprendida pelo modelo.
Não aplicar quando: Não usar workflow determinístico como lugar para chamadas de rede ou amostragem de LLM.

## R018:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Foram pesquisados casos Temporal em Stripe/Coinbase e Cadence em Uber. Relato Cadence não foi convertido em adoção Temporal; resultados não confirmados não entram como produção exata.
Consultas registradas: V4C-Q002, V4C-Q022, V4C-Q025, V4C-Q029.

## R018:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R018 → T241 [complements]
Como combinar: Reproduzir transições registradas sem recriar efeitos externos.
Interface: Histórico, versão de worker e decisões persistidas.
Condição: Recuperação ou upgrade exige replay.
Aceite proposto: Histórico suportado reproduz comandos compatíveis e não repete chamada sem necessidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R018 → T243 [complements]
Como combinar: Encaminhar estados remotos incertos ao reconciliador.
Interface: Operation_id, tentativa, prazo e observações do destino.
Condição: Timeout não resolve o resultado de negócio.
Aceite proposto: Cada ambiguidade recebe estado verificável antes de retry de efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir Cadence com Temporal apenas pela história compartilhada.
- Não confundir heartbeat recente com confirmação de efeito remoto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas completos sob quedas e atraso de rede, incluindo tempo de recuperação e duplicações. O ganho de durabilidade não deve ser atribuído a mais parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T159, T160, T162, T241, T243

## Fontes primárias associadas

### V2B-S005 — Temporal Workflow

[https://docs.temporal.io/workflows](https://docs.temporal.io/workflows)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico de eventos, replay determinístico e reutilização de resultados de Activities já confirmadas.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S006 — Activity Definition

[https://docs.temporal.io/activity-definition](https://docs.temporal.io/activity-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Activities para ações externas, possibilidade de múltiplas execuções e necessidade de idempotência.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2A-S010 — Detecting Activity failures

[https://docs.temporal.io/encyclopedia/detecting-activity-failures](https://docs.temporal.io/encyclopedia/detecting-activity-failures)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Timeouts de atividades, heartbeats, detalhes de progresso e tentativas posteriores.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

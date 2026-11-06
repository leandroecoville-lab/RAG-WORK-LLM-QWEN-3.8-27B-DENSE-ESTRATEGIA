# T040 — State-Aware Window

**Nome canônico:** State-Aware Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T040  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela orientada ao estado

## T040:C01 — conceito

Seleciona contexto segundo o estado atual da tarefa: etapa em andamento, dependências, ações pendentes e critérios de conclusão. Distingue o que foi concluído do que continua necessário. É uma política do runtime que depende de estado estruturado confiável.

Como funciona:
- Ler estado e versão da missão.
- Determinar informações necessárias à próxima transição.
- Compor janela com essas informações e histórico recente suficiente.

## T040:C02 — aplicacao

Quando usar:
- Workflows com etapas e pré-condições claras.
- Execuções que precisam retomar após falha sem repetir efeitos.

Quando não usar:
- Não usar um resumo narrativo não verificado como única fonte do estado.

Implementação proposta:
- Proposta: representar etapa, pendências, resultados e evidências em campos explícitos.
- Manter chamadas iniciadas e seus resultados em pares rastreáveis.
- Construir o contexto a partir de um snapshot consistente para evitar leitura de versões conflitantes.

Aplicação LAI proposta:
Proposta LAI: usar máquina de estados da missão como âncora da Helena; recuperar detalhes apenas das tarefas e contratos que condicionam a próxima ação.

## T040:C03 — riscos_validacao

Armadilhas:
- Estado atrasado pode omitir uma ação ainda pendente.
- O agente pode marcar uma etapa como concluída antes de validar seu resultado.

Métricas sugeridas:
- Transições inválidas e ações duplicadas.
- Contexto necessário por etapa e sucesso na retomada.

Testes propostos:
- Interromper entre executar ferramenta e confirmar resultado e verificar reconciliação.
- Criar dependência não satisfeita e impedir que ela desapareça da janela.

## T040:C04 — perguntas_proveniencia

Pergunta: Estado estruturado substitui o histórico?
Resposta: Não. Ele representa o momento atual; o histórico permite auditar e reconstruir como o estado foi obtido.

Pergunta: O estado deve ser editado livremente pela LLM?
Resposta: A LLM pode propor atualizações; o runtime valida transições, versões e evidências antes de persistir.

Pergunta: O último timestamp basta para detectar conflito?
Resposta: Nem sempre. Relógios e resolução temporal podem esconder concorrência. Prefira revisões ou condições de escrita definidas pelo armazenamento.

Pergunta: Uma ferramenta pode terminar depois do cancelamento?
Resposta: Pode. Preserve o resultado tardio e reconcilie seu efeito; não trate o cancelamento local como prova de que o serviço parou.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T040:C05 — mecanismo_avancado

Uma janela orientada ao estado deve registrar a revisão usada para montar a requisição. Enquanto o modelo responde, outro ator pode concluir uma etapa, cancelar uma missão ou atualizar uma dependência. O contexto gerado continua coerente com sua leitura, mas pode estar desatualizado para executar a ação seguinte. A proposta de transição precisa ser revalidada contra o estado atual antes de produzir efeitos.

Condição de contorno:
O mecanismo não resolve concorrência apenas por usar JSON: leituras consistentes e regras de transição precisam existir no armazenamento ou controlador.

Contrato proposto:
- Entradas: Snapshot identificado, etapa pretendida, dependências e operações externas ainda sem confirmação.
- Saídas: Contexto específico da transição e revisão que deverá ser conferida no momento de aplicá-la.
- Estado: Versão do workflow, tentativas em andamento, resultados observados e agenda de próximas ações.
- Invariante: Uma decisão calculada sobre estado antigo não sobrescreve silenciosamente atualizações posteriores.

Compromissos de projeto:
- Janelas por etapa reduzem ruído e acoplam montagem de contexto ao modelo de execução.
- Revalidar versões evita decisões obsoletas, mas pode exigir nova geração quando há muita concorrência.

## T040:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atualizar uma pré-condição enquanto a chamada ao modelo está em curso. A resposta antiga deve ser rejeitada ou reavaliada antes da transição, preservando o novo estado.

Plano de avaliação proposto:
Avaliação proposta: comparar histórico recente e contexto por transição em tarefas concorrentes. Medir decisões obsoletas aceitas, repetição de geração, cobertura de pendências e tempo de conclusão; variar atraso entre leitura e aplicação.

Comparações:
- T065 (complements): Controle transacional pode proteger aplicação de propostas calculadas com uma versão conhecida.
- T060 (complements): Checkpoint fornece estado e agenda de retomada, mas não valida sozinho efeitos externos.

Afirmação rastreável:
Os checkpoints do LangGraph incluem valores de estado, próximos nós e tarefas, além de identificadores de execução.
Suporte: related; fontes: V3A-S031
Limite: Usar esses campos para montar uma janela por transição é uma proposta de arquitetura, não um comportamento automático do mecanismo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T040:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu revisão antes de efeitos. Aqui contexto é uma projeção tipada por estado, com transições que determinam quais informações mudam de função.

Projeto e decomposição
Defina vistas para coletar, verificar e executar. Evidência incompleta pode ser suficiente para coletar, mas não para confirmar ação; a mudança de fase altera requisitos do contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

Controle adaptativo
Registre por que cada campo entrou na vista. Quando objetivo muda, recalcule relevância e mantenha obrigações transversais; não preserve automaticamente todos os detalhes da fase anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

Validação contrafactual
Compare janela uniforme e vistas por estado. Meça ações prematuras, repetição de coleta e perda de restrições em transições, incluindo resultados tardios de ferramentas. Unidade de avaliação: transição de tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

USO AVANÇADO — Preparação de alteração
Cenário: Agente passa de análise para edição.
Estratégia: Na análise, carregar hipóteses; na execução, exigir especificação confirmada, revisão-base e teste de aceite. Bloquear salto sem esses campos.
Papel do modelo pequeno: 3–7B verifica checklist estruturado.
Aceite proposto: Nenhuma edição pode usar revisão-base desconhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

USO AVANÇADO — Investigação interrompida
Cenário: Nova informação invalida plano.
Estratégia: Voltar a estado de análise, marcar plano anterior como suspenso e reconstruir contexto com evidência nova.
Papel do modelo pequeno: 15–30B replaneja; 8–14B valida.
Aceite proposto: Não executar etapa pendente do plano revogado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Validador de campos obrigatórios por estado, com máquina de estados externa.
8–14B: Gerador de propostas locais dentro da fase autorizada.
15–30B: Replanejador de transições complexas com justificativa de mudança.
Requisitos de treino/runtime: Máquina de estados, revisões e contratos de entrada por fase; prompt não substitui validação do controlador.
Não aplicar quando: Estado é inferido apenas da conversa e não existe registro confiável das transições.

## T040:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T040:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T040 → T065 [requires]
Como combinar: Confirmar transição e suas pré-condições juntas.
Interface: Estado anterior, revisão, evento e estado proposto.
Condição: Transação cobrir invariantes locais.
Aceite proposto: Simular duas transições concorrentes e rejeitar a obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T040 → T043 [complements]
Como combinar: Compactar por fases encerradas.
Interface: Fronteira de fase, obrigações ativas e referências.
Condição: Resumo não ocultar requisito da próxima fase.
Aceite proposto: Retomar execução com evidência obrigatória ausente e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar mensagem do modelo como confirmação de estado.
- Distinguir intenção de executar e execução observada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar correção de transições sob interrupções; capacidade linguística não substitui estado explícito.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T060, T064, T065

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

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

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

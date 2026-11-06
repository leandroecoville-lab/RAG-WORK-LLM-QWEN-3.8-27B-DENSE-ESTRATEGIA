# T226 — Heartbeat de progresso

**Nome canônico:** Heartbeat de progresso  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** protocol  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T226  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** progress heartbeat; batimento de progresso

## T226:C01 — conceito

Sinal periódico de uma atividade acompanhado, quando adequado, de um marcador de avanço. O recebimento de heartbeat demonstra comunicação recente; somente a evolução de um marcador confiável indica progresso. Temporal documenta heartbeats de atividades e recuperação de detalhes registrados, sujeitos às condições de entrega e persistência do runtime.

Como funciona:
- O worker envia identidade, etapa e último avanço confirmado ao supervisor.
- O supervisor avalia idade do sinal e evolução do marcador em janelas distintas.
- Ausência de sinal pode acionar timeout, enquanto sinal estático pode acionar investigação de estagnação.

## T226:C02 — aplicacao

Quando usar:
- Atividades demoradas, processamento em lotes e operações que precisam oferecer visibilidade entre início e conclusão.

Quando não usar:
- Usar a emissão do heartbeat como comprovação de que uma escrita externa terminou ou de que o objetivo da missão foi cumprido.

Implementação proposta:
- Proposta: incluir execution_id, sequência de progresso, etapa e referência ao último resultado persistido.
- Usar o horário de recebimento para expiração e evitar depender apenas de relógios de máquinas diferentes.
- Persistir avanço antes de anunciá-lo como confirmado; tratar sinais atrasados e duplicados com identidade e ordenação.
- Definir prazo de silêncio considerando latência e duração legítima das etapas.
- Manter o heartbeat pequeno e separar detalhes extensos em artefatos consultáveis.

Aplicação LAI proposta:
Proposta LAI: expor progresso de missões por marcos confirmados, permitindo ao supervisor distinguir worker acessível, trabalho em andamento e execução sem avanço.

## T226:C03 — riscos_validacao

Armadilhas:
- Um timer independente pode emitir sinais enquanto o trabalho está travado.
- Perda do sinal gera falso diagnóstico de falha.
- Detalhes emitidos imediatamente antes da queda podem não ter sido persistidos pelo serviço.

Métricas sugeridas:
- Idade do último sinal; atraso de entrega; tempo sem avanço; sequência confirmada; falsos timeouts.

Testes propostos:
- Manter o timer ativo e bloquear o trabalho para verificar detecção de marcador estacionário.
- Entregar sinais fora de ordem e impedir regressão do estado observado.
- Interromper entre persistência e envio e confirmar recuperação a partir do registro durável.

## T226:C04 — perguntas_proveniencia

Pergunta: Heartbeat e progresso são a mesma coisa?
Resposta: Não. O sinal informa presença recente; o marcador informa avanço definido pelo domínio. Os dois devem ser observados separadamente.

Pergunta: O último heartbeat sempre permite retomar exatamente?
Resposta: Não. Ele pode estar atrasado ou conter informação apenas parcial. A retomada precisa validar o checkpoint e reconciliar resultados externos pendentes.

Pergunta: Heartbeatar a cada item elimina perda de progresso?
Resposta: Não necessariamente, porque o SDK pode agrupar envios e o processo pode cair antes da transmissão.

Pergunta: Por que cancelamento pode demorar?
Resposta: Porque a atividade pode receber o sinal por heartbeat, cuja frequência e throttling influenciam a entrega.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T226:C05 — mecanismo_avancado

Heartbeat local e heartbeat persistido não são o mesmo evento. Temporal pode limitar a frequência de envio e manter apenas o detalhe mais recente antes da transmissão. Um crash nesse intervalo pode perder o avanço ainda não entregue. O cursor recuperável deve indicar uma fronteira cuja reexecução seja segura: registrar progresso antes do efeito pode pular trabalho; registrar depois pode exigir repetir uma operação já realizada.

Condição de contorno:
O heartbeat comprova comunicação, mas somente um marcador ligado a trabalho confirmado sustenta retomada correta.

Contrato proposto:
- Entradas: Identidade da atividade, cursor confirmado, heartbeat timeout e detalhes de progresso.
- Saídas: Sinal enviado, estado conhecido pelo serviço e informação para próxima tentativa.
- Estado: Último cursor local, último persistido conhecido e efeitos associados.
- Invariante: O cursor não avança além do trabalho durável que pode ser reconstruído ou repetido com segurança.

Compromissos de projeto:
- Heartbeats frequentes reduzem atraso de detecção e aumentam tráfego, sujeito a throttling.
- Lotes maiores economizam comunicação e ampliam a quantidade de trabalho potencialmente repetido.

## T226:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: concluir um lote e derrubar o worker antes de o heartbeat chegar ao serviço; exigir retomada sem pular itens e sem duplicar efeitos lógicos.

Plano de avaliação proposto:
Comparar periodicidade por tempo e por lote, controlando custo e idempotência. Medir atraso de falha, perda de cursor recente, repetição e latência de cancelamento. Escolher fronteira de progresso pela semântica do trabalho.

Comparações:
- T060 (complements): Detalhes de heartbeat podem funcionar como pequeno checkpoint de atividade, dentro do contrato do runtime.
- T162 (complements): Idempotência protege itens cuja confirmação e progresso podem divergir durante falha.

Afirmação rastreável:
Temporal documenta throttling de heartbeats e entrega de cancelamento associada a eles.
Suporte: direct; fontes: V2A-S010
Limite: O progresso só sobrevive se for entregue ao serviço; chamadas locais não confirmam persistência imediata.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T226:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciava heartbeat local e persistido. A expansão define marcadores de avanço por fase, interpreta silêncio e lida com resultados atrasados sem converter comunicação frequente em falsa prova de progresso.

Progresso mensurável por fase
Durante download, bytes confirmados podem ser sinal útil; durante teste, casos concluídos; durante edição, artefato validado. Um contador que avança por token gerado não demonstra aproximação do objetivo. Cada fase declara qual marcador representa trabalho retomável e qual é apenas atividade do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040, V4C-S001.

Silêncio com contexto
Uma fase de computação longa pode não emitir avanço incremental observável. Defina duração esperada e sinal auxiliar de vida sem inventar cursor. Não reinicie automaticamente porque um marcador ficou estável durante uma operação indivisível legítima. A política precisa distinguir ausência de transporte, fase longa e repetição sem avanço semântico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040, V2A-S011.

Marcador e efeito
O cursor deve apontar para uma fronteira cuja retomada seja segura. Emiti-lo antes do efeito pode pular trabalho; depois do efeito pode permitir repetição. Combine marcador com identidade da operação e estado de confirmação. A frequência de heartbeat reduz janela de incerteza, mas não substitui idempotência nem transação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S040.

USO AVANÇADO — Processamento por lotes
Cenário: Uma atividade transforma milhares de registros.
Estratégia: Emita último lote confirmado e referência de saída, após persistência. Na retomada, valide existência e integridade do lote e continue da próxima unidade. Se a plataforma agrupa heartbeats, aceite que o último progresso local possa precisar de repetição segura.
Papel do modelo pequeno: 3–7B processa registros; código registra lotes e cursor.
Aceite proposto: Proposta: nenhuma lacuna e repetição limitada ao trecho cuja confirmação não chegou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040.

USO AVANÇADO — Subagente em tarefa extensa
Cenário: O supervisor quer acompanhar progresso sem receber toda a conversa.
Estratégia: Publique fase, artefatos aceitos, bloqueios e último avanço significativo. Um ping de conexão continua separado. Se o trabalhador retorna apenas texto dizendo que está trabalhando, o supervisor não deve renovar indefinidamente o prazo da missão.
Papel do modelo pequeno: 8–14B resume estado tipado; 15–30B usa mudanças reais para replanejar.
Aceite proposto: Proposta: detectar trabalhador estagnado sem interromper etapas longas válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar unidades com confirmação externa simples, sem emitir progresso por autodeclaração.
8–14B: Converter resultados em estados de fase e impedimentos concretos.
15–30B: Avaliar se progresso observado sustenta continuidade, respeitando duração e custo restantes.
Requisitos de treino/runtime: Transmissão e persistência observáveis, cursor por geração e contrato para retomada de unidades.
Não aplicar quando: Não usar heartbeat MCP de conectividade como prova de progresso cognitivo ou de conclusão de ferramenta.

## T226:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Heartbeat descobre presença de servidores, sem comprovar progresso semântico de tarefa.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Temporal documenta semântica de heartbeat; gateway Uber documenta conectividade. Esses conceitos foram mantidos distintos, sem contar ping como adoção exata de progresso.
Consultas registradas: V4C-Q002, V4C-Q009.

## T226:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T226 → T225 [feeds]
Como combinar: Entregar ao watchdog marcadores confirmados e sinais separados de vida para decidir recuperação.
Interface: Fase, cursor, timestamp e geração.
Condição: O marcador tem significado definido para aquela atividade.
Aceite proposto: Restart só ocorre pela política correspondente ao tipo de falha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T226 → T240 [complements]
Como combinar: Incluir no snapshot o progresso que foi efetivamente confirmado, junto do estado correspondente.
Interface: Cursor e referência dos resultados persistidos.
Condição: Captura consistente, sem cursor posterior ao estado.
Aceite proposto: Retomada não pula trabalho ainda não incluído no snapshot.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040, V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Heartbeat frequente pode esconder ciclo se só relata atividade, não avanço.
- Resultado atrasado de geração antiga não deve atualizar o cursor atual sem validação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare detecção de falhas e custo de retomada com atividades iguais. Um modelo maior não torna seus sinais de progresso confiáveis sem vínculo a artefatos ou efeitos observáveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T218, T060, T243

## Fontes primárias associadas

### V2A-S010 — Detecting Activity failures

[https://docs.temporal.io/encyclopedia/detecting-activity-failures](https://docs.temporal.io/encyclopedia/detecting-activity-failures)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Timeouts de atividades, heartbeats, detalhes de progresso e tentativas posteriores.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V2A-S011 — Configure Liveness, Readiness and Startup Probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Probes de vida, prontidão e inicialização possuem efeitos operacionais distintos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

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

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

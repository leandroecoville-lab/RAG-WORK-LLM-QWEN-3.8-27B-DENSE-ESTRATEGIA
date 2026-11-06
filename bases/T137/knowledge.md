# T137 — Rate Limiting

**Nome canônico:** Rate Limiting  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T137  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de taxa

## T137:C01 — conceito

Controle da taxa de admissão de solicitações para respeitar capacidade, quotas e equidade. Pode medir requisições, tokens, bytes ou unidades de custo. Limitar frequência é diferente de limitar concorrência: operações longas podem acumular mesmo com poucas entradas por segundo.

Como funciona:
- Associar cada pedido às quotas globais, de destino e de cliente.
- Verificar saldo ou janela antes de admitir a operação.
- Enfileirar com prazo ou rejeitar de forma explícita quando não houver capacidade.

## T137:C02 — aplicacao

Quando usar:
- API com quota de chamadas ou tokens.
- Serviço compartilhado em que um cliente pode consumir capacidade excessiva.

Quando não usar:
- Usar apenas limite de requisições quando o consumo depende principalmente do tamanho de cada pedido.

Implementação proposta:
- Escolher token bucket ou janela conforme o contrato do fornecedor.
- Em múltiplas réplicas, coordenar o contador ou particionar quota sem ultrapassar o total.
- Reservar consumo estimado e reconciliar com o uso real após a resposta.

Aplicação LAI proposta:
Proposta: coordenar quotas de inferência e ferramentas da Helena com custo estimado por chamada, além de um limite de tarefas simultâneas.

## T137:C03 — riscos_validacao

Armadilhas:
- Limites apenas por processo falham quando o número de réplicas aumenta.
- Retries imediatos transformam limitação em tempestade de tráfego.

Métricas sugeridas:
- Taxa admitida, rejeitada e tempo na fila.
- Consumo real versus quota por tenant e backend.

Testes propostos:
- Submeter rajada controlada e verificar o limite durante toda a janela.
- Executar clientes concorrentes e confirmar que um não esgota todas as reservas.

## T137:C04 — perguntas_proveniencia

Pergunta: Um semáforo substitui rate limit?
Resposta: Não. O semáforo limita operações simultâneas; o rate limit controla admissão no tempo.

Pergunta: Token do bucket é token da LLM?
Resposta: Pode representar essa unidade, mas é apenas uma unidade de orçamento escolhida.

Pergunta: Tokens faturados podem ser usados diretamente como sinal de admissão?
Resposta: São úteis para reconciliação, mas chegam tarde para impedir o consumo já iniciado; é necessária estimativa ou reserva prévia.

Pergunta: Dividir uma quota por réplicas é sempre eficiente?
Resposta: Não. Uma réplica ociosa pode reter saldo enquanto outra rejeita trabalho; redistribuição introduz outro compromisso de coordenação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T137:C05 — mecanismo_avancado

Limitar unidades heterogêneas exige decidir quando o custo é conhecido. Em geração, tokens de saída são observados ao final; uma proposta é reservar capacidade antes do envio e reconciliar consumo posteriormente. Uma reserva conservadora reduz excesso e pode deixar capacidade ociosa. Em múltiplas réplicas, limitadores locais com orçamento completo multiplicam a admissão global; particionamento de quotas e coordenação têm propriedades diferentes.

Condição de contorno:
Uma taxa aceitável não protege memória quando a duração das chamadas cresce; também é necessário observar trabalho simultâneo e tamanho das filas.

Contrato proposto:
- Entradas: Identidade da quota, custo estimado, unidade contábil e prazo da requisição.
- Saídas: Admissão, espera ou rejeição, com reserva e motivo identificáveis.
- Estado: Saldo, reposição, reservas em aberto e consumo confirmado.
- Invariante: A mesma capacidade não é reservada duas vezes por réplicas concorrentes.

Compromissos de projeto:
- Coordenação global aproxima a quota total, acrescentando comunicação e um ponto operacional adicional.
- Reservas pelo teto de saída reduzem ultrapassagem e diminuem utilização quando respostas são curtas.

## T137:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: liberar requisições simultâneas em várias réplicas e atrasar a conclusão de algumas; verificar orçamento global, devolução de reservas e limite de concorrência.

Plano de avaliação proposto:
Comparar quotas locais, partilhadas e coordenadas sob carga estável e rajadas. Controlar distribuição de tamanhos e duração. Medir excesso admitido, utilização, espera e justiça por cliente. Escolher conforme tolerância contratual a rajadas e consistência.

Comparações:
- T167 (complements): Token bucket fornece um mecanismo de saldo; a política decide unidade, escopo e reserva.
- T175 (complements): Uma rejeição pode acionar alternativa somente dentro das quotas elegíveis.

Afirmação rastreável:
A documentação de retries da AWS distingue a quota de repetições da admissão da primeira chamada.
Suporte: direct; fontes: V3C-S010
Limite: Esse bucket específico não implementa automaticamente o orçamento total de tokens de uma aplicação.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T137:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou reserva de tokens e limites globais entre réplicas. O novo desenho combina admissão por dimensão, prioridades de negócio e liquidação de custos quando chamadas terminam parcialmente.

Vetor de recursos
Uma requisição pode consumir slots, tokens de entrada, geração e memória de contexto. Limitar apenas requests por segundo permite que poucas conversas longas ocupem o servidor. Uma proposta usa reservas por dimensão e só admite quando todas as obrigatórias cabem, mantendo a unidade de cada contador visível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S014.

Reserva ligada à intenção
Dê à reserva identidade própria e vincule-a à tentativa. Cancelamento ou timeout não libera automaticamente recursos que o servidor ainda usa. Marque reserva em reconciliação, consulte o estado quando disponível e aplique expiração conservadora para não admitir carga nova sobre trabalho ainda ativo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S005, V2A-S012.

Prioridade com conta separada
Separe capacidade para consultas interativas, recuperação e processamento adiável. O modelo não escolhe sua própria prioridade a partir de linguagem persuasiva; a aplicação deriva classe por política. Meça rejeição e tempo de espera por classe, pois uma média boa pode ocultar bloqueio prolongado de uma delas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S003.

USO AVANÇADO — Servidor local compartilhado
Cenário: Vários agentes usam a mesma GPU com modelos 3–30B.
Estratégia: Estime demanda por contexto e saída antes de admitir; reserve margem para verificação e limite sessões simultâneas. Quando faltar memória prevista, mantenha a tarefa em fila ou reduza escopo permitido, sem depender apenas da exceção de falta de memória.
Papel do modelo pequeno: Modelos pequenos processam tarefas admitidas; o limitador é determinístico.
Aceite proposto: Proposta: medir tarefas aceitas, espera, OOM e consumo efetivo, com mistura fixa de contextos curtos e longos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S009.

USO AVANÇADO — Proteção do serviço de ferramentas
Cenário: O modelo pode gerar muitas consultas corretas ao mesmo endpoint.
Estratégia: Atribua quota por serviço e operação lógica; cache ou coalescência reduzem duplicatas antes da admissão. Retry consome uma conta explícita, evitando competir ilimitadamente com primeiras tentativas.
Papel do modelo pequeno: 3–7B produz pedidos estruturados, sem decidir limites ou liberar saldo.
Aceite proposto: Proposta: introduzir rajadas e falhas transitórias; aceitar somente política que mantenha pressão limitada e rastreie saldo sem vazamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificar custo aproximado de tarefas curtas, com valores finais calculados pelo runtime.
8–14B: Proposta: montar pedidos de ferramentas com estimativas de saída e estratégia de paginação.
15–30B: Proposta: planejar lotes maiores sob cotas explicitamente fornecidas pelo controlador.
Requisitos de treino/runtime: São necessários medidores do servidor e tratamento de reservas órfãs; parâmetros não determinam sozinho memória consumida.
Não aplicar quando: Não usar estimativa de tokens como único limite quando o gargalo real é conexão, CPU, banco ou concorrência.

## T137:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: Quota de repetição limita tráfego de recuperação, distinta da chamada inicial.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

V4C-C023 — Google / Borg
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.
Mecanismo documentado: O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.
Correspondência com esta base: Admissão de cargas é relacionada a controle de capacidade, sem especificar o rate limiter da ficha.
Transferência proposta para modelo pequeno: Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.
Limite: O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.
Fontes: V4C-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AWS documenta quota de retries; os limites multidimensionais para LLM local são proposta, sem transplante automático de quotas corporativas.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q009.

## T137:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T137 → T167 [complements]
Como combinar: Buckets implementam uma dimensão de taxa dentro da política multidimensional.
Interface: Unidade, saldo, taxa de reposição e custo reservado.
Condição: Cada dimensão conserva contabilidade independente.
Aceite proposto: Reexecutar sequências de admissão e verificar ausência de saldo negativo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T137 → T150 [complements]
Como combinar: Coalescer consultas equivalentes evita cobrar capacidade duplicada antes do envio.
Interface: Chave de operação, participantes e reserva compartilhada.
Condição: Resultados e permissões são realmente compartilháveis.
Aceite proposto: Cancelar um participante sem devolver o saldo de todos os demais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não liberar reserva inteira com base apenas no cancelamento local.
- Reconciliar consumo observado e evitar que erro de estimativa se acumule indefinidamente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare vazão útil, cauda de latência e falhas com uma rota de fronteira sob igual política de admissão. Parâmetros menores não garantem menor custo quando a tarefa repete.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T163, T164, T167, T175

## Fontes primárias associadas

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S011 — golang/sync — singleflight implementation

[https://github.com/golang/sync/blob/master/singleflight/singleflight.go](https://github.com/golang/sync/blob/master/singleflight/singleflight.go)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro de chamadas em curso por chave; Forget permite nova chamada sem aguardar a chamada anterior.

Limite: Branch master pode mudar; semântica inspecionada não constitui cache durável ou deduplicação de efeitos entre processos.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T167 — Token Bucket

**Nome canônico:** Token Bucket  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T167  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** balde de tokens

## T167:C01 — conceito

Algoritmo de limitação com reservatório de capacidade B e reposição de r unidades por segundo. Uma operação consome unidades; se não houver saldo, ela espera ou é rejeitada. Permite rajadas limitadas e controla a taxa média, conforme as condições do contrato.

Como funciona:
- Atualizar saldo por b = min(B, b + r × tempo_decorrido).
- Calcular custo de admissão da operação.
- Deduzir saldo atomicamente quando a operação é admitida.

## T167:C02 — aplicacao

Quando usar:
- API aceita rajadas, mas impõe taxa sustentada.
- Pedidos têm consumo que pode ser modelado em unidades de orçamento.

Quando não usar:
- Usá-lo como único controle de concorrência ou memória ocupada por tarefas longas.

Implementação proposta:
- Usar relógio monotônico para intervalos locais.
- Coordenar saldo em múltiplos workers ou dividir quotas com limite global.
- Definir o que acontece quando uma operação custa mais que a capacidade máxima.

Aplicação LAI proposta:
Proposta: controlar chamadas e orçamento de tokens da Helena em buckets distintos, pois as quotas podem ter unidades diferentes.

## T167:C03 — riscos_validacao

Armadilhas:
- Atualização não atômica permite ultrapassar a quota.
- Reset do processo pode recriar saldo cheio e liberar rajada indevida.

Métricas sugeridas:
- Consumo admitido por janela e tamanho de rajada.
- Tempo de espera e divergência do saldo em concorrência.

Testes propostos:
- Usar relógio controlado e verificar reposição, teto e rejeição sem saldo.
- Fazer consumo simultâneo e garantir que a soma não excede o permitido.

## T167:C04 — perguntas_proveniencia

Pergunta: Bucket token significa token do tokenizer?
Resposta: Não. A unidade é definida pela aplicação, embora possa representar tokens de inferência.

Pergunta: Uma tarefa maior que B entra depois de esperar?
Resposta: Não sem política especial; o saldo nunca ultrapassa B.

Pergunta: Por que um pedido grande pode esperar para sempre?
Resposta: Se seu custo excede a capacidade máxima e a reserva exige o custo integral, nenhuma reposição produzirá saldo suficiente.

Pergunta: A taxa r limita concorrência?
Resposta: Não. Ela limita reposição de crédito; duração das operações determina quantas podem permanecer ativas.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T167:C05 — mecanismo_avancado

Para um bucket simples de capacidade B e reposição r, o saldo após intervalo Δt sem consumo é min(B, saldo+r·Δt). Se uma operação custa q e q>B, ela nunca cabe em uma reserva integral: esperar indefinidamente não resolve. Outra distinção é marcar, atrasar e rejeitar tráfego; token bucket pode apoiar as três políticas, mas elas produzem comportamentos diferentes para o consumidor.

Condição de contorno:
O limite de rajada permite consumo imediato acima da taxa instantânea r; ele não promete espaçamento uniforme entre chamadas.

Contrato proposto:
- Entradas: Custo da operação, saldo, capacidade, taxa e instante de referência.
- Saídas: Admissão, tempo de espera calculado ou rejeição por custo incompatível.
- Estado: Saldo, última reposição e reservas futuras eventualmente emitidas.
- Invariante: O saldo não excede B e reservas concorrentes não gastam o mesmo crédito.

Compromissos de projeto:
- Bucket grande absorve rajadas e pode sobrecarregar uma dependência sensível a simultaneidade.
- Granularidade fina representa custo melhor e amplia contabilidade e sincronização.

## T167:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: acumular saldo até o teto, lançar rajada concorrente e pedir uma operação maior que B; verificar teto, exclusão de dupla reserva e rejeição explícita do pedido impossível.

Plano de avaliação proposto:
Comparar bucket, janela fixa e espaçamento uniforme com a mesma taxa média. Medir rajada admitida, atraso e saturação da dependência. Dimensionar B pela tolerância real a rajadas, sem confundi-lo com quantidade máxima de tarefas simultâneas.

Comparações:
- T137 (complements): Rate limiting define política e escopo; o bucket é um mecanismo possível.
- T166 (distinct_from): Um bucket compartilhado limita volume, mas não distribui automaticamente parcela justa entre clientes.

Afirmação rastreável:
RFC 2697 especifica buckets limitados com taxa de reposição e tamanhos de rajada para marcação de tráfego.
Suporte: related; fontes: V3C-S021
Limite: O RFC usa dois buckets; o contrato de bucket simples para chamadas é uma adaptação editorial.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T167:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 apresentava saldo, capacidade e pedidos grandes demais. A ampliação introduz reservas para custo desconhecido, coordenação entre buckets e contabilização de chamadas canceladas ou parcialmente executadas.

Reserva com liquidação
Para inferência, o custo final pode ser desconhecido antes da chamada. Reserve uma estimativa ou limite permitido e ajuste após receber consumo confiável. Se liberar toda a reserva no cancelamento enquanto o servidor continua gerando, o sistema cria créditos fictícios. Mantenha estado pendente até confirmação ou política conservadora de expiração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021, V2A-S012.

Composição de limites
Uma requisição pode depender de créditos de organização, usuário e recurso. Reservar um bucket e aguardar outro pode reter capacidade sem progresso. Use aquisição coordenada, ordem estável ou devolução controlada; defina se todos precisam estar disponíveis antes do envio. A atomicidade entre processos depende do armazenamento e não surge da fórmula local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021, V3C-S009.

Quota por finalidade
Separe orçamento de tráfego original, retries e sondas. Um bucket único pode deixar a recuperação consumir todos os créditos ou bloquear uma sonda barata que revelaria retorno do serviço. Os limites compartilham um teto superior quando usam a mesma capacidade física, evitando que três quotas independentes somem mais do que o serviço suporta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

USO AVANÇADO — Agentes com saídas variáveis
Cenário: Um assistente ora extrai um campo, ora gera uma análise extensa.
Estratégia: Classifique a operação antes da admissão e reserve segundo o teto da classe. Após concluir, liquide com uso observado. Se a saída atingir o limite, não continue automaticamente com uma segunda chamada sem nova admissão e sem somar o consumo anterior.
Papel do modelo pequeno: 3–7B extrai com teto curto; 15–30B recebe reserva maior apenas quando a tarefa exige.
Aceite proposto: Proposta: saldo consistente com consumo real, inclusive cancelamentos e falhas após envio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021.

USO AVANÇADO — Recuperação de API degradada
Cenário: Chamadas novas e repetidas disputam capacidade reduzida.
Estratégia: Use bucket de retry além da admissão normal, expondo motivo de recusa ao controlador. Uma tentativa que não obteve crédito ainda não foi enviada; seu estado não deve sugerir efeito remoto incerto. Reabastecimento acompanha política operacional, não decisão improvisada da LLM.
Papel do modelo pequeno: 8–14B reformula o plano após recusa tipada; não cria créditos.
Aceite proposto: Proposta: retries limitados durante falha sustentada e preservação de tráfego útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Operações de custo delimitado tornam reservas mais precisas e baratas.
8–14B: Estimar classe de consumo a partir de tarefa e entrada, validando erro de previsão.
15–30B: Planejar decomposição de chamadas que excedem capacidade sem ocultar custo agregado.
Requisitos de treino/runtime: Relógio monotônico, armazenamento concorrente, unidade de crédito definida e reconciliação de reservas pendentes.
Não aplicar quando: Não esperar indefinidamente por q maior que capacidade nem devolver crédito de trabalho remoto ainda ativo.

## T167:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: O texto identifica token bucket para limitar retries dos SDKs.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SDK AWS documenta uso operacional para retries. Reservas por token e composição de múltiplos escopos são propostas que exigem implementação concorrente correta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T167:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T167 → T163 [complements]
Como combinar: AWS usa créditos de retry para limitar repetição além do backoff temporal.
Interface: Saldo de retry e resultado da tentativa.
Condição: A política distingue chamadas iniciais e adicionais.
Aceite proposto: Falha prolongada não gera tentativas ilimitadas.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T167 → T137 [complements]
Como combinar: O limitador transforma disponibilidade de créditos em admissão e resposta ao solicitante.
Interface: Quantidade reservada, escopo e motivo da rejeição.
Condição: Reserva corresponde a capacidade definida, não a pontuação subjetiva.
Aceite proposto: Nenhum envio ocorre quando os buckets obrigatórios recusam admissão.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

CONTROLES DE FALHA
- Contabilidade local por réplica pode multiplicar uma quota supostamente global.
- Refill baseado em relógio de parede pode criar saldo errado após ajuste de hora.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo e qualidade sob a mesma quota efetiva. Melhor throughput de um modelo pequeno não justifica reservas inconsistentes nem omissão do trabalho cancelado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T175

## Fontes primárias associadas

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S021 — RFC 2697 — A Single Rate Three Color Marker

[https://www.rfc-editor.org/rfc/rfc2697.html](https://www.rfc-editor.org/rfc/rfc2697.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Marcador de tráfego com buckets limitados, taxa comprometida e tamanhos de rajada explicitados.

Limite: RFC descreve marcação de pacotes com dois buckets; limitador simples de chamadas é uma adaptação, não essa especificação integral.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

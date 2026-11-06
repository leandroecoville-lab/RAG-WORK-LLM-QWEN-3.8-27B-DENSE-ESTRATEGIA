# P013 — Resilience Engine / Reliability Controller

**Nome canônico:** Resilience Engine / Reliability Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de resiliência; controlador proposto de confiabilidade

## P013:C01 — conceito

Resilience Engine / Reliability Controller é um nome editorial proposto para aplicar uma política coerente de recuperação às chamadas e etapas. Coordenaria timeouts, tentativas, backoff, limites e circuit breaker. Esses mecanismos são documentados individualmente; as fontes não confirmam um serviço LAI implementado nem uma combinação automaticamente adequada a todas as dependências.

Como funciona:
- Classificar erros em temporários, permanentes e resultado desconhecido, usando o contrato da operação.
- Aplicar orçamento global de tempo e tentativas, combinando backoff com jitter e orientações Retry-After quando compatíveis.
- Abrir o circuito diante de falhas persistentes e liberar poucas sondas em half-open antes da recuperação normal.

## P013:C02 — aplicacao

Quando usar:
- Dependências sujeitas a indisponibilidade transitória, limites de capacidade e latência variável.

Quando não usar:
- Para repetir indefinidamente erros de contrato ou ações externas ambíguas sem idempotência e reconciliação.

Implementação proposta:
- Proposta: escolher uma camada responsável pelas tentativas, evitando multiplicação entre SDK, gateway e executor.
- Persistir retries adiados com deadline, próxima tentativa e chave da intenção original; cada tentativa recebe identificador próprio.
- Combinar limitação de concorrência com fila limitada e sinais de saúde; quando o orçamento acabar, devolver estado final ou inconclusivo ao executor.

Aplicação LAI proposta:
Proposta LAI: P013 administra mecanismos de recuperação do P011, enquanto P015 verifica identidade e confirmação dos efeitos externos.

## P013:C03 — riscos_validacao

Armadilhas:
- Jitter reduz sincronização, mas não cria capacidade no serviço indisponível.
- Half-open sem coordenação entre réplicas pode virar uma nova rajada.
- Trocar a chave de idempotência em cada retry transforma uma repetição lógica em nova solicitação.

Métricas sugeridas:
- Recuperações por classe de erro, amplificação de tentativas, ocupação da fila e tempo até detectar recuperação.

Testes propostos:
- Aceite proposto: simular falha transitória e recuperação gradual, observando limites de fila, deadline e número de sondas.
- Enviar erro permanente e timeout com efeito remoto confirmado posteriormente; exigir ausência de retry cego e preservação da intenção.

## P013:C04 — perguntas_proveniencia

Pergunta: Todas as camadas devem fazer três tentativas?
Resposta: Não. Tentativas aninhadas multiplicam chamadas; a política deve definir uma responsabilidade e orçamento comuns.

Pergunta: Um circuito fechado indica que o negócio funcionou?
Resposta: Não. Indica que chamadas estão permitidas pela política; conclusão da operação ainda depende de sua resposta e confirmação verificável.

Pergunta: O que caracteriza uma tempestade de retries?
Resposta: Tentativas em múltiplas camadas ampliam a carga justamente quando a dependência falha.

Pergunta: Reiniciar é sempre recuperação?
Resposta: Não. Sem corrigir a condição ou retomar com estado consistente, o restart pode repetir o mesmo erro.

Escopo das fontes:
Fontes fundamentam mecanismos de resiliência; coordenação, fila e aceites são desenho proposto.

## P013:C05 — mecanismo_avancado

Resilience Engine / Reliability Controller propõe coordenar timeout, retry, circuit breaker e fallback sob um orçamento por operação. Cada camada não deve multiplicar tentativas sem conhecer o limite global. Falhas permanentes, como entrada inválida, precisam de tratamento diferente de indisponibilidade transitória. O controlador também deve distinguir processo vivo, serviço apto a receber tráfego e trabalho progredindo, pois responder a um health check não prova avanço da tarefa.

Condição de contorno:
Reiniciar continuamente um worker que depende de um serviço indisponível pode ampliar a falha. Liveness não deve substituir um diagnóstico de dependência ou de ausência de progresso.

Contrato proposto:
- Entradas: Operação identificada, classificação do erro, deadline, tentativas consumidas, estado de dependências e política de degradação.
- Saídas: Decisão de repetir, aguardar, abrir circuito, trocar rota ou encerrar, com motivo e próximo instante elegível.
- Estado: Contadores por operação, estados de circuitos, leases, observações de progresso e orçamento restante.
- Invariante: Retries de qualquer camada consomem o mesmo orçamento lógico; uma falha não pode restaurar o limite inicial.

Compromissos de projeto:
- Backoff reduz pressão durante falha, mas aumenta o tempo até uma tentativa que poderia funcionar.
- Circuitos evitam insistência inútil, porém precisam de sondagem controlada para detectar recuperação sem tempestade.

## P013:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: combinar timeout em cliente e retry no worker durante indisponibilidade prolongada; verificar limite global, jitter e recuperação gradual sem pico sincronizado de novas chamadas.

Plano de avaliação proposto:
Comparar política isolada por camada e orçamento compartilhado sob falhas transitórias e permanentes. Medir amplificação de chamadas, tempo de recuperação, tarefas abandonadas e latência de cauda. Registrar o custo da degradação e do fallback.

Comparações:
- T138 (complements): Circuit breaker controla acesso a dependências falhas.
- T227 (complements): Checks distinguem prontidão, vida e sinais específicos de progresso.

Afirmação rastreável:
Circuit breaker controla falhas de dependências; readiness e liveness têm efeitos operacionais diferentes.
Suporte: related; fontes: C-S005, V3D-S017
Limite: A política global proposta precisa ser implementada; a documentação Kubernetes não define progresso semântico da tarefa.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P013:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a proposta de confiabilidade com isolamento por domínio de falha, teste controlado de recuperação e orçamento contra tempestade de retries.

Domínio de falha correto
Proposta: particionar circuitos por recurso e falha observável, evitando que um cliente inválido bloqueie todos os demais. Falhas de autenticação, sobrecarga e indisponibilidade têm respostas distintas. Preservar métricas por tenant e operação ajuda a evitar um circuito que apenas oculta defeitos de contrato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

Recuperação com carga limitada
Usar probes com orçamento e competição controlada. A volta de uma dependência não autoriza liberar toda a fila acumulada de uma vez. Reintroduzir tráfego gradualmente e observar p95, rejeições e sucesso; um teste simples de conexão pode passar enquanto a operação real ainda falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

Amplificação entre camadas
Calcular o máximo de tentativas efetivas considerando SDK, gateway, workflow e agente. Um teto por camada pode multiplicar carga. A política global distribui créditos e conserva identidade lógica; jitter reduz sincronização, mas não cria capacidade ausente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

USO AVANÇADO — Provedor de modelo degradado
Cenário: Latência aumenta e alguns pedidos retornam erro transitório.
Estratégia: Limitar concorrência, usar deadline residual e alternar apenas para rota compatível quando houver orçamento.
Papel do modelo pequeno: LLM pequena continua tarefas elegíveis; a política de falha usa telemetria externa.
Aceite proposto: Carga no provedor cai durante falha e retorno não dispara pico maior que a capacidade medida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

USO AVANÇADO — Ferramenta com erro permanente
Cenário: Argumentos ou credenciais inválidos geram repetição inútil.
Estratégia: Classificar erro e encerrar retry de transporte; reparar contrato somente em fluxo apropriado.
Papel do modelo pequeno: Modelo pode explicar o erro tipado sem receber segredo ou autoridade de ignorar política.
Aceite proposto: Erros permanentes não consomem toda a fila nem o orçamento de tentativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: classificação auxiliar de mensagens, sem autoridade exclusiva sobre retry.
8–14B: 8–14B: reparo de argumentos dentro de schema e limite de tentativas.
15–30B: 15–30B: diagnóstico complexo sob demanda, sem ocupar o caminho crítico de cada requisição.
Requisitos de treino/runtime: Métricas, limites e estados do circuito pertencem ao runtime e precisam de testes de falha.
Não aplicar quando: Não usar fallback que viole o requisito da tarefa só para manter resposta disponível.

## P013:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: A coordenação proposta de resiliência pode reproduzir o princípio de um orçamento explícito.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Política de degradação é princípio do controlador editorial.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P013 é proposta. AWS, SRE Google e plataformas de fila sustentam mecanismos e limites, sem comprovar o controlador editorial completo.
Consultas registradas: V4C-Q001, V4C-Q003, V4C-Q004.

## P013:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P013 → T138 [complements]
Como combinar: Associar circuito ao recurso e classe de falha adequados.
Interface: Chave do circuito, estado, amostra e orçamento de probes.
Condição: Dependência apresenta falha correlacionada.
Aceite proposto: Erros de um escopo não derrubam escopos independentes sem evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S005, C-S026, V3D-S017, V4C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P013 → T163 [complements]
Como combinar: Distribuir esperas e tentativas dentro do teto lógico.
Interface: Deadline, retry_credit e identidade da operação.
Condição: Falha é transitória e repetição é segura.
Aceite proposto: Retries de todas as camadas respeitam o mesmo limite efetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S005, C-S026, V3D-S017, V4C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar indiscriminadamente liveness para reiniciar serviço saudável dependente de outro indisponível.
- Não interpretar jitter como proteção suficiente contra sobrecarga.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso e custo em falhas injetadas, não apenas operação normal. Reportar rejeições controladas e tempo até recuperação sem mascarar falhas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T138, T162, T163, T164, T165, T228, P011, P015

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S027 — Timeouts, retries, and backoff with jitter

[https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retries limitados, timeouts e jitter reduzem amplificação de falhas transitórias.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S017 — Kubernetes — Liveness, readiness and startup probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Liveness e readiness produzem efeitos diferentes de reinício e elegibilidade para receber tráfego.

Limite: Não oferece por si só comprovação de progresso semântico de uma tarefa de agente.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

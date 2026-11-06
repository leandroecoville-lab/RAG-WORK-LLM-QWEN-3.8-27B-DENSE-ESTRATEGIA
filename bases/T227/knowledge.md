# T227 — Health Checks — liveness, readiness e progresso

**Nome canônico:** Health Checks — liveness, readiness e progresso  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T227  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** liveness readiness progress; verificações de saúde

## T227:C01 — conceito

Conjunto de verificações que diferencia processo capaz de funcionar, instância pronta para atender e trabalho avançando. Kubernetes documenta liveness, readiness e startup probes. Progresso de uma missão é uma verificação de domínio adicional, não um quarto tipo nativo de probe que deva ser presumido universal.

Como funciona:
- Liveness identifica condições em que reiniciar pode recuperar o processo.
- Readiness controla se a instância deve receber tráfego ou novas tarefas.
- Startup oferece tolerância durante inicialização; progresso avalia evolução de uma tarefa ativa segundo critérios próprios.

## T227:C02 — aplicacao

Quando usar:
- Serviços com inicialização demorada, workers que dependem de filas e execução de missões com marcos observáveis.

Quando não usar:
- Usar uma chamada cara a todas as dependências como liveness ou considerar um worker ocioso como estagnado.

Implementação proposta:
- Proposta: definir respostas distintas para processo travado, indisponibilidade temporária e falta de avanço.
- Verificar readiness antes de atribuir trabalho e informar motivos úteis sem expor dados sensíveis.
- Criar tolerância de startup compatível com carregamento e migrações autorizadas.
- Avaliar progresso apenas quando existe missão ativa, com prazo específico para a etapa.
- Manter checks leves, limitar sua frequência e registrar mudanças de estado com timestamps.

Aplicação LAI proposta:
Proposta LAI: publicar saúde operacional dos workers e saúde das missões separadamente, fazendo o controlador reagir à causa observada com critérios verificáveis.

## T227:C03 — riscos_validacao

Armadilhas:
- Uma dependência indisponível pode causar reinícios em massa se liveness for mal definida.
- Readiness positiva não prova correção funcional.
- Um endpoint saudável pode coexistir com fila parada ou resultados incorretos.

Métricas sugeridas:
- Duração em cada estado; falhas por tipo; reinícios desnecessários; atraso de atribuição; missões sem avanço.

Testes propostos:
- Indisponibilizar uma dependência compartilhada e verificar retirada de readiness sem tempestade de restart.
- Bloquear o processo de trabalho mantendo o endpoint ativo e conferir alarme de progresso.
- Simular inicialização longa dentro do prazo e evitar reinício prematuro.

## T227:C04 — perguntas_proveniencia

Pergunta: Readiness falha reinicia o processo?
Resposta: No modelo documentado de Kubernetes, readiness regula disponibilidade para tráfego; ela não equivale por si só ao gatilho de reinício de liveness.

Pergunta: Como medir progresso sem tarefas ativas?
Resposta: Não há avanço de missão a exigir. O estado deve ser ocioso ou aguardando, acompanhado de checks de capacidade para receber trabalho.

Pergunta: Readiness falsa deve sempre causar restart?
Resposta: Não. Frequentemente significa apenas que a instância não deve receber tráfego enquanto recupera capacidade.

Pergunta: Liveness verdadeira prova que a tarefa avança?
Resposta: Não. O processo pode responder a uma sonda simples enquanto uma missão está estagnada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T227:C05 — mecanismo_avancado

Falha de readiness deve retirar a instância do tráfego que depende dessa sinalização; não implica automaticamente matar o processo. Uma startup probe protege inicialização lenta contra liveness prematura. Progresso do agente requer outro invariante: uma API saudável pode hospedar uma missão parada. A proposta separa saúde do servidor, capacidade de atender e estado de cada trabalho, evitando um endpoint único que misture todas as causas.

Condição de contorno:
Uma probe que verifica apenas resposta HTTP pode passar enquanto filas, modelo ou tarefas específicas estão bloqueados.

Contrato proposto:
- Entradas: Sinais de inicialização, capacidade de atendimento, vida do processo e avanço por missão.
- Saídas: Estados separados e ação de operação apropriada a cada um.
- Estado: Histórico de sondas, dependências observadas e cursor de progresso.
- Invariante: Indisponibilidade de uma missão não é automaticamente convertida em reinício de todas as missões da instância.

Compromissos de projeto:
- Sondas profundas detectam mais falhas e podem aumentar carga sobre dependências já degradadas.
- Sondas leves são baratas e fornecem evidência restrita de funcionamento.

## T227:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inicialização lenta, dependência temporariamente indisponível e missão sem progresso em processo responsivo; exigir três diagnósticos e respostas diferentes.

Plano de avaliação proposto:
Comparar endpoint único e sinais separados sob falhas controladas. Medir reinícios indevidos, tráfego enviado a instância incapaz e tempo para detectar missão parada. Dimensionar frequência pelos custos e tempos de recuperação relevantes.

Comparações:
- T225 (complements): O supervisor utiliza sinais de saúde para escolher se reinicia ou espera.
- T226 (complements): Heartbeat com cursor pode fornecer evidência de progresso de uma atividade.

Afirmação rastreável:
Kubernetes diferencia startup, liveness e readiness e documenta que readiness e liveness não dependem uma da outra.
Suporte: direct; fontes: V2A-S011
Limite: Sinal de progresso é requisito adicional da aplicação, sem equivalência automática a um tipo nativo de probe.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T227:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava liveness, readiness e avanço da missão. A expansão propõe checagens por capacidade e classe de trabalho, com inicialização controlada e respostas de recuperação proporcionais ao que falhou.

Readiness por capacidade
Um servidor pode aceitar texto curto e não ter recursos para multimodalidade ou contextos longos. Exponha capacidades elegíveis e suas dependências, em vez de um único booleano que promete tudo. O roteador precisa considerar essa informação junto da quota; estar pronto para um contrato não significa estar pronto para qualquer tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V4C-S018.

Inicialização e aquecimento
Carregamento de pesos, conexão e compilação podem levar mais tempo que uma chamada comum. Use fase explícita de startup e só admita tráfego quando recursos necessários estiverem disponíveis. Falha de readiness durante aquecimento não deve disparar repetição infinita do próprio aquecimento. Teste também a primeira chamada depois de deploy.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V2A-S012.

Cheque funcional delimitado
Uma checagem semântica pode validar parser, tokenizer e chamada mínima compatível, mas não representa toda distribuição de tarefas. Mantenha sondas baratas e limites para não competir com o serviço principal. Se a dependência externa cair, retire apenas capacidades afetadas quando o isolamento permitir, preservando funções saudáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V3C-S009.

USO AVANÇADO — Servidor de modelos local
Cenário: O processo responde HTTP enquanto o modelo ainda carrega ou ficou indisponível.
Estratégia: Separe endpoint de vida do estado de carregamento e da elegibilidade por recurso. Antes de liberar tráfego, execute contrato mínimo e registre configuração. Se um modelo falhar, não marque todos os outros como mortos quando compartilham processo mas têm isolamento válido.
Papel do modelo pequeno: 3–7B e 15–30B têm perfis diferentes; checagem usa capacidade real, não só nome.
Aceite proposto: Proposta: nenhuma admissão prematura e recuperação sem ciclos de startup.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V2A-S011.

USO AVANÇADO — Agente com várias ferramentas
Cenário: Algumas integrações falham, mas outras permanecem úteis.
Estratégia: Publique disponibilidade por ferramenta e mantenha tarefas dependentes em estado bloqueado. Não matar o supervisor saudável para corrigir API remota. Se a missão não progride apesar de todas as dependências prontas, encaminhe diagnóstico de tarefa, não uma falha genérica de servidor.
Papel do modelo pequeno: 8–14B explica degradação; controlador decide capacidade e ações.
Aceite proposto: Proposta: isolamento de falha e continuidade de trabalho independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Serviços pequenos podem ter startup mais simples, mas ainda precisam de contrato funcional.
8–14B: Classificar dependências afetadas por missão e produzir diagnóstico estruturado.
15–30B: Replanejar trabalho durante degradação sem redefinir saúde por opinião textual.
Requisitos de treino/runtime: Probes com escopo, limiares e consequências definidos; métricas de primeira chamada e tráfego admitido.
Não aplicar quando: Não misturar health de processo com qualidade de resposta ou progresso da missão.

## T227:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Kubernetes fundamenta probes; fontes de serving e gateways apoiam capacidades. O desenho por classes para agentes é proposta, sem ganho operacional medido.
Consultas registradas: V4C-Q004, V4C-Q018.

## T227:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T227 → T138 [complements]
Como combinar: Falhas funcionais de uma dependência alimentam breaker específico sem declarar todo o processo morto.
Interface: Capacidade afetada, classe da falha e janela observada.
Condição: Sonda corresponde ao caminho que o breaker protege.
Aceite proposto: Funções independentes continuam disponíveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026, V2A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T227 → T226 [complements]
Como combinar: Progresso por tarefa complementa saúde do serviço e detecta missão parada em servidor saudável.
Interface: Fase, último avanço e identidade da missão.
Condição: Progresso é definido por domínio.
Aceite proposto: Detectar tarefa sem avanço sem reiniciar outras tarefas válidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Probe pesada pode causar a sobrecarga que pretende detectar.
- Não interpretar readiness negativa como ordem universal de matar o processo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade funcional por classe e tempo de recuperação. Um modelo pequeno que cabe no recurso pode manter uma capacidade específica, sem substituir funcionalidades que não suporta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T226, T218

## Fontes primárias associadas

### V2A-S011 — Configure Liveness, Readiness and Startup Probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Probes de vida, prontidão e inicialização possuem efeitos operacionais distintos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S024 — Controllers

[https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Laços de controle com observação do estado atual e aproximação ao estado desejado.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

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

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

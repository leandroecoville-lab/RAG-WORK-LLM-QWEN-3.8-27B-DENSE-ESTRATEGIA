# T139 — Parallel Tool Calls

**Nome canônico:** Parallel Tool Calls  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T139  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** chamadas concorrentes de ferramentas

## T139:C01 — conceito

Execução concorrente de chamadas de ferramentas cujas entradas e efeitos não dependem umas das outras. A concorrência pode reduzir tempo total, mas o ganho depende de capacidade disponível, filas e duração das operações. A proposta de chamadas pela LLM não garante que o runtime as execute em paralelo.

Como funciona:
- Construir dependências entre chamadas antes de despachá-las.
- Executar conjunto independente com concorrência limitada.
- Reunir resultados associados aos identificadores originais, preservando falhas individuais.

## T139:C02 — aplicacao

Quando usar:
- Consultas independentes a fontes distintas.
- Leitura de vários arquivos para uma análise conjunta.

Quando não usar:
- Uma escrita precisa do resultado de outra ou duas operações disputam o mesmo estado mutável.

Implementação proposta:
- Usar task group ou mecanismo equivalente com timeout por chamada e global.
- Aplicar semáforo e quotas do backend.
- Escolher política de resultado parcial ou cancelamento do grupo antes da execução.

Aplicação LAI proposta:
Proposta: paralelizar leituras independentes da Helena, mantendo mutações e dependências em ordem explícita.

## T139:C03 — riscos_validacao

Armadilhas:
- Concorrência ilimitada esgota conexões e viola quotas.
- Confundir ordem de chegada com identidade mistura respostas de ferramentas.

Métricas sugeridas:
- Latência total comparada à execução sequencial.
- Pico de concorrência, taxa de erro e utilização do destino.

Testes propostos:
- Variar artificialmente a duração das chamadas e conferir associação correta de resultados.
- Fazer uma chamada falhar e verificar a política declarada para as restantes.

## T139:C04 — perguntas_proveniencia

Pergunta: Duas chamadas paralelas tornam a LLM paralela?
Resposta: Não. O paralelismo pertence ao runtime e às ferramentas.

Pergunta: O tempo final será o da mais lenta?
Resposta: Só como aproximação sem filas, limites ou overhead relevante.

Pergunta: Cancelar o grupo garante ausência de efeitos?
Resposta: Não. O cancelamento pode chegar depois da conclusão; cada operação precisa de confirmação ou reconciliação própria.

Pergunta: Como preservar ordem sem serializar chamadas?
Resposta: Atribuir índice ou ID estável às entradas e ordenar os resultados por essa identidade após a coleta.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T139:C05 — mecanismo_avancado

Concorrência exige escolher a política de erro do grupo. Em execução fail-fast, um erro sinaliza cancelamento dos irmãos; em coleta completa, todos os resultados são aguardados e classificados. O cancelamento costuma ser cooperativo: uma ferramenta pode ter concluído o efeito antes de observar o sinal. Por isso, o agregador deve acompanhar estados individuais em vez de inferir que todas as chamadas falharam junto com a primeira.

Condição de contorno:
O ganho desaparece quando as ferramentas competem pelo mesmo recurso ou quando a segunda chamada depende de um valor produzido pela primeira.

Contrato proposto:
- Entradas: Chamadas independentes, limites de concorrência e política de resultado parcial.
- Saídas: Resultado por chamada, ordem lógica e status de cancelamento confirmado ou pendente.
- Estado: IDs das chamadas, tarefas ativas, erros e deadline compartilhado.
- Invariante: A posição do resultado corresponde ao ID da chamada, não à ordem de chegada.

Compromissos de projeto:
- Fail-fast pode economizar trabalho; coleta completa preserva evidências úteis mesmo com falhas parciais.
- Limitar concorrência reduz pressão e pode aumentar tempo de um lote pequeno.

## T139:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: combinar uma chamada rápida com erro, uma lenta cancelável e uma escrita que conclui antes do cancelamento; exigir três desfechos distintos e reconciliação da escrita.

Plano de avaliação proposto:
Comparar sequência, paralelismo ilimitado e grupo limitado com latências heterogêneas. Controlar capacidade das ferramentas. Medir tempo do lote, carga máxima, efeitos redundantes e completude do resultado; escolher a política conforme dependência real de todos os ramos.

Comparações:
- T147 (complements): Fan-out define distribuição e junção; chamadas paralelas concretizam o trabalho dos ramos.

Afirmação rastreável:
errgroup associa propagação de erros, cancelamento por contexto e limite de tarefas ativas.
Suporte: direct; fontes: V3C-S007
Limite: A API não torna efeitos remotos reversíveis nem obriga funções a respeitarem imediatamente o cancelamento.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T139:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu cancelamento e políticas de erro do grupo. O aprofundamento acrescenta análise de efeitos, fan-out especulativo limitado e comparação consistente de resultados obtidos em momentos diferentes.

Independência por recurso
Construa uma matriz de leitura e escrita dos recursos envolvidos. Duas ferramentas com nomes distintos podem alterar o mesmo objeto; duas leituras podem produzir resultados incompatíveis se observarem versões diferentes. Paralelismo exige declarar tanto dependências de dados quanto a consistência necessária à junção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V4C-S015.

Especulação recuperável
Quando a próxima rota é incerta, uma busca barata pode começar enquanto outra classificação termina. Isso só compensa se o trabalho especulativo for cancelável, sem efeitos, e a latência economizada superar o custo de resultados descartados. Mantenha a especulação em orçamento separado para que ela não ocupe a capacidade das chamadas obrigatórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S007, V3C-S005.

Junção com proveniência temporal
Cada resultado precisa trazer fonte, versão ou instante de observação e estado de conclusão. O agregador não deve escolher o mais rápido como se fosse o mais atual. Quando a decisão exige uma visão consistente, revalide os campos críticos após reunir as respostas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S007, V3A-S030.

USO AVANÇADO — Pesquisa técnica por evidências independentes
Cenário: Uma pergunta exige contrato, código e relato operacional.
Estratégia: Dispare buscas em fontes distintas com objetivos delimitados; deduplique documentos e compare divergências. Se uma fonte falhar, preserve a lacuna e evite preencher seu papel com repetição das demais.
Papel do modelo pequeno: 3–7B extrai fatos por fonte; 8–30B confronta evidências sem transformar repetição em consenso.
Aceite proposto: Proposta: medir cobertura, duplicação de fontes e latência, mantendo o mesmo orçamento total da execução serial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

USO AVANÇADO — Diagnóstico de falha em aplicação
Cenário: Logs, métricas e revisão de código podem ser consultados simultaneamente.
Estratégia: Leia cada superfície com um intervalo e revisão declarados; combine por identificadores de execução. Só depois escolha uma mutação. Se os dados pertencem a instantes incompatíveis, faça uma leitura focada antes de propor reparo.
Papel do modelo pequeno: 8–14B organiza hipóteses; 15–30B integra relações entre subsistemas.
Aceite proposto: Proposta: aceitar diagnóstico apenas quando cada hipótese decisiva aponta para evidência identificável e temporalmente compatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: workers de extração com uma ferramenta ou domínio por vez, retornando campos curtos.
8–14B: Proposta: selecionar e combinar poucas consultas independentes sob limite explícito de concorrência.
15–30B: Proposta: coordenar investigação mais ampla, reservando a junção e verificação como etapas obrigatórias.
Requisitos de treino/runtime: O servidor precisa suportar concorrência real; definir limites por endpoint, timeout e semântica de cancelamento.
Não aplicar quando: Não paralelizar mutações concorrentes no mesmo recurso nem consultas cujo segundo argumento depende do primeiro resultado.

## T139:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O relato identifica chamadas paralelas de ferramentas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research comprova uso de ferramentas paralelas; outros sistemas fornecem princípios de consistência. Transferência de porte permanece proposta. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q003, V4C-Q010, V4D-Q018.

## T139:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T139 → T147 [complements]
Como combinar: O fan-out define participantes e condição de junção das chamadas paralelas.
Interface: Lista fechada de tarefas e resultados com status individual.
Condição: O produtor sinaliza que terminou de criar participantes.
Aceite proposto: Injetar falha em um ramo e verificar completude segundo a política escolhida.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T139 → T137 [complements]
Como combinar: Chamadas concorrentes precisam passar pela admissão para não transformar latência menor em sobrecarga.
Interface: Reserva por tentativa, destino e custo estimado.
Condição: O orçamento considera chamadas especulativas e retries.
Aceite proposto: Comparar pico de carga e tarefas aceitas contra execução serial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009, V3C-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar cancelamento do grupo como desfazimento dos efeitos já realizados.
- Descartar resultados sem identidade suficiente para ligá-los à subtarefa correta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelo pequeno com chamadas paralelas e modelo de fronteira serial ou paralelo sob custo igual. Ganho de latência da infraestrutura não prova ganho de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T147, T160, T162

## Fontes primárias associadas

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T174 — Priority-Based Scheduling

**Nome canônico:** Priority-Based Scheduling  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T174  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento por prioridade

## T174:C01 — conceito

Política que decide qual trabalho pronto deve ocupar um recurso segundo prioridade, prazo e capacidade. Usa frequentemente uma priority queue, mas também define preempção, reservas e admissão. Priorizar sem equidade pode reduzir a espera de alguns clientes enquanto paralisa outros.

Como funciona:
- Considerar somente tarefas cujas dependências estão satisfeitas.
- Comparar prioridade efetiva e compatibilidade com recursos livres.
- Despachar e atualizar política após término, espera ou expiração.

## T174:C02 — aplicacao

Quando usar:
- Interações imediatas competem com processamento em lote.
- Existem classes de serviço e prazos diferentes.

Quando não usar:
- Prioridades são autoatribuídas sem controle e qualquer pedido pode se declarar urgente.

Implementação proposta:
- Estabelecer classes, critérios de desempate e quotas por classe.
- Separar prioridade de política de preempção suportada pelo backend.
- Adotar aging ou reserva mínima para trabalhos de baixa prioridade.

Aplicação LAI proposta:
Proposta: priorizar atendimentos em andamento da Helena sem eliminar capacidade mínima para indexação e verificação de conhecimento.

## T174:C03 — riscos_validacao

Armadilhas:
- Interromper GPU ou ferramenta nem sempre é possível sem perder trabalho.
- Prioridade alta não supera dependência ainda não concluída.

Métricas sugeridas:
- Latência por classe e violações de prazo.
- Eficiência de utilização e tempo perdido com preempções.

Testes propostos:
- Misturar cargas e comparar com FIFO sob o mesmo limite de recursos.
- Inundar a classe prioritária e verificar proteção das demais conforme política.

## T174:C04 — perguntas_proveniencia

Pergunta: Priority queue implementa toda essa política?
Resposta: Não. A fila só ordena itens; o scheduler decide admissão e recursos.

Pergunta: Prioridade maior sempre executa primeiro?
Resposta: Somente entre tarefas admissíveis e recursos compatíveis.

Pergunta: Alta prioridade implica parar o que já está rodando?
Resposta: Não. Pode significar apenas preferência na próxima admissão; preempção é uma política adicional.

Pergunta: Por que uma tarefa urgente pode continuar parada?
Resposta: Porque falta recurso compatível ou uma dependência está bloqueada; reordenar a fila não remove essa condição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T174:C05 — mecanismo_avancado

Prioridade de espera e preempção de trabalho ativo são decisões distintas. Kubernetes permite uma classe prioritária que não remove Pods em execução. Em agentes, uma ação pode ser não preemptível depois de enviar um efeito; interrompê-la libera o cliente, mas não necessariamente a capacidade remota. Um escalonador precisa considerar custo de retomada, reservas e possibilidade de inversão de prioridade quando uma tarefa urgente depende de outra menos prioritária.

Condição de contorno:
Prioridade alta não cria recurso compatível nem reduz uma dependência que continua bloqueada.

Contrato proposto:
- Entradas: Trabalhos prontos, prioridades, recursos, dependências e pontos de interrupção válidos.
- Saídas: Admissão, espera, reserva ou preempção explicitamente suportada.
- Estado: Ocupação, recursos retidos, custo de retomada e prioridade herdada quando prevista.
- Invariante: Uma tarefa não é interrompida como se pudesse ser retomada sem contrato para isso.

Compromissos de projeto:
- Preempção melhora resposta urgente e pode desperdiçar progresso do trabalho interrompido.
- Não preemptir conserva trabalho e pode elevar muito a espera de uma tarefa importante.

## T174:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma tarefa urgente depende de recurso retido por tarefa menos prioritária; verificar se a política detecta o bloqueio em vez de apenas ordenar a fila.

Plano de avaliação proposto:
Comparar prioridade não preemptiva, reservas e preempção em pontos seguros. Medir tempo por classe, trabalho perdido e inanição. Definir urgência e justiça separadamente, sem assumir que o mesmo número resolve ambos.

Comparações:
- T149 (complements): A fila fornece ordem; o escalonador decide uso de recursos e interrupção.
- T161 (complements): Caminho crítico informa dependências que podem dominar a prioridade nominal.

Afirmação rastreável:
Kubernetes documenta prioridade sem preempção por meio de preemptionPolicy Never.
Suporte: direct; fontes: V3C-S016
Limite: Essa semântica ilustra a distinção; não é uma API de controle de ferramentas do agente.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T174:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia prioridade e preempção. A nova camada combina urgência, custo de retomada e recursos exclusivos, com decisões de admissão que evitam interromper trabalho cujo efeito não pode ser desfeito.

Urgência verificável
Traduza prioridade em objetivo operacional: deadline, atendimento interativo ou desbloqueio de uma cadeia. Uma etiqueta alta sem critério tende a se espalhar até perder significado. Exija justificativa por classe e reavalie urgência quando a tarefa ficar obsoleta, em vez de manter pedidos antigos consumindo a reserva indefinidamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S016.

Pontos de suspensão
Defina onde a tarefa pode liberar recursos sem perder invariantes. Entre chamadas pode ser seguro; durante escrita remota talvez não. Checkpoint de contexto não garante checkpoint da ferramenta. Se não houver suspensão válida, a política pode reservar capacidade futura e evitar admitir novos trabalhos longos, em vez de matar os atuais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S016, C-S026.

Recursos exclusivos
Duas tarefas de alta prioridade podem disputar o mesmo repositório ou chave de projeto. Respeite exclusão antes de ordenar elegíveis. Acelerar um consumidor bloqueado não ajuda se o produtor de sua dependência ficou sem recurso; transfira urgência apenas ao trecho necessário para liberá-lo e mantenha limite de justiça.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, C-S025.

USO AVANÇADO — Chamadas interativas e lote
Cenário: GPU serve respostas ao usuário e processamento de acervo.
Estratégia: Reserve capacidade interativa e permita empréstimo ao lote quando ociosa. Preempção só ocorre nos pontos suportados pelo servidor; caso contrário, limite duração do lote admitido. Meça desperdício de KV e trabalho reiniciado ao comparar políticas.
Papel do modelo pequeno: 3–7B pode atender a classe interativa estreita; 15–30B processa lote com reserva definida.
Aceite proposto: Proposta: cumprir latência por classe mantendo progresso mínimo do lote.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S023, V3C-S016.

USO AVANÇADO — Integração de alterações urgentes
Cenário: Correção bloqueadora precisa entrar em uma campanha de patches.
Estratégia: Determine quais validações e recursos a correção exige. Eleve a prioridade das dependências indispensáveis e pause somente trabalho ainda não publicado em pontos seguros. Não pule testes de contrato para confundir urgência com aceite automático.
Papel do modelo pequeno: 8–14B identifica impacto local; um planejador maior explicita a cadeia bloqueadora.
Aceite proposto: Proposta: menor tempo de integração sem perda de validação ou duplicação de efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Tarefas pequenas permitem limites de serviço mais previsíveis, mas ainda precisam de admissão.
8–14B: Estimativa de impacto e classificação de urgência apoiadas em regras de domínio.
15–30B: Planejamento de dependências urgentes e análise de alternativas quando o recurso está ocupado.
Requisitos de treino/runtime: Escalonador com classes, exclusões, pontos seguros e telemetria de trabalho descartado.
Não aplicar quando: Não interromper efeito remoto como se cancelar o cliente fosse desfazer a operação.

## T174:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: Seleção de trabalho respeita prioridade e restrições de concorrência.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Ordem por dependência e valor orienta campanha, sem demonstrar um scheduler genérico de prioridade.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C023 — Google / Borg
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.
Mecanismo documentado: O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.
Correspondência com esta base: Há políticas de scheduling operacionais, mas o abstract não detalha todos os algoritmos de prioridade.
Transferência proposta para modelo pequeno: Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.
Limite: O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.
Fontes: V4C-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Timestone comprova prioridade e exclusão em produção. Kubernetes fundamenta distinção de preempção; não foi assumido que cada ferramenta de agente suporta suspensão.
Consultas registradas: V4C-Q003, V4C-Q018.

## T174:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T174 → T149 [complements]
Como combinar: Timestone combina prioridade temporal e exclusão para decidir quais mensagens são entregues.
Interface: Deadline, chave de exclusão e estado da fila.
Condição: A tarefa está pronta e seu recurso exclusivo está disponível.
Aceite proposto: Nenhuma admissão simultânea proibida por chave.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S003. Casos: V4C-C005.

2. T174 → T166 [complements]
Como combinar: Reservas e aging limitam o custo da urgência para outras classes.
Interface: Espera acumulada, cota e custo observado.
Condição: Política declara o que significa justiça.
Aceite proposto: Tarefa elegível de baixa prioridade continua recebendo progresso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020, V3C-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não medir apenas tarefas urgentes e ocultar inanição do restante.
- Uma prioridade nova não elimina dependências nem cria memória compatível na GPU.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare políticas com recursos constantes e distribuição de carga igual. Benefício de modelos pequenos na fila depende de custo e qualidade por tarefa, não apenas do número de parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T149, T160, T166

## Fontes primárias associadas

### C-S014 — heapq — Heap queue algorithm

[https://docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estruturas heap permitem filas por prioridade; política de equidade é responsabilidade adicional.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S029 — Operating Systems: Three Easy Pieces — Scheduling: The Multi-Level Feedback Queue

[https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por prioridades precisa tratar inanição; boosts de prioridade são uma estratégia concreta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

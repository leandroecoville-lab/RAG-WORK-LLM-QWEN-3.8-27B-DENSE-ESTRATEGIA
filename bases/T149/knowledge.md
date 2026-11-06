# T149 — Priority Queue

**Nome canônico:** Priority Queue  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T149  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** fila de prioridade

## T149:C01 — conceito

Estrutura que retira itens conforme uma chave de prioridade, normalmente implementada por heap. A fila organiza ordem; não define sozinha a política correta de atendimento. Empates, mudanças de prioridade, cancelamento e equidade precisam ser especificados pela aplicação.

Como funciona:
- Calcular chave que representa prioridade e critério de desempate.
- Inserir item sem depender da ordem de chegada dos resultados.
- Retirar o item admissível mais prioritário para um worker disponível.

## T149:C02 — aplicacao

Quando usar:
- Pedidos com urgência ou prazos distintos.
- Scheduler com vários trabalhos prontos para executar.

Quando não usar:
- Todas as tarefas precisam estritamente da ordem de chegada por dependência de negócio.

Implementação proposta:
- Usar chave como prioridade e contador monotônico de desempate.
- Definir atualização ou invalidação de itens cancelados.
- Combinar com limite de concorrência e prevenção de inanição.

Aplicação LAI proposta:
Proposta: distinguir tarefas interativas e processamento em lote da Helena, sem permitir que relatórios atrasem toda interação.

## T149:C03 — riscos_validacao

Armadilhas:
- Objetos não comparáveis podem quebrar desempates do heap.
- Prioridade alta permanente pode impedir execução de tarefas de baixa prioridade.

Métricas sugeridas:
- Tempo na fila por classe.
- Número de itens expirados, cancelados e nunca atendidos.

Testes propostos:
- Inserir prioridades e empates conhecidos e verificar ordem estável esperada.
- Manter chegada de itens urgentes e observar se a política de equidade atende os antigos.

## T149:C04 — perguntas_proveniencia

Pergunta: Priority queue é scheduler completo?
Resposta: Não. Falta escolher política, capacidade e preempção.

Pergunta: Prioridade deve vir de texto livre do agente?
Resposta: Preferencialmente de campos e regras de negócio verificáveis.

Pergunta: Duas tarefas com prioridade igual saem em FIFO?
Resposta: Somente se o contrato adicionar um desempate por chegada ou usar uma implementação que o garanta.

Pergunta: Por que não mudar a chave dentro do heap?
Resposta: Porque a posição armazenada não é recalculada automaticamente; a estrutura pode deixar de representar a ordenação pretendida.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T149:C05 — mecanismo_avancado

Um heap não mantém ordem estável entre itens com a mesma prioridade sem critério adicional. Uma chave composta, como prioridade e sequência de chegada, resolve desempate sem comparar payloads heterogêneos. Alterar diretamente a prioridade de um item já inserido viola a organização do heap; uma estratégia proposta usa nova versão e marca a entrada anterior como obsoleta. Isso exige limpeza para não acumular itens mortos.

Condição de contorno:
A fila pode ordenar trabalho inviável: disponibilidade de recurso e dependências continuam sendo responsabilidades do escalonador.

Contrato proposto:
- Entradas: Item identificado, prioridade, sequência e versão da prioridade.
- Saídas: Próximo item vigente ou indicação de fila vazia.
- Estado: Heap, mapa de versões e entradas canceladas ou substituídas.
- Invariante: Cada item lógico é retirado no máximo uma vez para sua versão vigente.

Compromissos de projeto:
- Atualização por entradas obsoletas simplifica implementação e pode aumentar memória.
- Desempate por chegada oferece estabilidade, mas não resolve justiça entre clientes de volumes diferentes.

## T149:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir prioridades iguais com payloads não comparáveis, repriorizar um item e cancelar outro; verificar ordem definida e descarte das versões antigas.

Plano de avaliação proposto:
Comparar fila FIFO e prioridade com a mesma carga, incluindo mudanças de prioridade. Medir espera por classe, tamanho físico versus itens vivos e custo de inserção/retirada. Escolher política considerando justiça e necessidade de atualização, além da complexidade algorítmica.

Comparações:
- T174 (complements): O escalonador determina quando e em qual recurso executar o item retirado.
- T166 (complements): Aging pode atualizar prioridade, exigindo uma política consistente de manutenção da estrutura.

Afirmação rastreável:
A PriorityQueue de asyncio retira a menor chave de prioridade primeiro.
Suporte: direct; fontes: V3C-S008
Limite: Estabilidade, atualização e persistência não são garantidas automaticamente por esse comportamento básico.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T149:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou heaps, desempate e atualização de prioridades. Aqui a fila distingue urgência, elegibilidade e custo previsto, evitando que um item prioritário bloqueado impeça trabalho realmente executável.

Elegibilidade antes da ordem
Mantenha dependências e disponibilidade de recurso fora da chave de prioridade. Um item urgente sem artefato de entrada não está pronto. Separar filas de aguardando e elegível evita retirar e reinserir continuamente o mesmo trabalho, reduzindo custo de coordenação e diagnósticos enganosos de saturação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S024.

Deadline não é duração
Ordenar pelo prazo pode ser adequado para urgência, mas duas tarefas com o mesmo prazo podem ter custos muito diferentes. Registre estimativa e margem de término; uma tarefa que já não cabe no prazo precisa de decisão explícita, e não de prioridade infinita que comprometa todas as demais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003.

Particionamento por chave de efeito
Quando vários itens alteram o mesmo recurso, selecione apenas um elegível por chave. Outras chaves podem avançar em paralelo. A exclusão deve sobreviver a falha do worker e distinguir entrega duplicada de uma nova intenção, preservando a ordem relevante para aquele recurso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, C-S026.

USO AVANÇADO — Fila de inferência compartilhada
Cenário: Pedidos curtos interativos convivem com relatórios longos.
Estratégia: Crie classes e estimativas de consumo, mantendo cotas mínimas para trabalho antigo. Antes de iniciar uma geração longa, confira capacidade e deadline; evite interrompê-la se o servidor não consegue recuperar estado de forma útil.
Papel do modelo pequeno: Modelos 3–30B recebem trabalhos admitidos; a fila não delega política de prioridade à LLM.
Aceite proposto: Proposta: medir latência por classe, taxa de conclusão e espera máxima observada em carga mista repetível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S003.

USO AVANÇADO — Aplicação de patches por repositório
Cenário: Vários agentes preparam alterações que podem compartilhar uma base.
Estratégia: Use chave de exclusão para integração, não para toda pesquisa. Revisões e testes independentes podem ocorrer antes; ao liberar integração, confira novamente a base e revalide o patch que ficou esperando.
Papel do modelo pequeno: 8–30B produz candidatos, enquanto código coordena ordem e conflitos.
Aceite proposto: Proposta: introduzir alterações concorrentes e verificar que nenhuma prioridade permite sobrescrever trabalho não incorporado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificação de tipo de trabalho e extração de prazo de campos confiáveis, sem inventar urgência.
8–14B: Proposta: estimar subtarefas e identificar dependências para a fila verificar.
15–30B: Proposta: preparar alternativas de execução quando o prazo original se tornar inviável.
Requisitos de treino/runtime: Exige relógio apropriado, persistência de leases e telemetria de duração; prioridade textual não é mecanismo de autorização.
Não aplicar quando: Não usar uma única ordem global quando diferentes recursos ou efeitos exigem exclusão e capacidade independentes.

## T149:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: Fila de prioridade seleciona mensagens por deadlines.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Timestone oferece caso operacional direto; Borg foi acessado apenas pelo abstract, sem atribuir-lhe algoritmos não verificados.
Consultas registradas: V4C-Q003, V4C-Q018.

## T149:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T149 → T174 [feeds]
Como combinar: Timestone combina seleção por deadline com restrições de trabalho não paralelizável.
Interface: Mensagem, deadline e chave de exclusão.
Condição: O trabalho tem identidade e critério de elegibilidade.
Aceite proposto: Proposta: verificar ordem e ausência de execução concorrente da mesma chave.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S003. Casos: V4C-C005.

2. T149 → T166 [complements]
Como combinar: Aging evita que prioridade fixa esconda espera indefinida.
Interface: Tempo de espera, classe e prioridade efetiva.
Condição: A política define como a espera modifica a ordem.
Aceite proposto: Comparar distribuição de espera por tenant, não somente média global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020, V3C-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não descartar silenciosamente itens que expiraram enquanto aguardavam.
- Impedir que workers criem prioridades novas para suas próprias tentativas sem política comum.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos e rotas sob a mesma política de fila. Melhoria de latência por scheduler não demonstra que o modelo menor resolveu tarefas mais difíceis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T166, T174

## Fontes primárias associadas

### C-S014 — heapq — Heap queue algorithm

[https://docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estruturas heap permitem filas por prioridade; política de equidade é responsabilidade adicional.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S008 — Python asyncio — Queues

[https://docs.python.org/3/library/asyncio-queue.html](https://docs.python.org/3/library/asyncio-queue.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas limitadas bloqueiam put; PriorityQueue usa menor prioridade primeiro; task_done e join acompanham tarefas pendentes.

Limite: API consultada inclui shutdown recente; a versão local não foi presumida e a fila não é persistente por si.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

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

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

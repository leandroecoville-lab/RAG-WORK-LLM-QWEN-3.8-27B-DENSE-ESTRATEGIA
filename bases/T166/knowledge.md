# T166 — Queue Fairness / Aging

**Nome canônico:** Queue Fairness / Aging  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T166  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** equidade de filas; envelhecimento de prioridade

## T166:C01 — conceito

Políticas que distribuem oportunidades de execução e reduzem inanição de itens na fila. Aging aumenta a prioridade efetiva de uma tarefa conforme sua espera. Equidade pode ser por cliente, peso ou tempo; precisa de definição explícita e capacidade suficiente para atender a carga.

Como funciona:
- Medir espera e participação de cada classe ou cliente.
- Ajustar prioridade ou quota para impedir concentração indefinida.
- Escolher o próximo item entre os que respeitam dependências e limites.

## T166:C02 — aplicacao

Quando usar:
- Filas misturam trabalho interativo e em lote.
- Um tenant pode gerar continuamente mais tarefas que os demais.

Quando não usar:
- Prometer tempo máximo de atendimento sem limitar admissão ou reservar capacidade.

Implementação proposta:
- Definir a unidade de justiça: requisições, tempo de GPU ou custo.
- Aplicar aging com teto ou escalonamento justo por pesos.
- Combinar a política com deadlines e descarte de trabalho expirado.

Aplicação LAI proposta:
Proposta: a Helena reservar atendimento a tarefas interativas sem abandonar rotinas antigas de manutenção e análise.

## T166:C03 — riscos_validacao

Armadilhas:
- Igualdade por número de chamadas favorece pedidos muito caros.
- Aging sem cuidado transforma todo item antigo em urgente e perde diferenciação.

Métricas sugeridas:
- Espera por tenant e percentis por classe.
- Participação de recursos versus pesos contratados e incidência de inanição.

Testes propostos:
- Gerar fluxo contínuo de alta prioridade e verificar progresso dos itens antigos.
- Misturar tarefas curtas e longas e observar justiça na unidade escolhida.

## T166:C04 — perguntas_proveniencia

Pergunta: Aging garante estabilidade sob sobrecarga infinita?
Resposta: Não. É necessário controlar admissão ou aumentar capacidade.

Pergunta: Justiça significa atendimento idêntico?
Resposta: Não necessariamente; pesos diferentes podem ser justos se forem explícitos.

Pergunta: Rodízio de requisições garante equidade de custo?
Resposta: Não quando requisições têm tamanhos diferentes; a unidade distribuída precisa representar o recurso escasso.

Pergunta: Aging resolve sobrecarga ilimitada?
Resposta: Não. Ele reorganiza espera; capacidade insuficiente exige reduzir admissão, reagendar ou rejeitar trabalho.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T166:C05 — mecanismo_avancado

Justiça precisa definir a unidade distribuída: número de requisições, tokens, tempo de serviço ou custo. Atender uma chamada de cada cliente pode ser injusto quando os tamanhos diferem muito. Aging combate espera prolongada, mas não mede sozinho a parcela já consumida. Como referência distinta, o EEVDF acompanha lag de CPU e deadline virtual; transportar essa ideia a agentes exige estimar custo de tarefas que podem não ser preemptíveis.

Condição de contorno:
Nenhuma política garante atendimento finito para todas as classes se a carga sustentada excede a capacidade sem admissão ou descarte.

Contrato proposto:
- Entradas: Itens, cliente, custo estimado, peso e tempo de espera.
- Saídas: Ordem de admissão e justificativa de prioridade efetiva.
- Estado: Serviço acumulado por cliente, espera e dívida de atendimento.
- Invariante: A unidade de justiça permanece explícita e comparável entre clientes.

Compromissos de projeto:
- Aging reduz inanição e pode atrasar tarefas urgentes recém-chegadas.
- Cobrança por custo aproxima equidade e depende de estimativas corrigidas após execução.

## T166:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: um cliente envia tarefas longas e outro tarefas curtas; comparar igualdade por contagem com igualdade por serviço, sem interpretar ambas como a mesma justiça.

Plano de avaliação proposto:
Comparar FIFO, prioridade pura e política com aging ou pesos sob carga admissível e saturada. Medir espera por classe, parcela de serviço e rejeições. Escolher o objetivo de justiça antes de ajustar o algoritmo.

Comparações:
- T149 (complements): A fila implementa ordenação; a política define como a prioridade muda.
- T174 (complements): Escalonamento precisa combinar justiça, capacidade e urgência.

Afirmação rastreável:
EEVDF usa lag para representar parcela de CPU devida e seleciona tarefas elegíveis por deadline virtual.
Suporte: direct; fontes: V3C-S020
Limite: Essa referência de CPU não fornece implementação pronta para chamadas remotas longas e não preemptíveis.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T166:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava justiça por custo e aging. A nova camada trata estimativas manipuláveis, trabalho indivisível e efeitos de prioridades herdadas, para que justiça sobreviva à variação de tarefas LLM.

Crédito estimado e cobrança real
Reserve capacidade por custo previsto e ajuste a dívida após observar consumo. Cobrar apenas pelo número de pedidos favorece requisições grandes; cobrar somente a previsão permite subestimar para furar a fila. Mantenha histórico por classe e limite o desvio admitido, sem punir permanentemente um cliente por uma exceção legítima.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S020, V3C-S009.

Tarefas grandes elegíveis
Um trabalho maior que a parcela normal não pode ficar esperando eternamente por crédito impossível. Divida onde o contrato permitir ou ofereça uma classe de lote com acumulação e limite próprios. Aging deve elevar chance de atendimento sem transformar qualquer tarefa antiga em prioridade absoluta contra toda a carga interativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S020, V3C-S021.

Dependência e justiça
Uma tarefa urgente pode depender de outra classe com prioridade baixa. Propagar urgência pela dependência evita bloqueio, mas deve ser limitado ao trabalho necessário. Não permita que qualquer cliente declare uma dependência artificial para elevar toda sua campanha; a relação deve existir no grafo de artefatos e ser verificável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S016, C-S025.

USO AVANÇADO — Inferência compartilhada
Cenário: Extrações rápidas e análises longas competem pela mesma GPU.
Estratégia: Separe classes com reservas mínimas e contabilize tokens ou tempo efetivo. Em picos, preserve uma fração de progresso para lote; quando a carga interativa cai, empreste capacidade ociosa. Registre retomada da reserva para que empréstimo não vire promessa permanente.
Papel do modelo pequeno: 3–7B atende chamadas curtas; 15–30B recebe trabalhos de maior custo com admissão própria.
Aceite proposto: Proposta: medir espera por classe, cauda e custo efetivo, incluindo tarefas que nunca terminaram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S023.

USO AVANÇADO — Revisão de patches
Cenário: Uma campanha grande não deve bloquear correções pequenas de outras equipes.
Estratégia: Agende por projeto e custo de validação, não pelo volume de patches enviados. Use aging para evitar abandono de revisões lentas e reserve prioridade para dependências que bloqueiam integração já em andamento.
Papel do modelo pequeno: 8–14B estima escopo do diff; runtime decide créditos e exceções rastreáveis.
Aceite proposto: Proposta: limitar concentração por projeto sem degradar a integridade dos testes exigidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Trabalhos curtos previsíveis em classes com overhead pequeno.
8–14B: Estimativas de tamanho e agrupamento de tarefas por perfil operacional.
15–30B: Análise de dependências e identificação de divisões que preservem aceitação.
Requisitos de treino/runtime: Medição de custo real, política de empréstimo e proteção contra tarefas acima da capacidade máxima.
Não aplicar quando: Não afirmar justiça apenas porque a fila é FIFO ou porque cada cliente recebeu uma chamada.

## T166:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Borg sustenta admissão e isolamento, mas não prova este aging exato. Timestone documenta prioridade; não foi contado automaticamente como justiça por custo.
Consultas registradas: V4C-Q004, V4C-Q018.

## T166:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T166 → T149 [complements]
Como combinar: Aging altera a chave efetiva da fila segundo espera e classe, sem violar elegibilidade.
Interface: Prioridade base, idade e custo estimado.
Condição: Atualizações de prioridade têm semântica consistente.
Aceite proposto: Tarefa antiga elegível recebe progresso em carga sustentada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T166 → T174 [complements]
Como combinar: O escalonador implementa reservas e herança limitada de urgência.
Interface: Créditos por classe e dependências bloqueadoras.
Condição: Recursos compatíveis e pontos válidos de preempção.
Aceite proposto: Evitar inversão de prioridade sem sacrificar toda a classe de lote.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S016, V4C-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Excluir tarefas incompletas das métricas pode esconder inanição.
- Uma política justa em tokens pode ser injusta em tempo de GPU; declarar a unidade escolhida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare configurações pequenas e de fronteira por distribuição de espera, além da média de throughput. Justiça é propriedade do serviço, não competência emergente de um modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T149, T174

## Fontes primárias associadas

### C-S029 — Operating Systems: Three Easy Pieces — Scheduling: The Multi-Level Feedback Queue

[https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por prioridades precisa tratar inanição; boosts de prioridade são uma estratégia concreta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S021 — RFC 2697 — A Single Rate Three Color Marker

[https://www.rfc-editor.org/rfc/rfc2697.html](https://www.rfc-editor.org/rfc/rfc2697.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Marcador de tráfego com buckets limitados, taxa comprometida e tamanhos de rajada explicitados.

Limite: RFC descreve marcação de pacotes com dois buckets; limitador simples de chamadas é uma adaptação, não essa especificação integral.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

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

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

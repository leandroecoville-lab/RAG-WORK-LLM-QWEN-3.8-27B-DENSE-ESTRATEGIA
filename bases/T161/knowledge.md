# T161 — Critical Path Analysis

**Nome canônico:** Critical Path Analysis  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T161  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** análise do caminho crítico

## T161:C01 — conceito

Análise da sequência de dependências que determina a menor duração possível de um projeto sob as hipóteses do modelo. No caso clássico, é o caminho de maior duração em um DAG. Otimizar tarefas fora desse caminho pode não reduzir a duração final.

Como funciona:
- Anotar durações estimadas e dependências de cada tarefa.
- Calcular início mais cedo a partir do maior término dos predecessores.
- Determinar folgas e reavaliar o caminho crítico quando durações mudarem.

## T161:C02 — aplicacao

Quando usar:
- Pipelines lentos com várias etapas em paralelo.
- Escolha de onde investir esforço para reduzir latência total.

Quando não usar:
- Tratar estimativas sem filas ou recursos compartilhados como previsão garantida do tempo real.

Implementação proposta:
- Medir tempos de execução e espera separadamente.
- Construir caminho crítico com dados observados e cenários de variação.
- Incluir restrições de recursos na análise quando elas dominarem a duração.

Aplicação LAI proposta:
Proposta: medir o caminho entre pedido e entrega da Helena antes de otimizar tokens, ferramentas ou número de subagentes isoladamente.

## T161:C03 — riscos_validacao

Armadilhas:
- A etapa mais cara isoladamente nem sempre está no caminho crítico.
- O caminho pode mudar depois de uma otimização ou durante uma execução.

Métricas sugeridas:
- Duração prevista versus observada do workflow.
- Folga por tarefa e redução final obtida por melhoria localizada.

Testes propostos:
- Usar grafo pequeno com durações conhecidas e conferir cálculo manual.
- Reduzir duração de etapa fora do caminho e verificar se o tempo total realmente muda.

## T161:C04 — perguntas_proveniencia

Pergunta: Caminho crítico é a tarefa mais lenta?
Resposta: Não necessariamente; é uma sequência dependente que limita a conclusão.

Pergunta: Basta somar médias?
Resposta: Não para estimar cauda ou recursos concorrentes; essas hipóteses precisam ser modeladas.

Pergunta: Somar p95 de cada etapa produz o p95 do workflow?
Resposta: Não. Quantis não se somam dessa forma em geral; dependência estatística e paralelismo mudam a distribuição total.

Pergunta: Duplicar trabalhadores reduz o tempo pela metade?
Resposta: Somente se capacidade for o gargalo dominante e o trabalho puder ser distribuído; dependências podem impor o mesmo limite L.

Escopo das fontes:
Metadados do artigo original foram localizados, mas seu texto não foi aberto por bloqueio 403. Definição matemática geral e roteiro de aplicação são exposição editorial; graphlib sustenta apenas a operação com dependências.

## T161:C05 — mecanismo_avancado

Para tarefas indivisíveis com durações estimadas dᵥ, o comprimento L do maior caminho de dependências é um limite inferior do tempo total. Com m trabalhadores idênticos e trabalho total W=Σdᵥ, outro limite é W/m; assim, max(L,W/m) ajuda a separar gargalo de dependência e capacidade. Não é previsão exata: filas, transferência, recursos específicos e variação das durações podem aumentar o tempo observado.

Condição de contorno:
O caminho crítico calculado com médias pode mudar em cada execução quando ferramentas apresentam caudas de latência longas.

Contrato proposto:
- Entradas: DAG, durações estimadas, quantidade de trabalhadores e restrições de recurso.
- Saídas: Caminhos dominantes, folgas e limites inferiores com hipóteses declaradas.
- Estado: Estimativas versionadas e durações observadas por etapa.
- Invariante: Toda conclusão de economia identifica qual dependência ou restrição realmente encurtou o término.

Compromissos de projeto:
- Priorizar o caminho estimado pode reduzir término e atrasar trabalho independente importante.
- Medições detalhadas melhoram estimativas e introduzem custo de instrumentação.

## T161:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: acelerar uma tarefa com folga e depois uma etapa do caminho dominante; verificar que somente a segunda reduz o término sob as hipóteses originais.

Plano de avaliação proposto:
Comparar previsão e execução em grafos com diferentes larguras, controlando trabalhadores. Medir erro de previsão, mudança de caminho dominante e tempo final. Recalcular após otimizações, pois o gargalo pode migrar para outro ramo.

Comparações:
- T160 (complements): O escalonador respeita dependências e pode usar folga ou caminho remanescente como critério.
- T174 (complements): Prioridade pode incorporar caminho crítico sem ignorar justiça e restrições.

Afirmação rastreável:
LLMCompiler separa planejamento de dependências e execução paralela para reduzir serialização de chamadas.
Suporte: related; fontes: V3C-S002
Limite: Os limites L e W/m são modelagem clássica aplicada editorialmente, não resultados experimentais do pacote.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T161:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 fornecia limites inferiores e folgas. A camada nova usa caminho crítico como instrumento de decisão sob caudas, dependências informacionais e custo de transferência, distinguindo previsão de experimento causal.

Caminho por fase e percentil
Instrumente fila, execução, transferência e validação separadamente. O maior caminho das médias não descreve necessariamente a cauda da missão; uma ferramenta rara e lenta pode dominar o percentil alto. Reconstitua caminhos de traces reais e compare a frequência com que cada etapa impede o término, sem somar percentis como se fossem aditivos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S025, V4C-S004.

Valor de antecipar evidência
Algumas tarefas não estão no maior caminho de duração, mas revelam cedo uma condição que invalida o plano inteiro. Um teste barato de compatibilidade pode merecer execução antes de uma etapa longa. Acrescente ao planejamento o valor de evitar trabalho inútil, mantendo essa heurística separada do cálculo clássico de caminho crítico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S009.

Experimento de aceleração
Antes de contratar um modelo maior para uma etapa, estime quanto sua duração pode cair e qual etapa passará a dominar. Faça teste com limite de recursos constante; se a aceleração aumenta fila de outro consumidor, o ganho local pode desaparecer. Registre também o custo da qualidade perdida quando troca por um modelo menor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V4C-S023.

USO AVANÇADO — Campanha de alterações
Cenário: Milhares de pequenos patches precisam de validação compartilhada.
Estratégia: Meça se o gargalo está na geração, na compilação ou na revisão. Se CI domina, mais agentes só aumentam a fila; agrupe validações compatíveis ou reduza candidatos inválidos antes de enviá-los. Recalcule o caminho depois da mudança porque o gargalo pode migrar.
Papel do modelo pequeno: 3–7B filtra erros locais; 15–30B atua somente nas etapas cognitivas dominantes.
Aceite proposto: Proposta: menor duração total e custo por mudança aceita, mantendo a mesma cobertura de testes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S017.

USO AVANÇADO — Pesquisa com fontes lentas
Cenário: Várias consultas convergem em uma síntese única.
Estratégia: Inicie cedo as fontes de maior latência previsível e faça extração independente enquanto chegam outras respostas. Não comece conclusão que dependa da fonte ausente. Se o deadline vencer, produza estado de cobertura incompleta, sem fingir que otimização de agenda eliminou a lacuna.
Papel do modelo pequeno: 8–14B extrai por fonte; integrador recebe resultados progressivamente identificados.
Aceite proposto: Proposta: tempo até cobertura suficiente e impacto das fontes tardias na resposta final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar pré-checagens baratas e reduzir a entrada de etapas caras.
8–14B: Estimar classes de duração a partir de tarefas históricas sem decidir sozinho o SLA.
15–30B: Decompor planos e identificar dependências informacionais que a telemetria não explica.
Requisitos de treino/runtime: Tracing com causalidade, relógios adequados e distinção entre tempo de serviço e espera; modelos estimativos calibrados.
Não aplicar quando: Não otimizar pela duração média de um nó quando a missão é governada por cauda ou requisito de evidência.

## T161:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Borg e Conductor apoiam análise de recursos e coordenação; não foi encontrado caso operacional que valide esta heurística cognitiva exata.
Consultas registradas: V4C-Q003, V4C-Q018.

## T161:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T161 → T174 [feeds]
Como combinar: Entregar folga e etapa bloqueadora ao escalonador, sem permitir que prioridade viole dependência.
Interface: Grafo, estimativas e classes de recurso.
Condição: Tarefas prontas competem pelo mesmo recurso.
Aceite proposto: Reduzir término da missão sem inanição das demais classes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S025, V3C-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T161 → T147 [complements]
Como combinar: Limitar fan-out ao paralelismo que encurta o caminho e não apenas cria mais candidatos aguardando junção.
Interface: Duração por ramo, fila e critério de junção.
Condição: Ramos independentes e capacidade disponível.
Aceite proposto: Comparar largura e custo sob o mesmo conjunto de tarefas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma etapa acelerada com folga pode não reduzir o término.
- Não atribuir ao modelo um ganho produzido por ampliar hardware ou relaxar critério de conclusão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare configurações por prazo até resultado aceito. Um modelo pequeno pode vencer uma etapa curta; a competência para formular o grafo permanece variável independente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T147, T160, T174

## Fontes primárias associadas

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### C-S024 — graphlib — Functionality to operate with graph-like structures

[https://docs.python.org/3/library/graphlib.html](https://docs.python.org/3/library/graphlib.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ordenação topológica identifica tarefas liberadas por dependências e detecta ciclos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

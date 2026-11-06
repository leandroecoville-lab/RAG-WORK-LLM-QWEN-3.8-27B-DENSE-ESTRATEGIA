# T160 — DAG Scheduling

**Nome canônico:** DAG Scheduling  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T160  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento de grafo acíclico

## T160:C01 — conceito

Escalonamento de tarefas descritas por grafo acíclico direcionado de dependências. Uma tarefa só fica pronta quando suas precondições predecessoras são satisfeitas. Ordenação topológica determina o que pode executar, enquanto recursos, prioridades e quotas determinam quando realmente executará.

Como funciona:
- Construir nós de trabalho e arestas de dependência.
- Identificar nós prontos sem predecessores pendentes.
- Executar e liberar sucessores após conclusão válida dos nós anteriores.

## T160:C02 — aplicacao

Quando usar:
- Pipelines com etapas independentes e pontos de junção.
- Auditorias ou processamento em lote com dependências explícitas.

Quando não usar:
- Representar ciclos de agente sem uma camada própria que limite ou desenrole as iterações.

Implementação proposta:
- Validar ausência de ciclos antes de iniciar.
- Separar estados pronto, executando, concluído, falho e bloqueado.
- Definir como falha de um predecessor afeta seus descendentes e ramos independentes.

Aplicação LAI proposta:
Proposta: transformar planos verificáveis da Helena em dependências explícitas, com ramos paralelos apenas quando realmente independentes.

## T160:C03 — riscos_validacao

Armadilhas:
- Marcar chamada iniciada como concluída libera dependentes cedo demais.
- Paralelismo teórico do grafo pode exceder capacidade real de GPU ou API.

Métricas sugeridas:
- Tempo total do pipeline e ociosidade de workers.
- Tarefas bloqueadas e violações de dependência.

Testes propostos:
- Inserir ciclo proposital e exigir detecção antes da execução.
- Fazer predecessor falhar e confirmar que descendente não usa saída inexistente.

## T160:C04 — perguntas_proveniencia

Pergunta: Todo workflow de agente é DAG?
Resposta: Não. Agentes frequentemente têm ciclos; é preciso modelá-los separadamente.

Pergunta: Ordem topológica é ordem ótima de execução?
Resposta: Não. Ela respeita dependências, mas não otimiza recursos ou duração sozinha.

Pergunta: Marcar done significa que a tarefa teve sucesso?
Resposta: Para o ordenador, significa liberação topológica; a aplicação deve decidir se essa transição representa sucesso ou outro estado permitido.

Pergunta: Por que pode haver fila mesmo com vários nós prontos?
Resposta: Porque prontidão trata dependências; CPU, memória, quota e concorrência continuam limitando execução.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T160:C05 — mecanismo_avancado

Prontidão topológica e sucesso operacional são estados diferentes. Em graphlib, done informa ao ordenador que um nó foi processado; a biblioteca não comprova que o artefato exigido por seus sucessores existe. O executor precisa decidir se falha bloqueia descendentes, permite alternativa ou satisfaz uma dependência explicitamente tolerante. Em grafos dinâmicos, adicionar trabalho depois do início também requer uma política que o ordenador estático não oferece automaticamente.

Condição de contorno:
Um DAG sem ciclos pode ficar sem progresso por recursos indisponíveis ou por nós considerados prontos com entradas inválidas.

Contrato proposto:
- Entradas: Nós, predecessores, contratos de saída e recursos exigidos.
- Saídas: Conjunto pronto, tarefas bloqueadas e decisões de admissão.
- Estado: Contadores de dependências, estados de execução e versão do grafo.
- Invariante: Um sucessor só recebe disponibilidade semântica quando suas entradas requeridas estão confirmadas.

Compromissos de projeto:
- Grafo estático facilita validação e limita expansão durante execução.
- Grafo dinâmico adapta descoberta e exige mais controle sobre fechamento e detecção de ciclos.

## T160:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: um predecessor termina com erro e outro produz resultado válido; impedir que a simples finalização de ambos libere um sucessor que exige os dois artefatos.

Plano de avaliação proposto:
Comparar execução sequencial e escalonamento por prontidão, com recursos e durações controlados. Medir espera por dependência, utilização, descendentes executados indevidamente e tempo total. Separar benefício topológico de ganho por aumentar hardware.

Comparações:
- T161 (complements): Caminho crítico ajuda a priorizar entre tarefas prontas, mas não muda dependências.
- T147 (complements): Fan-out e junção podem ser subgrafos com critérios explícitos de completude.

Afirmação rastreável:
graphlib oferece prepare, get_ready e done para coordenar processamento topológico, incluindo detecção de ciclos.
Suporte: direct; fontes: C-S024
Limite: Conclusão funcional de uma tarefa não é verificada pelo ordenador topológico.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T160:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava prontidão topológica e sucesso funcional. Esta camada acrescenta artefatos tipados nas arestas, expansão controlada do grafo e reaproveitamento de resultados após invalidação seletiva.

Arestas carregam contratos
Cada dependência deve declarar qual artefato ou propriedade exige. Terminar análise sintática pode liberar edição local, mas não publicação se ainda faltar teste de integração. Distinga dependências de dados, exclusão de recurso e barreiras de qualidade; representar tudo como uma seta sem tipo dificulta explicar por que o nó está bloqueado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, C-S024.

Expansão com fechamento
Permita que a etapa de descoberta produza novos nós, mas defina quando o conjunto descoberto está fechado. Sem essa barreira, um integrador pode terminar antes de chegar a última subtarefa. Valide IDs estáveis, ausência de ciclos e teto de expansão; revisões posteriores abrem uma nova versão do subgrafo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004.

Invalidação mínima
Associe resultados à versão de suas entradas. Quando um arquivo muda, marque como obsoletos apenas descendentes que realmente dependem dele, desde que os contratos permitam essa análise. Um nó com efeitos já publicados exige compensação ou nova versão, não simples apagamento do estado de conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V4C-S004.

USO AVANÇADO — Refatoração entre pacotes
Cenário: Alterar uma API exige consumidores, testes e documentação coordenados.
Estratégia: Construa nós por mudança verificável e arestas por contrato de interface. Paralelize consumidores independentes após fixar o schema. Só libere integração quando todos os artefatos obrigatórios da mesma revisão estiverem aceitos; resultados antigos não satisfazem uma API nova.
Papel do modelo pequeno: 3–7B corrige chamadas; 8–14B analisa dependências locais; 15–30B propõe o grafo.
Aceite proposto: Proposta: nenhum consumidor publicado contra contrato incompatível e redução da espera evitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S004.

USO AVANÇADO — Relatório com fontes independentes
Cenário: Tópicos podem ser investigados em paralelo, mas conclusões se cruzam.
Estratégia: Produza tabelas de evidências por tópico e adie a síntese comparativa até a barreira de cobertura. Se uma contradição exigir consulta adicional, acrescente um subgrafo de resolução com prazo e critério de encerramento.
Papel do modelo pequeno: 8–14B coleta fatos delimitados; integrador maior reconcilia dependências informacionais.
Aceite proposto: Proposta: detectar conclusão emitida antes da cobertura e medir tempo do caminho efetivo até relatório aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar nós pequenos cujo contrato de saída caiba em schema e exemplos.
8–14B: Validar suficiência de artefatos e sugerir subdivisões de um nó bloqueado.
15–30B: Construir dependências e alternativas, submetidas à validação determinística do grafo.
Requisitos de treino/runtime: Executor deve distinguir pronto, em execução, aceito, falho e obsoleto; versionar entradas por aresta.
Não aplicar quando: Não usar DAG rígido para trabalho com ciclos de feedback sem representar a repetição como estado ou expansão limitada.

## T160:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Blueprint e avaliação coordenam dependências e tarefas elegíveis.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Etapas e gates coordenam dependências da implantação.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Orquestração coordena dependências, embora nem todo workflow seja um DAG estático.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor e UpCD sustentam coordenação operacional; a especialização para tarefas de 3–30B e invalidação por artefatos é proposta.
Consultas registradas: V4C-Q003, V4C-Q012.

## T160:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T160 → T148 [complements]
Como combinar: Conductor coordena tarefas e evolução de workflows; o grafo precisa compartilhar estados operacionais com o executor.
Interface: Versão do workflow, estado das tarefas e dependências.
Condição: A semântica de falha e término está definida no fluxo.
Aceite proposto: Não liberar dependente quando predecessor falhou sem alternativa válida.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S004. Casos: V4C-C006.

2. T160 → T161 [feeds]
Como combinar: Calcular caminho dominante sobre dependências e durações observadas para priorizar trabalho pronto.
Interface: DAG versionado e distribuição de duração por nó.
Condição: Estimativas incluem recursos e filas relevantes.
Aceite proposto: Otimização proposta reduz término, não só duração de nó com folga.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Fechar explicitamente a descoberta antes da junção final.
- Separar reexecução de cálculo da repetição de efeito publicado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare ganhos com os mesmos modelos e recursos antes de atribuí-los ao porte. Um DAG bem definido pode tornar tarefas menores viáveis sem resolver planejamento aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T147, T161

## Fontes primárias associadas

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

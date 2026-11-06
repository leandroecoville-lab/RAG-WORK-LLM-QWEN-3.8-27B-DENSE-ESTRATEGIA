# T146 — Adaptive Compute

**Nome canônico:** Adaptive Compute  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T146  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** computação adaptativa

## T146:C01 — conceito

Alocação variável de recursos de inferência conforme o valor esperado do processamento adicional. Recursos incluem tokens, candidatos, chamadas de ferramentas e modelos mais capazes. É uma família de políticas, não um botão universal capaz de melhorar qualquer tarefa aumentando o orçamento.

Como funciona:
- Estimar valor e custo de ações computacionais candidatas.
- Direcionar orçamento à opção com melhor ganho esperado admissível.
- Reavaliar após novos resultados e encerrar ao atingir o limite ou objetivo.

## T146:C02 — aplicacao

Quando usar:
- Carga com mistura de perguntas triviais e investigações difíceis.
- Operações de alto valor que justificam verificação adicional.

Quando não usar:
- Não existe medida confiável de qualidade nem mecanismo para detectar falta de progresso.

Implementação proposta:
- Definir orçamento total de missão, incluindo subagentes e retries.
- Comparar ações: recuperar fonte, testar código, gerar candidato ou trocar modelo.
- Calibrar política em curvas de qualidade versus custo.

Aplicação LAI proposta:
Proposta: reservar recursos da Helena segundo dificuldade e verificabilidade, tratando GPU, APIs e tempo do usuário como custos distintos.

## T146:C03 — riscos_validacao

Armadilhas:
- Mais tokens podem produzir justificativas maiores para a mesma conclusão errada.
- Custo local invisível, como ocupação de GPU, pode tornar a política ineficiente.

Métricas sugeridas:
- Resultado aceito por unidade de custo ou tempo.
- Distribuição do orçamento entre tarefas e taxa de esgotamento.

Testes propostos:
- Executar políticas alternativas sob orçamento total igual.
- Simular queda do ganho marginal e exigir término ou mudança de estratégia.

## T146:C04 — perguntas_proveniencia

Pergunta: Adaptive Compute é igual a MoE?
Resposta: Não. MoE é arquitetura interna; aqui a política controla recursos da execução.

Pergunta: Deve usar sempre todo orçamento disponível?
Resposta: Não. Encerrar cedo pode ser a melhor decisão quando o objetivo já foi comprovado.

Pergunta: Igualar tokens torna duas políticas comparáveis em latência?
Resposta: Não. Sequencialidade, tamanho do modelo, ferramentas e filas alteram o tempo mesmo com consumo textual semelhante.

Pergunta: Por que cobrar o verificador no orçamento?
Resposta: Porque seleção também consome recursos; omiti-la pode transformar uma aparente economia em custo total maior.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T146:C05 — mecanismo_avancado

Computação adaptativa distribui um vetor de recursos: número de candidatos, tamanho de contexto, chamadas de ferramenta, profundidade e força do modelo. Duas políticas com igual número de tokens podem consumir tempos e custos muito diferentes. Uma formulação operacional compara o benefício esperado da próxima alocação com seu custo marginal, incluindo o verificador que escolherá entre candidatos e os limites de concorrência que podem impedir paralelismo real.

Condição de contorno:
Gerar mais alternativas pouco diversas pode acrescentar custo sem ampliar a chance de encontrar uma solução correta.

Contrato proposto:
- Entradas: Classe de tarefa, recursos disponíveis, qualidade exigida e custos estimados.
- Saídas: Alocação por etapa e justificativa para ampliar ou encerrar processamento.
- Estado: Resultados intermediários, diversidade dos candidatos e consumo observado.
- Invariante: Todos os ramos e verificadores são contabilizados no mesmo objetivo.

Compromissos de projeto:
- Mais largura encontra alternativas e aumenta trabalho de seleção.
- Mais profundidade explora uma trajetória e pode reforçar uma premissa errada.

## T146:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir candidatos quase idênticos enquanto o avaliador os pontua igualmente; a política deve reconhecer baixo ganho informacional antes de ampliar indefinidamente a amostra.

Plano de avaliação proposto:
Comparar largura fixa, profundidade fixa e adaptação em orçamentos equivalentes de custo ou tempo, informando qual unidade foi igualada. Medir sucesso por classe, diversidade útil e custo de avaliação; escolher a alocação pela demanda observada.

Comparações:
- T145 (complements): A profundidade é uma dimensão possível, não o orçamento completo.
- T176 (complements): Planejamento informa antecipadamente onde o recurso pode destravar dependências.

Afirmação rastreável:
A alocação de computação em inferência pode beneficiar-se de adaptação por dificuldade em vez de estratégia uniforme.
Suporte: direct; fontes: V3C-S003
Limite: A fonte apresenta resultados em configuração experimental específica, sem garantir benefício de toda expansão de orçamento.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T146:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 apresentou o vetor de recursos e custo marginal. A camada nova define portfólios de ações concorrentes, diversidade útil e decisão de reduzir trabalho sob restrições de fila e verificação.

Portfólio de ações, não só amostras
Distribua orçamento entre buscar evidência, gerar alternativa e verificar um candidato. Muitas amostras do mesmo prompt podem repetir a mesma suposição errada. Prefira diversidade que altere informação ou método, como um cálculo executável e uma consulta documental, quando ambos respondem à mesma questão de forma comparável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S003, V4C-S009.

Custo de integração
Toda alternativa criada exige comparação e eventual reconciliação. O planejador precisa reservar esse trabalho, especialmente quando usa workers pequenos com saídas heterogêneas. Se o custo de integrar cresce mais rápido que o benefício de novos ramos, reduzir largura pode melhorar tempo até uma resposta realmente aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Adaptação condicionada à capacidade
Escolher mais paralelismo só reduz latência quando existe capacidade de execução. Sob fila saturada, ações adicionais competem com as já iniciadas. Use sinais de espera e utilização para preferir trabalho que destrava dependências, preservando verificações obrigatórias mesmo quando o contexto exploratório for reduzido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S009.

USO AVANÇADO — Escolha entre candidatos de código
Cenário: Há várias correções plausíveis para um defeito delimitado.
Estratégia: Gere poucos candidatos com hipóteses distintas e rode testes relevantes em ambiente separado. Amplie o conjunto apenas se nenhuma alternativa passou e houver uma nova hipótese. Evite decidir por eloquência ou pelo número de agentes concordando.
Papel do modelo pequeno: 8–14B gera correções locais; 15–30B compara evidências de integração.
Aceite proposto: Proposta: medir aceitação, regressões e custo total dos candidatos descartados contra um único candidato de fronteira.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S007, V4C-S009.

USO AVANÇADO — Pesquisa com orçamento variável
Cenário: Uma consulta exige mais cobertura quando há fontes conflitantes.
Estratégia: Faça uma busca inicial curta, estime lacunas por critério e distribua workers apenas para aspectos ainda descobertos. Reuse evidências já coletadas por identidade de documento; se a latência estiver comprometida, entregue cobertura parcial explicitamente permitida.
Papel do modelo pequeno: 3–7B extrai por fonte; 15–30B prioriza quais lacunas ainda podem mudar a conclusão.
Aceite proposto: Proposta: comparar cobertura, sustentação e custo por resposta aceita, preservando casos abandonados nas métricas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: especialistas baratos em tarefas fechadas, com poucas alternativas por chamada.
8–14B: Proposta: explorar hipóteses locais diferentes e produzir artefatos diretamente verificáveis.
15–30B: Proposta: alocar e integrar esforço em problemas delimitados, sem assumir orçamento ilimitado.
Requisitos de treino/runtime: Medir custo de verificação e integração, filas e memória; parâmetros não substituem profiling do hardware e do servidor.
Não aplicar quando: Não escalar quantidade de amostras quando faltam diversidade ou um verificador capaz de distingui-las.

## T146:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Reduzir trabalho em busca é analogia para adaptar esforço de inferência.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: Orçamento de reasoning controla uma dimensão de computação, não alocação geral.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes cobrem budgets e coordenação; a política de portfólio é proposta, não uma implantação demonstrada com todas as bandas.
Consultas registradas: V4C-Q004, V4C-Q014, V4C-Q009.

## T146:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T146 → T147 [complements]
Como combinar: Fan-out materializa apenas os ramos cujo benefício esperado justifica integração.
Interface: Lista de hipóteses, orçamento por ramo e condição de junção.
Condição: As saídas podem ser comparadas no mesmo critério.
Aceite proposto: Medir duplicação semântica e utilidade marginal dos ramos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T146 → T174 [complements]
Como combinar: Prioridade favorece ações que liberam caminho crítico sem bloquear tarefas antigas indefinidamente.
Interface: Custo estimado, dependências e deadline.
Condição: Há recursos disponíveis ou política de preempção definida.
Aceite proposto: Reproduzir carga mista e medir espera por classe e conclusão correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar que geração de candidatos consuma a reserva destinada à verificação.
- Não transferir uma vitória em benchmark sintético para todo tipo de tarefa sem estratificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fronteiras de qualidade, custo e latência em cargas equivalentes. Combinações de modelos pequenos podem vencer em nichos verificáveis, mantendo limites em conhecimento e planejamento aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T145, T184, T201

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S003 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Efetividade de estratégias de computação em inferência varia com dificuldade; alocação adaptativa pode superar orçamento uniforme no estudo.

Limite: Experimentos não validam política universal para agentes, ferramentas ou cargas LAI.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T224 — Spec-Driven Loop

**Nome canônico:** Spec-Driven Loop  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T224  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** spec driven development loop; ciclo orientado por especificação

## T224:C01 — conceito

Ciclo que conecta especificação, plano de implementação, tarefas, alterações e evidências de aceitação. A especificação torna explícito o resultado esperado e permite avaliar mudanças sem depender da memória da conversa. Spec Kit é uma referência de organização desse fluxo; o padrão pode ser aplicado sem adotar uma ferramenta específica.

Como funciona:
- Requisitos identificados originam tarefas e critérios de aceitação rastreáveis.
- A implementação produz artefatos e evidências vinculados à versão da especificação.
- Divergências entre requisito, código e teste retornam ao planejamento ou à revisão da especificação.

## T224:C02 — aplicacao

Quando usar:
- Funcionalidades com múltiplos módulos, integração entre agentes e requisitos que precisam sobreviver a várias sessões.

Quando não usar:
- Produzir documentação extensa para mudanças triviais ou tratar toda decisão inicial como imutável mesmo diante de nova evidência.

Implementação proposta:
- Proposta: escrever objetivo, comportamento observável, restrições e exclusões relevantes em linguagem verificável.
- Atribuir identificadores aos critérios e decompor o trabalho em tarefas com entradas, saída e evidência de conclusão.
- Manter decisões de projeto e hipóteses separadas dos requisitos confirmados.
- Quando o pedido mudar, versionar a especificação e identificar tarefas e testes afetados.
- Conferir rastreabilidade entre resultado solicitado, alteração entregue e verificação realmente executada antes de encerrar.

Aplicação LAI proposta:
Proposta LAI: manter especificações curtas e versionadas por missão, permitindo que planejador e executores compartilhem critérios estáveis e revisem mudanças de escopo de forma rastreável.

## T224:C03 — riscos_validacao

Armadilhas:
- Especificações podem ser ambíguas ou inconsistentes.
- Um teste que replica a mesma interpretação errada não resolve a ambiguidade.
- Burocracia excessiva reduz velocidade sem aumentar confiança.

Métricas sugeridas:
- Critérios cobertos por evidência; mudanças sem requisito associado; divergências abertas; retrabalho por ambiguidade; tempo de revisão.

Testes propostos:
- Introduzir uma mudança de requisito e verificar identificação dos módulos e testes afetados.
- Selecionar um critério ao acaso e percorrer tarefa, alteração e resultado de verificação.
- Testar uma especificação contraditória e exigir resolução explícita antes da implementação correspondente.

## T224:C04 — perguntas_proveniencia

Pergunta: A especificação precisa determinar cada linha de código?
Resposta: Não. Ela deve definir comportamento, restrições e critérios suficientes; detalhes de implementação podem permanecer no plano e evoluir.

Pergunta: Como lidar com uma descoberta que invalida o plano?
Resposta: Registrar a evidência, revisar a decisão afetada e atualizar tarefas e testes. Não declarar o requisito cumprido apenas porque o plano anterior terminou.

Pergunta: Uma tarefa concluída no plano prova requisito satisfeito?
Resposta: Somente se sua saída cumprir o critério e a evidência estiver vinculada à versão vigente do requisito.

Pergunta: O que fazer quando a implementação revela premissa falsa?
Resposta: Revisar a especificação com a decisão correspondente e propagar o impacto, em vez de ocultar a divergência no código.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T224:C05 — mecanismo_avancado

Uma especificação operacional liga requisito, decisão de projeto, tarefa e evidência de aceitação. Quando o requisito muda, essa ligação permite localizar os artefatos afetados; sem ela, o plano pode continuar executando uma versão antiga. Spec Kit fornece processos e templates, mas preencher documentos não comprova convergência. A proposta trata ambiguidades como questões explícitas e preserva a origem das decisões que as resolveram.

Condição de contorno:
Uma especificação extensa, porém contraditória ou desatualizada, pode produzir execução consistente com o documento e incompatível com a intenção vigente.

Contrato proposto:
- Entradas: Objetivo, requisitos identificados, restrições e decisões autorizadas.
- Saídas: Plano, tarefas e matriz de evidências por requisito.
- Estado: Versões da especificação, decisões e vínculos com alterações.
- Invariante: Critério alterado invalida ou reavalia evidências produzidas sob a versão anterior.

Compromissos de projeto:
- Rastreabilidade reduz interpretação implícita e aumenta manutenção documental.
- Especificação muito prescritiva restringe soluções melhores descobertas durante a implementação.

## T224:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar um requisito após testes aprovados e antes da entrega; exigir identificação dos testes e artefatos que precisam ser reavaliados.

Plano de avaliação proposto:
Comparar execução por prompt amplo e por especificação rastreável em tarefas equivalentes. Medir ambiguidades tardias, retrabalho e requisitos sem evidência. Avaliar documento e produto separadamente; quantidade de arquivos não é métrica de completude.

Comparações:
- T217 (complements): Testes materializam parte dos critérios de aceitação da especificação.
- T213 (complements): Micro-missões precisam de vínculo com resultados exigidos, evitando fragmentação sem finalidade.

Afirmação rastreável:
Spec Kit oferece processos estruturados, templates e resultados documentados para agentes de programação.
Suporte: direct; fontes: V2A-S023
Limite: O repositório é uma ferramenta de organização; a qualidade da especificação e das evidências depende da aplicação.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T224:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 conectava requisito, tarefa e evidência. A expansão transforma essa rastreabilidade em mecanismo de mudança controlada, com especificação mínima suficiente e resolução explícita de ambiguidades.

Especificação executável onde possível
Separe intenção de detalhes escolhidos pelo implementador. Converta requisitos objetivos em exemplos, invariantes ou contratos verificáveis. Texto que apenas descreve a solução favorita do agente não serve como critério independente de aceite. Quando a propriedade é subjetiva, declare avaliador e exemplos de fronteira em vez de simular precisão matemática.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V4C-S030.

Mudança de requisito
Ao revisar a especificação, identifique decisões, patches e testes afetados. Preserve a versão anterior para explicar resultados já obtidos, mas impeça publicar um candidato que só satisfaz o contrato antigo. Uma alteração aparentemente pequena de comportamento pode invalidar muitos consumidores; a rastreabilidade torna esse alcance visível antes de continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S034.

Granularidade útil
Uma especificação deve permitir começar trabalho verificável sem tentar prever cada linha. Requisitos grandes demais deixam o agente preencher lacunas; excesso de detalhe cria custo de manutenção e congela decisões que deveriam ser locais. Use contratos de fronteira e exemplos para permitir autonomia dentro das restrições, com questões abertas explicitamente listadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S002.

USO AVANÇADO — Feature entregue por modelos pequenos
Cenário: Uma funcionalidade possui entradas, saída e regras claras.
Estratégia: Defina casos de aceite antes de distribuir micro-missões. Gere implementação por módulo e mantenha uma matriz de requisito para teste e artefato. Se o agente encontra ambiguidade que muda comportamento, interrompa essa parte e obtenha decisão; não trate palpite como requisito aprovado.
Papel do modelo pequeno: 3–7B implementa unidades; 8–14B cria candidatos de teste; 15–30B verifica coerência do contrato.
Aceite proposto: Proposta: todos os requisitos obrigatórios têm evidência na versão final e nenhum teste contradiz a intenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S034.

USO AVANÇADO — Refatoração com comportamento preservado
Cenário: A arquitetura muda, mas o contrato externo deve permanecer.
Estratégia: Especifique propriedades que não podem mudar e variações permitidas. Use comparação de comportamento, testes existentes e invariantes estruturais. Se o teste depende de implementação antiga sem necessidade de domínio, revise-o com justificativa, mantendo evidência independente da compatibilidade externa.
Papel do modelo pequeno: 8–14B altera módulos; 15–30B analisa efeitos de fronteira.
Aceite proposto: Proposta: preservação dos contratos externos e redução mensurada da complexidade definida pelo projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Implementação de contratos pequenos e bem exemplificados, sem interpretação extensa de linguagem vaga.
8–14B: Transformação de requisitos em candidatos de teste e identificação de inconsistências locais.
15–30B: Revisão de escopo e dependências entre requisitos, preservando origem das decisões.
Requisitos de treino/runtime: Especificação versionada, matriz de rastreabilidade e avaliação independente de implementação.
Não aplicar quando: Não considerar documento preenchido ou número de páginas como evidência de qualidade da especificação.

## T224:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Verificações expressam critérios de engenharia, sem afirmar um processo integral spec-driven.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Harness Codex oferece invariantes e planos operacionais; não foi tomado como prova de adoção específica do Spec Kit nem de um método universal com este nome.
Consultas registradas: V4C-Q007, V4C-Q027.

## T224:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T224 → T213 [feeds]
Como combinar: Dividir requisitos em micro-missões com saídas e testes ligados à mesma versão de especificação.
Interface: ID do requisito, contrato e critério de aceite.
Condição: Dependências entre requisitos estão explícitas.
Aceite proposto: Integração não deixa requisito sem dono ou sem prova.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T224 → T217 [complements]
Como combinar: Testes de comportamento materializam parte do contrato e orientam ciclos de reparo.
Interface: Exemplo esperado, teste executável e revisão do candidato.
Condição: O teste falha pela propriedade correta.
Aceite proposto: Não ajustar requisito para justificar implementação que falhou.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Spec desatualizada pode produzir software coerente com o documento e errado para a intenção atual.
- Gerador e avaliador precisam consultar a origem do requisito, não apenas suas interpretações recíprocas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare entrega de requisitos delimitados com o mesmo conjunto de testes e revisão. Uma arquitetura rigorosa pode ampliar utilidade de 3–30B sem provar que compreendem requisitos inéditos como modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T208, T213, T217, T221

## Fontes primárias associadas

### V2A-S023 — Spec Kit

[https://github.com/github/spec-kit](https://github.com/github/spec-kit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo de especificação, plano, tarefas, implementação e convergência; exemplo concreto de desenvolvimento guiado por especificações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

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

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

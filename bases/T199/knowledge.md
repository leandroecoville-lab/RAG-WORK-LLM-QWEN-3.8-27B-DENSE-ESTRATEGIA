# T199 — Aprendizagem por avaliação

**Nome canônico:** Aprendizagem por Avaliação  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T199  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** evaluation-driven improvement; Aprendizagem por Avaliação

## T199:C01 — conceito

Rótulo geral para melhoria orientada por resultados de avaliações. O feedback pode alterar prompt, recuperação, memória procedural, política de roteamento ou pesos, dependendo do mecanismo implementado. Rodar um teste e guardar seu resultado não significa que o agente mudou seu comportamento.

Como funciona:
- Executar tarefas com critério de sucesso observável.
- Classificar falhas e escolher intervenção específica.
- Aplicar mudança versionada e avaliar novamente em casos separados.

Nota de nomenclatura: Rótulo editorial amplo; o mecanismo de aprendizagem precisa ser declarado em cada implementação.

## T199:C02 — aplicacao

Quando usar:
- Erros recorrentes têm diagnóstico e intervenção possíveis.
- Existe histórico de tarefas com resultados verificáveis.

Quando não usar:
- Avaliar no mesmo conjunto repetidamente e chamar memorização de melhoria geral.

Implementação proposta:
- Manter conjunto de desenvolvimento e teste reservado.
- Associar cada mudança a hipótese, métrica e evidência de efeito.
- Impedir promoção automática de memória inferida para fato comprovado.

Aplicação LAI proposta:
Proposta: usar episódios auditáveis da Helena para melhorar procedimentos e depois decidir, com métricas, se algum deles deve alimentar fine-tuning.

## T199:C03 — riscos_validacao

Armadilhas:
- Feedback incorreto pode consolidar um comportamento pior.
- Ajustar várias partes ao mesmo tempo impede identificar a causa do ganho.

Métricas sugeridas:
- Ganho em tarefas novas por intervenção.
- Regressões, repetição de erros e custo do ciclo de melhoria.

Testes propostos:
- Comparar versão nova e anterior em amostra temporal não usada na correção.
- Injetar feedback errado e verificar revisão ou quarentena antes da promoção.

## T199:C04 — perguntas_proveniencia

Pergunta: É sinônimo de reinforcement learning?
Resposta: Não. Pode haver melhoria sem gradiente, como memória e revisão de procedimento.

Pergunta: Avaliar sozinho faz aprender?
Resposta: Não. É preciso uma alteração concreta e provar seu efeito posterior.

Pergunta: Salvar resultados já é aprender?
Resposta: É registrar evidência; falta uma regra que altere comportamento persistente e uma avaliação dessa alteração.

Pergunta: Por que separar validação e teste final?
Resposta: Escolher repetidamente com a validação adapta decisões a ela; uma reserva independente estima melhor o desempenho após essa seleção.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T199:C05 — mecanismo_avancado

O ciclo de avaliação só produz aprendizagem quando modifica um componente persistente identificável: prompt, exemplos, roteador, recuperação, procedimento ou pesos. Otimizar repetidamente contra a mesma suíte transforma essa suíte em dado de desenvolvimento. O conjunto final precisa permanecer separado, inclusive de decisões manuais sobre quais mudanças manter. Uma métrica proxy pode ser explorada por respostas que aparentam sucesso sem cumprir a tarefa.

Condição de contorno:
Melhora no conjunto consultado a cada tentativa pode representar adaptação ao teste, sem generalização para novas tarefas.

Contrato proposto:
- Entradas: Casos de desenvolvimento, métrica, componente editável, orçamento e avaliação final reservada.
- Saídas: Nova versão do componente com diferenças e evidência independente.
- Estado: Histórico de experimentos, dados vistos e critérios de seleção.
- Invariante: Toda alegação de melhoria aponta para a alteração concreta que será reutilizada em execuções futuras.

Compromissos de projeto:
- Mais buscas de configuração ampliam oportunidades e risco de sobreajuste.
- Métricas baratas aceleram iteração e podem perder aspectos relevantes do objetivo.

## T199:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar um atalho que reconhece exemplos de desenvolvimento sem resolver variantes novas. Esperar ganho local e reprovação na avaliação independente, expondo o sobreajuste.

Plano de avaliação proposto:
Plano proposto: comparar versão inicial e selecionada em casos inéditos agrupados por origem. Medir qualidade, custo e regressões; reportar número de tentativas e mudanças avaliadas, aceitando ganhos somente fora do processo de seleção.

Comparações:
- T177 (distinct_from): A melhoria pode otimizar prompts ou exemplos sem atualizar pesos; fine-tuning é somente um mecanismo possível.

Afirmação rastreável:
DSPy descreve módulos parametrizados e otimização de pipelines para uma métrica especificada.
Suporte: direct; fontes: C-S020
Limite: A métrica escolhida não garante representar integralmente o objetivo de negócio ou correção factual.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T199:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu alteração persistente e teste reservado. Esta camada organiza o ciclo como experimentação causal, com seleção de falhas, prevenção de regressão e controle da dívida criada por ajustes sucessivos.

Uma mudança identificável
Associe cada hipótese a um componente: prompt, exemplo, índice, roteador, procedimento ou pesos. Registre diferença e critério esperado antes de testar. Alterar vários componentes simultaneamente pode melhorar a métrica sem explicar causa, dificultando manutenção e reversão quando a distribuição muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

Falhas representativas
Priorize erros por impacto e frequência, mas inclua classes raras relevantes. Transformar cada falha observada num exemplo quase idêntico pode produzir memorização de incidentes. Gere variações legítimas e teste em novas origens; preserve uma lista de problemas ainda não resolvidos em vez de remover casos difíceis da suíte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

Aprender não é só filtrar
Executar testes e rejeitar candidatos melhora a saída daquela execução; aprendizagem exige reutilizar uma mudança depois. AlphaEvolve mantém uma busca com avaliações e histórico, enquanto testes industriais podem apenas selecionar propostas. Descreva exatamente qual estado persiste antes de chamar o sistema de autoaperfeiçoamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

USO AVANÇADO — Melhorar extração recorrente
Cenário: Uma versão erra categorias específicas de documento.
Estratégia: Agrupe falhas, escolha uma intervenção pequena e compare com controle. Atualize exemplos ou recuperação quando a causa estiver neles, evitando fine-tuning automático para todo erro.
Papel do modelo pequeno: Um 3–7B pode ganhar utilidade especializada por melhoria do sistema ao redor dele.
Aceite proposto: Avaliar casos novos, regressões e custo por resultado correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

USO AVANÇADO — Evoluir procedimento de agente
Cenário: Execuções mostram uma sequência de ações desnecessária.
Estratégia: Crie uma nova skill ou política, valide pré-condições e compare em replay ou ambiente de teste. Promova somente a versão que mantém resultados e reduz custo observado.
Papel do modelo pequeno: Um 8–14B pode executar o procedimento melhorado sem precisar atualizar pesos.
Aceite proposto: Comprovar alteração persistente e ganho em tarefas fora das trajetórias usadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Melhorias de dados, ferramentas e contratos podem superar mudanças de pesos no início.
8–14B: Use um histórico de experimentos para evitar ciclos de correções contraditórias.
15–30B: Em 15–30B, custo de treino torna diagnóstico causal ainda mais importante.
Requisitos de treino/runtime: Pode modificar runtime, conteúdo ou pesos; declare qual componente mudou e como foi promovido.
Não aplicar quando: Não contar avaliação repetida como aprendizagem nem usar o teste final como guia contínuo de desenvolvimento.

## T199:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T199:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T199 → T177 [feeds]
Como combinar: Falhas verificadas podem alimentar um próximo ajuste quando a causa é comportamento aprendível.
Interface: Exemplos revisados e categoria de erro.
Condição: Separação entre dados de desenvolvimento e avaliação.
Aceite proposto: Medir generalização após o ajuste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S020, V4B-S022, V4B-S023, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T199 → T204 [feeds]
Como combinar: Procedimentos bem-sucedidos podem ser consolidados em skills versionadas.
Interface: Pré-condições, passos e evidência de resultado.
Condição: Generalização preserva parâmetros variáveis.
Aceite proposto: Reexecutar em situações novas e manter rollback.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S020, V4B-S022, V4B-S023, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não remover casos difíceis para melhorar o número agregado.
- Registrar mudanças rejeitadas e seus efeitos, evitando redescobrir regressões.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare versões da aplicação e um baseline de fronteira em tarefas novas. Um ciclo de melhoria pode reduzir lacunas específicas, sem estabelecer crescimento ilimitado ou inteligência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T071, T177, T190

## Fontes primárias associadas

### C-S051 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback verbal e memória episódica podem melhorar tentativas posteriores sem atualizar pesos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S020 — DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines

[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Otimização de pipelines de chamadas de LLM com objetivo mensurável.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

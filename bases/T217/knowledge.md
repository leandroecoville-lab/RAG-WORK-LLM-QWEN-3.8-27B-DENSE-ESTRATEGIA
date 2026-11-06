# T217 — Test-Driven Loop

**Nome canônico:** Test-Driven Loop  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T217  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** test driven development loop; ciclo orientado por testes

## T217:C01 — conceito

Ciclo de desenvolvimento no qual um comportamento esperado é expresso em teste, uma alteração busca satisfazê-lo e a verificação orienta o passo seguinte. Em agentes, esse ciclo precisa preservar a independência do critério de aceitação: mudar o teste para acomodar um defeito não comprova solução.

Como funciona:
- O teste oferece um observável para uma hipótese de comportamento.
- A falha inicial precisa decorrer do problema relevante, e não de ambiente quebrado ou dependência ausente.
- Depois da alteração, o resultado é comparado ao teste anterior e aos contratos afetados.

## T217:C02 — aplicacao

Quando usar:
- Correções reproduzíveis, regras de domínio, regressões e alterações com entradas e saídas verificáveis.

Quando não usar:
- Criar testes que apenas repetem a implementação, ou exigir testes novos para toda edição documental de baixo impacto.

Implementação proposta:
- Proposta: registrar o cenário, a expectativa e a razão pela qual ele representa o pedido.
- Executar a reprodução em ambiente adequado e preservar a mensagem de falha relevante.
- Fazer a menor mudança coerente, verificar o cenário e acrescentar regressões relacionadas quando houver risco concreto.
- Revisar mudanças nos próprios testes separadamente; documentar testes não executados e dependências indisponíveis.
- Encerrar quando os critérios acordados e a verificação proporcional estiverem atendidos.

Aplicação LAI proposta:
Proposta LAI: associar cada micro-missão a evidências proporcionais ao risco, com teste de regressão quando existir um comportamento verificável a proteger.

## T217:C03 — riscos_validacao

Armadilhas:
- Cobertura alta pode coexistir com asserções fracas.
- Testes instáveis produzem feedback enganoso.
- Um teste aprovado não demonstra propriedades que ele não observa.

Métricas sugeridas:
- Regressões detectadas; estabilidade do cenário; cobertura dos critérios; tempo até diagnóstico; falhas ainda sem explicação.

Testes propostos:
- Injetar uma versão defeituosa conhecida e confirmar que o teste a rejeita.
- Alterar somente a mensagem de saída para verificar se a asserção mede o comportamento essencial.
- Repetir casos instáveis antes de atribuir causalidade à correção.

## T217:C04 — perguntas_proveniencia

Pergunta: Todo ciclo precisa começar escrevendo um teste novo?
Resposta: Não. Uma reprodução existente ou teste de contrato pode servir. A escolha depende do problema e do valor real da nova verificação.

Pergunta: O agente pode corrigir o teste?
Resposta: Pode, se a expectativa estava errada e houver justificativa ligada ao requisito. Alterar a expectativa exige revisão, não deve ocultar uma falha do produto.

Pergunta: Um teste verde recém-criado prova que corrigi o defeito?
Resposta: Não sozinho. É útil demonstrar falha na versão anterior pelo motivo esperado e sucesso após a alteração, com execução real do caso.

Pergunta: Por que testar sequências?
Resposta: Porque criação, atualização e remoção podem interagir; cada operação isolada pode funcionar enquanto a sequência viola um invariante.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T217:C05 — mecanismo_avancado

O ciclo orientado por teste precisa distinguir regressão do produto e falha da infraestrutura de teste. Uma execução verde pode significar que nenhum caso foi descoberto, e uma vermelha pode decorrer de dependência indisponível. Além de exemplos, invariantes e sequências de ações ajudam revelar defeitos de estado que não aparecem em uma chamada isolada. O teste escolhido deve falhar pelo comportamento ausente, não por um detalhe incidental da implementação.

Condição de contorno:
Se produtor e verificador compartilham a mesma interpretação incorreta do requisito, o ciclo pode convergir para uma implementação errada com testes verdes.

Contrato proposto:
- Entradas: Requisito, caso que o exercita, ambiente identificado e alteração candidata.
- Saídas: Resultado por teste, motivo da falha e evidência de cobertura do comportamento.
- Estado: Versão dos testes, casos executados e baseline anterior.
- Invariante: Ausência de testes executados não é registrada como comprovação de correção.

Compromissos de projeto:
- Exemplos específicos são fáceis de explicar e podem cobrir pouco espaço de estados.
- Testes gerativos exploram mais sequências e exigem invariantes e modelos de referência corretos.

## T217:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar a descoberta para executar zero casos e introduzir uma falha de estado após duas operações; exigir detecção da ausência e cobertura da sequência.

Plano de avaliação proposto:
Comparar exemplos isolados e testes baseados em propriedades com defeitos introduzidos independentemente. Controlar orçamento de execução. Medir defeitos detectados, falsos alarmes e tempo de diagnóstico, sem usar apenas porcentagem de testes aprovados.

Comparações:
- T195 (complements): Verificação por execução é o mecanismo de evidência usado pelo ciclo.
- T224 (complements): A especificação fornece o comportamento que os testes devem representar.

Afirmação rastreável:
Hypothesis pode gerar sequências de ações em máquinas de estado e compará-las com um modelo de referência.
Suporte: direct; fontes: V3C-S032
Limite: A ferramenta explora o modelo fornecido; não valida automaticamente se o oráculo corresponde ao requisito real.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T217:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia testes vazios, infraestrutura e regressão. A camada nova define independência do requisito, progressão dos verificadores e política de reparo que impede adaptar a prova para aceitar uma implementação inadequada.

Falha que representa o requisito
Antes do reparo, reproduza o comportamento esperado e confirme que o teste falha pela razão relevante. Um teste recém-gerado pode falhar por import ou fixture, sem demonstrar o defeito do produto. Preserve a relação entre requisito e observação; só então use a falha como direção de mudança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S007.

Ciclo com permissões de reparo
Separe mudanças permitidas no produto, nos testes e no ambiente. Um agente encarregado de corrigir teste quebrado por mudança legítima não deve reverter o produto para satisfazer expectativa antiga. Já um reparador do produto não pode apagar asserções para obter verde. Encaminhe a falha ao papel adequado com justificativa verificável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

Pirâmide de evidência
Use verificações baratas antes das caras: parsing e contrato local, teste que reproduz, regressões relacionadas e integração necessária. Verde em uma etapa não substitui as seguintes. Se a alteração muda uma dependência, invalide resultados afetados e rerode sobre a revisão final, sem reaproveitar aprovação de bytes anteriores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S010.

USO AVANÇADO — Reparo por modelo pequeno
Cenário: Defeito localizado possui teste reproduzível e domínio conhecido.
Estratégia: Fixe o teste de comportamento, produza patch mínimo e execute verificação focada. Após passar, rode regressões relevantes e revise efeitos fora de escopo. Se repetir o mesmo erro, interrompa para diagnóstico em vez de aumentar indefinidamente o número de tentativas.
Papel do modelo pequeno: 3–7B propõe alteração local; 8–14B interpreta falhas; 15–30B trata hipótese mais ampla.
Aceite proposto: Proposta: solucionar o defeito sem apagar prova e sem introduzir regressões detectáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S007, V4C-S009.

USO AVANÇADO — Remoção automatizada de código
Cenário: Limpeza gera falhas em testes ou infraestrutura.
Estratégia: Classifique a causa e use reparadores restritos ao escopo correto. Depois de CI verde, execute verificações de propriedade e revisão de intenção. Uma aprovação de LLM não é prova formal de equivalência; mantenha limites e revisão adequada ao risco da mudança.
Papel do modelo pequeno: 8–14B faz diagnóstico e correção delimitada; ferramentas determinísticas executam transformações.
Aceite proposto: Proposta: rejeitar patches com alteração de semântica fora do escopo, mesmo quando CI passa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reparos pequenos guiados por teste externo, com linguagem e formato treinados.
8–14B: Diagnóstico entre código, fixture e ambiente, usando erros estruturados.
15–30B: Revisão de efeitos entre módulos e escolha de testes adicionais; não substituir execução por opinião.
Requisitos de treino/runtime: Ambiente reproduzível, contagem de testes executados, restrições de edição e revisão final imutável.
Não aplicar quando: Não aceitar testes que só repetem a implementação nem gerar evidência de sucesso sem execução real.

## T217:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Candidatos são avaliados e iterados com compilação e testes.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Atualizações do diff são reavaliadas por CI até sucesso ou limite de tentativas.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: A fonte descreve testes e builds na transformação Java; não demonstra explicitamente o ciclo orientado por falha exigido nesta ficha.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: Correções e refatorações concretas, sem protocolo genérico de patch comprovado.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: O sistema modifica programas com avaliação; não demonstra todos os mecanismos de aplicação de patch.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Geração de testes é parte da engenharia de código, não prova qualquer mecanismo de patch.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Ampliação de suíte se relaciona a engenharia de código com escopo específico.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Há ciclos de implementação e testes, mas não fica provado test-first para todas as alterações.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean e SapFix descrevem loops concretos de correção e validação. Testes genéricos de outros relatos foram mantidos como família, sem assumir test-first universal.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q012.

## T217:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T217 → T232 [complements]
Como combinar: AutoClean combina transformação AST com CI e reparadores especializados em falhas.
Interface: Patch estrutural, resultado de build e classe de diagnóstico.
Condição: Reparador respeita o tipo de arquivo e efeito autorizado.
Aceite proposto: Transformação passa validação sem relaxar o requisito original.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T217 → T233 [complements]
Como combinar: SapFix/Sapienz usa sinais de falha e valida candidatos antes de revisão.
Interface: Candidato, reprodução e resultados de testes.
Condição: A validação pertence à revisão candidata.
Aceite proposto: Rejeitar correção que não resolve a falha ou introduz regressão detectada.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S007. Casos: V4C-C009.

CONTROLES DE FALHA
- Testes verdes com zero casos executados não confirmam comportamento.
- O mesmo modelo pode gerar implementação e teste com o mesmo equívoco; buscar requisito e prova independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de correção e regressão com iguais verificadores e orçamento de tentativas. Modelos pequenos podem competir em defeitos locais verificáveis sem equivalência em design aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T224, T213, T233

## Fontes primárias associadas

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S023 — Spec Kit

[https://github.com/github/spec-kit](https://github.com/github/spec-kit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo de especificação, plano, tarefas, implementação e convergência; exemplo concreto de desenvolvimento guiado por especificações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

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

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

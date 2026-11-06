# T213 — Task Decomposition em micro-missões

**Nome canônico:** Task Decomposition em micro-missões  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T213  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** missões incrementais; decomposição orientada a resultado

## T213:C01 — conceito

Decomposição de um objetivo em unidades pequenas com resultado observável, fronteiras e critério de aceitação. Micro-missão é um rótulo operacional, não um tamanho padronizado. A qualidade da divisão depende de preservar dependências e permitir integração; fragmentar arbitrariamente pode aumentar o retrabalho.

Como funciona:
- Derivar unidades a partir de resultados desejados, não de um número fixo de linhas ou minutos.
- Declarar entradas, saída, dependências e responsável pela integração de cada unidade.
- Avaliar a conclusão local e depois verificar o comportamento conjunto do objetivo original.

## T213:C02 — aplicacao

Quando usar:
- Implementações extensas, auditorias por módulos e trabalho que precisa sobreviver a trocas de sessão.

Quando não usar:
- Quando a solução depende de uma mudança atômica indivisível ou a coordenação custa mais que executar diretamente.

Implementação proposta:
- Proposta: transformar a especificação em unidades com IDs e critérios de pronto verificáveis.
- Separar descoberta de implementação quando a arquitetura ainda é incerta; redividir após obter evidência.
- Executar em paralelo apenas unidades independentes, com propriedade de arquivos ou interfaces bem definida.
- Reservar uma missão de integração e registrar pendências comuns, evitando declarar o projeto pronto pela soma de status locais.

Aplicação LAI proposta:
Proposta LAI: usar missões com entrada, patch, teste e handoff explícitos, mantendo dependências visíveis para o coordenador.

## T213:C03 — riscos_validacao

Armadilhas:
- Micro-missões podem otimizar partes incompatíveis.
- Unidades pequenas demais desperdiçam contexto de inicialização.
- Subdivisão ilimitada pode ocultar falta de progresso real.

Métricas sugeridas:
- Duração e variância por unidade; retrabalho de integração; bloqueios; cobertura dos critérios globais.

Testes propostos:
- Dividir uma alteração de contrato entre produtor e consumidor e exigir uma verificação integrada.
- Remover uma dependência e conferir propagação de bloqueio.
- Tentar encerrar o projeto com uma missão sem evidência e impedir conclusão global.

## T213:C04 — perguntas_proveniencia

Pergunta: Toda micro-missão deve virar um subagente?
Resposta: Não. A divisão organiza o trabalho; delegação e paralelismo só ajudam quando há independência e contexto suficiente.

Pergunta: Qual é o tamanho correto?
Resposta: O menor que ainda produza um resultado útil e verificável sem impor coordenação excessiva ou perder contexto essencial.

Pergunta: Uma micro-missão deve caber em uma única chamada?
Resposta: Não necessariamente. A unidade útil é definida por resultado e dependências, embora orçamento e janela limitem sua execução.

Pergunta: Como reconhecer uma divisão ruim?
Resposta: Quando cada parte depende de decisões ainda mutáveis das outras e a integração exige refazer grande parte do trabalho.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T213:C05 — mecanismo_avancado

A fronteira de uma micro-missão deve reduzir dependências cruzadas e produzir um artefato testável. Dividir por número de linhas ou minutos pode cortar uma mudança no meio de seu contrato. Uma decomposição proposta distingue entradas estáveis, saídas integráveis e decisões compartilhadas que precisam ocorrer antes do fan-out. Quanto mais acoplados os resultados, maior o custo de resolver conflitos no fim.

Condição de contorno:
Quando as partes precisam alterar continuamente a mesma interface, fragmentação excessiva aumenta coordenação e retrabalho.

Contrato proposto:
- Entradas: Objetivo, dependências, interfaces e capacidade de execução.
- Saídas: Unidades com entrada versionada, saída esperada e critério de integração.
- Estado: DAG de micro-missões, responsáveis e contratos compartilhados.
- Invariante: Nenhuma unidade declara sucesso somente por produzir arquivo sem satisfazer a saída combinada.

Compromissos de projeto:
- Unidades pequenas facilitam retomada e geram mais overhead de despacho e revisão.
- Unidades maiores preservam coerência local e exigem mais contexto e tempo antes de gerar resultado verificável.

## T213:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dividir uma mudança em consumidor e produtor com contratos divergentes; verificar se a incompatibilidade é detectada na especificação compartilhada antes da integração final.

Plano de avaliação proposto:
Comparar divisão por arquivos, por funcionalidade e por dependências em tarefas equivalentes. Medir retrabalho de merge, tempo até artefato útil e custo de coordenação. Escolher granularidade pelo acoplamento observado, sem tamanho universal de micro-missão.

Comparações:
- T147 (complements): Fan-out explora independência das unidades já bem delimitadas.
- T208 (complements): Planner–Executor distribui e acompanha unidades com critérios explícitos.

Afirmação rastreável:
LLMCompiler identifica dependências para despachar funções que podem executar em paralelo.
Suporte: related; fontes: V3C-S002
Limite: A escolha de micro-missões de software amplia esse princípio; não é uma taxonomia padronizada fornecida pelo artigo.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T213:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculava micro-missões a artefatos testáveis. A expansão escolhe tamanho de unidade conforme variância e integração, cria orçamentos locais e diferencia decomposição útil de fragmentação que só multiplica mensagens.

Fronteira por invariantes
Uma micro-missão deve preservar ou transformar um conjunto claro de invariantes. Dividir um requisito entre dois agentes sem definir quem garante sua propriedade final deixa uma lacuna de responsabilidade. Prefira unidade que termine com artefato verificável e pouco estado compartilhado; decisões transversais devem ser tomadas antes da distribuição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S002.

Tamanho adaptativo
Tarefas repetitivas previsíveis podem ser agrupadas; exceções ambíguas merecem unidades menores e mais diagnóstico. Use histórico de retrabalho para ajustar tamanho, mantendo overhead de preparação e integração no cálculo. O número de parâmetros não define sozinho quantos arquivos cabem numa missão: acoplamento e clareza do teste importam mais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S014.

Orçamento herdado
Distribua tempo, tokens e tentativas a partir do teto global, reservando integração e contingência. Cada filho recebe sua parcela e não um orçamento novo completo. Ao encerrar uma unidade, devolva capacidade não usada conforme a política do controlador; não permita que a narrativa de sucesso esconda custo de subtarefas abandonadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S022.

USO AVANÇADO — Atualização de dependência
Cenário: Muitos consumidores precisam ajustar chamadas e validar comportamento.
Estratégia: Agrupe por módulo e contrato, defina revisão comum da API e produza patches separados. Execute validação local antes de integrar; uma incompatibilidade no contrato compartilhado suspende os dependentes afetados. Unidades concluídas que continuam compatíveis não precisam ser reescritas.
Papel do modelo pequeno: 3–7B faz alterações mecânicas; 8–14B diagnostica testes; 15–30B resolve contrato comum.
Aceite proposto: Proposta: custo por módulo aceito e retrabalho causado por mudanças transversais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S030.

USO AVANÇADO — Pesquisa de muitas bases
Cenário: Cada tópico exige aprofundamento e fontes próprias.
Estratégia: Atribua IDs únicos, contrato de conteúdo e arquivos separados, com junção só após validação. Fontes e casos podem ser compartilhados por identidade; tópicos não devem inventar casos para preencher uma quota. Reserve etapa de revisão cruzada para detectar nomenclatura e evidência indevidas.
Papel do modelo pequeno: 8–14B extrai e estrutura; 15–30B integra relações e audita alegações.
Aceite proposto: Proposta: cobertura integral dos IDs e nenhuma duplicação artificial de casos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Unidades curtas com transformação e teste local explícitos, sem múltiplos objetivos vagos.
8–14B: Missões com algumas dependências internas e retorno estruturado de impedimentos.
15–30B: Decomposição global, integração e resolução de interfaces compartilhadas.
Requisitos de treino/runtime: Identidade estável das unidades, arquivos ou áreas de escrita separados e orçamento global observável.
Não aplicar quando: Não fragmentar trabalho cujo aceite depende de contexto indivisível sem prever integrador capaz de recuperá-lo.

## T213:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Campanhas são decompostas em aplicações e ondas de dependências.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Operador relata decompor metas em blocos de design, código, revisão e testes com planos versionados.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: Decomposição de uma feature em mudanças revisáveis inspira micro-missões.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Amazon Q e harness Codex descrevem campanhas e decomposição; o método de tamanho adaptativo é proposta e não métrica comprovada.
Consultas registradas: V4C-Q012, V4C-Q027.

## T213:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T213 → T237 [feeds]
Como combinar: Transformar unidades independentes em tarefas de subagentes com retorno verificável.
Interface: ID, entradas, dono de escrita e critério de aceite.
Condição: Dependências compartilhadas resolvidas ou explicitadas.
Aceite proposto: Integrador consegue aceitar ou rejeitar cada unidade sem adivinhar estado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T213 → T234 [complements]
Como combinar: No harness Codex, planos e conhecimento do repositório sustentam decomposição e continuidade.
Interface: Plano versionado, decisão e referências de projeto.
Condição: Documentos correspondem à revisão em trabalho.
Aceite proposto: Etapas antigas não são executadas após mudança de requisito sem revisão.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

CONTROLES DE FALHA
- Unidades pequenas demais podem consumir mais coordenação que execução.
- Uma tarefa marcada concluída sem artefato aceito continua pendente para integração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare campanha inteira, incluindo planejamento e revisão, entre decomposição com modelos pequenos e modelo de fronteira. Sucesso em tarefas atomizadas não demonstra competência equivalente em requisitos abertos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T208, T237, T218

## Fontes primárias associadas

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

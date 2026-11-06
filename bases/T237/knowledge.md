# T237 — Subagent Offloading

**Nome canônico:** Subagent Offloading  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T237  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** subagent delegation; delegação de contexto

## T237:C01 — conceito

Delegação de uma parte delimitada do trabalho a outro agente, que produz resultado aproveitável pelo agente principal. A documentação de Claude Code descreve subagentes e seus contextos próprios. A forma de inicialização pode variar: não se deve assumir que toda delegação começa vazia nem que todo o histórico é sempre compartilhado.

Como funciona:
- O coordenador define objetivo, entradas, restrições e saída esperada da subtarefa.
- O subagente trabalha com seu contexto e ferramentas disponíveis.
- O resultado retorna em forma compacta, acompanhado de evidências e referências para verificação e integração.

## T237:C02 — aplicacao

Quando usar:
- Investigações independentes, leitura de módulos distintos, revisão paralela e tarefas cujo resultado possa ser integrado com clareza.

Quando não usar:
- Delegar atividades fortemente dependentes sem coordenação ou permitir que vários agentes editem os mesmos arquivos sem estratégia de integração.

Implementação proposta:
- Proposta: estabelecer um contrato por subtarefa com escopo de arquivos, critérios de conclusão e formato de retorno.
- Enviar contexto suficiente para evitar suposições e limitar material irrelevante.
- Atribuir responsabilidade de escrita ou usar checkouts separados quando houver alterações concorrentes.
- Exigir referência à revisão, fontes e testes efetivamente executados no retorno.
- O coordenador revisa evidências, resolve inconsistências e realiza a integração final dentro do orçamento global.

Aplicação LAI proposta:
Proposta LAI: distribuir missões independentes entre especialistas, mantendo integração, orçamento e responsabilidade final no coordenador.

## T237:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir condições e ressalvas importantes.
- Contextos separados não isolam automaticamente filesystem, rede ou credenciais.
- Delegação pode aumentar tokens e trabalho duplicado.

Métricas sugeridas:
- Tempo total até integração; custo agregado; retrabalho por contrato incompleto; conflitos; qualidade das evidências retornadas.

Testes propostos:
- Delegar a mesma investigação com contratos claros e medir redundância desnecessária.
- Introduzir conflito entre resultados e verificar resolução por evidência, não por maioria.
- Confirmar que um subagente não altera arquivos pertencentes a outro escopo de escrita.

## T237:C04 — perguntas_proveniencia

Pergunta: Subagentes economizam tokens automaticamente?
Resposta: Não. Eles podem reduzir o contexto do coordenador, mas suas próprias chamadas também consomem recursos. O ganho depende da divisão e da quantidade de trabalho repetido.

Pergunta: O coordenador pode aceitar qualquer resumo como conclusão?
Resposta: Não. Deve verificar a evidência necessária ao risco e aos critérios da tarefa, especialmente quando o resultado implica mudança de código ou estado externo.

Pergunta: Qual resultado de pesquisa é melhor que um resumo solto?
Resposta: Uma síntese com fontes, alegações específicas, limitações e referências que o coordenador consiga conferir.

Pergunta: Quem responde pela qualidade após o merge?
Resposta: O coordenador ou integrador definido pelo contrato; sucesso de cada tarefa isolada não prova compatibilidade do conjunto.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T237:C05 — mecanismo_avancado

A delegação precisa transferir uma unidade de decisão suficiente, sem depender de contexto que só o coordenador conhece. O retorno também deve separar resultado, evidência e limitações. Um subagente que afirma ter testado algo precisa devolver o alvo, revisão e resultado correspondente. Delegar pesquisa pode reduzir contexto do coordenador; delegar uma edição exige ainda um contrato de integração e propriedade sobre arquivos ou revisões.

Condição de contorno:
Um subagente não consegue resolver uma dependência omitida apenas por possuir outro contexto ou mais chamadas de modelo.

Contrato proposto:
- Entradas: Objetivo delimitado, entradas versionadas, ferramentas necessárias e critério de entrega.
- Saídas: Artefatos, fontes, decisões tomadas e questões não resolvidas.
- Estado: Responsável, orçamento delegado, revisão-base e estado da entrega.
- Invariante: O coordenador valida o resultado integrado e não trata o resumo como prova automática de execução.

Compromissos de projeto:
- Delegação reduz carga de contexto local e acrescenta custo de inicialização e comunicação.
- Workers autônomos resolvem detalhes e podem divergir de premissas não explicitadas no contrato.

## T237:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: omitir uma dependência crítica e fornecer duas tarefas que editam a mesma interface; exigir lacuna explícita e conflito identificado antes de integrar.

Plano de avaliação proposto:
Comparar execução central e offloading em subtarefas independentes e acopladas. Medir economia de contexto, retrabalho, tempo final e qualidade das evidências. Contabilizar chamadas de todos os agentes e trabalho do coordenador.

Comparações:
- T169 (complements): Contextos isolados são uma forma de executar a delegação, mas não seu critério de sucesso.
- T211 (complements): O formato de handoff pode organizar entradas e devolução do subagente.

Afirmação rastreável:
Claude Code descreve subagentes que trabalham em contexto próprio e devolvem resultados ao agente principal.
Suporte: direct; fontes: V2A-S018
Limite: Ferramentas, contexto inicial e persistência dependem do tipo e configuração; não se presume um padrão universal de fork.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T237:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigia contexto suficiente e evidência no retorno. A expansão escolhe o que terceirizar, limita integração e acompanha trabalhadores para que redução de contexto do supervisor não vire perda de controle sobre a missão.

Delegar por valor líquido
Compare trabalho local com custo de preparar, executar e integrar a delegação. Busca independente e revisão por propriedade costumam ter fronteiras claras; decisões fortemente acopladas podem gerar mais coordenação que ganho. Escolha unidades cuja resposta altere uma decisão do supervisor e que possam terminar sem depender de conversa não fornecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Retorno escalonado
Peça resultado curto com artefatos, evidências e limitações, mantendo detalhes disponíveis sob demanda. O supervisor verifica suficiência antes de integrar e pode solicitar esclarecimento específico. Não retransmita toda a trajetória de cada trabalhador; isso elimina boa parte do benefício de contexto e multiplica ruído de hipóteses já descartadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Responsabilidade de integração
O supervisor continua responsável por conflitos de versão, duplicação de fontes e critérios globais. Um trabalhador não pode declarar missão inteira concluída porque sua parte terminou. Atribua dono de escrita, revisão e critério de aceite, e espere sinal de prontidão antes de consumir arquivos que ainda podem estar mudando.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, C-S030.

USO AVANÇADO — Pesquisa paralela verificável
Cenário: Vários tópicos precisam de fontes e comparação posterior.
Estratégia: Distribua perguntas independentes e IDs exclusivos. Cada trabalhador retorna evidência e limite, com casos identificados para deduplicação. O supervisor revisa alegações que atravessam tópicos e não soma relatos do mesmo deployment como confirmações independentes. Reabra apenas lacunas específicas.
Papel do modelo pequeno: 8–14B coleta e extrai; 15–30B integra e audita relações.
Aceite proposto: Proposta: cobertura integral com menos contexto no supervisor e custo de integração registrado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

USO AVANÇADO — Revisores especializados de patch
Cenário: O candidato precisa respeitar propriedades distintas.
Estratégia: Delegue uma propriedade por revisor e forneça o mesmo artefato imutável. Um revisor devolve evidência de violação ou limite de avaliação. Agregue por requisito obrigatório, sem votação que esconda falha crítica, e rode verificações executáveis em paralelo quando forem independentes.
Papel do modelo pequeno: 3–7B cobre regras estreitas; 8–14B analisa trechos; 15–30B resolve conflitos de intenção.
Aceite proposto: Proposta: detectar violações inseridas sem excesso de falsos bloqueios ou revisões redundantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefas pequenas com contrato explícito e poucas dependências ocultas.
8–14B: Especialistas por documento, módulo ou propriedade, com evidência recuperável.
15–30B: Supervisão e síntese entre trabalhadores; manter o número de agentes compatível com orçamento e integração.
Requisitos de treino/runtime: Fila de tarefas, IDs, versões, donos de escrita e retorno final validado antes de consolidação.
Não aplicar quando: Não delegar apenas para aumentar paralelismo quando o resultado precisa de contexto compartilhado indivisível.

## T237:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O líder delega pesquisa e recebe resultados condensados.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Subagentes são modelados como ferramentas especializadas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Agentes revisam outros agentes no processo descrito.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Fixers e verificadores recebem papéis e escopos específicos.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e AutoClean demonstram delegação operacional. Não foi presumido que seus trabalhadores sejam modelos de 3–30B.
Consultas registradas: V4C-Q006, V4C-Q010.

## T237:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T237 → T147 [complements]
Como combinar: Claude Research usa subagentes paralelos e reúne resultados para a resposta do líder.
Interface: Perguntas, orçamento e artefatos retornados.
Condição: Trabalhos independentes com junção definida.
Aceite proposto: O líder integra resultados aceitos e identifica lacunas.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T237 → T200 [complements]
Como combinar: CodeCourt no AutoClean distribui avaliação por propriedades e usa os vereditos como gate do candidato.
Interface: Patch imutável, propriedade e parecer.
Condição: Critérios obrigatórios têm tratamento explícito de falha.
Aceite proposto: Um veredito negativo não desaparece na média dos demais.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Contexto isolado não garante arquivos ou efeitos isolados.
- Relato de teste de subagente precisa identificar alvo e revisão para ser aceito como evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare equipe pequena e agente de fronteira pelo orçamento total, incluindo supervisor e revisores. A especialização ajuda em tarefas verificáveis, mas integrações difíceis podem consumir toda a vantagem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T213, T239, T208

## Fontes primárias associadas

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

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

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

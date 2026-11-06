# T208 — Planner–Executor / Plan-and-Execute

**Nome canônico:** Planner–Executor / Plan-and-Execute  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T208  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** plan and execute; planejador e executor

## T208:C01 — conceito

Arquitetura que separa a formulação de um plano da execução de suas etapas. O planejador define objetivos intermediários e dependências; o executor realiza ações e devolve evidências. Uma revisão do plano incorpora resultados e obstáculos. A separação pode existir no mesmo modelo ou em processos distintos.

Como funciona:
- O plano é um conjunto versionado de etapas com precondições, resultado esperado e critério de conclusão.
- O executor recebe contexto suficiente para uma etapa, sem assumir que todo o plano permanece válido.
- Um controlador decide continuar, replanejar ou encerrar a partir de resultados observados.

## T208:C02 — aplicacao

Quando usar:
- Tarefas com várias dependências, investigação seguida de implementação ou execução distribuída entre especialistas.

Quando não usar:
- Pedidos curtos em que a preparação do plano custa mais que a ação e não reduz incerteza.

Implementação proposta:
- Proposta: gerar um plano estruturado, atribuir IDs às etapas e validar dependências antes de iniciar.
- Para cada etapa, persistir entrada, artefatos, avaliação e status; distinguir bloqueado de concluído.
- Replanejar quando uma precondição falhar, preservando o histórico de decisões e a autorização original.
- Limitar revisões sucessivas e exigir uma próxima ação verificável, em vez de planos cada vez mais longos.

Aplicação LAI proposta:
Proposta LAI: dividir alterações em investigação, patch e validação, preservando contratos entre etapas e um coordenador responsável pela conclusão global.

## T208:C03 — riscos_validacao

Armadilhas:
- Planos detalhados sobre fatos desconhecidos envelhecem rapidamente.
- Um executor pode declarar sucesso sem produzir o artefato esperado.
- Paralelismo incorreto viola dependências entre etapas.

Métricas sugeridas:
- Etapas concluídas com evidência; revisões úteis; retrabalho; custo de planejamento e integração.

Testes propostos:
- Simular dependência indisponível e verificar revisão apenas das etapas afetadas.
- Introduzir resultado que invalida uma hipótese central e exigir replanejamento explícito.
- Repetir uma conclusão recebida e impedir execução duplicada da etapa seguinte.

## T208:C04 — perguntas_proveniencia

Pergunta: Planner e executor precisam ser modelos diferentes?
Resposta: Não. São responsabilidades arquiteturais; podem usar o mesmo modelo com entradas, estados e critérios de saída separados.

Pergunta: Um plano aprovado garante que as próximas ações estão corretas?
Resposta: Não. Cada ação depende do estado atual e das evidências; mudanças relevantes exigem revisão do plano.

Pergunta: Replanejar deve zerar o histórico do executor?
Resposta: Não. O estado confirmado e as intenções concluídas precisam continuar disponíveis para evitar repetição de efeitos.

Pergunta: Qual é o retorno mínimo útil do executor?
Resposta: Resultado observado, evidência de conclusão, erro classificado e premissa afetada; apenas dizer que falhou deixa o planejador sem diagnóstico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T208:C05 — mecanismo_avancado

A fronteira entre planejador e executor deve incluir pré-condições verificáveis e dependências simbólicas. O executor não precisa receber toda a discussão que produziu o plano; precisa saber o que realizar, com quais entradas e como reconhecer sucesso. Replanejamento exige preservar a identidade das intenções já confirmadas, pois renumerar etapas e repeti-las como novas pode duplicar efeitos. Revisão do plano e tentativa de execução são eixos separados.

Condição de contorno:
A separação é pouco útil quando o planejador não recebe evidências suficientes para distinguir falha de ferramenta e falha de sua premissa.

Contrato proposto:
- Entradas: Objetivo, estado confirmado, ferramentas e resultados das etapas anteriores.
- Saídas: Plano versionado ou revisão com dependências e critérios de aceitação.
- Estado: Intenções estáveis, etapas, evidências e motivo de replanejamento.
- Invariante: Uma nova versão do plano não transforma automaticamente efeito já concluído em trabalho pendente.

Compromissos de projeto:
- Executor simples reduz custo por etapa e depende de instruções operacionais claras.
- Planejador mais frequente adapta melhor e aumenta latência e consumo de contexto.

## T208:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: confirmar uma escrita e depois invalidar uma premissa de uma etapa posterior; exigir replanejamento sem repetir a escrita confirmada.

Plano de avaliação proposto:
Comparar executor com autonomia limitada, executor reativo e plano detalhado. Controlar ferramentas e objetivos. Medir revisões, efeitos duplicados, passos descartados e custo por conclusão. Escolher separação pela quantidade de dependências que o plano consegue antecipar.

Comparações:
- T143 (complements): Plan-Then-Act descreve a ordem lógica; Planner–Executor explicita responsabilidades e contrato de retorno.
- T144 (alternative): Um agente reativo pode escolher a próxima ação sem manter dois papéis separados.

Afirmação rastreável:
LLMCompiler organiza planejamento de chamadas, despacho e execução como componentes distintos.
Suporte: direct; fontes: V3C-S002
Limite: O artigo não determina a granularidade ideal dos papéis nem garante economia em toda tarefa.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T208:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definia pré-condições e separava revisão do plano de tentativa. A camada nova organiza replanning por diagnóstico, delegação com autoridade delimitada e uma ponte explícita entre plano global e execução local adaptativa.

Plano como contrato executável
Cada etapa precisa de resultado, entradas e condição de parada. O executor pode escolher detalhes locais enquanto não muda esse contrato. Se descobrir requisito incompatível, devolve evidência e impedimento ao planejador; não altera a missão silenciosamente para transformar falha em sucesso. O plano é revisável, mas sua identidade continua rastreável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S012.

Replanejar a causa correta
Separe falha de transporte, ausência de capacidade, evidência que contradiz premissa e teste que rejeita resultado. Retry trata algumas falhas temporárias; reparo modifica uma chamada; replanejamento modifica dependências ou objetivo operacional. Uma mensagem genérica de erro impede escolher a reação adequada e incentiva o planejador a repetir a mesma ideia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V2A-S012.

Escopo de autonomia
O planejador entrega limites de ferramentas, orçamento e autoridade por etapa. O executor não herda automaticamente todas as permissões do supervisor. O retorno inclui evidências para a junção e o que ficou desconhecido. Quando um modelo maior planeja para um menor, as etapas precisam caber nas capacidades realmente testadas do trabalhador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S030.

USO AVANÇADO — Migração de API
Cenário: Um plano global define contrato novo e sequência entre consumidores.
Estratégia: Fixe a interface antes de distribuir edições. Executores fazem busca e testes locais, retornando patches com revisão base. Se vários consumidores exigirem exceção não prevista, suspenda a integração e revise a interface, preservando candidatos compatíveis.
Papel do modelo pequeno: 15–30B planeja; 3–7B edita chamadas simples; 8–14B trata diagnóstico local.
Aceite proposto: Proposta: taxa de integração correta e quantidade de etapas refeitas por premissa errada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S030.

USO AVANÇADO — Pesquisa longa
Cenário: O supervisor define questões e cada trabalhador explora uma fonte ou subtema.
Estratégia: Use plano global estável para cobertura e loop local para consultas adaptativas. O trabalhador para quando satisfaz a pergunta, esgota orçamento ou encontra contradição relevante. A síntese recebe evidências e lacunas, não uma declaração genérica de tarefa concluída.
Papel do modelo pequeno: 8–14B coleta e extrai; 15–30B revisa o plano quando fontes mudam a hipótese.
Aceite proposto: Proposta: cobertura por pergunta e custo de replanejamento, sem duplicar consultas confirmadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Etapas pequenas com ferramentas delimitadas e critérios de sucesso objetivos.
8–14B: Execução local adaptativa em domínio conhecido, devolvendo erro estruturado.
15–30B: Planejamento e integração de várias etapas; modelos de fronteira continuam elegíveis para exceções difíceis.
Requisitos de treino/runtime: Estado versionado, efeitos identificados, resultados persistidos e limites por executor.
Não aplicar quando: Não separar papéis se o custo de transferência excede a tarefa ou se faltam critérios de aceite.

## T208:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Responsabilidades de líder planejador e trabalhadores são explícitas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Planner e executor têm responsabilidades explícitas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn e Claude Research sustentam combinação operacional de planejamento e execução. Bandas de parâmetros e testes propostos não foram medidos localmente.
Consultas registradas: V4C-Q010, V4C-Q012.

## T208:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T208 → T144 [complements]
Como combinar: Hiring Assistant combina planejamento com execução local baseada em ReAct.
Interface: Plano global, tarefa local e observações do executor.
Condição: O loop local respeita o escopo da tarefa delegada.
Aceite proposto: Falha de premissa volta ao supervisor com evidência.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T208 → T237 [complements]
Como combinar: Claude Research usa liderança e trabalhadores especializados para executar partes do plano.
Interface: Pergunta, orçamento e artefato de retorno.
Condição: A tarefa permite divisão e integração verificável.
Aceite proposto: Reunir cobertura sem contar duplicatas como confirmação independente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

CONTROLES DE FALHA
- Replanejar não renova orçamento já consumido.
- Revisar números de etapas não deve criar novas identidades para efeitos já confirmados.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare divisão entre modelos e um executor de fronteira com o mesmo conjunto de ferramentas. Vantagens em campanhas decomponíveis não demonstram planejamento geral equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T213, T237

## Fontes primárias associadas

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

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

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

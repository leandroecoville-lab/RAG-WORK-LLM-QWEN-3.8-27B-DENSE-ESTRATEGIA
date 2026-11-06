# T143 — Plan-Then-Act

**Nome canônico:** Plan-Then-Act  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T143  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejar e depois agir

## T143:C01 — conceito

Padrão que explicita um plano antes de executar ações. Ajuda a decompor objetivos, verificar dependências e estabelecer critérios de aceite. O plano é uma hipótese operacional e deve mudar quando novas observações invalidarem suas premissas; não é uma sequência que deva ser cumprida cegamente.

Como funciona:
- Decompor o objetivo em etapas com entregáveis verificáveis.
- Validar precondições, dependências e permissões de cada etapa.
- Executar e replanejar somente a parte afetada por novas evidências.

## T143:C02 — aplicacao

Quando usar:
- Missões com dependências previsíveis.
- Operações que se beneficiam de revisão do plano antes de efeitos externos.

Quando não usar:
- Ambiente altamente dinâmico no qual um plano longo fica obsoleto imediatamente.

Implementação proposta:
- Usar schema para etapa, entrada, saída, responsável e condição de conclusão.
- Persistir versão do plano e vincular alterações ao evento que as motivou.
- Colocar limites de tempo, orçamento e replanejamentos.

Aplicação LAI proposta:
Proposta: planejar auditorias da Helena com artefatos e testes por etapa, mantendo espaço para descoberta durante execução.

## T143:C03 — riscos_validacao

Armadilhas:
- Detalhar demais cria aparência de precisão sem informação suficiente.
- Marcar etapa concluída pelo texto da LLM sem validar entregável.

Métricas sugeridas:
- Percentual de etapas executáveis na primeira tentativa.
- Retrabalho por premissas invalidadas e tempo até resultado aceito.

Testes propostos:
- Remover uma precondição e verificar que a etapa dependente não executa.
- Mudar um dado relevante no meio da missão e exigir revisão localizada do plano.

## T143:C04 — perguntas_proveniencia

Pergunta: Planejar elimina ReAct?
Resposta: Não. Um plano global pode conter ciclos locais de observação e ação.

Pergunta: O plano precisa expor raciocínio interno completo?
Resposta: Não. Objetivos, dependências e justificativas operacionais são suficientes.

Pergunta: Um plano pode conter chamadas ainda sem todos os argumentos?
Resposta: Sim, como dependências simbólicas explícitas; a execução aguarda valores reais antes de enviar a chamada.

Pergunta: Devo descartar todo o plano após uma surpresa?
Resposta: Não necessariamente. Invalidar o subgrafo dependente da premissa alterada pode preservar trabalho ainda correto.

Escopo das fontes:
Plan-and-Solve é uma referência relacionada de prompting; o workflow de ferramentas e persistência descrito aqui é extensão editorial.

## T143:C05 — mecanismo_avancado

Um plano útil representa dependências de informação, não apenas ordem textual. Uma etapa pode declarar que consumirá o resultado ainda desconhecido de outra, preservando um espaço reservado em vez de inventar esse valor. ReWOO explora separar planejamento e observações para evitar reprocessar toda a trajetória a cada chamada. A economia depende de quanto da estrutura pode ser antecipado; contingências reais ainda exigem revisão do plano.

Condição de contorno:
Planejamento antecipado perde precisão quando a próxima ação depende de conteúdo imprevisível ou de efeitos difíceis de reverter.

Contrato proposto:
- Entradas: Objetivo, ferramentas disponíveis, hipóteses e critérios por etapa.
- Saídas: Plano versionado, dependências simbólicas e condições para replanejar.
- Estado: Etapas confirmadas, resultados referenciados e premissas ainda não verificadas.
- Invariante: Uma variável de resultado não é substituída por valor imaginado antes da observação.

Compromissos de projeto:
- Um plano amplo reduz chamadas ao planejador e amplia o custo de corrigir premissas erradas.
- Etapas menores permitem revisão frequente e aumentam overhead de coordenação.

## T143:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma ferramenta devolve entidade diferente da esperada na etapa inicial; verificar se o executor invalida dependências afetadas e preserva etapas ainda válidas.

Plano de avaliação proposto:
Comparar plano único, replanejamento por etapa e gatilhos por premissa invalidada. Controlar ferramentas e casos. Medir chamadas de planejamento, etapas descartadas, custo total e objetivos concluídos; escolher frequência pela volatilidade observada.

Comparações:
- T144 (alternative): ReAct incorpora observações a cada ciclo, enquanto o planejamento antecipado tenta reutilizar estrutura prevista.
- T208 (complements): Separar planejador e executor oferece um lugar explícito para validar o plano.

Afirmação rastreável:
ReWOO desacopla planejamento de observações para reduzir redundância de contexto.
Suporte: direct; fontes: V3C-S012
Limite: O estudo não permite presumir que todas as dependências possam ser previstas antes da execução.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T143:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou dependências de informação e valores ainda desconhecidos. A novidade é planejar por compromissos reversíveis, permitindo validar premissas baratas antes de consumir orçamento em etapas dependentes.

Plano com pontos de decisão
Marque etapas como investigação, preparação ou efeito. Primeiro resolva premissas que podem invalidar muitas ações posteriores. Um plano textual pode parecer completo e ainda esconder a hipótese de que uma API, arquivo ou versão existe; esses pontos precisam virar verificações antes da execução custosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V4C-S017.

Replanejamento localizado
Quando uma premissa falha, identifique os descendentes que dependem dela e invalide apenas esse conjunto. Preserve resultados independentes com suas versões. Recomeçar todo o plano desperdiça trabalho; conservar tudo indiscriminadamente propaga conclusões produzidas sobre uma base que deixou de existir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S012.

Plano como orçamento auditável
Atribua uma previsão de custo e critério de aceite a cada etapa, incluindo integração e testes. Estimativas são hipóteses revisáveis, não autorização para exceder limites. Se o esforço previsto ultrapassar o orçamento, reduza escopo permitido ou exponha o impedimento antes de iniciar metade da missão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S017.

USO AVANÇADO — Upgrade com dependências internas
Cenário: Uma aplicação depende de bibliotecas ainda incompatíveis com a versão alvo.
Estratégia: Inventarie dependências, execute um build inicial e organize ondas. Atualize bases compartilhadas antes de consumidores; quando uma biblioteca não for coberta pela automação, crie uma pendência própria em vez de declarar a aplicação migrada.
Papel do modelo pequeno: 8–14B resume incompatibilidades; 15–30B sugere plano por módulos com evidências.
Aceite proposto: Proposta: medir módulos concluídos, esforço refeito e falhas descobertas tardiamente contra ordem simples por arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017.

USO AVANÇADO — Pesquisa com decisão operacional
Cenário: É preciso comparar alternativas e preparar uma recomendação condicionada.
Estratégia: Planeje critérios, fontes e lacunas antes das buscas. O executor adapta consultas localmente; o planejador revisita apenas critérios afetados por novas evidências. Conclua com condições de adoção e pontos não resolvidos, não com um plano artificialmente cumprido.
Papel do modelo pequeno: 3–7B coleta campos por fonte; 15–30B integra critérios e contradições.
Aceite proposto: Proposta: avaliar cobertura dos critérios e correção das dependências, com custo de coleta e verificação incluído.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: preencher etapas de templates conhecidos, verificando uma premissa por vez.
8–14B: Proposta: produzir planos curtos com dependências explícitas e operações do catálogo.
15–30B: Proposta: replanejar subconjuntos após falhas, mantendo histórico de decisões e motivos.
Requisitos de treino/runtime: Exige um validador de grafo e entradas versionadas; treino pode melhorar formato, não garantir validade do plano.
Não aplicar quando: Não usar planejamento extenso quando o ambiente muda mais rápido que a execução ou o próximo passo é uma simples leitura.

## T143:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Transformação apresenta plano de dependências e substituições.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Planejamento estruturado antecede execução de tarefas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Architect antecipa proposta antes da edição.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn e Amazon documentam combinações específicas; o protocolo de compromissos e invalidação local é desenho proposto.
Consultas registradas: V4C-Q010, V4C-Q012.

## T143:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T143 → T144 [complements]
Como combinar: Hiring Assistant combina plano global com ciclo ReAct no executor local.
Interface: Plano de tarefas e observações produzidas durante sua execução.
Condição: O domínio permite decomposição e adaptação dentro de cada tarefa.
Aceite proposto: Proposta: verificar que contingência local não altera objetivo sem retorno ao planejador.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T143 → T213 [feeds]
Como combinar: Cada etapa planejada vira micro-missão com critério de aceite e fronteira de dependência.
Interface: Pacote de trabalho, pré-condições e artefato esperado.
Condição: Há valor em validar etapas separadamente.
Aceite proposto: Medir lacunas entre entregas e retrabalho de integração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não substituir valores desconhecidos por palpites para completar o plano.
- Revalidar premissas críticas imediatamente antes de efeitos que dependam delas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare planos e resultados com um modelo de fronteira em migrações delimitadas. Bons templates podem reduzir diferença em tarefas recorrentes, sem garantir planejamento aberto equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T144, T160

## Fontes primárias associadas

### C-S010 — Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models

[https://arxiv.org/abs/2305.04091](https://arxiv.org/abs/2305.04091)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separar planejamento e resolução é uma estratégia de prompting estudada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

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

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

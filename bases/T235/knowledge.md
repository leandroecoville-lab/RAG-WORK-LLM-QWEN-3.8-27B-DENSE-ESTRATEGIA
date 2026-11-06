# T235 — Headless Mode em loop / Headless Controller

**Nome canônico:** Headless Mode em loop / Headless Controller  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T235  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** headless controller; execução programática de agente

## T235:C01 — conceito

Execução de um agente por interface programática, sem depender de uma conversa interativa visível, sob coordenação de um controlador externo. Codex e Claude Code documentam interfaces dessa natureza. Um controlador em loop acrescenta política de agendamento, orçamento, avaliação de resultado e recuperação; isso não é garantido apenas pelo modo headless.

Como funciona:
- O controlador fornece tarefa e contexto delimitados ao executor.
- O executor retorna eventos, saída e estado de processo conforme a interface documentada.
- O controlador interpreta o resultado, verifica critérios e decide encerrar, continuar ou registrar um bloqueio.

## T235:C02 — aplicacao

Quando usar:
- Jobs de automação, análise de código, tarefas em fila e missões repetíveis com entradas e resultados verificáveis.

Quando não usar:
- Um laço infinito que reinicia o agente sem verificar progresso, autorização, custo ou efeitos da tentativa anterior.

Implementação proposta:
- Proposta: escolher a interface oficial disponível e registrar a versão utilizada, sem inventar opções de linha de comando.
- Definir contrato de entrada, formato de resultado, prazo, limite de tentativas e orçamento total.
- Executar em diretório e ambiente apropriados, com permissões necessárias ao escopo já autorizado.
- Capturar saída e diagnóstico como artefatos, evitando depender de texto livre para todos os estados.
- Verificar evidências antes de declarar sucesso e reconciliar operações incertas antes de continuar após falha.

Aplicação LAI proposta:
Proposta LAI: orquestrar execuções programáticas por missão, preservando resultado verificável, orçamento e identidade da operação entre tentativas.

## T235:C03 — riscos_validacao

Armadilhas:
- Exit code zero pode representar execução normal do processo sem cumprimento do objetivo.
- Saída estruturada pode continuar semanticamente errada.
- Duas instâncias do controlador podem atribuir a mesma tarefa.

Métricas sugeridas:
- Tarefas concluídas com evidência; tentativas; duração; custo agregado; saídas inválidas; concorrência duplicada.

Testes propostos:
- Retornar processo bem-sucedido com critério de aceitação não atendido e impedir conclusão falsa.
- Interromper durante uma mutação e exigir reconciliação na retomada.
- Injetar resultado incompatível com o contrato e verificar encerramento controlado ou reparo limitado.

## T235:C04 — perguntas_proveniencia

Pergunta: Headless significa que o agente possui mais permissões?
Resposta: Não. A ausência de interface interativa não amplia autorização. O controlador deve respeitar as capacidades e controles configurados.

Pergunta: Quais flags devo usar?
Resposta: Consulte a documentação oficial da versão instalada de Codex ou Claude Code. Esta entrada descreve o padrão operacional e não prescreve flags não verificadas.

Pergunta: Uma resposta final válida em JSON confirma os testes?
Resposta: Não. Ela é uma declaração estruturada; testes e artefatos exigem recibos ou resultados verificáveis.

Pergunta: O que impede um loop headless infinito?
Resposta: Critérios de término, orçamento global e análise de progresso implementados no controlador, não a ausência de interface gráfica.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T235:C05 — mecanismo_avancado

Um controlador headless precisa distinguir eventos intermediários e resultado final. Em Codex, JSONL fornece eventos da execução, enquanto output-schema restringe a resposta final; são contratos diferentes. Um processo que termina tecnicamente pode ainda entregar tarefa inconclusiva. A retomada deve usar identidade da sessão e do objetivo, evitando iniciar nova missão somente porque um processo anterior caiu. O controlador também precisa de regra explícita para parar de agendar novas iterações.

Condição de contorno:
Modo não interativo não define por si critérios de sucesso, limite de custo ou repetição segura de efeitos.

Contrato proposto:
- Entradas: Objetivo identificado, sessão, eventos estruturados e orçamento de execução.
- Saídas: Estado final da missão, artefatos e decisão de retomar ou encerrar.
- Estado: Cursor do stream, sessão corrente, tentativas e evidências de conclusão.
- Invariante: Fim do processo não é convertido automaticamente em aceitação do objetivo.

Compromissos de projeto:
- Eventos detalhados permitem diagnóstico e exigem parser versionado e armazenamento.
- Resposta final estruturada simplifica integração e não contém necessariamente todo o histórico de ações.

## T235:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o processo após uma edição e antes da mensagem final; exigir recuperação dos artefatos e estado, sem assumir fracasso total ou repetir a missão do início.

Plano de avaliação proposto:
Comparar execução única e controlador com retomada em interrupções controladas. Medir duplicação, tempo de reorientação, custo e conclusão verificada. Testar ausência de evento final, evento de falha e final estruturalmente válido, mas inconclusivo.

Comparações:
- T210 (complements): Rotação e retomada precisam preservar o estado da missão entre processos.
- T225 (distinct_from): Watchdog restaura capacidade; controlador headless interpreta eventos e decide o próximo trabalho.

Afirmação rastreável:
Codex documenta JSONL para eventos e JSON Schema para a resposta final em execução não interativa.
Suporte: direct; fontes: V3C-S039
Limite: As opções foram verificadas na documentação; a CLI não foi executada nem encontrada no PATH local.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T235:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava eventos, resposta final e estado de processo. A expansão define controlador não interativo por contrato de missão, gestão de recursos e parada explícita, evitando confundir autonomia de processo com conclusão correta.

Controlador é autoridade de ciclo
O processo do agente executa uma unidade; o controlador decide agendar, continuar, interromper ou finalizar. Use estados como em execução, aguardando dependência, candidato pronto e aceito. Exit code e texto final são sinais, não critérios únicos. Um processo que termina sem artefato pode estar inconclusivo; um que permanece vivo pode estar sem progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, V4C-S016.

Eventos e artefatos
Consuma eventos com parser tolerante a versões conhecidas e preserve tipos desconhecidos para diagnóstico. O artefato final passa por contrato próprio e deve apontar à revisão de trabalho. Não transforme evento de ferramenta concluída em missão concluída: a ferramenta pode ter retornado erro ou apenas preparado um candidato ainda sem validação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, V4C-S030.

Recursos e encerramento
O controlador gerencia timeout, orçamento, logs, subprocessos e cancelamento cooperativo. Ao parar, classifica efeitos pendentes e preserva estado retomável. Agendar outro processo com o mesmo prompt não é retomada equivalente se a identidade da missão, diretório e revisão não forem conservados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, C-S026.

USO AVANÇADO — Pipeline de alterações em lote
Cenário: Um job dispara agentes para tarefas de programação repetitivas.
Estratégia: Crie entrada estruturada por tarefa e workspace isolado. Execute agente, valide artefato e testes, e publique candidato para integração. Rejeição retorna diagnóstico limitado; após teto, encerre com pendências. Não manter loop infinito até o modelo declarar sucesso.
Papel do modelo pequeno: 3–7B cobre tarefas mecânicas; 8–14B repara falhas; 15–30B analisa exceções.
Aceite proposto: Proposta: cada job termina em resultado classificado, com custo e evidência completos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S039.

USO AVANÇADO — Pesquisa assíncrona
Cenário: Coleta e síntese precisam continuar sem interação contínua.
Estratégia: Defina perguntas, limites de pesquisa e artefatos esperados antes de iniciar. O controlador acompanha fontes recuperadas e cobertura, acionando nova etapa somente quando pré-condições forem satisfeitas. Na falta de evidência, o resultado é lacuna explícita, não consulta infinita por obrigação de preencher quota.
Papel do modelo pequeno: 8–14B extrai; 15–30B integra dentro de critério de suficiência.
Aceite proposto: Proposta: cobertura rastreável e término previsível mesmo quando uma fonte fica indisponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S039.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Jobs curtos, schema fixo e poucos estados facilitam execução não interativa confiável.
8–14B: Tratamento de erros locais e geração de candidatos com evidência recuperável.
15–30B: Coordenação de etapas amplas, com controlador determinístico mantendo limites e publicação.
Requisitos de treino/runtime: API ou CLI com eventos documentados, diretório e revisão fixados, captura de logs e política de parada.
Não aplicar quando: Não habilitar autoridade ilimitada só porque o modo não oferece prompts interativos.

## T235:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: O recurso executa trabalho em background com logs.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: GitHub e OpenAI documentam agentes e interfaces operacionais; recursos disponíveis não provam implantação deste controlador específico nem justificam loops ilimitados.
Consultas registradas: V4C-Q011, V4C-Q027.

## T235:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T235 → T225 [complements]
Como combinar: Watchdog recupera processo quando necessário, sem reiniciar automaticamente a missão lógica.
Interface: Estado do job, última evidência e geração.
Condição: Recuperação preserva identidade e orçamento acumulado.
Aceite proposto: Queda do processo não causa duplicação de efeitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T235 → T233 [feeds]
Como combinar: Resultado headless é candidato para validação, e só o gate decide aceite da alteração.
Interface: Artefato, base e registros de execução.
Condição: Contrato final foi satisfeito e os testes correspondem à revisão.
Aceite proposto: Texto de sucesso sem evidência é rejeitado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S039, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar JSONL de eventos como se todos os itens obedecessem ao schema da resposta final.
- Subprocessos e efeitos externos podem sobreviver ao encerramento do cliente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo por job aceito e taxa de intervenção com o mesmo controlador. Rodar um modelo pequeno sem UI não demonstra autonomia cognitiva equivalente à de um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T228, T218, T243

## Fontes primárias associadas

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S006 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Claude Code programático pelo CLI ou SDK; controle explícito de entrada, saída e ciclo de execução.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

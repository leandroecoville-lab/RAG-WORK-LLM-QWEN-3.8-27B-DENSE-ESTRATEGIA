# T218 — Loop Detection / detecção de estagnação e ciclos

**Nome canônico:** Loop Detection / detecção de estagnação e ciclos  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T218  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** stagnation detection; cycle detection

## T218:C01 — conceito

Detecção de repetição sem progresso significativo durante a execução de um agente. O objetivo é interromper ciclos improdutivos e obter informação nova. O rótulo descreve uma política de controle: repetição de texto ou de comandos, isoladamente, não prova estagnação, pois algumas verificações são legitimamente periódicas.

Como funciona:
- O controlador observa ações, respostas, mudanças de artefatos e critérios de avanço.
- Assinaturas de estado permitem reconhecer ciclos como A→B→A, além da repetição imediata.
- Uma janela temporal e um limiar contextual diferenciam trabalho lento de ausência persistente de avanço.

Nota de nomenclatura: Política editorial de supervisão; não é apresentada como algoritmo universal de um produto.

## T218:C02 — aplicacao

Quando usar:
- Agentes longos que repetem buscas, recompilam sem alterações ou alternam correções que desfazem umas às outras.

Quando não usar:
- Como motivo automático para encerrar uma tarefa apenas porque o mesmo comando apareceu duas vezes.

Implementação proposta:
- Proposta: registrar hash do artefato relevante, erro normalizado, hipótese atual, ação e resultado.
- Definir progresso por tarefa: nova evidência, teste resolvido, hipótese descartada ou marco concluído.
- Ao detectar estagnação, pedir mudança de estratégia, leitura direcionada ou retorno ao planejador, dentro do orçamento existente.
- Limitar intervenções repetidas e preservar o diagnóstico quando nenhum caminho autorizado produzir avanço.
- Excluir da assinatura ruído como timestamps, sem apagar códigos de erro ou detalhes causais úteis.

Aplicação LAI proposta:
Proposta LAI: usar supervisão de progresso baseada em marcos e evidência, enviando ao planejador a hipótese que falhou e as tentativas já descartadas.

## T218:C03 — riscos_validacao

Armadilhas:
- Normalização excessiva une falhas diferentes.
- Pequenas edições irrelevantes podem enganar uma métrica baseada apenas em hashes.
- Reiniciar a sessão pode reproduzir o mesmo ciclo.

Métricas sugeridas:
- Loops detectados; falsos alarmes; ações sem informação nova; custo até intervenção; recuperação após mudança de estratégia.

Testes propostos:
- Simular três execuções com o mesmo erro e nenhum delta e exigir intervenção.
- Simular testes repetidos com avanço verificável e evitar alarme prematuro.
- Construir um ciclo entre duas revisões e verificar reconhecimento por histórico.

## T218:C04 — perguntas_proveniencia

Pergunta: Limite de passos resolve loops?
Resposta: Ele limita o dano, mas não identifica a causa nem recupera a estratégia. A detecção usa sinais do conteúdo e do estado.

Pergunta: Uma tentativa sem alteração conta como progresso?
Resposta: Pode contar quando elimina uma hipótese ou revela informação relevante. O critério deve registrar essa evidência, não apenas a atividade.

Pergunta: Trocar palavras na próxima tentativa desfaz um loop?
Resposta: Não se ação, informação disponível e efeito esperado continuam iguais sem nova evidência.

Pergunta: O que fazer depois de detectar estagnação?
Resposta: Registrar a hipótese do bloqueio e escolher uma intervenção que altere informação ou estratégia; repetir o mesmo passo com prazo maior pode não ajudar.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T218:C05 — mecanismo_avancado

Detectar ciclos pode usar assinatura de ação normalizada, estado relevante e observação resultante. Igualdade de comando não basta: polling legítimo repete consultas enquanto o estado externo avança. Também não basta uma mensagem nova, pois reformular texto pode esconder a mesma falta de progresso. Uma proposta acompanha variáveis de domínio, como requisitos resolvidos, artefatos confirmados ou hipóteses eliminadas, junto do custo das repetições.

Condição de contorno:
Um limite de passos detecta consumo excessivo, mas não demonstra estagnação; tarefas válidas podem exigir muitas iterações.

Contrato proposto:
- Entradas: Traço de ações, estado relevante, objetivos pendentes e orçamento.
- Saídas: Sinal de ciclo provável, evidências e ação de recuperação indicada.
- Estado: Assinaturas recentes, progresso confirmado e janelas temporais.
- Invariante: Repetição é avaliada contra mudança de estado e finalidade, não somente contra similaridade textual.

Compromissos de projeto:
- Assinaturas muito específicas deixam passar ciclos com pequenas variações.
- Normalização agressiva pode confundir ações parecidas sobre recursos diferentes.

## T218:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar duas consultas equivalentes sem nova informação e, separadamente, repetir polling com progresso real; exigir alerta no primeiro caso e continuidade controlada no segundo.

Plano de avaliação proposto:
Comparar contagem de passos, repetição textual e assinatura com progresso em trajetórias rotuladas. Medir detecção precoce, falsos positivos e custo evitado. Definir resposta proporcional: buscar informação, mudar estratégia ou encerrar com pendências.

Comparações:
- T219 (distinct_from): Limite de execução estabelece uma fronteira de orçamento; detecção de loop interpreta comportamento.
- T145 (complements): Profundidade adaptativa pode consumir o sinal de progresso para decidir continuidade.

Afirmação rastreável:
LangGraph informa que GRAPH_RECURSION_LIMIT pode resultar de ciclos, mas também de grafos complexos válidos.
Suporte: related; fontes: V2A-S009
Limite: O detector semântico de progresso é proposta editorial, não capacidade demonstrada por esse erro do runtime.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T218:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 combinava assinatura de ações e progresso de domínio. A ampliação distingue repetição produtiva de repetição sem aprendizado e define intervenções graduais com critérios para terminar.

Assinatura semântica
Normalize ferramenta, argumentos relevantes, revisão de entrada e classe do resultado. Trocar a ordem de campos ou reformular a explicação não torna a ação nova. Ao mesmo tempo, consultar o mesmo ID depois de uma mudança de estado pode ser legítimo. A assinatura precisa incluir o que poderia alterar a conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V4C-S014.

Progresso verificável
Acompanhe redução de pendências, novas evidências, hipóteses eliminadas ou artefatos aceitos. Aumento de texto e número de ferramentas não demonstram avanço. Uma ação sem resultado pode ser justificável uma vez para testar hipótese; repetição exige explicar qual variável mudou ou qual evento externo está sendo aguardado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S031.

Escada de intervenção
Primeiro sinalize o padrão, depois exija hipótese alternativa ou nova observação e por fim suspenda a etapa. A intervenção também consome orçamento; não crie um loop de críticos comentando a estagnação sem alterar a execução. Encerramento deve preservar o último estado válido e um impedimento específico para retomada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S006.

USO AVANÇADO — Reparo preso em teste
Cenário: O agente alterna duas alterações que produzem o mesmo erro.
Estratégia: Compare hashes de diffs e assinatura da falha. Ao detectar oscilação, recupere requisito e contexto omitido, bloqueie temporariamente as duas propostas equivalentes e peça teste discriminante. Se não houver evidência nova dentro do orçamento, encaminhe a exceção com histórico mínimo.
Papel do modelo pequeno: 3–7B gera patch local; 8–14B classifica ciclo; 15–30B revisa premissa.
Aceite proposto: Proposta: reduzir tentativas inúteis sem interromper reparos que apresentam progresso objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S032.

USO AVANÇADO — Polling prolongado
Cenário: Uma tarefa remota demora e o agente consulta repetidamente seu estado.
Estratégia: Delegue polling mecânico ao runtime com intervalo e deadline. A repetição é válida enquanto houver contrato de espera e sinais externos; não invoque a LLM a cada estado idêntico. Se o prazo exceder o normal, gere diagnóstico com idade e último progresso confirmado.
Papel do modelo pequeno: 8–14B recebe somente transições relevantes; o temporizador não depende do modelo.
Aceite proposto: Proposta: menos chamadas de modelo e detecção de ausência de progresso sem falsos positivos por tarefa lenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Evitar delegar loops abertos; receber ações delimitadas e retornar estados tipados.
8–14B: Classificar repetições e propor uma observação que distinga hipóteses.
15–30B: Reformular etapa ou plano quando o padrão indica premissa errada, sob orçamento remanescente.
Requisitos de treino/runtime: Registro de assinaturas, métricas de domínio e distinção entre espera externa e repetição cognitiva.
Não aplicar quando: Não usar somente limite de passos ou texto repetido como prova de estagnação.

## T218:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber descreve mover polling mecânico para código. Não foi encontrado deployment que comprove exatamente o detector semântico proposto. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T218:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T218 → T209 [complements]
Como combinar: Transformar padrão de falha em hipótese procedimental testável e contextualizada.
Interface: Tentativas, feedback e variável proposta para mudança.
Condição: A reflexão recebe evidência suficiente de causa.
Aceite proposto: Nova tentativa altera fator relevante, sem repetir apenas a explicação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T218 → T219 [complements]
Como combinar: O limite estrutural encerra consumo máximo enquanto o detector busca parar ciclos antes dele.
Interface: Contadores por unidade e sinal de progresso.
Condição: Teto não se reinicia após intervenção ou delegação.
Aceite proposto: Ciclo termina dentro do orçamento e tarefa lenta válida não é confundida com recursão excessiva.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mascarar observações antigas pode esconder que uma tentativa já falhou.
- Uma mensagem de progresso sem mudança de estado não deve reiniciar o watchdog cognitivo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare eficiência e falsos encerramentos em tarefas que contêm tanto polling legítimo quanto ciclos reais. O detector pode ajudar modelos pequenos, mas sua classificação também precisa ser avaliada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T219, T226, T208

## Fontes primárias associadas

### V2A-S009 — GRAPH_RECURSION_LIMIT

[https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limite de passos de execução do grafo antes de alcançar condição de parada.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

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

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V3C-S029 — Reflexion — authors implementation and experiments

[https://github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementações, notebooks e estratégias de reflexão associadas a tipos de agente e ambientes experimentais.

Limite: Repositório de pesquisa em branch mutável; resultados publicados não foram reproduzidos nem usados como avaliação deste corpus.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

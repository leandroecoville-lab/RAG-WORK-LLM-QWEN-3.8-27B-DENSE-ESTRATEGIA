# T206 — Process Verification

**Nome canônico:** Process Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T206  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** verificação de processo

## T206:C01 — conceito

Verificação de que as etapas observáveis de uma execução cumprem precondições, ordem, invariantes e resultados esperados. Complementa a verificação da saída final. Neste catálogo é um rótulo amplo de engenharia, distinto de Process Supervision, que fornece sinais para treinamento.

Como funciona:
- Definir transições válidas e evidências exigidas por etapa.
- Conferir eventos e resultados contra essas regras durante ou depois da execução.
- Rejeitar conclusão quando houver lacuna material ou transição inválida.

## T206:C02 — aplicacao

Quando usar:
- Workflows com dependências, permissões ou resultados intermediários críticos.
- Um resultado final plausível pode esconder etapa não executada.

Quando não usar:
- Julgar processo apenas por narrativa de intenção produzida pelo próprio agente.

Implementação proposta:
- Registrar eventos com identificador de etapa e vínculo ao artefato.
- Definir invariantes como não concluir sem recibo ou não consumir saída inexistente.
- Reconciliar estado final com histórico e evidências externas.

Aplicação LAI proposta:
Proposta: a Helena separar planejado, executado, testado e comprovado por eventos e recibos vinculados, sem depender da eloquência do relatório.

## T206:C03 — riscos_validacao

Armadilhas:
- Logs incompletos podem parecer processo correto por ausência de erro.
- Procedimento correto em etapas isoladas pode falhar no requisito global.

Métricas sugeridas:
- Violações de transição e etapas sem evidência.
- Cobertura de invariantes e divergência entre estado e histórico.

Testes propostos:
- Remover evento de conclusão e conferir que missão não é marcada comprovada.
- Reordenar etapas dependentes e exigir detecção da violação.

## T206:C04 — perguntas_proveniencia

Pergunta: Process Verification é Process Supervision?
Resposta: Não. Uma verifica execução; a outra treina usando feedback sobre etapas.

Pergunta: Log escrito pelo agente prova que a ferramenta rodou?
Resposta: Não sozinho; o registro precisa estar ligado a evidência da execução.

Pergunta: Pode reconstruir ordem apenas pelo relógio?
Resposta: Nem sempre. Relógios diferentes e concorrência exigem relações causais e identificadores, além dos horários.

Pergunta: Processo correto garante objetivo correto?
Resposta: Pode cumprir uma especificação errada ou incompleta; valide também se critérios e pós-condições correspondem à necessidade real.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T206:C05 — mecanismo_avancado

Um registro de execução oferece observabilidade, mas verificar o processo exige regras sobre transições permitidas e evidências que sustentem cada etapa. Em sistemas concorrentes, timestamps sozinhos não definem causalidade; IDs, relações entre operações e versões ajudam a reconstruir o que ocorreu. Uma mensagem “sucesso” emitida pela própria ação não prova que sua pós-condição se realizou no recurso externo.

Condição de contorno:
Traces incompletos ou amostrados podem omitir a etapa que violou o contrato; ausência de evento não demonstra ausência de ação.

Contrato proposto:
- Entradas: Eventos correlacionados, versões de estado, pré/pós-condições e regras de transição.
- Saídas: Relatório de invariantes atendidas, violações e lacunas de evidência.
- Estado: Identidades de operações, vínculos causais, resultados observados e política de retenção.
- Invariante: Toda conclusão de processo indica quais eventos e estados realmente a sustentam.

Compromissos de projeto:
- Mais instrumentação melhora diagnóstico e acrescenta custo e volume.
- Checagem de resultado externo fortalece evidência e pode exigir consultas adicionais.

## T206:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: registrar sucesso antes de uma gravação que falha, duplicar uma operação e remover um evento intermediário. Esperar distinção entre violação, duplicidade e evidência insuficiente.

Plano de avaliação proposto:
Plano proposto: comparar execuções corretas e falhas injetadas com traces completos e parciais. Medir detecção, falsos alarmes e capacidade de localizar a transição inválida; aprovar somente conclusões proporcionais à cobertura observada.

Comparações:
- T194 (distinct_from): Verificação inspeciona execução; process supervision usa sinais de etapas para treinamento.

Afirmação rastreável:
OpenTelemetry representa operações por spans e oferece vínculos, eventos e contexto para correlacionar trabalho distribuído.
Suporte: related; fontes: V3B-S023
Limite: A fonte define observabilidade; o verificador de invariantes é uma camada adicional proposta, não garantia automática do tracing.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T206:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou causalidade dos eventos e pós-condições. Esta camada trata completude do registro, reconstrução de tentativas e limites do que pode ser certificado quando parte do processo ocorre fora do sistema.

Evidência ausente
Um trace sem erro não prova que todas as etapas ocorreram; pode faltar instrumentação ou ter havido perda de eventos. Defina eventos obrigatórios e estados terminais, distinguindo sucesso, falha, cancelamento e desconhecido. A validação deve detectar lacunas, não preenchê-las com a narrativa do agente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

Tentativas e efeitos
Retries podem criar múltiplas tentativas para a mesma operação lógica. Registre identificadores distintos e vínculo causal, preservando qual tentativa produziu o efeito confirmado. Um evento de envio e um timeout não permitem concluir se a ação externa ocorreu; reconciliação precisa consultar estado ou recibo confiável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

Processo versus resultado
Cumprir etapas não garante que o objetivo final foi atingido, e um resultado correto por acaso não legitima etapas proibidas. Avalie ambos. Revisores e barreiras como os descritos no AutoClean oferecem um padrão operacional, mas a evidência deve declarar exatamente quais propriedades e transições foram checadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

USO AVANÇADO — Workflow de atualização
Cenário: O agente deve consultar, propor, validar e alterar um recurso.
Estratégia: Modele estados permitidos, exija pré-condições observadas e relacione cada ação a sua decisão. Verifique estado final no sistema externo e mantenha pendências de reconciliação.
Papel do modelo pequeno: Um 3–7B pode executar uma máquina de estados estreita com ferramentas.
Aceite proposto: Nenhuma transição sem evidência obrigatória nem sucesso sem pós-condição observada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

USO AVANÇADO — Revisão de execução longa
Cenário: Um agente declara ter concluído muitas etapas.
Estratégia: Reconstrua cadeia causal a partir dos eventos e artefatos, confronte com o plano e identifique passos não observados. Não considere texto de progresso como recibo.
Papel do modelo pequeno: Um 8–14B pode resumir evidências; validação de invariantes deve ser determinística quando possível.
Aceite proposto: Detectar etapas omitidas, versões incorretas e efeitos duplicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Estados explícitos reduzem dependência de memória textual em modelos pequenos.
8–14B: Fluxos concorrentes exigem IDs e regras de causalidade além de timestamps.
15–30B: Um 15–30B pode planejar mais etapas, mas isso aumenta a necessidade de auditoria de processo.
Requisitos de treino/runtime: Instrumentação, armazenamento de eventos e regras de transição; não implica supervisão de raciocínio interno do modelo.
Não aplicar quando: Não declarar uma ação concluída só porque a ferramenta foi chamada ou o agente escreveu 'feito'.

## T206:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Propriedades como ausência de desvio de intenção verificam requisitos do processo, sem prova formal.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q019.

## T206:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T206 → T194 [complements]
Como combinar: Eventos verificáveis podem apoiar feedback sobre etapas de um procedimento.
Interface: Transições, resultados e falhas localizadas.
Condição: Rótulos descrevem observações, não inferências inventadas.
Aceite proposto: Comparar supervisão com evidência real do ambiente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S023, C-S047, V4C-S009, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T206 → T200 [complements]
Como combinar: Auditoria independente confronta execução declarada e registros externos.
Interface: Trace, artefatos e recibos.
Condição: Fontes não dependem apenas do narrador.
Aceite proposto: Injetar eventos ausentes e contradições para testar detecção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S023, C-S047, V4C-S009, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter estado desconhecido quando não há evidência para decidir.
- Não usar ordem de chegada de logs como causalidade universal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare tarefas concluídas com processo permitido e evidência suficiente. Observabilidade ajuda a confiar numa aplicação pequena; não aumenta diretamente a capacidade do modelo nem prova o que não foi observado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T159, T194, T200

## Fontes primárias associadas

### C-S047 — Let's Verify Step by Step

[https://arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão por etapas difere de rotular apenas o resultado final.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S023 — OpenTelemetry — Traces

[https://opentelemetry.io/docs/concepts/signals/traces/](https://opentelemetry.io/docs/concepts/signals/traces/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Spans, relações de causalidade, eventos e metadados observáveis de execução.

Limite: Tracing registra operações; checagem de invariantes e interpretação de sucesso são contratos adicionais propostos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

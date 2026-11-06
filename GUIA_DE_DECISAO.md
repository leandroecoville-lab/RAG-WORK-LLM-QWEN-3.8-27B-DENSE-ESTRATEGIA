# Guia de decisão: transformar o inventário em um sistema menor e mensurável

Este guia organiza escolhas de arquitetura. Os 243 IDs preservam o inventário; não representam 243 mecanismos independentes a instalar. As referências R descrevem projetos ou pesquisas, e os componentes P são propostas editoriais. As relações detalhadas estão em `catalogo/relacoes_detalhadas.json` e `exports/comparacoes.csv`.

## 1. Comece pelo erro observado

Escolha um gargalo com exemplos reproduzíveis antes de combinar técnicas. Uma mesma falha aparente pode ter causas diferentes: a informação não foi armazenada, não foi recuperada, foi excluída da montagem, foi ignorada pelo modelo ou a execução não confirmou o efeito necessário. Instrumentar essas fronteiras permite escolher o mecanismo adequado.

| Sintoma reproduzível | Primeira pergunta | Entradas para investigar | Evidência de aceite sugerida |
|---|---|---|---|
| O agente perde uma decisão antiga | O dado existe e sua versão é recuperável? | T047, T060, T064, T072 | Retomada com objetivo, restrições e pendências corretos |
| A fonte correta não aparece | Falha na geração de candidatos, filtro ou ranking? | T027, T028, T032, T036 | Cobertura e posição da evidência em perguntas reservadas |
| O contexto cresce sem melhorar respostas | Quais informações são necessárias ao próximo passo? | T018, T024, T037, T043, T222 | Menos tokens com requisitos e qualidade preservados |
| O primeiro token demora | A espera está na fila ou no prefill? | T082, T088, T094, T102 | TTFT sob carga, com mesmo modelo e tarefas |
| A geração longa fica lenta | O gargalo é memória, cálculo ou comunicação? | T086, T099, T100, T107, T118 | Latência por token, memória e qualidade medidas |
| Uma queda repete uma ação externa | Existe intenção estável e confirmação consultável? | T159, T162, T240–T243 | Recuperação sem duplicar o efeito lógico |
| O agente repete planos sem avançar | Há progresso verificável e limite global? | T218, T219, T225–T228 | Encerramento ou recuperação com motivo observável |
| A edição destrói alterações concorrentes | O patch está vinculado ao estado-base? | T229–T233, T239 | Conflito detectado antes de sobrescrever conteúdo |
| O JSON é válido, mas a ação está errada | Quais regras semânticas faltam no aceite? | T190, T195–T200 | Critérios de domínio e evidência executável satisfeitos |
| Instruções repetidas custam caro | O comportamento é estável e treinável? | T179, T180; fundamento em T178 | Estudante avaliado sem instrução, com custo total menor |

Esses são eixos práticos de investigação, não uma nova contagem de capacidades únicas. Os critérios são propostas para avaliação posterior no ambiente escolhido.

## 2. Separe contexto, memória, cache e pesos

**Contexto** é o conteúdo disponibilizado ao modelo na inferência. **Memória externa** é informação armazenada que pode voltar ao contexto. **Cache de inferência** reaproveita computação compatível. **Treinamento** altera parâmetros. Essas camadas interagem, mas uma não substitui automaticamente a outra. A distinção entre estado de thread e dados entre threads aparece na documentação de persistência do LangGraph; a receita de prompt distillation do Tinker descreve um estudante treinado sem a instrução usada pelo professor. [V3D-S016](https://docs.langchain.com/oss/python/langgraph/persistence), [V3D-S008](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/).

| Mecanismo | O que persiste ou reaproveita | Mudança que exige revisão |
|---|---|---|
| Consolidação por resumos, T069 | Síntese externa de informações | Novos fatos, correções e perda de detalhes necessários |
| Checkpoint, T060 | Estado recuperável de uma execução | Código, schema e fronteiras de efeitos externos |
| RAG, T009 | Documentos, índices e referências | Conteúdo, filtros, embeddings e critérios de relevância |
| Cache por hash, T007 | Resposta associada a uma chave exata | Qualquer entrada ou política relevante fora da chave |
| Cache semântico, T005 | Resposta de consulta considerada semelhante | Limiar, domínio, validade temporal e contexto do usuário |
| Prefix caching, T082 | Estado computacional de prefixo compatível | Modelo, adaptador, tokenizer e demais identidades do cálculo |
| Destilação paramétrica, T179 | Comportamento incorporado aos pesos | Política alvo, dados de treinamento e distribuição de uso |

As condições de invalidação da tabela são recomendações de projeto a validar. Para cache de prefixos, a documentação vLLM explicita fatores adicionais na identidade dos blocos; sua documentação de segurança também limita o papel do salt como separação do cache. Não se deve inferir isolamento completo entre clientes a partir desse campo. [V3D-S004](https://docs.vllm.ai/en/latest/design/prefix_caching/), [V3D-S005](https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md).

## 3. Preserve a fronteira entre fato e proposta

Uma ficha pode conter uma definição bem apoiada e um contrato de implementação ainda não executado. `research.json` torna essa diferença explícita: a afirmação possui fontes e ressalva; os campos de contrato, falha e avaliação descrevem trabalho proposto. Para os 17 componentes P, o suporte é sempre relacionado aos princípios, sem alegar existência de um produto LAI implementado.

Ao transformar uma ficha em trabalho de engenharia, registre: versão da fonte, hipótese, baseline, alteração isolada, entrada, resultado esperado e resultado medido. Um ganho apresentado pelo autor de um artigo não deve ser transferido para outro hardware ou domínio sem reprodução. A ausência de resultado local deve permanecer como ausência, em vez de ser substituída por um número plausível.

## 4. Faça a recuperação falhar de modo identificável

Observe candidatos, ranking, filtros, contexto montado e resposta separadamente. Recuperar T243 por uma consulta sobre efeitos externos é diferente de produzir uma resposta que preserve suas condições. Uma pontuação BM25 alta não é probabilidade de verdade. O protocolo deste pacote distingue desenvolvimento e reserva, e o relatório conserva resultados por caso.

O motor padrão tem expansão lexical aproximada, sem compreensão semântica neural. O perfil `exact` permite comparar o efeito dessa heurística no mesmo corpus. Embeddings, fusão e reranking são candidatos para uma próxima experiência se houver erros concretos que a busca lexical não resolve. A literatura de avaliação RAG separa recuperação, fidelidade ao contexto e resposta; este pacote não executou uma avaliação de geração real. [V3D-S002](https://arxiv.org/abs/2309.15217).

Uma política de ingestão proposta deve preservar `chunk_id`, `entry_id`, `scope`, versão, fonte e estado de evidência. Não use o diretório histórico como corpus ativo: ele contém versões anteriores deliberadamente guardadas para comparação. Depois de mudar o texto, reconstrua embeddings e invalide índices associados ao hash anterior.

## 5. Desenhe recuperação de execução antes de automatizar retries

Separe pelo menos três situações: falha antes de enviar a ação, falha confirmada pelo destino e ação enviada com resultado desconhecido. A última exige reconciliação. Um checkpoint local não resolve sozinho essa ambiguidade.

A outbox associa alteração e evento pendente na mesma transação local, mas publicação pode ser repetida. O destinatário ainda precisa reconhecer duplicatas. Temporal, por sua vez, estabelece restrições de determinismo em relação ao histórico e uma fronteira para Activities; isso não fornece idempotência universal a qualquer API externa. [V3D-S018](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [V3D-S019](https://docs.temporal.io/workflow-definition).

Um teste útil interrompe o worker imediatamente depois de um efeito remoto e antes da confirmação local. A retomada deve descobrir o estado real ou manter uma pendência explícita. Testar apenas restart antes da primeira ação deixa essa fronteira sem cobertura.

## 6. Valide estrutura e comportamento separadamente

Gramáticas restringem sequências possíveis. Schemas verificam propriedades declaradas. Testes executáveis verificam comportamentos selecionados. Fontes sustentam afirmações delimitadas. Cada camada oferece evidência diferente.

XGrammar documenta o ciclo de máscara, amostragem e atualização do matcher. Guidance documenta diferenças de suporte entre backends e limitações de JSON Schema. Uma geração interrompida pode permanecer incompleta; o consumidor precisa validar o objeto final e as regras de domínio. [V3D-S013](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html), [V3D-S014](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html).

O aceite deve ser vinculado ao artefato avaliado. Se o código, schema ou evidência mudar, a aprovação anterior pode não valer. Hash ajuda a identificar bytes, sem comprovar correção semântica. A proposta P012 descreve decisões por critério, e P015 cobre a associação entre intenção, versão e resultado.

## 7. Compare custo por tarefa aceita

Para uma janela de observação definida, uma medida útil é:

`custo por tarefa aceita = custo de todas as tentativas e verificações / número de tarefas aceitas`

Quando nenhuma tarefa for aceita, essa razão não é calculável; reporte zero aceites e o custo total, sem apresentar custo por sucesso igual a zero. Inclua retries, fallback, busca, geração, avaliação e trabalho refeito. Compare também taxa de aceite, latência e tipos de falha: um custo baixo obtido abandonando casos difíceis não representa a mesma qualidade de serviço. LoRA e QLoRA são opções de adaptação dos pesos e não removem instruções por si. O mesmo raciocínio de custo vale para destilação: economizar tokens por chamada precisa compensar preparação, treinamento, validação e atualização.

Escolha primeiro um conjunto pequeno de mecanismos que resolva a falha comprovada. Acrescente o seguinte somente quando a medição mostrar o limite do anterior. Os nomes P podem representar responsabilidades dentro do mesmo processo; não há motivo automático para criar 17 serviços separados.

## 8. Use o pacote sem confundir estudo com implantação

1. Abra `ABRIR_CATALOGO.html` e selecione as fichas relacionadas ao gargalo.
2. Consulte `research.json` para limites, comparação e experimento proposto.
3. Use a busca local e confira fontes; a lista completa continua em `LISTA_COMPLETA_243.md`.
4. Construa uma experiência pequena com critérios definidos antes de executá-la.
5. Registre resultados reais separadamente do conteúdo editorial e atualize a ficha somente com evidência identificada.

O ZIP entrega conhecimento, recuperação local e testes do próprio pacote. Não altera produção, pesos de modelos, banco vetorial ou memória de um agente existente.

# T116 — KV Cache Recomputation

**Nome canônico:** KV Cache Recomputation  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T116  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recomputação de KV

## T116:C01 — conceito

Reconstrói estados KV que deixaram de estar disponíveis, reprocessando os tokens necessários com a mesma configuração do modelo. Pode ocorrer após preempção, expiração ou perda de cache. É troca de memória por trabalho repetido; não significa regenerar arbitrariamente a resposta já aceita.

Como funciona:
- Preservar sequência lógica e posição de progresso fora do cache descartável.
- Reexecutar prefill ou trecho necessário para reconstruir os estados.
- Retomar geração a partir do ponto aceito, sem duplicar conteúdo publicado.

## T116:C02 — aplicacao

Quando usar:
- Pressão de memória exige preemptar algumas sequências.
- Cache perdido pode ser reconstruído mais barato que armazenado ou transferido.

Quando não usar:
- Repetir recomputação continuamente sem reduzir a carga que causa a pressão.

Implementação proposta:
- Registrar tokens aceitos, versão do modelo e revisão de template para reconstrução.
- Distinguir o tempo de recomputação do tempo de progresso útil nas métricas.
- Definir limite de tentativas e política de admissão para conter thrashing.

Aplicação LAI proposta:
Proposta LAI: monitorar recomputação como sinal de saturação do runtime; não confundir ausência de OOM com operação eficiente.

## T116:C03 — riscos_validacao

Armadilhas:
- Reprocessar texto retokenizado de forma diferente pode produzir estados incompatíveis.
- Publicar novamente tokens anteriores gera duplicação mesmo que o estado interno esteja correto.

Métricas sugeridas:
- Tokens recomputados por token novo útil.
- Preempções, latência de retomada e tempo sem progresso.

Testes propostos:
- Eliminar deliberadamente um cache e comparar continuação com uma execução sem perda dentro das condições definidas.
- Provocar pressão sustentada e exigir progresso limitado e erro claro quando não houver capacidade.

## T116:C04 — perguntas_proveniencia

Pergunta: Recomputation altera os pesos?
Resposta: Não. Executa novamente parte do mesmo modelo para recuperar estados temporários.

Pergunta: É igual a recuperar memória episódica?
Resposta: Não. Recuperação episódica seleciona registros; recomputação KV refaz representações numéricas de tokens.

Pergunta: Recomputar é o mesmo que fazer nova resposta?
Resposta: Não. Deve processar tokens confirmados como entrada e retomar somente onde ainda falta gerar.

Pergunta: Pode restaurar com outro adaptador?
Resposta: Isso altera as projeções e possivelmente a distribuição futura; exige uma mudança declarada de configuração, não simples recuperação de cache.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T116:C05 — mecanismo_avancado

Reconstruir KV exige repetir o processamento do histórico confirmado, não repetir decisões de amostragem que já produziram tokens publicados. O cursor da resposta e o cursor do cache devem ser distintos: reconstrução avança estado interno sem emitir novamente a conversa. Se pesos ou adaptadores mudaram, recomputar produz outro estado e requer uma política explícita de migração, em vez de fingir continuidade idêntica.

Condição de contorno:
Sem os token IDs e posições originais, o texto salvo pode não reconstruir exatamente o prefixo esperado.

Contrato proposto:
- Entradas: Histórico confirmado, identidade do modelo, posição de retomada e orçamento disponível.
- Saídas: Cache restaurado e continuação a partir do primeiro token ainda não confirmado.
- Estado: Cursor de emissão, cursor reconstruído e tentativas de preempção.
- Invariante: Tokens já entregues não são reamostrados nem duplicados no transporte.

Compromissos de projeto:
- Liberar memória permite atender outros pedidos e adiciona prefill repetido.
- Preempções frequentes podem transformar capacidade aparente em trabalho improdutivo.

## T116:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: expulsar cache após alguns tokens enviados e reiniciar a reconstrução após interrupção. Esperar uma única sequência publicada e logits compatíveis com execução contínua, usando os mesmos pesos.

Plano de avaliação proposto:
Plano proposto: comparar execução sem preempção com pressões de memória controladas. Medir tokens recalculados, progresso útil, latência e repetições de preempção; ajustar admissão quando a reconstrução impede satisfazer os objetivos do serviço.

Comparações:
- T105 (complements): A política de remoção precisa preservar dados suficientes para reconstruir os estados necessários.

Afirmação rastreável:
O vLLM documenta recomputação de requisições preemptadas quando volta a existir espaço suficiente para KV.
Suporte: direct; fontes: B-S014
Limite: A documentação não garante que recomputação seja mais barata que transferência em qualquer arquitetura.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T116:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou reconstrução de cache e emissão de tokens. A nova camada formula recomputação como escolha de recuperação, com orçamento, pontos seguros e prevenção de trabalho repetido em cascata.

Reconstruir versus restaurar
Se houver cópia em memória inferior, compare seu custo com prefill do histórico confirmado. Um caminho longo com baixa banda pode favorecer recomputação; um histórico caro pode favorecer transferência. Estime ambos com medições da fase relevante e use margem para erro, evitando decisões baseadas só em bytes ou tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

Preempção repetida
Sob pressão, a mesma sequência pode ser reconstruída e novamente preemptada antes de avançar. Conte trabalho descartado e proteja temporariamente pedidos que já pagaram esse custo, dentro de limites de justiça. Sem esse controle, o serviço pode consumir recursos intensamente e entregar poucos tokens novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

Recuperação após falha
Persistir tokens confirmados e identidade do modelo permite reconstruir estado depois de perder um worker, mas não recupera automaticamente chamadas de ferramenta ou efeitos externos. O protocolo de resposta precisa distinguir texto emitido, ação solicitada e ação concluída; retomar a geração não autoriza repetir uma operação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

USO AVANÇADO — Sessão longa pouco ativa
Cenário: Manter KV residente custa mais que o padrão de uso justifica.
Estratégia: Descarte a cópia reconstruível após inatividade e mantenha histórico autorizado e versão. Na retomada, aplique limite de custo e informe estado de carregamento no serviço.
Papel do modelo pequeno: Um 3–7B pode oferecer sessões esporádicas com capacidade reduzida de cache.
Aceite proposto: Retomada deve preservar tokens anteriores e não duplicar eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

USO AVANÇADO — Falha de worker
Cenário: Uma resposta é interrompida antes de terminar.
Estratégia: Reatribua a sequência com cursor confirmado; reconstrua até esse ponto e gere somente a continuação faltante. Se a versão não estiver disponível, aplique política explícita de reinício.
Papel do modelo pequeno: Um 8–14B pode ter réplicas independentes mais econômicas que cache distribuído complexo.
Aceite proposto: Injetar falha em vários pontos e verificar entrega única e histórico coerente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Históricos curtos podem favorecer recomputação simples, mas frequência de retomada importa.
8–14B: Compare restore e prefill sob concorrência, incluindo impacto em outros usuários.
15–30B: Recomputar contextos extensos em 15–30B pode consumir capacidade significativa; reserve orçamento e evite ciclos.
Requisitos de treino/runtime: Runtime precisa manter tokens confirmados, versão e estado das ações. Isso não exige novo treinamento.
Não aplicar quando: Não reamostrar prefixos publicados nem reconstruir com adapter diferente fingindo continuidade idêntica.

## T116:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T116:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T116 → T105 [complements]
Como combinar: Evicção só pode escolher recomputação se houver histórico e identidade suficientes.
Interface: Tokens confirmados e motivo de remoção.
Condição: Custo futuro estimado e estado reconstruível.
Aceite proposto: Medir quantas evicções levam a trabalho repetido sem progresso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S014, V3B-S005, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T116 → T120 [feeds]
Como combinar: Roteamento escolhe worker considerando prefill restante e disponibilidade real.
Interface: Cursor e custo estimado de reconstrução.
Condição: Destino consegue executar a mesma identidade do modelo.
Aceite proposto: Comparar decisões com tempos observados na retomada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S014, V3B-S005, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar o número de reconstruções consecutivas sem avanço.
- Separar idempotência de ações externas da reconstrução de estado matemático.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O benefício é operacional em sessões interrompidas. Compare tempo e custo de recuperação com a mesma qualidade de modelo; recomputar histórico não acrescenta evidência nova nem corrige respostas anteriores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T105, T115, T121

## Fontes primárias associadas

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

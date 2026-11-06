# T105 — KV Cache Eviction

**Nome canônico:** KV Cache Eviction  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T105  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** despejo de cache KV

## T105:C01 — conceito

Remoção de estados KV para liberar memória. É preciso separar descarte de cache reutilizável ocioso, preempção com recomputação e poda de tokens ainda necessários à atenção. As duas primeiras podem preservar a semântica; a última normalmente altera o que o modelo consegue consultar.

Como funciona:
- Determinar quais blocos estão em uso e quais são candidatos a remoção.
- Aplicar política de retenção e atualizar todas as referências ao bloco.
- Recomputar quando necessário ou declarar explicitamente a mudança de contexto se houver poda.

## T105:C02 — aplicacao

Quando usar:
- Cache de prefixos compete com novas sequências pela mesma memória.
- Há política definida para pressão e recuperação sem corrupção de estado.

Quando não usar:
- Descartar KV ativo silenciosamente e continuar como se o contexto permanecesse completo.

Implementação proposta:
- Classificar cada evento como remoção ociosa, preempção recuperável ou compressão com perda.
- Proteger estados referenciados e impedir uso após liberação.
- Limitar ciclos de despejo e recomputação que produzem thrashing.

Aplicação LAI proposta:
Proposta LAI: alertar sobre thrashing do runtime e reduzir admissão antes de permitir que uma política de memória altere silenciosamente o contexto da missão.

## T105:C03 — riscos_validacao

Armadilhas:
- Alta taxa de acerto pode esconder alto custo de recomputar sequências preemptadas.
- Remover por idade é inadequado se o objeto antigo ainda está em uso.

Métricas sugeridas:
- Evictions por classe, recomputações e bytes recuperados.
- Latência de cauda e trabalho repetido por pressão de memória.

Testes propostos:
- Reduzir memória disponível e verificar que todas as saídas continuam corretas no modo sem perda.
- Retomar uma sequência preemptada e comparar com referência sem preempção.

## T105:C04 — perguntas_proveniencia

Pergunta: Apagar KV sempre faz o modelo esquecer?
Resposta: Não se o estado for reconstruído antes do uso; poda sem reconstrução é uma operação diferente.

Pergunta: Eviction libera memória de pesos?
Resposta: Não. Atua nos estados de atenção, não no checkpoint carregado.

Pergunta: Eviction é equivalente a esquecer informação?
Resposta: Só quando o estado deixa de ser reconstruído antes de necessário; um cache dispensável pode ser removido sem perda semântica.

Pergunta: Qual métrica revela thrashing?
Resposta: Recomputações repetidas dos mesmos tokens, associadas a transferências ou preempções, além de baixa progressão efetiva da geração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T105:C05 — mecanismo_avancado

Expulsar cache pode significar remover uma cópia reconstruível de prefixo inativo ou eliminar estados ainda necessários ao contexto de uma sequência. O primeiro caso muda custo; o segundo muda a função do modelo, salvo reconstrução antes do uso. Uma política de memória precisa declarar qual semântica pratica. Custo de reconstrução e probabilidade de reúso podem orientar retenção, mas são estimativas sujeitas a mudanças de carga.

Condição de contorno:
Uma política aparentemente econômica pode gerar thrashing quando estados expulsos são reconstruídos repetidamente antes de terminar a requisição.

Contrato proposto:
- Entradas: Pressão de memória, referências ativas, estimativas de reúso e custo de reconstrução.
- Saídas: Blocos removidos, bytes liberados e plano para futuros acessos.
- Estado: Disponibilidade física, histórico reconstruível e dependências dos consumidores.
- Invariante: Nenhum estado necessário desaparece silenciosamente do contexto lógico prometido.

Compromissos de projeto:
- Reter estados caros economiza cálculo futuro e limita admissões.
- Políticas sofisticadas custam metadados e podem reagir mal a estimativas desatualizadas.

## T105:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: forçar pressão durante duas continuações que compartilham um ancestral e acessá-lo novamente após remoção permitida. Esperar proteção de referências ativas ou reconstrução correta, sem contexto reduzido ocultamente.

Plano de avaliação proposto:
Plano proposto: comparar LRU e uma política baseada em custo sob sequências de acesso controladas. Medir bytes liberados, recomputação, misses, preempções e latência; escolher pelo custo total preservando a semântica contratada.

Comparações:
- T116 (complements): Recomputação pode restaurar estado removido quando o histórico necessário permanece disponível.

Afirmação rastreável:
O desenho de RadixAttention protege nós usados por requisições ativas e remove folhas elegíveis.
Suporte: direct; fontes: V3B-S011
Limite: A política documentada não representa todas as variantes de poda ou compressão de contexto.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T105:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou expulsão reconstruível de remoção semântica. Esta estratégia acrescenta custo de oportunidade, proteção durante transferências e experimentos que medem o prejuízo futuro da decisão.

Valor por recurso escasso
Uma política proposta estima benefício de reúso dividido pelo recurso que bloqueia: bytes de GPU, banda de restore ou espaço de armazenamento. O recurso dominante muda durante a carga. Um prefixo popular pode merecer retenção na RAM sem merecer GPU; usar somente frequência mistura decisões de níveis distintos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

Estados em trânsito
Evicção, cópia e cancelamento podem se cruzar. Dê a cada transferência uma referência temporária e um destino ainda não publicável; a remoção da origem só é segura quando existe cópia confirmada ou reconstrução possível. Contadores de referências devem sobreviver a retries e não depender exclusivamente do término normal do pedido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

Custo contrafactual
Conte misses causados por expulsão recente e tempo gasto em reconstrução, preservando uma amostra de decisões. Isso permite distinguir uma política agressiva demais de uma mudança genuína de demanda. Não atribua toda queda de hit rate à evicção: versões de templates, adapters e distribuição de usuários também alteram os prefixos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

USO AVANÇADO — Picos de conversas novas
Cenário: Uma campanha aumenta sessões sem histórico compartilhado.
Estratégia: Reduza retenção de prefixos inativos antes de limitar sequências em execução. Preserve uma margem para crescimento dos decodes e revise a pressão depois do pico.
Papel do modelo pequeno: Um 3–7B pode aceitar mais sessões sem alterar a semântica do contexto ativo.
Aceite proposto: Confirmar ausência de OOM e registrar reconstruções posteriores causadas pela intervenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

USO AVANÇADO — Cache com documentos sensíveis
Cenário: Uma fonte é revogada ou expira.
Estratégia: Propague invalidação por versão e domínio de acesso, tornando cópias antigas inelegíveis mesmo antes de sua remoção física. Não confunda liberação de memória com revogação lógica.
Papel do modelo pequeno: O modelo pequeno continua recebendo somente contexto autorizado na nova versão.
Aceite proposto: Testar revogação em GPU, RAM e armazenamento, incluindo transferências já iniciadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Use políticas simples quando o custo de manutenção superar o prefill evitado; não deduza isso só do número de parâmetros.
8–14B: Meça o conjunto de sessões simultâneas e o crescimento das respostas antes de reservar cache inativo.
15–30B: Uma política favorável ao reúso pode impedir o carregamento de novos pedidos grandes; trate capacidade como orçamento explícito.
Requisitos de treino/runtime: Runtime precisa expor referências, cancelamento e residência. Remover tokens do contexto requer método aproximado separado.
Não aplicar quando: Não expulsar estados ativos sem reconstrução antes do próximo uso.

## T105:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T105:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T105 → T084 [complements]
Como combinar: A validade de prefixos inclui expiração e revogação, além de pressão de memória.
Interface: Versão, domínio de acesso e marcador de invalidação.
Condição: Workers observam a mesma regra de elegibilidade.
Aceite proposto: Repetir um pedido após revogação e provar que não ocorreu reúso antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031, B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T105 → T086 [alternative]
Como combinar: Comparar compactação KV com evicção permite escolher entre perda numérica e recomputação.
Interface: Bytes liberados, erro observado e custo de restore.
Condição: Experimentos separam as duas intervenções.
Aceite proposto: Conferir qualidade e latência em ensaios isolados e depois combinados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031, B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contabilizar memória ainda referenciada como capacidade imediatamente recuperada.
- Simular cancelamento durante cópia e reinício do worker com restauração incompleta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A política deve ser comparada pelo custo de servir respostas válidas, incluindo reconstrução. Aumentar cache hit não estabelece vantagem de qualidade frente a um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T093, T104, T116

## Fontes primárias associadas

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S011 — SGLang: Efficient Execution of Structured Language Model Programs — full text

[https://arxiv.org/html/2312.07104v2](https://arxiv.org/html/2312.07104v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention, busca de prefixos e ciclo de vida/remoção de cache em árvore.

Limite: Texto do projeto consultado; não representa garantia de compatibilidade de implantação ou reprodução de resultados.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

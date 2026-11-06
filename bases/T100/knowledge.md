# T100 — Grouped-Query Attention — GQA

**Nome canônico:** Grouped-Query Attention — GQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T100  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** grouped-query attention; atenção com consultas agrupadas

## T100:C01 — conceito

Arquitetura intermediária entre MHA e MQA: grupos de cabeças de consulta compartilham cabeças KV. Reduz o volume de KV sem usar necessariamente uma única cabeça compartilhada. O número de grupos é característica do checkpoint; o artigo de referência também investiga conversão com treinamento adicional.

Como funciona:
- Projetar várias cabeças de consulta e um conjunto menor de cabeças KV.
- Associar cada grupo de consultas à cabeça KV correspondente.
- Executar a atenção preservando esse mapeamento em treino e inferência.

## T100:C02 — aplicacao

Quando usar:
- Modelos precisam equilibrar capacidade da atenção e custo de decode.
- Planejamento de memória de um checkpoint que já utiliza GQA.

Quando não usar:
- Interpretar GQA como solução de cache que pode ser ativada sem mudar um checkpoint MHA incompatível.

Implementação proposta:
- Registrar num_attention_heads, num_key_value_heads e dimensão de cada cabeça.
- Estimar KV convencional como aproximadamente 2 × camadas × tokens × cabeças_KV × dimensão × bytes, ajustando arquitetura e batch.
- Medir memória real, pois alinhamento, paginação e outros estados alteram a estimativa.

Aplicação LAI proposta:
Proposta LAI: incluir o número real de cabeças KV no cálculo de concorrência do modelo local, em vez de estimar apenas pelo total de parâmetros.

## T100:C03 — riscos_validacao

Armadilhas:
- A divisão de cabeças precisa respeitar requisitos do modelo e kernel.
- A fórmula convencional não cobre automaticamente arquiteturas híbridas, compressão latente ou todas as camadas locais.

Métricas sugeridas:
- Memória observada versus estimativa para diferentes comprimentos.
- Latência de decode e acerto de tarefas do checkpoint.

Testes propostos:
- Conferir mapeamento de grupos com uma implementação de referência.
- Aumentar contexto e batch e verificar se a projeção de capacidade prevê a saturação.

## T100:C04 — perguntas_proveniencia

Pergunta: GQA é igual a MQA?
Resposta: MQA representa o caso de uma cabeça KV; GQA geralmente usa um número intermediário de grupos.

Pergunta: GQA reduz a quantidade de tokens de entrada?
Resposta: Não. Reduz parte dos estados por token, mantendo a sequência.

Pergunta: Mudar Hkv no arquivo de configuração basta?
Resposta: Não. Formas e significado dos pesos precisam corresponder; editar metadados não produz pesos corretamente adaptados.

Pergunta: Por que medir memória por GPU?
Resposta: A redução lógica pode ser parcialmente anulada por replicação necessária ao particionamento ou por expansões introduzidas no kernel.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T100:C05 — mecanismo_avancado

Com Hq consultas e Hkv grupos KV, cada consulta precisa apontar para o grupo correto. Nas configurações uniformes comuns, Hq é múltiplo de Hkv; o layout físico pode ainda repartir ou replicar grupos entre dispositivos. O número intermediário de grupos permite ajustar memória e diversidade de representação, mas constitui escolha de arquitetura e de pesos, não apenas uma política de alocação de cache.

Condição de contorno:
Uma implementação que expande materialmente todas as cabeças pode manter correção e perder parte da economia pretendida.

Contrato proposto:
- Entradas: Configuração de cabeças, pesos treinados ou adaptados e mapa consulta-grupo.
- Saídas: Saídas das consultas e cache com agrupamento consistente.
- Estado: Layout KV, shard por dispositivo e eventual replicação declarada.
- Invariante: O mesmo mapa de grupos é preservado no carregamento, prefill e decode.

Compromissos de projeto:
- Mais grupos podem aumentar diversidade e custo de cache.
- Distribuição entre GPUs pode introduzir replicação quando grupos não se repartem adequadamente.

## T100:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: permutar duas associações de grupos somente no decode. Comparar logits com prefill e referência expandida; a transição deve revelar a inconsistência.

Plano de avaliação proposto:
Plano proposto: primeiro comparar kernels com pesos idênticos; depois comparar arquiteturas com treinamento e avaliação controlados. Medir qualidade, bytes físicos por dispositivo e tempos de prefill/decode; aceitar a troca segundo o orçamento definido para a aplicação.

Comparações:
- T099 (alternative): MQA é o extremo com um grupo KV; GQA preserva múltiplos grupos.

Afirmação rastreável:
O trabalho de GQA apresenta grupos KV intermediários e uma receita de adaptação de checkpoints multi-head.
Suporte: direct; fontes: B-S019
Limite: Os resultados de adaptação do artigo não garantem qualidade de uma conversão arbitrária ou sem treinamento.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T100:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou mapeamento entre consultas e grupos. Esta ficha trata GQA na seleção de modelos e no planejamento distribuído, incluindo validação de layouts e separação entre mudança arquitetural, implementação de kernel e qualidade do checkpoint.

Grupos como restrição de implantação
Use números de heads Q/KV para verificar divisibilidade e estratégia de particionamento admitida pelo runtime. Quando grupos não se distribuem uniformemente, o backend pode replicar ou restringir TP. Essa escolha afeta memória e comunicação; valide antes de reservar máquinas com uma divisão que o modelo não suporta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

Conversão com orçamento completo
O trabalho de GQA investiga adaptação de checkpoints, mas isso não torna conversão gratuita. Planeje dados, treinamento adicional, validação e artefatos de rollback. Para um projeto aplicado, escolher um checkpoint já treinado com GQA pode ser mais simples; compare essa opção antes de investir em modificar arquitetura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

Qualidade versus implementação
Teste primeiro se o kernel preserva o mapeamento correto; depois avalie a qualidade do modelo. Um bug de expansão ou shard pode parecer perda inerente de GQA. Use referência que materializa grupos para comparar numericamente, mesmo que seja lenta, e só use o caminho compacto no serving após equivalência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

USO AVANÇADO — Servidor com memória limitada
Cenário: É necessário escolher entre modelos de porte semelhante.
Estratégia: Compare tarefas reais, tamanho de cache por comprimento e suporte do executor. Dê preferência ao candidato que entrega qualidade dentro do SLO, não ao menor número de grupos isoladamente. Registre tokenizer e treino como fatores de confusão.
Papel do modelo pequeno: Um 8–14B GQA pode oferecer equilíbrio útil entre cache e qualidade, sujeito a teste.
Aceite proposto: Aprovar por custo por resposta aceita e regressões por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

USO AVANÇADO — Portabilidade entre runtimes
Cenário: O checkpoint muda de biblioteca sem trocar pesos.
Estratégia: Valide ordem de heads, reshape e offsets com entradas curtas e longas. Compare prefill e decode separadamente. Se a nova biblioteca expande KV permanentemente, registre perda de memória mesmo quando as saídas permanecem corretas.
Papel do modelo pequeno: Um 3–30B precisa conservar o compartilhamento no layout físico para obter a economia pretendida.
Aceite proposto: Exigir erro numérico tolerado e bytes KV compatíveis com o layout documentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, uma arquitetura já treinada com GQA permite experimentar baixo custo sem projeto de conversão.
8–14B: Em 8–14B, verificar qualidade por tarefa e eficiência do kernel antes de escolher o número de grupos.
15–30B: Em 15–30B, planejar TP pelo layout KV e possíveis réplicas, não só pelo tamanho das matrizes.
Requisitos de treino/runtime: A escolha de grupos pertence ao checkpoint; implementar compartilhamento é runtime, converter grupos exige adaptação.
Não aplicar quando: Não comparar modelos diferentes e atribuir toda diferença de desempenho exclusivamente a GQA.

## T100:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Tabela Q/KV documenta agrupamento nas variantes pertinentes.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005, V4B-Q016.

## T100:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T100 → T106 [feeds]
Como combinar: Fornecer o layout por camada para dimensionar cache e admissão.
Interface: Heads Q/KV, dimensões, dtype e política de retenção.
Condição: Configuração corresponde à revisão carregada.
Aceite proposto: Conferir estimativa com memória real por sequência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T100 → T090 [complements]
Como combinar: Executar atenção agrupada com backend fundido que preserve compartilhamento.
Interface: Q com múltiplas heads e KV agrupado.
Condição: Kernel suporta GQA sem expansão persistente desnecessária.
Aceite proposto: Comparar com referência expandida e medir temporários.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar correspondência de grupos após conversão de pesos e sharding.
- Manter referência numérica independente do caminho otimizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas específicas contra a fronteira sob orçamento total equivalente. GQA ajuda eficiência arquitetural, mas não permite concluir que um modelo pequeno alcança capacidades gerais de outro maior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T106, T108

## Fontes primárias associadas

### B-S019 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

[https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grupos de consultas compartilham cabeças KV; conversão proposta envolve treinamento.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

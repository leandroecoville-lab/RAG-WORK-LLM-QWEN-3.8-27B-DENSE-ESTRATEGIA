# T117 — Context Parallelism

**Nome canônico:** Context Parallelism  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T117  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** paralelismo de contexto

## T117:C01 — conceito

Distribui o processamento de uma mesma sequência entre dispositivos, particionando a dimensão de contexto. É útil quando ativações e estados de uma entrada extensa ultrapassam a capacidade local. Não deve ser confundido com enviar documentos independentes a agentes paralelos ou com tensor parallelism.

Como funciona:
- Dividir posições da sequência mantendo identidade posicional global.
- Executar operações locais e comunicar dependências de atenção entre partições.
- Combinar resultados de forma consistente com o modelo completo.

## T117:C02 — aplicacao

Quando usar:
- Treino ou inferência suportada precisa processar uma sequência muito extensa.
- Há múltiplos dispositivos e interconexão adequada à comunicação.

Quando não usar:
- A carga é pequena e comunicação custa mais que o cálculo distribuído.

Implementação proposta:
- Definir se o runtime particiona prefill, decode, ativações ou KV, pois implementações diferem.
- Verificar interação com TP, PP e máscaras do modelo.
- Começar em entrada que caiba numa GPU para criar referência numérica.

Aplicação LAI proposta:
Proposta LAI: considerar após demonstrar necessidade de uma sequência maior que a capacidade local; RAG e contexto seletivo continuam alternativas de aplicação.

## T117:C03 — riscos_validacao

Armadilhas:
- Context parallelism não cria capacidade posicional ausente no checkpoint.
- Sequence parallelism pode nomear divisão de apenas certas ativações; os termos não são universalmente intercambiáveis.

Métricas sugeridas:
- Memória por GPU, tráfego e eficiência de escala.
- Tempo por sequência e desequilíbrio entre partições.

Testes propostos:
- Comparar saída distribuída e referência local em comprimentos e partições variados.
- Testar posições que atravessam fronteiras de partição e preservar causalidade.

## T117:C04 — perguntas_proveniencia

Pergunta: É simplesmente aumentar max_model_len?
Resposta: Não. Exige distribuição real de estados e operações, além de compatibilidade do modelo.

Pergunta: Uma GPU usa context parallelism entre seus agentes?
Resposta: Não nesse sentido distribuído; agentes paralelos e partição de uma sequência são mecanismos distintos.

Pergunta: CP é igual a TP?
Resposta: Não. CP divide posições do contexto; TP divide operações ou parâmetros dentro das camadas, podendo coexistir.

Pergunta: Mais contexto distribuído prova melhor compreensão?
Resposta: Não. A capacidade de executar a sequência e a capacidade do modelo de utilizar informação distante precisam ser avaliadas separadamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T117:C05 — mecanismo_avancado

Particionar o eixo de contexto muda a localização de ativações e dependências de atenção, mas posições continuam pertencendo a uma sequência global. Uma partição causal ingênua pode deixar os primeiros segmentos com menos trabalho que os últimos, pois há menos passado permitido. Balanceamento precisa considerar conexões efetivamente calculadas, além de distribuir quantidades iguais de tokens. Comunicação torna acessíveis estados que residem em outras partições.

Condição de contorno:
Dividir contexto entre dispositivos não significa que cada trecho possa ser executado independentemente sem combinar dependências.

Contrato proposto:
- Entradas: Sequência, partição por posições, plano de comunicação e máscara global.
- Saídas: Representações locais equivalentes ao modelo não particionado.
- Estado: Mapas de posições, ativações por camada e buffers de troca.
- Invariante: Cada consulta recebe exatamente as chaves permitidas na sequência global.

Compromissos de projeto:
- Mais dispositivos reduzem memória local e introduzem transferências e sincronizações.
- Balancear tokens pode não balancear cálculo sob máscaras causais.

## T117:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repartir sequência causal em segmentos desiguais e verificar tokens nas fronteiras. Comparar com referência única e registrar o trabalho por dispositivo para detectar desequilíbrio.

Plano de avaliação proposto:
Plano proposto: controlar pesos, comprimento, dtype e máscara, medindo memória por dispositivo, comunicação exposta e duração. Comparar capacidade e velocidade separadamente; aprovar somente quando a divisão atende ao objetivo sem alterar os resultados.

Comparações:
- T101 (complements): Ring Attention pode realizar a troca de blocos em uma implementação de contexto distribuído.

Afirmação rastreável:
O guia Megatron distingue context parallelism, aplicado às ativações de todas as camadas, de sequence parallelism em camadas específicas.
Suporte: direct; fontes: B-S045
Limite: A terminologia depende do framework; suporte de treinamento não implica caminho idêntico no servidor de inferência.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T117:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou posições e balanceamento causal. Esta camada considera quando paralelizar contexto é apropriado, como interage com GQA e quais aspectos de implantação foram efetivamente descritos pelos operadores.

Escopo de aplicação
Context parallelism ajuda a distribuir trabalho ou estados associados ao comprimento, especialmente em prefill longo. Decode com uma consulta nova possui outra relação entre computação e comunicação. Uma topologia adequada para uma fase não precisa ser mantida em todas; qualquer transição deve considerar redistribuição do estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

Partição composta
Combinar contexto e tensor parallelism cria eixos de comunicação distintos. Registre qual grupo possui cada posição e cada conjunto de cabeças, incluindo réplicas KV quando necessário. Uma redução de memória por eixo não se multiplica automaticamente pela outra se buffers ou estados forem replicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

Evidência operacional delimitada
Meta descreve caminhos de paralelismo de contexto em sua infraestrutura e Amazon descreve prefill distribuído no Rufus. Esses relatos sustentam viabilidade operacional nas configurações publicadas, sem demonstrar benefício para um 3–30B ou para a interconexão local. A política precisa ser reavaliada no tamanho de contexto realmente usado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Contexto excepcionalmente longo
Cenário: Poucos pedidos ultrapassam o orçamento de uma réplica.
Estratégia: Crie uma classe de execução distribuída e mantenha pedidos comuns no caminho simples. Inclua tempo de formar grupo e mover estado no orçamento da solicitação.
Papel do modelo pequeno: Um 15–30B pode precisar dessa classe por comprimento, mesmo cabendo em pesos numa GPU.
Aceite proposto: Validar equivalência e medir espera da classe longa sem bloquear consultas curtas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Estudo de seleção de topologia
Cenário: A carga mistura documentos e conversas curtas.
Estratégia: Compare réplicas, TP e CP em entradas estratificadas por comprimento. Evite concluir a partir do maior contexto suportado, que pode ser raro.
Papel do modelo pequeno: Modelos 8–14B oferecem uma faixa útil para avaliar se comunicação supera a economia.
Aceite proposto: Escolher pelo conjunto real de chegadas e respostas válidas dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: CP pode ser excesso de complexidade para contextos usuais; testar réplica inteira primeiro.
8–14B: Considere CP apenas quando comprimento ou throughput de prefill justificam múltiplos dispositivos.
15–30B: Modele partição por camada e comunicação, incluindo o espaço necessário para buffers.
Requisitos de treino/runtime: Runtime e kernels devem suportar a arquitetura e topologia. Não exige novo treino se a operação for equivalente.
Não aplicar quando: Não usar CP como promessa de aumentar a janela treinada ou a capacidade de compreender contexto distante.

## T117:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: O prefill divide entrada pela dimensão de sequência.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Particionamento de contexto é explicitamente implementado.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003, V4B-Q004.

## T117:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T117 → T101 [complements]
Como combinar: Troca de blocos em anel é uma possível implementação do eixo de contexto.
Interface: Posições, blocos KV e estatísticas parciais.
Condição: Máscara global e ordenação corretas.
Aceite proposto: Comparar contra atenção não particionada em comprimentos variados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T117 → T118 [complements]
Como combinar: Os eixos de contexto e tensor podem compor uma malha.
Interface: Mapa de posições, shards e grupos de coletivas.
Condição: Interconexão e divisibilidade sustentam o plano.
Aceite proposto: Medir buffers replicados e custo de comunicação por fase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar distribuição causal desbalanceada e comprimentos não divisíveis.
- Não atribuir prefill distribuído automaticamente a todas as fases ou versões de um produto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira precisa igualar contexto útil e medir compreensão. Distribuir uma sequência permite executá-la; não prova que o modelo pequeno aproveita todas as informações presentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T101, T118, T119, T169

## Fontes primárias associadas

### B-S045 — Parallelisms Guide — Megatron Bridge

[https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html](https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Context parallelism particiona dimensão de sequência; distinto do sequence parallelism descrito no guia.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S020 — Ring Attention with Blockwise Transformers for Near-Infinite Context

[https://arxiv.org/abs/2310.01889](https://arxiv.org/abs/2310.01889)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sequência distribuída e circulação de blocos KV com computação sobreposta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

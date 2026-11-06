# T118 — Tensor Parallelism

**Nome canônico:** Tensor Parallelism  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T118  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** paralelismo tensorial

## T118:C01 — conceito

Divide matrizes e operações de uma camada entre dispositivos, que cooperam para produzir o resultado da mesma inferência. Ajuda a acomodar modelos maiores ou acelerar operações suficientemente grandes, mas adiciona comunicação frequente. Não agrega VRAM como memória uniforme sem custo.

Como funciona:
- Particionar parâmetros e operações segundo um plano consistente.
- Calcular partes da mesma camada em paralelo.
- Realizar coletivas ou trocas necessárias para combinar resultados entre camadas.

## T118:C02 — aplicacao

Quando usar:
- Modelo não cabe em um dispositivo e o runtime suporta particionamento.
- Interconexão e tamanho das operações permitem amortizar comunicação.

Quando não usar:
- Modelo cabe numa GPU e a comunicação lenta supera o trabalho que seria dividido.

Implementação proposta:
- Registrar topologia física e benchmark de coletivas antes de escolher o grau de TP.
- Checar divisibilidade de cabeças, dimensões e suporte à quantização.
- Comparar TP com réplicas independentes quando a meta principal for atender mais usuários.

Aplicação LAI proposta:
Proposta LAI: antes de comprar outra GPU, comparar benefício para um modelo particionado versus dois workers e medir a interconexão disponível.

## T118:C03 — riscos_validacao

Armadilhas:
- Duas GPUs podem aumentar capacidade sem reduzir a latência individual.
- Interconexão PCIe ou rede pode virar o gargalo a cada token.

Métricas sugeridas:
- Tempo de coletivas, memória por dispositivo e tokens por segundo.
- Latência por usuário e goodput com capacidade total equivalente.

Testes propostos:
- Comparar logits contra modelo sem partição em caso que caiba na referência.
- Aumentar grau de TP e verificar se ganhos superam comunicação; registrar regressões.

## T118:C04 — perguntas_proveniencia

Pergunta: TP é igual a usar dois modelos diferentes?
Resposta: Não. Dispositivos cooperam no mesmo modelo e na mesma passagem.

Pergunta: Posso somar a VRAM e ignorar rede?
Resposta: Não. Pesos e estados podem ser divididos, mas a comunicação e buffers fazem parte do custo.

Pergunta: Dividir por duas GPUs divide a latência por dois?
Resposta: Não. Comunicação, partes não paralelizáveis e formas menores alteram o custo.

Pergunta: Como validar um checkpoint repartido?
Resposta: Reconstrua ou compare a função global em exemplos controlados, conferindo offsets e orientação das matrizes, não apenas seus tamanhos.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T118:C05 — mecanismo_avancado

Uma multiplicação linear pode ser repartida por colunas de saída ou por dimensões contraídas de entrada. No segundo caso, os produtos parciais precisam ser somados; no primeiro, o consumidor pode operar com saídas repartidas ou exigir reunião posterior. A localização das coletivas determina custo e dependências. Mais shards reduzem a parte de pesos por dispositivo, mas podem tornar a comunicação dominante em pequenos lotes.

Condição de contorno:
Dimensões, cabeças e grupos KV nem sempre são divisíveis pelo grau escolhido sem padding, replicação ou implementação específica.

Contrato proposto:
- Entradas: Pesos, plano de shards, topologia e convenções das coletivas.
- Saídas: Saída equivalente à camada completa, repartida ou reunida conforme o próximo operador.
- Estado: Mapa global de parâmetros, grupos de comunicação e buffers parciais.
- Invariante: Cada contribuição é somada ou concatenada uma única vez, na ordem semântica correta.

Compromissos de projeto:
- Maior grau reduz memória de pesos local e aumenta sincronização.
- Sobrepor comunicação ajuda apenas quando existem operações independentes suficientes.

## T118:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: carregar uma fatia de pesos na posição errada e atrasar um participante da coletiva. Esperar divergência detectada no primeiro caso e timeout controlado no segundo.

Plano de avaliação proposto:
Plano proposto: comparar graus de paralelismo com modelo e orçamento total explícitos. Medir memória, tempo de coletivas, prefill e decode por lote; escolher pela capacidade e latência reais, evitando inferir speedup linear.

Comparações:
- T119 (complements): Particionar dentro da camada pode coexistir com distribuição de conjuntos de camadas em estágios.

Afirmação rastreável:
Megatron-LM apresenta paralelismo intra-camada com operações de comunicação para combinar o trabalho distribuído.
Suporte: direct; fontes: B-S030
Limite: A receita do artigo é uma arquitetura de treinamento; cada implementação de inferência precisa validar seu plano.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T118:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou shards e coletivas. A nova camada aborda seleção econômica do grau de paralelismo, consistência de carregamento e comportamento quando o conjunto de dispositivos deixa de progredir junto.

Paralelismo mínimo suficiente
Mais shards podem permitir carregar pesos e reduzir computação local, mas acrescentam sincronizações. Compare o menor grau que atende memória com graus maiores sob a carga real. Para modelos que cabem inteiros, réplicas podem oferecer melhor capacidade total, enquanto TP pode ser útil para um prazo individual específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

Carregamento verificável
Uma distribuição errada de pesos pode produzir tensores válidos e resultados incorretos. Versione o plano de shards, nomes, offsets e configuração de quantização. Confirme checksums dos artefatos e compare camadas selecionadas com uma referência não distribuída, especialmente após conversões de layout.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

Falha e progresso
Uma coletiva atrasada pode prender todo o grupo. A saúde de uma GPU isolada não prova saúde da réplica distribuída. Observe progresso de passos, watchdogs e falhas de comunicação; ao reiniciar, trate o conjunto como unidade consistente e reconstrua cache a partir de estado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Modelo que excede uma GPU
Cenário: O checkpoint especializado precisa de mais memória de pesos.
Estratégia: Escolha topologia com comunicação adequada, distribua pesos e reserve espaço para KV e temporários. Não ocupe toda a memória só porque a divisão dos pesos parece caber.
Papel do modelo pequeno: Um 15–30B pode usar TP quando quantização adequada não atende o objetivo.
Aceite proposto: Carregar, completar contexto alvo e manter qualidade e latência sob concorrência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Menor latência por pedido
Cenário: Uma única réplica atende pouco tráfego, mas há prazo rígido.
Estratégia: Compare TP com réplica inteira usando lote pequeno, incluindo sincronização. Se TP não reduzir o caminho crítico, prefira capacidade independente.
Papel do modelo pequeno: Um 8–14B deve justificar a distribuição por medição, não por associação com infraestrutura de bigtech.
Aceite proposto: Medir percentis de latência e custo reservado por resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, comunicação e overhead podem dominar; réplicas independentes são uma hipótese inicial.
8–14B: Teste divisibilidade de cabeças e layouts quantizados antes de escolher o grau.
15–30B: Inclua falha conjunta, buffers e KV no dimensionamento; pesos são apenas uma parcela.
Requisitos de treino/runtime: Runtime distribuído, coletivas e checkpoint compatíveis; TP preserva a arquitetura quando implementado corretamente.
Não aplicar quando: Não inferir aceleração a partir da quantidade de GPUs nem da soma nominal de suas capacidades.

## T118:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Tensor parallelism integra as estratégias híbridas descritas.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: Atenção usa tensor parallelism no deployment descrito.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: O operador descreve implementação e otimização de tensor parallelism.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003, V4B-Q004.

## T118:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T118 → T117 [complements]
Como combinar: Contexto e tensor podem ser particionados em eixos diferentes.
Interface: Malha e propriedade de tensores.
Condição: Plano consistente em todas as camadas.
Aceite proposto: Comparar memória real com estimativa e validar resultados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S030, B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T118 → T122 [complements]
Como combinar: Interconexão de baixa sobrecarga pode transportar dados das coletivas quando suportada.
Interface: Buffers, grupos e eventos de conclusão.
Condição: Stack e topologia efetivamente habilitam o caminho.
Aceite proposto: Medir comunicação e testar falhas sem consumidores de dados parciais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S030, B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checar versões e layouts idênticos em todos os ranks.
- Não servir resultados de um grupo com estado divergente após recuperação parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
TP pode tornar um modelo especializado executável ou mais rápido, sem alterar sua competência. Compare custo por tarefa concluída e inclua recursos ociosos reservados ao grupo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T117, T119, T122, T107

## Fontes primárias associadas

### B-S030 — Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

[https://arxiv.org/abs/1909.08053](https://arxiv.org/abs/1909.08053)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Paralelismo dentro de camadas, complementar ao pipeline.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S045 — Parallelisms Guide — Megatron Bridge

[https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html](https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Context parallelism particiona dimensão de sequência; distinto do sequence parallelism descrito no guia.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

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

### V4D-S014 — Profiling Data in DeepSeek Infra

[https://github.com/deepseek-ai/profile-data/blob/main/README.md](https://github.com/deepseek-ai/profile-data/blob/main/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descrição de sobreposição computação/comunicação, RDMA e configurações ligadas ao deployment online V3/R1.

Limite: Os traces publicados simulam roteamento MoE perfeitamente balanceado; não são reprodução integral de tráfego real. EP32/EP128 deste perfil e EP32/EP320 do relatório são contextos/revisões diferentes.

### V4D-S015 — DeepSeek-V3 Technical Report — v2

[https://arxiv.org/html/2412.19437v2](https://arxiv.org/html/2412.19437v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seção 3.4 descreve deployment de inferência com prefill/decode separados, TP/EP e redundância de especialistas guiada por carga.

Limite: Modelo de 671B totais, fora de 3–30B. Custos publicados de treino não incluem toda a pesquisa. MTP especulativo avaliado não prova ativação em todo serviço online.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

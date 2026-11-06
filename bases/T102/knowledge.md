# T102 — Disaggregated Inference / Disaggregated Prefill-Decode

**Nome canônico:** Inferência com prefill e decode desagregados  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T102  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Disaggregated Inference / Prefill-Decode; prefill-decode disaggregation; inferência desagregada; Disaggregated Prefill-Decode; PD disaggregation

## T102:C01 — conceito

Disaggregated Inference, no escopo desta ficha, separa prefill e decode em instâncias ou conjuntos de recursos distintos. Prefill processa a entrada e produz estados KV; decode reutiliza esses estados para gerar tokens. A arquitetura permite ajustar capacidade e latência por fase, mas acrescenta transferência, coordenação e compatibilidade de estados. Separar recursos não demonstra ganho automático de throughput.

Como funciona:
- Encaminhar a entrada para um worker de prefill e produzir o KV correspondente à sequência tokenizada.
- Transferir ou disponibilizar o KV por um conector compatível e encaminhar a continuação ao worker de decode.
- Dimensionar os grupos considerando filas, comprimento de entrada, duração da geração e custo da interconexão.

## T102:C02 — aplicacao

Quando usar:
- Cargas mistas nas quais prompts longos interferem no intervalo entre tokens de gerações já em andamento.

Quando não usar:
- Quando o custo de movimentar KV supera o benefício, há pouca concorrência ou o backend não suporta a configuração pretendida.

Implementação proposta:
- Proposta: medir uma instalação integrada como baseline e separar TTFT, latência entre tokens, transferência de KV e filas de cada fase.
- Fixar revisão de pesos, tokenizer, tokens de entrada, dtype e layout compatíveis; validar também adaptadores e opções de paralelismo.
- Definir timeout e limpeza para transferência incompleta e cancelamento; liberar buffers que perderam seu consumidor.
- Comparar desagregação com chunked prefill sob a mesma carga antes de escolher a topologia.

Aplicação LAI proposta:
Proposta LAI: avaliar desagregação apenas depois de medir interferência entre fases e validar o conector no hardware escolhido; não há implantação demonstrada neste corpus.

## T102:C03 — riscos_validacao

Armadilhas:
- Repetir tokenização ou usar revisões diferentes pode tornar o KV inválido.
- Um grupo ocioso e outro saturado elevam custo sem reduzir latência; tráfego de KV pode virar gargalo.

Métricas sugeridas:
- TTFT e ITL p95/p99, bytes e tempo de transferência, utilização de cada pool e custo por solicitação completa.

Testes propostos:
- Teste proposto: comparar saídas equivalentes com execução integrada e rastrear IDs de sequência através da transferência.
- Interromper a conexão durante envio de KV e confirmar falha explícita, limpeza e ausência de continuação com estado incorreto.

## T102:C04 — perguntas_proveniencia

Pergunta: Desagregar significa executar duas cópias completas da mesma geração?
Resposta: Não. As fases são separadas e compartilham os estados necessários; duplicar o trabalho eliminaria parte do benefício esperado.

Pergunta: O recurso do vLLM promete mais throughput?
Resposta: A documentação consultada o apresenta para ajustar TTFT e ITL e declara que não melhora throughput; resultados de outras arquiteturas exigem medição própria.

Pergunta: Goodput é igual a tokens por segundo?
Resposta: Não. Aqui interessa trabalho concluído atendendo aos prazos definidos, não apenas produção bruta.

Pergunta: É suficiente enviar o tensor?
Resposta: Não. O destino também precisa saber posições, formas, dtype, identidade dos pesos e qual continuação aquele estado representa.

Escopo das fontes:
vLLM fundamenta a separação e suas limitações; Dynamo apoia gestão de KV. Topologia e testes são propostas.

## T102:C05 — mecanismo_avancado

A separação de fases introduz uma transferência de propriedade do estado KV. Como proposta de contrato, o worker de decode só deve iniciar após receber todos os segmentos necessários e verificar identidade, comprimento e layout. O tempo mínimo de transporte inclui bytes divididos pela banda efetiva, além de latência e serialização. Separar filas permite alocação diferente para prefill e decode, mas não elimina essa conta.

Condição de contorno:
Quando prompts são pequenos ou o transporte é caro, a perda de localidade pode superar a redução de interferência entre fases.

Contrato proposto:
- Entradas: Tokens processados, estado KV versionado, destino e configuração compatível dos workers.
- Saídas: Confirmação de transferência e ponto de continuação inequívoco.
- Estado: Manifesto de segmentos, offsets recebidos e proprietário atual do pedido.
- Invariante: Decode nunca usa cache parcial nem mistura segmentos de revisões distintas.

Compromissos de projeto:
- Pools independentes permitem dimensionar fases conforme suas cargas.
- Transferência adiciona falhas parciais, memória transitória e pressão na rede.

## T102:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o envio após algumas camadas e duplicar uma confirmação. Esperar retomada idempotente ou reconstrução explícita, sem geração baseada em estado incompleto.

Plano de avaliação proposto:
Plano proposto: comparar colocação conjunta e separada com mesmos recursos totais e chegadas. Medir TTFT, tempo por token, goodput dentro dos prazos e tráfego KV; aceitar somente quando os objetivos conjuntos melhoram no cenário real.

Comparações:
- T122 (complements): RDMA pode reduzir custos de transferência, mas não substitui o contrato de consistência.

Afirmação rastreável:
DistServe separa prefill e decode e considera banda de comunicação ao escolher alocação e posicionamento.
Suporte: direct; fontes: V3B-S010
Limite: O estudo não garante benefício com qualquer rede ou número de GPUs.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T102:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu entrega íntegra do KV antes do decode. A expansão aborda filas independentes, transferência por camada, cancelamento e ponto de equilíbrio, para dimensionar a arquitetura por demanda real e não por promessa abstrata de separação.

Capacidade em duas filas
Estime chegadas de tokens de entrada e de saída separadamente. Um pool de prefill rápido pode inundar decode com estados que não cabem; um pool de decode amplo pode ficar ocioso se não receber prompts prontos. Use controle de admissão que considere vagas no destino antes de produzir KV caro de transportar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

Transferência progressiva
Um sistema pode começar a transferir camadas já prontas enquanto o restante do prefill executa, como no relato da Perplexity. A aplicação precisa de manifesto e confirmação por segmento, com início do decode condicionado à prontidão exigida. Sobreposição reduz espera possível, mas não elimina bytes nem necessidade de consistência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

Cancelamento e propriedade
Se o cliente cancelar durante transporte, coordene liberação na origem e no destino. Uma confirmação tardia não pode reativar a requisição. Use identificador de tentativa e geração do estado para impedir que uma transferência antiga seja anexada a uma repetição posterior do mesmo pedido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

USO AVANÇADO — Entradas longas e saídas interativas
Cenário: Prefills extensos interrompem frequentemente o streaming.
Estratégia: Compare chunked prefill local com pools separados. Inclua banda, buffers, filas e falhas no ensaio. Escolha separação apenas se aumentar tarefas dentro do SLO; alocar mais máquinas sem igualar custo não demonstra superioridade da arquitetura.
Papel do modelo pequeno: Um 15–30B pode justificar separação em volume alto, sem que isso seja necessário em um único servidor.
Aceite proposto: Aprovar por goodput e custo completo, com TTFT e intervalos de saída separados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

USO AVANÇADO — Fleet com recursos diferentes
Cenário: Há dispositivos adequados a cálculo e outros com maior memória disponível.
Estratégia: Planeje perfis de prefill/decode compatíveis em pesos, layout e dtype. Valide transferência antes de experimentar hardware heterogêneo. Se for necessária conversão de KV, meça erro e tempo; não suponha interoperabilidade binária.
Papel do modelo pequeno: Um 3–14B só merece essa complexidade se demanda e custo de fila compensarem.
Aceite proposto: Exigir continuidade numérica e recuperação sem duplicação após falha de worker.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, começar pelo serviço agregado; overhead de transporte pode superar interferência evitada.
8–14B: Em 8–14B, avaliar separação apenas após medir mistura de comprimentos e demanda sustentada.
15–30B: Em 15–30B, perfilar crescimento KV e dimensionar pools pela distribuição de entrada/saída.
Requisitos de treino/runtime: Requer runtime/conector compatíveis, transferência de estados e coordenação; não altera pesos nem competência do modelo.
Não aplicar quando: Não adotar em baixa demanda apenas por ser usado em infraestruturas de grande escala.

## T102:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: A seção de deployment separa explicitamente prefill e decoding.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: A descrição operacional separa clusters de prefill e decode.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: Separação de pools e transporte de KV são descritos na implementação do operador.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003.

## T102:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T102 → T122 [complements]
Como combinar: Transferir KV por camada com conclusão observável antes do consumo.
Interface: Páginas KV, metadados e sinalização entre workers.
Condição: Caminho RDMA e registro de memória são suportados.
Aceite proposto: Medir transporte e impedir decode com estado parcial.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S002. Casos: V4B-C002.

2. T102 → T094 [alternative]
Como combinar: Reduzir interferência mantendo fases no mesmo worker quando transporte não compensa.
Interface: Orçamento de chunks e SLO por fase.
Condição: Runtime local consegue intercalar trabalho corretamente.
Aceite proposto: Comparar custo igualado e caudas nas mesmas chegadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S010, V4B-S002, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Impor backpressure quando decode não possui capacidade para novo KV.
- Testar cancelamento, replay e transferência atrasada com IDs de tentativa diferentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar responsividade de uma tarefa contra a fronteira incluindo todos os nós e rede. Separação pode melhorar eficiência do serviço; não amplia conhecimento, raciocínio ou precisão do checkpoint.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T094, T120, P009

## Fontes primárias associadas

### B-S021 — Disaggregated Prefilling (experimental)

[https://docs.vllm.ai/en/latest/features/disagg_prefill/](https://docs.vllm.ai/en/latest/features/disagg_prefill/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de prefill e decode em instâncias; ajuste independente de latências; recurso experimental na página consultada.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S010 — DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

[https://arxiv.org/abs/2401.09670](https://arxiv.org/abs/2401.09670)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interferência entre prefill/decode, objetivos TTFT/TPOT e alocação considerando banda de comunicação.

Limite: Resumo consultado; regras de transferência e testes de falha das fichas são propostas editoriais.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

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

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

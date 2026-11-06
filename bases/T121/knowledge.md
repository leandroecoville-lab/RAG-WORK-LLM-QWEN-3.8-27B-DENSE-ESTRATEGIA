# T121 — GPU Scheduling

**Nome canônico:** GPU Scheduling  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T121  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento de GPU

## T121:C01 — conceito

Família de políticas que decide qual trabalho ocupará o acelerador e quando. No serving de LLMs, inclui admissão de sequências, prioridade entre prefill/decode e controle de pressão KV. Difere do agendamento interno de warps pelo hardware; ambos influenciam desempenho em níveis distintos.

Como funciona:
- Observar fila, recursos disponíveis e prazos das requisições.
- Selecionar trabalho para a próxima unidade de execução.
- Atualizar uso de memória e progresso, reconsiderando prioridades sem perder estado.

## T121:C02 — aplicacao

Quando usar:
- Atendimento interativo compartilha GPU com tarefas longas ou em lote.
- Picos de demanda produzem OOM, preempções ou cauda de latência alta.

Quando não usar:
- Admitir tudo imediatamente com objetivo de manter utilização aparente alta.

Implementação proposta:
- Definir objetivos por classe de serviço e orçamento de memória para crescimento de KV.
- Adicionar limites de fila e envelhecimento para impedir starvation.
- Separar métricas do scheduler de aplicação, runtime e kernels.

Aplicação LAI proposta:
Proposta LAI: estabelecer prioridade de interação humana e limites para tarefas em lote, com quotas medidas e sem prometer que ambas cabem simultaneamente.

## T121:C03 — riscos_validacao

Armadilhas:
- Prioridade absoluta para tarefas curtas pode impedir conclusão das longas.
- GPU ocupada recomputando estados pode parecer eficiente enquanto o trabalho útil cai.

Métricas sugeridas:
- Goodput por classe, espera p95 e tempo de starvation.
- Preempções, memória livre e tokens úteis versus recomputados.

Testes propostos:
- Misturar fluxos curtos, longos e cancelados; exigir prazos e progresso mínimo definidos para cada classe.
- Exceder a capacidade e verificar backpressure previsível em vez de falha em cascata.

## T121:C04 — perguntas_proveniencia

Pergunta: Utilização máxima é sempre o objetivo?
Resposta: Não. O objetivo útil é concluir trabalho correto dentro dos prazos e do orçamento.

Pergunta: Scheduler de GPU é só uma fila FIFO?
Resposta: Pode usar FIFO, mas LLMs também exigem considerar memória, fases e duração variável.

Pergunta: Token é uma unidade uniforme de custo?
Resposta: Não. Seu custo depende da fase, contexto, modelo e lote; estimativas precisam ser calibradas na carga.

Pergunta: Pode prometer prazo pelo tamanho do prompt?
Resposta: Não sozinho. Saída, fila, cache e comunicação também influenciam a conclusão.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T121:C05 — mecanismo_avancado

Uma fila de inferência contém trabalhos com custos heterogêneos: prefill longo, decode curto e crescimento futuro de KV não são equivalentes. Como proposta de escalonamento, use custos estimados e prioridades envelhecidas, reavaliando após cada unidade permitida de execução. Interromper uma requisição entre iterações é diferente de preemptar arbitrariamente um kernel já em execução; a granularidade oferecida pelo backend limita a política real.

Condição de contorno:
Ocupação alta pode ocultar trabalho repetido, esperas injustas ou violações de prazo; utilização isolada não mede serviço útil.

Contrato proposto:
- Entradas: Fila, estimativas de trabalho, memória, prazos e pontos permitidos de decisão.
- Saídas: Plano da próxima rodada e justificativas de admissão, espera ou preempção.
- Estado: Idades, custos previstos, progresso confirmado e reservas de crescimento.
- Invariante: O escalonador respeita recursos e não confunde trabalho iniciado com trabalho concluído.

Compromissos de projeto:
- Favorecer trabalhos curtos pode reduzir média e prejudicar longos sem envelhecimento.
- Reservar margem de memória reduz falhas e pode deixar capacidade momentaneamente ociosa.

## T121:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: misturar fluxo contínuo de pedidos curtos com um longo, além de saídas maiores que a previsão. Esperar progresso do longo e política explícita para pressão de memória.

Plano de avaliação proposto:
Plano proposto: comparar políticas com a mesma sequência de chegadas e comprimentos. Medir goodput, deadlines, TTFT, intervalos entre tokens e recomputação; aceitar apenas melhorias que preservem os requisitos por classe definidos previamente.

Comparações:
- T088 (complements): Continuous batching oferece pontos de decisão; a política define quais sequências participam.

Afirmação rastreável:
Sarathi-Serve explora a separação de características entre prefill e decode para reduzir interferência no escalonamento.
Suporte: related; fontes: V3B-S004
Limite: O artigo apoia esse princípio; política de envelhecimento e reservas desta ficha é proposta, não configuração universal.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T121:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu unidades heterogêneas e pontos de decisão. O aprofundamento acrescenta erro de previsão, contratos de justiça e estratégias de admissão que tornam o serviço estável em sobrecarga.

Previsões revisáveis
Comprimento de saída raramente é conhecido antes de gerar. Reserve margem inicial e atualize estimativas conforme o pedido avança, sem contar memória futura como gratuita. Registre erro da previsão por classe; uma classe com respostas longas pode consumir capacidade muito além do custo estimado na admissão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

Justiça observável
Prioridade de negócio precisa de limite de espera e de capacidade ocupada. Meça distribuição de atraso por classe e por tamanho, não só média global. Uma política pode melhorar números agregados deixando pedidos longos sem progresso; envelhecimento e cotas oferecem controles, mas devem ser testados sob chegada contínua.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

Sobrecarga explícita
Quando a chegada excede capacidade, fila ilimitada não cria throughput. Use admissão, deadlines e cancelamento para evitar gastar GPU em respostas que o cliente já abandonou. Distinga rejeição antecipada de falha depois de consumir recursos, e exponha causas para que o cliente não multiplique retries agressivos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

USO AVANÇADO — Assistente interativo e lote interno
Cenário: As duas cargas compartilham a mesma frota.
Estratégia: Reserve capacidade para o interativo e permita ao lote usar sobra com checkpoints ou reexecução delimitada. Defina quais unidades podem ser interrompidas e o custo dessa decisão.
Papel do modelo pequeno: Um 3–7B pode assumir tarefas de lote enquanto um modelo maior atende casos complexos, se houver roteamento validado.
Aceite proposto: Medir prazos das duas classes e custo de trabalho descartado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

USO AVANÇADO — Pico de demanda imprevisível
Cenário: Pedidos novos têm tamanho muito variável.
Estratégia: Adote orçamento por tokens e memória, revise durante execução e cancele trabalho expirado. Aumente capacidade com réplicas somente após separar gargalo de fila, prefill e decode.
Papel do modelo pequeno: Modelos 8–14B podem oferecer capacidade especializada sob limites explícitos.
Aceite proposto: Estabilidade da fila e proporção de respostas úteis dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Muitas sequências pequenas podem ser limitadas por overhead; política simples pode ser suficiente.
8–14B: Separar prefill e decode no orçamento ajuda a lidar com documentos longos.
15–30B: Reservas maiores precisam incluir crescimento de KV e grupo de dispositivos quando distribuído.
Requisitos de treino/runtime: Runtime deve oferecer pontos seguros de agendamento e cancelamento; não há preempção arbitrária garantida de kernels.
Não aplicar quando: Não maximizar tokens por segundo ignorando tempo de espera, abandono ou respostas truncadas.

## T121:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Scheduler equilibra throughput e SLO de requisições.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Admissão assíncrona usa capacidade observada, sem expor todos os detalhes do scheduler GPU.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T121:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T121 → T094 [complements]
Como combinar: Prefill em blocos permite intercalar trabalho longo e decodes.
Interface: Custo do próximo bloco e prazo das sequências.
Condição: Backend suporta a granularidade escolhida.
Aceite proposto: Verificar melhora de prazos sem excesso de fragmentação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T121 → T087 [requires]
Como combinar: Continuous batching executa a agenda com entrada e saída dinâmica.
Interface: Lote ativo e reservas por sequência.
Condição: Admissão respeita memória e crescimento.
Aceite proposto: Aplicar carga aberta para observar saturação real.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar idade e deadline ao reenfileirar ou migrar.
- Medir cancelamento efetivo na GPU, não apenas desconexão do cliente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare respostas válidas por orçamento sob a mesma chegada de usuários. Um serviço rápido em teste fechado pode falhar sob sobrecarga real; isso precisa ser separado de qualidade do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T094, T149, T166, T174

## Fontes primárias associadas

### B-S008 — Orca: A Distributed Serving System for Transformer-Based Generative Models

[https://www.usenix.org/conference/osdi22/presentation/yu](https://www.usenix.org/conference/osdi22/presentation/yu)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por iteração e batching seletivo para geração autorregressiva.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S047 — Batchers — NVIDIA Triton Inference Server

[https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Batching dinâmico agrupa requisições compatíveis e permite controlar espera e filas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S004 — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[https://arxiv.org/abs/2403.02310](https://arxiv.org/abs/2403.02310)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre prefill e decode; chunked prefills e escalonamento para reduzir interrupções.

Limite: Resumo consultado; não extrapolar ganhos de sistemas ou hardware publicados para implantação local.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

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

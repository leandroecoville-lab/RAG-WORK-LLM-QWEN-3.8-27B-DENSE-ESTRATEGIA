# T088 — Continuous Batching

**Nome canônico:** Continuous Batching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T088  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** iteration-level scheduling; in-flight batching

## T088:C01 — conceito

Escalonamento que recompõe o lote durante a geração: sequências terminadas saem e novas requisições entram entre iterações. Evita esperar o texto mais longo de um lote fixo para admitir trabalho novo. Exige gerenciamento independente do estado de cada sequência.

Como funciona:
- Executar uma iteração das sequências admitidas.
- Remover finalizadas ou canceladas e reservar memória para novas admissões.
- Montar a próxima iteração respeitando orçamento de tokens e estados ativos.

## T088:C02 — aplicacao

Quando usar:
- Servidor recebe requisições com comprimentos muito diferentes.
- Vários usuários compartilham um modelo com geração autorregressiva.

Quando não usar:
- Admitir sequências além da memória disponível esperando que todas terminem rapidamente.

Implementação proposta:
- Definir limites de sequências, tokens por passo e reserva para crescimento de KV.
- Medir carga com chegadas reais, não somente um lote enviado de uma vez.
- Separar métricas de espera, prefill e decode e preservar cancelamento por requisição.

Aplicação LAI proposta:
Proposta LAI: validar capacidade simultânea de atendimento com distribuição real de duração, preservando um orçamento mais restrito para interação por voz.

## T088:C03 — riscos_validacao

Armadilhas:
- Mais sequências podem aumentar throughput e piorar o intervalo entre tokens.
- Uma política voltada apenas a throughput pode deixar requisições longas esperando indefinidamente.

Métricas sugeridas:
- Goodput: requisições concluídas dentro dos limites de latência.
- Taxa de preempção, espera p95 e ocupação de KV.

Testes propostos:
- Intercalar respostas curtas e longas e confirmar que vagas são reutilizadas antes do término de todas.
- Aplicar sobrecarga e verificar fila limitada e ausência de starvation conforme a política definida.

## T088:C04 — perguntas_proveniencia

Pergunta: É apenas aumentar batch_size?
Resposta: Não. O conjunto de sequências muda entre iterações; batch_size fixo não descreve toda a política.

Pergunta: Qual a métrica principal?
Resposta: Throughput dentro do prazo exigido, acompanhado de latência de cauda e preempções.

Pergunta: Mais sequências ativas significa mais trabalho útil?
Resposta: Não quando a pressão provoca preempções repetidas e reconstrução do mesmo contexto.

Pergunta: Por que versionar o slot?
Resposta: Após cancelamento e reutilização, uma resposta atrasada poderia ser aplicada à sequência errada sem essa distinção.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T088:C05 — mecanismo_avancado

O recurso escasso muda durante a execução: uma sequência admitida ganha tokens e amplia seu estado, enquanto outra termina e libera espaço. Um escalonador precisa contabilizar tokens processados, capacidade KV e prazos, além do número de requisições. Prefills longos introduzidos entre decodes podem aumentar o intervalo entre tokens; a política de admissão determina quem suporta esse atraso.

Condição de contorno:
Melhor ocupação média não garante boa latência de cauda quando crescimento do cache causa preempções ou reconstruções.

Contrato proposto:
- Entradas: Fila de entrada, sequências ativas, orçamento de tokens e blocos disponíveis.
- Saídas: Conjunto de trabalho por iteração e eventos de admissão, término ou preempção.
- Estado: Slots com identificadores de geração, estado KV e prazos individuais.
- Invariante: Resultado assíncrono só atualiza a sequência que ainda possui aquele slot e geração.

Compromissos de projeto:
- Admitir mais sequências aproveita recursos e eleva pressão de memória.
- Priorizar decodes reduz interrupções, mas pode aumentar espera por primeiro token.

## T088:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir prompt muito longo entre várias gerações curtas e cancelar uma delas antes do retorno do kernel. Esperar preservação de identidade e registro explícito das interrupções.

Plano de avaliação proposto:
Plano proposto: comparar lotes fixos e escalonamento por iteração com mesmos comprimentos e chegadas. Medir tokens úteis por segundo, TTFT, intervalos entre tokens, preempções e falhas; escolher uma política que satisfaça os objetivos por classe.

Comparações:
- T094 (complements): Dividir prefills limita o trabalho que uma admissão longa introduz em cada rodada.

Afirmação rastreável:
O Orca propõe escalonamento na granularidade de uma iteração do modelo, permitindo mudanças no lote.
Suporte: direct; fontes: B-S008
Limite: O princípio publicado não determina sozinho reserva de memória, prioridades ou comportamento de um servidor específico.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T088:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu crescimento KV e admissão entre iterações. Agora o foco é justiça temporal, cancelamento e capacidade efetivamente entregue, incluindo diferença entre uma política que maximiza tokens e outra que preserva a experiência de cada usuário.

Justiça em unidades de trabalho
Uma sequência longa pode consumir muitas iterações enquanto outras aguardam. Monitore atraso acumulado, tokens já recebidos e custo estimado restante, sem exigir estimativa perfeita do tamanho final. Projete envelhecimento de prioridade e limites por cliente; dar preferência permanente a solicitações curtas pode excluir tarefas longas necessárias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

Cancelamento com prazo
Quando um cliente abandona a requisição, interrompa geração e libere recursos assim que o backend puder fazê-lo com segurança. Registre a diferença entre pedido de cancelamento e confirmação de liberação. Jobs mortos que continuam decodificando reduzem capacidade e contaminam throughput aparente com tokens que ninguém utilizará.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

Capacidade sob SLO
Defina capacidade como a maior taxa de chegada que mantém qualidade, TTFT e intervalos entre tokens dentro dos limites escolhidos. Não basta encontrar a saturação de tokens por segundo. Teste long tails de prompt e resposta, pois uma pequena fração de pedidos extremos pode alterar a política ótima do restante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

USO AVANÇADO — Assistentes com fan-out
Cenário: Uma tarefa abre muitas análises independentes de candidatos ou documentos.
Estratégia: Adicione limite por missão e reúna as subrequisições pelo scheduler contínuo. Cancele ramos que se tornaram desnecessários depois de seleção antecipada; preserve a contabilização do custo consumido por eles.
Papel do modelo pequeno: Um 8–30B pode atender análises especializadas em paralelo sem carregar uma cópia por ramo.
Aceite proposto: Aprovar por tempo da missão e justiça entre clientes, mantendo resultados associados ao ramo correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

USO AVANÇADO — Serviço misto online e offline
Cenário: Classificações adiáveis disputam o acelerador com conversas.
Estratégia: Use admissão prioritária para o fluxo interativo e aproveite folga para o offline. Reserve uma cota mínima ao offline para evitar inanição. Reavalie quando prompts ou comprimentos médios mudarem.
Papel do modelo pequeno: Um 3–14B pode manter alta utilização em períodos ociosos, desde que jobs adiáveis aceitem pausa.
Aceite proposto: Medir SLO interativo e progresso offline simultaneamente; nenhum pode desaparecer da avaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, verificar se orquestração CPU e montagem do lote limitam o ganho antes do cálculo GPU.
8–14B: Em 8–14B, ajustar admissão por comprimento e tipo de tarefa costuma ser mais informativo que apenas aumentar sequências.
15–30B: Em 15–30B, pressão de KV exige limites claros e avaliação de preempção/recomputação.
Requisitos de treino/runtime: Runtime deve manter estados por sequência, remoção segura e métricas por requisição; lista de prompts numa API não prova batching contínuo.
Não aplicar quando: Não ativar grandes limites sem margem para crescimento da saída e sem mecanismo de cancelamento verificável.

## T088:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Continuous batching é aplicado pelo scheduler do líder.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O operador descreve batching por iteração para o mesmo workload.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passo 4: requisição entra no próximo lote de decode por continuous batching. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C010 — Hugging Face / HuggingChat — relato de 2023
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: O operador informou em 2023 que TGI alimentava HuggingChat e integrava seus serviços de inferência.
Mecanismo documentado: Servidor dedicado de geração com streaming e otimizações disponíveis na pilha; o relato identifica o runtime efetivamente usado.
Correspondência com esta base: É recurso do TGI, mas a fonte não detalha a configuração exata de batching desse deployment.
Transferência proposta para modelo pequeno: Proposta: usar o caso como referência de migração e compatibilidade; novos serviços 3–30B devem considerar estado atual de manutenção e testar alternativas.
Limite: Não demonstra stack atual do HuggingChat. O maintenance mode documentado em 2026 é preservado, e disponibilidade histórica não é recomendação automática de nova adoção.
Fontes: V4B-S019, V3D-S006.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: Recomposição de batch a cada geração é o mecanismo descrito.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T088:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T088 → T094 [complements]
Como combinar: Dividir prefills extensos para reduzir interrupções do decode de sequências admitidas.
Interface: Orçamento de tokens novos e estados de prefill parcial.
Condição: Scheduler intercala fases mantendo causalidade.
Aceite proposto: Medir TTFT e maior intervalo de streaming por classe.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T088 → T082 [complements]
Como combinar: Reutilizar prefixos comuns no fan-out antes de preencher novas posições do lote.
Interface: Blocos compartilhados e tokens novos por pedido.
Condição: Estados possuem a mesma identidade de execução.
Aceite proposto: Comparar memória compartilhada e capacidade dentro do SLO.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Registrar tokens produzidos após cancelamento como desperdício.
- Expor métricas por cliente e comprimento para detectar inanição mascarada pela média.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar um fluxo completo contra a fronteira sob a mesma taxa de chegada. Continuous batching melhora utilização; a comparação de qualidade continua exigindo testes de domínio independentes do scheduler.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T087, T093, T094, T121

## Fontes primárias associadas

### B-S008 — Orca: A Distributed Serving System for Transformer-Based Generative Models

[https://www.usenix.org/conference/osdi22/presentation/yu](https://www.usenix.org/conference/osdi22/presentation/yu)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por iteração e batching seletivo para geração autorregressiva.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

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

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V3D-S006 — Text Generation Inference — maintenance status

[https://huggingface.co/docs/text-generation-inference/en/index](https://huggingface.co/docs/text-generation-inference/en/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estado de manutenção do TGI com correções menores, documentação e tarefas leves.

Limite: Estado documental verificado em 2026-11-05; não demonstra interrupção de serviço existente.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S019 — Open-Source Text Generation & LLM Ecosystem at Hugging Face

[https://huggingface.co/blog/os-llms](https://huggingface.co/blog/os-llms)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico do operador de TGI servindo HuggingChat e integração nos serviços de inferência.

Limite: Fonte histórica; não prova stack atual do HuggingChat nem cancela estado atual de manutenção do TGI.

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

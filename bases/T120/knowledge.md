# T120 — KV Cache Routing

**Nome canônico:** KV Cache Routing  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T120  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cache-aware routing; roteamento consciente de KV

## T120:C01 — conceito

Escolhe o worker de inferência considerando quais estados KV já estão disponíveis e quanto trabalho ele tem em andamento. Busca reduzir prefill repetido sem concentrar tráfego num servidor saturado. Seleção de destino e transporte de estados são funções relacionadas, mas separadas.

Como funciona:
- Consultar um índice de prefixos ou estados disponíveis por worker.
- Combinar afinidade de cache com carga, elegibilidade e custo previsto.
- Encaminhar a requisição e atualizar o índice com eventos de criação ou remoção.

## T120:C02 — aplicacao

Quando usar:
- Várias réplicas atendem prompts ou conversas com prefixos reutilizáveis.
- Cache local faz diferença material no custo de prefill.

Quando não usar:
- Um único worker atende tudo ou a informação de cache fica tão stale que prejudica decisões.

Implementação proposta:
- Definir identidade de blocos e escopo de isolamento consistente entre roteador e workers.
- Manter caminho de fallback para worker válido sem cache.
- Penalizar carga projetada e medir o equilíbrio entre localidade e fila.

Aplicação LAI proposta:
Proposta LAI: adotar somente quando houver várias réplicas; manter identidade de tenant e checkpoint no contrato para evitar afinidade indevida.

## T120:C03 — riscos_validacao

Armadilhas:
- Preferir sempre o maior cache hit pode criar um ponto de saturação.
- Eventos perdidos podem anunciar blocos já removidos e levar a decisões ruins.

Métricas sugeridas:
- Prefixo efetivamente reutilizado após roteamento e acertos previstos versus reais.
- Tempo de fila, distribuição de carga e TTFT por worker.

Testes propostos:
- Simular cache quente em worker ocupado e confirmar escolha coerente com a meta de latência.
- Excluir estados sem atualizar imediatamente o índice e verificar recuperação segura de cache miss.

## T120:C04 — perguntas_proveniencia

Pergunta: Roteamento de KV escolhe o melhor modelo?
Resposta: Não necessariamente. Em geral escolhe uma instância compatível; model routing decide entre modelos.

Pergunta: Cache hit deve sempre ganhar?
Resposta: Não. Espera e carga podem tornar um worker sem cache mais rápido no custo total.

Pergunta: Roteamento transfere automaticamente o KV?
Resposta: Não necessariamente. A decisão de posicionamento e o mecanismo de transporte têm contratos separados.

Pergunta: Por que reservar carga ao decidir?
Resposta: Sem contabilizar decisões simultâneas, vários pedidos podem escolher o mesmo worker aparentemente livre e criar uma fila inesperada.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T120:C05 — mecanismo_avancado

O índice de localização é uma previsão de disponibilidade, não uma reserva irrevogável. Entre seleção e execução, um prefixo pode ser expulso ou o worker receber nova carga. Como proposta operacional, o destino confirma identidade e disponibilidade antes de reutilizar; um miss real deve provocar prefill explícito ou nova decisão, preservando o pedido. A função de custo precisa incluir trabalho já comprometido, não somente a fila observada.

Condição de contorno:
Enviar sempre ao maior prefixo pode criar um ponto quente e piorar latência apesar de economizar tokens de prefill.

Contrato proposto:
- Entradas: Tokens normalizados, elegibilidade dos workers, afinidade de cache e carga projetada.
- Saídas: Destino escolhido com estimativa de custo e confirmação do hit real.
- Estado: Índice de eventos, decisões pendentes e carga já atribuída.
- Invariante: A localização sugerida nunca autoriza reutilizar estado incompatível ou ausente.

Compromissos de projeto:
- Afinidade economiza reconstrução e pode concentrar carga.
- Índices mais frequentes reduzem defasagem e aumentam tráfego de controle.

## T120:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover o prefixo logo após o roteamento e atrasar seu evento de exclusão. Esperar miss reconhecido e recuperação correta, sem assumir que o índice garantiu presença.

Plano de avaliação proposto:
Plano proposto: comparar round-robin, carga e custo com cache sob chegadas idênticas. Medir hits confirmados, erro da previsão, TTFT e distribuição de carga; aceitar benefício sem degradar classes de pedidos menos reutilizáveis.

Comparações:
- T102 (complements): Em fases separadas, escolher workers e transferir estado são responsabilidades distintas.

Afirmação rastreável:
O Dynamo combina sobreposição de prefixo com carga ativa de prefill e decode para escolher workers.
Suporte: direct; fontes: B-S032
Limite: O teste de índice defasado é uma proposta editorial; não declara um defeito observado no produto.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T120:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu localização prevista de disponibilidade confirmada. A nova análise introduz custo de remanejamento, incerteza da observação e efeitos de afinidade na distribuição de capacidade.

Índice com atraso
Eventos de cache chegam depois de mudanças no worker. Guarde idade da observação e confiança da estimativa, em vez de tratar todos os hits anunciados como equivalentes. Uma confirmação negativa deve atualizar o índice e permitir prefill normal; repetir roteamento indefinidamente pode consumir o prazo sem executar trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

Afinidade versus fila
Um worker com prefixo pode ser pior destino que outro livre que precisa recomputar. Compare economia de prefill com espera, transferências e reservas já comprometidas. Session affinity, como documentada no Workers AI, é um mecanismo útil, mas não equivale por si só a otimização global baseada em inventário de KV.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

Evitar oscilação
Mover pedidos entre destinos conforme pequenas mudanças de fila pode gerar tráfego e decisões contraditórias. Aplique histerese e limite de reatribuições, mantendo uma decisão estável após reserva confirmada. Se houver migração de estado, o destino só assume propriedade depois de verificar completude e identidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

USO AVANÇADO — Chat com prefixo recorrente
Cenário: Sessões compartilham um contexto estável e alternam atividade.
Estratégia: Use afinidade como sinal, junto com custo atual e prazo. Quando a réplica estiver congestionada, permita execução fria em outra sem alterar o conteúdo da conversa.
Papel do modelo pequeno: Um 3–7B pode ser replicado para isolar picos e manter uma política simples.
Aceite proposto: Comparar ganho de reúso com aumento de espera por sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

USO AVANÇADO — Roteamento de documentos longos
Cenário: Pedidos próximos reutilizam documentos distintos.
Estratégia: Indexe prefixos por versão e domínio, estime prefill evitado e limite concentração por família. Não mova contexto sensível para um destino inelegível.
Papel do modelo pequeno: Um 15–30B pode economizar prefill caro quando o padrão de reúso é estável.
Aceite proposto: Medir hits consumidos, transferências inúteis e cumprimento de prazos por família.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Recomputar prompts curtos pode custar menos que manter um roteador sofisticado.
8–14B: Use observações por réplica e meça a divergência entre custo previsto e real.
15–30B: Quando um pedido ocupa vários dispositivos, destino significa um grupo saudável, não apenas uma GPU.
Requisitos de treino/runtime: Runtime precisa publicar disponibilidade e carga; arquitetura do modelo permanece a mesma.
Não aplicar quando: Não usar afinidade de sessão como autorização de acesso nem semântica aproximada para reutilizar KV.

## T120:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 5.1/Algoritmo 1 de Mooncake v1 escolhe worker usando prefixo reutilizável, fila, transferência prevista e TTFT/SLO.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Roteamento busca a mesma instância, sem comprovar consulta dinâmica a blocos KV de todos os workers.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002, V4B-Q022.

## T120:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T120 → T082 [feeds]
Como combinar: O roteamento aumenta chance de consumir prefixos já calculados.
Interface: Identidade completa do prefixo e comprimento.
Condição: Hit confirmado no destino.
Aceite proposto: Atribuir economia apenas a tokens realmente reutilizados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S032, V4B-S004, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T120 → T102 [complements]
Como combinar: Em serviço desagregado, escolha de destino inclui quem fará prefill e quem manterá decode.
Interface: Plano de transferência e reserva em ambos os pools.
Condição: Custo do transporte entra na decisão.
Aceite proposto: Testar saturação de rede e fallback sem duplicar pedido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S032, V4B-S004, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar retries de roteamento e preservar idade original do pedido.
- Separar misses de índice obsoleto, evicção e incompatibilidade de configuração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação deve avaliar o serviço distribuído completo. Roteamento de cache pode baixar custo, mas não altera a informação ou capacidade disponíveis ao modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T102, T103, T133, T171

## Fontes primárias associadas

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

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

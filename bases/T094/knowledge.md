# T094 — Chunked Prefill

**Nome canônico:** Chunked Prefill  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T094  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** prefill em partes

## T094:C01 — conceito

Divide o processamento inicial de um prompt longo em partes escalonáveis. Preserva a sequência lógica e seus estados; não resume nem retira conteúdo. A finalidade é controlar interferência entre entradas longas e sequências que já estão produzindo tokens.

Como funciona:
- Reservar um orçamento de tokens de trabalho por iteração.
- Processar somente uma parte do prefill quando o prompt excede o orçamento.
- Continuar o restante em iterações seguintes junto de outros trabalhos compatíveis.

## T094:C02 — aplicacao

Quando usar:
- Prompts longos chegam enquanto outras conversas estão em decode.
- Latência entre tokens sofre picos causados por grandes prefills.

Quando não usar:
- Confundir o mecanismo com cortar documentos em chamadas independentes sem preservar o estado do modelo.

Implementação proposta:
- Medir separadamente TTFT das novas entradas e ITL das sequências ativas.
- Varrer alguns orçamentos de tokens mantendo a mesma carga e limites de memória.
- Verificar qual política prioriza decode e como ela impede espera indefinida de prefill.

Aplicação LAI proposta:
Proposta LAI: usar como candidato de ajuste quando ingestão ou contexto longo prejudica atendimento; não copiar um tamanho de chunk sem ensaio.

## T094:C03 — riscos_validacao

Armadilhas:
- Partes pequenas demais aumentam overhead e podem atrasar muito o primeiro token.
- Partes grandes demais preservam throughput mas ainda interrompem a fluidez de conversas ativas.

Métricas sugeridas:
- TTFT e ITL por faixa de comprimento do prompt.
- Tempo de fila e tokens de prefill processados por iteração.

Testes propostos:
- Injetar um prompt longo durante vários streams; exigir ITL dentro da meta escolhida.
- Comparar logits após prefill integral e dividido, preservando tokens e máscara, com tolerância numérica.

## T094:C04 — perguntas_proveniencia

Pergunta: Chunked prefill reduz a quantidade de tokens do contexto?
Resposta: Não. Distribui o cálculo no tempo mantendo o prompt lógico.

Pergunta: Qual tamanho devo usar?
Resposta: Aquele que equilibra TTFT e ITL no perfil de carga e hardware medidos.

Pergunta: O cache reinicia em cada trecho?
Resposta: Não quando o objetivo é preservar a mesma atenção; o estado permitido anterior precisa continuar acessível.

Pergunta: Chunk menor sempre reduz TTFT?
Resposta: Não. Mais rodadas e sobrecarga podem alongar a conclusão do prefill, embora melhorem a cadência de outras respostas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T094:C05 — mecanismo_avancado

Dividir um prefill não significa tratar cada trecho como uma sequência independente. As consultas do trecho atual precisam acessar todos os estados anteriores permitidos pela arquitetura e respeitar a causalidade dentro do próprio trecho. O orçamento deve contar trabalho novo e interferência com decodes ativos. Trechos muito pequenos podem multiplicar lançamentos e reduzir eficiência matricial; trechos grandes podem provocar pausas longas entre tokens.

Condição de contorno:
O tamanho ideal depende de mistura de comprimentos, contexto já processado, backend e objetivo de latência; não existe número universal.

Contrato proposto:
- Entradas: Prompt completo, offset processado, KV anterior e orçamento da rodada.
- Saídas: Cache estendido e offset confirmado, mantendo ordem causal.
- Estado: Trechos pendentes, posições absolutas e sequências de decode concorrentes.
- Invariante: Divisão de execução não altera o contexto visível definido pelo modelo.

Compromissos de projeto:
- Menores trechos favorecem intercalamento e podem aumentar custo total.
- Priorizar decode melhora cadência, mas pode elevar TTFT de novas entradas.

## T094:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar evidência no fim de um trecho e consulta no início do seguinte, variando fronteiras. Esperar resultado compatível com prefill integral e ausência de reset posicional.

Plano de avaliação proposto:
Plano proposto: comparar prefill inteiro e vários tamanhos de trecho com mesma chegada. Medir TTFT, intervalo entre tokens, duração de prefill e interrupções; selecionar pela combinação de objetivos de serviço, sem confundir throughput agregado com responsividade.

Comparações:
- T095 (distinct_from): Chunking organiza execução; uma janela altera a conectividade permitida pela atenção.

Afirmação rastreável:
Sarathi-Serve combina prefills divididos e escalonamento para reduzir interrupções das sequências em decode.
Suporte: direct; fontes: V3B-S004
Limite: O método publicado não fixa um tamanho ótimo válido para todos os modelos e cargas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T094:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou causalidade entre chunks e compromisso de granularidade. Agora a política considera prazo de primeiro token, regularidade de streaming e estimativa de custo por forma, para decidir quanto prefill admitir sem prejudicar sessões já abertas.

Dois relógios de serviço
O novo pedido espera seu primeiro token, enquanto pedidos antigos esperam o próximo. Reserve orçamento entre esses dois compromissos em vez de priorizar indefinidamente apenas um deles. Uma política que protege todo decode pode deixar prefills longos sem progresso; o inverso gera pausas visíveis nas conversas ativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

Orçamento em custo observado
Igual número de tokens novos não garante duração igual quando contextos e arquiteturas diferem. Use observações por faixa de comprimento e forma para limitar tempo aproximado da iteração, mantendo teto conservador. Reavalie a estimativa após quantização, troca de backend ou alteração de batch, pois o gargalo pode mudar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

Aquecimento e formas recorrentes
Um conjunto pequeno de tamanhos de chunk pode facilitar compilação e reutilização de grafos, se o runtime suportar. Muitos tamanhos adaptativos podem causar aquecimento repetido e consumir memória de grafos. Meça esse efeito antes de adotar uma política aparentemente mais fina; flexibilidade tem custo de engenharia e execução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

USO AVANÇADO — Documento longo durante chat ativo
Cenário: Um usuário envia um arquivo extenso enquanto outros recebem streaming.
Estratégia: Processe o arquivo com orçamento por iteração e progresso mínimo garantido. Reduza chunks quando o intervalo de streaming exceder a meta, mas aplique envelhecimento para que o arquivo avance. Registre separadamente tempo em fila e tempo de prefill.
Papel do modelo pequeno: Um 8–30B pode compartilhar GPU entre leitura longa e diálogos curtos.
Aceite proposto: Aprovar pela combinação de TTFT do arquivo e regularidade do streaming existente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

USO AVANÇADO — Importação seguida de perguntas
Cenário: Muitos documentos serão consultados após ingestão.
Estratégia: Prepare prefills oportunisticamente apenas para conteúdos com probabilidade de uso, preservando orçamento de pedidos ativos. Combine com prefix caching quando houver reuso exato. Se a demanda não vier, contabilize prefill antecipado como custo desperdiçado.
Papel do modelo pequeno: Um 3–14B pode reduzir espera percebida sem exigir um modelo maior.
Aceite proposto: Medir economia nas consultas reais e custo dos prefills nunca consumidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, chunks muito pequenos podem ser dominados por lançamentos e controle CPU.
8–14B: Em 8–14B, escolher poucas faixas de tamanho por objetivo de latência facilita operação e diagnóstico.
15–30B: Em 15–30B, considerar pressão KV e duração das operações distribuídas ao fixar orçamento.
Requisitos de treino/runtime: É scheduling runtime; preserva contexto lógico e requer suporte correto ao prefill parcial.
Não aplicar quando: Não tratar chunks como documentos independentes nem usá-los para contornar o limite de contexto do checkpoint.

## T094:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Processamento do prompt em blocos de 64 preserva histórico KV na configuração publicada. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passo 2, e seção 4.1: prefill longo é dividido em chunks conforme limiar e processado em pipeline. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T094:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T094 → T088 [complements]
Como combinar: Reservar trabalho de prefill dentro de cada iteração do lote contínuo.
Interface: Tokens novos, decodes ativos e prazos de cada pedido.
Condição: O scheduler mantém estados de prefill parcial.
Aceite proposto: Comparar piores intervalos entre tokens e progresso de pedidos longos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, B-S014, V4B-S002, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T094 → T102 [alternative]
Como combinar: Separar fases em pools quando interferência persistir e transferência compensar.
Interface: Custo de prefill, volume KV e atraso de transporte.
Condição: Carga e infraestrutura justificam uma segunda camada de coordenação.
Aceite proposto: Comparar goodput com todas as transferências e filas incluídas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, B-S014, V4B-S002, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Garantir progresso mínimo para entradas longas.
- Testar variação de chunks com mesma máscara e saída de referência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar experiência de leitura e conversa contra uma fronteira usando os mesmos documentos e perguntas. Melhor escalonamento pode reduzir espera, mas não prova que o modelo pequeno compreende todo o documento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T102, T121

## Fontes primárias associadas

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S004 — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[https://arxiv.org/abs/2403.02310](https://arxiv.org/abs/2403.02310)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre prefill e decode; chunked prefills e escalonamento para reduzir interrupções.

Limite: Resumo consultado; não extrapolar ganhos de sistemas ou hardware publicados para implantação local.

### V3B-S007 — Mistral 7B — full text

[https://arxiv.org/html/2310.06825v1](https://arxiv.org/html/2310.06825v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campo receptivo em camadas, cache circular e chunking com janela.

Limite: Refere-se à arquitetura publicada; não prova qualidade para contexto arbitrário nem compatibilidade com checkpoint do usuário.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

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

# T082 — Prefix Caching

**Nome canônico:** Prefix Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T082  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** automatic prefix caching; cache de prefixos

## T082:C01 — conceito

Reaproveita o processamento de um início idêntico de sequência entre requisições. O cache pode guardar blocos KV desse prefixo e reduzir o trabalho de prefill. Não reutiliza automaticamente a resposta anterior e não retira os tokens da janela lógica do modelo.

Como funciona:
- Tokenizar o prompt completo com a mesma política usada no servidor.
- Encontrar o maior prefixo já calculado e compatível.
- Recuperar estados correspondentes e calcular apenas o sufixo ausente.

## T082:C02 — aplicacao

Quando usar:
- Instruções estáveis compartilhadas por muitas chamadas.
- Perguntas diferentes sobre o mesmo documento inicial longo.

Quando não usar:
- Prompts cujo início muda constantemente ou quando a persistência do cache não compensa seu custo.

Implementação proposta:
- Colocar instruções estáveis antes dos dados variáveis sem alterar o sentido da tarefa.
- Medir separadamente chamadas frias e quentes com concorrência representativa.
- Definir escopo de isolamento e invalidar por versão de modelo, template e adaptador.

Aplicação LAI proposta:
Proposta LAI: estabilizar o prefixo das ferramentas e regras recorrentes da Helena e medir a economia antes de expandir o cache.

## T082:C03 — riscos_validacao

Armadilhas:
- Timestamps e ordem variável de ferramentas no início podem destruir os acertos.
- Um acerto reduz computação de entrada; não implica redução proporcional da duração total.

Métricas sugeridas:
- Taxa de tokens de prefixo reaproveitados, além da taxa de requisições com hit.
- Tempo até o primeiro token e latência final em cache frio/quente.

Testes propostos:
- Enviar dois prompts com prefixo igual e sufixos diferentes; verificar redução de prefill sem troca de respostas.
- Alterar o primeiro token e confirmar que o runtime não reutiliza estados incompatíveis.

## T082:C04 — perguntas_proveniencia

Pergunta: Prefix cache aumenta a janela?
Resposta: Não. Reaproveita cálculo; o prefixo continua fazendo parte da sequência atendida.

Pergunta: É igual a response caching?
Resposta: Não. Response caching devolve saída armazenada; prefix caching ainda gera uma nova resposta.

Pergunta: Prefix caching acelera automaticamente o decode?
Resposta: Não. Seu benefício direto é evitar construção repetida de estados do prefixo; a atenção sobre eles continua necessária.

Pergunta: Como comparar caches com blocos diferentes?
Resposta: Use tokens e tempo realmente poupados, além da memória ocupada; uma taxa bruta de hits não é comparável.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T082:C05 — mecanismo_avancado

Um hit de prefixo economiza parte do prefill, mas as consultas do sufixo ainda atendem ao prefixo reutilizado. O benefício depende dos tokens efetivamente cobertos e do custo evitado, não apenas da quantidade de requisições com algum hit. Em caches por blocos completos, um prefixo quase coincidente pode reutilizar menos tokens que seu comprimento textual sugere.

Condição de contorno:
Prompts com conteúdo variável no início ou poucas repetições podem consumir memória de cache sem amortizar sua construção.

Contrato proposto:
- Entradas: Tokens de entrada, identidade do modelo, domínio de compartilhamento e tamanho dos blocos.
- Saídas: Extensão reutilizada e sufixo que ainda necessita processamento.
- Estado: Blocos completos indexados com ancestralidade do prefixo.
- Invariante: O hit termina antes da primeira divergência efetiva de tokens ou identidade.

Compromissos de projeto:
- Reservar prefixos aumenta reúso, mas reduz espaço para sequências ativas.
- Reorganizar prompts só é aceitável quando preserva significado e instruções.

## T082:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: variar um token próximo à fronteira de bloco e alternar templates de chat. Esperar hits apenas nos blocos anteriores compatíveis, com saída equivalente à execução fria.

Plano de avaliação proposto:
Plano proposto: comparar cache frio e aquecido sob a mesma mistura de prompts. Variar tamanho do prefixo e do sufixo, medir tokens reutilizados, TTFT, ocupação e caudas; aprovar pela redução de custo end-to-end sem divergência.

Comparações:
- T088 (complements): O escalonador pode aproveitar menos trabalho de prefill sem eliminar contenção entre requisições.

Afirmação rastreável:
O projeto de prefix caching do vLLM identifica blocos com ancestralidade e armazena somente blocos completos.
Suporte: direct; fontes: B-S005
Limite: Esse detalhe descreve o projeto documentado; outros servidores podem adotar granularidades diferentes.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T082:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mediu hits por tokens e discutiu prefixos comuns. O aprofundamento passa a desenhar famílias de prompts, políticas de retenção e experimentos econômicos, mantendo separados benefício do cache, mudança editorial do prompt e qualidade da tarefa.

Famílias estáveis de prompts
Crie versões explícitas de um prefixo por produto, idioma e conjunto de ferramentas. Coloque conteúdo variável após a região realmente compartilhável, preservando a ordem exigida pelo modelo. Não reúna instruções incompatíveis só para aumentar hits: prefixo mais longo também ocupa contexto e pode aumentar o decode.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

Valor de retenção
Estime valor de um prefixo por custo de prefill evitado vezes probabilidade de revisita, descontando memória ocupada e pressão sobre sequências ativas. Um prefixo popular e barato de reconstruir pode merecer menos espaço que outro caro e recorrente. Atualize a estimativa por classe de tráfego e não por média única.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

Experimento sem confusão causal
Mantenha duas comparações: mesmo prompt com cache ligado/desligado e prompt reorganizado com cache equivalente. A primeira isola o mecanismo; a segunda mede mudança de instruções e posicionamento. Relate cache frio, aquecido e após invalidação, porque o resultado de uma demonstração aquecida não representa implantação recém-iniciada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

USO AVANÇADO — Análise de muitos documentos
Cenário: O mesmo contrato de extração processa documentos independentes.
Estratégia: Versione instruções e exemplos fixos, deixando cada documento no sufixo. Distribua chamadas considerando afinidade e fila. Invalide o prefixo quando mudar schema ou adaptador, mesmo se o texto principal continuar parecido.
Papel do modelo pequeno: Um especialista 3–14B pode atender extração repetitiva com verificação de campos.
Aceite proposto: Aprovar pela combinação de custo por documento válido, TTFT e ausência de mistura entre clientes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

USO AVANÇADO — Chat com ferramentas estáveis
Cenário: As definições de ferramentas se repetem entre turnos.
Estratégia: Canonize a serialização das ferramentas e evite reordenar propriedades sem necessidade. Preserve o tokenizador e template; calcule quanto do prefixo é reutilizado depois de cada resposta. Limite retenção de sessões que não retornam.
Papel do modelo pequeno: Um 15–30B mantém contexto útil sem recalcular tudo a cada turno.
Aceite proposto: Comparar tokens reutilizados e latência nas revisitas, incluindo custo de retenção ociosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, prefira prefixos curtos e frequentes; não infle instruções para criar uma economia artificial de cache.
8–14B: Em 8–14B, organizar famílias por ferramenta e tarefa pode melhorar reutilização sem misturar contratos.
15–30B: Em 15–30B, medir a disputa entre prefixos residentes e KV de conversas longas antes de ampliar retenção.
Requisitos de treino/runtime: É otimização runtime; cache exige identidade de tokens e condições de execução, não similaridade semântica.
Não aplicar quando: Não esperar redução de tokens lógicos na janela nem reuso automático entre workers sem suporte explícito.

## T082:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: O operador afirma que o serviço usa prefix caching.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O relato de serving explicita reuso de prefixos comuns no Hiring Assistant.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passos 1–2: recuperar prefixo KV existente e executar apenas prefill incremental. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: Prefix caching integra os recursos descritos.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Prefixos comuns reutilizam os mesmos nós de KV.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T082:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T082 → T120 [complements]
Como combinar: Encaminhar para um worker com prefixo compatível somente se o ganho superar espera adicional.
Interface: Hash de identidade, comprimento reutilizável e estimativa de fila.
Condição: Métricas estão atualizadas e respeitam isolamento.
Aceite proposto: Comparar afinidade com balanceamento de carga sob rajadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T082 → T088 [complements]
Como combinar: Compartilhar prefixos em lotes contínuos sem bloquear admissões por cache ocioso.
Interface: Referências KV e orçamento por iteração.
Condição: Scheduler e cache contabilizam blocos compartilhados uma única vez.
Aceite proposto: Medir concorrência útil e verificar liberação após cancelamento.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Separar taxa de hit de economia efetiva em tokens e tempo.
- Invalidar por revisão do template e testar início frio após implantação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar extração ou atendimento com uma fronteira sob o mesmo nível de qualidade verificável. Prefix caching pode reduzir custo da solução pequena; não recupera conhecimento ausente nem melhora automaticamente a exatidão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T002, T007, T081, T083, T103, T171

## Fontes primárias associadas

### B-S004 — Automatic Prefix Caching

[https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reaproveitamento de prefixos idênticos para evitar prefill repetido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

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

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

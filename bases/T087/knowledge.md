# T087 — Batching — Static Batching e Dynamic Batching

**Nome canônico:** Static Batching e Dynamic Batching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T087  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Batching; processamento em lotes; lote estático; lote dinâmico

## T087:C01 — conceito

Batching reúne entradas compatíveis para executar operações conjuntamente. Static Batching forma um lote definido antes da execução, frequentemente pelo cliente ou por uma fila de trabalho. Dynamic Batching reúne requisições que chegam ao servidor conforme capacidade e espera permitida. Continuous Batching, descrito em T088, muda a composição durante os passos de geração e merece avaliação separada.

Como funciona:
- No lote estático, selecionar previamente as entradas, executar e mapear cada saída ao seu identificador.
- No lote dinâmico, acumular requisições elegíveis e despachar ao atingir tamanho, disponibilidade ou prazo de espera.
- Manter compatibilidade de modelo, shapes e opções exigidas pelo backend; tamanhos maiores podem exigir mais memória e padding.

## T087:C02 — aplicacao

Quando usar:
- Processamento offline de muitas entradas ou tráfego concorrente suficiente para aproveitar execução conjunta dentro do orçamento de latência.

Quando não usar:
- Quando esperar outras requisições viola o prazo ou entradas incompatíveis não podem compartilhar a execução.

Implementação proposta:
- Proposta: começar com limite de lote e espera zero; medir a curva de throughput e latência antes de aumentar a janela de agregação.
- Separar tempo na fila de tempo de inferência e testar distribuição real de comprimentos; agrupar comprimentos próximos quando padding dominar o custo.
- Definir fila máxima, cancelamento e identificação de respostas; garantir que um item não receba a saída de outro.
- Para modelos stateful, confirmar suporte ao agrupamento de sequências; o batcher dinâmico genérico do Triton destina-se a modelos stateless.

Aplicação LAI proposta:
Proposta LAI: escolher separadamente batching offline para ingestão e batching do servidor para inferência interativa; os limites dependem de medições locais ainda não realizadas.

## T087:C03 — riscos_validacao

Armadilhas:
- Um benchmark com lote sempre cheio não representa tráfego esparso.
- Aumento do throughput pode coexistir com piora de p95 e pico de memória.

Métricas sugeridas:
- Requisições por segundo, tamanho efetivo dos lotes, tempo em fila, p95/p99 e utilização de memória.

Testes propostos:
- Teste proposto: comparar lote estático fixo com chegadas esparsas e em rajada no dinâmico, mantendo modelo e entradas.
- Cancelar um item enfileirado e conferir correspondência, completude e isolamento das respostas restantes.

## T087:C04 — perguntas_proveniencia

Pergunta: Dynamic Batching é automaticamente Continuous Batching?
Resposta: Não. O primeiro forma lotes a partir de chegadas; o segundo admite e retira sequências entre passos de geração.

Pergunta: Um lote maior sempre é melhor?
Resposta: Não. Pode aumentar espera, padding e memória. A configuração deve atender simultaneamente throughput e metas de latência.

Pergunta: Lote maior é sempre mais eficiente?
Resposta: Não. Memória, formas, preenchimento e custo das operações podem mudar a região eficiente.

Pergunta: Qual throughput contabilizar?
Resposta: Trabalho útil concluído, acompanhado de erros e tempo de espera; posições de padding não representam serviço entregue.

Escopo das fontes:
Triton fundamenta formação dinâmica e controles de fila. Comparação e critérios LAI são propostas.

## T087:C05 — mecanismo_avancado

A latência observada combina espera na fila e serviço do lote. Aumentar a janela de agregação pode melhorar utilização e simultaneamente piorar respostas em tráfego esparso. Em um lote retangular com padding, sum(comprimentos)/(número_de_sequências·maior_comprimento) estima a fração de posições úteis; essa conta descreve desperdício estrutural, não prevê diretamente o tempo de um kernel com caminhos especializados.

Condição de contorno:
Agregação dinâmica de requisições independentes não resolve automaticamente o estado autoregressivo nem substitui escalonamento por iteração.

Contrato proposto:
- Entradas: Requisições com identidade, forma, prazo e instante de chegada.
- Saídas: Lotes compatíveis e respostas associadas aos solicitantes corretos.
- Estado: Fila, deadline original, limites de tamanho e cancelamentos.
- Invariante: Novas chegadas não reiniciam indefinidamente o prazo da requisição mais antiga.

Compromissos de projeto:
- Esperar mais aumenta oportunidades de agregação e custo de fila.
- Agrupar por comprimento reduz padding, mas pode postergar classes pouco frequentes.

## T087:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar rajadas e longos intervalos, incluindo uma requisição extensa e cancelamentos. Esperar cumprimento do limite de espera e ausência de troca de respostas após reordenação.

Plano de avaliação proposto:
Plano proposto: comparar execução individual, lotes fixos e agregação dinâmica com mesma chegada e hardware. Medir espera, serviço, throughput útil, padding e latências de cauda; aceitar configuração apenas dentro do objetivo de serviço de cada classe.

Comparações:
- T088 (distinct_from): Continuous batching altera participantes entre iterações, além de formar lotes na entrada.

Afirmação rastreável:
O Triton permite limitar o atraso para juntar requisições e envia o lote disponível quando o prazo termina.
Suporte: direct; fontes: B-S047
Limite: A documentação recomenda esse batcher para modelos sem estado; integração autoregressiva exige cuidados adicionais.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T087:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou espera de lote e desperdício de padding. A expansão concentra-se em controle de admissão, mistura de prioridades e medição sob chegadas realistas, para que throughput alto não esconda filas crescentes ou resultados entregues fora de prazo.

Tráfego aberto versus fechado
Um ensaio que envia a próxima requisição somente após receber a anterior limita artificialmente a fila. Para avaliar serviço, reproduza chegadas independentes, rajadas e períodos esparsos. Mantenha também um teste fechado para capacidade individual, mas não use sua latência como promessa de comportamento sob demanda externa crescente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

Lotes por compatibilidade real
Agrupe por modelo, formato de entrada e restrições do backend, preservando identificadores individuais. Separar comprimentos pode reduzir desperdício, mas criar filas demais deixa lotes pequenos esperando. Escolha poucas classes justificadas por distribuição observada e imponha prazo máximo de espera mesmo quando o lote ideal não se completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

Contabilidade de entrega
Meça itens concluídos corretamente por unidade de tempo, com contagem de rejeições, expirados e cancelados. O throughput do acelerador pode crescer enquanto a taxa de resultados úteis cai. Para jobs offline, registre progresso durável por item; repetir um lote após falha não deve duplicar gravações já confirmadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

USO AVANÇADO — Enriquecimento de catálogo
Cenário: Milhões de registros independentes precisam de classificação ou extração.
Estratégia: Use lotes estáticos para partições conhecidas, ordene por comprimento quando permitido e grave saída vinculada ao ID original. Faça retries apenas dos itens sem conclusão verificável. Preserve uma amostra temporal fora da otimização.
Papel do modelo pequeno: Um 3–14B especializado pode executar grande volume com validação determinística de campos.
Aceite proposto: Aprovar por custo por registro válido e prazo do job, incluindo retrabalho e persistência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

USO AVANÇADO — Endpoint com demanda irregular
Cenário: Chamadas interativas chegam em picos curtos.
Estratégia: Use agregação dinâmica com janela limitada por prazo. Se a fila crescer, rejeite ou encaminhe antes de acumular atraso irrecuperável. Separe pedidos urgentes de processamento adiado somente quando houver capacidade garantida para ambos.
Papel do modelo pequeno: Um 15–30B pode amortizar pesos com lotes, mas não deve atrasar indefinidamente requisições pequenas.
Aceite proposto: Comparar distribuição de espera e serviço por classe, com carga aberta e cancelamentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, overhead de rede e tokenização pode dominar; medir lotes pequenos antes de buscar máxima ocupação.
8–14B: Em 8–14B, poucas faixas de comprimento ajudam a explorar eficiência sem fragmentar excessivamente a demanda.
15–30B: Em 15–30B, aumentar lote exige reservar KV e buffers, além de caberem os pesos.
Requisitos de treino/runtime: Batching é runtime; embeddings, classificação e geração têm perfis diferentes e não compartilham automaticamente o mesmo scheduler.
Não aplicar quando: Não usar lote fixo para tarefas com prazos incompatíveis nem comparar throughput offline com latência interativa.

## T087:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: O relato de serving de query understanding identifica batching no cliente e servidor.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T087:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T087 → T088 [alternative]
Como combinar: Trocar o lote fechado por composição por iteração quando comprimentos de geração variam muito.
Interface: Fila de requisições e estados independentes.
Condição: O runtime suporta entrada e saída de sequências ativas.
Aceite proposto: Comparar utilidade entregue com a mesma chegada e orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S047, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T087 → T162 [complements]
Como combinar: Confirmar cada resultado por chave idempotente antes de marcar o lote concluído.
Interface: ID do item, revisão da entrada e hash da saída.
Condição: Há armazenamento com deduplicação de commits.
Aceite proposto: Falhar após gravação parcial e verificar que nenhum efeito é repetido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S047, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não excluir timeouts da estatística principal de latência.
- Preservar correspondência entre item e saída após reordenação por comprimento.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar classificação ou extração em lote com uma fronteira usando o mesmo conjunto e orçamento de erro. Batching permite economia operacional do pequeno modelo; não corrige categorias que ele não aprende.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T137, P009

## Fontes primárias associadas

### B-S047 — Batchers — NVIDIA Triton Inference Server

[https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Batching dinâmico agrupa requisições compatíveis e permite controlar espera e filas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

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

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

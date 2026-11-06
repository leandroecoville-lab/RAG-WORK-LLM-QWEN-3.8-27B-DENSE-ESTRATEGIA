# R009 — vLLM

**Nome canônico:** vLLM  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R009  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** vllm runtime

## R009:C01 — conceito

Projeto de inferência e serving de modelos, com gerenciamento KV, escalonamento e kernels especializados. É um runtime, não um modelo nem uma memória de agente. A documentação consultada lista batching contínuo, cache de prefixos, quantização e APIs de serving; suporte efetivo depende de arquitetura, versão e backend.

Como funciona:
- Carregar checkpoint e tokenizer com configuração de execução compatível.
- Administrar filas, estados e chamadas a kernels durante prefill e decode.
- Expor resultados, streaming e métricas ao cliente de aplicação.

## R009:C02 — aplicacao

Quando usar:
- Servir modelos abertos para múltiplas requisições com observabilidade.
- Comparar ajustes de throughput e latência sem reescrever o modelo.

Quando não usar:
- Presumir que um recurso listado funciona em toda combinação de quantização, arquitetura e GPU.

Implementação proposta:
- Fixar versão do runtime e revisão dos pesos numa configuração reproduzível.
- Validar chat template, parser de ferramentas e formato de saída antes de otimizar.
- Medir carga mista com limites de memória, tokens e requisições explícitos.

Aplicação LAI proposta:
Proposta LAI: usar como candidato de runtime configurável; este pacote não inspecionou nem alterou a instalação local do usuário.

## R009:C03 — riscos_validacao

Armadilhas:
- API compatível não significa semântica idêntica de todas as opções de outro provedor.
- Uma configuração que passa em chamada curta pode falhar sob contexto longo ou concorrência.

Métricas sugeridas:
- TTFT, ITL, goodput, erros e ocupação KV.
- Acerto de ferramentas e estabilidade em carga representativa.

Testes propostos:
- Reproduzir tarefas com e sem otimizações mantendo o checkpoint fixo e comparar correção e custo.
- Cancelar, reiniciar e sobrecarregar em ambiente de teste para verificar contratos operacionais.

## R009:C04 — perguntas_proveniencia

Pergunta: vLLM ensina o modelo a usar ferramentas?
Resposta: Não. Oferece serving e parsers; competência depende do checkpoint, template e avaliação.

Pergunta: As opções latest valem para minha versão instalada?
Resposta: Não necessariamente. A configuração deve ser conferida na documentação da versão real.

Pergunta: cache_salt resolve sozinho o isolamento entre clientes?
Resposta: Não. Ele participa da separação do cache; a própria documentação exige considerar outras superfícies compartilhadas.

Pergunta: Qual ganho medir primeiro?
Resposta: Separe prefill e decode; avalie TTFT sob carga antes de atribuir melhora global ao cache.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## R009:C05 — mecanismo_avancado

Em vLLM, o reúso de prefixos se apoia na identidade de blocos e de seus antecessores. Tokens iguais isoladamente não bastam quando adaptadores, conteúdo multimodal ou outros fatores alteram o cálculo. A documentação inclui identificadores adicionais e cache_salt na chave. A documentação de segurança também esclarece que compartilhar o processo servidor não oferece isolamento completo entre locatários. O gateway precisa definir o domínio de confiança antes de otimizar o cache.

Condição de contorno:
A presença de uma opção na documentação atual não comprova suporte no binário instalado; versão, arquitetura do checkpoint e configuração precisam ser registrados juntos.

Contrato proposto:
- Entradas: Revisão do modelo, tokenizer, adaptador, mensagens serializadas, identidade autorizada e política de cache por domínio.
- Saídas: Tokens gerados, motivo de término, uso reportado e métricas de prefill, decode, fila e reutilização.
- Estado: Mapa de blocos KV, referências ativas, filas de requisições e configuração efetiva do processo servidor.
- Invariante: Nenhuma solicitação deve selecionar diretamente o namespace de cache de outro domínio; identidades incompatíveis exigem separação ou miss.

Compromissos de projeto:
- Prefixos frequentes podem reduzir trabalho de prefill, mas dados mantidos ocupam memória que serviria à concorrência.
- Separar processos aumenta custo operacional; compartilhar requer avaliar explicitamente os limites reais de isolamento.

## R009:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: enviar prompts idênticos com adaptadores distintos e identidades separadas; verificar que não ocorre reúso incompatível e que um cancelamento libera recursos da requisição.

Plano de avaliação proposto:
Comparar cache desligado e ligado com distribuição fixa de comprimentos, concorrência e proporção de prefixos repetidos. Medir TTFT, latência entre tokens, throughput, memória e qualidade. Não extrapolar ganho de prefill para geração longa.

Comparações:
- T082 (complements): O servidor materializa cache de prefixos e outros mecanismos.
- T093 (complements): A gestão paginada de KV participa do uso eficiente de memória.

Afirmação rastreável:
A chave do cache de prefixos inclui contexto anterior e identidades adicionais; o processo compartilhado não é uma fronteira geral de isolamento.
Suporte: direct; fontes: V3D-S004, V3D-S005
Limite: Documentação atual consultada; nenhuma instalação ou configuração do usuário foi inspecionada.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R009:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 priorizou identidade do cache e isolamento. Esta camada transforma vLLM em uma opção de serviço a qualificar por workload, observabilidade e contrato do cliente, usando casos reais sem transferir suas configurações.

Escolha por workload
Prefill longo, decode longo e alta concorrência pressionam partes diferentes do runtime. Comece com uma configuração simples e meça fila, TTFT, intervalo entre tokens e respostas completas. Ativar todas as otimizações juntas impede identificar a causa de uma melhora ou regressão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

Recursos com maturidade distinta
A documentação atual inclui métricas experimentais de aceitação especulativa com restrições próprias. Trate disponibilidade e estabilidade por recurso e versão, não pelo nome vLLM. API de uso, motivo de término e métricas precisam ser validadas no cliente, inclusive em streaming e cancelamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

Casos que orientam hipóteses
LinkedIn descreve vLLM em Hiring Assistant e busca de vagas; Amazon relata Rufus com integração Neuron e execução multinó. Esses exemplos demonstram adoção em ambientes específicos. Não fixam hardware, versão, modelo ou melhor política para uma implantação 3–30B local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

USO AVANÇADO — Servidor especializado compartilhado
Cenário: Vários clientes usam modelos ou adapters relacionados.
Estratégia: Defina domínios de confiança, limites e identidade completa antes de otimizar prefixos. Teste batching e cache com carga representativa, monitorando justiça e cancelamento.
Papel do modelo pequeno: Um 8–14B pode atender tarefas de domínio com capacidade ajustada ao contexto real.
Aceite proposto: Qualidade-base preservada e prazos atendidos por cliente, sem mistura de estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

USO AVANÇADO — Avaliar especulação
Cenário: Respostas longas apresentam padrões repetitivos.
Estratégia: Escolha proponente compatível, confira métricas por pedido quando disponíveis e compare com alvo sozinho. Registre CPU, memória e capacidade, além da aceitação.
Papel do modelo pequeno: Um 15–30B pode ser alvo; 3–7B também é possível se o custo adicional compensar.
Aceite proposto: Ganho líquido no serviço e correção do algoritmo sob configurações reais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma réplica simples pode bastar; complexidade de orquestração deve responder a carga medida.
8–14B: Explore cache e batching antes de distribuir o modelo sem necessidade.
15–30B: Reserve KV e temporários, verificando topologia quando houver paralelismo.
Requisitos de treino/runtime: Runtime precisa suportar arquitetura, dtype, quantização e recursos escolhidos na versão fixada.
Não aplicar quando: Não presumir que endpoint semelhante a outra API oferece semântica idêntica ou isolamento completo entre locatários.

## R009:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 3. Lacuna: 7. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 3. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: vLLM é parte explícita do runtime lançado.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: vLLM é identificado como runtime do serviço.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: vLLM serve o componente de interpretação de consultas.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: O scorer offline implementado utiliza servidores vLLM.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4B-C023 — Snowflake / Suffix Decoding
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: pesquisa sobre LLM.
Uso observado: A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.
Mecanismo documentado: Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.
Correspondência com esta base: Integração com runtime não comprova toda configuração de vLLM.
Transferência proposta para modelo pequeno: Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.
Limite: Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.
Fontes: B-S040.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q018.

## R009:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R009 → T082 [complements]
Como combinar: O Hiring Assistant usa prefix caching no serving descrito pelo LinkedIn.
Interface: Prefixo compatível e configuração de serviço.
Condição: Escopo do caso documentado.
Aceite proposto: Medir tokens realmente reutilizados e latência.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

2. R009 → T088 [complements]
Como combinar: O mesmo caso descreve continuous batching junto ao serving vLLM.
Interface: Sequências ativas e política de lote.
Condição: Configuração e modelo compatíveis.
Aceite proposto: Avaliar carga aberta e prazos por requisição.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Fixar versões de modelo, tokenizer, runtime e parâmetros no manifest.
- Não promover resposta truncada a sucesso só porque o HTTP terminou normalmente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
vLLM é infraestrutura, não fonte de capacidade cognitiva. Compare o serviço completo de um modelo pequeno com fronteira em qualidade, custo e prazo sob condições explícitas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T088, T093, T094, T102

## Fontes primárias associadas

### B-S044 — vLLM — Welcome

[https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de inferência e serving com API, batching, gerenciamento KV e kernels especializados.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S004 — Automatic Prefix Caching — vLLM design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos, hash do prefixo anterior, tokens e fatores adicionais como adaptador, multimodalidade e cache_salt.

Limite: Documentação latest; não comprova configuração instalada nem ganho local.

### V3D-S005 — Security — vLLM

[https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md](https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites de isolamento em processos compartilhados e papel limitado de cache_salt.

Limite: Arquivo main consultado; namespace de cache não constitui isolamento geral entre locatários.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM

[https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvores de sufixos sobre tokens anteriores produzem candidatos especulativos sem modelo auxiliar.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

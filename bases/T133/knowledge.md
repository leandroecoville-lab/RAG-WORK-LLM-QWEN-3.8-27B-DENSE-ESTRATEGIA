# T133 — Model Routing

**Nome canônico:** Model Routing  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T133  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** roteamento de modelos

## T133:C01 — conceito

Seleção do modelo que atenderá uma solicitação segundo capacidade, custo, latência e restrições. O roteador pode usar regras ou um preditor aprendido. Ele decide onde executar; não torna o modelo escolhido mais capaz nem elimina a necessidade de verificar seu resultado.

Como funciona:
- Extrair sinais da tarefa, do tamanho do contexto e das capacidades necessárias.
- Excluir destinos incompatíveis com ferramentas, modalidade ou política de dados.
- Escolher o destino admissível e registrar a justificativa operacional da rota.

## T133:C02 — aplicacao

Quando usar:
- Carga heterogênea com tarefas simples e difíceis.
- Mais de um backend disponível com custo ou desempenho diferentes.

Quando não usar:
- Um único destino atende toda a carga sem vantagem medida de seleção.

Implementação proposta:
- Construir conjunto de tarefas com resultados de todos os modelos candidatos.
- Comparar regra simples com roteador aprendido usando separação temporal dos dados.
- Configurar limiar de qualidade, fallback e orçamento por missão.

Aplicação LAI proposta:
Proposta: encaminhar tarefas locais previsíveis ao Qwen e escalar casos difíceis somente quando o teste da tarefa justificar; medir a política antes de adotá-la.

## T133:C03 — riscos_validacao

Armadilhas:
- Roteador barato pode errar justamente nas tarefas mais difíceis.
- Medir apenas economia esconde aumento de retrabalho ou falhas.

Métricas sugeridas:
- Custo por tarefa aceita, incluindo escalonamentos.
- Qualidade por tipo de tarefa e taxa de encaminhamento incorreto.

Testes propostos:
- No mesmo conjunto reservado, comparar com sempre usar cada modelo isoladamente.
- Remover um backend e verificar se a decisão respeita capacidades e orçamento.

## T133:C04 — perguntas_proveniencia

Pergunta: O roteador sabe qual modelo acertará?
Resposta: Ele estima a adequação; a estimativa pode estar errada e precisa de avaliação.

Pergunta: Roteamento exige treinar uma rede?
Resposta: Não. Regras explícitas são um baseline útil antes de um classificador aprendido.

Pergunta: É correto interpretar escore 0,8 como 80% de acerto?
Resposta: Somente se o escore tiver essa semântica e calibração demonstrada; um limiar de roteamento pode representar outra quantidade.

Pergunta: Como evitar aprender apenas com rotas já escolhidas?
Resposta: Usar avaliação emparelhada separada, com resultados das alternativas e custo registrado, antes de alterar a política.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T133:C05 — mecanismo_avancado

O limiar de um roteador aprendido deve ser interpretado na distribuição usada para calibrá-lo. Selecionar uma fração de chamadas ao modelo forte não estabelece uma probabilidade universal de correção. Há ainda viés de observação: registrar somente a resposta do modelo escolhido impede saber como a alternativa se comportaria naquela pergunta. Uma avaliação offline emparelhada permite estimar essa diferença antes de atualizar a política.

Condição de contorno:
Uma mudança de domínio, idioma ou par de modelos pode alterar a ordenação de dificuldade e invalidar o limiar anterior.

Contrato proposto:
- Entradas: Consulta, capacidades obrigatórias, par de modelos versionado e orçamento restante.
- Saídas: Rota elegível, pontuação, versão da política e justificativa operacional.
- Estado: Distribuição de calibração, histogramas de escores e resultados por classe.
- Invariante: Restrições de capacidade são aplicadas antes da otimização de custo.

Compromissos de projeto:
- Aumentar chamadas ao modelo forte pode melhorar cobertura, mas o ganho marginal depende das perguntas deslocadas.
- Reavaliar ambos os modelos custa mais offline e reduz decisões baseadas em observações incompletas.

## T133:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: calibrar em consultas curtas e avaliar depois documentos longos com ferramentas obrigatórias; registrar desvio da fração roteada e recusar destinos incompatíveis.

Plano de avaliação proposto:
Comparar roteador, seleção única e política simples no mesmo conjunto reservado. Controlar versões, prompts e verificadores. Reportar qualidade por classe, custo por sucesso e curva de compromisso; adotar a política somente se satisfizer os critérios definidos para a tarefa.

Comparações:
- T135 (distinct_from): Roteamento inicial escolhe antes da resposta; cascata pode observar a primeira tentativa.

Afirmação rastreável:
O RouteLLM recomenda calibrar limiares com consultas semelhantes ao tráfego esperado.
Suporte: direct; fontes: V3C-S001
Limite: O repositório não garante que a fração estimada permaneça estável sob mudança de distribuição.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T133:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou calibração e avaliação emparelhada. A camada nova separa política de qualidade, contrato de capacidades e decisão operacional em duas fases, conservando evidências quando a rota muda.

Admissão anterior à preferência
Construa primeiro um conjunto elegível por idioma, ferramentas, limite de entrada e formato efetivamente testados. Só depois use a previsão de qualidade para escolher. Um modelo com menor custo não participa da disputa quando falha um requisito obrigatório; capacidade desconhecida recebe estado próprio, sem ser convertida em compatibilidade presumida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S011.

Rota como decisão versionada
Registre a versão da política, características observadas e candidatos recusados em um recibo. Se a execução ocorrer depois de uma espera, revalide disponibilidade e orçamento, mantendo o mesmo objetivo. Isso permite distinguir mudança de modelo causada pelo conteúdo de mudança causada por saturação, evitando misturar os dois fenômenos na recalibração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S012, V4C-S014.

Evidência de qualidade atrasada
Agrupe resultados por tipo de tarefa e revisão de modelo, pois aceitação pode chegar depois da resposta. Um patch aceito, revertido ou rejeitado produz sinais distintos. Atualizar o roteador apenas com likes ou respostas sintaticamente válidas incentivaria rotas que parecem baratas antes de contabilizar retrabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014.

USO AVANÇADO — Triagem de tickets com saída verificável
Cenário: Fila mistura extração de campos e investigação de incidentes.
Estratégia: Execute extrator econômico para campos fechados; direcione investigação com dependências a outro fluxo. Após validação, escale somente os campos ou perguntas sem suporte, levando os documentos originais, não apenas a interpretação anterior.
Papel do modelo pequeno: Um 3–7B pode classificar intenção e extrair candidatos delimitados.
Aceite proposto: Proposta: medir erros por classe, escalonamentos desnecessários e custo até aceite, incluindo tickets reabertos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S011, V4C-S014.

USO AVANÇADO — Revisão de mudanças por risco observado
Cenário: Há patches pequenos, mas com impactos muito diferentes.
Estratégia: Calcule superfície alterada, dependências e testes disponíveis em código. Use esses sinais para escolher revisão local ou análise mais ampla; se o diagnóstico não encontrar evidência, devolva insuficiência em vez de transformar confiança textual em aprovação.
Papel do modelo pequeno: Modelos 8–30B analisam trechos e justificam achados ligados a linhas.
Aceite proposto: Proposta: comparar com rota fixa de fronteira nos mesmos patches, contabilizando falsos positivos, bugs omitidos e reversões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S010, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificador compacto de classes fechadas; abstém-se em entradas fora do domínio calibrado.
8–14B: Proposta: executor de rotas conhecidas com recuperação de documentos e ferramentas validadas.
15–30B: Proposta: sintetizador de subtarefas difíceis, ainda sujeito a validação externa e escalonamento.
Requisitos de treino/runtime: Separar dados de calibração por projeto ou tempo; registrar versões e capacidades do servidor real.
Não aplicar quando: Não usar roteamento aprendido quando faltam rótulos de aceite ou a chamada do roteador custa mais que a tarefa.

## T133:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C013 — Uber / GenAI Gateway
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A Uber relata equipes internas utilizando o gateway para consultas a modelos externos e hospedados internamente.
Mecanismo documentado: Adaptadores expõem uma interface comum e integram autenticação, política de dados, métricas e atribuição de custos.
Correspondência com esta base: A plataforma oferece acesso a diferentes modelos, sem provar roteador de qualidade por pergunta nesta publicação.
Transferência proposta para modelo pequeno: Proposta: centralizar adapters de 3–30B e registrar capacidades reais de cada endpoint; separar seleção do modelo da tradução de protocolos e da medição do custo por tarefa aceita.
Limite: Interface compatível não torna modelos semanticamente equivalentes. Não mapear automaticamente disponibilidade de múltiplos fornecedores a cascata ou fallback comprovado.
Fontes: V4C-S012.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: A fonte descreve seleção por workload, modelo principal e padrão de subagentes; estratégias mais amplas de routing são discutidas como direção futura, não decisão preditiva por consulta demonstrada.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C012 — Amazon Web Services / Amazon Bedrock Intelligent Prompt Routing
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação disponibiliza um endpoint de roteamento que prevê qualidade e escolhe entre dois modelos compatíveis da mesma família.
Mecanismo documentado: Configuração define modelos, critério e fallback; resposta informa o modelo usado. A página é documentação de produto, não relato de implantação de um cliente.
Correspondência com esta base: Escolha de modelo por consulta é o recurso documentado.
Transferência proposta para modelo pequeno: Proposta: comparar um roteador local 3–30B com regras simples, rotas fixas e escalonamento após validação. Rejeitar candidatos sem capacidade necessária antes de estimar qualidade.
Limite: Classificado como operational_product. Não conta para dez casos comprovados em produção; lista de modelos e regiões muda. Exemplos com modelos maiores não validam as bandas pequenas.
Fontes: V4C-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Bedrock é recurso de produto; Uber descreve seleção operacional por carga. Nenhum deles demonstra dez deployments de roteamento 3–30B.
Consultas registradas: V4C-Q008, V4C-Q009.

## T133:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T133 → T173 [feeds]
Como combinar: A escolha inicial informa candidatos elegíveis; fallback só usa os que preservam requisitos.
Interface: Recibo de rota, capacidades, objetivo e orçamento residual.
Condição: O erro é classificado antes da troca.
Aceite proposto: Injetar falha e conferir que a rota alternativa não relaxa o formato exigido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T133 → T171 [complements]
Como combinar: Residência de cache entra no custo operacional depois da elegibilidade de qualidade.
Interface: Prefixo identificado, versão do modelo e custo estimado de recomputação.
Condição: A chave representa o mesmo cálculo.
Aceite proposto: Comparar custo total com e sem preferência por cache mantendo qualidade aceita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S014, V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar rejeição por capacidade de erro de conteúdo na telemetria.
- Suspender atualização automática quando rótulos de aceitação atrasarem ou mudarem de significado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo por tarefa aceita e erro por classe com modelo de fronteira fixo. Uma rota pequena que vence em extração não demonstra equivalência em planejamento aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T134, T135, T173, T203

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

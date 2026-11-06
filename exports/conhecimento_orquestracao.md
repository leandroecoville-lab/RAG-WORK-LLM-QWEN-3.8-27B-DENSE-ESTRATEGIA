# Orquestração, execução e resiliência

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

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


---

# T134 — Semantic Routing

**Nome canônico:** Semantic Routing  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T134  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** roteamento semântico

## T134:C01 — conceito

Encaminhamento baseado no significado da solicitação, normalmente representado por embeddings, classificação ou uma LLM. Pode selecionar modelo, ferramenta ou workflow. A proximidade semântica ajuda a reconhecer a intenção, mas não demonstra dificuldade, autorização ou chance de acerto.

Como funciona:
- Representar a pergunta e comparar com intenções ou exemplos de referência.
- Produzir rótulo de rota e uma medida de separação entre alternativas.
- Usar rota de abstenção quando a decisão for ambígua.

## T134:C02 — aplicacao

Quando usar:
- Catálogo de intenções com vocabulário variável.
- Entrada em linguagem natural que precisa escolher uma capacidade conhecida.

Quando não usar:
- Regras de autorização ou limites financeiros que exigem decisão determinística.

Implementação proposta:
- Criar exemplos positivos e negativos para cada rota.
- Avaliar erros entre intenções vizinhas e perguntas com múltiplas intenções.
- Separar o classificador de intenção da checagem de permissões e disponibilidade.

Aplicação LAI proposta:
Proposta: classificar solicitações da Helena por capacidade e então aplicar uma política separada para escolher executor e modelo.

## T134:C03 — riscos_validacao

Armadilhas:
- Embeddings similares podem esconder requisitos de execução diferentes.
- Limiares treinados em um domínio degradam após mudança de vocabulário.

Métricas sugeridas:
- Matriz de confusão por intenção.
- Cobertura e erro nos exemplos que o roteador aceita.

Testes propostos:
- Testar paráfrases, negações e pedidos que combinam duas tarefas.
- Inserir tema fora do catálogo e exigir abstenção ou descoberta adicional.

## T134:C04 — perguntas_proveniencia

Pergunta: Semantic routing é busca RAG?
Resposta: Ambos podem usar embeddings, mas o roteamento escolhe um destino e a busca recupera conteúdo.

Pergunta: Similaridade alta autoriza uma ação?
Resposta: Não. Autorização depende da identidade, do recurso e da operação.

Pergunta: Uma margem alta prova que a rota está correta?
Resposta: Não. Um pedido fora do domínio pode ficar relativamente mais perto de uma classe errada que das demais.

Pergunta: Como representar duas intenções legítimas?
Resposta: Decompor o pedido ou produzir um conjunto de destinos com dependências explícitas, sem esconder a segunda intenção em uma classe única.

Escopo das fontes:
RouteLLM e os workflows documentados sustentam seleção por sinais da entrada; o fluxo semântico aqui é uma proposta genérica, não uma reprodução de algoritmo específico.

## T134:C05 — mecanismo_avancado

Um classificador semântico precisa distinguir intenção e elegibilidade operacional. Duas consultas quase iguais podem exigir ferramentas diferentes quando muda o tipo de entidade ou o escopo. Em uma proposta baseada em vetores, a distância ao protótipo e a margem entre as duas melhores classes oferecem sinais diferentes: a primeira detecta afastamento geral; a segunda revela ambiguidade entre destinos conhecidos. Nenhum desses sinais resolve sozinho pedidos com múltiplas intenções.

Condição de contorno:
Quando todas as classes estão distantes ou o pedido combina ações incompatíveis, forçar a classe mais próxima produz encaminhamento artificial.

Contrato proposto:
- Entradas: Texto, catálogo de rotas, exemplos representativos e restrições da tarefa.
- Saídas: Classe ou conjunto de classes, evidências de seleção e estado de ambiguidade.
- Estado: Versão do encoder, protótipos, rótulos e limiares por classe.
- Invariante: Um destino semanticamente parecido continua sujeito aos requisitos de capacidade.

Compromissos de projeto:
- Mais protótipos capturam variedade, mas aumentam manutenção e oportunidades de sobreposição.
- Uma rota de revisão para casos ambíguos acrescenta latência e reduz encaminhamento indevido.

## T134:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar pares que diferem somente no escopo, além de pedidos fora do catálogo; exigir distinção do primeiro grupo e ambiguidade explícita no segundo.

Plano de avaliação proposto:
Comparar regras lexicais, embeddings e classificação por modelo em exemplos separados por intenção e período. Medir matriz de confusão, cobertura e erros entre rotas incompatíveis. Ajustar limiares em validação e preservar teste final sem reutilização.

Comparações:
- T133 (distinct_from): Escolher domínio ou workflow por significado não estima automaticamente qual modelo resolverá melhor.
- T148 (complements): O rótulo validado pode alimentar uma condição do grafo.

Afirmação rastreável:
RouteLLM demonstra que decisões de roteamento e seus limiares dependem das consultas utilizadas na calibração.
Suporte: related; fontes: V3C-S001
Limite: A fonte apoia o princípio de calibração; protótipos, margens e abstinência nesta ficha são proposta de arquitetura semântica.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T134:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu margem, distância e elegibilidade. O aprofundamento adiciona roteamento hierárquico com resolução de entidade, múltiplas intenções e revisão do catálogo durante a execução.

Intenção não é endereço
Separe o rótulo semântico da identidade do recurso. Classificar uma mensagem como consulta financeira não determina conta, período ou ferramenta autorizada. Uma segunda etapa resolve esses parâmetros em dados confiáveis, evitando que semelhança de nomes seja tratada como autorização para operar sobre um objeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Hierarquia com custo de descoberta
Para catálogos extensos, selecione domínio, servidor e ferramenta em etapas, carregando descrições progressivamente. Cada descida consome contexto e pode propagar erro; retenha alternativas plausíveis até validar o schema e as pré-condições. Não force uma rota completa se o primeiro nível continua ambíguo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Mudança de significado controlada
Versione exemplos, rótulos e ferramentas que os implementam. Ao dividir uma categoria antiga em duas, reavalie consultas fronteiriças e preserve a rota usada por missões em andamento. Uma alteração editorial na descrição pode mudar a seleção mesmo quando o código da ferramenta permanece idêntico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S004.

USO AVANÇADO — Descoberta em catálogo corporativo
Cenário: Um assistente precisa escolher entre ferramentas de equipes distintas.
Estratégia: Recupere poucos servidores por intenção; peça schema somente dos candidatos relevantes; confirme campos essenciais por catálogo ou pergunta. Se o domínio não oferece a operação, pare a descoberta com motivo, sem percorrer todo o catálogo indefinidamente.
Papel do modelo pequeno: 3–7B classifica domínios; 8–14B resolve composição curta de argumentos.
Aceite proposto: Proposta: medir ferramenta correta, etapas de descoberta e chamadas a destinos incompatíveis, usando intenções novas e ambíguas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Pedido com ações independentes
Cenário: Uma mensagem pede consultar estoque e preparar uma descrição comercial.
Estratégia: Decomponha intenções com saídas separadas; confirme dependências antes de permitir paralelismo. A consulta fornece fatos versionados à redação quando necessário. Não permita que uma rota textual execute implicitamente a mutação descrita no pedido.
Papel do modelo pequeno: 15–30B pode decompor solicitações compostas, com validação determinística das rotas.
Aceite proposto: Proposta: aceitar apenas quando todas as intenções obrigatórias têm resultado ou impedimento identificado e nenhum efeito excede o escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: reconhecer poucas classes estáveis e devolver desconhecido quando faltam entidades.
8–14B: Proposta: selecionar ferramentas de um domínio e explicar ambiguidades entre contratos semelhantes.
15–30B: Proposta: decompor pedidos com várias intenções e produzir dependências explicitamente verificáveis.
Requisitos de treino/runtime: Usar negativos difíceis, rótulos versionados e catálogo carregado por revisão; não basta ajustar embeddings.
Não aplicar quando: Evitar quando o destino correto depende de fatos ausentes que a linguagem da consulta não fornece.

## T134:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Descoberta de servidor utiliza intenção da consulta.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Roteamento entre tarefas é relatado, sem protocolo exato de seleção de ferramentas.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Omni MCP documenta descoberta por intenção. A arquitetura hierárquica proposta deve ser validada no catálogo local, sem alegar adoção das bandas pequenas.
Consultas registradas: V4C-Q009, V4C-Q010.

## T134:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T134 → T151 [feeds]
Como combinar: A classificação reduz o conjunto cujos schemas serão carregados.
Interface: Domínio candidato, IDs de ferramentas e versão do catálogo.
Condição: A descoberta mantém opção de retornar ao nível anterior.
Aceite proposto: Testar categoria errada e exigir recuperação ou abstenção, sem execução indevida.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

2. T134 → T148 [feeds]
Como combinar: O rótulo validado vira guarda, sem entregar o controle inteiro ao classificador.
Interface: Enum de rota, entidades resolvidas e estado desconhecido.
Condição: Pré-condições são verificadas novamente antes da ação.
Aceite proposto: Pedidos ambíguos devem seguir uma saída de esclarecimento ou investigação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar rótulo de intenção após mudança material do pedido.
- Registrar catálogos vazios e contratos ausentes como limites, sem inventar ferramenta equivalente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare com fronteira na seleção de ferramentas sob catálogo idêntico. O teste mede roteamento e cobertura de intenções, não capacidade geral de resolver cada domínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T148

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S013 — Workflows and agents

[https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento e arestas condicionais selecionam fluxos conforme estado ou classificação da entrada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T135 — Model Cascade

**Nome canônico:** Model Cascade  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T135  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cascata de modelos

## T135:C01 — conceito

Cascata executa modelos em sequência e decide, após cada resposta, se já existe qualidade suficiente ou se deve escalar. Diferencia-se do roteamento inicial porque consome o resultado de uma etapa para escolher a próxima. O custo inclui todas as etapas percorridas.

Como funciona:
- Consultar o estágio inicial de menor custo admissível.
- Validar a resposta por critérios externos ou estimativa calibrada.
- Encerrar quando aceita ou encaminhar ao próximo estágio dentro do orçamento.

## T135:C02 — aplicacao

Quando usar:
- Tarefas com verificador barato e objetivo.
- Muitos casos fáceis e uma minoria que exige modelo mais capaz.

Quando não usar:
- Quando quase todas as tarefas percorrem a cascata inteira ou o avaliador não distingue erros.

Implementação proposta:
- Definir estágios, saída padronizada e critério de aceite.
- Calibrar o limiar usando casos não utilizados para ajustar a política.
- Registrar custo acumulado, motivo de escalada e mudança de resposta.

Aplicação LAI proposta:
Proposta: testar extração estruturada local seguida de validação; escalar somente falhas de conteúdo ou incerteza real, sem repetir chamadas que já atenderam ao contrato.

## T135:C03 — riscos_validacao

Armadilhas:
- Confiança declarada pelo próprio modelo pode aceitar resposta errada.
- Vários estágios ampliam latência de cauda e custo de tarefas difíceis.

Métricas sugeridas:
- Fração resolvida em cada estágio.
- Custo e latência por resultado correto, comparados ao melhor destino único.

Testes propostos:
- Injetar resposta plausível porém errada no primeiro estágio e verificar a rejeição.
- Comparar a cascata em orçamento total equivalente ao baseline.

## T135:C04 — perguntas_proveniencia

Pergunta: Cascata sempre economiza?
Resposta: Não. Muitas escaladas podem custar mais que chamar diretamente o modelo final.

Pergunta: Um erro de rede é o mesmo que baixa qualidade?
Resposta: Não. Falhas operacionais e de conteúdo precisam de políticas separadas.

Pergunta: Uma primeira chamada barata sempre reduz a conta?
Resposta: Não. Seu custo soma-se ao avaliador e às escaladas; pode acrescentar despesa a todas as tarefas difíceis.

Pergunta: Devo passar a primeira resposta ao modelo seguinte?
Resposta: É uma opção experimental: comparar reaproveitamento com resolução independente para medir ancoragem e consumo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T135:C05 — mecanismo_avancado

Para uma cascata de dois modelos, um modelo simplificado de custo é E[C]=c₁+cᵥ+pₑ·c₂, onde c₁ e c₂ são custos médios das chamadas, cᵥ o custo de avaliação e pₑ a probabilidade de escalonamento. A fórmula exige explicitar se o segundo modelo recebe a primeira resposta, pois isso muda custo e pode propagar seu erro. A latência de quem escala inclui a etapa anterior, mesmo quando a média global diminui.

Condição de contorno:
Se a primeira etapa aceita erros difíceis de detectar ou quase todas as tarefas escalam, a economia prevista pode desaparecer.

Contrato proposto:
- Entradas: Pergunta, candidatos de modelos, contrato de aceitação e orçamento total.
- Saídas: Resposta aceita ou escalonamento, trilha de custos e resultados dos verificadores.
- Estado: Ordem da cascata, limiares e histórico de tentativas.
- Invariante: Cada nova etapa consome o orçamento remanescente e preserva a identidade da tarefa.

Compromissos de projeto:
- Um avaliador forte detecta mais erros, mas pode custar tanto quanto executar diretamente o modelo seguinte.
- Reutilizar a tentativa anterior economiza trabalho e pode ancorar o próximo modelo em uma conclusão errada.

## T135:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer respostas curtas e convincentes, porém incorretas, ao critério de aceitação; observar se erros atravessam a cascata sem escalonamento.

Plano de avaliação proposto:
Comparar execução direta, roteamento inicial e cascata com o mesmo conjunto. Medir falsa aceitação, custo completo e latência dos casos escalados. Separar custo do avaliador e dos modelos; decidir por qualidade exigida e distribuição real de escalonamento.

Comparações:
- T133 (alternative): Um roteador pode evitar pagar pela etapa inicial nas tarefas já reconhecidas como difíceis.

Afirmação rastreável:
FrugalGPT trata cascatas de modelos como estratégia de controle conjunto de custo e desempenho.
Suporte: direct; fontes: C-S002
Limite: A expressão de custo é uma simplificação editorial; dependências e custos condicionais precisam ser medidos.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T135:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 formalizou custo esperado e propagação da primeira resposta. A camada nova usa cascatas por evidência e orçamento de erro, com transferência seletiva de artefatos entre estágios.

Portões heterogêneos
Não use um único escore de confiança em todos os estágios. Extração pode ser verificada por schema e localização; cálculo por execução; resposta documental por cobertura das fontes. A cascata só escala quando o verificador identifica uma lacuna específica que o estágio seguinte tem chance de resolver.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, C-S002.

Escalonar evidência, não persuasão
Prepare um pacote com entrada original, fatos confirmados, falhas do verificador e trechos necessários. A resposta anterior entra como candidato explicitamente falível. Em tarefas suscetíveis a ancoragem, execute a rota forte primeiro sem o candidato e compare depois; esse custo adicional precisa entrar na avaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S002.

Interrupção com resultado parcial
Reserve uma etapa de encerramento antes de consumir todo o orçamento. Ela identifica o que foi confirmado, o que ficou pendente e o motivo de parada. Um último modelo mais forte não deve ser iniciado quando o prazo restante não permite executar também sua verificação obrigatória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S011, V2A-S012.

USO AVANÇADO — Extração documental com resolução localizada
Cenário: Documentos contêm campos simples e poucas cláusulas ambíguas.
Estratégia: O modelo econômico extrai campos com referências; regras validam formato e consistência. Reenvie apenas cláusulas inconclusivas junto de contexto suficiente. Se a ambiguidade for documental, preserve-a em vez de continuar pagando por modelos maiores.
Papel do modelo pequeno: 3–7B executa extração fechada; 15–30B examina exceções com fontes.
Aceite proposto: Proposta: comparar custo total, campos corrigidos e erros introduzidos na escalada, sem esconder documentos abandonados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S002, V4C-S014.

USO AVANÇADO — Cascata de reparadores de CI
Cenário: Falhas de build incluem ajustes mecânicos e problemas semânticos.
Estratégia: Aplique reparadores determinísticos reconhecidos; encaminhe os demais a um modelo com escopo de arquivos restrito. Rode CI novamente e finalize após limite sem progresso. Nunca permita alterar código de produção apenas para contornar um teste válido.
Papel do modelo pequeno: 8–14B propõe reparos locais; 15–30B analisa dependências entre falhas.
Aceite proposto: Proposta: medir correções aceitas, regressões e alterações fora do escopo em falhas reais retidas da calibração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: primeiro estágio para respostas curtas verificáveis e seleção de regras mecânicas.
8–14B: Proposta: resolver exceções locais depois de receber diagnósticos concretos, sem revisar tudo novamente.
15–30B: Proposta: último estágio local para integração de evidências, com possibilidade explícita de encaminhar além da banda.
Requisitos de treino/runtime: O verificador precisa detectar erro relevante melhor que mera autoconfiança; contabilizar todos os estágios.
Não aplicar quando: Não usar quando quase toda tarefa exige a rota forte ou quando o verificador aprova sistematicamente respostas erradas.

## T135:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean mostra cascata de reparadores, não prova uma cascata universal de tamanhos de LLM. Bedrock routing é recurso distinto de cascata pós-resposta.
Consultas registradas: V4C-Q008, V4C-Q009, V4C-Q006.

## T135:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T135 → T200 [complements]
Como combinar: O portão precisa de evidência separada para decidir se continua.
Interface: Resultado por critério, falha localizada e artefato avaliado.
Condição: A independência exigida é funcional; erro correlacionado deve ser medido.
Aceite proposto: Testar candidatos plausíveis mas incorretos e observar escalonamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S002, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T135 → T220 [complements]
Como combinar: Falhas reconhecidas alimentam reparo de chamada antes de trocar de modelo.
Interface: Erro tipado, argumentos originais e schema vigente.
Condição: Não existe efeito remoto ainda desconhecido.
Aceite proposto: Confirmar que reparar formato não cria nova intenção de negócio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009, V3C-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Impedir que cada estágio reinicie o orçamento da tarefa.
- Separar rejeição por falta de evidência de rejeição por indisponibilidade operacional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare cascata com fronteira fixa na mesma carga e com todas as tarefas contabilizadas. Economia média pode esconder latência pior e erros concentrados em casos difíceis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T136, T190

## Fontes primárias associadas

### C-S002 — FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

[https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cascatas de modelos e decisões de encaminhamento podem ser otimizadas sob orçamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S038 — LangChain — Prebuilt middleware

[https://docs.langchain.com/oss/python/langchain/middleware/built-in](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Middleware de erro de ferramenta é distinto de retry; ordem de composição determina tratamento de exceções e limites.

Limite: Documentação dinâmica com requisitos de versão; não se pressupõe disponibilidade de classes no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T136 — Fallback Chains

**Nome canônico:** Fallback Chains  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T136  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cadeia de contingência

## T136:C01 — conceito

Cadeia de alternativas acionadas quando uma operação falha ou fica indisponível. Cada transição precisa definir erro elegível, destino, orçamento restante e semântica preservada. Fallback é um mecanismo de resiliência; trocar de fornecedor não resolve automaticamente uma resposta incorreta.

Como funciona:
- Classificar falha de transporte, limite de taxa, capacidade ou contrato.
- Selecionar a próxima alternativa permitida para aquela classe de falha.
- Encerrar com erro explícito quando nenhuma alternativa segura atende ao contrato.

## T136:C02 — aplicacao

Quando usar:
- Dependências remotas sujeitas a indisponibilidade.
- Sistemas que toleram qualidade ou funcionalidades reduzidas explicitamente definidas.

Quando não usar:
- Alternativa viola residência de dados, permissões ou efeito de negócio esperado.

Implementação proposta:
- Declarar cadeia acíclica com limite global de tentativas e tempo.
- Propagar chave de idempotência e identificador de correlação.
- Validar schema e capacidades do destino antes de refazer a operação.

Aplicação LAI proposta:
Proposta: definir alternativas explícitas para inferência e consultas da Helena, registrando quando houve degradação ou mudança de modelo.

## T136:C03 — riscos_validacao

Armadilhas:
- Fallback pode repetir efeito já concluído cuja resposta se perdeu.
- Cadeias escondidas em várias camadas multiplicam chamadas e custo.

Métricas sugeridas:
- Taxa de recuperação por tipo de falha.
- Número total de tentativas e custo extra por solicitação.

Testes propostos:
- Simular timeout após commit e exigir reconciliação antes de repetir escrita.
- Indisponibilizar todos os destinos e conferir término limitado, sem loop.

## T136:C04 — perguntas_proveniencia

Pergunta: Fallback é retry?
Resposta: Retry repete uma tentativa; fallback muda o caminho ou serviço.

Pergunta: Pode trocar de modelo sem checar ferramentas?
Resposta: Não. O destino deve cumprir o contrato necessário à etapa.

Pergunta: Por que duas alternativas podem falhar juntas?
Resposta: Porque podem compartilhar provedor, quota, banco, rede ou serviço de recuperação, embora apresentem nomes diferentes.

Pergunta: Posso substituir silenciosamente uma resposta parcialmente transmitida?
Resposta: Somente com um contrato explícito de substituição; o consumidor precisa saber qual tentativa e versão está recebendo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T136:C05 — mecanismo_avancado

Uma cadeia de alternativas precisa conservar a semântica do resultado e classificar em que momento a primeira rota falhou. Antes do envio, a troca costuma ser simples; depois de uma resposta parcial ou de um possível efeito remoto, existe estado a reconciliar. A disponibilidade de outro fornecedor não resolve essa ambiguidade. Quotas e dependências compartilhadas também tornam falhas correlacionadas: duas URLs podem terminar no mesmo serviço congestionado.

Condição de contorno:
Fallback perde utilidade quando todos os destinos compartilham o gargalo ou quando a mudança altera um requisito obrigatório.

Contrato proposto:
- Entradas: Operação, estágio da falha, destinos elegíveis e deadline global.
- Saídas: Destino escolhido, estado migrado e desfecho confirmado ou desconhecido.
- Estado: Rotas já visitadas, custos acumulados e identificadores das tentativas.
- Invariante: Nenhum ciclo reinicia o prazo ou apaga um possível efeito já enviado.

Compromissos de projeto:
- Diversidade de fornecedores reduz algumas correlações e aumenta diferenças de contrato.
- Migrar contexto integral facilita continuidade, mas custa tokens e exige preservar versões e formatos.

## T136:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o primeiro destino após produzir saída parcial e simular saturação também no segundo; a cadeia deve terminar dentro do prazo, sem fundir respostas como se fossem uma execução única.

Plano de avaliação proposto:
Comparar falha explícita, fila e fallback sob os mesmos incidentes injetados. Medir objetivos concluídos, custo ampliado, atraso e incompatibilidades semânticas. Escolher alternativas por capacidade observada e independência de falhas, não apenas pelo número de endpoints.

Comparações:
- T173 (complements): Model Fallback Controlado detalha o caso específico de troca de modelo dentro de uma cadeia geral de alternativas.
- T243 (complements): Desfechos remotos incertos exigem reconciliação antes de uma repetição equivalente.

Afirmação rastreável:
O tratamento de sobrecarga precisa considerar como os clientes reagem às rejeições para evitar ampliar o incidente.
Suporte: related; fontes: V3C-S009
Limite: A fonte de SRE apoia a dinâmica de sobrecarga; migração entre modelos é uma proposta específica desta ficha.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T136:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu falhas correlacionadas e resultados ambíguos. Aqui a cadeia vira um protocolo de degradação explícita, com classes de substituição e capacidade reservada para recuperação.

Níveis de equivalência
Classifique alternativas como equivalente de contrato, resultado degradado permitido ou impossibilidade. Trocar endpoint mantendo schema não garante a mesma cobertura factual. A camada consumidora precisa receber o nível de serviço entregue e quais requisitos foram adiados, para não usar uma resposta parcial como confirmação completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S005, V4C-S011.

Reserva em vez de migração em massa
Se todos os clientes migram simultaneamente para a alternativa, ela pode falhar pelo próprio mecanismo de recuperação. Reserve admissão para casos prioritários e limite a taxa de transferência. A fila de espera conserva prazo e intenção; não gere uma segunda fila invisível dentro de cada cliente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V2A-S012.

Sessão portátil somente por contrato
A passagem entre modelos deve reconstruir mensagens, resultados de ferramentas e restrições numa representação neutra. Estado interno de raciocínio ou cache não é necessariamente transportável. Verifique o pacote no tokenizer e no formato de ferramentas do destino antes de iniciar a continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S012, V3C-S004.

USO AVANÇADO — Assistente que perde o provedor principal
Cenário: O endpoint remoto falha enquanto um modelo local continua disponível.
Estratégia: Encaminhe apenas tarefas que o local consegue atender com fontes e verificadores existentes. Para pesquisa aberta, reduza o escopo autorizado ou adie a etapa; preserve o estado confirmado e informe o que não foi concluído.
Papel do modelo pequeno: 3–30B pode manter extração, classificação e consultas locais delimitadas.
Aceite proposto: Proposta: injetar indisponibilidade e medir tarefas concluídas corretamente, degradações comunicadas e sobrecarga transferida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S005, V4C-S012.

USO AVANÇADO — Falha durante fluxo de edição
Cenário: O modelo deixa um patch parcial antes de perder conexão.
Estratégia: Congele o candidato como artefato não aceito, valide aplicabilidade e registre a base. O substituto recebe o objetivo e diferenças, podendo continuar ou descartar o candidato. Nenhuma parte é publicada apenas porque o primeiro endpoint caiu.
Papel do modelo pequeno: 8–14B recupera alterações locais; 15–30B replaneja dependências confirmadas.
Aceite proposto: Proposta: verificar que o resultado final corresponde a uma única revisão testada, sem misturar fragmentos incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: contingência para funções estreitas com saída verificável, sem assumir o papel integral do principal.
8–14B: Proposta: continuidade de subtarefas com contexto reconstruído e contratos conhecidos.
15–30B: Proposta: alternativa local mais ampla, ainda sem equivalência automática a um modelo de fronteira.
Requisitos de treino/runtime: Adapters devem preservar mensagens e erros; a reserva de capacidade precisa ser medida sob falha simultânea.
Não aplicar quando: Não usar troca automática quando o destino não oferece capacidade obrigatória ou existe efeito externo não reconciliado.

## T136:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Resposta degradada é alternativa operacional, sem ser necessariamente troca de modelo.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes mostram degradação e contratos de rotas; dez cadeias específicas de fallback LLM em produção não foram identificadas nesta busca.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q008.

## T136:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T136 → T175 [complements]
Como combinar: A admissão da rota alternativa respeita quota própria e prioridade.
Interface: Capacidade livre, classe de degradação e orçamento restante.
Condição: A alternativa não compartilha o mesmo gargalo oculto.
Aceite proposto: Simular queda global e exigir fila limitada e motivo de rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T136 → T211 [complements]
Como combinar: Continuação entre sessões precisa transportar estado confirmado de modo legível ao novo executor.
Interface: Objetivo, artefatos, pendências e revisão da memória externa.
Condição: Handoff é suficiente para a subtarefa escolhida.
Aceite proposto: Retomar sem histórico conversacional e comparar requisitos preservados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015, V2A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não concatenar streams de modelos diferentes como uma única resposta sem revalidação.
- Limitar tentativas em toda a cadeia e conservar quem realizou cada possível efeito.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade útil e correção com a rota de fronteira em cenários de falha. Manter serviço parcial com 3–30B é um resultado distinto de paridade geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T135, T138, T162, T173, T175

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T137 — Rate Limiting

**Nome canônico:** Rate Limiting  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T137  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de taxa

## T137:C01 — conceito

Controle da taxa de admissão de solicitações para respeitar capacidade, quotas e equidade. Pode medir requisições, tokens, bytes ou unidades de custo. Limitar frequência é diferente de limitar concorrência: operações longas podem acumular mesmo com poucas entradas por segundo.

Como funciona:
- Associar cada pedido às quotas globais, de destino e de cliente.
- Verificar saldo ou janela antes de admitir a operação.
- Enfileirar com prazo ou rejeitar de forma explícita quando não houver capacidade.

## T137:C02 — aplicacao

Quando usar:
- API com quota de chamadas ou tokens.
- Serviço compartilhado em que um cliente pode consumir capacidade excessiva.

Quando não usar:
- Usar apenas limite de requisições quando o consumo depende principalmente do tamanho de cada pedido.

Implementação proposta:
- Escolher token bucket ou janela conforme o contrato do fornecedor.
- Em múltiplas réplicas, coordenar o contador ou particionar quota sem ultrapassar o total.
- Reservar consumo estimado e reconciliar com o uso real após a resposta.

Aplicação LAI proposta:
Proposta: coordenar quotas de inferência e ferramentas da Helena com custo estimado por chamada, além de um limite de tarefas simultâneas.

## T137:C03 — riscos_validacao

Armadilhas:
- Limites apenas por processo falham quando o número de réplicas aumenta.
- Retries imediatos transformam limitação em tempestade de tráfego.

Métricas sugeridas:
- Taxa admitida, rejeitada e tempo na fila.
- Consumo real versus quota por tenant e backend.

Testes propostos:
- Submeter rajada controlada e verificar o limite durante toda a janela.
- Executar clientes concorrentes e confirmar que um não esgota todas as reservas.

## T137:C04 — perguntas_proveniencia

Pergunta: Um semáforo substitui rate limit?
Resposta: Não. O semáforo limita operações simultâneas; o rate limit controla admissão no tempo.

Pergunta: Token do bucket é token da LLM?
Resposta: Pode representar essa unidade, mas é apenas uma unidade de orçamento escolhida.

Pergunta: Tokens faturados podem ser usados diretamente como sinal de admissão?
Resposta: São úteis para reconciliação, mas chegam tarde para impedir o consumo já iniciado; é necessária estimativa ou reserva prévia.

Pergunta: Dividir uma quota por réplicas é sempre eficiente?
Resposta: Não. Uma réplica ociosa pode reter saldo enquanto outra rejeita trabalho; redistribuição introduz outro compromisso de coordenação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T137:C05 — mecanismo_avancado

Limitar unidades heterogêneas exige decidir quando o custo é conhecido. Em geração, tokens de saída são observados ao final; uma proposta é reservar capacidade antes do envio e reconciliar consumo posteriormente. Uma reserva conservadora reduz excesso e pode deixar capacidade ociosa. Em múltiplas réplicas, limitadores locais com orçamento completo multiplicam a admissão global; particionamento de quotas e coordenação têm propriedades diferentes.

Condição de contorno:
Uma taxa aceitável não protege memória quando a duração das chamadas cresce; também é necessário observar trabalho simultâneo e tamanho das filas.

Contrato proposto:
- Entradas: Identidade da quota, custo estimado, unidade contábil e prazo da requisição.
- Saídas: Admissão, espera ou rejeição, com reserva e motivo identificáveis.
- Estado: Saldo, reposição, reservas em aberto e consumo confirmado.
- Invariante: A mesma capacidade não é reservada duas vezes por réplicas concorrentes.

Compromissos de projeto:
- Coordenação global aproxima a quota total, acrescentando comunicação e um ponto operacional adicional.
- Reservas pelo teto de saída reduzem ultrapassagem e diminuem utilização quando respostas são curtas.

## T137:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: liberar requisições simultâneas em várias réplicas e atrasar a conclusão de algumas; verificar orçamento global, devolução de reservas e limite de concorrência.

Plano de avaliação proposto:
Comparar quotas locais, partilhadas e coordenadas sob carga estável e rajadas. Controlar distribuição de tamanhos e duração. Medir excesso admitido, utilização, espera e justiça por cliente. Escolher conforme tolerância contratual a rajadas e consistência.

Comparações:
- T167 (complements): Token bucket fornece um mecanismo de saldo; a política decide unidade, escopo e reserva.
- T175 (complements): Uma rejeição pode acionar alternativa somente dentro das quotas elegíveis.

Afirmação rastreável:
A documentação de retries da AWS distingue a quota de repetições da admissão da primeira chamada.
Suporte: direct; fontes: V3C-S010
Limite: Esse bucket específico não implementa automaticamente o orçamento total de tokens de uma aplicação.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T137:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou reserva de tokens e limites globais entre réplicas. O novo desenho combina admissão por dimensão, prioridades de negócio e liquidação de custos quando chamadas terminam parcialmente.

Vetor de recursos
Uma requisição pode consumir slots, tokens de entrada, geração e memória de contexto. Limitar apenas requests por segundo permite que poucas conversas longas ocupem o servidor. Uma proposta usa reservas por dimensão e só admite quando todas as obrigatórias cabem, mantendo a unidade de cada contador visível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S014.

Reserva ligada à intenção
Dê à reserva identidade própria e vincule-a à tentativa. Cancelamento ou timeout não libera automaticamente recursos que o servidor ainda usa. Marque reserva em reconciliação, consulte o estado quando disponível e aplique expiração conservadora para não admitir carga nova sobre trabalho ainda ativo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S005, V2A-S012.

Prioridade com conta separada
Separe capacidade para consultas interativas, recuperação e processamento adiável. O modelo não escolhe sua própria prioridade a partir de linguagem persuasiva; a aplicação deriva classe por política. Meça rejeição e tempo de espera por classe, pois uma média boa pode ocultar bloqueio prolongado de uma delas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S003.

USO AVANÇADO — Servidor local compartilhado
Cenário: Vários agentes usam a mesma GPU com modelos 3–30B.
Estratégia: Estime demanda por contexto e saída antes de admitir; reserve margem para verificação e limite sessões simultâneas. Quando faltar memória prevista, mantenha a tarefa em fila ou reduza escopo permitido, sem depender apenas da exceção de falta de memória.
Papel do modelo pequeno: Modelos pequenos processam tarefas admitidas; o limitador é determinístico.
Aceite proposto: Proposta: medir tarefas aceitas, espera, OOM e consumo efetivo, com mistura fixa de contextos curtos e longos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S009.

USO AVANÇADO — Proteção do serviço de ferramentas
Cenário: O modelo pode gerar muitas consultas corretas ao mesmo endpoint.
Estratégia: Atribua quota por serviço e operação lógica; cache ou coalescência reduzem duplicatas antes da admissão. Retry consome uma conta explícita, evitando competir ilimitadamente com primeiras tentativas.
Papel do modelo pequeno: 3–7B produz pedidos estruturados, sem decidir limites ou liberar saldo.
Aceite proposto: Proposta: introduzir rajadas e falhas transitórias; aceitar somente política que mantenha pressão limitada e rastreie saldo sem vazamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificar custo aproximado de tarefas curtas, com valores finais calculados pelo runtime.
8–14B: Proposta: montar pedidos de ferramentas com estimativas de saída e estratégia de paginação.
15–30B: Proposta: planejar lotes maiores sob cotas explicitamente fornecidas pelo controlador.
Requisitos de treino/runtime: São necessários medidores do servidor e tratamento de reservas órfãs; parâmetros não determinam sozinho memória consumida.
Não aplicar quando: Não usar estimativa de tokens como único limite quando o gargalo real é conexão, CPU, banco ou concorrência.

## T137:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: Quota de repetição limita tráfego de recuperação, distinta da chamada inicial.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

V4C-C023 — Google / Borg
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.
Mecanismo documentado: O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.
Correspondência com esta base: Admissão de cargas é relacionada a controle de capacidade, sem especificar o rate limiter da ficha.
Transferência proposta para modelo pequeno: Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.
Limite: O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.
Fontes: V4C-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AWS documenta quota de retries; os limites multidimensionais para LLM local são proposta, sem transplante automático de quotas corporativas.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q009.

## T137:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T137 → T167 [complements]
Como combinar: Buckets implementam uma dimensão de taxa dentro da política multidimensional.
Interface: Unidade, saldo, taxa de reposição e custo reservado.
Condição: Cada dimensão conserva contabilidade independente.
Aceite proposto: Reexecutar sequências de admissão e verificar ausência de saldo negativo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T137 → T150 [complements]
Como combinar: Coalescer consultas equivalentes evita cobrar capacidade duplicada antes do envio.
Interface: Chave de operação, participantes e reserva compartilhada.
Condição: Resultados e permissões são realmente compartilháveis.
Aceite proposto: Cancelar um participante sem devolver o saldo de todos os demais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não liberar reserva inteira com base apenas no cancelamento local.
- Reconciliar consumo observado e evitar que erro de estimativa se acumule indefinidamente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare vazão útil, cauda de latência e falhas com uma rota de fronteira sob igual política de admissão. Parâmetros menores não garantem menor custo quando a tarefa repete.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T163, T164, T167, T175

## Fontes primárias associadas

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S011 — golang/sync — singleflight implementation

[https://github.com/golang/sync/blob/master/singleflight/singleflight.go](https://github.com/golang/sync/blob/master/singleflight/singleflight.go)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro de chamadas em curso por chave; Forget permite nova chamada sem aguardar a chamada anterior.

Limite: Branch master pode mudar; semântica inspecionada não constitui cache durável ou deduplicação de efeitos entre processos.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T138 — Circuit Breaker

**Nome canônico:** Circuit Breaker  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T138  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** disjuntor de chamadas

## T138:C01 — conceito

Máquina de estados que interrompe temporariamente chamadas a uma dependência com falhas persistentes. Normalmente usa estados fechado, aberto e parcialmente aberto. Seu objetivo é limitar desperdício e permitir recuperação, sem concluir que todo erro pertence à mesma causa.

Como funciona:
- No estado fechado, observar erros e latências dentro de uma janela.
- Abrir o circuito quando o critério configurado for atingido.
- Após espera, admitir sondagens limitadas antes de restaurar o tráfego.

## T138:C02 — aplicacao

Quando usar:
- Serviço remoto degradado que recebe retries contínuos.
- Dependência cuja falha pode ocupar todos os workers.

Quando não usar:
- Erros de validação específicos do usuário que não indicam degradação do serviço.

Implementação proposta:
- Separar circuitos por destino e operação relevante.
- Definir volume mínimo de observações e limiares contra flutuação.
- Expor estado, motivo da abertura e próxima possibilidade de sondagem.

Aplicação LAI proposta:
Proposta: proteger consultas e modelos remotos da Helena para que falha externa não aprisione todo o executor.

## T138:C03 — riscos_validacao

Armadilhas:
- Misturar tenants ou operações distintas gera bloqueios desnecessários.
- Todos os clientes sondarem juntos causa nova sobrecarga na recuperação.

Métricas sugeridas:
- Tempo gasto em circuito aberto.
- Chamadas evitadas e taxa de sucesso das sondagens.

Testes propostos:
- Forçar falhas suficientes e confirmar que novas chamadas não atingem o backend.
- Recuperar a dependência e verificar reentrada gradual com concorrência limitada.

## T138:C04 — perguntas_proveniencia

Pergunta: Circuit breaker substitui timeout?
Resposta: Não. Timeout limita cada espera; o circuito controla novas tentativas após falhas.

Pergunta: Circuito aberto significa serviço definitivamente indisponível?
Resposta: Não. É uma decisão temporária baseada em observações e política.

Pergunta: Todo HTTP 4xx deve contar como indisponibilidade?
Resposta: Não. Muitos indicam erro de contrato ou autorização; a classificação deve seguir a semântica da operação e do serviço.

Pergunta: Por que 100% de falhas pode ser um sinal fraco?
Resposta: Porque pode representar uma única observação; duração da janela e tamanho da amostra mudam sua interpretação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T138:C05 — mecanismo_avancado

A chave de um circuito determina quais falhas compartilham destino operacional. Agregar todos os erros de um provedor pode interromper operações saudáveis porque apenas um recurso ou método falhou; granularidade excessiva gera amostras pequenas e estado demais. A janela de observação precisa diferenciar erro do cliente, rejeição por carga e indisponibilidade. Uma porcentagem de falhas sem volume mínimo pode oscilar violentamente em tráfego esparso.

Condição de contorno:
Circuitos não detectam bem incidentes quando as chamadas observadas não representam a operação protegida ou quando a classificação de erros está errada.

Contrato proposto:
- Entradas: Resultado da chamada, chave do circuito, instante e categoria de falha.
- Saídas: Permitir, rejeitar rapidamente ou admitir sonda, com motivo.
- Estado: Janela de resultados, transições, prazo de abertura e sondas ativas.
- Invariante: Só falhas elegíveis alimentam o critério que protege aquela dependência.

Compromissos de projeto:
- Circuitos finos isolam falhas e exigem mais dados para detectar tendência.
- Abrir cedo reduz desperdício e pode interromper um serviço que já se recuperava.

## T138:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: misturar erros de validação em uma operação e sucesso em outra no mesmo provedor; verificar que a chave e a classificação não bloqueiam indevidamente o caminho saudável.

Plano de avaliação proposto:
Comparar chave global e segmentada sob tráfego com falhas parciais. Medir requisições poupadas, bloqueios indevidos e tempo de recuperação. Ajustar janela e amostra mínima em dados de incidentes, sem adotar porcentagem universal.

Comparações:
- T165 (complements): Half-open detalha a fase de sondagem e retorno do circuito, enquanto o circuit breaker inclui todos os estados.
- T163 (complements): Backoff pode espaçar tentativas permitidas, mas não substitui a decisão de abrir o circuito.

Afirmação rastreável:
O padrão Microsoft separa bloqueio temporário de chamadas e tentativa de recuperação em estados distintos.
Suporte: direct; fontes: C-S005
Limite: Particionamento de chaves e critérios estatísticos descritos aqui são decisões de implementação propostas.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T138:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou granularidade e amostragem do circuito. A nova camada define circuitos por capacidade observável, interações com degradação e separação entre falha operacional e reprovação semântica.

Dois painéis de falha
Mantenha disponibilidade e qualidade em métricas distintas. Erros de transporte podem justificar abrir circuito; respostas incorretas precisam de avaliação por domínio e versão. Misturar ambos no mesmo contador impede saber se a rota está fora do ar ou apenas inadequada para uma classe difícil de consultas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V4C-S014.

Circuito com estado durável limitado
Persistir a decisão de bloqueio ajuda após restart, mas copiar uma janela antiga cegamente pode bloquear dependência já recuperada. Guarde tempo, versão da política e motivo; ao restaurar, reavalie a validade da observação e coordene sondas sem permitir que cada réplica faça sua própria avalanche.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3C-S028.

Recuperação sob demanda real
Uma sonda barata de saúde não representa necessariamente uma operação grande. Defina classes representativas para testar autenticação, contrato e capacidade, começando com chamadas sem efeitos. Retorno gradual deve aumentar carga apenas após resultados coerentes, com mecanismo para voltar a bloquear quando a recuperação não sustenta tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3D-S017.

USO AVANÇADO — Ferramenta parcialmente indisponível
Cenário: Busca funciona, mas escrita no mesmo serviço falha.
Estratégia: Abra circuito apenas para a operação afetada, conservando consultas elegíveis. Marque ações pendentes e escolha se o fluxo pode produzir uma preparação útil sem afirmar que a escrita ocorreu.
Papel do modelo pequeno: 3–14B adapta a apresentação ao estado fornecido; não decide abrir ou fechar o circuito.
Aceite proposto: Proposta: falhar somente escrita e conferir que leituras continuam e nenhum efeito é declarado concluído sem recibo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, C-S026.

USO AVANÇADO — Endpoint de inferência oscilante
Cenário: Uma revisão de servidor produz timeouts em contextos longos.
Estratégia: Segmente telemetria por revisão e classe de entrada; reduza tráfego da combinação problemática e preserve o caminho estável. Antes de reabilitar, execute sondas representativas sem alterar a identidade de tarefas pendentes.
Papel do modelo pequeno: 15–30B pode servir como rota alternativa apenas para requisitos comprovadamente compatíveis.
Aceite proposto: Proposta: medir oscilações, tarefas preservadas e carga de sondagem, incluindo restart simultâneo de controladores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: respostas de contingência e extração local durante bloqueio de dependências externas.
8–14B: Proposta: continuar ramos independentes e preparar ações pendentes para confirmação posterior.
15–30B: Proposta: substituir algumas inferências rejeitadas, respeitando capacidade e contexto do endpoint local.
Requisitos de treino/runtime: O estado do circuito pertence ao runtime; são necessários relógios, contadores e propagação da decisão entre réplicas.
Não aplicar quando: Não abrir circuito global por poucas respostas difíceis ou por erros permanentes dos argumentos do usuário.

## T138:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes fundamentam proteção e sondagem. Casos de quota de retry não foram apresentados como prova de circuit breaker implantado.
Consultas registradas: V4C-Q001, V4C-Q004.

## T138:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T138 → T165 [complements]
Como combinar: O retorno controlado usa sondas e admissão gradual quando a política inclui estado half-open.
Interface: Época do circuito, quota de sondas e resultado classificado.
Condição: Existe observação capaz de representar a dependência.
Aceite proposto: Testar competição entre réplicas e impedir fechamento por resposta de época antiga.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T138 → T175 [feeds]
Como combinar: O circuito informa indisponibilidade operacional ao seletor de alternativas.
Interface: Rota bloqueada, causa, escopo e próxima reavaliação.
Condição: Fallback possui capacidade independente e requisitos preservados.
Aceite proposto: Forçar falha comum a todas as rotas e exigir encerramento, não circulação infinita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Rejeitar respostas tardias que tentem fechar uma época já substituída.
- Não reutilizar sondas com efeitos de negócio irreversíveis.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare proteção operacional e conclusão correta usando servidores locais e de fronteira sujeitos às mesmas falhas. Circuit breaker não eleva competência cognitiva do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T163, T165

## Fontes primárias associadas

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V3D-S017 — Kubernetes — Liveness, readiness and startup probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Liveness e readiness produzem efeitos diferentes de reinício e elegibilidade para receber tráfego.

Limite: Não oferece por si só comprovação de progresso semântico de uma tarefa de agente.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T139 — Parallel Tool Calls

**Nome canônico:** Parallel Tool Calls  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T139  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** chamadas concorrentes de ferramentas

## T139:C01 — conceito

Execução concorrente de chamadas de ferramentas cujas entradas e efeitos não dependem umas das outras. A concorrência pode reduzir tempo total, mas o ganho depende de capacidade disponível, filas e duração das operações. A proposta de chamadas pela LLM não garante que o runtime as execute em paralelo.

Como funciona:
- Construir dependências entre chamadas antes de despachá-las.
- Executar conjunto independente com concorrência limitada.
- Reunir resultados associados aos identificadores originais, preservando falhas individuais.

## T139:C02 — aplicacao

Quando usar:
- Consultas independentes a fontes distintas.
- Leitura de vários arquivos para uma análise conjunta.

Quando não usar:
- Uma escrita precisa do resultado de outra ou duas operações disputam o mesmo estado mutável.

Implementação proposta:
- Usar task group ou mecanismo equivalente com timeout por chamada e global.
- Aplicar semáforo e quotas do backend.
- Escolher política de resultado parcial ou cancelamento do grupo antes da execução.

Aplicação LAI proposta:
Proposta: paralelizar leituras independentes da Helena, mantendo mutações e dependências em ordem explícita.

## T139:C03 — riscos_validacao

Armadilhas:
- Concorrência ilimitada esgota conexões e viola quotas.
- Confundir ordem de chegada com identidade mistura respostas de ferramentas.

Métricas sugeridas:
- Latência total comparada à execução sequencial.
- Pico de concorrência, taxa de erro e utilização do destino.

Testes propostos:
- Variar artificialmente a duração das chamadas e conferir associação correta de resultados.
- Fazer uma chamada falhar e verificar a política declarada para as restantes.

## T139:C04 — perguntas_proveniencia

Pergunta: Duas chamadas paralelas tornam a LLM paralela?
Resposta: Não. O paralelismo pertence ao runtime e às ferramentas.

Pergunta: O tempo final será o da mais lenta?
Resposta: Só como aproximação sem filas, limites ou overhead relevante.

Pergunta: Cancelar o grupo garante ausência de efeitos?
Resposta: Não. O cancelamento pode chegar depois da conclusão; cada operação precisa de confirmação ou reconciliação própria.

Pergunta: Como preservar ordem sem serializar chamadas?
Resposta: Atribuir índice ou ID estável às entradas e ordenar os resultados por essa identidade após a coleta.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T139:C05 — mecanismo_avancado

Concorrência exige escolher a política de erro do grupo. Em execução fail-fast, um erro sinaliza cancelamento dos irmãos; em coleta completa, todos os resultados são aguardados e classificados. O cancelamento costuma ser cooperativo: uma ferramenta pode ter concluído o efeito antes de observar o sinal. Por isso, o agregador deve acompanhar estados individuais em vez de inferir que todas as chamadas falharam junto com a primeira.

Condição de contorno:
O ganho desaparece quando as ferramentas competem pelo mesmo recurso ou quando a segunda chamada depende de um valor produzido pela primeira.

Contrato proposto:
- Entradas: Chamadas independentes, limites de concorrência e política de resultado parcial.
- Saídas: Resultado por chamada, ordem lógica e status de cancelamento confirmado ou pendente.
- Estado: IDs das chamadas, tarefas ativas, erros e deadline compartilhado.
- Invariante: A posição do resultado corresponde ao ID da chamada, não à ordem de chegada.

Compromissos de projeto:
- Fail-fast pode economizar trabalho; coleta completa preserva evidências úteis mesmo com falhas parciais.
- Limitar concorrência reduz pressão e pode aumentar tempo de um lote pequeno.

## T139:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: combinar uma chamada rápida com erro, uma lenta cancelável e uma escrita que conclui antes do cancelamento; exigir três desfechos distintos e reconciliação da escrita.

Plano de avaliação proposto:
Comparar sequência, paralelismo ilimitado e grupo limitado com latências heterogêneas. Controlar capacidade das ferramentas. Medir tempo do lote, carga máxima, efeitos redundantes e completude do resultado; escolher a política conforme dependência real de todos os ramos.

Comparações:
- T147 (complements): Fan-out define distribuição e junção; chamadas paralelas concretizam o trabalho dos ramos.

Afirmação rastreável:
errgroup associa propagação de erros, cancelamento por contexto e limite de tarefas ativas.
Suporte: direct; fontes: V3C-S007
Limite: A API não torna efeitos remotos reversíveis nem obriga funções a respeitarem imediatamente o cancelamento.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T139:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu cancelamento e políticas de erro do grupo. O aprofundamento acrescenta análise de efeitos, fan-out especulativo limitado e comparação consistente de resultados obtidos em momentos diferentes.

Independência por recurso
Construa uma matriz de leitura e escrita dos recursos envolvidos. Duas ferramentas com nomes distintos podem alterar o mesmo objeto; duas leituras podem produzir resultados incompatíveis se observarem versões diferentes. Paralelismo exige declarar tanto dependências de dados quanto a consistência necessária à junção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V4C-S015.

Especulação recuperável
Quando a próxima rota é incerta, uma busca barata pode começar enquanto outra classificação termina. Isso só compensa se o trabalho especulativo for cancelável, sem efeitos, e a latência economizada superar o custo de resultados descartados. Mantenha a especulação em orçamento separado para que ela não ocupe a capacidade das chamadas obrigatórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S007, V3C-S005.

Junção com proveniência temporal
Cada resultado precisa trazer fonte, versão ou instante de observação e estado de conclusão. O agregador não deve escolher o mais rápido como se fosse o mais atual. Quando a decisão exige uma visão consistente, revalide os campos críticos após reunir as respostas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S007, V3A-S030.

USO AVANÇADO — Pesquisa técnica por evidências independentes
Cenário: Uma pergunta exige contrato, código e relato operacional.
Estratégia: Dispare buscas em fontes distintas com objetivos delimitados; deduplique documentos e compare divergências. Se uma fonte falhar, preserve a lacuna e evite preencher seu papel com repetição das demais.
Papel do modelo pequeno: 3–7B extrai fatos por fonte; 8–30B confronta evidências sem transformar repetição em consenso.
Aceite proposto: Proposta: medir cobertura, duplicação de fontes e latência, mantendo o mesmo orçamento total da execução serial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

USO AVANÇADO — Diagnóstico de falha em aplicação
Cenário: Logs, métricas e revisão de código podem ser consultados simultaneamente.
Estratégia: Leia cada superfície com um intervalo e revisão declarados; combine por identificadores de execução. Só depois escolha uma mutação. Se os dados pertencem a instantes incompatíveis, faça uma leitura focada antes de propor reparo.
Papel do modelo pequeno: 8–14B organiza hipóteses; 15–30B integra relações entre subsistemas.
Aceite proposto: Proposta: aceitar diagnóstico apenas quando cada hipótese decisiva aponta para evidência identificável e temporalmente compatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: workers de extração com uma ferramenta ou domínio por vez, retornando campos curtos.
8–14B: Proposta: selecionar e combinar poucas consultas independentes sob limite explícito de concorrência.
15–30B: Proposta: coordenar investigação mais ampla, reservando a junção e verificação como etapas obrigatórias.
Requisitos de treino/runtime: O servidor precisa suportar concorrência real; definir limites por endpoint, timeout e semântica de cancelamento.
Não aplicar quando: Não paralelizar mutações concorrentes no mesmo recurso nem consultas cujo segundo argumento depende do primeiro resultado.

## T139:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O relato identifica chamadas paralelas de ferramentas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research comprova uso de ferramentas paralelas; outros sistemas fornecem princípios de consistência. Transferência de porte permanece proposta. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q003, V4C-Q010, V4D-Q018.

## T139:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T139 → T147 [complements]
Como combinar: O fan-out define participantes e condição de junção das chamadas paralelas.
Interface: Lista fechada de tarefas e resultados com status individual.
Condição: O produtor sinaliza que terminou de criar participantes.
Aceite proposto: Injetar falha em um ramo e verificar completude segundo a política escolhida.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T139 → T137 [complements]
Como combinar: Chamadas concorrentes precisam passar pela admissão para não transformar latência menor em sobrecarga.
Interface: Reserva por tentativa, destino e custo estimado.
Condição: O orçamento considera chamadas especulativas e retries.
Aceite proposto: Comparar pico de carga e tarefas aceitas contra execução serial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009, V3C-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar cancelamento do grupo como desfazimento dos efeitos já realizados.
- Descartar resultados sem identidade suficiente para ligá-los à subtarefa correta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelo pequeno com chamadas paralelas e modelo de fronteira serial ou paralelo sob custo igual. Ganho de latência da infraestrutura não prova ganho de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T147, T160, T162

## Fontes primárias associadas

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T140 — Tool Use / Function Calling

**Nome canônico:** Tool Use / Function Calling  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T140  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** uso de ferramentas; chamada de função

## T140:C01 — conceito

Mecanismo pelo qual o modelo propõe uma ferramenta e argumentos estruturados, e o runtime decide como validar e executar essa proposta. A chamada expõe uma interface de ação; a LLM não recebe automaticamente autoridade, credenciais ou garantia de que a execução ocorreu.

Como funciona:
- Disponibilizar nomes, descrições e schemas de ferramentas permitidas.
- Validar nome, argumentos, identidade e precondições antes da execução.
- Devolver resultado estruturado associado à chamada e registrar seu efeito.

## T140:C02 — aplicacao

Quando usar:
- Consulta a estado externo ou execução de cálculo confiável.
- Ações que exigem integração com sistemas da empresa.

Quando não usar:
- Encaminhar texto arbitrário do modelo diretamente a shell ou SQL sem contrato e controles adequados.

Implementação proposta:
- Projetar operações pequenas com entradas explícitas e erros tipados.
- Separar ferramentas de leitura e mutação com política no backend.
- Adotar timeout, idempotência quando aplicável e recibo verificável.

Aplicação LAI proposta:
Proposta: cada integração da Helena expor contratos claros, com recibos que possam ser recuperados pelo RAG como evidência.

## T140:C03 — riscos_validacao

Armadilhas:
- Schema válido não impede argumento semanticamente errado.
- Mensagem produzida pelo modelo dizendo feito não comprova efeito na ferramenta.

Métricas sugeridas:
- Taxa de seleção correta e argumentos válidos.
- Resultado de negócio confirmado por execução, não pela narrativa.

Testes propostos:
- Enviar ferramenta inexistente e argumento fora do domínio; ambos devem ser recusados.
- Simular erro de execução e exigir que a resposta final não declare sucesso.

## T140:C04 — perguntas_proveniencia

Pergunta: A função é executada pelo modelo?
Resposta: O modelo emite a proposta; o runtime ou serviço executa.

Pergunta: JSON válido prova que a ação foi correta?
Resposta: Não. É preciso validar semântica e conferir o efeito.

Pergunta: Um isError falso equivale a objetivo cumprido?
Resposta: Não necessariamente. É um sinal do contrato da ferramenta; o domínio pode exigir verificar recibo, estado ou pós-condição.

Pergunta: Por que registrar a revisão usada?
Resposta: Porque o mesmo nome pode aceitar outros argumentos ou interpretar valores de maneira diferente após evolução do serviço.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T140:C05 — mecanismo_avancado

Uma chamada possui pelo menos três camadas de resultado: transporte ou protocolo, execução da ferramenta e efeito de domínio. Um envelope recebido corretamente pode carregar erro operacional, enquanto uma resposta perdida pode esconder um efeito bem-sucedido. Na revisão MCP analisada, o contrato de entrada e a saída estruturada são descritos separadamente; a existência de outputSchema torna possível verificar uma dimensão que simples texto não resolve.

Condição de contorno:
Validar argumentos não confirma disponibilidade atual do alvo nem a conclusão do efeito solicitado.

Contrato proposto:
- Entradas: Identificador da ferramenta, revisão de contrato, argumentos e contexto de execução.
- Saídas: Conteúdo, resultado estruturado quando previsto, erro operacional e referência ao recibo.
- Estado: Correlação entre chamada, tentativa, versão da ferramenta e resultado recebido.
- Invariante: A mensagem que propõe a chamada não é registrada como prova de execução.

Compromissos de projeto:
- Contratos mais estritos facilitam consumo automático e exigem migração quando o domínio evolui.
- Separar falha de protocolo e falha de negócio aumenta precisão e amplia o número de estados tratados.

## T140:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: enviar argumentos inválidos, receber erro de domínio em um envelope válido e perder uma resposta após confirmação remota; o executor deve distingui-los sem retry genérico.

Plano de avaliação proposto:
Comparar integração somente textual e integração estruturada em operações rotuladas. Fixar revisão do protocolo e schemas. Medir classificação de erros, argumentos rejeitados corretamente e efeitos confirmados; aceitar a integração quando estados ambíguos permanecerem rastreáveis.

Comparações:
- T141 (complements): Uma saída estruturada descreve o resultado, mas não executa a ferramenta.
- T243 (complements): Reconciliação resolve efeitos incertos após falhas de comunicação.

Afirmação rastreável:
MCP 2025-11-25 especifica inputSchema, outputSchema opcional e resultados estruturados de ferramentas.
Suporte: direct; fontes: V3C-S004
Limite: A revisão foi consultada como contrato identificado, sem pressupor ser a mais recente ou estar instalada.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T140:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou transporte, execução e efeito. A nova estratégia introduz fronteira de responsabilidade entre LLM e ferramenta, contratos de intenção e descoberta progressiva de capacidades reais.

Decomposição pela verificabilidade
Entregue ao modelo escolhas semânticas que precisam de interpretação e mantenha transformações precisas em código. Em edição, decidir onde simplificar pode exigir contexto, enquanto simplificar uma expressão booleana pode ser função determinística. Essa divisão reduz a quantidade de comportamento que depende de instruções longas ou de raciocínio textual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

Definição não é disponibilidade
A ferramenta descoberta precisa estar habilitada, com schema e destino resolvidos na revisão usada. Um catálogo pode conter definições ainda não expostas. A aplicação deve distinguir conhecer a operação, poder invocá-la e ter recebido confirmação do seu efeito, devolvendo cada estado ao agente de modo explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Envelope mínimo de execução
Associe argumentos ao objetivo, alvo e base esperada antes do envio. Campos de controle, credenciais e identidades são preenchidos pelo runtime, não inventados pela LLM. O resultado volta com dados necessários à próxima decisão e referência ao artefato completo quando houver detalhes extensos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V4C-S013.

USO AVANÇADO — Refatoração com cálculo determinístico
Cenário: Modelo precisa remover ramificações associadas a uma flag obsoleta.
Estratégia: Deixe o modelo localizar os fluxos e propor o escopo; uma ferramenta transforma a estrutura e produz diff. Compile e teste antes de solicitar revisão. Se a decisão sobre a flag estiver incerta, não trate transformação correta como autorização para removê-la.
Papel do modelo pequeno: 8–14B identifica locais; 15–30B acompanha propagação entre funções.
Aceite proposto: Proposta: medir preservação de comportamento, alterações indevidas e esforço de revisão, com flags fora dos exemplos do prompt.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

USO AVANÇADO — Consulta corporativa com payload grande
Cenário: Uma API devolve centenas de campos, mas a tarefa usa poucos.
Estratégia: Descubra o schema, selecione campos necessários e execute projeção no gateway. Guarde referência ao resultado integral quando permitido. Se o verificador precisar de campo omitido, faça nova leitura específica em vez de inferir seu valor.
Papel do modelo pequeno: 3–7B escolhe campos em schema pequeno e produz resposta com referências.
Aceite proposto: Proposta: comparar tokens, campos recuperados e erros por omissão contra resposta integral, mantendo mesmas perguntas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: uma ferramenta de cada vez, enumerações curtas e validação externa dos argumentos.
8–14B: Proposta: cadeias curtas com resultados tipados e reparo delimitado de contratos.
15–30B: Proposta: coordenação entre ferramentas, mantendo identidades e mutações controladas pelo runtime.
Requisitos de treino/runtime: Pode exigir treino de formato ou exemplos do protocolo; suporte nominal a JSON não demonstra seleção correta de ferramenta.
Não aplicar quando: Não usar agente para substituir cálculo exato disponível ou para inventar campos que o serviço não retornou.

## T140:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: PolyglotPiranha é exposto ao agente por MCP.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: O gateway traduz e executa chamadas MCP para serviços.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: Tool calling integra o framework descrito.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: Há integração documentada de tool calling com parser específico.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

V4D-C004 — Google / Chrome built-in AI / Summarizer API
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação lista a Summarizer API no Chrome estável desde a versão 138.
Mecanismo documentado: Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.
Correspondência com esta base: API de aplicação não equivale a function calling aprendido pelo modelo.
Transferência proposta para modelo pequeno: Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.
Limite: Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.
Fontes: V4D-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean e MCP Gateway comprovam combinações específicas. Não se contam cada ferramenta ou cada estágio desses sistemas como novos deployments. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q006, V4C-Q009, V4D-Q018.

## T140:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T140 → T232 [feeds]
Como combinar: No AutoClean, o agente invoca PolyglotPiranha por MCP para transformações estruturais.
Interface: Chamada de ferramenta e código alvo; a integração local define versão e recibo adicionais.
Condição: A transformação determinística cobre o padrão desejado.
Aceite proposto: Proposta: comparar estrutura e comportamento antes e depois, vinculando os testes ao diff.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T140 → T158 [complements]
Como combinar: O executor resolve ferramenta habilitada e contrato antes de aceitar uma invocação descoberta.
Interface: ID de ferramenta, schema, revisão e estado de habilitação.
Condição: O registro é a autoridade operacional da integração.
Aceite proposto: Alterar schema entre descoberta e execução e exigir revalidação.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

CONTROLES DE FALHA
- Tratar saída textual da ferramenta como dado, sem elevar instruções embutidas a controle do agente.
- Preservar intenção em retries e separar erro de contrato de resultado remoto desconhecido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare 3–30B com fronteira em tarefas cujo cálculo está nas ferramentas. A combinação pode melhorar execução delimitada sem demonstrar equivalência em escolha aberta de objetivos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T141, T158, T170, T197

## Fontes primárias associadas

### C-S007 — Tools — Model Context Protocol, 2025-06-18

[https://modelcontextprotocol.io/specification/2025-06-18/server/tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ferramentas expõem nome, schema, descoberta e chamada por contrato; protocolo não concede autorização de negócio.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S007 — Built-in AI APIs

[https://developer.chrome.com/docs/ai/built-in-apis](https://developer.chrome.com/docs/ai/built-in-apis)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade e estágio das APIs locais do Chrome; Summarizer documentado como estável desde Chrome 138.

Limite: Tabela é mutável e partes textuais podem acompanhar versões em ritmos diferentes. API disponível não comprova uso por cliente; não identifica porte exato do checkpoint.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T141 — Structured Outputs

**Nome canônico:** Structured Outputs  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T141  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** saídas estruturadas

## T141:C01 — conceito

Saídas sujeitas a contrato de estrutura, como objetos JSON com campos e tipos definidos. Podem ser obtidas por decodificação restrita ou por validação com correção. Garantia estrutural não significa veracidade: um objeto perfeito pode conter fatos, identificadores ou decisões incorretos.

Como funciona:
- Definir representação da resposta e distinguir campos obrigatórios de opcionais.
- Gerar conteúdo com mecanismo compatível com as restrições necessárias.
- Validar estrutura e depois regras de domínio antes de consumir a saída.

## T141:C02 — aplicacao

Quando usar:
- Integrações entre agentes e APIs.
- Extração de entidades ou decisões que alimentam um workflow.

Quando não usar:
- Quando o schema elimina informação necessária ou força certeza onde deveria existir desconhecido.

Implementação proposta:
- Permitir valores nulos ou estados de insuficiência de evidência quando apropriado.
- Fixar versão do schema e testar o subconjunto suportado pelo backend.
- Validar referências e intervalos após o parsing.

Aplicação LAI proposta:
Proposta: padronizar respostas de especialistas da Helena com conclusão, evidências, incerteza e próximos passos.

## T141:C03 — riscos_validacao

Armadilhas:
- JSON mode pode garantir apenas JSON sintaticamente válido.
- Limite de saída ou interrupção pode produzir objeto incompleto.

Métricas sugeridas:
- Validade sintática, conformidade ao schema e correção semântica separadamente.
- Número de reparos e tokens consumidos por objeto aceito.

Testes propostos:
- Usar campos ausentes, enums desconhecidos e números extremos como casos negativos.
- Fornecer pergunta sem resposta nos documentos e exigir representação explícita da lacuna.

## T141:C04 — perguntas_proveniencia

Pergunta: Structured output acaba com alucinação?
Resposta: Não. Restringe formato; a factualidade ainda exige fontes e verificação.

Pergunta: Todo JSON é structured output garantido?
Resposta: Não. O contrato e o mecanismo de validação precisam ser especificados.

Pergunta: Campo opcional e campo nullable são iguais?
Resposta: Não. Opcional permite ausência; nullable admite null como valor quando o campo está presente, conforme o schema.

Pergunta: Por que um schema válido pode falhar no gerador?
Resposta: Porque validade do schema e suporte do decodificador são propriedades diferentes; o backend pode aceitar um subconjunto.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T141:C05 — mecanismo_avancado

Definir properties em JSON Schema não torna os campos obrigatórios: required estabelece presença. Também é diferente aceitar null e permitir ausência. Ao compor schemas, additionalProperties considera propriedades reconhecidas no seu escopo; extensões com allOf podem surpreender quem presume união informal dos campos. Versões mais recentes oferecem unevaluatedProperties para controlar o que já foi avaliado, mas um decodificador pode suportar somente parte desse vocabulário.

Condição de contorno:
A garantia estrutural depende do dialeto, do validador e do subconjunto efetivamente aceito pelo mecanismo de geração.

Contrato proposto:
- Entradas: Schema identificado, dialeto, política de campos extras e estado esperado da resposta.
- Saídas: Documento validado ou diagnóstico por campo, incluindo término incompleto.
- Estado: Versão compilada do schema, capacidades do backend e registros de validação.
- Invariante: Ausência, null, recusa e truncamento são estados distintos no contrato.

Compromissos de projeto:
- Fechar objetos facilita detectar erros de digitação e dificulta evolução aditiva de campos.
- Validação posterior cobre vocabulário adicional, mas não impede que a geração gaste tokens em uma saída rejeitada.

## T141:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar objeto sem campo requerido, objeto com null, campo extra e extensão via allOf; conferir resultado no validador e comportamento do backend separadamente.

Plano de avaliação proposto:
Comparar geração livre validada e decodificação restrita usando o mesmo schema e modelo. Medir conformidade inicial, tentativas de correção, truncamento e correção de domínio. Aprovar o contrato somente com matriz explícita de recursos suportados.

Comparações:
- T196 (complements): Decodificação restrita pode evitar algumas violações durante a geração.
- T197 (complements): Validação completa do documento ocorre com um validador do dialeto definido.

Afirmação rastreável:
A documentação JSON Schema diferencia definição de propriedades, obrigatoriedade e controle de propriedades adicionais.
Suporte: direct; fontes: V3C-S013
Limite: Isso não garante suporte integral do mesmo vocabulário em todos os provedores de geração.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T141:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou vocabulário de JSON Schema e limites de decodificadores. A nova camada distingue proposta gerada, objeto validado e recibo de execução, impedindo que a mesma estrutura atribua autoridade a dados não verificados.

Schemas por fronteira
Use um schema pequeno para a proposta do modelo e outro para o registro persistido. O segundo inclui campos calculados pela aplicação, como identidade, revisão e status da validação. Aceitar JSON válido do modelo não lhe dá o direito de preencher esses campos como se a execução já tivesse acontecido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S013, V4C-S013.

Campos incertos representáveis
Modele ausência de evidência explicitamente, com motivo e referência ao trecho disponível. Obrigar todo campo a conter uma string incentiva preenchimento inventado. Uma união controlada entre encontrado, ausente e ambíguo permite ao consumidor distinguir falta de dado de falha de geração sem interpretar texto livre.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S013.

Semântica cruzada fora do parser
Depois de validar tipos, verifique relações entre campos: datas ordenadas, IDs pertencentes ao mesmo recurso, unidades e consistência entre total e parcelas. Essas regras não devem depender de uma segunda frase de autoconfiança. Registre qual versão da regra aceitou o objeto para reavaliá-lo quando o contrato mudar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S010.

USO AVANÇADO — Extração de configuração técnica
Cenário: Manuais descrevem parâmetros com versões e exceções.
Estratégia: Peça valor, unidade, condição e fonte, permitindo ambiguidade. O runtime resolve referências e testa relações relevantes. Se houver conflito entre versões, produza candidatos separados e deixe a seleção depender da versão efetivamente utilizada.
Papel do modelo pequeno: 3–7B pode extrair campos em contexto curto; 8–14B distingue exceções locais.
Aceite proposto: Proposta: medir campos sustentados por fonte, conflitos detectados e objetos estruturalmente válidos porém incorretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S013.

USO AVANÇADO — Plano de manutenção executável
Cenário: Uma tarefa precisa virar etapas de ferramentas.
Estratégia: Gere operações de um catálogo fechado com dependências e pré-condições. Converta a proposta em comandos apenas após validar recursos e ordem. Resultados confirmados entram num schema distinto, evitando que o modelo marque suas próprias etapas como concluídas.
Papel do modelo pequeno: 15–30B produz plano limitado; código verifica referências e estados.
Aceite proposto: Proposta: rejeitar ciclos, alvos inexistentes e confirmações sem recibo, comparando com planejamento livre em texto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: objetos curtos, enums pequenos e estados de ausência explícitos, com recuperação local de valores.
8–14B: Proposta: extrações com relações simples entre campos, verificadas posteriormente por regras.
15–30B: Proposta: planos estruturados mais extensos, ainda sem autoridade para criar IDs ou estados confirmados.
Requisitos de treino/runtime: Conferir dialeto aceito pelo servidor e tratar truncamento; treino de formato não substitui avaliação factual.
Não aplicar quando: Não usar quando o schema força falsa precisão ou quando a aplicação não consegue tratar ausência e conflito.

## T141:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: Tipos gerados são restringidos por geração guiada.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: A pesquisa Google teve bloqueio de abertura; a ficha se apoia em JSON Schema e gateway aberto, sem inventar caso de uso Google em produção.
Consultas registradas: V4C-Q009, V4C-Q013.

## T141:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T141 → T140 [feeds]
Como combinar: A proposta estruturada alimenta argumentos somente depois da validação.
Interface: Objeto candidato, versão de schema e erros por campo.
Condição: Campos de identidade operacional vêm de fontes confiáveis.
Aceite proposto: Forçar ID plausível inexistente e exigir rejeição anterior à execução.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T141 → T170 [complements]
Como combinar: Mudanças de schema precisam preservar significado nos produtores e consumidores.
Interface: Versão de contrato e conversor explicitamente identificado.
Condição: Migração não elimina estados de incerteza.
Aceite proposto: Reprocessar exemplos antigos e conferir que campos ausentes não viram fatos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013, V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Recusar mensagem truncada antes de interpretá-la como objeto completo.
- Separar falha de parsing, de schema e de regra de domínio nas métricas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos pequenos e fronteira na extração sustentada, não apenas na taxa de JSON válido. Formato controlado pode equalizar sintaxe sem equalizar compreensão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T196, T197

## Fontes primárias associadas

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T142 — Agent Frameworks com Planning

**Nome canônico:** Agent Frameworks com Planning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T142  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** frameworks de agentes com planejamento

## T142:C01 — conceito

Família de frameworks que coordena estado, ferramentas e planejamento de agentes. O plano pode ser produzido pela LLM ou por código, enquanto o framework executa transições. Adotar uma biblioteca não garante qualidade do plano, recuperação após falhas nem respeito às regras da aplicação.

Como funciona:
- Representar estado da missão e etapas de execução.
- Converter decisões de planejamento em transições observáveis.
- Executar nós, persistir resultados e decidir término ou replanejamento.

## T142:C02 — aplicacao

Quando usar:
- Missões com várias etapas e ferramentas.
- Necessidade de inspeção, retomada e controle de fluxo explícito.

Quando não usar:
- Fluxo simples e fixo em que um serviço convencional resolve com menor complexidade.

Implementação proposta:
- Escolher framework pela necessidade de estado e replay, não pelo número de abstrações.
- Separar planejador, executor e verificador por contratos.
- Definir critérios de término e testes para transições ilegais.

Aplicação LAI proposta:
Proposta: comparar o runtime atual da Helena com uma implementação mínima de grafo antes de decidir incorporar outro framework.

## T142:C03 — riscos_validacao

Armadilhas:
- Plano bonito sem precondições gera ações inexequíveis.
- Estado apenas em memória desaparece quando o processo cai.

Métricas sugeridas:
- Conclusão correta por missão e número de replanejamentos.
- Esforço de operação, replay e diagnóstico de falhas.

Testes propostos:
- Interromper missão entre duas etapas e conferir retomada sem repetir efeitos.
- Apresentar plano com dependência ausente e exigir rejeição antes da execução.

## T142:C04 — perguntas_proveniencia

Pergunta: Framework com planning pensa melhor sozinho?
Resposta: Não. Ele organiza execução; a qualidade depende de modelos, ferramentas e validação.

Pergunta: LangGraph impõe um planejador?
Resposta: Não. Seu runtime permite definir arquitetura e controle de fluxo.

Pergunta: Um reducer que concatena listas é idempotente?
Resposta: Em geral, não: aplicar duas vezes a mesma atualização duplica elementos, salvo deduplicação por identidade.

Pergunta: Compilação do grafo prova que o plano resolve a tarefa?
Resposta: Não. Ela verifica aspectos estruturais do grafo, enquanto viabilidade e suficiência do plano exigem critérios da tarefa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T142:C05 — mecanismo_avancado

Em um runtime de grafos, a composição do estado é tão importante quanto o plano. Nós paralelos podem produzir atualizações para a mesma chave; sem regra de combinação, ocorre conflito ou sobrescrita conforme o runtime. Reducers com concatenação também podem duplicar resultados quando há reexecução. Definir identidade dos itens e semântica de merge permite distinguir repetir processamento de registrar nova evidência.

Condição de contorno:
Um grafo que compila corretamente ainda pode conter ciclos sem progresso, dependências semânticas omitidas ou reducers inadequados.

Contrato proposto:
- Entradas: Estado tipado, nós, transições, políticas de merge e plano corrente.
- Saídas: Atualizações do estado, tarefas prontas e motivo de término ou interrupção.
- Estado: Versões do grafo, checkpoint, reducers e itens já confirmados.
- Invariante: Atualizações concorrentes preservam identidade e não descartam silenciosamente resultados de outro nó.

Compromissos de projeto:
- Estado compartilhado simplifica coordenação e torna conflitos mais frequentes.
- Subgrafos isolados reduzem acoplamento, exigindo contratos explícitos na junção.

## T142:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois nós escrevem na mesma lista e um é reexecutado após falha; verificar que a política escolhida não perde nem duplica resultados lógicos.

Plano de avaliação proposto:
Comparar fluxo simples e grafo com paralelismo na mesma tarefa. Fixar modelos e ferramentas. Medir repetição de nós, coerência do estado, tempo e conclusão por objetivo. Escolher a abstração quando sua vantagem compensar custo de estado e depuração.

Comparações:
- R008 (distinct_from): LangGraph é um runtime concreto; a família de frameworks com planejamento inclui decisões que o aplicativo ainda precisa definir.
- T208 (complements): Planner–Executor define responsabilidades que podem ser representadas em nós separados.

Afirmação rastreável:
LangGraph define canais de estado e reducers para combinar atualizações dos nós.
Suporte: direct; fontes: V3C-S006
Limite: As regras exatas dependem da versão; requisitos de deduplicação do domínio não são fornecidos automaticamente.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T142:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou estado e reducers. A nova camada trata o framework como interpretador de uma linguagem operacional restrita, com separação entre plano proposto, validação e comandos efetivamente executados.

Representação intermediária
Defina um conjunto pequeno de operações, condições e dependências que o agente pode propor. Compile esse plano para o runtime somente após checar referências e caminhos de término. Isso reduz o espaço de ações de um modelo pequeno e permite rejeitar planos inválidos sem executar ferramentas para descobrir o erro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S006.

Estado de controle separado
Mensagens do modelo não devem ser a única fonte de status. Mantenha no controlador etapas elegíveis, leases, resultados e prazos; o texto contém interpretação e evidência. Assim, uma compactação ou mudança de prompt não apaga a informação de que uma ação já foi confirmada ou continua ambígua.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V4C-S015.

Evolução por compatibilidade
Uma missão em andamento precisa conhecer a versão do plano e do interpretador. Ao atualizar ferramentas ou nós, decida se ela continua na versão anterior, migra com conversão explícita ou é interrompida. Um deploy que compila corretamente ainda pode modificar o significado de comandos de históricos existentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

USO AVANÇADO — Agente de atendimento técnico delimitado
Cenário: O processo sempre coleta diagnóstico, consulta documentos e prepara ação.
Estratégia: Modele etapas recorrentes em código e permita ao modelo selecionar perguntas e evidências dentro delas. Só abra planejamento livre quando o fluxo conhecido não cobrir a solicitação, preservando o estado e o motivo da saída.
Papel do modelo pequeno: 3–7B preenche operações locais; 8–14B escolhe caminhos entre poucas alternativas.
Aceite proposto: Proposta: comparar conclusão, passos inúteis e falhas de contrato com um loop inteiramente livre.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

USO AVANÇADO — Workflow de migração de código
Cenário: Várias bibliotecas precisam ser atualizadas com dependências.
Estratégia: Gere um plano por módulo, valide a ordem e execute em checkpoints. Quando build falhar, replaneje somente o subgrafo afetado; resultados anteriores são reutilizados apenas se suas entradas continuarem válidas.
Papel do modelo pequeno: 15–30B propõe dependências e reparos; o framework conserva execução e verificação.
Aceite proposto: Proposta: interromper, atualizar um módulo e retomar; medir trabalho reutilizado corretamente e testes invalidados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: executor de uma linguagem pequena de tarefas com esquemas curtos e respostas verificáveis.
8–14B: Proposta: planejamento de workflows de domínio conhecido, com compilação e testes do plano.
15–30B: Proposta: supervisão de subgrafos e tratamento de exceções, sem substituir o interpretador determinístico.
Requisitos de treino/runtime: Exige schemas, controle de versão e persistência do runtime; instalar uma biblioteca não produz essas políticas.
Não aplicar quando: Evitar framework complexo para uma chamada isolada ou quando o domínio não possui estados e critérios de término definidos.

## T142:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor, Cadence e Hiring Assistant sustentam princípios diferentes; não se atribui um framework específico ao operador sem identificação explícita.
Consultas registradas: V4C-Q002, V4C-Q003, V4C-Q010.

## T142:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T142 → T143 [feeds]
Como combinar: O planejador emite a representação que o framework valida e executa.
Interface: Plano versionado com entradas, dependências e resultados exigidos.
Condição: As operações pertencem ao catálogo permitido.
Aceite proposto: Gerar planos adversos e conferir rejeição antes de qualquer efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T142 → T159 [complements]
Como combinar: Persistência conserva as fronteiras confirmadas do plano ao longo de falhas.
Interface: Histórico de comandos, resultados e versão do interpretador.
Condição: Operações externas são separadas da reconstrução.
Aceite proposto: Retomar uma missão interrompida e comparar efeitos com a execução sem falha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não deixar o modelo sobrescrever estados confirmados por texto de planejamento.
- Exigir migração explícita quando nomes de etapas ou significado de argumentos mudarem.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare framework restrito com modelo de fronteira usando o mesmo catálogo e verificadores. Uma arquitetura melhor pode reduzir erros de execução sem ampliar conhecimento geral do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T159, T160, R008

## Fontes primárias associadas

### C-S009 — LangGraph overview

[https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime de grafos com estado, controle de fluxo e integração de operações determinísticas e de LLM.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T143 — Plan-Then-Act

**Nome canônico:** Plan-Then-Act  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T143  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejar e depois agir

## T143:C01 — conceito

Padrão que explicita um plano antes de executar ações. Ajuda a decompor objetivos, verificar dependências e estabelecer critérios de aceite. O plano é uma hipótese operacional e deve mudar quando novas observações invalidarem suas premissas; não é uma sequência que deva ser cumprida cegamente.

Como funciona:
- Decompor o objetivo em etapas com entregáveis verificáveis.
- Validar precondições, dependências e permissões de cada etapa.
- Executar e replanejar somente a parte afetada por novas evidências.

## T143:C02 — aplicacao

Quando usar:
- Missões com dependências previsíveis.
- Operações que se beneficiam de revisão do plano antes de efeitos externos.

Quando não usar:
- Ambiente altamente dinâmico no qual um plano longo fica obsoleto imediatamente.

Implementação proposta:
- Usar schema para etapa, entrada, saída, responsável e condição de conclusão.
- Persistir versão do plano e vincular alterações ao evento que as motivou.
- Colocar limites de tempo, orçamento e replanejamentos.

Aplicação LAI proposta:
Proposta: planejar auditorias da Helena com artefatos e testes por etapa, mantendo espaço para descoberta durante execução.

## T143:C03 — riscos_validacao

Armadilhas:
- Detalhar demais cria aparência de precisão sem informação suficiente.
- Marcar etapa concluída pelo texto da LLM sem validar entregável.

Métricas sugeridas:
- Percentual de etapas executáveis na primeira tentativa.
- Retrabalho por premissas invalidadas e tempo até resultado aceito.

Testes propostos:
- Remover uma precondição e verificar que a etapa dependente não executa.
- Mudar um dado relevante no meio da missão e exigir revisão localizada do plano.

## T143:C04 — perguntas_proveniencia

Pergunta: Planejar elimina ReAct?
Resposta: Não. Um plano global pode conter ciclos locais de observação e ação.

Pergunta: O plano precisa expor raciocínio interno completo?
Resposta: Não. Objetivos, dependências e justificativas operacionais são suficientes.

Pergunta: Um plano pode conter chamadas ainda sem todos os argumentos?
Resposta: Sim, como dependências simbólicas explícitas; a execução aguarda valores reais antes de enviar a chamada.

Pergunta: Devo descartar todo o plano após uma surpresa?
Resposta: Não necessariamente. Invalidar o subgrafo dependente da premissa alterada pode preservar trabalho ainda correto.

Escopo das fontes:
Plan-and-Solve é uma referência relacionada de prompting; o workflow de ferramentas e persistência descrito aqui é extensão editorial.

## T143:C05 — mecanismo_avancado

Um plano útil representa dependências de informação, não apenas ordem textual. Uma etapa pode declarar que consumirá o resultado ainda desconhecido de outra, preservando um espaço reservado em vez de inventar esse valor. ReWOO explora separar planejamento e observações para evitar reprocessar toda a trajetória a cada chamada. A economia depende de quanto da estrutura pode ser antecipado; contingências reais ainda exigem revisão do plano.

Condição de contorno:
Planejamento antecipado perde precisão quando a próxima ação depende de conteúdo imprevisível ou de efeitos difíceis de reverter.

Contrato proposto:
- Entradas: Objetivo, ferramentas disponíveis, hipóteses e critérios por etapa.
- Saídas: Plano versionado, dependências simbólicas e condições para replanejar.
- Estado: Etapas confirmadas, resultados referenciados e premissas ainda não verificadas.
- Invariante: Uma variável de resultado não é substituída por valor imaginado antes da observação.

Compromissos de projeto:
- Um plano amplo reduz chamadas ao planejador e amplia o custo de corrigir premissas erradas.
- Etapas menores permitem revisão frequente e aumentam overhead de coordenação.

## T143:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma ferramenta devolve entidade diferente da esperada na etapa inicial; verificar se o executor invalida dependências afetadas e preserva etapas ainda válidas.

Plano de avaliação proposto:
Comparar plano único, replanejamento por etapa e gatilhos por premissa invalidada. Controlar ferramentas e casos. Medir chamadas de planejamento, etapas descartadas, custo total e objetivos concluídos; escolher frequência pela volatilidade observada.

Comparações:
- T144 (alternative): ReAct incorpora observações a cada ciclo, enquanto o planejamento antecipado tenta reutilizar estrutura prevista.
- T208 (complements): Separar planejador e executor oferece um lugar explícito para validar o plano.

Afirmação rastreável:
ReWOO desacopla planejamento de observações para reduzir redundância de contexto.
Suporte: direct; fontes: V3C-S012
Limite: O estudo não permite presumir que todas as dependências possam ser previstas antes da execução.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T143:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou dependências de informação e valores ainda desconhecidos. A novidade é planejar por compromissos reversíveis, permitindo validar premissas baratas antes de consumir orçamento em etapas dependentes.

Plano com pontos de decisão
Marque etapas como investigação, preparação ou efeito. Primeiro resolva premissas que podem invalidar muitas ações posteriores. Um plano textual pode parecer completo e ainda esconder a hipótese de que uma API, arquivo ou versão existe; esses pontos precisam virar verificações antes da execução custosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V4C-S017.

Replanejamento localizado
Quando uma premissa falha, identifique os descendentes que dependem dela e invalide apenas esse conjunto. Preserve resultados independentes com suas versões. Recomeçar todo o plano desperdiça trabalho; conservar tudo indiscriminadamente propaga conclusões produzidas sobre uma base que deixou de existir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S012.

Plano como orçamento auditável
Atribua uma previsão de custo e critério de aceite a cada etapa, incluindo integração e testes. Estimativas são hipóteses revisáveis, não autorização para exceder limites. Se o esforço previsto ultrapassar o orçamento, reduza escopo permitido ou exponha o impedimento antes de iniciar metade da missão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S017.

USO AVANÇADO — Upgrade com dependências internas
Cenário: Uma aplicação depende de bibliotecas ainda incompatíveis com a versão alvo.
Estratégia: Inventarie dependências, execute um build inicial e organize ondas. Atualize bases compartilhadas antes de consumidores; quando uma biblioteca não for coberta pela automação, crie uma pendência própria em vez de declarar a aplicação migrada.
Papel do modelo pequeno: 8–14B resume incompatibilidades; 15–30B sugere plano por módulos com evidências.
Aceite proposto: Proposta: medir módulos concluídos, esforço refeito e falhas descobertas tardiamente contra ordem simples por arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017.

USO AVANÇADO — Pesquisa com decisão operacional
Cenário: É preciso comparar alternativas e preparar uma recomendação condicionada.
Estratégia: Planeje critérios, fontes e lacunas antes das buscas. O executor adapta consultas localmente; o planejador revisita apenas critérios afetados por novas evidências. Conclua com condições de adoção e pontos não resolvidos, não com um plano artificialmente cumprido.
Papel do modelo pequeno: 3–7B coleta campos por fonte; 15–30B integra critérios e contradições.
Aceite proposto: Proposta: avaliar cobertura dos critérios e correção das dependências, com custo de coleta e verificação incluído.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: preencher etapas de templates conhecidos, verificando uma premissa por vez.
8–14B: Proposta: produzir planos curtos com dependências explícitas e operações do catálogo.
15–30B: Proposta: replanejar subconjuntos após falhas, mantendo histórico de decisões e motivos.
Requisitos de treino/runtime: Exige um validador de grafo e entradas versionadas; treino pode melhorar formato, não garantir validade do plano.
Não aplicar quando: Não usar planejamento extenso quando o ambiente muda mais rápido que a execução ou o próximo passo é uma simples leitura.

## T143:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Transformação apresenta plano de dependências e substituições.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Planejamento estruturado antecede execução de tarefas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Architect antecipa proposta antes da edição.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn e Amazon documentam combinações específicas; o protocolo de compromissos e invalidação local é desenho proposto.
Consultas registradas: V4C-Q010, V4C-Q012.

## T143:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T143 → T144 [complements]
Como combinar: Hiring Assistant combina plano global com ciclo ReAct no executor local.
Interface: Plano de tarefas e observações produzidas durante sua execução.
Condição: O domínio permite decomposição e adaptação dentro de cada tarefa.
Aceite proposto: Proposta: verificar que contingência local não altera objetivo sem retorno ao planejador.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T143 → T213 [feeds]
Como combinar: Cada etapa planejada vira micro-missão com critério de aceite e fronteira de dependência.
Interface: Pacote de trabalho, pré-condições e artefato esperado.
Condição: Há valor em validar etapas separadamente.
Aceite proposto: Medir lacunas entre entregas e retrabalho de integração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não substituir valores desconhecidos por palpites para completar o plano.
- Revalidar premissas críticas imediatamente antes de efeitos que dependam delas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare planos e resultados com um modelo de fronteira em migrações delimitadas. Bons templates podem reduzir diferença em tarefas recorrentes, sem garantir planejamento aberto equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T144, T160

## Fontes primárias associadas

### C-S010 — Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models

[https://arxiv.org/abs/2305.04091](https://arxiv.org/abs/2305.04091)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separar planejamento e resolução é uma estratégia de prompting estudada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T144 — ReAct Pattern

**Nome canônico:** ReAct Pattern  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T144  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reasoning and acting

## T144:C01 — conceito

Padrão de agente que intercala deliberação operacional, ação de ferramenta e observação. A observação atualiza o próximo passo, permitindo adaptar a execução a informação externa. A existência do ciclo não demonstra que o modelo sabe verificar tudo o que encontra.

Como funciona:
- Identificar a próxima lacuna de informação ou ação útil.
- Emitir chamada de ferramenta e obter observação do ambiente.
- Atualizar estado e escolher nova ação ou término com evidência.

## T144:C02 — aplicacao

Quando usar:
- Tarefas exploratórias com dependências descobertas durante execução.
- Consultas que exigem ferramentas e correção de percurso.

Quando não usar:
- Processo determinístico já conhecido em que chamadas de LLM em cada passo só aumentam custo.

Implementação proposta:
- Limitar número de passos, tempo e repetição da mesma ação.
- Registrar observações como dados, separadas das instruções do agente.
- Exigir condição de término observável e preservar referências aos resultados.

Aplicação LAI proposta:
Proposta: usar ciclos ReAct limitados para investigação da Helena, com estado resumido e evidências externas persistidas.

## T144:C03 — riscos_validacao

Armadilhas:
- Loop pode repetir buscas sem acumular informação nova.
- Texto retornado por ferramenta pode tentar introduzir instruções indevidas.

Métricas sugeridas:
- Passos por tarefa resolvida e chamadas redundantes.
- Correção final com e sem ferramentas em conjunto de avaliação.

Testes propostos:
- Produzir resultado de ferramenta vazio e conferir adaptação ou abstenção.
- Injetar instrução estranha em documento recuperado e verificar que não altera a política do runtime.

## T144:C04 — perguntas_proveniencia

Pergunta: ReAct exige mostrar pensamentos privados?
Resposta: Não. O sistema pode registrar decisões operacionais curtas, ações e observações.

Pergunta: Mais ciclos significam mais inteligência?
Resposta: Não. Sem informação nova ou verificação, podem apenas repetir o erro.

Pergunta: Reagir a toda observação é sempre mais inteligente?
Resposta: Não. Algumas observações apenas confirmam passos previsíveis; a chamada adicional pode não mudar nenhuma decisão.

Pergunta: Como distinguir retry útil de loop?
Resposta: Pela categoria do erro, mudança de condições e evidência de progresso; igualdade de texto sozinha não decide todos os casos.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T144:C05 — mecanismo_avancado

A vantagem do ciclo observação–ação aparece quando a informação recém-obtida muda a próxima escolha. Seu custo cresce se cada rodada reenviar grandes resultados anteriores ou repetir uma consulta porque o estado de conclusão não está explícito. Um controle proposto identifica observações pelo conteúdo e pela origem, registra o que elas mudaram e diferencia investigação adicional de repetição sem informação nova.

Condição de contorno:
Em tarefas com dependências já conhecidas e ferramentas independentes, o ciclo estritamente serial pode introduzir latência evitável.

Contrato proposto:
- Entradas: Estado da tarefa, última observação, catálogo de ações e orçamento.
- Saídas: Próxima ação justificada por evidência operacional ou término verificável.
- Estado: Chamadas anteriores, observações referenciadas e hipóteses atualizadas.
- Invariante: Repetir uma ação exige nova finalidade, mudança de entrada ou política explícita de recuperação.

Compromissos de projeto:
- Reagir a cada resultado aumenta adaptação e também número de interações com o modelo.
- Agrupar observações economiza chamadas e pode retardar a percepção de um resultado decisivo.

## T144:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma ferramenta devolve repetidamente o mesmo resultado sem avanço; exigir identificação da repetição e mudança de estratégia ou encerramento com limitação.

Plano de avaliação proposto:
Comparar ReAct serial, planejamento antecipado e execução de grupos independentes. Fixar informação disponível e critérios de sucesso. Medir observações úteis por chamada, repetições, latência e conclusão; usar cenários onde resultados realmente alterem decisões.

Comparações:
- T143 (alternative): O plano antecipado evita algumas rodadas, mas depende mais de premissas estáveis.
- T218 (complements): Um detector de repetição pode limitar ciclos sem informação adicional.

Afirmação rastreável:
LLMCompiler identifica custos da chamada sequencial e propõe planejamento, despacho e execução paralela de funções.
Suporte: direct; fontes: V3C-S002
Limite: A comparação apoia um limite do serialismo, não a superioridade de paralelismo em tarefas com dependências desconhecidas.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T144:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou ganho informacional por observação. A camada nova delimita episódios de exploração, separa hipótese de fato e usa memória de decisões para impedir que cada turno reabra problemas já resolvidos.

Observação com pergunta associada
Cada chamada deve responder a uma lacuna explícita: localizar arquivo, verificar hipótese ou obter dado necessário. Ao retornar, registre se a lacuna foi resolvida e qual evidência mudou. Isso permite avaliar o ciclo por decisões melhoradas, sem depender da extensão de deliberação ou da quantidade bruta de ferramentas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

Subciclo dentro de contrato
Um executor reativo pode explorar livremente dentro de uma micro-missão, mas não alterar silenciosamente seu critério de término. Quando descobrir que o objetivo é impossível ou que falta autorização, devolva esse estado ao supervisor. A flexibilidade local fica separada da responsabilidade por redefinir o trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

Hipóteses com validade
Mantenha hipóteses descartadas e a evidência usada, associadas à revisão observada. Uma mudança de código pode reabrir uma hipótese legitimamente; repetição sem mudança não. Essa distinção evita tanto a perseveração quanto o bloqueio indevido de caminhos que se tornaram relevantes após nova informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

USO AVANÇADO — Investigação de teste intermitente
Cenário: O mesmo teste falha apenas em algumas condições.
Estratégia: Comece por reproduzir e registrar ambiente; escolha próxima ferramenta conforme a hipótese ainda não testada. Se a falha não se repetir, preserve a incerteza e busque evidência adicional. Não aplique correção apenas porque um novo run passou.
Papel do modelo pequeno: 8–14B organiza hipóteses locais; 15–30B relaciona concorrência e dependências.
Aceite proposto: Proposta: medir hipóteses eliminadas, chamadas redundantes e correções confirmadas sob repetição controlada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

USO AVANÇADO — Navegação de catálogo de ferramentas
Cenário: A primeira ferramenta encontrada não possui os campos necessários.
Estratégia: Inspecione o schema, reformule a busca por capacidade e teste a compatibilidade antes de invocar. Guarde candidatos rejeitados e motivo para não redescobrir repetidamente o mesmo contrato inadequado.
Papel do modelo pequeno: 3–7B executa escolhas entre poucos candidatos e estados tipados.
Aceite proposto: Proposta: usar consultas ambíguas e contratos próximos; aceitar seleção correta ou impedimento explícito dentro do orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: ciclos curtos de seleção e leitura, com pequena lista de ações e resultado verificável.
8–14B: Proposta: diagnóstico local com memória de hipóteses e evidências estruturadas.
15–30B: Proposta: exploração mais ampla dentro de uma missão delimitada, com supervisão do objetivo.
Requisitos de treino/runtime: O runtime precisa conservar estado factual separado do texto gerado e limitar tempo, ferramentas e repetição.
Não aplicar quando: Evitar ciclos abertos quando uma função determinística ou um plano estável já resolve a tarefa com menos chamadas.

## T144:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: O executor utiliza ReAct dentro do plano.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Hiring Assistant usa ReAct localmente; isso não prova que um loop genérico sem estados e verificadores seja apropriado a qualquer modelo pequeno.
Consultas registradas: V4C-Q006, V4C-Q009, V4C-Q010.

## T144:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T144 → T218 [feeds]
Como combinar: Mudanças de hipótese e observações fornecem sinais para detectar estagnação.
Interface: Estado semântico, evidências novas e ação realizada.
Condição: O detector distingue repetição legítima após mudança de entrada.
Aceite proposto: Injetar respostas idênticas de ferramentas e exigir parada ou mudança fundamentada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T144 → T208 [complements]
Como combinar: O supervisor delega exploração local e recebe resultado ou impedimento.
Interface: Missão, fatos confirmados e próximo requisito não satisfeito.
Condição: Escopo e término são definidos antes da delegação.
Aceite proposto: Comparar retorno do executor com o plano vigente, detectando desvio de objetivo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

CONTROLES DE FALHA
- Não promover uma sugestão do modelo a observação da ferramenta.
- Proibir que o loop esconda falha mudando o requisito que pretendia satisfazer.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de diagnóstico correto e custo por resolução com fronteira sob mesmas ferramentas. Loops adicionais podem ampliar erros de um modelo pequeno quando os verificadores são fracos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T190, T199

## Fontes primárias associadas

### C-S011 — ReAct: Synergizing Reasoning and Acting in Language Models

[https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alternância entre deliberação explícita, ações e observações externas em tarefas de agentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T145 — Adaptive Depth

**Nome canônico:** Adaptive Depth  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T145  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** profundidade adaptativa

## T145:C01 — conceito

Rótulo amplo para variar a profundidade de processamento conforme a tarefa. Neste inventário significa variar rodadas, etapas ou verificações do agente; não significa saltar camadas de qualquer transformer existente. Profundidade adicional só vale quando melhora o resultado de forma mensurável.

Como funciona:
- Estimar dificuldade ou detectar falha após uma primeira tentativa.
- Escolher entre encerrar, verificar ou expandir outra etapa.
- Parar por critério de qualidade, ganho marginal ou limite de orçamento.

## T145:C02 — aplicacao

Quando usar:
- Tarefas com dificuldade muito desigual.
- Possibilidade de testar se uma rodada adicional corrigiu algo concreto.

Quando não usar:
- Usar número fixo de reflexões apenas para aparentar análise profunda.

Implementação proposta:
- Definir níveis curtos, médios e extensos de execução.
- Avaliar política de passagem entre níveis em dados separados.
- Registrar contribuição de cada rodada e detectar repetição sem progresso.

Aplicação LAI proposta:
Proposta: a Helena expandir investigação apenas quando faltarem evidências ou um teste falhar, preservando respostas já aceitas.

## T145:C03 — riscos_validacao

Armadilhas:
- Indicador de dificuldade pode confundir texto longo com tarefa difícil.
- Rodadas extras podem degradar uma resposta inicialmente correta.

Métricas sugeridas:
- Qualidade versus número de etapas.
- Custo marginal de cada correção realmente obtida.

Testes propostos:
- Comparar profundidade fixa e adaptativa no mesmo teto de custo.
- Dar tarefa já resolvida e verificar encerramento sem revisões desnecessárias.

## T145:C04 — perguntas_proveniencia

Pergunta: Adaptive Depth reduz camadas do Qwen?
Resposta: Não nesta proposta; atua no workflow do agente.

Pergunta: Qual profundidade é ideal?
Resposta: Depende de tarefa e verificador e deve ser estimada por avaliação.

Pergunta: Uma resposta mais longa demonstra maior profundidade útil?
Resposta: Não. O ganho deve aparecer em evidências, hipóteses resolvidas ou resultados verificados, não em extensão textual.

Pergunta: Quando a política deve registrar inconclusão?
Resposta: Quando o objetivo permanece pendente e não há orçamento ou ação elegível que sustente nova etapa.

Escopo das fontes:
s1 sustenta o tema de orçamento em inferência; a política de profundidade de agente é uma proposta distinta, não o algoritmo do artigo.

## T145:C05 — mecanismo_avancado

Profundidade adaptativa pode usar o ganho observado entre etapas como sinal de continuidade: um novo teste elimina uma hipótese, uma busca resolve uma lacuna ou uma revisão corrige um defeito. Contar palavras de deliberação não mede esse ganho. Uma política proposta combina orçamento residual e evidência de progresso, reservando uma saída explícita quando a próxima rodada não tem uma operação verificável capaz de alterar a conclusão.

Condição de contorno:
Um sinal de progresso mal definido pode premiar reformulações repetidas e interromper cedo tarefas difíceis cujo benefício aparece apenas depois.

Contrato proposto:
- Entradas: Estado atual, critérios pendentes, custo da próxima etapa e limite global.
- Saídas: Continuar, concluir ou interromper com pendências identificadas.
- Estado: Profundidade percorrida, mudanças verificadas e recursos restantes.
- Invariante: Maior profundidade não substitui evidência de satisfação do requisito.

Compromissos de projeto:
- Parar cedo reduz desperdício e pode perder soluções de descoberta tardia.
- Manter exploração mínima melhora cobertura e aumenta custo em casos já resolvidos.

## T145:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer uma tarefa resolvida na primeira rodada e outra que exige buscar um dado ausente; verificar se a política diferencia conclusão de simples confiança declarada.

Plano de avaliação proposto:
Comparar número fixo de rodadas e política adaptativa sob o mesmo orçamento máximo. Estratificar por dificuldade medida independentemente. Avaliar sucesso, custo e interrupções prematuras; decidir pela fronteira entre qualidade e trabalho adicional, sem limiar universal.

Comparações:
- T146 (specializes): Profundidade controla número de etapas; adaptive compute também distribui largura, modelos e verificadores.
- T219 (complements): O limite global de passos encerra a execução; profundidade adaptativa decide como distribuir esforço dentro desse limite.

Afirmação rastreável:
O estudo de computação em inferência mostra que a utilidade das estratégias varia com a dificuldade da consulta.
Suporte: related; fontes: V3C-S003
Limite: Os experimentos de raciocínio não validam diretamente este detector de progresso para workflows.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T145:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 usou progresso verificável como sinal de continuidade. O aprofundamento separa limite de raciocínio do modelo, número de ações e profundidade do workflow, com orçamento reservado para concluir e verificar.

Três profundidades distintas
Tokens internos de reasoning, rodadas de ferramenta e caminhos no grafo não são intercambiáveis. Um modelo pode raciocinar muito sem obter informação nova; outro pode realizar várias leituras úteis com pouca geração. A política deve definir qual dimensão está controlando e medir o efeito de cada uma separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

Parada compatível com o servidor
Um limiar de thinking pode ser aproximado e depender de delimitadores ou mecanismos específicos. Reserve espaço para a resposta final e trate corte prematuro como resultado incompleto. Não suponha que um parâmetro com nome semelhante tenha o mesmo comportamento em outro modelo, template ou backend.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018.

Próxima etapa com valor esperado
Antes de ampliar esforço, identifique uma ação que possa mudar a decisão e seu custo provável. Se faltam fontes, mais reasoning sobre os mesmos dados não cria evidência. Se há candidatos verificáveis, uma rodada adicional pode valer mais que aumentar o tamanho da resposta final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S003.

USO AVANÇADO — Resposta técnica com recuperação
Cenário: Perguntas variam entre busca factual e integração de condições.
Estratégia: Use esforço curto para localizar fatos; amplie somente quando existirem conflitos ou etapas dedutivas verificáveis. Se a fonte não responder, finalize insuficiência. Execute o verificador antes de consumir a reserva da resposta final.
Papel do modelo pequeno: 3–7B extrai; 8–14B integra poucas condições; 15–30B analisa exceções delimitadas.
Aceite proposto: Proposta: comparar matriz de orçamentos em perguntas reservadas, incluindo cortes de saída e afirmações sem fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

USO AVANÇADO — Reparo com tentativas progressivas
Cenário: Um patch falha em testes e o erro se mantém.
Estratégia: Diferencie erro de formato, falha conhecida e ausência de progresso. Permita nova tentativa somente com diagnóstico diferente ou mudança concreta de estratégia; a tentativa seguinte recebe o orçamento restante, não o orçamento inicial.
Papel do modelo pequeno: 8–30B prepara candidatos de reparo enquanto ferramentas verificam comportamento.
Aceite proposto: Proposta: medir reparos aceitos por rodada e encerrar quando a política definida antes do teste não justificar continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: poucas decisões locais com saída curta; profundidade adicional só após sinal externo de necessidade.
8–14B: Proposta: orçamento de reasoning específico do checkpoint e loops limitados por teste.
15–30B: Proposta: revisão de casos mais complexos mantendo reserva explícita de verificação e síntese.
Requisitos de treino/runtime: Confirmar suporte e semântica do parâmetro; a banda de tamanho não define o orçamento adequado.
Não aplicar quando: Não ampliar profundidade quando falta informação externa ou quando o modelo repete a mesma conclusão sem nova evidência.

## T145:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: O modelo controla orçamento de thinking interno; isso é relacionado, mas não comprova profundidade de rodadas ou etapas do agente.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron 9B documenta mecanismo de orçamento; a documentação não comprova dez implantações de profundidade adaptativa nem ganhos gerais.
Consultas registradas: V4C-Q014, V4C-Q009.

## T145:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T145 → T168 [complements]
Como combinar: O limite suave dispara encerramento planejado antes do teto que pode truncar o resultado.
Interface: Consumo atual, reserva de saída e semântica do servidor.
Condição: O orçamento é medido na unidade correta.
Aceite proposto: Forçar limite próximo e exigir estado de conclusão coerente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T145 → T218 [feeds]
Como combinar: A política recebe sinais de estagnação para decidir se outra etapa é útil.
Interface: Mudança de artefato, teste e hipótese entre rodadas.
Condição: A tarefa admite medir progresso observável.
Aceite proposto: Comparar parada por teto com parada por falta de progresso em falhas conhecidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar resposta truncada como tentativa semanticamente avaliada.
- Registrar esforço solicitado e efetivamente observado, incluindo excesso permitido pelo backend.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas qualidade–custo por tarefa com um modelo de fronteira. Um ponto favorável em orçamento controlado não demonstra que mais tokens eliminem a diferença de capacidade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T146, T190, T201

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S003 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Efetividade de estratégias de computação em inferência varia com dificuldade; alocação adaptativa pode superar orçamento uniforme no estudo.

Limite: Experimentos não validam política universal para agentes, ferramentas ou cargas LAI.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T146 — Adaptive Compute

**Nome canônico:** Adaptive Compute  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T146  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** computação adaptativa

## T146:C01 — conceito

Alocação variável de recursos de inferência conforme o valor esperado do processamento adicional. Recursos incluem tokens, candidatos, chamadas de ferramentas e modelos mais capazes. É uma família de políticas, não um botão universal capaz de melhorar qualquer tarefa aumentando o orçamento.

Como funciona:
- Estimar valor e custo de ações computacionais candidatas.
- Direcionar orçamento à opção com melhor ganho esperado admissível.
- Reavaliar após novos resultados e encerrar ao atingir o limite ou objetivo.

## T146:C02 — aplicacao

Quando usar:
- Carga com mistura de perguntas triviais e investigações difíceis.
- Operações de alto valor que justificam verificação adicional.

Quando não usar:
- Não existe medida confiável de qualidade nem mecanismo para detectar falta de progresso.

Implementação proposta:
- Definir orçamento total de missão, incluindo subagentes e retries.
- Comparar ações: recuperar fonte, testar código, gerar candidato ou trocar modelo.
- Calibrar política em curvas de qualidade versus custo.

Aplicação LAI proposta:
Proposta: reservar recursos da Helena segundo dificuldade e verificabilidade, tratando GPU, APIs e tempo do usuário como custos distintos.

## T146:C03 — riscos_validacao

Armadilhas:
- Mais tokens podem produzir justificativas maiores para a mesma conclusão errada.
- Custo local invisível, como ocupação de GPU, pode tornar a política ineficiente.

Métricas sugeridas:
- Resultado aceito por unidade de custo ou tempo.
- Distribuição do orçamento entre tarefas e taxa de esgotamento.

Testes propostos:
- Executar políticas alternativas sob orçamento total igual.
- Simular queda do ganho marginal e exigir término ou mudança de estratégia.

## T146:C04 — perguntas_proveniencia

Pergunta: Adaptive Compute é igual a MoE?
Resposta: Não. MoE é arquitetura interna; aqui a política controla recursos da execução.

Pergunta: Deve usar sempre todo orçamento disponível?
Resposta: Não. Encerrar cedo pode ser a melhor decisão quando o objetivo já foi comprovado.

Pergunta: Igualar tokens torna duas políticas comparáveis em latência?
Resposta: Não. Sequencialidade, tamanho do modelo, ferramentas e filas alteram o tempo mesmo com consumo textual semelhante.

Pergunta: Por que cobrar o verificador no orçamento?
Resposta: Porque seleção também consome recursos; omiti-la pode transformar uma aparente economia em custo total maior.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T146:C05 — mecanismo_avancado

Computação adaptativa distribui um vetor de recursos: número de candidatos, tamanho de contexto, chamadas de ferramenta, profundidade e força do modelo. Duas políticas com igual número de tokens podem consumir tempos e custos muito diferentes. Uma formulação operacional compara o benefício esperado da próxima alocação com seu custo marginal, incluindo o verificador que escolherá entre candidatos e os limites de concorrência que podem impedir paralelismo real.

Condição de contorno:
Gerar mais alternativas pouco diversas pode acrescentar custo sem ampliar a chance de encontrar uma solução correta.

Contrato proposto:
- Entradas: Classe de tarefa, recursos disponíveis, qualidade exigida e custos estimados.
- Saídas: Alocação por etapa e justificativa para ampliar ou encerrar processamento.
- Estado: Resultados intermediários, diversidade dos candidatos e consumo observado.
- Invariante: Todos os ramos e verificadores são contabilizados no mesmo objetivo.

Compromissos de projeto:
- Mais largura encontra alternativas e aumenta trabalho de seleção.
- Mais profundidade explora uma trajetória e pode reforçar uma premissa errada.

## T146:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir candidatos quase idênticos enquanto o avaliador os pontua igualmente; a política deve reconhecer baixo ganho informacional antes de ampliar indefinidamente a amostra.

Plano de avaliação proposto:
Comparar largura fixa, profundidade fixa e adaptação em orçamentos equivalentes de custo ou tempo, informando qual unidade foi igualada. Medir sucesso por classe, diversidade útil e custo de avaliação; escolher a alocação pela demanda observada.

Comparações:
- T145 (complements): A profundidade é uma dimensão possível, não o orçamento completo.
- T176 (complements): Planejamento informa antecipadamente onde o recurso pode destravar dependências.

Afirmação rastreável:
A alocação de computação em inferência pode beneficiar-se de adaptação por dificuldade em vez de estratégia uniforme.
Suporte: direct; fontes: V3C-S003
Limite: A fonte apresenta resultados em configuração experimental específica, sem garantir benefício de toda expansão de orçamento.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T146:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 apresentou o vetor de recursos e custo marginal. A camada nova define portfólios de ações concorrentes, diversidade útil e decisão de reduzir trabalho sob restrições de fila e verificação.

Portfólio de ações, não só amostras
Distribua orçamento entre buscar evidência, gerar alternativa e verificar um candidato. Muitas amostras do mesmo prompt podem repetir a mesma suposição errada. Prefira diversidade que altere informação ou método, como um cálculo executável e uma consulta documental, quando ambos respondem à mesma questão de forma comparável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S003, V4C-S009.

Custo de integração
Toda alternativa criada exige comparação e eventual reconciliação. O planejador precisa reservar esse trabalho, especialmente quando usa workers pequenos com saídas heterogêneas. Se o custo de integrar cresce mais rápido que o benefício de novos ramos, reduzir largura pode melhorar tempo até uma resposta realmente aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Adaptação condicionada à capacidade
Escolher mais paralelismo só reduz latência quando existe capacidade de execução. Sob fila saturada, ações adicionais competem com as já iniciadas. Use sinais de espera e utilização para preferir trabalho que destrava dependências, preservando verificações obrigatórias mesmo quando o contexto exploratório for reduzido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S009.

USO AVANÇADO — Escolha entre candidatos de código
Cenário: Há várias correções plausíveis para um defeito delimitado.
Estratégia: Gere poucos candidatos com hipóteses distintas e rode testes relevantes em ambiente separado. Amplie o conjunto apenas se nenhuma alternativa passou e houver uma nova hipótese. Evite decidir por eloquência ou pelo número de agentes concordando.
Papel do modelo pequeno: 8–14B gera correções locais; 15–30B compara evidências de integração.
Aceite proposto: Proposta: medir aceitação, regressões e custo total dos candidatos descartados contra um único candidato de fronteira.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S007, V4C-S009.

USO AVANÇADO — Pesquisa com orçamento variável
Cenário: Uma consulta exige mais cobertura quando há fontes conflitantes.
Estratégia: Faça uma busca inicial curta, estime lacunas por critério e distribua workers apenas para aspectos ainda descobertos. Reuse evidências já coletadas por identidade de documento; se a latência estiver comprometida, entregue cobertura parcial explicitamente permitida.
Papel do modelo pequeno: 3–7B extrai por fonte; 15–30B prioriza quais lacunas ainda podem mudar a conclusão.
Aceite proposto: Proposta: comparar cobertura, sustentação e custo por resposta aceita, preservando casos abandonados nas métricas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: especialistas baratos em tarefas fechadas, com poucas alternativas por chamada.
8–14B: Proposta: explorar hipóteses locais diferentes e produzir artefatos diretamente verificáveis.
15–30B: Proposta: alocar e integrar esforço em problemas delimitados, sem assumir orçamento ilimitado.
Requisitos de treino/runtime: Medir custo de verificação e integração, filas e memória; parâmetros não substituem profiling do hardware e do servidor.
Não aplicar quando: Não escalar quantidade de amostras quando faltam diversidade ou um verificador capaz de distingui-las.

## T146:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Reduzir trabalho em busca é analogia para adaptar esforço de inferência.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: Orçamento de reasoning controla uma dimensão de computação, não alocação geral.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes cobrem budgets e coordenação; a política de portfólio é proposta, não uma implantação demonstrada com todas as bandas.
Consultas registradas: V4C-Q004, V4C-Q014, V4C-Q009.

## T146:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T146 → T147 [complements]
Como combinar: Fan-out materializa apenas os ramos cujo benefício esperado justifica integração.
Interface: Lista de hipóteses, orçamento por ramo e condição de junção.
Condição: As saídas podem ser comparadas no mesmo critério.
Aceite proposto: Medir duplicação semântica e utilidade marginal dos ramos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T146 → T174 [complements]
Como combinar: Prioridade favorece ações que liberam caminho crítico sem bloquear tarefas antigas indefinidamente.
Interface: Custo estimado, dependências e deadline.
Condição: Há recursos disponíveis ou política de preempção definida.
Aceite proposto: Reproduzir carga mista e medir espera por classe e conclusão correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar que geração de candidatos consuma a reserva destinada à verificação.
- Não transferir uma vitória em benchmark sintético para todo tipo de tarefa sem estratificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fronteiras de qualidade, custo e latência em cargas equivalentes. Combinações de modelos pequenos podem vencer em nichos verificáveis, mantendo limites em conhecimento e planejamento aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T145, T184, T201

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S003 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Efetividade de estratégias de computação em inferência varia com dificuldade; alocação adaptativa pode superar orçamento uniforme no estudo.

Limite: Experimentos não validam política universal para agentes, ferramentas ou cargas LAI.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T147 — Parallel Fan-Out

**Nome canônico:** Parallel Fan-Out  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T147  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** distribuição paralela em ramos

## T147:C01 — conceito

Decomposição de uma etapa em vários ramos independentes executados concorrentemente, seguida de agregação. Pode envolver ferramentas, trabalhadores ou agentes. O coordenador precisa definir o que constitui conjunto completo, resultado parcial aceitável e falha impeditiva.

Como funciona:
- Criar unidades de trabalho com escopo e identificadores exclusivos.
- Distribuir unidades para executores com limite de concorrência.
- Agregar resultados verificando cobertura, duplicatas e inconsistências.

## T147:C02 — aplicacao

Quando usar:
- Busca em fontes independentes.
- Processamento de documentos que podem ser analisados separadamente.

Quando não usar:
- Cada ramo precisa conhecer continuamente todos os resultados dos demais.

Implementação proposta:
- Fixar contrato de entrada e saída para cada ramo.
- Declarar política de timeout, cancelamento e resultados parciais.
- Persistir manifest com unidades esperadas e concluídas antes da síntese.
- Reservar prazo para a agregação depois do encerramento dos ramos.

Aplicação LAI proposta:
Proposta: separar auditorias por módulos com especialistas consultivos e consolidar por um decisor, usando artefatos como interface.

## T147:C03 — riscos_validacao

Armadilhas:
- Agregador pode esconder ausência de um ramo importante.
- Aumentar fan-out sem capacidade disponível só aumenta filas.

Métricas sugeridas:
- Cobertura das unidades e tempo de cauda.
- Custo de coordenação e fração de resultados duplicados.

Testes propostos:
- Perder um ramo e exigir que o consolidado sinalize cobertura incompleta.
- Entregar respostas fora de ordem e confirmar reconstrução determinística do conjunto.

## T147:C04 — perguntas_proveniencia

Pergunta: Fan-out é sinônimo de multiagente?
Resposta: Não. Os ramos podem ser funções comuns sem LLM.

Pergunta: O consolidado pode assumir que todos responderam?
Resposta: Não. Deve comparar os resultados recebidos com o manifest esperado.

Pergunta: Quando todos os ramos existentes terminaram, o fan-out acabou?
Resposta: Somente se a fase que pode criar novos ramos também estiver encerrada.

Pergunta: Uma lista de resultados em ordem de chegada é reproduzível?
Resposta: Não necessariamente; preservar IDs e aplicar ordenação estável quando o consumidor depende da sequência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T147:C05 — mecanismo_avancado

A junção de um fan-out precisa saber quando o conjunto esperado está completo. Em expansão dinâmica, terminar a criação dos ramos é um evento diferente de terminar os ramos existentes. Uma política pode exigir todos, quorum ou melhor resultado até o deadline, mas cada escolha muda o significado da entrega. Agregações sensíveis à ordem devem usar uma chave lógica, pois ordem de término depende de latência e não de relevância.

Condição de contorno:
Ramos que editam o mesmo artefato ou dependem da saída uns dos outros não são independentes apenas porque foram delegados separadamente.

Contrato proposto:
- Entradas: Unidades de trabalho identificadas, cardinalidade ou condição de fechamento e regra de junção.
- Saídas: Agregado, cobertura dos ramos e ausências explicitadas.
- Estado: Ramos previstos, criados, concluídos, falhos e cancelados.
- Invariante: A junção não declara completude antes do fechamento da expansão.

Compromissos de projeto:
- Esperar todos preserva cobertura e fica sujeito ao ramo mais lento.
- Aceitar quorum reduz cauda de latência e exige provar que o requisito tolera resultados ausentes.

## T147:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar a descoberta do último ramo e concluir rapidamente os demais; impedir que o agregador feche a tarefa antes de conhecer a cardinalidade final.

Plano de avaliação proposto:
Comparar junção completa e parcial com distribuição de latências controlada. Medir cobertura, tempo do ramo crítico, consumo e qualidade do agregado. Adotar entrega parcial apenas quando o critério da tarefa a distinguir de conclusão integral.

Comparações:
- T139 (complements): Concorrência de chamadas é um mecanismo de execução dos ramos.
- T160 (complements): Um DAG representa dependências e a condição de prontidão da junção.

Afirmação rastreável:
LangGraph oferece Send para fan-out dinâmico e reducers para agregar atualizações de estado.
Suporte: direct; fontes: V3C-S006
Limite: A biblioteca não determina o quorum de negócio nem garante independência dos efeitos de cada ramo.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T147:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu completude de ramos e políticas de junção. O novo desenho acrescenta contratos de diversidade, tratamento de atrasos e limitação hierárquica para impedir explosão de subagentes.

Partição por pergunta diferente
Delegue ramos que respondam aspectos distintos ou usem evidências independentes. Dividir a mesma pergunta sem mudar fontes tende a gerar duplicação e erro correlacionado. O coordenador precisa registrar qual lacuna cada ramo cobre e reconhecer quando dois resultados são apenas paráfrases do mesmo documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Capacidade compartilhada na árvore
Cada subagente pode gerar novas chamadas, portanto limitar apenas o número de filhos diretos não limita a carga total. Passe orçamento residual e contador global pela árvore. Expansão exige reservar capacidade, evitando que um worker reinicie cotas ao criar outro worker.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S009.

Atraso com significado
Um ramo lento pode ser o único responsável por um requisito obrigatório. Encerrar por quorum sem olhar a cobertura pode entregar uma resposta incompleta com aparência de consenso. Diferencie requisito indispensável, redundância e exploração opcional; prazo expirado deve produzir uma lacuna identificada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S007.

USO AVANÇADO — Verificação de patch por propriedades
Cenário: O mesmo diff precisa preservar comportamento, escopo e ausência de resíduos.
Estratégia: Distribua propriedades independentes a revisores delimitados, incluindo ferramentas determinísticas. Agregue por critério, não por votação global. Se uma propriedade obrigatória falhar ou não for avaliada, mantenha o candidato sem aceite.
Papel do modelo pequeno: 3–14B revisa critérios estreitos; 15–30B integra conflitos com evidências.
Aceite proposto: Proposta: medir bugs detectados, falso bloqueio e custo de revisão em patches com defeitos introduzidos conhecidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

USO AVANÇADO — Inventário técnico de vários módulos
Cenário: Uma migração exige mapear dependências de dezenas de componentes.
Estratégia: Particione por módulo com entradas versionadas e formato comum. Reserve um ramo de integração para detectar dependências entre módulos; alterações compartilhadas voltam a uma fila serial, evitando duas correções concorrentes do mesmo arquivo.
Papel do modelo pequeno: 3–7B extrai símbolos e versões; 8–30B interpreta relações e exceções.
Aceite proposto: Proposta: conferir cobertura do inventário, conflitos e tempo de integração contra processamento sequencial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: workers com uma pergunta objetiva e saída curta, evitando autonomia recursiva.
8–14B: Proposta: revisores ou executores especializados em um módulo com contrato explícito.
15–30B: Proposta: coordenador de conjunto limitado, com integração obrigatória e memória de cobertura.
Requisitos de treino/runtime: Necessita orçamento compartilhado, identidade dos ramos e agregador que trate ausência, erro e duplicação.
Não aplicar quando: Não usar quando os ramos dependem fortemente do mesmo estado mutável ou quando integração domina todo o trabalho.

## T147:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O líder cria subagentes em paralelo e agrega suas saídas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Workflows incluem forks paralelos e junções.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: CodeCourt executa revisores por propriedade em paralelo e agrega todos os resultados antes de encaminhar o diff.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: O sistema limita paralelismo onde ele violaria estado; não é fan-out de ferramentas LLM.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e AutoClean documentam fan-out em funções diferentes. Cada deployment aparece uma vez, independentemente do número de ramos.
Consultas registradas: V4C-Q003, V4C-Q006, V4C-Q010.

## T147:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T147 → T237 [feeds]
Como combinar: A decomposição fornece tarefas delimitadas aos subagentes e recebe resultados por objetivo.
Interface: Objetivo, fontes, escopo, formato e estado de cada ramo.
Condição: A delegação possui lacunas identificáveis e resultados comparáveis.
Aceite proposto: Proposta: medir cobertura real sem contar respostas duplicadas como contribuição nova.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T147 → T200 [complements]
Como combinar: CodeCourt usa revisores paralelos por propriedade e agrega seus vereditos.
Interface: Diff e critérios separados para cada revisor.
Condição: Cada propriedade obrigatória precisa passar.
Aceite proposto: Proposta: semear violações distintas e conferir qual revisor as identifica.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Impedir fan-out recursivo sem consumo do orçamento comum.
- Conservar resultado tardio como evidência adicional, sem alterar silenciosamente uma entrega já publicada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare equipes pequenas com fronteira individual e com fronteira paralela, igualando custo e ferramentas. Mais agentes não garantem independência nem melhor resposta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T001, T139, T169

## Fontes primárias associadas

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T148 — Conditional Branching

**Nome canônico:** Conditional Branching  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T148  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ramificação condicional

## T148:C01 — conceito

Controle de fluxo que escolhe próximos passos segundo condições do estado. A condição pode ser determinística ou uma classificação produzida por modelo, desde que validada. Ramificação cria caminhos distintos e exige que cada caminho tenha saída, dependências e término definidos.

Como funciona:
- Ler um estado consistente e os campos exigidos pela condição.
- Avaliar regra ou classificador e converter resultado em rota conhecida.
- Executar somente o ramo autorizado e registrar a transição.

## T148:C02 — aplicacao

Quando usar:
- Fluxos com tratamento distinto para sucesso, falha e falta de informação.
- Triagem entre capacidades ou tipos de documento.

Quando não usar:
- Condição crítica é texto livre não validado ou pode selecionar código arbitrário.

Implementação proposta:
- Usar enum de rotas permitidas e tratar estado desconhecido.
- Separar decisão de domínio de controles obrigatórios de autorização.
- Testar cada aresta, inclusive erro e caminho sem correspondência.

Aplicação LAI proposta:
Proposta: a Helena ter ramos claros para evidência suficiente, busca adicional, correção e impossibilidade, evitando loops implícitos.

## T148:C03 — riscos_validacao

Armadilhas:
- Ramo padrão pode transformar incerteza em uma decisão silenciosa.
- Mudança de schema pode invalidar condições sem erro evidente.

Métricas sugeridas:
- Cobertura das transições em testes.
- Frequência de rota desconhecida e retrabalho por classificação incorreta.

Testes propostos:
- Fornecer enum inesperado e exigir falha explícita ou recuperação definida.
- Alterar um campo de estado e verificar que somente a rota correspondente é executada.

## T148:C04 — perguntas_proveniencia

Pergunta: Uma LLM pode escolher o ramo?
Resposta: Sim, mas sua saída deve pertencer ao conjunto permitido e respeitar controles externos.

Pergunta: Branching exige DAG?
Resposta: Não. Pode existir em máquina de estados com ciclos limitados.

Pergunta: Desconhecido deve virar false automaticamente?
Resposta: Não. A política precisa decidir se busca dados, espera ou termina inconclusiva; ausência e negação têm significados distintos.

Pergunta: Como tornar uma decisão reproduzível?
Resposta: Persistir versão do estado, versão da regra e valor observado, em vez de recalcular a partir de um estado posterior.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T148:C05 — mecanismo_avancado

Condições de fluxo devem diferenciar falso, desconhecido e erro de avaliação. Tratar ausência de evidência como falso pode enviar o workflow para uma ação prematura. Quando a condição vem de uma LLM, o valor precisa ser validado contra um conjunto fechado de rotas, e o estado utilizado na decisão deve ser registrado. Atualizações concorrentes podem tornar a decisão obsoleta entre avaliação e execução.

Condição de contorno:
Uma guarda baseada em estado mutável precisa de revalidação ou vínculo de versão antes de efeitos dependentes daquela condição.

Contrato proposto:
- Entradas: Estado versionado, expressão da guarda ou classificação validada e mapa de destinos.
- Saídas: Destino permitido ou estado de decisão inconclusiva.
- Estado: Valor observado, regra aplicada e revisão do estado.
- Invariante: Toda saída da guarda pertence ao mapa de rotas e possui caminho de término.

Compromissos de projeto:
- Condições determinísticas são auditáveis, mas exigem dados formalizados.
- Classificação por modelo lida com linguagem ambígua e introduz variabilidade e custo de validação.

## T148:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover um campo necessário à guarda e alterar o estado após sua avaliação; exigir inconclusão no primeiro caso e rejeição ou reavaliação da decisão obsoleta no segundo.

Plano de avaliação proposto:
Comparar regras, classificador e combinação dos dois usando estados com rótulos conhecidos. Medir rotas indevidas, ambiguidades corretamente preservadas e ciclos introduzidos. Escolher por erro de encaminhamento e custo, não apenas por acerto médio.

Comparações:
- T134 (complements): Roteamento semântico pode produzir um sinal, mas o grafo deve validar a transição.
- T142 (complements): O framework fornece transições e estado; a guarda pertence ao contrato da tarefa.

Afirmação rastreável:
LangGraph permite transições condicionais e atualização de estado associada ao encaminhamento por Command.
Suporte: direct; fontes: V3C-S006
Limite: Um destino válido estruturalmente não demonstra que a condição semântica foi bem avaliada.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T148:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu falso, desconhecido e erro. A camada nova valida exaustividade de caminhos, precedência entre guardas e estabilidade das decisões diante de eventos fora de ordem.

Tabela de decisão verificável
Escreva combinações relevantes de condições e o destino correspondente antes de codificar o grafo. Guardas sobrepostas precisam de prioridade explícita; condições não cobertas precisam de uma saída definida. Isso evita que a ordem acidental de ifs determine decisões diferentes após uma refatoração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S032.

Versão da guarda e do estado
Uma decisão deve registrar qual estado observou e qual regra a produziu. Se houver evento concorrente relevante, reavalie antes do efeito ou use uma pré-condição atômica. O modelo pode sugerir uma categoria, mas a transição confirmada pertence ao controlador e ao contrato vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S002.

Estados terminais protegidos
Mensagens atrasadas não devem reabrir trabalho concluído por uma simples sobrescrita. Defina quais transições podem corrigir um estado terminal e exija um evento explícito para elas. Reabertura de tarefa é mudança de domínio distinta de retransmissão de uma atualização antiga.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004.

USO AVANÇADO — Promoção de uma alteração de código
Cenário: Um patch precisa passar build, testes e revisão antes de avançar.
Estratégia: Use guardas por evidência versionada, com estados aprovado, reprovado e ainda não avaliado. Quando o patch mudar, invalide os resultados dependentes. Uma mensagem tardia de sucesso da versão anterior não libera a nova alteração.
Papel do modelo pequeno: 3–30B pode explicar diagnóstico; regras de promoção continuam determinísticas.
Aceite proposto: Proposta: permutar ordem dos eventos de testes e exigir decisões idênticas para o mesmo conjunto de fatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S032.

USO AVANÇADO — Fluxo conversacional com informação incompleta
Cenário: O usuário alterna entre consultar dados e preparar uma ação.
Estratégia: Classifique intenção, resolva entidades e mantenha uma rota para informação insuficiente. Antes de escrever, confirme requisitos no estado atual. Se a consulta mudou, encerre ou substitua o plano antigo explicitamente, preservando o histórico.
Papel do modelo pequeno: 3–7B classifica; 8–14B extrai entidades; 15–30B propõe decomposição complexa.
Aceite proposto: Proposta: testar pedidos ambíguos, mudanças de objetivo e eventos duplicados, medindo ações incorretas e esclarecimentos úteis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: produzir enums de condição entre poucos caminhos com suporte explícito a desconhecido.
8–14B: Proposta: extrair fatos para guardas compostas, sem decidir o efeito sozinho.
15–30B: Proposta: propor novos caminhos para revisão, conservando a máquina de estados como autoridade operacional.
Requisitos de treino/runtime: Exige testes de tabela de decisão, versões de regras e pré-condições no backend que executa mutações.
Não aplicar quando: Não deixar transições críticas dependerem somente de texto livre ou de confiança não calibrada do modelo.

## T148:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: O DSL representa condicionais e outras transições.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Gates condicionam a transição entre estágios de deployment.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor e Up CD sustentam coordenação por condições. A tabela de decisão e seus testes são propostas para a integração local.
Consultas registradas: V4C-Q003, V4C-Q002, V4C-Q010.

## T148:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T148 → T141 [feeds]
Como combinar: Enums e evidências estruturadas tornam a classificação consumível pela guarda.
Interface: Condição, origem, versão e estado de validação.
Condição: O parser distingue desconhecido de falso.
Aceite proposto: Fornecer valores inválidos e exigir rota de erro explícita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T148 → T241 [complements]
Como combinar: Replay deve reproduzir a interpretação de decisões usando versões compatíveis.
Interface: Eventos ordenados e versão do avaliador de guardas.
Condição: Regras históricas continuam disponíveis ou têm migração definida.
Aceite proposto: Reprocessar eventos permutáveis e conferir invariantes de estado terminal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S004, V3C-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não liberar ação com base em evidência de artefato diferente.
- Detectar guardas contraditórias e caminhos sem término antes de publicar o workflow.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos na classificação de entradas que alimentam as guardas, mantendo controlador igual. Desempenho do workflow não pode ser atribuído inteiro à LLM.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T134, T143, T160

## Fontes primárias associadas

### C-S013 — Workflows and agents

[https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento e arestas condicionais selecionam fluxos conforme estado ou classificação da entrada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T149 — Priority Queue

**Nome canônico:** Priority Queue  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T149  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** fila de prioridade

## T149:C01 — conceito

Estrutura que retira itens conforme uma chave de prioridade, normalmente implementada por heap. A fila organiza ordem; não define sozinha a política correta de atendimento. Empates, mudanças de prioridade, cancelamento e equidade precisam ser especificados pela aplicação.

Como funciona:
- Calcular chave que representa prioridade e critério de desempate.
- Inserir item sem depender da ordem de chegada dos resultados.
- Retirar o item admissível mais prioritário para um worker disponível.

## T149:C02 — aplicacao

Quando usar:
- Pedidos com urgência ou prazos distintos.
- Scheduler com vários trabalhos prontos para executar.

Quando não usar:
- Todas as tarefas precisam estritamente da ordem de chegada por dependência de negócio.

Implementação proposta:
- Usar chave como prioridade e contador monotônico de desempate.
- Definir atualização ou invalidação de itens cancelados.
- Combinar com limite de concorrência e prevenção de inanição.

Aplicação LAI proposta:
Proposta: distinguir tarefas interativas e processamento em lote da Helena, sem permitir que relatórios atrasem toda interação.

## T149:C03 — riscos_validacao

Armadilhas:
- Objetos não comparáveis podem quebrar desempates do heap.
- Prioridade alta permanente pode impedir execução de tarefas de baixa prioridade.

Métricas sugeridas:
- Tempo na fila por classe.
- Número de itens expirados, cancelados e nunca atendidos.

Testes propostos:
- Inserir prioridades e empates conhecidos e verificar ordem estável esperada.
- Manter chegada de itens urgentes e observar se a política de equidade atende os antigos.

## T149:C04 — perguntas_proveniencia

Pergunta: Priority queue é scheduler completo?
Resposta: Não. Falta escolher política, capacidade e preempção.

Pergunta: Prioridade deve vir de texto livre do agente?
Resposta: Preferencialmente de campos e regras de negócio verificáveis.

Pergunta: Duas tarefas com prioridade igual saem em FIFO?
Resposta: Somente se o contrato adicionar um desempate por chegada ou usar uma implementação que o garanta.

Pergunta: Por que não mudar a chave dentro do heap?
Resposta: Porque a posição armazenada não é recalculada automaticamente; a estrutura pode deixar de representar a ordenação pretendida.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T149:C05 — mecanismo_avancado

Um heap não mantém ordem estável entre itens com a mesma prioridade sem critério adicional. Uma chave composta, como prioridade e sequência de chegada, resolve desempate sem comparar payloads heterogêneos. Alterar diretamente a prioridade de um item já inserido viola a organização do heap; uma estratégia proposta usa nova versão e marca a entrada anterior como obsoleta. Isso exige limpeza para não acumular itens mortos.

Condição de contorno:
A fila pode ordenar trabalho inviável: disponibilidade de recurso e dependências continuam sendo responsabilidades do escalonador.

Contrato proposto:
- Entradas: Item identificado, prioridade, sequência e versão da prioridade.
- Saídas: Próximo item vigente ou indicação de fila vazia.
- Estado: Heap, mapa de versões e entradas canceladas ou substituídas.
- Invariante: Cada item lógico é retirado no máximo uma vez para sua versão vigente.

Compromissos de projeto:
- Atualização por entradas obsoletas simplifica implementação e pode aumentar memória.
- Desempate por chegada oferece estabilidade, mas não resolve justiça entre clientes de volumes diferentes.

## T149:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir prioridades iguais com payloads não comparáveis, repriorizar um item e cancelar outro; verificar ordem definida e descarte das versões antigas.

Plano de avaliação proposto:
Comparar fila FIFO e prioridade com a mesma carga, incluindo mudanças de prioridade. Medir espera por classe, tamanho físico versus itens vivos e custo de inserção/retirada. Escolher política considerando justiça e necessidade de atualização, além da complexidade algorítmica.

Comparações:
- T174 (complements): O escalonador determina quando e em qual recurso executar o item retirado.
- T166 (complements): Aging pode atualizar prioridade, exigindo uma política consistente de manutenção da estrutura.

Afirmação rastreável:
A PriorityQueue de asyncio retira a menor chave de prioridade primeiro.
Suporte: direct; fontes: V3C-S008
Limite: Estabilidade, atualização e persistência não são garantidas automaticamente por esse comportamento básico.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T149:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou heaps, desempate e atualização de prioridades. Aqui a fila distingue urgência, elegibilidade e custo previsto, evitando que um item prioritário bloqueado impeça trabalho realmente executável.

Elegibilidade antes da ordem
Mantenha dependências e disponibilidade de recurso fora da chave de prioridade. Um item urgente sem artefato de entrada não está pronto. Separar filas de aguardando e elegível evita retirar e reinserir continuamente o mesmo trabalho, reduzindo custo de coordenação e diagnósticos enganosos de saturação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V3C-S024.

Deadline não é duração
Ordenar pelo prazo pode ser adequado para urgência, mas duas tarefas com o mesmo prazo podem ter custos muito diferentes. Registre estimativa e margem de término; uma tarefa que já não cabe no prazo precisa de decisão explícita, e não de prioridade infinita que comprometa todas as demais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003.

Particionamento por chave de efeito
Quando vários itens alteram o mesmo recurso, selecione apenas um elegível por chave. Outras chaves podem avançar em paralelo. A exclusão deve sobreviver a falha do worker e distinguir entrega duplicada de uma nova intenção, preservando a ordem relevante para aquele recurso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, C-S026.

USO AVANÇADO — Fila de inferência compartilhada
Cenário: Pedidos curtos interativos convivem com relatórios longos.
Estratégia: Crie classes e estimativas de consumo, mantendo cotas mínimas para trabalho antigo. Antes de iniciar uma geração longa, confira capacidade e deadline; evite interrompê-la se o servidor não consegue recuperar estado de forma útil.
Papel do modelo pequeno: Modelos 3–30B recebem trabalhos admitidos; a fila não delega política de prioridade à LLM.
Aceite proposto: Proposta: medir latência por classe, taxa de conclusão e espera máxima observada em carga mista repetível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S003.

USO AVANÇADO — Aplicação de patches por repositório
Cenário: Vários agentes preparam alterações que podem compartilhar uma base.
Estratégia: Use chave de exclusão para integração, não para toda pesquisa. Revisões e testes independentes podem ocorrer antes; ao liberar integração, confira novamente a base e revalide o patch que ficou esperando.
Papel do modelo pequeno: 8–30B produz candidatos, enquanto código coordena ordem e conflitos.
Aceite proposto: Proposta: introduzir alterações concorrentes e verificar que nenhuma prioridade permite sobrescrever trabalho não incorporado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificação de tipo de trabalho e extração de prazo de campos confiáveis, sem inventar urgência.
8–14B: Proposta: estimar subtarefas e identificar dependências para a fila verificar.
15–30B: Proposta: preparar alternativas de execução quando o prazo original se tornar inviável.
Requisitos de treino/runtime: Exige relógio apropriado, persistência de leases e telemetria de duração; prioridade textual não é mecanismo de autorização.
Não aplicar quando: Não usar uma única ordem global quando diferentes recursos ou efeitos exigem exclusão e capacidade independentes.

## T149:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: Fila de prioridade seleciona mensagens por deadlines.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Timestone oferece caso operacional direto; Borg foi acessado apenas pelo abstract, sem atribuir-lhe algoritmos não verificados.
Consultas registradas: V4C-Q003, V4C-Q018.

## T149:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T149 → T174 [feeds]
Como combinar: Timestone combina seleção por deadline com restrições de trabalho não paralelizável.
Interface: Mensagem, deadline e chave de exclusão.
Condição: O trabalho tem identidade e critério de elegibilidade.
Aceite proposto: Proposta: verificar ordem e ausência de execução concorrente da mesma chave.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S003. Casos: V4C-C005.

2. T149 → T166 [complements]
Como combinar: Aging evita que prioridade fixa esconda espera indefinida.
Interface: Tempo de espera, classe e prioridade efetiva.
Condição: A política define como a espera modifica a ordem.
Aceite proposto: Comparar distribuição de espera por tenant, não somente média global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020, V3C-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não descartar silenciosamente itens que expiraram enquanto aguardavam.
- Impedir que workers criem prioridades novas para suas próprias tentativas sem política comum.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos e rotas sob a mesma política de fila. Melhoria de latência por scheduler não demonstra que o modelo menor resolveu tarefas mais difíceis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T166, T174

## Fontes primárias associadas

### C-S014 — heapq — Heap queue algorithm

[https://docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estruturas heap permitem filas por prioridade; política de equidade é responsabilidade adicional.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S008 — Python asyncio — Queues

[https://docs.python.org/3/library/asyncio-queue.html](https://docs.python.org/3/library/asyncio-queue.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas limitadas bloqueiam put; PriorityQueue usa menor prioridade primeiro; task_done e join acompanham tarefas pendentes.

Limite: API consultada inclui shutdown recente; a versão local não foi presumida e a fila não é persistente por si.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T150 — Request Coalescing / Singleflight

**Nome canônico:** Request Coalescing / Singleflight  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T150  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** coalescência de solicitações; singleflight

## T150:C01 — conceito

Coalescência faz solicitações concorrentes equivalentes compartilhar uma execução já em andamento. Singleflight é uma implementação conhecida desse padrão. Difere de cache persistente: o foco é evitar trabalho duplicado simultâneo, ainda que o resultado não seja guardado depois.

Como funciona:
- Derivar chave que identifica operação e entradas equivalentes.
- O primeiro solicitante inicia a execução; os demais aguardam o mesmo trabalho.
- Distribuir resultado ou erro e liberar a entrada em andamento.

## T150:C02 — aplicacao

Quando usar:
- Muitas consultas simultâneas ao mesmo recurso.
- Expiração de cache que provoca várias recomputações idênticas.

Quando não usar:
- Ações com intenção diferente, dados privados distintos ou respostas dependentes do solicitante.

Implementação proposta:
- Incluir tenant, autorização e versão relevante na chave.
- Definir cancelamento por assinante sem cancelar indevidamente os demais.
- Limitar tempo de vida e remover registros órfãos após falha.

Aplicação LAI proposta:
Proposta: coalescer carregamento de documentos e consultas repetidas de especialistas da Helena quando o contrato comprovar equivalência.

## T150:C03 — riscos_validacao

Armadilhas:
- Chave incompleta pode compartilhar resposta entre clientes.
- Uma execução lenta cria fila de espera para todos os solicitantes daquela chave.

Métricas sugeridas:
- Número de operações reais por solicitações equivalentes.
- Latência dos seguidores e economia de chamadas.

Testes propostos:
- Disparar várias leituras idênticas e exigir uma execução real em andamento.
- Repetir com tenants distintos e conferir que nunca compartilham resposta.

## T150:C04 — perguntas_proveniencia

Pergunta: Singleflight garante uma execução para sempre?
Resposta: Não. Suprime duplicatas concorrentes dentro do escopo implementado.

Pergunta: Substitui idempotência?
Resposta: Não. Uma nova tentativa futura ainda pode repetir efeito e precisa de proteção própria.

Pergunta: Coalescer erros equivale a cache negativo?
Resposta: Não. O erro é compartilhado entre aguardantes da chamada ativa; guardá-lo depois exige política adicional de expiração.

Pergunta: A chave pode ser só o nome do documento?
Resposta: Não se revisão, escopo ou parâmetros alterarem a leitura; a chave deve representar equivalência real do resultado.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T150:C05 — mecanismo_avancado

A equivalência de solicitações precisa incluir mais que o texto visível: versão do recurso, parâmetros efetivos, identidade de escopo e nível de consistência podem mudar o resultado. Singleflight distribui inclusive o mesmo erro aos aguardantes; se todos repetirem imediatamente, forma-se uma nova rajada. No código Go consultado, Forget libera futuras chamadas da espera pela execução anterior, sem cancelá-la; isso permite coexistência de trabalhos para a mesma chave.

Condição de contorno:
Coalescer operações com efeitos diferentes ou dados de escopos distintos viola a semântica, mesmo quando os argumentos aparentam igualdade.

Contrato proposto:
- Entradas: Chave de equivalência completa, função de leitura e deadline de cada interessado.
- Saídas: Resultado compartilhado, erro e indicação de participação na execução comum.
- Estado: Execução líder, aguardantes e ciclo de vida da chave.
- Invariante: Cancelar um aguardante não cancela implicitamente trabalho ainda necessário aos demais.

Compromissos de projeto:
- Compartilhar reduz trabalho repetido e acopla a latência dos aguardantes ao líder.
- Esquecer uma chave destrava novas tentativas e pode duplicar carga enquanto a chamada anterior termina.

## T150:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: cancelar um aguardante, manter outro e chamar Forget enquanto a operação está ativa; verificar separadamente resultado compartilhado e possibilidade de nova execução.

Plano de avaliação proposto:
Comparar sem coalescência e com coalescência sob rajadas de chaves populares e falhas. Medir execuções físicas por intenção de leitura, espera, erros compartilhados e memória retida. Separar efeitos de cache posterior e compartilhamento apenas em andamento.

Comparações:
- T157 (distinct_from): Hash de prefixo localiza estado de inferência; singleflight coordena uma execução ativa por chave.
- T162 (distinct_from): Idempotência limita efeito lógico; coalescência não a garante entre processos ou após término.

Afirmação rastreável:
A implementação Go documenta que Forget permite novas chamadas sem esperar pela chamada anterior.
Suporte: direct; fontes: V3C-S011
Limite: Essa semântica é da implementação inspecionada, não uma propriedade universal de todos os coalescedores.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T150:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou equivalência de chave e comportamento de Forget. A camada nova trata ciclo de vida dos aguardantes, publicação por versão e limites da coalescência em gerações probabilísticas.

Dono e consumidores distintos
Uma execução compartilhada tem uma identidade própria; cada consumidor mantém prazo e cancelamento independentes. A saída de um aguardante não deve cancelar a operação enquanto outros ainda precisam dela. Quando ninguém resta, a política pode cancelar o produtor, mas precisa confirmar o que já consumiu ou realizou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V4C-S022.

Publicação vinculada à versão
Se o recurso mudar durante a execução, o resultado antigo não deve preencher a chave da nova revisão. Registre versão observada e versão solicitada, publicando apenas no espaço correspondente. Invalidação de cache e fim do singleflight são eventos distintos: excluir uma entrada não interrompe necessariamente trabalho em andamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V3C-S037.

Probabilidade e privacidade
Duas inferências com o mesmo texto podem esperar diversidade ou contextos privados diferentes. Compartilhe somente quando contrato, fontes, identidade de escopo e política de amostragem permitirem o mesmo resultado. A redução de chamadas não justifica colapsar tentativas deliberadamente independentes usadas para avaliação ou busca de alternativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V3C-S017.

USO AVANÇADO — Busca documental após cache miss
Cenário: Muitos agentes solicitam o mesmo documento versionado.
Estratégia: Use uma busca compartilhada por documento, revisão e escopo. Distribua o resultado e seu estado aos aguardantes; erros recebem uma política comum de espera para impedir que todos reiniciem simultaneamente a chamada que acabou de falhar.
Papel do modelo pequeno: 3–7B consome trechos já recuperados; coalescência fica no cliente determinístico.
Aceite proposto: Proposta: medir chamadas à origem, espera por consumidor e contaminação entre versões durante rajadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S022, V3C-S011.

USO AVANÇADO — Inferência repetitiva de classificação
Cenário: Vários workflows pedem a mesma classificação sobre entrada imutável.
Estratégia: Fixe template, revisão do modelo e schema antes de compartilhar. Se a tarefa exige múltiplas amostras, inclua identidade da amostra e evite coalescência entre elas. Guarde a decisão de compartilhamento para auditar economias reais.
Papel do modelo pequeno: 3–14B pode atender classes fechadas; 15–30B não muda o requisito de equivalência.
Aceite proposto: Proposta: comparar resultado e custo com execução independente, incluindo cancelamento de parte dos consumidores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificador determinístico ou quase determinístico em domínio fechado, com revisão fixada.
8–14B: Proposta: extrações repetidas de fontes imutáveis sob contrato idêntico.
15–30B: Proposta: tarefas mais caras com evidência compartilhável, sem colapsar exploração de hipóteses diferentes.
Requisitos de treino/runtime: Requer gestão de aguardantes, timeout próprio e chave completa; singleflight local não coordena automaticamente réplicas.
Não aplicar quando: Não usar para ações de negócio distintas, inferência privada incompatível ou amostras que deveriam ser independentes.

## T150:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C022 — Cloudflare / CDN — request collapsing
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A documentação descreve cache lock para solicitações simultâneas do mesmo asset em um data center.
Mecanismo documentado: A primeira solicitação busca a origem; as demais aguardam e recebem a resposta compartilhada. O escopo é por localização, não exclusão global de todas as chamadas.
Correspondência com esta base: Há coalescência explícita de solicitações simultâneas por chave de asset.
Transferência proposta para modelo pequeno: Proposta: coalescer leitura idêntica de documentos ou inferência determinística com escopo e versões iguais, separando cancelamento de um consumidor do trabalho compartilhado.
Limite: Operational_product: documentação de comportamento do serviço sem deployment específico de cliente. Cache HTTP não demonstra equivalência de respostas probabilísticas de LLM.
Fontes: V4C-S022.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cloudflare documenta request collapsing como recurso; não foi promovido a caso identificado de cliente nem a prova de coalescência LLM em produção.
Consultas registradas: V4C-Q009, V4C-Q017.

## T150:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T150 → T137 [complements]
Como combinar: Uma execução compartilhada consome uma reserva de produtor, conservando custos de entrega aos consumidores.
Interface: Chave, participantes e reserva de execução.
Condição: Cancelar um consumidor não liquida a reserva de todos.
Aceite proposto: Testar entradas e saídas concorrentes sem saldo duplicado ou perdido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T150 → T171 [complements]
Como combinar: Coalescência protege misses enquanto cache reaproveita resultados ou cálculo já armazenado.
Interface: Estado ativo, resultado publicado e versão de cache.
Condição: As políticas de expiração são separadas.
Aceite proposto: Alterar recurso durante a chamada e impedir publicação na revisão errada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S022, V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Diferenciar entrega duplicada de intenção nova que tem parâmetros iguais.
- Não apresentar uma exclusão local por chave como garantia distribuída de exatamente uma vez.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare redução de chamadas e equivalência de resultado em tarefas fixas, contra modelos locais e fronteira. A técnica economiza execução repetida, sem melhorar competência do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T007, T162

## Fontes primárias associadas

### C-S015 — singleflight package

[https://pkg.go.dev/golang.org/x/sync/singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas simultâneas de mesma chave compartilham a execução em andamento e seu resultado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S011 — golang/sync — singleflight implementation

[https://github.com/golang/sync/blob/master/singleflight/singleflight.go](https://github.com/golang/sync/blob/master/singleflight/singleflight.go)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro de chamadas em curso por chave; Forget permite nova chamada sem aguardar a chamada anterior.

Limite: Branch master pode mudar; semântica inspecionada não constitui cache durável ou deduplicação de efeitos entre processos.

### V4C-S022 — Default Cache Behavior — Request collapsing

[https://developers.cloudflare.com/cache/concepts/default-cache-behavior/](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache lock colapsa requisições simultâneas pelo mesmo asset em um data center e distribui a resposta aos aguardantes.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S017 — Transformers — Utilities for generation

[https://huggingface.co/docs/transformers/internal/generation_utils](https://huggingface.co/docs/transformers/internal/generation_utils)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TemperatureLogitsWarper e filtros top-k/top-p transformam logits e distribuição de amostragem.

Limite: Parâmetros e ordem de aplicação variam por backend; não garantem factualidade ou determinismo entre ambientes.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T151 — Lazy Loading de ferramentas

**Nome canônico:** Lazy Loading de Ferramentas  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T151  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** carregamento tardio de ferramentas; Lazy Loading de Ferramentas

## T151:C01 — conceito

Carregamento do contrato completo de uma ferramenta apenas quando sua capacidade é necessária. Um catálogo inicial pequeno orienta descoberta; depois o runtime entrega o schema selecionado. O mecanismo reduz contexto de definições, mas depende de descrições que permitam encontrar a ferramenta correta.

Como funciona:
- Expor metadados mínimos de capacidades ou uma ferramenta de descoberta.
- Selecionar candidatas de acordo com a tarefa e permissões.
- Carregar schemas completos, conferir versão e então permitir a chamada.

## T151:C02 — aplicacao

Quando usar:
- Catálogo grande com baixa fração utilizada por missão.
- Ferramentas especializadas com schemas extensos.

Quando não usar:
- Poucas ferramentas pequenas cujo carregamento completo já tem custo desprezível.

Implementação proposta:
- Escrever descrições com finalidade, entradas e situações de uso.
- Versionar descoberta e schema para evitar mudança entre seleção e execução.
- Medir custo total incluindo chamadas extras de busca.

Aplicação LAI proposta:
Proposta: a Helena carregar por domínio os contratos efetivamente usados, mantendo ferramentas essenciais de descoberta e estado sempre disponíveis.

## T151:C03 — riscos_validacao

Armadilhas:
- O agente não pode usar uma capacidade que não consegue descobrir.
- Schema carregado tardiamente pode exceder orçamento reservado ou invalidar o plano.

Métricas sugeridas:
- Tokens de definições carregados por missão.
- Recall da descoberta e acerto da ferramenta escolhida.

Testes propostos:
- Dar uma tarefa cujo instrumento não aparece no catálogo inicial e testar descoberta.
- Remover permissão após descoberta e exigir bloqueio no momento da execução.

## T151:C04 — perguntas_proveniencia

Pergunta: Lazy loading elimina o registro de ferramentas?
Resposta: Não. Precisa de metadados confiáveis para localizar o contrato.

Pergunta: O ganho é gratuito?
Resposta: Não. Descoberta acrescenta latência e pode errar; precisa de medição.

Pergunta: Uma notificação de mudança elimina a necessidade de versionamento?
Resposta: Não. Ela informa que algo mudou; ainda é necessário identificar o contrato efetivamente usado pela chamada.

Pergunta: Quando o carregamento tardio piora a tarefa?
Resposta: Quando descoberta repetida e definições omitidas causam mais rodadas ou erros que a economia inicial de tokens.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T151:C05 — mecanismo_avancado

O carregamento tardio precisa fechar a corrida entre descoberta e execução. O catálogo pode indicar uma versão cujo schema mudou antes da chamada. Uma proposta é carregar um descritor identificado, validar argumentos contra essa revisão e confirmar compatibilidade ao executar. O catálogo mínimo também deve expor informação suficiente para distinguir ferramentas com nomes próximos; reduzir descrições indiscriminadamente aumenta falsas seleções.

Condição de contorno:
Quando a tarefa depende de muitas ferramentas em cada rodada, a economia inicial pode ser consumida por sucessivas buscas e carregamentos.

Contrato proposto:
- Entradas: Intenção, catálogo leve, revisão conhecida e orçamento para descoberta.
- Saídas: Definição completa selecionada ou dependência ausente identificada.
- Estado: Ferramentas descobertas, carregadas, invalidadas e versões utilizadas.
- Invariante: Uma chamada usa o contrato carregado e não uma descrição desatualizada presumida.

Compromissos de projeto:
- Catálogo curto poupa contexto e reduz informação para seleção.
- Fixar revisão melhora reprodutibilidade e exige lidar com ferramentas retiradas ou incompatíveis.

## T151:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o tipo de um argumento após a descoberta e antes da execução; o carregador deve detectar incompatibilidade ou atualizar o contrato antes de enviar a operação.

Plano de avaliação proposto:
Comparar todas as definições no prompt, seleção fixa e carregamento sob demanda em tarefas com catálogos crescentes. Medir tokens totais, rodadas de descoberta, seleção incorreta e latência; decidir pela curva completa, incluindo falhas de descoberta.

Comparações:
- T158 (complements): O registro fornece identidade, metadados e sinal de alteração do catálogo.
- T045 (distinct_from): Recuperação escolhe candidatos; carregamento disponibiliza o contrato necessário para utilizá-los.

Afirmação rastreável:
MCP oferece notificação de alteração da lista de ferramentas quando a capacidade correspondente é declarada.
Suporte: direct; fontes: V3C-S004
Limite: A notificação não torna toda leitura e chamada uma transação atômica de catálogo.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T151:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou a corrida entre descoberta e execução. O aprofundamento define descoberta progressiva com orçamento, apresentação de contratos mínimos e invalidação de descrições que mudam a seleção.

Escada de detalhe
Comece com nomes de domínio e capacidades, depois carregue descrição curta e só então schema completo. Cada nível deve conter o suficiente para decidir se vale aprofundar. Um índice excessivamente resumido perde distinções essenciais; um schema inteiro para cada candidato elimina a economia que motivou o carregamento tardio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Busca terminável
Defina quando a descoberta termina: ferramenta compatível, ausência confirmada no catálogo consultado ou orçamento esgotado. Repetir buscas com sinônimos não deve esconder a mesma lista de resultados. Guarde candidatos já examinados e razões de rejeição, permitindo reabrir um candidato apenas se o catálogo ou o objetivo mudou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, C-S030.

Contrato carregado não vira memória eterna
Descritores podem expirar ou ser revogados. A sessão deve conservar a versão utilizada para explicar decisões, mas consultar habilitação atual antes da execução. Separar histórico de disponibilidade impede que uma ferramenta removida continue operando apenas porque sua definição ficou no contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S004.

USO AVANÇADO — Agente com milhares de ferramentas
Cenário: Uma consulta local demanda poucas operações de um catálogo amplo.
Estratégia: Resolva servidor por intenção, liste ferramentas relevantes, carregue schema do candidato e valide argumentos. Se a chamada falhar por revisão incompatível, atualize o descritor uma vez e reavalie; não transforme erro permanente em busca infinita.
Papel do modelo pequeno: 3–7B pode selecionar entre poucos candidatos; 8–14B compõe argumentos curtos.
Aceite proposto: Proposta: medir tokens de catálogo, escolha correta e custo total de descoberta em ferramentas desconhecidas do treino.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Sessões de programação frequentes
Cenário: A maioria das tarefas usa apenas arquivos e testes, mas há integrações externas disponíveis.
Estratégia: Mantenha ferramentas básicas no início e resolva integrações específicas quando uma lacuna real surgir. Execute polling mecânico em código e devolva resumo, evitando carregar schemas e resultados intermediários em todos os turnos.
Papel do modelo pequeno: 8–30B mantém o objetivo; um wrapper determinístico resolve protocolos e espera.
Aceite proposto: Proposta: comparar custo e conclusão com carregamento integral, incluindo tarefas que exigem a integração rara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: descoberta em duas ou três etapas com conjuntos pequenos e critérios explícitos de abstenção.
8–14B: Proposta: composição de contratos locais e seleção de campos de resposta.
15–30B: Proposta: descoberta entre domínios com estado persistido dos candidatos e orçamento de investigação.
Requisitos de treino/runtime: Exige registro pesquisável, descrições úteis e cache de schemas versionado; menor prompt não garante melhor seleção.
Não aplicar quando: Não usar quando a ferramenta é sempre necessária e o custo de buscá-la supera a economia de contexto.

## T151:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Schemas são obtidos progressivamente em vez de carregar o catálogo inteiro.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Omni MCP e harnesses Uber comprovam descoberta gradual; as bandas e políticas de orçamento são propostas locais.
Consultas registradas: V4C-Q009.

## T151:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T151 → T158 [complements]
Como combinar: No Omni MCP, a descoberta resolve ferramentas presentes no registro antes da invocação.
Interface: IDs de servidor e ferramenta, schema e estado de habilitação.
Condição: O plano de controle conhece a revisão executável.
Aceite proposto: Proposta: retirar ferramenta do catálogo ativo e conferir rejeição apesar do descritor antigo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

2. T151 → T214 [complements]
Como combinar: Depois de carregar o contrato, selecione campos de resposta necessários à próxima decisão.
Interface: Schema de saída e projeção de campos.
Condição: Campos omitidos podem ser recuperados se a tarefa mudar.
Aceite proposto: Comparar erros por omissão com economia total de tokens.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir ferramenta descoberta com ferramenta habilitada para aquele chamador.
- Evitar que descrições geradas automaticamente mudem sem revisão e rastreabilidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare escolha de ferramentas entre 3–30B e fronteira com catálogos idênticos. A descoberta reduz distração e custo, mas não prova capacidade equivalente de executar qualquer ferramenta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T045, T158, T170

## Fontes primárias associadas

### C-S016 — Introducing advanced tool use on the Claude Developer Platform

[https://www.anthropic.com/research/advanced-tool-use](https://www.anthropic.com/research/advanced-tool-use)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas sob demanda evita inserir antecipadamente todos os schemas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T152 — Token Budget Allocation

**Nome canônico:** Token Budget Allocation  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T152  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** alocação de orçamento de tokens

## T152:C01 — conceito

Distribuição do orçamento de tokens entre instruções, ferramentas, estado, evidências, histórico e saída. É uma política de engenharia de contexto. A soma deve respeitar o limite efetivo do backend, incluindo template e tokens especiais; contagem por caracteres é apenas estimativa.

Como funciona:
- Contabilizar entrada com tokenizer e template do modelo de destino.
- Reservar espaço de saída antes de preencher o contexto recuperado.
- Selecionar evidências dentro do saldo, preservando conteúdo obrigatório.

## T152:C02 — aplicacao

Quando usar:
- RAG com muitos trechos candidatos.
- Agentes cujo histórico e schemas crescem durante a missão.

Quando não usar:
- Remover restrições essenciais só para caber mais texto de baixa utilidade.

Implementação proposta:
- Definir regiões obrigatórias e prioridades das opcionais.
- Registrar tokens previstos e reportados pelo backend para corrigir estimativas.
- Tratar separadamente limites de contexto, custo e saída máxima.

Aplicação LAI proposta:
Proposta: a Helena reservar instruções e estado antes de distribuir espaço entre fontes; o orçamento proposto deve ser calibrado no modelo realmente servido.

## T152:C03 — riscos_validacao

Armadilhas:
- Tokenizer diferente altera a contagem real.
- Uma ferramenta pode retornar volume inesperado e estourar a reserva.

Métricas sugeridas:
- Taxa de overflow e diferença entre contagem prevista e efetiva.
- Recall das evidências necessárias por token de entrada.

Testes propostos:
- Montar prompt próximo ao limite e conferir contagem após aplicar template.
- Injetar resultado de ferramenta grande e exigir recorte com referência ao original.

## T152:C04 — perguntas_proveniencia

Pergunta: Uma janela de 32 mil permite 32 mil tokens de entrada?
Resposta: Depende do backend e da reserva de saída; não se deve assumir.

Pergunta: Reduzir tokens sempre melhora?
Resposta: Não. Pode remover evidência crítica e aumentar erros.

Pergunta: Tokens de prefixo em cache deixam de ocupar contexto?
Resposta: Não necessariamente. Reutilização computacional e capacidade lógica da janela são dimensões distintas.

Pergunta: Por que reservar espaço para ferramentas futuras?
Resposta: Porque a chamada pode caber e seu resultado não; sem plano de ingestão, a observação necessária pode ser perdida.

Escopo das fontes:
A documentação de tokenização sustenta a contagem; regiões, prioridades e critérios de seleção são proposta editorial de controle de contexto.

## T152:C05 — mecanismo_avancado

O orçamento deve distinguir ocupação da janela e consumo acumulado da missão. Um prefixo reutilizado pode continuar ocupando contexto mesmo quando seu custo computacional ou faturado diminui. Resultados de ferramentas ainda não recebidos precisam de reserva ou estratégia de truncamento controlado. A contagem antecipada inclui template, definições de ferramentas e multimodalidade, e continua sujeita às particularidades do backend.

Condição de contorno:
Uma soma baseada apenas nos textos visíveis não protege o limite quando mensagens estruturadas acrescentam tokens ou quando a resposta esperada cresce.

Contrato proposto:
- Entradas: Capacidade do modelo, entrada montada, reservas de saída e resultados esperados.
- Saídas: Cotas por bloco, margem disponível e decisão de redução ou divisão.
- Estado: Estimativa inicial, consumo observado, reservas e orçamento acumulado.
- Invariante: Economia por cache não é tratada automaticamente como aumento da janela física.

Compromissos de projeto:
- Reservas generosas evitam estouro e podem excluir evidência útil.
- Redistribuição dinâmica usa melhor a janela e exige recontagem após mudanças relevantes.

## T152:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma ferramenta com schema longo e receber resultado maior que o previsto; exigir recontagem e política explícita de preservação dos dados necessários.

Plano de avaliação proposto:
Comparar cotas fixas e reservas adaptadas ao histórico de tamanho das ferramentas. Fixar tarefas e modelos. Medir estouro, qualidade de evidência, tokens descartados e custo acumulado. Ajustar a margem à variabilidade observada sem percentual universal.

Comparações:
- T168 (complements): Limites suave e rígido definem ações quando o orçamento se aproxima das fronteiras.
- T176 (complements): O plano estima demandas futuras que precisam de reserva.

Afirmação rastreável:
A contagem de tokens da Anthropic aceita mensagens estruturadas, ferramentas e entradas multimodais.
Suporte: direct; fontes: V3C-S022
Limite: O endpoint fornece estimativa específica do fornecedor e não conta por si todo o custo futuro da missão.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T152:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou janela, gasto acumulado e reservas para ferramentas. A camada nova atribui utilidade a segmentos de contexto e vincula redução de tokens à preservação de obrigações verificáveis.

Orçamento por função documental
Reserve espaço para objetivo vigente, restrições, fatos, incertezas e saída. Cada segmento tem uma política de redução: logs podem virar referências, mas critérios de aceite não devem desaparecer por serem antigos. Distribuição fixa pode servir de baseline; adaptação só deve ocorrer com métricas de perda e custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S022.

Custo de ida e volta
Uma economia local pode gerar consultas adicionais depois. Remover detalhe de uma ferramenta reduz a entrada atual, mas pode exigir releitura ou induzir erro. Meça tokens e tempo até a tarefa aceita, incluindo resumos, buscas e reparos, para evitar otimizar um contador enquanto piora o fluxo completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S013.

Reserva por etapa e tokenizer
Um plano com modelos diferentes não compartilha necessariamente a mesma contagem. Reconstrua o pacote no template do destino e reserve espaço para validação e resposta final. O custo faturado do prefixo e sua ocupação da janela continuam sendo medidas distintas, especialmente quando cache e compactação se combinam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S022, V4C-S018.

USO AVANÇADO — Análise de repositório em janela curta
Cenário: O agente precisa alterar uma função sem carregar o projeto inteiro.
Estratégia: Inclua contrato, trecho alvo, chamadas relevantes e teste que define o comportamento. Use mapa para solicitar detalhes por necessidade; se a alteração afetar uma dependência, transfira parte do orçamento exploratório para essa evidência, preservando critérios de aceite.
Papel do modelo pequeno: 3–7B executa mudanças muito locais; 8–30B amplia escopo apenas com evidências recuperadas.
Aceite proposto: Proposta: medir regressões, leituras adicionais e tokens totais contra contexto amplo uniforme.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V2A-S007.

USO AVANÇADO — Pesquisa com muitas respostas de ferramenta
Cenário: Cada consulta retorna texto e metadados volumosos.
Estratégia: Projete campos, mantenha referências e extraia somente fatos que respondem aos critérios. Antes de sintetizar, verifique cobertura; se uma lacuna depender de material omitido, recupere-o especificamente em vez de aumentar toda a janela.
Papel do modelo pequeno: 8–14B estrutura evidências; 15–30B integra conclusões condicionais.
Aceite proposto: Proposta: comparar sustentação, completude e custo incluindo recuperação posterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: orçamento focado em fatos diretamente usados na próxima operação, com respostas curtas.
8–14B: Proposta: múltiplos segmentos documentais pequenos e reconsulta orientada por lacuna.
15–30B: Proposta: integração de evidências mais extensa, reservando verificação e conclusão desde o início.
Requisitos de treino/runtime: Contar com tokenizer e template reais; registrar consumo observado por etapa, não apenas estimativa prévia.
Não aplicar quando: Não reduzir contexto quando detalhes aparentemente acessórios determinam exceções ou identidade do recurso.

## T152:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber documenta otimizações por sessão e NVIDIA controles específicos; nenhum limiar corporativo é recomendado automaticamente para 3–30B.
Consultas registradas: V4C-Q009, V4C-Q014.

## T152:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T152 → T222 [feeds]
Como combinar: O monitor informa ocupação e erro de previsão para ajustar reservas futuras.
Interface: Contagem real, estimativa, segmento e revisão do template.
Condição: As unidades são comparáveis dentro do mesmo backend.
Aceite proposto: Detectar mudança de tokenizer por desvio sistemático de contagem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T152 → T214 [complements]
Como combinar: Poda por campos implementa parte da redução planejada sem reescrever todos os dados.
Interface: Lista de campos necessários e referência ao payload integral.
Condição: O contrato preserva informação de controle e incerteza.
Aceite proposto: Reexecutar casos com campo decisivo fora da projeção inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não gastar a reserva de verificação para produzir mais deliberação ou candidatos.
- Manter separados tokenização real, caracteres e preços do provedor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos com orçamento total e critérios iguais, incluindo releituras. Um modelo pequeno bem contextualizado pode resolver tarefas delimitadas sem equivalência geral de janela ou conhecimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T168, T176

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T153 — Output Streaming com interrupção

**Nome canônico:** Output Streaming com Interrupção  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T153  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** streaming cancelável; Output Streaming com Interrupção

## T153:C01 — conceito

Entrega incremental da resposta com possibilidade de interromper seu processamento. Diminui tempo até o primeiro conteúdo visível, mas não necessariamente o tempo total. Parar a interface, fechar a conexão e cancelar a geração no servidor são eventos diferentes e precisam ser conectados explicitamente.

Como funciona:
- Receber fragmentos identificados da resposta em andamento.
- Exibir conteúdo parcial preservando distinção entre trecho e mensagem concluída.
- Propagar cancelamento ao backend e registrar o estado final efetivamente observado.

## T153:C02 — aplicacao

Quando usar:
- Interface interativa que beneficia de resposta progressiva.
- Usuário pode corrigir objetivo antes do término da geração.

Quando não usar:
- Consumidor exige objeto completo e validado antes de qualquer uso ou efeito.

Implementação proposta:
- Implementar evento de início, fragmento, erro e término.
- Usar identificador de geração para evitar mistura após reconexão.
- Não executar comando parcial nem tratar JSON incompleto como decisão válida.

Aplicação LAI proposta:
Proposta: permitir interromper respostas da Helena sem perder estado da missão nem confirmar ações cujo resultado ainda não chegou.

## T153:C03 — riscos_validacao

Armadilhas:
- Conteúdo já exibido não pode ser desexibido por garantia técnica.
- Cancelamento local pode deixar geração consumindo recursos no servidor.

Métricas sugeridas:
- Tempo até primeiro fragmento e até término.
- Tokens gerados após pedido de interrupção e frequência de streams incompletos.

Testes propostos:
- Interromper em diferentes momentos e verificar fechamento consistente da sessão.
- Simular perda de conexão e exigir estado incompleto, sem declaração de sucesso.

## T153:C04 — perguntas_proveniencia

Pergunta: Fechar SSE garante cancelamento da LLM?
Resposta: Não. O contrato do servidor precisa oferecer e executar esse cancelamento.

Pergunta: Streaming reduz custo automaticamente?
Resposta: Não. Só pode economizar geração se ela realmente parar antes.

Pergunta: Fechar a aba prova que a geração foi cancelada?
Resposta: Não. O sinal pode não chegar ao backend; confirmação ou observabilidade do servidor é necessária para afirmar isso.

Pergunta: Posso aproveitar texto parcial após interrupção?
Resposta: Sim, se for identificado como parcial e não usado como estrutura completa ou confirmação de uma ação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T153:C05 — mecanismo_avancado

Interromper uma resposta incremental exige tratar a corrida entre último fragmento, fechamento e confirmação do cancelamento. A interface pode parar de exibir dados antes de o servidor liberar a geração. Fragmentos já recebidos também podem terminar no meio de UTF-8, de uma estrutura JSON ou de um argumento de ferramenta; a reconstrução deve usar o protocolo de framing e não presumir que cada pacote seja uma unidade semântica.

Condição de contorno:
Se o backend não oferece cancelamento verificável, o cliente pode interromper consumo sem comprovar economia imediata de computação.

Contrato proposto:
- Entradas: Stream identificado, eventos ordenados e sinal de interrupção.
- Saídas: Conteúdo confirmado, estado parcial e confirmação ou incerteza de cancelamento.
- Estado: Última sequência recebida, buffers e estado de fechamento.
- Invariante: Fragmento parcial não é promovido a ação executável sem validação completa.

Compromissos de projeto:
- Exibir cedo melhora percepção de resposta e expõe conteúdo ainda passível de revisão.
- Bufferizar até unidade válida aumenta atraso inicial e facilita consumidores estruturados.

## T153:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper durante um argumento JSON e fazer o evento final chegar após o pedido de cancelamento; exigir classificação consistente e ausência de execução do argumento incompleto.

Plano de avaliação proposto:
Comparar entrega integral e streaming sob interrupções em vários pontos. Medir tempo até conteúdo útil, trabalho após cancelamento e consistência da saída parcial. Distinguir economia observada do servidor e simples redução de exibição.

Comparações:
- T172 (complements): O controlador administra buffers, framing e estados do stream.
- T089 (distinct_from): Término por EOS ou limite é decisão de geração; interrupção do consumidor é outro evento.

Afirmação rastreável:
MCP documenta que notificações de cancelamento podem chegar após a conclusão da requisição.
Suporte: related; fontes: V3C-S005
Limite: A mesma corrida orienta o projeto de streaming, mas o transporte e a geração podem ter contratos adicionais.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T153:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu framing e corrida de cancelamento. Agora a transmissão distingue conteúdo provisório, eventos confirmados e mensagens de encerramento, preservando integridade quando o usuário interrompe uma tarefa longa.

Provisório não é confirmado
A interface pode exibir texto incremental sem permitir que outros componentes o tratem como resposta final. Use estados explícitos para rascunho, concluído e interrompido. Em objetos estruturados, só publique campos acionáveis quando o protocolo e a validação permitirem, sem executar argumentos ainda incompletos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V3C-S004.

Cancelamento em árvore
Interromper o stream deve alcançar produtor, ferramentas e subagentes conforme suas possibilidades. Cada filho devolve se parou, terminou ou possui resultado desconhecido. O controlador agrega esses estados; fechar a conexão do usuário não é prova de que a GPU, a consulta ou a operação externa foram encerradas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S005, V3C-S007.

Reutilização após interrupção
Resultados confirmados de leituras podem ser guardados para continuar depois, enquanto uma resposta parcial fica marcada como incompleta. A próxima sessão precisa receber objetivo e estado de cada operação, não apenas o último texto exibido. Assim, interromper para mudar de ideia não exige perder todo trabalho útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S030.

USO AVANÇADO — Pesquisa que o usuário redefine
Cenário: Durante a coleta, o usuário reduz o escopo da pergunta.
Estratégia: Pare novas buscas, cancele ramos desnecessários e preserve evidências dos restantes. Emita uma revisão do objetivo e monte uma nova entrega com o que continua válido. Não misture o final da resposta antiga ao início da nova.
Papel do modelo pequeno: 3–7B extrai fatos por ramo; 15–30B reavalia relevância sob o objetivo atualizado.
Aceite proposto: Proposta: medir chamadas evitadas, evidências reutilizadas e fragmentos indevidamente atribuídos à nova resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

USO AVANÇADO — Geração de patch cancelada
Cenário: A saída estava formando uma alteração quando a sessão foi interrompida.
Estratégia: Guarde o candidato como incompleto, sem aplicá-lo automaticamente. Se a edição já ocorreu por ferramenta, registre revisão e efeitos confirmados. A continuação decide entre validar, completar ou descartar, sempre contra a base atual.
Papel do modelo pequeno: 8–30B reconstrói a intenção; código distingue texto parcial de arquivo realmente alterado.
Aceite proposto: Proposta: interromper em vários pontos e exigir ausência de publicação de patch não validado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S030, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: respostas curtas com estados simples de conclusão e nenhum efeito disparado por fragmento.
8–14B: Proposta: transmissão de etapas de ferramenta com recibos separados do texto explicativo.
15–30B: Proposta: coordenação de streams de pesquisa ou edição mantendo cancelamento por ramo.
Requisitos de treino/runtime: Confirmar suporte de streaming e parser do modelo; alguns contratos de ferramentas exigem resposta completa.
Não aplicar quando: Não depender de cancelamento para desfazer um efeito externo ou recuperar memória de GPU imediatamente.

## T153:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn documenta experiência incremental; protocolos de cancelamento vêm de especificações. Não se inventou deployment que conecte todos esses detalhes.
Consultas registradas: V4C-Q010, V4C-Q013.

## T153:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T153 → T172 [feeds]
Como combinar: O controlador interpreta frames, aplica backpressure e preserva o estado terminal.
Interface: ID do stream, sequência e evento de término ou interrupção.
Condição: O consumidor reconhece revisões e duplicatas.
Aceite proposto: Injetar desconexão e impedir conclusão falsa por último fragmento recebido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T153 → T243 [complements]
Como combinar: Operações já enviadas durante o stream precisam de reconciliação separada.
Interface: Intenção, tentativa e status observado pelo destino.
Condição: O efeito pode sobreviver à conexão encerrada.
Aceite proposto: Cancelar após envio e confirmar que não há repetição cega.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar um botão de parar como confirmação do servidor.
- Liquidar custos e reservas somente conforme o estado observado das operações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare responsividade e integridade sob cancelamento em modelos pequenos e fronteira. Percepção de rapidez não equivale a menor tempo de conclusão validada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T089, T172

## Fontes primárias associadas

### C-S018 — HTML Standard — Server-sent events

[https://html.spec.whatwg.org/multipage/server-sent-events.html](https://html.spec.whatwg.org/multipage/server-sent-events.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Eventos incrementais, identificação e reconexão SSE; cancelamento de inferência depende do servidor, não da norma SSE.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V3C-S019 — WHATWG Streams Standard

[https://streams.spec.whatwg.org/](https://streams.spec.whatwg.org/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas, estratégias de tamanho, high-water marks, backpressure, cancelamento e propagação por pipelines.

Limite: É o modelo de streams da Web; transporte, backend de geração e durabilidade precisam de contratos adicionais.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S030 — Claude Code — Checkpointing

[https://code.claude.com/docs/en/checkpointing](https://code.claude.com/docs/en/checkpointing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing distingue restauração de código, conversa e sumarização; escopo de arquivos e retenção são limitados.

Limite: Documentação consultada em 2026-11-05; não extrapolar cobertura para estado externo, todas as ferramentas ou outras versões.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T154 — Multi-Turn Conversation Management

**Nome canônico:** Multi-Turn Conversation Management  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T154  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gerenciamento de conversas multiturno

## T154:C01 — conceito

Gerenciamento da continuidade entre turnos: identidade da sessão, histórico, chamadas de ferramentas, objetivos, fatos vigentes e limites de contexto. A conversa exibida é apenas uma projeção; o sistema precisa manter estado consistente mesmo quando resume ou deixa mensagens antigas fora do prompt.

Como funciona:
- Associar mensagem a usuário, tenant, thread e ordem correta.
- Atualizar estado e referências de ferramentas de forma persistente.
- Montar próximo contexto com histórico selecionado e decisões ainda vigentes.

## T154:C02 — aplicacao

Quando usar:
- Assistentes que retomam tarefas ao longo de várias sessões.
- Fluxos com correções de instruções e ferramentas pendentes.

Quando não usar:
- Concatenar todo o histórico sem tratar limite, conflito temporal ou isolamento.

Implementação proposta:
- Guardar eventos originais e projeção compacta separadamente.
- Serializar mutações por thread ou usar controle otimista de versão.
- Tratar mensagem nova durante execução como evento que pode alterar objetivo ou cancelar etapa.

Aplicação LAI proposta:
Proposta: a Helena usar estado versionado por missão e memória externa recuperável, preservando a decisão atual de Leandro.

## T154:C03 — riscos_validacao

Armadilhas:
- Resumo pode preservar decisão antiga já revogada.
- Threads concorrentes podem sobrescrever o mesmo estado ou misturar clientes.

Métricas sugeridas:
- Retenção de restrições após muitos turnos.
- Conflitos de estado, respostas a objetivo antigo e erros de associação de ferramenta.

Testes propostos:
- Corrigir uma decisão e verificar que o próximo turno usa a versão vigente.
- Reiniciar o processo e retomar com resultados de ferramentas corretamente vinculados.

## T154:C04 — perguntas_proveniencia

Pergunta: Histórico completo é memória suficiente?
Resposta: Não. Precisa de identificação, atualidade e recuperação correta.

Pergunta: Checkpoint em RAM é durável?
Resposta: Não após queda do processo; é necessário backend persistente.

Pergunta: Uma nova tentativa deve criar nova mensagem lógica?
Resposta: Depende do contrato. Duplicata de entrega deve manter identidade; regeneração intencional pode criar versão ou ramo distinto.

Pergunta: Como explicar uma resposta baseada em decisão antiga?
Resposta: Registrar a revisão de entrada permite identificar desatualização e decidir se a resposta precisa ser refeita.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T154:C05 — mecanismo_avancado

Uma conversa com turnos concorrentes precisa definir qual revisão de estado cada turno leu. Sem essa relação, duas respostas podem atualizar objetivos e histórico em ordens incompatíveis. Um modelo de append com IDs de mensagem preserva eventos, mas decisões vigentes podem exigir controle de versão separado. Editar ou refazer um turno também cria uma ramificação lógica: não se deve misturar automaticamente respostas produzidas a partir de passados diferentes.

Condição de contorno:
Um identificador de sessão isolado não resolve concorrência, duplicatas de transporte ou regenerações de mensagens.

Contrato proposto:
- Entradas: Sessão, ID do turno, revisão de origem e novas observações.
- Saídas: Resposta vinculada à revisão e atualização confirmada ou conflito explícito.
- Estado: Histórico de eventos, versão ativa, chamadas pendentes e ramificações.
- Invariante: Uma resposta mantém vínculo com o estado usado para produzi-la.

Compromissos de projeto:
- Serializar turnos simplifica consistência e acrescenta espera.
- Permitir concorrência reduz latência e exige merge ou rejeição de atualizações incompatíveis.

## T154:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar dois turnos sobre a mesma versão e fazer o segundo concluir primeiro; verificar ordem de aplicação ou conflito conforme a política, preservando ambos os eventos.

Plano de avaliação proposto:
Comparar fila por sessão e concorrência com controle otimista em conversas com mudanças de objetivo. Medir conflitos, atualizações perdidas, latência e reconstrução histórica. Definir o contrato antes de otimizar paralelismo.

Comparações:
- T060 (complements): Checkpoints persistem o estado por sessão, mas não definem sozinhos como aceitar turnos simultâneos.
- T207 (complements): Um fluxo de eventos pode registrar mensagens e revisões sem apagar o passado.

Afirmação rastreável:
LangGraph persiste estado por thread por meio de checkpointers e diferencia esse escopo dos stores compartilhados.
Suporte: direct; fontes: A-S022
Limite: Políticas de edição, concorrência e ramificação da conversa são propostas do aplicativo.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T154:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou revisões concorrentes e ramificações de histórico. A camada nova trata conversa como entrada de um sistema de tarefas, com objetivo vigente, mensagens deduplicadas e comunicação entre sessões.

Mensagem e tarefa têm ciclos diferentes
Uma mensagem pode iniciar várias tarefas e uma tarefa pode sobreviver a muitos turnos. Dê identidades separadas a ambas. O estado operacional informa o que está em andamento; a conversa explica decisões e preferências, evitando que um novo turno apague inadvertidamente tarefas ainda válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

Revisão de objetivo
Quando o usuário corrige uma instrução, registre quais tarefas e artefatos ela invalida. Resultados independentes podem ser conservados; efeitos já realizados exigem reconciliação ou compensação de domínio. O modelo não deve simplesmente reescrever a narrativa como se a intenção anterior nunca tivesse sido executada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, C-S026.

Sincronização por eventos
Eventos de progresso precisam ser associados à revisão de objetivo que os gerou. Uma interface pode receber conclusão antiga depois de uma correção nova; o controlador deve classificá-la como resultado histórico, pendente ou ainda relevante. Mostrar uma lista concatenada de mensagens não resolve essa interpretação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S028.

USO AVANÇADO — Missão de programação atravessando sessões
Cenário: O agente prepara uma alteração, pausa e depois recebe um requisito adicional.
Estratégia: Releia o objetivo e a revisão do repositório, compare com o último pacote de trabalho e invalide testes afetados. Continue apenas as subtarefas que permanecem válidos; mudanças de escopo entram como nova versão, com motivo.
Papel do modelo pequeno: 8–14B realiza retomada local; 15–30B avalia impacto entre módulos.
Aceite proposto: Proposta: medir requisitos perdidos e trabalho indevidamente reutilizado em cenários com correções e edição concorrente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S037.

USO AVANÇADO — Assistente com trabalho em background
Cenário: Uma consulta longa continua enquanto o usuário inicia outra interação.
Estratégia: Use mailbox ou fila por instância, deduplique mensagens e preserve prioridade das correções. Atualizações de tarefas não devem bloquear leitura de novos pedidos nem assumir que todo pedido novo cancela o anterior.
Papel do modelo pequeno: 3–7B classifica eventos; 8–30B interpreta mudanças dentro de contratos conhecidos.
Aceite proposto: Proposta: permutar entregas e confirmar objetivo vigente, tarefas ativas e respostas atribuídas às solicitações corretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: atualizar campos simples de estado a partir de mensagens estruturadas, com confirmação de ambiguidades.
8–14B: Proposta: continuar tarefas locais com resumo fiel, artefatos e histórico de requisitos.
15–30B: Proposta: coordenar objetivos e resultados paralelos, sem usar a janela como único armazenamento.
Requisitos de treino/runtime: Exige persistência, identificação de usuário e tarefa, deduplicação e política de invalidação; aumentar contexto não resolve concorrência.
Não aplicar quando: Não manter tarefas autônomas quando a correção do usuário tornou seu efeito incompatível com a intenção vigente.

## T154:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Instância e mailbox conservam continuidade da interação.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Hiring Assistant é caso operacional; extrapolações para programação e modelos pequenos são propostas, e Brooklin é analogia de transporte de eventos.
Consultas registradas: V4C-Q010, V4C-Q020.

## T154:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T154 → T208 [complements]
Como combinar: Hiring Assistant mantém instâncias e mailbox enquanto o supervisor coordena plano e execução.
Interface: Mensagens, tarefas e resultados do ciclo de planejamento.
Condição: A instância tem identidade e regras de ciclo de vida.
Aceite proposto: Proposta: interromper uma interação e verificar que o estado da tarefa permanece coerente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T154 → T211 [feeds]
Como combinar: A conversa fornece objetivo e decisões ao pacote de continuidade.
Interface: Revisão do objetivo, artefatos e pendências confirmadas.
Condição: O pacote distingue fatos de interpretações do agente.
Aceite proposto: Retomar sem todo o chat e recuperar corretamente próximos passos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reexecutar mensagem duplicada como nova intenção de mutação.
- Nunca usar apenas ordem de chegada à interface para definir causalidade entre eventos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare retenção de requisitos e retomada com fronteira sob o mesmo estado externo. Contexto persistido reduz esquecimento operacional, sem garantir compreensão equivalente de instruções complexas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T049, T064, T075

## Fontes primárias associadas

### C-S019 — Persistence — LangGraph

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers mantêm estado de threads; stores preservam informação definida pela aplicação entre threads.

Limite: A URL durable-execution redirecionou para persistence na consulta; exemplos InMemory não demonstram durabilidade após queda de processo.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T155 — System Prompt Optimization / prompt de sistema enxuto

**Nome canônico:** Otimização e concisão do prompt de sistema  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T155  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** System Prompt Optimization; otimização do prompt de sistema; prompt de sistema enxuto

## T155:C01 — conceito

System Prompt Optimization ajusta instruções de sistema para melhorar resultados segundo critérios observáveis. Um prompt enxuto remove repetição e conteúdo que pode ser carregado sob demanda, preservando regras e contratos necessários. Menos tokens é uma hipótese de eficiência, não uma prova de qualidade. A edição altera a entrada de inferência e não treina automaticamente os pesos do modelo.

Como funciona:
- Identificar obrigações permanentes, instruções redundantes, exemplos úteis e conhecimento específico que pode sair do núcleo fixo.
- Construir variantes mantendo a intenção, prioridades e condições de execução.
- Comparar versões com casos representativos, critérios de segurança operacional e um conjunto reservado para confirmação.

## T155:C02 — aplicacao

Quando usar:
- Prompts de sistema extensos, contraditórios ou repetidos em todas as chamadas, quando é possível avaliar comportamentos relevantes.

Quando não usar:
- Para remover requisitos essenciais apenas para atingir um tamanho desejado ou corrigir limitações que pertencem ao runtime e às ferramentas.

Implementação proposta:
- Proposta: inventariar cada regra e vinculá-la a um caso de avaliação; consolidar duplicatas sem apagar exceções.
- Manter no núcleo papel, contratos de saída e condições indispensáveis; carregar procedimentos de domínio quando a tarefa os exigir.
- Versionar prompt, modelo, ferramentas e dataset; mudar uma hipótese por comparação e acompanhar tokens e taxa de conclusão correta.
- Separar exemplos usados na otimização dos casos finais e incluir instruções conflitantes, ferramenta indisponível e tarefa fora do escopo.

Aplicação LAI proposta:
Proposta LAI: manter um núcleo de sistema conciso e procedimentos recuperáveis, com aprovação de versão baseada em evidência de avaliação, não em preferência estética.

## T155:C03 — riscos_validacao

Armadilhas:
- Uma frase curta pode ser ambígua e produzir mais tentativas ou tokens de saída.
- Otimizar somente no conjunto conhecido favorece sobreajuste e esconde regressões em casos raros.

Métricas sugeridas:
- Tokens fixos por chamada, custo total por tarefa correta, violações de contrato e regressões por categoria.

Testes propostos:
- Teste proposto: comparar versão original e enxuta nas mesmas tarefas, registrando resultado e motivo das falhas.
- Remover uma regra por vez em ambiente de avaliação para verificar se a simplificação perdeu comportamento necessário.

## T155:C04 — perguntas_proveniencia

Pergunta: Prompt menor significa tarefa mais barata?
Resposta: Não necessariamente. Pode aumentar erros, retries ou saída. Meça custo completo por tarefa concluída corretamente.

Pergunta: Quais instruções podem sair do núcleo fixo?
Resposta: Conteúdo de domínio carregável sob demanda. Regras indispensáveis à interpretação e execução devem permanecer disponíveis no ponto em que se aplicam.

Pergunta: Otimização sem treino pode sobreajustar?
Resposta: Sim. A seleção repetida de candidatos pode explorar particularidades do conjunto de validação, mesmo com pesos congelados.

Pergunta: Como saber se otimizar compensou financeiramente?
Resposta: Somar custo da busca e medir economia por chamada aceita, estimando quantas chamadas reais amortizam a preparação.

Escopo das fontes:
DSPy e engenharia de contexto apoiam otimização; evals sustentam comparação. A divisão do núcleo LAI é proposta.

## T155:C05 — mecanismo_avancado

Otimizar instruções exige distinguir busca do prompt e avaliação final. Examinar repetidamente o mesmo conjunto para escolher candidatos adapta o prompt àquele conjunto, mesmo sem gradiente ou atualização de pesos. MIPROv2 combina propostas de instruções e demonstrações; isso mostra que o objetivo pode melhorar com um prompt maior, não necessariamente mais enxuto. Redução de tokens deve entrar como critério separado ou restrição explícita.

Condição de contorno:
Uma edição que melhora a métrica escolhida pode remover comportamento necessário que o avaliador não mede.

Contrato proposto:
- Entradas: Programa de prompts, exemplos de ajuste, métrica e regras obrigatórias.
- Saídas: Prompt candidato versionado, resultados de seleção e avaliação reservada.
- Estado: Histórico de candidatos, orçamento de busca e divisões de dados.
- Invariante: Casos usados para escolher o prompt não são apresentados como teste independente.

Compromissos de projeto:
- Busca extensa encontra combinações e aumenta risco de sobreajuste à métrica.
- Instruções curtas reduzem custo por chamada e podem exigir exemplos ou contexto adicional para desambiguar.

## T155:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir no conjunto reservado uma obrigação ausente dos exemplos de ajuste; verificar se a redução do prompt preserva esse comportamento.

Plano de avaliação proposto:
Comparar prompt original, edição manual e otimização automática com o mesmo modelo. Medir qualidade por requisito, tokens, custo de busca e ponto de amortização em chamadas futuras. Aprovar alterações somente se a economia mantiver os critérios definidos.

Comparações:
- T179 (distinct_from): Destilação paramétrica altera o modelo; busca de instruções altera a entrada utilizada em inferência.
- T152 (complements): Orçamento identifica custo de contexto, mas não escolhe automaticamente a melhor instrução.

Afirmação rastreável:
MIPROv2 otimiza conjuntamente instruções e exemplos por busca sobre candidatos.
Suporte: direct; fontes: V3C-S014
Limite: A melhoria depende da métrica e dos dados; o otimizador não garante prompt mínimo ou generalização.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T155:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava busca de prompts e avaliação reservada. Esta camada propõe compilar instruções por fase, localizar conflitos e avaliar o custo de manutenção do prompt, além do seu tamanho.

Núcleo e módulos ativados
Separe obrigações permanentes, contrato da tarefa e orientações de ferramenta. O núcleo declara precedência; módulos entram apenas quando o estado exige. A redução útil evita carregar instruções mutuamente irrelevantes. Guardar tudo em arquivos só funciona se existir mecanismo verificável de descoberta e leitura antes da decisão correspondente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

Diagnóstico por requisito
Associe cada instrução a uma falha observável que pretende evitar. Remova uma regra candidata e repita casos que exercitem essa obrigação; mantenha interações entre regras na avaliação. Se duas instruções se contradizem, encurtá-las pode esconder o problema. Resolva autoridade, exceção e condição de aplicação antes de otimizar tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S014, V4C-S030.

Custo de estabilidade
Fixe o início compartilhável do prompt e acrescente contexto variável depois, quando o backend puder reaproveitar prefixos. Uma economia textual pode piorar o cache ou aumentar rodadas de esclarecimento. Compare custo por tarefa aceita, incluindo manutenção dos módulos e buscas adicionais, com a distribuição real de tarefas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S015.

USO AVANÇADO — Editor especializado
Cenário: Um agente pequeno recebe muitas correções locais semelhantes.
Estratégia: Mantenha no núcleo as regras de edição e carregue convenções da linguagem somente após localizar o arquivo. Em mudanças entre linguagens, reavalie os módulos ativos; não reutilize instruções Python em uma etapa SQL por continuidade textual.
Papel do modelo pequeno: 3–7B segue contrato curto e formato fixo; o controlador seleciona módulos.
Aceite proposto: Proposta: zero perda das obrigações críticas e menos tokens totais por edição aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

USO AVANÇADO — Pesquisa com papéis diferentes
Cenário: Coleta e síntese precisam de critérios diferentes de evidência.
Estratégia: O coletor recebe regras de proveniência e extração; o sintetizador recebe matriz de alegações e lacunas. Faça teste cruzado para detectar uma regra de coleta que desapareceu na passagem. Só compartilhe o núcleo que os dois papéis realmente exigem.
Papel do modelo pequeno: 8–14B extrai; 15–30B integra conflitos sob contrato explícito.
Aceite proposto: Proposta: medir cobertura de fontes, contradições e custo com prompts gerais e modulares.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Aplicar instruções curtas para operações repetitivas, com poucos exemplos representativos.
8–14B: Selecionar módulos por classificação de tarefa e explicar conflitos de requisitos.
15–30B: Propor revisões do prompt com justificativa por requisito e avaliar interações mais amplas.
Requisitos de treino/runtime: Versionar prompt, módulos, tokenizer e conjunto de seleção; separar exemplos de avaliação final.
Não aplicar quando: Não remover instruções cujo comportamento necessário não esteja coberto por casos de avaliação.

## T155:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Prompt engineering e simulações foram usados para corrigir falhas de delegação.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Instrução monolítica foi substituída por mapa curto.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Adaptação e otimização de prompts são descritas.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Especialização permitiu reduzir o prompt mantendo instrução explícita de formato.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: OpenAI descreve mapa curto de instruções; Anthropic relata especialização de prompts. O desenho modular para 3–30B é proposta, não resultado medido.
Consultas registradas: V4C-Q024, V4C-Q027.

## T155:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T155 → T234 [complements]
Como combinar: Usar o arquivo de instruções como mapa para fontes específicas, estratégia documentada no harness interno Codex.
Interface: Versão do mapa, caminhos e revisão do repositório.
Condição: Arquivos devem estar acessíveis e atualizados.
Aceite proposto: Verificar se a orientação necessária foi lida antes da edição.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

2. T155 → T157 [complements]
Como combinar: Ordenar módulos estáveis antes dos dados mutáveis para preservar prefixos reutilizáveis.
Interface: Tokens efetivos e identidade da configuração.
Condição: Backend com cache compatível e isolamento definido.
Aceite proposto: Comparar acertos, prefill e correção após mudanças de módulo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma regra ausente pode parecer otimização se o avaliador nunca exigir seu comportamento.
- Tratar documentos recuperados como dados; sua presença não altera a precedência das instruções.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare agente pequeno com prompt modular e modelo de fronteira com as mesmas ferramentas. Ganho em edição rotineira não demonstra compreensão equivalente de requisitos inéditos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T151, T176, P001, P016

## Fontes primárias associadas

### C-S020 — DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines

[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Otimização de pipelines de chamadas de LLM com objetivo mensurável.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### V3C-S014 — DSPy — MIPROv2 optimizer

[https://dspy.ai/current/api/optimizers/MIPROv2/](https://dspy.ai/current/api/optimizers/MIPROv2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Otimização conjunta de instruções e demonstrações com propostas de candidatos e busca por otimização Bayesiana.

Limite: O programa de avaliação define o objetivo; melhorias locais não demonstram generalização nem redução de tokens.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T156 — Temperature Tuning

**Nome canônico:** Temperature Tuning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T156  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ajuste de temperatura

## T156:C01 — conceito

Ajuste da temperatura de amostragem para controlar quão concentrada fica a distribuição usada na escolha de tokens. Temperaturas menores tendem a concentrar escolhas; maiores favorecem diversidade. Isso não corresponde a um controle direto de factualidade, criatividade útil ou inteligência.

Como funciona:
- Aplicar escala aos logits antes da amostragem, conforme o backend.
- Combinar temperatura com outros parâmetros, como top-p, de forma explícita.
- Avaliar o resultado da tarefa e a diversidade, não apenas variação textual.

## T156:C02 — aplicacao

Quando usar:
- Geração de candidatos para seleção posterior.
- Extração ou classificação que requer estabilidade de formato e decisão.

Quando não usar:
- Tentar corrigir conhecimento incorreto exclusivamente reduzindo temperatura.

Implementação proposta:
- Testar poucos valores compatíveis com o endpoint e manter demais parâmetros fixos.
- Registrar versão de modelo e seed quando suportada.
- Escolher configuração por tarefa com critério de qualidade, não por preferência abstrata.

Aplicação LAI proposta:
Proposta: perfis de amostragem da Helena serem definidos por avaliação de extração, planejamento e geração de alternativas.

## T156:C03 — riscos_validacao

Armadilhas:
- Temperatura zero não garante reprodução exata em toda infraestrutura.
- Misturar alterações de temperatura, top-p e prompt impede atribuir causa ao ganho.

Métricas sugeridas:
- Acerto médio e variância em repetições.
- Diversidade de soluções válidas e custo por candidato aceito.

Testes propostos:
- Repetir mesmas entradas com configurações controladas e comparar resultados.
- Confirmar que valor não suportado gera erro explícito em vez de ajuste silencioso.

## T156:C04 — perguntas_proveniencia

Pergunta: Temperatura baixa elimina alucinação?
Resposta: Não. Pode repetir com maior estabilidade uma resposta errada.

Pergunta: Temperatura de calibração é a mesma coisa?
Resposta: Não. Calibração ajusta probabilidades de confiança; amostragem escolhe tokens.

Pergunta: Temperatura zero produz verdade?
Resposta: Não. Ela tende a escolher o candidato dominante; se a distribuição favorece um erro, esse erro pode se repetir.

Pergunta: Por que variar também top-p atrapalha o teste?
Resposta: Porque muda o conjunto de tokens elegíveis, impedindo atribuir o efeito observado somente à temperatura.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T156:C05 — mecanismo_avancado

Para logits zᵢ e temperatura T positiva, a amostragem pode usar pᵢ(T)=exp(zᵢ/T)/Σⱼexp(zⱼ/T), antes ou em composição com outros filtros. Diminuir T amplia diferenças relativas, mas não corrige a ordenação de candidatos que o modelo já calculou incorretamente. O limite T→0 concentra massa nos maiores logits; um backend pode oferecer modo guloso em vez de aceitar divisão numérica por zero.

Condição de contorno:
Quando filtros, penalidades ou implementação mudam, o mesmo valor de temperatura não descreve sozinho a distribuição final.

Contrato proposto:
- Entradas: Logits, temperatura, demais filtros e configuração de amostragem.
- Saídas: Token amostrado ou escolha gulosa, com configuração identificada.
- Estado: Seed quando suportada, sequência anterior e versão do backend.
- Invariante: Comparações de temperatura mantêm iguais os demais fatores de geração.

Compromissos de projeto:
- Concentração reduz diversidade e pode repetir consistentemente um erro dominante.
- Diversidade amplia exploração e aumenta o trabalho para selecionar respostas corretas.

## T156:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar um caso em que a alternativa mais provável é errada; comparar múltiplas amostras sem assumir que temperatura baixa melhora factualidade.

Plano de avaliação proposto:
Comparar temperaturas com várias repetições, controlando modelo, prompt, top-p e limite de saída. Medir correção, diversidade útil e custo do verificador. Escolher por tarefa, reportando variabilidade; uma seed isolada não sustenta conclusão geral.

Comparações:
- T146 (complements): Diversidade de amostragem pode compor a largura da busca sob orçamento.
- T198 (distinct_from): Concentração dos logits não equivale à calibração de confiança factual.

Afirmação rastreável:
Transformers documenta TemperatureLogitsWarper e sua combinação com filtros top-k e top-p.
Suporte: direct; fontes: V3C-S017
Limite: O contrato exato de temperatura zero e determinismo depende da biblioteca e do modo de geração.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T156:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava temperatura e diversidade. A expansão trata políticas de amostragem por fase, repetição útil e seleção verificável, evitando usar aleatoriedade para mascarar um problema de contrato.

Exploração e emissão separadas
Use diversidade onde alternativas podem ser avaliadas: hipóteses de causa, estratégias de consulta ou candidatos de patch. Na emissão de argumentos de ferramenta, privilegie o contrato validável. Não altere a temperatura de uma conversa inteira só porque uma das fases exige criatividade; registre a política em cada chamada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V3C-S017.

Diversidade efetiva
Múltiplas amostras que diferem apenas em nomes de variáveis não representam explorações independentes. Agrupe candidatos por alteração semântica ou hipótese e contabilize famílias distintas. Quando todos seguem a mesma interpretação errada, forneça evidência nova ou mude a decomposição; aumentar o número de amostras pode apenas multiplicar custo correlacionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S017, V4C-S029.

Configuração completa
Temperatura participa de uma política que também contém top-p, penalidades, limites e modo de raciocínio. A documentação Nemotron diferencia regimes de geração; essa configuração não é um padrão universal. Na migração de backend, valide o comportamento efetivo e confirme se algum parâmetro foi ignorado pelo servidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018.

USO AVANÇADO — Busca de reparos pequenos
Cenário: Há teste reproduzível que distingue alterações corretas de incorretas.
Estratégia: Gere candidatos diversos em cópias isoladas, deduplique patches equivalentes e rode primeiro o teste que reproduz o defeito. Se todos falharem da mesma forma, interrompa a rodada e solicite observação adicional antes de aumentar diversidade.
Papel do modelo pequeno: 3–7B produz alternativas locais; verificador executável escolhe elegíveis.
Aceite proposto: Proposta: medir taxa de solução por família de candidatos e custo até o primeiro patch aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V3C-S017.

USO AVANÇADO — Extração com ambiguidades
Cenário: Documento permite duas interpretações de um campo.
Estratégia: Faça uma primeira extração com política estável. Quando validação de domínio detectar ambiguidade, peça candidatos estruturados apoiados em trechos, em vez de reamostrar silenciosamente até surgir valor conveniente. Preserve a possibilidade de não resolver o campo.
Papel do modelo pequeno: 8–14B gera interpretações; 15–30B confronta evidência conflitante.
Aceite proposto: Proposta: erro factual, abstenção apropriada e estabilidade entre repetições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Amostras curtas em domínio estreito, com parser e teste externos.
8–14B: Explorar estratégias de consulta e pequenas interpretações alternativas sem substituir evidência.
15–30B: Comparar candidatos de maior alcance mantendo orçamento e verificador independente.
Requisitos de treino/runtime: Registrar política inteira, versão de pesos, runtime e seed quando suportada; usar várias repetições.
Não aplicar quando: Não usar diversidade como substituto de dado ausente nem voto de modelos como prova de verdade.

## T156:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: A model card distingue configurações de amostragem por modo.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron documenta parâmetros por regime; OpenAI relata seleção entre candidatos. Não foi encontrado ensaio operacional que determine temperatura universal por faixa de parâmetros.
Consultas registradas: V4C-Q014, V4C-Q027.

## T156:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T156 → T146 [complements]
Como combinar: Dedicar largura de busca a famílias diferentes de hipótese, usando amostragem como uma das fontes de variedade.
Interface: Identidade do candidato, política e grupo semântico.
Condição: Existe avaliador capaz de comparar resultados.
Aceite proposto: Ganho por candidato útil, incluindo custo dos descartados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T156 → T200 [complements]
Como combinar: Enviar candidatos ao verificador antes de selecionar uma resposta definitiva.
Interface: Artefato imutável, resultado de teste e motivo da rejeição.
Condição: Critério independente da preferência textual do gerador.
Aceite proposto: Rejeitar candidato eloquente que falha o requisito objetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Baixa temperatura pode reproduzir deterministicamente o erro dominante.
- Votar entre amostras correlacionadas não gera confiança calibrada; reportar desacordo e origem das alternativas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo por solução validada, controlando quantas amostras o modelo de fronteira recebe. Um pequeno modelo com muitas tentativas não deve ser comparado a uma única tentativa sem explicitar orçamento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T188, T198

## Fontes primárias associadas

### C-S021 — sampling_params — vLLM

[https://docs.vllm.ai/en/latest/api/vllm/sampling_params/](https://docs.vllm.ai/en/latest/api/vllm/sampling_params/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Parâmetros de amostragem incluem temperatura e limites de saída; compatibilidade deve ser conferida na versão instalada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S017 — Transformers — Utilities for generation

[https://huggingface.co/docs/transformers/internal/generation_utils](https://huggingface.co/docs/transformers/internal/generation_utils)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TemperatureLogitsWarper e filtros top-k/top-p transformam logits e distribuição de amostragem.

Limite: Parâmetros e ordem de aplicação variam por backend; não garantem factualidade ou determinismo entre ambientes.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T157 — Prefix Hashing

**Nome canônico:** Prefix Hashing  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T157  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** hash de prefixos

## T157:C01 — conceito

Identificação de prefixos ou blocos de contexto por hash para localizar estados computacionais reutilizáveis. A identidade deve refletir os tokens e as condições relevantes da execução, não apenas texto visualmente semelhante. O hash serve para indexação; não prova que um conteúdo é verdadeiro.

Como funciona:
- Tokenizar com configuração compatível com o modelo servido.
- Combinar conteúdo, histórico ancestral e metadados necessários em uma chave.
- Reutilizar estado somente quando a identidade de cache corresponde.

## T157:C02 — aplicacao

Quando usar:
- Runtime com reutilização de KV cache para prefixos idênticos.
- Muitas chamadas compartilham instruções ou documentos estáveis.

Quando não usar:
- Reutilizar cache entre checkpoints, adaptadores ou tenants sem identidade compatível.

Implementação proposta:
- Incluir versão de modelo e configuração relevante no namespace do cache.
- Adotar hash apropriado e política de isolamento entre clientes.
- Testar invalidadores como troca de adaptador, template e conteúdo multimodal.

Aplicação LAI proposta:
Proposta: conferir a implementação real do servidor antes de organizar prompts da Helena para reaproveitamento de prefixo.

## T157:C03 — riscos_validacao

Armadilhas:
- Pequena mudança no começo do prompt invalida reutilização posterior.
- Hash de texto ignora diferenças introduzidas por template ou tokenização.

Métricas sugeridas:
- Taxa de acerto por blocos e tokens de prefill evitados.
- Número de reutilizações inválidas detectadas em testes de isolamento.

Testes propostos:
- Alterar um token do prefixo e verificar que blocos dependentes não são tratados como iguais.
- Trocar adaptador ou identidade de cliente e conferir segregação do cache.

## T157:C04 — perguntas_proveniencia

Pergunta: Hash semelhante indica prefixo parecido?
Resposta: Não em hash criptográfico comum; ele identifica igualdade do conteúdo representado.

Pergunta: Prefix hashing é semantic caching?
Resposta: Não. Reutilização exata de estado difere de aproximar perguntas pelo significado.

Pergunta: Texto igual garante KV igual?
Resposta: Não. Modelo, tokenização, adaptador e entradas multimodais podem alterar o cálculo apesar da aparência textual.

Pergunta: Por que incluir a identidade do bloco anterior?
Resposta: Porque a representação de um token depende do prefixo causal; igualar somente o bloco local ignora esse contexto.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T157:C05 — mecanismo_avancado

No desenho de prefix caching do vLLM, a identidade de um bloco depende do hash do bloco anterior, dos tokens do bloco e de extras relevantes. Encadear o pai impede tratar o mesmo fragmento como equivalente após históricos diferentes. Conteúdo multimodal merece atenção: placeholders textuais iguais podem corresponder a imagens distintas, exigindo identidade adicional. Adaptadores e grupos de compartilhamento também podem afetar a chave.

Condição de contorno:
Uma chave incompleta permite reutilização indevida; uma chave excessivamente específica destrói acertos sem necessidade.

Contrato proposto:
- Entradas: Tokens efetivos, ancestralidade do bloco, modelo e metadados de execução relevantes.
- Saídas: Chave de bloco e resolução para KV compatível ou cache miss.
- Estado: Mapa de blocos, contagens de referência e política de expiração.
- Invariante: Só blocos semanticamente equivalentes para o cálculo de atenção compartilham identidade.

Compromissos de projeto:
- Isolar grupos de cache reduz compartilhamento e evita mistura de domínios que devem permanecer separados.
- Blocos maiores reduzem metadados e podem perder reaproveitamento de prefixos parcialmente iguais.

## T157:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter tokens de placeholder e trocar a imagem ou o adaptador; exigir cache miss quando a representação computada mudar.

Plano de avaliação proposto:
Comparar reutilização com cache desabilitado, controlando modelo, tokenizer e entradas. Medir acerto de blocos, tempo de prefill, memória e igualdade esperada dos resultados numéricos. Considerar também mudanças de prefixo e cache frio.

Comparações:
- T171 (complements): Orquestração usa identidade de prefixo para estimar onde existe trabalho reutilizável.
- T150 (distinct_from): Singleflight compartilha uma execução em curso; hashing endereça estado computacional armazenado.

Afirmação rastreável:
O design vLLM inclui hash do pai, tokens e extras como LoRA, hashes multimodais e salt.
Suporte: direct; fontes: V3C-S015
Limite: A documentação descreve aquela implementação; não se deve presumir a mesma composição em outros backends.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T157:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhava hash encadeado de blocos. Esta camada considera migração de versões, isolamento entre domínios e investigação de falsos acertos, com decisões que preservam equivalência computacional.

Namespace de execução
Construa a identidade de cache a partir da configuração efetivamente servida, não do alias comercial do modelo. Troca de quantização, adaptador ou template deve ser avaliada como mudança de execução. Um namespace explícito reduz o risco de um alias mutável apontar para pesos novos enquanto blocos antigos continuam elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

Invalidar com alcance definido
Organize quais mudanças invalidam todos os blocos e quais afetam apenas uma ramificação do prefixo. Uma alteração no núcleo inicial invalida seus descendentes; mudar somente o último documento não precisa destruir prefixos anteriores compatíveis. Esse desenho permite publicar prompts novos com convivência controlada entre gerações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

Auditar equivalência
Acompanhe acertos por classe de chave e compare amostras com recomputação sem cache. Um resultado incorreto pode vir de colisão lógica por metadado ausente, mesmo sem colisão criptográfica. Testes devem trocar imagem, adaptador, tenant e template separadamente para localizar a dimensão que a chave deixou de representar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Assistentes por organização
Cenário: Vários clientes usam instruções parecidas e documentos diferentes.
Estratégia: Compartilhe somente o prefixo cuja reutilização seja permitida e computacionalmente compatível; introduza identidade de domínio onde necessário. Documentos privados não se tornam compartilháveis apenas porque o texto inicial coincide. Compare isolamento estrito e compartilhamento aprovado sob carga.
Papel do modelo pequeno: 3–7B atende tarefas curtas; o runtime determina identidade, sem delegá-la ao modelo.
Aceite proposto: Proposta: nenhum reaproveitamento entre domínios proibidos e redução de prefill nos casos elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Atualização de instruções
Cenário: O mesmo agente recebe uma revisão do núcleo operacional.
Estratégia: Publique nova geração do prompt, mantenha a anterior para execuções já iniciadas e contabilize aquecimento. Não misture tokens de um template com estado calculado por outro. Expire versões antigas quando suas execuções e requisitos de retenção terminarem.
Papel do modelo pequeno: 8–14B e 15–30B mantêm papéis; a compatibilidade depende da configuração, não do porte.
Aceite proposto: Proposta: resposta equivalente à recomputação e custo de aquecimento explicitado na migração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Beneficiar-se de prefixos curtos muito repetidos, sem esperar ganho quando decode domina.
8–14B: Usar templates estáveis de extração e registrar variações por tarefa.
15–30B: Reaproveitar instruções longas e repositórios comuns, medindo pressão de KV e concorrência.
Requisitos de treino/runtime: Backend com identidade documentada, política de expulsão e telemetria por versão; não reimplementar hash ad hoc.
Não aplicar quando: Não compartilhar estado entre modelos ou representações multimodais apenas porque textos visíveis são iguais.

## T157:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 5.1/Algoritmo 1: chave de bloco combina tokens locais e hash do bloco anterior. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes de vLLM e políticas Uber apoiam implementação e afinidade. Request collapsing de CDN não é prefix KV cache e não foi contado como o mesmo mecanismo.
Consultas registradas: V4C-Q009, V4C-Q017.

## T157:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T157 → T171 [feeds]
Como combinar: Fornecer identidade e idade de residência para decisão de afinidade, mantendo possibilidade de recomputar.
Interface: Chave de prefixo, namespace e timestamp de telemetria.
Condição: Estimativa de economia compete com espera na fila.
Aceite proposto: Rota correta mesmo após expulsão de bloco.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T157 → T155 [complements]
Como combinar: Avaliar edição do prompt também pelo quanto invalida prefixos frequentes.
Interface: Versões de módulos e distribuição de reutilização.
Condição: Qualidade é aprovada antes da economia de cache.
Aceite proposto: Comparar custo total após troca e não apenas tokens removidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Hash forte não corrige a ausência de uma dimensão semântica da chave.
- Telemetria de hit não comprova equivalência; manter teste de recomputação em mudanças de runtime.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno e fronteira com cache frio e quente separados. Vantagem por prefixo repetido é propriedade da carga e infraestrutura, não equivalência geral de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T171

## Fontes primárias associadas

### C-S022 — Automatic Prefix Caching — vLLM

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos inclui hash ancestral, tokens e informações como adaptador e salt de isolamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

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


---

# T158 — Tool Registry

**Nome canônico:** Tool Registry  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T158  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** registro de ferramentas

## T158:C01 — conceito

Catálogo de ferramentas com identificadores, descrições, schemas, versões, responsáveis e requisitos de acesso. O registro informa o que pode ser descoberto e chamado; a execução precisa revalidar permissão e disponibilidade. É infraestrutura de integração, não uma habilidade paramétrica da LLM.

Como funciona:
- Registrar contrato e metadados da operação em identidade estável.
- Consultar capacidades filtradas pelo contexto e permissões do agente.
- Resolver versão e endpoint antes de executar uma chamada validada.

## T158:C02 — aplicacao

Quando usar:
- Muitos agentes compartilham integrações.
- Ferramentas mudam de versão ou pertencem a domínios diferentes.

Quando não usar:
- Catálogo vira depósito de nomes sem schema, responsável ou política de compatibilidade.

Implementação proposta:
- Definir descrição operacional e exemplos mínimos de entrada.
- Manter status ativo, obsoleto e indisponível explicitamente.
- Validar contratos de entrada e saída no registro e no executor.

Aplicação LAI proposta:
Proposta: integrar contratos dos softwares LAI em um registro consultável pela Helena, preservando versões e escopos.

## T158:C03 — riscos_validacao

Armadilhas:
- Descoberta pode revelar ferramenta que o usuário não pode utilizar.
- Nome estável com semântica alterada quebra agentes mesmo se o JSON continua válido.

Métricas sugeridas:
- Cobertura de contratos e ferramentas sem proprietário.
- Falhas de resolução, schema incompatível e descoberta incorreta.

Testes propostos:
- Publicar versão incompatível e conferir que clientes fixados não a recebem silenciosamente.
- Consultar como identidade sem acesso e verificar filtragem e bloqueio na execução.

## T158:C04 — perguntas_proveniencia

Pergunta: O registro executa a ferramenta?
Resposta: Pode resolver o destino; execução é responsabilidade separada ou claramente delimitada.

Pergunta: MCP é obrigatório?
Resposta: Não. É uma opção de protocolo; o catálogo pode existir com outras interfaces.

Pergunta: Remover uma ferramenta indisponível resolve o histórico?
Resposta: Não. Uma execução antiga ainda precisa apontar para o descritor utilizado; disponibilidade e identidade histórica devem ser separadas.

Pergunta: Duas ferramentas com o mesmo nome são intercambiáveis?
Resposta: Somente após verificar origem, contrato e efeitos; igualdade nominal não demonstra equivalência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T158:C05 — mecanismo_avancado

Um registro distribuído de ferramentas deve representar identidade e disponibilidade separadamente. Uma ferramenta conhecida pode estar temporariamente fora de serviço; removê-la do catálogo sem histórico pode tornar tarefas antigas impossíveis de explicar. Na agregação de vários servidores, nomes iguais exigem namespace. Uma fotografia do catálogo por execução permite reconstruir quais descrições e schemas orientaram a seleção, mesmo após mudanças posteriores.

Condição de contorno:
Catálogo atualizado não prova que a ferramenta continuará disponível ou autorizada no momento da chamada.

Contrato proposto:
- Entradas: Descritores por servidor, capacidades declaradas, revisões e sinal de alteração.
- Saídas: Catálogo normalizado, namespace inequívoco e fotografia da seleção.
- Estado: Revisões conhecidas, descritores carregados e estado operacional separado.
- Invariante: O nome visível nunca é usado para fundir ferramentas de origens diferentes sem identidade explícita.

Compromissos de projeto:
- Atualização imediata reduz obsolescência e pode alterar comportamento no meio de uma missão.
- Fixar uma fotografia melhora explicação e exige revalidar disponibilidade na execução.

## T158:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: registrar dois servidores com ferramenta homônima e atualizar apenas um schema; verificar seleção inequívoca e invalidação da definição correta.

Plano de avaliação proposto:
Comparar refresh por período e atualização por notificação sob mudanças de catálogo. Medir atraso de propagação, chamadas com contrato antigo e custo de descoberta. Definir a política segundo frequência de alteração e duração das tarefas.

Comparações:
- T151 (complements): O registro abastece a descoberta usada pelo carregamento tardio.
- T170 (complements): Versionamento define como interpretar revisões dos contratos catalogados.

Afirmação rastreável:
MCP define listagem de ferramentas e notificação listChanged para servidores que declaram essa capacidade.
Suporte: direct; fontes: V3C-S004
Limite: Agregação entre servidores, snapshots e histórico do catálogo são propostas de aplicação.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T158:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia catálogo, disponibilidade e namespace. Esta camada acrescenta governança de descoberta, habilitação e publicação de descritores para impedir que uma ferramenta encontrada se torne executável sem contrato revisado.

Descoberta não habilita
Modele estados encontrado, descrito, revisado, habilitado e retirado. Um crawler pode identificar serviços que nunca deveriam ser oferecidos ao agente. O mecanismo do gateway Uber motiva uma revisão de descritor antes da exposição; a proposta mantém separada a identidade do serviço de sua elegibilidade por tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Descritor como código
Trate mudança de nome, descrição e exemplos como alteração comportamental. Mesmo com schema idêntico, uma descrição nova pode alterar seleção do modelo. Versione o conjunto inteiro e compare consultas que antes roteavam corretamente. Se o dono da ferramenta mudar a unidade ou o efeito, a revisão precisa tratar significado além da sintaxe.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S013.

Retirada em duas fases
Uma ferramenta retirada pode continuar citada em tarefas duráveis. Bloqueie novas seleções, mas conserve o descritor histórico para explicar decisões passadas. Se uma execução antiga precisar agir, faça nova checagem de elegibilidade; não considere seu snapshot histórico uma autorização permanente para chamar a versão atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S004.

USO AVANÇADO — Catálogo empresarial crescente
Cenário: Centenas de APIs mudam em ritmos diferentes.
Estratégia: Automatize descoberta e geração inicial de metadados, encaminhe diferenças ao proprietário e publique somente versões revisadas. Habilite progressivamente um subconjunto com tarefas conhecidas. Uma regressão de seleção deve permitir voltar ao catálogo anterior sem apagar o histórico.
Papel do modelo pequeno: 3–7B classifica descritores; 8–14B sugere exemplos e casos ambíguos para revisão.
Aceite proposto: Proposta: medir falsas habilitações, latência de atualização e precisão de seleção por revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Ferramentas por especialidade
Cenário: Especialistas pequenos precisam de poucos recursos do catálogo geral.
Estratégia: Crie uma visão por função e carregue schema completo apenas após descoberta. Conserve o identificador global no resultado para que a integração reconheça a origem. Se duas especialidades pedirem a mesma ação, compare contratos e escopos antes de fundir chamadas.
Papel do modelo pequeno: 15–30B planeja o conjunto de capacidades; trabalhadores menores recebem visões restritas.
Aceite proposto: Proposta: nenhuma resolução ambígua de nomes e redução de schemas carregados por tarefa aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Selecionar em listas curtas de ferramentas bem distintas e exemplos concretos.
8–14B: Discriminar ferramentas próximas usando schema e descrição recuperados sob demanda.
15–30B: Relacionar capacidades entre serviços, mas sem decidir habilitação organizacional por conta própria.
Requisitos de treino/runtime: Registro com donos, versões, ambiente, escopo e processo de publicação; descritores testados como interface.
Não aplicar quando: Não usar descoberta automática como prova de acesso permitido ou de estabilidade operacional.

## T158:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: MCP Registry mantém ferramentas, schemas, propriedade e habilitação.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Gateway Uber comprova integração de catálogo, descoberta e invocação. Propostas de revisão por banda de parâmetros não foram medidas.
Consultas registradas: V4C-Q009.

## T158:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T158 → T151 [complements]
Como combinar: O registro do gateway fornece descoberta progressiva até a resolução do schema específico.
Interface: Servidor, ferramenta e revisão do schema.
Condição: Somente itens habilitados devem ser expostos.
Aceite proposto: Validar o schema recuperado no momento da invocação.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

2. T158 → T170 [complements]
Como combinar: Publicar mudança de contrato junto do descritor e manter versões históricas.
Interface: Diferença semântica, versão e consumidores afetados.
Condição: Existe estratégia de migração ou compatibilidade comprovada.
Aceite proposto: Testar consultas antigas e novas antes de ativar a revisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma ferramenta descoberta e desabilitada deve continuar invisível à invocação elegível.
- Descrições geradas por modelo precisam de revisão contra o efeito real da API.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare seletores pequenos e de fronteira no mesmo catálogo e nas mesmas ambiguidades. Facilidade de roteamento com catálogo curado não demonstra domínio de APIs inéditas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T045, T151, T170

## Fontes primárias associadas

### C-S007 — Tools — Model Context Protocol, 2025-06-18

[https://modelcontextprotocol.io/specification/2025-06-18/server/tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ferramentas expõem nome, schema, descoberta e chamada por contrato; protocolo não concede autorização de negócio.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T159 — Durable Execution

**Nome canônico:** Durable Execution  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T159  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execução durável

## T159:C01 — conceito

Execução que persiste progresso para continuar após interrupções ou falhas. Histórico, checkpoints e replay reconstroem a posição do workflow. A durabilidade do fluxo não implica efeito externo exatamente uma vez: operações remotas ainda precisam de idempotência, recibos ou reconciliação.

Como funciona:
- Registrar decisões e resultados de etapas em armazenamento durável.
- Após falha, recuperar estado e distinguir trabalho concluído de pendente.
- Retomar respeitando contratos de replay e efeitos externos.

## T159:C02 — aplicacao

Quando usar:
- Missões longas que atravessam reinícios.
- Fluxos que aguardam eventos externos ou aprovação já prevista.

Quando não usar:
- Reexecutar chamadas não determinísticas durante replay sem registrar seus resultados.

Implementação proposta:
- Escolher unidade de persistência e política de commit por etapa.
- Executar I/O não determinístico em atividades com resultado registrado.
- Versionar workflow para que código novo consiga interpretar históricos existentes.

Aplicação LAI proposta:
Proposta: a Helena persistir progresso e recibos por missão, permitindo continuar tarefas sem depender de uma conversa permanentemente aberta.

## T159:C03 — riscos_validacao

Armadilhas:
- Queda entre efeito remoto e registro local cria estado incerto.
- Mudança incompatível no código torna replay inválido.

Métricas sugeridas:
- Taxa de retomada correta e trabalho repetido após falha.
- Tempo de recuperação e quantidade de históricos incompatíveis.

Testes propostos:
- Matar worker após cada fronteira crítica e verificar continuação.
- Simular resposta perdida após efeito externo e exigir consulta ou deduplicação antes de repetir.

## T159:C04 — perguntas_proveniencia

Pergunta: Durable execution garante exactly once no CRM?
Resposta: Não. Essa propriedade depende também do contrato do CRM e da reconciliação.

Pergunta: Checkpoint basta para qualquer retomada?
Resposta: Não. Precisa estar consistente com efeitos já realizados.

Pergunta: Uma LLM com temperatura zero pode rodar livremente dentro do replay?
Resposta: Não se deve presumir determinismo externo. O resultado precisa ser registrado pelo mecanismo apropriado do runtime.

Pergunta: Por que testar apenas workflows novos é insuficiente?
Resposta: Porque eles não exercitam históricos produzidos por versões anteriores, onde alterações de comandos podem quebrar a retomada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T159:C05 — mecanismo_avancado

Replay durável não exige que cada instrução de máquina seja idêntica; exige compatibilidade com o histórico de comandos observáveis pelo runtime. No Temporal, chamadas não determinísticas, inclusive consultas e LLMs, pertencem a Activities. Uma alteração que muda a ordem de comandos pode impedir retomar workflows antigos mesmo que o novo código funcione em execuções recém-criadas. Evolução do código é, portanto, parte do contrato de continuidade.

Condição de contorno:
Persistir eventos sem manter código capaz de interpretá-los não garante retomada após uma atualização.

Contrato proposto:
- Entradas: Histórico, versão compatível do workflow e resultados registrados das atividades.
- Saídas: Estado reconstruído e próximos comandos consistentes com o histórico.
- Estado: Versão de código, pontos de migração e resultados duráveis.
- Invariante: Replay não solicita novamente uma observação externa apenas para reproduzir uma decisão já registrada.

Compromissos de projeto:
- Histórico detalhado aumenta capacidade de reconstrução e custo de armazenamento.
- Manter versões antigas facilita continuidade e aumenta esforço de operação e migração.

## T159:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: pausar um workflow, trocar a ordem de duas atividades no código e tentar retomá-lo; exigir detecção de incompatibilidade ou migração prevista, nunca continuidade silenciosamente divergente.

Plano de avaliação proposto:
Comparar retomada com a versão original e com migração controlada. Medir falhas de replay, tarefas reexecutadas e tempo de recuperação. Usar históricos reais de desenvolvimento separados dos casos de decisão; aceitar mudança somente com compatibilidade demonstrada.

Comparações:
- T241 (complements): Replay é um mecanismo de reconstrução usado por runtimes duráveis.
- T162 (complements): Efeitos de Activities continuam precisando de identidade e repetição segura.

Afirmação rastreável:
Temporal exige compatibilidade determinística de comandos e orienta colocar operações externas em Activities.
Suporte: direct; fontes: V3C-S018
Limite: A semântica de durabilidade varia entre runtimes; a fonte não prova efeito remoto exatamente uma vez.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T159:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava determinismo de replay e evolução de código. A ampliação define fronteiras de falha entre decisão cognitiva e efeitos, crescimento do histórico e retomada de atividades longas sem depender da memória conversacional.

Decisão registrada antes do efeito
Faça o resultado da LLM virar um artefato validado contendo ação, argumentos e versão do contrato. O workflow durável registra a decisão; uma atividade separada executa o efeito com identidade estável. Se a chamada ao modelo falhar antes de produzir decisão válida, uma nova geração pode ser legítima; depois da decisão confirmada, replay deve reutilizá-la.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, C-S026.

Histórico finito e referências
Não persista documentos enormes em cada evento. Registre referências imutáveis, hashes e os campos necessários para decidir próximos passos. A existência do evento não garante que seu arquivo externo continue acessível: retenção do artefato e do histórico precisam ser coordenadas. Divida missões longas em segmentos com estado de passagem explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S024.

Operação sob versões múltiplas
Mantenha workers compatíveis com execuções antigas enquanto novas usam a versão aprovada. Exercite históricos de falhas, não apenas trajetórias felizes. Uma retomada que relança a atividade pode repetir acesso remoto; durabilidade do coordenador não elimina a necessidade de idempotência, reconciliação e classificação de falhas na integração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

USO AVANÇADO — Migração de código demorada
Cenário: Uma campanha atravessa centenas de módulos e quedas de workers.
Estratégia: Registre plano, revisão base e conclusão de cada unidade. Gere patch em atividade separada, valide e publique referência do candidato. Após queda, recupere o próximo módulo pendente; se a publicação ficou incerta, consulte seu identificador antes de refazer a alteração.
Papel do modelo pequeno: 3–7B edita unidades simples; 15–30B planeja dependências e exceções.
Aceite proposto: Proposta: nenhuma unidade esquecida ou publicada duas vezes após falhas injetadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S018.

USO AVANÇADO — Pesquisa interrompida por horas
Cenário: Coletas remotas e síntese não terminam na mesma sessão.
Estratégia: Persistir cada fonte com data, conteúdo identificado e estado de extração. A retomada reutiliza observações confirmadas e reconsulta somente itens cuja validade venceu. Se a pergunta mudou, crie nova revisão em vez de reinterpretar silenciosamente decisões já registradas.
Papel do modelo pequeno: 8–14B extrai; coordenador durável controla fases e revisões.
Aceite proposto: Proposta: equivalência de cobertura entre execução contínua e retomada, com atualização explícita de fontes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atividades pequenas com saída validável e baixa variância de duração.
8–14B: Etapas com recuperação de documentos e retorno estruturado, desacopladas do histórico do workflow.
15–30B: Planejamento mais amplo em atividade registrada; nunca executar chamadas externas diretamente no replay determinístico.
Requisitos de treino/runtime: Runtime durável, armazenamento de artefatos, versão de worker e contratos idempotentes na borda.
Não aplicar quando: Não prometer continuidade se somente mensagens de chat foram salvas ou se artefatos referenciados desaparecem.

## T159:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: O relato inclui recuperação de processos distribuídos longos.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Execução durável de workflows é o mecanismo central relatado.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber documenta Cadence operacional; Cadence e Temporal permanecem produtos distintos. Fontes Temporal explicam contrato, sem inferir adoção de um a partir do outro.
Consultas registradas: V4C-Q002, V4C-Q022.

## T159:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T159 → T241 [complements]
Como combinar: Cadence usa reprodução do histórico para continuidade e validação de execução.
Interface: Histórico compatível e versão do worker.
Condição: Operações externas têm resultados registrados.
Aceite proposto: Retomar após queda sem gerar decisões externas para reconstruir passado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S001. Casos: V4C-C003.

2. T159 → T162 [complements]
Como combinar: Associar efeito remoto a identidade estável quando uma atividade pode repetir.
Interface: Chave de intenção e parâmetros normalizados.
Condição: Serviço de destino oferece deduplicação ou reconciliação.
Aceite proposto: Queda após confirmação remota não duplica o efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar um histórico incompatível em nova execução silenciosa.
- Distinguir atividade não concluída de efeito remoto desconhecido antes de repetir.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos por qualidade das atividades; compare runtimes por recuperação. Um modelo pequeno com durabilidade pode completar mais missões interrompidas sem possuir maior capacidade cognitiva.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T162, R008

## Fontes primárias associadas

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T160 — DAG Scheduling

**Nome canônico:** DAG Scheduling  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T160  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento de grafo acíclico

## T160:C01 — conceito

Escalonamento de tarefas descritas por grafo acíclico direcionado de dependências. Uma tarefa só fica pronta quando suas precondições predecessoras são satisfeitas. Ordenação topológica determina o que pode executar, enquanto recursos, prioridades e quotas determinam quando realmente executará.

Como funciona:
- Construir nós de trabalho e arestas de dependência.
- Identificar nós prontos sem predecessores pendentes.
- Executar e liberar sucessores após conclusão válida dos nós anteriores.

## T160:C02 — aplicacao

Quando usar:
- Pipelines com etapas independentes e pontos de junção.
- Auditorias ou processamento em lote com dependências explícitas.

Quando não usar:
- Representar ciclos de agente sem uma camada própria que limite ou desenrole as iterações.

Implementação proposta:
- Validar ausência de ciclos antes de iniciar.
- Separar estados pronto, executando, concluído, falho e bloqueado.
- Definir como falha de um predecessor afeta seus descendentes e ramos independentes.

Aplicação LAI proposta:
Proposta: transformar planos verificáveis da Helena em dependências explícitas, com ramos paralelos apenas quando realmente independentes.

## T160:C03 — riscos_validacao

Armadilhas:
- Marcar chamada iniciada como concluída libera dependentes cedo demais.
- Paralelismo teórico do grafo pode exceder capacidade real de GPU ou API.

Métricas sugeridas:
- Tempo total do pipeline e ociosidade de workers.
- Tarefas bloqueadas e violações de dependência.

Testes propostos:
- Inserir ciclo proposital e exigir detecção antes da execução.
- Fazer predecessor falhar e confirmar que descendente não usa saída inexistente.

## T160:C04 — perguntas_proveniencia

Pergunta: Todo workflow de agente é DAG?
Resposta: Não. Agentes frequentemente têm ciclos; é preciso modelá-los separadamente.

Pergunta: Ordem topológica é ordem ótima de execução?
Resposta: Não. Ela respeita dependências, mas não otimiza recursos ou duração sozinha.

Pergunta: Marcar done significa que a tarefa teve sucesso?
Resposta: Para o ordenador, significa liberação topológica; a aplicação deve decidir se essa transição representa sucesso ou outro estado permitido.

Pergunta: Por que pode haver fila mesmo com vários nós prontos?
Resposta: Porque prontidão trata dependências; CPU, memória, quota e concorrência continuam limitando execução.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T160:C05 — mecanismo_avancado

Prontidão topológica e sucesso operacional são estados diferentes. Em graphlib, done informa ao ordenador que um nó foi processado; a biblioteca não comprova que o artefato exigido por seus sucessores existe. O executor precisa decidir se falha bloqueia descendentes, permite alternativa ou satisfaz uma dependência explicitamente tolerante. Em grafos dinâmicos, adicionar trabalho depois do início também requer uma política que o ordenador estático não oferece automaticamente.

Condição de contorno:
Um DAG sem ciclos pode ficar sem progresso por recursos indisponíveis ou por nós considerados prontos com entradas inválidas.

Contrato proposto:
- Entradas: Nós, predecessores, contratos de saída e recursos exigidos.
- Saídas: Conjunto pronto, tarefas bloqueadas e decisões de admissão.
- Estado: Contadores de dependências, estados de execução e versão do grafo.
- Invariante: Um sucessor só recebe disponibilidade semântica quando suas entradas requeridas estão confirmadas.

Compromissos de projeto:
- Grafo estático facilita validação e limita expansão durante execução.
- Grafo dinâmico adapta descoberta e exige mais controle sobre fechamento e detecção de ciclos.

## T160:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: um predecessor termina com erro e outro produz resultado válido; impedir que a simples finalização de ambos libere um sucessor que exige os dois artefatos.

Plano de avaliação proposto:
Comparar execução sequencial e escalonamento por prontidão, com recursos e durações controlados. Medir espera por dependência, utilização, descendentes executados indevidamente e tempo total. Separar benefício topológico de ganho por aumentar hardware.

Comparações:
- T161 (complements): Caminho crítico ajuda a priorizar entre tarefas prontas, mas não muda dependências.
- T147 (complements): Fan-out e junção podem ser subgrafos com critérios explícitos de completude.

Afirmação rastreável:
graphlib oferece prepare, get_ready e done para coordenar processamento topológico, incluindo detecção de ciclos.
Suporte: direct; fontes: C-S024
Limite: Conclusão funcional de uma tarefa não é verificada pelo ordenador topológico.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T160:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava prontidão topológica e sucesso funcional. Esta camada acrescenta artefatos tipados nas arestas, expansão controlada do grafo e reaproveitamento de resultados após invalidação seletiva.

Arestas carregam contratos
Cada dependência deve declarar qual artefato ou propriedade exige. Terminar análise sintática pode liberar edição local, mas não publicação se ainda faltar teste de integração. Distinga dependências de dados, exclusão de recurso e barreiras de qualidade; representar tudo como uma seta sem tipo dificulta explicar por que o nó está bloqueado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, C-S024.

Expansão com fechamento
Permita que a etapa de descoberta produza novos nós, mas defina quando o conjunto descoberto está fechado. Sem essa barreira, um integrador pode terminar antes de chegar a última subtarefa. Valide IDs estáveis, ausência de ciclos e teto de expansão; revisões posteriores abrem uma nova versão do subgrafo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004.

Invalidação mínima
Associe resultados à versão de suas entradas. Quando um arquivo muda, marque como obsoletos apenas descendentes que realmente dependem dele, desde que os contratos permitam essa análise. Um nó com efeitos já publicados exige compensação ou nova versão, não simples apagamento do estado de conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V4C-S004.

USO AVANÇADO — Refatoração entre pacotes
Cenário: Alterar uma API exige consumidores, testes e documentação coordenados.
Estratégia: Construa nós por mudança verificável e arestas por contrato de interface. Paralelize consumidores independentes após fixar o schema. Só libere integração quando todos os artefatos obrigatórios da mesma revisão estiverem aceitos; resultados antigos não satisfazem uma API nova.
Papel do modelo pequeno: 3–7B corrige chamadas; 8–14B analisa dependências locais; 15–30B propõe o grafo.
Aceite proposto: Proposta: nenhum consumidor publicado contra contrato incompatível e redução da espera evitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S004.

USO AVANÇADO — Relatório com fontes independentes
Cenário: Tópicos podem ser investigados em paralelo, mas conclusões se cruzam.
Estratégia: Produza tabelas de evidências por tópico e adie a síntese comparativa até a barreira de cobertura. Se uma contradição exigir consulta adicional, acrescente um subgrafo de resolução com prazo e critério de encerramento.
Papel do modelo pequeno: 8–14B coleta fatos delimitados; integrador maior reconcilia dependências informacionais.
Aceite proposto: Proposta: detectar conclusão emitida antes da cobertura e medir tempo do caminho efetivo até relatório aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar nós pequenos cujo contrato de saída caiba em schema e exemplos.
8–14B: Validar suficiência de artefatos e sugerir subdivisões de um nó bloqueado.
15–30B: Construir dependências e alternativas, submetidas à validação determinística do grafo.
Requisitos de treino/runtime: Executor deve distinguir pronto, em execução, aceito, falho e obsoleto; versionar entradas por aresta.
Não aplicar quando: Não usar DAG rígido para trabalho com ciclos de feedback sem representar a repetição como estado ou expansão limitada.

## T160:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Blueprint e avaliação coordenam dependências e tarefas elegíveis.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Etapas e gates coordenam dependências da implantação.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Orquestração coordena dependências, embora nem todo workflow seja um DAG estático.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Conductor e UpCD sustentam coordenação operacional; a especialização para tarefas de 3–30B e invalidação por artefatos é proposta.
Consultas registradas: V4C-Q003, V4C-Q012.

## T160:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T160 → T148 [complements]
Como combinar: Conductor coordena tarefas e evolução de workflows; o grafo precisa compartilhar estados operacionais com o executor.
Interface: Versão do workflow, estado das tarefas e dependências.
Condição: A semântica de falha e término está definida no fluxo.
Aceite proposto: Não liberar dependente quando predecessor falhou sem alternativa válida.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S004. Casos: V4C-C006.

2. T160 → T161 [feeds]
Como combinar: Calcular caminho dominante sobre dependências e durações observadas para priorizar trabalho pronto.
Interface: DAG versionado e distribuição de duração por nó.
Condição: Estimativas incluem recursos e filas relevantes.
Aceite proposto: Otimização proposta reduz término, não só duração de nó com folga.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Fechar explicitamente a descoberta antes da junção final.
- Separar reexecução de cálculo da repetição de efeito publicado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare ganhos com os mesmos modelos e recursos antes de atribuí-los ao porte. Um DAG bem definido pode tornar tarefas menores viáveis sem resolver planejamento aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T147, T161

## Fontes primárias associadas

### C-S024 — graphlib — Functionality to operate with graph-like structures

[https://docs.python.org/3/library/graphlib.html](https://docs.python.org/3/library/graphlib.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ordenação topológica identifica tarefas liberadas por dependências e detecta ciclos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T161 — Critical Path Analysis

**Nome canônico:** Critical Path Analysis  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T161  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** análise do caminho crítico

## T161:C01 — conceito

Análise da sequência de dependências que determina a menor duração possível de um projeto sob as hipóteses do modelo. No caso clássico, é o caminho de maior duração em um DAG. Otimizar tarefas fora desse caminho pode não reduzir a duração final.

Como funciona:
- Anotar durações estimadas e dependências de cada tarefa.
- Calcular início mais cedo a partir do maior término dos predecessores.
- Determinar folgas e reavaliar o caminho crítico quando durações mudarem.

## T161:C02 — aplicacao

Quando usar:
- Pipelines lentos com várias etapas em paralelo.
- Escolha de onde investir esforço para reduzir latência total.

Quando não usar:
- Tratar estimativas sem filas ou recursos compartilhados como previsão garantida do tempo real.

Implementação proposta:
- Medir tempos de execução e espera separadamente.
- Construir caminho crítico com dados observados e cenários de variação.
- Incluir restrições de recursos na análise quando elas dominarem a duração.

Aplicação LAI proposta:
Proposta: medir o caminho entre pedido e entrega da Helena antes de otimizar tokens, ferramentas ou número de subagentes isoladamente.

## T161:C03 — riscos_validacao

Armadilhas:
- A etapa mais cara isoladamente nem sempre está no caminho crítico.
- O caminho pode mudar depois de uma otimização ou durante uma execução.

Métricas sugeridas:
- Duração prevista versus observada do workflow.
- Folga por tarefa e redução final obtida por melhoria localizada.

Testes propostos:
- Usar grafo pequeno com durações conhecidas e conferir cálculo manual.
- Reduzir duração de etapa fora do caminho e verificar se o tempo total realmente muda.

## T161:C04 — perguntas_proveniencia

Pergunta: Caminho crítico é a tarefa mais lenta?
Resposta: Não necessariamente; é uma sequência dependente que limita a conclusão.

Pergunta: Basta somar médias?
Resposta: Não para estimar cauda ou recursos concorrentes; essas hipóteses precisam ser modeladas.

Pergunta: Somar p95 de cada etapa produz o p95 do workflow?
Resposta: Não. Quantis não se somam dessa forma em geral; dependência estatística e paralelismo mudam a distribuição total.

Pergunta: Duplicar trabalhadores reduz o tempo pela metade?
Resposta: Somente se capacidade for o gargalo dominante e o trabalho puder ser distribuído; dependências podem impor o mesmo limite L.

Escopo das fontes:
Metadados do artigo original foram localizados, mas seu texto não foi aberto por bloqueio 403. Definição matemática geral e roteiro de aplicação são exposição editorial; graphlib sustenta apenas a operação com dependências.

## T161:C05 — mecanismo_avancado

Para tarefas indivisíveis com durações estimadas dᵥ, o comprimento L do maior caminho de dependências é um limite inferior do tempo total. Com m trabalhadores idênticos e trabalho total W=Σdᵥ, outro limite é W/m; assim, max(L,W/m) ajuda a separar gargalo de dependência e capacidade. Não é previsão exata: filas, transferência, recursos específicos e variação das durações podem aumentar o tempo observado.

Condição de contorno:
O caminho crítico calculado com médias pode mudar em cada execução quando ferramentas apresentam caudas de latência longas.

Contrato proposto:
- Entradas: DAG, durações estimadas, quantidade de trabalhadores e restrições de recurso.
- Saídas: Caminhos dominantes, folgas e limites inferiores com hipóteses declaradas.
- Estado: Estimativas versionadas e durações observadas por etapa.
- Invariante: Toda conclusão de economia identifica qual dependência ou restrição realmente encurtou o término.

Compromissos de projeto:
- Priorizar o caminho estimado pode reduzir término e atrasar trabalho independente importante.
- Medições detalhadas melhoram estimativas e introduzem custo de instrumentação.

## T161:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: acelerar uma tarefa com folga e depois uma etapa do caminho dominante; verificar que somente a segunda reduz o término sob as hipóteses originais.

Plano de avaliação proposto:
Comparar previsão e execução em grafos com diferentes larguras, controlando trabalhadores. Medir erro de previsão, mudança de caminho dominante e tempo final. Recalcular após otimizações, pois o gargalo pode migrar para outro ramo.

Comparações:
- T160 (complements): O escalonador respeita dependências e pode usar folga ou caminho remanescente como critério.
- T174 (complements): Prioridade pode incorporar caminho crítico sem ignorar justiça e restrições.

Afirmação rastreável:
LLMCompiler separa planejamento de dependências e execução paralela para reduzir serialização de chamadas.
Suporte: related; fontes: V3C-S002
Limite: Os limites L e W/m são modelagem clássica aplicada editorialmente, não resultados experimentais do pacote.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T161:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 fornecia limites inferiores e folgas. A camada nova usa caminho crítico como instrumento de decisão sob caudas, dependências informacionais e custo de transferência, distinguindo previsão de experimento causal.

Caminho por fase e percentil
Instrumente fila, execução, transferência e validação separadamente. O maior caminho das médias não descreve necessariamente a cauda da missão; uma ferramenta rara e lenta pode dominar o percentil alto. Reconstitua caminhos de traces reais e compare a frequência com que cada etapa impede o término, sem somar percentis como se fossem aditivos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S025, V4C-S004.

Valor de antecipar evidência
Algumas tarefas não estão no maior caminho de duração, mas revelam cedo uma condição que invalida o plano inteiro. Um teste barato de compatibilidade pode merecer execução antes de uma etapa longa. Acrescente ao planejamento o valor de evitar trabalho inútil, mantendo essa heurística separada do cálculo clássico de caminho crítico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S009.

Experimento de aceleração
Antes de contratar um modelo maior para uma etapa, estime quanto sua duração pode cair e qual etapa passará a dominar. Faça teste com limite de recursos constante; se a aceleração aumenta fila de outro consumidor, o ganho local pode desaparecer. Registre também o custo da qualidade perdida quando troca por um modelo menor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S004, V4C-S023.

USO AVANÇADO — Campanha de alterações
Cenário: Milhares de pequenos patches precisam de validação compartilhada.
Estratégia: Meça se o gargalo está na geração, na compilação ou na revisão. Se CI domina, mais agentes só aumentam a fila; agrupe validações compatíveis ou reduza candidatos inválidos antes de enviá-los. Recalcule o caminho depois da mudança porque o gargalo pode migrar.
Papel do modelo pequeno: 3–7B filtra erros locais; 15–30B atua somente nas etapas cognitivas dominantes.
Aceite proposto: Proposta: menor duração total e custo por mudança aceita, mantendo a mesma cobertura de testes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S017.

USO AVANÇADO — Pesquisa com fontes lentas
Cenário: Várias consultas convergem em uma síntese única.
Estratégia: Inicie cedo as fontes de maior latência previsível e faça extração independente enquanto chegam outras respostas. Não comece conclusão que dependa da fonte ausente. Se o deadline vencer, produza estado de cobertura incompleta, sem fingir que otimização de agenda eliminou a lacuna.
Papel do modelo pequeno: 8–14B extrai por fonte; integrador recebe resultados progressivamente identificados.
Aceite proposto: Proposta: tempo até cobertura suficiente e impacto das fontes tardias na resposta final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar pré-checagens baratas e reduzir a entrada de etapas caras.
8–14B: Estimar classes de duração a partir de tarefas históricas sem decidir sozinho o SLA.
15–30B: Decompor planos e identificar dependências informacionais que a telemetria não explica.
Requisitos de treino/runtime: Tracing com causalidade, relógios adequados e distinção entre tempo de serviço e espera; modelos estimativos calibrados.
Não aplicar quando: Não otimizar pela duração média de um nó quando a missão é governada por cauda ou requisito de evidência.

## T161:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Borg e Conductor apoiam análise de recursos e coordenação; não foi encontrado caso operacional que valide esta heurística cognitiva exata.
Consultas registradas: V4C-Q003, V4C-Q018.

## T161:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T161 → T174 [feeds]
Como combinar: Entregar folga e etapa bloqueadora ao escalonador, sem permitir que prioridade viole dependência.
Interface: Grafo, estimativas e classes de recurso.
Condição: Tarefas prontas competem pelo mesmo recurso.
Aceite proposto: Reduzir término da missão sem inanição das demais classes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S025, V3C-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T161 → T147 [complements]
Como combinar: Limitar fan-out ao paralelismo que encurta o caminho e não apenas cria mais candidatos aguardando junção.
Interface: Duração por ramo, fila e critério de junção.
Condição: Ramos independentes e capacidade disponível.
Aceite proposto: Comparar largura e custo sob o mesmo conjunto de tarefas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma etapa acelerada com folga pode não reduzir o término.
- Não atribuir ao modelo um ganho produzido por ampliar hardware ou relaxar critério de conclusão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare configurações por prazo até resultado aceito. Um modelo pequeno pode vencer uma etapa curta; a competência para formular o grafo permanece variável independente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T147, T160, T174

## Fontes primárias associadas

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### C-S024 — graphlib — Functionality to operate with graph-like structures

[https://docs.python.org/3/library/graphlib.html](https://docs.python.org/3/library/graphlib.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ordenação topológica identifica tarefas liberadas por dependências e detecta ciclos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T162 — Idempotência

**Nome canônico:** Idempotência  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T162  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** idempotency

## T162:C01 — conceito

Propriedade de uma operação cuja repetição, com a mesma intenção lógica, não produz efeitos adicionais relevantes. Em APIs, costuma exigir chave de idempotência, armazenamento do resultado e regra para pedidos concorrentes. Não significa que toda resposta de rede será idêntica nem que repetições nunca ocorrerão.

Como funciona:
- Associar a intenção a identificador estável antes da primeira tentativa.
- Registrar processamento e resultado de forma consistente com o efeito.
- Em repetição, devolver estado existente ou reconciliar em vez de repetir efeito.

## T162:C02 — aplicacao

Quando usar:
- Criação de registros, cobranças, mensagens ou jobs sujeitos a retries.
- Workers que podem receber o mesmo evento mais de uma vez.

Quando não usar:
- Reutilizar a mesma chave para intenções diferentes ou parâmetros incompatíveis.

Implementação proposta:
- Vincular chave ao tenant, operação e fingerprint dos argumentos.
- Definir retenção suficiente para a janela de retries e deduplicação.
- Resolver concorrência com transação ou exclusão apropriada.

Aplicação LAI proposta:
Proposta: toda mutação da Helena receber identificador de intenção que sobreviva a reinícios, com recibo consultável.

## T162:C03 — riscos_validacao

Armadilhas:
- Registrar chave depois do efeito deixa janela de duplicação.
- Expirar chave cedo demais permite repetir uma operação antiga.

Métricas sugeridas:
- Número de efeitos de negócio por intenção única.
- Conflitos de chave, duplicatas evitadas e estados incertos reconciliados.

Testes propostos:
- Enviar solicitações iguais simultaneamente e exigir um efeito lógico.
- Repetir chave com argumentos diferentes e exigir erro explícito.

## T162:C04 — perguntas_proveniencia

Pergunta: Idempotência é não repetir chamada?
Resposta: Não. Pode repetir a chamada preservando um único efeito lógico.

Pergunta: Timeout prova que a escrita falhou?
Resposta: Não. O efeito pode ter ocorrido antes da perda da resposta.

Pergunta: Reusar a mesma chave dias depois é sempre seguro?
Resposta: Não. É necessário conhecer retenção e expiração; após remoção, a chave pode criar uma nova operação.

Pergunta: É correto gerar nova chave a cada tentativa?
Resposta: Não para a mesma intenção. Isso elimina a identidade que permite ao servidor reconhecer a repetição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T162:C05 — mecanismo_avancado

Idempotência prática possui horizonte temporal e identidade de payload. Depois de expirar o registro de uma chave, o servidor pode tratar a mesma chave como operação nova. Também precisa decidir o que ocorre quando a chave reaparece com parâmetros diferentes ou enquanto a primeira chamada está em andamento. Na Stripe API v1, respostas são guardadas após início de execução, inclusive erros 500; a documentação distingue esse comportamento da API v2.

Condição de contorno:
Uma chave sem retenção compatível com o período de retry não protege repetições tardias.

Contrato proposto:
- Entradas: Intenção estável, chave, parâmetros normalizados e versão do contrato.
- Saídas: Resultado lógico registrado, conflito de parâmetros ou operação pendente.
- Estado: Chave, digest do pedido, status e prazo de retenção.
- Invariante: A mesma chave não representa duas intenções distintas nem payloads incompatíveis.

Compromissos de projeto:
- Retenção longa amplia proteção e aumenta armazenamento e obrigações de limpeza.
- Reutilizar a resposta facilita repetição e pode conservar um erro que exige diagnóstico por outra via.

## T162:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir a chave com payload alterado, em concorrência e após expiração simulada; verificar os três comportamentos previstos pelo contrato.

Plano de avaliação proposto:
Comparar efeitos reais com e sem chave sob respostas perdidas e reentrega. Controlar período de retenção e normalização. Medir duplicações, conflitos e operações pendentes; a aceitação depende de cobrir o horizonte de repetição esperado.

Comparações:
- T243 (complements): Reconciliação consulta o efeito quando a camada idempotente não fornece conclusão suficiente.
- T150 (distinct_from): Compartilhar uma chamada ativa não conserva necessariamente a intenção após seu término.

Afirmação rastreável:
A Stripe documenta retenção finita, comparação de parâmetros e diferenças de idempotência entre APIs v1 e v2.
Suporte: direct; fontes: V3C-S025
Limite: Essas regras são exemplo concreto; outro serviço pode ter políticas completamente diferentes.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T162:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava expiração e reutilização de chaves. A ampliação modela idempotência como protocolo de intenção, com decisões para duplicatas concorrentes, mudança legítima de objetivo e resultados cujo efeito persiste além da sessão.

Intenção antes de tentativa
Gere o identificador da operação no controlador e persista-o antes do primeiro envio. Todas as tentativas da mesma intenção usam essa identidade, inclusive após reinício. Uma nova intenção com os mesmos parâmetros recebe outra chave; duas instâncias iguais podem ser desejadas. O texto do pedido sozinho não define equivalência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

Reserva e resultado atômicos
No destino, associe chave, parâmetros e estado da operação. Se o processo registra a chave e cai antes do efeito, precisa retomar ou indicar pendência; se realiza o efeito e perde o registro, a deduplicação falha. A implementação deve garantir atomicidade onde possível e usar reconciliação quando atravessa sistemas sem transação comum.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

Efeito versus representação
Uma resposta anterior pode continuar sendo a resposta semântica da tentativa mesmo que o recurso tenha mudado depois. Repetir a chamada não deve recriar um objeto que o usuário apagou legitimamente. Separe consultar o estado atual de repetir a intenção histórica; exponha essa diferença aos agentes que interpretam o resultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S025.

USO AVANÇADO — Criação de ambiente de teste
Cenário: Um agente solicita infraestrutura e perde a conexão durante a criação.
Estratégia: Persista pedido e chave; após timeout, consulte a operação por essa chave. Somente crie nova intenção quando o primeiro resultado estiver reconciliado ou quando o usuário realmente pedir outro ambiente. Expiração do registro exige investigação antes de tentar novamente.
Papel do modelo pequeno: 3–7B preenche parâmetros; código durável administra identidade e reconciliação.
Aceite proposto: Proposta: nenhuma duplicação sob timeout após commit remoto, queda local e resposta atrasada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

USO AVANÇADO — Publicação de artefato
Cenário: A mesma alteração é entregue após retomadas de vários workers.
Estratégia: Identifique publicação por tarefa, revisão base e hash do artefato. Uma segunda tentativa com conteúdo diferente deve falhar como conflito de intenção, não sobrescrever silenciosamente. Para substituir o candidato, crie uma nova revisão e preserve a ligação com a anterior.
Papel do modelo pequeno: 8–14B explica conflitos; 15–30B decide reformulação sem controlar o ledger por linguagem natural.
Aceite proposto: Proposta: duplicata retorna resultado consistente e divergência de payload é detectada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar ações tipadas de escopo restrito com IDs fornecidos pelo runtime.
8–14B: Classificar resposta em concluída, pendente ou conflitante conforme contrato verificável.
15–30B: Planejar compensações e revisões sem confundir nova intenção com nova tentativa.
Requisitos de treino/runtime: Ledger persistente, retenção alinhada ao horizonte de repetição e payload normalizado; evitar IDs gerados de novo após crash.
Não aplicar quando: Não afirmar exatamente uma vez quando o destino não deduplica e o efeito não é consultável.

## T162:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: O contrato documentado controla repetição da mesma intenção no RunInstances.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: EC2 é caso operacional de API idempotente. A aplicação a patches e agentes pequenos é proposta; deduplicação de mensagens não foi confundida com efeito exatamente uma vez.
Consultas registradas: V4C-Q001, V4C-Q019.

## T162:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T162 → T243 [complements]
Como combinar: Resolver efeito desconhecido por identidade antes de escolher retry ou compensação.
Interface: Chave, parâmetros, confirmação remota e janela de retenção.
Condição: O destino permite consulta ou deduplicação verificável.
Aceite proposto: Falha após efeito confirmado não produz uma segunda alteração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T162 → T159 [complements]
Como combinar: Persistir a chave no estado durável para que todas as tentativas representem a mesma intenção.
Interface: Workflow, atividade lógica e identificador externo.
Condição: A identidade sobrevive ao reinício do worker.
Aceite proposto: Reproduzir histórico e repetir atividade mantendo a chave.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mesmo payload pode representar intenção nova; mesmo ID com payload novo é conflito.
- A chave expirada não autoriza presumir que o efeito original nunca ocorreu.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sistemas pelo número de efeitos corretos, inclusive sob falhas. Capacidade linguística superior não substitui atomicidade nem identidade persistente da operação.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T150, T159

## Fontes primárias associadas

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S025 — Stripe API — Idempotent requests

[https://docs.stripe.com/api/idempotent_requests](https://docs.stripe.com/api/idempotent_requests)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: API v1 guarda resposta após início de execução, compara parâmetros e possui retenção finita; API v2 tem semântica distinta explicitada.

Limite: Exemplo concreto de contrato; não generalizar política de retenção ou tratamento de erros a toda API.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T163 — Backoff exponencial com jitter

**Nome canônico:** Exponential backoff with jitter  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T163  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Backoff com Jitter; exponential backoff with jitter; recuo exponencial aleatório

## T163:C01 — conceito

Backoff exponencial com jitter aumenta o intervalo de novas tentativas e adiciona aleatoriedade para distribuir retornos de clientes após falhas transitórias. O crescimento é limitado por um teto, número de tentativas e prazo global. A política controla pressão sobre dependências; não corrige erros permanentes e não torna operações com efeitos seguros para repetição.

Como funciona:
- Classificar a falha e verificar se a operação admite retry dentro do prazo restante.
- Calcular um limite exponencial, por exemplo b_n = min(teto, base × 2^n), com índice inicial documentado.
- Aplicar uma variante definida de jitter; em full jitter, sortear atraso entre zero e b_n, sem sincronizar todos os clientes.

## T163:C02 — aplicacao

Quando usar:
- Erros transitórios de rede, sobrecarga e indisponibilidade temporária quando houver chance concreta de recuperação.

Quando não usar:
- Para repetir credenciais inválidas, entrada malformada ou escrita cujo resultado anterior é desconhecido e não pode ser reconciliado.

Implementação proposta:
- Proposta: definir timeout por tentativa, deadline global e orçamento total de retries; não recomeçar o prazo a cada falha.
- Honrar Retry-After quando aplicável. Se a espera exigida ultrapassar o deadline, encerrar ou reprogramar conforme contrato, sem antecipar a tentativa.
- Coordenar a política em uma camada responsável; retries independentes em cliente, gateway e ferramenta multiplicam carga.
- Persistir attempt, next_attempt_at e idempotency_key em filas duráveis, mantendo a intenção original em todas as tentativas.

Aplicação LAI proposta:
Proposta LAI: usar uma política única e rastreável por operação, integrada à fila e ao circuit breaker, sem declarar sucesso quando todas as tentativas acabarem.

## T163:C03 — riscos_validacao

Armadilhas:
- Usar geradores com semente igual em várias réplicas pode recriar sincronização.
- Um teto por atraso não limita sozinho o tempo total nem a quantidade de chamadas.

Métricas sugeridas:
- Tentativas por operação, taxa de recuperação, atraso acumulado, amplificação de tráfego e deadlines excedidos.

Testes propostos:
- Teste proposto: simular muitos clientes contra falha temporária e verificar dispersão dos horários de retry.
- Injetar erro permanente, Retry-After longo e resposta perdida após escrita; conferir classificação, término e reconciliação.

## T163:C04 — perguntas_proveniencia

Pergunta: Jitter é somar sempre o mesmo atraso?
Resposta: Não. Exige variação aleatória segundo uma distribuição definida; um deslocamento fixo mantém clientes sincronizados.

Pergunta: Posso repetir uma escrita após timeout?
Resposta: Só com garantia adequada de idempotência ou reconciliação. Timeout não informa se o servidor já aplicou o efeito.

Pergunta: Um teto de atraso limita a duração total?
Resposta: Não. Faltam quantidade de tentativas, duração das chamadas, filas e deadline global.

Pergunta: Quota de retries também atrasa a primeira chamada?
Resposta: No mecanismo documentado, não; essa quota limita repetições, e admissão inicial pertence a outro controle.

Escopo das fontes:
AWS fundamenta backoff, jitter e idempotência; RFC 9110 fundamenta Retry-After. Fórmula e testes são receita proposta.

## T163:C05 — mecanismo_avancado

O atraso entre tentativas deve caber junto do tempo da próxima execução no deadline restante. Somar apenas os sleeps subestima a duração total quando cada tentativa leva tempo para falhar. Uma quota de retries adiciona um limite compartilhado de trabalho em falha; ela é diferente do teto de tentativas por chamada. O SDK AWS consultado usa esse tipo de quota e distingue políticas por modalidade e geração do comportamento.

Condição de contorno:
Quando a falha é permanente, esperar mais apenas posterga a mesma rejeição; quando o efeito é incerto, repetir pode ser semanticamente incorreto.

Contrato proposto:
- Entradas: Erro classificado, tentativa, deadline, sinal do servidor e quota de retries.
- Saídas: Próximo instante elegível ou término por orçamento ou erro não repetível.
- Estado: Contador, reserva de tentativa, atraso sorteado e tempo já consumido.
- Invariante: Nova tentativa não começa sem orçamento para seu custo esperado e identificação da intenção.

Compromissos de projeto:
- Janelas maiores reduzem pressão e prolongam recuperação de falhas breves.
- Quota compartilhada protege a dependência e pode negar retries a requisições que individualmente ainda teriam saldo.

## T163:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: cada tentativa demora quase todo o timeout e depois falha; exigir que o prazo global impeça uma sequência que o teto de sleeps permitiria.

Plano de avaliação proposto:
Comparar backoff isolado e backoff com quota global sob incidentes iguais. Medir amplificação de chamadas, recuperação, prazo excedido e dispersão de tentativas. Fixar política de classificação e separar falhas transitórias de permanentes.

Comparações:
- T164 (complements): Retry-After adiciona uma orientação temporal do servidor.
- T228 (complements): Uma fila durável persiste elegibilidade e orçamento entre reinícios.

Afirmação rastreável:
AWS documenta um token bucket de quota que pode encerrar retries quando a capacidade de repetição se esgota.
Suporte: direct; fontes: V3C-S010
Limite: A página distingue comportamento recente com opt-in; não foi assumida configuração efetiva de nenhum SDK LAI.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T163:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 integrava deadline, jitter e quota. Esta camada coordena retries entre camadas, diferencia falha temporária de progresso impossível e propõe controle de amplificação por missão.

Dono único da repetição
Escolha qual camada repete cada tipo de falha e faça as demais exporem suas tentativas. Se SDK, ferramenta e agente repetem independentemente, a multiplicação pode ocorrer antes que o coordenador veja um erro. Propague limite restante e informação de tentativa para impedir que uma nova chamada do agente renove artificialmente todo o orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

Classificação antes de esperar
Backoff é útil quando tempo pode mudar a probabilidade de sucesso. Argumento inválido, schema incompatível ou capacidade ausente exigem correção ou término, não atraso exponencial. Uma rejeição de quota deve considerar o escopo da quota e sinais do servidor; uma falha de transporte após envio pode exigir reconciliação do efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, C-S026.

Estabilidade da recuperação
Após uma falha generalizada, milhares de chamadas podem voltar juntas. Jitter distribui tentativas, mas não cria capacidade. Combine admissão e limite de retries com a carga útil; recuperação sustentada deve preservar espaço para novas requisições, evitando que o trabalho de reparação ocupe permanentemente todo o serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S009.

USO AVANÇADO — Ferramenta externa intermitente
Cenário: Agentes pequenos dependem de uma API com erros transitórios.
Estratégia: Execute a chamada com política central; devolva ao modelo resultado final classificado, incluindo se houve efeito possível. Não peça ao modelo para dormir e repetir por conta própria. Quando a quota de retries acabar, registre pendência ou alternativa compatível.
Papel do modelo pequeno: 3–7B reconhece a classe devolvida; código implementa timers e limites.
Aceite proposto: Proposta: limitar amplificação observada e manter sucesso útil durante degradação controlada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012.

USO AVANÇADO — CI compartilhada saturada
Cenário: Revisores tentam consultar builds que ainda estão executando.
Estratégia: Distinga polling normal de falha de transporte. Aumente o intervalo de consulta conforme duração esperada e respeite eventos quando disponíveis. Repetir o disparo do build não é substituto de consultar seu estado; use ID estável e deadline da campanha.
Papel do modelo pequeno: 8–14B resume falhas de build; 15–30B escolhe mudança de estratégia após evidência suficiente.
Aceite proposto: Proposta: nenhuma duplicação de build e queda no volume de consultas sem atrasar detecção além da tolerância.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Receber estados de falha tipados, sem delegação de controle temporal.
8–14B: Sugerir correção de argumentos quando erro é permanente e há evidência explícita.
15–30B: Planejar fallback ou redução de escopo após orçamento central esgotado.
Requisitos de treino/runtime: Timers monotônicos, contabilidade por tentativa, política do SDK conhecida e propagação do deadline.
Não aplicar quando: Não repetir efeito potencialmente realizado sem identidade ou procedimento de reconciliação.

## T163:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: Backoff e jitter são descritos como mecanismos utilizados nos clientes.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SDK AWS fornece caso operacional de retry com quota. O controlador de missão e polling adaptado para agentes é composição proposta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T163:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T163 → T167 [complements]
Como combinar: SDK AWS usa bucket para limitar tentativas adicionais e conter recuperação agressiva.
Interface: Saldo de retry e classificação da falha.
Condição: Separar quota de retry de admissão inicial.
Aceite proposto: Sob falha sustentada, retries ficam limitados pela política compartilhada.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T163 → T164 [complements]
Como combinar: Interpretar Retry-After como restrição temporal adicional antes da nova tentativa.
Interface: Tempo mínimo anunciado e deadline restante.
Condição: A operação continua elegível para repetição.
Aceite proposto: Não dormir além do prazo nem ignorar orientação válida do destino.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contabilizar tentativas internas do SDK para não ocultar amplificação.
- Esgotar retry deve produzir estado final explícito; não reiniciar o mesmo loop com nome diferente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare qualidade após falhas com mesmo orçamento de tentativas. Um agente pequeno pode obter maior disponibilidade pela engenharia do runtime, sem superar o modelo de fronteira no problema original.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T162, T164, T228, P013

## Fontes primárias associadas

### C-S027 — Timeouts, retries, and backoff with jitter

[https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retries limitados, timeouts e jitter reduzem amplificação de falhas transitórias.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T164 — Retry-After

**Nome canônico:** Retry-After  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** protocol  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T164  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cabeçalho Retry-After

## T164:C01 — conceito

Cabeçalho HTTP que orienta quanto esperar antes de uma solicitação subsequente. Pode conter uma data HTTP ou um número de segundos. É um sinal do servidor que precisa ser interpretado junto com código de resposta, contrato da API, deadline e política de repetição.

Como funciona:
- Ler o cabeçalho e identificar sua forma válida.
- Converter a indicação em instante de próxima tentativa.
- Aguardar somente se a operação puder ser repetida e o prazo total permitir.

## T164:C02 — aplicacao

Quando usar:
- Serviço informa indisponibilidade temporária.
- Resposta de quota fornece um prazo de nova tentativa segundo seu contrato.

Quando não usar:
- Usar o cabeçalho para justificar retry de ação não idempotente sem reconciliar seu estado.

Implementação proposta:
- Suportar segundos e data HTTP com parser robusto.
- Tratar relógio divergente, valor ausente e valor inválido.
- Se a espera ultrapassar o deadline, devolver status explícito em vez de continuar ocultamente.

Aplicação LAI proposta:
Proposta: o cliente HTTP da Helena interpretar o cabeçalho de forma centralizada para que cada integração não implemente uma regra diferente.

## T164:C03 — riscos_validacao

Armadilhas:
- Interpretar segundos como milissegundos causa rajada prematura.
- Repetir antes do instante sugerido aumenta bloqueios e desperdício.

Métricas sugeridas:
- Proporção de tentativas respeitando o instante indicado.
- Falhas de parsing e prazo excedido enquanto aguardava.

Testes propostos:
- Testar data futura, segundos, data passada e valor malformado.
- Fornecer espera maior que o prazo da missão e exigir término ou reagendamento explícito.

## T164:C04 — perguntas_proveniencia

Pergunta: Retry-After é sempre obrigatório na resposta 429?
Resposta: Não se deve presumir; consultar contrato do serviço e tratar sua ausência.

Pergunta: Ele autoriza nova escrita?
Resposta: Não. Só informa espera; segurança da repetição depende da operação.

Pergunta: Se a espera supera meu deadline, devo tentar imediatamente?
Resposta: Não. Isso ignora a orientação adotada; encerrar ou reagendar com prazo explícito preserva o contrato.

Pergunta: Uma data passada deve gerar espera negativa?
Resposta: Não. O parser precisa normalizar esse caso conforme política documentada, mantendo registro do valor recebido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T164:C05 — mecanismo_avancado

Um valor em segundos é relativo ao recebimento da resposta; uma data HTTP requer interpretar relógio de parede. Após calcular a espera, uma implementação pode usar relógio monotônico para evitar que ajustes locais de hora distorçam o timer. Valores inválidos, datas no passado e atrasos maiores que o deadline precisam de tratamento explícito. A orientação do servidor não transforma uma operação insegura para repetição em operação idempotente.

Condição de contorno:
Quando o prazo restante é menor que a espera solicitada, não é possível cumprir ambos; é necessário adiar a missão ou terminar essa tentativa.

Contrato proposto:
- Entradas: Status HTTP, Retry-After bruto, instante de recebimento e deadline.
- Saídas: Espera interpretada, origem do cálculo e decisão de repetir ou encerrar.
- Estado: Valor original, relógio de referência e próxima elegibilidade persistida.
- Invariante: Uma política não repete antes do intervalo que decidiu respeitar apenas para manter seu backoff local.

Compromissos de projeto:
- Respeitar o sinal reduz pressão e pode aumentar latência do cliente.
- Adicionar jitter após o instante mínimo dispersa clientes e amplia espera de alguns deles.

## T164:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: enviar segundos, data futura, data passada e valor inválido, além de alterar o relógio local durante a espera; verificar comportamento documentado e limite global.

Plano de avaliação proposto:
Comparar interpretação completa com parser apenas numérico usando respostas controladas. Medir repetições prematuras, prazo excedido e dispersão temporal. Adotar a política que preserve o contrato do serviço e a semântica da tarefa.

Comparações:
- T163 (complements): Backoff local e orientação do servidor devem formar uma única próxima elegibilidade.
- T162 (complements): Identidade da intenção permanece necessária nas operações repetidas.

Afirmação rastreável:
RFC 9110 permite Retry-After como HTTP-date ou delay-seconds e define segundos após recebimento.
Suporte: direct; fontes: C-S028
Limite: O RFC descreve semântica HTTP; jitter e integração com orçamento são políticas propostas da aplicação.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T164:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciava data HTTP, segundos e relógio monotônico. A camada nova trata Retry-After como sinal compartilhado, combinando destino, tenant e prazo sem transformar uma resposta em bloqueio global indevido.

Escopo do sinal
Associe a orientação à entidade que a resposta realmente limita: recurso, conta, endpoint ou serviço. Um único cliente que esgotou sua quota não deve congelar clientes independentes. Quando o escopo for desconhecido, use política conservadora documentada e telemetria; não deduza independência apenas por URLs diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S009.

Agenda persistente
Converta a espera em elegibilidade futura e retire o worker da execução ativa quando a pausa for longa. Persistir a próxima data evita perder a orientação após reinício. Ao retomar, reconcilie relógio e deadline; um timer antigo não prova que ainda existe orçamento ou que o resultado continua necessário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S023.

Retomada sem avalanche
O horário anunciado pode coincidir para muitos consumidores. Depois da elegibilidade mínima, uma política local de admissão distribui quem realmente envia primeiro. Acrescente atraso somente quando permitido pelo prazo; não subtraia jitter de uma espera mínima válida para antecipar chamadas que o servidor pediu para adiar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, C-S028.

USO AVANÇADO — Coleta de documentos com quota
Cenário: Um lote de agentes recebe limitação do mesmo serviço.
Estratégia: Agrupe o sinal por escopo confirmado, suspenda novas tentativas daquele grupo e preserve outros serviços. No retorno, libere créditos gradualmente e verifique se respostas novas atualizam a orientação. Não carregue o texto inteiro do erro repetidamente no contexto dos agentes.
Papel do modelo pequeno: 3–7B interpreta a classificação já normalizada; runtime administra calendário.
Aceite proposto: Proposta: nenhuma chamada prematura e manutenção de progresso nos destinos independentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S009.

USO AVANÇADO — Missão com prazo curto
Cenário: A espera anunciada supera o tempo restante.
Estratégia: Calcule se ainda cabe executar e validar o resultado. Se não couber, produza falha de prazo ou opção compatível, sem esperar inutilmente. Uma alternativa exige quota independente e preservação das capacidades; o sinal não justifica encaminhar dados a qualquer destino disponível.
Papel do modelo pequeno: 8–14B explica a limitação; 15–30B reformula o plano dentro do escopo autorizado.
Aceite proposto: Proposta: resposta final antes do deadline e ausência de tentativas sem chance de conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V3C-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir estrutura normalizada com atraso e escopo, sem fazer aritmética crítica em texto.
8–14B: Associar operações pendentes ao destino correto e detectar pedido que ficou obsoleto.
15–30B: Planejar alternativas com qualidade e prazo explícitos quando a espera inviabiliza a missão.
Requisitos de treino/runtime: Parser conforme HTTP, relógio confiável, limites para cabeçalhos inválidos e persistência de timers longos.
Não aplicar quando: Não assumir que Retry-After garante disponibilidade no horário indicado ou torna idempotente uma operação.

## T164:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes HTTP e AWS apoiam semântica e retries; não foi encontrado relato específico de dez bigtechs operando esta composição exata em agentes.
Consultas registradas: V4C-Q001, V4C-Q004.

## T164:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T164 → T163 [complements]
Como combinar: A próxima tentativa respeita o sinal do servidor junto de backoff e orçamento local.
Interface: Elegibilidade mínima, classe da falha e tempo restante.
Condição: Todas as restrições devem permitir nova tentativa.
Aceite proposto: Datas passadas, valores inválidos e atraso excessivo têm resultados definidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S028, V2A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T164 → T175 [complements]
Como combinar: A política decide esperar ou usar destino compatível com quota independente.
Interface: Escopo da quota e matriz de alternativas.
Condição: Troca preserva contrato e não mascara o consumo anterior.
Aceite proposto: Evitar circuito entre endpoints que compartilham a mesma limitação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter espera longa em bloqueio de thread ou vaga de GPU.
- Um cabeçalho novo pode alterar a agenda; versionar o sinal para não usar timers obsoletos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sistemas por conclusão dentro do prazo e requisições desperdiçadas. Nenhum porte de modelo consegue eliminar a espera contratual apenas gerando um plano diferente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T162, T163, T175

## Fontes primárias associadas

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T165 — Half-open — estado do Circuit Breaker

**Nome canônico:** Estado half-open do circuit breaker  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T165  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Half-Open Circuit Breaker; circuito parcialmente aberto; sondagem de recuperação do circuito

## T165:C01 — conceito

Half-open é o estado de sondagem de um circuit breaker após um período aberto. Uma quantidade limitada de solicitações testa a recuperação antes de restaurar o fluxo normal. A ficha preserva esse subcomponente com identidade própria para detalhar regras de operação, sem apresentá-lo como mecanismo independente que substitui o circuito completo.

Como funciona:
- Quando o critério de transição for atingido, sair de open para half-open com quota restrita de chamadas.
- Contabilizar sucessos, falhas e latência das sondagens na dependência protegida.
- Fechar o circuito quando o limiar documentado for satisfeito; reabrir diante de falha que indique recuperação insuficiente.

## T165:C02 — aplicacao

Quando usar:
- Dependências que voltam gradualmente e precisam de tráfego de teste antes de receber a carga completa.

Quando não usar:
- Como substituto de health checks abrangentes, correção da dependência ou confirmação de integridade de operações pendentes.

Implementação proposta:
- Proposta: definir quota de sondagens por destino, limite de simultaneidade, timeout e contador de sucessos exigidos.
- Quando houver muitas réplicas, coordenar a quota ou explicitar que o limite é local; um limite por processo pode multiplicar o tráfego global.
- Classificar cancelamento, erro do cliente e falha da dependência separadamente, evitando fechar o circuito com amostra inadequada.
- Usar sondagens representativas e seguras; se envolverem escrita, conservar a mesma disciplina de idempotência das demais chamadas.

Aplicação LAI proposta:
Proposta LAI: expor closed/open/half-open por dependência, com transições registradas e limiares configuráveis avaliados sob falhas controladas.

## T165:C03 — riscos_validacao

Armadilhas:
- Abrir todas as filas ao primeiro sucesso pode derrubar novamente um serviço que recuperou apenas capacidade parcial.
- Um ping superficial pode funcionar enquanto a operação principal continua falhando.

Métricas sugeridas:
- Sondagens simultâneas, taxa e latência de sucesso, tempo em half-open e número de reaberturas após fechamento.

Testes propostos:
- Teste proposto: simular recuperação parcial e confirmar que a quota se mantém enquanto chamadas normais continuam limitadas.
- Fazer uma sondagem falhar e verificar retorno a open, reinício do intervalo e ausência de vazamento de chamadas pendentes.

## T165:C04 — perguntas_proveniencia

Pergunta: Half-open quer dizer liberar metade das requisições?
Resposta: Não. O nome identifica um estado; a quota de teste é definida pela implementação e pode ser apenas uma chamada.

Pergunta: Um sucesso basta para fechar o circuito?
Resposta: Somente se essa for a política validada. Pode ser necessário exigir vários sucessos representativos e condições de latência aceitáveis.

Pergunta: Um sucesso antigo prova recuperação atual?
Resposta: Não. É necessário saber em qual fase e condições a operação foi iniciada e se é representativa da sondagem vigente.

Pergunta: Uma sonda por processo significa uma sonda global?
Resposta: Não. Com várias réplicas, a carga pode multiplicar; o escopo da quota deve ser declarado.

Escopo das fontes:
O padrão Microsoft fundamenta os três estados. Coordenação entre réplicas e aceite LAI são propostas operacionais.

## T165:C05 — mecanismo_avancado

Sondas precisam pertencer à geração correta do estado do circuito. Uma chamada lenta iniciada antes da abertura pode terminar com sucesso durante uma sondagem posterior; usá-la para fechar o circuito confunde evidência antiga com recuperação atual. Uma proposta associa epoch à transição e contabiliza apenas resultados elegíveis daquela fase. Em várias réplicas, a quota efetiva é a soma das sondagens locais, salvo coordenação explícita.

Condição de contorno:
Sondas que exercitam somente uma operação leve não comprovam recuperação da operação que causou a abertura.

Contrato proposto:
- Entradas: Destino, geração do circuito, quota de sondas e critérios de recuperação.
- Saídas: Sonda admitida ou rejeitada e transição fundamentada em resultado vigente.
- Estado: Epoch, sondas em voo, sucessos válidos e prazo de observação.
- Invariante: Resultado atrasado de geração anterior não fecha o circuito atual.

Compromissos de projeto:
- Coordenação global limita rajadas e acrescenta dependência operacional.
- Sondas representativas fornecem evidência melhor e podem custar mais ao serviço ainda frágil.

## T165:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar uma chamada antiga, reabrir o circuito e entregar seu sucesso durante novo half-open; exigir que a resposta obsoleta não determine fechamento.

Plano de avaliação proposto:
Comparar sondagem simples e identificação por geração com falhas intermitentes. Medir fechamento prematuro, carga de sondas e tempo até recuperação sustentável. Escolher critérios pela capacidade que a operação realmente necessita.

Comparações:
- T138 (specializes): Half-open detalha a fase de recuperação da máquina de estados completa.
- T227 (distinct_from): Probe de readiness do processo não substitui sonda da operação protegida.

Afirmação rastreável:
Polly descreve sondagem após o período aberto e transição conforme o resultado, separada de retries.
Suporte: direct; fontes: V3C-S026
Limite: Epochs e coordenação entre réplicas são extensão editorial proposta, não recurso presumido de toda biblioteca.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T165:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 introduzia gerações e limites de sondagem. A expansão escolhe sondas representativas, separa recuperação parcial e explica por que sucesso superficial não autoriza reabrir toda a carga.

Sonda de capacidade real
Uma chamada de saúde barata pode passar enquanto a operação principal continua falhando. Defina uma sonda que exercite o caminho relevante com efeito controlado, ou use uma requisição real elegível sob quota pequena. Diferencie conectividade, aceitação e conclusão semântica; cada evidência sustenta uma transição diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, V3C-S026.

Circuitos por classe
Serviços podem recuperar leitura antes de escrita, ou aceitar prompts curtos enquanto rejeitam contextos grandes. Um circuito único simplifica operação e pode bloquear trabalho saudável; fragmentar demais causa sondas excessivas. Escolha classes com falhas correlacionadas demonstráveis e limite o total agregado de sondas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3C-S009.

Retorno graduado
Ao observar recuperação, aumente carga em etapas com critérios de recuo. Não confunda uma amostra bem-sucedida com capacidade para a fila acumulada. Defina quantos resultados elegíveis, em qual janela e sob qual carga sustentam a decisão; esses valores são parâmetros de operação a calibrar, não constantes da técnica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V2A-S012.

USO AVANÇADO — Provedor de inferência oscilante
Cenário: O endpoint responde a saúde, mas chamadas longas falham.
Estratégia: Separe classes por contrato de entrada quando a evidência justificar. Use poucas solicitações representativas e acompanhe resultado completo, incluindo parser e prazo. Se a classe curta recuperar, libere apenas essa classe enquanto contextos extensos continuam em espera ou fallback.
Papel do modelo pequeno: 3–7B pode servir tarefa curta local; controlador decide abertura e elegibilidade.
Aceite proposto: Proposta: nenhuma reabertura global baseada em sonda inadequada e limite de carga durante recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026.

USO AVANÇADO — Ferramenta de escrita remota
Cenário: Após incidente, é necessário testar uma API com efeitos.
Estratégia: Prefira consulta que verifique a dependência crítica ou uma operação idempotente de teste aprovada. Não use criação repetida de objetos reais como sonda genérica. Se não houver teste seguro representativo, uma requisição real limitada precisa de reconciliação explícita.
Papel do modelo pequeno: 8–14B classifica resposta; 15–30B analisa alternativas de fluxo sem gerar sondas arbitrárias.
Aceite proposto: Proposta: recuperação detectada sem efeitos duplicados ou objetos órfãos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atuar como fallback delimitado; não calcular a saúde do circuito por impressão textual.
8–14B: Agrupar sintomas por tipo de operação e apoiar diagnóstico de recuperação parcial.
15–30B: Propor reorganização do fluxo enquanto circuitos específicos continuam indisponíveis.
Requisitos de treino/runtime: Epoch do circuito, limites globais de sondas, contadores por classe e telemetria de resultado completo.
Não aplicar quando: Não sondar efeitos irreversíveis sem contrato adequado nem usar sucesso de outra geração para fechar o circuito.

## T165:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Resilience4j documenta o estado; AWS/SRE apoiam limites de recuperação. A seleção semântica de sondas para agentes é proposta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T165:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T165 → T138 [complements]
Como combinar: O estado half-open fornece evidência para a transição controlada do breaker.
Interface: Epoch, resultados elegíveis e limite de amostra.
Condição: Conclusões pertencem à geração corrente.
Aceite proposto: Sucesso tardio de chamada antiga não fecha circuito novo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T165 → T173 [complements]
Como combinar: Mantenha fallback elegível enquanto a rota principal passa por recuperação parcial.
Interface: Capacidade restaurada por classe e contrato do pedido.
Condição: Voltar à rota principal não deve reiniciar efeitos já executados.
Aceite proposto: Transferência preserva tentativa, orçamento e resultado confirmado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S001, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contar sondas de todas as réplicas, não apenas de um processo.
- Uma resposta HTTP bem-sucedida com conteúdo inválido não prova recuperação funcional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade e erro semântico sob incidentes reproduzíveis. Trocar por modelo de fronteira não corrige sondas mal escolhidas ou tempestade de reabertura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T138, T163, T227, P013

## Fontes primárias associadas

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T166 — Queue Fairness / Aging

**Nome canônico:** Queue Fairness / Aging  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T166  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** equidade de filas; envelhecimento de prioridade

## T166:C01 — conceito

Políticas que distribuem oportunidades de execução e reduzem inanição de itens na fila. Aging aumenta a prioridade efetiva de uma tarefa conforme sua espera. Equidade pode ser por cliente, peso ou tempo; precisa de definição explícita e capacidade suficiente para atender a carga.

Como funciona:
- Medir espera e participação de cada classe ou cliente.
- Ajustar prioridade ou quota para impedir concentração indefinida.
- Escolher o próximo item entre os que respeitam dependências e limites.

## T166:C02 — aplicacao

Quando usar:
- Filas misturam trabalho interativo e em lote.
- Um tenant pode gerar continuamente mais tarefas que os demais.

Quando não usar:
- Prometer tempo máximo de atendimento sem limitar admissão ou reservar capacidade.

Implementação proposta:
- Definir a unidade de justiça: requisições, tempo de GPU ou custo.
- Aplicar aging com teto ou escalonamento justo por pesos.
- Combinar a política com deadlines e descarte de trabalho expirado.

Aplicação LAI proposta:
Proposta: a Helena reservar atendimento a tarefas interativas sem abandonar rotinas antigas de manutenção e análise.

## T166:C03 — riscos_validacao

Armadilhas:
- Igualdade por número de chamadas favorece pedidos muito caros.
- Aging sem cuidado transforma todo item antigo em urgente e perde diferenciação.

Métricas sugeridas:
- Espera por tenant e percentis por classe.
- Participação de recursos versus pesos contratados e incidência de inanição.

Testes propostos:
- Gerar fluxo contínuo de alta prioridade e verificar progresso dos itens antigos.
- Misturar tarefas curtas e longas e observar justiça na unidade escolhida.

## T166:C04 — perguntas_proveniencia

Pergunta: Aging garante estabilidade sob sobrecarga infinita?
Resposta: Não. É necessário controlar admissão ou aumentar capacidade.

Pergunta: Justiça significa atendimento idêntico?
Resposta: Não necessariamente; pesos diferentes podem ser justos se forem explícitos.

Pergunta: Rodízio de requisições garante equidade de custo?
Resposta: Não quando requisições têm tamanhos diferentes; a unidade distribuída precisa representar o recurso escasso.

Pergunta: Aging resolve sobrecarga ilimitada?
Resposta: Não. Ele reorganiza espera; capacidade insuficiente exige reduzir admissão, reagendar ou rejeitar trabalho.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T166:C05 — mecanismo_avancado

Justiça precisa definir a unidade distribuída: número de requisições, tokens, tempo de serviço ou custo. Atender uma chamada de cada cliente pode ser injusto quando os tamanhos diferem muito. Aging combate espera prolongada, mas não mede sozinho a parcela já consumida. Como referência distinta, o EEVDF acompanha lag de CPU e deadline virtual; transportar essa ideia a agentes exige estimar custo de tarefas que podem não ser preemptíveis.

Condição de contorno:
Nenhuma política garante atendimento finito para todas as classes se a carga sustentada excede a capacidade sem admissão ou descarte.

Contrato proposto:
- Entradas: Itens, cliente, custo estimado, peso e tempo de espera.
- Saídas: Ordem de admissão e justificativa de prioridade efetiva.
- Estado: Serviço acumulado por cliente, espera e dívida de atendimento.
- Invariante: A unidade de justiça permanece explícita e comparável entre clientes.

Compromissos de projeto:
- Aging reduz inanição e pode atrasar tarefas urgentes recém-chegadas.
- Cobrança por custo aproxima equidade e depende de estimativas corrigidas após execução.

## T166:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: um cliente envia tarefas longas e outro tarefas curtas; comparar igualdade por contagem com igualdade por serviço, sem interpretar ambas como a mesma justiça.

Plano de avaliação proposto:
Comparar FIFO, prioridade pura e política com aging ou pesos sob carga admissível e saturada. Medir espera por classe, parcela de serviço e rejeições. Escolher o objetivo de justiça antes de ajustar o algoritmo.

Comparações:
- T149 (complements): A fila implementa ordenação; a política define como a prioridade muda.
- T174 (complements): Escalonamento precisa combinar justiça, capacidade e urgência.

Afirmação rastreável:
EEVDF usa lag para representar parcela de CPU devida e seleciona tarefas elegíveis por deadline virtual.
Suporte: direct; fontes: V3C-S020
Limite: Essa referência de CPU não fornece implementação pronta para chamadas remotas longas e não preemptíveis.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T166:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava justiça por custo e aging. A nova camada trata estimativas manipuláveis, trabalho indivisível e efeitos de prioridades herdadas, para que justiça sobreviva à variação de tarefas LLM.

Crédito estimado e cobrança real
Reserve capacidade por custo previsto e ajuste a dívida após observar consumo. Cobrar apenas pelo número de pedidos favorece requisições grandes; cobrar somente a previsão permite subestimar para furar a fila. Mantenha histórico por classe e limite o desvio admitido, sem punir permanentemente um cliente por uma exceção legítima.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S020, V3C-S009.

Tarefas grandes elegíveis
Um trabalho maior que a parcela normal não pode ficar esperando eternamente por crédito impossível. Divida onde o contrato permitir ou ofereça uma classe de lote com acumulação e limite próprios. Aging deve elevar chance de atendimento sem transformar qualquer tarefa antiga em prioridade absoluta contra toda a carga interativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S020, V3C-S021.

Dependência e justiça
Uma tarefa urgente pode depender de outra classe com prioridade baixa. Propagar urgência pela dependência evita bloqueio, mas deve ser limitado ao trabalho necessário. Não permita que qualquer cliente declare uma dependência artificial para elevar toda sua campanha; a relação deve existir no grafo de artefatos e ser verificável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S016, C-S025.

USO AVANÇADO — Inferência compartilhada
Cenário: Extrações rápidas e análises longas competem pela mesma GPU.
Estratégia: Separe classes com reservas mínimas e contabilize tokens ou tempo efetivo. Em picos, preserve uma fração de progresso para lote; quando a carga interativa cai, empreste capacidade ociosa. Registre retomada da reserva para que empréstimo não vire promessa permanente.
Papel do modelo pequeno: 3–7B atende chamadas curtas; 15–30B recebe trabalhos de maior custo com admissão própria.
Aceite proposto: Proposta: medir espera por classe, cauda e custo efetivo, incluindo tarefas que nunca terminaram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S023.

USO AVANÇADO — Revisão de patches
Cenário: Uma campanha grande não deve bloquear correções pequenas de outras equipes.
Estratégia: Agende por projeto e custo de validação, não pelo volume de patches enviados. Use aging para evitar abandono de revisões lentas e reserve prioridade para dependências que bloqueiam integração já em andamento.
Papel do modelo pequeno: 8–14B estima escopo do diff; runtime decide créditos e exceções rastreáveis.
Aceite proposto: Proposta: limitar concentração por projeto sem degradar a integridade dos testes exigidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Trabalhos curtos previsíveis em classes com overhead pequeno.
8–14B: Estimativas de tamanho e agrupamento de tarefas por perfil operacional.
15–30B: Análise de dependências e identificação de divisões que preservem aceitação.
Requisitos de treino/runtime: Medição de custo real, política de empréstimo e proteção contra tarefas acima da capacidade máxima.
Não aplicar quando: Não afirmar justiça apenas porque a fila é FIFO ou porque cada cliente recebeu uma chamada.

## T166:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Borg sustenta admissão e isolamento, mas não prova este aging exato. Timestone documenta prioridade; não foi contado automaticamente como justiça por custo.
Consultas registradas: V4C-Q004, V4C-Q018.

## T166:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T166 → T149 [complements]
Como combinar: Aging altera a chave efetiva da fila segundo espera e classe, sem violar elegibilidade.
Interface: Prioridade base, idade e custo estimado.
Condição: Atualizações de prioridade têm semântica consistente.
Aceite proposto: Tarefa antiga elegível recebe progresso em carga sustentada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T166 → T174 [complements]
Como combinar: O escalonador implementa reservas e herança limitada de urgência.
Interface: Créditos por classe e dependências bloqueadoras.
Condição: Recursos compatíveis e pontos válidos de preempção.
Aceite proposto: Evitar inversão de prioridade sem sacrificar toda a classe de lote.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S016, V4C-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Excluir tarefas incompletas das métricas pode esconder inanição.
- Uma política justa em tokens pode ser injusta em tempo de GPU; declarar a unidade escolhida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare configurações pequenas e de fronteira por distribuição de espera, além da média de throughput. Justiça é propriedade do serviço, não competência emergente de um modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T149, T174

## Fontes primárias associadas

### C-S029 — Operating Systems: Three Easy Pieces — Scheduling: The Multi-Level Feedback Queue

[https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por prioridades precisa tratar inanição; boosts de prioridade são uma estratégia concreta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S021 — RFC 2697 — A Single Rate Three Color Marker

[https://www.rfc-editor.org/rfc/rfc2697.html](https://www.rfc-editor.org/rfc/rfc2697.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Marcador de tráfego com buckets limitados, taxa comprometida e tamanhos de rajada explicitados.

Limite: RFC descreve marcação de pacotes com dois buckets; limitador simples de chamadas é uma adaptação, não essa especificação integral.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T167 — Token Bucket

**Nome canônico:** Token Bucket  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T167  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** balde de tokens

## T167:C01 — conceito

Algoritmo de limitação com reservatório de capacidade B e reposição de r unidades por segundo. Uma operação consome unidades; se não houver saldo, ela espera ou é rejeitada. Permite rajadas limitadas e controla a taxa média, conforme as condições do contrato.

Como funciona:
- Atualizar saldo por b = min(B, b + r × tempo_decorrido).
- Calcular custo de admissão da operação.
- Deduzir saldo atomicamente quando a operação é admitida.

## T167:C02 — aplicacao

Quando usar:
- API aceita rajadas, mas impõe taxa sustentada.
- Pedidos têm consumo que pode ser modelado em unidades de orçamento.

Quando não usar:
- Usá-lo como único controle de concorrência ou memória ocupada por tarefas longas.

Implementação proposta:
- Usar relógio monotônico para intervalos locais.
- Coordenar saldo em múltiplos workers ou dividir quotas com limite global.
- Definir o que acontece quando uma operação custa mais que a capacidade máxima.

Aplicação LAI proposta:
Proposta: controlar chamadas e orçamento de tokens da Helena em buckets distintos, pois as quotas podem ter unidades diferentes.

## T167:C03 — riscos_validacao

Armadilhas:
- Atualização não atômica permite ultrapassar a quota.
- Reset do processo pode recriar saldo cheio e liberar rajada indevida.

Métricas sugeridas:
- Consumo admitido por janela e tamanho de rajada.
- Tempo de espera e divergência do saldo em concorrência.

Testes propostos:
- Usar relógio controlado e verificar reposição, teto e rejeição sem saldo.
- Fazer consumo simultâneo e garantir que a soma não excede o permitido.

## T167:C04 — perguntas_proveniencia

Pergunta: Bucket token significa token do tokenizer?
Resposta: Não. A unidade é definida pela aplicação, embora possa representar tokens de inferência.

Pergunta: Uma tarefa maior que B entra depois de esperar?
Resposta: Não sem política especial; o saldo nunca ultrapassa B.

Pergunta: Por que um pedido grande pode esperar para sempre?
Resposta: Se seu custo excede a capacidade máxima e a reserva exige o custo integral, nenhuma reposição produzirá saldo suficiente.

Pergunta: A taxa r limita concorrência?
Resposta: Não. Ela limita reposição de crédito; duração das operações determina quantas podem permanecer ativas.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T167:C05 — mecanismo_avancado

Para um bucket simples de capacidade B e reposição r, o saldo após intervalo Δt sem consumo é min(B, saldo+r·Δt). Se uma operação custa q e q>B, ela nunca cabe em uma reserva integral: esperar indefinidamente não resolve. Outra distinção é marcar, atrasar e rejeitar tráfego; token bucket pode apoiar as três políticas, mas elas produzem comportamentos diferentes para o consumidor.

Condição de contorno:
O limite de rajada permite consumo imediato acima da taxa instantânea r; ele não promete espaçamento uniforme entre chamadas.

Contrato proposto:
- Entradas: Custo da operação, saldo, capacidade, taxa e instante de referência.
- Saídas: Admissão, tempo de espera calculado ou rejeição por custo incompatível.
- Estado: Saldo, última reposição e reservas futuras eventualmente emitidas.
- Invariante: O saldo não excede B e reservas concorrentes não gastam o mesmo crédito.

Compromissos de projeto:
- Bucket grande absorve rajadas e pode sobrecarregar uma dependência sensível a simultaneidade.
- Granularidade fina representa custo melhor e amplia contabilidade e sincronização.

## T167:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: acumular saldo até o teto, lançar rajada concorrente e pedir uma operação maior que B; verificar teto, exclusão de dupla reserva e rejeição explícita do pedido impossível.

Plano de avaliação proposto:
Comparar bucket, janela fixa e espaçamento uniforme com a mesma taxa média. Medir rajada admitida, atraso e saturação da dependência. Dimensionar B pela tolerância real a rajadas, sem confundi-lo com quantidade máxima de tarefas simultâneas.

Comparações:
- T137 (complements): Rate limiting define política e escopo; o bucket é um mecanismo possível.
- T166 (distinct_from): Um bucket compartilhado limita volume, mas não distribui automaticamente parcela justa entre clientes.

Afirmação rastreável:
RFC 2697 especifica buckets limitados com taxa de reposição e tamanhos de rajada para marcação de tráfego.
Suporte: related; fontes: V3C-S021
Limite: O RFC usa dois buckets; o contrato de bucket simples para chamadas é uma adaptação editorial.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T167:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 apresentava saldo, capacidade e pedidos grandes demais. A ampliação introduz reservas para custo desconhecido, coordenação entre buckets e contabilização de chamadas canceladas ou parcialmente executadas.

Reserva com liquidação
Para inferência, o custo final pode ser desconhecido antes da chamada. Reserve uma estimativa ou limite permitido e ajuste após receber consumo confiável. Se liberar toda a reserva no cancelamento enquanto o servidor continua gerando, o sistema cria créditos fictícios. Mantenha estado pendente até confirmação ou política conservadora de expiração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021, V2A-S012.

Composição de limites
Uma requisição pode depender de créditos de organização, usuário e recurso. Reservar um bucket e aguardar outro pode reter capacidade sem progresso. Use aquisição coordenada, ordem estável ou devolução controlada; defina se todos precisam estar disponíveis antes do envio. A atomicidade entre processos depende do armazenamento e não surge da fórmula local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021, V3C-S009.

Quota por finalidade
Separe orçamento de tráfego original, retries e sondas. Um bucket único pode deixar a recuperação consumir todos os créditos ou bloquear uma sonda barata que revelaria retorno do serviço. Os limites compartilham um teto superior quando usam a mesma capacidade física, evitando que três quotas independentes somem mais do que o serviço suporta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

USO AVANÇADO — Agentes com saídas variáveis
Cenário: Um assistente ora extrai um campo, ora gera uma análise extensa.
Estratégia: Classifique a operação antes da admissão e reserve segundo o teto da classe. Após concluir, liquide com uso observado. Se a saída atingir o limite, não continue automaticamente com uma segunda chamada sem nova admissão e sem somar o consumo anterior.
Papel do modelo pequeno: 3–7B extrai com teto curto; 15–30B recebe reserva maior apenas quando a tarefa exige.
Aceite proposto: Proposta: saldo consistente com consumo real, inclusive cancelamentos e falhas após envio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S021.

USO AVANÇADO — Recuperação de API degradada
Cenário: Chamadas novas e repetidas disputam capacidade reduzida.
Estratégia: Use bucket de retry além da admissão normal, expondo motivo de recusa ao controlador. Uma tentativa que não obteve crédito ainda não foi enviada; seu estado não deve sugerir efeito remoto incerto. Reabastecimento acompanha política operacional, não decisão improvisada da LLM.
Papel do modelo pequeno: 8–14B reformula o plano após recusa tipada; não cria créditos.
Aceite proposto: Proposta: retries limitados durante falha sustentada e preservação de tráfego útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Operações de custo delimitado tornam reservas mais precisas e baratas.
8–14B: Estimar classe de consumo a partir de tarefa e entrada, validando erro de previsão.
15–30B: Planejar decomposição de chamadas que excedem capacidade sem ocultar custo agregado.
Requisitos de treino/runtime: Relógio monotônico, armazenamento concorrente, unidade de crédito definida e reconciliação de reservas pendentes.
Não aplicar quando: Não esperar indefinidamente por q maior que capacidade nem devolver crédito de trabalho remoto ainda ativo.

## T167:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: O texto identifica token bucket para limitar retries dos SDKs.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SDK AWS documenta uso operacional para retries. Reservas por token e composição de múltiplos escopos são propostas que exigem implementação concorrente correta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T167:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T167 → T163 [complements]
Como combinar: AWS usa créditos de retry para limitar repetição além do backoff temporal.
Interface: Saldo de retry e resultado da tentativa.
Condição: A política distingue chamadas iniciais e adicionais.
Aceite proposto: Falha prolongada não gera tentativas ilimitadas.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T167 → T137 [complements]
Como combinar: O limitador transforma disponibilidade de créditos em admissão e resposta ao solicitante.
Interface: Quantidade reservada, escopo e motivo da rejeição.
Condição: Reserva corresponde a capacidade definida, não a pontuação subjetiva.
Aceite proposto: Nenhum envio ocorre quando os buckets obrigatórios recusam admissão.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

CONTROLES DE FALHA
- Contabilidade local por réplica pode multiplicar uma quota supostamente global.
- Refill baseado em relógio de parede pode criar saldo errado após ajuste de hora.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo e qualidade sob a mesma quota efetiva. Melhor throughput de um modelo pequeno não justifica reservas inconsistentes nem omissão do trabalho cancelado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T175

## Fontes primárias associadas

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S021 — RFC 2697 — A Single Rate Three Color Marker

[https://www.rfc-editor.org/rfc/rfc2697.html](https://www.rfc-editor.org/rfc/rfc2697.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Marcador de tráfego com buckets limitados, taxa comprometida e tamanhos de rajada explicitados.

Limite: RFC descreve marcação de pacotes com dois buckets; limitador simples de chamadas é uma adaptação, não essa especificação integral.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T168 — Soft Limit / Hard Limit de tokens

**Nome canônico:** Soft Limit / Hard Limit de Tokens  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T168  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limites suave e rígido de tokens; Soft Limit / Hard Limit de Tokens

## T168:C01 — conceito

Dois níveis de orçamento: limite suave aciona redução de contexto ou checkpoint; limite rígido impede exceder uma fronteira. Podem ser definidos por chamada ou missão. É necessário distinguir orçamento escolhido pela aplicação do máximo técnico aceito pelo modelo e pelo servidor.

Como funciona:
- Contabilizar consumo acumulado e estimar próximo passo.
- Ao atingir limite suave, resumir estado ou reduzir material opcional.
- Ao atingir limite rígido, encerrar ou recusar nova etapa com status explícito.

## T168:C02 — aplicacao

Quando usar:
- Missões longas com expansão imprevisível do histórico.
- Contratos de custo ou latência que exigem teto verificável.

Quando não usar:
- Interromper no meio de uma mutação sem mecanismo para verificar seu resultado.

Implementação proposta:
- Reservar espaço para mensagem final e persistência do estado.
- Definir limites de entrada, saída e total de missão separadamente.
- Considerar chamadas de especialistas, retries e ferramentas no orçamento total.

Aplicação LAI proposta:
Proposta: a Helena salvar estado antes de esgotar contexto, permitindo retomar com referências e orçamento novo autorizado pela política da missão.

## T168:C03 — riscos_validacao

Armadilhas:
- Aviso suave ignorado deixa o agente sem espaço para concluir.
- Corte rígido pode produzir JSON incompleto e não desfaz ações já realizadas.

Métricas sugeridas:
- Missões que atingem cada limite e taxa de retomada.
- Overflow técnico e custo excedido por erro de contagem.

Testes propostos:
- Forçar limite suave e verificar checkpoint contendo próximos passos e evidências.
- Atingir limite rígido e exigir saída incompleta explícita sem falsa conclusão.

## T168:C04 — perguntas_proveniencia

Pergunta: Soft limit é uma capacidade do modelo?
Resposta: É uma política da aplicação, salvo recurso específico do backend.

Pergunta: Hard limit garante resposta completa?
Resposta: Não. Precisa de reserva e tratamento de truncamento.

Pergunta: Por que não compactar somente ao atingir o máximo?
Resposta: Porque a própria operação ou resultados ainda em voo podem precisar de espaço que já não existe.

Pergunta: Limite suave deve ser um percentual fixo?
Resposta: Não necessariamente. O tamanho da próxima etapa e o custo de recuperação podem ser mais informativos que uma fração constante.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T168:C05 — mecanismo_avancado

Um limite suave precisa deixar margem para a ação corretiva que aciona. Compactar, gerar um handoff ou receber uma ferramenta em andamento também consome contexto; disparar a recuperação no último token disponível pode torná-la impossível. A margem pode considerar distribuição de crescimento por etapa e diferença entre contagem estimada e observada. O limite rígido continua sendo uma fronteira de rejeição, não uma rotina de recuperação.

Condição de contorno:
Se a próxima unidade obrigatória já excede a capacidade restante, apenas elevar o limiar suave não torna a chamada viável.

Contrato proposto:
- Entradas: Ocupação estimada, crescimento pendente, capacidade e custo da recuperação.
- Saídas: Continuar, compactar, dividir ou interromper com estado preservado.
- Estado: Margem reservada, picos observados e gatilhos já acionados.
- Invariante: A ação de recuperação deve caber antes do limite rígido ou usar procedimento externo compatível.

Compromissos de projeto:
- Margem ampla reduz emergências e diminui espaço útil para evidência.
- Gatilhos adaptativos acompanham variabilidade e podem oscilar sem histerese ou controle de reentrada.

## T168:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: entregar resultado grande enquanto uma compactação é planejada; verificar que a reserva inclui o material pendente e evita repetidas compactações sem ganho.

Plano de avaliação proposto:
Comparar limiares fixos e margens baseadas em tamanhos observados. Controlar ferramentas e modelos. Medir estouros, recuperação concluída, informação preservada e compactações redundantes. Definir fronteiras por carga e custo de continuidade.

Comparações:
- T152 (complements): A alocação distribui cotas; os limites determinam quando mudar de estratégia.
- T212 (complements): Auto-compact é uma resposta possível ao gatilho suave, não sua definição completa.

Afirmação rastreável:
A contagem antecipada pode considerar mensagens e ferramentas estruturadas para orientar tamanho de entrada.
Suporte: related; fontes: V3C-S022
Limite: As fronteiras suave/rígida e a reserva de recuperação são desenho editorial, não comportamento universal do endpoint.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T168:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 enfatizava margem para recuperação. Esta camada diferencia limite de raciocínio, resposta, contexto e consumo acumulado, com uma política de degradação que termina em artefato útil e verificável.

Quatro fronteiras distintas
Mantenha contadores para entrada total, saída visível, raciocínio quando exposto pelo backend e orçamento da missão. Um teto de saída não impede o histórico de crescer; uma janela disponível não autoriza gastar indefinidamente. Expresse qual limite é imposto pelo servidor e qual é apenas gatilho do controlador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V3C-S022.

Limite suave condicionado
O ponto de ação deve depender do próximo passo. Receber um log grande exige margem diferente de emitir JSON curto. Antes de chamar ferramenta com saída imprevisível, negocie paginação ou projeção; se não existir limite de payload, o controlador precisa tratar o resultado fora da janela antes de apresentá-lo ao modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S018.

Finalização reservada
Reserve capacidade para registrar estado, evidências e pendências. A resposta final parcial deve distinguir o que foi verificado do que ficou sem executar. Cortar no meio de uma chamada de ferramenta ou de um JSON pode deixar artefato inutilizável; trate truncamento como falha de contrato e preserve o último resultado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S022, V4C-S018.

USO AVANÇADO — Modelo de raciocínio local
Cenário: Um 9B pode consumir orçamento em raciocínio antes de responder.
Estratégia: Teste limites com o backend real e observe a diferença entre pedido de interrupção e término efetivo. A documentação Nemotron mostra controle específico de thinking; não suponha que o parâmetro seja uma barreira rígida idêntica em todos os servidores. Defina reserva para a saída validável.
Papel do modelo pequeno: 8–14B executa raciocínio delimitado; um controlador externo contabiliza a conclusão.
Aceite proposto: Proposta: taxa de respostas completas, consumo acima do alvo e qualidade por faixa de orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

USO AVANÇADO — Análise de repositório extensa
Cenário: O agente se aproxima do limite antes de terminar o patch.
Estratégia: Interrompa expansão de arquivos, salve a revisão e um plano de continuação, e valide o que já foi editado. Uma nova sessão recebe apenas objetivos pendentes e referências. Não declare concluído porque o limite rígido encerrou a geração.
Papel do modelo pequeno: 3–7B atua em trechos; 15–30B integra lotes com reservas explícitas.
Aceite proposto: Proposta: retomada sem perder alterações confirmadas e sem aceitar JSON ou patch truncado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Saídas curtas e schemas simples reduzem risco de consumir a reserva de finalização.
8–14B: Raciocínio condicionado ao orçamento, medido no backend que realmente servirá o modelo.
15–30B: Dividir análises longas em estágios com checkpoint e critérios de integração.
Requisitos de treino/runtime: Contador por tokenizer, telemetria do provedor e tratamento de finish reason; margem baseada em payload observado.
Não aplicar quando: Não tratar orçamento de thinking como limite universal nem compactar quando já não cabe a própria compactação.

## T168:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: Limiar de thinking e limite final de geração têm semânticas diferentes.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron oferece evidência direta de modelo dentro da faixa pedida e controles documentados; implantação específica e ganhos locais não foram demonstrados.
Consultas registradas: V4C-Q014, V4C-Q027.

## T168:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T168 → T222 [feeds]
Como combinar: Publicar consumo e margem para disparar ação antes do limite rígido.
Interface: Contadores por categoria e estimativa do próximo payload.
Condição: Medidas distinguem uso observado de previsão.
Aceite proposto: Gatilho ocorre com espaço para a ação corretiva escolhida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T168 → T211 [complements]
Como combinar: Ao atingir limite suave, gerar passagem de estado antes de perder a capacidade de registrar pendências.
Interface: Objetivos, revisão, artefatos e próximo passo.
Condição: Handoff precisa ser validado e persistido antes do encerramento.
Aceite proposto: Nova sessão retoma sem inventar conclusão das etapas ausentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Timeout, limite de tokens e término normal precisam de estados diferentes.
- Uma saída válida sintaticamente ainda pode ter omitido requisito para caber no teto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas de qualidade por orçamento em vez de uma única configuração. O 9B documentado é recurso concreto, mas sua existência não demonstra equivalência geral a modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T060, T152, T176

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T169 — Multi-Agent com contextos isolados

**Nome canônico:** Multi-Agent com Contextos Isolados  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T169  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** subagentes com contexto separado; Multi-Agent com Contextos Isolados

## T169:C01 — conceito

Arquitetura em que especialistas trabalham em contextos separados e trocam resultados por contratos ou artefatos. Evita que todo histórico de cada especialidade ocupe o coordenador. Isolamento de contexto não é isolamento de segurança: arquivos, credenciais e ferramentas podem continuar compartilhados.

Como funciona:
- Delegar subtarefa com objetivo, entradas e critérios de aceite delimitados.
- Cada especialista executa usando apenas contexto necessário.
- Consolidar evidências e divergências em um ponto de decisão definido.

## T169:C02 — aplicacao

Quando usar:
- Pesquisa paralelizável e auditoria por módulos.
- Conjunto de informações excede o contexto útil de um único agente.

Quando não usar:
- Tarefa depende de estado compartilhado mutável atualizado continuamente entre todos os agentes.

Implementação proposta:
- Definir quem pode escrever cada artefato e quem decide integração.
- Exigir resultados com fontes, limitações e referências estáveis.
- Estabelecer orçamento agregado e procedimento para resultados conflitantes.

Aplicação LAI proposta:
Proposta: manter Helena como coordenadora e especialistas consultivos com contextos delimitados, preservando um responsável explícito pelas mutações.

## T169:C03 — riscos_validacao

Armadilhas:
- Especialistas podem repetir trabalho ou omitir dependências.
- Resumo do coordenador pode distorcer detalhes; preservar artefato original evita parte da perda.

Métricas sugeridas:
- Cobertura, duplicação e custo total por missão.
- Erros de integração e divergências resolvidas com evidência.

Testes propostos:
- Dar fatos contraditórios a especialistas e exigir que a consolidação preserve o conflito.
- Matar um agente e verificar que o coordenador detecta lacuna de cobertura.

## T169:C04 — perguntas_proveniencia

Pergunta: Contextos isolados tornam agentes independentes de verdade?
Resposta: Não. Podem compartilhar modelo, fontes e erros correlacionados.

Pergunta: Mais agentes sempre ajudam?
Resposta: Não. Coordenação e consumo podem superar o ganho em tarefas pouco separáveis.

Pergunta: Dois agentes com contextos separados podem sobrescrever o mesmo arquivo?
Resposta: Sim, se compartilham a árvore de trabalho; é necessário separar responsabilidade ou controlar versões.

Pergunta: Como avaliar se delegar economizou?
Resposta: Contabilizar coordenação, resumos, merge e correções no custo total do objetivo, além do trabalho de cada agente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T169:C05 — mecanismo_avancado

Isolar contexto muda a distribuição de informação entre agentes, mas cria custo de integração. Um resumo final pode perder exceções descobertas pelo especialista; por isso, o retorno proposto inclui artefatos, evidências, versões de entrada e pendências. Se agentes compartilham diretório, escritas concorrentes continuam possíveis. Contexto separado e exclusão de escrita são propriedades independentes, assim como custo faturado por cada agente.

Condição de contorno:
A delegação pode piorar tarefas curtas ou fortemente acopladas quando a comunicação custa mais que o trabalho paralelo aproveitável.

Contrato proposto:
- Entradas: Submissões delimitadas, versões comuns, recursos atribuídos e critério de entrega.
- Saídas: Resultado por agente, artefatos, fontes e conflitos identificados.
- Estado: Responsáveis por arquivos, bases de edição e estados dos ramos.
- Invariante: O coordenador não confunde resumo do especialista com evidência completa de alteração ou teste.

Compromissos de projeto:
- Especialização concentra informação relevante e pode ocultar premissas necessárias à integração.
- Isolamento de escrita reduz conflito e exige etapa explícita de merge.

## T169:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois agentes recebem a mesma base e produzem mudanças incompatíveis no mesmo contrato; exigir detecção da divergência antes de consolidar ambos.

Plano de avaliação proposto:
Comparar agente único e divisão por responsabilidades com orçamento total equivalente. Medir qualidade integrada, retrabalho, tokens de comunicação e tempo final. A decisão deve considerar resultado do conjunto, não apenas rapidez individual de cada agente.

Comparações:
- T237 (complements): Offloading define a unidade delegada; isolamento de contexto define parte da fronteira de execução.
- T239 (complements): Worktrees podem separar árvores de edição, sem substituir contratos de integração.

Afirmação rastreável:
Claude Code documenta subagentes com contexto próprio e consumo de solicitações associado ao mesmo conjunto de limites.
Suporte: direct; fontes: V2A-S018
Limite: Inicialização, ferramentas e permissões variam por tipo e versão; não se presume isolamento de sistema operacional.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T169:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava isolamento de contexto e exclusão de escrita. A camada nova define fronteiras de conhecimento, contratos de retorno e seleção de trabalhadores pequenos conforme a verificabilidade de cada subtarefa.

Pacote mínimo suficiente
O trabalhador recebe objetivo local, entradas necessárias, critérios de aceite e limites da conclusão. Não envie toda a conversa apenas para parecer completo. Inclua exceções capazes de mudar a decisão: uma tarefa de remoção de código precisa saber quais comportamentos preservar. Isolamento útil reduz distração sem amputar dependências informacionais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Resultado com evidência recuperável
Peça artefato e referências precisas, não apenas um parágrafo de confiança. O integrador deve conseguir reabrir a evidência e descobrir o que foi inferido, testado ou deixado pendente. Se um resultado depende de uma versão antiga, essa incompatibilidade precisa aparecer antes da síntese, mesmo que o texto final pareça coerente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Diversidade de papéis e falhas
Especializar por objeto ou propriedade reduz mistura de responsabilidades, mas agentes do mesmo modelo ainda compartilham vieses. Faça verificação por mecanismos diferentes quando possível: parser, compilador e teste de execução. Revisores independentes de contexto podem detectar problemas distintos sem se tornarem provas independentes de verdade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, C-S030.

USO AVANÇADO — Revisão por propriedade
Cenário: Um patch deve preservar comportamento e não introduzir mudanças fora de escopo.
Estratégia: Dê a cada revisor uma propriedade e acesso ao diff e às evidências pertinentes. Agregue resultados identificando exatamente qual propriedade falhou; não use maioria para anular uma violação obrigatória. Reabra evidência quando houver conflito entre revisores.
Papel do modelo pequeno: 3–7B faz checklist estreito; 8–14B examina relações locais; 15–30B integra conflitos.
Aceite proposto: Proposta: detectar violações inseridas e medir falsos bloqueios por propriedade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

USO AVANÇADO — Pesquisa especializada
Cenário: Fontes técnicas pertencem a ecossistemas distintos.
Estratégia: Divida por pergunta verificável, distribua orçamento e exija fonte primária com data. O integrador verifica se dois trabalhadores citaram a mesma evidência antes de tratá-los como confirmação independente. Encaminhe lacunas específicas, sem repetir a missão inteira para cada agente.
Papel do modelo pequeno: 8–14B extrai por documento; integrador maior resolve contradições e limites.
Aceite proposto: Proposta: cobertura por questão, duplicação de coleta e custo total de coordenação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefas estreitas, com entradas curtas e saída verificável por contrato.
8–14B: Especialistas com poucos documentos e critérios claros de abstenção.
15–30B: Integração de dependências e conflitos; não delegar mais contexto do que o próximo passo exige.
Requisitos de treino/runtime: Registro de versões, artefatos compartilhados com dono e política de concorrência; contabilização por agente.
Não aplicar quando: Não dividir uma decisão cuja evidência precisa ser comparada conjuntamente sem preservar ponte de integração.

## T169:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Subagentes possuem contextos próprios no sistema relatado.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Subagentes delimitados usam modelo padrão mais econômico que o principal.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Arquitetura multiagente é mencionada sem especificação de isolamento.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e harnesses Uber fornecem casos operacionais. O papel por faixa de parâmetros é proposta: as fontes não informam que os trabalhadores usados sejam 3–30B.
Consultas registradas: V4C-Q009, V4C-Q010.

## T169:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T169 → T237 [complements]
Como combinar: Claude Research distribui tarefas a subagentes e recebe resultados com referências para integração.
Interface: Objetivo local, orçamento e artefato retornado.
Condição: Tarefas distinguíveis e mecanismo de reunião.
Aceite proposto: Verificar suficiência do retorno antes de declarar cobertura.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T169 → T171 [complements]
Como combinar: Harness Uber diferencia perfis de cache entre interação e subagentes, articulando contexto e custo.
Interface: Perfil de sessão, prefixo estável e política de retenção.
Condição: Compatibilidade do provedor e configuração atual.
Aceite proposto: Medir economia sem misturar estados incompatíveis.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

CONTROLES DE FALHA
- Contexto separado não impede dois agentes de escreverem no mesmo arquivo.
- Confirmações que derivam da mesma fonte ou do mesmo erro não contam como evidências independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare uma equipe pequena com um agente de fronteira sob orçamento total equivalente. Ganhos em tarefas paralelizáveis não significam superioridade em raciocínio indivisível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T139, T147, T186, T200

## Fontes primárias associadas

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T170 — Tool Schema Versioning

**Nome canônico:** Tool Schema Versioning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T170  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** versionamento de schemas de ferramentas

## T170:C01 — conceito

Versionamento dos contratos de entrada e saída das ferramentas para que clientes conheçam sua semântica e compatibilidade. Um schema pode continuar sintaticamente válido enquanto o significado mudou. Versão precisa abranger unidades, enums, efeitos, erros e regras relevantes, não apenas nomes de campos.

Como funciona:
- Identificar a versão do contrato disponível e a versão esperada pelo cliente.
- Validar compatibilidade antes de aceitar chamada.
- Migrar ou rejeitar explicitamente quando a mudança quebra o contrato.

## T170:C02 — aplicacao

Quando usar:
- Integrações evoluem com vários agentes consumidores.
- Missões duráveis podem retomar depois de atualização de ferramenta.

Quando não usar:
- Alterar significado de campo mantendo versão e esperar que agentes deduzam a mudança.

Implementação proposta:
- Guardar schemas imutáveis com identificador e changelog.
- Testar consumidores antigos contra alterações aditivas e restritivas.
- Fixar versão por execução e definir política de descontinuação.

Aplicação LAI proposta:
Proposta: os contratos recuperados pelo RAG da Helena carregarem versão e validade; o executor confirmar a versão antes de agir.

## T170:C03 — riscos_validacao

Armadilhas:
- Campo opcional novo pode quebrar consumidor estrito.
- Remover enum usado por missão antiga impede replay ou retomada.

Métricas sugeridas:
- Falhas por incompatibilidade e tempo de migração.
- Cobertura de testes de contrato para versões ainda suportadas.

Testes propostos:
- Reexecutar exemplos antigos contra a nova versão e classificar diferenças.
- Tentar chamada com versão desconhecida e exigir erro específico, sem coerção silenciosa.

## T170:C04 — perguntas_proveniencia

Pergunta: MCP versiona automaticamente meu schema de negócio?
Resposta: Não. A aplicação precisa manter seu próprio contrato e compatibilidade.

Pergunta: Adicionar campo é sempre seguro?
Resposta: Não. Depende do comportamento dos consumidores e validadores.

Pergunta: Adicionar campo opcional é sempre retrocompatível?
Resposta: Não. Consumidores que rejeitam propriedades extras podem falhar ao receber o novo campo.

Pergunta: Como detectar mudança de segundos para milissegundos?
Resposta: Registrar unidade no contrato e usar casos de domínio; ambos os valores continuam sendo números válidos para um schema genérico.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T170:C05 — mecanismo_avancado

Compatibilidade possui direções diferentes: um servidor novo aceitar pedidos antigos não implica que um cliente antigo aceite respostas novas. Acrescentar um campo opcional pode quebrar um consumidor com objeto fechado; acrescentar valor a enum pode invalidar um switch exaustivo. Mudanças de unidade ou significado podem passar em todos os schemas e ainda alterar o comportamento. Uma matriz de produtor e consumidor torna essas diferenças verificáveis.

Condição de contorno:
Versionar apenas o arquivo JSON é insuficiente quando defaults, efeitos ou semântica de erro mudam sem alteração estrutural.

Contrato proposto:
- Entradas: Contrato antigo e novo, clientes suportados, exemplos e semântica de domínio.
- Saídas: Classificação de compatibilidade, estratégia de migração e revisão efetiva.
- Estado: Schemas publicados, consumidores conhecidos e janela de coexistência.
- Invariante: A revisão identifica significado dos campos e comportamento, não somente sintaxe.

Compromissos de projeto:
- Manter versões paralelas facilita migração e multiplica testes e suporte.
- Aceitar campos desconhecidos melhora extensibilidade e pode ocultar erros de digitação importantes.

## T170:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar um valor de enum e alterar uma unidade preservando o tipo numérico; verificar quebra estrutural no primeiro caso quando aplicável e detecção semântica no segundo.

Plano de avaliação proposto:
Executar matriz de pedidos e respostas entre versões com fixtures independentes. Medir incompatibilidades, migrações exigidas e divergências silenciosas. Decidir compatibilidade pelos consumidores reais, sem tratar toda adição como mudança segura.

Comparações:
- T158 (complements): O registro precisa anunciar e conservar as revisões dos contratos.
- T141 (complements): Schema delimita estrutura, mas a migração também precisa de testes de significado.

Afirmação rastreável:
JSON Schema diferencia propriedades permitidas e avaliadas, afetando a aceitação de extensões de objetos.
Suporte: direct; fontes: V3C-S013
Limite: A compatibilidade de negócio exige critérios adicionais que o schema não consegue expressar sozinho.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T170:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia compatibilidade estrutural e semântica. A expansão considera coexistência de consumidores, migração de resultados pendentes e o efeito das descrições sobre a escolha de ferramentas pela LLM.

Versão de comportamento
Versione unidades, defaults, efeitos e interpretação de erros junto do schema. Adicionar um campo opcional pode alterar o padrão escolhido pelo modelo mesmo quando o parser continua aceitando a resposta. A compatibilidade deve ser decidida em trajetórias de uso, incluindo quem produz argumentos e quem interpreta o retorno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S013.

Matriz produtor-consumidor
Mantenha fixtures de pedidos e respostas para as combinações que coexistirão. Um adaptador não deve inventar valor necessário ausente na versão antiga; precisa rejeitar ou representar ausência explicitamente. Mudanças de enum merecem casos de desconhecido, porque um consumidor pode receber valor novo antes de ter sido atualizado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S013, V4C-S013.

Execuções em trânsito
Uma tarefa longa pode ter escolhido ferramenta com descritor antigo e invocá-la depois de um deploy. Revalide a revisão no momento de agir e registre qualquer tradução aplicada. Se a mudança altera intenção, volte ao planejamento; preservar o formato JSON não demonstra que o efeito desejado continua o mesmo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S018.

USO AVANÇADO — API com mudança de unidade
Cenário: Um serviço passa a devolver duração em outra escala.
Estratégia: Publique contrato explícito com unidade, migre consumidores e use exemplos numéricos de domínio para detectar conversões erradas. Proíba que a LLM deduza unidade pela ordem de grandeza. Durante convivência, anexe versão e normalize num adaptador determinístico antes de apresentar dados ao agente.
Papel do modelo pequeno: 3–7B interpreta dados já normalizados; 8–14B auxilia inventário de consumidores.
Aceite proposto: Proposta: matriz de versões sem conversões silenciosas ou valores plausíveis porém incorretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S013.

USO AVANÇADO — Catálogo de ferramentas renovado
Cenário: Uma descrição nova melhora descoberta, mas muda seleção de chamadas.
Estratégia: Compare consultas representativas contra os dois catálogos, incluindo nomes parecidos e operações com efeitos diferentes. Faça publicação gradual por tarefas elegíveis; conserve histórico do catálogo usado em cada execução para investigar regressão.
Papel do modelo pequeno: 15–30B propõe descrição; seletores pequenos são avaliados com o mesmo conjunto de consultas.
Aceite proposto: Proposta: nenhum aumento de escolha de ferramenta semanticamente incompatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Contratos estáveis e enums curtos, com rejeição explícita de valores desconhecidos.
8–14B: Adaptar representações após validação e classificar mudanças por consumidor afetado.
15–30B: Analisar migrações entre serviços, sem substituir testes de compatibilidade.
Requisitos de treino/runtime: Catálogo versionado, fixtures independentes e tradução determinística de campos com significado preciso.
Não aplicar quando: Não tratar semver, nome do endpoint ou sucesso de parsing como prova completa de compatibilidade.

## T170:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: O gateway documenta diffs, revisão e rollback de configuração/descritores; isso não prova uma política completa de versionamento e compatibilidade semântica de entrada e saída.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

V4C-C013 — Uber / GenAI Gateway
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A Uber relata equipes internas utilizando o gateway para consultas a modelos externos e hospedados internamente.
Mecanismo documentado: Adaptadores expõem uma interface comum e integram autenticação, política de dados, métricas e atribuição de custos.
Correspondência com esta base: Tradução de interfaces ilustra compatibilidade, mas a fonte não demonstra versionamento integral de schemas de ferramentas.
Transferência proposta para modelo pequeno: Proposta: centralizar adapters de 3–30B e registrar capacidades reais de cada endpoint; separar seleção do modelo da tradução de protocolos e da medição do custo por tarefa aceita.
Limite: Interface compatível não torna modelos semanticamente equivalentes. Não mapear automaticamente disponibilidade de múltiplos fornecedores a cascata ou fallback comprovado.
Fontes: V4C-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber documenta controle de configuração e registro; a matriz completa de compatibilidade e suas bandas de modelos são propostas de engenharia.
Consultas registradas: V4C-Q009, V4C-Q013.

## T170:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T170 → T158 [complements]
Como combinar: Proposta: vincular revisão semântica do contrato à publicação de descritores, estendendo a governança de configuração do gateway.
Interface: Revisão do contrato, dono e configuração habilitada.
Condição: A versão executável corresponde à definição recuperada.
Aceite proposto: Rollback de catálogo preserva explicação das execuções antigas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T170 → T141 [complements]
Como combinar: Validar estrutura antes de aplicar testes semânticos e regras de domínio.
Interface: Schema, instância e versão declarada.
Condição: Campos desconhecidos e obrigatórios têm política explícita.
Aceite proposto: Casos válidos sintaticamente mas errados em unidade são rejeitados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Um adaptador pode produzir saída válida e semanticamente falsa; testar significado.
- Não alterar um contrato já referenciado sem preservar identidade histórica.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos na migração de exemplos delimitados, com o mesmo adaptador e validação. Robustez do contrato não deve ser atribuída a raciocínio superior do agente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T158, T159

## Fontes primárias associadas

### C-S007 — Tools — Model Context Protocol, 2025-06-18

[https://modelcontextprotocol.io/specification/2025-06-18/server/tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ferramentas expõem nome, schema, descoberta e chamada por contrato; protocolo não concede autorização de negócio.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T171 — Cache-Aware Orchestration

**Nome canônico:** Cache-Aware Orchestration  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T171  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** orquestração orientada a cache

## T171:C01 — conceito

Orquestração que considera possibilidade de reutilizar contexto ou resultados ao ordenar chamadas e escolher destinos. É uma política de sistema: um backend com prefixo reutilizável pode economizar prefill, mas esperar por ele pode aumentar a latência. A decisão deve avaliar o custo total.

Como funciona:
- Identificar partes estáveis e identidade de cache aplicável.
- Estimar benefício de reutilização junto com fila e carga do destino.
- Organizar chamadas sem violar dependências, atualidade ou isolamento.

## T171:C02 — aplicacao

Quando usar:
- Muitas tarefas usam instruções e documentos iguais.
- Múltiplas réplicas têm estados de cache diferentes.

Quando não usar:
- Maximizar acerto de cache sacrificando qualidade, permissão ou prazo da tarefa.

Implementação proposta:
- Manter prefixo estável quando o contrato permitir.
- Incluir versões e contexto de autorização nas chaves necessárias.
- Comparar política orientada a cache com balanceamento simples sob carga realista.

Aplicação LAI proposta:
Proposta: alinhar montagem de contexto da Helena com o cache do runtime somente depois de medir comportamento do servidor usado.

## T171:C03 — riscos_validacao

Armadilhas:
- Agrupar pedidos pode aumentar espera mais que economiza computação.
- Alterações pequenas no prefixo invalidam benefício estimado.

Métricas sugeridas:
- Tokens de prefill evitados e latência de cauda.
- Custo total incluindo fila, recomputação e invalidação.

Testes propostos:
- Variar tamanho de prefixo compartilhado e carga para medir ponto de benefício.
- Atualizar documento ou política e exigir invalidação correta.

## T171:C04 — perguntas_proveniencia

Pergunta: Prefixo estável sempre é melhor?
Resposta: Não se ele inclui conteúdo desnecessário ou desatualizado.

Pergunta: Cache-aware routing é a mesma coisa que semantic routing?
Resposta: Não. Um usa estado de reutilização; o outro usa significado da solicitação.

Pergunta: Mais cache hit significa menor latência sempre?
Resposta: Não. Uma fila longa ou custo de transferência pode superar a economia de prefill.

Pergunta: Cache miss após o roteamento deve mudar a resposta?
Resposta: Não por si. O backend deve recomputar o prefixo compatível; cache afeta custo e tempo, não a intenção da tarefa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T171:C05 — mecanismo_avancado

A afinidade de cache deve competir com o custo de fila. Uma rota com prefixo reutilizável pode ser mais lenta que outra fria se estiver congestionada. Uma estimativa proposta soma espera, prefill não reutilizado, transferência e decode esperado. A informação de residência também envelhece: um bloco anunciado pode ser removido antes da admissão. O plano precisa tolerar cache miss sem alterar correção da resposta.

Condição de contorno:
Quando decode ou ferramenta externa domina o tempo, economizar prefill pode ter efeito pequeno sobre a latência final.

Contrato proposto:
- Entradas: Prefixos identificados, residência estimada, carga dos destinos e requisitos do modelo.
- Saídas: Rota elegível e expectativa separada de economia e espera.
- Estado: Hashes, versões, acertos observados e idade da telemetria.
- Invariante: Uma decisão por cache nunca troca modelo ou contexto incompatível apenas para aumentar acertos.

Compromissos de projeto:
- Afinidade aumenta reutilização e pode concentrar tráfego em poucos workers.
- Balancear carga distribui filas e pode duplicar prefixos na memória de vários destinos.

## T171:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: tornar o worker com cache quente lento e remover blocos após anunciar residência; exigir execução correta e registro de cache miss, sem insistência ilimitada no destino.

Plano de avaliação proposto:
Comparar balanceamento sem afinidade e política combinada sob diferentes tamanhos de prefixo e ocupação. Medir latência completa, prefill poupado, memória e desequilíbrio de filas. Decidir pela métrica de serviço, não só pela taxa de cache hit.

Comparações:
- T157 (complements): Identidade de prefixo permite verificar qual estado pode ser reutilizado.
- T120 (complements): Roteamento de KV é uma aplicação específica dessa consideração de residência e custo.

Afirmação rastreável:
O design de cache do vLLM identifica blocos reutilizáveis pelo contexto encadeado e metadados relevantes.
Suporte: related; fontes: V3C-S015
Limite: A fórmula de decisão entre fila e cache é uma proposta de orquestração, não garantia fornecida pelo hashing.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T171:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 comparava afinidade de cache e custo de fila. Esta camada organiza prompts, tarefas e duração de sessões para preservar reutilização sem concentrar carga nem confundir cache de conteúdo com estado cognitivo.

Reutilização por fase
Agrupe tarefas que compartilham instruções e evidências estáveis, mas mantenha dados específicos depois desse prefixo. A ordenação só vale quando preserva semântica e isolamento. Um agrupamento excessivo pode esperar por tarefas futuras e aumentar latência; defina limite de espera e permita envio frio quando o prazo exigir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

Retenção conforme retorno provável
Uma sessão interativa pode voltar várias vezes ao mesmo prefixo, enquanto um trabalhador curto pode nunca reutilizá-lo. Avalie política de retenção pela frequência e intervalo de retorno, incluindo custo e pressão de memória. O perfil operacional relatado pela Uber é evidência de diferenciação, não valor universal de TTL.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014.

Caminhos de falha
Se a rota quente falhar, o plano precisa funcionar com recomputação fria em destino compatível. Carregue referências suficientes para reconstruir entrada, não só uma indicação de que havia cache. Se a implementação distribui KV, verifique custo e compatibilidade de transferência antes de presumir ganho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, B-S032.

USO AVANÇADO — Extração de muitos registros
Cenário: Várias chamadas aplicam o mesmo manual a dados diferentes.
Estratégia: Mantenha manual e exemplos estáveis, distribua registros em lotes que caibam no contrato e registre configuração. Compare afinidade com balanceamento simples sob cache frio, quente e saturado. Não reduza o manual necessário somente para aumentar throughput aparente.
Papel do modelo pequeno: 3–7B extrai campos repetitivos; verificação externa detecta desvios.
Aceite proposto: Proposta: menor custo de prefill por registro aceito sem aumento da cauda de latência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Especialistas de uma campanha
Cenário: Subagentes compartilham convenções do repositório, mas trabalham em módulos diferentes.
Estratégia: Prepare núcleo comum curto e anexe contexto de módulo após ele. Escolha retenção para a duração esperada dos lotes; não mantenha todo o KV de trabalhadores encerrados se não houver reuso plausível. Durante retomada, recupere documentos por versão e aceite cache miss.
Papel do modelo pequeno: 8–14B executa módulos; 15–30B coordena integração sem exigir cache compartilhado de toda a conversa.
Aceite proposto: Proposta: medir memória por tarefa, reutilização e custo completo da campanha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Cargas repetitivas curtas podem beneficiar-se mais de throughput que de prefixos enormes.
8–14B: Templates especializados e estáveis oferecem reutilização previsível entre chamadas.
15–30B: Contextos maiores exigem avaliar benefício de prefill contra pressão de KV e concorrência.
Requisitos de treino/runtime: Telemetria de hits, filas, expulsões e versões; controle de isolamento e possibilidade de recomputação.
Não aplicar quando: Não escolher modelo incompatível ou adiar indefinidamente uma tarefa somente para aproveitar cache.

## T171:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Política de cache distingue sessões interativas e subagentes de duração curta.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber fornece caso operacional de ajuste por perfil. vLLM fundamenta identidade de blocos; políticas propostas não foram executadas neste pacote.
Consultas registradas: V4C-Q009, V4C-Q017.

## T171:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T171 → T169 [complements]
Como combinar: Uber diferencia perfis de uso e cache entre sessões e subagentes do harness.
Interface: Tipo de sessão, duração prevista e prefixo compatível.
Condição: A política de cache acompanha o ciclo do trabalhador.
Aceite proposto: Medir economia em chamadas aceitas, não apenas hits.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

2. T171 → T157 [complements]
Como combinar: Usar identidade completa do prefixo para decidir o que pode ser reutilizado.
Interface: Hash, namespace e configuração de execução.
Condição: Tokens e metadados de computação são compatíveis.
Aceite proposto: Troca de adaptador provoca invalidação adequada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cache de resultado textual, prefix KV e singleflight resolvem problemas distintos.
- Queda de hit após deploy pode ser aquecimento legítimo; analisar junto de latência e qualidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno e fronteira sob taxas de repetição declaradas. Uma vantagem em carga cacheável pode desaparecer em perguntas únicas e não transfere capacidade de generalização.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T002, T082, T157

## Fontes primárias associadas

### C-S022 — Automatic Prefix Caching — vLLM

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos inclui hash ancestral, tokens e informações como adaptador e salt de isolamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S054 — SGLang: Efficient Execution of Structured Language Model Programs

[https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenação entre programas de LLM e runtime permite otimizar compartilhamento de contexto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T172 — Streaming Controller

**Nome canônico:** Streaming Controller  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T172  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador de streaming

## T172:C01 — conceito

Componente responsável pelo ciclo de vida de uma resposta incremental: abertura, fragmentos, buffering, backpressure, cancelamento e fechamento. Organiza a transmissão e a consistência da experiência do usuário. Não deve tratar qualquer fragmento recebido como saída final aprovada.

Como funciona:
- Associar cada stream a uma geração e consumidor identificados.
- Controlar entrega e acumulação dos fragmentos recebidos.
- Emitir término, erro ou cancelamento de forma inequívoca.

## T172:C02 — aplicacao

Quando usar:
- Interfaces de chat, voz ou acompanhamento de tarefa.
- Consumidores mais lentos que a geração de eventos.

Quando não usar:
- Usar buffer ilimitado ou ignorar desconexões do consumidor.

Implementação proposta:
- Modelar estados aberto, finalizado, falho e cancelado com transições válidas.
- Limitar buffer e definir política de pressão ou descarte admissível.
- Validar mensagem completa antes de gerar efeitos dependentes de seu conteúdo.

Aplicação LAI proposta:
Proposta: um controlador comum para saídas da Helena, separando eventos de progresso, texto ao usuário e confirmação de ferramentas.

## T172:C03 — riscos_validacao

Armadilhas:
- Reconexão pode duplicar fragmentos se não houver identificação.
- Eventos de erro depois de conteúdo parcial podem ser perdidos pela interface.

Métricas sugeridas:
- Latência até o primeiro evento e ocupação do buffer.
- Streams órfãos, duplicações e cancelamentos sem confirmação.

Testes propostos:
- Atrasar consumidor e confirmar limite de memória.
- Interromper conexão no meio do evento e verificar que não aparece resposta completa falsa.

## T172:C04 — perguntas_proveniencia

Pergunta: Streaming controller é uma técnica de LLM?
Resposta: É um componente de aplicação que coordena dados incrementais.

Pergunta: Um evento de fim significa que a tarefa inteira terminou?
Resposta: Apenas se o contrato definir e verificar essa conclusão.

Pergunta: Dez chunks garantem pouca memória?
Resposta: Não. Um chunk pode ser muito grande; a estratégia deve considerar tamanho quando memória for a restrição.

Pergunta: Fila vazia significa término?
Resposta: Não. Pode significar que o produtor está temporariamente sem dados; término requer evento ou estado explícito.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T172:C05 — mecanismo_avancado

Um controlador de streaming precisa limitar filas em uma unidade adequada. Contar fragmentos pode esconder grandes diferenças de tamanho; contar bytes aproxima memória ocupada. O high-water mark é um sinal para pressão reversa, não necessariamente uma barreira absoluta se o produtor ignora o sinal ou envia um fragmento enorme. Framing, sequência e estados de fechamento permitem distinguir atraso temporário, término normal e erro após conteúdo parcial.

Condição de contorno:
Se o produtor não coopera com pressão reversa, o controlador precisa aplicar outra política de buffer, descarte ou encerramento.

Contrato proposto:
- Entradas: Fluxo de eventos, tamanho de cada fragmento e velocidade do consumidor.
- Saídas: Fragmentos ordenados, sinais de pressão e término classificado.
- Estado: Fila com tamanho, sequência, consumidor ativo e estado de cancelamento.
- Invariante: O evento final e os erros não são descartados como se fossem fragmentos opcionais.

Compromissos de projeto:
- Buffer maior absorve diferenças de velocidade e aumenta memória e atraso acumulado.
- Buffer pequeno expõe lentidão cedo e pode reduzir throughput se o framing for muito granular.

## T172:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: desacelerar o consumidor e enviar um fragmento maior que a marca de água; verificar limitação operacional e tratamento explícito, sem crescimento indefinido da fila.

Plano de avaliação proposto:
Comparar filas por contagem e por bytes sob tamanhos variáveis. Medir pico de memória, atraso por fragmento, interrupções e integridade da sequência. Escolher estratégia conforme payload e cooperação real do backend.

Comparações:
- T153 (complements): Interrupção do usuário precisa propagar pelo controlador até a origem.
- T137 (distinct_from): Controle de fluxo entre produtor e consumidor não é a mesma política de admissão de requisições.

Afirmação rastreável:
O padrão WHATWG calcula desiredSize a partir da marca de água e do tamanho da fila para sinalizar backpressure.
Suporte: direct; fontes: V3C-S019
Limite: O produtor ainda precisa responder ao sinal; o padrão não transforma cada marca em limite físico universal.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T172:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava filas, framing e backpressure. A nova camada organiza múltiplos produtores, estado parcial e reconexão do consumidor sem confundir uma sequência de tokens com confirmação de tarefa concluída.

Canal de controle separado
Eventos de início, progresso, cancelamento, erro e conclusão precisam de semântica estável, independentemente do texto produzido. Uma mensagem final não deve ficar presa atrás de megabytes de logs opcionais. Defina priorização e retenção de eventos essenciais, sem reordenar conteúdo que depende de uma sequência anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V4C-S015.

Multiplexação identificada
Quando subagentes produzem simultaneamente, anexe origem, tarefa e sequência por fluxo. Misturar fragmentos de respostas diferentes pode formar texto plausível e impossível de auditar. O agregador pode apresentar progresso resumido, mas o consumidor precisa distinguir artefato completo de atualização parcial de outro trabalhador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, C-S030.

Reconexão com cursor
Um consumidor desconectado pode retornar depois que a tarefa avançou. Use cursor e retenção suficiente para repetir eventos necessários ou ofereça snapshot atual acompanhado do ponto de continuidade. Reentregar um evento não deve executar novamente a ação que o originou; apresentação e execução são camadas distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S019.

USO AVANÇADO — Missão assíncrona acompanhada por UI
Cenário: Pesquisa ou edição continua enquanto o usuário troca de dispositivo.
Estratégia: Persistir estado da tarefa e publicar eventos por sessão com identidade. Na reconexão, reconstruir visão atual e destacar quais resultados ainda são provisórios. Uma mudança de objetivo invalida a apresentação correspondente sem apagar evidências históricas.
Papel do modelo pequeno: 3–7B pode resumir progresso factual; o controlador não depende do texto para decidir estado.
Aceite proposto: Proposta: mesma visão final em consumidores lentos, rápidos e reconectados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

USO AVANÇADO — Ferramenta com saída extensa
Cenário: Build ou busca produz milhares de linhas enquanto o modelo espera.
Estratégia: Transmita contadores e diagnósticos selecionados, guardando o log completo como artefato. Aplique pressão reversa quando possível; se precisar truncar apresentação, preserve erro terminal e caminho para recuperar trechos. Não envie de volta ao modelo cada linha de progresso.
Papel do modelo pequeno: 8–14B extrai diagnóstico após critérios de seleção; 15–30B decide próximo passo.
Aceite proposto: Proposta: memória limitada e nenhum erro terminal perdido sob consumidor lento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Resumo de eventos tipados e pequenos; evitar interpretar fragmentos incompletos como dados finais.
8–14B: Classificação de diagnósticos e extração de erros com referências ao log.
15–30B: Integração de múltiplos fluxos por tarefa, mantendo proveniência e estados de confirmação.
Requisitos de treino/runtime: Sequência, cursor, retenção e política de buffer; resultado completo possui contrato separado de eventos intermediários.
Não aplicar quando: Não executar chamadas estruturadas enquanto argumentos ainda estão parciais ou misturados entre produtores.

## T172:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Canal por sessão e transmissão parcial são documentados, mas não todo o contrato de controle de fluxo, backpressure e cancelamento desta ficha.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C022 — Cloudflare / CDN — request collapsing
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A documentação descreve cache lock para solicitações simultâneas do mesmo asset em um data center.
Mecanismo documentado: A primeira solicitação busca a origem; as demais aguardam e recebem a resposta compartilhada. O escopo é por localização, não exclusão global de todas as chamadas.
Correspondência com esta base: A resposta é transmitida aos aguardantes, sem descrever um controlador completo de streaming LLM.
Transferência proposta para modelo pequeno: Proposta: coalescer leitura idêntica de documentos ou inferência determinística com escopo e versões iguais, separando cancelamento de um consumidor do trabalho compartilhado.
Limite: Operational_product: documentação de comportamento do serviço sem deployment específico de cliente. Cache HTTP não demonstra equivalência de respostas probabilísticas de LLM.
Fontes: V4C-S022.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Guardas controlam liberação de perguntas; não se documenta o ciclo completo do controlador, com pressão reversa e encerramento.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn descreve integração operacional de trabalho assíncrono e streaming; a implementação de cursor e retenção proposta precisa de validação própria. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q010, V4C-Q009, V4D-Q020.

## T172:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T172 → T154 [complements]
Como combinar: Proposta: combinar canal por sessão e transmissão parcial com controle explícito de fluxo e reconexão; o relato LinkedIn apoia somente as duas primeiras partes.
Interface: Sessão, tarefa e estado apresentado ao cliente.
Condição: Consumidores identificam contexto e atualização.
Aceite proposto: Troca de dispositivo não transforma progresso antigo em nova ação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T172 → T153 [complements]
Como combinar: Propagar interrupção do consumidor e registrar estado terminal sem presumir cancelamento do efeito remoto.
Interface: Pedido de cancelamento, confirmação e últimas saídas aceitas.
Condição: A ferramenta define se coopera com cancelamento.
Aceite proposto: Nenhum texto após cancelamento é apresentado como resposta confirmada inadvertidamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Fila vazia não prova término e silêncio não prova falha.
- Deduplicar eventos de apresentação sem descartar atualizações com sequência nova.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare experiência, integridade e consumo com o mesmo modelo. Streaming melhora acompanhamento e pode reduzir espera percebida sem reduzir o trabalho necessário para concluir.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T153, T159

## Fontes primárias associadas

### C-S018 — HTML Standard — Server-sent events

[https://html.spec.whatwg.org/multipage/server-sent-events.html](https://html.spec.whatwg.org/multipage/server-sent-events.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Eventos incrementais, identificação e reconexão SSE; cancelamento de inferência depende do servidor, não da norma SSE.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S019 — WHATWG Streams Standard

[https://streams.spec.whatwg.org/](https://streams.spec.whatwg.org/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas, estratégias de tamanho, high-water marks, backpressure, cancelamento e propagação por pipelines.

Limite: É o modelo de streams da Web; transporte, backend de geração e durabilidade precisam de contratos adicionais.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S022 — Default Cache Behavior — Request collapsing

[https://developers.cloudflare.com/cache/concepts/default-cache-behavior/](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache lock colapsa requisições simultâneas pelo mesmo asset em um data center e distribui a resposta aos aguardantes.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T173 — Model Fallback Controlado

**Nome canônico:** Model Fallback Controlado  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T136  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** contingência controlada de modelo

## T173:C01 — conceito

Aplicação de fallback a modelos de linguagem com verificação explícita de capacidades, custo, dados e estado da execução. A alternativa precisa receber contexto compatível e produzir o mesmo contrato exigido. É uma especialização de Fallback Chains, mantida como entrada para consultas específicas.

Como funciona:
- Identificar se a falha pede nova tentativa, troca de modelo ou interrupção.
- Filtrar modelos alternativos pelo contrato e pelo orçamento restante.
- Recriar requisição compatível e verificar o resultado antes de continuar.

Nota de nomenclatura: Especialização de T136; não contar como um mecanismo independente.

## T173:C02 — aplicacao

Quando usar:
- Backend de inferência indisponível ou saturado.
- Modelo não suporta uma capacidade requerida que foi detectada antes da ação.

Quando não usar:
- Trocar destino ultrapassa permissões, orçamento ou limite de exposição de dados.

Implementação proposta:
- Manter matriz de capacidade por modelo e versão.
- Converter mensagens e ferramentas por adaptadores testados.
- Registrar destino efetivo para atribuir erros, custos e qualidade corretamente.

Aplicação LAI proposta:
Proposta: a Helena escalar de modelo local para API somente por política explícita da tarefa e com preservação do estado validado.

## T173:C03 — riscos_validacao

Armadilhas:
- Templates e parâmetros diferentes podem alterar comportamento mesmo com prompt similar.
- Repetir chamadas após geração parcial pode duplicar ações de ferramentas.

Métricas sugeridas:
- Recuperação operacional e taxa de conformidade no destino alternativo.
- Custo da troca e divergências semânticas entre destinos.

Testes propostos:
- Forçar indisponibilidade do primário e conferir escolha apenas entre alternativas elegíveis.
- Oferecer fallback sem suporte ao schema exigido e exigir rejeição.

## T173:C04 — perguntas_proveniencia

Pergunta: Fallback controlado garante mesma resposta?
Resposta: Não. Garante que a transição foi validada; conteúdo ainda precisa ser avaliado.

Pergunta: É uma técnica independente de fallback?
Resposta: É uma especialização aplicada a modelos.

Pergunta: Um endpoint compatível com a mesma API é substituto completo?
Resposta: Não. Modelos podem divergir em modalidades, janela, ferramentas e subconjunto de schema aceito.

Pergunta: Resumir a entrada para caber no fallback é neutro?
Resposta: Não. Pode remover evidência relevante; a transformação deve ser avaliada e registrada como parte da tentativa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T173:C05 — mecanismo_avancado

Fallback entre modelos exige negociar capacidades antes de adaptar o pedido. Uma alternativa pode aceitar texto, mas não a modalidade de imagem, a mesma gramática ou o tamanho de saída. Transformações como resumir contexto são mudanças informacionais e precisam aparecer no registro da tentativa. Se a resposta original já foi transmitida, o consumidor deve reconhecer substituição, continuação ou nova tentativa como estados distintos.

Condição de contorno:
A alternativa não é semanticamente equivalente quando exige remover evidências ou ferramentas indispensáveis à tarefa.

Contrato proposto:
- Entradas: Falha da rota atual, contrato de resposta, modalidades e contexto versionado.
- Saídas: Rota compatível, transformações aplicadas e tentativa identificada.
- Estado: Capacidades efetivas, modelos já tentados e consumo acumulado.
- Invariante: Nenhum campo obrigatório desaparece silenciosamente durante a adaptação ao novo modelo.

Compromissos de projeto:
- Normalizar para um contrato mínimo amplia alternativas e pode excluir capacidades úteis.
- Manter adapters específicos preserva recursos e aumenta testes de compatibilidade.

## T173:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: o modelo principal falha em uma tarefa multimodal e o substituto suporta apenas texto; exigir bloqueio dessa rota ou reformulação explícita que ainda satisfaça o requisito.

Plano de avaliação proposto:
Comparar falha explícita e fallback em cenários de indisponibilidade com modelos elegíveis. Medir preservação do contrato, custo total e tempo até resultado aceito. Separar sucesso de transporte de qualidade da resposta substituta.

Comparações:
- T136 (specializes): É a cadeia geral aplicada a capacidades e contexto de modelos.
- T133 (complements): O roteador fornece candidatos, mas a política de falha decide quando mudar.

Afirmação rastreável:
MCP e JSON Schema tornam explícitos contratos de entrada e saída que integrações precisam preservar.
Suporte: related; fontes: V3C-S004
Limite: A fonte apoia contratos estruturados; a migração entre modelos descrita aqui é proposta editorial.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T173:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 negociava capacidades entre modelos. A expansão diferencia recuperação operacional de recuperação de qualidade, define destino de respostas parcialmente emitidas e evita perder decisões já confirmadas na troca.

Causa determina transição
Timeout ou indisponibilidade pode permitir repetir a mesma tarefa em rota compatível; resposta incorreta exige diagnóstico e talvez evidência nova. Se o problema é requisito ambíguo, trocar modelo pode apenas produzir outra interpretação. Registre o motivo e o teste que permitiria aceitar a alternativa antes de gastar outra tentativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S001, V4C-S011.

Estado mínimo portátil
Prepare entrada com objetivo atual, evidências referenciadas, contrato de saída e operações concluídas. Remova apenas detalhes dispensáveis com regra explícita. Ferramentas, multimodalidade e raciocínio podem ter interfaces diferentes; um adaptador deve declarar perdas de representação e recusar substituição quando faltar capacidade essencial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S004, V4C-S018.

Publicação de resposta alternativa
Depois de transmitir parte da resposta, não concatene automaticamente tokens de outro modelo. A alternativa pode contradizer o início ou reiniciar um JSON. Apresente nova tentativa identificada, ou mantenha saída em buffer até validação quando o produto exigir atomicidade. O contrato de interface define substituição e continuidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V4C-S015.

USO AVANÇADO — Extração local com escalonamento
Cenário: Um modelo pequeno falha em documento fora do padrão conhecido.
Estratégia: Verifique se o erro é parsing, contexto ausente ou entendimento. Repare formato apenas quando o conteúdo já satisfaz o requisito; recupere trecho faltante quando necessário. Acione modelo maior para a ambiguidade restante, fornecendo o diagnóstico e todas as evidências indispensáveis.
Papel do modelo pequeno: 3–7B cobre padrão comum; 15–30B ou fronteira trata exceção após gate.
Aceite proposto: Proposta: reduzir custo por extração aceita sem esconder erros na taxa agregada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S011, V3C-S013.

USO AVANÇADO — Indisponibilidade de provedor
Cenário: A rota escolhida deixa de responder durante uma campanha.
Estratégia: Selecione alternativa previamente testada para o mesmo schema e ferramentas. Reutilize resultados externos confirmados; não volte a executar todas as ações porque a conversa mudou de modelo. Se não houver rota compatível, preserve pendência e retome depois.
Papel do modelo pequeno: 8–14B continua tarefas tipadas quando autorizado; controlador preserva ledger de efeitos.
Aceite proposto: Proposta: nenhuma duplicação externa e manutenção do contrato sob falhas injetadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Fallback para tarefas estritas que cabem nas capacidades efetivamente testadas.
8–14B: Recuperação de extrações ou classificação com fontes suficientes e schema estável.
15–30B: Integração de exceções locais; escalonar além da faixa quando o critério independente falhar.
Requisitos de treino/runtime: Matriz de capacidades, adaptadores testados e contabilização acumulada entre rotas.
Não aplicar quando: Não usar substituto textual para tarefa cuja imagem ou ferramenta é indispensável sem reformulação válida.

## T173:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C012 — Amazon Web Services / Amazon Bedrock Intelligent Prompt Routing
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação disponibiliza um endpoint de roteamento que prevê qualidade e escolhe entre dois modelos compatíveis da mesma família.
Mecanismo documentado: Configuração define modelos, critério e fallback; resposta informa o modelo usado. A página é documentação de produto, não relato de implantação de um cliente.
Correspondência com esta base: Fallback do roteador é definido por critério de qualidade, não equivale automaticamente a recuperação por indisponibilidade.
Transferência proposta para modelo pequeno: Proposta: comparar um roteador local 3–30B com regras simples, rotas fixas e escalonamento após validação. Rejeitar candidatos sem capacidade necessária antes de estimar qualidade.
Limite: Classificado como operational_product. Não conta para dez casos comprovados em produção; lista de modelos e regiões muda. Exemplos com modelos maiores não validam as bandas pequenas.
Fontes: V4C-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Bedrock documenta roteamento por qualidade; gateway Uber demonstra integração de provedores. Nenhum dos dois prova sozinho toda esta cadeia de recuperação.
Consultas registradas: V4C-Q008, V4C-Q009.

## T173:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T173 → T133 [complements]
Como combinar: Obter candidatos elegíveis do roteador e aplicar política específica após a falha.
Interface: Capacidades, custo e motivo de transição.
Condição: Roteamento inicial e fallback possuem critérios distintos.
Aceite proposto: Não trocar por destino que elimina requisito obrigatório.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S011, V3C-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T173 → T243 [complements]
Como combinar: Reconciliar operações pendentes antes de continuar com outro modelo.
Interface: Intenções, chaves e confirmações remotas.
Condição: Mudança de modelo não altera identidade da missão.
Aceite proposto: Alternativa não repete efeito já realizado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- A mesma API de chat não significa a mesma capacidade de ferramentas.
- Fallback de qualidade do Bedrock não deve ser apresentado como prova de recuperação de qualquer outage.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare cascata e modelo de fronteira isolado com qualidade mínima comum e custo completo. Redução de custo médio não demonstra que o modelo menor resolve sozinho as exceções.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T136, T140

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

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

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V3C-S019 — WHATWG Streams Standard

[https://streams.spec.whatwg.org/](https://streams.spec.whatwg.org/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas, estratégias de tamanho, high-water marks, backpressure, cancelamento e propagação por pipelines.

Limite: É o modelo de streams da Web; transporte, backend de geração e durabilidade precisam de contratos adicionais.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T174 — Priority-Based Scheduling

**Nome canônico:** Priority-Based Scheduling  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T174  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento por prioridade

## T174:C01 — conceito

Política que decide qual trabalho pronto deve ocupar um recurso segundo prioridade, prazo e capacidade. Usa frequentemente uma priority queue, mas também define preempção, reservas e admissão. Priorizar sem equidade pode reduzir a espera de alguns clientes enquanto paralisa outros.

Como funciona:
- Considerar somente tarefas cujas dependências estão satisfeitas.
- Comparar prioridade efetiva e compatibilidade com recursos livres.
- Despachar e atualizar política após término, espera ou expiração.

## T174:C02 — aplicacao

Quando usar:
- Interações imediatas competem com processamento em lote.
- Existem classes de serviço e prazos diferentes.

Quando não usar:
- Prioridades são autoatribuídas sem controle e qualquer pedido pode se declarar urgente.

Implementação proposta:
- Estabelecer classes, critérios de desempate e quotas por classe.
- Separar prioridade de política de preempção suportada pelo backend.
- Adotar aging ou reserva mínima para trabalhos de baixa prioridade.

Aplicação LAI proposta:
Proposta: priorizar atendimentos em andamento da Helena sem eliminar capacidade mínima para indexação e verificação de conhecimento.

## T174:C03 — riscos_validacao

Armadilhas:
- Interromper GPU ou ferramenta nem sempre é possível sem perder trabalho.
- Prioridade alta não supera dependência ainda não concluída.

Métricas sugeridas:
- Latência por classe e violações de prazo.
- Eficiência de utilização e tempo perdido com preempções.

Testes propostos:
- Misturar cargas e comparar com FIFO sob o mesmo limite de recursos.
- Inundar a classe prioritária e verificar proteção das demais conforme política.

## T174:C04 — perguntas_proveniencia

Pergunta: Priority queue implementa toda essa política?
Resposta: Não. A fila só ordena itens; o scheduler decide admissão e recursos.

Pergunta: Prioridade maior sempre executa primeiro?
Resposta: Somente entre tarefas admissíveis e recursos compatíveis.

Pergunta: Alta prioridade implica parar o que já está rodando?
Resposta: Não. Pode significar apenas preferência na próxima admissão; preempção é uma política adicional.

Pergunta: Por que uma tarefa urgente pode continuar parada?
Resposta: Porque falta recurso compatível ou uma dependência está bloqueada; reordenar a fila não remove essa condição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T174:C05 — mecanismo_avancado

Prioridade de espera e preempção de trabalho ativo são decisões distintas. Kubernetes permite uma classe prioritária que não remove Pods em execução. Em agentes, uma ação pode ser não preemptível depois de enviar um efeito; interrompê-la libera o cliente, mas não necessariamente a capacidade remota. Um escalonador precisa considerar custo de retomada, reservas e possibilidade de inversão de prioridade quando uma tarefa urgente depende de outra menos prioritária.

Condição de contorno:
Prioridade alta não cria recurso compatível nem reduz uma dependência que continua bloqueada.

Contrato proposto:
- Entradas: Trabalhos prontos, prioridades, recursos, dependências e pontos de interrupção válidos.
- Saídas: Admissão, espera, reserva ou preempção explicitamente suportada.
- Estado: Ocupação, recursos retidos, custo de retomada e prioridade herdada quando prevista.
- Invariante: Uma tarefa não é interrompida como se pudesse ser retomada sem contrato para isso.

Compromissos de projeto:
- Preempção melhora resposta urgente e pode desperdiçar progresso do trabalho interrompido.
- Não preemptir conserva trabalho e pode elevar muito a espera de uma tarefa importante.

## T174:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma tarefa urgente depende de recurso retido por tarefa menos prioritária; verificar se a política detecta o bloqueio em vez de apenas ordenar a fila.

Plano de avaliação proposto:
Comparar prioridade não preemptiva, reservas e preempção em pontos seguros. Medir tempo por classe, trabalho perdido e inanição. Definir urgência e justiça separadamente, sem assumir que o mesmo número resolve ambos.

Comparações:
- T149 (complements): A fila fornece ordem; o escalonador decide uso de recursos e interrupção.
- T161 (complements): Caminho crítico informa dependências que podem dominar a prioridade nominal.

Afirmação rastreável:
Kubernetes documenta prioridade sem preempção por meio de preemptionPolicy Never.
Suporte: direct; fontes: V3C-S016
Limite: Essa semântica ilustra a distinção; não é uma API de controle de ferramentas do agente.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T174:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia prioridade e preempção. A nova camada combina urgência, custo de retomada e recursos exclusivos, com decisões de admissão que evitam interromper trabalho cujo efeito não pode ser desfeito.

Urgência verificável
Traduza prioridade em objetivo operacional: deadline, atendimento interativo ou desbloqueio de uma cadeia. Uma etiqueta alta sem critério tende a se espalhar até perder significado. Exija justificativa por classe e reavalie urgência quando a tarefa ficar obsoleta, em vez de manter pedidos antigos consumindo a reserva indefinidamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V3C-S016.

Pontos de suspensão
Defina onde a tarefa pode liberar recursos sem perder invariantes. Entre chamadas pode ser seguro; durante escrita remota talvez não. Checkpoint de contexto não garante checkpoint da ferramenta. Se não houver suspensão válida, a política pode reservar capacidade futura e evitar admitir novos trabalhos longos, em vez de matar os atuais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S016, C-S026.

Recursos exclusivos
Duas tarefas de alta prioridade podem disputar o mesmo repositório ou chave de projeto. Respeite exclusão antes de ordenar elegíveis. Acelerar um consumidor bloqueado não ajuda se o produtor de sua dependência ficou sem recurso; transfira urgência apenas ao trecho necessário para liberá-lo e mantenha limite de justiça.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, C-S025.

USO AVANÇADO — Chamadas interativas e lote
Cenário: GPU serve respostas ao usuário e processamento de acervo.
Estratégia: Reserve capacidade interativa e permita empréstimo ao lote quando ociosa. Preempção só ocorre nos pontos suportados pelo servidor; caso contrário, limite duração do lote admitido. Meça desperdício de KV e trabalho reiniciado ao comparar políticas.
Papel do modelo pequeno: 3–7B pode atender a classe interativa estreita; 15–30B processa lote com reserva definida.
Aceite proposto: Proposta: cumprir latência por classe mantendo progresso mínimo do lote.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S023, V3C-S016.

USO AVANÇADO — Integração de alterações urgentes
Cenário: Correção bloqueadora precisa entrar em uma campanha de patches.
Estratégia: Determine quais validações e recursos a correção exige. Eleve a prioridade das dependências indispensáveis e pause somente trabalho ainda não publicado em pontos seguros. Não pule testes de contrato para confundir urgência com aceite automático.
Papel do modelo pequeno: 8–14B identifica impacto local; um planejador maior explicita a cadeia bloqueadora.
Aceite proposto: Proposta: menor tempo de integração sem perda de validação ou duplicação de efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S003, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Tarefas pequenas permitem limites de serviço mais previsíveis, mas ainda precisam de admissão.
8–14B: Estimativa de impacto e classificação de urgência apoiadas em regras de domínio.
15–30B: Planejamento de dependências urgentes e análise de alternativas quando o recurso está ocupado.
Requisitos de treino/runtime: Escalonador com classes, exclusões, pontos seguros e telemetria de trabalho descartado.
Não aplicar quando: Não interromper efeito remoto como se cancelar o cliente fosse desfazer a operação.

## T174:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: Seleção de trabalho respeita prioridade e restrições de concorrência.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Ordem por dependência e valor orienta campanha, sem demonstrar um scheduler genérico de prioridade.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C023 — Google / Borg
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.
Mecanismo documentado: O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.
Correspondência com esta base: Há políticas de scheduling operacionais, mas o abstract não detalha todos os algoritmos de prioridade.
Transferência proposta para modelo pequeno: Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.
Limite: O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.
Fontes: V4C-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Timestone comprova prioridade e exclusão em produção. Kubernetes fundamenta distinção de preempção; não foi assumido que cada ferramenta de agente suporta suspensão.
Consultas registradas: V4C-Q003, V4C-Q018.

## T174:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T174 → T149 [complements]
Como combinar: Timestone combina prioridade temporal e exclusão para decidir quais mensagens são entregues.
Interface: Deadline, chave de exclusão e estado da fila.
Condição: A tarefa está pronta e seu recurso exclusivo está disponível.
Aceite proposto: Nenhuma admissão simultânea proibida por chave.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S003. Casos: V4C-C005.

2. T174 → T166 [complements]
Como combinar: Reservas e aging limitam o custo da urgência para outras classes.
Interface: Espera acumulada, cota e custo observado.
Condição: Política declara o que significa justiça.
Aceite proposto: Tarefa elegível de baixa prioridade continua recebendo progresso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S020, V3C-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não medir apenas tarefas urgentes e ocultar inanição do restante.
- Uma prioridade nova não elimina dependências nem cria memória compatível na GPU.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare políticas com recursos constantes e distribuição de carga igual. Benefício de modelos pequenos na fila depende de custo e qualidade por tarefa, não apenas do número de parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T149, T160, T166

## Fontes primárias associadas

### C-S014 — heapq — Heap queue algorithm

[https://docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estruturas heap permitem filas por prioridade; política de equidade é responsabilidade adicional.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S029 — Operating Systems: Three Easy Pieces — Scheduling: The Multi-Level Feedback Queue

[https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por prioridades precisa tratar inanição; boosts de prioridade são uma estratégia concreta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S016 — Kubernetes — Pod Priority and Preemption

[https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prioridade na fila é distinta de preempção; uma classe pode priorizar sem remover trabalho em execução.

Limite: Semântica de Pods serve como referência de escalonamento, não implementação automática de tarefas de agentes.

### V3C-S020 — Linux Kernel — EEVDF Scheduler

[https://docs.kernel.org/scheduler/sched-eevdf.html](https://docs.kernel.org/scheduler/sched-eevdf.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EEVDF usa lag e deadline virtual para distinguir elegibilidade, parcela justa e resposta à latência.

Limite: Escalonamento de CPU não se transfere literalmente a jobs remotos não preemptíveis; comparação é de princípios.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S025 — Critical-path planning and scheduling

[https://doi.org/10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Referência original do método do caminho crítico em planejamento de projetos.

Limite: Metadados bibliográficos localizados; abertura do DOI retornou HTTP 403. Procedimento descrito usa definição geral do método, não leitura integral deste artigo.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T175 — Rate Limiting com Fallback

**Nome canônico:** Rate Limiting com Fallback  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T175  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de taxa com contingência

## T175:C01 — conceito

Composição de controle de taxa e alternativas de execução. Quando a capacidade admissível do destino se esgota, a aplicação pode aguardar, usar alternativa autorizada ou falhar explicitamente. O mecanismo não deve contornar a quota contratada nem esconder uma mudança de qualidade.

Como funciona:
- Consultar orçamento de chamadas, tokens e concorrência antes da admissão.
- Comparar espera estimada com deadline e alternativas elegíveis.
- Reservar capacidade do destino escolhido e registrar a decisão.

## T175:C02 — aplicacao

Quando usar:
- Múltiplos backends autorizados com quotas diferentes.
- Picos de carga que excedem capacidade momentânea de um destino.

Quando não usar:
- Criar novas identidades ou contas para evitar controles de um serviço.

Implementação proposta:
- Manter orçamento agregado por missão e por destino.
- Respeitar Retry-After e circuito aberto antes de retentar.
- Definir se fallback pode degradar modalidade, contexto ou qualidade.

Aplicação LAI proposta:
Proposta: a Helena tratar orçamento e disponibilidade em um ponto comum, evitando que cada subagente tente trocar de provedor por conta própria.

## T175:C03 — riscos_validacao

Armadilhas:
- Todas as alternativas podem compartilhar o mesmo gargalo.
- Oscilação entre destinos aumenta custo e torna latência imprevisível.

Métricas sugeridas:
- Quotas respeitadas e volume de fallback.
- Qualidade e custo dos pedidos desviados versus pedidos originais.

Testes propostos:
- Esgotar quota do primário e confirmar que alternativa também reserva seu próprio saldo.
- Esgotar todos os destinos e exigir fila limitada ou erro explícito.

## T175:C04 — perguntas_proveniencia

Pergunta: Fallback elimina 429?
Resposta: Não. Pode redistribuir carga autorizada; o destino alternativo também tem limites.

Pergunta: Sempre é melhor trocar que esperar?
Resposta: Não. Deve considerar prazo, custo, compatibilidade e resultado esperado.

Pergunta: Uma URL nova significa uma quota nova?
Resposta: Não. A quota pode ser por conta, organização, modelo, região ou recurso compartilhado.

Pergunta: Como diferenciar fila e retry?
Resposta: Fila aguarda admissão ainda não concedida; retry repete uma tentativa que ocorreu ou falhou, com implicações diferentes de efeito e custo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T175:C05 — mecanismo_avancado

Fallback após limitação deve identificar qual quota foi atingida. Trocar de endpoint sob a mesma quota organizacional não cria capacidade adicional; pode apenas multiplicar rejeições. Uma alternativa realmente independente ainda precisa de orçamento próprio e capacidade semântica. Uma proposta mantém o estado de admissão separado da falha da ferramenta para que uma rejeição antes do envio não seja confundida com tentativa de efeito remoto.

Condição de contorno:
Quando todos os destinos pertencem à mesma restrição contratual, a ação coerente pode ser esperar ou encerrar, não circular entre URLs.

Contrato proposto:
- Entradas: Quota atingida, escopo de cobrança, destinos elegíveis e prazo restante.
- Saídas: Espera, admissão alternativa ou rejeição final fundamentada.
- Estado: Consumo por quota, rotas visitadas e próxima elegibilidade.
- Invariante: Alternativas não reutilizam o mesmo crédito nem ocultam consumo de tentativas anteriores.

Compromissos de projeto:
- Diversificar destinos melhora disponibilidade potencial e amplia complexidade de contabilidade.
- Esperar preserva consistência do backend e pode violar o prazo da tarefa.

## T175:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois endpoints compartilham uma quota esgotada e um terceiro possui contrato incompatível; exigir espera ou falha explícita, sem rota artificialmente considerada válida.

Plano de avaliação proposto:
Comparar fila e fallback sob saturação localizada e global. Medir rejeições repetidas, conclusão, custo e equidade entre clientes. Distinguir ganho por capacidade adicional real de aparente ganho por contabilização incompleta.

Comparações:
- T137 (complements): O limitador fornece motivo e escopo da rejeição.
- T173 (complements): Fallback de modelos precisa manter capacidades além de encontrar quota disponível.

Afirmação rastreável:
Google SRE trata quotas e rejeição por criticidade como controles que devem propagar pela cadeia de serviços.
Suporte: related; fontes: V3C-S009
Limite: A política de troca entre provedores é composição editorial, dependente de contratos e quotas efetivos.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T175:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia quotas compartilhadas e independentes. A expansão considera o custo marginal do fallback, reservas já consumidas e política de degradação sem transformar indisponibilidade em vazamento de orçamento.

Mapa de domínios de quota
Represente relações entre conta, organização, modelo e região. Dois destinos podem compartilhar um limite superior mesmo quando possuem quotas locais diferentes. A decisão precisa consultar o limite que realmente bloqueou o pedido; trocar rota sem essa informação pode aumentar rejeições e ocultar a causa original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V3C-S010.

Reserva antes de transferir
Adquira capacidade na alternativa antes de abandonar uma rota ainda válida, quando o protocolo permitir. Libere a reserva original apenas quando o estado do envio estiver claro. Se a primeira chamada segue executando, cobrar só a segunda subestima uso e pode ultrapassar o teto global da missão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S010, C-S026.

Degradação por contrato
Uma alternativa pode oferecer menos contexto ou ferramentas. A política deve decidir se o requisito ainda pode ser cumprido, não apenas se existe crédito. Em alguns casos, resposta parcial com evidências e pendências é melhor que forçar conclusão em rota incapaz; essa escolha precisa aparecer no estado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S001, V4C-S005.

USO AVANÇADO — Pico de consultas interativas
Cenário: O backend habitual fica limitado por taxa durante horário de pico.
Estratégia: Mantenha fila curta e calcule se o prazo ainda permite espera. Quando houver alternativa compatível com quota independente, compare custo total e latência prevista. Se o limite for global, aplique admissão ou resposta de indisponibilidade em vez de circular por endpoints equivalentes.
Papel do modelo pequeno: 3–7B local cobre apenas classes pré-validadas; pedidos complexos permanecem em fila apropriada.
Aceite proposto: Proposta: menor rejeição útil sem aumentar erro por substituição inadequada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S005.

USO AVANÇADO — Campanha de pesquisa com orçamento
Cenário: Agentes paralelos consomem quota de vários serviços.
Estratégia: Distribua créditos por destino e prioridade da pergunta. Ao receber limitação, reduza fan-out e reprograme coletas; não duplique a busca em todos os provedores por padrão. Resultados já confirmados seguem para extração enquanto fontes indispensáveis aguardam.
Papel do modelo pequeno: 8–14B aproveita evidência disponível; 15–30B decide quais lacunas justificam custo adicional.
Aceite proposto: Proposta: cobertura por pergunta e custo de tentativas rejeitadas, com prazo explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Fallback local para tarefas estritas, com teto de qualidade e capacidade medido.
8–14B: Triagem de demandas para filas diferentes sem inventar independência de quota.
15–30B: Replanejar cobertura e escopo quando limitações tornam a missão original inviável.
Requisitos de treino/runtime: Telemetria por quota, matriz de capacidades, reservas pendentes e orçamento agregado entre destinos.
Não aplicar quando: Não usar novas credenciais ou endpoints para contornar restrições de acesso ou contratos do serviço.

## T175:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Controle de sobrecarga combinado com degradação é relacionado a fallback por limite.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SRE fornece controles de sobrecarga e degradação; a troca coordenada entre provedores é proposta, sem alegação de dez adoções específicas.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q008.

## T175:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T175 → T137 [complements]
Como combinar: O limitador informa qual escopo recusou admissão para orientar a decisão de espera ou troca.
Interface: Quota, saldo, próximo prazo elegível e motivo.
Condição: Causa da limitação é conhecida ou marcada como incerta.
Aceite proposto: Não realizar fallback circular entre destinos sob o mesmo limite.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T175 → T173 [complements]
Como combinar: Antes da troca, confirmar que o modelo alternativo preserva modalidades, ferramentas e resultado exigido.
Interface: Contrato da tarefa e capacidades efetivas.
Condição: Existe orçamento e qualidade mínima comprovada.
Aceite proposto: Alternativa incompatível é rejeitada mesmo com quota sobrando.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S001, V4C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Falha de admissão anterior ao envio não significa efeito remoto incerto.
- Cancelamento do cliente não libera automaticamente consumo no backend original.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade sob quota fixa e qualidade mínima constante. Mais respostas obtidas por remover requisitos não são ganho legítimo de capacidade para modelos pequenos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T137, T164, T173

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T176 — Token-Aware Planning

**Nome canônico:** Token-Aware Planning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T176  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejamento consciente de tokens

## T176:C01 — conceito

Planejamento que considera custo e espaço de contexto de cada etapa, além das dependências funcionais. O plano estima entradas, saídas, ferramentas e verificações e pode decompor trabalho quando necessário. Trata-se de política de orquestração; não existe uma fórmula universal que preveja todo consumo.

Como funciona:
- Estimar tokens e número de chamadas de cada etapa planejada.
- Reservar espaço para evidências, resultado e verificação.
- Atualizar estimativas com consumo observado antes de liberar próximas etapas.

## T176:C02 — aplicacao

Quando usar:
- Missões extensas com RAG, várias ferramentas ou subagentes.
- Contexto e custo são restrições reais do fluxo.

Quando não usar:
- Escolher o plano mais curto em tokens mesmo quando perde evidência ou qualidade necessária.

Implementação proposta:
- Manter estimativa central e margem de incerteza por tipo de etapa.
- Preferir referências a artefatos grandes e recuperar detalhes sob demanda.
- Planejar checkpoint antes de regiões com alto risco de expansão.

Aplicação LAI proposta:
Proposta: o planejador da Helena incluir orçamento por etapa, reservando capacidade para checagens e retomada em vez de consumir tudo no planejamento.

## T176:C03 — riscos_validacao

Armadilhas:
- Saída de ferramenta pode ser muito maior que o previsto.
- Decomposição excessiva repete instruções em várias chamadas e aumenta custo.

Métricas sugeridas:
- Erro de previsão de tokens por etapa.
- Taxa de conclusão dentro do orçamento e custo por tarefa aceita.

Testes propostos:
- Executar missões com documentos de tamanhos variados e comparar previsão versus uso.
- Fazer uma etapa exceder previsão e verificar replanejamento sem apagar restrições.

## T176:C04 — perguntas_proveniencia

Pergunta: Token-aware significa sempre usar prompt menor?
Resposta: Não. Um trecho maior pode evitar várias chamadas e reduzir custo total.

Pergunta: A estimativa é garantia?
Resposta: Não. Precisa de margem e revisão durante a execução.

Pergunta: Dividir sempre em tarefas menores economiza tokens?
Resposta: Não. Instruções repetidas, resumos e integração podem superar a economia de cada chamada.

Pergunta: Como planejar uma saída de ferramenta sem tamanho conhecido?
Resposta: Usar distribuição observada ou intervalo conservador e definir previamente como selecionar, paginar ou referenciar o excedente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T176:C05 — mecanismo_avancado

Planejamento sensível a tokens deve modelar crescimento de evidência, não apenas tamanho do prompt inicial. Uma etapa de busca pode expandir candidatos e tornar o passo seguinte inviável; uma etapa de síntese pode reduzir espaço e perder detalhes necessários à verificação. Estimativas por intervalo permitem planejar contingências: extrair por referência, dividir subtarefas ou reservar uma rodada de recuperação, mantendo custo de coordenação no orçamento.

Condição de contorno:
Quando o tamanho das observações é desconhecido, um plano com estimativas pontuais otimistas pode falhar mesmo sem nenhuma resposta excepcional.

Contrato proposto:
- Entradas: DAG de trabalho, intervalos de entrada/saída, janela e orçamento acumulado.
- Saídas: Plano viável, reservas e alternativas para etapas que ultrapassem a estimativa.
- Estado: Consumo real por tipo de operação e dependências informacionais.
- Invariante: Uma etapa não elimina informações exigidas por seu próprio critério de validação.

Compromissos de projeto:
- Dividir o trabalho reduz contexto por chamada e aumenta mensagens de integração.
- Carregar documentos completos evita novas buscas e pode expulsar evidência mais relevante.

## T176:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma pesquisa retorna muitos candidatos e a verificação exige trechos originais; exigir seleção rastreável e preservação de referências antes de continuar.

Plano de avaliação proposto:
Comparar plano sem custo, plano por estimativa média e plano com contingências. Controlar tarefas e ferramentas. Medir estouros, replanejamentos, perda de evidência e custo por conclusão; escolher a política pela variabilidade observada.

Comparações:
- T152 (complements): Alocação implementa as reservas que o plano estima.
- T143 (specializes): Acrescenta restrições de contexto e consumo ao planejamento antecipado.

Afirmação rastreável:
ReWOO reduz repetição de contexto ao separar planejamento e observações em sua arquitetura.
Suporte: direct; fontes: V3C-S012
Limite: Previsões por intervalos e contingências desta ficha são propostas; a economia do estudo não é transferida para LAI.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T176:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 estimava crescimento de evidência e contingências. A nova camada planeja a distribuição informacional entre chamadas, incluindo custo de integrar resultados e a reserva necessária para verificar o que foi produzido.

Grafo informacional
Para cada etapa, declare quais fatos precisa receber e quais deve preservar para seus sucessores. Uma saída curta pode omitir o detalhe necessário ao teste seguinte. Planeje interfaces por campos e referências, não apenas por número de tokens; a compressão é aceitável quando a informação excluída permanece recuperável no momento certo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S012, V4C-S013.

Custo de coordenação
Dividir uma tarefa reduz contexto local e acrescenta instruções repetidas, chamadas, resultados intermediários e síntese. Estime esse custo antes de criar especialistas. Quando a comunicação domina o trabalho útil, mantenha etapas juntas ou use funções determinísticas para filtrar dados, em vez de multiplicar agentes pequenos por princípio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Plano com gatilhos
Defina ações quando a observação ultrapassar a previsão: paginação, seleção de campos, nova subtarefa ou interrupção para handoff. O gatilho deve ocorrer antes de consumir a reserva de validação. Replanejamento altera somente etapas ainda abertas; artefatos já aceitos permanecem referenciados e podem ser invalidados apenas por mudança de requisito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S022.

USO AVANÇADO — Refatoração em repositório grande
Cenário: O contexto completo não cabe de forma útil no modelo local.
Estratégia: Comece com mapa de símbolos e dependências, leia trechos necessários e produza patch por unidade. Reserve leitura de consumidores e execução de testes antes de integrar. Se um tipo comum mudar, reabra o planejamento dos módulos afetados em vez de continuar com resumos antigos.
Papel do modelo pequeno: 3–7B aplica mudanças locais; 8–14B seleciona contexto; 15–30B integra contratos.
Aceite proposto: Proposta: nenhuma mudança aceita sem contexto de validação e menor consumo por tarefa concluída.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S012.

USO AVANÇADO — Síntese de fontes extensas
Cenário: Há documentos suficientes para exceder várias janelas.
Estratégia: Extraia tabelas de alegação, trecho e limite por fonte. Planeje a síntese sobre essas tabelas e reserve consultas pontuais aos originais para conflitos. Não conte apenas tokens de síntese: some extração, revisões e recuperações adicionais para comparar arquiteturas.
Papel do modelo pequeno: 8–14B realiza extração padronizada; 15–30B compara alegações apoiadas.
Aceite proposto: Proposta: cobertura de evidência e custo completo frente à leitura monolítica quando ela for viável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Nós de transformação estreitos, com saída curta e critério determinístico.
8–14B: Seleção e extração de contexto com referências que permitam recuperação posterior.
15–30B: Planejamento de dependências informacionais e integração de exceções sem carregar todos os intermediários.
Requisitos de treino/runtime: Contagem com tokenizer real, estimativas por etapa e medição do custo de reconsulta e integração.
Não aplicar quando: Não chamar de economia uma compressão que elimina a evidência necessária para verificar o resultado.

## T176:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: ReWOO e relatos de harness sustentam separação de fases; as estimativas e critérios propostos não foram executados nem tratados como benchmark.
Consultas registradas: V4C-Q009, V4C-Q014, V4C-Q027.

## T176:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T176 → T152 [feeds]
Como combinar: Converter previsão do plano em reservas de entrada, saída e validação por etapa.
Interface: Estimativas, variabilidade e prioridade informacional.
Condição: Reservas cabem na janela e no orçamento acumulado.
Aceite proposto: Estouro de uma ferramenta dispara contingência antes de invalidar a chamada seguinte.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T176 → T214 [complements]
Como combinar: Projetar campos de ferramentas conforme a necessidade da próxima etapa.
Interface: Schema da resposta e campos requeridos pelo contrato.
Condição: Dados omitidos permanecem recuperáveis por referência.
Aceite proposto: Poda não remove identificação, erro ou campo necessário ao teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mais trabalhadores podem aumentar tokens totais apesar de reduzir janela individual.
- Não iniciar síntese final sem reserva para conferir fontes e produzir estado de cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare arquitetura pequena e modelo de fronteira com custo de todas as fases e taxa de conclusão válida. Planejamento pode compensar contexto limitado em tarefas decomponíveis, sem garantir paridade em sínteses indivisíveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T152, T168

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

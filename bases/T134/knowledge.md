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

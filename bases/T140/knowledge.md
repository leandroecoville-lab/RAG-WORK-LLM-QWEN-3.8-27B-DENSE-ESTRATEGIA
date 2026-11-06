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

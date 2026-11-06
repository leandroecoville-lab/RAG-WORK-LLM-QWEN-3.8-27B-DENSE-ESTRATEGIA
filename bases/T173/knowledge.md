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

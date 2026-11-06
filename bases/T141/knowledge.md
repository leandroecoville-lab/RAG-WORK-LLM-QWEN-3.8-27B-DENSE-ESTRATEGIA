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

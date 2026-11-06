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

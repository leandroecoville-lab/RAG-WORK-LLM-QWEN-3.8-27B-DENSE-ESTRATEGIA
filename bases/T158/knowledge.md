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

# T220 — Tool Call Repair

**Nome canônico:** Tool Call Repair  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T220  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** tool argument repair; reparo de argumentos

## T220:C01 — conceito

Reparo de uma chamada de ferramenta inválida por meio de diagnóstico estruturado e correção dos argumentos ou da seleção da ferramenta. É seguro repetir uma chamada rejeitada antes da execução quando o erro foi corrigido. Uma resposta perdida após uma mutação exige reconciliação, pois o efeito pode já ter ocorrido.

Como funciona:
- O executor distingue erro de esquema, erro de domínio, falta de permissão e resultado de execução incerto.
- Feedback limitado informa o campo inválido e a restrição aplicável.
- O agente produz uma nova proposta que passa novamente pelas validações e pelo controle de autorização.

## T220:C02 — aplicacao

Quando usar:
- Argumentos malformados, tipos incompatíveis, identificadores não encontrados ou seleção incorreta entre ferramentas disponíveis.

Quando não usar:
- Repetir cegamente uma mutação após timeout ou modificar permissões para contornar uma rejeição.

Implementação proposta:
- Proposta: validar os argumentos antes de executar e classificar a resposta com um código de erro estável.
- Permitir poucas tentativas de reparo, preservando o objetivo e os valores já confirmados.
- Quando um identificador estiver errado, recuperar o identificador real na fonte autorizada; não adivinhar um substituto.
- Registrar a relação entre chamada original e corrigida, incluindo identidade e resultado da execução.
- Para efeitos incertos, consultar estado ou chave idempotente antes de qualquer repetição.

Aplicação LAI proposta:
Proposta LAI: introduzir um contrato de erro entre controlador e ferramentas, encaminhando ambiguidades de efeito ao reconciliador e erros de formato ao reparador.

## T220:C03 — riscos_validacao

Armadilhas:
- Esquema válido não significa destinatário, arquivo ou valor de negócio correto.
- Mensagens de erro podem conter conteúdo não confiável.
- Reparo infinito consome orçamento sem resolver incompatibilidade de capacidade.

Métricas sugeridas:
- Reparos aceitos; taxa de execução duplicada; tentativas por erro; rejeições por categoria; resultados incertos reconciliados.

Testes propostos:
- Enviar argumento de tipo errado e verificar rejeição sem efeito.
- Fornecer chamada válida com alvo inexistente e exigir descoberta fundamentada.
- Simular mutação concluída com resposta perdida e impedir duplicação no reparo.

## T220:C04 — perguntas_proveniencia

Pergunta: Modo estrito elimina a necessidade de reparo?
Resposta: Não. Ele pode restringir o formato a um esquema suportado, mas não confirma existência do alvo, permissão ou consistência de negócio.

Pergunta: Quando um retry deixa de ser reparo?
Resposta: Quando a chamada já foi executada ou seu resultado é desconhecido. Nessa situação, repetição é uma decisão de recuperação com controle de idempotência.

Pergunta: Preencher um campo ausente com valor plausível é reparo válido?
Resposta: Somente se houver fonte ou default contratual; plausibilidade não fornece o dado que falta.

Pergunta: Quando reparar deveria parar?
Resposta: Quando falta informação indispensável, a mesma classe de erro persiste ou o orçamento acaba, preservando o diagnóstico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T220:C05 — mecanismo_avancado

Reparo pode alterar seleção da ferramenta, nome de campo, tipo, enum ou referência de recurso; cada classe exige diagnóstico diferente. Converter um número em string resolve sintaxe, mas pode mudar significado, como zeros à esquerda de um identificador. A proposta recebe erros estruturados e preserva o objetivo original. Rejeição comprovada antes da execução permite uma nova tentativa corrigida; desfecho incerto precisa de outra estratégia.

Condição de contorno:
Um erro genérico após envio não comprova que nada ocorreu; reparar e reenviar pode duplicar um efeito já aplicado.

Contrato proposto:
- Entradas: Chamada original, schema efetivo, diagnóstico e fase de execução alcançada.
- Saídas: Chamada revisada, justificativa da mudança e decisão de executar ou reconciliar.
- Estado: Número de reparos, alterações realizadas e identidade da intenção.
- Invariante: O reparo não muda silenciosamente o recurso ou objetivo para obter uma resposta sem erro.

Compromissos de projeto:
- Correções determinísticas são previsíveis e cobrem poucos tipos de falha.
- Reparo por modelo trata casos diversos e pode inventar valores apenas para satisfazer o schema.

## T220:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer enum inválido, ID desconhecido e resposta perdida após escrita; exigir correção no primeiro, busca ou inconclusão no segundo e reconciliação no terceiro.

Plano de avaliação proposto:
Comparar regras e reparo por modelo em erros rotulados por fase. Medir recuperação correta, alterações semânticas indevidas, loops e custo. Limitar reparos por intenção e separar erros recuperáveis de ausência de informação.

Comparações:
- T170 (complements): A revisão do schema define se o erro decorre de contrato obsoleto.
- T243 (distinct_from): Reconciliação investiga efeito incerto; não é simples correção dos argumentos.

Afirmação rastreável:
LangChain distingue middleware que transforma erro da ferramenta em feedback e middleware que repete a chamada.
Suporte: direct; fontes: V3C-S038
Limite: A composição não prova que todo erro é repetível nem que corrigir argumentos preserva a intenção.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T220:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava tipos de erro e efeito incerto. A camada nova usa reparo mínimo, validação de intenção e escalonamento por diagnóstico para evitar que um argumento válido faça a operação errada.

Reparo mínimo explicável
Produza uma diferença entre chamada original e corrigida, indicando qual erro cada mudança resolve. Corrigir nome de campo não autoriza mudar recurso ou ampliar seleção. Se o reparo exige adivinhar informação ausente, devolva necessidade de contexto em vez de preencher um valor plausível apenas para satisfazer o schema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S004, V3C-S038.

Fronteira de não execução
Reparo automático simples é apropriado quando há evidência de rejeição antes do efeito. Depois de timeout ou erro interno genérico, consulte a operação original antes de reenviar. Um parser local pode rejeitar antes da rede; um erro retornado pelo serviço precisa ser interpretado conforme seu contrato, não pela aparência do texto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V2A-S012.

Diagnóstico hierárquico
Tente primeiro transformações determinísticas autorizadas, como normalização de enum conhecida. Use LLM quando o erro exige relação entre objetivo, ferramenta e schema. Trocar ferramenta ou recurso é decisão de plano e deve passar por validação mais forte que um ajuste de formato. Cada reparo mantém a identidade da intenção quando ela permanece a mesma.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S038.

USO AVANÇADO — Ferramenta exige schema estrito
Cenário: Um pequeno modelo emite argumento com tipo ou nome errado.
Estratégia: Retorne erro estruturado e schema relevante, peça somente a correção mínima e valide novamente antes de executar. Preserve zeros à esquerda e unidades de identificadores; uma conversão aparentemente óbvia pode alterar o alvo. Limite ciclos e registre a classe que não foi resolvida.
Papel do modelo pequeno: 3–7B pode reparar formato curto; 8–14B relaciona campo e significado.
Aceite proposto: Proposta: corrigir sintaxe sem mudar recurso, quantidade ou efeito pretendido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S004, V3C-S013.

USO AVANÇADO — Catálogo mudou durante a missão
Cenário: A ferramenta selecionada teve revisão incompatível.
Estratégia: Resolva contrato vigente e compare com a intenção registrada. Se existir tradução sem perda, aplique adaptador testado; se a mudança exigir novo dado ou alterar efeito, volte ao planejador. Não usar tentativa e erro em produção como mecanismo de descoberta de schema.
Papel do modelo pequeno: 15–30B analisa incompatibilidade; runtime faz tradução validada e controle de efeitos.
Aceite proposto: Proposta: nenhuma chamada executada com parâmetros inventados para satisfazer versão nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Correções de formato e enum em chamadas pequenas, com validação determinística.
8–14B: Reparo semântico local quando objetivo e dados necessários estão explícitos.
15–30B: Replanejar escolha de ferramenta diante de mudança de capacidade, sem ocultar a mudança de intenção.
Requisitos de treino/runtime: Erros estruturados, schema versionado, prova de não execução ou reconciliação e limite de tentativas.
Não aplicar quando: Não reenviar efeito desconhecido nem preencher identificadores por similaridade sem fonte.

## T220:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Gateway e middleware fornecem contratos; a política de reparo mínimo é proposta. Não confundir reparadores de código AutoClean com reparo de argumentos de ferramenta.
Consultas registradas: V4C-Q009, V4C-Q013, V4C-Q023.

## T220:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T220 → T141 [complements]
Como combinar: Validar estrutura antes e depois do reparo, preservando separadamente os invariantes de intenção.
Interface: Chamada original, diff de argumentos e resultado de validação.
Condição: Schema corresponde à versão executável.
Aceite proposto: Reparo passa parser e conserva alvo e unidade corretos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T220 → T243 [complements]
Como combinar: Resolver desfecho incerto antes de permitir nova chamada corrigida.
Interface: Identificador da operação e estado observado no destino.
Condição: Timeout não foi tratado automaticamente como ausência de efeito.
Aceite proposto: Nenhuma duplicação após erro retornado tarde.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar reparos evita transformar uma chamada inválida em busca ilimitada de combinações.
- Um argumento aceito pelo schema pode continuar violando o requisito de negócio.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de chamadas corretas e efeitos errados entre modelos com o mesmo verificador. Reparo de formato pode favorecer 3–30B, mas não supre informação ausente ou escolha equivocada de ferramenta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T243, T228, T218

## Fontes primárias associadas

### V2A-S022 — Function calling

[https://developers.openai.com/api/docs/guides/function-calling](https://developers.openai.com/api/docs/guides/function-calling)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas de ferramentas com esquema de argumentos, modo estrito e resultados associados.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S038 — LangChain — Prebuilt middleware

[https://docs.langchain.com/oss/python/langchain/middleware/built-in](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Middleware de erro de ferramenta é distinto de retry; ordem de composição determina tratamento de exceções e limites.

Limite: Documentação dinâmica com requisitos de versão; não se pressupõe disponibilidade de classes no ambiente do usuário.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

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

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

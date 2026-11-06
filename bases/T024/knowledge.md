# T024 — Context Broker e Context Builder

**Nome canônico:** Context Broker / Context Builder  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T024  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** montador de contexto; gerenciador de contexto; Context Broker / Context Builder

## T024:C01 — conceito

Componente do runtime que monta a entrada de cada chamada a partir de objetivo, regras, estado, histórico e evidências. É uma fronteira de engenharia para tornar seleção e orçamento observáveis. Não existe um único algoritmo padronizado com esse nome.

Como funciona:
- Receber objetivo, identidade, modelo e limites de entrada/saída.
- Selecionar fontes autorizadas e informações necessárias.
- Ordenar, validar e emitir um pacote de contexto com manifesto.

Nota de nomenclatura: Nome arquitetural descritivo; implementação e critérios propostos são editoriais.

## T024:C02 — aplicacao

Quando usar:
- Sistemas com vários agentes, fontes e modelos.
- Necessidade de explicar por que uma informação entrou ou ficou fora de uma decisão.

Quando não usar:
- Não delegar ao broker a criação de permissões que não existem no sistema de origem.

Implementação proposta:
- Proposta: manter políticas obrigatórias fora da seleção probabilística.
- Registrar documentos, versões, critérios de seleção e estimativa de tokens.
- Se o essencial não couber, dividir a tarefa ou reduzir saída, em vez de cortar silenciosamente restrições.

Aplicação LAI proposta:
Proposta LAI: centralizar seleção de contexto sob Helena, mantendo contratos de entrada e saída independentes do provedor de LLM.

## T024:C03 — riscos_validacao

Armadilhas:
- O broker pode se tornar gargalo de latência.
- Pontuações de relevância podem remover informação necessária mas semanticamente distante.

Métricas sugeridas:
- Violações de orçamento e taxa de omissão de campos obrigatórios.
- Custo de construção, cache hit e sucesso da missão.

Testes propostos:
- Criar contexto com documentos de dois tenants e permitir somente o autorizado.
- Forçar orçamento menor que as instruções obrigatórias e exigir erro controlado.

## T024:C04 — perguntas_proveniencia

Pergunta: É obrigatório usar um framework específico?
Resposta: Não. A interface pode ser implementada com funções e armazenamento próprios.

Pergunta: O broker deve resumir tudo?
Resposta: Não. Ele decide quais originais, resumos e referências são adequados à chamada atual.

Pergunta: O manifesto precisa copiar todo o prompt?
Resposta: Não necessariamente. Pode referenciar blocos imutáveis e registrar versões e posições, desde que permita reconstrução autorizada da entrada.

Pergunta: Como diagnosticar uma resposta sem fundamento?
Resposta: Verifique primeiro se a evidência existia, depois se foi recuperada, incluída e corretamente interpretada. Cada etapa exige observáveis diferentes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T024:C05 — mecanismo_avancado

O montador de contexto pode ser tratado como uma função observável: recebe estado e candidatos, produz a requisição e um manifesto de seleção. Isso permite distinguir falha de recuperação de falha de montagem. Categorias como instrução vigente, observação externa e hipótese derivada precisam permanecer identificáveis; concatenar tudo como texto homogêneo facilita confusão de autoridade e origem.

Condição de contorno:
Um builder não consegue reparar uma fonte inexistente ou um estado inconsistente apenas reorganizando mensagens; precisa detectar e expor a falta.

Contrato proposto:
- Entradas: Objetivo, estado versionado, regras vigentes, candidatos e orçamento do modelo.
- Saídas: Requisição compatível e manifesto de blocos incluídos e excluídos.
- Estado: Versões de seletores, fontes, templates e contagem de tokens.
- Invariante: Conteúdo recuperado permanece evidência ou dado, sem ganhar autoridade de instrução pelo simples posicionamento.

Compromissos de projeto:
- Centralizar seleção facilita auditoria, mas pode criar ponto de latência e acoplamento.
- Regras determinísticas melhoram reprodução; relevância aprendida acrescenta adaptação e variabilidade.

## T024:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir em um documento recuperado uma instrução que contradiga o objetivo. O manifesto deve mantê-la como conteúdo da fonte e a montagem não deve promovê-la a regra do sistema.

Plano de avaliação proposto:
Avaliação proposta: comparar montagem fixa e seletiva com candidatos idênticos. Medir fatos excluídos indevidamente, custo, estabilidade entre execuções e clareza da proveniência; decidir pela qualidade da tarefa e capacidade de explicar a seleção.

Comparações:
- T222 (complements): O monitor fornece orçamento; o builder decide como distribui-lo entre conteúdos.
- T066 (complements): O resolvedor entrega versões e conteúdos que o builder pode incorporar.

Afirmação rastreável:
MCP descreve recursos como dados de contexto cuja incorporação é decidida pela aplicação hospedeira.
Suporte: related; fontes: V3A-S019
Limite: A fonte apoia a responsabilidade do host; Context Broker é um componente arquitetural proposto, não uma API universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T024:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu manifesto e confiança. Aqui broker e builder negociam orçamento de aquisição por utilidade marginal e prazo.

Projeto e decomposição
O broker propõe candidatos com custo, atraso e tipo de suporte. O builder seleciona evidências para afirmações prioritárias, expondo lacunas que justificam nova aquisição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

Controle adaptativo
Imponha prazo por estágio e caminho de resposta parcial. Fontes lentas só são aguardadas quando podem alterar decisão importante; paralelismo sem critério pode apenas aumentar custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

Validação contrafactual
Compare busca fixa e negociação iterativa. Meça cobertura por afirmação, diversidade relevante e tempo até evidência suficiente. Unidade de avaliação: requisição com fontes. Simule fonte lenta que poderia alterar a conclusão e fonte lenta que só acrescentaria contexto decorativo. A política deve esperar ou marcar insuficiência no primeiro caso e poder concluir no segundo. Registre essa classificação antes do resultado chegar, para não avaliar decisão de espera com informação retrospectiva que o controlador não possuía.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

USO AVANÇADO — Resposta com sistemas heterogêneos
Cenário: Fatos estão em documentos e APIs.
Estratégia: Consultar primeiro dados estruturados para campos exatos, depois textos para justificativas; marcar divergências entre canais.
Papel do modelo pequeno: 3–7B roteia campos; 8–14B integra.
Aceite proposto: Cada fato deve vir do canal adequado e revisão conhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

USO AVANÇADO — Análise sob prazo
Cenário: Uma fonte externa está lenta.
Estratégia: Preparar resposta parcial identificada e aguardar somente lacuna decisiva; atualizar quando evidência nova mudar conclusão.
Papel do modelo pequeno: 15–30B avalia impacto de lacunas.
Aceite proposto: Não afirmar completude enquanto fonte obrigatória estiver pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Roteador de necessidades tipadas para fontes autorizadas.
8–14B: Compositor de pacotes por afirmação com orçamento moderado.
15–30B: Planejador de aquisição condicional para perguntas interdependentes.
Requisitos de treino/runtime: Catálogo de fontes com custos e semântica de timeout; decisões de prioridade devem ser registradas.
Não aplicar quando: A política não consegue distinguir fonte opcional de evidência indispensável.

## T024:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Seleção de fontes inspira broker, sem confirmar componente LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Coordena aquisição e síntese de contexto; não usa o nome editorial como produto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q020.

## T024:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T024 → T152 [requires]
Como combinar: Negociar tokens entre aquisição, evidência e saída.
Interface: Orçamento, prioridade e custo estimado.
Condição: Cotas respeitarem requisitos obrigatórios.
Aceite proposto: Testar fonte grande que compete com outra indispensável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T024 → T067 [feeds]
Como combinar: Transformar lacuna específica em nova consulta.
Interface: claim_id, evidência faltante e limite de tentativas.
Condição: Consulta nova poder modificar a decisão.
Aceite proposto: Medir novas evidências úteis por tentativa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar timeout como inexistência de informação.
- Conservar conflitos entre fontes no pacote final.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade por prazo e custo; coordenação melhor não elimina limites do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T042, T067, T152

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

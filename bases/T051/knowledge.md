# T051 — Graph-Based Memory

**Nome canônico:** Graph-Based Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T051  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória baseada em grafos

## T051:C01 — conceito

Organiza informação persistida como entidades e relações, permitindo consultar conexões e caminhos. A semântica das arestas deve ser explícita: depende de, pertence a e contradiz não significam a mesma coisa. Um grafo é representação; qualidade depende de identidade, proveniência e atualização.

Como funciona:
- Definir entidades, tipos de relação e escopo.
- Associar cada relação a fonte e estado de verificação.
- Consultar vizinhança ou caminhos relevantes e recuperar evidências.

## T051:C02 — aplicacao

Quando usar:
- Dependências entre softwares, contratos e componentes.
- Memórias em que relações são mais úteis que documentos isolados.

Quando não usar:
- Evitar transformar cada coocorrência de palavras em relação factual.

Implementação proposta:
- Proposta: resolver identidade usando chaves do domínio antes de similaridade.
- Manter relações extraídas separadas das confirmadas.
- Limitar profundidade de expansão e incluir origem de cada aresta no resultado.

Aplicação LAI proposta:
Proposta LAI: mapear serviços, eventos e schemas do ecossistema com versão e fonte; recomendações de mudança devem abrir o contrato original.

## T051:C03 — riscos_validacao

Armadilhas:
- Uma fusão errada de entidades contamina muitos caminhos.
- Caminhos longos podem parecer explicações causais sem evidência causal.

Métricas sugeridas:
- Precisão de nós e relações.
- Recall de caminhos úteis e tempo de atualização.

Testes propostos:
- Criar entidades homônimas e exigir distinção pelo domínio.
- Remover evidência de uma aresta e verificar invalidação de resultados dependentes.

## T051:C04 — perguntas_proveniencia

Pergunta: Grafo de memória exige Neo4j?
Resposta: Não. A representação pode existir em banco relacional, documentos ou bibliotecas de grafo.

Pergunta: Uma conexão no grafo prova causa?
Resposta: Não. Causalidade exige significado da relação e evidência compatível, não apenas um caminho.

Pergunta: Toda aresta precisa apontar a uma fonte?
Resposta: Para uso como evidência, deve ter suporte rastreável ou status explícito de hipótese. Arestas puramente organizacionais também precisam de tipo claro.

Pergunta: Um ciclo no grafo é sempre erro?
Resposta: Não. Relações sociais ou dependências informacionais podem formar ciclos. A validade depende da semântica do tipo de relação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T051:C05 — mecanismo_avancado

Em memória por grafo, duas operações precisam ser separadas: identificar a entidade e decidir se uma nova relação substitui, complementa ou contradiz outra. Um nome parecido não resolve identidade; uma relação mais recente não substitui automaticamente todas as anteriores. A evolução das notas pode atualizar descrições úteis à busca, mas essas descrições derivadas precisam manter vínculos com as evidências que motivaram a mudança.

Condição de contorno:
O grafo perde confiabilidade quando extração probabilística é tratada como fato confirmado ou quando mudanças de ontologia reinterpretam arestas antigas sem migração explícita.

Contrato proposto:
- Entradas: Observações com entidades candidatas, tipos de relação, origem e contexto temporal.
- Saídas: Nós e arestas identificados, com decisões de resolução e registros de derivação.
- Estado: Ontologia versionada, aliases, evidências ligadas e histórico de revisão das relações.
- Invariante: Uma aresta derivada permanece distinguível da observação que a sustenta e de uma relação apenas hipotética.

Compromissos de projeto:
- Grafo explicita conexões úteis a perguntas relacionais e aumenta custo de manutenção de identidade.
- Atualização incremental evita reconstrução completa e exige invalidar caminhos dependentes quando uma relação muda.

## T051:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas organizações homônimas e inserir fatos diferentes em cada uma. A resolução deve manter identidades separadas; uma fusão deliberadamente errada deve ser reversível com seus vínculos de origem.

Plano de avaliação proposto:
Avaliação proposta: comparar grafo e índice de passagens em perguntas relacionais com mesmo orçamento de leitura. Medir precisão de entidades, sustentação das arestas, custo de atualização e caminhos inválidos; não confundir caminho encontrado com explicação comprovada.

Comparações:
- T029 (complements): GraphRAG usa estrutura para recuperação; memória por grafo também exige políticas de escrita e evolução ao longo do tempo.
- T077 (complements): Adicionar validade temporal às relações é uma especialização que permite consultar diferentes estados históricos.

Afirmação rastreável:
A-MEM conecta notas e atualiza suas representações; Graphiti mantém relações temporais ligadas aos episódios de origem.
Suporte: direct; fontes: V3A-S034, A-S035, V3A-S035
Limite: Essas implementações usam organizações distintas; nenhuma transforma ligações extraídas em causalidade identificada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T051:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou identidade e ontologia. Aqui memória em grafo mantém perspectivas por agente e caminhos de evidência sem confundir crença com mundo.

Projeto e decomposição
Separe grafo de fatos observados e grafo de crenças ou hipóteses do agente. Uma relação pode existir como crença sem estar confirmada no domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

Controle adaptativo
Faça consultas exigirem tipo de perspectiva e validade. Agregação de memórias de vários agentes deve preservar quem observou, quem inferiu e quem apenas repetiu a informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

Validação contrafactual
Compare grafo unificado e perspectivas separadas. Meça fusões incorretas, propagação de inferências e respostas que atribuem a um agente conhecimento que ele ainda não possuía. Unidade de avaliação: afirmação em grafo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

USO AVANÇADO — Equipe de agentes
Cenário: Trabalhadores veem subconjuntos distintos.
Estratégia: Registrar observações por origem e compartilhar evidências confirmadas; não fundir hipóteses contraditórias em uma relação única.
Papel do modelo pequeno: 3–7B extrai relações; 15–30B reconcilia.
Aceite proposto: Uma crença individual não pode virar consenso sem suporte adicional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

USO AVANÇADO — Investigação histórica
Cenário: É necessário explicar decisões passadas.
Estratégia: Consultar perspectiva e informações disponíveis ao decisor na época, distinguindo fatos descobertos posteriormente.
Papel do modelo pequeno: 8–14B lê subgrafo restrito.
Aceite proposto: Resposta deve evitar conhecimento retrospectivo na explicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de relações em vocabulário fechado e origem explícita.
8–14B: Leitor de subgrafo pequeno com perspectiva fixada.
15–30B: Reconciliador de perspectivas e contradições entre agentes.
Requisitos de treino/runtime: Entidades estáveis, campos de perspectiva e proveniência por aresta; expansão deve respeitar escopo.
Não aplicar quando: O sistema não consegue distinguir observação, inferência e repetição de outra fonte.

## T051:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C013 — Google / Knowledge Graph na busca Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Anúncio relata início da implantação a usuários da busca.
Mecanismo documentado: Entidades e relações permitem desambiguação e apresentação de fatos relacionados.
Correspondência com esta base: Grafo de conhecimento operacional; memória de agente não demonstrada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.
Limite: Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S018.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: TAO pertence à família de armazenamento em grafo, sem provar memória de agente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Grafo de evidência não implica memória episódica completa.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q021, V4A-Q023.

## T051:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T051 → T056 [requires]
Como combinar: Restringir conhecimento por perspectiva temporal.
Interface: valid_time, recorded_time e observador.
Condição: Consulta declarar o instante de conhecimento.
Aceite proposto: Inserir descoberta tardia e impedir vazamento retrospectivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S034, V4A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T051 → T075 [complements]
Como combinar: Reconciliar relações concorrentes sem apagar origem.
Interface: Arestas conflitantes, versões e fontes.
Condição: Critério de reconciliação ser explícito.
Aceite proposto: Preservar conflito quando evidência não decidir.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S034, V4A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não deduzir causalidade de caminho no grafo.
- Não contar agentes que repetem uma origem como fontes independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar atribuição correta de conhecimento e relações; densidade do grafo pode amplificar erro de extração.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T029, T057, T077

## Fontes primárias associadas

### A-S035 — Graphiti: Build Real-Time Knowledge Graphs for AI Agents

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grafo temporal de entidades, relações e episódios com rastreabilidade.

Limite: README consultado; sem auditoria de código, teste de escala ou confirmação de promessas comerciais.

### V3A-S034 — A-MEM: Agentic Memory for LLM Agents

[https://arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Notas estruturadas, conexão entre memórias e evolução das representações de notas anteriores.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S035 — Zep: A Temporal Knowledge Graph Architecture for Agent Memory

[https://arxiv.org/abs/2501.13956](https://arxiv.org/abs/2501.13956)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura temporal Graphiti para integração de conversas e dados estruturados com relações históricas.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S018 — Introducing the Knowledge Graph: things, not strings

[https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação gradual de entidades e relações na busca Google; não é GraphRAG moderno.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

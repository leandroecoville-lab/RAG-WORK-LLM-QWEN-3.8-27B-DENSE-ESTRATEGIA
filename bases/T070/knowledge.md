# T070 — Episodic Store

**Nome canônico:** Episodic Store  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T070  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repositório de episódios

## T070:C01 — conceito

Componente de armazenamento de episódios com índices, versões, relações e evidências. A memória episódica é o conceito; o store é sua implementação persistente. Precisa permitir recuperar o resumo de uma experiência e, quando necessário, abrir ações e artefatos originais.

Como funciona:
- Receber episódio com fronteiras e schema definidos.
- Persistir resumo, eventos associados e referências.
- Oferecer consultas por identidade, tempo, problema e resultado.

## T070:C02 — aplicacao

Quando usar:
- Muitas missões precisam reaproveitar experiências anteriores.
- Auditoria requer distinguir resultado relatado e resultado comprovado.

Quando não usar:
- Não tratar um índice vetorial de resumos como armazenamento completo dos episódios.

Implementação proposta:
- Proposta: usar episode_id, mission_id, environment_version e outcome_status.
- Manter eventos de origem imutáveis e resumos como projeções.
- Indexar fracassos e condições de aplicação, não apenas casos de sucesso.

Aplicação LAI proposta:
Proposta LAI: criar um store para missões da Helena com estado de verificação explícito; decisões de reutilização devem considerar versão e condições.

## T070:C03 — riscos_validacao

Armadilhas:
- Uma experiência pode ser fragmentada em episódios inconsistentes.
- Referências a logs temporários podem deixar o resumo sem evidência.

Métricas sugeridas:
- Episódios completos e referências resolvíveis.
- Precisão da recuperação de casos comparáveis.

Testes propostos:
- Reconstruir um episódio a partir do índice e abrir todas as evidências citadas.
- Consultar pelo tipo de falha e recuperar tanto correção quanto tentativa malsucedida relevante.

## T070:C04 — perguntas_proveniencia

Pergunta: Qual banco devo usar?
Resposta: O contrato e a carga orientam a escolha; armazenamento relacional com índice lexical pode ser suficiente inicialmente.

Pergunta: Devo guardar só o resumo para economizar?
Resposta: Mantenha originais conforme retenção. Sem eles, o episódio perde capacidade de auditoria e reinterpretação.

Pergunta: Timestamp de conclusão é uma boa chave de ordenação única?
Resposta: Pode haver empates, atrasos e episódios reabertos. Use critério determinístico adicional e semântica definida para atualizações.

Pergunta: O resumo deve ser o registro autoritativo?
Resposta: Somente se esse for um contrato conscientemente limitado. Para reconstrução, preserve eventos e artefatos que permitem verificar o que o resumo afirma.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T070:C05 — mecanismo_avancado

O store episódico precisa suportar operações com semânticas diferentes: localizar casos semelhantes, listar episódios de uma missão e reconstruir todos os eventos de um caso. Um top-k semântico atende à primeira operação, mas não comprova completude das outras. Paginação, ordenação estável e fronteiras de leitura tornam-se essenciais quando uma auditoria ou consolidação precisa percorrer todo o conjunto, inclusive registros pouco relevantes lexicalmente.

Condição de contorno:
Um banco de exemplos com apenas resumos e links expirados pode servir à orientação, mas não consegue comprovar a sequência operacional que os resumos descrevem.

Contrato proposto:
- Entradas: Episódios identificados, eventos de origem, estado do desfecho e metadados de missão e ambiente.
- Saídas: Resultados de busca ou enumeração com modo declarado, paginação e referências recuperáveis.
- Estado: Índices, revisões de ingestão, posição de atualização e política de ordenação por operação.
- Invariante: Busca ranqueada limitada nunca é apresentada como inventário completo de episódios elegíveis.

Compromissos de projeto:
- Índices por problema facilitam analogias e podem esconder casos raros sem uma via de enumeração.
- Guardar detalhes completos melhora auditoria e amplia armazenamento, manutenção e custos de leitura.

## T070:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar mais episódios que o limite padrão de busca, deixando uma falha relevante além da primeira página. A enumeração deve recuperá-la ou informar incompletude, sem concluir que todos os casos tiveram sucesso.

Plano de avaliação proposto:
Avaliação proposta: comparar busca semântica e enumeração filtrada nas respectivas tarefas. Medir recall de casos úteis, completude, estabilidade de paginação, recuperação dos artefatos e atraso de indexação; testar mudanças concorrentes durante a listagem.

Comparações:
- T049 (complements): A memória episódica define o conteúdo de uma experiência; o store oferece persistência e operações de acesso.
- T059 (complements): Eventos podem constituir a origem reconstruível dos episódios, enquanto resumos são projeções para busca.

Afirmação rastreável:
A documentação de stores do LangGraph explicita limites de listagem, paginação e ordenação dependente do backend.
Suporte: related; fontes: V3A-S032
Limite: É suporte para contratos de armazenamento; a fonte não implementa automaticamente o modelo episódico proposto aqui.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T070:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou top-k e enumeração. Aqui o store permite amostragem controlada e análise de cobertura sem enviesar avaliação pela recuperação.

Projeto e decomposição
Mantenha consultas de busca e de auditoria separadas. A primeira prioriza relevância; a segunda precisa enumerar ou amostrar população com probabilidades conhecidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

Controle adaptativo
Registre episódios pendentes, fracassados e incompletos. Excluir esses registros pode transformar o store numa coleção de sucessos e produzir procedimentos excessivamente otimistas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

Validação contrafactual
Compare resultados sobre episódios recuperados e sobre amostra independente. Meça viés de seleção, cobertura de falhas e perda por paginação; um top-k não define distribuição da população. Unidade de avaliação: população de episódios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

USO AVANÇADO — Revisão de desempenho
Cenário: Equipe quer saber quais falhas se repetem.
Estratégia: Consultar episódios por intervalo e status, amostrar de forma reproduzível e agregar causas somente quando sustentadas.
Papel do modelo pequeno: 3–7B categoriza; código agrega.
Aceite proposto: Contagens devem refletir população ou amostra explicitada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

USO AVANÇADO — Memória para decisão atual
Cenário: É preciso recuperar caso parecido.
Estratégia: Buscar por condições, incluir exemplos negativos elegíveis e preservar referência ao episódio completo.
Papel do modelo pequeno: 8–14B compara contexto.
Aceite proposto: Não inferir frequência de sucesso pela ordem de similaridade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de episódios com campos e status explícitos.
8–14B: Leitor de pequenos conjuntos relevantes com casos negativos.
15–30B: Analista de padrões de experiências com estatísticas calculadas externamente.
Requisitos de treino/runtime: IDs estáveis, paginação consistente, filtros temporais e estados de conclusão; índices são projeções do store.
Não aplicar quando: Não há forma de distinguir episódio ausente, incompleto ou excluído da consulta.

## T070:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Operador descreve migração real de todos os metadados e listagem fortemente consistente.
Mecanismo documentado: Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.
Correspondência com esta base: Listagem completa inspira enumeração de episódios; objeto não é episódio.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.
Limite: Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S007, V4A-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q008, V4A-Q023.

## T070:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T070 → T049 [feeds]
Como combinar: Retornar experiência com contexto suficiente.
Interface: Condições, ações, resultado e campos desconhecidos.
Condição: Recuperação preservar episódio completo ou link.
Aceite proposto: Testar episódio sem resultado e impedir preenchimento por suposição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S002, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T070 → T056 [requires]
Como combinar: Aplicar corte de conhecimento em auditoria histórica.
Interface: Tempos de ocorrência e registro.
Condição: Amostra usar perspectiva temporal declarada.
Aceite proposto: Inserir episódio atrasado e comparar consultas antes e depois.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S002, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não calcular taxa de sucesso usando apenas top-k.
- Não confundir deduplicação de relato com remoção de episódio distinto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de decisão com amostragem e busca adequadas; tamanho do store não mede memória efetivamente utilizável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T059, T060, T066

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

### V4A-S005 — Spanner: Google's Globally-Distributed Database

[https://research.google/pubs/spanner-googles-globally-distributed-database-2/](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco multiversão, transações externamente consistentes e incerteza temporal.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency

[https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração efetiva dos metadados do Cloud Storage para Spanner e consistência de listagem.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

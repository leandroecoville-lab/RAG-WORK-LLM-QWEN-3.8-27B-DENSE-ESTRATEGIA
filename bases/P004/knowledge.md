# P004 — LAI Memory Runtime

**Nome canônico:** LAI Memory Runtime  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** runtime proposto de memória LAI

## P004:C01 — conceito

LAI Memory Runtime é um nome editorial proposto para os serviços de persistência, consulta e evolução da memória do agente. Abrangeria escopos de sessão e de projeto, versões e referências às evidências. A proposta reúne princípios de stores, checkpoints e temporalidade; não representa uma plataforma existente comprovada pelas fontes nem pressupõe atualização dos pesos do modelo.

Como funciona:
- Separar estado de execução por sessão de informações reutilizáveis entre sessões, com namespaces explícitos.
- Registrar cada objeto com identidade, tipo, conteúdo, proveniência, versão e escopo de leitura e escrita.
- Quando o domínio exigir consultas históricas, distinguir tempo de validade do fato e tempo em que foi registrado.

## P004:C02 — aplicacao

Quando usar:
- Agentes que retomam trabalhos e precisam recordar decisões, artefatos e fatos sem depender da conversa atual.

Quando não usar:
- Como substituto de um índice de busca bem avaliado ou como evidência de que um fato extraído é correto.

Implementação proposta:
- Proposta: definir operações get, query, put e supersede com contratos diferentes para evidência, hipótese e decisão.
- Aplicar concorrência otimista às atualizações e preservar vínculos entre revisão anterior e nova, evitando sobrescrita silenciosa.
- Escolher armazenamento durável e política de retenção por tipo; publicar índices somente com a versão de origem identificada.

Aplicação LAI proposta:
Proposta LAI: fornecer a P005 uma camada única de contratos de memória, com implementação de armazenamento substituível e evidências preservadas por referência.

## P004:C03 — riscos_validacao

Armadilhas:
- Um checkpointer em memória volátil não demonstra recuperação após reinício do processo.
- Índice e registro canônico podem divergir; resultados devem informar versão e atrasos de indexação.
- Confundir a data do evento com a data de ingestão impede corrigir fatos recebidos tardiamente.

Métricas sugeridas:
- Durabilidade confirmada, conflitos de versão, atraso de indexação e consistência de consultas históricas.

Testes propostos:
- Aceite proposto: reiniciar o serviço após uma gravação confirmada e recuperar o mesmo objeto versionado.
- Testar duas atualizações concorrentes e um fato atrasado; exigir conflito explícito e respostas temporais coerentes.

## P004:C04 — perguntas_proveniencia

Pergunta: Persistir memória treina o modelo?
Resposta: Não. Nesta proposta os objetos ficam em armazenamento externo e precisam ser recuperados ou inseridos no contexto.

Pergunta: Por que separar sessão e projeto?
Resposta: Porque retomar um fluxo exige estado específico da sessão, enquanto decisões do projeto podem ser reutilizadas sob outro ciclo de execução.

Pergunta: O índice vetorial deve ser a única memória?
Resposta: A proposta mantém origem e histórico recuperáveis para reconstruir índices e explicar correções.

Pergunta: Uma correção apaga o erro anterior?
Resposta: Não por padrão: registra nova informação e permite consultar o que era conhecido em cada momento.

Escopo das fontes:
As fontes apoiam escopos, persistência e tempo; a combinação LAI e seus contratos permanecem propostas.

## P004:C05 — mecanismo_avancado

LAI Memory Runtime é aqui um nome de proposta para coordenar gravação, leitura temporal e proveniência de memórias. Cada atualização deve distinguir quando o fato vale no domínio e quando foi registrado. A promoção de uma observação para memória consolidada precisa apontar as evidências usadas e preservar contradições ainda não resolvidas. Recomenda-se tratar índices e resumos como projeções reconstruíveis, mantendo o registro autorizado de origem separado de conveniências de busca.

Condição de contorno:
Uma transação local não torna atômica a atualização de todo índice externo. A aplicação precisa declarar consistência, atraso tolerado e estratégia de reconstrução das projeções.

Contrato proposto:
- Entradas: Observação identificada, origem, escopo autorizado, tempos de validade e registro, versão esperada e política de retenção.
- Saídas: Memória versionada, referências de evidência, evento de atualização e resultado explícito de conflito ou deduplicação.
- Estado: Registro de memórias, histórico temporal, chaves de deduplicação e cursores das projeções de busca.
- Invariante: Toda memória promovida deve manter origem rastreável; corrigir um fato não pode reescrever silenciosamente o histórico de conhecimento.

Compromissos de projeto:
- Histórico temporal aumenta armazenamento, mas permite explicar decisões tomadas com informação disponível à época.
- Atualizar índices de forma assíncrona reduz acoplamento, porém exige controlar atraso e leituras de versões antigas.

## P004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: repetir o mesmo evento, inserir correção retroativa e interromper atualização do índice; verificar deduplicação, consultas temporais consistentes e reconstrução sem perda de origem.

Plano de avaliação proposto:
Avaliar uma sequência conhecida de fatos, correções e conflitos. Comparar armazenamento de último valor e memória versionada por acerto temporal, rastreabilidade, atraso de projeção e custo. Todos os testes de runtime descritos são propostos.

Comparações:
- T056 (complements): Bitemporalidade separa validade do fato e registro.
- T065 (complements): Transações delimitam confirmações locais.

Afirmação rastreável:
Transações agrupam operações locais; modelos temporais distinguem validade e registro de fatos.
Suporte: related; fontes: V3D-S020, A-S032
Limite: A composição LAI Memory Runtime é editorial; as fontes não comprovam sua existência ou implantação.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu persistência e projeções. Aqui LAI Memory Runtime é proposto com contratos explícitos de visibilidade após escrita e reconstrução.

Projeto e decomposição
Diferencie commit no registro canônico e visibilidade no índice. Uma escrita confirmada pode ainda não aparecer em busca; o cliente precisa receber revisão e cursor de projeção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

Controle adaptativo
Ofereça leitura por identidade para confirmar atualização recente e busca para descoberta. Exigir read-your-writes em toda busca pode custar mais; declare onde a garantia é necessária e como verificar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

Validação contrafactual
Compare leitura imediata, busca assíncrona e fallback ao canônico. Meça atraso de projeção, respostas obsoletas e tempo de reconstrução; durabilidade do banco não garante atualização do embedding. Unidade de avaliação: operação de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

USO AVANÇADO — Correção de memória ativa
Cenário: Usuário corrige fato usado no próximo turno.
Estratégia: Confirmar registro, retornar revisão e consultar diretamente a versão nova até índice alcançar cursor correspondente.
Papel do modelo pequeno: 3–7B extrai correção.
Aceite proposto: Próxima resposta não pode recuperar versão revogada como vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

USO AVANÇADO — Reconstrução de índice
Cenário: Embedding muda ou índice falha.
Estratégia: Reconstruir a partir do canônico em paralelo, validar amostra e trocar manifesto ativo sem interromper consultas pinadas.
Papel do modelo pequeno: 8–14B valida conteúdo; código reconstrói.
Aceite proposto: Nenhuma consulta pode combinar índices com versões incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de propostas tipadas e leitor de objetos identificados.
8–14B: Leitor de projeções com capacidade de detectar atraso e lacuna.
15–30B: Analista de conflitos entre registros e reconstruções, sem controlar transações livremente.
Requisitos de treino/runtime: Store canônico, cursor de projeção, versões e recuperação testável; componente LAI não está implementado neste pacote.
Não aplicar quando: O único registro é o índice vetorial ou o sistema não consegue dizer qual revisão foi lida.

## P004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Operador descreve migração real de todos os metadados e listagem fortemente consistente.
Mecanismo documentado: Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.
Correspondência com esta base: Inspira contrato de persistência; não demonstra runtime LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.
Limite: Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S007, V4A-S005.

V4A-C027 — Letta / Framework de agentes stateful
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.
Mecanismo documentado: Persistência do agente e ferramentas de memória externas ao modelo.
Correspondência com esta base: Inspira contratos do runtime proposto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.
Limite: Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S026, V2B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q023.

## P004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P004 → T065 [requires]
Como combinar: Confirmar registro e evento de atualização localmente.
Interface: Objeto, versão esperada, commit e evento.
Condição: Invariantes locais cobertos pela transação.
Aceite proposto: Interromper entre escrita e publicação e verificar recuperação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P004 → P007 [feeds]
Como combinar: Expor revisão e atraso para recuperação.
Interface: Objeto, index_revision e projection_cursor.
Condição: Retriever respeitar requisito de frescor.
Aceite proposto: Consultar logo após correção e detectar índice atrasado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P004 → T072 [requires]
Como combinar: Publicar manifesto coerente de projeções.
Interface: Store_revision, embedding e índices ativos.
Condição: Troca preservar leitores pinados.
Aceite proposto: Reconstruir índice e comparar objetos ausentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar confirmação do índice em prova de verdade.
- Não presumir atomicidade entre todos os serviços externos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência percebida pelo leitor; modelos maiores também erram quando a camada de memória entrega revisão obsoleta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T056, T060, T072, T075, P003, P005

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### V3D-S020 — PostgreSQL — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade e confirmação de operações agrupadas numa transação local.

Limite: A garantia não se estende automaticamente a serviços externos ou outros armazenamentos independentes.

### V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services

[https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transações serializáveis em partições e experiência com serviços Google em produção.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency

[https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração efetiva dos metadados do Cloud Storage para Spanner e consistência de listagem.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V2B-S002 — Stateful agents

[https://docs.letta.com/concepts/stateful-agents](https://docs.letta.com/concepts/stateful-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade persistente, memória compartilhada entre conversas do mesmo agente e distinção entre agentes locais e com backup em nuvem.

Limite: Documentação atual consultada; não comprova isolamento ou durabilidade de uma implantação específica.

### V4A-S005 — Spanner: Google's Globally-Distributed Database

[https://research.google/pubs/spanner-googles-globally-distributed-database-2/](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco multiversão, transações externamente consistentes e incerteza temporal.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

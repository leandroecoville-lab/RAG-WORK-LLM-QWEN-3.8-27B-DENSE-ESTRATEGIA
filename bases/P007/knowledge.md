# P007 — Memory Retriever

**Nome canônico:** Memory Retriever  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recuperador proposto de memória

## P007:C01 — conceito

Memory Retriever é um nome editorial proposto para localizar memórias relevantes e devolver evidências identificáveis, sem modificar o conhecimento armazenado. Poderia combinar filtros, busca lexical, vetorial e reranking. As fontes sustentam esses mecanismos individualmente; não confirmam um produto LAI com esse nome nem garantem que a combinação tenha qualidade suficiente para cada domínio.

Como funciona:
- Receber consulta, escopo de projeto, identidade do solicitante e instante de interesse quando a pergunta for temporal.
- Aplicar critérios de elegibilidade e recuperar candidatos por métodos adequados, combinando rankings sem tratar escores heterogêneos como probabilidades comparáveis.
- Reordenar, deduplicar e expandir filhos para pais quando necessário, devolvendo conteúdo e referências às versões originais.

## P007:C02 — aplicacao

Quando usar:
- Perguntas que dependem de decisões passadas, arquivos específicos ou fatos fora da janela ativa.

Quando não usar:
- Como mecanismo para converter similaridade semântica em veracidade, validade temporal ou autorização de acesso.

Implementação proposta:
- Proposta: definir um contrato search_memory com filtros explícitos e resultados contendo ID, versão, localização, evidência e motivo de seleção.
- Separar o conjunto de candidatos do contexto final; dimensionar a recuperação para que o reranker tenha alternativas úteis.
- Quando faltarem fontes elegíveis, devolver ausência ou insuficiência; não preencher o resultado com fatos apenas semanticamente próximos.

Aplicação LAI proposta:
Proposta LAI: fornecer a P001 evidências elegíveis e a P005 candidatos para reconciliação, mantendo a escrita sob contrato distinto.

## P007:C03 — riscos_validacao

Armadilhas:
- Filtrar somente depois de um top-k estreito pode eliminar todos os candidatos úteis.
- Uma memória revogada ainda pode ter alta similaridade; o estado de validade precisa ser considerado.
- Expandir um filho pode carregar um pai de outra versão se os vínculos não forem verificáveis.

Métricas sugeridas:
- Recall e ranking sobre perguntas rotuladas independentes, correção temporal, latência e proporção de evidências realmente utilizadas.

Testes propostos:
- Aceite proposto: perguntar por uma decisão substituída e exigir a versão válida no instante solicitado.
- Construir casos de código literal, paráfrase e ausência de resposta; avaliar recuperação e abstenção separadamente.

## P007:C04 — perguntas_proveniencia

Pergunta: O primeiro resultado é necessariamente o fato vigente?
Resposta: Não. Ranking mede adequação à consulta; vigência depende da versão, temporalidade e estado do registro.

Pergunta: Como avaliar um caso sem resposta no acervo?
Resposta: Rotular a ausência e verificar se o recuperador comunica insuficiência, em vez de entregar um candidato parecido como prova.

Pergunta: Score alto significa evidência verdadeira?
Resposta: Não. Ranking estima correspondência à consulta; validade e qualidade da fonte precisam de critérios próprios.

Pergunta: Por que testar o documento pai?
Resposta: Uma expansão pode reintroduzir conteúdo que a busca inicial filtrou corretamente.

Escopo das fontes:
Fontes apoiam recuperação, reranking e temporalidade; contrato e aceites são propostas editoriais.

## P007:C05 — mecanismo_avancado

Memory Retriever é proposto como interface de recuperação que recebe escopo, tempo e objetivo, além do texto da consulta. A filtragem precisa alcançar todas as rotas de busca e também a expansão de um trecho para seu documento pai. Combinar rankings lexicais e vetoriais pode ampliar cobertura, mas scores de origens diferentes não devem ser somados sem uma regra explícita. O retorno deve preservar por que cada evidência foi escolhida e qual versão estava disponível.

Condição de contorno:
Uma consulta histórica exige distinguir fatos válidos na data de interesse e fatos conhecidos na data da decisão. Recuperação recente por similaridade não responde automaticamente a essa pergunta temporal.

Contrato proposto:
- Entradas: Consulta, identidade autorizada, filtros temporais, tipos de memória, orçamento e versão dos índices.
- Saídas: Evidências com IDs, fontes, tempos, scores ou posições e indicação de cobertura insuficiente.
- Estado: Índices, mapeamento de documentos, versões de embeddings e políticas de fusão e expansão.
- Invariante: Filtrar apenas a lista final é insuficiente quando expansões ou etapas intermediárias podem expor conteúdo fora do escopo.

Compromissos de projeto:
- Busca híbrida melhora cobertura em alguns conjuntos, mas adiciona índices, latência e decisões de fusão.
- Reranking pode melhorar ordem dos candidatos, sem recuperar evidência que ficou fora da etapa inicial.

## P007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: criar documentos semanticamente iguais em escopos distintos e um pai com conteúdo restrito; verificar isolamento em busca lexical, vetorial, fusão e expansão de contexto.

Plano de avaliação proposto:
Comparar recuperação lexical, vetorial e híbrida com mesmas perguntas e filtros. Medir Recall@k, MRR, precisão das evidências, latência e violações de escopo; separar consultas temporais das perguntas factuais atuais.

Comparações:
- T027 (complements): Busca híbrida combina canais de candidatos.
- T032 (complements): Expansão parent-child exige manter escopo e proveniência.

Afirmação rastreável:
RRF funde rankings por posição; modelos temporais permitem distinguir validade e registro.
Suporte: related; fontes: A-S021, A-S032
Limite: A combinação, filtros e invariantes deste retriever são projeto editorial, não garantias dos produtos citados.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu filtros e ranking. Aqui Memory Retriever é proposto como serviço de evidência por requisito, com recuperação de apoio e contraposição.

Projeto e decomposição
Receba requisitos, não apenas uma string. O serviço deve distinguir localizar objeto exato, responder atributo, comparar alternativas e procurar evidência contrária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

Controle adaptativo
Distribua orçamento entre canais e fontes por contribuição exclusiva. Quando candidatos repetem mesma origem, ampliar diversidade pode ser mais útil que aumentar top-k do mesmo índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

Validação contrafactual
Compare busca global e recuperação por requisito. Meça cobertura de afirmações, evidências contraditórias encontradas e custo de expansão; não usar similaridade como substituto de validade. Unidade de avaliação: requisição de evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

USO AVANÇADO — Comparação de decisões
Cenário: Cada alternativa precisa suporte equivalente.
Estratégia: Criar consultas simétricas por critério, recuperar fontes independentes e devolver lacunas por alternativa antes da síntese.
Papel do modelo pequeno: 3–7B decompõe; 8–14B lê.
Aceite proposto: Nenhuma alternativa pode parecer melhor por ter sido mais pesquisada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

USO AVANÇADO — Correção de memória
Cenário: Fato antigo continua parecido com pergunta.
Estratégia: Aplicar validade e revisão antes de ranking, buscar também evento de correção e retornar conflito quando resolução ainda estiver pendente.
Papel do modelo pequeno: 15–30B integra histórico.
Aceite proposto: Resposta deve usar revisão elegível ou declarar insuficiência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reformulador de consultas fechadas e extrator de filtros.
8–14B: Leitor de candidatos com suporte e contradição rotulados.
15–30B: Planejador de busca multietapas para requisitos dependentes.
Requisitos de treino/runtime: Índices com origem, versões e elegibilidade; conjunto de consultas próprio para avaliar cobertura e abstenção.
Não aplicar quando: A fonte necessária não existe ou a recuperação é usada para modificar memória sem contrato de escrita.

## P007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Recuperador editorial pode adotar contrato semelhante, sem alegar adoção.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Inspira interface de recuperação; não comprova componente editorial.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q020.

## P007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P007 → T027 [complements]
Como combinar: Combinar canais conforme tipo de requisito.
Interface: Consulta, termos protegidos, filtros e orçamento.
Condição: Canais respeitarem mesma elegibilidade.
Aceite proposto: Testar código literal e paráfrase com orçamento igual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P007 → T028 [feeds]
Como combinar: Ordenar por capacidade de sustentar requisito.
Interface: Candidato, requisito, origem e tipo de suporte.
Condição: Contradições materiais não forem eliminadas.
Aceite proposto: Medir evidência suficiente na lista final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P007 → P001 [feeds]
Como combinar: Entregar evidências e lacunas à montagem.
Interface: requirement_id, trechos, referências e cobertura.
Condição: Builder preservar lacunas e conflitos.
Aceite proposto: Gerar pacote sem suporte para campo obrigatório e exigir insuficiência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não inferir ausência universal de resultado vazio.
- Não confundir múltiplos trechos da mesma fonte com corroboradores independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura por afirmação e fidelidade final; bom retriever amplia evidência disponível sem garantir capacidade geral do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T027, T032, T056, T067, P001, P004

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S020 — Retrieve & Re-Rank

[https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação inicial seguida de pontuação conjunta consulta-documento por cross-encoder.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S021 — Reciprocal rank fusion

[https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação por posições de múltiplos rankings, incluindo busca lexical e vetorial.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

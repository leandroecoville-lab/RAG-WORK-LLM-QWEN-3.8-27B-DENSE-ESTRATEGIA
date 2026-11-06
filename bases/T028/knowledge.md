# T028 — Reranking

**Nome canônico:** Reranking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T028  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reordenação de resultados; cross-encoder reranking

## T028:C01 — conceito

Reordena um conjunto inicial de candidatos com um avaliador mais caro ou específico. Um cross-encoder considera consulta e trecho conjuntamente. O reranker melhora seleção dentro dos candidatos disponíveis; não recupera um documento que a primeira etapa nunca encontrou.

Como funciona:
- Recuperar um conjunto amplo com busca eficiente.
- Pontuar pares consulta-trecho com o reranker.
- Selecionar evidências relevantes e diversas dentro do orçamento.

## T028:C02 — aplicacao

Quando usar:
- Busca inicial retorna muitos trechos aparentemente próximos.
- Perguntas dependem de distinções finas entre conceitos semelhantes.

Quando não usar:
- Não adicionar reranker antes de resolver recall insuficiente ou fontes ausentes.

Implementação proposta:
- Proposta: escolher modelo compatível com idioma e comprimento dos trechos.
- Manter consulta e documento sem truncar o detalhe decisivo.
- Comparar precisão final com e sem reranking e registrar os documentos descartados.

Aplicação LAI proposta:
Proposta LAI: usar para distinguir técnicas com nomes próximos, como compressão textual e destilação paramétrica, após garantir que ambas são recuperáveis.

## T028:C03 — riscos_validacao

Armadilhas:
- Reranker treinado em outro domínio pode preferir textos genéricos.
- Scores altos não certificam verdade, validade temporal ou permissão de acesso.

Métricas sugeridas:
- nDCG, MRR e precisão dos trechos usados na resposta.
- Latência por par e total por consulta.

Testes propostos:
- Colocar documento correto fora dos candidatos e confirmar a limitação.
- Testar duas definições parecidas que diferem por modificar ou não os pesos.

## T028:C04 — perguntas_proveniencia

Pergunta: Reranking é geração de resposta?
Resposta: Não. É seleção e ordenação de evidências antes ou durante a montagem do contexto.

Pergunta: O primeiro resultado deve ser tratado como verdadeiro?
Resposta: Não. Relevância e verdade são dimensões diferentes; a fonte e a evidência ainda precisam ser avaliadas.

Pergunta: Posso excluir um candidato por score abaixo de um valor copiado?
Resposta: Somente após calibrar o uso desse score no modelo e domínio. Escalas de rerankers diferentes não são intercambiáveis.

Pergunta: Uma passagem bem ranqueada basta para citar uma conclusão?
Resposta: Não. Relevância e sustentação são diferentes; a conclusão precisa ser conferida contra o conteúdo e suas condições.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T028:C05 — mecanismo_avancado

O teto do reranker é determinado pelos candidatos recebidos. Separar recall da primeira etapa e qualidade da ordenação evita culpar o avaliador por um documento ausente. Também é necessário conhecer o truncamento interno de consulta e passagem: um classificador pode receber apenas o início do trecho, atribuindo score sem observar a parte que contém a evidência decisiva.

Condição de contorno:
O estágio não ajuda quando a evidência relevante está fora do conjunto candidato ou quando seu custo consome o prazo disponível sem melhorar a seleção final.

Contrato proposto:
- Entradas: Consulta, candidatos identificados e limite efetivo do modelo de ranking.
- Saídas: Ordem revisada e scores associados às versões originais.
- Estado: Modelo, configuração de truncamento, candidatos iniciais e seleção final.
- Invariante: Score de relevância não é apresentado como probabilidade calibrada de verdade ou suporte lógico.

Compromissos de projeto:
- Mais candidatos elevam o teto de recall e o trabalho de avaliação.
- Modelos conjuntos capturam interação consulta-texto, mas são mais caros que comparar vetores pré-computados.

## T028:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar a evidência relevante no fim de uma passagem longa e depois fora do conjunto candidato. O diagnóstico deve distinguir truncamento do reranker de falha de recuperação inicial.

Plano de avaliação proposto:
Avaliação proposta: usar a mesma lista para comparar ordenação original e reranking, e depois variar sua cobertura. Medir ranking, suporte das passagens selecionadas, duração e custo; incluir uma ordenação ideal dos candidatos para estimar o teto disponível.

Comparações:
- T027 (complements): A união híbrida pode aumentar a diversidade de candidatos oferecida ao reranker.
- T037 (distinct_from): Reranking ordena unidades; compressão condicionada à pergunta modifica a representação enviada.

Afirmação rastreável:
O trabalho de Nogueira e Cho aplica BERT à reordenação de passagens em função da consulta.
Suporte: direct; fontes: V3A-S025
Limite: A técnica publicada é uma implementação específica; modelos atuais têm outros limites e distribuições de scores.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T028:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou teto de candidatos e truncamento. Aqui reranking ganha comparação em pares difíceis e decisão de parada por utilidade marginal.

Projeto e decomposição
Separe relevância temática de capacidade de sustentar resposta. Um texto sobre o assunto pode não conter a condição pedida; rótulos de treino e validação precisam refletir suporte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

Controle adaptativo
Use segunda rodada apenas quando os melhores candidatos forem redundantes ou contraditórios. O orçamento deve priorizar diversidade de evidência, preservando versões e documentos de autoridade necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

Validação contrafactual
Compare cross-encoder, julgamento pequeno por pares e ranking original. Meça posição da primeira evidência suficiente, diversidade útil e latência por tamanho de lista; incluir documentos longos que excedem entrada do reranker. Unidade de avaliação: lista de candidatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

USO AVANÇADO — Pergunta com exceção
Cenário: Resultados populares omitem condição rara.
Estratégia: Rerankear pelo requisito completo e manter candidato que contém a exceção mesmo com menor similaridade global.
Papel do modelo pequeno: 3–7B julga suporte binário em trechos.
Aceite proposto: Exceção deve chegar ao leitor em consultas que a exigem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

USO AVANÇADO — Contradições de versão
Cenário: Dois documentos parecem igualmente relevantes.
Estratégia: Aplicar elegibilidade temporal antes de relevância; sinalizar conflito quando ambos forem válidos em escopos diferentes.
Papel do modelo pequeno: 8–14B explica distinção de escopo.
Aceite proposto: Não promover documento obsoleto por linguagem mais parecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de suporte em pares curtos, preferencialmente especializado.
8–14B: Reranker de listas pequenas com justificativa vinculada a trecho.
15–30B: Revisor de candidatos conflitantes, usado somente em listas difíceis.
Requisitos de treino/runtime: Candidatos com evidência rotulada e tamanho real de entrada; considerar modelos menores que 3B quando suficientes.
Não aplicar quando: A evidência correta está fora do conjunto inicial ou o custo de julgamento supera benefício.

## T028:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C008 — Microsoft / Bing: transformers na busca global
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Operador afirma modelos transformer aplicados às consultas Bing globais no período descrito.
Mecanismo documentado: Compreensão contextual de consultas e páginas com inferência otimizada.
Correspondência com esta base: Ranking neural é relacionado; fonte não especifica integralmente o pipeline desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Empregar modelo compacto para julgar pares consulta-trecho, medindo custo e ordenação.
Limite: BERT destilado do relato não é um gerador 3–30B; números de infraestrutura não são transportáveis. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S008.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Segundo ranking explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q016.

## T028:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T028 → T027 [requires]
Como combinar: Receber candidatos diversos antes de reordenar.
Interface: União de resultados e proveniência de cada canal.
Condição: Filtros aplicados de maneira consistente.
Aceite proposto: Testar recuperação da evidência antes de atribuir erro ao reranker.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T028 → T037 [feeds]
Como combinar: Comprimir depois de selecionar suporte.
Interface: Trechos selecionados e requisitos da pergunta.
Condição: Compressão preservar evidência que justificou posição.
Aceite proposto: Comparar decisão com trecho integral e comprimido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar score de ranking como verdade.
- Não avaliar somente documentos que o próprio reranker selecionou.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar suporte entregue ao leitor e custo por pergunta; qualidade de ranking não equivale à qualidade de raciocínio geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T027, T036, T198

## Fontes primárias associadas

### A-S020 — Retrieve & Re-Rank

[https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação inicial seguida de pontuação conjunta consulta-documento por cross-encoder.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S025 — Passage Re-ranking with BERT

[https://arxiv.org/abs/1901.04085](https://arxiv.org/abs/1901.04085)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de BERT para reordenar passagens em função da consulta, como estágio específico de recuperação.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S026 — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models

[https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Generalização entre domínios e comparação de recuperadores lexicais, densos e reranking com custos distintos.

Limite: Consultados resumo e conclusões gerais de avaliação; perguntas e gabaritos do benchmark não foram consultados. Comparações publicadas não se transferem automaticamente a modelos atuais.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S008 — Bing delivers its largest improvement in search experience using Azure GPUs

[https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos transformer aplicados às consultas Bing; inferência otimizada e compreensão da consulta.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T027 — Hybrid Retrieval — BM25 + vetores

**Nome canônico:** Hybrid Retrieval — BM25 + Vetores  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T027  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** hybrid search; busca híbrida; Hybrid Retrieval — BM25 + Vetores

## T027:C01 — conceito

Combina busca lexical e vetorial para aproveitar correspondência exata e semelhança de significado. BM25 ajuda com siglas, códigos e nomes; vetores podem recuperar paráfrases. Os rankings precisam ser fundidos de forma explícita, pois seus escores geralmente não são comparáveis diretamente.

Como funciona:
- Executar ambos os recuperadores com filtros equivalentes.
- Unificar candidatos por identidade documental.
- Combinar posições, por exemplo por RRF, e opcionalmente reranquear.

## T027:C02 — aplicacao

Quando usar:
- Bases técnicas com códigos exatos e perguntas em linguagem natural.
- Consultas que misturam nomes conhecidos e descrição de problema.

Quando não usar:
- Não chamar uma busca lexical com expansão de sinônimos de híbrida vetorial se nenhum embedding for usado.

Implementação proposta:
- Proposta: versionar analisador lexical, modelo de embedding e parâmetros de fusão.
- Garantir que ambos os lados busquem o mesmo snapshot autorizado.
- Calibrar conjunto de candidatos antes de escolher o top-k final.

Aplicação LAI proposta:
Proposta LAI: manter busca lexical funcional como base e adicionar embeddings quando um modelo de vetorização estiver configurado e avaliado.

## T027:C03 — riscos_validacao

Armadilhas:
- Somar escores sem normalização favorece um recuperador arbitrariamente.
- Filtros diferentes entre índices podem causar vazamento ou inconsistência.

Métricas sugeridas:
- Recall@k e nDCG comparados a cada recuperador sozinho.
- Latência dos dois caminhos e custo do reranker.

Testes propostos:
- Testar códigos raros e paráfrases sem palavras em comum.
- Verificar que documentos expirados não entram por um dos caminhos.

## T027:C04 — perguntas_proveniencia

Pergunta: RRF mistura os valores de BM25 e cosine?
Resposta: Ele usa posições nos rankings, evitando assumir que os escores têm a mesma escala.

Pergunta: Busca híbrida sempre vence?
Resposta: Não. Qualidade de índices, filtros e fusão deve ser medida no conjunto de perguntas do domínio.

Pergunta: Peso igual significa contribuição igual?
Resposta: Não. Escalas, cobertura e distribuição dos scores importam. Mesmo após normalização, pesos iguais não garantem influência semântica equivalente.

Pergunta: Qual canal devo remover se quiser reduzir custo?
Resposta: Meça a evidência exclusiva que cada um recupera nas consultas relevantes. A decisão por média agregada pode prejudicar códigos raros ou linguagem do domínio.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T027:C05 — mecanismo_avancado

A fusão começa antes da soma: ambos os canais precisam usar identidades e filtros compatíveis. Na normalização por conjunto retornado, mudar a quantidade de candidatos altera a escala dos escores, mesmo para um documento cujo score bruto ficou igual. RRF reduz dependência das escalas, mas troca intensidade de relevância por posições e continua sensível à cobertura de cada lista.

Condição de contorno:
Combinar dois rankings que falham nos mesmos documentos pode acrescentar custo sem recall; somar escores não calibrados pode deixar um canal dominar arbitrariamente.

Contrato proposto:
- Entradas: Consulta, índices alinhados, filtros comuns e política de fusão.
- Saídas: Ranking deduplicado com posição e contribuição de cada canal.
- Estado: Versões dos índices, embeddings, pesos ou parâmetros de fusão.
- Invariante: Um documento inelegível não reaparece pela união de um canal com filtros menos restritivos.

Compromissos de projeto:
- Normalização preserva diferenças de score e depende da distribuição de candidatos.
- Fusão por ranking evita comparar escalas diretamente, mas perde informação sobre distância entre posições.

## T027:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir um outlier lexical e variar o tamanho das listas. Conferir se a fusão muda como previsto e se o resultado continua respeitando os filtros em ambos os canais.

Plano de avaliação proposto:
Avaliação proposta: comparar BM25, vetores, RRF e normalização sobre o mesmo corpus. Controlar candidatos e orçamento final; medir recall complementar, qualidade do topo, latência e desempenho por consultas com identificadores e paráfrases.

Comparações:
- T028 (complements): Reranking pode avaliar a união de candidatos depois da fusão.
- T009 (complements): A busca híbrida implementa a etapa de recuperação, sem resolver sozinha o uso da evidência pelo gerador.

Afirmação rastreável:
OpenSearch calcula estatísticas de normalização a partir dos resultados retornados por cada cláusula.
Suporte: direct; fontes: V3A-S022
Limite: A consequência depende da técnica de normalização; não deve ser generalizada a toda fusão híbrida.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T027:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou fusão de escores. Aqui canais recebem orçamento conforme sinais da consulta e são avaliados por contribuição exclusiva.

Projeto e decomposição
Consultas com códigos literais exigem quota lexical protegida. Paráfrases e descrições vagas podem justificar mais candidatos vetoriais. O ajuste deve ocorrer antes de reranking, preservando filtros comuns.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

Controle adaptativo
Registre candidatos encontrados exclusivamente por cada canal. Quando ambos retornam quase o mesmo conjunto, manter duas buscas pode custar mais sem ampliar cobertura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

Validação contrafactual
Compare fusão fixa e orçamento condicionado por intenção com o mesmo número total de candidatos. Separe consultas de identificador, terminologia rara e paráfrase; médias globais podem esconder regressão crítica. Unidade de avaliação: consulta e candidatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

USO AVANÇADO — Suporte de API
Cenário: Usuário fornece erro exato ou descrição livre.
Estratégia: Detectar identificador sem removê-lo, recuperar lexicalmente e complementar semanticamente quando o termo não aparecer. Rerankear conjunto deduplicado.
Papel do modelo pequeno: 3–7B extrai sinais; 8–14B lê candidatos.
Aceite proposto: Exigir recuperação do código exato quando presente no corpus.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

USO AVANÇADO — Pesquisa de decisões
Cenário: O usuário não lembra a formulação original.
Estratégia: Gerar consulta semântica preservando nomes e datas; recuperar também registros literais desses filtros.
Papel do modelo pequeno: 15–30B sintetiza decisões relacionadas.
Aceite proposto: Não confundir decisão de entidade homônima com correspondência válida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator determinístico assistido de códigos, nomes e datas.
8–14B: Reformulador controlado de intenção para canal vetorial.
15–30B: Integrador de evidências de canais diferentes e conflitos.
Requisitos de treino/runtime: Índices versionados, fusão explícita e métricas por canal; orçamento total deve permanecer comparável.
Não aplicar quando: Um único canal já cobre os casos relevantes com menor custo e sem regressão nas classes raras.

## T027:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Documenta canal híbrido com RRF como entrada elegível.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q020.

## T027:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T027 → T028 [feeds]
Como combinar: Rerankear união deduplicada dos canais.
Interface: document_id, posições lexicais/vetoriais e filtros.
Condição: Candidatos elegíveis e versões compatíveis.
Aceite proposto: Medir ganho de ranking sem perder candidatos exclusivos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T027 → T036 [complements]
Como combinar: Preservar identificadores na reformulação.
Interface: Consulta original, termos protegidos e expansão.
Condição: Expansão não substituir requisito literal.
Aceite proposto: Testar códigos parecidos e nomes com acentos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não somar escores heterogêneos sem regra validada.
- Não remover candidato raro só por aparecer em um canal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura e evidência final com contexto equivalente; recuperação forte não garante leitura correta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T028, T036

## Fontes primárias associadas

### A-S021 — Reciprocal rank fusion

[https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação por posições de múltiplos rankings, incluindo busca lexical e vetorial.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S022 — Normalization processor

[https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/](https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Normalização e combinação de scores; estatísticas calculadas sobre candidatos retornados e sensibilidade ao tamanho desse conjunto.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

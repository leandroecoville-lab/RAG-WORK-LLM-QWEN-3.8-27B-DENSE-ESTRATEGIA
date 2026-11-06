# T011 — Semantic Chunking

**Nome canônico:** Semantic Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T011  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação semântica

## T011:C01 — conceito

Escolhe fronteiras de trechos a partir de mudanças de significado, frequentemente comparando embeddings de sentenças ou grupos vizinhos. A noção de mudança depende do modelo e do limiar. A palavra semântico não garante automaticamente melhor recuperação.

Como funciona:
- Segmentar o texto em sentenças ou unidades iniciais.
- Medir a proximidade entre grupos vizinhos e propor fronteiras.
- Aplicar limites de tamanho e preservar posições na fonte.

## T011:C02 — aplicacao

Quando usar:
- Documentos longos que alternam temas sem cabeçalhos claros.
- Texto livre no qual cortes fixos separam explicações relacionadas.

Quando não usar:
- Não substitui um parser quando a estrutura formal do documento já é conhecida.

Implementação proposta:
- Proposta: testar limiares em documentação portuguesa e código misto.
- Impor teto em tokens do embedder mesmo quando não aparece mudança temática.
- Comparar custo de ingestão e recall com uma divisão recursiva simples.

Aplicação LAI proposta:
Proposta LAI: experimentar em transcrições e bases teóricas; manter fronteiras e documentos originais para revisar erros do segmentador.

## T011:C03 — riscos_validacao

Armadilhas:
- Paráfrases podem esconder uma mudança decisiva de regra.
- Pontuação ruim e transcrições ruidosas comprometem a segmentação inicial.

Métricas sugeridas:
- Coesão dos trechos e recall por pergunta.
- Custo de embeddings por documento ingerido.

Testes propostos:
- Inserir mudança de tema com vocabulário parecido e inspecionar a fronteira.
- Verificar que um capítulo homogêneo extenso não excede o limite de embedding.

## T011:C04 — perguntas_proveniencia

Pergunta: Semantic chunking usa sempre uma LLM geradora?
Resposta: Não. Muitas implementações usam embeddings e regras de distância, sem geração de texto.

Pergunta: Devo substituir todos os trechos fixos?
Resposta: Só após comparar em perguntas reais. A complexidade e o custo adicionais precisam produzir ganho observado.

Pergunta: Limiar por percentil evita calibragem?
Resposta: Não. Ele troca a escala absoluta por uma regra relativa, cuja frequência de cortes ainda precisa ser justificada e testada.

Pergunta: Coerência do chunk basta para boa recuperação?
Resposta: Não. A unidade também precisa conter o fato e suas condições em tamanho que o recuperador e o gerador utilizem adequadamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T011:C05 — mecanismo_avancado

O detector de fronteiras depende de como representa cada sentença e seu entorno. Um limiar absoluto de distância e um percentil das distâncias do próprio documento produzem comportamentos diferentes: o segundo pode impor cortes até em um texto uniforme. Mudanças de idioma, listas e tabelas também alteram a distribuição dos escores sem necessariamente representar uma troca real de assunto.

Condição de contorno:
Quando coerência local já é preservada por seções naturais, o cálculo semântico pode acrescentar custo sem melhorar a evidência recuperada.

Contrato proposto:
- Entradas: Texto, segmentação de sentenças, embedding e política explícita de fronteiras.
- Saídas: Chunks com escores de corte, offsets e limites de tamanho.
- Estado: Versões do segmentador e do modelo, mais distribuição observada de tamanhos.
- Invariante: A fronteira semântica não elimina a necessidade de limite operacional do consumidor.

Compromissos de projeto:
- Grupos maiores preservam continuidade, mas podem acumular assuntos independentes.
- Ajustar cortes por documento adapta a distribuição, porém dificulta comparar escores entre coleções.

## T011:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar um documento uniforme e outro com mudança de idioma sem mudança de assunto. Verificar cortes artificiais e a preservação de referências que atravessam a fronteira.

Plano de avaliação proposto:
Avaliação proposta: comparar tamanho fixo, divisão estrutural e semântica sob orçamento final equivalente. Controlar embedding e reranker; medir ingestão, distribuição de tamanho, evidência recuperada e resposta, incluindo documentos fora do domínio de ajuste.

Comparações:
- T010 (alternative): Tamanho fixo fornece baseline de custo e permite identificar ganhos atribuíveis às fronteiras.
- T033 (alternative): Estrutura editorial pode oferecer fronteiras úteis sem inferir mudança de assunto por vetor.

Afirmação rastreável:
O estudo de Qu e colaboradores encontrou benefícios inconsistentes da segmentação semântica nas tarefas examinadas.
Suporte: direct; fontes: V3A-S013
Limite: Não é prova de inutilidade; o resultado exige avaliar domínio, baseline e custo específicos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T011:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 questionou custo e limiar semântico. Aqui o foco é segmentação estável perante pequenas edições e adaptação por domínio.

Projeto e decomposição
Uma edição curta pode mudar várias fronteiras quando o limiar depende da distribuição do documento. Compare estabilidade dos IDs e custo de reindexação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

Controle adaptativo
Calibre segmentação separadamente para narrativa, perguntas frequentes e documentação técnica. Similaridade entre frases não identifica automaticamente unidade útil de resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

Validação contrafactual
Meça qualidade de recuperação e churn de chunks após alterações locais. Um ganho pequeno pode não justificar reconstrução frequente do índice. Unidade de avaliação: família de documentos. Uma edição de pontuação e outra de assunto devem produzir efeitos distintos. A primeira idealmente preserva a organização útil; a segunda pode exigir nova divisão. Medir churn de IDs, embeddings refeitos e respostas alteradas torna visível o custo operacional da segmentação semântica, que uma avaliação estática de recuperação tende a omitir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

USO AVANÇADO — Documentos vivos
Cenário: A base recebe edições diárias.
Estratégia: Identificar regiões alteradas, recomputar fronteiras locais e comparar com segmentação integral antes de publicar.
Papel do modelo pequeno: 3–7B apenas valida tópico de fronteiras candidatas.
Aceite proposto: Mudança local não deve esconder evidência fora da região.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

USO AVANÇADO — Corpus multilíngue
Cenário: Mesmos temas aparecem em idiomas diferentes.
Estratégia: Calibrar por idioma e testar mistura de termos técnicos; preservar identificadores literais independentemente do embedding.
Papel do modelo pequeno: 8–14B verifica coerência do segmento.
Aceite proposto: Cobertura deve permanecer estável entre idiomas avaliados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Validador binário de fronteira candidata em poucos parágrafos.
8–14B: Revisor de continuidade temática e exceções entre segmentos.
15–30B: Integrador de segmentos heterogêneos, sem decidir fronteiras por intuição livre.
Requisitos de treino/runtime: Embedding versionado e conjunto de validação por domínio; trocar embedding exige recalibração.
Não aplicar quando: O custo de reindexação supera benefício ou documento exige separadores estruturais rígidos.

## T011:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Fronteiras por distância semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T011:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T011 → T072 [requires]
Como combinar: Publicar segmentação como versão do índice.
Interface: Documento, embedding, limiar e mapa de fronteiras.
Condição: Cada resultado apontar versão compatível.
Aceite proposto: Consultar durante atualização e detectar mistura de versões.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, V3A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T011 → T033 [complements]
Como combinar: Respeitar estruturas antes da distância semântica.
Interface: Blocos tipados e fronteiras permitidas.
Condição: Tabelas e código manterem integridade.
Aceite proposto: Injetar tabela semanticamente heterogênea e impedir corte destrutivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, V3A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar limiar entre modelos sem validação.
- Medir mudança de fronteira causada por ruído de OCR.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retorno útil por token e estabilidade de atualização; coerência textual não prova utilidade na resposta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T012, T034

## Fontes primárias associadas

### A-S041 — Semantic splitter

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de parsers semânticos e janelas de sentenças.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S013 — Is Semantic Chunking Worth the Computational Cost?

[https://arxiv.org/abs/2410.13070](https://arxiv.org/abs/2410.13070)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de segmentação semântica e tamanho fixo em recuperação de documentos, evidência e respostas; ganhos não universais.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

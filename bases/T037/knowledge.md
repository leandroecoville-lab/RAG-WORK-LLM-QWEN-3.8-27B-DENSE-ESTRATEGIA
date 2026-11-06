# T037 — Query-Aware Compression

**Nome canônico:** Query-Aware Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T037  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão orientada à consulta

## T037:C01 — conceito

Reduz um conjunto de informações levando em conta a pergunta atual. Preserva conteúdo que ajuda a responder aquela consulta e pode descartar informação útil para outras. O resultado é uma representação condicionada à pergunta, não um resumo universal do documento.

Como funciona:
- Receber pergunta e documentos candidatos já autorizados.
- Pontuar passagens por utilidade para as condições da consulta.
- Preservar evidências e qualificações dentro do orçamento.

## T037:C02 — aplicacao

Quando usar:
- RAG retorna documentos extensos com poucos trechos relevantes.
- Perguntas muito específicas sobre um acervo amplo.

Quando não usar:
- Não reutilizar a versão comprimida para uma nova pergunta sem reavaliar o que foi omitido.

Implementação proposta:
- Proposta: incluir hash da pergunta e versão documental nos metadados.
- Proteger trechos que definem exceções, unidades e escopo.
- Armazenar offsets da seleção e indicar campos da pergunta ainda sem evidência.

Aplicação LAI proposta:
Proposta LAI: usar para montar respostas sobre mecanismos específicos, mantendo definições exatas e limitações; uma seleção para custo não deve ser reutilizada para compatibilidade.

## T037:C03 — riscos_validacao

Armadilhas:
- O compressor pode escolher apenas trechos que confirmam uma resposta provável.
- Compressão agressiva pode remover a relação entre condição e conclusão.

Métricas sugeridas:
- Cobertura de cada requisito da pergunta.
- Tokens economizados, fidelidade e tempo do compressor.

Testes propostos:
- Fazer duas perguntas diferentes sobre o mesmo documento e comparar seleções.
- Incluir evidência contraditória e exigir que ambas as posições relevantes sobrevivam.

## T037:C04 — perguntas_proveniencia

Pergunta: É igual a resumir o documento inteiro?
Resposta: Não. A relevância é definida pela consulta; informações importantes para outras tarefas podem ficar de fora.

Pergunta: A consulta também pode ser comprimida?
Resposta: Pode, mas deve preservar intenção, negação, identidade e escopo; perder isso invalida a seleção.

Pergunta: Como cachear a compressão?
Resposta: Inclua pergunta ou intenção formal, versões das fontes e configuração do compressor. Cache por documento apenas mistura seleções feitas para objetivos diferentes.

Pergunta: Uma síntese fiel basta para responder bem?
Resposta: Não. Ela pode ser fiel ao que selecionou e omitir uma condição indispensável. Fidelidade e suficiência precisam ser avaliadas separadamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T037:C05 — mecanismo_avancado

O compressor condicionado à pergunta implementa uma decisão sobre utilidade futura, não apenas sobre relevância lexical imediata. Em problemas com várias etapas, um trecho aparentemente secundário pode conter a ligação necessária para a próxima busca. RECOMP também permite saída vazia quando os documentos não acrescentam informação útil, evitando alimentar o gerador com contexto irrelevante. Essa escolha exige distinguir ausência de utilidade e ausência de evidência.

Condição de contorno:
Uma representação comprimida perde validade quando muda a finalidade, a pergunta ou a versão das fontes; correspondência temática não garante reutilização segura.

Contrato proposto:
- Entradas: Pergunta, documentos candidatos, orçamento e requisitos de sustentação da resposta.
- Saídas: Trechos ou síntese condicionada, referências de suporte e campos sem cobertura.
- Estado: Identidade da consulta, versões documentais, seletor e motivos de descarte recuperáveis.
- Invariante: Saída vazia não é registrada automaticamente como prova de que a afirmação consultada é falsa.

Compromissos de projeto:
- Seleção agressiva reduz leitura, mas aumenta risco de excluir pontes necessárias a inferências posteriores.
- Compressão treinada para o gerador pode melhorar compatibilidade e restringe transferência entre tarefas e modelos.

## T037:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar duas fontes em que a ligação depende de uma definição pouco semelhante à pergunta. O compressor deve preservar a ponte ou indicar cobertura insuficiente, sem fabricar a conexão.

Plano de avaliação proposto:
Avaliação proposta: comparar contexto integral, seleção extrativa e síntese com custo completo de compressão e geração. Medir sustentação, recall de relações intermediárias e erros por falsa ausência; repetir após mudança de pergunta para detectar reutilização indevida.

Comparações:
- T036 (complements): A consulta pode ser adaptada antes da busca, mas a compressão precisa respeitar a intenção original.
- T020 (complements): Um compressor aprendido pode ser condicionado à consulta; aprendizado e condicionamento são dimensões diferentes.

Afirmação rastreável:
RECOMP estuda compressores extrativos e abstrativos orientados ao desempenho posterior e permite contexto vazio quando não acrescenta utilidade.
Suporte: direct; fontes: V3A-S003
Limite: Os experimentos do artigo não justificam um limiar universal de descarte nem garantem cobertura de tarefas novas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T037:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou utilidade e pontes de evidência. Aqui compressão por consulta produz pacotes diferentes para resposta e verificação.

Projeto e decomposição
O leitor precisa de suporte suficiente; o verificador precisa também de contexto que possa desmentir a resposta. Usar um único recorte altamente favorável para ambos enfraquece auditoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

Controle adaptativo
Preserve identificadores e condições em faixa protegida, compactando explicações periféricas. A seleção deve poder retornar vazio sem obrigar o leitor a preencher uma resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

Validação contrafactual
Compare pacote único e pacote de verificação expandido. Meça respostas sustentadas, falsos aceites do verificador e custo adicional; avaliar perguntas cuja exceção fica fora da frase mais semelhante. Unidade de avaliação: consulta e documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

USO AVANÇADO — Resposta factual curta
Cenário: Documento longo contém um número condicionado.
Estratégia: Extrair número, unidade, população e período; manter parágrafo adjacente para verificar ressalvas.
Papel do modelo pequeno: 3–7B lê campos; 8–14B verifica escopo.
Aceite proposto: Nenhum valor pode ser citado sem seus qualificadores relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

USO AVANÇADO — Comparação de argumentos
Cenário: Há evidências dos dois lados.
Estratégia: Produzir recortes separados de apoio e oposição, com ligação entre eles; não reduzir tudo a conclusão única.
Papel do modelo pequeno: 15–30B integra posições.
Aceite proposto: A síntese deve preservar objeção material presente na fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de spans diretamente ligados a campos da pergunta.
8–14B: Compressor que preserva relações e exceções em poucos documentos.
15–30B: Sintetizador de argumentos com pacote de auditoria separado.
Requisitos de treino/runtime: Consulta estável, alinhamento com origem e medição do par compressor-leitor; treinamento pode ser necessário para compressão abstrativa.
Não aplicar quando: Pergunta muda continuamente ou a seleção esconde contradições indispensáveis.

## T037:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Redução de entrada é relacionada, sem igualdade ao RECOMP.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q017, V4A-Q024.

## T037:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T037 → T200 [feeds]
Como combinar: Entregar ao verificador contexto ampliado e independente.
Interface: Resposta candidata, spans e vizinhança de fonte.
Condição: Verificador não ficar limitado ao recorte favorável.
Aceite proposto: Incluir exceção fora do span selecionado e exigir detecção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S003, A-S018, V4A-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T037 → T015 [requires]
Como combinar: Manter acesso ao trecho integral.
Interface: Documento, revisão, offsets e tipo de transformação.
Condição: Referência permitir conferir paráfrases.
Aceite proposto: Abrir origem quando qualificador não estiver preservado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S003, A-S018, V4A-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar compressão de pergunta diferente.
- Distinguir vazio por irrelevância de falha do compressor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar precisão de qualificadores; leitor de fronteira pode compensar lacunas que 3–7B não consegue detectar.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T018, T036

## Fontes primárias associadas

### A-S018 — LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression

[https://arxiv.org/abs/2310.06839](https://arxiv.org/abs/2310.06839)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão voltada à informação relevante em contextos longos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S003 — RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation

[https://arxiv.org/abs/2310.04408](https://arxiv.org/abs/2310.04408)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressores extrativo e abstrativo orientados à tarefa; possibilidade de retornar contexto vazio quando não agrega informação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T010 — Fixed-Size Chunking

**Nome canônico:** Fixed-Size Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T010  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação de tamanho fixo

## T010:C01 — conceito

Divide documentos em segmentos de tamanho alvo medido em caracteres, palavras ou tokens, geralmente com sobreposição opcional. O tamanho só faz sentido acompanhado da unidade e do tokenizer. É uma linha de base simples e reproduzível para construir índices.

Como funciona:
- Definir unidade, tamanho máximo e quantidade de sobreposição.
- Percorrer o documento preservando offsets e identificador da origem.
- Indexar cada trecho com metadados suficientes para localizar o original.

## T010:C02 — aplicacao

Quando usar:
- Primeiro protótipo de recuperação e comparação de estratégias.
- Documentos relativamente uniformes sem estrutura confiável.

Quando não usar:
- É insuficiente quando tabelas, código ou cláusulas devem permanecer como unidades completas.

Implementação proposta:
- Proposta: aplicar tokenizer do embedding e respeitar seu limite real.
- Guardar início e fim do trecho e versão do segmentador.
- Avaliar vários tamanhos no mesmo conjunto de perguntas, mantendo filtros e retriever constantes.

Aplicação LAI proposta:
Proposta LAI: usar como baseline mensurável para manuais; preferir parsers estruturais em contratos de eventos, schemas e código.

## T010:C03 — riscos_validacao

Armadilhas:
- Sobreposição excessiva aumenta duplicação no contexto.
- Quebrar uma condição da sua consequência prejudica interpretação.

Métricas sugeridas:
- Distribuição real dos tamanhos e tokens descartados pelo embedding.
- Recall de respostas cruzando fronteiras de trechos.

Testes propostos:
- Colocar pergunta e resposta em lados opostos de uma fronteira.
- Reconstituir cobertura de offsets e detectar lacunas na ingestão.

## T010:C04 — perguntas_proveniencia

Pergunta: Quinhentos caracteres equivalem a quinhentos tokens?
Resposta: Não. A correspondência varia com idioma, símbolos e tokenizer.

Pergunta: Mais overlap resolve qualquer quebra?
Resposta: Não. Pode ajudar em fronteiras próximas, mas não substitui preservação da estrutura do documento.

Pergunta: Sobreposição deve ser removida antes do embedding?
Resposta: Se remover o conteúdo sobreposto, muda o método. A deduplicação costuma ser considerada na montagem dos candidatos, preservando o contexto usado na indexação.

Pergunta: Tokens e caracteres produzem o mesmo tamanho efetivo?
Resposta: Não. Idioma, código e símbolos mudam a relação; o contrato deve usar a unidade realmente relevante para o consumidor.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T010:C05 — mecanismo_avancado

Tamanho e sobreposição determinam quantidade de unidades e redundância. Para um documento longo com N tokens, blocos de c tokens e sobreposição o<c produzem aproximadamente N/(c-o) blocos, desconsiderando bordas. O orçamento de recuperação deve considerar duplicação de evidências entre vizinhos; contar os mesmos tokens duas vezes pode expulsar outra fonte relevante do contexto final.

Condição de contorno:
O modelo deixa de ser uma aproximação útil para documentos curtos, segmentação por caracteres ou processamento que altera a tokenização entre ingestão e consulta.

Contrato proposto:
- Entradas: Texto normalizado, tokenizer identificado, tamanho e sobreposição declarados.
- Saídas: Chunks com offsets, ordem e revisão do documento de origem.
- Estado: Versão do segmentador e mapeamento entre bytes e unidades indexadas.
- Invariante: Todo trecho recuperado pode ser relacionado a uma região identificável do original.

Compromissos de projeto:
- Blocos maiores preservam entorno, mas podem diluir sinais específicos na representação vetorial.
- Sobreposição protege fronteiras, porém aumenta índice, ingestão e repetição na resposta.

## T010:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: posicionar uma condição e sua exceção em lados opostos da fronteira. Comparar recuperação com e sem sobreposição e verificar se a montagem reconhece que o primeiro trecho está incompleto.

Plano de avaliação proposto:
Avaliação proposta: usar tamanho fixo como baseline e variar tamanho e sobreposição mantendo corpus, embeddings e orçamento de resposta. Medir recall de evidências, redundância, custo de índice e qualidade da resposta, sem escolher pelo número bruto de chunks.

Comparações:
- T011 (alternative): Fronteiras semânticas acrescentam cálculo; precisam demonstrar ganho sobre esta linha de base.
- T032 (complements): Trechos pequenos podem localizar um pai maior que fornece contexto após a recuperação.

Afirmação rastreável:
Um estudo comparativo não encontrou ganhos consistentes que justificassem sempre o custo adicional da segmentação semântica.
Suporte: direct; fontes: V3A-S013
Limite: Esse resultado é restrito às tarefas e configurações avaliadas; não demonstra superioridade universal do tamanho fixo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T010:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou duplicação por overlap. Aqui chunks fixos são dimensionados pela tarefa e por restrições de leitura do modelo.

Projeto e decomposição
Use varredura de tamanhos na validação e escolha pelo custo por resposta correta. Chunks menores aumentam candidatos; maiores diluem sinais e ocupam leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

Controle adaptativo
Trate overlap como orçamento de relações atravessando fronteiras. Registre onde uma resposta exige dois chunks, para ajustar sobreposição com evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

Validação contrafactual
Compare tamanhos com mesmo orçamento final de tokens, evitando favorecer configuração que simplesmente fornece mais conteúdo ao leitor. Unidade de avaliação: documento com fronteiras. Crie documentos com resposta perto de cada posição possível da fronteira e com condições separadas por diferentes distâncias. A curva de cobertura por distância ajuda a escolher overlap com base em dependências reais. Controle o orçamento total recuperado: duplicar contexto através de sobreposição não deve ser confundido com melhora intrínseca da segmentação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

USO AVANÇADO — Logs padronizados
Cenário: Registros longos têm formato estável.
Estratégia: Particionar por teto de tokens respeitando registros completos; recuperar vizinhos apenas quando uma operação cruza a borda.
Papel do modelo pequeno: 3–7B identifica eventos tipados.
Aceite proposto: Nenhum registro obrigatório pode aparecer mutilado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

USO AVANÇADO — Documentação homogênea
Cenário: Manuais repetem estrutura previsível.
Estratégia: Criar grade de tamanhos, medir cobertura por pergunta e escolher configuração por família documental.
Papel do modelo pequeno: 8–14B responde com contexto de poucos chunks.
Aceite proposto: Aceitar tamanho que preserve qualidade dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor com pequeno conjunto de chunks e campos previamente identificados.
8–14B: Comparador de chunks adjacentes para requisitos que cruzam fronteiras.
15–30B: Síntese com vários chunks quando benefício superar custo de leitura.
Requisitos de treino/runtime: Tokenizer correto, offsets e avaliação reservada por documento; segmentação continua determinística.
Não aplicar quando: Tabelas ou relações essenciais são rompidas repetidamente pelo teto fixo.

## T010:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Tamanho fixo configurável.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T010:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T010 → T032 [complements]
Como combinar: Expandir vizinhança quando o trecho é insuficiente.
Interface: chunk_id, documento, offsets e parent_id.
Condição: Pai pertencer à mesma revisão.
Aceite proposto: Verificar que expansão recupera condição sem duplicar evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T010 → T042 [requires]
Como combinar: Dimensionar recuperação pela janela do consumidor.
Interface: Tokens por chunk e reserva de resposta.
Condição: Contar serialização efetiva.
Aceite proposto: Comparar configurações sob orçamento idêntico.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter offsets antes e depois da normalização.
- Não duplicar confiança por sobreposição textual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar extração de fatos próximos às bordas; grande janela não substitui análise das fronteiras.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T011, T012, T033

## Fontes primárias associadas

### A-S004 — Splitting recursively

[https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores ordenados, limite de tamanho e sobreposição na divisão recursiva de texto.

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

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T033 — Structure-Aware Chunking

**Nome canônico:** Structure-Aware Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T033  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação consciente da estrutura

## T033:C01 — conceito

Segmenta respeitando a estrutura do documento: títulos, seções, tabelas, listas, funções ou schemas. A unidade recuperável segue fronteiras com significado formal, e não apenas comprimento. Ainda precisa de limites de tamanho e de uma estratégia para unidades maiores que a janela.

Como funciona:
- Interpretar o formato e extrair sua estrutura.
- Criar unidades com caminho de cabeçalhos ou símbolos.
- Subdividir unidades grandes sem perder a relação com o bloco original.

## T033:C02 — aplicacao

Quando usar:
- Documentação Markdown, HTML, código e contratos estruturados.
- Perguntas que dependem de escopo de uma seção ou função.

Quando não usar:
- Não confiar no parser quando a extração de PDF perdeu colunas, tabelas ou ordem de leitura.

Implementação proposta:
- Proposta: escolher parser por MIME e guardar sua versão.
- Preservar nomes de seção, página, função e relações pai-filho.
- Em tabelas, repetir cabeçalho necessário sem inventar células ou separar chave do valor.

Aplicação LAI proposta:
Proposta LAI: usar para README, contratos de eventos e módulos de software, preservando o caminho até a evidência original.

## T033:C03 — riscos_validacao

Armadilhas:
- Cabeçalho pode ser confundido com texto dentro de bloco de código.
- Estruturas muito grandes exigem subdivisão contextual adicional.

Métricas sugeridas:
- Fração de unidades com metadados estruturais válidos.
- Recall de tabelas, exceções e símbolos de código.

Testes propostos:
- Usar Markdown com cerquilhas dentro de código e verificar que não viram títulos.
- Testar tabela multipágina e conferir associação entre coluna e valor.

## T033:C04 — perguntas_proveniencia

Pergunta: Structure-aware é sempre semântico?
Resposta: Ele reconhece estrutura formal; significado profundo ainda depende da interpretação e da pergunta.

Pergunta: Preciso guardar o texto integral?
Resposta: Sim, para reconstrução, verificação e nova segmentação se o parser estiver errado.

Pergunta: A versão do splitter basta para reproduzir os chunks?
Resposta: Não. Também registre o particionador e seus parâmetros. Alterar reconhecimento de títulos ou tabelas modifica a estrutura antes da divisão.

Pergunta: Uma tabela deve sempre permanecer inteira?
Resposta: Somente se couber e for utilizável. A subdivisão precisa conservar identificação das colunas, unidades e vínculo com a tabela original.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T033:C05 — mecanismo_avancado

A estrutura usada para agrupar trechos é resultado de uma etapa anterior de interpretação. Um erro de classificação transforma uma legenda em título e pode mudar os limites de todas as unidades seguintes. O chunker precisa conservar elementos originais e separar limites rígidos, como tamanho máximo, de preferências, como não juntar seções. Unidades estruturais gigantes ainda exigem subdivisão explícita.

Condição de contorno:
A vantagem diminui quando a estrutura é inferida de extração desordenada ou quando a pergunta depende de relações que atravessam vários elementos.

Contrato proposto:
- Entradas: Elementos tipados com ordem, documento, seção e coordenadas ou offsets recuperáveis.
- Saídas: Chunks com lista de elementos de origem, divisões internas e metadados herdados.
- Estado: Versões do particionador, regras de agrupamento e tratamento de elementos excedentes.
- Invariante: A reconstrução da origem não depende de interpretar novamente o texto sintetizado do chunk.

Compromissos de projeto:
- Agrupar elementos inteiros conserva relações locais, mas pode desperdiçar orçamento ao respeitar fronteiras.
- Mesclar seções pequenas reduz fragmentação; também pode juntar assuntos cuja separação tinha significado.

## T033:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: classificar deliberadamente uma legenda como título e inserir uma tabela maior que o limite. O processamento deve expor a segmentação derivada e conservar associação entre cabeçalho, linhas e fonte.

Plano de avaliação proposto:
Avaliação proposta: comparar segmentação por elementos e recursiva usando a mesma extração inicial. Medir fidelidade estrutural, cobertura de relações tabela-texto, proporção de subdivisões e recuperação por orçamento; separar falhas do parser das do chunker.

Comparações:
- T012 (alternative): A divisão recursiva usa separadores textuais; elementos estruturados carregam tipos e relações produzidos antes do agrupamento.
- T032 (complements): A expansão parental pode recuperar contexto que uma unidade estrutural pequena não contém.

Afirmação rastreável:
O Unstructured agrupa elementos previamente particionados e divide elementos que excedem o tamanho máximo.
Suporte: direct; fontes: V3A-S027
Limite: O comportamento depende da estratégia e configuração; preservar toda seção não é uma garantia universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T033:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou erros de parsing. Aqui estruturas viram unidades de evidência com contratos distintos de leitura e comparação.

Projeto e decomposição
Trate tabela, procedimento, figura e código como tipos diferentes. Uma tabela precisa de cabeçalhos e unidades; procedimento precisa de ordem; código precisa de contexto sintático.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

Controle adaptativo
Produza duas representações: texto para busca e objeto estruturado para leitura. O índice pode omitir detalhes, mas a geração deve acessar a representação que conserva relações necessárias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

Validação contrafactual
Compare texto linearizado e blocos tipados em perguntas que dependem de linhas, colunas ou ordem. Meça erros de associação, não só recuperação do documento correto. Unidade de avaliação: bloco estrutural.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

USO AVANÇADO — Tabelas comparativas
Cenário: Valores similares pertencem a modelos diferentes.
Estratégia: Recuperar tabela pelo tema, selecionar linhas em código e fornecer cabeçalho completo ao leitor. Preservar notas de rodapé aplicáveis.
Papel do modelo pequeno: 3–7B verbaliza células selecionadas.
Aceite proposto: Não trocar coluna, unidade ou condição de nota.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

USO AVANÇADO — Procedimento operacional
Cenário: Passos incluem ramos condicionais.
Estratégia: Preservar ordem e condições em estrutura; fornecer somente ramo aplicável, mantendo ponto de retorno.
Papel do modelo pequeno: 8–14B explica execução.
Aceite proposto: Toda ação deve respeitar pré-condições e ordem documentadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de células e campos com relações explícitas.
8–14B: Interpretador de listas condicionais e blocos de código pequenos.
15–30B: Comparador de múltiplas estruturas com referências cruzadas.
Requisitos de treino/runtime: Parser com testes por formato e ligação entre texto indexado e objeto de leitura; OCR exige avaliação própria.
Não aplicar quando: Extração não preserva layout decisivo e não há imagem ou original disponível para conferir.

## T033:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Respeita limites lógicos em conteúdo analisado, sem todos os parsers desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Transcrições permitem endereçar trechos, sem comprovar splitter estrutural próprio.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q022.

## T033:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T033 → T032 [feeds]
Como combinar: Expandir filho em estrutura completa necessária.
Interface: Tipo, bloco_id, cabeçalhos e revisão.
Condição: Pai estrutural corresponder à mesma origem.
Aceite proposto: Recuperar célula sem perder cabeçalho que muda significado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S027, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T033 → T195 [complements]
Como combinar: Verificar propriedades calculáveis da estrutura.
Interface: Tabela tipada ou código e regras de validação.
Condição: Execução autorizada e ambiente adequado.
Aceite proposto: Detectar soma ou sintaxe inválida antes da resposta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S027, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar ordem visual como sequência temporal sem indicação.
- Conservar vínculo entre nota e células afetadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar leitura relacional de tabelas e procedimentos; domínio estrutural pode permitir bons resultados com modelos menores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T012, T032, T035

## Fontes primárias associadas

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S027 — Chunking

[https://docs.unstructured.io/open-source/core-functionality/chunking](https://docs.unstructured.io/open-source/core-functionality/chunking)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento em elementos estruturais antes de agrupar chunks; tratamento de tabelas, tamanho e fronteiras por título.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

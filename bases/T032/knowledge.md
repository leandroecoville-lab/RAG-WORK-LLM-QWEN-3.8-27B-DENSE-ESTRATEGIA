# T032 — Parent-Child Retrieval / Parent-Child Chunking

**Nome canônico:** Parent-Child Chunking e Parent-Child Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T032  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Parent-Child Retrieval; recuperação pai-filho; Parent-Child Chunking; segmentação pai-filho

## T032:C01 — conceito

Parent-Child Chunking cria unidades grandes de contexto e trechos filhos menores para indexação. Parent-Child Retrieval usa os filhos encontrados para recuperar os pais correspondentes. São etapas complementares de preparação e consulta, não nomes de um método de treinamento. O objetivo é localizar passagens específicas sem perder definições, exceções e relações presentes no entorno.

Como funciona:
- Dividir o documento em pais coerentes, como seções; dividir cada pai em filhos com vínculo estável.
- Indexar representações dos filhos e guardar o texto integral dos pais em armazenamento endereçável.
- Na consulta, localizar filhos, resolver parent_id, deduplicar pais e selecionar expansões compatíveis com o orçamento.

## T032:C02 — aplicacao

Quando usar:
- Manuais, contratos e documentos técnicos nos quais uma frase responde à busca, mas sua interpretação exige a seção correspondente.

Quando não usar:
- Quando documentos já são curtos ou os pais incluem grandes blocos irrelevantes que tornam a expansão mais prejudicial que útil.

Implementação proposta:
- Proposta: registrar document_id, version_id, parent_id, child_id, offsets e namespace; um pai pode ser uma seção, não obrigatoriamente o arquivo inteiro.
- Dimensionar filhos pela precisão da busca e pais pela suficiência contextual, avaliando perguntas reais; não presumir um tamanho universal.
- Manter o filho que originou o resultado para destacar a evidência e aplicar as mesmas permissões ao filho e ao pai.
- Reindexar vínculos quando mudar a segmentação ou a versão, removendo referências órfãs antes da publicação do índice.

Aplicação LAI proposta:
Proposta LAI: usar módulos ou seções como pais e preservar os trechos filhos que justificaram sua inclusão no contexto de programação.

## T032:C03 — riscos_validacao

Armadilhas:
- Misturar filho antigo com pai atualizado pode produzir uma citação inexistente.
- Muitos filhos do mesmo pai podem ocupar o ranking e reduzir diversidade de documentos.

Métricas sugeridas:
- Recall dos filhos, diversidade de pais, tokens de expansão e proporção de respostas que preservam exceções relevantes.

Testes propostos:
- Teste proposto: buscar uma cláusula cujo pai contém a exceção e conferir que ambas chegam à geração.
- Atualizar e excluir uma seção; verificar integridade dos vínculos, versão e permissões na próxima consulta.

## T032:C04 — perguntas_proveniencia

Pergunta: Parent-Child Chunking já executa recuperação?
Resposta: Não. Ele prepara a hierarquia; a recuperação precisa consultar os filhos e resolver os pais armazenados.

Pergunta: O documento pai precisa ser o arquivo completo?
Resposta: Não. Pode ser um bloco maior ou seção. A implementação oficial permite um parent_splitter separado do child_splitter.

Pergunta: Pai é sempre o documento completo?
Resposta: Não. Pode ser um bloco maior gerado previamente. O tamanho adequado depende do contexto necessário e do orçamento de leitura.

Pergunta: Top-k de filhos é igual a top-k de pais?
Resposta: Não. Vários filhos podem apontar ao mesmo pai. Controle diversidade e cobertura no nível realmente entregue ao gerador.

Escopo das fontes:
Código oficial ParentDocumentRetriever inspecionado. Versionamento, critérios de expansão, testes e aplicação LAI são propostas editoriais, sem resultado de benchmark alegado.

## T032:C05 — mecanismo_avancado

O vínculo filho-pai precisa incluir revisão, além de identidade lógica. Se o índice vetorial contém um filho antigo e o docstore devolve o pai novo, o trecho usado para localizar a resposta pode não existir no conteúdo entregue. Também é necessário deduplicar pais: muitos filhos semelhantes podem consumir todo o conjunto candidato e devolver apenas um documento.

Condição de contorno:
A expansão perde valor quando o pai é grande demais para o orçamento, inclui conteúdo inelegível ou não corresponde à versão do filho recuperado.

Contrato proposto:
- Entradas: Filhos indexados, mapa de parent_id e pais com versões recuperáveis.
- Saídas: Pais elegíveis ou regiões selecionadas, com evidência dos filhos que motivaram a expansão.
- Estado: Revisão de ingestão, presença dos pais e política de publicação do índice.
- Invariante: Nenhum filho é apresentado como evidência da versão de um pai à qual ele não pertence.

Compromissos de projeto:
- Filhos pequenos localizam detalhes, mas exigem lookup adicional e manutenção de relações.
- Pais maiores preservam contexto e podem introduzir ruído ou duplicação na montagem final.

## T032:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper ingestão entre a escrita de filhos e pais, e depois alterar um pai sem reindexar. A consulta deve detectar ausência ou incompatibilidade, sem substituir silenciosamente o conteúdo.

Plano de avaliação proposto:
Avaliação proposta: comparar filhos isolados e expansão parental com orçamento igual. Medir pais únicos recuperados, integridade dos vínculos, recall de condições e custo de lookup; avaliar também muitas correspondências concentradas num único pai.

Comparações:
- T026 (complements): A hierarquia pode orientar busca; parent-child separa unidade de indexação da unidade entregue.
- T010 (complements): Um divisor simples pode gerar filhos, desde que os vínculos e versões sejam preservados.

Afirmação rastreável:
O ParentDocumentRetriever armazena o identificador do pai nos metadados dos filhos e mantém os pais num docstore.
Suporte: direct; fontes: V2C-S003
Limite: O código consultado faz operações em stores distintos; atomicidade entre eles não deve ser presumida.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T032:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou consistência filho-pai. Aqui a expansão é seletiva por regiões do pai, com cota compartilhada entre evidências concorrentes.

Projeto e decomposição
Expanda somente regiões que restauram dependências do filho, como cabeçalho, definição e ressalva. Carregar o pai inteiro pode introduzir ruído e consumir a janela de outros documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

Controle adaptativo
Una filhos do mesmo pai antes de expandir e preserve todos os motivos de seleção. A deduplicação do pai não pode apagar evidência de que vários trechos respondem a partes distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

Validação contrafactual
Compare expansão integral, janela local e blocos estruturais. Meça cobertura de condições por token, diversidade de pais e versões indevidas; manter constante a recuperação inicial. Unidade de avaliação: grupo de filhos recuperados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

USO AVANÇADO — Contratos técnicos
Cenário: Cláusula recuperada depende de definição anterior.
Estratégia: Abrir definição e exceções relacionadas, preservando seções e revisão; gerar resposta condicionada ao escopo do contrato.
Papel do modelo pequeno: 8–14B integra fragmentos.
Aceite proposto: A resposta deve incluir condição que muda interpretação da cláusula.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

USO AVANÇADO — Código distribuído
Cenário: Função encontrada depende de tipo ou chamada.
Estratégia: Expandir assinatura, tipo referenciado e ponto de uso, não todo o arquivo. Se dependência não resolver, declarar lacuna.
Papel do modelo pequeno: 3–7B localiza; 15–30B integra fluxo.
Aceite proposto: Não atribuir comportamento sem verificar interfaces relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Localizador de trechos e dependências explícitas de um filho.
8–14B: Leitor de pequenos conjuntos de blocos do mesmo pai.
15–30B: Integrador entre pais quando a resposta exige contexto cruzado.
Requisitos de treino/runtime: Mapeamento filho-pai com offsets e revisão, parser estrutural e orçamento por evidência.
Não aplicar quando: Os vínculos não são confiáveis ou todo pai é necessário para qualquer interpretação.

## T032:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Recuperação de filhos seguida da substituição por pais.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T032:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T032 → T033 [requires]
Como combinar: Identificar blocos que completam contexto.
Interface: Cabeçalho, definição, ressalva e intervalos.
Condição: Parser conservar identidade dos blocos.
Aceite proposto: Testar cláusula com exceção distante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2C-S003, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T032 → T042 [complements]
Como combinar: Distribuir expansão entre pais distintos.
Interface: Tokens previstos, requisitos e número de pais únicos.
Condição: Pai dominante não consumir toda a cota.
Aceite proposto: Comparar respostas com evidência distribuída em vários pais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2C-S003, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Reaplicar filtros no conteúdo expandido.
- Não confundir número de filhos com número de fontes independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar completude interpretativa por token; contexto extra só ajuda se o leitor distinguir escopo e exceções.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T026, T035, P007

## Fontes primárias associadas

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

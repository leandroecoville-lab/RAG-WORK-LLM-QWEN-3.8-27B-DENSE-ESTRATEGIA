# T030 — RAPTOR

**Nome canônico:** RAPTOR  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T030  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Recursive Abstractive Processing for Tree-Organized Retrieval

## T030:C01 — conceito

RAPTOR significa Recursive Abstractive Processing for Tree-Organized Retrieval. O método constrói representações em vários níveis por embeddings, agrupamento e resumos recursivos, e recupera material dessa estrutura. Foi proposto para ampliar a visão de documentos além de pequenos trechos contíguos.

Como funciona:
- Criar trechos e embeddings dos documentos.
- Agrupar e sintetizar repetidamente formando níveis de abstração.
- Buscar informação relevante entre os nós da árvore.

## T030:C02 — aplicacao

Quando usar:
- Perguntas temáticas sobre documentos extensos.
- Consultas que combinam detalhe e visão geral.

Quando não usar:
- Não assumir vantagem para dados transacionais de alta frequência sem avaliar custo de reconstrução.

Implementação proposta:
- Proposta: preservar folhas originais e ligações de cada resumo aos filhos.
- Versionar agrupamento, embedder e gerador de resumos.
- Comparar com RAG plano sob o mesmo modelo de resposta e conjunto de perguntas.

Aplicação LAI proposta:
Proposta LAI: avaliar sobre bases teóricas extensas e manuais; não tratar o nome RAPTOR como garantia de ganho na configuração local.

## T030:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir exceções ou introduzir relações indevidas.
- Atualizações no corpus podem exigir revisar agrupamentos e ancestrais.

Métricas sugeridas:
- Correção de perguntas globais e pontuais.
- Custo de construção, atualização e tokens recuperados.

Testes propostos:
- Exigir evidência original para afirmações vindas de nós de resumo.
- Medir comportamento após alteração de um documento, sem aceitar resumo antigo como atual.

## T030:C04 — perguntas_proveniencia

Pergunta: RAPTOR muda os pesos da LLM?
Resposta: A estrutura de recuperação não exige, por si só, retreinar o gerador.

Pergunta: Basta uma pasta com resumos para ter RAPTOR?
Resposta: Não. É preciso implementar e registrar o processo específico de agrupamento, níveis e recuperação ou declarar que é apenas inspirado nele.

Pergunta: BIC escolhe o melhor número de grupos para responder perguntas?
Resposta: Não diretamente. Ele avalia um critério estatístico do modelo de mistura, não a utilidade downstream de cada agrupamento.

Pergunta: Posso trocar o embedding sem reconstruir a estrutura?
Resposta: Isso pode tornar representações e grupos incompatíveis. A migração deve incluir nova indexação e validação, preservando a versão anterior para comparação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T030:C05 — mecanismo_avancado

O código consultado reduz dimensionalidade com UMAP e usa misturas gaussianas, selecionando número de componentes por BIC. A associação por probabilidades acima de um limiar permite que um trecho pertença a mais de um grupo. Consequentemente, a estrutura chamada árvore não deve ser interpretada como partição necessariamente disjunta; duplicação de origens precisa ser considerada na recuperação e síntese.

Condição de contorno:
Agrupamento de poucos pontos, embeddings inadequados ou textos altamente heterogêneos podem produzir grupos frágeis, independentemente da qualidade do sumarizador.

Contrato proposto:
- Entradas: Chunks, embeddings compatíveis, configuração de agrupamento e sumarização.
- Saídas: Representações em níveis e referências aos trechos que sustentam cada nó.
- Estado: Versões dos modelos, seeds, configurações e relações de pertencimento.
- Invariante: Múltiplos caminhos até a mesma origem não contam como confirmações independentes.

Compromissos de projeto:
- Pertencimento múltiplo preserva temas transversais, mas aumenta redundância e custo de resumos.
- Redução dimensional torna agrupamento viável e pode alterar vizinhanças relevantes para consultas específicas.

## T030:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um trecho que conecte dois temas e rastrear sua presença em resumos diferentes. A resposta deve evitar duplicar contagens e continuar permitindo acesso à mesma origem.

Plano de avaliação proposto:
Avaliação proposta: comparar folhas, resumos em níveis e conjunto combinado com orçamento idêntico. Variar agrupamento e resumidor; medir estabilidade, recuperação de detalhes e temas, custo de ingestão e redundância de evidências.

Comparações:
- T023 (specializes): RAPTOR implementa uma hierarquia recursiva com escolha específica de agrupamento e recuperação.
- T029 (alternative): GraphRAG organiza entidades e comunidades; RAPTOR agrupa representações de texto para produzir resumos.

Afirmação rastreável:
O código oficial usa probabilidades de GaussianMixture acima de limiar para atribuir grupos.
Suporte: direct; fontes: V3A-S029
Limite: Foi realizada leitura de código, sem execução; detalhes podem mudar em outras revisões do repositório.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T030:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou clustering do RAPTOR. Aqui o foco é atualização de árvores e controle do custo de sobreposição entre clusters.

Projeto e decomposição
A participação de uma folha em vários clusters melhora rotas possíveis, mas também multiplica sínteses e dependências de atualização. Registre grau de participação por documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

Controle adaptativo
Após alteração de folha, escolha entre atualização local e reconstrução segundo mudança de vizinhança. Reusar resumos quando a composição do cluster mudou pode conservar uma interpretação inválida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

Validação contrafactual
Compare índice original, atualização local e reconstrução completa em corpus editado. Meça cobertura, custo de regeneração e duplicação de evidência no contexto final, mantendo consultas reservadas. Unidade de avaliação: coleção resumida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

USO AVANÇADO — Base técnica em evolução
Cenário: Poucos documentos mudam por semana.
Estratégia: Marcar resumos dependentes, recalcular clusters afetados e publicar revisão completa somente após validar ligações às folhas.
Papel do modelo pequeno: 3–7B extrai mudanças; 8–14B resume clusters.
Aceite proposto: Consulta não pode misturar resumo antigo e folha nova sem indicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

USO AVANÇADO — Perguntas de síntese
Cenário: Resposta exige vários níveis de abstração.
Estratégia: Recuperar resumos para orientação e folhas para afirmações precisas; deduplicar folhas alcançadas por caminhos diferentes.
Papel do modelo pequeno: 15–30B integra níveis.
Aceite proposto: Cada detalhe factual deve apontar à folha original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de atributos e verificador de cobertura das folhas.
8–14B: Resumidor de grupos pequenos, com limites de tamanho e conteúdo.
15–30B: Integrador de múltiplos níveis quando síntese realmente exigir abstração.
Requisitos de treino/runtime: Implementação RAPTOR compatível, vínculos muitos-para-muitos e versionamento de clusters; não substituir por árvore genérica.
Não aplicar quando: Atualizações frequentes fazem reconstrução dominar custo ou resumos não melhoram tarefas do acervo.

## T030:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q021.

## T030:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T030 → T072 [requires]
Como combinar: Publicar uma revisão coerente de folhas e resumos.
Interface: Manifesto de clusters, versões e dependências.
Condição: Consulta pinada a revisão consistente.
Aceite proposto: Testar leitura durante troca de índice.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S014, V3A-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T030 → T032 [alternative]
Como combinar: Preferir pais documentais quando hierarquia natural basta.
Interface: Documento, filho e pai estrutural.
Condição: Estrutura documental conservar contexto necessário.
Aceite proposto: Comparar custo e qualidade com agrupamento aprendido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S014, V3A-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar mesma folha várias vezes como evidência adicional.
- Não chamar configuração diferente de clustering de reprodução exata.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar questões de abstração e detalhe separadamente; ganhos relatados do RAPTOR não garantem ganhos com leitores pequenos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T023, T026

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S029 — RAPTOR cluster_utils.py

[https://github.com/parthsarthi03/raptor/blob/master/raptor/cluster_utils.py](https://github.com/parthsarthi03/raptor/blob/master/raptor/cluster_utils.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: UMAP, GaussianMixture, seleção por BIC e associação por probabilidades acima de limiar; leitura do código, sem execução.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

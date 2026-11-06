# T026 — Hierarchical Retrieval

**Nome canônico:** Hierarchical Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T026  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recuperação hierárquica

## T026:C01 — conceito

Recupera informação usando níveis de organização, como coleção, documento, seção e trecho. A busca pode descer do resumo ao detalhe ou combinar candidatos de vários níveis. O objetivo é melhorar descoberta sem perder precisão e contexto local.

Como funciona:
- Construir ligações entre unidades amplas e unidades específicas.
- Pesquisar no nível adequado à pergunta.
- Expandir candidatos relevantes e entregar evidência na granularidade necessária.

## T026:C02 — aplicacao

Quando usar:
- Bases com muitos documentos e estrutura temática consistente.
- Perguntas que alternam visão geral e detalhe de implementação.

Quando não usar:
- Não impor uma hierarquia rígida quando temas relevantes atravessam vários ramos sem ligações.

Implementação proposta:
- Proposta: armazenar nível, parent_id e caminho de origem.
- Aplicar filtros de acesso em todos os níveis, inclusive resumos.
- Comparar rota de cima para baixo com busca plana para detectar poda prematura de ramos relevantes.

Aplicação LAI proposta:
Proposta LAI: índice por domínio, técnica e seção, com busca direta alternativa para não depender de navegar sempre pela taxonomia.

## T026:C03 — riscos_validacao

Armadilhas:
- Um resumo superior ruim impede encontrar uma folha correta.
- A expansão de muitos pais pode exceder o orçamento.

Métricas sugeridas:
- Recall de documentos e trechos em cada estágio.
- Número de nós lidos até encontrar evidência suficiente.

Testes propostos:
- Criar resposta situada em ramo cuja descrição é pouco semelhante à pergunta.
- Consultar tema transversal e verificar recuperação de mais de uma categoria.

## T026:C04 — perguntas_proveniencia

Pergunta: Recuperação hierárquica exige resumos por LLM?
Resposta: Não. Cabeçalhos, pastas e metadados podem fornecer a hierarquia.

Pergunta: É igual a Parent-Child Retrieval?
Resposta: Parent-child é um caso particular; uma hierarquia pode ter muitos níveis e diferentes políticas de expansão.

Pergunta: Um nó relevante garante filhos relevantes?
Resposta: Não. A síntese pode representar apenas parte dos descendentes. É preciso selecionar e verificar quais folhas sustentam a pergunta.

Pergunta: Como contar cobertura sem inflá-la?
Resposta: Deduplicate referências à mesma evidência e registre a contribuição de cada nível. Um fato citado pelo resumo e pela folha não se torna duas confirmações independentes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T026:C05 — mecanismo_avancado

A navegação descendente pode tornar um erro inicial irreversível: ao excluir uma coleção no topo, seus melhores trechos deixam de competir. Uma alternativa é manter mais de um caminho e combinar candidatos de níveis diferentes, com deduplicação por evidência. Resumos superiores orientam descoberta, mas os detalhes recuperados ainda precisam sustentar a resposta final.

Condição de contorno:
Quando títulos e resumos não representam os fatos procurados, restringir busca a poucos ramos reduz recall mesmo com um excelente buscador local.

Contrato proposto:
- Entradas: Consulta, hierarquia versionada e orçamento de caminhos e candidatos.
- Saídas: Evidências selecionadas com nível, origem e caminho de recuperação.
- Estado: Mapeamento entre nós e folhas, pontuações e ramos descartados.
- Invariante: A resposta distingue material original de sínteses usadas para orientar a busca.

Compromissos de projeto:
- Busca em poucos ramos reduz custo, mas amplifica erros de roteamento.
- Combinar níveis aumenta cobertura e pode repetir a mesma evidência em resumo e folha.

## T026:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ocultar um fato relevante sob um título pouco relacionado à pergunta. Comparar navegação restrita e busca global de fallback; a política deve reconhecer a limitação do roteamento inicial.

Plano de avaliação proposto:
Avaliação proposta: comparar busca plana, descendente e combinação de níveis com igual orçamento final. Medir recall por estágio, diversidade de fontes, duplicação e latência; decidir conforme perguntas locais e globais do domínio.

Comparações:
- T032 (complements): Parent-child expande o entorno após localizar um filho; a hierarquia também pode orientar a localização inicial.
- T030 (complements): RAPTOR oferece uma estrutura concreta de recuperação em níveis de abstração.

Afirmação rastreável:
RAPTOR constrói representações recursivas e permite recuperar informação em diferentes níveis de abstração.
Suporte: direct; fontes: A-S014
Limite: A política de múltiplos caminhos e fallback proposta precisa ser avaliada separadamente da arquitetura publicada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T026:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu perda no roteamento hierárquico. Aqui busca em feixe e orçamento de exploração protegem ramos pouco prováveis.

Projeto e decomposição
Mantenha mais de um ramo candidato quando descritores se sobrepõem. O tamanho do feixe depende de diversidade e custo dos ramos, não de um top-k fixo em toda a árvore.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

Controle adaptativo
Reserve cota para um ramo alternativo quando o melhor ramo não fornecer evidência suficiente. Registre cobertura real dos ramos; navegar repetidamente pelo mesmo ancestral não é exploração nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

Validação contrafactual
Compare top-1, feixe fixo e expansão por insuficiência. Meça recall de folhas relevantes, custo de navegação e falhas em documentos inseridos recentemente, ainda pouco representados nos resumos. Unidade de avaliação: consulta hierárquica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

USO AVANÇADO — Manuais por produto
Cenário: Uma consulta cruza versões e componentes.
Estratégia: Roteie por produto e versão obrigatórios, depois explore componentes candidatos. Rejeite ramo semanticamente próximo com versão incompatível.
Papel do modelo pequeno: 3–7B roteia; 8–14B verifica folhas.
Aceite proposto: Toda evidência final deve respeitar produto e revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

USO AVANÇADO — Revisão interdisciplinar
Cenário: Termos iguais aparecem em áreas diferentes.
Estratégia: Abrir ramos de sentidos alternativos, reunir evidências discriminantes e somente depois fechar interpretação.
Papel do modelo pequeno: 15–30B integra resultados por sentido.
Aceite proposto: Não excluir um sentido correto apenas pelo resumo dominante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Navegador com poucas opções e filtros estruturados.
8–14B: Avaliador de suficiência e desambiguação entre ramos próximos.
15–30B: Planejador de exploração limitada em hierarquias múltiplas.
Requisitos de treino/runtime: Descritores de nós, custo por expansão e vínculos às folhas; testar também ramos novos e raros.
Não aplicar quando: A taxonomia não representa a organização das perguntas e quase toda consulta cruza todos os ramos.

## T026:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q009, V4A-Q021.

## T026:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T026 → T008 [requires]
Como combinar: Construir descritores adequados para cada nível.
Interface: node_id, escopo, filhos e resumo de descoberta.
Condição: Resumo não eliminar termos distintivos.
Aceite proposto: Testar consulta respondível apenas em folha minoritária.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T026 → T027 [complements]
Como combinar: Usar busca lexical e vetorial nas folhas elegíveis.
Interface: Lista de ramos permitidos e filtros.
Condição: Ambos os canais respeitarem escopo.
Aceite proposto: Comparar recall antes e depois do filtro hierárquico.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar ramo não explorado de ramo sem resposta.
- Impedir ciclo em hierarquias que permitem múltiplos pais.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar recall por custo de navegação; uma árvore profunda não prova raciocínio melhor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T023, T030, T032

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V3A-S023 — GraphRAG Global Search

[https://microsoft.github.io/graphrag/query/global_search/](https://microsoft.github.io/graphrag/query/global_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Consulta global por relatórios de comunidades com map-reduce; efeito do nível de comunidade no custo e detalhe.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

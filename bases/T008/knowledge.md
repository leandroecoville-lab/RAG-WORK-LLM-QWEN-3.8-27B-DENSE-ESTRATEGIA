# T008 — Hierarchical Summarization

**Nome canônico:** Hierarchical Summarization  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** sumarização hierárquica

## T008:C01 — conceito

Cria resumos em níveis: partes são sintetizadas, grupos de resumos formam sínteses maiores e cada nível conserva vínculos aos seus descendentes. Permite navegar por visão geral e detalhe, mas níveis superiores acumulam perdas se não houver revisão e acesso aos originais.

Como funciona:
- Separar o conteúdo em unidades coerentes e identificáveis.
- Resumir unidades e depois grupos, respeitando orçamento por nível.
- Guardar relações pai-filho e evidências de afirmações importantes.

## T008:C02 — aplicacao

Quando usar:
- Coleções extensas com estrutura temática ou documental.
- Relatórios gerais que precisam permitir rastreamento até trechos específicos.

Quando não usar:
- Não usar o resumo raiz como substituto dos dados quando a resposta exige detalhe exato.

Implementação proposta:
- Proposta: construir árvore com versões de nós e hashes dos filhos.
- Recalcular apenas ancestrais afetados por uma atualização.
- Recuperar folhas para conferir números ou conflitos citados em um resumo superior.

Aplicação LAI proposta:
Proposta LAI: organizar conhecimento por software, módulo e contrato; usar sínteses para descoberta e documentos originais para comprovação.

## T008:C03 — riscos_validacao

Armadilhas:
- O mesmo fato pode ser contado duas vezes em ramos diferentes.
- Mudança em uma folha pode deixar ancestrais desatualizados.

Métricas sugeridas:
- Fidelidade entre nós pais e fontes descendentes.
- Cobertura de perguntas globais e pontuais por nível.

Testes propostos:
- Alterar uma folha e exigir invalidação dos resumos dependentes.
- Perguntar por uma exceção rara e verificar navegação ao texto original.

## T008:C04 — perguntas_proveniencia

Pergunta: É igual ao RAPTOR?
Resposta: RAPTOR é uma arquitetura específica que combina agrupamento, embeddings e resumos recursivos. A sumarização hierárquica é mais geral.

Pergunta: Todos os resumos precisam caber na chamada?
Resposta: Não. A hierarquia existe justamente para selecionar níveis e ramos conforme a pergunta.

Pergunta: Uma árvore de resumos garante rastreabilidade?
Resposta: Somente se a implementação preservar referências e versões. Uma árvore contendo apenas prosa pode perder a ligação verificável com as fontes.

Pergunta: Devo sempre recuperar a raiz?
Resposta: Não. A raiz pode ser genérica demais. Selecione o nível conforme a pergunta e expanda até evidência suficiente, respeitando o orçamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T008:C05 — mecanismo_avancado

A profundidade da hierarquia influencia tanto navegação quanto número de transformações sofridas por uma evidência. Atualizar uma folha exige invalidar os resumos que dependem dela; conservar um nó superior antigo junto de folhas novas cria versões incoerentes. Uma política de reconstrução deve registrar dependências e publicar uma árvore consistente, em vez de trocar nós isolados sem fronteira identificável.

Condição de contorno:
Quando perguntas exigem detalhes que os resumos descartaram e as folhas não são recuperáveis, mais níveis apenas reorganizam a perda.

Contrato proposto:
- Entradas: Unidades originais versionadas, agrupamento e orçamento por nível.
- Saídas: Nós resumidos com referências aos descendentes e à revisão da árvore.
- Estado: DAG de dependências, versões de sumarizadores e fila de nós inválidos.
- Invariante: Cada afirmação resumida é distinguida da evidência original e aponta para sua origem.

Compromissos de projeto:
- Mais níveis reduzem contexto por leitura, mas aumentam ingestão e manutenção.
- Resumos amplos ajudam perguntas globais, enquanto trechos locais preservam especificidade e exceções.

## T008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir uma folha depois de construir a hierarquia. Consultas não devem combinar a correção com um resumo ancestral que ainda afirme o valor antigo sem sinalizar desatualização.

Plano de avaliação proposto:
Avaliação proposta: comparar busca apenas nas folhas com busca em múltiplos níveis, mantendo o orçamento final. Medir recuperação de fatos, perguntas globais, custo de atualização e proporção de nós obsoletos após mudanças.

Comparações:
- T023 (complements): A árvore recursiva explicita uma organização possível da sumarização hierárquica.
- T030 (complements): RAPTOR combina hierarquia com embeddings, agrupamento e recuperação em seus níveis.

Afirmação rastreável:
O código oficial de RAPTOR permite construir, persistir e carregar uma árvore para recuperação.
Suporte: direct; fontes: V3A-S011
Limite: A publicação de estados consistentes e a invalidação incremental aqui descritas são propostas de engenharia.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T008:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou invalidação de ancestrais. A novidade é síntese com orçamento desigual e expansão direcionada por desacordo entre níveis.

Projeto e decomposição
Distribua orçamento por diversidade de evidências, não pelo número de folhas. Um ramo consensual pode receber menos espaço que outro com condições incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Controle adaptativo
Conserve resumo e contraexemplos separados em cada nó. Se a conclusão do pai excluir exceção presente no filho, abrir o ramo antes de responder.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Validação contrafactual
Compare árvore uniforme e alocação por divergência. Avalie preservação de exceções e custo de expansão, sem confundir profundidade com qualidade. Unidade de avaliação: árvore documental. Introduza uma exceção sustentada por uma única folha num ramo com muitos relatos concordantes. A síntese deve preservar a exceção quando ela afeta a pergunta, mesmo que a maioria dos documentos repita a regra geral. Compare seleção por quantidade de folhas e por diversidade de condições, registrando quais requisitos desapareceram em cada nível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Revisão de políticas
Cenário: Departamentos descrevem regras parcialmente diferentes.
Estratégia: Resumir por escopo, detectar incompatibilidades e produzir síntese condicionada ao departamento.
Papel do modelo pequeno: 8–14B resume folhas; 15–30B integra conflitos.
Aceite proposto: Nenhuma regra local vira regra universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Panorama técnico
Cenário: Muitos relatórios sobre sistemas distintos.
Estratégia: Gerar mapas temáticos e abrir folhas somente para afirmações decisivas ou contestadas.
Papel do modelo pequeno: 3–7B extrai evidência por tema.
Aceite proposto: Toda conclusão comparativa deve apontar suportes específicos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de afirmações e exceções dentro de uma folha.
8–14B: Resumidor intermediário de poucos documentos relacionados.
15–30B: Integrador de ramos conflitantes com expansão seletiva.
Requisitos de treino/runtime: Árvore com vínculos estáveis e orçamento por nó; rotular divergência separadamente de redundância.
Não aplicar quando: As relações centrais cruzam tantos ramos que a hierarquia oculta mais do que organiza.

## T008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Síntese hierárquica faz parte da abordagem.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q021.

## T008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T008 → T029 [alternative]
Como combinar: Usar comunidades quando relações cruzarem a árvore.
Interface: Conjunto de documentos e vínculos temáticos.
Condição: Grafo representar relações sustentadas por fontes.
Aceite proposto: Comparar cobertura de relações entre ramos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T008 → T044 [complements]
Como combinar: Abrir descendente responsável por exceção.
Interface: node_id, exceção e referência de folha.
Condição: Origem da exceção permanecer rastreável.
Aceite proposto: Recuperar detalhe sem expandir toda a árvore.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar repetição da mesma fonte como consenso.
- Preservar diferença entre resumo do nó e evidência primária.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar síntese de exceções distribuídas; uma árvore maior não implica melhor entendimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T023, T026, T030, T062

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S021 — Recursively Summarizing Books with Human Feedback

[https://arxiv.org/abs/2109.10862](https://arxiv.org/abs/2109.10862)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Decomposição recursiva de sumarização e treinamento com feedback humano; avaliação em níveis distintos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

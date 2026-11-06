# T029 — GraphRAG

**Nome canônico:** GraphRAG  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T029  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** graph-based RAG; RAG com grafos

## T029:C01 — conceito

Família de RAG apoiado em grafos e, neste inventário, também referência à implementação da Microsoft. Essa implementação extrai entidades e relações, organiza comunidades e produz resumos para diferentes modos de consulta. O grafo organiza relações; uma aresta extraída por LLM não é automaticamente um fato comprovado.

Como funciona:
- Extrair entidades e relações ligadas aos trechos de origem.
- Organizar grafo e resumos de comunidades conforme o método escolhido.
- Consultar relações locais ou temas globais e recuperar evidência.

## T029:C02 — aplicacao

Quando usar:
- Perguntas sobre dependências e relações entre documentos.
- Sínteses globais que trechos isolados cobrem mal.

Quando não usar:
- Pode ser custo desnecessário para perguntas factuais simples respondidas por poucos trechos.

Implementação proposta:
- Proposta: definir identidade de entidades antes da extração.
- Separar arestas extraídas, verificadas e inferidas.
- Medir custo de indexação e atualização, além da qualidade da resposta, contra RAG plano.

Aplicação LAI proposta:
Proposta LAI: experimentar com contratos e dependências entre softwares; manter trechos de código e documentação como base de verificação das arestas.

## T029:C03 — riscos_validacao

Armadilhas:
- Resolver duas entidades distintas como uma contamina muitas consultas.
- Erros de extração podem se propagar para resumos de comunidades.

Métricas sugeridas:
- Precisão de entidades e relações com evidência.
- Qualidade de perguntas relacionais e custo por atualização.

Testes propostos:
- Criar duas APIs com o mesmo nome em softwares distintos e manter identidades separadas.
- Retirar a evidência de uma relação e exigir invalidação ou marcação de incerteza.

## T029:C04 — perguntas_proveniencia

Pergunta: Qualquer banco de grafos é GraphRAG?
Resposta: Não. É necessário um processo de recuperação que use o grafo para fundamentar a geração.

Pergunta: GraphRAG substitui busca lexical?
Resposta: Não obrigatoriamente. Muitas arquiteturas combinam os mecanismos conforme a pergunta.

Pergunta: Mais arestas significam mais conhecimento confiável?
Resposta: Não. Também podem significar mais duplicatas e associações erradas. A qualidade precisa considerar identidade, proveniência e precisão das relações.

Pergunta: Como atualizar um documento alterado?
Resposta: Identifique suas contribuições e regenere estruturas dependentes conforme o pipeline. Manter relatórios antigos com fatos novos exige marcação explícita ou reconstrução consistente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T029:C05 — mecanismo_avancado

Na implementação Microsoft, busca global e local usam materiais diferentes: relatórios de comunidades favorecem síntese do corpus; entidades, relações e trechos originais favorecem investigação localizada. A escolha do modo é parte da consulta. Erros de resolução de entidades, como unir homônimos, propagam-se para relações e relatórios, multiplicando a aparência de suporte de um fato incorreto.

Condição de contorno:
Grafos pouco conectados, extração imprecisa ou perguntas predominantemente literais podem não justificar o custo de construir e atualizar comunidades e resumos.

Contrato proposto:
- Entradas: Documentos versionados, esquema de entidades e modo de consulta definido.
- Saídas: Resposta com referências às fontes e distinção entre extração e síntese.
- Estado: Grafo, relatórios, mapeamento para trechos e versão da ingestão.
- Invariante: Uma relação extraída não ganha confirmação independente por aparecer também num relatório gerado dela.

Compromissos de projeto:
- Relatórios globais ampliam cobertura temática, mas acumulam decisões de síntese.
- Expansão local preserva detalhe e pode perder relações distantes que não entraram no subgrafo.

## T029:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir duas entidades homônimas com relações incompatíveis. Verificar se a resolução evita fusão ou mantém ambiguidade, sem produzir um perfil híbrido inexistente.

Plano de avaliação proposto:
Avaliação proposta: comparar busca textual, modo local e global em tarefas correspondentes. Controlar corpus e orçamento; medir suporte das relações, cobertura temática, custo de ingestão e atualização, além da qualidade final.

Comparações:
- T051 (complements): Memória em grafo pode compartilhar entidades, mas GraphRAG acrescenta um pipeline de recuperação e geração.
- T057 (distinct_from): Relações do grafo não identificam causalidade sem hipóteses e evidências causais adicionais.

Afirmação rastreável:
GraphRAG documenta busca global com relatórios de comunidades e busca local combinando grafo e texto original.
Suporte: direct; fontes: V3A-S023, V3A-S024
Limite: As capacidades descritas não garantem correção das extrações nem ganho em toda classe de pergunta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T029:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou consultas locais e globais. Aqui o grafo distingue camadas de evidência, hipótese e decisão para evitar propagação indevida.

Projeto e decomposição
Crie arestas tipadas por natureza: relação declarada, inferência extraída e hipótese analítica. Não permita que comunidades resumidas tratem todas como observações equivalentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

Controle adaptativo
Propague proveniência por caminho e limite profundidade por utilidade. Um caminho longo com cada elo plausível pode produzir conclusão que nenhuma fonte sustenta; composição exige teste próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

Validação contrafactual
Compare busca textual, grafo factual e grafo com hipóteses separadas. Meça identidade correta, suporte de caminhos e afirmações novas indevidamente apresentadas como fatos. Unidade de avaliação: subgrafo consultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

USO AVANÇADO — Dependências de produto
Cenário: Documentos descrevem componentes e responsáveis.
Estratégia: Extrair relações explícitas, resolver identidade e consultar impacto por caminho. Validar cada salto antes de recomendar mudança.
Papel do modelo pequeno: 3–7B extrai; 15–30B explica impacto.
Aceite proposto: Nenhum impacto obrigatório pode depender de aresta sem fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

USO AVANÇADO — Panorama de controvérsias
Cenário: Fontes discordam sobre relações.
Estratégia: Agrupar posições por origem e gerar resumo de comunidades mantendo arestas incompatíveis separadas.
Papel do modelo pequeno: 8–14B resume posições locais.
Aceite proposto: Preservar desacordo e independência das fontes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de relações em ontologia pequena com opção desconhecido.
8–14B: Resumidor de comunidade já validada por identidade.
15–30B: Leitor de caminhos e controvérsias, sem inferir causalidade por conectividade.
Requisitos de treino/runtime: Ontologia, resolução de entidades e estados de evidência; orçamento de extração e atualização pode dominar consulta.
Não aplicar quando: Relações são instáveis ou pouco confiáveis e o grafo amplifica erros de extração.

## T029:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Trabalho específico GraphRAG.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q021.

## T029:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T029 → T051 [complements]
Como combinar: Persistir relações com tipo epistemológico e origem.
Interface: Entidades, aresta, fonte e status de evidência.
Condição: Grafo separar inferência de observação.
Aceite proposto: Inserir hipótese e impedir promoção automática a fato.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S024, V3A-S023, V3A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T029 → T057 [conflicts]
Como combinar: Impedir leitura causal de simples conexão.
Interface: Caminho associativo e hipótese causal separada.
Condição: Não existir identificação causal independente.
Aceite proposto: Testar pergunta causal e exigir pressupostos explícitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S024, V3A-S023, V3A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar centralidade como medida de verdade.
- Evitar contar derivados da mesma origem como corroboradores independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perguntas relacionais específicas; um grafo maior pode apenas multiplicar conexões espúrias.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T051, T077

## Fontes primárias associadas

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S023 — GraphRAG Global Search

[https://microsoft.github.io/graphrag/query/global_search/](https://microsoft.github.io/graphrag/query/global_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Consulta global por relatórios de comunidades com map-reduce; efeito do nível de comunidade no custo e detalhe.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S024 — GraphRAG Local Search

[https://microsoft.github.io/graphrag/query/local_search/](https://microsoft.github.io/graphrag/query/local_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de entidades, relações, relatórios e trechos originais para consultas locais.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

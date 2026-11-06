# T019 — Few-Shot Pruning

**Nome canônico:** Few-Shot Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T019  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de demonstrações

## T019:C01 — conceito

Seleciona ou remove demonstrações de um prompt few-shot para economizar contexto sem perder exemplos necessários de comportamento. O alvo são exemplos de tarefa, não fatos atuais. Redundância visual não implica redundância funcional: um caso raro pode ensinar a única exceção importante.

Como funciona:
- Inventariar exemplos por intenção, formato e dificuldade.
- Estimar contribuição e redundância no conjunto.
- Manter um subconjunto que cubra comportamentos e casos de falha.

Nota de nomenclatura: Rótulo descritivo de seleção de exemplos, não método único; a fonte documenta uma ferramenta de seleção relacionada.

## T019:C02 — aplicacao

Quando usar:
- Prompts com muitos exemplos semelhantes.
- Extração ou classificação com poucos padrões realmente distintos.

Quando não usar:
- Não remover a única demonstração de uma classe rara sem testar o efeito correspondente.

Implementação proposta:
- Proposta: avaliar remoção de um exemplo por vez em um conjunto separado.
- Impor cobertura mínima por classe e tipo de erro.
- Fixar ordem e versão do subconjunto para tornar resultados comparáveis.

Aplicação LAI proposta:
Proposta LAI: reduzir exemplos repetidos em contratos de ferramentas; preservar casos que ensinam ausência de evidência, erro de schema e necessidade de recuperação.

## T019:C03 — riscos_validacao

Armadilhas:
- Escolher exemplos usando o conjunto de teste causa vazamento de avaliação.
- A ordem dos exemplos pode mudar resultados mesmo com o mesmo subconjunto.

Métricas sugeridas:
- Acurácia por classe e número de tokens de exemplos.
- Degradação nos casos raros após cada remoção.

Testes propostos:
- Usar consultas não vistas de todas as classes e condições negativas.
- Comparar seleção podada com aleatória sob igual orçamento.

## T019:C04 — perguntas_proveniencia

Pergunta: Few-shot pruning modifica os pesos?
Resposta: Não. Ele muda o conjunto de exemplos apresentado na entrada.

Pergunta: É igual a seleção dinâmica?
Resposta: Não. Pode produzir um subconjunto fixo; seleção dinâmica escolhe exemplos para cada nova consulta.

Pergunta: Exemplos quase duplicados são sempre dispensáveis?
Resposta: Não. Podem mostrar diferenças mínimas que ensinam uma fronteira de decisão. Verifique a função do exemplo antes de comparar apenas o texto.

Pergunta: Posso escolher o subconjunto pela melhor nota final?
Resposta: Use desenvolvimento separado. Escolher com o teste final transforma a avaliação em otimização sobre o gabarito e superestima generalização.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T019:C05 — mecanismo_avancado

Remover demonstrações altera simultaneamente cobertura de casos, distribuição de rótulos e posição dos exemplos restantes. Portanto, atribuir todo ganho à economia de tokens pode esconder um efeito de ordem. Uma política de poda deve proteger exemplos que ensinam exceções ou formatos raros, mesmo quando eles têm pouca similaridade superficial com a maioria das consultas.

Condição de contorno:
Quando o único exemplo de uma regra importante é removido, o conjunto reduzido pode deixar de especificar o comportamento que se pretendia demonstrar.

Contrato proposto:
- Entradas: Conjunto de demonstrações verificadas, categorias de comportamento e orçamento.
- Saídas: Subconjunto ordenado com razões de exclusão e cobertura declarada.
- Estado: Versão do pool, critérios de seleção e separação do conjunto de avaliação.
- Invariante: Exemplos e respostas reservados à avaliação não entram no pool usado para escolher ou ajustar a poda.

Compromissos de projeto:
- Menos exemplos reduzem entrada e podem eliminar ruído, mas também retiram contraexemplos úteis.
- Diversidade aumenta cobertura, porém consome orçamento com casos menos próximos da consulta.

## T019:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir uma exceção demonstrada apenas uma vez e vários exemplos redundantes da regra comum. A poda deve preservar a exceção quando ela pertence ao contrato da tarefa.

Plano de avaliação proposto:
Avaliação proposta: comparar conjunto integral, remoção aleatória e poda orientada, controlando ordem e orçamento. Medir acerto por categoria, formato e sensibilidade a permutações; escolher pelo comportamento dos casos relevantes, não só pela média.

Comparações:
- T046 (complements): Seleção dinâmica escolhe exemplos por consulta; poda pode reduzir previamente o pool ou o conjunto final.

Afirmação rastreável:
O estudo sobre ordem de prompts mostra que a permutação das demonstrações afeta desempenho e não transfere automaticamente entre modelos.
Suporte: direct; fontes: V3A-S017
Limite: Os experimentos são históricos e restritos; a entrada propõe controle de ordem, não um efeito universal de magnitude fixa.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T019:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou ordem e classes. Aqui a poda de demonstrações considera cobertura de confusões específicas e incompatibilidade entre exemplos.

Projeto e decomposição
Construa matriz de confusões do modelo e selecione exemplos que distingam classes confundidas. Exemplos fáceis redundantes consomem janela sem alterar decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

Controle adaptativo
Remova demonstração apenas após testar fronteiras que ela representa. Preserve exemplos de abstenção e exceção, evitando selecionar somente respostas positivas frequentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

Validação contrafactual
Compare seleção por similaridade, diversidade e erro corrigido. Faça validação com novos documentos para não medir memorização de exemplos quase iguais. Unidade de avaliação: família de exemplos. Teste exemplos que corrigem uma confusão específica e exemplos apenas semelhantes no vocabulário. O ganho esperado deve aparecer nos casos de fronteira, sem aumentar cópia de entidades ou valores. Uma análise leave-one-out pode identificar demonstração indispensável, mas a escolha final precisa ser confirmada em documentos diferentes dos usados nessa análise.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

USO AVANÇADO — Extração de requisitos
Cenário: Permissão e obrigação são confundidas.
Estratégia: Manter pares contrastivos de modalidade e eliminar exemplos que apenas repetem formato. Testar frases novas com negação.
Papel do modelo pequeno: 3–7B extrai modalidade em esquema fechado.
Aceite proposto: Não transformar recomendação em obrigação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

USO AVANÇADO — Classificação de atendimento
Cenário: Categorias raras são comercialmente relevantes.
Estratégia: Escolher exemplos por fronteira entre categorias, reservando demonstração de informação insuficiente.
Papel do modelo pequeno: 8–14B classifica e explica evidência.
Aceite proposto: Recall das classes raras deve satisfazer critério acordado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucos pares contrastivos com rótulos estáveis e esquema simples.
8–14B: Conjunto variado por tipo de ambiguidade, não apenas proximidade lexical.
15–30B: Exemplos de decisões compostas e justificativas verificáveis.
Requisitos de treino/runtime: Banco de demonstrações rotulado, separado da avaliação; mudanças de modelo exigem nova análise de confusão.
Não aplicar quando: Exemplos contradizem instrução atual ou revelam dados fora do escopo.

## T019:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q016, V4A-Q024.

## T019:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T019 → T046 [complements]
Como combinar: Selecionar subconjunto por confusão prevista.
Interface: Intenção, classes candidatas e exemplos elegíveis.
Condição: Selector não consultar resposta esperada.
Aceite proposto: Testar exemplos irrelevantes com formato semelhante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T019 → T198 [feeds]
Como combinar: Calibrar abstenção com exemplos difíceis.
Interface: Classe, evidência e sinal mensurável de incerteza.
Condição: Calibração independente dos exemplos exibidos.
Aceite proposto: Comparar erros confiantes antes e depois da poda.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não escolher ordem usando o conjunto final de teste.
- Evitar duplicatas da mesma origem como diversidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar acerto nas fronteiras difíceis; redução do prompt pode expor limitações do modelo pequeno.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T046, T155

## Fontes primárias associadas

### A-S031 — SemanticSimilarityExampleSelector

[https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector](https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Seleção de exemplos por similaridade semântica.

Limite: Resultado de busca e módulo oficial consultados; abertura direta rejeitada por content-type text/markdown.

### V3A-S017 — Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity

[https://aclanthology.org/2022.acl-long.556/](https://aclanthology.org/2022.acl-long.556/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sensibilidade à ordem de demonstrações e não transferência automática de uma boa permutação entre modelos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S016 — What Makes Good In-Context Examples for GPT-3?

[https://arxiv.org/abs/2101.06804](https://arxiv.org/abs/2101.06804)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de demonstrações por recuperação de exemplos semelhantes; comportamento depende do conjunto e do modelo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

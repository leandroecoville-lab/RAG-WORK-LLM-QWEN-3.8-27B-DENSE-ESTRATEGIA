# T189 — Best-of-N Verification

**Nome canônico:** Best-of-N Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T189  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** seleção do melhor de N

## T189:C01 — conceito

Geração de N candidatos seguida da seleção daquele com maior nota de um verificador. O critério é qualidade avaliada, não popularidade entre candidatos. A confiabilidade depende do avaliador e de sua resistência a soluções que parecem boas, mas exploram falhas da métrica.

Como funciona:
- Gerar candidatos com diversidade suficiente.
- Avaliar cada um com testes, rubrica ou modelo verificador.
- Selecionar o melhor candidato admissível ou abster se nenhum atende ao mínimo.

## T189:C02 — aplicacao

Quando usar:
- Resultado possui teste objetivo ou avaliador confiável.
- Gerar alternativas é barato em relação ao valor de acertar.

Quando não usar:
- O avaliador apenas prefere estilo convincente ou foi ajustado nos mesmos candidatos de teste.

Implementação proposta:
- Separar geração e critério de avaliação.
- Contabilizar custo de N gerações e N verificações.
- Conservar candidatos rejeitados para analisar por que a seleção errou.

Aplicação LAI proposta:
Proposta: selecionar patches ou consultas produzidos pela Helena por execução e contratos, com orçamento limitado de alternativas.

## T189:C03 — riscos_validacao

Armadilhas:
- Quanto maior N, maior chance de explorar defeitos de um juiz imperfeito.
- Selecionar sempre um candidato força resposta mesmo quando todos estão errados.

Métricas sugeridas:
- Taxa de candidato correto presente versus taxa de seleção correta.
- Ganho de qualidade por custo adicional de N.

Testes propostos:
- Construir conjunto com candidato correto de estilo simples e incorreto muito eloquente.
- Variar N e medir se o verificador melhora seleção ou só aumenta confiança aparente.

## T189:C04 — perguntas_proveniencia

Pergunta: Best-of-N é votação?
Resposta: Não. Um avaliador escolhe; o candidato mais frequente não precisa vencer.

Pergunta: N maior sempre melhora?
Resposta: Não. Custo cresce e o verificador pode selecionar erros cada vez mais persuasivos.

Pergunta: Se há solução correta entre cem, o sistema acertou?
Resposta: Somente se a identificar e entregar; cobertura do conjunto não é precisão da seleção.

Pergunta: Pode avaliar usando o mesmo verificador?
Resposta: Isso mede alinhamento ao seletor; qualidade final precisa de evidência ou referência independente para detectar exploração do score.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T189:C05 — mecanismo_avancado

Gerar mais candidatos melhora a chance de incluir uma solução correta somente sob hipóteses sobre a distribuição. Mesmo que exista um candidato correto, o seletor pode preferir outro. Maximizar um score imperfeito também seleciona extremos de seu erro: respostas que exploram o avaliador podem vencer com notas altas. Por isso, qualidade do conjunto de candidatos e qualidade da seleção devem ser medidas separadamente.

Condição de contorno:
O melhor score observado não é uma estimativa imparcial de qualidade, principalmente quando N aumenta e o avaliador tem ruído.

Contrato proposto:
- Entradas: N candidatos, verificador versionado, regra de seleção e orçamento total.
- Saídas: Candidato selecionado com notas, empates e evidências disponíveis.
- Estado: Todos os candidatos, configuração de geração e resultados independentes de avaliação.
- Invariante: A nota usada para escolher não substitui a referência independente usada para medir acerto.

Compromissos de projeto:
- Mais candidatos ampliam cobertura e custo de geração/verificação.
- Seleção mais forte pode elevar qualidade e favorecer exploração de falhas da métrica.

## T189:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir candidato incorreto que satisfaz sinais superficiais do avaliador e candidato correto menos persuasivo. Esperar que a avaliação externa revele a seleção errada.

Plano de avaliação proposto:
Plano proposto: variar N com orçamento e comparadores declarados. Medir presença de solução correta, acerto da escolha, score proxy e resultado externo; aprovar escalabilidade somente quando a qualidade real acompanha o custo adicional.

Comparações:
- T188 (alternative): A seleção por nota não depende de uma resposta formar maioria entre amostras.

Afirmação rastreável:
O estudo de overoptimization examina deterioração do objetivo de referência ao otimizar excessivamente um reward proxy, incluindo best-of-N.
Suporte: direct; fontes: V3B-S018
Limite: O experimento usa um ambiente sintético de reward models; não fornece um limiar universal seguro para N.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T189:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou cobertura dos candidatos e seleção. Esta camada trata diversidade dirigida, custo do verificador e avaliação de exploração da métrica conforme o número de candidatos cresce.

Cobertura controlada
Gere alternativas que diferem em decisões relevantes, não apenas estilo. Para código, varie algoritmo ou decomposição; para extração, varie hipótese de evidência. Registre se o conjunto contém uma solução correta com um oráculo independente, permitindo localizar falha de geração versus falha de seleção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

Seleção sob pressão
Quanto mais candidatos, maior a chance de encontrar uma resposta que explora defeitos do score. Compare qualidade independente ao aumentar N. Se a nota sobe enquanto o acerto cai, o seletor está escolhendo extremos de seu erro; reduzir orçamento ou melhorar o critério pode ser melhor que gerar mais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

Verificador caro
Nem todos os candidatos precisam receber a checagem mais cara. Use filtros baratos que não eliminem soluções válidas sistematicamente, depois verificação aprofundada nos sobreviventes. Registre custo e falsos negativos de cada estágio. Um pipeline de filtros deve ser avaliado como composição, não por precisão isolada do último juiz.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

USO AVANÇADO — Geração de funções pequenas
Cenário: Há testes e restrições de interface.
Estratégia: Gere candidatos com abordagens distintas, compile, execute testes e examine propriedades não cobertas. Escolha pelo critério de tarefa, mantendo empates e falhas de infraestrutura explícitos.
Papel do modelo pequeno: Um 3–7B pode produzir candidatos úteis quando a solução correta aparece com frequência suficiente.
Aceite proposto: Medir cobertura do conjunto, acerto da seleção e custo total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

USO AVANÇADO — Resposta com evidências alternativas
Cenário: Uma consulta admite várias sínteses.
Estratégia: Gere versões com cobertura diferente, verifique alegações contra fontes e selecione a que cumpre requisitos. Não premiar comprimento ou tom de certeza.
Papel do modelo pequeno: Um 8–14B pode propor sínteses enquanto um verificador checa citações e cobertura.
Aceite proposto: Avaliar fidelidade e utilidade, inclusive quando nenhum candidato é aceitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Pode compensar instabilidade em tarefas estreitas, mas N alto não resolve ausência de capacidade.
8–14B: O verificador deve ser mais confiável que o critério implícito usado pelo gerador.
15–30B: Compare N candidatos de 15–30B com uma chamada mais forte, incluindo custo de julgar e esperar.
Requisitos de treino/runtime: Orquestração de inferência; treinamento do verificador é etapa opcional separada.
Não aplicar quando: Não chamar busca evolutiva inteira de best-of-N independente nem assumir que maior score significa maior verdade.

## T189:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T189:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T189 → T195 [complements]
Como combinar: Execução fornece sinais objetivos para selecionar código ou planos executáveis.
Interface: Artefato, entradas e resultados esperados.
Condição: Ambiente e oráculo são confiáveis dentro do escopo.
Aceite proposto: Separar erro de infraestrutura de reprovação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S018, C-S043, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T189 → T201 [feeds]
Como combinar: Best-of-N é uma forma de investir orçamento em largura.
Interface: Custo por candidato e qualidade marginal.
Condição: Política de parada observa retorno útil.
Aceite proposto: Comparar largura com refinamento sequencial no mesmo orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S018, C-S043, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Permitir rejeitar todos os candidatos.
- Avaliar robustez do juiz a respostas que imitam a rubrica sem satisfazer a tarefa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O alvo é obter mais respostas corretas por orçamento em tarefas verificáveis. Um grande conjunto e um juiz fraco podem piorar resultados; não há equivalência geral com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T188, T190, T195

## Fontes primárias associadas

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

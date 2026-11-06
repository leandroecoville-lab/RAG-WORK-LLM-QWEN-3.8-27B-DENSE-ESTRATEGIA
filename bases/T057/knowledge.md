# T057 — Causal Memory

**Nome canônico:** Causal Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T057  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória causal

## T057:C01 — conceito

Rótulo arquitetural para guardar hipóteses causais, intervenções, condições, estimativas e evidências de resultados. Não transforma associações em causas. É necessário distinguir relato de sequência temporal, mecanismo proposto e efeito causal identificado sob premissas explícitas.

Como funciona:
- Representar hipótese, tratamento ou ação e resultado de interesse.
- Registrar desenho de comparação e premissas de identificação.
- Guardar estimativa, incerteza, testes e limites de transferência.

Nota de nomenclatura: Não foi identificado um padrão único com esse nome; a fonte sustenta princípios de inferência causal, não uma implementação universal de memória.

## T057:C02 — aplicacao

Quando usar:
- Reutilizar aprendizados de experimentos e decisões anteriores.
- Evitar repetir interpretações causais já refutadas.

Quando não usar:
- Não concluir que uma ação causou melhora somente porque a melhora veio depois dela.

Implementação proposta:
- Proposta: separar efeito observado de efeito estimado por método causal.
- Guardar variáveis de ajuste e critérios de inclusão.
- Recuperar também evidências contrárias e condições em que a conclusão deixou de valer.

Aplicação LAI proposta:
Proposta LAI: guardar hipóteses e resultados de campanhas em estrutura causal verificável; a memória orienta investigação, sem garantir efeitos em novas campanhas.

## T057:C03 — riscos_validacao

Armadilhas:
- Confundimento e seleção podem criar efeito aparente.
- Transportar resultado entre públicos ou versões pode invalidar a interpretação.

Métricas sugeridas:
- Proporção de alegações com desenho e premissas explícitas.
- Estabilidade de estimativas e desempenho em validação externa quando disponível.

Testes propostos:
- Apresentar uma correlação sem identificação e exigir rótulo de hipótese.
- Usar um experimento com resultado nulo e impedir promoção de narrativa favorável como fato.

## T057:C04 — perguntas_proveniencia

Pergunta: Um grafo direcionado já é causal?
Resposta: Não. As arestas precisam de interpretação causal e de premissas sustentadas.

Pergunta: O agente pode aprender causa com logs?
Resposta: Logs ajudam, mas a identificação depende do desenho, das variáveis observadas e das hipóteses, não apenas do volume.

Pergunta: Uma LLM pode escolher o grafo causal?
Resposta: Pode propor hipóteses para revisão. Conhecimento de domínio, desenho de estudo e restrições observáveis precisam sustentar a escolha.

Pergunta: Uma estimativa pode ser lembrada após mudança de população?
Resposta: Pode ser recuperada como referência, preservando seu escopo. Transportá-la exige justificar compatibilidade dos mecanismos e das condições relevantes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T057:C05 — mecanismo_avancado

O conteúdo mínimo de uma memória causal inclui a pergunta estimada, a população, a intervenção, o desfecho e as premissas de identificação. Guardar somente “A causa B” apaga as condições que tornam a inferência defensável. Também convém separar o grafo assumido, o estimando identificado, a estimativa calculada e os testes de robustez: mudar uma dessas partes pode invalidar a conclusão sem alterar os dados brutos.

Condição de contorno:
Um efeito não identificado pelas hipóteses e dados disponíveis não se torna identificado por armazená-lo num grafo, aumentar o histórico ou pedir explicações à LLM.

Contrato proposto:
- Entradas: Hipótese causal, desenho de estudo, dados, premissas, estimando e procedimento de estimação.
- Saídas: Registro da conclusão com incerteza, testes, limites de transporte e evidências rastreáveis.
- Estado: Versões de dados, grafo assumido, estimador e resultados de análises de sensibilidade.
- Invariante: Associação, sequência temporal e efeito causal identificado permanecem categorias distintas na memória.

Compromissos de projeto:
- Registrar premissas torna conclusões revisáveis e aumenta o esforço de modelagem.
- Testes de robustez detectam fragilidades, mas aprovação em testes não prova ausência de confundimento ou identificação correta.

## T057:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar um confundidor plausível e repetir análise de sensibilidade. A memória deve registrar alteração e condições de fragilidade, sem manter a afirmação antiga como verdade incondicional.

Plano de avaliação proposto:
Avaliação proposta: avaliar recuperação de estimando, premissas e limites junto da conclusão. Comparar registro textual simples e ficha estruturada; medir confusão causal, reprodução da análise e comportamento diante de populações diferentes, sem inferir causalidade de acerto preditivo.

Comparações:
- T051 (distinct_from): Um grafo de memória organiza relações; um grafo causal exige interpretação e hipóteses adicionais.
- T049 (complements): Episódios podem fornecer observações e hipóteses, mas precisam de desenho apropriado para estimar efeitos.

Afirmação rastreável:
DoWhy distingue controles negativos, validação de grafo e sensibilidade à violação de premissas nas refutações de estimativas.
Suporte: direct; fontes: V3A-S041
Limite: Refutações são diagnósticos; passar nelas não constitui prova de que todas as premissas causais sejam verdadeiras.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T057:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou hipótese, estimando e identificação. Aqui memória causal guarda condições de transporte e revisões motivadas por novos ambientes.

Projeto e decomposição
Registre intervenção, desfecho, população e pressupostos junto da estimativa. Um efeito observado num ambiente pode não transportar para outro com mecanismo ou composição diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

Controle adaptativo
Use a memória para propor experimentos discriminantes, não para declarar causalidade por semelhança. Arestas representam hipóteses ou conclusões condicionadas; armazenar relações em grafo não identifica efeito causal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

Validação contrafactual
Compare recomendações com e sem verificação de transportabilidade. Avalie se o sistema detecta mudança de população, tratamento ou confundidor; um teste de refutação aprovado não prova todos os pressupostos. Unidade de avaliação: hipótese causal com pressupostos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

USO AVANÇADO — Otimização de pipeline
Cenário: Mudanças anteriores reduziram latência.
Estratégia: Recuperar experimento com hardware, carga e configuração; propor repetição controlada antes de atribuir ganho à mesma alteração no novo ambiente.
Papel do modelo pequeno: 3–7B extrai condições; código estima.
Aceite proposto: Separar efeito da mudança de variação de carga e hardware.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

USO AVANÇADO — Investigação de regressão
Cenário: Vários componentes mudaram juntos.
Estratégia: Construir hipóteses alternativas e planejar ablações isoladas; preservar resultado inconclusivo quando intervenções não forem identificáveis.
Papel do modelo pequeno: 15–30B organiza desenho; análise estatística externa.
Aceite proposto: Não chamar associação temporal de causa confirmada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de variáveis, intervenções e condições explicitadas.
8–14B: Comparador de pressupostos entre estudos ou ambientes.
15–30B: Planejador de ablações e explicador de limites, sem substituir estimador causal.
Requisitos de treino/runtime: Dados adequados, desenho de identificação e ferramentas estatísticas; memória armazena evidência, não cria identificação.
Não aplicar quando: Não há suporte para pressupostos ou intervenção relevante não pode ser distinguida de mudanças simultâneas.

## T057:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q021, V4A-Q025.

## T057:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T057 → T049 [requires]
Como combinar: Recuperar condições do episódio que originou hipótese.
Interface: Ambiente, intervenção, resultado e incertezas.
Condição: Episódio não omitir fatores relevantes.
Aceite proposto: Comparar caso semelhante com confundidor diferente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S041, A-S036. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T057 → T195 [complements]
Como combinar: Executar experimento ou cálculo que avalia hipótese.
Interface: Plano de ablação, dados e estimador.
Condição: Execução autorizada e desenho adequado.
Aceite proposto: Testar hipótese alternativa e registrar resultado nulo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S041, A-S036. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar plausibilidade linguística como evidência causal.
- Não exportar efeito estimado sem verificar população e intervenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar identificação de pressupostos e qualidade do desenho; modelo de fronteira também não extrai causalidade de dados insuficientes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T051, T056

## Fontes primárias associadas

### A-S036 — DoWhy

[https://github.com/py-why/dowhy](https://github.com/py-why/dowhy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelagem explícita e testes de premissas causais.

Limite: Fundamenta a distinção entre associação e identificação causal; não define uma técnica universal chamada Causal Memory.

### V3A-S041 — DoWhy Refuting Effect Estimates

[https://www.pywhy.org/dowhy/main/user_guide/refuting_causal_estimates/refuting_effect_estimates/index.html](https://www.pywhy.org/dowhy/main/user_guide/refuting_causal_estimates/refuting_effect_estimates/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles negativos, testes de robustez, validação de grafo e sensibilidade a pressupostos causais.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

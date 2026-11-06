# T203 — Correctness-Based Routing

**Nome canônico:** Correctness-Based Routing  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T203  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** roteamento por correção

## T203:C01 — conceito

Roteamento orientado à chance de cumprir um critério de correção da tarefa, e não somente ao custo, tamanho ou tema do pedido. Pode usar resultados de verificadores após tentativa ou previsões calibradas antes dela. É uma especialização de política de roteamento, sem algoritmo universal associado ao nome.

Como funciona:
- Definir o que conta como resultado correto para a tarefa.
- Estimar capacidade por modelo usando avaliações e sinais disponíveis.
- Escolher destino ou escalar quando a verificação rejeitar a resposta.

## T203:C02 — aplicacao

Quando usar:
- Critérios de qualidade podem ser medidos por domínio.
- Modelos apresentam competências distintas, não apenas preços diferentes.

Quando não usar:
- Usar autoconfiança verbal como única evidência de que a resposta está correta.

Implementação proposta:
- Construir matriz modelo × tarefa com resultados observados.
- Incluir abstenção e custo de verificações na política.
- Reavaliar rotas após mudança de modelo, prompt ou ferramentas.

Aplicação LAI proposta:
Proposta: a Helena selecionar modelos por evidência de competência na subtarefa, usando nomes comerciais apenas como identificação do backend.

## T203:C03 — riscos_validacao

Armadilhas:
- Preferência humana por estilo pode não representar correção factual.
- Dados antigos podem estimar mal a capacidade da versão atual.

Métricas sugeridas:
- Taxa de resultado correto por rota.
- Custo por tarefa aceita e erro entre previsão de capacidade e resultado.

Testes propostos:
- Testar tarefas de igual tamanho, mas dificuldade e requisitos distintos.
- Apresentar resposta fluente incorreta e exigir escalada pelo critério de conteúdo.

## T203:C04 — perguntas_proveniencia

Pergunta: É melhor que roteamento por tamanho?
Resposta: Pode ser, se o sinal de correção for confiável; precisa de comparação.

Pergunta: RouteLLM mede exatamente toda correção?
Resposta: Não. A fonte usa sinais de preferência; a política proposta deve definir seus próprios critérios.

Pergunta: Pode chamar o maior modelo em todo caso difícil?
Resposta: É uma política possível, mas dificuldade prevista e capacidade real precisam ser medidas, incluindo erros do modelo maior.

Pergunta: Por que guardar o resultado depois do roteamento?
Resposta: Ele permite verificar calibração e detectar mudança de desempenho; guardar apenas a decisão impede avaliar se a escolha cumpriu o contrato.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T203:C05 — mecanismo_avancado

Para prever correção, o roteador precisa de um evento verificável, como passar um contrato ou resolver um caso com referência. Preferência humana entre respostas é outro alvo e pode valorizar estilo. Se dados registram somente o modelo escolhido anteriormente, faltam resultados contrafactuais dos demais, criando viés de seleção. Avaliação offline deve comparar candidatos em uma amostra apropriada ou declarar essa limitação.

Condição de contorno:
Um classificador de tema ou tamanho de prompt não estima automaticamente a chance de cada modelo cumprir a tarefa.

Contrato proposto:
- Entradas: Tarefa, executores elegíveis, custos e sinais calibrados contra um critério de correção.
- Saídas: Destino, regra de escalonamento e resultado verificado quando disponível.
- Estado: Histórico de decisões, versões dos modelos e dados de desempenho por domínio.
- Invariante: Preferência, confiança e correção observada permanecem métricas distintas.

Compromissos de projeto:
- Modelos menores podem resolver parte da carga e reduzir custo.
- Escalonar após falha adiciona latência e depende de detectar a falha corretamente.

## T203:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: construir respostas de estilo preferido, mas factualmente erradas, e alterar o modelo de destino sem recalibrar. Esperar identificação do desalinhamento entre proxy e critério real.

Plano de avaliação proposto:
Plano proposto: comparar roteamento fixo, por custo e por correção em tarefas novas. Medir acerto externo, custo, latência e erros de escalonamento por classe; validar novamente após troca de modelos ou distribuição.

Comparações:
- T184 (distinct_from): Seleciona executores de tarefas; MoE seleciona especialistas internos de uma rede.

Afirmação rastreável:
RouteLLM aprende roteadores a partir de preferências para equilibrar custo e qualidade entre modelos.
Suporte: related; fontes: C-S001
Limite: A fonte é relacionada: preferência não é rótulo universal de correção, e o nome desta ficha não designa algoritmo padronizado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T203:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou viés de seleção e definição de correção. Esta camada propõe roteamento como política versionada, com experimentos contrafactuais, custo de escalonamento e limites de elegibilidade antes da otimização.

Elegibilidade primeiro
Antes de estimar acerto, filtre executores por acesso, ferramentas, contexto, formato e prazo. Um modelo forte sem acesso à evidência necessária pode ser uma escolha pior que outro com ferramentas adequadas. Capacidade e autorização não devem ser comprimidas numa única nota de confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

Contrafactuais medidos
Numa amostra autorizada, execute candidatos sob condições equivalentes para estimar quais casos cada um resolve. Dados históricos do roteador anterior refletem suas escolhas e podem ocultar alternativas melhores. Registre custo de produzir essa amostra e mantenha avaliação final independente da política aprendida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

Escalonar tem custo
Uma tentativa pequena seguida de modelo maior soma fila, geração e verificação. Se o primeiro caminho raramente resolve uma classe, encaminhar diretamente pode ser mais econômico. Além disso, o modelo maior precisa receber evidências e falhas relevantes, sem herdar como verdade a resposta incorreta anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

USO AVANÇADO — Automação com modelo pequeno
Cenário: Grande parte dos pedidos é rotineira e verificável.
Estratégia: Use executor 3–7B nas classes validadas, aplique verificador e escale falhas com diagnóstico. Compare com encaminhamento direto para evitar dupla cobrança sem benefício.
Papel do modelo pequeno: O pequeno modelo assume a região de competência demonstrada, não todos os pedidos por padrão.
Aceite proposto: Medir correção, cobertura, custo e prazo por caminho completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

USO AVANÇADO — Escolha entre especialista e generalista
Cenário: Há modelos com capacidades complementares.
Estratégia: Colete resultados por domínio e evidência disponível, calibre a política e monitore deriva. Mantenha opção de buscar dados ou abster-se quando nenhum executor é adequado.
Papel do modelo pequeno: Um 8–14B especializado pode ser preferível em tarefas estreitas mesmo diante de modelo maior.
Aceite proposto: Comparar contrafactuais e evitar regressões em classes raras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize contratos fechados com checagem barata para automatização seletiva.
8–14B: Especialização deve ser demonstrada com dados de resultado e não pelo nome do checkpoint.
15–30B: Um 15–30B pode ser destino intermediário; o número de etapas precisa justificar custo e latência.
Requisitos de treino/runtime: Runtime com política e sinais calibrados; treino do roteador é opcional. Preferência humana não é idêntica a correção.
Não aplicar quando: Não encaminhar indefinidamente para modelos maiores quando falta informação ou a tarefa é mal definida.

## T203:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T203:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T203 → T198 [requires]
Como combinar: A política usa sinais avaliados contra o evento de sucesso definido.
Interface: Scores, domínio e resultados observados.
Condição: Calibração válida para o caminho de implantação.
Aceite proposto: Medir erro e cobertura após seleção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S001, C-S050, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T203 → T195 [complements]
Como combinar: Execução pode confirmar resultado e decidir escalonamento em tarefas verificáveis.
Interface: Artefato, testes e falhas.
Condição: Oráculo cobre a propriedade relevante.
Aceite proposto: Comparar sucesso completo e custo de duas tentativas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S001, C-S050, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não treinar o roteador apenas com resultados dos destinos escolhidos historicamente sem declarar o viés.
- Preservar contexto e evidências ao escalar, sem validar automaticamente a resposta anterior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a política inteira com um baseline de fronteira, incluindo tentativas pequenas que falharam. A vantagem possível é custo em uma distribuição específica, sem promessa de equivalência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T135, T190, T198

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

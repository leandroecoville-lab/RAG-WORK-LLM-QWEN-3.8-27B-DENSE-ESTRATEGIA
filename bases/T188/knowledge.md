# T188 — Self-Consistency

**Nome canônico:** Self-Consistency  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T188  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** autoconsistência

## T188:C01 — conceito

Estratégia que amostra diferentes soluções para a mesma tarefa e agrega a resposta final mais consistente entre elas. O trabalho original considera caminhos de resolução diversos. Consistência amostral pode melhorar seleção, mas não transforma concordância em certeza nem substitui evidência externa.

Como funciona:
- Gerar múltiplos candidatos com diversidade de amostragem apropriada.
- Extrair e normalizar respostas finais comparáveis.
- Agregar respostas equivalentes e sinalizar falta de consenso suficiente.

## T188:C02 — aplicacao

Quando usar:
- Problema tem resposta final comparável, como cálculo ou classificação.
- Uma única amostra é instável e existe orçamento para várias tentativas.

Quando não usar:
- Resposta aberta sem critério confiável de equivalência ou todos os candidatos compartilham a mesma premissa falsa.

Implementação proposta:
- Definir número máximo de amostras e método de normalização.
- Avaliar efeito da temperatura sem alterar outras variáveis simultaneamente.
- Comparar com seleção por verificador sob o mesmo orçamento.

Aplicação LAI proposta:
Proposta: usar self-consistency em subtarefas bem delimitadas da Helena, preservando o verificador externo como referência quando existir.

## T188:C03 — riscos_validacao

Armadilhas:
- Normalização inadequada separa respostas equivalentes ou une respostas diferentes.
- Várias amostras podem reforçar erro comum.

Métricas sugeridas:
- Acerto versus número de amostras e custo.
- Margem do voto e erro condicional à concordância.

Testes propostos:
- Testar variações equivalentes de unidades e formato da mesma resposta.
- Incluir perguntas com premissa falsa e verificar se o sistema abstém ou contesta.

## T188:C04 — perguntas_proveniencia

Pergunta: É o mesmo que pedir para o modelo revisar uma vez?
Resposta: Não. Há amostragem de caminhos e agregação de respostas.

Pergunta: Exige guardar pensamentos internos completos?
Resposta: Não. A aplicação pode operar com soluções e resultados observáveis.

Pergunta: Usar a mesma seed em todas as chamadas ajuda?
Resposta: Pode eliminar diversidade útil; registre como a amostragem realmente varia e verifique duplicatas.

Pergunta: Pode parar quando uma resposta lidera?
Resposta: É uma política possível, mas precisa considerar incerteza da contagem e risco de viés introduzido pela parada adaptativa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T188:C05 — mecanismo_avancado

Agregar respostas exige uma função de equivalência anterior à contagem: 0,5 e 1/2 podem representar o mesmo número, mas 1 metro e 1 centímetro não. A diversidade dos caminhos amostrados também depende de temperatura, seeds e formulação da tarefa. Se todos convergem ao mesmo erro por conhecimento compartilhado, aumentar amostras estabiliza uma maioria incorreta em vez de corrigi-la.

Condição de contorno:
Frequência de uma resposta entre amostras não é automaticamente probabilidade calibrada de que ela esteja correta.

Contrato proposto:
- Entradas: Problema, política de amostragem, orçamento e normalizador de respostas.
- Saídas: Resposta agregada com contagens, candidatos rejeitados e possíveis ambiguidades.
- Estado: Amostras independentes de execução, unidades, equivalências e critérios de validade.
- Invariante: Somente respostas semanticamente equivalentes e válidas participam da mesma classe de votos.

Compromissos de projeto:
- Mais amostras reduzem ruído de contagem e aumentam custo.
- Normalização agressiva pode fundir respostas distintas; normalização literal pode separar equivalentes.

## T188:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar respostas numericamente equivalentes com formatos distintos e respostas iguais com unidades diferentes. Esperar agrupamento correto e preservação das diferenças de unidade.

Plano de avaliação proposto:
Plano proposto: comparar uma amostra, maioria literal e maioria normalizada em tarefas com referência externa. Controlar orçamento e amostragem; medir correção, diversidade efetiva, erros do normalizador e custo, sem aprovar apenas pelo aumento de concordância.

Comparações:
- T189 (alternative): Best-of-N usa uma nota de qualidade; self-consistency seleciona pela massa de respostas equivalentes.

Afirmação rastreável:
O trabalho original amostra caminhos diversos e agrega as respostas resultantes para selecionar a mais consistente.
Suporte: direct; fontes: C-S042
Limite: A intuição sobre múltiplos caminhos não garante que a resposta dominante seja verdadeira em toda distribuição.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T188:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu equivalência e erros de maioria. Esta camada analisa orçamento adaptativo de amostragem, dependência entre respostas e critérios de parada que não fabricam certeza.

Amostras informativas
Temperatura mais alta pode aumentar diversidade e também produzir saídas inválidas. Meça quantas amostras trazem soluções distintas e corretas, não apenas variação de redação. Se o modelo repete o mesmo erro estrutural, aumentar N pode estabilizar uma resposta errada com aparente confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

Parada adaptativa
Interromper cedo quando uma resposta lidera reduz custo, mas muda a distribuição de casos que recebem mais computação. Avalie a política inteira num conjunto separado, incluindo casos em que a liderança inicial estava errada. Uma margem de votos escolhida a olho não é uma garantia estatística universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

Resposta e raciocínio
O agrupamento deve priorizar o resultado verificável, preservando detalhes relevantes como unidade e condições. Não é necessário tratar explicações longas como prova de raciocínio correto. Quando existe um executor ou cálculo independente, use-o para distinguir candidatos que parecem diferentes mas representam o mesmo resultado válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

USO AVANÇADO — Problemas com resposta verificável
Cenário: Uma tarefa admite número, classe ou solução curta.
Estratégia: Amostre com orçamento limitado, normalize respostas e valide restrições. Compare maioria com seleção por verificador para saber qual mecanismo realmente agrega valor.
Papel do modelo pequeno: Um 3–7B pode melhorar em problemas que já resolve em parte das tentativas.
Aceite proposto: Medir probabilidade de incluir e selecionar a resposta correta separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

USO AVANÇADO — Decisão com custo variável
Cenário: Casos fáceis são frequentes e difíceis são raros.
Estratégia: Use uma primeira amostra e sinais calibrados para decidir se ampliar o conjunto. Se faltar evidência, busque-a em vez de repetir geração.
Papel do modelo pequeno: Um 8–14B pode gastar computação adicional apenas em situações justificadas.
Aceite proposto: Comparar política adaptativa com N fixo sob o mesmo orçamento médio e prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Amostragem ajuda apenas se existe massa de probabilidade em soluções corretas.
8–14B: Teste tarefas distintas; uma política útil em matemática pode não ajudar extração factual.
15–30B: Um 15–30B pode precisar de menos amostras, mas isso deve ser medido por tarefa.
Requisitos de treino/runtime: Runtime de amostragem e agregação; não é treinamento. Normalização e política de parada fazem parte do sistema.
Não aplicar quando: Não apresentar consistência como calibração nem supor independência porque as seeds diferem.

## T188:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T188:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T188 → T189 [alternative]
Como combinar: Um verificador pode selecionar candidatos quando frequência não corresponde a correção.
Interface: Conjunto de respostas e evidências.
Condição: Critério externo suficientemente informativo.
Aceite proposto: Comparar escolha por maioria e por verificação no mesmo conjunto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S042, V3B-S020, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T188 → T202 [complements]
Como combinar: Discordância pode acionar aquisição de informação, não apenas mais amostras.
Interface: Tipos de divergência e lacunas identificadas.
Condição: A ação adicional reduz uma incerteza relevante.
Aceite proposto: Medir se a observação muda a decisão corretamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S042, V3B-S020, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Guardar respostas inválidas no denominador do custo, sem contá-las como votos úteis.
- Separar amostras de desenvolvimento das usadas para avaliar a regra de parada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sucesso e custo frente a fronteira sob orçamento total explícito. Self-consistency pode melhorar tarefas específicas, mas não cria conhecimento que todas as amostras desconhecem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T156, T187, T189, T205

## Fontes primárias associadas

### C-S042 — Self-Consistency Improves Chain of Thought Reasoning in Language Models

[https://arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Amostra caminhos diversos e agrega respostas finais equivalentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

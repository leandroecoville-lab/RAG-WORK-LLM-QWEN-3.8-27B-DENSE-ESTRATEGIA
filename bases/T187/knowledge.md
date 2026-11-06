# T187 — Ensemble Voting

**Nome canônico:** Ensemble Voting  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T187  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** votação de ensemble

## T187:C01 — conceito

Agregação das previsões de vários modelos ou executores por votação. Hard voting combina rótulos; soft voting combina probabilidades, que precisam ser comparáveis e preferencialmente calibradas. Para respostas livres, antes de votar é necessário definir equivalência semântica e tratamento de abstenções.

Como funciona:
- Obter previsões independentes ou tão diversas quanto o desenho permitir.
- Normalizar rótulos ou respostas equivalentes.
- Aplicar regra de voto, pesos e desempate definidos previamente.

## T187:C02 — aplicacao

Quando usar:
- Classificação com espaço de respostas claro.
- Modelos apresentam erros parcialmente complementares.

Quando não usar:
- Respostas dependem da mesma fonte incorreta ou probabilidades têm escalas incompatíveis.

Implementação proposta:
- Medir correlação de erros entre componentes.
- Ajustar pesos apenas em validação e reservar teste final.
- Permitir abstenção quando não houver margem suficiente.
- Incluir custo de todos os componentes na comparação com o baseline.

Aplicação LAI proposta:
Proposta: testar votação para classificações específicas da Helena com referência observável, sem usar contagem de opiniões como substituto de evidência.

## T187:C03 — riscos_validacao

Armadilhas:
- Muitos modelos redundantes só repetem o mesmo viés.
- Maioria pode ser errada mesmo com alta concordância.

Métricas sugeridas:
- Acerto do ensemble comparado ao melhor componente.
- Calibração, discordância e custo por previsão aceita.

Testes propostos:
- Criar casos em que dois componentes compartilham erro e um está correto.
- Testar empates e probabilidades não calibradas antes de usar soft voting.

## T187:C04 — perguntas_proveniencia

Pergunta: Soft voting é sempre superior?
Resposta: Não. Probabilidades mal calibradas podem dar peso excessivo a um modelo confiante e errado.

Pergunta: Votar exige vários modelos?
Resposta: Pode agregar execuções, mas a independência e diversidade precisam ser avaliadas.

Pergunta: Maioria de três cópias iguais aumenta evidência?
Resposta: Não. Repetir o mesmo erro não acrescenta informação independente.

Pergunta: Como lidar com abstenção?
Resposta: Defina se ela reduz o peso disponível ou provoca escalonamento; não converta ausência de evidência em voto por uma classe arbitrária.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T187:C05 — mecanismo_avancado

Antes de somar probabilidades, todos os participantes precisam usar o mesmo espaço de classes e a mesma ordem. Uma permutação silenciosa de rótulos pode produzir um ensemble numericamente válido e semanticamente errado. Pesos de votação devem ser ajustados em dados separados da avaliação final. Para respostas livres, a normalização que agrupa equivalentes também vira parte do sistema e pode errar.

Condição de contorno:
Erros correlacionados limitam o benefício de adicionar modelos; soft voting não corrige automaticamente probabilidades mal calibradas.

Contrato proposto:
- Entradas: Predições, rótulos canônicos, probabilidades disponíveis e política de pesos/empates.
- Saídas: Decisão agregada com votos, abstenções e proveniência.
- Estado: Mapas de classes, pesos escolhidos e versão do normalizador.
- Invariante: Cada coluna de probabilidade representa a mesma classe em todos os participantes.

Compromissos de projeto:
- Hard voting perde intensidade de preferência e exige menos informação.
- Soft voting usa mais sinal e exige comparabilidade probabilística e alinhamento rigoroso.

## T187:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inverter a ordem de classes de um modelo sem alterar seus números e inserir empate. Esperar detecção do desalinhamento e aplicação explícita da regra de desempate.

Plano de avaliação proposto:
Plano proposto: comparar membros individuais e ensemble em dados independentes. Medir correção, calibração, correlação de erros e custo; avaliar pesos sem reutilizar o conjunto final e aceitar agregação somente quando melhora o objetivo definido.

Comparações:
- T188 (alternative): Self-consistency agrega amostras de soluções, frequentemente do mesmo modelo, em vez de pressupor classificadores distintos.

Afirmação rastreável:
A documentação scikit-learn define soft voting pela agregação ponderada de probabilidades e escolha da classe com maior média.
Suporte: direct; fontes: C-S041
Limite: O procedimento matemático não garante calibração nem trata automaticamente equivalência de respostas abertas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T187:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou espaço de classes e normalização. A nova camada quantifica o valor da diversidade, considera abstenções e separa votação de sistemas que apenas usam vários modelos em etapas distintas.

Erros conjuntos
Avalie a matriz de erros compartilhados, não somente a precisão isolada de cada participante. Um terceiro modelo que repete os erros dos dois primeiros pode adicionar pouco valor. Diversidade útil precisa ser medida no domínio; marcas, prompts ou seeds diferentes não demonstram independência estatística.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

Abstenção e empate
Defina como votos ausentes, respostas inválidas e empates afetam a decisão. Forçar todos a escolher pode produzir maioria artificial em casos sem informação suficiente. Uma política proposta só publica quando há suporte válido e um verificador de requisitos passa; caso contrário, busca evidência ou encaminha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

Vários modelos não implica votação
AlphaEvolve usa modelos com papéis na busca de programas, mas isso não comprova decisão por maioria. Registre o mecanismo exato de agregação: votação de classe, média de probabilidades, ranking por juiz ou evolução. Essas formas têm custos e garantias diferentes e não devem compartilhar um rótulo genérico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

USO AVANÇADO — Classificação com rótulos fechados
Cenário: Erros de uma classe específica têm custo elevado.
Estratégia: Escolha participantes com falhas complementares, ajuste pesos em desenvolvimento e teste abstenção. Use probabilidades somente quando significado e calibração forem comparáveis.
Papel do modelo pequeno: Modelos 3–7B especializados podem compor uma decisão estreita, se a diversidade compensar o custo.
Aceite proposto: Medir erro por classe, cobertura e custo adicional frente ao melhor participante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

USO AVANÇADO — Extração de campos
Cenário: Há discordância sobre valores recuperáveis em documentos.
Estratégia: Peça extrações independentes e confronte divergências com a evidência original. Não vote sobre strings sem normalização de unidade e identidade.
Papel do modelo pequeno: Um 8–14B pode ser um dos extratores; o documento é a referência decisiva.
Aceite proposto: Avaliar campos corretos e erros compartilhados, incluindo ausência de informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Vários modelos baratos podem custar mais que uma chamada melhor; comparar orçamento total.
8–14B: Especialização complementar é hipótese mais concreta que duplicar o mesmo prompt.
15–30B: Um 15–30B pode funcionar como participante ou árbitro, mas arbitrar não é votar.
Requisitos de treino/runtime: Orquestração de inferência; pesos de votação exigem dados separados. Não implica atualização dos modelos.
Não aplicar quando: Não converter proporção de votos em probabilidade de verdade sem calibração na distribuição relevante.

## T187:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de sistemas com múltiplos modelos consultada. Casos como AlphaEvolve não são classificados automaticamente como ensemble voting; não foi confirmado caso exato adicional de votação em produção neste recorte.
Consultas registradas: V4B-Q011.

## T187:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T187 → T198 [requires]
Como combinar: Probabilidades e limiares de abstenção precisam de avaliação de confiabilidade.
Interface: Votos, scores e resultados rotulados.
Condição: Conjunto final independente dos pesos escolhidos.
Aceite proposto: Medir calibração e cobertura por domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S041, V4B-S022, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T187 → T200 [complements]
Como combinar: Evidência independente pode resolver discordâncias que a maioria não decide corretamente.
Interface: Campos contestados e fontes originais.
Condição: Verificador não recebe a maioria como resposta esperada.
Aceite proposto: Incluir casos em que todos os participantes erram igual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S041, V4B-S022, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar votos individuais para detectar correlação e mudança de comportamento.
- Não agrupar respostas semanticamente distintas apenas para aumentar consenso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o ensemble com uma chamada de fronteira sob custo e prazo equivalentes. Um ganho em classificação fechada não prova capacidade geral nem justifica votar sobre fatos sem evidência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T186, T188, T198, T205

## Fontes primárias associadas

### C-S041 — Voting Classifier — scikit-learn

[https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hard voting usa votos de classe e soft voting agrega probabilidades.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T202 — Uncertainty-Aware Planning

**Nome canônico:** Uncertainty-Aware Planning  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T202  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejamento com incerteza

## T202:C01 — conceito

Planejamento que representa explicitamente o que é conhecido, estimado e desconhecido e considera a utilidade de obter informação antes de agir. A incerteza pode estar na entrada, nas ferramentas ou na chance de sucesso. Não deve ser reduzida a um número arbitrário declarado pelo modelo.

Como funciona:
- Mapear premissas e consequências das alternativas.
- Identificar qual observação reduziria incerteza relevante à decisão.
- Escolher entre agir, investigar, escalar ou encerrar conforme custo e viabilidade.

## T202:C02 — aplicacao

Quando usar:
- Há informação incompleta que pode mudar a escolha de ação.
- Ferramentas têm confiabilidade ou disponibilidade variáveis.

Quando não usar:
- Adicionar checagens sem relação com decisão material ou com custo maior que seu benefício esperado.

Implementação proposta:
- Distinguir falta de dado, ambiguidade e falha de capacidade.
- Usar estimativas calibradas quando houver dados e faixas explícitas nos demais casos.
- Atualizar plano após observação, preservando hipóteses descartadas com motivo.

Aplicação LAI proposta:
Proposta: a Helena consultar versão, evidência ou estado real antes de ações cuja escolha depende desses dados, evitando escalar apenas por linguagem insegura.

## T202:C03 — riscos_validacao

Armadilhas:
- Probabilidade inventada cria falsa precisão.
- Planejador pode investigar indefinidamente sem uma regra de término.

Métricas sugeridas:
- Decisões corrigidas por informação adicional.
- Custo de investigação e taxa de ações inviáveis evitadas.

Testes propostos:
- Criar cenário em que uma consulta muda a ação ótima e verificar sua escolha.
- Criar informação irrelevante e conferir que o agente não gasta recursos desnecessários.

## T202:C04 — perguntas_proveniencia

Pergunta: Planejar com incerteza exige probabilidades exatas?
Resposta: Não. Pode usar intervalos e estados de desconhecimento explícitos.

Pergunta: SayCan prova isso para software?
Resposta: Não. A transferência do princípio de viabilidade para ferramentas é proposta de engenharia.

Pergunta: Uma probabilidade por ação basta para o plano?
Resposta: Não se ações compartilham falhas ou mudam o estado; dependências precisam entrar na avaliação.

Pergunta: Quando perguntar ao usuário?
Resposta: Quando a informação ausente depende de sua intenção e altera materialmente a escolha; outras lacunas podem ser resolvidas por observação autorizada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T202:C05 — mecanismo_avancado

A incerteza pode estar na interpretação do objetivo, no estado do ambiente ou no resultado da ação. Cada fonte pede uma resposta diferente: esclarecer objetivo, observar o ambiente ou testar uma ação reversível. Um plano deve distinguir utilidade para a tarefa de viabilidade operacional. Combinar scores sem calibração ou hipóteses claras produz um ranking, não necessariamente uma probabilidade válida de sucesso do plano inteiro.

Condição de contorno:
Uma ação pode ser linguisticamente plausível e impossível no estado atual, mesmo quando descrita com alta confiança.

Contrato proposto:
- Entradas: Objetivo, observações, ações disponíveis, estimativas e custos de adquirir informação.
- Saídas: Próxima ação ou observação com justificativa baseada na lacuna relevante.
- Estado: Crenças, pré-condições verificadas e origem de cada estimativa.
- Invariante: O plano não trata uma hipótese desconhecida como pré-condição satisfeita.

Compromissos de projeto:
- Observar antes reduz alguns erros e consome tempo ou recursos.
- Planos conservadores podem ser confiáveis e deixar de explorar alternativas úteis.

## T202:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer uma ferramenta mencionada na documentação, mas indisponível na sessão, e outra disponível com efeito incerto. Esperar distinção entre falta de acesso e incerteza sobre resultado.

Plano de avaliação proposto:
Plano proposto: comparar planejamento direto e planejamento com aquisição de informação em ambientes controlados. Medir sucesso, ações inválidas, custo de observação e arrependimento frente às opções disponíveis; definir política conforme consequências e reversibilidade.

Comparações:
- T198 (complements): Calibração ajuda quando existe evento de sucesso bem definido, mas não substitui representar estados desconhecidos.

Afirmação rastreável:
SayCan combina conhecimento procedural de linguagem com funções de valor associadas a habilidades no ambiente físico.
Suporte: related; fontes: C-S053
Limite: A fonte apoia distinguir utilidade e viabilidade; o contrato geral de incerteza desta ficha é proposta editorial.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T202:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou fontes de incerteza. O aprofundamento transforma essa distinção em ações de observação, atualizações de plano e critérios para evitar que confiança verbal substitua pré-condições.

Lacuna localizada
Registre qual variável falta e qual decisão depende dela. Incerteza sobre identidade pede consulta ou confirmação; sobre estado pede observação; sobre efeito pode pedir teste reversível. Uma nota global de confiança não informa qual ação reduz o risco nem se a tarefa pode prosseguir parcialmente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

Valor de informação
Compare custo de observar com impacto de decidir errado. Nem toda busca adicional é útil: a fonte pode repetir informação já conhecida ou não resolver a ambiguidade relevante. Uma política proposta só solicita observação quando ela pode alterar a decisão ou confirmar uma pré-condição importante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

Atualização coerente
Depois de receber evidência, revise premissas e ações dependentes, preservando o que permanece válido. Se observações se contradizem, mantenha o estado como incerto até adjudicar fonte e tempo. Não multiplique scores de linguagem e viabilidade como probabilidades do plano inteiro sem hipóteses e calibração apropriadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

USO AVANÇADO — Agente de operação
Cenário: Uma ação depende do estado atual de um recurso.
Estratégia: Consulte o recurso, confirme versão e pré-condição, e planeje a ação sobre essa observação. Se houver mudança concorrente, reavalie antes de executar.
Papel do modelo pequeno: Um 3–7B pode seguir um fluxo estreito quando a API fornece estado verificável.
Aceite proposto: Nenhuma pré-condição desconhecida tratada como satisfeita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

USO AVANÇADO — Pesquisa com entidades ambíguas
Cenário: A consulta pode se referir a produtos ou versões diferentes.
Estratégia: Faça uma busca discriminante ou solicite o detalhe mínimo necessário. Evite redigir uma resposta longa sobre uma entidade escolhida por suposição.
Papel do modelo pequeno: Um 8–14B pode comparar hipóteses e selecionar a observação mais informativa.
Aceite proposto: Resolver ambiguidade com menos chamadas e manter proveniência da escolha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Planos curtos com estados explícitos são mais adequados que estimativas abstratas de confiança.
8–14B: Use ferramentas para observar variáveis, preservando limites quando a evidência não existe.
15–30B: Maior porte pode explorar hipóteses complexas, mas não torna observações desatualizadas válidas.
Requisitos de treino/runtime: Runtime de planejamento com fontes e estado; probabilidades exigem avaliação empírica quando usadas numericamente.
Não aplicar quando: Não interpretar confiança alta como permissão para ignorar uma condição externa não observada.

## T202:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019, V4B-Q024.

## T202:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T202 → T198 [feeds]
Como combinar: Calibração permite interpretar sinais usados para decidir observar ou encaminhar.
Interface: Evento de sucesso e score validado.
Condição: Distribuição compatível com a decisão.
Aceite proposto: Comparar erro e cobertura após a política.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S053, C-S050, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T202 → T203 [complements]
Como combinar: Roteamento pode escolher executor ou busca adicional conforme a lacuna.
Interface: Tipo de incerteza, elegibilidade e custo.
Condição: Encaminhar realmente oferece capacidade ou informação nova.
Aceite proposto: Medir resolução de falhas, não apenas troca de modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S053, C-S050, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não repetir buscas que não podem mudar a decisão.
- Registrar hipóteses revogadas para evitar que retornem silenciosamente ao plano.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare decisões corretas e custo de observação com fronteira sob o mesmo acesso ao ambiente. Planejamento explícito ajuda a administrar limites; não cria informação inexistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T198, T203

## Fontes primárias associadas

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S053 — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

[https://arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Planejamento pode combinar adequação linguística com estimativas de viabilidade das habilidades.

Limite: Fonte primária sobre robótica; aplicação a ferramentas de software é uma analogia de engenharia, não resultado demonstrado pelo artigo.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

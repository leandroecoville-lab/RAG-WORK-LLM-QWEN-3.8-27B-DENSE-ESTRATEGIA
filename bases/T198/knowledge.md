# T198 — Calibrated Confidence

**Nome canônico:** Calibrated Confidence  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T198  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** confiança calibrada

## T198:C01 — conceito

Confiança calibrada é uma estimativa de probabilidade cuja frequência observada de acerto corresponde aproximadamente aos valores previstos no domínio avaliado. Uma LLM declarar alta confiança não estabelece calibração. É necessário definir o evento de acerto e comparar previsões com resultados em dados separados.

Como funciona:
- Coletar escores e resultados verdadeiros em tarefas representativas.
- Ajustar transformação de calibração quando apropriado.
- Avaliar confiabilidade por faixa de escore e monitorar mudança de distribuição.

## T198:C02 — aplicacao

Quando usar:
- Decisões precisam de limiares de aceitação ou escalada.
- Existe referência suficiente para medir acertos e erros.

Quando não usar:
- Transformar linguagem de certeza em probabilidade sem validação ou extrapolar calibração entre domínios.

Implementação proposta:
- Separar dados de ajuste e teste da calibração.
- Medir Brier score, curvas de confiabilidade e cobertura de abstenção.
- Recalibrar após troca de modelo, prompt ou distribuição quando necessário.

Aplicação LAI proposta:
Proposta: a Helena usar probabilidades apenas quando vinculadas a avaliação de evento definido; nos demais casos, declarar evidência e incerteza qualitativa.

## T198:C03 — riscos_validacao

Armadilhas:
- ECE depende de divisão em faixas e pode esconder erros locais.
- Modelo calibrado globalmente pode falhar em subgrupos ou tarefas específicas.

Métricas sugeridas:
- Brier score e erro de calibração com tamanho de amostra.
- Erro dos casos aceitos em cada limiar de cobertura.

Testes propostos:
- Avaliar em período posterior ao utilizado no ajuste.
- Criar deslocamento de distribuição e verificar se confiança perde aderência aos acertos.

## T198:C04 — perguntas_proveniencia

Pergunta: Noventa por cento dito pelo modelo é probabilidade real?
Resposta: Não sem calibração observada.

Pergunta: Temperatura de calibração altera criatividade?
Resposta: É outro uso da escala de logits, aplicado a confiança; não se confunde com temperatura de geração.

Pergunta: Confiança de 90% certifica um caso individual?
Resposta: Não. O significado é frequencial em casos comparáveis, condicionado ao evento e à distribuição avaliados.

Pergunta: Aumentar temperatura sempre calibra?
Resposta: Não. O parâmetro deve ser ajustado e validado; uma transformação adequada em um conjunto pode falhar sob mudança de distribuição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T198:C05 — mecanismo_avancado

Calibração é uma propriedade estatística de previsões e resultados em uma distribuição. Agrupar exemplos por confiança e comparar frequência de acerto revela desvios, mas a escolha dos bins pode ocultar erros locais. Uma pontuação própria, como Brier, avalia probabilidades contra eventos observados sem depender apenas do rótulo vencedor. Para respostas abertas, o evento de acerto precisa ser definido antes de produzir o número.

Condição de contorno:
Calibração em um domínio não se preserva automaticamente após mudança de modelo, prompt, ferramenta ou população de consultas.

Contrato proposto:
- Entradas: Predições probabilísticas, critério de correção e dados de calibração separados da avaliação.
- Saídas: Estimador calibrado e relatório por faixa, domínio e cobertura.
- Estado: Transformação aprendida, versões e distribuição de referência.
- Invariante: Nenhum resultado usado para ajustar a calibração conta como evidência independente de sua qualidade final.

Compromissos de projeto:
- Calibrar pode melhorar decisões sem aumentar acurácia do classificador.
- Abster-se reduz cobertura e pode diminuir erro entre respostas entregues.

## T198:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter confiança constante enquanto muda a frequência real de acerto em outro domínio. Esperar detecção de descalibração e revisão da política de decisão.

Plano de avaliação proposto:
Plano proposto: comparar probabilidades originais e calibradas em dados novos. Medir Brier, curvas de confiabilidade, acurácia e risco versus cobertura; escolher limites de abstenção conforme custo dos erros, sem limiar universal inventado.

Comparações:
- T203 (complements): Estimativas calibradas podem orientar quando encaminhar uma tarefa a outro executor.

Afirmação rastreável:
O estudo de calibração avalia discrepâncias entre confiança e acerto e métodos de ajuste, incluindo temperature scaling.
Suporte: direct; fontes: C-S050
Limite: Resultados de classificação não tornam confiança verbal de uma LLM automaticamente uma probabilidade válida.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T198:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu calibração estatística e Brier. Esta camada orienta definição do evento, avaliação de cobertura e manutenção de limiares quando modelo, domínio ou política de seleção mudam.

Evento mensurável
Escolha o que significa sucesso: campo correto, teste passado, resposta sustentada ou tarefa concluída. Um único número para toda resposta pode esconder componentes com riscos diferentes. Para linguagem aberta, rotule com critérios consistentes e preserve discordâncias; sem evento definido, a confiança não possui interpretação operacional estável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

Seleção altera distribuição
Um roteador pode mandar apenas casos difíceis ao modelo maior e apenas casos fáceis ao menor. Calibração medida antes dessa seleção pode deixar de valer. Avalie por caminho efetivo, incluindo abstenções e rejeições. A precisão dos casos respondidos deve ser acompanhada da fração de casos que o sistema aceita responder.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

Mudanças de versão
Quantização, adapter, prompt e ferramenta podem alterar a relação entre score e acerto. Monitore deriva e reavalie limiares com dados recentes separados. Não ajuste continuamente sobre a mesma amostra que será usada para anunciar melhoria; registre quais dados informaram cada versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

USO AVANÇADO — Roteamento com abstenção
Cenário: Uma aplicação aceita automatizar apenas casos de baixo risco.
Estratégia: Calibre um sinal contra resultado verificável, escolha limiar no desenvolvimento e avalie cobertura/erro em dados independentes. Encaminhe ou busque evidência quando o sinal não basta.
Papel do modelo pequeno: Um 3–7B pode atender a região em que foi validado, sem fingir confiança universal.
Aceite proposto: Medir erro entre aceitos e custo dos encaminhamentos por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

USO AVANÇADO — Extração com revisão humana
Cenário: Alguns campos exigem mais certeza que outros.
Estratégia: Calibre por tipo de campo e contexto, usando evidência do documento e sinais do modelo. Mostre incerteza útil para revisão, evitando um percentual decorativo.
Papel do modelo pequeno: Um 8–14B pode produzir valores e sinais, mas o número final depende de validação.
Aceite proposto: Reduzir trabalho de revisão sem aumentar erros importantes omitidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Confiança verbal do 3–7B não é uma probabilidade calibrada; usar dados de resultado.
8–14B: Modelos intermediários precisam de avaliação por domínio e tipo de tarefa.
15–30B: Maior porte pode melhorar acerto sem melhorar calibração na mesma proporção.
Requisitos de treino/runtime: Etapa estatística sobre resultados observados; não basta pedir ao modelo uma nota de certeza.
Não aplicar quando: Não interpretar aprovação de schema ou de política formal como probabilidade de verdade de toda resposta.

## T198:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019, V4B-Q024.

## T198:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T198 → T203 [feeds]
Como combinar: Estimativas calibradas ajudam a escolher executores e escalonamento.
Interface: Probabilidade do evento definido, custo e domínio.
Condição: Distribuição de implantação compatível ou monitorada.
Aceite proposto: Comparar correção e cobertura por destino.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V3B-S019, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T198 → T202 [complements]
Como combinar: Incerteza pode orientar qual observação adicional adquirir.
Interface: Lacuna e efeito esperado de obter evidência.
Condição: Sinal tem interpretação validada.
Aceite proposto: Medir se a ação reduz erro, não apenas aumenta confiança.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V3B-S019, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Avaliar subgrupos em que a média global esconde falhas.
- Manter abstenções e casos rejeitados no relatório de cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas de erro e cobertura sob o mesmo critério de sucesso. Uma confiança calibrada permite decidir onde usar um modelo pequeno; não amplia sua capacidade nem garante cada resposta individual.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T156, T187, T202, T203

## Fontes primárias associadas

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

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

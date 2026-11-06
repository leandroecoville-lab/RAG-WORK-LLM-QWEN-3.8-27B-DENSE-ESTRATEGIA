# R012 — Tinker — Prompt Distillation

**Nome canônico:** Tinker Prompt Distillation  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Tinker prompt-distillation recipe; Tinker Prompt Distillation

## R012:C01 — conceito

Receita do Tinker Cookbook para gerar exemplos com um professor condicionado por instruções e treinar um aluno para a tarefa com prompt reduzido. A documentação consultada demonstra classificação de linguagem. É uma referência de implementação de treinamento, não uma memória externa nem garantia de suporte a todo checkpoint local.

Como funciona:
- Gerar dataset de exemplos usando o professor e o prompt da tarefa.
- Aplicar treinamento do aluno com os exemplos selecionados.
- Amostrar e avaliar o checkpoint para conferir retenção do comportamento.

## R012:C02 — aplicacao

Quando usar:
- Experimentação de destilação de um prompt estável.
- Equipe dispõe de dados representativos e acesso à infraestrutura de treinamento necessária.

Quando não usar:
- Presumir que uma receita demonstra resultados em português, ferramentas ou modelos não avaliados.

Implementação proposta:
- Conferir requisitos atuais e compatibilidade do modelo antes de iniciar.
- Substituir exemplos demonstrativos por dataset com curadoria e divisão correta.
- Registrar prompt, dados, configuração e checkpoint em cada experimento.

Aplicação LAI proposta:
Proposta: usar a receita como referência para experimento controlado da Helena; priorizar medição antes de ampliar treino ou inferir economia.

## R012:C03 — riscos_validacao

Armadilhas:
- Executar receita de classificação não comprova transferência a agentes completos.
- Custos e modelos disponíveis podem mudar; esta base não fixa preço nem disponibilidade.

Métricas sugeridas:
- Qualidade em teste reservado com prompt reduzido.
- Tokens economizados e custo total do experimento.

Testes propostos:
- Comparar aluno base, aluno treinado e professor com prompt completo.
- Testar exceções e linguagem não vistas na geração dos dados.

## R012:C04 — perguntas_proveniencia

Pergunta: O pacote RAG executou esse treinamento?
Resposta: Não. Ele documenta a técnica e os critérios de avaliação.

Pergunta: A receita serve como banco de fatos atualizados?
Resposta: Não. É um fluxo de aprendizagem paramétrica de comportamento.

Pergunta: Distilar este inventário substitui RAG com fontes?
Resposta: Não automaticamente. Treinar comportamento e recuperar evidência verificável resolvem necessidades diferentes.

Pergunta: Quando o investimento compensa?
Resposta: Quando a economia por chamada e a qualidade sustentada superam custo de dados, treino, atualização e avaliação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## R012:C05 — mecanismo_avancado

A receita de prompt distillation do Tinker descreve um professor que recebe instrução p e consulta q, produzindo resposta r. O estudante aprende a prever r a partir de q sem receber p. O efeito desejado é incorporar comportamento recorrente nos parâmetros. Para preparar uma experiência útil, a curadoria precisa separar exemplos de treino e avaliação por famílias de entrada; repetir as mesmas perguntas com pequenas alterações pode criar uma impressão enganosa de generalização.

Condição de contorno:
Um comportamento treinado pode envelhecer quando a política muda. Dados factuais voláteis e evidências que precisam de citação continuam exigindo mecanismos de atualização e recuperação.

Contrato proposto:
- Entradas: Prompt professor versionado, consultas representativas, respostas verificadas, checkpoint estudante e orçamento de treino.
- Saídas: Checkpoint ou adaptador, manifesto dos dados e relatório de tarefas com e sem a instrução original.
- Estado: Proveniência de exemplos, partições imutáveis, hiperparâmetros e associação entre versão do prompt e pesos.
- Invariante: A avaliação reservada não participa da seleção de exemplos, ajuste do prompt professor ou escolha de checkpoint.

Compromissos de projeto:
- Remover instruções repetidas pode reduzir tokens de entrada, mas transfere custo para coleta, treino e validação.
- Um estudante pode reproduzir regularidades e também erros do professor; aceitação depende de avaliação independente.

## R012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar uma regra após o treinamento e confrontar casos antigos e novos; verificar se a versão do comportamento fica identificável e se o fallback preserva a política vigente.

Plano de avaliação proposto:
Comparar modelo base com prompt, base sem prompt e estudante sem prompt em partição reservada. Medir acerto, violações de regra, tokens e custo total amortizado. Definir o volume de chamadas necessário para compensar o treinamento.

Comparações:
- T180 (specializes): A receita é uma implementação do objetivo de destilar instruções.
- T069 (distinct_from): Um resumo externo não altera os parâmetros do estudante.

Afirmação rastreável:
A receita treina o estudante sem o prompt usado pelo professor para produzir os exemplos.
Suporte: direct; fontes: V3D-S008
Limite: O tutorial demonstra um procedimento; não garante desempenho em novos domínios ou checkpoints.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R012:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu a receita professor com prompt e aluno sem prompt. A nova camada define critérios para escolher a receita, acompanhar disponibilidade dos modelos e comparar transferência on-policy e dados estáticos.

Receita como ponto de partida
O exemplo do cookbook demonstra uma tarefa, não uma configuração universal. Antes de adaptar, declare quais instruções são estáveis e quais entradas continuam variáveis. Preserve um prompt mínimo quando necessário para selecionar comportamento; retirar tudo pode tornar casos diferentes indistinguíveis para o aluno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

Disponibilidade temporal
Modelos e exemplos do serviço mudam. A documentação atual de distillation usa opções diferentes de exemplos históricos que foram retirados. Registre identificadores disponíveis no momento do experimento e não prometa treinamento de um checkpoint local arbitrário só porque o nome da família aparece numa receita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

Sinal na distribuição do aluno
As receitas e o estudo de on-policy distillation motivam avaliar o professor nos estados gerados pelo aluno. Compare com dados estáticos do professor e rótulos corretos quando disponíveis. Isso muda custo e cobertura; um sinal de imitação continua sujeito a erros do professor e limitações de capacidade do estudante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

USO AVANÇADO — Destilar classificação de domínio
Cenário: Um prompt extenso define categorias estáveis.
Estratégia: Gere consultas representativas, obtenha respostas verificadas e ajuste o aluno com entradas reduzidas. Teste fronteiras entre classes e exemplos fora do padrão.
Papel do modelo pequeno: Um 3–7B ou outro porte efetivamente suportado pode executar classificação estreita.
Aceite proposto: Acurácia por classe e custo completo após retirar instruções, em dados inéditos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

USO AVANÇADO — Melhorar trajetórias do aluno
Cenário: O aluno falha em estados que o professor raramente visita.
Estratégia: Colete estados em ambiente controlado e obtenha supervisão apropriada. Compare políticas sem contaminar avaliação e mantenha filtros de qualidade.
Papel do modelo pequeno: Um 8–14B pode ser estudado se disponível e adequado; faixa não implica suporte atual de todo modelo.
Aceite proposto: Sucesso de tarefa e estabilidade após a transferência, além da loss de treino.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize comportamento delimitado e verificador confiável; suporte do serviço é requisito separado.
8–14B: Receitas atuais precisam ser lidas com identificadores e APIs da versão utilizada.
15–30B: Compare custo de destilar 15–30B com adaptar diretamente um checkpoint disponível, sem presumir oferta do serviço.
Requisitos de treino/runtime: É referência de treinamento; requer dados, estudante suportado e avaliação. Não é cache nem memória externa.
Não aplicar quando: Não afirmar que recipe reproduzida em documentação foi executada neste pacote ou que transfere toda capacidade do professor.

## R012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: É a referência Tinker para prompt distillation.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## R012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R012 → T180 [feeds]
Como combinar: A receita concretiza transferência de instruções estáveis para comportamento do aluno.
Interface: Prompt professor, consultas e respostas revisadas.
Condição: Parâmetros variáveis preservados na entrada.
Aceite proposto: Testar com e sem instrução original em famílias novas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R012 → T178 [complements]
Como combinar: On-policy e off-policy são escolhas de distribuição do sinal de destilação.
Interface: Trajetórias, logits ou textos disponíveis.
Condição: Objetivo e acesso ao professor explícitos.
Aceite proposto: Comparar cobertura e qualidade sob orçamento total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Versionar professor, estudante, receita e dados; não copiar nomes de exemplos retirados.
- Manter casos reservados fora da geração e seleção de exemplos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a rotina aprendida com professor e fronteira na mesma tarefa. Tinker oferece meios para experimentar transferência; a receita não estabelece paridade geral nem economia garantida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T179, T180, T182

## Fontes primárias associadas

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

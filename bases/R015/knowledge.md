# R015 — Learning by Distilling Context

**Nome canônico:** Learning by Distilling Context  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Snell, Klein e Zhong 2022; context distillation por treinamento

## R015:C01 — conceito

Learning by Distilling Context investiga transferir para os parâmetros de um modelo benefícios antes dependentes de instruções, exemplos ou rascunhos no contexto. O trabalho de Snell, Klein e Zhong usa autotreinamento com respostas produzidas sob contexto mais informativo. É aprendizagem paramétrica; não equivale a resumir uma conversa em arquivo para reutilização posterior.

Como funciona:
- Para entradas da tarefa, o modelo condicionado em instruções pode produzir rascunho e resposta final.
- O treinamento usa a resposta final como alvo, condicionada somente na entrada, sem exigir aquelas instruções ou o rascunho.
- O professor e o aluno podem partir do mesmo modelo; a vantagem supervisionada vem do contexto adicional.

Nota de nomenclatura: Distinguir esta referência de consolidação por resumos, registrada em T069. Não transportar resultados publicados para Qwen ou português sem avaliação.

## R015:C02 — aplicacao

Quando usar:
- Tarefas repetidas com instruções estáveis e dados representativos para um experimento de treinamento.

Quando não usar:
- Fatos mutáveis que precisam de atualização imediata ou situações sem avaliação confiável das respostas geradas.

Implementação proposta:
- Proposta: escolher uma tarefa estreita, congelar instruções e gerar entradas sintéticas sem misturar exemplos de teste.
- Produzir alvos com contexto completo, filtrar erros verificáveis e manter vínculo entre entrada, prompt e resposta.
- Treinar um aluno em cópia controlada do checkpoint e comparar com o modelo base e o professor contextualizado.

Aplicação LAI proposta:
Proposta LAI: avaliar destilação de uma rotina estável de classificação ou extração; continuar recuperando documentos para conhecimento atualizado e auditável.

## R015:C03 — riscos_validacao

Armadilhas:
- Erros do professor podem virar supervisão; respostas fluentes não bastam para selecionar bons exemplos.
- Reduzir tokens de instrução pode sacrificar flexibilidade; mudanças de política exigem nova avaliação ou adaptação.

Métricas sugeridas:
- Acerto em teste reservado, aderência a novas instruções, tokens por inferência e custo total de treinamento.

Testes propostos:
- Proposta: avaliar todos os sistemas nas mesmas entradas, mantendo separados dados de geração, treino e teste.
- Incluir exceções, mudanças de regra e tarefas fora da distribuição para medir perdas ocultadas pela média.

## R015:C04 — perguntas_proveniencia

Pergunta: Esse método cria memória externa?
Resposta: Não. Ele ajusta parâmetros para internalizar comportamento que se beneficiava de contexto adicional.

Pergunta: O professor precisa ser maior que o aluno?
Resposta: Não neste desenho. O mesmo modelo recebe contexto privilegiado para produzir os alvos usados no treinamento.

Pergunta: Destilar exige um professor maior?
Resposta: Não necessariamente. O professor pode ser o mesmo modelo com contexto ou processo de geração mais informativo.

Pergunta: O aluno passa a fornecer a fonte de cada resposta?
Resposta: Não automaticamente. Treinamento paramétrico não cria proveniência por afirmação; quando citações são necessárias, mantenha um mecanismo explícito de recuperação e verificação.

Escopo das fontes:
Resumo e metadados do paper original foram consultados novamente em 2026-11-05. O mecanismo descrito está no resumo. O protocolo LAI é proposta editorial, sem reprodução experimental nem treinamento executado.

## R015:C05 — mecanismo_avancado

O ganho do professor em Learning by Distilling Context vem de uma assimetria informacional: ele recebe contexto instrutivo e pode produzir um rascunho antes da resposta; o treinamento pede ao aluno a resposta final sem aqueles apoios. Professor e aluno podem partir do mesmo modelo. A supervisão transfere comportamento observado, não garante copiar todo o processo que o produziu nem preservar informações ausentes das entradas de treinamento.

Condição de contorno:
A destilação pode falhar quando respostas do professor contêm erros, entradas sintéticas não cobrem o domínio ou a informação omitida varia de modo imprevisível em cada chamada.

Contrato proposto:
- Entradas: Modelo, instruções enriquecidas, entradas da tarefa e respostas finais produzidas com o contexto professor.
- Saídas: Modelo ajustado e avaliação de desempenho sem o contexto removido.
- Estado: Dados de autotreinamento, versões dos pesos, processo de filtragem e escopo de avaliação.
- Invariante: Remover contexto na inferência só é considerado adequado após verificar o comportamento em entradas independentes.

Compromissos de projeto:
- Internalizar instruções pode reduzir custo recorrente e acrescenta treinamento e manutenção.
- Saídas sintéticas ampliam supervisão e podem reproduzir vieses ou erros do próprio modelo professor.

## R015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir dados em que o professor usa uma instrução válida somente para parte das entradas e depois avaliar uma exceção nova. O aluno deve ser testado quanto a generalização indevida, mesmo que imite bem os dados sintéticos.

Plano de avaliação proposto:
Avaliação proposta: comparar modelo base com e sem contexto, professor enriquecido e aluno ajustado em divisões independentes. Medir qualidade por condição, regressões, obediência a instruções novas e custo amortizado; manter exemplos de avaliação fora da geração de treinamento.

Comparações:
- T179 (specializes): O trabalho é uma referência concreta para destilação paramétrica de benefícios do contexto.
- T069 (distinct_from): Consolidação por resumos preserva informação em texto externo; aqui o aprendizado altera os parâmetros do modelo.

Afirmação rastreável:
Snell, Klein e Zhong treinam o modelo a prever respostas finais sem instruções ou scratchpad presentes na geração dos alvos.
Suporte: direct; fontes: A-S040
Limite: O artigo não demonstra que qualquer conhecimento possa ser internalizado sem perda nem elimina necessidade de evidência atualizada em tarefas mutáveis.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R015:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou professor contextual e aluno. Aqui distilação de contexto é avaliada pela capacidade de atualizar, esquecer e detectar conhecimento não internalizado.

Projeto e decomposição
Defina qual conhecimento ou comportamento deve ser internalizado e qual continuará recuperável externamente. Um aluno pode reproduzir respostas frequentes sem aprender condições que as tornam válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

Controle adaptativo
Atualização de contexto exige dados novos e análise de interferência. Manter evidência externa facilita corrigir fatos sem depender apenas de retreino, especialmente quando domínio muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

Validação contrafactual
Compare aluno antes/depois, professor com contexto e aluno com RAG. Meça generalização, atualização de fatos e regressões fora da tarefa; não assumir que todo raciocínio do professor foi transferido. Unidade de avaliação: ciclo de distilação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

USO AVANÇADO — Procedimento estável de alta frequência
Cenário: Instruções repetidas dominam custo.
Estratégia: Gerar exemplos com variações e exceções, treinar aluno e manter teste de aderência à versão vigente. Retirar prompt somente após validar.
Papel do modelo pequeno: 3–7B aluno especializado.
Aceite proposto: Casos novos devem obedecer condições, não só reproduzir formatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

USO AVANÇADO — Conhecimento técnico mutável
Cenário: Fatos mudam após treinamento.
Estratégia: Internalizar vocabulário e habilidades estáveis, mantendo dados recentes em RAG; testar se aluno aceita correção explícita das fontes.
Papel do modelo pequeno: 8–14B leitor híbrido.
Aceite proposto: Não insistir em fato antigo quando evidência atual contradiz pesos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Aluno de tarefa fechada com dados de alta qualidade e cobertura de exceções.
8–14B: Aluno híbrido que combina habilidade internalizada e conhecimento externo.
15–30B: Professor ou aluno de integração complexa quando custo de treino justificar.
Requisitos de treino/runtime: Acesso a treino, dados autorizados, versão de contexto e avaliação por origem; compressão externa T069 não é o mesmo processo.
Não aplicar quando: Conhecimento muda rápido, dados são insuficientes ou aluno não demonstra generalização além de respostas vistas.

## R015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q017, V4A-Q024.

## R015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R015 → T179 [complements]
Como combinar: Formalizar transferência como atualização de parâmetros.
Interface: Professor, contexto, exemplos e checkpoint do aluno.
Condição: Treino e mudança de pesos serem verificáveis.
Aceite proposto: Comparar comportamento em exemplos inéditos e exceções.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S040, A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R015 → T009 [complements]
Como combinar: Manter fatos voláteis em recuperação externa.
Interface: Consulta, evidência vigente e versão.
Condição: Aluno respeitar contexto quando contradiz memória paramétrica.
Aceite proposto: Atualizar fato no corpus e medir resposta sem retreinar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S040, A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar resumo salvo de destilação paramétrica.
- Não usar resultado do professor como verdade sem verificar dados de treino.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefa delimitada e custo amortizado; aprender com professor contextual não transfere toda sua capacidade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R012, T069, T177, T178, T179, T180, P017

## Fontes primárias associadas

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

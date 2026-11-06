# R006 — PRISM

**Nome canônico:** PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** PRISM prompt compression; internalização seletiva em LoRA

## R006:C01 — conceito

Trabalho que identifica qual componente do prompt mais contribui para uma tarefa e procura internalizar esse comportamento em adaptadores LoRA. Distingue tarefas dominadas por padrões de exemplos daquelas dominadas por instruções procedimentais. O diagnóstico orienta o alvo da compressão paramétrica.

Como funciona:
- Comparar desempenho com instruções isoladas e com exemplos isolados.
- Gerar dados de supervisão a partir das saídas com o prompt completo.
- Treinar adaptadores para reproduzir o componente selecionado com menos contexto explícito.

Nota de nomenclatura: Nome desambiguado pelo título completo e pela fonte A-S011; não confundir com outros projetos PRISM.

## R006:C02 — aplicacao

Quando usar:
- Tarefas repetidas com prompts estáveis e conjunto de avaliação reservado.
- Estudo de troca entre custo de treinamento e custo recorrente de inferência.

Quando não usar:
- Para memorizar fatos voláteis que precisam de atualização exata e imediata.

Implementação proposta:
- Proposta: medir a linha de base e os dois componentes do prompt sem alterar o restante da tarefa.
- Filtrar exemplos gerados pelo professor e registrar suas falhas antes do treinamento.
- Comparar adaptador e prompt completo em tarefas novas, incluindo alterações posteriores de instrução.

Aplicação LAI proposta:
Proposta LAI: considerar para schemas e procedimentos estáveis do Qwen somente depois de medir a alternativa com prompt curto e recuperação de exemplos.

## R006:C03 — riscos_validacao

Armadilhas:
- Uma saída errada gerada com o prompt completo pode virar supervisão persistente.
- Um benefício medido em um conjunto não garante transferência a outro domínio ou checkpoint.

Métricas sugeridas:
- Desempenho sem o componente removido e quantidade de tokens efetivamente eliminada.
- Custo total de treinamento, inferência e atualização do comportamento.

Testes propostos:
- Proposta: reservar exemplos fora do processo de geração e seleção de dados.
- Mudar uma regra de execução e medir se o adaptador respeita a nova instrução ou retém o comportamento antigo.

## R006:C04 — perguntas_proveniencia

Pergunta: PRISM dispensa treinamento?
Resposta: Não. A proposta identificada usa autodestilação e treinamento de adaptadores LoRA.

Pergunta: PRISM significa qualquer projeto com esse nome?
Resposta: Não. Aqui a referência é o título completo registrado na ACL Anthology; há homônimos.

Pergunta: O diagnóstico garante que treinar compensa?
Resposta: Não. É um sinal sobre a contribuição do prompt. Custo, reutilização, generalização e preservação de exceções ainda precisam ser medidos.

Pergunta: Posso remover toda instrução após o treinamento?
Resposta: Somente se o desenho e a avaliação sustentarem isso. Regras variáveis e condições novas podem continuar exigindo contexto explícito.

Escopo das fontes:
A-S011 sustenta diagnóstico de componentes e internalização em LoRA. Percentuais do artigo não foram reproduzidos ou prometidos para a LAI.

## R006:C05 — mecanismo_avancado

O diagnóstico de PRISM compara comportamento com instruções e com exemplos para escolher o componente a internalizar. Essa ablação é informativa, mas interação entre componentes pode impedir interpretação puramente aditiva: exemplos podem ensinar formato somente quando uma instrução explica a exceção. A supervisão silver vem do modelo com prompt completo; portanto, erros sistemáticos desse professor podem ser transferidos ao adaptador, mesmo que a compressão preserve seu comportamento.

Condição de contorno:
O ganho diminui quando a tarefa muda frequentemente, há pouca reutilização para amortizar treinamento ou os exemplos não representam as exceções operacionais importantes.

Contrato proposto:
- Entradas: Tarefa, prompt decomposto, modelo base, entradas de treinamento e dados independentes de avaliação.
- Saídas: Adaptador identificado e prompt residual, acompanhados do diagnóstico de componentes e resultados verificáveis.
- Estado: Versão do backbone, prompt professor, dados silver, configuração de treinamento e escopo da tarefa.
- Invariante: Um adaptador não é apresentado como equivalente ao prompt completo fora das condições em que essa equivalência foi avaliada.

Compromissos de projeto:
- Internalização reduz contexto repetido e torna correções dependentes de um ciclo de treinamento e validação.
- Dados silver reduzem anotação humana e herdam limitações do professor e da distribuição de entradas.

## R006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir exceções dependentes da interação entre instrução e exemplo, depois comprimir o componente selecionado. A avaliação deve detectar perda das exceções, ainda que a média das tarefas comuns pareça boa.

Plano de avaliação proposto:
Avaliação proposta: comparar prompt completo, componentes isolados, prompt reduzido sem adaptador e PRISM na mesma divisão independente. Medir qualidade por caso, obediência a novas instruções, tokens e custo amortizado de treinamento; não escolher o diagnóstico usando o teste final.

Comparações:
- R007 (distinct_from): PRISM seleciona comportamento de componentes do prompt; SADA enfatiza interface interna e alinhamento de estados para adaptadores.
- T069 (distinct_from): Resumo externo continua sendo lido como dados; PRISM modifica comportamento por pesos adicionais treinados.

Afirmação rastreável:
PRISM usa diagnóstico entre instruções e exemplos e autodestilação de saídas do prompt completo para treinar adaptadores LoRA.
Suporte: direct; fontes: A-S011
Limite: A sigla é ambígua fora deste catálogo; esta ficha corresponde exclusivamente ao trabalho de Jha, Wang, Barbu e Aggarwal na EMNLP 2026.

Nota de pesquisa:
Identificação reconferida em 2026-11-05: PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights, Eshita Jha, Mingxian Wang, Andrei Barbu e Chetan Aggarwal, https://aclanthology.org/2026.emnlp-main.2431/. Escopo coincide com a v2; não foram associados trabalhos homônimos. Contratos e testes são propostas editoriais, sem treinamento ou reprodução de resultados.

## R006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 verificou PRISM e suas ablações. Aqui o foco é governar atualização de adapters quando o componente internalizado do prompt muda.

Projeto e decomposição
Mantenha identidade exata: Prompt Representation Internalization via Selective Compression into LoRA Weights. A proposta distingue o que foi internalizado e o que continua explícito no prompt.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

Controle adaptativo
Uma mudança de procedimento ou padrão exige avaliar se adapter antigo permanece válido. Remover instrução do contexto e depois esquecê-la no treinamento cria divergência difícil de observar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

Validação contrafactual
Compare mesmo modelo com prompt completo, adapter e prompt residual. Meça aderência a mudanças, custo de retreino e interferência em tarefas não alvo; rótulos do professor podem propagar erro. Unidade de avaliação: adapter por versão de instrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

USO AVANÇADO — Rotina repetitiva estável
Cenário: Instruções extensas se repetem em muitos pedidos.
Estratégia: Identificar componente dominante, gerar dados de treino autorizados e validar substituição seletiva antes de retirar texto do prompt.
Papel do modelo pequeno: 3–7B aluno em tarefa estreita.
Aceite proposto: Adapter deve manter exceções e formato em casos novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

USO AVANÇADO — Política com revisões
Cenário: Uma regra internalizada precisa mudar.
Estratégia: Versionar instrução e adapter juntos, testar regra antiga versus nova e manter prompt explícito durante transição.
Papel do modelo pequeno: 8–14B aluno; 15–30B professor possível.
Aceite proposto: Nenhuma resposta pode seguir regra revogada sem detecção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Aluno especializado em padrão fechado, com controle de regressões.
8–14B: Aluno para procedimento mais variado e prompt residual explícito.
15–30B: Professor ou aluno complexo quando treinamento e benefício forem demonstrados.
Requisitos de treino/runtime: Treino LoRA, dados de professor, versão da instrução e avaliação independente; nenhuma implantação PRISM foi executada.
Não aplicar quando: Regras mudam rápido, exigem auditoria literal a cada chamada ou diagnóstico não identifica componente estável.

## R006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C032 — Eshita Jha, Mingxian Wang, Andrei Barbu, Chetan Aggarwal / PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda internalização seletiva de componente de prompt.
Mecanismo documentado: Diagnóstico distingue padrões e procedimentos; dados derivados do professor treinam LoRA.
Correspondência com esta base: Título e autores preservam identidade da sigla.
Transferência proposta para modelo pequeno: Proposta de engenharia: Comparar adapter 3–30B ao mesmo modelo com instrução completa e medir custo de atualização.
Limite: Não encontrada implantação bigtech exata nesta pesquisa; resultados não legitimam trocar de PRISM homônimo. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Consulta encontrou pesquisa e integração relacionada de compressão, não implantação bigtech exata do PRISM identificado. Sigla não foi associada a trabalhos homônimos.
Consultas registradas: V4A-Q017, V4A-Q024.

## R006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R006 → T179 [complements]
Como combinar: Tratar internalização como atualização paramétrica.
Interface: Prompt de origem, dados e adapter versionado.
Condição: Pesos realmente serem treinados e avaliados.
Aceite proposto: Comparar aluno antes e depois, mantendo tarefa e fontes constantes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S011, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R006 → T072 [requires]
Como combinar: Vincular adapter à versão de instrução.
Interface: adapter_id, instrução, base model e dados.
Condição: Roteamento impedir uso de versão incompatível.
Aceite proposto: Enviar pedido sob regra nova ao adapter antigo e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S011, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir PRISM com trabalhos homônimos.
- Não apresentar LoRA treinada como cache de contexto sem custo de manutenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar substituição de instrução numa tarefa definida; não inferir paridade geral com o professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T179, T180, T182, R007

## Fontes primárias associadas

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

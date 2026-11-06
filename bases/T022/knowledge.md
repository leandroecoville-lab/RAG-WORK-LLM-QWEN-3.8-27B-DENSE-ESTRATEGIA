# T022 — Instruction Compression

**Nome canônico:** Instruction Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T022  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão de instruções

## T022:C01 — conceito

Reduz o espaço ocupado por instruções preservando as regras necessárias. Pode significar reescrita textual concisa ou compressão aprendida; o método precisa ser declarado. Alterar o texto não é o mesmo que internalizar uma política nos pesos.

Como funciona:
- Separar regras obrigatórias, exemplos e explicações auxiliares.
- Eliminar redundância ou produzir representação compatível.
- Comparar cumprimento de regras no prompt original e no comprimido.

## T022:C02 — aplicacao

Quando usar:
- Instruções estáveis com muita repetição.
- Múltiplos blocos que expressam a mesma regra em linguagem diferente.

Quando não usar:
- Não remover condições, prioridades ou exceções para obter uma taxa arbitrária de redução.

Implementação proposta:
- Proposta: extrair uma tabela de requisitos observáveis antes de reescrever.
- Gerar casos positivos, negativos e de conflito para cada regra.
- Versionar original e versão compacta e proibir promoção sem avaliação de cumprimento.

Aplicação LAI proposta:
Proposta LAI: compactar orientações recorrentes de ferramenta; manter permissões obrigatórias também em verificações do runtime, não apenas em linguagem natural.

## T022:C03 — riscos_validacao

Armadilhas:
- Uma frase curta pode ampliar a autorização originalmente restrita.
- Abreviações podem ser interpretadas de formas distintas por modelos diferentes.

Métricas sugeridas:
- Taxa de cumprimento por regra.
- Tokens economizados e necessidade de esclarecimentos adicionais.

Testes propostos:
- Testar conflitos entre regras e exceções raras.
- Executar o mesmo conjunto em dois consumidores se o prompt pretende ser portátil.

## T022:C04 — perguntas_proveniencia

Pergunta: Posso substituir instruções por siglas inventadas?
Resposta: Só se o consumidor tiver uma forma confiável de resolver essas siglas; do contrário você retirou informação.

Pergunta: É Context Distillation?
Resposta: A reescrita textual não. Destilação paramétrica envolve treinamento para internalizar comportamento.

Pergunta: Posso validar somente se a resposta parece adequada?
Resposta: Isso perde violações raras. Transforme cada regra relevante em casos observáveis e examine erros por categoria.

Pergunta: Qual conteúdo não convém abreviar agressivamente?
Resposta: Identificadores, condições numéricas, exceções e escopos que mudam decisões precisam de representação inequívoca; a escolha deve seguir o contrato da tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T022:C05 — mecanismo_avancado

Instruções devem ser testadas como contratos de comportamento: condição, ação, exceção e precedência. Uma reescrita curta pode preservar os verbos e perder o escopo de uma proibição. Em compressão latente, a verificação muda de inspeção textual para comportamento do par encoder/consumidor. Ambas exigem casos que distingam interpretações próximas, não apenas exemplos típicos de sucesso.

Condição de contorno:
Quando uma regra nova contradiz ou especializa a antiga, reutilizar sua representação comprimida sem atualização pode manter um comportamento obsoleto.

Contrato proposto:
- Entradas: Instruções versionadas, casos de comportamento e método de compressão declarado.
- Saídas: Texto reduzido ou representação latente ligada ao consumidor correto.
- Estado: Versão da política original, compressor e resultados de validação.
- Invariante: Exceções e limites de autorização não desaparecem por serem pouco frequentes nos exemplos.

Compromissos de projeto:
- Reescrita textual é inspecionável, mas depende da interpretação posterior.
- Compressão aprendida pode reutilizar representações, porém exige compatibilidade e testes quando as regras mudam.

## T022:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar uma regra geral com exceção explícita e depois alterar somente a exceção. A representação nova deve acompanhar a mudança, enquanto a anterior permanece identificável como obsoleta.

Plano de avaliação proposto:
Avaliação proposta: comparar instrução integral e comprimida em pares de casos que diferem em condição, negação ou precedência. Medir violações por regra, tokens e custo, mantendo exemplos de desenvolvimento separados dos testes finais.

Comparações:
- T020 (complements): Métodos aprendidos podem comprimir instruções, mas também outros tipos de contexto.
- T179 (distinct_from): Destilação paramétrica pode eliminar a necessidade do contexto de tarefa; compressão textual ainda precisa ser fornecida.

Afirmação rastreável:
Gisting treina um modelo com máscaras de atenção para representar prompts em conjuntos menores de gist tokens.
Suporte: direct; fontes: A-S033
Limite: O mecanismo requer treinamento e consumidor compatível; não é uma abreviação que qualquer API de texto interprete.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T022:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou exceções e precedência. Aqui instruções são compiladas em contratos testáveis antes da redução textual.

Projeto e decomposição
Separe objetivos, restrições e formato de saída em estrutura intermediária. Só então gere instrução curta; a forma reduzida precisa representar o mesmo conjunto de condições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

Controle adaptativo
Use testes de fronteira para detectar mudança semântica: permissões condicionais, prioridades e exceções. Frases redundantes podem funcionar como sinal ao modelo pequeno e não devem ser removidas por estética.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

Validação contrafactual
Compare instrução original, abreviada e estruturada. Meça violações por tipo, incluindo pedidos que ativam simultaneamente condições conflitantes. Unidade de avaliação: família de instruções. Use pares de pedidos que ativam a regra geral e sua exceção, incluindo um caso em que duas restrições competem. A instrução reduzida deve preservar a mesma precedência observada na especificação. Quando a forma curta falhar apenas num consumidor pequeno, aumentar explicitação local pode ser preferível a copiar integralmente todo o prompt original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

USO AVANÇADO — Classificador de documentos
Cenário: Política extensa define poucos campos.
Estratégia: Converter regras em tabela de decisão, fornecer apenas ramo aplicável e manter justificativa de seleção.
Papel do modelo pequeno: 3–7B executa decisão delimitada.
Aceite proposto: Saída deve cumprir todas as regras ativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

USO AVANÇADO — Agente com ferramentas
Cenário: Instruções misturam planejamento e protocolos.
Estratégia: Manter contrato de chamada em schema e resumo de intenção no prompt; carregar procedimento completo para operação rara.
Papel do modelo pequeno: 8–14B escolhe operação.
Aceite proposto: Nenhuma pré-condição pode desaparecer na versão curta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de regras curtas com poucos ramos e exemplos contrastivos.
8–14B: Interpretador de contrato estruturado com exceções explícitas.
15–30B: Planejador que seleciona subcontratos sem alterar sua autoridade.
Requisitos de treino/runtime: Especificação de regras, testes independentes e versão do prompt; métodos paramétricos exigem treino distinto.
Não aplicar quando: A redução muda prioridade ou o modelo não interpreta confiavelmente a estrutura escolhida.

## T022:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C032 — Eshita Jha, Mingxian Wang, Andrei Barbu, Chetan Aggarwal / PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda internalização seletiva de componente de prompt.
Mecanismo documentado: Diagnóstico distingue padrões e procedimentos; dados derivados do professor treinam LoRA.
Correspondência com esta base: Internalização de instrução se relaciona à redução de prompt, mas não é simples abreviação.
Transferência proposta para modelo pequeno: Proposta de engenharia: Comparar adapter 3–30B ao mesmo modelo com instrução completa e medir custo de atualização.
Limite: Não encontrada implantação bigtech exata nesta pesquisa; resultados não legitimam trocar de PRISM homônimo. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q017, V4A-Q024.

## T022:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T022 → T197 [complements]
Como combinar: Validar formato fora do texto de instrução.
Interface: Schema, campos obrigatórios e versão.
Condição: Validação sintática não substituir semântica.
Aceite proposto: Produzir saída bem formada que viole regra e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S033, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T022 → T014 [complements]
Como combinar: Carregar regra especializada somente quando aplicável.
Interface: Intenção, pré-condições e referência ao procedimento.
Condição: Roteamento manter cobertura de exceções.
Aceite proposto: Testar operação rara omitida do resumo inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S033, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir compressão textual com PRISM ou destilação paramétrica.
- Preservar teste da instrução original como controle.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar aderência a regras difíceis; instrução curta não garante capacidade de interpretação equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T020, T155, T179

## Fontes primárias associadas

### A-S033 — Learning to Compress Prompts with Gist Tokens

[https://arxiv.org/abs/2304.08467](https://arxiv.org/abs/2304.08467)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações compactas de prompt treinadas com alterações de máscara de atenção.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

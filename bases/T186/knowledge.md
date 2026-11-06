# T186 — Debate entre agentes

**Nome canônico:** Debate entre Agentes  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T186  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multiagent debate; Debate entre Agentes

## T186:C01 — conceito

Procedimento em que várias instâncias produzem propostas e depois confrontam argumentos, evidências ou críticas em rodadas. Pode revelar erros e alternativas, mas consenso não é prova. Agentes semelhantes podem compartilhar o mesmo erro e persuadir os demais sem informação nova.

Como funciona:
- Coletar propostas iniciais separadas para reduzir ancoragem.
- Trocar críticas específicas e pedir evidências para pontos contestados.
- Escolher resultado por critério explícito, preferindo verificação externa quando disponível.

## T186:C02 — aplicacao

Quando usar:
- Problema admite alternativas e comparação por critérios.
- Há valor em identificar objeções e hipóteses concorrentes.

Quando não usar:
- Questão já pode ser resolvida por cálculo ou teste determinístico mais barato.

Implementação proposta:
- Definir papéis, número de rodadas e orçamento total.
- Preservar propostas originais e mapear quais críticas alteraram conclusões.
- Usar árbitro com rubrica e acesso a fontes, sem votação automática por eloquência.

Aplicação LAI proposta:
Proposta: usar especialistas consultivos para contestar escolhas de arquitetura da Helena, mantendo um decisor e um critério de aceitação observável.

## T186:C03 — riscos_validacao

Armadilhas:
- Debate pode transformar diversidade inicial em erro consensual.
- Custo cresce com agentes, rodadas e contexto compartilhado.

Métricas sugeridas:
- Correções verificadas após debate versus regressões.
- Custo por decisão correta e diversidade inicial dos candidatos.

Testes propostos:
- Inserir argumento persuasivo porém falso e verificar resistência baseada em evidência.
- Comparar debate com o mesmo orçamento em candidatos independentes e teste externo.

## T186:C04 — perguntas_proveniencia

Pergunta: Três agentes concordando provam um fato?
Resposta: Não. Fontes e erros podem ser compartilhados.

Pergunta: Debate exige modelos diferentes?
Resposta: Não, mas diversidade de modelo ou evidência pode alterar correlação dos erros.

Pergunta: Agentes com nomes diferentes são diversos?
Resposta: Não necessariamente. Diversidade relevante envolve fontes, estratégias e padrões de erro, não apenas personas.

Pergunta: O árbitro deve escolher o argumento mais longo?
Resposta: Não. Deve aplicar critérios de evidência e correção; comprimento ou confiança verbal podem favorecer um erro persuasivo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T186:C05 — mecanismo_avancado

Uma rodada de debate pode acrescentar informação ou apenas redistribuir a mesma crença. Como proposta experimental, preserve respostas iniciais independentes antes de expor argumentos, registre quais alegações mudaram e exija evidência para a mudança. Agentes com pesos, fontes e prompts semelhantes tendem a compartilhar falhas; multiplicar instâncias não equivale a obter observações independentes. A ordem de exposição também pode induzir ancoragem.

Condição de contorno:
Consenso crescente pode esconder contágio de uma premissa falsa, especialmente quando um participante escreve de maneira mais persuasiva.

Contrato proposto:
- Entradas: Problema, propostas iniciais isoladas, regras de interação e evidências acessíveis.
- Saídas: Resposta selecionada com divergências e mudanças justificadas.
- Estado: Histórico por rodada, origem das alegações e orçamento de chamadas.
- Invariante: Nenhuma afirmação ganha validade apenas por ser repetida por vários participantes.

Compromissos de projeto:
- Rodadas adicionais ampliam oportunidade de crítica e custo de coordenação.
- Diversidade pode revelar erros e produzir conflitos que exigem adjudicação externa.

## T186:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma justificativa convincente com premissa falsa em um participante e variar sua posição na rodada. Esperar detecção por evidência independente e medir propagação do erro.

Plano de avaliação proposto:
Plano proposto: comparar resposta única, votação sem interação e debate com orçamento de tokens equivalente. Medir correção externa, erros compartilhados, mudanças corretas/incorretas e custo; aprovar debate quando seu ganho supera alternativas igualmente custosas.

Comparações:
- T187 (alternative): Votação agrega propostas; debate permite que participantes revisem suas próprias respostas após interação.

Afirmação rastreável:
O estudo de debate multiagente usa múltiplas instâncias que propõem e discutem respostas em rodadas.
Suporte: direct; fontes: C-S040
Limite: Melhorias experimentais não provam independência dos agentes nem tornam consenso um certificado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T186:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou respostas iniciais e destacou erros correlacionados. O aprofundamento diferencia debate, revisão paralela e arbitragem, e propõe medir se a interação acrescenta evidência ou só persuasão.

Papéis com informação distinta
Separar agentes por nomes não cria independência. Dê a cada papel um critério verificável ou fonte distinta, como contrato, execução e risco de regressão. Se todos recebem o mesmo texto e não acessam evidência adicional, a rodada pode apenas amplificar uma hipótese inicial convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

Mudança rastreável
Registre alegações, contraexemplos e motivo de cada revisão. Uma conclusão deve mudar por evidência identificada ou violação demonstrada, não porque um agente falou por último. Limite rodadas e permita manter desacordo; obrigar consenso pode apagar sinais úteis de incerteza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

Custo e juiz
Um árbitro pode herdar os mesmos vieses dos participantes. Learning Zone descreve papéis de revisão e comparação com humanos em avaliação; AutoClean usa revisores por propriedade. Esses casos apoiam desenhos delimitados, sem provar que debate livre melhora qualquer tarefa ou que todos os modelos pequenos julgam corretamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

USO AVANÇADO — Revisão de objeto de negócio
Cenário: Uma saída precisa atender conteúdo, formato e consistência.
Estratégia: Faça avaliações separadas por critério e peça discussão somente sobre conflitos concretos. Use validadores determinísticos quando o critério puder ser formalizado.
Papel do modelo pequeno: Modelos 3–7B podem revisar aspectos estreitos, preservando um árbitro externo para casos difíceis.
Aceite proposto: Medir defeitos adicionais detectados por rodada e custo de falsos alarmes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

USO AVANÇADO — Planejamento com hipóteses concorrentes
Cenário: Há duas estratégias plausíveis para resolver uma tarefa.
Estratégia: Peça planos independentes, busque evidências que os discriminem e use debate para atualizar pressupostos. Pare quando o orçamento acabar ou a evidência for suficiente.
Papel do modelo pequeno: Um 8–14B pode explorar alternativas com ferramentas, sem ser tratado como especialista universal.
Aceite proposto: Comparar decisão final com baseline de uma chamada sob orçamento equivalente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Papéis estreitos e verificadores externos reduzem exigência cognitiva de cada participante.
8–14B: Diversidade de fontes e critérios importa mais que multiplicar instâncias idênticas.
15–30B: Um 15–30B pode arbitrar casos mais complexos, mas deve ser avaliado contra julgamentos independentes.
Requisitos de treino/runtime: Orquestração em runtime; não implica treinamento. Resultados dependem de prompts, fontes, juiz e tarefa.
Não aplicar quando: Não interpretar unanimidade como probabilidade calibrada nem confundir revisão paralela sem interação com debate.

## T186:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Reviewer/Critic/Meta-Reviewer apoiam avaliação offline.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T186:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T186 → T200 [complements]
Como combinar: Uma verificação externa pode resolver desacordos sem depender da retórica.
Interface: Alegação contestada e evidência reproduzível.
Condição: Verificador possui critério independente.
Aceite proposto: Injetar argumento persuasivo falso e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S040, V4D-S012, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T186 → T193 [complements]
Como combinar: Critérios verificáveis podem funcionar como barreiras antes da discussão.
Interface: Resultados por regra e motivos de falha.
Condição: Guardrail cobre apenas o que realmente consegue verificar.
Aceite proposto: Evitar gastar debate em erros estruturais já decidíveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S040, V4D-S012, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar respostas iniciais para medir influência e ancoragem.
- Não ajustar o juiz até concordar com a conclusão desejada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare debate com uma chamada e com amostragem adicional sob o mesmo orçamento. Mais agentes podem ajudar numa tarefa, mas não equivalem a mais inteligência independente por definição.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T187, T188, T200

## Fontes primárias associadas

### C-S040 — Improving Factuality and Reasoning in Language Models through Multiagent Debate

[https://arxiv.org/abs/2305.14325](https://arxiv.org/abs/2305.14325)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instâncias debatem propostas em rodadas; concordância não é garantia universal de correção.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

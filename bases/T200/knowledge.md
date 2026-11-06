# T200 — Independent Verification

**Nome canônico:** Independent Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T200  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** verificação independente

## T200:C01 — conceito

Verificação feita por processo que reduz dependência dos mesmos pressupostos, fontes ou artefatos usados pelo gerador. Independência é uma propriedade do desenho, não do nome auditor. Um segundo agente com o mesmo contexto e modelo pode reproduzir exatamente o primeiro erro.

Como funciona:
- Extrair requisitos e artefatos finais sem depender apenas da justificativa do autor.
- Construir checagens com evidências ou métodos distintos quando possível.
- Relatar achados, escopo e limites sem transformar ausência de achado em prova absoluta.

## T200:C02 — aplicacao

Quando usar:
- Entrega de código, relatório ou integração precisa de validação adicional.
- Custo de erro justifica revisão separada.

Quando não usar:
- Revisor apenas confirma a narrativa do gerador sem inspecionar o resultado.

Implementação proposta:
- Separar autoria e revisão de testes críticos.
- Dar ao verificador acesso às fontes originais e critérios de aceite.
- Registrar o que foi efetivamente checado e quais áreas ficaram sem cobertura.

Aplicação LAI proposta:
Proposta: especialista consultivo revisar evidências da Helena com autonomia de método, enquanto decisão e execução permanecem explicitamente coordenadas.

## T200:C03 — riscos_validacao

Armadilhas:
- Modelos distintos ainda podem compartilhar a mesma fonte errada.
- Revisão com pouco contexto pode perder requisito relevante.

Métricas sugeridas:
- Defeitos encontrados que o autor não detectou.
- Falsos achados e cobertura dos critérios de aceite.

Testes propostos:
- Introduzir erro plausível com justificativa convincente e verificar detecção.
- Fornecer artefato que contradiz o resumo do autor e exigir preferência pela evidência.

## T200:C04 — perguntas_proveniencia

Pergunta: Outro agente basta para ser independente?
Resposta: Não. Precisa avaliar compartilhamento de modelo, dados, contexto e critérios.

Pergunta: Verificação independente é infalível?
Resposta: Não. Seu alcance deve ser descrito e medido.

Pergunta: Outro agente já é auditor independente?
Resposta: Não necessariamente. Verifique o que ele recebeu, quais fontes usa e como decide.

Pergunta: Um verificador formal resolve tudo?
Resposta: Pode provar propriedades de uma formalização sob hipóteses; a correspondência entre essa formalização e a necessidade real ainda precisa ser examinada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T200:C05 — mecanismo_avancado

Independência possui eixos diferentes: fonte, método, implementação e informação disponível. Um verificador de outra marca pode reutilizar a mesma fonte errada; dois programas podem compartilhar a mesma biblioteca defeituosa. Como proposta, derive casos da especificação, mantenha checagem cega quando possível e use métodos complementares. Divergência precisa de adjudicação por evidência, em vez de ser resolvida automaticamente pela confiança verbal.

Condição de contorno:
Uma checagem independente pode discordar por interpretar outro requisito; alinhar a especificação continua necessário.

Contrato proposto:
- Entradas: Artefato, especificação, evidências de origem e métodos de checagem com dependências registradas.
- Saídas: Veredito limitado aos critérios examinados e divergências documentadas.
- Estado: Mapa de fontes e componentes compartilhados entre gerador e verificador.
- Invariante: O verificador não recebe a conclusão esperada como substituto da evidência que deveria examinar.

Compromissos de projeto:
- Diversidade de métodos reduz alguns erros comuns e aumenta custo.
- Checagem cega reduz ancoragem e pode exigir explicitar melhor o contexto necessário.

## T200:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer a ambos a mesma fonte adulterada e depois incluir uma fonte independente ou teste derivado da especificação. Esperar identificação de que concordância inicial não demonstrava validade.

Plano de avaliação proposto:
Plano proposto: medir detecção de defeitos conhecidos, falsos alarmes e correlação de erros entre verificadores. Comparar métodos com orçamento declarado; aceitar independência pela redução observada de falhas compartilhadas, não pelo número de agentes.

Comparações:
- T191 (complements): Fatorar perguntas reduz contaminação contextual, enquanto diversificar fontes e métodos aborda dependências adicionais.

Afirmação rastreável:
O estudo de autocorreção intrínseca observou limitações e regressões quando modelos tentavam corrigir raciocínio sem feedback externo.
Suporte: direct; fontes: V3B-S019
Limite: Esse resultado empírico não prova incapacidade universal; sustenta a necessidade de avaliar dependências e fontes de feedback.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T200:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu eixos de independência. Esta camada define uma matriz de evidências, resolução de conflitos e testes que verificam se o revisor é sensível ao erro sem depender da conclusão do gerador.

Dependências compartilhadas
Mapeie modelo, fonte, código, biblioteca e dados usados pelo gerador e pelo verificador. Independência numa dimensão pode coexistir com dependência em outra. Dois revisores que consultam a mesma tabela errada não oferecem duas evidências independentes sobre o fato; um compilador pode verificar sintaxe sem verificar a intenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

Checagem cega quando útil
Forneça especificação e artefato, evitando apresentar a aprovação anterior como resultado esperado. Em tarefas factuais, peça busca da evidência original; em código, derive testes do contrato. Compare resultados com e sem a narrativa do gerador para medir ancoragem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

Conflito e alcance
Quando métodos discordam, examine contraexemplos e premissas antes de votar. O veredito deve indicar critérios cobertos e pendentes. AutoClean descreve revisores por propriedade antes da revisão humana; isso é um desenho operacional delimitado, não uma garantia de independência total nem ausência de erro compartilhado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

USO AVANÇADO — Revisar alteração de código
Cenário: O gerador declara que a mudança está pronta.
Estratégia: Execute testes derivados do contrato e revise efeitos laterais em uma etapa separada. Preserve artefato e evidências para que o humano examine divergências reais.
Papel do modelo pequeno: Um 3–7B pode gerar ou revisar partes estreitas; ferramentas decidem propriedades executáveis.
Aceite proposto: Detectar defeitos deliberados sem depender do texto de autoavaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

USO AVANÇADO — Resposta com política e fatos
Cenário: Uma explicação combina regras e dados externos.
Estratégia: Use verificador formal para a política e fontes para os fatos. Não deixe a aprovação de uma camada legitimar alegações que ela não examinou.
Papel do modelo pequeno: Um 8–14B pode redigir a resposta e organizar evidências com limites explícitos.
Aceite proposto: Cada afirmação relevante deve ter suporte apropriado ao seu tipo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Dividir trabalho por critérios verificáveis é mais concreto que pedir ao mesmo modelo para 'ser crítico'.
8–14B: Modelos intermediários podem revisar contexto maior, mas dependências precisam continuar visíveis.
15–30B: Um 15–30B como juiz não substitui referência independente nem garante resistência a persuasão.
Requisitos de treino/runtime: Arquitetura de verificação em runtime; independência é propriedade das evidências e métodos, não do nome do agente.
Não aplicar quando: Não tratar consenso entre revisores ou troca de marca de modelo como prova automática de independência.

## T200:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: CodeCourt separa propriedades de aceitação do agente que fez a limpeza.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: A detecção exige evidência específica, mas o oráculo continua limitado ao comportamento modelado.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Validação separada da geração e revisão humana fornecem sinais adicionais, sem independência estatística demonstrada.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4B-C022 — Amazon Web Services / Bedrock Automated Reasoning checks
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação descreve uma funcionalidade disponível de verificação por raciocínio automatizado para respostas em linguagem natural vinculadas a políticas.
Mecanismo documentado: Políticas são expressas formalmente e a tradução de texto para afirmações é analisada. O recurso é de detecção e possui restrições de idioma e resposta completa.
Correspondência com esta base: A aceitação é sustentada por um verificador externo dentro do escopo da política.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para redigir respostas e um verificador externo para políticas formalizáveis, encaminhando traduções ambíguas para revisão.
Limite: Disponibilidade não comprova adoção específica. Validade em uma política não garante verdade externa, atualização dos fatos ou correção da tradução de linguagem natural.
Fontes: V4B-S027.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Estudo humano confronta os julgamentos, mas não demonstra independência causal de todo erro.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q019.

## T200:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T200 → T190 [complements]
Como combinar: AutoClean usa avaliações por propriedade para controlar o fluxo de correção e revisão.
Interface: Artefato e relatórios de critérios.
Condição: Critérios ligados à revisão exata.
Aceite proposto: Medir falhas e discordâncias antes da liberação.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T200 → T195 [complements]
Como combinar: Execução oferece um método diferente de julgamento textual.
Interface: Contrato, testes e ambiente.
Condição: Oráculo não replica cegamente o erro do gerador.
Aceite proposto: Usar casos adversos e mutações conhecidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S019, C-S048, V4C-S009, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não fornecer a conclusão desejada como parte do critério de avaliação.
- Registrar lacunas de cobertura mesmo quando todos os critérios executados passam.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Verificação independente pode tornar uma solução pequena mais confiável em propriedades observáveis. A comparação com fronteira deve considerar falhas não cobertas e custo de toda a checagem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T186, T190, T195

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S044 — Chain-of-Verification Reduces Hallucination in Large Language Models

[https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rascunho, perguntas de checagem, respostas independentes e revisão final compõem CoVe.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# P012 — Verification Engine / Verification Controller

**Nome canônico:** Verification Engine / Verification Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de verificação de resultados; controlador proposto de verificação

## P012:C01 — conceito

Verification Engine / Verification Controller é um nome editorial proposto para verificar um resultado concreto antes de aceitá-lo no fluxo. Reuniria verificadores adequados ao artefato: schema, evidência documental, execução e regras de domínio. As fontes fundamentam essas classes de teste; não comprovam um componente LAI existente nem um verificador universal capaz de demonstrar qualquer alegação.

Como funciona:
- Receber candidato, contrato de aceitação, versão das entradas e evidências necessárias à decisão.
- Aplicar verificações estruturais e semânticas separadas; executar testes quando houver um ambiente e um oráculo apropriados.
- Devolver aprovado, reprovado ou inconclusivo, com motivos, evidências e limites do que foi verificado.

## P012:C02 — aplicacao

Quando usar:
- Respostas factuais com fontes, patches de código, chamadas estruturadas e artefatos com critérios de correção definidos.

Quando não usar:
- Para declarar correto um resultado apenas porque outro modelo concordou ou porque o JSON passou na validação.

Implementação proposta:
- Proposta: selecionar verificadores por tipo de saída e registrar versões dos testes, dados e ferramentas utilizados.
- Separar o produtor do candidato dos critérios de avaliação; quando possível, usar casos que não tenham sido vistos durante sua construção.
- Quando faltar uma fonte ou um teste não puder executar, marcar a dimensão como inconclusiva em vez de fabricar aprovação.

Aplicação LAI proposta:
Proposta LAI: verificar saídas do P011 e alimentar escalonamento de P010, anexando um recibo de verificação ao artefato avaliado.

## P012:C03 — riscos_validacao

Armadilhas:
- Testes gerados a partir da mesma implementação podem reproduzir seu erro e passar sem verificar o requisito.
- Uma resposta pode ser estruturalmente válida e conter fatos falsos ou referências inexistentes.
- Aprovação parcial não deve ser apresentada como cobertura integral de todos os requisitos.

Métricas sugeridas:
- Falsas aceitações e rejeições em conjunto rotulado, cobertura de requisitos e frequência de resultados inconclusivos.

Testes propostos:
- Aceite proposto: fornecer JSON válido com um ID inexistente e exigir falha na verificação semântica.
- Introduzir um defeito conhecido e um teste indisponível; o relatório deve separar reprovação comprovada de dimensão não avaliada.

## P012:C04 — perguntas_proveniencia

Pergunta: Validar schema confirma a verdade do conteúdo?
Resposta: Não. Schema verifica restrições estruturais; existência, veracidade e cumprimento do requisito exigem verificadores adicionais.

Pergunta: O que fazer quando o ambiente de teste falha?
Resposta: Registrar que a verificação não foi concluída nessa dimensão; falha do teste não é evidência suficiente de aprovação ou defeito do artefato.

Pergunta: Uma aprovação pode ser reutilizada após editar o arquivo?
Resposta: Somente se o contrato provar equivalência relevante; por padrão a mudança exige nova verificação.

Pergunta: Como representar falta de evidência?
Resposta: Use estado não verificável e liste a lacuna, sem converter ausência de falha em aprovação.

Escopo das fontes:
Fontes apoiam verificadores e avaliação; agregação, estados e integração LAI são propostas editoriais.

## P012:C05 — mecanismo_avancado

Verification Engine / Verification Controller propõe produzir decisões acompanhadas de evidência, distinguindo aprovado, reprovado e não verificável. Cada verificação deve identificar o artefato exato, idealmente por hash, o critério, a versão do verificador e o resultado. Validar um objeto JSON só cobre as regras expressas pelo schema; não comprova execução de uma ação nem verdade factual. Verificadores independentes precisam reduzir dependência de premissas compartilhadas, não apenas repetir a mesma pergunta.

Condição de contorno:
Um verificador pode ter falsos positivos e negativos. Quando depende de modelo, sua concordância com o gerador não é prova suficiente de correção.

Contrato proposto:
- Entradas: Artefato identificado, critérios de aceite, evidências autorizadas, ambiente de teste e orçamento de verificação.
- Saídas: Decisão por critério, evidência reproduzível, lacunas e motivos de insuficiência ou rejeição.
- Estado: Versões de verificadores, resultados anteriores por hash e dependências usadas para avaliar o artefato.
- Invariante: Qualquer alteração no artefato ou critério invalida a aprovação que se referia à versão anterior.

Compromissos de projeto:
- Verificação por execução pode ser forte para propriedades testáveis, mas depende da cobertura e do ambiente.
- Múltiplos verificadores aumentam custo; correlação entre seus erros pode limitar o ganho real.

## P012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: validar um artefato, modificá-lo e tentar reutilizar o laudo antigo; exigir invalidação. Incluir saída com schema válido e regra de negócio violada para confirmar separação das verificações.

Plano de avaliação proposto:
Comparar verificação estrutural, testes executáveis e avaliação semântica em conjunto com defeitos conhecidos. Medir falsos aceites, rejeições indevidas, custo e cobertura por critério. Reservar casos que não orientaram a construção dos verificadores.

Comparações:
- T197 (complements): JSON Schema cobre uma parte estrutural do contrato.
- T200 (complements): Verificação independente pode reduzir erros compartilhados quando usa evidência distinta.

Afirmação rastreável:
JSON Schema define validação estrutural; estudos de avaliação de código mostram a necessidade de testes discriminativos.
Suporte: related; fontes: C-S049, C-S048
Limite: A composição de verificadores e o vínculo por hash são propostas de engenharia, não resultados experimentais apresentados aqui.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P012:C07 — estrategia_3_30b

NOVA CAMADA v4 — Avança além de cobertura, hashes e independência já tratados na v3: propõe cascatas de verificação por risco, auditoria amostral das respostas aceitas e testes contra exploração do próprio verificador.

Cascata com abstenção calibrada
Proposta: ordenar verificadores por custo e poder discriminativo medidos no domínio. Um teste barato pode reprovar cedo; sua aprovação não encerra automaticamente casos de alto risco. Calibrar limiares numa divisão de desenvolvimento e congelá-los antes da avaliação final. Medir curva de cobertura versus erro entre aceitos, incluindo o custo dos verificadores adicionais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

Auditoria depois do aceite
Revisar uma amostra dos itens que passaram, incluindo respostas de alta confiança. Amostrar apenas rejeições deixa os falsos aceites invisíveis. Se erros raros forem superamostrados, guardar probabilidades de inclusão e reportar estratos separadamente ou ponderar a estimativa; não apresentar a amostra enriquecida como frequência natural do tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

Exploração do juiz e testes discriminativos
Um gerador ajustado repetidamente ao mesmo juiz pode melhorar a pontuação sem melhorar o requisito. Manter testes finais fora do loop de ajuste e introduzir negativos conhecidos e transformações metamórficas cuja invariância seja justificada pelo domínio. Mutantes equivalentes ou transformações inválidas devem ser excluídos antes de julgar a qualidade do verificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

USO AVANÇADO — Leitor pequeno com escalada seletiva
Cenário: Grande volume de respostas factuais permite auditoria humana limitada.
Estratégia: Executar checagem barata, escalar classes difíceis e auditar aleatoriamente parte dos aceitos; revisar política apenas fora da avaliação congelada.
Papel do modelo pequeno: 3–14B gera ou classifica alegações; aceitação depende da política calibrada, não de autoconfiança verbal.
Aceite proposto: Estimar falsos aceites por classe e custo por resultado correto; publicar cobertura e quantidade enviada à revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

USO AVANÇADO — Código que aprende a passar no juiz
Cenário: Repetidos reparos usam retorno de testes conhecidos e podem explorar lacunas.
Estratégia: Separar feedback de desenvolvimento e testes finais; usar entradas metamórficas válidas e defeitos semânticos rotulados para medir discriminação.
Papel do modelo pequeno: Modelo pequeno propõe candidatos; um executor compara propriedades independentes da pontuação narrativa.
Aceite proposto: Detectar defeitos inseridos sem reprovar transformações equivalentes; congelar avaliação após escolhas de hiperparâmetros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: primeiro estágio barato quando sua taxa de falsos aceites estiver medida; abstenção deve ser permitida.
8–14B: 8–14B: juiz especializado de evidência em domínio estreito, sujeito a auditoria de exemplos aceitos.
15–30B: 15–30B: estágio adicional para classes difíceis apenas se o ganho discriminativo compensar custo e correlação.
Requisitos de treino/runtime: Exige rótulos independentes, política versionada, amostragem conhecida e avaliação separada do ajuste.
Não aplicar quando: Não otimizar indefinidamente no mesmo juiz ou tratar taxa de aprovação como qualidade verdadeira.

## P012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Compilação e testes exemplificam critérios de aceite.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Rubricas de avaliação ilustram verificações propostas, não o produto editorial LAI.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Validação vinculada à revisão e ao responsável inspira o gate editorial.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: A cadeia de verificações exemplifica o componente editorial.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Gates verificáveis inspiram o componente editorial.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Critérios de gate ilustram um verificador editorial.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: O gate de propriedades inspira o componente proposto, sem demonstrar um produto LAI.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P012 é proposta. AutoClean, Tricorder e reparadores industriais mostram mecanismos delimitados; não confirmam um verificador universal ou produto LAI.
Consultas registradas: V4C-Q005, V4C-Q007, V4C-Q011.

## P012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P012 → T198 [complements]
Como combinar: Usar calibração empírica para definir quando aceitar, verificar novamente ou abster-se.
Interface: Score, classe da tarefa, versão da calibração e rótulos externos.
Condição: Há dados representativos suficientes para avaliar erro entre aceitos.
Aceite proposto: Curvas por classe mostram cobertura e erro; limiares não são escolhidos no conjunto final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, C-S050, V4C-S009, C-S049. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P012 → T205 [complements]
Como combinar: Aplicar equivalências justificadas como testes metamórficos do candidato e do juiz.
Interface: Transformação, precondições e propriedade que deve permanecer.
Condição: O domínio oferece relações semânticas conhecidas.
Aceite proposto: O sistema distingue violações reais de mudanças equivalentes sem depender de igualdade textual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, C-S050, V4C-S009, C-S049. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar ausência de erro numa amostra pequena como risco zero.
- Não somar votos correlacionados como se fossem ensaios independentes.
- Não esconder timeouts e abstinências ao calcular custo e cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar candidato 3–30B e baseline na mesma política, depois ablar a cascata. Auditar falsos aceites também na rota de fronteira; medir qualidade observada e incerteza sem chamar maior aprovação de maior inteligência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T195, T197, T200, T205, T206, P010, P011, P016

## Fontes primárias associadas

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

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

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

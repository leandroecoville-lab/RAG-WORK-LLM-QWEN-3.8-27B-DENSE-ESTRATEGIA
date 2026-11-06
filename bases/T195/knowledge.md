# T195 — Verificação baseada em execução

**Nome canônico:** Verificação Baseada em Execução  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T195  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execution-based verification; Verificação Baseada em Execução

## T195:C01 — conceito

Avaliação de uma proposta por executá-la em ambiente controlado e observar efeitos, saídas ou testes. É especialmente útil para código, consultas e transformações de dados. Passar em testes fornece evidência limitada à cobertura e ao ambiente, sem provar ausência de todos os defeitos.

Como funciona:
- Converter requisitos em entradas, invariantes e resultados esperados.
- Executar candidato em ambiente reproduzível com recursos limitados.
- Comparar comportamento observado e preservar logs ou artefatos de evidência.

## T195:C02 — aplicacao

Quando usar:
- Código ou transformação pode ser testado sem afetar produção.
- Há propriedade objetiva que o resultado deve cumprir.

Quando não usar:
- Executar conteúdo não confiável com acesso irrestrito a segredos ou sistemas reais.

Implementação proposta:
- Isolar ambiente e controlar rede, tempo e recursos necessários.
- Separar testes públicos de testes reservados relevantes.
- Registrar versão do código, dependências e dados usados.

Aplicação LAI proposta:
Proposta: a Helena sustentar declarações de funcionamento com comandos, resultados e testes pertinentes, separando validação local de operação real.

## T195:C03 — riscos_validacao

Armadilhas:
- Teste superficial pode aprovar solução incorreta.
- Ambiente de teste diferente do alvo pode esconder falha de integração.

Métricas sugeridas:
- Cobertura funcional relevante e taxa de falso aceite.
- Reprodutibilidade da execução e regressões encontradas.

Testes propostos:
- Introduzir mutações conhecidas que violam requisitos e conferir se testes falham.
- Reexecutar artefato em ambiente limpo para verificar dependências não declaradas.

## T195:C04 — perguntas_proveniencia

Pergunta: Passar em todos os testes prova perfeição?
Resposta: Não. Prova apenas comportamento nos casos e propriedades cobertos.

Pergunta: Só serve para código?
Resposta: Não. Pode verificar cálculos, schemas, arquivos e efeitos de workflows controlados.

Pergunta: Um exit code zero prova sucesso?
Resposta: Somente se o programa e o harness definem esse código de forma confiável e os critérios necessários foram realmente executados.

Pergunta: Como testar o próprio verificador?
Resposta: Use casos com resultados conhecidos, mutações que deveriam falhar e falhas de infraestrutura deliberadas para conferir a classificação dos resultados.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T195:C05 — mecanismo_avancado

A execução verifica uma relação entre artefato, entradas, ambiente e oráculo. Se o oráculo contém o mesmo erro do gerador, passar nos testes oferece falsa segurança. É preciso distinguir falha da proposta, falha da infraestrutura e caso não coberto. Para código, entradas de fronteira, efeitos laterais e limites de recursos fazem parte do comportamento; retorno correto em exemplos comuns não demonstra equivalência completa.

Condição de contorno:
Um conjunto finito de testes geralmente refuta defeitos encontrados, mas não prova correção para todas as entradas possíveis.

Contrato proposto:
- Entradas: Artefato identificado, ambiente controlado, casos, resultados esperados e limites de execução.
- Saídas: Observações reproduzíveis com estado aprovado, reprovado ou inconclusivo por critério.
- Estado: Versões de dependências, entradas, logs e identidade exata do artefato.
- Invariante: Erro do executor ou timeout nunca é convertido silenciosamente em teste aprovado.

Compromissos de projeto:
- Mais casos ampliam cobertura e tempo de avaliação.
- Ambiente isolado melhora controle e pode diferir das condições reais de implantação.

## T195:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar implementação correta nos exemplos originais, mas errada em entrada vazia, overflow ou repetição. Acrescentar casos independentes e exigir que o verificador detecte a falha.

Plano de avaliação proposto:
Plano proposto: comparar suíte inicial e ampliada com defeitos conhecidos e versões corretas. Medir falsos aceites, falsos alarmes, cobertura relevante e custo; reportar explicitamente domínio testado e ambiente, sem extrapolar para prova universal.

Comparações:
- T205 (complements): Comparação diferencial executa duas versões para investigar se preservam o comportamento especificado.

Afirmação rastreável:
EvalPlus ampliou casos de teste e identificou programas incorretos que passavam em suítes anteriores.
Suporte: direct; fontes: C-S048
Limite: A evidência mostra insuficiência de certas suítes, não que expansão automática garanta cobertura completa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T195:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu execução, ambiente e oráculo. Esta camada trata qualidade dos próprios testes, cobertura de efeitos e desenho de um executor que produz evidência reproduzível para seleção ou reparo.

Testar o verificador
Uma suíte que sempre passa pode estar vazia, desabilitada ou incapaz de detectar o defeito relevante. Use alterações deliberadas e mutações plausíveis para verificar sensibilidade. ACH documenta geração orientada por mutações; matar um mutante demonstra discriminação daquele comportamento, sem provar cobertura de todos os defeitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

Efeitos observáveis
Além de retorno, registre arquivos alterados, chamadas externas, recursos consumidos e exceções quando fazem parte do contrato. Um teste pode aprovar um valor enquanto a implementação modifica dados indevidamente. Limites de tempo e memória devem produzir estado inconclusivo ou reprovado conforme a regra, nunca sucesso por ausência de saída.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

Ambiente reproduzível
Fixe dependências, entradas e versão do artefato; preserve logs suficientes para reproduzir falhas. Isole execução de propostas de ambientes com efeitos reais não autorizados. Resultados em um simulador só sustentam o que ele modela; diferenças de integração precisam de checagem específica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

USO AVANÇADO — Geração de testes úteis
Cenário: Um modelo propõe ampliar uma suíte existente.
Estratégia: Exija que testes executem de forma estável e detectem uma alteração relevante. TestGen-LLM relata filtros industriais de compilação, execução e cobertura; preserve limites desses critérios.
Papel do modelo pequeno: Um 3–7B pode propor testes locais quando recebe contrato e exemplos.
Aceite proposto: Medir defeitos detectados e testes frágeis, não apenas linhas cobertas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

USO AVANÇADO — Busca de algoritmo
Cenário: Há muitas propostas com custo ou comportamento mensurável.
Estratégia: Execute em entradas representativas e adversas, filtre incorretas e compare desempenho somente entre válidas. AlphaEvolve é um caso de busca com avaliadores, em configurações próprias.
Papel do modelo pequeno: Um 8–14B pode explorar variantes pequenas dentro de um domínio executável.
Aceite proposto: Aceitar melhoria reproduzível sem regressão nos observáveis definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Critérios estreitos e ambientes rápidos tornam tentativa e verificação economicamente plausíveis.
8–14B: A dificuldade de produzir candidato correto e a qualidade do oráculo continuam limitantes.
15–30B: Modelos maiores podem gerar mais complexidade; orçamento de execução precisa acompanhar essa complexidade.
Requisitos de treino/runtime: Runtime de execução e avaliação; pode alimentar treino depois, mas executar testes não atualiza pesos.
Não aplicar quando: Não chamar cobertura alta de prova de correção nem executar código gerado em produção por mera aprovação textual.

## T195:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 3. Lacuna: 7. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 3. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Execução e avaliadores de código produzem sinais verificáveis.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Testes executáveis validam candidatos.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Testes são executados para aceitar candidatos.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Compilação e testes contribuem para validação do resultado.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T195:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T195 → T190 [feeds]
Como combinar: AutoClean usa resultados de verificações para controlar progressão de correções.
Interface: Revisão e evidência de execução.
Condição: Resultados correspondem à versão final.
Aceite proposto: Injetar falhas e verificar bloqueio ou reparo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T195 → T205 [complements]
Como combinar: Comparação diferencial e propriedades metamórficas ampliam testes quando não há resposta única.
Interface: Entradas, referência e observáveis.
Condição: Normalização não apaga diferenças relevantes.
Aceite proposto: Gerar contraexemplos e reduzi-los para reprodução.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Confirmar que os testes foram efetivamente descobertos e executados.
- Separar defeito do candidato de indisponibilidade do ambiente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Execução pode tornar modelos pequenos úteis em tarefas com bons oráculos. A comparação com fronteira deve incluir custo de candidatos descartados e falhas que a suíte não observa.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T189, T190, T200, T205

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

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

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

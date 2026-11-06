# T205 — Semantic Equivalence Testing

**Nome canônico:** Semantic Equivalence Testing  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T205  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** teste de equivalência semântica

## T205:C01 — conceito

Verificação de que duas representações preservam o comportamento ou significado relevante para uma tarefa. O critério depende do domínio: programas podem ser comparados por execução, objetos por regras normalizadas e textos por alegações preservadas. Similaridade de embeddings sozinha não prova equivalência.

Como funciona:
- Definir quais propriedades precisam permanecer iguais.
- Aplicar normalização admissível e comparação adequada ao domínio.
- Registrar divergências e limites da cobertura do teste.

## T205:C02 — aplicacao

Quando usar:
- Comparação entre versões de prompt, resumo, código ou schema.
- Validação de compactação de contexto e mudanças de formato.

Quando não usar:
- Declarar equivalência geral de programas arbitrários com base em poucos exemplos.

Implementação proposta:
- Construir casos positivos equivalentes e negativos próximos.
- Usar execução diferencial para código e checagem de alegações para textos.
- Separar diferenças cosméticas de mudanças com efeito observável.

Aplicação LAI proposta:
Proposta: avaliar se resumos e procedimentos da Helena preservam restrições, identificadores e condições essenciais antes de substituir versões anteriores.

## T205:C03 — riscos_validacao

Armadilhas:
- Paráfrase pode inverter negação ou prazo mantendo alta similaridade.
- Casos de teste finitos não cobrem todos os comportamentos possíveis.

Métricas sugeridas:
- Falsas equivalências e falsas divergências.
- Cobertura de propriedades e taxa de regressão detectada.

Testes propostos:
- Comparar frases que diferem apenas por negação e exigir rejeição.
- Testar programas com mesmo resultado comum, mas divergentes em condição de borda.

## T205:C04 — perguntas_proveniencia

Pergunta: Embeddings provam que dois textos dizem a mesma coisa?
Resposta: Não. Proximidade semântica pode esconder contradição.

Pergunta: Teste de equivalência prova todos os casos?
Resposta: Só se existir prova formal apropriada; testes comuns têm cobertura limitada.

Pergunta: Similaridade de embeddings prova equivalência textual?
Resposta: Não. Textos semanticamente próximos podem inverter uma condição, quantidade ou negação decisiva.

Pergunta: Round-trip perfeito prova um codec correto?
Resposta: Não sozinho. Encoder e decoder podem compartilhar o mesmo erro; compare também com especificação ou implementação independente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T205:C05 — mecanismo_avancado

Equivalência precisa declarar quais observáveis importam: valor retornado, efeitos laterais, exceções, ordem, precisão ou tempo. Duas funções podem devolver o mesmo resultado e modificar entradas de modo diferente. Comparação diferencial usa uma referência independente; propriedades metamórficas verificam relações entre entradas e saídas quando não existe resposta completa conhecida. A normalização deve preservar distinções relevantes, como unidades, ordem ou multiplicidade.

Condição de contorno:
Testes amostrais podem encontrar contraexemplos, mas ausência deles não prova equivalência para todo o domínio.

Contrato proposto:
- Entradas: Duas representações, domínio válido, observáveis e tolerâncias justificadas.
- Saídas: Contraexemplos reproduzíveis ou evidência limitada de equivalência nos casos examinados.
- Estado: Geradores de entradas, referências e regras de normalização.
- Invariante: Nenhuma diferença relevante é apagada pela normalização antes de ser avaliada.

Compromissos de projeto:
- Comparação estrita detecta diferenças e pode rejeitar variações aceitáveis.
- Tolerâncias amplas acomodam precisão finita e podem esconder erros significativos.

## T205:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar implementações iguais em listas sem duplicatas, mas diferentes quando há repetição, NaN ou mutação da entrada. Esperar contraexemplo no domínio realmente permitido.

Plano de avaliação proposto:
Plano proposto: combinar casos de fronteira, geração por propriedades e comparação diferencial. Medir defeitos detectados, reprodutibilidade e cobertura das classes de entrada; aceitar equivalência somente no escopo declarado, preservando casos descobertos para regressão.

Comparações:
- T195 (complements): Execução fornece observações para comparar comportamento entre versões, dentro do domínio declarado.

Afirmação rastreável:
A documentação Hypothesis apresenta testes por propriedades e comparação de implementação otimizada com referência, usando entradas geradas.
Suporte: direct; fontes: V3B-S022
Limite: O mecanismo explora entradas; uma prova geral exigiria argumento ou ferramenta formal compatível com a propriedade.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T205:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu observáveis e propriedades metamórficas. A nova camada considera domínio de equivalência, geração de contraexemplos e uso responsável de evidência empírica versus prova formal.

Domínio explícito
Declare entradas válidas, estados iniciais e tolerâncias. Duas implementações podem coincidir em números pequenos e divergir em overflow, Unicode, valores vazios ou concorrência. Excluir uma classe de entradas só é legítimo se o contrato também a exclui; não estreite o domínio depois de observar uma falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

Contraexemplo útil
Quando houver divergência, reduza a entrada preservando o defeito para facilitar correção. Mantenha sementes e ambiente para reprodução. Testes por propriedades e metamorfismo são úteis quando não existe uma resposta completa para cada entrada, mas a própria propriedade pode estar errada ou ser fraca.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

Força da evidência
Passar uma suíte finita oferece evidência limitada; prova formal tem alcance definido pelo modelo e premissas. AlphaEvolve relata verificação de funcionalidade em uma alteração de circuito, enquanto ACH usa mutações para testar detecção. Não use esses exemplos para declarar equivalência universal de qualquer patch gerado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

USO AVANÇADO — Refatoração automatizada
Cenário: Um modelo altera estrutura mantendo comportamento.
Estratégia: Defina retornos, efeitos, exceções e ordenação relevantes; compare com referência e adicione propriedades. Teste entradas de fronteira e mudanças concorrentes quando aplicáveis.
Papel do modelo pequeno: Um 3–7B pode propor refatorações locais, com aceitação externa.
Aceite proposto: Nenhuma divergência no domínio testado, com limites de cobertura registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

USO AVANÇADO — Normalização de respostas
Cenário: Várias representações podem expressar o mesmo resultado.
Estratégia: Use parser de domínio para números, unidades ou estruturas; preserve distinções como ordem e multiplicidade quando importam. Encaminhe ambiguidades em vez de forçar equivalência.
Papel do modelo pequeno: Um 8–14B pode produzir candidatos, mas a regra de equivalência deve ser auditável.
Aceite proposto: Detectar exemplos aparentemente iguais com semântica diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Mudanças pequenas e contratos claros tornam verificação mais viável.
8–14B: Para transformações maiores, amplie cobertura e revise premissas do normalizador.
15–30B: Um 15–30B não dispensa equivalência; pode produzir alterações mais complexas que exigem verificadores melhores.
Requisitos de treino/runtime: Ferramentas de teste, referências ou métodos formais conforme o domínio. Não exige treinamento do gerador.
Não aplicar quando: Não apagar diferenças relevantes com arredondamento, ordenação ou remoção de campos apenas para fazer testes passarem.

## T205:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Há verificação de funcionalidade e desempenho, sem equivaler a qualquer receita de treinamento por recompensas.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T205:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T205 → T195 [complements]
Como combinar: Execução fornece observações para comparação diferencial.
Interface: Artefatos, entradas e efeitos registrados.
Condição: Ambientes comparáveis e referência confiável.
Aceite proposto: Reproduzir e minimizar divergências.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T205 → T188 [feeds]
Como combinar: Agregação de respostas precisa agrupar somente equivalentes semanticamente.
Interface: Forma canônica e regras de unidade.
Condição: Normalizador validado no domínio.
Aceite proposto: Testar frações, unidades e respostas condicionais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar os casos que revelaram divergência como regressões de desenvolvimento.
- Distinguir ausência de contraexemplo encontrado de prova completa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare transformações corretas e custo de verificação. Equivalência de uma função ou resposta não demonstra competência geral do modelo que a produziu.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T019, T043, T188, T195

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S022 — Introduction to Hypothesis

[https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Testes baseados em propriedades, geração de entradas de domínio e comparação diferencial/round-trip.

Limite: Amostragem de entradas e contraexemplos não constituem prova geral de equivalência.

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

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

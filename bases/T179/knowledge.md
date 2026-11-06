# T179 — Context Distillation Paramétrica

**Nome canônico:** Context Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T179  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** destilação paramétrica de contexto

## T179:C01 — conceito

Treinamento para reproduzir comportamentos obtidos com contexto privilegiado sem precisar fornecer todo esse contexto em inferência. Instruções ou exemplos condicionam o professor; o aluno aprende a tarefa com entrada reduzida. Isso modifica parâmetros e é distinto de resumir texto ou guardá-lo em memória externa.

Como funciona:
- Executar professor com contexto extenso e entradas representativas.
- Associar entradas reduzidas às respostas verificadas produzidas.
- Ajustar o aluno e avaliar sua execução sem o contexto privilegiado.

## T179:C02 — aplicacao

Quando usar:
- Regras de comportamento estáveis e repetidas em grande volume.
- Prompt longo contém habilidades que podem ser aprendidas por exemplos.

Quando não usar:
- Fatos mutáveis, permissões obrigatórias ou registros exatos que precisam de atualização imediata.

Implementação proposta:
- Definir claramente o que será removido do prompt após treinamento.
- Curar exemplos que cubram exceções e conflitos das instruções.
- Avaliar retenção e regressão sempre que o contexto original mudar.

Aplicação LAI proposta:
Proposta: destilar habilidades estáveis da Helena depois que memória externa e avaliações já estiverem funcionando; manter dados atuais recuperáveis.

## T179:C03 — riscos_validacao

Armadilhas:
- Desempenho pode depender de instruções que o treino não internalizou.
- Mudar política depois exige adaptação ou controles explícitos fora dos pesos.

Métricas sugeridas:
- Qualidade com prompt completo versus aluno com prompt reduzido.
- Tokens economizados e custo total do ciclo de treinamento e manutenção.

Testes propostos:
- Usar casos inéditos que dependem de partes distintas do contexto original.
- Alterar uma regra e verificar se comportamento antigo permanece no adaptador.

## T179:C04 — perguntas_proveniencia

Pergunta: É uma forma de resumo?
Resposta: Não no sentido textual: aqui a compressão pretendida ocorre por aprendizado paramétrico.

Pergunta: O professor precisa ser outra LLM?
Resposta: Não. O mesmo modelo com contexto adicional pode gerar supervisão.

Pergunta: Destilar é guardar uma cópia recuperável do contexto?
Resposta: Não. O efeito fica distribuído nos parâmetros e não oferece consulta literal ou proveniência automática.

Pergunta: Quando manter RAG junto?
Resposta: Quando fatos precisam de atualização, auditoria ou acesso condicionado à consulta, além do comportamento estável aprendido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T179:C05 — mecanismo_avancado

O professor recebe informação privilegiada C e entrada X, enquanto o aluno opera somente com X. Se a resposta depende de uma variável de C que muda entre consultas e não pode ser inferida de X, não há como garantir reprodução exata em todos os casos. A destilação pode internalizar regularidades e procedimentos, mas não cria um canal para fatos futuros ou mudanças que nunca chegaram aos pesos.

Condição de contorno:
Contexto variável indispensável precisa continuar disponível por entrada, ferramenta ou recuperação; removê-lo pode tornar a tarefa subdeterminada.

Contrato proposto:
- Entradas: Pares de entrada reduzida e contexto privilegiado, saídas revisadas e distribuição de implantação.
- Saídas: Aluno capaz de executar o comportamento aprendido com o contexto reduzido declarado.
- Estado: Versões de contexto, pesos e exemplos usados na transferência.
- Invariante: A avaliação retira do aluno exatamente a informação que será ausente na implantação.

Compromissos de projeto:
- Contexto menor reduz custo por consulta e aumenta dependência da atualização dos pesos.
- Comprimir comportamento dificulta localizar ou remover uma regra específica posteriormente.

## T179:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter X igual e variar em C um fato decisivo, produzindo respostas corretas diferentes. Esperar identificação da ambiguidade, em vez de prometer que o aluno sem C reproduzirá ambas.

Plano de avaliação proposto:
Plano proposto: comparar professor com contexto, aluno base sem contexto e aluno destilado. Separar tarefas de procedimento estável e fatos variáveis; medir generalização e custo, aceitando apenas capacidades demonstradas sem vazamento do contexto privilegiado.

Comparações:
- T181 (distinct_from): AMD fornece memórias externas ao aluno; esta variante modifica parâmetros para reduzir contexto explícito.

Afirmação rastreável:
Learning by Distilling Context treina o aluno com entrada da tarefa sem as instruções ou scratchpad usados para produzir a supervisão.
Suporte: direct; fontes: C-S033
Limite: O estudo demonstra tarefas específicas; não prova compressão sem perda de informação arbitrária.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T179:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 estabeleceu o limite da informação privilegiada. Esta camada trata o que escolher para internalizar, como testar redução de dependência do contexto e como atualizar um comportamento que ficou nos pesos.

Decompor o contexto
Classifique o material do professor em procedimento estável, exemplos, fatos mutáveis e dados de acesso restrito. Internalizar procedimentos pode reduzir instruções; fatos dinâmicos continuam precisando de entrada ou recuperação. Dados que variam por usuário não devem desaparecer sem um identificador autorizado que preserve a distinção entre casos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

Teste de informação removida
Compare professor com contexto, aluno sem contexto e aluno com um resumo mínimo. Use casos em que a informação omitida muda a resposta para revelar limites de identificabilidade. Se o aluno acerta apenas por correlações do dataset, uma troca de entidade ou de versão pode expor a dependência indevida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

Atualização e revogação
Depois de incorporar um comportamento nos pesos, editar o documento de origem não atualiza o modelo. Versione a relação entre contexto e checkpoint e defina quando retreinar ou voltar a fornecer instruções explícitas. Remover um arquivo do RAG também não demonstra remoção de informação internalizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

USO AVANÇADO — Procedimento estável de classificação
Cenário: Um manual extenso define categorias duráveis.
Estratégia: Produza exemplos contrastivos, incluindo fronteiras e exceções, e ajuste um aluno que recebe somente os campos variáveis. Mantenha a versão do manual no manifest e no teste.
Papel do modelo pequeno: Um 3–7B pode classificar casos estreitos sem reler o manual inteiro a cada pedido.
Aceite proposto: Avaliar casos novos e mudanças controladas de regra, com abstenção quando faltam dados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

USO AVANÇADO — Rotina de ferramentas
Cenário: O professor usa contexto com convenções de uma API.
Estratégia: Destile padrões estáveis, mas mantenha schema, versão e credenciais fora dos pesos. Teste execução contra a API atual e simule mudanças de contrato.
Papel do modelo pequeno: Um 8–14B pode aprender procedimento sem memorizar valores de sessão.
Aceite proposto: Medir sucesso executável e capacidade de reconhecer contrato incompatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize regras simples e estáveis, com exceções claramente testáveis.
8–14B: Procedimentos mais extensos podem ser estudados, mas não presuma retenção completa de um manual.
15–30B: Compare com recuperação do contexto: maior capacidade pode tornar desnecessário internalizar fatos difíceis de atualizar.
Requisitos de treino/runtime: Exige treinamento e pares que removam do aluno exatamente a informação ausente no uso real.
Não aplicar quando: Não destilar variáveis secretas ou futuras como se o aluno pudesse inferi-las sem um canal de entrada.

## T179:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: Receita de prompt distillation transfere comportamento condicionado por contexto.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## T179:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T179 → T180 [complements]
Como combinar: A decomposição do contexto identifica quais instruções do prompt podem virar comportamento.
Interface: Regras estáveis e parâmetros que permanecem explícitos.
Condição: Sem ambiguidade entre regimes de tarefa.
Aceite proposto: Testar mudanças de parâmetro que devem alterar a saída.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S033, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T179 → T009 [complements]
Como combinar: Recuperação mantém fatos variáveis fora dos pesos enquanto procedimentos são aprendidos.
Interface: Documento vigente e versão do comportamento.
Condição: Aluno distingue evidência atual de padrão aprendido.
Aceite proposto: Testar contradições entre memória paramétrica e documento atualizado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S033, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Avaliar por origem e tempo, evitando que exemplos quase iguais ocultem falta de informação.
- Não afirmar que redução de prompt preservou todos os detalhes sem testar as exceções.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare com fronteira recebendo a mesma informação disponível na implantação. O aluno pode executar uma rotina específica com menos contexto, mas não reproduzir informação privada que foi retirada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T069, T177, T178, T180

## Fontes primárias associadas

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

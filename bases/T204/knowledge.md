# T204 — Skills / Procedural Learning

**Nome canônico:** Skills / Procedural Learning  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T204  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** habilidades procedurais; aprendizagem procedural

## T204:C01 — conceito

Skills são pacotes reutilizáveis de instruções, recursos e eventualmente scripts para um procedimento. Aprendizagem procedural é o processo de transformar experiências verificadas em procedimentos aplicáveis. Criar um arquivo de skill não altera pesos nem comprova que o agente executará corretamente o procedimento.

Como funciona:
- Extrair uma tarefa recorrente e suas condições de aplicação.
- Empacotar objetivo, entradas, passos, saídas e referências.
- Descobrir e carregar o procedimento quando a missão corresponder ao seu escopo.

## T204:C02 — aplicacao

Quando usar:
- Procedimentos repetidos com contratos relativamente estáveis.
- Especialidades que devem ser acessíveis sem carregar todo material de início.

Quando não usar:
- Generalizar uma experiência isolada sem considerar condições que permitiram seu sucesso.

Implementação proposta:
- Definir gatilhos e limites de uso em metadados claros.
- Separar instrução principal de referências volumosas.
- Versionar scripts e validar exemplos representativos antes de promover a skill.

Aplicação LAI proposta:
Proposta: converter episódios comprovados da Helena em procedimentos recuperáveis, preservando evidências e condições antes de pensar em destilação paramétrica.

## T204:C03 — riscos_validacao

Armadilhas:
- Skill desatualizada pode orientar chamadas incompatíveis.
- Catálogo com descrições vagas impede descoberta e aumenta seleção incorreta.

Métricas sugeridas:
- Acerto de seleção e conclusão correta do procedimento.
- Economia de contexto e regressões por versão de skill.

Testes propostos:
- Apresentar tarefas dentro e fora do escopo e verificar seleção.
- Atualizar uma dependência e exigir revalidação dos exemplos afetados.

## T204:C04 — perguntas_proveniencia

Pergunta: Criar skill significa treinar GPT?
Resposta: Não no sentido de atualizar pesos; fornece instruções e ferramentas reutilizáveis.

Pergunta: Skill substitui RAG?
Resposta: Pode usar RAG para recuperar referências e exemplos necessários ao procedimento.

Pergunta: Uma skill é memória paramétrica?
Resposta: Não. É um artefato externo consumido durante execução; aprendizado de pesos seria outro mecanismo.

Pergunta: Como evitar regras frágeis?
Resposta: Documente pré-condições e parâmetros, teste variantes relevantes e preserve evidência dos limites encontrados em vez de transformar um exemplo em regra universal.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T204:C05 — mecanismo_avancado

Uma skill executável precisa separar condições de aplicação, instruções centrais e recursos carregados sob demanda. Metadados ajudam a selecionar o procedimento, mas não demonstram que seus scripts, caminhos e dependências estão válidos. Aprender um procedimento a partir de uma execução exige generalizar somente o que se repete, deixando parâmetros variáveis explícitos. Copiar a trajetória inteira pode cristalizar atalhos ou suposições locais.

Condição de contorno:
Um procedimento que funcionou uma vez pode depender de estado, permissões ou versões ausentes em outra tarefa.

Contrato proposto:
- Entradas: Experiência verificada, objetivo recorrente, pré-condições e recursos necessários.
- Saídas: Pacote de procedimento versionado e critérios para ativar ou interromper sua execução.
- Estado: Instruções, scripts, referências, exemplos e histórico de alterações.
- Invariante: Recursos necessários são carregados e validados antes da etapa que deles depende.

Compromissos de projeto:
- Carregamento progressivo reduz contexto inicial e exige referências confiáveis.
- Procedimentos específicos facilitam execução e podem generalizar mal fora de suas condições.

## T204:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ativar a skill com dependência ausente e com caso semelhante, mas fora do domínio declarado. Esperar diagnóstico de pré-condição ou não aplicação, sem improvisar uma execução supostamente equivalente.

Plano de avaliação proposto:
Plano proposto: comparar execução sem skill e com skill em tarefas novas da mesma classe e em casos fora dela. Medir sucesso verificado, chamadas, contexto e ativações indevidas; aprovar somente reutilização que preserve condições e critérios.

Comparações:
- T199 (complements): Avaliações podem justificar atualização da skill, mas o pacote precisa mudar de fato para alterar comportamento futuro.

Afirmação rastreável:
A especificação Agent Skills define SKILL.md com metadados/instruções e carregamento progressivo de recursos conforme necessidade.
Suporte: direct; fontes: V3B-S021
Limite: O formato organiza conteúdo; não treina pesos nem comprova que o procedimento está correto ou autorizado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T204:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu pacote e pré-condições. A nova camada aborda descoberta de habilidades, invalidação de recursos e aprendizado procedural que mantém argumentos variáveis e evidência de execução.

Seleção por contrato
Descrições de skills devem distinguir objetivo, pré-condições e resultado esperado. Similaridade textual pode recuperar um procedimento inadequado porque compartilha vocabulário. Antes de executar, verifique ambiente, versão e permissões; carregar uma skill é uma decisão de planejamento, não prova de que ela se aplica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

Recursos sob demanda
Mantenha instruções centrais curtas e carregue scripts ou referências quando a etapa exige. Isso reduz competição por contexto, mas a execução precisa confirmar que o recurso existe e corresponde à versão descrita. Um link antigo ou script quebrado invalida a habilidade mesmo que o texto continue convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

Generalização de trajetória
Converta uma execução bem-sucedida em procedimento somente depois de separar constantes, parâmetros e contingências. Inclua caminhos de falha e critérios de interrupção. AMD oferece pesquisa sobre memória procedural hierárquica; transferir seu padrão para uma skill é proposta de engenharia, não implantação comprovada do pacote LAI.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

USO AVANÇADO — Rotina técnica repetida
Cenário: O agente precisa executar uma sequência conhecida com variações.
Estratégia: Empacote passos, argumentos e verificações; teste em múltiplas instâncias e preserve evidências. Deixe o modelo selecionar e preencher parâmetros, enquanto scripts fazem operações determinísticas.
Papel do modelo pequeno: Um 3–7B pode executar uma rotina estreita com menos improvisação.
Aceite proposto: Medir sucesso em casos novos e detectar pré-condições ausentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

USO AVANÇADO — Acervo de procedimentos crescente
Cenário: Muitas skills competem pela atenção do agente.
Estratégia: Organize metadados por tarefa e ambiente, avalie recuperação e rejeite candidatos incompatíveis. Carregue apenas o trecho necessário e registre qual versão orientou a ação.
Papel do modelo pequeno: Um 8–14B pode coordenar subtarefas sem inserir todo o acervo no prompt.
Aceite proposto: Avaliar seleção correta, recurso carregado e resultado final separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Procedimentos curtos com scripts confiáveis reduzem exigência de planejamento aberto.
8–14B: Bibliotecas maiores exigem testes de seleção e conflitos entre skills.
15–30B: Um 15–30B pode compor rotinas, mas composição demanda novos testes de interfaces e estado.
Requisitos de treino/runtime: Memória procedural externa pode ser atualizada sem treinar pesos; aprendizagem paramétrica é outra rota.
Não aplicar quando: Não tratar uma trajetória copiada como procedimento universal nem texto da skill como prova de execução.

## T204:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: Memórias procedurais se relacionam a habilidades recuperáveis.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q023.

## T204:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T204 → T181 [complements]
Como combinar: Memórias hierárquicas podem informar criação e seleção de procedimentos.
Interface: Trajetória, pré-condições e resultados.
Condição: Generalização remove dados de sessão e preserva validade.
Aceite proposto: Testar aplicação em ambiente distinto e versão compatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S021, C-S052, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T204 → T206 [requires]
Como combinar: Verificação de processo confirma que etapas e recursos foram efetivamente usados.
Interface: Eventos, versão da skill e pós-condições.
Condição: Observabilidade cobre ações relevantes.
Aceite proposto: Comparar plano declarado com execução real.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S021, C-S052, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Suspender skills cujo recurso ou contrato mudou até revalidar.
- Não ocultar parâmetros variáveis em exemplos fixos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare execução de rotinas com fronteira usando as mesmas ferramentas. Uma biblioteca procedural pode ampliar utilidade especializada de um modelo pequeno, sem conferir compreensão geral de tarefas desconhecidas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T055, T071, T181

## Fontes primárias associadas

### C-S052 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills empacotam instruções e recursos carregados progressivamente.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S021 — Agent Skills Specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estrutura SKILL.md, metadados, recursos e carregamento progressivo.

Limite: Especificação de formato não prova correção do procedimento nem autorização universal de ferramentas.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

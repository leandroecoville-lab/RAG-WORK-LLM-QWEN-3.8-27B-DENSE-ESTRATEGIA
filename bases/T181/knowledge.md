# T181 — Agent Memory Distillation

**Nome canônico:** Agent Memory Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T181  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** AMD; destilação de memória de agentes

## T181:C01 — conceito

No trabalho de Kim, Kim e Hwang identificado como AMD, conhecimento de trajetórias bem-sucedidas de um agente professor é organizado em memórias de workflow, subtarefa e função. O aluno recupera essas memórias durante a execução, sem atualização dos pesos no método descrito.

Como funciona:
- Extrair estratégias, exemplos intermediários e convenções de chamada de trajetórias do professor.
- Fornecer memórias de workflow e subtarefa antes da execução.
- Recuperar memória de função quando surgirem erros de uso de ferramentas.

Nota de nomenclatura: Identificação confirmada em arXiv:2608.07169; não confundir com qualquer método chamado genericamente memory distillation.

## T181:C02 — aplicacao

Quando usar:
- Aluno tem dificuldade de produzir trajetórias próprias bem-sucedidas.
- Procedimentos podem ser representados em exemplos e guias recuperáveis.

Quando não usar:
- Assumir que memória de ferramenta antiga continua aplicável após mudança de API ou ambiente.

Implementação proposta:
- Conservar trajetória original, versão de ferramenta e evidência de sucesso.
- Separar memória procedural da verdade factual e da autorização de ação.
- Avaliar recuperação e transferência em tarefas não vistas pelo professor.

Aplicação LAI proposta:
Proposta: criar memória procedural da Helena a partir de missões comprovadas por modelos fortes e avaliar no modelo local antes de considerar treinamento.

## T181:C03 — riscos_validacao

Armadilhas:
- Procedimento do professor pode exigir capacidade que o aluno não possui.
- Memórias sem condições de aplicação podem induzir ações inadequadas.

Métricas sugeridas:
- Sucesso de uso de ferramentas com e sem memória.
- Ganho por granularidade de memória e custo de recuperação.

Testes propostos:
- Comparar aluno base, memória genérica e memória hierárquica no mesmo conjunto reservado.
- Mudar versão de função e testar invalidação de guias incompatíveis.

## T181:C04 — perguntas_proveniencia

Pergunta: AMD modifica os pesos do aluno?
Resposta: O trabalho identificado usa transferência por memória externa, sem treinamento do aluno.

Pergunta: Resultados em modelos pequenos provam ganho no meu Qwen?
Resposta: Não. Essa combinação precisa de avaliação própria.

Pergunta: Por que sucesso do professor não basta?
Resposta: Pode depender de ferramentas, contexto ou habilidades que o aluno não possui; condições de execução precisam acompanhar a memória.

Pergunta: AMD é necessariamente fine-tuning?
Resposta: Não no método identificado por esta ficha: trata-se de framework training-free que fornece memórias ao aluno.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T181:C05 — mecanismo_avancado

A separação entre memórias proativas e reativas cria pontos diferentes de falha. Estratégias e exemplos introduzidos no início podem enviesar todo o plano; convenções de função recuperadas apenas após erro ajudam a corrigir chamadas, mas podem não aparecer quando a ferramenta retorna sucesso estrutural com conteúdo semanticamente errado. A utilidade da trajetória do professor depende de o aluno conseguir executar o procedimento no ambiente atual.

Condição de contorno:
Uma memória extraída de sucesso antigo pode ficar inválida após mudanças na API, permissões ou semântica da ferramenta.

Contrato proposto:
- Entradas: Trajetórias bem-sucedidas com evidências, contratos de ferramentas e tarefa do aluno.
- Saídas: Memórias hierárquicas com origem e sugestões aplicáveis à execução atual.
- Estado: Versões de workflow, subtarefa, função e eventos que acionam recuperação.
- Invariante: A memória preserva condições de validade e não transforma uma trajetória em regra universal.

Compromissos de projeto:
- Memórias detalhadas aumentam orientação e consumo de contexto.
- Recuperação somente após falha poupa tokens e pode perder erros sem exceção explícita.

## T181:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar um parâmetro da ferramenta e fazer outra chamada retornar sucesso com efeito errado. Esperar detecção por contrato externo; observar se a memória reativa cobre apenas o primeiro caso.

Plano de avaliação proposto:
Plano proposto: comparar aluno sem memória, memórias próprias e hierarquia do professor em tarefas novas. Medir sucesso verificado, chamadas, recuperação e tokens; realizar ablações por nível e validar atualização após mudança do ambiente.

Comparações:
- T179 (distinct_from): No AMD identificado, transferência ocorre por memória externa, sem atualização de pesos.

Afirmação rastreável:
O paper AMD descreve workflow e subtarefa proativos, com memória de função recuperada reativamente após erros de chamada.
Suporte: direct; fontes: C-S035
Limite: O trabalho consultado consta como sob revisão; seus resultados não certificam generalização para ferramentas do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T181:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu memória proativa e reativa. Esta camada organiza a memória como artefato executável versionado, com seleção por pré-condições, avaliação de transferência e expiração de procedimentos.

Memória com pré-condições
Uma trajetória bem-sucedida só é reutilizável quando ferramentas, permissões e estado do problema são compatíveis. Extraia pré-condições e resultados observados junto ao procedimento. Memória de workflow orienta o plano; memória de função deve preservar argumentos, efeitos e erros conhecidos, sem transformar valores de uma sessão em constantes universais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

Recuperação antes do erro
Falha sintática é um gatilho fácil, mas uma ferramenta pode retornar sucesso com conteúdo inadequado. Acrescente verificações de pós-condição e divergência de estado para acionar memória reativa. O aluno deve poder rejeitar uma recomendação quando suas condições não se aplicam, em vez de segui-la como instrução absoluta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

Validade temporal
Mudanças de API e ambiente podem tornar memórias antigas nocivas. Versione fonte, data e contrato, e suspenda exemplos que falham em reexecução controlada. O projeto AMD apresenta pesquisa em agentes pequenos; isso não comprova funcionamento contínuo em produção nem elimina manutenção do acervo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

USO AVANÇADO — Agente em API especializada
Cenário: As falhas se concentram em convenções pouco intuitivas.
Estratégia: Colete trajetórias autorizadas com resultados verificáveis, extraia padrões de função e recupere somente os compatíveis com a versão atual. Teste erros que exigem abandonar a receita.
Papel do modelo pequeno: Um 3–7B pode receber instrução procedural concreta em vez de inferir tudo do nome da ferramenta.
Aceite proposto: Medir conclusão de tarefa e ações incorretas, incluindo casos novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

USO AVANÇADO — Workflow com muitas etapas
Cenário: O aluno se perde entre subtarefas recorrentes.
Estratégia: Recupere um esqueleto de workflow, depois detalhe apenas a etapa atual. Preserve estado real fora do texto e verifique cada transição relevante.
Papel do modelo pequeno: Um 8–14B pode usar memória hierárquica para reduzir carga de planejamento.
Aceite proposto: Avaliar execução completa, adaptação a desvios e custo de recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Memórias curtas e condicionais podem ajudar tarefas limitadas; excesso de exemplos compete pela janela.
8–14B: Explore hierarquia e seleção por etapa, evitando inserir todo o acervo em cada prompt.
15–30B: Compare benefício marginal com capacidade própria do 15–30B e custo de manter memórias.
Requisitos de treino/runtime: No método descrito, memória externa não exige necessariamente atualizar pesos; não confundir com destilação paramétrica.
Não aplicar quando: Não reaproveitar credenciais, caminhos ou dados de clientes contidos em trajetórias sem tratamento apropriado.

## T181:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: A referência trata de Agent Memory Distillation.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q023.

## T181:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T181 → T204 [complements]
Como combinar: Memórias de função podem virar habilidades com contrato de entrada, saída e versão.
Interface: Procedimento, pré-condições e pós-condições.
Condição: Execução atual satisfaz o contrato.
Aceite proposto: Reexecutar em casos novos e detectar incompatibilidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S035, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T181 → T195 [requires]
Como combinar: Ferramentas e testes verificam se a trajetória transferida realmente funcionou.
Interface: Resultados de execução e estado final.
Condição: Oráculo de sucesso independente da narrativa do agente.
Aceite proposto: Rejeitar trajetórias que apenas declaram sucesso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S035, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar recomendações do professor de resultados efetivamente observados.
- Testar memórias obsoletas e instruções conflitantes antes de liberar o acervo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare agentes na mesma tarefa, ferramentas e orçamento. Benchmarks AMD não demonstram equivalência geral; o benefício depende de o procedimento ser recuperado e executável no ambiente atual.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T055, T062, T178, T204

## Fontes primárias associadas

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T219 — Limite de recursão / profundidade de execução

**Nome canônico:** Limite de recursão / profundidade de execução  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T219  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execution depth limit; recursion budget

## T219:C01 — conceito

Orçamento explícito para limitar passos de execução, chamadas aninhadas ou profundidade de delegação. Esses limites medem coisas diferentes. No LangGraph, GRAPH_RECURSION_LIMIT trata do número de passos do grafo antes de uma condição de parada; não deve ser confundido automaticamente com a pilha de recursão da linguagem.

Como funciona:
- O runtime mantém contadores associados à execução e verifica o orçamento antes de avançar.
- Um limite alcançado gera um estado terminal controlado ou uma suspensão recuperável.
- A condição de término do fluxo continua necessária: aumentar o teto não corrige uma transição circular.

## T219:C02 — aplicacao

Quando usar:
- Workflows com laços, planejadores iterativos e delegação recursiva de agentes.

Quando não usar:
- Como único controle de custo ou como substituto de prazo, orçamento de tokens e limites para efeitos externos.

Implementação proposta:
- Proposta: definir separadamente máximo de passos, profundidade de agentes, chamadas de ferramentas e duração total.
- Documentar a unidade de contagem do framework e compartilhar o orçamento agregado com os descendentes.
- Preservar estado, motivo da interrupção e ações concluídas para permitir retomada consciente.
- Investigar o caminho de transições quando o teto for atingido; aumentar o orçamento somente com justificativa operacional.
- Planejar margem suficiente para registrar o resultado e liberar recursos antes de encerrar.

Aplicação LAI proposta:
Proposta LAI: atribuir orçamentos por missão e orçamento global do projeto, preservando o último estado confirmado quando uma execução atingir o limite.

## T219:C03 — riscos_validacao

Armadilhas:
- Um limite local por subagente pode permitir explosão do total global.
- Etapas longas ultrapassam o prazo mesmo com poucos passos.
- Uma parada abrupta pode deixar operações externas em resultado incerto.

Métricas sugeridas:
- Passos por tarefa; profundidade máxima; frequência de interrupção; custo agregado; operações pendentes ao parar.

Testes propostos:
- Criar um grafo sem condição de saída e verificar término limitado com diagnóstico.
- Testar um fluxo legítimo próximo do teto e conferir margem para finalizar.
- Simular delegação ramificada e verificar que o orçamento global prevalece.

## T219:C04 — perguntas_proveniencia

Pergunta: Posso usar o mesmo número para todos os limites?
Resposta: Pode ser inadequado: profundidade, passos e chamadas têm escalas diferentes. Escolha cada teto com base no comportamento esperado e na unidade real do runtime.

Pergunta: Atingir o limite significa que o modelo falhou?
Resposta: Não necessariamente. Pode indicar orçamento insuficiente, condição de parada incorreta ou tarefa maior que a prevista; o histórico permite distinguir as causas.

Pergunta: Um grafo com dez nós exige dez passos?
Resposta: Não necessariamente. Nós paralelos podem compartilhar superstep, enquanto ciclos podem executar o mesmo nó várias vezes.

Pergunta: Por que limitar só profundidade de subagentes é insuficiente?
Resposta: Porque muitos agentes podem ser criados em cada nível; o total de trabalho cresce mesmo com profundidade pequena.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T219:C05 — mecanismo_avancado

Um limite de profundidade não limita necessariamente o trabalho total. Em uma árvore com fator de ramificação b e profundidade d, a quantidade de nós pode crescer como 1+b+…+bᵈ. Já supersteps de um grafo podem conter vários nós paralelos. O contador precisa indicar sua unidade: etapas do grafo, chamadas de modelo, delegações aninhadas ou operações. Um orçamento compartilhado evita que cada filho receba inadvertidamente o orçamento integral da missão.

Condição de contorno:
Elevar o limite resolve apenas interrupção por orçamento insuficiente; não corrige uma condição de término ausente.

Contrato proposto:
- Entradas: Unidade de contagem, limite, orçamento global e contexto da delegação.
- Saídas: Permissão para novo passo ou interrupção com estado retomável.
- Estado: Consumo acumulado, profundidade corrente e reservas dos filhos.
- Invariante: A soma do trabalho delegado permanece contabilizada no objetivo principal.

Compromissos de projeto:
- Limites apertados reduzem explosão de trabalho e podem interromper tarefas válidas.
- Limites amplos acomodam fluxos complexos e aumentam custo de um ciclo defeituoso.

## T219:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar árvore rasa com muitos filhos e cadeia profunda sem ramificação; verificar que a política distingue volume total e profundidade, sem usar um contador como substituto do outro.

Plano de avaliação proposto:
Comparar limite único e orçamento multidimensional em grafos conhecidos. Medir interrupções corretas, falsas interrupções e consumo máximo. Calibrar pela estrutura observada e preservar diagnóstico do contador que realmente atingiu a fronteira.

Comparações:
- T218 (distinct_from): Detecção de estagnação interpreta progresso; limite de execução apenas impõe um teto.
- T147 (complements): Fan-out pode aumentar trabalho total sem ampliar muito a profundidade.

Afirmação rastreável:
LangGraph distingue supersteps paralelos e sequenciais e documenta limite de passos até uma condição de parada.
Suporte: direct; fontes: V3C-S006
Limite: Esse contador não equivale automaticamente à pilha de recursão de Python ou ao total de chamadas externas.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T219:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia profundidade, largura e supersteps. A ampliação propõe um orçamento de expansão verificável, critérios para conceder extensão e saída útil quando a execução alcança o teto.

Contadores tipados
Mantenha limites separados para delegação aninhada, transições do grafo, chamadas externas e custo acumulado. Uma unidade não substitui as outras: um nó pode disparar muitas operações, e vários nós podem avançar no mesmo superstep. Exponha ao controlador qual contador bloqueou a próxima ação, para não diagnosticar como falha cognitiva uma restrição estrutural.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V2A-S018.

Expansão com reserva
Antes de criar filhos, reserve parte do orçamento para juntar e validar seus resultados. Um supervisor que distribui todo o saldo aos trabalhadores pode ficar incapaz de concluir a missão. Limite também a quantidade de filhos ativos e de novas fronteiras abertas; profundidade baixa não impede fan-out excessivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Extensão condicionada
Permitir mais passos exige evidência de progresso e estimativa do trabalho restante. Não renove o limite somente porque o agente pediu para continuar. Registre motivo, saldo adicional e critério de término; mantenha teto absoluto da missão. Se a condição de saída não está definida, aumentar o limite apenas adia a falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3C-S032.

USO AVANÇADO — Delegação recursiva
Cenário: Um planejador divide tarefas e especialistas querem criar novos especialistas.
Estratégia: Autorize expansão somente se o filho produzir resultado integrável e couber na reserva. Exija referência à necessidade descoberta e elimine subproblemas duplicados. No último nível, o agente deve resolver com suas ferramentas ou devolver impedimento, sem contornar o teto criando nova sessão.
Papel do modelo pequeno: 3–7B não delega por padrão; 8–14B pede divisão; 15–30B decide com orçamento global.
Aceite proposto: Proposta: crescimento limitado e nenhum ramo abandonado sem estado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V2A-S018.

USO AVANÇADO — Grafo de reparo iterativo
Cenário: O agente alterna editar, testar e diagnosticar.
Estratégia: Defina número máximo de ciclos e custo total, mas ofereça saída com patch parcial e diagnóstico antes do teto. Se há progresso comprovado, uma extensão explícita pode continuar; repetição do mesmo erro deve acionar diagnóstico e não simplesmente incrementar o limite.
Papel do modelo pequeno: 8–14B executa ciclos locais; controlador valida progresso e extensão.
Aceite proposto: Proposta: distinguir tarefas longas produtivas de ciclos sem solução, medindo encerramento prematuro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3C-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar uma etapa ou pequeno ciclo com término claro, reduzindo necessidade de profundidade.
8–14B: Tratar subproblemas com algumas iterações e retornar saldo e impedimentos.
15–30B: Planejar expansão e integração, submetendo decisões de orçamento ao controlador determinístico.
Requisitos de treino/runtime: Contadores globais persistentes, reserva de finalização e documentação da unidade de limite do framework.
Não aplicar quando: Não interpretar recursion_limit de uma biblioteca como número universal de chamadas LLM ou profundidade de linguagem.

## T219:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação de grafos e agentes apoia os controles; relatos de delegação não demonstram esta política completa de limites nem justificam dez casos exatos. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q002, V4C-Q010, V4C-Q021, V4D-Q021.

## T219:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T219 → T218 [complements]
Como combinar: O detector identifica ciclos antes do teto, enquanto o limite garante término máximo mesmo quando a detecção falha.
Interface: Contadores, assinatura de repetição e progresso observado.
Condição: Intervenções não reiniciam o saldo.
Aceite proposto: Encerrar ciclo conhecido e permitir sequência longa que ainda avança.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T219 → T237 [complements]
Como combinar: Delegação consome orçamento do pai e devolve resultado que cabe na reserva de integração.
Interface: Quota do filho, profundidade e contrato de retorno.
Condição: Expansão autorizada pelo controlador e não apenas pelo texto do prompt.
Aceite proposto: Soma de quotas e reservas não excede o teto global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V2A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Trocar o nome da sessão ou do agente não deve zerar contadores da missão.
- Ao atingir o teto, preservar estado aceito e explicitar o trabalho não executado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de conclusão sob orçamento igual, contando todos os descendentes. A equipe pequena não deve ganhar vantagem aparente por ocultar chamadas atrás de um único superstep.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T218, T237, T243

## Fontes primárias associadas

### V2A-S009 — GRAPH_RECURSION_LIMIT

[https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limite de passos de execução do grafo antes de alcançar condição de parada.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

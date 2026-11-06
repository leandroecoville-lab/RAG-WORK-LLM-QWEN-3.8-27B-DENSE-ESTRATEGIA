# T050 — Working Memory Window

**Nome canônico:** Working Memory Window  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T050  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela de memória de trabalho

## T050:C01 — conceito

Parte da informação operacional mantida ativamente para a etapa corrente: objetivo, próximos passos, dados recentes e dependências. Pode ser materializada em mensagens e campos estruturados. É memória de trabalho do sistema, não uma leitura dos estados internos ocultos da LLM.

Como funciona:
- Identificar a decisão ou ação da próxima etapa.
- Carregar estado e evidências necessárias.
- Remover ou arquivar conteúdo concluído mantendo ponteiros para reabertura.

## T050:C02 — aplicacao

Quando usar:
- Agentes de execução com orçamento restrito.
- Fluxos que alternam análise, ferramentas e verificação.

Quando não usar:
- Não confundir a janela ativa com todo o conhecimento persistido ou com a totalidade do histórico.

Implementação proposta:
- Proposta: manter objetivo, restrições, etapa e dúvidas em campos pequenos.
- Reservar uma parcela do orçamento para novas observações.
- Atualizar a janela apenas depois de persistir resultados que precisam sobreviver.

Aplicação LAI proposta:
Proposta LAI: usar um estado de missão compacto da Helena como núcleo e anexar evidência específica conforme a tarefa, sem prometer retenção ilimitada na janela.

## T050:C03 — riscos_validacao

Armadilhas:
- Um plano desatualizado pode continuar ocupando posição privilegiada.
- Reduzir demais a janela impede interpretar a próxima ferramenta.

Métricas sugeridas:
- Correção da próxima ação e retomada.
- Tokens ativos e referências abertas por rodada.

Testes propostos:
- Trocar a etapa do workflow e verificar mudança das informações carregadas.
- Remover detalhe já arquivado e recuperá-lo quando uma dependência reaparecer.

## T050:C04 — perguntas_proveniencia

Pergunta: Working memory é um arquivo ou um prompt?
Resposta: É um papel funcional. Pode usar arquivos, estado e prompt, desde que o necessário seja carregado para a decisão.

Pergunta: Ela deve guardar todas as tentativas anteriores?
Resposta: Não necessariamente. Tentativas podem ficar no registro episódico e ser recuperadas quando úteis.

Pergunta: O scratchpad inteiro deve ficar ativo?
Resposta: Não necessariamente. Mantenha os campos que condicionam a próxima decisão e referências para detalhes, verificando se as relações necessárias continuam disponíveis.

Pergunta: Uma referência ocupa menos tokens que seu conteúdo; por que não usar só referências?
Resposta: Porque o modelo precisa ler a informação relevante para decidir. Ponteiros economizam espaço apenas quando podem ser resolvidos a tempo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T050:C05 — mecanismo_avancado

A janela de trabalho é uma visão operacional derivada de estado e fontes, com vida útil ligada à etapa. Convém separar itens fixos, como objetivo vigente, de itens temporários, como uma observação que serve à próxima decisão. Após a etapa, parte do conteúdo pode ser promovida a memória durável e parte descartada. Essa rotação não corresponde a apagar parâmetros nem a modificar diretamente estados neurais ocultos.

Condição de contorno:
Se a tarefa exige relações entre muitos itens simultâneos, externalizar tudo sem uma representação de ligação pode impedir que o modelo compare as evidências necessárias.

Contrato proposto:
- Entradas: Objetivo atual, transição pretendida, observações recentes e referências a conteúdo disponível.
- Saídas: Visão compacta com dependências suficientes para a decisão e lacunas explicitamente abertas.
- Estado: Revisão da visão, conteúdo fixado, observações temporárias e orçamento reservado à próxima interação.
- Invariante: Toda decisão baseada na janela identifica a versão do estado e das evidências que estavam presentes.

Compromissos de projeto:
- Reduzir material temporário diminui ruído e pode aumentar consultas repetidas.
- Fixar conteúdo essencial protege continuidade e reduz espaço para novas evidências; o conjunto fixo também precisa revisão.

## T050:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: concluir uma subtarefa e mudar o objetivo mantendo uma hipótese anterior no bloco fixo. A reconstrução deve revisar a hipótese e carregar dependências do novo objetivo.

Plano de avaliação proposto:
Avaliação proposta: comparar janela recente e visão por etapa, mantendo o mesmo orçamento. Medir ações corretas, abertura repetida de fontes, uso de hipóteses obsoletas e custo de reconstrução; testar tarefas que exigem comparação simultânea.

Comparações:
- T063 (complements): Memória virtual move conteúdo entre níveis; a janela de trabalho especifica o conjunto ativo para a etapa.
- T043 (complements): Compactação pode reconstruir a visão, mas não é necessária a cada atualização pequena.

Afirmação rastreável:
MemGPT propõe mover informação entre níveis de memória para utilizar conteúdo além da janela ativa limitada.
Suporte: direct; fontes: A-S009
Limite: A janela de trabalho aqui descrita é uma política arquitetural; não é acesso ao raciocínio interno ou à memória biológica de um modelo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T050:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou vista e persistência. Aqui a memória de trabalho é organizada por hipóteses ativas e custo de alternar tarefas.

Projeto e decomposição
Mantenha quadro com objetivo, hipótese em teste, evidência necessária e próxima decisão. Conteúdo entra por função nessa etapa, não apenas por ter aparecido recentemente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

Controle adaptativo
Ao alternar tarefa, salve o quadro e carregue outro com identificação explícita. Misturar hipóteses de tarefas diferentes pode produzir respostas coerentes com o projeto errado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

Validação contrafactual
Compare janela cronológica e quadro por hipótese. Meça retomada após interrupção, repetição de testes e confusão de entidades entre tarefas, mantendo o mesmo limite de tokens. Unidade de avaliação: etapa de raciocínio operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

USO AVANÇADO — Depuração com interrupções
Cenário: Usuário muda prioridade durante investigação.
Estratégia: Persistir hipótese e teste pendente, suspender trabalho e retomar somente após confirmar que revisão do código continua compatível.
Papel do modelo pequeno: 8–14B administra hipótese local.
Aceite proposto: Não repetir teste concluído nem aplicar resultado a revisão diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

USO AVANÇADO — Leitura analítica
Cenário: Várias questões usam o mesmo corpus.
Estratégia: Manter quadro por questão com evidências específicas; compartilhar apenas fontes, não conclusões provisórias entre quadros.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra.
Aceite proposto: Cada resposta deve usar o quadro e o escopo corretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de uma hipótese ou campo por etapa, com estado estruturado externo.
8–14B: Analista de poucas hipóteses com identificação de evidência faltante.
15–30B: Integrador de hipóteses interdependentes quando alternância simples não basta.
Requisitos de treino/runtime: Quadro serializável, identidade de tarefa e revisão da origem; o modelo não precisa reter todo histórico.
Não aplicar quando: A tarefa depende de contexto implícito que o quadro não representa e não pode recuperar.

## T050:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T050:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T050 → T053 [complements]
Como combinar: Persistir quadro de trabalho entre chamadas.
Interface: task_id, hipótese, teste e referência de evidência.
Condição: Arquivo não misturar tarefas sem namespace.
Aceite proposto: Interromper processo e retomar quadro correto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T050 → T039 [requires]
Como combinar: Fixar evidência da hipótese ativa temporariamente.
Interface: Blocos necessários e condição de liberação.
Condição: Hipótese ainda estiver aberta.
Aceite proposto: Encerrar hipótese e conferir liberação de espaço.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover hipótese ativa automaticamente a memória durável.
- Não usar resumo de tarefa anterior como estado atual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade e precisão ao alternar tarefas; janela organizada não substitui capacidade de resolver a hipótese.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T039, T040, T053

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

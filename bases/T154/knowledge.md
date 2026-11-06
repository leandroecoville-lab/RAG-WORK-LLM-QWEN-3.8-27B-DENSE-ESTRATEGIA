# T154 — Multi-Turn Conversation Management

**Nome canônico:** Multi-Turn Conversation Management  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T154  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gerenciamento de conversas multiturno

## T154:C01 — conceito

Gerenciamento da continuidade entre turnos: identidade da sessão, histórico, chamadas de ferramentas, objetivos, fatos vigentes e limites de contexto. A conversa exibida é apenas uma projeção; o sistema precisa manter estado consistente mesmo quando resume ou deixa mensagens antigas fora do prompt.

Como funciona:
- Associar mensagem a usuário, tenant, thread e ordem correta.
- Atualizar estado e referências de ferramentas de forma persistente.
- Montar próximo contexto com histórico selecionado e decisões ainda vigentes.

## T154:C02 — aplicacao

Quando usar:
- Assistentes que retomam tarefas ao longo de várias sessões.
- Fluxos com correções de instruções e ferramentas pendentes.

Quando não usar:
- Concatenar todo o histórico sem tratar limite, conflito temporal ou isolamento.

Implementação proposta:
- Guardar eventos originais e projeção compacta separadamente.
- Serializar mutações por thread ou usar controle otimista de versão.
- Tratar mensagem nova durante execução como evento que pode alterar objetivo ou cancelar etapa.

Aplicação LAI proposta:
Proposta: a Helena usar estado versionado por missão e memória externa recuperável, preservando a decisão atual de Leandro.

## T154:C03 — riscos_validacao

Armadilhas:
- Resumo pode preservar decisão antiga já revogada.
- Threads concorrentes podem sobrescrever o mesmo estado ou misturar clientes.

Métricas sugeridas:
- Retenção de restrições após muitos turnos.
- Conflitos de estado, respostas a objetivo antigo e erros de associação de ferramenta.

Testes propostos:
- Corrigir uma decisão e verificar que o próximo turno usa a versão vigente.
- Reiniciar o processo e retomar com resultados de ferramentas corretamente vinculados.

## T154:C04 — perguntas_proveniencia

Pergunta: Histórico completo é memória suficiente?
Resposta: Não. Precisa de identificação, atualidade e recuperação correta.

Pergunta: Checkpoint em RAM é durável?
Resposta: Não após queda do processo; é necessário backend persistente.

Pergunta: Uma nova tentativa deve criar nova mensagem lógica?
Resposta: Depende do contrato. Duplicata de entrega deve manter identidade; regeneração intencional pode criar versão ou ramo distinto.

Pergunta: Como explicar uma resposta baseada em decisão antiga?
Resposta: Registrar a revisão de entrada permite identificar desatualização e decidir se a resposta precisa ser refeita.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T154:C05 — mecanismo_avancado

Uma conversa com turnos concorrentes precisa definir qual revisão de estado cada turno leu. Sem essa relação, duas respostas podem atualizar objetivos e histórico em ordens incompatíveis. Um modelo de append com IDs de mensagem preserva eventos, mas decisões vigentes podem exigir controle de versão separado. Editar ou refazer um turno também cria uma ramificação lógica: não se deve misturar automaticamente respostas produzidas a partir de passados diferentes.

Condição de contorno:
Um identificador de sessão isolado não resolve concorrência, duplicatas de transporte ou regenerações de mensagens.

Contrato proposto:
- Entradas: Sessão, ID do turno, revisão de origem e novas observações.
- Saídas: Resposta vinculada à revisão e atualização confirmada ou conflito explícito.
- Estado: Histórico de eventos, versão ativa, chamadas pendentes e ramificações.
- Invariante: Uma resposta mantém vínculo com o estado usado para produzi-la.

Compromissos de projeto:
- Serializar turnos simplifica consistência e acrescenta espera.
- Permitir concorrência reduz latência e exige merge ou rejeição de atualizações incompatíveis.

## T154:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar dois turnos sobre a mesma versão e fazer o segundo concluir primeiro; verificar ordem de aplicação ou conflito conforme a política, preservando ambos os eventos.

Plano de avaliação proposto:
Comparar fila por sessão e concorrência com controle otimista em conversas com mudanças de objetivo. Medir conflitos, atualizações perdidas, latência e reconstrução histórica. Definir o contrato antes de otimizar paralelismo.

Comparações:
- T060 (complements): Checkpoints persistem o estado por sessão, mas não definem sozinhos como aceitar turnos simultâneos.
- T207 (complements): Um fluxo de eventos pode registrar mensagens e revisões sem apagar o passado.

Afirmação rastreável:
LangGraph persiste estado por thread por meio de checkpointers e diferencia esse escopo dos stores compartilhados.
Suporte: direct; fontes: A-S022
Limite: Políticas de edição, concorrência e ramificação da conversa são propostas do aplicativo.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T154:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou revisões concorrentes e ramificações de histórico. A camada nova trata conversa como entrada de um sistema de tarefas, com objetivo vigente, mensagens deduplicadas e comunicação entre sessões.

Mensagem e tarefa têm ciclos diferentes
Uma mensagem pode iniciar várias tarefas e uma tarefa pode sobreviver a muitos turnos. Dê identidades separadas a ambas. O estado operacional informa o que está em andamento; a conversa explica decisões e preferências, evitando que um novo turno apague inadvertidamente tarefas ainda válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

Revisão de objetivo
Quando o usuário corrige uma instrução, registre quais tarefas e artefatos ela invalida. Resultados independentes podem ser conservados; efeitos já realizados exigem reconciliação ou compensação de domínio. O modelo não deve simplesmente reescrever a narrativa como se a intenção anterior nunca tivesse sido executada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, C-S026.

Sincronização por eventos
Eventos de progresso precisam ser associados à revisão de objetivo que os gerou. Uma interface pode receber conclusão antiga depois de uma correção nova; o controlador deve classificá-la como resultado histórico, pendente ou ainda relevante. Mostrar uma lista concatenada de mensagens não resolve essa interpretação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S028.

USO AVANÇADO — Missão de programação atravessando sessões
Cenário: O agente prepara uma alteração, pausa e depois recebe um requisito adicional.
Estratégia: Releia o objetivo e a revisão do repositório, compare com o último pacote de trabalho e invalide testes afetados. Continue apenas as subtarefas que permanecem válidos; mudanças de escopo entram como nova versão, com motivo.
Papel do modelo pequeno: 8–14B realiza retomada local; 15–30B avalia impacto entre módulos.
Aceite proposto: Proposta: medir requisitos perdidos e trabalho indevidamente reutilizado em cenários com correções e edição concorrente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S037.

USO AVANÇADO — Assistente com trabalho em background
Cenário: Uma consulta longa continua enquanto o usuário inicia outra interação.
Estratégia: Use mailbox ou fila por instância, deduplique mensagens e preserve prioridade das correções. Atualizações de tarefas não devem bloquear leitura de novos pedidos nem assumir que todo pedido novo cancela o anterior.
Papel do modelo pequeno: 3–7B classifica eventos; 8–30B interpreta mudanças dentro de contratos conhecidos.
Aceite proposto: Proposta: permutar entregas e confirmar objetivo vigente, tarefas ativas e respostas atribuídas às solicitações corretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: atualizar campos simples de estado a partir de mensagens estruturadas, com confirmação de ambiguidades.
8–14B: Proposta: continuar tarefas locais com resumo fiel, artefatos e histórico de requisitos.
15–30B: Proposta: coordenar objetivos e resultados paralelos, sem usar a janela como único armazenamento.
Requisitos de treino/runtime: Exige persistência, identificação de usuário e tarefa, deduplicação e política de invalidação; aumentar contexto não resolve concorrência.
Não aplicar quando: Não manter tarefas autônomas quando a correção do usuário tornou seu efeito incompatível com a intenção vigente.

## T154:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Instância e mailbox conservam continuidade da interação.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Hiring Assistant é caso operacional; extrapolações para programação e modelos pequenos são propostas, e Brooklin é analogia de transporte de eventos.
Consultas registradas: V4C-Q010, V4C-Q020.

## T154:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T154 → T208 [complements]
Como combinar: Hiring Assistant mantém instâncias e mailbox enquanto o supervisor coordena plano e execução.
Interface: Mensagens, tarefas e resultados do ciclo de planejamento.
Condição: A instância tem identidade e regras de ciclo de vida.
Aceite proposto: Proposta: interromper uma interação e verificar que o estado da tarefa permanece coerente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T154 → T211 [feeds]
Como combinar: A conversa fornece objetivo e decisões ao pacote de continuidade.
Interface: Revisão do objetivo, artefatos e pendências confirmadas.
Condição: O pacote distingue fatos de interpretações do agente.
Aceite proposto: Retomar sem todo o chat e recuperar corretamente próximos passos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reexecutar mensagem duplicada como nova intenção de mutação.
- Nunca usar apenas ordem de chegada à interface para definir causalidade entre eventos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare retenção de requisitos e retomada com fronteira sob o mesmo estado externo. Contexto persistido reduz esquecimento operacional, sem garantir compreensão equivalente de instruções complexas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T049, T064, T075

## Fontes primárias associadas

### C-S019 — Persistence — LangGraph

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers mantêm estado de threads; stores preservam informação definida pela aplicação entre threads.

Limite: A URL durable-execution redirecionou para persistence na consulta; exemplos InMemory não demonstram durabilidade após queda de processo.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

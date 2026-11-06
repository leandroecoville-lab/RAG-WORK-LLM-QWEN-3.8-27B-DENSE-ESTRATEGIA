# T159 — Durable Execution

**Nome canônico:** Durable Execution  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T159  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execução durável

## T159:C01 — conceito

Execução que persiste progresso para continuar após interrupções ou falhas. Histórico, checkpoints e replay reconstroem a posição do workflow. A durabilidade do fluxo não implica efeito externo exatamente uma vez: operações remotas ainda precisam de idempotência, recibos ou reconciliação.

Como funciona:
- Registrar decisões e resultados de etapas em armazenamento durável.
- Após falha, recuperar estado e distinguir trabalho concluído de pendente.
- Retomar respeitando contratos de replay e efeitos externos.

## T159:C02 — aplicacao

Quando usar:
- Missões longas que atravessam reinícios.
- Fluxos que aguardam eventos externos ou aprovação já prevista.

Quando não usar:
- Reexecutar chamadas não determinísticas durante replay sem registrar seus resultados.

Implementação proposta:
- Escolher unidade de persistência e política de commit por etapa.
- Executar I/O não determinístico em atividades com resultado registrado.
- Versionar workflow para que código novo consiga interpretar históricos existentes.

Aplicação LAI proposta:
Proposta: a Helena persistir progresso e recibos por missão, permitindo continuar tarefas sem depender de uma conversa permanentemente aberta.

## T159:C03 — riscos_validacao

Armadilhas:
- Queda entre efeito remoto e registro local cria estado incerto.
- Mudança incompatível no código torna replay inválido.

Métricas sugeridas:
- Taxa de retomada correta e trabalho repetido após falha.
- Tempo de recuperação e quantidade de históricos incompatíveis.

Testes propostos:
- Matar worker após cada fronteira crítica e verificar continuação.
- Simular resposta perdida após efeito externo e exigir consulta ou deduplicação antes de repetir.

## T159:C04 — perguntas_proveniencia

Pergunta: Durable execution garante exactly once no CRM?
Resposta: Não. Essa propriedade depende também do contrato do CRM e da reconciliação.

Pergunta: Checkpoint basta para qualquer retomada?
Resposta: Não. Precisa estar consistente com efeitos já realizados.

Pergunta: Uma LLM com temperatura zero pode rodar livremente dentro do replay?
Resposta: Não se deve presumir determinismo externo. O resultado precisa ser registrado pelo mecanismo apropriado do runtime.

Pergunta: Por que testar apenas workflows novos é insuficiente?
Resposta: Porque eles não exercitam históricos produzidos por versões anteriores, onde alterações de comandos podem quebrar a retomada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T159:C05 — mecanismo_avancado

Replay durável não exige que cada instrução de máquina seja idêntica; exige compatibilidade com o histórico de comandos observáveis pelo runtime. No Temporal, chamadas não determinísticas, inclusive consultas e LLMs, pertencem a Activities. Uma alteração que muda a ordem de comandos pode impedir retomar workflows antigos mesmo que o novo código funcione em execuções recém-criadas. Evolução do código é, portanto, parte do contrato de continuidade.

Condição de contorno:
Persistir eventos sem manter código capaz de interpretá-los não garante retomada após uma atualização.

Contrato proposto:
- Entradas: Histórico, versão compatível do workflow e resultados registrados das atividades.
- Saídas: Estado reconstruído e próximos comandos consistentes com o histórico.
- Estado: Versão de código, pontos de migração e resultados duráveis.
- Invariante: Replay não solicita novamente uma observação externa apenas para reproduzir uma decisão já registrada.

Compromissos de projeto:
- Histórico detalhado aumenta capacidade de reconstrução e custo de armazenamento.
- Manter versões antigas facilita continuidade e aumenta esforço de operação e migração.

## T159:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: pausar um workflow, trocar a ordem de duas atividades no código e tentar retomá-lo; exigir detecção de incompatibilidade ou migração prevista, nunca continuidade silenciosamente divergente.

Plano de avaliação proposto:
Comparar retomada com a versão original e com migração controlada. Medir falhas de replay, tarefas reexecutadas e tempo de recuperação. Usar históricos reais de desenvolvimento separados dos casos de decisão; aceitar mudança somente com compatibilidade demonstrada.

Comparações:
- T241 (complements): Replay é um mecanismo de reconstrução usado por runtimes duráveis.
- T162 (complements): Efeitos de Activities continuam precisando de identidade e repetição segura.

Afirmação rastreável:
Temporal exige compatibilidade determinística de comandos e orienta colocar operações externas em Activities.
Suporte: direct; fontes: V3C-S018
Limite: A semântica de durabilidade varia entre runtimes; a fonte não prova efeito remoto exatamente uma vez.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T159:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava determinismo de replay e evolução de código. A ampliação define fronteiras de falha entre decisão cognitiva e efeitos, crescimento do histórico e retomada de atividades longas sem depender da memória conversacional.

Decisão registrada antes do efeito
Faça o resultado da LLM virar um artefato validado contendo ação, argumentos e versão do contrato. O workflow durável registra a decisão; uma atividade separada executa o efeito com identidade estável. Se a chamada ao modelo falhar antes de produzir decisão válida, uma nova geração pode ser legítima; depois da decisão confirmada, replay deve reutilizá-la.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, C-S026.

Histórico finito e referências
Não persista documentos enormes em cada evento. Registre referências imutáveis, hashes e os campos necessários para decidir próximos passos. A existência do evento não garante que seu arquivo externo continue acessível: retenção do artefato e do histórico precisam ser coordenadas. Divida missões longas em segmentos com estado de passagem explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S024.

Operação sob versões múltiplas
Mantenha workers compatíveis com execuções antigas enquanto novas usam a versão aprovada. Exercite históricos de falhas, não apenas trajetórias felizes. Uma retomada que relança a atividade pode repetir acesso remoto; durabilidade do coordenador não elimina a necessidade de idempotência, reconciliação e classificação de falhas na integração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

USO AVANÇADO — Migração de código demorada
Cenário: Uma campanha atravessa centenas de módulos e quedas de workers.
Estratégia: Registre plano, revisão base e conclusão de cada unidade. Gere patch em atividade separada, valide e publique referência do candidato. Após queda, recupere o próximo módulo pendente; se a publicação ficou incerta, consulte seu identificador antes de refazer a alteração.
Papel do modelo pequeno: 3–7B edita unidades simples; 15–30B planeja dependências e exceções.
Aceite proposto: Proposta: nenhuma unidade esquecida ou publicada duas vezes após falhas injetadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S018.

USO AVANÇADO — Pesquisa interrompida por horas
Cenário: Coletas remotas e síntese não terminam na mesma sessão.
Estratégia: Persistir cada fonte com data, conteúdo identificado e estado de extração. A retomada reutiliza observações confirmadas e reconsulta somente itens cuja validade venceu. Se a pergunta mudou, crie nova revisão em vez de reinterpretar silenciosamente decisões já registradas.
Papel do modelo pequeno: 8–14B extrai; coordenador durável controla fases e revisões.
Aceite proposto: Proposta: equivalência de cobertura entre execução contínua e retomada, com atualização explícita de fontes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atividades pequenas com saída validável e baixa variância de duração.
8–14B: Etapas com recuperação de documentos e retorno estruturado, desacopladas do histórico do workflow.
15–30B: Planejamento mais amplo em atividade registrada; nunca executar chamadas externas diretamente no replay determinístico.
Requisitos de treino/runtime: Runtime durável, armazenamento de artefatos, versão de worker e contratos idempotentes na borda.
Não aplicar quando: Não prometer continuidade se somente mensagens de chat foram salvas ou se artefatos referenciados desaparecem.

## T159:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: O relato inclui recuperação de processos distribuídos longos.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Execução durável de workflows é o mecanismo central relatado.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber documenta Cadence operacional; Cadence e Temporal permanecem produtos distintos. Fontes Temporal explicam contrato, sem inferir adoção de um a partir do outro.
Consultas registradas: V4C-Q002, V4C-Q022.

## T159:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T159 → T241 [complements]
Como combinar: Cadence usa reprodução do histórico para continuidade e validação de execução.
Interface: Histórico compatível e versão do worker.
Condição: Operações externas têm resultados registrados.
Aceite proposto: Retomar após queda sem gerar decisões externas para reconstruir passado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S001. Casos: V4C-C003.

2. T159 → T162 [complements]
Como combinar: Associar efeito remoto a identidade estável quando uma atividade pode repetir.
Interface: Chave de intenção e parâmetros normalizados.
Condição: Serviço de destino oferece deduplicação ou reconciliação.
Aceite proposto: Queda após confirmação remota não duplica o efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar um histórico incompatível em nova execução silenciosa.
- Distinguir atividade não concluída de efeito remoto desconhecido antes de repetir.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos por qualidade das atividades; compare runtimes por recuperação. Um modelo pequeno com durabilidade pode completar mais missões interrompidas sem possuir maior capacidade cognitiva.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T162, R008

## Fontes primárias associadas

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T225 — Watchdog com Auto-Restart

**Nome canônico:** Watchdog com Auto-Restart  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T225  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** watchdog; supervisor com reinício

## T225:C01 — conceito

Supervisor que identifica falha de uma execução e inicia recuperação conforme uma política limitada. Reiniciar um processo recupera capacidade de execução, mas não esclarece automaticamente o estado das suas ações. Um agente que caiu após enviar uma operação pode precisar consultar o sistema externo antes de continuar.

Como funciona:
- O watchdog observa processo, sinais de saúde, prazo e progresso confirmado.
- Uma política determina se a falha permite reinício, espera ou intervenção.
- Uma nova execução adquire responsabilidade exclusiva e recupera estado antes de produzir novos efeitos.

## T225:C02 — aplicacao

Quando usar:
- Workers de longa duração, processos sujeitos a interrupções e tarefas com estado persistente recuperável.

Quando não usar:
- Reiniciar indefinidamente um erro determinístico ou usar restart para contornar falta de permissão e dependências permanentemente ausentes.

Implementação proposta:
- Proposta: definir quais sinais representam falha e quais representam lentidão esperada.
- Usar identidade de execução e mecanismo de exclusão, como lease com fencing, para impedir dois executores válidos após uma pausa longa.
- Persistir checkpoint e resultados confirmados; consultar efeitos incertos antes de retomar a fila.
- Aplicar limite de reinícios, intervalo crescente e estado de falha persistente quando o orçamento acabar.
- Separar diagnóstico da aplicação e diagnóstico do supervisor para evitar que o mesmo defeito derrube ambos.

Aplicação LAI proposta:
Proposta LAI: supervisionar workers de missões com orçamento de recuperação e exclusividade verificável, encaminhando operações incertas para reconciliação antes de novos efeitos.

## T225:C03 — riscos_validacao

Armadilhas:
- Heartbeats continuam chegando enquanto o agente gira em falso.
- Reinício prematuro duplica trabalho.
- Uma partição de rede pode manter o processo antigo ativo mesmo após o supervisor considerar o lease expirado.

Métricas sugeridas:
- Tempo para detectar falha; tempo de recuperação; reinícios por tarefa; execuções concorrentes indevidas; efeitos duplicados.

Testes propostos:
- Interromper um worker após persistir progresso e verificar retomada pelo estado confirmado.
- Pausar o worker antigo, iniciar recuperação e confirmar rejeição das escritas antigas pelo fencing.
- Provocar falha permanente e verificar que o supervisor para de reiniciar.

## T225:C04 — perguntas_proveniencia

Pergunta: Auto-restart garante continuidade correta?
Resposta: Não. Ele precisa de estado persistente, controle de concorrência e tratamento das operações que podem ter concluído antes da queda.

Pergunta: Toda falha de dependência pede restart?
Resposta: Não. Reiniciar pode piorar uma indisponibilidade compartilhada. A política deve distinguir processo quebrado de serviço temporariamente inacessível.

Pergunta: Processo vivo mas sem avanço deve sempre reiniciar?
Resposta: Não. Primeiro distinguir espera legítima, bloqueio externo e defeito local; cada caso exige resposta diferente.

Pergunta: Um novo processo pode começar pela primeira etapa?
Resposta: Somente se o contrato garantir repetição segura; caso contrário, deve recuperar estado e reconciliar efeitos já enviados.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T225:C05 — mecanismo_avancado

Reinício precisa classificar falha de processo, indisponibilidade de dependência e ausência de progresso. Reiniciar repetidamente uma aplicação saudável porque seu banco está fora pode ampliar a carga de inicialização e atrasar recuperação. A política proposta mantém orçamento de reinícios, espera entre tentativas e informação de propriedade da missão. Antes de retomar efeitos, reconcilia o último ponto confirmado e resultados externos ainda desconhecidos.

Condição de contorno:
Quando a causa permanece externa ou determinística, reiniciar o mesmo código com o mesmo estado tende a reproduzir o problema.

Contrato proposto:
- Entradas: Sinais de vida e progresso, causa de término e estado durável da missão.
- Saídas: Reinício, espera, isolamento ou término explícito com diagnóstico.
- Estado: Histórico de reinícios, geração do worker e operações pendentes.
- Invariante: Um worker antigo não reaparece como escritor válido após a recuperação assumir nova geração.

Compromissos de projeto:
- Detecção rápida reduz indisponibilidade e pode reiniciar trabalho apenas lento.
- Espera maior protege dependências e aumenta tempo de recuperação de falhas simples.

## T225:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter processo vivo, interromper dependência e pausar o worker antigo durante a troca; exigir política que evite tempestade de reinícios e escritas obsoletas.

Plano de avaliação proposto:
Comparar restart imediato e recuperação com classificação e orçamento sob falhas de processo e serviço externo. Medir retomada, reinícios inúteis, efeitos duplicados e progresso preservado. Escolher pelo objetivo de recuperação, não só por uptime do processo.

Comparações:
- T227 (complements): Sinais de saúde precisam separar quem deve reiniciar de quem deve parar de receber tráfego.
- T243 (complements): Reconciliação identifica o que a execução anterior efetivamente realizou.

Afirmação rastreável:
Kubernetes distingue readiness para retirar tráfego e liveness para detectar condições que podem exigir reinício.
Suporte: direct; fontes: V2A-S011
Limite: Essas probes não conhecem automaticamente o progresso de uma missão nem seus efeitos externos.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T225:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia processo, dependência e progresso. A expansão define recuperação escalonada, evita ciclos de restart e trata a nova instância como sucessora que precisa demonstrar propriedade e estado antes de agir.

Diagnóstico antes do restart
Use sinais separados de processo vivo, capacidade de responder e avanço da missão. Falha de GPU, deadlock local e serviço externo indisponível pedem respostas diferentes. Capture diagnóstico suficiente antes de encerrar o processo quando isso for possível; reiniciar rapidamente pode destruir a evidência necessária para corrigir uma falha determinística.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V3C-S040.

Orçamento de recuperação
Imponha intervalo mínimo, teto de reinícios e período de estabilidade antes de considerar a recuperação bem-sucedida. Uma sequência de processos novos não representa disponibilidade se nenhum conclui trabalho útil. Ao esgotar o orçamento, suspenda a missão com estado preservado e causa explícita, evitando a amplificação de inicialização e recomputação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V4C-S023.

Sucessão de executor
A instância nova lê checkpoint, confirma revisão e reconcilia operações em voo. Se a antiga ainda puder terminar, seus resultados recebem geração e precisam ser validados antes de publicar. Uma lease vencida não revoga automaticamente acesso remoto; use fencing onde o destino o suporta e reconciliação nos demais casos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, C-S026.

USO AVANÇADO — Worker local de inferência
Cenário: Uma missão longa sofre falha de processo ou falta de memória.
Estratégia: Identifique se o erro é transitório ou se o mesmo payload excederá novamente a capacidade. Para o segundo caso, reduza lote ou contexto mediante contrato antes de retomar. Recarregar os mesmos pesos e reenviar a mesma entrada não corrige incapacidade estrutural.
Papel do modelo pequeno: 3–7B pode servir classe reduzida; 15–30B requer admissão compatível com recursos disponíveis.
Aceite proposto: Proposta: recuperação termina em resultado útil, sem tempestade de recarga ou perda de checkpoint.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S023, V3C-S028.

USO AVANÇADO — Controlador de edição interrompido
Cenário: O processo cai após enviar patch ou disparar CI.
Estratégia: Recupere artefatos persistidos e consulte IDs de publicação e build. Se já existem, acompanhe-os; se o desfecho continua desconhecido, mantenha reconciliação. Só reinicie a etapa lógica quando houver evidência de que ela ainda é necessária.
Papel do modelo pequeno: 8–14B interpreta diagnóstico; runtime administra sucessão e efeitos.
Aceite proposto: Proposta: nenhuma duplicação de publicação ou CI após falhas em pontos diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atividades curtas permitem checkpoints frequentes e menor custo de reinício.
8–14B: Diagnóstico de falhas locais e sugestão de redução de escopo, sob regras determinísticas.
15–30B: Replanejamento da missão após repetidos reinícios, sem apagar histórico de falhas.
Requisitos de treino/runtime: Supervisor externo ao processo monitorado, orçamento persistente e identidade de geração para escritores.
Não aplicar quando: Não reiniciar aplicação saudável só porque uma dependência externa caiu ou uma tarefa válida é longa.

## T225:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cadence e Borg apoiam continuidade e gestão de recursos; a política completa de watchdog cognitivo é proposta, sem implantação LAI alegada.
Consultas registradas: V4C-Q002, V4C-Q018.

## T225:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T225 → T226 [complements]
Como combinar: Usar progresso confirmado para distinguir processo ocupado de missão estagnada.
Interface: Cursor, último avanço e geração do executor.
Condição: Heartbeat corresponde a unidade realmente concluída.
Aceite proposto: Silêncio e ausência de avanço acionam políticas distintas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T225 → T243 [complements]
Como combinar: Reconciliar o que a instância anterior pode ter realizado antes de repetir etapas.
Interface: Intenção, envio e observação remota.
Condição: A nova instância não assume ausência de efeito por ausência de confirmação local.
Aceite proposto: Queda após efeito não produz duplicata.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Restart sem mudança de condição tende a repetir falha determinística.
- Custo de carregamento e aquecimento precisa entrar no orçamento de recuperação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare recuperação por tarefa concluída, não por tempo até processo responder. Modelos menores podem reiniciar mais barato, mas ainda dependem de estado durável e fronteiras corretas de efeito.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T226, T227, T243, T060

## Fontes primárias associadas

### V2A-S010 — Detecting Activity failures

[https://docs.temporal.io/encyclopedia/detecting-activity-failures](https://docs.temporal.io/encyclopedia/detecting-activity-failures)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Timeouts de atividades, heartbeats, detalhes de progresso e tentativas posteriores.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S011 — Configure Liveness, Readiness and Startup Probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Probes de vida, prontidão e inicialização possuem efeitos operacionais distintos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S024 — Controllers

[https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Laços de controle com observação do estado atual e aproximação ao estado desejado.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

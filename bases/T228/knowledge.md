# T228 — Fila de retries com backoff exponencial

**Nome canônico:** Fila de retries com backoff exponencial  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T228  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** exponential backoff retry queue; retry com jitter

## T228:C01 — conceito

Fila de novas tentativas que espaça falhas transitórias com atraso crescente e variação aleatória. Backoff reduz pressão repetida sobre uma dependência; jitter evita que muitos clientes repitam juntos. A política também precisa decidir se repetir é semanticamente seguro e quando abandonar a tentativa.

Como funciona:
- Uma falha classificada como recuperável agenda nova tentativa com prazo e orçamento.
- O atraso pode crescer exponencialmente até um teto, com jitter para dispersar clientes.
- A identidade da operação lógica permanece estável, enquanto cada tentativa recebe um identificador próprio.

## T228:C02 — aplicacao

Quando usar:
- Erros transitórios de rede, limitação de taxa e indisponibilidade temporária em operações com recuperação segura.

Quando não usar:
- Repetir erros permanentes de validação, rejeições de permissão ou mutações de resultado desconhecido sem mecanismo de reconciliação.

Implementação proposta:
- Proposta: registrar operação, parâmetros, chave idempotente quando suportada, tentativas e deadline.
- Escolher atraso aleatório entre zero e o teto crescente como uma opção de full jitter; documentar a fórmula e o limite adotados.
- Respeitar instruções válidas do serviço, como prazo de nova tentativa, dentro do orçamento global.
- Evitar retries independentes em várias camadas que multipliquem a carga.
- Enviar falhas esgotadas para análise com histórico e estado final, preservando resultados incertos como incertos.

Aplicação LAI proposta:
Proposta LAI: usar retries classificados e limitados por missão, combinando backoff com idempotência e reconciliação para preservar a intenção original.

## T228:C03 — riscos_validacao

Armadilhas:
- Timeout não demonstra que o efeito não ocorreu.
- Gerar nova chave idempotente para a mesma intenção pode duplicar a operação.
- Uma fila sem prazo mantém tarefas obsoletas indefinidamente.

Métricas sugeridas:
- Tentativas por operação; atraso acumulado; sucesso após retry; carga adicional; mensagens esgotadas; duplicações.

Testes propostos:
- Simular muitos workers falhando juntos e verificar distribuição dos horários de retry.
- Retornar erro permanente e confirmar ausência de repetição.
- Simular conclusão externa com resposta perdida e conferir consulta ao resultado antes de nova mutação.

## T228:C04 — perguntas_proveniencia

Pergunta: Backoff garante ausência de duplicação?
Resposta: Não. Ele controla o tempo entre tentativas. Evitar efeitos duplicados depende de identidade, idempotência ou consulta confiável ao resultado.

Pergunta: O número máximo de tentativas basta?
Resposta: Não. Um deadline também impede que tarefas permaneçam elegíveis quando o resultado já perdeu utilidade ou excedeu o orçamento permitido.

Pergunta: Persistir apenas o payload é suficiente?
Resposta: Não. Sem intenção, tentativa, prazo e elegibilidade, a recuperação pode repetir cedo demais ou reiniciar o orçamento.

Pergunta: O fim da lease prova que o worker parou?
Resposta: Não. Pode haver pausa ou isolamento de rede; resultados tardios precisam ser avaliados pela geração e pela identidade da operação.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T228:C05 — mecanismo_avancado

Uma fila de retries persistente precisa distinguir elegibilidade temporal e posse temporária do item. Após crash do consumidor, uma lease expira e outro pode assumir; o consumidor antigo ainda pode terminar tarde. Persistir attempt e next_attempt_at sem identidade de intenção e geração de execução não impede duplicatas. Um item cujo prazo acabou deve sair da fila elegível com motivo, em vez de circular indefinidamente.

Condição de contorno:
Backoff correto em memória não sobrevive reinício se o próximo instante e o orçamento não forem persistidos.

Contrato proposto:
- Entradas: Operação repetível, erro, intenção, deadline e próxima elegibilidade.
- Saídas: Item reagendado, atribuído ou encerrado com resultado verificável.
- Estado: Tentativas, lease, geração, payload versionado e recibos.
- Invariante: Cada posse reconhece a geração vigente; reentrega conserva a intenção lógica original.

Compromissos de projeto:
- Leases curtas recuperam consumidores mortos cedo e aumentam disputa com tarefas lentas.
- Leases longas reduzem troca indevida e atrasam retomada após crash.

## T228:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: derrubar o consumidor após executar a operação e antes de confirmar a fila; a nova tentativa deve reconciliar ou repetir de modo idempotente, sem criar outro efeito.

Plano de avaliação proposto:
Comparar fila volátil e durável com crashes em diferentes pontos. Medir trabalhos perdidos, duplicados, atraso de elegibilidade e prazo excedido. Validar semântica de entrega e efeito separadamente.

Comparações:
- T163 (complements): Backoff calcula atraso; a fila conserva o calendário e o estado entre processos.
- T243 (complements): Reentrega de efeito incerto exige reconciliação antes de tratar o item como novo.

Afirmação rastreável:
Temporal distingue política de retry por atividade e limites por tentativas e duração total.
Suporte: direct; fontes: V3C-S023
Limite: A fila genérica descrita nesta ficha é proposta; não herda automaticamente as garantias do serviço Temporal.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T228:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava elegibilidade temporal e posse do item. A expansão define fila de recuperação com causa persistida, política de expiração e controle de tráfego para impedir que repetição atrasada execute intenção já obsoleta.

Item é tentativa de intenção
Persista intenção, argumentos, causa da falha, tentativa atual e próximo horário. Um novo consumo do item não cria nova operação lógica. A fila deve saber se houve envio anterior e se o efeito está desconhecido; nesse caso, a próxima ação pode ser consulta de reconciliação, não repetição da chamada original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V2A-S012.

Validade ao consumir
Antes de executar, verifique prazo, versão do objetivo e estado atual da dependência. A tarefa pode ter sido cancelada, substituída ou concluída por resposta tardia enquanto aguardava. Retirar da fila por obsolescência é um resultado legítimo e deve ser distinguido de sucesso da operação; não execute trabalho vencido só porque chegou sua vez.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V3C-S023.

Fila de erro final
Depois do orçamento ou de falha permanente, mova o item para estado terminal com diagnóstico e evidências. Reprocessar manualmente exige nova decisão com identidade e política explícitas; despejar todos os itens de volta pode reproduzir o incidente. A fila precisa de métricas por idade e causa, não apenas profundidade total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S009.

USO AVANÇADO — Integração intermitente
Cenário: Tarefas de agentes dependem de um serviço com falhas temporárias.
Estratégia: Agende tentativas persistentes com backoff e limite de carga. Quando o serviço volta, libere itens por capacidade e prioridade, revalidando os mais antigos. Se o serviço informa espera mínima, preserve essa orientação ao reiniciar o consumidor.
Papel do modelo pequeno: 3–7B prepara argumentos; runtime controla agenda e limite global.
Aceite proposto: Proposta: nenhuma avalanche após recuperação e nenhum item executado além de seu prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, C-S028.

USO AVANÇADO — Publicação de patches
Cenário: Uma entrega fica sem confirmação após falha de rede.
Estratégia: Enfileire reconciliação pelo ID do candidato, não outra publicação cega. Se o candidato já foi publicado, confirme e feche; se há base nova, volte à validação; se a operação está ausente com evidência suficiente, repita com a mesma intenção quando o contrato permitir.
Papel do modelo pequeno: 8–14B interpreta divergência; 15–30B replaneja patch incompatível.
Aceite proposto: Proposta: uma publicação efetiva por intenção e nenhuma aprovação de base antiga.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidores de tarefas tipadas, com tentativa e prazo fornecidos pelo controlador.
8–14B: Diagnóstico de erros permanentes e classificação de necessidade de reparo.
15–30B: Decisões de replanejamento e reprocessamento excepcional, com evidência e orçamento.
Requisitos de treino/runtime: Fila persistente, exclusão por geração, políticas de retenção e resultado terminal rastreável.
Não aplicar quando: Não reenfileirar indefinidamente um item impossível nem confundir lease com exatamente uma vez.

## T228:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Filas atrasadas e reparação apoiam retomada, sem provar uma política única de backoff exponencial.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AWS apoia retries seguros e Conductor mostra coordenação operacional. A composição desta fila é proposta e não foi contada como recurso exato de todos esses sistemas.
Consultas registradas: V4C-Q001, V4C-Q003, V4C-Q019.

## T228:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T228 → T163 [complements]
Como combinar: A política de backoff calcula elegibilidade, e a fila persiste o instante entre reinícios.
Interface: Tentativa, atraso, deadline e orçamento remanescente.
Condição: Classificação permite repetição e capacidade admite consumo.
Aceite proposto: Reinício não antecipa a próxima tentativa nem zera contador.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T228 → T243 [complements]
Como combinar: Itens com efeito desconhecido executam reconciliação antes de decidir reenvio.
Interface: Chave, recibo e resultado observado.
Condição: Destino oferece correlação suficiente ou mantém estado desconhecido.
Aceite proposto: Evitar duplicação após entrega confirmada tardiamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Consumidor antigo pode terminar depois de perder posse; validar geração no commit local.
- Fila menor pode significar descarte indevido; medir resultados por causa de saída.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare recuperação e amplificação com mesma carga e falhas injetadas. O porte do modelo não determina segurança de reprocessamento; o contrato da fila e do destino determina.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T243, T220, T225

## Fontes primárias associadas

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

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

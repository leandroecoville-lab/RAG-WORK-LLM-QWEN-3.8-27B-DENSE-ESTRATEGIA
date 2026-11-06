# T163 — Backoff exponencial com jitter

**Nome canônico:** Exponential backoff with jitter  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T163  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Backoff com Jitter; exponential backoff with jitter; recuo exponencial aleatório

## T163:C01 — conceito

Backoff exponencial com jitter aumenta o intervalo de novas tentativas e adiciona aleatoriedade para distribuir retornos de clientes após falhas transitórias. O crescimento é limitado por um teto, número de tentativas e prazo global. A política controla pressão sobre dependências; não corrige erros permanentes e não torna operações com efeitos seguros para repetição.

Como funciona:
- Classificar a falha e verificar se a operação admite retry dentro do prazo restante.
- Calcular um limite exponencial, por exemplo b_n = min(teto, base × 2^n), com índice inicial documentado.
- Aplicar uma variante definida de jitter; em full jitter, sortear atraso entre zero e b_n, sem sincronizar todos os clientes.

## T163:C02 — aplicacao

Quando usar:
- Erros transitórios de rede, sobrecarga e indisponibilidade temporária quando houver chance concreta de recuperação.

Quando não usar:
- Para repetir credenciais inválidas, entrada malformada ou escrita cujo resultado anterior é desconhecido e não pode ser reconciliado.

Implementação proposta:
- Proposta: definir timeout por tentativa, deadline global e orçamento total de retries; não recomeçar o prazo a cada falha.
- Honrar Retry-After quando aplicável. Se a espera exigida ultrapassar o deadline, encerrar ou reprogramar conforme contrato, sem antecipar a tentativa.
- Coordenar a política em uma camada responsável; retries independentes em cliente, gateway e ferramenta multiplicam carga.
- Persistir attempt, next_attempt_at e idempotency_key em filas duráveis, mantendo a intenção original em todas as tentativas.

Aplicação LAI proposta:
Proposta LAI: usar uma política única e rastreável por operação, integrada à fila e ao circuit breaker, sem declarar sucesso quando todas as tentativas acabarem.

## T163:C03 — riscos_validacao

Armadilhas:
- Usar geradores com semente igual em várias réplicas pode recriar sincronização.
- Um teto por atraso não limita sozinho o tempo total nem a quantidade de chamadas.

Métricas sugeridas:
- Tentativas por operação, taxa de recuperação, atraso acumulado, amplificação de tráfego e deadlines excedidos.

Testes propostos:
- Teste proposto: simular muitos clientes contra falha temporária e verificar dispersão dos horários de retry.
- Injetar erro permanente, Retry-After longo e resposta perdida após escrita; conferir classificação, término e reconciliação.

## T163:C04 — perguntas_proveniencia

Pergunta: Jitter é somar sempre o mesmo atraso?
Resposta: Não. Exige variação aleatória segundo uma distribuição definida; um deslocamento fixo mantém clientes sincronizados.

Pergunta: Posso repetir uma escrita após timeout?
Resposta: Só com garantia adequada de idempotência ou reconciliação. Timeout não informa se o servidor já aplicou o efeito.

Pergunta: Um teto de atraso limita a duração total?
Resposta: Não. Faltam quantidade de tentativas, duração das chamadas, filas e deadline global.

Pergunta: Quota de retries também atrasa a primeira chamada?
Resposta: No mecanismo documentado, não; essa quota limita repetições, e admissão inicial pertence a outro controle.

Escopo das fontes:
AWS fundamenta backoff, jitter e idempotência; RFC 9110 fundamenta Retry-After. Fórmula e testes são receita proposta.

## T163:C05 — mecanismo_avancado

O atraso entre tentativas deve caber junto do tempo da próxima execução no deadline restante. Somar apenas os sleeps subestima a duração total quando cada tentativa leva tempo para falhar. Uma quota de retries adiciona um limite compartilhado de trabalho em falha; ela é diferente do teto de tentativas por chamada. O SDK AWS consultado usa esse tipo de quota e distingue políticas por modalidade e geração do comportamento.

Condição de contorno:
Quando a falha é permanente, esperar mais apenas posterga a mesma rejeição; quando o efeito é incerto, repetir pode ser semanticamente incorreto.

Contrato proposto:
- Entradas: Erro classificado, tentativa, deadline, sinal do servidor e quota de retries.
- Saídas: Próximo instante elegível ou término por orçamento ou erro não repetível.
- Estado: Contador, reserva de tentativa, atraso sorteado e tempo já consumido.
- Invariante: Nova tentativa não começa sem orçamento para seu custo esperado e identificação da intenção.

Compromissos de projeto:
- Janelas maiores reduzem pressão e prolongam recuperação de falhas breves.
- Quota compartilhada protege a dependência e pode negar retries a requisições que individualmente ainda teriam saldo.

## T163:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: cada tentativa demora quase todo o timeout e depois falha; exigir que o prazo global impeça uma sequência que o teto de sleeps permitiria.

Plano de avaliação proposto:
Comparar backoff isolado e backoff com quota global sob incidentes iguais. Medir amplificação de chamadas, recuperação, prazo excedido e dispersão de tentativas. Fixar política de classificação e separar falhas transitórias de permanentes.

Comparações:
- T164 (complements): Retry-After adiciona uma orientação temporal do servidor.
- T228 (complements): Uma fila durável persiste elegibilidade e orçamento entre reinícios.

Afirmação rastreável:
AWS documenta um token bucket de quota que pode encerrar retries quando a capacidade de repetição se esgota.
Suporte: direct; fontes: V3C-S010
Limite: A página distingue comportamento recente com opt-in; não foi assumida configuração efetiva de nenhum SDK LAI.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T163:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 integrava deadline, jitter e quota. Esta camada coordena retries entre camadas, diferencia falha temporária de progresso impossível e propõe controle de amplificação por missão.

Dono único da repetição
Escolha qual camada repete cada tipo de falha e faça as demais exporem suas tentativas. Se SDK, ferramenta e agente repetem independentemente, a multiplicação pode ocorrer antes que o coordenador veja um erro. Propague limite restante e informação de tentativa para impedir que uma nova chamada do agente renove artificialmente todo o orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S010.

Classificação antes de esperar
Backoff é útil quando tempo pode mudar a probabilidade de sucesso. Argumento inválido, schema incompatível ou capacidade ausente exigem correção ou término, não atraso exponencial. Uma rejeição de quota deve considerar o escopo da quota e sinais do servidor; uma falha de transporte após envio pode exigir reconciliação do efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, C-S026.

Estabilidade da recuperação
Após uma falha generalizada, milhares de chamadas podem voltar juntas. Jitter distribui tentativas, mas não cria capacidade. Combine admissão e limite de retries com a carga útil; recuperação sustentada deve preservar espaço para novas requisições, evitando que o trabalho de reparação ocupe permanentemente todo o serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, V3C-S009.

USO AVANÇADO — Ferramenta externa intermitente
Cenário: Agentes pequenos dependem de uma API com erros transitórios.
Estratégia: Execute a chamada com política central; devolva ao modelo resultado final classificado, incluindo se houve efeito possível. Não peça ao modelo para dormir e repetir por conta própria. Quando a quota de retries acabar, registre pendência ou alternativa compatível.
Papel do modelo pequeno: 3–7B reconhece a classe devolvida; código implementa timers e limites.
Aceite proposto: Proposta: limitar amplificação observada e manter sucesso útil durante degradação controlada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012.

USO AVANÇADO — CI compartilhada saturada
Cenário: Revisores tentam consultar builds que ainda estão executando.
Estratégia: Distinga polling normal de falha de transporte. Aumente o intervalo de consulta conforme duração esperada e respeite eventos quando disponíveis. Repetir o disparo do build não é substituto de consultar seu estado; use ID estável e deadline da campanha.
Papel do modelo pequeno: 8–14B resume falhas de build; 15–30B escolhe mudança de estratégia após evidência suficiente.
Aceite proposto: Proposta: nenhuma duplicação de build e queda no volume de consultas sem atrasar detecção além da tolerância.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Receber estados de falha tipados, sem delegação de controle temporal.
8–14B: Sugerir correção de argumentos quando erro é permanente e há evidência explícita.
15–30B: Planejar fallback ou redução de escopo após orçamento central esgotado.
Requisitos de treino/runtime: Timers monotônicos, contabilidade por tentativa, política do SDK conhecida e propagação do deadline.
Não aplicar quando: Não repetir efeito potencialmente realizado sem identidade ou procedimento de reconciliação.

## T163:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: Backoff e jitter são descritos como mecanismos utilizados nos clientes.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SDK AWS fornece caso operacional de retry com quota. O controlador de missão e polling adaptado para agentes é composição proposta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T163:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T163 → T167 [complements]
Como combinar: SDK AWS usa bucket para limitar tentativas adicionais e conter recuperação agressiva.
Interface: Saldo de retry e classificação da falha.
Condição: Separar quota de retry de admissão inicial.
Aceite proposto: Sob falha sustentada, retries ficam limitados pela política compartilhada.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V2A-S012. Casos: V4C-C002.

2. T163 → T164 [complements]
Como combinar: Interpretar Retry-After como restrição temporal adicional antes da nova tentativa.
Interface: Tempo mínimo anunciado e deadline restante.
Condição: A operação continua elegível para repetição.
Aceite proposto: Não dormir além do prazo nem ignorar orientação válida do destino.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contabilizar tentativas internas do SDK para não ocultar amplificação.
- Esgotar retry deve produzir estado final explícito; não reiniciar o mesmo loop com nome diferente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare qualidade após falhas com mesmo orçamento de tentativas. Um agente pequeno pode obter maior disponibilidade pela engenharia do runtime, sem superar o modelo de fronteira no problema original.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T162, T164, T228, P013

## Fontes primárias associadas

### C-S027 — Timeouts, retries, and backoff with jitter

[https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retries limitados, timeouts e jitter reduzem amplificação de falhas transitórias.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

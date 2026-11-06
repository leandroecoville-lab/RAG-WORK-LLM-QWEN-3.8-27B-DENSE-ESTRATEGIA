# T165 — Half-open — estado do Circuit Breaker

**Nome canônico:** Estado half-open do circuit breaker  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T165  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Half-Open Circuit Breaker; circuito parcialmente aberto; sondagem de recuperação do circuito

## T165:C01 — conceito

Half-open é o estado de sondagem de um circuit breaker após um período aberto. Uma quantidade limitada de solicitações testa a recuperação antes de restaurar o fluxo normal. A ficha preserva esse subcomponente com identidade própria para detalhar regras de operação, sem apresentá-lo como mecanismo independente que substitui o circuito completo.

Como funciona:
- Quando o critério de transição for atingido, sair de open para half-open com quota restrita de chamadas.
- Contabilizar sucessos, falhas e latência das sondagens na dependência protegida.
- Fechar o circuito quando o limiar documentado for satisfeito; reabrir diante de falha que indique recuperação insuficiente.

## T165:C02 — aplicacao

Quando usar:
- Dependências que voltam gradualmente e precisam de tráfego de teste antes de receber a carga completa.

Quando não usar:
- Como substituto de health checks abrangentes, correção da dependência ou confirmação de integridade de operações pendentes.

Implementação proposta:
- Proposta: definir quota de sondagens por destino, limite de simultaneidade, timeout e contador de sucessos exigidos.
- Quando houver muitas réplicas, coordenar a quota ou explicitar que o limite é local; um limite por processo pode multiplicar o tráfego global.
- Classificar cancelamento, erro do cliente e falha da dependência separadamente, evitando fechar o circuito com amostra inadequada.
- Usar sondagens representativas e seguras; se envolverem escrita, conservar a mesma disciplina de idempotência das demais chamadas.

Aplicação LAI proposta:
Proposta LAI: expor closed/open/half-open por dependência, com transições registradas e limiares configuráveis avaliados sob falhas controladas.

## T165:C03 — riscos_validacao

Armadilhas:
- Abrir todas as filas ao primeiro sucesso pode derrubar novamente um serviço que recuperou apenas capacidade parcial.
- Um ping superficial pode funcionar enquanto a operação principal continua falhando.

Métricas sugeridas:
- Sondagens simultâneas, taxa e latência de sucesso, tempo em half-open e número de reaberturas após fechamento.

Testes propostos:
- Teste proposto: simular recuperação parcial e confirmar que a quota se mantém enquanto chamadas normais continuam limitadas.
- Fazer uma sondagem falhar e verificar retorno a open, reinício do intervalo e ausência de vazamento de chamadas pendentes.

## T165:C04 — perguntas_proveniencia

Pergunta: Half-open quer dizer liberar metade das requisições?
Resposta: Não. O nome identifica um estado; a quota de teste é definida pela implementação e pode ser apenas uma chamada.

Pergunta: Um sucesso basta para fechar o circuito?
Resposta: Somente se essa for a política validada. Pode ser necessário exigir vários sucessos representativos e condições de latência aceitáveis.

Pergunta: Um sucesso antigo prova recuperação atual?
Resposta: Não. É necessário saber em qual fase e condições a operação foi iniciada e se é representativa da sondagem vigente.

Pergunta: Uma sonda por processo significa uma sonda global?
Resposta: Não. Com várias réplicas, a carga pode multiplicar; o escopo da quota deve ser declarado.

Escopo das fontes:
O padrão Microsoft fundamenta os três estados. Coordenação entre réplicas e aceite LAI são propostas operacionais.

## T165:C05 — mecanismo_avancado

Sondas precisam pertencer à geração correta do estado do circuito. Uma chamada lenta iniciada antes da abertura pode terminar com sucesso durante uma sondagem posterior; usá-la para fechar o circuito confunde evidência antiga com recuperação atual. Uma proposta associa epoch à transição e contabiliza apenas resultados elegíveis daquela fase. Em várias réplicas, a quota efetiva é a soma das sondagens locais, salvo coordenação explícita.

Condição de contorno:
Sondas que exercitam somente uma operação leve não comprovam recuperação da operação que causou a abertura.

Contrato proposto:
- Entradas: Destino, geração do circuito, quota de sondas e critérios de recuperação.
- Saídas: Sonda admitida ou rejeitada e transição fundamentada em resultado vigente.
- Estado: Epoch, sondas em voo, sucessos válidos e prazo de observação.
- Invariante: Resultado atrasado de geração anterior não fecha o circuito atual.

Compromissos de projeto:
- Coordenação global limita rajadas e acrescenta dependência operacional.
- Sondas representativas fornecem evidência melhor e podem custar mais ao serviço ainda frágil.

## T165:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar uma chamada antiga, reabrir o circuito e entregar seu sucesso durante novo half-open; exigir que a resposta obsoleta não determine fechamento.

Plano de avaliação proposto:
Comparar sondagem simples e identificação por geração com falhas intermitentes. Medir fechamento prematuro, carga de sondas e tempo até recuperação sustentável. Escolher critérios pela capacidade que a operação realmente necessita.

Comparações:
- T138 (specializes): Half-open detalha a fase de recuperação da máquina de estados completa.
- T227 (distinct_from): Probe de readiness do processo não substitui sonda da operação protegida.

Afirmação rastreável:
Polly descreve sondagem após o período aberto e transição conforme o resultado, separada de retries.
Suporte: direct; fontes: V3C-S026
Limite: Epochs e coordenação entre réplicas são extensão editorial proposta, não recurso presumido de toda biblioteca.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T165:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 introduzia gerações e limites de sondagem. A expansão escolhe sondas representativas, separa recuperação parcial e explica por que sucesso superficial não autoriza reabrir toda a carga.

Sonda de capacidade real
Uma chamada de saúde barata pode passar enquanto a operação principal continua falhando. Defina uma sonda que exercite o caminho relevante com efeito controlado, ou use uma requisição real elegível sob quota pequena. Diferencie conectividade, aceitação e conclusão semântica; cada evidência sustenta uma transição diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, V3C-S026.

Circuitos por classe
Serviços podem recuperar leitura antes de escrita, ou aceitar prompts curtos enquanto rejeitam contextos grandes. Um circuito único simplifica operação e pode bloquear trabalho saudável; fragmentar demais causa sondas excessivas. Escolha classes com falhas correlacionadas demonstráveis e limite o total agregado de sondas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3C-S009.

Retorno graduado
Ao observar recuperação, aumente carga em etapas com critérios de recuo. Não confunda uma amostra bem-sucedida com capacidade para a fila acumulada. Defina quantos resultados elegíveis, em qual janela e sob qual carga sustentam a decisão; esses valores são parâmetros de operação a calibrar, não constantes da técnica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V2A-S012.

USO AVANÇADO — Provedor de inferência oscilante
Cenário: O endpoint responde a saúde, mas chamadas longas falham.
Estratégia: Separe classes por contrato de entrada quando a evidência justificar. Use poucas solicitações representativas e acompanhe resultado completo, incluindo parser e prazo. Se a classe curta recuperar, libere apenas essa classe enquanto contextos extensos continuam em espera ou fallback.
Papel do modelo pequeno: 3–7B pode servir tarefa curta local; controlador decide abertura e elegibilidade.
Aceite proposto: Proposta: nenhuma reabertura global baseada em sonda inadequada e limite de carga durante recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026.

USO AVANÇADO — Ferramenta de escrita remota
Cenário: Após incidente, é necessário testar uma API com efeitos.
Estratégia: Prefira consulta que verifique a dependência crítica ou uma operação idempotente de teste aprovada. Não use criação repetida de objetos reais como sonda genérica. Se não houver teste seguro representativo, uma requisição real limitada precisa de reconciliação explícita.
Papel do modelo pequeno: 8–14B classifica resposta; 15–30B analisa alternativas de fluxo sem gerar sondas arbitrárias.
Aceite proposto: Proposta: recuperação detectada sem efeitos duplicados ou objetos órfãos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atuar como fallback delimitado; não calcular a saúde do circuito por impressão textual.
8–14B: Agrupar sintomas por tipo de operação e apoiar diagnóstico de recuperação parcial.
15–30B: Propor reorganização do fluxo enquanto circuitos específicos continuam indisponíveis.
Requisitos de treino/runtime: Epoch do circuito, limites globais de sondas, contadores por classe e telemetria de resultado completo.
Não aplicar quando: Não sondar efeitos irreversíveis sem contrato adequado nem usar sucesso de outra geração para fechar o circuito.

## T165:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Resilience4j documenta o estado; AWS/SRE apoiam limites de recuperação. A seleção semântica de sondas para agentes é proposta.
Consultas registradas: V4C-Q001, V4C-Q004.

## T165:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T165 → T138 [complements]
Como combinar: O estado half-open fornece evidência para a transição controlada do breaker.
Interface: Epoch, resultados elegíveis e limite de amostra.
Condição: Conclusões pertencem à geração corrente.
Aceite proposto: Sucesso tardio de chamada antiga não fecha circuito novo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T165 → T173 [complements]
Como combinar: Mantenha fallback elegível enquanto a rota principal passa por recuperação parcial.
Interface: Capacidade restaurada por classe e contrato do pedido.
Condição: Voltar à rota principal não deve reiniciar efeitos já executados.
Aceite proposto: Transferência preserva tentativa, orçamento e resultado confirmado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S001, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contar sondas de todas as réplicas, não apenas de um processo.
- Uma resposta HTTP bem-sucedida com conteúdo inválido não prova recuperação funcional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade e erro semântico sob incidentes reproduzíveis. Trocar por modelo de fronteira não corrige sondas mal escolhidas ou tempestade de reabertura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T138, T163, T227, P013

## Fontes primárias associadas

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

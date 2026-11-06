# T138 — Circuit Breaker

**Nome canônico:** Circuit Breaker  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T138  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** disjuntor de chamadas

## T138:C01 — conceito

Máquina de estados que interrompe temporariamente chamadas a uma dependência com falhas persistentes. Normalmente usa estados fechado, aberto e parcialmente aberto. Seu objetivo é limitar desperdício e permitir recuperação, sem concluir que todo erro pertence à mesma causa.

Como funciona:
- No estado fechado, observar erros e latências dentro de uma janela.
- Abrir o circuito quando o critério configurado for atingido.
- Após espera, admitir sondagens limitadas antes de restaurar o tráfego.

## T138:C02 — aplicacao

Quando usar:
- Serviço remoto degradado que recebe retries contínuos.
- Dependência cuja falha pode ocupar todos os workers.

Quando não usar:
- Erros de validação específicos do usuário que não indicam degradação do serviço.

Implementação proposta:
- Separar circuitos por destino e operação relevante.
- Definir volume mínimo de observações e limiares contra flutuação.
- Expor estado, motivo da abertura e próxima possibilidade de sondagem.

Aplicação LAI proposta:
Proposta: proteger consultas e modelos remotos da Helena para que falha externa não aprisione todo o executor.

## T138:C03 — riscos_validacao

Armadilhas:
- Misturar tenants ou operações distintas gera bloqueios desnecessários.
- Todos os clientes sondarem juntos causa nova sobrecarga na recuperação.

Métricas sugeridas:
- Tempo gasto em circuito aberto.
- Chamadas evitadas e taxa de sucesso das sondagens.

Testes propostos:
- Forçar falhas suficientes e confirmar que novas chamadas não atingem o backend.
- Recuperar a dependência e verificar reentrada gradual com concorrência limitada.

## T138:C04 — perguntas_proveniencia

Pergunta: Circuit breaker substitui timeout?
Resposta: Não. Timeout limita cada espera; o circuito controla novas tentativas após falhas.

Pergunta: Circuito aberto significa serviço definitivamente indisponível?
Resposta: Não. É uma decisão temporária baseada em observações e política.

Pergunta: Todo HTTP 4xx deve contar como indisponibilidade?
Resposta: Não. Muitos indicam erro de contrato ou autorização; a classificação deve seguir a semântica da operação e do serviço.

Pergunta: Por que 100% de falhas pode ser um sinal fraco?
Resposta: Porque pode representar uma única observação; duração da janela e tamanho da amostra mudam sua interpretação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T138:C05 — mecanismo_avancado

A chave de um circuito determina quais falhas compartilham destino operacional. Agregar todos os erros de um provedor pode interromper operações saudáveis porque apenas um recurso ou método falhou; granularidade excessiva gera amostras pequenas e estado demais. A janela de observação precisa diferenciar erro do cliente, rejeição por carga e indisponibilidade. Uma porcentagem de falhas sem volume mínimo pode oscilar violentamente em tráfego esparso.

Condição de contorno:
Circuitos não detectam bem incidentes quando as chamadas observadas não representam a operação protegida ou quando a classificação de erros está errada.

Contrato proposto:
- Entradas: Resultado da chamada, chave do circuito, instante e categoria de falha.
- Saídas: Permitir, rejeitar rapidamente ou admitir sonda, com motivo.
- Estado: Janela de resultados, transições, prazo de abertura e sondas ativas.
- Invariante: Só falhas elegíveis alimentam o critério que protege aquela dependência.

Compromissos de projeto:
- Circuitos finos isolam falhas e exigem mais dados para detectar tendência.
- Abrir cedo reduz desperdício e pode interromper um serviço que já se recuperava.

## T138:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: misturar erros de validação em uma operação e sucesso em outra no mesmo provedor; verificar que a chave e a classificação não bloqueiam indevidamente o caminho saudável.

Plano de avaliação proposto:
Comparar chave global e segmentada sob tráfego com falhas parciais. Medir requisições poupadas, bloqueios indevidos e tempo de recuperação. Ajustar janela e amostra mínima em dados de incidentes, sem adotar porcentagem universal.

Comparações:
- T165 (complements): Half-open detalha a fase de sondagem e retorno do circuito, enquanto o circuit breaker inclui todos os estados.
- T163 (complements): Backoff pode espaçar tentativas permitidas, mas não substitui a decisão de abrir o circuito.

Afirmação rastreável:
O padrão Microsoft separa bloqueio temporário de chamadas e tentativa de recuperação em estados distintos.
Suporte: direct; fontes: C-S005
Limite: Particionamento de chaves e critérios estatísticos descritos aqui são decisões de implementação propostas.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T138:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou granularidade e amostragem do circuito. A nova camada define circuitos por capacidade observável, interações com degradação e separação entre falha operacional e reprovação semântica.

Dois painéis de falha
Mantenha disponibilidade e qualidade em métricas distintas. Erros de transporte podem justificar abrir circuito; respostas incorretas precisam de avaliação por domínio e versão. Misturar ambos no mesmo contador impede saber se a rota está fora do ar ou apenas inadequada para uma classe difícil de consultas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V4C-S014.

Circuito com estado durável limitado
Persistir a decisão de bloqueio ajuda após restart, mas copiar uma janela antiga cegamente pode bloquear dependência já recuperada. Guarde tempo, versão da política e motivo; ao restaurar, reavalie a validade da observação e coordene sondas sem permitir que cada réplica faça sua própria avalanche.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3C-S028.

Recuperação sob demanda real
Uma sonda barata de saúde não representa necessariamente uma operação grande. Defina classes representativas para testar autenticação, contrato e capacidade, começando com chamadas sem efeitos. Retorno gradual deve aumentar carga apenas após resultados coerentes, com mecanismo para voltar a bloquear quando a recuperação não sustenta tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, V3D-S017.

USO AVANÇADO — Ferramenta parcialmente indisponível
Cenário: Busca funciona, mas escrita no mesmo serviço falha.
Estratégia: Abra circuito apenas para a operação afetada, conservando consultas elegíveis. Marque ações pendentes e escolha se o fluxo pode produzir uma preparação útil sem afirmar que a escrita ocorreu.
Papel do modelo pequeno: 3–14B adapta a apresentação ao estado fornecido; não decide abrir ou fechar o circuito.
Aceite proposto: Proposta: falhar somente escrita e conferir que leituras continuam e nenhum efeito é declarado concluído sem recibo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S026, C-S026.

USO AVANÇADO — Endpoint de inferência oscilante
Cenário: Uma revisão de servidor produz timeouts em contextos longos.
Estratégia: Segmente telemetria por revisão e classe de entrada; reduza tráfego da combinação problemática e preserve o caminho estável. Antes de reabilitar, execute sondas representativas sem alterar a identidade de tarefas pendentes.
Papel do modelo pequeno: 15–30B pode servir como rota alternativa apenas para requisitos comprovadamente compatíveis.
Aceite proposto: Proposta: medir oscilações, tarefas preservadas e carga de sondagem, incluindo restart simultâneo de controladores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: respostas de contingência e extração local durante bloqueio de dependências externas.
8–14B: Proposta: continuar ramos independentes e preparar ações pendentes para confirmação posterior.
15–30B: Proposta: substituir algumas inferências rejeitadas, respeitando capacidade e contexto do endpoint local.
Requisitos de treino/runtime: O estado do circuito pertence ao runtime; são necessários relógios, contadores e propagação da decisão entre réplicas.
Não aplicar quando: Não abrir circuito global por poucas respostas difíceis ou por erros permanentes dos argumentos do usuário.

## T138:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes fundamentam proteção e sondagem. Casos de quota de retry não foram apresentados como prova de circuit breaker implantado.
Consultas registradas: V4C-Q001, V4C-Q004.

## T138:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T138 → T165 [complements]
Como combinar: O retorno controlado usa sondas e admissão gradual quando a política inclui estado half-open.
Interface: Época do circuito, quota de sondas e resultado classificado.
Condição: Existe observação capaz de representar a dependência.
Aceite proposto: Testar competição entre réplicas e impedir fechamento por resposta de época antiga.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T138 → T175 [feeds]
Como combinar: O circuito informa indisponibilidade operacional ao seletor de alternativas.
Interface: Rota bloqueada, causa, escopo e próxima reavaliação.
Condição: Fallback possui capacidade independente e requisitos preservados.
Aceite proposto: Forçar falha comum a todas as rotas e exigir encerramento, não circulação infinita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Rejeitar respostas tardias que tentem fechar uma época já substituída.
- Não reutilizar sondas com efeitos de negócio irreversíveis.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare proteção operacional e conclusão correta usando servidores locais e de fronteira sujeitos às mesmas falhas. Circuit breaker não eleva competência cognitiva do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T163, T165

## Fontes primárias associadas

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V3D-S017 — Kubernetes — Liveness, readiness and startup probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Liveness e readiness produzem efeitos diferentes de reinício e elegibilidade para receber tráfego.

Limite: Não oferece por si só comprovação de progresso semântico de uma tarefa de agente.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

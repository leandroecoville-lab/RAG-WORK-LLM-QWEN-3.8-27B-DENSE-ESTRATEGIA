# T164 — Retry-After

**Nome canônico:** Retry-After  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** protocol  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T164  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cabeçalho Retry-After

## T164:C01 — conceito

Cabeçalho HTTP que orienta quanto esperar antes de uma solicitação subsequente. Pode conter uma data HTTP ou um número de segundos. É um sinal do servidor que precisa ser interpretado junto com código de resposta, contrato da API, deadline e política de repetição.

Como funciona:
- Ler o cabeçalho e identificar sua forma válida.
- Converter a indicação em instante de próxima tentativa.
- Aguardar somente se a operação puder ser repetida e o prazo total permitir.

## T164:C02 — aplicacao

Quando usar:
- Serviço informa indisponibilidade temporária.
- Resposta de quota fornece um prazo de nova tentativa segundo seu contrato.

Quando não usar:
- Usar o cabeçalho para justificar retry de ação não idempotente sem reconciliar seu estado.

Implementação proposta:
- Suportar segundos e data HTTP com parser robusto.
- Tratar relógio divergente, valor ausente e valor inválido.
- Se a espera ultrapassar o deadline, devolver status explícito em vez de continuar ocultamente.

Aplicação LAI proposta:
Proposta: o cliente HTTP da Helena interpretar o cabeçalho de forma centralizada para que cada integração não implemente uma regra diferente.

## T164:C03 — riscos_validacao

Armadilhas:
- Interpretar segundos como milissegundos causa rajada prematura.
- Repetir antes do instante sugerido aumenta bloqueios e desperdício.

Métricas sugeridas:
- Proporção de tentativas respeitando o instante indicado.
- Falhas de parsing e prazo excedido enquanto aguardava.

Testes propostos:
- Testar data futura, segundos, data passada e valor malformado.
- Fornecer espera maior que o prazo da missão e exigir término ou reagendamento explícito.

## T164:C04 — perguntas_proveniencia

Pergunta: Retry-After é sempre obrigatório na resposta 429?
Resposta: Não se deve presumir; consultar contrato do serviço e tratar sua ausência.

Pergunta: Ele autoriza nova escrita?
Resposta: Não. Só informa espera; segurança da repetição depende da operação.

Pergunta: Se a espera supera meu deadline, devo tentar imediatamente?
Resposta: Não. Isso ignora a orientação adotada; encerrar ou reagendar com prazo explícito preserva o contrato.

Pergunta: Uma data passada deve gerar espera negativa?
Resposta: Não. O parser precisa normalizar esse caso conforme política documentada, mantendo registro do valor recebido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T164:C05 — mecanismo_avancado

Um valor em segundos é relativo ao recebimento da resposta; uma data HTTP requer interpretar relógio de parede. Após calcular a espera, uma implementação pode usar relógio monotônico para evitar que ajustes locais de hora distorçam o timer. Valores inválidos, datas no passado e atrasos maiores que o deadline precisam de tratamento explícito. A orientação do servidor não transforma uma operação insegura para repetição em operação idempotente.

Condição de contorno:
Quando o prazo restante é menor que a espera solicitada, não é possível cumprir ambos; é necessário adiar a missão ou terminar essa tentativa.

Contrato proposto:
- Entradas: Status HTTP, Retry-After bruto, instante de recebimento e deadline.
- Saídas: Espera interpretada, origem do cálculo e decisão de repetir ou encerrar.
- Estado: Valor original, relógio de referência e próxima elegibilidade persistida.
- Invariante: Uma política não repete antes do intervalo que decidiu respeitar apenas para manter seu backoff local.

Compromissos de projeto:
- Respeitar o sinal reduz pressão e pode aumentar latência do cliente.
- Adicionar jitter após o instante mínimo dispersa clientes e amplia espera de alguns deles.

## T164:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: enviar segundos, data futura, data passada e valor inválido, além de alterar o relógio local durante a espera; verificar comportamento documentado e limite global.

Plano de avaliação proposto:
Comparar interpretação completa com parser apenas numérico usando respostas controladas. Medir repetições prematuras, prazo excedido e dispersão temporal. Adotar a política que preserve o contrato do serviço e a semântica da tarefa.

Comparações:
- T163 (complements): Backoff local e orientação do servidor devem formar uma única próxima elegibilidade.
- T162 (complements): Identidade da intenção permanece necessária nas operações repetidas.

Afirmação rastreável:
RFC 9110 permite Retry-After como HTTP-date ou delay-seconds e define segundos após recebimento.
Suporte: direct; fontes: C-S028
Limite: O RFC descreve semântica HTTP; jitter e integração com orçamento são políticas propostas da aplicação.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T164:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciava data HTTP, segundos e relógio monotônico. A camada nova trata Retry-After como sinal compartilhado, combinando destino, tenant e prazo sem transformar uma resposta em bloqueio global indevido.

Escopo do sinal
Associe a orientação à entidade que a resposta realmente limita: recurso, conta, endpoint ou serviço. Um único cliente que esgotou sua quota não deve congelar clientes independentes. Quando o escopo for desconhecido, use política conservadora documentada e telemetria; não deduza independência apenas por URLs diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S009.

Agenda persistente
Converta a espera em elegibilidade futura e retire o worker da execução ativa quando a pausa for longa. Persistir a próxima data evita perder a orientação após reinício. Ao retomar, reconcilie relógio e deadline; um timer antigo não prova que ainda existe orçamento ou que o resultado continua necessário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S023.

Retomada sem avalanche
O horário anunciado pode coincidir para muitos consumidores. Depois da elegibilidade mínima, uma política local de admissão distribui quem realmente envia primeiro. Acrescente atraso somente quando permitido pelo prazo; não subtraia jitter de uma espera mínima válida para antecipar chamadas que o servidor pediu para adiar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S012, C-S028.

USO AVANÇADO — Coleta de documentos com quota
Cenário: Um lote de agentes recebe limitação do mesmo serviço.
Estratégia: Agrupe o sinal por escopo confirmado, suspenda novas tentativas daquele grupo e preserve outros serviços. No retorno, libere créditos gradualmente e verifique se respostas novas atualizam a orientação. Não carregue o texto inteiro do erro repetidamente no contexto dos agentes.
Papel do modelo pequeno: 3–7B interpreta a classificação já normalizada; runtime administra calendário.
Aceite proposto: Proposta: nenhuma chamada prematura e manutenção de progresso nos destinos independentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S028, V3C-S009.

USO AVANÇADO — Missão com prazo curto
Cenário: A espera anunciada supera o tempo restante.
Estratégia: Calcule se ainda cabe executar e validar o resultado. Se não couber, produza falha de prazo ou opção compatível, sem esperar inutilmente. Uma alternativa exige quota independente e preservação das capacidades; o sinal não justifica encaminhar dados a qualquer destino disponível.
Papel do modelo pequeno: 8–14B explica a limitação; 15–30B reformula o plano dentro do escopo autorizado.
Aceite proposto: Proposta: resposta final antes do deadline e ausência de tentativas sem chance de conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V3C-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir estrutura normalizada com atraso e escopo, sem fazer aritmética crítica em texto.
8–14B: Associar operações pendentes ao destino correto e detectar pedido que ficou obsoleto.
15–30B: Planejar alternativas com qualidade e prazo explícitos quando a espera inviabiliza a missão.
Requisitos de treino/runtime: Parser conforme HTTP, relógio confiável, limites para cabeçalhos inválidos e persistência de timers longos.
Não aplicar quando: Não assumir que Retry-After garante disponibilidade no horário indicado ou torna idempotente uma operação.

## T164:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes HTTP e AWS apoiam semântica e retries; não foi encontrado relato específico de dez bigtechs operando esta composição exata em agentes.
Consultas registradas: V4C-Q001, V4C-Q004.

## T164:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T164 → T163 [complements]
Como combinar: A próxima tentativa respeita o sinal do servidor junto de backoff e orçamento local.
Interface: Elegibilidade mínima, classe da falha e tempo restante.
Condição: Todas as restrições devem permitir nova tentativa.
Aceite proposto: Datas passadas, valores inválidos e atraso excessivo têm resultados definidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S028, V2A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T164 → T175 [complements]
Como combinar: A política decide esperar ou usar destino compatível com quota independente.
Interface: Escopo da quota e matriz de alternativas.
Condição: Troca preserva contrato e não mascara o consumo anterior.
Aceite proposto: Evitar circuito entre endpoints que compartilham a mesma limitação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter espera longa em bloqueio de thread ou vaga de GPU.
- Um cabeçalho novo pode alterar a agenda; versionar o sinal para não usar timers obsoletos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sistemas por conclusão dentro do prazo e requisições desperdiçadas. Nenhum porte de modelo consegue eliminar a espera contratual apenas gerando um plano diferente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T162, T163, T175

## Fontes primárias associadas

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

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

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

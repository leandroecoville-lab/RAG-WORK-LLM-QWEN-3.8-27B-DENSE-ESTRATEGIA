# T175 — Rate Limiting com Fallback

**Nome canônico:** Rate Limiting com Fallback  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T175  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de taxa com contingência

## T175:C01 — conceito

Composição de controle de taxa e alternativas de execução. Quando a capacidade admissível do destino se esgota, a aplicação pode aguardar, usar alternativa autorizada ou falhar explicitamente. O mecanismo não deve contornar a quota contratada nem esconder uma mudança de qualidade.

Como funciona:
- Consultar orçamento de chamadas, tokens e concorrência antes da admissão.
- Comparar espera estimada com deadline e alternativas elegíveis.
- Reservar capacidade do destino escolhido e registrar a decisão.

## T175:C02 — aplicacao

Quando usar:
- Múltiplos backends autorizados com quotas diferentes.
- Picos de carga que excedem capacidade momentânea de um destino.

Quando não usar:
- Criar novas identidades ou contas para evitar controles de um serviço.

Implementação proposta:
- Manter orçamento agregado por missão e por destino.
- Respeitar Retry-After e circuito aberto antes de retentar.
- Definir se fallback pode degradar modalidade, contexto ou qualidade.

Aplicação LAI proposta:
Proposta: a Helena tratar orçamento e disponibilidade em um ponto comum, evitando que cada subagente tente trocar de provedor por conta própria.

## T175:C03 — riscos_validacao

Armadilhas:
- Todas as alternativas podem compartilhar o mesmo gargalo.
- Oscilação entre destinos aumenta custo e torna latência imprevisível.

Métricas sugeridas:
- Quotas respeitadas e volume de fallback.
- Qualidade e custo dos pedidos desviados versus pedidos originais.

Testes propostos:
- Esgotar quota do primário e confirmar que alternativa também reserva seu próprio saldo.
- Esgotar todos os destinos e exigir fila limitada ou erro explícito.

## T175:C04 — perguntas_proveniencia

Pergunta: Fallback elimina 429?
Resposta: Não. Pode redistribuir carga autorizada; o destino alternativo também tem limites.

Pergunta: Sempre é melhor trocar que esperar?
Resposta: Não. Deve considerar prazo, custo, compatibilidade e resultado esperado.

Pergunta: Uma URL nova significa uma quota nova?
Resposta: Não. A quota pode ser por conta, organização, modelo, região ou recurso compartilhado.

Pergunta: Como diferenciar fila e retry?
Resposta: Fila aguarda admissão ainda não concedida; retry repete uma tentativa que ocorreu ou falhou, com implicações diferentes de efeito e custo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T175:C05 — mecanismo_avancado

Fallback após limitação deve identificar qual quota foi atingida. Trocar de endpoint sob a mesma quota organizacional não cria capacidade adicional; pode apenas multiplicar rejeições. Uma alternativa realmente independente ainda precisa de orçamento próprio e capacidade semântica. Uma proposta mantém o estado de admissão separado da falha da ferramenta para que uma rejeição antes do envio não seja confundida com tentativa de efeito remoto.

Condição de contorno:
Quando todos os destinos pertencem à mesma restrição contratual, a ação coerente pode ser esperar ou encerrar, não circular entre URLs.

Contrato proposto:
- Entradas: Quota atingida, escopo de cobrança, destinos elegíveis e prazo restante.
- Saídas: Espera, admissão alternativa ou rejeição final fundamentada.
- Estado: Consumo por quota, rotas visitadas e próxima elegibilidade.
- Invariante: Alternativas não reutilizam o mesmo crédito nem ocultam consumo de tentativas anteriores.

Compromissos de projeto:
- Diversificar destinos melhora disponibilidade potencial e amplia complexidade de contabilidade.
- Esperar preserva consistência do backend e pode violar o prazo da tarefa.

## T175:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois endpoints compartilham uma quota esgotada e um terceiro possui contrato incompatível; exigir espera ou falha explícita, sem rota artificialmente considerada válida.

Plano de avaliação proposto:
Comparar fila e fallback sob saturação localizada e global. Medir rejeições repetidas, conclusão, custo e equidade entre clientes. Distinguir ganho por capacidade adicional real de aparente ganho por contabilização incompleta.

Comparações:
- T137 (complements): O limitador fornece motivo e escopo da rejeição.
- T173 (complements): Fallback de modelos precisa manter capacidades além de encontrar quota disponível.

Afirmação rastreável:
Google SRE trata quotas e rejeição por criticidade como controles que devem propagar pela cadeia de serviços.
Suporte: related; fontes: V3C-S009
Limite: A política de troca entre provedores é composição editorial, dependente de contratos e quotas efetivos.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T175:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia quotas compartilhadas e independentes. A expansão considera o custo marginal do fallback, reservas já consumidas e política de degradação sem transformar indisponibilidade em vazamento de orçamento.

Mapa de domínios de quota
Represente relações entre conta, organização, modelo e região. Dois destinos podem compartilhar um limite superior mesmo quando possuem quotas locais diferentes. A decisão precisa consultar o limite que realmente bloqueou o pedido; trocar rota sem essa informação pode aumentar rejeições e ocultar a causa original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V3C-S010.

Reserva antes de transferir
Adquira capacidade na alternativa antes de abandonar uma rota ainda válida, quando o protocolo permitir. Libere a reserva original apenas quando o estado do envio estiver claro. Se a primeira chamada segue executando, cobrar só a segunda subestima uso e pode ultrapassar o teto global da missão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S010, C-S026.

Degradação por contrato
Uma alternativa pode oferecer menos contexto ou ferramentas. A política deve decidir se o requisito ainda pode ser cumprido, não apenas se existe crédito. Em alguns casos, resposta parcial com evidências e pendências é melhor que forçar conclusão em rota incapaz; essa escolha precisa aparecer no estado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S001, V4C-S005.

USO AVANÇADO — Pico de consultas interativas
Cenário: O backend habitual fica limitado por taxa durante horário de pico.
Estratégia: Mantenha fila curta e calcule se o prazo ainda permite espera. Quando houver alternativa compatível com quota independente, compare custo total e latência prevista. Se o limite for global, aplique admissão ou resposta de indisponibilidade em vez de circular por endpoints equivalentes.
Papel do modelo pequeno: 3–7B local cobre apenas classes pré-validadas; pedidos complexos permanecem em fila apropriada.
Aceite proposto: Proposta: menor rejeição útil sem aumentar erro por substituição inadequada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V4C-S005.

USO AVANÇADO — Campanha de pesquisa com orçamento
Cenário: Agentes paralelos consomem quota de vários serviços.
Estratégia: Distribua créditos por destino e prioridade da pergunta. Ao receber limitação, reduza fan-out e reprograme coletas; não duplique a busca em todos os provedores por padrão. Resultados já confirmados seguem para extração enquanto fontes indispensáveis aguardam.
Papel do modelo pequeno: 8–14B aproveita evidência disponível; 15–30B decide quais lacunas justificam custo adicional.
Aceite proposto: Proposta: cobertura por pergunta e custo de tentativas rejeitadas, com prazo explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Fallback local para tarefas estritas, com teto de qualidade e capacidade medido.
8–14B: Triagem de demandas para filas diferentes sem inventar independência de quota.
15–30B: Replanejar cobertura e escopo quando limitações tornam a missão original inviável.
Requisitos de treino/runtime: Telemetria por quota, matriz de capacidades, reservas pendentes e orçamento agregado entre destinos.
Não aplicar quando: Não usar novas credenciais ou endpoints para contornar restrições de acesso ou contratos do serviço.

## T175:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Controle de sobrecarga combinado com degradação é relacionado a fallback por limite.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: SRE fornece controles de sobrecarga e degradação; a troca coordenada entre provedores é proposta, sem alegação de dez adoções específicas.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q008.

## T175:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T175 → T137 [complements]
Como combinar: O limitador informa qual escopo recusou admissão para orientar a decisão de espera ou troca.
Interface: Quota, saldo, próximo prazo elegível e motivo.
Condição: Causa da limitação é conhecida ou marcada como incerta.
Aceite proposto: Não realizar fallback circular entre destinos sob o mesmo limite.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T175 → T173 [complements]
Como combinar: Antes da troca, confirmar que o modelo alternativo preserva modalidades, ferramentas e resultado exigido.
Interface: Contrato da tarefa e capacidades efetivas.
Condição: Existe orçamento e qualidade mínima comprovada.
Aceite proposto: Alternativa incompatível é rejeitada mesmo com quota sobrando.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S001, V4C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Falha de admissão anterior ao envio não significa efeito remoto incerto.
- Cancelamento do cliente não libera automaticamente consumo no backend original.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade sob quota fixa e qualidade mínima constante. Mais respostas obtidas por remover requisitos não são ganho legítimo de capacidade para modelos pequenos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T137, T164, T173

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S004 — rate package

[https://pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limitador token bucket mantém taxa média e capacidade de rajada configuráveis.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

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

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

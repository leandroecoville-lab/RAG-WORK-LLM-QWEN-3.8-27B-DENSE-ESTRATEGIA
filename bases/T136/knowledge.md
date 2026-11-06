# T136 — Fallback Chains

**Nome canônico:** Fallback Chains  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T136  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cadeia de contingência

## T136:C01 — conceito

Cadeia de alternativas acionadas quando uma operação falha ou fica indisponível. Cada transição precisa definir erro elegível, destino, orçamento restante e semântica preservada. Fallback é um mecanismo de resiliência; trocar de fornecedor não resolve automaticamente uma resposta incorreta.

Como funciona:
- Classificar falha de transporte, limite de taxa, capacidade ou contrato.
- Selecionar a próxima alternativa permitida para aquela classe de falha.
- Encerrar com erro explícito quando nenhuma alternativa segura atende ao contrato.

## T136:C02 — aplicacao

Quando usar:
- Dependências remotas sujeitas a indisponibilidade.
- Sistemas que toleram qualidade ou funcionalidades reduzidas explicitamente definidas.

Quando não usar:
- Alternativa viola residência de dados, permissões ou efeito de negócio esperado.

Implementação proposta:
- Declarar cadeia acíclica com limite global de tentativas e tempo.
- Propagar chave de idempotência e identificador de correlação.
- Validar schema e capacidades do destino antes de refazer a operação.

Aplicação LAI proposta:
Proposta: definir alternativas explícitas para inferência e consultas da Helena, registrando quando houve degradação ou mudança de modelo.

## T136:C03 — riscos_validacao

Armadilhas:
- Fallback pode repetir efeito já concluído cuja resposta se perdeu.
- Cadeias escondidas em várias camadas multiplicam chamadas e custo.

Métricas sugeridas:
- Taxa de recuperação por tipo de falha.
- Número total de tentativas e custo extra por solicitação.

Testes propostos:
- Simular timeout após commit e exigir reconciliação antes de repetir escrita.
- Indisponibilizar todos os destinos e conferir término limitado, sem loop.

## T136:C04 — perguntas_proveniencia

Pergunta: Fallback é retry?
Resposta: Retry repete uma tentativa; fallback muda o caminho ou serviço.

Pergunta: Pode trocar de modelo sem checar ferramentas?
Resposta: Não. O destino deve cumprir o contrato necessário à etapa.

Pergunta: Por que duas alternativas podem falhar juntas?
Resposta: Porque podem compartilhar provedor, quota, banco, rede ou serviço de recuperação, embora apresentem nomes diferentes.

Pergunta: Posso substituir silenciosamente uma resposta parcialmente transmitida?
Resposta: Somente com um contrato explícito de substituição; o consumidor precisa saber qual tentativa e versão está recebendo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T136:C05 — mecanismo_avancado

Uma cadeia de alternativas precisa conservar a semântica do resultado e classificar em que momento a primeira rota falhou. Antes do envio, a troca costuma ser simples; depois de uma resposta parcial ou de um possível efeito remoto, existe estado a reconciliar. A disponibilidade de outro fornecedor não resolve essa ambiguidade. Quotas e dependências compartilhadas também tornam falhas correlacionadas: duas URLs podem terminar no mesmo serviço congestionado.

Condição de contorno:
Fallback perde utilidade quando todos os destinos compartilham o gargalo ou quando a mudança altera um requisito obrigatório.

Contrato proposto:
- Entradas: Operação, estágio da falha, destinos elegíveis e deadline global.
- Saídas: Destino escolhido, estado migrado e desfecho confirmado ou desconhecido.
- Estado: Rotas já visitadas, custos acumulados e identificadores das tentativas.
- Invariante: Nenhum ciclo reinicia o prazo ou apaga um possível efeito já enviado.

Compromissos de projeto:
- Diversidade de fornecedores reduz algumas correlações e aumenta diferenças de contrato.
- Migrar contexto integral facilita continuidade, mas custa tokens e exige preservar versões e formatos.

## T136:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o primeiro destino após produzir saída parcial e simular saturação também no segundo; a cadeia deve terminar dentro do prazo, sem fundir respostas como se fossem uma execução única.

Plano de avaliação proposto:
Comparar falha explícita, fila e fallback sob os mesmos incidentes injetados. Medir objetivos concluídos, custo ampliado, atraso e incompatibilidades semânticas. Escolher alternativas por capacidade observada e independência de falhas, não apenas pelo número de endpoints.

Comparações:
- T173 (complements): Model Fallback Controlado detalha o caso específico de troca de modelo dentro de uma cadeia geral de alternativas.
- T243 (complements): Desfechos remotos incertos exigem reconciliação antes de uma repetição equivalente.

Afirmação rastreável:
O tratamento de sobrecarga precisa considerar como os clientes reagem às rejeições para evitar ampliar o incidente.
Suporte: related; fontes: V3C-S009
Limite: A fonte de SRE apoia a dinâmica de sobrecarga; migração entre modelos é uma proposta específica desta ficha.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T136:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu falhas correlacionadas e resultados ambíguos. Aqui a cadeia vira um protocolo de degradação explícita, com classes de substituição e capacidade reservada para recuperação.

Níveis de equivalência
Classifique alternativas como equivalente de contrato, resultado degradado permitido ou impossibilidade. Trocar endpoint mantendo schema não garante a mesma cobertura factual. A camada consumidora precisa receber o nível de serviço entregue e quais requisitos foram adiados, para não usar uma resposta parcial como confirmação completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S005, V4C-S011.

Reserva em vez de migração em massa
Se todos os clientes migram simultaneamente para a alternativa, ela pode falhar pelo próprio mecanismo de recuperação. Reserve admissão para casos prioritários e limite a taxa de transferência. A fila de espera conserva prazo e intenção; não gere uma segunda fila invisível dentro de cada cliente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S009, V2A-S012.

Sessão portátil somente por contrato
A passagem entre modelos deve reconstruir mensagens, resultados de ferramentas e restrições numa representação neutra. Estado interno de raciocínio ou cache não é necessariamente transportável. Verifique o pacote no tokenizer e no formato de ferramentas do destino antes de iniciar a continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S012, V3C-S004.

USO AVANÇADO — Assistente que perde o provedor principal
Cenário: O endpoint remoto falha enquanto um modelo local continua disponível.
Estratégia: Encaminhe apenas tarefas que o local consegue atender com fontes e verificadores existentes. Para pesquisa aberta, reduza o escopo autorizado ou adie a etapa; preserve o estado confirmado e informe o que não foi concluído.
Papel do modelo pequeno: 3–30B pode manter extração, classificação e consultas locais delimitadas.
Aceite proposto: Proposta: injetar indisponibilidade e medir tarefas concluídas corretamente, degradações comunicadas e sobrecarga transferida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S005, V4C-S012.

USO AVANÇADO — Falha durante fluxo de edição
Cenário: O modelo deixa um patch parcial antes de perder conexão.
Estratégia: Congele o candidato como artefato não aceito, valide aplicabilidade e registre a base. O substituto recebe o objetivo e diferenças, podendo continuar ou descartar o candidato. Nenhuma parte é publicada apenas porque o primeiro endpoint caiu.
Papel do modelo pequeno: 8–14B recupera alterações locais; 15–30B replaneja dependências confirmadas.
Aceite proposto: Proposta: verificar que o resultado final corresponde a uma única revisão testada, sem misturar fragmentos incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: contingência para funções estreitas com saída verificável, sem assumir o papel integral do principal.
8–14B: Proposta: continuidade de subtarefas com contexto reconstruído e contratos conhecidos.
15–30B: Proposta: alternativa local mais ampla, ainda sem equivalência automática a um modelo de fronteira.
Requisitos de treino/runtime: Adapters devem preservar mensagens e erros; a reserva de capacidade precisa ser medida sob falha simultânea.
Não aplicar quando: Não usar troca automática quando o destino não oferece capacidade obrigatória ou existe efeito externo não reconciliado.

## T136:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Resposta degradada é alternativa operacional, sem ser necessariamente troca de modelo.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes mostram degradação e contratos de rotas; dez cadeias específicas de fallback LLM em produção não foram identificadas nesta busca.
Consultas registradas: V4C-Q001, V4C-Q004, V4C-Q008.

## T136:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T136 → T175 [complements]
Como combinar: A admissão da rota alternativa respeita quota própria e prioridade.
Interface: Capacidade livre, classe de degradação e orçamento restante.
Condição: A alternativa não compartilha o mesmo gargalo oculto.
Aceite proposto: Simular queda global e exigir fila limitada e motivo de rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T136 → T211 [complements]
Como combinar: Continuação entre sessões precisa transportar estado confirmado de modo legível ao novo executor.
Interface: Objetivo, artefatos, pendências e revisão da memória externa.
Condição: Handoff é suficiente para a subtarefa escolhida.
Aceite proposto: Retomar sem histórico conversacional e comparar requisitos preservados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015, V2A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não concatenar streams de modelos diferentes como uma única resposta sem revalidação.
- Limitar tentativas em toda a cadeia e conservar quem realizou cada possível efeito.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade útil e correção com a rota de fronteira em cenários de falha. Manter serviço parcial com 3–30B é um resultado distinto de paridade geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T135, T138, T162, T173, T175

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S009 — Google SRE — Handling Overload

[https://sre.google/sre-book/handling-overload/](https://sre.google/sre-book/handling-overload/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Admissão e rejeição por sobrecarga, throttling adaptativo e propagação de criticidade entre serviços.

Limite: Arquitetura de referência; classes e parâmetros operacionais do Google não são prescrições universais.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

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

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

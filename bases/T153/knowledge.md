# T153 — Output Streaming com interrupção

**Nome canônico:** Output Streaming com Interrupção  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T153  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** streaming cancelável; Output Streaming com Interrupção

## T153:C01 — conceito

Entrega incremental da resposta com possibilidade de interromper seu processamento. Diminui tempo até o primeiro conteúdo visível, mas não necessariamente o tempo total. Parar a interface, fechar a conexão e cancelar a geração no servidor são eventos diferentes e precisam ser conectados explicitamente.

Como funciona:
- Receber fragmentos identificados da resposta em andamento.
- Exibir conteúdo parcial preservando distinção entre trecho e mensagem concluída.
- Propagar cancelamento ao backend e registrar o estado final efetivamente observado.

## T153:C02 — aplicacao

Quando usar:
- Interface interativa que beneficia de resposta progressiva.
- Usuário pode corrigir objetivo antes do término da geração.

Quando não usar:
- Consumidor exige objeto completo e validado antes de qualquer uso ou efeito.

Implementação proposta:
- Implementar evento de início, fragmento, erro e término.
- Usar identificador de geração para evitar mistura após reconexão.
- Não executar comando parcial nem tratar JSON incompleto como decisão válida.

Aplicação LAI proposta:
Proposta: permitir interromper respostas da Helena sem perder estado da missão nem confirmar ações cujo resultado ainda não chegou.

## T153:C03 — riscos_validacao

Armadilhas:
- Conteúdo já exibido não pode ser desexibido por garantia técnica.
- Cancelamento local pode deixar geração consumindo recursos no servidor.

Métricas sugeridas:
- Tempo até primeiro fragmento e até término.
- Tokens gerados após pedido de interrupção e frequência de streams incompletos.

Testes propostos:
- Interromper em diferentes momentos e verificar fechamento consistente da sessão.
- Simular perda de conexão e exigir estado incompleto, sem declaração de sucesso.

## T153:C04 — perguntas_proveniencia

Pergunta: Fechar SSE garante cancelamento da LLM?
Resposta: Não. O contrato do servidor precisa oferecer e executar esse cancelamento.

Pergunta: Streaming reduz custo automaticamente?
Resposta: Não. Só pode economizar geração se ela realmente parar antes.

Pergunta: Fechar a aba prova que a geração foi cancelada?
Resposta: Não. O sinal pode não chegar ao backend; confirmação ou observabilidade do servidor é necessária para afirmar isso.

Pergunta: Posso aproveitar texto parcial após interrupção?
Resposta: Sim, se for identificado como parcial e não usado como estrutura completa ou confirmação de uma ação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T153:C05 — mecanismo_avancado

Interromper uma resposta incremental exige tratar a corrida entre último fragmento, fechamento e confirmação do cancelamento. A interface pode parar de exibir dados antes de o servidor liberar a geração. Fragmentos já recebidos também podem terminar no meio de UTF-8, de uma estrutura JSON ou de um argumento de ferramenta; a reconstrução deve usar o protocolo de framing e não presumir que cada pacote seja uma unidade semântica.

Condição de contorno:
Se o backend não oferece cancelamento verificável, o cliente pode interromper consumo sem comprovar economia imediata de computação.

Contrato proposto:
- Entradas: Stream identificado, eventos ordenados e sinal de interrupção.
- Saídas: Conteúdo confirmado, estado parcial e confirmação ou incerteza de cancelamento.
- Estado: Última sequência recebida, buffers e estado de fechamento.
- Invariante: Fragmento parcial não é promovido a ação executável sem validação completa.

Compromissos de projeto:
- Exibir cedo melhora percepção de resposta e expõe conteúdo ainda passível de revisão.
- Bufferizar até unidade válida aumenta atraso inicial e facilita consumidores estruturados.

## T153:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper durante um argumento JSON e fazer o evento final chegar após o pedido de cancelamento; exigir classificação consistente e ausência de execução do argumento incompleto.

Plano de avaliação proposto:
Comparar entrega integral e streaming sob interrupções em vários pontos. Medir tempo até conteúdo útil, trabalho após cancelamento e consistência da saída parcial. Distinguir economia observada do servidor e simples redução de exibição.

Comparações:
- T172 (complements): O controlador administra buffers, framing e estados do stream.
- T089 (distinct_from): Término por EOS ou limite é decisão de geração; interrupção do consumidor é outro evento.

Afirmação rastreável:
MCP documenta que notificações de cancelamento podem chegar após a conclusão da requisição.
Suporte: related; fontes: V3C-S005
Limite: A mesma corrida orienta o projeto de streaming, mas o transporte e a geração podem ter contratos adicionais.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T153:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu framing e corrida de cancelamento. Agora a transmissão distingue conteúdo provisório, eventos confirmados e mensagens de encerramento, preservando integridade quando o usuário interrompe uma tarefa longa.

Provisório não é confirmado
A interface pode exibir texto incremental sem permitir que outros componentes o tratem como resposta final. Use estados explícitos para rascunho, concluído e interrompido. Em objetos estruturados, só publique campos acionáveis quando o protocolo e a validação permitirem, sem executar argumentos ainda incompletos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V3C-S004.

Cancelamento em árvore
Interromper o stream deve alcançar produtor, ferramentas e subagentes conforme suas possibilidades. Cada filho devolve se parou, terminou ou possui resultado desconhecido. O controlador agrega esses estados; fechar a conexão do usuário não é prova de que a GPU, a consulta ou a operação externa foram encerradas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S005, V3C-S007.

Reutilização após interrupção
Resultados confirmados de leituras podem ser guardados para continuar depois, enquanto uma resposta parcial fica marcada como incompleta. A próxima sessão precisa receber objetivo e estado de cada operação, não apenas o último texto exibido. Assim, interromper para mudar de ideia não exige perder todo trabalho útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S030.

USO AVANÇADO — Pesquisa que o usuário redefine
Cenário: Durante a coleta, o usuário reduz o escopo da pergunta.
Estratégia: Pare novas buscas, cancele ramos desnecessários e preserve evidências dos restantes. Emita uma revisão do objetivo e monte uma nova entrega com o que continua válido. Não misture o final da resposta antiga ao início da nova.
Papel do modelo pequeno: 3–7B extrai fatos por ramo; 15–30B reavalia relevância sob o objetivo atualizado.
Aceite proposto: Proposta: medir chamadas evitadas, evidências reutilizadas e fragmentos indevidamente atribuídos à nova resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

USO AVANÇADO — Geração de patch cancelada
Cenário: A saída estava formando uma alteração quando a sessão foi interrompida.
Estratégia: Guarde o candidato como incompleto, sem aplicá-lo automaticamente. Se a edição já ocorreu por ferramenta, registre revisão e efeitos confirmados. A continuação decide entre validar, completar ou descartar, sempre contra a base atual.
Papel do modelo pequeno: 8–30B reconstrói a intenção; código distingue texto parcial de arquivo realmente alterado.
Aceite proposto: Proposta: interromper em vários pontos e exigir ausência de publicação de patch não validado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S030, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: respostas curtas com estados simples de conclusão e nenhum efeito disparado por fragmento.
8–14B: Proposta: transmissão de etapas de ferramenta com recibos separados do texto explicativo.
15–30B: Proposta: coordenação de streams de pesquisa ou edição mantendo cancelamento por ramo.
Requisitos de treino/runtime: Confirmar suporte de streaming e parser do modelo; alguns contratos de ferramentas exigem resposta completa.
Não aplicar quando: Não depender de cancelamento para desfazer um efeito externo ou recuperar memória de GPU imediatamente.

## T153:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn documenta experiência incremental; protocolos de cancelamento vêm de especificações. Não se inventou deployment que conecte todos esses detalhes.
Consultas registradas: V4C-Q010, V4C-Q013.

## T153:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T153 → T172 [feeds]
Como combinar: O controlador interpreta frames, aplica backpressure e preserva o estado terminal.
Interface: ID do stream, sequência e evento de término ou interrupção.
Condição: O consumidor reconhece revisões e duplicatas.
Aceite proposto: Injetar desconexão e impedir conclusão falsa por último fragmento recebido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T153 → T243 [complements]
Como combinar: Operações já enviadas durante o stream precisam de reconciliação separada.
Interface: Intenção, tentativa e status observado pelo destino.
Condição: O efeito pode sobreviver à conexão encerrada.
Aceite proposto: Cancelar após envio e confirmar que não há repetição cega.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar um botão de parar como confirmação do servidor.
- Liquidar custos e reservas somente conforme o estado observado das operações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare responsividade e integridade sob cancelamento em modelos pequenos e fronteira. Percepção de rapidez não equivale a menor tempo de conclusão validada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T089, T172

## Fontes primárias associadas

### C-S018 — HTML Standard — Server-sent events

[https://html.spec.whatwg.org/multipage/server-sent-events.html](https://html.spec.whatwg.org/multipage/server-sent-events.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Eventos incrementais, identificação e reconexão SSE; cancelamento de inferência depende do servidor, não da norma SSE.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S006 — Coroutines and tasks

[https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tasks concorrentes, agrupamento, timeouts e cancelamento de operações assíncronas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S005 — Model Context Protocol — Cancellation, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cancelamento é uma notificação sujeita a corridas; tarefas possuem mecanismo de cancelamento próprio nesta revisão.

Limite: Cancelar processamento não desfaz efeitos já confirmados; aplicabilidade depende da revisão negociada.

### V3C-S019 — WHATWG Streams Standard

[https://streams.spec.whatwg.org/](https://streams.spec.whatwg.org/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas, estratégias de tamanho, high-water marks, backpressure, cancelamento e propagação por pipelines.

Limite: É o modelo de streams da Web; transporte, backend de geração e durabilidade precisam de contratos adicionais.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### V3C-S007 — Go errgroup — synchronization, error propagation and cancellation

[https://pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: WithContext cancela contexto associado no primeiro erro ou retorno de Wait; SetLimit limita goroutines ativas.

Limite: Cancelamento é cooperativo; não prova cancelamento de efeito remoto e não se aplica a toda biblioteca de concorrência.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S030 — Claude Code — Checkpointing

[https://code.claude.com/docs/en/checkpointing](https://code.claude.com/docs/en/checkpointing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing distingue restauração de código, conversa e sumarização; escopo de arquivos e retenção são limitados.

Limite: Documentação consultada em 2026-11-05; não extrapolar cobertura para estado externo, todas as ferramentas ou outras versões.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

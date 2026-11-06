# T172 — Streaming Controller

**Nome canônico:** Streaming Controller  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T172  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador de streaming

## T172:C01 — conceito

Componente responsável pelo ciclo de vida de uma resposta incremental: abertura, fragmentos, buffering, backpressure, cancelamento e fechamento. Organiza a transmissão e a consistência da experiência do usuário. Não deve tratar qualquer fragmento recebido como saída final aprovada.

Como funciona:
- Associar cada stream a uma geração e consumidor identificados.
- Controlar entrega e acumulação dos fragmentos recebidos.
- Emitir término, erro ou cancelamento de forma inequívoca.

## T172:C02 — aplicacao

Quando usar:
- Interfaces de chat, voz ou acompanhamento de tarefa.
- Consumidores mais lentos que a geração de eventos.

Quando não usar:
- Usar buffer ilimitado ou ignorar desconexões do consumidor.

Implementação proposta:
- Modelar estados aberto, finalizado, falho e cancelado com transições válidas.
- Limitar buffer e definir política de pressão ou descarte admissível.
- Validar mensagem completa antes de gerar efeitos dependentes de seu conteúdo.

Aplicação LAI proposta:
Proposta: um controlador comum para saídas da Helena, separando eventos de progresso, texto ao usuário e confirmação de ferramentas.

## T172:C03 — riscos_validacao

Armadilhas:
- Reconexão pode duplicar fragmentos se não houver identificação.
- Eventos de erro depois de conteúdo parcial podem ser perdidos pela interface.

Métricas sugeridas:
- Latência até o primeiro evento e ocupação do buffer.
- Streams órfãos, duplicações e cancelamentos sem confirmação.

Testes propostos:
- Atrasar consumidor e confirmar limite de memória.
- Interromper conexão no meio do evento e verificar que não aparece resposta completa falsa.

## T172:C04 — perguntas_proveniencia

Pergunta: Streaming controller é uma técnica de LLM?
Resposta: É um componente de aplicação que coordena dados incrementais.

Pergunta: Um evento de fim significa que a tarefa inteira terminou?
Resposta: Apenas se o contrato definir e verificar essa conclusão.

Pergunta: Dez chunks garantem pouca memória?
Resposta: Não. Um chunk pode ser muito grande; a estratégia deve considerar tamanho quando memória for a restrição.

Pergunta: Fila vazia significa término?
Resposta: Não. Pode significar que o produtor está temporariamente sem dados; término requer evento ou estado explícito.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T172:C05 — mecanismo_avancado

Um controlador de streaming precisa limitar filas em uma unidade adequada. Contar fragmentos pode esconder grandes diferenças de tamanho; contar bytes aproxima memória ocupada. O high-water mark é um sinal para pressão reversa, não necessariamente uma barreira absoluta se o produtor ignora o sinal ou envia um fragmento enorme. Framing, sequência e estados de fechamento permitem distinguir atraso temporário, término normal e erro após conteúdo parcial.

Condição de contorno:
Se o produtor não coopera com pressão reversa, o controlador precisa aplicar outra política de buffer, descarte ou encerramento.

Contrato proposto:
- Entradas: Fluxo de eventos, tamanho de cada fragmento e velocidade do consumidor.
- Saídas: Fragmentos ordenados, sinais de pressão e término classificado.
- Estado: Fila com tamanho, sequência, consumidor ativo e estado de cancelamento.
- Invariante: O evento final e os erros não são descartados como se fossem fragmentos opcionais.

Compromissos de projeto:
- Buffer maior absorve diferenças de velocidade e aumenta memória e atraso acumulado.
- Buffer pequeno expõe lentidão cedo e pode reduzir throughput se o framing for muito granular.

## T172:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: desacelerar o consumidor e enviar um fragmento maior que a marca de água; verificar limitação operacional e tratamento explícito, sem crescimento indefinido da fila.

Plano de avaliação proposto:
Comparar filas por contagem e por bytes sob tamanhos variáveis. Medir pico de memória, atraso por fragmento, interrupções e integridade da sequência. Escolher estratégia conforme payload e cooperação real do backend.

Comparações:
- T153 (complements): Interrupção do usuário precisa propagar pelo controlador até a origem.
- T137 (distinct_from): Controle de fluxo entre produtor e consumidor não é a mesma política de admissão de requisições.

Afirmação rastreável:
O padrão WHATWG calcula desiredSize a partir da marca de água e do tamanho da fila para sinalizar backpressure.
Suporte: direct; fontes: V3C-S019
Limite: O produtor ainda precisa responder ao sinal; o padrão não transforma cada marca em limite físico universal.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T172:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava filas, framing e backpressure. A nova camada organiza múltiplos produtores, estado parcial e reconexão do consumidor sem confundir uma sequência de tokens com confirmação de tarefa concluída.

Canal de controle separado
Eventos de início, progresso, cancelamento, erro e conclusão precisam de semântica estável, independentemente do texto produzido. Uma mensagem final não deve ficar presa atrás de megabytes de logs opcionais. Defina priorização e retenção de eventos essenciais, sem reordenar conteúdo que depende de uma sequência anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V4C-S015.

Multiplexação identificada
Quando subagentes produzem simultaneamente, anexe origem, tarefa e sequência por fluxo. Misturar fragmentos de respostas diferentes pode formar texto plausível e impossível de auditar. O agregador pode apresentar progresso resumido, mas o consumidor precisa distinguir artefato completo de atualização parcial de outro trabalhador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, C-S030.

Reconexão com cursor
Um consumidor desconectado pode retornar depois que a tarefa avançou. Use cursor e retenção suficiente para repetir eventos necessários ou ofereça snapshot atual acompanhado do ponto de continuidade. Reentregar um evento não deve executar novamente a ação que o originou; apresentação e execução são camadas distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S019.

USO AVANÇADO — Missão assíncrona acompanhada por UI
Cenário: Pesquisa ou edição continua enquanto o usuário troca de dispositivo.
Estratégia: Persistir estado da tarefa e publicar eventos por sessão com identidade. Na reconexão, reconstruir visão atual e destacar quais resultados ainda são provisórios. Uma mudança de objetivo invalida a apresentação correspondente sem apagar evidências históricas.
Papel do modelo pequeno: 3–7B pode resumir progresso factual; o controlador não depende do texto para decidir estado.
Aceite proposto: Proposta: mesma visão final em consumidores lentos, rápidos e reconectados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

USO AVANÇADO — Ferramenta com saída extensa
Cenário: Build ou busca produz milhares de linhas enquanto o modelo espera.
Estratégia: Transmita contadores e diagnósticos selecionados, guardando o log completo como artefato. Aplique pressão reversa quando possível; se precisar truncar apresentação, preserve erro terminal e caminho para recuperar trechos. Não envie de volta ao modelo cada linha de progresso.
Papel do modelo pequeno: 8–14B extrai diagnóstico após critérios de seleção; 15–30B decide próximo passo.
Aceite proposto: Proposta: memória limitada e nenhum erro terminal perdido sob consumidor lento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S019, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Resumo de eventos tipados e pequenos; evitar interpretar fragmentos incompletos como dados finais.
8–14B: Classificação de diagnósticos e extração de erros com referências ao log.
15–30B: Integração de múltiplos fluxos por tarefa, mantendo proveniência e estados de confirmação.
Requisitos de treino/runtime: Sequência, cursor, retenção e política de buffer; resultado completo possui contrato separado de eventos intermediários.
Não aplicar quando: Não executar chamadas estruturadas enquanto argumentos ainda estão parciais ou misturados entre produtores.

## T172:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Canal por sessão e transmissão parcial são documentados, mas não todo o contrato de controle de fluxo, backpressure e cancelamento desta ficha.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C022 — Cloudflare / CDN — request collapsing
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A documentação descreve cache lock para solicitações simultâneas do mesmo asset em um data center.
Mecanismo documentado: A primeira solicitação busca a origem; as demais aguardam e recebem a resposta compartilhada. O escopo é por localização, não exclusão global de todas as chamadas.
Correspondência com esta base: A resposta é transmitida aos aguardantes, sem descrever um controlador completo de streaming LLM.
Transferência proposta para modelo pequeno: Proposta: coalescer leitura idêntica de documentos ou inferência determinística com escopo e versões iguais, separando cancelamento de um consumidor do trabalho compartilhado.
Limite: Operational_product: documentação de comportamento do serviço sem deployment específico de cliente. Cache HTTP não demonstra equivalência de respostas probabilísticas de LLM.
Fontes: V4C-S022.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Guardas controlam liberação de perguntas; não se documenta o ciclo completo do controlador, com pressão reversa e encerramento.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn descreve integração operacional de trabalho assíncrono e streaming; a implementação de cursor e retenção proposta precisa de validação própria. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q010, V4C-Q009, V4D-Q020.

## T172:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T172 → T154 [complements]
Como combinar: Proposta: combinar canal por sessão e transmissão parcial com controle explícito de fluxo e reconexão; o relato LinkedIn apoia somente as duas primeiras partes.
Interface: Sessão, tarefa e estado apresentado ao cliente.
Condição: Consumidores identificam contexto e atualização.
Aceite proposto: Troca de dispositivo não transforma progresso antigo em nova ação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T172 → T153 [complements]
Como combinar: Propagar interrupção do consumidor e registrar estado terminal sem presumir cancelamento do efeito remoto.
Interface: Pedido de cancelamento, confirmação e últimas saídas aceitas.
Condição: A ferramenta define se coopera com cancelamento.
Aceite proposto: Nenhum texto após cancelamento é apresentado como resposta confirmada inadvertidamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Fila vazia não prova término e silêncio não prova falha.
- Deduplicar eventos de apresentação sem descartar atualizações com sequência nova.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare experiência, integridade e consumo com o mesmo modelo. Streaming melhora acompanhamento e pode reduzir espera percebida sem reduzir o trabalho necessário para concluir.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T153, T159

## Fontes primárias associadas

### C-S018 — HTML Standard — Server-sent events

[https://html.spec.whatwg.org/multipage/server-sent-events.html](https://html.spec.whatwg.org/multipage/server-sent-events.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Eventos incrementais, identificação e reconexão SSE; cancelamento de inferência depende do servidor, não da norma SSE.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S019 — WHATWG Streams Standard

[https://streams.spec.whatwg.org/](https://streams.spec.whatwg.org/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas, estratégias de tamanho, high-water marks, backpressure, cancelamento e propagação por pipelines.

Limite: É o modelo de streams da Web; transporte, backend de geração e durabilidade precisam de contratos adicionais.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S022 — Default Cache Behavior — Request collapsing

[https://developers.cloudflare.com/cache/concepts/default-cache-behavior/](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache lock colapsa requisições simultâneas pelo mesmo asset em um data center e distribui a resposta aos aguardantes.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

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

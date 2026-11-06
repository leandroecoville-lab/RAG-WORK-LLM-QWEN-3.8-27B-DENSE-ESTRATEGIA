# Continuidade, programação e controle operacional

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

# T207 — Memory Stream

**Nome canônico:** Memory Stream  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T207  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** fluxo de experiências; stream de memória

## T207:C01 — conceito

Fluxo cronológico de registros de experiência usados como matéria-prima da memória do agente. Em Generative Agents, experiências podem ser recuperadas e alimentar reflexões. Um Memory Stream mantém acontecimentos e suas origens; sua seleção para o contexto é uma operação posterior, sujeita a relevância e orçamento.

Como funciona:
- Cada registro representa uma observação ou resultado identificado, com momento, origem e escopo.
- A recuperação escolhe experiências pertinentes; reflexões derivadas apontam para os registros que as sustentam.
- Correções preservam a relação com o registro anterior para evitar transformar versões conflitantes em um único fato.

## T207:C02 — aplicacao

Quando usar:
- Continuidade de depuração, histórico de decisões e recuperação de experiências entre sessões.

Quando não usar:
- Como único mecanismo de autorização ou como substituto do estado transacional de uma operação.

Implementação proposta:
- Proposta: definir um envelope com event_id, tarefa, origem, conteúdo, timestamp e referência ao artefato.
- Separar observação, inferência e decisão em tipos diferentes; deduplicar pela identidade da ocorrência.
- Armazenar o original fora do prompt e indexar trechos recuperáveis, respeitando o escopo do projeto.
- Registrar também falhas e resultados inconclusivos; aplicar retenção compatível com a necessidade de auditoria.

Aplicação LAI proposta:
Proposta LAI: manter eventos de desenvolvimento com links para testes e commits; recuperar apenas experiências relevantes à micro-missão atual.

## T207:C03 — riscos_validacao

Armadilhas:
- Uma sequência temporal não prova causalidade.
- Recontar a mesma experiência com texto diferente pode inflar artificialmente sua importância.
- Uma reflexão pode interpretar incorretamente fatos corretos.

Métricas sugeridas:
- Taxa de duplicação; cobertura de proveniência; precisão da recuperação; custo por experiência recuperada.

Testes propostos:
- Inserir dois relatos da mesma execução e verificar deduplicação sem perder origens.
- Corrigir uma observação e consultar tanto a versão atual quanto a história.
- Pedir justificativa de uma reflexão e exigir suas experiências de origem.

## T207:C04 — perguntas_proveniencia

Pergunta: Memory Stream é o mesmo que Event Sourcing?
Resposta: Não. Um fluxo de memória pode conter relatos e inferências; Event Sourcing exige eventos adequados para reconstruir estado de domínio.

Pergunta: O agente precisa reler todo o fluxo?
Resposta: Não. O fluxo pode crescer fora do contexto, enquanto a recuperação seleciona episódios e referências para a tarefa.

Pergunta: Uma memória muito acessada é mais confiável?
Resposta: Não. Acesso mede uso; confiabilidade depende de fonte, validade e correções.

Pergunta: Uma reflexão deve substituir as observações que a originaram?
Resposta: Não por padrão. Preservar o vínculo permite revisar a inferência quando uma observação for corrigida.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T207:C05 — mecanismo_avancado

O Memory Stream de Generative Agents registra descrição, criação e acesso recente. A recuperação combina relevância, importância e recência; no experimento, recência depende do último acesso, não apenas da ocorrência. Essa escolha pode reforçar memórias já recuperadas, sem torná-las mais verdadeiras. Em uma aplicação proposta, observação, inferência e decisão devem manter tipos e vínculos de origem distintos para que uma reflexão não pareça experiência diretamente observada.

Condição de contorno:
Uma linha do tempo de acesso não substitui tempo de validade dos fatos nem ordem causal de eventos externos.

Contrato proposto:
- Entradas: Registro de experiência, instante de criação, origem e tipo de evidência.
- Saídas: Memória identificada e candidatos recuperados com componentes de pontuação.
- Estado: Fluxo persistente, histórico de acesso e relações entre observações e reflexões.
- Invariante: Ler uma memória não altera silenciosamente a data ou a verdade do acontecimento descrito.

Compromissos de projeto:
- Reforçar recência de acesso mantém continuidade e pode concentrar atenção em memórias populares.
- Guardar experiências completas amplia rastreabilidade e custo de armazenamento e seleção.

## T207:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: recuperar repetidamente uma informação antiga e apresentar depois correção válida; verificar que frequência de acesso não vence automaticamente a nova evidência.

Plano de avaliação proposto:
Comparar recuperação por recência de criação, acesso e combinação com relevância em perguntas temporais rotuladas. Medir cobertura, repetição de memórias e correção de vigência. Definir pesos por tarefa, sem importar parâmetros do simulador como defaults universais.

Comparações:
- T056 (complements): Bitemporalidade acrescenta validade e registro, dimensões diferentes do acesso recente.
- T209 (distinct_from): Reflexion usa feedback de tentativas; stream registra experiências que podem alimentar diferentes mecanismos.

Afirmação rastreável:
Generative Agents combina recência, importância e relevância, armazenando criação e acesso nos objetos de memória.
Suporte: direct; fontes: A-S008
Limite: O estudo busca comportamento verossímil em simulação, não certificação factual de memória empresarial.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T207:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia observações, inferências e recência de acesso. A expansão propõe manutenção de validade, recuperação por tipo de decisão e tratamento de contradições sem transformar um fluxo de memória em registro infalível.

Evento e fato vigente
Guarde que algo foi observado em determinado momento, mas represente separadamente se continua válido. Uma mudança posterior não apaga a observação antiga; cria vínculo de substituição ou contradição. O recuperador precisa saber se a pergunta é histórica ou atual para não apresentar como vigente uma preferência ou configuração já revogada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V4C-S015.

Recuperação por finalidade
Uma lembrança útil para explicar uma decisão pode ser insuficiente para executar uma ação. Defina políticas por finalidade: evidência original para comprovar, resumo para orientar, estado confirmado para continuar. Recência e similaridade entram depois da elegibilidade por tipo e validade; acessos frequentes não elevam automaticamente a autoridade do conteúdo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3C-S028.

Memória derivada revisável
Reflexões e resumos devem apontar para os eventos que os sustentam. Se uma origem for corrigida ou retirada, marque derivados afetados para revisão. Essa linhagem impede que uma inferência sobreviva como fato isolado após sua evidência mudar. O índice de recuperação é reconstruível; não deve ser a única cópia das observações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V4C-S025.

USO AVANÇADO — Continuidade de projeto
Cenário: Um agente acompanha mudanças de arquitetura ao longo de várias sessões.
Estratégia: Registre decisões com revisão do repositório e alternativas rejeitadas. Ao retomar, recupere primeiro decisões vigentes do módulo e depois o histórico necessário para explicar exceções. Se documentação e código divergirem, abrir verificação em vez de escolher a memória mais recente por reflexo.
Papel do modelo pequeno: 3–7B extrai eventos tipados; 8–14B relaciona decisões; 15–30B resolve contradições.
Aceite proposto: Proposta: consultas históricas e atuais respondem com períodos e fontes corretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, A-S008.

USO AVANÇADO — Assistência assíncrona
Cenário: Pedidos evoluem enquanto tarefas permanecem abertas.
Estratégia: Separe mensagem recebida, interpretação e decisão confirmada. Uma atualização pode invalidar somente parte das tarefas; preserve resultados ainda compatíveis e marque quais foram produzidos sob objetivo antigo. A memória não deve sobrescrever silenciosamente o contrato de uma operação já enviada.
Papel do modelo pequeno: 8–14B classifica mudança de intenção; controlador conserva causalidade e estado externo.
Aceite proposto: Proposta: nenhum resultado antigo apresentado como resposta à revisão nova sem verificação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extração de fatos e eventos com campos obrigatórios e links de origem.
8–14B: Recuperação especializada por módulo ou tarefa, com filtro temporal e de validade.
15–30B: Síntese de conflitos apoiada em eventos originais; não criar autoridade por narrativa.
Requisitos de treino/runtime: Armazenamento de origens, IDs estáveis, índice reconstruível e política de correção de derivados.
Não aplicar quando: Não usar relevância vetorial como prova de verdade nem tratar broker de eventos como memória cognitiva pronta.

## T207:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Memória cognitiva conserva contexto, sem comprovar o mesmo algoritmo do Memory Stream.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Fluxo de eventos pode abastecer memória, mas Brooklin não implementa por isso o algoritmo cognitivo Memory Stream.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Hiring Assistant relata memória cognitiva, sem provar o algoritmo Memory Stream. Generative Agents fornece o conceito experimental; Brooklin entra apenas como família de infraestrutura.
Consultas registradas: V4C-Q010, V4C-Q020.

## T207:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T207 → P008 [complements]
Como combinar: Usar o Event Store editorial como substrato de observações, mantendo índices e inferências em camadas separadas.
Interface: Evento, origem, tempo e referências de derivação.
Condição: Retenção e correção preservam rastreabilidade.
Aceite proposto: Reconstruir índice e identificar derivados de evento corrigido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S025, A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T207 → T211 [feeds]
Como combinar: Selecionar decisões vigentes e pendências para um pacote curto de continuidade.
Interface: Memórias elegíveis, versão do objetivo e links originais.
Condição: O handoff declara o que é observado e inferido.
Aceite proposto: Sessão seguinte recupera a evidência necessária sem receber todo o fluxo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Correção precisa alcançar resumos e índices que repetem o fato anterior.
- Brooklin demonstra transporte de eventos; isso não comprova relevância, reflexão ou memória de agente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare memória estruturada com histórico bruto usando perguntas temporais e decisões verificáveis. Um modelo pequeno pode recuperar melhor quando o estado é curado, sem ganhar memória factual intrínseca.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R004, T059, T241

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S024 — Open sourcing Brooklin: Near real-time data streaming at scale

[https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso operacional de Brooklin na LinkedIn para replicação e streaming, incluindo CDC; arquitetura técnica detalhada em fonte separada.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T208 — Planner–Executor / Plan-and-Execute

**Nome canônico:** Planner–Executor / Plan-and-Execute  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T208  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** plan and execute; planejador e executor

## T208:C01 — conceito

Arquitetura que separa a formulação de um plano da execução de suas etapas. O planejador define objetivos intermediários e dependências; o executor realiza ações e devolve evidências. Uma revisão do plano incorpora resultados e obstáculos. A separação pode existir no mesmo modelo ou em processos distintos.

Como funciona:
- O plano é um conjunto versionado de etapas com precondições, resultado esperado e critério de conclusão.
- O executor recebe contexto suficiente para uma etapa, sem assumir que todo o plano permanece válido.
- Um controlador decide continuar, replanejar ou encerrar a partir de resultados observados.

## T208:C02 — aplicacao

Quando usar:
- Tarefas com várias dependências, investigação seguida de implementação ou execução distribuída entre especialistas.

Quando não usar:
- Pedidos curtos em que a preparação do plano custa mais que a ação e não reduz incerteza.

Implementação proposta:
- Proposta: gerar um plano estruturado, atribuir IDs às etapas e validar dependências antes de iniciar.
- Para cada etapa, persistir entrada, artefatos, avaliação e status; distinguir bloqueado de concluído.
- Replanejar quando uma precondição falhar, preservando o histórico de decisões e a autorização original.
- Limitar revisões sucessivas e exigir uma próxima ação verificável, em vez de planos cada vez mais longos.

Aplicação LAI proposta:
Proposta LAI: dividir alterações em investigação, patch e validação, preservando contratos entre etapas e um coordenador responsável pela conclusão global.

## T208:C03 — riscos_validacao

Armadilhas:
- Planos detalhados sobre fatos desconhecidos envelhecem rapidamente.
- Um executor pode declarar sucesso sem produzir o artefato esperado.
- Paralelismo incorreto viola dependências entre etapas.

Métricas sugeridas:
- Etapas concluídas com evidência; revisões úteis; retrabalho; custo de planejamento e integração.

Testes propostos:
- Simular dependência indisponível e verificar revisão apenas das etapas afetadas.
- Introduzir resultado que invalida uma hipótese central e exigir replanejamento explícito.
- Repetir uma conclusão recebida e impedir execução duplicada da etapa seguinte.

## T208:C04 — perguntas_proveniencia

Pergunta: Planner e executor precisam ser modelos diferentes?
Resposta: Não. São responsabilidades arquiteturais; podem usar o mesmo modelo com entradas, estados e critérios de saída separados.

Pergunta: Um plano aprovado garante que as próximas ações estão corretas?
Resposta: Não. Cada ação depende do estado atual e das evidências; mudanças relevantes exigem revisão do plano.

Pergunta: Replanejar deve zerar o histórico do executor?
Resposta: Não. O estado confirmado e as intenções concluídas precisam continuar disponíveis para evitar repetição de efeitos.

Pergunta: Qual é o retorno mínimo útil do executor?
Resposta: Resultado observado, evidência de conclusão, erro classificado e premissa afetada; apenas dizer que falhou deixa o planejador sem diagnóstico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T208:C05 — mecanismo_avancado

A fronteira entre planejador e executor deve incluir pré-condições verificáveis e dependências simbólicas. O executor não precisa receber toda a discussão que produziu o plano; precisa saber o que realizar, com quais entradas e como reconhecer sucesso. Replanejamento exige preservar a identidade das intenções já confirmadas, pois renumerar etapas e repeti-las como novas pode duplicar efeitos. Revisão do plano e tentativa de execução são eixos separados.

Condição de contorno:
A separação é pouco útil quando o planejador não recebe evidências suficientes para distinguir falha de ferramenta e falha de sua premissa.

Contrato proposto:
- Entradas: Objetivo, estado confirmado, ferramentas e resultados das etapas anteriores.
- Saídas: Plano versionado ou revisão com dependências e critérios de aceitação.
- Estado: Intenções estáveis, etapas, evidências e motivo de replanejamento.
- Invariante: Uma nova versão do plano não transforma automaticamente efeito já concluído em trabalho pendente.

Compromissos de projeto:
- Executor simples reduz custo por etapa e depende de instruções operacionais claras.
- Planejador mais frequente adapta melhor e aumenta latência e consumo de contexto.

## T208:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: confirmar uma escrita e depois invalidar uma premissa de uma etapa posterior; exigir replanejamento sem repetir a escrita confirmada.

Plano de avaliação proposto:
Comparar executor com autonomia limitada, executor reativo e plano detalhado. Controlar ferramentas e objetivos. Medir revisões, efeitos duplicados, passos descartados e custo por conclusão. Escolher separação pela quantidade de dependências que o plano consegue antecipar.

Comparações:
- T143 (complements): Plan-Then-Act descreve a ordem lógica; Planner–Executor explicita responsabilidades e contrato de retorno.
- T144 (alternative): Um agente reativo pode escolher a próxima ação sem manter dois papéis separados.

Afirmação rastreável:
LLMCompiler organiza planejamento de chamadas, despacho e execução como componentes distintos.
Suporte: direct; fontes: V3C-S002
Limite: O artigo não determina a granularidade ideal dos papéis nem garante economia em toda tarefa.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T208:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definia pré-condições e separava revisão do plano de tentativa. A camada nova organiza replanning por diagnóstico, delegação com autoridade delimitada e uma ponte explícita entre plano global e execução local adaptativa.

Plano como contrato executável
Cada etapa precisa de resultado, entradas e condição de parada. O executor pode escolher detalhes locais enquanto não muda esse contrato. Se descobrir requisito incompatível, devolve evidência e impedimento ao planejador; não altera a missão silenciosamente para transformar falha em sucesso. O plano é revisável, mas sua identidade continua rastreável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S012.

Replanejar a causa correta
Separe falha de transporte, ausência de capacidade, evidência que contradiz premissa e teste que rejeita resultado. Retry trata algumas falhas temporárias; reparo modifica uma chamada; replanejamento modifica dependências ou objetivo operacional. Uma mensagem genérica de erro impede escolher a reação adequada e incentiva o planejador a repetir a mesma ideia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V2A-S012.

Escopo de autonomia
O planejador entrega limites de ferramentas, orçamento e autoridade por etapa. O executor não herda automaticamente todas as permissões do supervisor. O retorno inclui evidências para a junção e o que ficou desconhecido. Quando um modelo maior planeja para um menor, as etapas precisam caber nas capacidades realmente testadas do trabalhador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S030.

USO AVANÇADO — Migração de API
Cenário: Um plano global define contrato novo e sequência entre consumidores.
Estratégia: Fixe a interface antes de distribuir edições. Executores fazem busca e testes locais, retornando patches com revisão base. Se vários consumidores exigirem exceção não prevista, suspenda a integração e revise a interface, preservando candidatos compatíveis.
Papel do modelo pequeno: 15–30B planeja; 3–7B edita chamadas simples; 8–14B trata diagnóstico local.
Aceite proposto: Proposta: taxa de integração correta e quantidade de etapas refeitas por premissa errada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S030.

USO AVANÇADO — Pesquisa longa
Cenário: O supervisor define questões e cada trabalhador explora uma fonte ou subtema.
Estratégia: Use plano global estável para cobertura e loop local para consultas adaptativas. O trabalhador para quando satisfaz a pergunta, esgota orçamento ou encontra contradição relevante. A síntese recebe evidências e lacunas, não uma declaração genérica de tarefa concluída.
Papel do modelo pequeno: 8–14B coleta e extrai; 15–30B revisa o plano quando fontes mudam a hipótese.
Aceite proposto: Proposta: cobertura por pergunta e custo de replanejamento, sem duplicar consultas confirmadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Etapas pequenas com ferramentas delimitadas e critérios de sucesso objetivos.
8–14B: Execução local adaptativa em domínio conhecido, devolvendo erro estruturado.
15–30B: Planejamento e integração de várias etapas; modelos de fronteira continuam elegíveis para exceções difíceis.
Requisitos de treino/runtime: Estado versionado, efeitos identificados, resultados persistidos e limites por executor.
Não aplicar quando: Não separar papéis se o custo de transferência excede a tarefa ou se faltam critérios de aceite.

## T208:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Responsabilidades de líder planejador e trabalhadores são explícitas.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Planner e executor têm responsabilidades explícitas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: LinkedIn e Claude Research sustentam combinação operacional de planejamento e execução. Bandas de parâmetros e testes propostos não foram medidos localmente.
Consultas registradas: V4C-Q010, V4C-Q012.

## T208:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T208 → T144 [complements]
Como combinar: Hiring Assistant combina planejamento com execução local baseada em ReAct.
Interface: Plano global, tarefa local e observações do executor.
Condição: O loop local respeita o escopo da tarefa delegada.
Aceite proposto: Falha de premissa volta ao supervisor com evidência.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S015. Casos: V4C-C016.

2. T208 → T237 [complements]
Como combinar: Claude Research usa liderança e trabalhadores especializados para executar partes do plano.
Interface: Pergunta, orçamento e artefato de retorno.
Condição: A tarefa permite divisão e integração verificável.
Aceite proposto: Reunir cobertura sem contar duplicatas como confirmação independente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

CONTROLES DE FALHA
- Replanejar não renova orçamento já consumido.
- Revisar números de etapas não deve criar novas identidades para efeitos já confirmados.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare divisão entre modelos e um executor de fronteira com o mesmo conjunto de ferramentas. Vantagens em campanhas decomponíveis não demonstram planejamento geral equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T213, T237

## Fontes primárias associadas

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T209 — Reflexion

**Nome canônico:** Reflexion  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T209  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reflexão episódica por feedback

## T209:C01 — conceito

Método de agentes que transforma feedback de tentativas em reflexão textual mantida em memória episódica para orientar tentativas posteriores. Reflexion aprende operacionalmente por contexto, sem atualizar os pesos do modelo nesse mecanismo. Seu diferencial é a relação entre tentativa, avaliação, reflexão e nova tentativa.

Como funciona:
- Executar a tarefa e obter feedback de um avaliador, ambiente ou teste.
- Produzir uma reflexão sobre decisões que contribuíram para o resultado, vinculando-a ao feedback concreto.
- Recuperar reflexões pertinentes na próxima tentativa e observar se a estratégia mudou de forma útil.

## T209:C02 — aplicacao

Quando usar:
- Problemas repetíveis de programação, navegação ou raciocínio com resultado avaliável e tentativas comparáveis.

Quando não usar:
- Quando repetir a tarefa pode duplicar um efeito externo irreversível ou quando não existe feedback confiável.

Implementação proposta:
- Proposta: guardar tentativa, condições iniciais, resultado e uma reflexão curta com hipótese verificável.
- Priorizar feedback de testes e ambiente sobre autoconfiança verbal; registrar contradições entre avaliadores.
- Limitar tentativas e o tamanho da memória, consolidando lições redundantes sem apagar contraexemplos.
- Avaliar a nova tentativa em casos adicionais para distinguir melhoria da simples adaptação ao teste observado.

Aplicação LAI proposta:
Proposta LAI: registrar lições de falhas de integração com a evidência original e reutilizá-las apenas em tarefas compatíveis.

## T209:C03 — riscos_validacao

Armadilhas:
- Reflexões plausíveis podem atribuir a falha à causa errada.
- Acumular conselhos incompatíveis piora a próxima decisão.
- Memória textual não equivale a treinamento paramétrico.

Métricas sugeridas:
- Reincidência do mesmo erro; melhoria entre tentativas; custo de reflexão; generalização em casos reservados.

Testes propostos:
- Fornecer erro de compilação e verificar que a reflexão menciona a evidência relevante.
- Criar feedback enganoso e exigir incerteza, em vez de uma lição categórica.
- Comparar execução com e sem memória reflexiva sob o mesmo orçamento.

## T209:C04 — perguntas_proveniencia

Pergunta: Reflexion e Self-Refine são sinônimos?
Resposta: Não. Reflexion mantém feedback reflexivo entre tentativas; Self-Refine itera geração, autocrítica e revisão de uma saída.

Pergunta: Uma reflexão correta garante a próxima solução?
Resposta: Não. Ela é orientação contextual; a nova execução continua precisando de avaliação independente e controle de efeitos.

Pergunta: Uma reflexão deve sempre orientar a próxima tarefa?
Resposta: Não. É necessário comparar escopo, condições e evidências; uma regra local pode ser incorreta fora da tentativa original.

Pergunta: Como distinguir aprendizado de repetição retórica?
Resposta: Verificar se a próxima ação muda de maneira relevante e se o erro deixa de ocorrer sob avaliação independente.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T209:C05 — mecanismo_avancado

A reflexão textual precisa preservar a ligação entre tentativa, feedback e recomendação. Um erro de ferramenta pode produzir uma lição incorreta se interpretado como falha de estratégia. Da mesma forma, passar em testes fracos pode reforçar um atalho inválido. Uma proposta trata reflexões como hipóteses procedurais com escopo e evidência, permitindo substituição quando novas tentativas contradizem a regra, sem convertê-las em verdades globais sobre o projeto.

Condição de contorno:
Sem feedback informativo ou com avaliador sistematicamente errado, acumular reflexões pode consolidar o mesmo erro em linguagem mais convincente.

Contrato proposto:
- Entradas: Trajetória referenciada, feedback verificável e objetivo da próxima tentativa.
- Saídas: Reflexão acionável, condições de aplicação e vínculo com o resultado.
- Estado: Memória de tentativas, revisões das lições e evidências contraditórias.
- Invariante: Uma recomendação registra de qual falha foi inferida e não apaga o feedback original.

Compromissos de projeto:
- Lições curtas facilitam reutilização e podem omitir condições importantes.
- Histórico amplo preserva contexto e pode consumir a janela com experiências irrelevantes.

## T209:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar feedback equivocado por falha do ambiente e depois corrigir o ambiente; verificar se a reflexão é revisada, em vez de continuar culpando uma estratégia válida.

Plano de avaliação proposto:
Comparar nova tentativa sem memória, com resumo factual e com reflexão acionável. Fixar número de tentativas e avaliador. Medir sucesso acumulado, repetição do erro e transferência indevida de lições para outros casos; incluir tarefas onde a regra aprendida não se aplica.

Comparações:
- T192 (distinct_from): Self-Refine revisa um candidato; Reflexion conserva feedback para orientar tentativas futuras.
- T204 (complements): Lições verificadas podem alimentar procedimentos, com critérios de promoção separados.

Afirmação rastreável:
O repositório dos autores implementa diferentes agentes e estratégias de reflexão em ambientes experimentais.
Suporte: direct; fontes: V3C-S029
Limite: Uma estratégia bem-sucedida em um ambiente não demonstra que toda autocrítica verbal produz aprendizado útil.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T209:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava reflexões como hipóteses procedurais. A ampliação define quando uma lição merece ser recuperada, como testar seu benefício e como impedir que feedback ruim se torne política permanente.

Separar diagnóstico e regra
Uma reflexão deve registrar o que falhou, qual observação sustenta a causa e qual mudança será tentada. Não converter um erro transitório em regra global como evitar uma ferramenta. Se a causa continua incerta, preserve hipóteses concorrentes e um teste discriminante; a reflexão útil orienta coleta de evidência, não apenas reescreve a tentativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, V3C-S032.

Validade contextual
Indexe a lição por classe de tarefa, ferramenta e versão. Uma solução de compatibilidade antiga pode se tornar contraproducente após atualização. Recuperação deve exigir correspondência de condições e permitir expiração ou revisão; manter todo conselho acumulado no prompt cria conflitos que o modelo pequeno pode não conseguir resolver.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S001, V4C-S030.

Avaliar transferência
Compare novas tarefas com e sem as reflexões candidatas usando o mesmo orçamento. Uma lição que só explica o exemplo que a gerou não demonstra generalização. Meça também efeitos negativos: correções excessivas, chamadas evitadas indevidamente e aumento de tokens. Promova a regra somente quando seu escopo e benefício forem verificáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, V3C-S032.

USO AVANÇADO — Reparo de chamadas de ferramenta
Cenário: O agente repete uma classe específica de argumento inválido.
Estratégia: Guarde erro estruturado, schema vigente e exemplo mínimo corrigido. Na próxima tarefa semelhante, recupere a regra antes de gerar argumentos. Se a falha ocorreu depois de efeito incerto, a lição deve mandar reconciliar, não simplesmente trocar o formato e reenviar.
Papel do modelo pequeno: 3–7B aplica exemplos estreitos; 8–14B diagnostica a classe; controlador verifica efeito.
Aceite proposto: Proposta: menor repetição do mesmo erro sem aumento de chamadas semanticamente incorretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, C-S026.

USO AVANÇADO — Ciclos de programação
Cenário: Uma tentativa falha num teste de comportamento.
Estratégia: Extraia a propriedade violada e formule a próxima hipótese de reparo. Preserve o teste que falhou e evite ensinar a remover a asserção. Quando o teste estava errado, corrija sua origem de requisito e registre por que a lição anterior foi invalidada.
Papel do modelo pequeno: 8–14B analisa falha local; 15–30B propõe alternativas sob testes independentes.
Aceite proposto: Proposta: resolver novos defeitos da mesma classe e detectar regressões produzidas pela lição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Lições curtas ligadas a erros tipados e condições claras de aplicação.
8–14B: Diagnóstico local e comparação de hipóteses com feedback executável.
15–30B: Síntese de regras condicionais entre tarefas, mantendo revisão e possibilidade de descarte.
Requisitos de treino/runtime: Memória de tentativas, avaliador informativo e casos reservados para medir transferência.
Não aplicar quando: Não acumular reflexões quando feedback é arbitrário ou quando só há autoconcordância do gerador.

## T209:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Foram encontrados loops de revisão em operadores, mas não comprovação de adoção exata de Reflexion nesses casos. O método permanece apoiado em pesquisa, sem inflar produção.
Consultas registradas: V4C-Q024, V4C-Q027, V4C-Q028.

## T209:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T209 → T218 [complements]
Como combinar: Repetições sem progresso disparam diagnóstico, que propõe mudança testável em vez de outro turno equivalente.
Interface: Assinatura do ciclo, observações e hipótese nova.
Condição: Existe sinal de estagnação além de mero número de passos.
Aceite proposto: A próxima tentativa altera variável relevante e seu efeito é medido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T209 → T234 [complements]
Como combinar: Guardar apenas lições promovidas e contextualizadas na memória do projeto.
Interface: Regra, escopo, origem e condição de invalidação.
Condição: A regra passou por revisão e teste de transferência.
Aceite proposto: Atualização de versão remove ou revisa orientação incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma lição eloquente pode explicar a causa errada; exigir evidência discriminante.
- Não confundir reflexão textual com atualização de pesos ou com o método formal de uma implantação não identificada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno com memória de reflexões e fronteira com o mesmo feedback. Avalie generalização em tarefas novas; mais iterações no próprio exemplo não provam aprendizado transferível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T192, T207, T217

## Fontes primárias associadas

### V2A-S001 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback linguístico, memória episódica reflexiva e revisão de tentativas sem atualizar pesos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S002 — Self-Refine: Iterative Refinement with Self-Feedback

[https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração, feedback e refinamento iterativo pelo mesmo modelo; distinção de Reflexion.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S029 — Reflexion — authors implementation and experiments

[https://github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementações, notebooks e estratégias de reflexão associadas a tipos de agente e ambientes experimentais.

Limite: Repositório de pesquisa em branch mutável; resultados publicados não foram reproduzidos nem usados como avaliação deste corpus.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T210 — Session Rotation

**Nome canônico:** Session Rotation  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T210  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** renovação de sessão; context reset com handoff

## T210:C01 — conceito

Padrão operacional de encerrar uma sessão de agente e iniciar outra usando estado persistido, referências e objetivos explícitos. A rotação reduz a dependência de um histórico extenso, mas exige reconstruir o contexto necessário. Não é um recurso universal com o mesmo comando em todos os produtos.

Como funciona:
- Escolher uma fronteira estável: etapa concluída, contexto pressionado ou mudança de especialidade.
- Persistir objetivo, revisão do código, evidências, pendências e efeitos externos ainda incertos.
- A próxima sessão valida esse pacote contra o ambiente antes de assumir a continuação.

## T210:C02 — aplicacao

Quando usar:
- Tarefas longas atravessando janelas de contexto ou execução interrompida por limites operacionais.

Quando não usar:
- No meio de uma operação externa cujo resultado não foi registrado nem pode ser reconciliado.

Implementação proposta:
- Proposta: atribuir ID ao trabalho durável e IDs próprios às sessões sucessivas.
- Gerar handoff com próximo passo, critérios de conclusão, hashes e resultados de testes, preservando autorizações relevantes.
- Iniciar a sessão seguinte lendo instruções de projeto, status do repositório e evidências recentes.
- Resolver divergências entre handoff e ambiente; impedir que duas sessões se tornem escritoras simultâneas da mesma etapa.

Aplicação LAI proposta:
Proposta LAI: permitir renovação de contexto ao terminar micro-missões, mantendo um identificador de trabalho e evidências persistentes entre sessões.

## T210:C03 — riscos_validacao

Armadilhas:
- Uma sessão nova pode repetir exploração já feita ou perder restrições.
- Um resumo desatualizado pode mencionar arquivos que mudaram.
- Rotacionar frequentemente acrescenta custo de reconstrução.

Métricas sugeridas:
- Tempo para retomar trabalho útil; reexploração; perda de requisitos; conflitos entre sessões.

Testes propostos:
- Retomar de um pacote incompleto e exigir identificação dos campos ausentes.
- Alterar o commit depois do handoff e verificar detecção da divergência.
- Interromper após envio externo e exigir reconciliação antes de repetir.

## T210:C04 — perguntas_proveniencia

Pergunta: Rotação mantém a memória interna do modelo?
Resposta: Não. A continuidade depende do material persistido e do que o novo contexto consegue recuperar.

Pergunta: É sempre melhor começar uma sessão nova?
Resposta: Não. Se o contexto atual ainda está adequado, a rotação pode aumentar custo e risco de perda de informações.

Pergunta: Encerrar a sessão cancela todos os efeitos antigos?
Resposta: Não. Operações remotas podem continuar; sua identidade e resultado devem atravessar a transferência.

Pergunta: O resumo basta para assumir a missão?
Resposta: Não quando há estado operacional. A nova sessão precisa localizar versões, pendências e critérios de conclusão verificáveis.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T210:C05 — mecanismo_avancado

Rotacionar sessões pode ser tratado como transferência de responsabilidade sobre uma versão de estado. A sessão antiga publica um ponto consistente; a nova confirma leitura e assume a geração vigente. Chamadas atrasadas da sessão anterior continuam possíveis, por isso escritas precisam ser associadas à revisão ou propriedade atual. Uma lease ajuda a detectar ausência de comunicação, mas não impede sozinha um processo antigo de escrever em serviço externo que ignora essa identidade.

Condição de contorno:
Se a sessão nova recebe apenas um resumo sem cursor, artefatos e operações pendentes, ela não consegue reconstruir o limite entre concluído e desconhecido.

Contrato proposto:
- Entradas: Estado confirmado, manifesto de transferência e geração atual da missão.
- Saídas: Sessão sucessora preparada e responsabilidade de escrita transferida.
- Estado: Geração, cursor, operações em voo e confirmação de leitura.
- Invariante: A sessão anterior não aplica atualizações obsoletas a um estado que já mudou de responsável.

Compromissos de projeto:
- Esperar drenar operações simplifica transferência e pode alongar a pausa.
- Transferir com operações pendentes reduz espera e exige reconciliação explícita.

## T210:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar uma nova sessão e entregar depois um resultado da antiga; exigir tratamento como resposta tardia vinculada à tentativa original, sem sobrescrever decisões novas.

Plano de avaliação proposto:
Comparar rotação em fronteira estável e rotação durante operação. Medir retomada correta, duplicação, perda de estado e tempo de reorientação. Aceitar a política quando preservar o mesmo objetivo e evidências sob interrupção.

Comparações:
- T211 (complements): Handoff carrega o manifesto e os pontos necessários à transferência.
- T243 (complements): Operações pendentes precisam de reconciliação após a troca de sessão.

Afirmação rastreável:
etcd fornece transações condicionais por revisão e leases que expiram na ausência de keepalive.
Suporte: related; fontes: V3C-S028
Limite: Essas primitivas apoiam coordenação; a proteção contra escritor antigo precisa alcançar cada destino de escrita.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T210:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 modelava transferência de propriedade do estado. A expansão define critérios para rotacionar, preserva contexto que não pode ser reconstruído e trata a retomada como operação verificável com custo próprio.

Motivo de rotação
Rotacione quando o histórico deixou de ajudar, a janela ficou pressionada ou uma fase terminou com fronteira clara. Reiniciar por um número fixo de turnos pode interromper raciocínio útil e aumentar reconsultas. Use sinais de ocupação e de término de fase, mantendo a decisão separada de erro de ferramenta ou falha do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S014.

Pacote de retomada testável
Antes de encerrar, publique objetivo atual, artefatos, decisões, operações pendentes e próximo passo. Faça uma leitura de validação como se fosse um novo executor: referências resolvem, revisões coincidem e pendências não parecem concluídas. O custo dessa passagem deve entrar na comparação entre sessão longa e rotação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, V4C-S030.

Fronteira entre sessões
A sessão nova assume uma geração de estado; respostas atrasadas da anterior precisam ser classificadas por tarefa e revisão. Não descarte automaticamente um resultado válido só por ser antigo, mas não o publique sem verificar compatibilidade. Operações externas em andamento continuam pertencendo à mesma intenção até reconciliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S028.

USO AVANÇADO — Campanha com modelos locais
Cenário: Um agente trabalha horas em módulos separados.
Estratégia: Rotacione após validar e persistir uma micro-missão, não no meio de uma edição ainda sem teste. A nova sessão lê o mapa geral e a memória do módulo seguinte, reabrindo arquivos atuais. Preserve decisões compartilhadas que ainda condicionam os próximos módulos.
Papel do modelo pequeno: 3–7B executa micro-missões; 15–30B supervisiona fronteiras e integração.
Aceite proposto: Proposta: continuidade correta com menos contexto ativo e sem aumento excessivo de releituras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S028.

USO AVANÇADO — Mudança de papel
Cenário: Uma sessão coletou evidências e outra fará síntese crítica.
Estratégia: Publique matriz de alegações e referências, mantendo os documentos completos acessíveis. A nova sessão recebe perguntas de comparação e lacunas, reduzindo contaminação por hipóteses prematuras do coletor. Compare resultados para detectar perda de exceções na passagem.
Papel do modelo pequeno: 8–14B coleta; 15–30B sintetiza com critérios próprios.
Aceite proposto: Proposta: cobertura preservada e detecção de contradições após rotação de papel.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Sessões por tarefa estreita, com estado externo mínimo e verificável.
8–14B: Alternar coleta e análise mantendo fontes acessíveis por referência.
15–30B: Integração entre fases, avaliando se o pacote preserva dependências relevantes.
Requisitos de treino/runtime: Manifesto de estado, versões de artefatos e controle de geração; retorno de chamada antiga não publica sozinho.
Não aplicar quando: Não usar rotação para esconder falha não resolvida ou reiniciar orçamento e contadores.

## T210:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos de planos persistidos e subagentes apoiam continuidade; não foi encontrado caso que comprove exatamente esta política de rotação como produto padronizado.
Consultas registradas: V4C-Q002, V4C-Q027.

## T210:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T210 → T211 [complements]
Como combinar: Handoff materializa o estado que a nova sessão precisa consumir.
Interface: Manifesto, revisão e operações pendentes.
Condição: Membros persistidos antes da publicação do manifesto.
Aceite proposto: Novo executor resolve referências e identifica próximo passo inequívoco.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T210 → T243 [complements]
Como combinar: Reconciliar efeitos enviados pela sessão anterior antes de novas tentativas.
Interface: Identidade da intenção e observações remotas.
Condição: A transferência mantém a mesma missão.
Aceite proposto: Nenhum efeito duplicado por tratar sessão nova como execução nova.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Resumo curto não prova completude de estado.
- Resultados tardios exigem checagem de versão e objetivo, não aceitação ou descarte automático.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sessões rotacionadas e contínuas com os mesmos modelos e custo total. A técnica pode aliviar contexto de 3–30B, mas não recompõe informação que o handoff omitiu.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T060, T243

## Fontes primárias associadas

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S006 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Claude Code programático pelo CLI ou SDK; controle explícito de entrada, saída e ciclo de execução.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T211 — Handoff File

**Nome canônico:** Handoff File  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T211  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** arquivo de passagem; arquivo de continuidade

## T211:C01 — conceito

Arquivo de transferência que descreve o estado operacional necessário para outra sessão ou agente continuar uma tarefa. Deve permitir reconstrução verificável, combinando objetivo, decisões e referências. Um handoff é uma visão organizada do trabalho; não substitui os arquivos reais, logs ou recibos de operações.

Como funciona:
- Registrar o que já foi feito, o que permanece incerto e a próxima ação justificável.
- Associar afirmações de conclusão a testes, commits ou outros artefatos observáveis.
- Manter uma versão e um ponto de referência para saber quando a descrição ficou desatualizada.

## T211:C02 — aplicacao

Quando usar:
- Transferência entre sessões, agentes ou pessoas; retomada após pausa planejada ou falha de processo.

Quando não usar:
- Como armazenamento de credenciais, despejo integral de logs ou substituto de um checkpoint executável.

Implementação proposta:
- Proposta: usar seções fixas: objetivo, escopo, estado observado, alterações, validação, pendências, riscos concretos e próximo passo.
- Incluir caminhos, revisão-base e identificadores de operações; diferenciar tentativa de confirmação.
- Escrever o arquivo atomicamente ao concluir uma etapa e preservar uma versão anterior recuperável.
- Na retomada, conferir os artefatos citados; atualizar divergências antes de seguir a recomendação.

Aplicação LAI proposta:
Proposta LAI: gerar um pacote curto de continuidade por micro-missão, incluindo estado do patch, testes efetivamente executados e efeitos ainda pendentes.

## T211:C03 — riscos_validacao

Armadilhas:
- Texto muito genérico obriga o sucessor a refazer a investigação.
- Copiar uma instrução antiga sem seu escopo pode alterar a tarefa.
- Marcar um envio como concluído sem recibo elimina informação de incerteza.

Métricas sugeridas:
- Tempo de retomada; referências resolvidas; campos obrigatórios presentes; decisões revertidas por contexto insuficiente.

Testes propostos:
- Entregar o handoff a um agente sem o histórico e pedir a próxima ação com justificativa.
- Remover um artefato citado e verificar que a retomada reporta evidência ausente.
- Injetar operação com status desconhecido e exigir consulta ao sistema externo.

## T211:C04 — perguntas_proveniencia

Pergunta: Handoff File é apenas um resumo?
Resposta: Não necessariamente. Além de síntese, contém referências, precondições e um contrato operacional para a retomada.

Pergunta: Pode afirmar que um teste passou sem seu registro?
Resposta: Deve registrar essa limitação. Uma conclusão verificável aponta para o resultado e para a revisão que foi testada.

Pergunta: Um arquivo chamado FINAL prova que está completo?
Resposta: Não. É necessário verificar os membros, suas revisões e a publicação concluída conforme o contrato.

Pergunta: O que fazer se o código mudou desde o handoff?
Resposta: Comparar revisões, identificar divergências e reconstruir o estado afetado antes de executar instruções baseadas na versão antiga.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T211:C05 — mecanismo_avancado

Um handoff pode ser organizado como manifesto de publicação: conteúdo descritivo, revisões dos artefatos, cursor de eventos e estado de operações externas. A publicação só fica pronta depois que seus membros estão persistidos. Isso evita uma transferência que aponta para arquivo ainda incompleto. Hashes identificam bytes; o manifesto também precisa explicar significado e escopo, pois integridade textual não demonstra que o documento descreve a versão vigente.

Condição de contorno:
Um handoff consistente fica obsoleto se o projeto mudar depois da publicação sem registrar uma nova versão.

Contrato proposto:
- Entradas: Objetivo atual, decisões, evidências, revisões e pendências.
- Saídas: Manifesto completo com identificação de pronto e referências resolvíveis.
- Estado: Versão de publicação, membros esperados e confirmação de persistência.
- Invariante: O marcador de pronto não antecede a gravação dos artefatos que ele declara completos.

Compromissos de projeto:
- Manifesto detalhado reduz redescoberta e exige manutenção.
- Resumo mínimo acelera leitura e pode ocultar dependências essenciais à retomada.

## T211:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper a gravação de um artefato antes de publicar o handoff; o consumidor deve rejeitar transferência incompleta, sem assumir que arquivo existente significa conteúdo final.

Plano de avaliação proposto:
Comparar retomada por conversa integral, resumo livre e manifesto com referências. Medir tempo até primeira ação correta, referências quebradas e repetição de trabalho. Usar tarefas interrompidas em pontos diferentes, com aceitação por estado esperado.

Comparações:
- T210 (complements): Rotação define a transferência; handoff fornece seu pacote verificável.
- T240 (distinct_from): Snapshot captura estado; handoff também orienta o próximo responsável e explica pendências.

Afirmação rastreável:
A Anthropic descreve artefatos persistentes de progresso e histórico Git para orientar sessões sucessivas.
Suporte: related; fontes: V2A-S004
Limite: O protocolo de publicação por manifesto é proposta editorial, apoiada também em controle de versão e persistência.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T211:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava o handoff como manifesto publicado. A expansão projeta seu conteúdo como interface entre executores, com ordem de leitura, teste de suficiência e atualização após mudanças concorrentes.

Primeira leitura orientada à ação
Organize o arquivo por objetivo vigente, estado confirmado, próximo passo e impedimentos. Histórico detalhado fica em referências. O novo executor deve saber o que pode fazer sem reinterpretar toda a conversa. Uma explicação extensa que esconde o próximo passo aumenta a chance de repetir trabalho ou partir de premissa ultrapassada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V2A-S004.

Evidência por afirmação operacional
Para cada item concluído, indique artefato e validação correspondente. Para pendência externa, registre se houve envio, confirmação ou desfecho desconhecido. Diferencie decisão aprovada, sugestão e hipótese. O handoff não precisa copiar todos os logs, mas precisa permitir reabrir a prova que justifica uma ação subsequente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V4C-S030.

Consumo e envelhecimento
O consumidor confirma a revisão lida e verifica se arquivos ou objetivo avançaram desde a publicação. Se houver diferença, faça atualização incremental ou nova passagem; não edite o manifesto antigo como se sempre tivesse descrito o estado atual. Esse cuidado preserva investigação de falhas entre sessões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S027, V3C-S028.

USO AVANÇADO — Troca de executor em programação
Cenário: Uma tarefa parcialmente concluída passa a outro agente.
Estratégia: Publique revisão base, arquivos alterados, testes realmente executados e falhas restantes. A nova sessão verifica diff e ambiente antes de editar. Se o comando de teste não foi executado, registrar explicitamente como plano, sem transformar instrução em evidência.
Papel do modelo pequeno: 3–7B pode continuar ajuste local; 8–14B diagnostica divergências; 15–30B decide replanejamento.
Aceite proposto: Proposta: retomada produz mesmo conjunto de pendências e não reverte mudanças válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S027.

USO AVANÇADO — Passagem entre coleta e relatório
Cenário: Pesquisadores encerram antes da síntese final.
Estratégia: Entregue tabela de questões, fontes consultadas, evidência encontrada e lacunas. Inclua identidade de casos para evitar contar a mesma implantação várias vezes. O sintetizador resolve referências e recusa alegações sem fonte suficiente antes de redigir a conclusão.
Papel do modelo pequeno: 8–14B prepara extrações; 15–30B integra sem herdar como fatos as interpretações do coletor.
Aceite proposto: Proposta: todas as alegações finais rastreáveis e lacunas preservadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir um próximo passo delimitado com referências pequenas e contrato de saída.
8–14B: Checar suficiência do pacote e localizar divergências entre texto e artefatos.
15–30B: Reconciliar múltiplos handoffs e dependências, mantendo autoria e versões.
Requisitos de treino/runtime: Publicação atômica do manifesto após seus membros, identificação de revisão e política para referências ausentes.
Não aplicar quando: Não usar o arquivo como prova de execução quando só contém narrativa ou comandos sugeridos.

## T211:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: Histórico e commits ajudam transferência de trabalho, sem provar handoff de agentes.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Planos versionados no harness Codex sustentam artefatos de continuidade; o schema editorial de handoff é proposta e não produto implantado demonstrado.
Consultas registradas: V4C-Q024, V4C-Q027.

## T211:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T211 → T210 [feeds]
Como combinar: O manifesto fornece o estado que permite rotacionar sessão sem depender de memória conversacional.
Interface: Objetivo, geração, artefatos e pendências.
Condição: Leitura confirmada antes de nova escrita.
Aceite proposto: Sessão seguinte distingue concluído, falho e desconhecido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T211 → T240 [complements]
Como combinar: Snapshot fornece dados de estado e o handoff explica significado e próximo passo.
Interface: Identificador do snapshot e revisão dos artefatos.
Condição: Ambos correspondem ao mesmo ponto de publicação.
Aceite proposto: Rejeitar manifesto que aponta para snapshot posterior ou incompleto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S027, V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Hash correto prova identidade de bytes, não verdade do relato.
- Um comando mencionado em histórico não deve virar teste aprovado sem registro de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare retomada por handoff e histórico bruto medindo decisões corretas e custo de reconstrução. Texto bem organizado facilita modelos pequenos, mas não elimina necessidade de verificar estado externo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T210, T234, T060

## Fontes primárias associadas

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T212 — Auto-Compact por gatilho

**Nome canônico:** Auto-Compact por gatilho  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T212  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compactação automática por limiar

## T212:C01 — conceito

Compactação acionada automaticamente por uma condição de execução, como pressão no orçamento de contexto. O histórico selecionado é transformado em representação menor, preservando informações necessárias à continuidade. O gatilho e a forma de compactar são decisões distintas; nenhum percentual único serve para todos os modelos e ferramentas.

Como funciona:
- O monitor estima contexto ocupado e reserva espaço para resposta e retorno de ferramentas.
- Ao atingir a condição, seleciona material antigo ou menos útil e cria uma representação reduzida.
- A execução prossegue com instruções relevantes, estado atual e referências ao conteúdo externo preservado.

## T212:C02 — aplicacao

Quando usar:
- Conversas extensas com crescimento previsível ou ferramentas que produzem muito texto.

Quando não usar:
- Quando não existe margem para produzir e validar a compactação ou o único registro dos fatos seria descartado.

Implementação proposta:
- Proposta: definir gatilho com margem, histerese e limite de compactações sucessivas.
- Manter objetivos, restrições, decisões abertas, evidências recentes e identificadores de operações fora do descarte indiscriminado.
- Guardar histórico original recuperável e registrar origem, revisão e conteúdo substituído.
- Validar fatos críticos após compactar; reduzir a fonte de crescimento se uma única saída imediatamente lotar o contexto novamente.

Aplicação LAI proposta:
Proposta LAI: acionar compactação em fronteiras de etapa com um núcleo de estado verificado, deixando documentos completos acessíveis por referência.

## T212:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir negações, números ou condições.
- Compactação recorrente pode produzir deriva cumulativa.
- O mecanismo disponível em Claude Code não implica configuração idêntica em Codex ou outro runtime.

Métricas sugeridas:
- Tokens antes e depois; fatos críticos preservados; frequência de compactação; custo de recuperação posterior.

Testes propostos:
- Plantar uma restrição antiga e exigir seu cumprimento após o gatilho.
- Simular retorno grande de ferramenta e testar a reserva de espaço.
- Repetir compactações e medir se os mesmos identificadores e pendências permanecem corretos.

## T212:C04 — perguntas_proveniencia

Pergunta: Auto-Compact aumenta a janela física do modelo?
Resposta: Não. Reorganiza ou reduz o conteúdo enviado, dentro dos limites suportados pelo modelo e pelo runtime.

Pergunta: O gatilho precisa usar apenas tokens?
Resposta: Não. Pode combinar tokens, fase da tarefa e crescimento previsto, desde que a regra seja observável e testável.

Pergunta: Um resumo gerado em paralelo pode substituir o histórico inteiro?
Resposta: Somente se abranger exatamente essa versão; caso contrário, é necessário preservar a cauda que chegou depois.

Pergunta: Taxa de compressão alta prova boa compactação?
Resposta: Não. É preciso medir preservação de decisões, evidências e capacidade de continuar o trabalho.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T212:C05 — mecanismo_avancado

Compactação concorrente exige definir qual prefixo do histórico foi resumido. Enquanto o resumo é produzido, novos turnos podem chegar; substituí-los junto com o prefixo causaria perda. Uma proposta prende a compactação a um cursor e combina o resumo com a cauda posterior, validando a versão antes da troca. A documentação atual da Anthropic distingue compactação sob demanda, em segundo plano e por limiar, com contratos próprios para reinserção de turnos.

Condição de contorno:
O gatilho pode disparar corretamente e o resumo ainda omitir informação necessária; controle de ocupação e qualidade da síntese são problemas separados.

Contrato proposto:
- Entradas: Histórico versionado, cursor a compactar, instruções de preservação e orçamento.
- Saídas: Resumo do intervalo, referências e cauda não resumida preservada.
- Estado: Job de compactação, base observada e turno mais recente.
- Invariante: Nenhum turno posterior ao cursor é descartado por uma síntese que não o recebeu.

Compromissos de projeto:
- Compactação em segundo plano reduz pausa e introduz corrida de versões.
- Compactar mais cedo reduz pressão e pode repetir o custo de síntese sem necessidade.

## T212:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma decisão enquanto o resumo está em produção; exigir que a decisão apareça na cauda preservada ou em nova síntese corretamente identificada.

Plano de avaliação proposto:
Comparar compactação bloqueante e concorrente com a mesma política de preservação. Medir pausa, perda de fatos, tokens finais e recomputações. Separar compressão alcançada e capacidade de retomar a tarefa.

Comparações:
- T168 (complements): O limiar suave precisa reservar espaço para executar a compactação.
- T215 (alternative): Masking remove observações antigas sem produzir uma síntese semântica delas.

Afirmação rastreável:
A documentação Anthropic diferencia compactação por limiar e sob demanda, incluindo operação em segundo plano.
Suporte: direct; fontes: V3C-S031
Limite: Os recursos consultados são específicos da API e têm condições de suporte; a proposta não presume disponibilidade local.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T212:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descrevia cursor de compactação e cauda concorrente. A expansão seleciona o que pode ser resumido, protege dependências abertas e mede o efeito da compactação sobre recuperação e término da tarefa.

Compactar por utilidade residual
Separe observações consumidas, decisões vigentes, evidências ainda necessárias e histórico de tentativas. Logs repetitivos podem ser candidatos; recibos de efeito e exceções pendentes precisam de preservação explícita. Um gatilho por ocupação inicia a análise, mas não decide sozinho quais unidades podem ser substituídas por resumo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S031.

Resumo com acesso ao original
O resumo deve indicar o intervalo coberto e referências para recuperar detalhes. Se a próxima etapa falhar por falta de informação, registre essa reconsulta como custo da política. Compressão que reduz tokens agora e exige várias releituras depois pode piorar a missão; compare custo completo e não somente tamanho do prompt seguinte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S031.

Efeito sobre comportamento
Resumir pode remover sinais de que uma abordagem já foi tentada ou de que o trabalho deve terminar. Preserve critérios de conclusão e hipóteses rejeitadas relevantes. Avalie repetição, duração e decisões após compactação, além de fidelidade textual. O mesmo modelo resumidor pode carregar o erro original para uma versão mais curta e convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S032.

USO AVANÇADO — Longa sessão de ferramentas
Cenário: O histórico cresce com buscas e saídas intermediárias.
Estratégia: Quando atingir limite suave, compactar apenas o prefixo fechado e manter observações protegidas. Valide o resumo contra obrigações pendentes antes de trocar o contexto. Se a validação falhar, use poda seletiva ou rotação com artefatos, sem insistir em resumir tudo.
Papel do modelo pequeno: 3–7B extrai estados simples; 8–14B resume trechos com schema; 15–30B revisa exceções.
Aceite proposto: Proposta: menor contexto ativo sem perda de campos necessários à próxima decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S031, V4C-S031.

USO AVANÇADO — Campanha de programação
Cenário: Várias iterações do mesmo teste ocupam a janela.
Estratégia: Guarde logs integrais fora do prompt, resuma evolução do defeito e preserve último erro completo. Compare compactação por fase com masking de observações antigas. Não adote limiar de outro operador sem medir janela, tokenizer e custo dos próprios modelos.
Papel do modelo pequeno: 8–14B acompanha estado local; controlador mede gatilho e preserva logs.
Aceite proposto: Proposta: resolução, custo e repetição de hipóteses sob as duas políticas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extração de campos estáveis pode ser mais confiável que sumarização aberta de histórico extenso.
8–14B: Resumos por episódio com referências e limites curtos, verificados antes da inserção.
15–30B: Integração de episódios e exceções; compacidade não deve apagar obrigações críticas.
Requisitos de treino/runtime: Cursor consistente, reserva para resumir e validar, contagem real de tokens e arquivo integral recuperável.
Não aplicar quando: Não aplicar limiar de 400k de um harness com janela maior a um modelo pequeno sem compatibilidade real.

## T212:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Compactação automática é configurada nos harnesses interativos.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C030 — JetBrains Research / autores / SWE-agent com políticas de contexto
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo compara estratégias de contexto em tarefas SWE-bench Verified.
Mecanismo documentado: Masking oculta observações anteriores; sumarização substitui histórico por texto sintetizado; avaliação considera resolução e custo.
Correspondência com esta base: Sumarização de trajetória é avaliada, sem provar uma política universal de gatilho de compactação.
Transferência proposta para modelo pequeno: Proposta: avaliar remoção seletiva antes de acrescentar um resumidor 3–30B, preservando observações necessárias ao próximo teste.
Limite: Pesquisa controlada não conta como produção; não generalizar comparação para todo domínio ou modelo.
Fontes: V4C-S031.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber relata compactação operacional; o estudo comparativo é pesquisa. Critérios e bandas propostos permanecem sem medição neste ambiente. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T212:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T212 → T222 [complements]
Como combinar: Harness Uber usa ocupação de contexto como gatilho de compactação; a política local precisa de margem e contagem.
Interface: Ocupação, limiar e perfil do modelo.
Condição: Janela e implementação correspondem à configuração efetiva.
Aceite proposto: Compactação ocorre antes de estourar e deixa espaço para continuidade.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

2. T212 → T215 [alternative]
Como combinar: Comparar resumo e masking para observações já consumidas, mantendo critérios iguais de tarefa e custo.
Interface: Histórico, observações protegidas e orçamento.
Condição: Ambas as políticas permitem recuperar detalhes necessários.
Aceite proposto: Escolher por resolução e consumo total, não pela sofisticação aparente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não resumir e apagar turnos que chegaram depois do cursor capturado.
- Não apresentar resultados do estudo com 32B como prova direta da faixa solicitada de até 30B.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare variantes dentro do mesmo harness antes de comparar portes. O estudo de masking mostra que estratégias simples merecem baseline, sem estabelecer uma vencedora universal.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T222, T004, T210

## Fontes primárias associadas

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T213 — Task Decomposition em micro-missões

**Nome canônico:** Task Decomposition em micro-missões  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T213  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** missões incrementais; decomposição orientada a resultado

## T213:C01 — conceito

Decomposição de um objetivo em unidades pequenas com resultado observável, fronteiras e critério de aceitação. Micro-missão é um rótulo operacional, não um tamanho padronizado. A qualidade da divisão depende de preservar dependências e permitir integração; fragmentar arbitrariamente pode aumentar o retrabalho.

Como funciona:
- Derivar unidades a partir de resultados desejados, não de um número fixo de linhas ou minutos.
- Declarar entradas, saída, dependências e responsável pela integração de cada unidade.
- Avaliar a conclusão local e depois verificar o comportamento conjunto do objetivo original.

## T213:C02 — aplicacao

Quando usar:
- Implementações extensas, auditorias por módulos e trabalho que precisa sobreviver a trocas de sessão.

Quando não usar:
- Quando a solução depende de uma mudança atômica indivisível ou a coordenação custa mais que executar diretamente.

Implementação proposta:
- Proposta: transformar a especificação em unidades com IDs e critérios de pronto verificáveis.
- Separar descoberta de implementação quando a arquitetura ainda é incerta; redividir após obter evidência.
- Executar em paralelo apenas unidades independentes, com propriedade de arquivos ou interfaces bem definida.
- Reservar uma missão de integração e registrar pendências comuns, evitando declarar o projeto pronto pela soma de status locais.

Aplicação LAI proposta:
Proposta LAI: usar missões com entrada, patch, teste e handoff explícitos, mantendo dependências visíveis para o coordenador.

## T213:C03 — riscos_validacao

Armadilhas:
- Micro-missões podem otimizar partes incompatíveis.
- Unidades pequenas demais desperdiçam contexto de inicialização.
- Subdivisão ilimitada pode ocultar falta de progresso real.

Métricas sugeridas:
- Duração e variância por unidade; retrabalho de integração; bloqueios; cobertura dos critérios globais.

Testes propostos:
- Dividir uma alteração de contrato entre produtor e consumidor e exigir uma verificação integrada.
- Remover uma dependência e conferir propagação de bloqueio.
- Tentar encerrar o projeto com uma missão sem evidência e impedir conclusão global.

## T213:C04 — perguntas_proveniencia

Pergunta: Toda micro-missão deve virar um subagente?
Resposta: Não. A divisão organiza o trabalho; delegação e paralelismo só ajudam quando há independência e contexto suficiente.

Pergunta: Qual é o tamanho correto?
Resposta: O menor que ainda produza um resultado útil e verificável sem impor coordenação excessiva ou perder contexto essencial.

Pergunta: Uma micro-missão deve caber em uma única chamada?
Resposta: Não necessariamente. A unidade útil é definida por resultado e dependências, embora orçamento e janela limitem sua execução.

Pergunta: Como reconhecer uma divisão ruim?
Resposta: Quando cada parte depende de decisões ainda mutáveis das outras e a integração exige refazer grande parte do trabalho.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T213:C05 — mecanismo_avancado

A fronteira de uma micro-missão deve reduzir dependências cruzadas e produzir um artefato testável. Dividir por número de linhas ou minutos pode cortar uma mudança no meio de seu contrato. Uma decomposição proposta distingue entradas estáveis, saídas integráveis e decisões compartilhadas que precisam ocorrer antes do fan-out. Quanto mais acoplados os resultados, maior o custo de resolver conflitos no fim.

Condição de contorno:
Quando as partes precisam alterar continuamente a mesma interface, fragmentação excessiva aumenta coordenação e retrabalho.

Contrato proposto:
- Entradas: Objetivo, dependências, interfaces e capacidade de execução.
- Saídas: Unidades com entrada versionada, saída esperada e critério de integração.
- Estado: DAG de micro-missões, responsáveis e contratos compartilhados.
- Invariante: Nenhuma unidade declara sucesso somente por produzir arquivo sem satisfazer a saída combinada.

Compromissos de projeto:
- Unidades pequenas facilitam retomada e geram mais overhead de despacho e revisão.
- Unidades maiores preservam coerência local e exigem mais contexto e tempo antes de gerar resultado verificável.

## T213:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dividir uma mudança em consumidor e produtor com contratos divergentes; verificar se a incompatibilidade é detectada na especificação compartilhada antes da integração final.

Plano de avaliação proposto:
Comparar divisão por arquivos, por funcionalidade e por dependências em tarefas equivalentes. Medir retrabalho de merge, tempo até artefato útil e custo de coordenação. Escolher granularidade pelo acoplamento observado, sem tamanho universal de micro-missão.

Comparações:
- T147 (complements): Fan-out explora independência das unidades já bem delimitadas.
- T208 (complements): Planner–Executor distribui e acompanha unidades com critérios explícitos.

Afirmação rastreável:
LLMCompiler identifica dependências para despachar funções que podem executar em paralelo.
Suporte: related; fontes: V3C-S002
Limite: A escolha de micro-missões de software amplia esse princípio; não é uma taxonomia padronizada fornecida pelo artigo.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T213:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculava micro-missões a artefatos testáveis. A expansão escolhe tamanho de unidade conforme variância e integração, cria orçamentos locais e diferencia decomposição útil de fragmentação que só multiplica mensagens.

Fronteira por invariantes
Uma micro-missão deve preservar ou transformar um conjunto claro de invariantes. Dividir um requisito entre dois agentes sem definir quem garante sua propriedade final deixa uma lacuna de responsabilidade. Prefira unidade que termine com artefato verificável e pouco estado compartilhado; decisões transversais devem ser tomadas antes da distribuição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S002.

Tamanho adaptativo
Tarefas repetitivas previsíveis podem ser agrupadas; exceções ambíguas merecem unidades menores e mais diagnóstico. Use histórico de retrabalho para ajustar tamanho, mantendo overhead de preparação e integração no cálculo. O número de parâmetros não define sozinho quantos arquivos cabem numa missão: acoplamento e clareza do teste importam mais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S014.

Orçamento herdado
Distribua tempo, tokens e tentativas a partir do teto global, reservando integração e contingência. Cada filho recebe sua parcela e não um orçamento novo completo. Ao encerrar uma unidade, devolva capacidade não usada conforme a política do controlador; não permita que a narrativa de sucesso esconda custo de subtarefas abandonadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S022.

USO AVANÇADO — Atualização de dependência
Cenário: Muitos consumidores precisam ajustar chamadas e validar comportamento.
Estratégia: Agrupe por módulo e contrato, defina revisão comum da API e produza patches separados. Execute validação local antes de integrar; uma incompatibilidade no contrato compartilhado suspende os dependentes afetados. Unidades concluídas que continuam compatíveis não precisam ser reescritas.
Papel do modelo pequeno: 3–7B faz alterações mecânicas; 8–14B diagnostica testes; 15–30B resolve contrato comum.
Aceite proposto: Proposta: custo por módulo aceito e retrabalho causado por mudanças transversais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S017, V4C-S030.

USO AVANÇADO — Pesquisa de muitas bases
Cenário: Cada tópico exige aprofundamento e fontes próprias.
Estratégia: Atribua IDs únicos, contrato de conteúdo e arquivos separados, com junção só após validação. Fontes e casos podem ser compartilhados por identidade; tópicos não devem inventar casos para preencher uma quota. Reserve etapa de revisão cruzada para detectar nomenclatura e evidência indevidas.
Papel do modelo pequeno: 8–14B extrai e estrutura; 15–30B integra relações e audita alegações.
Aceite proposto: Proposta: cobertura integral dos IDs e nenhuma duplicação artificial de casos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Unidades curtas com transformação e teste local explícitos, sem múltiplos objetivos vagos.
8–14B: Missões com algumas dependências internas e retorno estruturado de impedimentos.
15–30B: Decomposição global, integração e resolução de interfaces compartilhadas.
Requisitos de treino/runtime: Identidade estável das unidades, arquivos ou áreas de escrita separados e orçamento global observável.
Não aplicar quando: Não fragmentar trabalho cujo aceite depende de contexto indivisível sem prever integrador capaz de recuperá-lo.

## T213:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Campanhas são decompostas em aplicações e ondas de dependências.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Operador relata decompor metas em blocos de design, código, revisão e testes com planos versionados.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: Decomposição de uma feature em mudanças revisáveis inspira micro-missões.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Amazon Q e harness Codex descrevem campanhas e decomposição; o método de tamanho adaptativo é proposta e não métrica comprovada.
Consultas registradas: V4C-Q012, V4C-Q027.

## T213:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T213 → T237 [feeds]
Como combinar: Transformar unidades independentes em tarefas de subagentes com retorno verificável.
Interface: ID, entradas, dono de escrita e critério de aceite.
Condição: Dependências compartilhadas resolvidas ou explicitadas.
Aceite proposto: Integrador consegue aceitar ou rejeitar cada unidade sem adivinhar estado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T213 → T234 [complements]
Como combinar: No harness Codex, planos e conhecimento do repositório sustentam decomposição e continuidade.
Interface: Plano versionado, decisão e referências de projeto.
Condição: Documentos correspondem à revisão em trabalho.
Aceite proposto: Etapas antigas não são executadas após mudança de requisito sem revisão.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

CONTROLES DE FALHA
- Unidades pequenas demais podem consumir mais coordenação que execução.
- Uma tarefa marcada concluída sem artefato aceito continua pendente para integração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare campanha inteira, incluindo planejamento e revisão, entre decomposição com modelos pequenos e modelo de fronteira. Sucesso em tarefas atomizadas não demonstra competência equivalente em requisitos abertos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T208, T237, T218

## Fontes primárias associadas

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T214 — Tool Output Pruning

**Nome canônico:** Tool Output Pruning  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T214  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de saída de ferramentas

## T214:C01 — conceito

Redução seletiva de saídas de ferramentas antes de incluí-las no contexto. A poda pode remover linhas repetidas, campos irrelevantes ou trechos já conhecidos, mantendo acesso ao resultado original. Seu objetivo é aumentar densidade de informação sem esconder dados necessários para interpretar sucesso, falha ou alcance da consulta.

Como funciona:
- Capturar a saída completa em artefato e produzir uma visão compacta específica para o tipo de ferramenta.
- Preservar metadados como código de saída, cobertura, truncamento e localização dos detalhes omitidos.
- Permitir expansão direcionada quando o agente necessita de evidência que ficou fora da visão inicial.

## T214:C02 — aplicacao

Quando usar:
- Logs volumosos, resultados de busca, respostas JSON extensas e listagens de repositórios.

Quando não usar:
- Quando a seleção não consegue identificar campos críticos ou a saída é curta e já relevante.

Implementação proposta:
- Proposta: criar adaptadores por ferramenta, com regras determinísticas para erros, avisos e linhas representativas.
- Mostrar contagem total e omitida, além de referência estável para o original.
- Em testes, destacar falhas e contexto de stack trace; em buscas, manter arquivos, linhas e limites da pesquisa.
- Ajustar a política por tarefa, sem converter ausência na amostra em ausência no conjunto completo.

Aplicação LAI proposta:
Proposta LAI: entregar ao agente uma visão de logs com erro, resultado e ponteiros, mantendo a evidência completa para inspeção.

## T214:C03 — riscos_validacao

Armadilhas:
- Guardar apenas as primeiras linhas pode esconder o erro final.
- Filtrar por palavras-chave pode remover a causa anterior da falha.
- Poda destrutiva impede auditoria posterior.

Métricas sugeridas:
- Tokens poupados; recuperação de detalhes; erros críticos omitidos; latência adicional do adaptador.

Testes propostos:
- Colocar um erro no meio e no fim de um log e verificar sua preservação.
- Produzir saída sem resultado por limite de busca e exigir aviso de cobertura.
- Comparar decisões com saída integral e podada em casos representativos.

## T214:C04 — perguntas_proveniencia

Pergunta: Poda precisa usar outro LLM?
Resposta: Não. Seleção de campos, deduplicação e limites por seção podem ser determinísticos; um resumo por LLM é outra opção.

Pergunta: Poda e Observation Masking são iguais?
Resposta: Não. Poda seleciona partes de uma saída; masking normalmente oculta observações antigas inteiras por uma política de histórico.

Pergunta: Posso guardar só a última linha do comando?
Resposta: Somente se ela representar o resultado necessário; muitos comandos produzem avisos ou falhas relevantes antes dela.

Pergunta: Como diferenciar ausência de erro e erro removido?
Resposta: Preservar metadados de completude e critérios de seleção, além de acesso à saída original.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T214:C05 — mecanismo_avancado

Podar uma saída exige preservar sinais que determinam sua interpretação: código de retorno, alcance da consulta, paginação, truncamento e contexto do erro. Selecionar apenas linhas com sucesso pode transformar falha parcial em aparente conclusão. Uma proposta mantém um cabeçalho de proveniência e uma referência ao original, separando fatos extraídos de texto omitido. A extração deve ocorrer por unidades semânticas, como registro ou traceback completo.

Condição de contorno:
Se a informação necessária não pode ser reconhecida por regras confiáveis, poda agressiva pode custar mais em releituras que o contexto economizado.

Contrato proposto:
- Entradas: Saída original, metadados de execução, objetivo da leitura e orçamento.
- Saídas: Trechos selecionados, indicadores de completude e referência ao original.
- Estado: Hash ou versão, regra de seleção e intervalos omitidos.
- Invariante: A poda não altera sucesso, falha ou alcance sem registrar essa mudança de representação.

Compromissos de projeto:
- Filtros determinísticos são baratos e podem perder exceções inesperadas.
- Síntese por modelo capta significado e introduz custo e risco de inferência indevida.

## T214:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar a única falha no meio de milhares de linhas de sucesso e ocultar a última página; exigir preservação da falha e indicação de incompletude.

Plano de avaliação proposto:
Comparar saída integral, filtros por campos e seleção semântica em logs rotulados. Medir tokens, falhas relevantes preservadas e releituras necessárias. Aprovar redução somente se mantiver os sinais exigidos pela decisão posterior.

Comparações:
- T215 (distinct_from): Masking substitui observações antigas; pruning pode selecionar dentro de uma observação atual.
- T238 (complements): Referências por faixa permitem recuperar detalhes omitidos quando necessário.

Afirmação rastreável:
O estudo de observation masking identifica saídas de ferramentas como parte importante do crescimento de contexto de agentes de software.
Suporte: related; fontes: V2A-S003
Limite: A fonte motiva reduzir observações; o contrato de poda seletiva e seus filtros são proposta editorial.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T214:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservava proveniência, erros e paginação na poda. A expansão projeta respostas de ferramenta antes da transferência, usa seleção em duas passagens e protege dados que terão função em verificações futuras.

Projeção junto à origem
Quando o serviço suporta seleção de campos, peça somente o que a próxima decisão exige. Isso reduz rede e parsing além de tokens. A seleção precisa incluir identificador, versão e estado de completude; omitir um campo de erro pode tornar uma resposta parcial indistinguível de sucesso. Projeção é contrato, não simples corte de caracteres.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Índice seguido de detalhe
Para resultados desconhecidos, peça primeiro metadados ou índice e depois os itens relevantes. A segunda passagem custa latência e só compensa quando evita grande volume inútil. Mantenha uma reserva para buscar detalhes que surgirem como necessários; não avalie a política apenas pelos tokens do primeiro retorno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S014.

Poda orientada ao teste
Marque campos exigidos pelo critério de aceite como protegidos. Se a etapa seguinte compara versões ou verifica integridade, esses metadados não podem sair porque parecem repetitivos. Ao compactar logs, mantenha unidade semântica completa do erro e referência para o original; a seleção deve ser reprodutível para investigar omissões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S031.

USO AVANÇADO — API retorna objetos extensos
Cenário: O agente precisa de três campos de um conjunto profundo.
Estratégia: Resolva o schema, derive projeção explícita e valide que os campos obrigatórios vieram. Se o servidor não suportar projeção, armazene a resposta integral e selecione num adaptador determinístico antes de inserir no contexto. Retorno vazio exige distinguir ausência de dados e projeção incorreta.
Papel do modelo pequeno: 3–7B consome objeto curto; 8–14B propõe projeção revisada pelo contrato.
Aceite proposto: Proposta: redução de bytes e tokens sem campos críticos ausentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Diagnóstico de build
Cenário: Milhares de linhas contêm poucos erros causais.
Estratégia: Agrupe falhas por teste e preserve traceback completo do primeiro erro relevante, versão e comando executado. Deixe avisos secundários recuperáveis. Quando o reparo falhar, recupere linhas ao redor antes de inventar nova hipótese sobre log que foi ocultado.
Papel do modelo pequeno: 8–14B classifica diagnósticos; 15–30B analisa causas entre módulos.
Aceite proposto: Proposta: mesma taxa de diagnóstico correto com menos contexto e reconsultas contabilizadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir campos estritos e pequenos, preservando sinais de ausência e erro.
8–14B: Selecionar unidades relevantes com retorno de referências ao original.
15–30B: Projetar dados para decisões compostas e identificar dependências informacionais futuras.
Requisitos de treino/runtime: Schemas confiáveis, armazenamento integral quando necessário e métricas de reconsulta e omissão.
Não aplicar quando: Não podar evidência que sustenta um resultado ainda pendente de validação.

## T214:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Response Projection reduz respostas aos campos selecionados.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Code-mode mantém polling e dados intermediários fora do contexto da LLM.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Gateway Uber documenta ResponseProjection e exposição progressiva. Critérios de preservação para cada tarefa são propostas a testar. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T214:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T214 → T151 [complements]
Como combinar: OmniMCP combina descoberta progressiva e projeção de resposta para reduzir exposição desnecessária de contexto.
Interface: Schema resolvido e lista de campos solicitados.
Condição: A projeção respeita a ferramenta escolhida.
Aceite proposto: Campo ausente é tratado como ausência explícita, não sucesso presumido.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

2. T214 → T238 [complements]
Como combinar: Após retorno resumido, permitir leitura pontual dos trechos necessários para diagnóstico ou validação.
Interface: Referência imutável e intervalo requerido.
Condição: Original permanece disponível e na mesma revisão.
Aceite proposto: Releitura entrega evidência exatamente correspondente à seleção inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013, V4C-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cortar por caracteres pode destruir JSON, traceback ou registro multipartido.
- Resultado projetado deve indicar se houve paginação, truncamento ou falha parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelo pequeno com projeção e fronteira com a mesma evidência relevante. Vantagem por remoção de ruído não significa capacidade de reconstruir campos descartados.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T215, T238, T222

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S003 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://kairos.jetbrains.com/research/articles/the-complexity-trap](https://kairos.jetbrains.com/research/articles/the-complexity-trap)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação controlada de mascaramento de observações e resumo de trajetória; são transformações distintas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T215 — Observation Masking

**Nome canônico:** Observation Masking  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T215  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** mascaramento de observações

## T215:C01 — conceito

Mecanismo de gestão de contexto que substitui observações antigas de ferramentas por marcadores curtos, preservando a estrutura necessária da trajetória. Ele descarta detalhes do contexto ativo em vez de gerar uma síntese semântica. O conteúdo original pode continuar disponível em armazenamento externo para recuperação posterior.

Como funciona:
- Aplicar uma política, como janela recente, para decidir quais observações permanecem visíveis.
- Trocar observações antigas por marcadores identificáveis sem apagar a relação entre ação e resultado.
- Preservar evidências críticas ou permitir recarregá-las por referência quando voltarem a ser necessárias.

## T215:C02 — aplicacao

Quando usar:
- Agentes com muitas observações extensas e repetitivas, como leitura de código e execução de testes.

Quando não usar:
- Quando o raciocínio seguinte depende de detalhes antigos que não foram preservados nem podem ser recuperados.

Implementação proposta:
- Proposta: armazenar resultados integrais por ID, medir tamanho e estabelecer uma janela de observações recentes.
- Mascarar o corpo das observações elegíveis, mantendo chamada, status e referência; preservar a validade estrutural das mensagens.
- Definir exceções para erros ainda abertos, contratos e evidências de efeitos externos.
- Avaliar a janela por tipo de tarefa; os resultados de um estudo em agentes de programação não garantem comportamento em outro domínio.

Aplicação LAI proposta:
Proposta LAI: experimentar mascaramento de logs antigos já resolvidos, preservando resultados atuais e referências a evidências auditáveis.

## T215:C03 — riscos_validacao

Armadilhas:
- O marcador não transmite o significado do conteúdo omitido.
- O agente pode esquecer por que uma opção falhou.
- Confundir mascaramento com resumo esconde qual informação foi realmente preservada.

Métricas sugeridas:
- Tokens removidos; releituras; taxa de conclusão; regressões por dependência de observações antigas.

Testes propostos:
- Criar tarefa cuja solução exige um resultado antigo e testar recuperação pelo marcador.
- Comparar masking e resumo usando mesmo modelo, tarefas e orçamento.
- Verificar que cada resposta de ferramenta continua associada à chamada correta.

## T215:C04 — perguntas_proveniencia

Pergunta: Observation Masking produz um resumo?
Resposta: Não. A operação central oculta o conteúdo e deixa um marcador; não tenta reescrever sua informação principal.

Pergunta: É comprovadamente superior em qualquer agente?
Resposta: Não. Há evidência em configurações estudadas; a escolha depende do tipo de observação, dependências temporais e custo de releitura.

Pergunta: Mascarar significa resumir com menos palavras?
Resposta: Não. O mecanismo pode apenas substituir o conteúdo por um marcador, sem representar semanticamente o que foi retirado.

Pergunta: Por que medir releituras na avaliação?
Resposta: Porque a economia inicial pode ser compensada por ferramentas repetidas para recuperar observações removidas cedo demais.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T215:C05 — mecanismo_avancado

Masking preserva a estrutura da trajetória enquanto retira o conteúdo de observações selecionadas. Essa assimetria pode deixar uma ação sem a evidência que a justificou, favorecendo releitura ou repetição. Uma política proposta marca observações protegidas por dependências ainda abertas: resultados que comprovam uma decisão pendente não entram na mesma regra de expiração que logs já consumidos. O marcador deve permitir localizar a observação integral quando necessário.

Condição de contorno:
Observações antigas continuam essenciais quando contêm único recibo, exceção ou detalhe ainda exigido pelo próximo passo.

Contrato proposto:
- Entradas: Trajetória, janela recente, dependências pendentes e referências ao arquivo original.
- Saídas: Histórico mascarado com marcadores estáveis e conteúdo protegido.
- Estado: Observações omitidas, motivos e acessos posteriores.
- Invariante: Mascarar contexto não significa apagar a evidência original nem declarar seu conteúdo irrelevante para sempre.

Compromissos de projeto:
- Regras simples reduzem custo de síntese e podem provocar novas consultas.
- Proteções por dependência preservam informação útil e exigem estado adicional do workflow.

## T215:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mascarar a única observação que contém um identificador necessário ao passo seguinte; exigir recuperação por referência ou proteção antecipada, sem inventar o identificador.

Plano de avaliação proposto:
Comparar histórico integral, masking e sumarização no mesmo agente e orçamento. Medir conclusão, releituras, repetição de ações e custo total, incluindo a síntese. Evitar extrapolar resultados de uma configuração para outros modelos e tarefas.

Comparações:
- T212 (alternative): Auto-compact produz resumo; masking decide quais observações deixar fora da janela.
- T214 (complements): Poda interna e masking por observação podem ser combinados com responsabilidades distintas.

Afirmação rastreável:
O estudo da JetBrains compara omissão de observações e sumarização e não encontra superioridade consistente da síntese em todas as configurações avaliadas.
Suporte: direct; fontes: V2A-S003
Limite: Os resultados pertencem aos agentes e benchmarks estudados; não demonstram que descarte sempre preserve melhor informação.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T215:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegia observações com dependências abertas. A expansão mede efeitos de masking na tomada de decisão, define recuperação de detalhes e distingue ocultação no prompt de remoção do histórico persistente.

Marcador informativo
Substitua observação ocultada por marcador com ferramenta, status, identificador e referência, conforme necessidade. Um marcador vazio informa que algo ocorreu, mas não ajuda a distinguir sucesso, erro ou efeito incerto. Preserve estrutura exigida pelo protocolo de mensagens para não deixar chamada sem resposta correspondente no histórico apresentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S031.

Proteção por dependência
Mantenha observações que sustentam a próxima ação ou o critério de conclusão, mesmo se antigas. Uma janela temporal simples pode funcionar em carga homogênea e falhar em missões com longa espera entre decisão e uso da evidência. Expire a proteção quando a dependência fecha, registrando por que a observação se tornou dispensável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, C-S026.

Teste de recuperação
O agente deve reconhecer quando o marcador não basta e recuperar o original. Meça releituras e repetições de ferramentas causadas por masking; ocultar uma resposta e depois executar a mesma ação novamente pode ser mais caro ou perigoso que manter alguns campos. A política deve favorecer consulta do artefato antes de refazer efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, C-S026.

USO AVANÇADO — Pesquisa com muitas páginas
Cenário: Observações antigas ocupam a janela depois da extração.
Estratégia: Guarde os documentos, preserve tabela de alegações e oculte corpos já consumidos. Quando surgir contradição, recupere o trecho original por identidade. Compare masking com sumarização mantendo o mesmo número de documentos acessíveis e o mesmo critério de evidência.
Papel do modelo pequeno: 3–7B trabalha em extração local; 15–30B integra apenas registros necessários.
Aceite proposto: Proposta: cobertura e fidelidade de citações com custo total, incluindo recuperações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031.

USO AVANÇADO — Sessão longa de programação
Cenário: Muitos logs antigos repetem resultados já resolvidos.
Estratégia: Oculte logs encerrados, mantenha último erro completo e recibos de alterações externas. Preserve vínculo entre comando e versão do código testado. Se um defeito reaparecer, recuperar o log antigo permite comparar condições sem supor que a mesma mensagem tem a mesma causa.
Papel do modelo pequeno: 8–14B diagnostica localmente; runtime protege evidência de validação ainda vigente.
Aceite proposto: Proposta: menor contexto sem aumento de repetição ou perda de estado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Benefício potencial em trajetórias ruidosas; precisa de marcadores simples e recuperáveis.
8–14B: Classificação de observações consumidas e seleção de detalhes a reabrir.
15–30B: Integração de evidências preservadas, com acesso sob demanda a exceções antigas.
Requisitos de treino/runtime: Histórico persistente separado do prompt, referências estáveis e teste de compatibilidade com mensagens de ferramentas.
Não aplicar quando: Não ocultar único recibo de efeito ou evidência de requisito ainda em aberto.

## T215:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C030 — JetBrains Research / autores / SWE-agent com políticas de contexto
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo compara estratégias de contexto em tarefas SWE-bench Verified.
Mecanismo documentado: Masking oculta observações anteriores; sumarização substitui histórico por texto sintetizado; avaliação considera resolução e custo.
Correspondência com esta base: Observation masking é objeto central do experimento.
Transferência proposta para modelo pequeno: Proposta: avaliar remoção seletiva antes de acrescentar um resumidor 3–30B, preservando observações necessárias ao próximo teste.
Limite: Pesquisa controlada não conta como produção; não generalizar comparação para todo domínio ou modelo.
Fontes: V4C-S031.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Há estudo primário específico, classificado research_only. Não foi identificado nesta pesquisa um deployment de bigtech que documente esta mesma política como mecanismo comprovado.
Consultas registradas: V4C-Q028.

## T215:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T215 → T212 [alternative]
Como combinar: Comparar masking e resumo no mesmo scaffold, tratando diferenças de informação como variável explícita.
Interface: Trajetória, política e observações protegidas.
Condição: Mesmo conjunto de tarefas e orçamento total.
Aceite proposto: Medir resolução, duração, custo e reconsultas sem declarar vencedor universal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T215 → T238 [complements]
Como combinar: Reabrir observação por referência quando o marcador deixa de bastar.
Interface: Identidade, versão e trecho solicitado.
Condição: Original acessível e não substituído silenciosamente.
Aceite proposto: Não repetir ferramenta com efeito só para recuperar uma informação já registrada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Ocultar no prompt não equivale a apagar dados persistidos.
- Ausência da observação pode induzir repetição; o estado de conclusão deve permanecer explícito.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Use a comparação publicada como motivação para baseline, não como garantia para 3–30B. Os modelos locais avaliados no artigo incluem 32B e 480B, fora da faixa exata solicitada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T214, T041, T004

## Fontes primárias associadas

### V2A-S003 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://kairos.jetbrains.com/research/articles/the-complexity-trap](https://kairos.jetbrains.com/research/articles/the-complexity-trap)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação controlada de mascaramento de observações e resumo de trajetória; são transformações distintas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T216 — Repo Map / mapa do repositório

**Nome canônico:** Repo Map / mapa do repositório  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T216  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repository map; repo map

## T216:C01 — conceito

Índice compacto do repositório que apresenta arquivos, símbolos e relações úteis para orientar uma alteração. Aider documenta mapas com classes, funções e assinaturas. O mapa oferece navegação e contexto estrutural; decisões sobre comportamento exigem leitura do código pertinente, dos contratos e dos testes.

Como funciona:
- Um extrator identifica símbolos e referências a partir de uma revisão conhecida.
- Um seletor prioriza partes relevantes para a tarefa, respeitando um orçamento de contexto.
- Links para caminhos e posições permitem recuperar a implementação quando uma hipótese precisa ser confirmada.

## T216:C02 — aplicacao

Quando usar:
- Repositórios grandes, investigação inicial, descoberta de pontos de extensão e identificação de dependentes de uma mudança.

Quando não usar:
- Como prova de que uma função faz o que seu nome sugere ou como representação completa de dependências dinâmicas.

Implementação proposta:
- Proposta: gerar o mapa a partir de uma revisão identificada e registrar versão do extrator.
- Incluir caminho, linguagem, símbolo, assinatura e origem da relação; excluir artefatos gerados quando não acrescentam informação.
- Atualizar arquivos alterados e remover símbolos apagados; marcar dados de outra revisão como potencialmente desatualizados.
- Combinar consulta ao mapa com leitura dirigida e rastreamento dos testes associados antes de editar.

Aplicação LAI proposta:
Proposta LAI: gerar um mapa por projeto e módulo, deixando cada agente expandir somente os arquivos necessários à sua micro-missão.

## T216:C03 — riscos_validacao

Armadilhas:
- Reflexão, configuração e chamadas construídas em runtime podem escapar à análise estática.
- Um mapa antigo aponta para símbolos inexistentes.
- Excesso de detalhes recria o problema de consumir todo o contexto.

Métricas sugeridas:
- Cobertura de símbolos; referências inválidas; tokens do mapa; leituras necessárias até encontrar o alvo correto.

Testes propostos:
- Renomear um símbolo em uma cópia e conferir atualização das referências.
- Consultar um fluxo com ligação dinâmica e verificar que o mapa admite cobertura incompleta.
- Confirmar que cada posição recuperada corresponde à revisão declarada.

## T216:C04 — perguntas_proveniencia

Pergunta: O mapa substitui a leitura do arquivo?
Resposta: Não. Ele ajuda a localizar o arquivo e suas conexões; a implementação e seus invariantes continuam sendo a evidência do comportamento.

Pergunta: Um grafo de chamadas é obrigatório?
Resposta: Não. Assinaturas e hierarquia de arquivos já ajudam. Relações adicionais devem ser usadas quando o extrator consegue produzi-las com precisão conhecida.

Pergunta: Posso editar apenas com assinatura vista no mapa?
Resposta: Somente quando o contrato é suficiente e confirmado; normalmente é preciso ler implementação, usos e condições relevantes.

Pergunta: Por que registrar a revisão do mapa?
Resposta: Porque arquivos, símbolos e linhas mudam; sem ela, uma referência aparentemente válida pode apontar para outra realidade.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T216:C05 — mecanismo_avancado

O repo map do Aider seleciona partes relevantes usando ranking de um grafo de arquivos e dependências sob orçamento de tokens. Isso fornece orientação estrutural, mas não identifica automaticamente o comportamento executado em tempo de execução. Imports dinâmicos, geração de código e configuração podem escapar do grafo estático. Um mapa ligado à revisão do repositório evita que nomes e posições antigos orientem uma edição sobre código já alterado.

Condição de contorno:
Símbolos centrais no grafo podem não ser os relevantes para um defeito localizado ou ativado por configuração rara.

Contrato proposto:
- Entradas: Revisão do repositório, arquivos indexáveis, símbolos e objetivo da navegação.
- Saídas: Mapa compacto, relações selecionadas e referências resolvíveis.
- Estado: Índice por linguagem, revisão analisada e critérios de ranking.
- Invariante: O mapa é uma representação de uma revisão identificada, não autoridade sobre código que não foi lido.

Compromissos de projeto:
- Mapas amplos ajudam orientação inicial e consomem janela com relações pouco úteis.
- Ranking focado melhora densidade e pode esconder caminhos raros de execução.

## T216:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mover uma função, atualizar o repositório e manter mapa antigo; exigir detecção da revisão divergente antes de usar a posição para editar.

Plano de avaliação proposto:
Comparar navegação por busca textual, mapa e combinação de ambos em tarefas independentes. Medir leituras até localizar o trecho correto, cobertura de dependências e alterações em lugar errado. Separar tarefas estáticas de casos dependentes de configuração.

Comparações:
- T238 (complements): O mapa indica onde ler; faixas de linhas fornecem o conteúdo necessário à decisão.
- T232 (complements): Metadados sintáticos podem enriquecer referências sem provar comportamento dinâmico.

Afirmação rastreável:
Aider documenta seleção do repo map por ranking de um grafo de arquivos e dependências dentro de orçamento ativo.
Suporte: direct; fontes: V2A-S007
Limite: O grafo e o ranking são mecanismos de orientação; não equivalem a análise completa de fluxo em execução.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T216:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava ranking de símbolos e limites do grafo estático. A expansão usa o mapa para formular leituras direcionadas, verifica sua validade incremental e combina estrutura de código com evidência de execução.

Mapa orienta, arquivo decide
Inclua símbolos, caminhos e relações suficientes para localizar candidatos, mas confirme conteúdo atual antes de editar. Nomes centrais podem ser irrelevantes para a falha; arquivos raros ativados por configuração podem ser decisivos. Use o mapa como índice de hipóteses de localização, sem tratá-lo como descrição completa do comportamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

Atualização por mudança
Uma edição pode alterar assinatura, import ou relação de dependência. Marque partes afetadas do mapa e regenere o índice correspondente antes de delegar nova tarefa. Um mapa ligado ao commit original pode continuar útil para explicar o passado, mas não deve orientar substituição textual em uma revisão posterior sem revalidação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V3C-S027.

Estrutura e execução
Combine símbolos estáticos com trace, teste ou configuração que indique o caminho realmente exercitado. Não acrescente todo o runtime ao mapa: mantenha camadas consultáveis por finalidade. O modelo pequeno recebe uma trilha curta de arquivos e a evidência que justificou cada leitura, reduzindo busca ampla sem ocultar alternativas relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V4C-S029.

USO AVANÇADO — Defeito em monorepo
Cenário: O agente precisa localizar a implementação entre muitos módulos.
Estratégia: Comece por ponto de entrada e símbolo provável, leia interfaces e siga chamadores ou consumidores relevantes. Se o teste aponta para código gerado ou import dinâmico, abandone a hipótese puramente estática e examine geração e configuração. Atualize a trilha de evidência após cada descoberta.
Papel do modelo pequeno: 3–7B lê funções curtas; 8–14B navega dependências; 15–30B resolve ligações transversais.
Aceite proposto: Proposta: localizar o arquivo correto com menos leituras, sem perder defeitos ativados por configuração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

USO AVANÇADO — Delegação por módulo
Cenário: Vários agentes editam partes independentes do projeto.
Estratégia: Forneça mapa global curto e mapa local da revisão atribuída. Defina símbolos compartilhados que não podem mudar sem coordenação. Ao integrar, regenere relações afetadas e verifique se todos os consumidores continuam compatíveis.
Papel do modelo pequeno: 8–14B executa módulos; integrador maior usa o mapa para escolher testes de fronteira.
Aceite proposto: Proposta: nenhum uso de assinatura obsoleta e custo de atualização menor que reconstrução desnecessária do mapa inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Contexto local com assinatura e poucas relações; evitar mapas enormes que só repetem nomes.
8–14B: Navegação entre arquivos e seleção de leituras baseada em dependências explícitas.
15–30B: Análise de impacto entre módulos, com confirmação em código e testes.
Requisitos de treino/runtime: Índice por revisão, extração de símbolos confiável e acesso ao conteúdo atual dos arquivos.
Não aplicar quando: Não editar somente a partir do mapa nem presumir que análise estática captura configuração e geração dinâmica.

## T216:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta repo map; relatos internos mostram navegação assistida, mas não foram convertidos em adoções exatas do algoritmo de ranking do Aider.
Consultas registradas: V4C-Q023, V4C-Q024, V4C-Q027.

## T216:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T216 → T238 [feeds]
Como combinar: Transformar caminhos e símbolos do mapa em pedidos de leitura de trechos relevantes.
Interface: Arquivo, revisão, símbolo e intervalo a resolver.
Condição: Posições são recalculadas ou validadas contra o conteúdo atual.
Aceite proposto: Leitura inclui contexto suficiente para a alteração pretendida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T216 → T213 [complements]
Como combinar: Usar relações estruturais para escolher unidades com baixo acoplamento e interfaces explícitas.
Interface: Subgrafo de módulos e símbolos compartilhados.
Condição: Critérios de aceite cobrem as fronteiras entre unidades.
Aceite proposto: Integração detecta consumidores omitidos pelo mapa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mapas muito compactos podem ocultar a única relação necessária ao diagnóstico.
- A centralidade no grafo não substitui evidência de que o código participa do comportamento defeituoso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare localização e reparo com mapa, busca textual e modelo de fronteira sob o mesmo acesso ao repositório. Redução de leitura não demonstra compreensão completa do sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T238, T222, T213

## Fontes primárias associadas

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T217 — Test-Driven Loop

**Nome canônico:** Test-Driven Loop  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T217  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** test driven development loop; ciclo orientado por testes

## T217:C01 — conceito

Ciclo de desenvolvimento no qual um comportamento esperado é expresso em teste, uma alteração busca satisfazê-lo e a verificação orienta o passo seguinte. Em agentes, esse ciclo precisa preservar a independência do critério de aceitação: mudar o teste para acomodar um defeito não comprova solução.

Como funciona:
- O teste oferece um observável para uma hipótese de comportamento.
- A falha inicial precisa decorrer do problema relevante, e não de ambiente quebrado ou dependência ausente.
- Depois da alteração, o resultado é comparado ao teste anterior e aos contratos afetados.

## T217:C02 — aplicacao

Quando usar:
- Correções reproduzíveis, regras de domínio, regressões e alterações com entradas e saídas verificáveis.

Quando não usar:
- Criar testes que apenas repetem a implementação, ou exigir testes novos para toda edição documental de baixo impacto.

Implementação proposta:
- Proposta: registrar o cenário, a expectativa e a razão pela qual ele representa o pedido.
- Executar a reprodução em ambiente adequado e preservar a mensagem de falha relevante.
- Fazer a menor mudança coerente, verificar o cenário e acrescentar regressões relacionadas quando houver risco concreto.
- Revisar mudanças nos próprios testes separadamente; documentar testes não executados e dependências indisponíveis.
- Encerrar quando os critérios acordados e a verificação proporcional estiverem atendidos.

Aplicação LAI proposta:
Proposta LAI: associar cada micro-missão a evidências proporcionais ao risco, com teste de regressão quando existir um comportamento verificável a proteger.

## T217:C03 — riscos_validacao

Armadilhas:
- Cobertura alta pode coexistir com asserções fracas.
- Testes instáveis produzem feedback enganoso.
- Um teste aprovado não demonstra propriedades que ele não observa.

Métricas sugeridas:
- Regressões detectadas; estabilidade do cenário; cobertura dos critérios; tempo até diagnóstico; falhas ainda sem explicação.

Testes propostos:
- Injetar uma versão defeituosa conhecida e confirmar que o teste a rejeita.
- Alterar somente a mensagem de saída para verificar se a asserção mede o comportamento essencial.
- Repetir casos instáveis antes de atribuir causalidade à correção.

## T217:C04 — perguntas_proveniencia

Pergunta: Todo ciclo precisa começar escrevendo um teste novo?
Resposta: Não. Uma reprodução existente ou teste de contrato pode servir. A escolha depende do problema e do valor real da nova verificação.

Pergunta: O agente pode corrigir o teste?
Resposta: Pode, se a expectativa estava errada e houver justificativa ligada ao requisito. Alterar a expectativa exige revisão, não deve ocultar uma falha do produto.

Pergunta: Um teste verde recém-criado prova que corrigi o defeito?
Resposta: Não sozinho. É útil demonstrar falha na versão anterior pelo motivo esperado e sucesso após a alteração, com execução real do caso.

Pergunta: Por que testar sequências?
Resposta: Porque criação, atualização e remoção podem interagir; cada operação isolada pode funcionar enquanto a sequência viola um invariante.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T217:C05 — mecanismo_avancado

O ciclo orientado por teste precisa distinguir regressão do produto e falha da infraestrutura de teste. Uma execução verde pode significar que nenhum caso foi descoberto, e uma vermelha pode decorrer de dependência indisponível. Além de exemplos, invariantes e sequências de ações ajudam revelar defeitos de estado que não aparecem em uma chamada isolada. O teste escolhido deve falhar pelo comportamento ausente, não por um detalhe incidental da implementação.

Condição de contorno:
Se produtor e verificador compartilham a mesma interpretação incorreta do requisito, o ciclo pode convergir para uma implementação errada com testes verdes.

Contrato proposto:
- Entradas: Requisito, caso que o exercita, ambiente identificado e alteração candidata.
- Saídas: Resultado por teste, motivo da falha e evidência de cobertura do comportamento.
- Estado: Versão dos testes, casos executados e baseline anterior.
- Invariante: Ausência de testes executados não é registrada como comprovação de correção.

Compromissos de projeto:
- Exemplos específicos são fáceis de explicar e podem cobrir pouco espaço de estados.
- Testes gerativos exploram mais sequências e exigem invariantes e modelos de referência corretos.

## T217:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar a descoberta para executar zero casos e introduzir uma falha de estado após duas operações; exigir detecção da ausência e cobertura da sequência.

Plano de avaliação proposto:
Comparar exemplos isolados e testes baseados em propriedades com defeitos introduzidos independentemente. Controlar orçamento de execução. Medir defeitos detectados, falsos alarmes e tempo de diagnóstico, sem usar apenas porcentagem de testes aprovados.

Comparações:
- T195 (complements): Verificação por execução é o mecanismo de evidência usado pelo ciclo.
- T224 (complements): A especificação fornece o comportamento que os testes devem representar.

Afirmação rastreável:
Hypothesis pode gerar sequências de ações em máquinas de estado e compará-las com um modelo de referência.
Suporte: direct; fontes: V3C-S032
Limite: A ferramenta explora o modelo fornecido; não valida automaticamente se o oráculo corresponde ao requisito real.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T217:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia testes vazios, infraestrutura e regressão. A camada nova define independência do requisito, progressão dos verificadores e política de reparo que impede adaptar a prova para aceitar uma implementação inadequada.

Falha que representa o requisito
Antes do reparo, reproduza o comportamento esperado e confirme que o teste falha pela razão relevante. Um teste recém-gerado pode falhar por import ou fixture, sem demonstrar o defeito do produto. Preserve a relação entre requisito e observação; só então use a falha como direção de mudança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S007.

Ciclo com permissões de reparo
Separe mudanças permitidas no produto, nos testes e no ambiente. Um agente encarregado de corrigir teste quebrado por mudança legítima não deve reverter o produto para satisfazer expectativa antiga. Já um reparador do produto não pode apagar asserções para obter verde. Encaminhe a falha ao papel adequado com justificativa verificável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

Pirâmide de evidência
Use verificações baratas antes das caras: parsing e contrato local, teste que reproduz, regressões relacionadas e integração necessária. Verde em uma etapa não substitui as seguintes. Se a alteração muda uma dependência, invalide resultados afetados e rerode sobre a revisão final, sem reaproveitar aprovação de bytes anteriores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S010.

USO AVANÇADO — Reparo por modelo pequeno
Cenário: Defeito localizado possui teste reproduzível e domínio conhecido.
Estratégia: Fixe o teste de comportamento, produza patch mínimo e execute verificação focada. Após passar, rode regressões relevantes e revise efeitos fora de escopo. Se repetir o mesmo erro, interrompa para diagnóstico em vez de aumentar indefinidamente o número de tentativas.
Papel do modelo pequeno: 3–7B propõe alteração local; 8–14B interpreta falhas; 15–30B trata hipótese mais ampla.
Aceite proposto: Proposta: solucionar o defeito sem apagar prova e sem introduzir regressões detectáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S007, V4C-S009.

USO AVANÇADO — Remoção automatizada de código
Cenário: Limpeza gera falhas em testes ou infraestrutura.
Estratégia: Classifique a causa e use reparadores restritos ao escopo correto. Depois de CI verde, execute verificações de propriedade e revisão de intenção. Uma aprovação de LLM não é prova formal de equivalência; mantenha limites e revisão adequada ao risco da mudança.
Papel do modelo pequeno: 8–14B faz diagnóstico e correção delimitada; ferramentas determinísticas executam transformações.
Aceite proposto: Proposta: rejeitar patches com alteração de semântica fora do escopo, mesmo quando CI passa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reparos pequenos guiados por teste externo, com linguagem e formato treinados.
8–14B: Diagnóstico entre código, fixture e ambiente, usando erros estruturados.
15–30B: Revisão de efeitos entre módulos e escolha de testes adicionais; não substituir execução por opinião.
Requisitos de treino/runtime: Ambiente reproduzível, contagem de testes executados, restrições de edição e revisão final imutável.
Não aplicar quando: Não aceitar testes que só repetem a implementação nem gerar evidência de sucesso sem execução real.

## T217:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Candidatos são avaliados e iterados com compilação e testes.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Atualizações do diff são reavaliadas por CI até sucesso ou limite de tentativas.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: A fonte descreve testes e builds na transformação Java; não demonstra explicitamente o ciclo orientado por falha exigido nesta ficha.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: Correções e refatorações concretas, sem protocolo genérico de patch comprovado.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: O sistema modifica programas com avaliação; não demonstra todos os mecanismos de aplicação de patch.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Geração de testes é parte da engenharia de código, não prova qualquer mecanismo de patch.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Ampliação de suíte se relaciona a engenharia de código com escopo específico.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Há ciclos de implementação e testes, mas não fica provado test-first para todas as alterações.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean e SapFix descrevem loops concretos de correção e validação. Testes genéricos de outros relatos foram mantidos como família, sem assumir test-first universal.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q012.

## T217:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T217 → T232 [complements]
Como combinar: AutoClean combina transformação AST com CI e reparadores especializados em falhas.
Interface: Patch estrutural, resultado de build e classe de diagnóstico.
Condição: Reparador respeita o tipo de arquivo e efeito autorizado.
Aceite proposto: Transformação passa validação sem relaxar o requisito original.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T217 → T233 [complements]
Como combinar: SapFix/Sapienz usa sinais de falha e valida candidatos antes de revisão.
Interface: Candidato, reprodução e resultados de testes.
Condição: A validação pertence à revisão candidata.
Aceite proposto: Rejeitar correção que não resolve a falha ou introduz regressão detectada.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S007. Casos: V4C-C009.

CONTROLES DE FALHA
- Testes verdes com zero casos executados não confirmam comportamento.
- O mesmo modelo pode gerar implementação e teste com o mesmo equívoco; buscar requisito e prova independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de correção e regressão com iguais verificadores e orçamento de tentativas. Modelos pequenos podem competir em defeitos locais verificáveis sem equivalência em design aberto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T224, T213, T233

## Fontes primárias associadas

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S023 — Spec Kit

[https://github.com/github/spec-kit](https://github.com/github/spec-kit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo de especificação, plano, tarefas, implementação e convergência; exemplo concreto de desenvolvimento guiado por especificações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T218 — Loop Detection / detecção de estagnação e ciclos

**Nome canônico:** Loop Detection / detecção de estagnação e ciclos  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T218  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** stagnation detection; cycle detection

## T218:C01 — conceito

Detecção de repetição sem progresso significativo durante a execução de um agente. O objetivo é interromper ciclos improdutivos e obter informação nova. O rótulo descreve uma política de controle: repetição de texto ou de comandos, isoladamente, não prova estagnação, pois algumas verificações são legitimamente periódicas.

Como funciona:
- O controlador observa ações, respostas, mudanças de artefatos e critérios de avanço.
- Assinaturas de estado permitem reconhecer ciclos como A→B→A, além da repetição imediata.
- Uma janela temporal e um limiar contextual diferenciam trabalho lento de ausência persistente de avanço.

Nota de nomenclatura: Política editorial de supervisão; não é apresentada como algoritmo universal de um produto.

## T218:C02 — aplicacao

Quando usar:
- Agentes longos que repetem buscas, recompilam sem alterações ou alternam correções que desfazem umas às outras.

Quando não usar:
- Como motivo automático para encerrar uma tarefa apenas porque o mesmo comando apareceu duas vezes.

Implementação proposta:
- Proposta: registrar hash do artefato relevante, erro normalizado, hipótese atual, ação e resultado.
- Definir progresso por tarefa: nova evidência, teste resolvido, hipótese descartada ou marco concluído.
- Ao detectar estagnação, pedir mudança de estratégia, leitura direcionada ou retorno ao planejador, dentro do orçamento existente.
- Limitar intervenções repetidas e preservar o diagnóstico quando nenhum caminho autorizado produzir avanço.
- Excluir da assinatura ruído como timestamps, sem apagar códigos de erro ou detalhes causais úteis.

Aplicação LAI proposta:
Proposta LAI: usar supervisão de progresso baseada em marcos e evidência, enviando ao planejador a hipótese que falhou e as tentativas já descartadas.

## T218:C03 — riscos_validacao

Armadilhas:
- Normalização excessiva une falhas diferentes.
- Pequenas edições irrelevantes podem enganar uma métrica baseada apenas em hashes.
- Reiniciar a sessão pode reproduzir o mesmo ciclo.

Métricas sugeridas:
- Loops detectados; falsos alarmes; ações sem informação nova; custo até intervenção; recuperação após mudança de estratégia.

Testes propostos:
- Simular três execuções com o mesmo erro e nenhum delta e exigir intervenção.
- Simular testes repetidos com avanço verificável e evitar alarme prematuro.
- Construir um ciclo entre duas revisões e verificar reconhecimento por histórico.

## T218:C04 — perguntas_proveniencia

Pergunta: Limite de passos resolve loops?
Resposta: Ele limita o dano, mas não identifica a causa nem recupera a estratégia. A detecção usa sinais do conteúdo e do estado.

Pergunta: Uma tentativa sem alteração conta como progresso?
Resposta: Pode contar quando elimina uma hipótese ou revela informação relevante. O critério deve registrar essa evidência, não apenas a atividade.

Pergunta: Trocar palavras na próxima tentativa desfaz um loop?
Resposta: Não se ação, informação disponível e efeito esperado continuam iguais sem nova evidência.

Pergunta: O que fazer depois de detectar estagnação?
Resposta: Registrar a hipótese do bloqueio e escolher uma intervenção que altere informação ou estratégia; repetir o mesmo passo com prazo maior pode não ajudar.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T218:C05 — mecanismo_avancado

Detectar ciclos pode usar assinatura de ação normalizada, estado relevante e observação resultante. Igualdade de comando não basta: polling legítimo repete consultas enquanto o estado externo avança. Também não basta uma mensagem nova, pois reformular texto pode esconder a mesma falta de progresso. Uma proposta acompanha variáveis de domínio, como requisitos resolvidos, artefatos confirmados ou hipóteses eliminadas, junto do custo das repetições.

Condição de contorno:
Um limite de passos detecta consumo excessivo, mas não demonstra estagnação; tarefas válidas podem exigir muitas iterações.

Contrato proposto:
- Entradas: Traço de ações, estado relevante, objetivos pendentes e orçamento.
- Saídas: Sinal de ciclo provável, evidências e ação de recuperação indicada.
- Estado: Assinaturas recentes, progresso confirmado e janelas temporais.
- Invariante: Repetição é avaliada contra mudança de estado e finalidade, não somente contra similaridade textual.

Compromissos de projeto:
- Assinaturas muito específicas deixam passar ciclos com pequenas variações.
- Normalização agressiva pode confundir ações parecidas sobre recursos diferentes.

## T218:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar duas consultas equivalentes sem nova informação e, separadamente, repetir polling com progresso real; exigir alerta no primeiro caso e continuidade controlada no segundo.

Plano de avaliação proposto:
Comparar contagem de passos, repetição textual e assinatura com progresso em trajetórias rotuladas. Medir detecção precoce, falsos positivos e custo evitado. Definir resposta proporcional: buscar informação, mudar estratégia ou encerrar com pendências.

Comparações:
- T219 (distinct_from): Limite de execução estabelece uma fronteira de orçamento; detecção de loop interpreta comportamento.
- T145 (complements): Profundidade adaptativa pode consumir o sinal de progresso para decidir continuidade.

Afirmação rastreável:
LangGraph informa que GRAPH_RECURSION_LIMIT pode resultar de ciclos, mas também de grafos complexos válidos.
Suporte: related; fontes: V2A-S009
Limite: O detector semântico de progresso é proposta editorial, não capacidade demonstrada por esse erro do runtime.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T218:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 combinava assinatura de ações e progresso de domínio. A ampliação distingue repetição produtiva de repetição sem aprendizado e define intervenções graduais com critérios para terminar.

Assinatura semântica
Normalize ferramenta, argumentos relevantes, revisão de entrada e classe do resultado. Trocar a ordem de campos ou reformular a explicação não torna a ação nova. Ao mesmo tempo, consultar o mesmo ID depois de uma mudança de estado pode ser legítimo. A assinatura precisa incluir o que poderia alterar a conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V4C-S014.

Progresso verificável
Acompanhe redução de pendências, novas evidências, hipóteses eliminadas ou artefatos aceitos. Aumento de texto e número de ferramentas não demonstram avanço. Uma ação sem resultado pode ser justificável uma vez para testar hipótese; repetição exige explicar qual variável mudou ou qual evento externo está sendo aguardado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S031.

Escada de intervenção
Primeiro sinalize o padrão, depois exija hipótese alternativa ou nova observação e por fim suspenda a etapa. A intervenção também consome orçamento; não crie um loop de críticos comentando a estagnação sem alterar a execução. Encerramento deve preservar o último estado válido e um impedimento específico para retomada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S006.

USO AVANÇADO — Reparo preso em teste
Cenário: O agente alterna duas alterações que produzem o mesmo erro.
Estratégia: Compare hashes de diffs e assinatura da falha. Ao detectar oscilação, recupere requisito e contexto omitido, bloqueie temporariamente as duas propostas equivalentes e peça teste discriminante. Se não houver evidência nova dentro do orçamento, encaminhe a exceção com histórico mínimo.
Papel do modelo pequeno: 3–7B gera patch local; 8–14B classifica ciclo; 15–30B revisa premissa.
Aceite proposto: Proposta: reduzir tentativas inúteis sem interromper reparos que apresentam progresso objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S032.

USO AVANÇADO — Polling prolongado
Cenário: Uma tarefa remota demora e o agente consulta repetidamente seu estado.
Estratégia: Delegue polling mecânico ao runtime com intervalo e deadline. A repetição é válida enquanto houver contrato de espera e sinais externos; não invoque a LLM a cada estado idêntico. Se o prazo exceder o normal, gere diagnóstico com idade e último progresso confirmado.
Papel do modelo pequeno: 8–14B recebe somente transições relevantes; o temporizador não depende do modelo.
Aceite proposto: Proposta: menos chamadas de modelo e detecção de ausência de progresso sem falsos positivos por tarefa lenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Evitar delegar loops abertos; receber ações delimitadas e retornar estados tipados.
8–14B: Classificar repetições e propor uma observação que distinga hipóteses.
15–30B: Reformular etapa ou plano quando o padrão indica premissa errada, sob orçamento remanescente.
Requisitos de treino/runtime: Registro de assinaturas, métricas de domínio e distinção entre espera externa e repetição cognitiva.
Não aplicar quando: Não usar somente limite de passos ou texto repetido como prova de estagnação.

## T218:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber descreve mover polling mecânico para código. Não foi encontrado deployment que comprove exatamente o detector semântico proposto. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T218:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T218 → T209 [complements]
Como combinar: Transformar padrão de falha em hipótese procedimental testável e contextualizada.
Interface: Tentativas, feedback e variável proposta para mudança.
Condição: A reflexão recebe evidência suficiente de causa.
Aceite proposto: Nova tentativa altera fator relevante, sem repetir apenas a explicação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T218 → T219 [complements]
Como combinar: O limite estrutural encerra consumo máximo enquanto o detector busca parar ciclos antes dele.
Interface: Contadores por unidade e sinal de progresso.
Condição: Teto não se reinicia após intervenção ou delegação.
Aceite proposto: Ciclo termina dentro do orçamento e tarefa lenta válida não é confundida com recursão excessiva.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mascarar observações antigas pode esconder que uma tentativa já falhou.
- Uma mensagem de progresso sem mudança de estado não deve reiniciar o watchdog cognitivo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare eficiência e falsos encerramentos em tarefas que contêm tanto polling legítimo quanto ciclos reais. O detector pode ajudar modelos pequenos, mas sua classificação também precisa ser avaliada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T219, T226, T208

## Fontes primárias associadas

### V2A-S009 — GRAPH_RECURSION_LIMIT

[https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limite de passos de execução do grafo antes de alcançar condição de parada.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V3C-S029 — Reflexion — authors implementation and experiments

[https://github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementações, notebooks e estratégias de reflexão associadas a tipos de agente e ambientes experimentais.

Limite: Repositório de pesquisa em branch mutável; resultados publicados não foram reproduzidos nem usados como avaliação deste corpus.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T219 — Limite de recursão / profundidade de execução

**Nome canônico:** Limite de recursão / profundidade de execução  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T219  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execution depth limit; recursion budget

## T219:C01 — conceito

Orçamento explícito para limitar passos de execução, chamadas aninhadas ou profundidade de delegação. Esses limites medem coisas diferentes. No LangGraph, GRAPH_RECURSION_LIMIT trata do número de passos do grafo antes de uma condição de parada; não deve ser confundido automaticamente com a pilha de recursão da linguagem.

Como funciona:
- O runtime mantém contadores associados à execução e verifica o orçamento antes de avançar.
- Um limite alcançado gera um estado terminal controlado ou uma suspensão recuperável.
- A condição de término do fluxo continua necessária: aumentar o teto não corrige uma transição circular.

## T219:C02 — aplicacao

Quando usar:
- Workflows com laços, planejadores iterativos e delegação recursiva de agentes.

Quando não usar:
- Como único controle de custo ou como substituto de prazo, orçamento de tokens e limites para efeitos externos.

Implementação proposta:
- Proposta: definir separadamente máximo de passos, profundidade de agentes, chamadas de ferramentas e duração total.
- Documentar a unidade de contagem do framework e compartilhar o orçamento agregado com os descendentes.
- Preservar estado, motivo da interrupção e ações concluídas para permitir retomada consciente.
- Investigar o caminho de transições quando o teto for atingido; aumentar o orçamento somente com justificativa operacional.
- Planejar margem suficiente para registrar o resultado e liberar recursos antes de encerrar.

Aplicação LAI proposta:
Proposta LAI: atribuir orçamentos por missão e orçamento global do projeto, preservando o último estado confirmado quando uma execução atingir o limite.

## T219:C03 — riscos_validacao

Armadilhas:
- Um limite local por subagente pode permitir explosão do total global.
- Etapas longas ultrapassam o prazo mesmo com poucos passos.
- Uma parada abrupta pode deixar operações externas em resultado incerto.

Métricas sugeridas:
- Passos por tarefa; profundidade máxima; frequência de interrupção; custo agregado; operações pendentes ao parar.

Testes propostos:
- Criar um grafo sem condição de saída e verificar término limitado com diagnóstico.
- Testar um fluxo legítimo próximo do teto e conferir margem para finalizar.
- Simular delegação ramificada e verificar que o orçamento global prevalece.

## T219:C04 — perguntas_proveniencia

Pergunta: Posso usar o mesmo número para todos os limites?
Resposta: Pode ser inadequado: profundidade, passos e chamadas têm escalas diferentes. Escolha cada teto com base no comportamento esperado e na unidade real do runtime.

Pergunta: Atingir o limite significa que o modelo falhou?
Resposta: Não necessariamente. Pode indicar orçamento insuficiente, condição de parada incorreta ou tarefa maior que a prevista; o histórico permite distinguir as causas.

Pergunta: Um grafo com dez nós exige dez passos?
Resposta: Não necessariamente. Nós paralelos podem compartilhar superstep, enquanto ciclos podem executar o mesmo nó várias vezes.

Pergunta: Por que limitar só profundidade de subagentes é insuficiente?
Resposta: Porque muitos agentes podem ser criados em cada nível; o total de trabalho cresce mesmo com profundidade pequena.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T219:C05 — mecanismo_avancado

Um limite de profundidade não limita necessariamente o trabalho total. Em uma árvore com fator de ramificação b e profundidade d, a quantidade de nós pode crescer como 1+b+…+bᵈ. Já supersteps de um grafo podem conter vários nós paralelos. O contador precisa indicar sua unidade: etapas do grafo, chamadas de modelo, delegações aninhadas ou operações. Um orçamento compartilhado evita que cada filho receba inadvertidamente o orçamento integral da missão.

Condição de contorno:
Elevar o limite resolve apenas interrupção por orçamento insuficiente; não corrige uma condição de término ausente.

Contrato proposto:
- Entradas: Unidade de contagem, limite, orçamento global e contexto da delegação.
- Saídas: Permissão para novo passo ou interrupção com estado retomável.
- Estado: Consumo acumulado, profundidade corrente e reservas dos filhos.
- Invariante: A soma do trabalho delegado permanece contabilizada no objetivo principal.

Compromissos de projeto:
- Limites apertados reduzem explosão de trabalho e podem interromper tarefas válidas.
- Limites amplos acomodam fluxos complexos e aumentam custo de um ciclo defeituoso.

## T219:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar árvore rasa com muitos filhos e cadeia profunda sem ramificação; verificar que a política distingue volume total e profundidade, sem usar um contador como substituto do outro.

Plano de avaliação proposto:
Comparar limite único e orçamento multidimensional em grafos conhecidos. Medir interrupções corretas, falsas interrupções e consumo máximo. Calibrar pela estrutura observada e preservar diagnóstico do contador que realmente atingiu a fronteira.

Comparações:
- T218 (distinct_from): Detecção de estagnação interpreta progresso; limite de execução apenas impõe um teto.
- T147 (complements): Fan-out pode aumentar trabalho total sem ampliar muito a profundidade.

Afirmação rastreável:
LangGraph distingue supersteps paralelos e sequenciais e documenta limite de passos até uma condição de parada.
Suporte: direct; fontes: V3C-S006
Limite: Esse contador não equivale automaticamente à pilha de recursão de Python ou ao total de chamadas externas.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T219:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia profundidade, largura e supersteps. A ampliação propõe um orçamento de expansão verificável, critérios para conceder extensão e saída útil quando a execução alcança o teto.

Contadores tipados
Mantenha limites separados para delegação aninhada, transições do grafo, chamadas externas e custo acumulado. Uma unidade não substitui as outras: um nó pode disparar muitas operações, e vários nós podem avançar no mesmo superstep. Exponha ao controlador qual contador bloqueou a próxima ação, para não diagnosticar como falha cognitiva uma restrição estrutural.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V2A-S018.

Expansão com reserva
Antes de criar filhos, reserve parte do orçamento para juntar e validar seus resultados. Um supervisor que distribui todo o saldo aos trabalhadores pode ficar incapaz de concluir a missão. Limite também a quantidade de filhos ativos e de novas fronteiras abertas; profundidade baixa não impede fan-out excessivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Extensão condicionada
Permitir mais passos exige evidência de progresso e estimativa do trabalho restante. Não renove o limite somente porque o agente pediu para continuar. Registre motivo, saldo adicional e critério de término; mantenha teto absoluto da missão. Se a condição de saída não está definida, aumentar o limite apenas adia a falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3C-S032.

USO AVANÇADO — Delegação recursiva
Cenário: Um planejador divide tarefas e especialistas querem criar novos especialistas.
Estratégia: Autorize expansão somente se o filho produzir resultado integrável e couber na reserva. Exija referência à necessidade descoberta e elimine subproblemas duplicados. No último nível, o agente deve resolver com suas ferramentas ou devolver impedimento, sem contornar o teto criando nova sessão.
Papel do modelo pequeno: 3–7B não delega por padrão; 8–14B pede divisão; 15–30B decide com orçamento global.
Aceite proposto: Proposta: crescimento limitado e nenhum ramo abandonado sem estado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V2A-S018.

USO AVANÇADO — Grafo de reparo iterativo
Cenário: O agente alterna editar, testar e diagnosticar.
Estratégia: Defina número máximo de ciclos e custo total, mas ofereça saída com patch parcial e diagnóstico antes do teto. Se há progresso comprovado, uma extensão explícita pode continuar; repetição do mesmo erro deve acionar diagnóstico e não simplesmente incrementar o limite.
Papel do modelo pequeno: 8–14B executa ciclos locais; controlador valida progresso e extensão.
Aceite proposto: Proposta: distinguir tarefas longas produtivas de ciclos sem solução, medindo encerramento prematuro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3C-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar uma etapa ou pequeno ciclo com término claro, reduzindo necessidade de profundidade.
8–14B: Tratar subproblemas com algumas iterações e retornar saldo e impedimentos.
15–30B: Planejar expansão e integração, submetendo decisões de orçamento ao controlador determinístico.
Requisitos de treino/runtime: Contadores globais persistentes, reserva de finalização e documentação da unidade de limite do framework.
Não aplicar quando: Não interpretar recursion_limit de uma biblioteca como número universal de chamadas LLM ou profundidade de linguagem.

## T219:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação de grafos e agentes apoia os controles; relatos de delegação não demonstram esta política completa de limites nem justificam dez casos exatos. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q002, V4C-Q010, V4C-Q021, V4D-Q021.

## T219:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T219 → T218 [complements]
Como combinar: O detector identifica ciclos antes do teto, enquanto o limite garante término máximo mesmo quando a detecção falha.
Interface: Contadores, assinatura de repetição e progresso observado.
Condição: Intervenções não reiniciam o saldo.
Aceite proposto: Encerrar ciclo conhecido e permitir sequência longa que ainda avança.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T219 → T237 [complements]
Como combinar: Delegação consome orçamento do pai e devolve resultado que cabe na reserva de integração.
Interface: Quota do filho, profundidade e contrato de retorno.
Condição: Expansão autorizada pelo controlador e não apenas pelo texto do prompt.
Aceite proposto: Soma de quotas e reservas não excede o teto global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V2A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Trocar o nome da sessão ou do agente não deve zerar contadores da missão.
- Ao atingir o teto, preservar estado aceito e explicitar o trabalho não executado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de conclusão sob orçamento igual, contando todos os descendentes. A equipe pequena não deve ganhar vantagem aparente por ocultar chamadas atrás de um único superstep.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T218, T237, T243

## Fontes primárias associadas

### V2A-S009 — GRAPH_RECURSION_LIMIT

[https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limite de passos de execução do grafo antes de alcançar condição de parada.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

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

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T220 — Tool Call Repair

**Nome canônico:** Tool Call Repair  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T220  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** tool argument repair; reparo de argumentos

## T220:C01 — conceito

Reparo de uma chamada de ferramenta inválida por meio de diagnóstico estruturado e correção dos argumentos ou da seleção da ferramenta. É seguro repetir uma chamada rejeitada antes da execução quando o erro foi corrigido. Uma resposta perdida após uma mutação exige reconciliação, pois o efeito pode já ter ocorrido.

Como funciona:
- O executor distingue erro de esquema, erro de domínio, falta de permissão e resultado de execução incerto.
- Feedback limitado informa o campo inválido e a restrição aplicável.
- O agente produz uma nova proposta que passa novamente pelas validações e pelo controle de autorização.

## T220:C02 — aplicacao

Quando usar:
- Argumentos malformados, tipos incompatíveis, identificadores não encontrados ou seleção incorreta entre ferramentas disponíveis.

Quando não usar:
- Repetir cegamente uma mutação após timeout ou modificar permissões para contornar uma rejeição.

Implementação proposta:
- Proposta: validar os argumentos antes de executar e classificar a resposta com um código de erro estável.
- Permitir poucas tentativas de reparo, preservando o objetivo e os valores já confirmados.
- Quando um identificador estiver errado, recuperar o identificador real na fonte autorizada; não adivinhar um substituto.
- Registrar a relação entre chamada original e corrigida, incluindo identidade e resultado da execução.
- Para efeitos incertos, consultar estado ou chave idempotente antes de qualquer repetição.

Aplicação LAI proposta:
Proposta LAI: introduzir um contrato de erro entre controlador e ferramentas, encaminhando ambiguidades de efeito ao reconciliador e erros de formato ao reparador.

## T220:C03 — riscos_validacao

Armadilhas:
- Esquema válido não significa destinatário, arquivo ou valor de negócio correto.
- Mensagens de erro podem conter conteúdo não confiável.
- Reparo infinito consome orçamento sem resolver incompatibilidade de capacidade.

Métricas sugeridas:
- Reparos aceitos; taxa de execução duplicada; tentativas por erro; rejeições por categoria; resultados incertos reconciliados.

Testes propostos:
- Enviar argumento de tipo errado e verificar rejeição sem efeito.
- Fornecer chamada válida com alvo inexistente e exigir descoberta fundamentada.
- Simular mutação concluída com resposta perdida e impedir duplicação no reparo.

## T220:C04 — perguntas_proveniencia

Pergunta: Modo estrito elimina a necessidade de reparo?
Resposta: Não. Ele pode restringir o formato a um esquema suportado, mas não confirma existência do alvo, permissão ou consistência de negócio.

Pergunta: Quando um retry deixa de ser reparo?
Resposta: Quando a chamada já foi executada ou seu resultado é desconhecido. Nessa situação, repetição é uma decisão de recuperação com controle de idempotência.

Pergunta: Preencher um campo ausente com valor plausível é reparo válido?
Resposta: Somente se houver fonte ou default contratual; plausibilidade não fornece o dado que falta.

Pergunta: Quando reparar deveria parar?
Resposta: Quando falta informação indispensável, a mesma classe de erro persiste ou o orçamento acaba, preservando o diagnóstico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T220:C05 — mecanismo_avancado

Reparo pode alterar seleção da ferramenta, nome de campo, tipo, enum ou referência de recurso; cada classe exige diagnóstico diferente. Converter um número em string resolve sintaxe, mas pode mudar significado, como zeros à esquerda de um identificador. A proposta recebe erros estruturados e preserva o objetivo original. Rejeição comprovada antes da execução permite uma nova tentativa corrigida; desfecho incerto precisa de outra estratégia.

Condição de contorno:
Um erro genérico após envio não comprova que nada ocorreu; reparar e reenviar pode duplicar um efeito já aplicado.

Contrato proposto:
- Entradas: Chamada original, schema efetivo, diagnóstico e fase de execução alcançada.
- Saídas: Chamada revisada, justificativa da mudança e decisão de executar ou reconciliar.
- Estado: Número de reparos, alterações realizadas e identidade da intenção.
- Invariante: O reparo não muda silenciosamente o recurso ou objetivo para obter uma resposta sem erro.

Compromissos de projeto:
- Correções determinísticas são previsíveis e cobrem poucos tipos de falha.
- Reparo por modelo trata casos diversos e pode inventar valores apenas para satisfazer o schema.

## T220:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer enum inválido, ID desconhecido e resposta perdida após escrita; exigir correção no primeiro, busca ou inconclusão no segundo e reconciliação no terceiro.

Plano de avaliação proposto:
Comparar regras e reparo por modelo em erros rotulados por fase. Medir recuperação correta, alterações semânticas indevidas, loops e custo. Limitar reparos por intenção e separar erros recuperáveis de ausência de informação.

Comparações:
- T170 (complements): A revisão do schema define se o erro decorre de contrato obsoleto.
- T243 (distinct_from): Reconciliação investiga efeito incerto; não é simples correção dos argumentos.

Afirmação rastreável:
LangChain distingue middleware que transforma erro da ferramenta em feedback e middleware que repete a chamada.
Suporte: direct; fontes: V3C-S038
Limite: A composição não prova que todo erro é repetível nem que corrigir argumentos preserva a intenção.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T220:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava tipos de erro e efeito incerto. A camada nova usa reparo mínimo, validação de intenção e escalonamento por diagnóstico para evitar que um argumento válido faça a operação errada.

Reparo mínimo explicável
Produza uma diferença entre chamada original e corrigida, indicando qual erro cada mudança resolve. Corrigir nome de campo não autoriza mudar recurso ou ampliar seleção. Se o reparo exige adivinhar informação ausente, devolva necessidade de contexto em vez de preencher um valor plausível apenas para satisfazer o schema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S004, V3C-S038.

Fronteira de não execução
Reparo automático simples é apropriado quando há evidência de rejeição antes do efeito. Depois de timeout ou erro interno genérico, consulte a operação original antes de reenviar. Um parser local pode rejeitar antes da rede; um erro retornado pelo serviço precisa ser interpretado conforme seu contrato, não pela aparência do texto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V2A-S012.

Diagnóstico hierárquico
Tente primeiro transformações determinísticas autorizadas, como normalização de enum conhecida. Use LLM quando o erro exige relação entre objetivo, ferramenta e schema. Trocar ferramenta ou recurso é decisão de plano e deve passar por validação mais forte que um ajuste de formato. Cada reparo mantém a identidade da intenção quando ela permanece a mesma.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S038.

USO AVANÇADO — Ferramenta exige schema estrito
Cenário: Um pequeno modelo emite argumento com tipo ou nome errado.
Estratégia: Retorne erro estruturado e schema relevante, peça somente a correção mínima e valide novamente antes de executar. Preserve zeros à esquerda e unidades de identificadores; uma conversão aparentemente óbvia pode alterar o alvo. Limite ciclos e registre a classe que não foi resolvida.
Papel do modelo pequeno: 3–7B pode reparar formato curto; 8–14B relaciona campo e significado.
Aceite proposto: Proposta: corrigir sintaxe sem mudar recurso, quantidade ou efeito pretendido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S004, V3C-S013.

USO AVANÇADO — Catálogo mudou durante a missão
Cenário: A ferramenta selecionada teve revisão incompatível.
Estratégia: Resolva contrato vigente e compare com a intenção registrada. Se existir tradução sem perda, aplique adaptador testado; se a mudança exigir novo dado ou alterar efeito, volte ao planejador. Não usar tentativa e erro em produção como mecanismo de descoberta de schema.
Papel do modelo pequeno: 15–30B analisa incompatibilidade; runtime faz tradução validada e controle de efeitos.
Aceite proposto: Proposta: nenhuma chamada executada com parâmetros inventados para satisfazer versão nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, C-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Correções de formato e enum em chamadas pequenas, com validação determinística.
8–14B: Reparo semântico local quando objetivo e dados necessários estão explícitos.
15–30B: Replanejar escolha de ferramenta diante de mudança de capacidade, sem ocultar a mudança de intenção.
Requisitos de treino/runtime: Erros estruturados, schema versionado, prova de não execução ou reconciliação e limite de tentativas.
Não aplicar quando: Não reenviar efeito desconhecido nem preencher identificadores por similaridade sem fonte.

## T220:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Gateway e middleware fornecem contratos; a política de reparo mínimo é proposta. Não confundir reparadores de código AutoClean com reparo de argumentos de ferramenta.
Consultas registradas: V4C-Q009, V4C-Q013, V4C-Q023.

## T220:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T220 → T141 [complements]
Como combinar: Validar estrutura antes e depois do reparo, preservando separadamente os invariantes de intenção.
Interface: Chamada original, diff de argumentos e resultado de validação.
Condição: Schema corresponde à versão executável.
Aceite proposto: Reparo passa parser e conserva alvo e unidade corretos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T220 → T243 [complements]
Como combinar: Resolver desfecho incerto antes de permitir nova chamada corrigida.
Interface: Identificador da operação e estado observado no destino.
Condição: Timeout não foi tratado automaticamente como ausência de efeito.
Aceite proposto: Nenhuma duplicação após erro retornado tarde.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar reparos evita transformar uma chamada inválida em busca ilimitada de combinações.
- Um argumento aceito pelo schema pode continuar violando o requisito de negócio.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de chamadas corretas e efeitos errados entre modelos com o mesmo verificador. Reparo de formato pode favorecer 3–30B, mas não supre informação ausente ou escolha equivocada de ferramenta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T243, T228, T218

## Fontes primárias associadas

### V2A-S022 — Function calling

[https://developers.openai.com/api/docs/guides/function-calling](https://developers.openai.com/api/docs/guides/function-calling)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas de ferramentas com esquema de argumentos, modo estrito e resultados associados.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S038 — LangChain — Prebuilt middleware

[https://docs.langchain.com/oss/python/langchain/middleware/built-in](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Middleware de erro de ferramenta é distinto de retry; ordem de composição determina tratamento de exceções e limites.

Limite: Documentação dinâmica com requisitos de versão; não se pressupõe disponibilidade de classes no ambiente do usuário.

### V3C-S004 — Model Context Protocol — Tools, revision 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos inputSchema/outputSchema, listChanged, resultados estruturados e distinção entre erro de protocolo e erro da ferramenta.

Limite: Revisão fixada para análise; não alegada como revisão mais recente nem adotada pelo servidor do usuário.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S013 — JSON Schema — Understanding objects

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: properties não implica required; controle de propriedades extras e composição dependem do vocabulário e do escopo.

Limite: Validação estrutural não prova semântica de negócio; suporte do decodificador pode ser subconjunto do schema.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T221 — Goal Reminder Injection

**Nome canônico:** Goal Reminder Injection  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T221  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** goal reminder; lembrete de objetivo

## T221:C01 — conceito

Reintrodução controlada de uma versão curta do objetivo e dos critérios de conclusão durante uma tarefa longa. A expressão é um rótulo operacional, não uma técnica com eficácia universal demonstrada. O lembrete deve refletir a última instrução autorizada e ajudar o agente a avaliar o próximo passo.

Como funciona:
- O controlador mantém objetivo, restrições relevantes e critérios verificáveis fora da memória volátil.
- Em pontos definidos, injeta uma visão compacta desse contrato no contexto da execução.
- O lembrete referencia a versão vigente para evitar que uma meta antiga sobreviva a uma correção do usuário.

Nota de nomenclatura: Nome operacional proposto. As fontes apoiam contexto seletivo e continuidade; não comprovam uma política universal de injeção.

## T221:C02 — aplicacao

Quando usar:
- Tarefas extensas, retomada de sessão, troca de subagente ou momentos de replanejamento.

Quando não usar:
- Repetir instruções extensas em toda interação ou converter conteúdo de documentos recuperados em novas ordens para o agente.

Implementação proposta:
- Proposta: registrar objetivo atual, versão, critérios de aceitação e próximo marco verificável.
- Gerar lembrete curto após compactação, handoff ou divergência detectada, com orçamento próprio de tokens.
- Incluir progresso confirmado e questão ainda aberta; evitar recontar todo o histórico.
- Atualizar o contrato quando o usuário mudar o escopo, mantendo a origem e a precedência da decisão.
- Avaliar a utilidade pelo alinhamento das ações seguintes, não pela frequência dos lembretes.

Aplicação LAI proposta:
Proposta LAI: manter um contrato resumido por missão e recuperá-lo nos handoffs, acompanhado de evidências dos marcos já concluídos e da pergunta técnica restante.

## T221:C03 — riscos_validacao

Armadilhas:
- Lembretes desatualizados causam perseveração em uma meta cancelada.
- Formulações vagas acrescentam tokens sem orientar decisões.
- Repetição excessiva desloca evidência técnica necessária do contexto.

Métricas sugeridas:
- Ações alinhadas ao objetivo; versões antigas utilizadas; tokens de lembrete; marcos concluídos; desvios corrigidos.

Testes propostos:
- Mudar um requisito durante a missão e verificar que o próximo lembrete incorpora a mudança.
- Inserir uma ordem contraditória em material recuperado e confirmar que ela permanece como dado.
- Remover evidência de conclusão e testar se o agente evita declarar sucesso apenas pelo lembrete.

## T221:C04 — perguntas_proveniencia

Pergunta: O lembrete pode ampliar a autorização da tarefa?
Resposta: Não. Ele deve representar instruções já existentes. Uma geração incorreta do lembrete não cria permissão para agir.

Pergunta: Deve aparecer em todo turno?
Resposta: Não há frequência universal. Pontos de mudança de estado costumam fornecer um gatilho mais justificável que repetição indiscriminada.

Pergunta: O lembrete deve repetir todo o plano?
Resposta: Não. O plano pode mudar; resultado desejado e critérios vigentes são mais estáveis e úteis para orientar a próxima decisão.

Pergunta: Como impedir que lembretes entrem em conflito?
Resposta: Vinculá-los à versão do objetivo e tratar alteração autorizada como supersessão explícita da versão anterior.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T221:C05 — mecanismo_avancado

Nessa política editorial, o lembrete deve ser uma projeção da versão vigente do objetivo, não um novo objetivo redigido livremente. Mudanças autorizadas precisam invalidar lembretes antigos; repetir ambos aumenta conflito. O conteúdo proposto distingue resultado desejado, critérios de conclusão e próxima decisão, evitando transformar detalhes do plano em requisitos permanentes. Inserção frequente demais compete por contexto com a evidência que permitiria cumprir o objetivo.

Condição de contorno:
Lembrar uma meta incorreta ou obsoleta reforça desvio em vez de corrigi-lo.

Contrato proposto:
- Entradas: Objetivo versionado, alterações autorizadas e critérios ainda pendentes.
- Saídas: Lembrete curto vinculado à revisão vigente e ponto de uso.
- Estado: Versão ativa, lembretes emitidos e critérios resolvidos.
- Invariante: O lembrete não acrescenta requisito nem preserva instrução revogada como se continuasse vigente.

Compromissos de projeto:
- Repetição frequente reduz esquecimento e aumenta custo e redundância.
- Lembretes por evento são mais seletivos e dependem de bons sinais de desvio ou transição.

## T221:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o escopo no meio da tarefa e acionar novo lembrete; exigir referência à nova versão e remoção da obrigação revogada.

Plano de avaliação proposto:
Comparar ausência de lembrete, periodicidade fixa e gatilhos por troca de sessão ou plano. Usar tarefas longas com mudanças de escopo documentadas. Medir conclusão correta, persistência de metas antigas e consumo adicional; não presumir eficácia universal.

Comparações:
- T211 (complements): Handoff transporta objetivo e decisões para a próxima sessão.
- T212 (complements): Após compactação, o lembrete pode reintroduzir critérios vigentes sem reconstruir todo o histórico.

Afirmação rastreável:
A Anthropic identifica declaração prematura de conclusão e perda de continuidade como falhas de agentes em tarefas longas.
Suporte: related; fontes: V2A-S004
Limite: A fonte motiva o controle de objetivo; Goal Reminder Injection é uma proposta operacional, não técnica validada isoladamente pelo artigo.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T221:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definia lembrete como projeção do objetivo vigente. A expansão escolhe pontos de inserção, limita conteúdo por decisão e verifica se o lembrete reduz desvio sem substituir evidência ou alterar requisitos.

Lembrete por transição
Insira orientação ao mudar de fase, retomar sessão ou receber observação que pode desviar o plano. Repetir o objetivo em todo turno aumenta custo e pode fazer o modelo ignorá-lo como ruído. O conteúdo deve apontar resultado exigido, condição de conclusão e próxima decisão, evitando um histórico resumido disfarçado de lembrete.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S031.

Separar meta e método
Um plano contém meios que podem mudar; o objetivo contém o resultado autorizado. Se um lembrete fixa a primeira estratégia como requisito, o agente pode insistir nela apesar de evidência contrária. Mantenha restrições obrigatórias separadas das preferências e permita replanejar métodos preservando o critério de aceite.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S015, V3C-S012.

Atualização com proveniência
Gere o lembrete a partir de campos versionados, não por livre reinterpretação de toda a conversa. Quando o usuário altera escopo, invalide projeções anteriores. Uma instrução encontrada em documento de ferramenta não se torna objetivo por estar recente; o controlador preserva origem e autoridade das mudanças.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S028.

USO AVANÇADO — Pesquisa com descobertas atraentes
Cenário: O agente encontra temas interessantes fora da pergunta original.
Estratégia: Depois da coleta, apresente as perguntas ainda abertas e o critério de suficiência. Registre descobertas laterais como opcionais, sem expandir automaticamente a missão. Se uma descoberta altera uma premissa necessária, peça replanejamento explícito ligado ao objetivo, não abandono silencioso do escopo.
Papel do modelo pequeno: 3–7B classifica relevância local; 15–30B compara a descoberta com os requisitos.
Aceite proposto: Proposta: menor desvio de escopo e mesma cobertura das perguntas obrigatórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S030.

USO AVANÇADO — Programação com múltiplos ciclos
Cenário: Reparos sucessivos podem transformar uma mudança pequena em refatoração ampla.
Estratégia: Antes de editar de novo, recupere comportamento desejado, arquivos autorizados e testes de aceite. Compare o próximo patch com esses campos. Se o escopo precisa aumentar, registre motivo e impacto; não use o lembrete como autorização para modificar tudo relacionado.
Papel do modelo pequeno: 8–14B avalia aderência de diff; 15–30B resolve conflitos de requisito.
Aceite proposto: Proposta: menos alterações fora de escopo sem bloquear ajustes necessários demonstrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Lembretes curtos em campos estáveis ajudam tarefas estreitas, desde que não concorram com evidência essencial.
8–14B: Checagem de aderência da próxima ação ao objetivo e ao teste de aceite.
15–30B: Revisão de plano quando fatos novos exigem trocar o método preservando intenção.
Requisitos de treino/runtime: Objetivo versionado, autoridade de mudança e gatilhos por fase; contagem do custo de inserir lembretes.
Não aplicar quando: Não repetir requisito obsoleto nem transformar hipótese do agente em nova obrigação do usuário.

## T221:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes de planejamento e instruções persistidas apoiam princípios. Não foi comprovado produto ou técnica padronizada de bigtech com este nome editorial exato. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q010, V4C-Q027, V4D-Q022.

## T221:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T221 → T208 [complements]
Como combinar: O planejador publica objetivo e critérios; o executor recebe lembrete apropriado à fase atual.
Interface: Versão da meta, restrições e próxima decisão.
Condição: O lembrete não substitui pré-condições da etapa.
Aceite proposto: Mudança autorizada invalida lembretes anteriores.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T221 → T223 [complements]
Como combinar: A checagem compara o candidato com os requisitos vigentes lembrados, citando evidência concreta.
Interface: Critérios aplicáveis e artefato candidato.
Condição: Regras não aplicáveis são distinguidas de cumpridas.
Aceite proposto: Detectar um resultado elegante que não responde à pergunta atual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Repetição excessiva pode ocupar espaço das fontes necessárias ao objetivo.
- O lembrete é técnica editorial de controle em runtime, não garantia de alinhamento ou método de treino.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare política por transição com ausência e repetição fixa de lembretes. Meça aderência e custo; melhoria em tarefas delimitadas não demonstra entendimento superior da intenção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T212, T224

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T222 — Context Budget Monitor

**Nome canônico:** Context Budget Monitor  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T222  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** context budget monitoring; monitor de tokens

## T222:C01 — conceito

Monitoramento do espaço consumido e reservado na janela de contexto durante uma execução. A função é antecipar falta de capacidade e decidir quais conteúdos manter, recuperar ou compactar. Contagem de mensagens ou tamanho em bytes são aproximações fracas: o orçamento depende do modelo, do tokenizador e do protocolo usado.

Como funciona:
- O controlador contabiliza instruções, histórico, ferramentas, evidências recuperadas e outros conteúdos enviados ao modelo.
- Uma reserva cobre a saída esperada e as próximas observações necessárias.
- Gatilhos graduais acionam recuperação seletiva, poda, compactação ou rotação antes de um limite impeditivo.

## T222:C02 — aplicacao

Quando usar:
- Agentes com sessões longas, resultados extensos de ferramentas e recuperação de múltiplos documentos.

Quando não usar:
- Usar um percentual fixo como garantia universal ou assumir que cache de prompt remove tokens da janela.

Implementação proposta:
- Proposta: obter os limites documentados do modelo e contabilizar tokens reais quando a API os expuser.
- Reservar margem para resposta e chamadas subsequentes, incluindo variações na tokenização e no tamanho de ferramentas.
- Separar conteúdo protegido, evidência recuperável e dados descartáveis; medir o ganho e a perda de informação após cada redução.
- Aplicar histerese para evitar compactações repetidas próximas do mesmo limiar.
- Registrar estimativas e uso reportado, recalibrando o monitor quando houver mudança de modelo ou configuração.

Aplicação LAI proposta:
Proposta LAI: combinar orçamento de contexto com leitura sob demanda e referências recuperáveis, mantendo objetivo, restrições e estado confirmado dentro da margem definida.

## T222:C03 — riscos_validacao

Armadilhas:
- Um documento curto visualmente pode consumir muitos tokens.
- Saídas inesperadas de ferramentas esgotam a margem.
- Reduzir contexto sem verificar fatos essenciais pode melhorar custo e piorar a resposta.

Métricas sugeridas:
- Tokens por categoria; margem disponível; erro da estimativa; compactações por missão; recuperação de fatos após redução.

Testes propostos:
- Testar código, texto multilíngue e logs para comparar estimativa com uso reportado.
- Simular resultado muito maior que o previsto e verificar contenção antes da próxima chamada.
- Consultar um requisito protegido depois de compactar e exigir preservação.

## T222:C04 — perguntas_proveniencia

Pergunta: Tokens em cache deixam de contar no contexto?
Resposta: Não se deve assumir isso. Cache pode alterar processamento ou custo conforme o provedor, mas o conteúdo continua sujeito aos limites documentados da chamada.

Pergunta: Compactação aumenta a janela do modelo?
Resposta: Não. Ela reduz a representação enviada, podendo perder informação. O monitor precisa observar capacidade e qualidade da recuperação.

Pergunta: Reduzir a janela recupera tokens já faturados?
Resposta: Não. Pode reduzir chamadas futuras; o consumo passado permanece no custo da missão.

Pergunta: Contar mensagens serve para estimar contexto?
Resposta: É um sinal muito fraco quando mensagens e resultados têm tamanhos variados; contar unidades efetivas é mais informativo.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T222:C05 — mecanismo_avancado

O monitor precisa observar ocupação por categoria e erro de estimativa. O aumento pode vir de schemas, multimodalidade ou mensagens adicionadas pelo runtime, não apenas de novos turnos. Uma proposta compara previsão e uso observado para atualizar margem, mantendo duas visões: tokens ativos na próxima chamada e consumo acumulado da missão. Sem essa separação, compactar pode parecer reduzir custos já incorridos.

Condição de contorno:
Um contador sem ação associada apenas informa o estouro depois que o próximo resultado grande já foi produzido.

Contrato proposto:
- Entradas: Mensagens efetivas, modelo, tokenizer ou contador do backend e reservas pendentes.
- Saídas: Ocupação estimada, margem, desvio de previsão e gatilho de ação.
- Estado: Histórico de estimativas, valores observados e eventos de crescimento.
- Invariante: Tokens retirados da janela não são subtraídos do consumo acumulado já realizado.

Compromissos de projeto:
- Contagem frequente melhora precisão e acrescenta chamadas ou processamento.
- Amostragem por eventos reduz overhead e pode perder crescimento não instrumentado.

## T222:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter texto do usuário fixo e aumentar o schema de ferramentas; exigir que o monitor detecte o crescimento e ajuste a decisão antes de enviar.

Plano de avaliação proposto:
Comparar contagem por caracteres, tokenizer e endpoint oficial quando disponível. Controlar modelos e estruturas. Medir erro por categoria, estouros evitados e overhead; dimensionar margem pela distribuição observada, sem pressupor equivalência entre idiomas.

Comparações:
- T152 (complements): A alocação consome os sinais do monitor para redistribuir espaço.
- T168 (complements): Fronteiras suave e rígida convertem observação de orçamento em ação.

Afirmação rastreável:
A API de contagem Anthropic considera system prompt, ferramentas e outros elementos estruturados da mensagem.
Suporte: direct; fontes: V3C-S022
Limite: A estimativa é específica do backend e não representa automaticamente métricas internas de outro modelo.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T222:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava ocupação e consumo acumulado. A expansão transforma o monitor em controlador de ações com previsão de payload, orçamento de emergência e telemetria que explica por que uma janela cresceu.

Contabilidade por origem
Atribua tokens a instruções, histórico, documentos, schemas, ferramentas e saída prevista. Uma mudança de catálogo pode elevar uso sem novos turnos do usuário. Mostre diferenças por chamada e por revisão do prompt, permitindo corrigir a causa em vez de compactar tudo indiscriminadamente. Valores estimados e observados devem permanecer distinguíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S014.

Previsão do próximo passo
Antes da ferramenta, estime intervalo de saída e a margem para processá-la. Quando o tamanho não é limitado, escolha paginação, projeção ou arquivo externo. O monitor não deve esperar o payload chegar para descobrir que já não cabe; a decisão de admissão usa o risco de crescimento, não somente ocupação atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S022.

Ações ordenadas por perda
Priorize remover duplicatas recuperáveis, podar campos dispensáveis e ocultar observações encerradas antes de resumir evidência crítica. Cada ação possui custo e risco. Reserve capacidade para handoff se nenhuma redução preservar o requisito; o monitor deve poder bloquear a próxima chamada e produzir um estado retomável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S022.

USO AVANÇADO — Muitas ferramentas disponíveis
Cenário: Schemas consomem a maior parte da janela de um modelo local.
Estratégia: Meça contribuição do catálogo e substitua carga integral por descoberta progressiva. Registre schemas carregados por tarefa e descarte apenas os que não serão necessários ao próximo passo. Se uma ferramenta muda de versão, invalide seu descritor e atualize a estimativa.
Papel do modelo pequeno: 3–7B usa conjunto mínimo; 8–14B seleciona ferramentas; runtime mede bytes e tokens reais.
Aceite proposto: Proposta: maior espaço útil para evidência sem queda na seleção correta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Missão de edição longa
Cenário: O agente aproxima-se do limite enquanto ainda precisa testar e entregar.
Estratégia: Reserve explicitamente retorno de testes, interpretação e relatório final. Quando a previsão ameaça essa reserva, interrompa expansão e compacte ou faça handoff em ponto seguro. Não confunda redução do prompt com devolução de custo já gasto no provedor.
Papel do modelo pequeno: 15–30B integra etapas; modelos menores executam blocos com teto local.
Aceite proposto: Proposta: nenhum estouro inesperado e conclusão com evidência de validação disponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Monitor externo evita gastar contexto do próprio modelo para contar a janela.
8–14B: Classificação de conteúdo por utilidade pode apoiar ações, mantendo contagem determinística.
15–30B: Planejamento de contingência e tradeoffs quando várias obrigações competem por espaço.
Requisitos de treino/runtime: Tokenizer e template reais, telemetria do servidor, limites conhecidos e reserva para operações de recuperação.
Não aplicar quando: Não tratar contador aproximado como garantia de caber nem expor apenas porcentagem sem ação correspondente.

## T222:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Métricas de tokens por requisição e sessão orientam controle de contexto.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber e NVIDIA fornecem controles concretos; a ordem de ações e reserva por tarefa são propostas avaliáveis, não resultados observados neste ambiente.
Consultas registradas: V4C-Q009, V4C-Q014, V4C-Q028.

## T222:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T222 → T212 [complements]
Como combinar: Harness Uber usa ocupação para disparar compactação em seu perfil de contexto.
Interface: Uso observado, limiar configurado e política de compactação.
Condição: O limiar pertence ao modelo e backend usados.
Aceite proposto: Gatilho deixa margem e o resumo mantém informação necessária.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

2. T222 → T214 [complements]
Como combinar: O monitor identifica custo de ferramenta e orienta projeção antes da próxima transferência.
Interface: Previsão de payload e campos necessários.
Condição: Projeção preserva erro, identidade e completude.
Aceite proposto: Redução medida sem omissão de campo exigido pelo aceite.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Multimodalidade e mensagens ocultas do runtime podem invalidar estimativa textual simples.
- Compactar reduz ocupação futura, não apaga consumo acumulado da missão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de conclusão dentro da janela e custo total por tarefa entre portes. Um bom monitor torna limites previsíveis, mas não aumenta a capacidade intrínseca de raciocinar sobre informação excluída.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T152, T212, T214, T238

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S002 — Prompt caching

[https://platform.claude.com/docs/en/build-with-claude/prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reutilização computacional de prefixos de prompt; sem reutilização automática da resposta gerada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T223 — Constitutional Self-Check

**Nome canônico:** Constitutional Self-Check  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T223  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** principle based self check; checagem por princípios

## T223:C01 — conceito

Checagem de uma proposta contra princípios explícitos antes de concluir uma ação ou resposta. Neste catálogo, é uma adaptação de revisão por princípios durante a inferência. Constitutional AI descreve um método de treinamento mais amplo; executar uma autocrítica com regras não equivale a treinar ou reproduzir esse método.

Como funciona:
- Uma lista curta de princípios é traduzida em perguntas observáveis sobre a proposta.
- O revisor associa cada conclusão a trechos, resultados ou condições verificáveis.
- Uma revisão pode gerar correção, solicitação de evidência ou indicação de conflito ainda não resolvido.

Nota de nomenclatura: Adaptação editorial durante inferência; manter distinção explícita de Constitutional AI como método de treinamento.

## T223:C02 — aplicacao

Quando usar:
- Verificar aderência a especificações, qualidade de citações, requisitos de formato e limites operacionais de uma missão.

Quando não usar:
- Como único controle de permissão ou como certificação automática de segurança e correção do sistema.

Implementação proposta:
- Proposta: selecionar princípios relevantes ao tipo de alteração e definir o que comprova cada um.
- Submeter a proposta e suas evidências ao revisor, mantendo o texto das regras separado dos documentos analisados.
- Exigir resultado estruturado com critério, evidência, falha encontrada e correção sugerida.
- Executar validações determinísticas quando existir uma propriedade verificável por código ou contrato.
- Preservar críticas não resolvidas no encerramento; não repetir a revisão até obter artificialmente uma aprovação.

Aplicação LAI proposta:
Proposta LAI: aplicar revisão por princípios aos entregáveis de cada missão, com critérios pequenos e rastreáveis e validação automática das propriedades que permitirem isso.

## T223:C03 — riscos_validacao

Armadilhas:
- O mesmo modelo pode reproduzir o erro da proposta original.
- Regras vagas incentivam aprovação superficial.
- Uma crítica eloquente pode inventar problemas ou evidências inexistentes.

Métricas sugeridas:
- Falhas reais identificadas; falsos positivos; critérios com evidência; correções confirmadas; custo da revisão.

Testes propostos:
- Apresentar uma proposta que viola um critério explícito e verificar a localização exata do problema.
- Incluir um resultado de teste ausente e exigir reconhecimento da falta de evidência.
- Comparar aprovação do revisor com verificações determinísticas disponíveis.

## T223:C04 — perguntas_proveniencia

Pergunta: Isso é Constitutional AI completo?
Resposta: Não. O uso aqui é uma checagem em execução inspirada em revisão por princípios. A referência original inclui processos de treinamento que não são executados nesta base.

Pergunta: Uma aprovação do modelo autoriza uma operação?
Resposta: Não. Autorizações pertencem ao controle de acesso e às instruções válidas. Uma autochecagem fornece avaliação, não concessão de permissão.

Pergunta: Não encontrar uma violação prova conformidade?
Resposta: Não. Pode refletir cobertura limitada ou critério mal interpretado; o relatório deve explicitar escopo e evidência.

Pergunta: Preciso verificar novamente após uma correção?
Resposta: Sim, nas dimensões afetadas: o artefato mudou e a evidência anterior pode não valer para a nova versão.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T223:C05 — mecanismo_avancado

Uma autochecagem por princípios precisa testar aplicabilidade, evidência e conflito entre regras. Pedir apenas uma nota geral incentiva aprovação superficial. A proposta vincula cada princípio relevante a uma parte concreta do candidato e registra satisfeito, violado ou não determinado. Critério não aplicável não equivale a critério cumprido. Se a revisão altera o artefato, verificações afetadas precisam ser refeitas sobre a nova versão.

Condição de contorno:
Autocrítica pelo mesmo modelo pode reproduzir o erro inicial; concordância interna não substitui uma evidência externa disponível.

Contrato proposto:
- Entradas: Candidato versionado, princípios vigentes e evidências necessárias.
- Saídas: Diagnóstico por princípio, correções propostas e pontos inconclusivos.
- Estado: Versão das regras, aplicabilidade e artefato revisado.
- Invariante: Uma revisão não declara aprovação em dimensões para as quais não possui evidência.

Compromissos de projeto:
- Regras detalhadas tornam revisão mais rastreável e podem conflitar ou ocupar muito contexto.
- Checagem interna é barata relativamente a revisão externa e compartilha vieses do produtor.

## T223:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir dois princípios que exigem interpretação conflitante e um fato impossível de verificar; exigir identificação do conflito e inconclusão factual, sem nota única de aprovação.

Plano de avaliação proposto:
Comparar autochecagem, checklist determinístico e revisão independente em candidatos com violações conhecidas. Medir falsa aprovação, correções que introduzem defeitos e custo. Separar avaliação da proposta da avaliação do artefato já corrigido.

Comparações:
- T200 (complements): Verificação independente testa dimensões que a autochecagem pode interpretar incorretamente.
- T206 (complements): Verificação de processo acompanha se a sequência respeitou critérios definidos.

Afirmação rastreável:
Constitutional AI utiliza princípios em crítica e revisão como parte de um método de treinamento mais amplo.
Suporte: related; fontes: V2A-S020
Limite: A checagem de inferência desta ficha é adaptação editorial e não reproduz o treinamento descrito no paper.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T223:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculava princípios a evidências e estados de avaliação. A expansão trata a autochecagem como revisão limitada, define resposta a conflito e impede confundir crítica em inferência com treinamento constitucional.

Princípio operacionalizável
Traduza cada regra aplicável em uma pergunta verificável sobre o candidato. Exigir preservar a API pode gerar comparação de assinatura e testes; exigir clareza pode precisar de revisão humana ou critérios mais subjetivos. Não atribua a mesma força probatória aos dois tipos. Registre desconhecido quando falta evidência, em vez de aprovação por ausência de objeção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V2A-S020.

Conflito e precedência
Princípios podem entrar em tensão: brevidade versus cobertura, velocidade versus validação. Defina quais são restrições e quais são objetivos de otimização. O revisor não deve inventar precedência para aprovar a própria proposta; conflito material volta ao controlador com alternativas e consequências. Uma constituição longa e contraditória piora a verificabilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S020, V4C-S030.

Crítica muda a evidência
Se a autochecagem altera o artefato, verificações anteriores podem deixar de valer. Vincule o parecer à versão candidata e rerode critérios afetados. Separar gerador e crítico pode reduzir alguns vieses, mas modelos semelhantes ainda podem concordar no mesmo erro; use verificadores externos sempre que houver propriedade executável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S032.

USO AVANÇADO — Resposta técnica com fontes
Cenário: O agente precisa respeitar escopo, evidência e incerteza.
Estratégia: Revise alegações individuais: existe fonte, ela sustenta o detalhe e a limitação foi preservada? Marque inferência separadamente e remova certeza indevida. Não aceitar citação apenas porque o domínio parece confiável; conferir conteúdo quando a alegação importa.
Papel do modelo pequeno: 3–7B faz checklist estreito; 8–14B relaciona alegação e trecho; 15–30B examina conflitos.
Aceite proposto: Proposta: detectar alegações sem suporte e preservar lacunas sem bloquear conclusões sustentadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S032.

USO AVANÇADO — Patch com invariantes
Cenário: Uma mudança deve manter semântica e evitar adições fora do escopo.
Estratégia: Use revisões por propriedade e combine-as com compilação e testes. Uma violação obrigatória bloqueia o candidato mesmo que a maioria das avaliações seja positiva. Se a propriedade não puder ser provada pelo método, registrar limite e pedir verificação adequada.
Papel do modelo pequeno: 8–14B revisa propriedades locais; 15–30B analisa intenção e efeitos transversais.
Aceite proposto: Proposta: rejeitar violações inseridas e medir falsos negativos de cada critério.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Regras poucas, concretas e ligadas a trechos ou campos explícitos.
8–14B: Revisão de aderência com evidência recuperável e estado desconhecido permitido.
15–30B: Análise de conflitos e síntese de pareceres, mantendo validação externa independente.
Requisitos de treino/runtime: Versão das regras, versão do artefato e testes ligados a requisitos; critérios subjetivos precisam de calibração.
Não aplicar quando: Não tratar autoconcordância como prova formal nem chamar o procedimento de fine-tuning constitucional.

## T223:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean documenta revisão por propriedades, não adoção do rótulo Constitucional Self-Check. O componente desta ficha é composição editorial em inferência. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q006, V4C-Q027, V4D-Q023.

## T223:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T223 → T200 [complements]
Como combinar: Encaminhar propriedades objetivas a verificador externo e conservar o parecer textual como evidência de natureza diferente.
Interface: Critério, artefato e resultado observável.
Condição: Verificador não depende apenas da opinião do gerador.
Aceite proposto: Candidato elogiado mas reprovado em requisito objetivo é rejeitado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T223 → T221 [complements]
Como combinar: Usar a versão vigente do objetivo para selecionar princípios aplicáveis à revisão.
Interface: Meta, restrições e critérios de aceite.
Condição: Mudança autorizada atualiza a base da checagem.
Aceite proposto: Não reprovar ou aprovar por regra obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checklist preenchido não comprova que os itens foram verificados.
- Parecer sobre versão anterior não acompanha automaticamente a versão corrigida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare ganho incremental da autochecagem frente a verificação externa e frente a modelo de fronteira. O procedimento pode melhorar aderência, mas continua limitado por capacidade e vieses do crítico.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T185, T224, T217

## Fontes primárias associadas

### V2A-S020 — Constitutional AI: Harmlessness from AI Feedback

[https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Crítica e revisão guiadas por princípios, dentro de um método de treinamento mais amplo.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S022 — Function calling

[https://developers.openai.com/api/docs/guides/function-calling](https://developers.openai.com/api/docs/guides/function-calling)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas de ferramentas com esquema de argumentos, modo estrito e resultados associados.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T224 — Spec-Driven Loop

**Nome canônico:** Spec-Driven Loop  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T224  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** spec driven development loop; ciclo orientado por especificação

## T224:C01 — conceito

Ciclo que conecta especificação, plano de implementação, tarefas, alterações e evidências de aceitação. A especificação torna explícito o resultado esperado e permite avaliar mudanças sem depender da memória da conversa. Spec Kit é uma referência de organização desse fluxo; o padrão pode ser aplicado sem adotar uma ferramenta específica.

Como funciona:
- Requisitos identificados originam tarefas e critérios de aceitação rastreáveis.
- A implementação produz artefatos e evidências vinculados à versão da especificação.
- Divergências entre requisito, código e teste retornam ao planejamento ou à revisão da especificação.

## T224:C02 — aplicacao

Quando usar:
- Funcionalidades com múltiplos módulos, integração entre agentes e requisitos que precisam sobreviver a várias sessões.

Quando não usar:
- Produzir documentação extensa para mudanças triviais ou tratar toda decisão inicial como imutável mesmo diante de nova evidência.

Implementação proposta:
- Proposta: escrever objetivo, comportamento observável, restrições e exclusões relevantes em linguagem verificável.
- Atribuir identificadores aos critérios e decompor o trabalho em tarefas com entradas, saída e evidência de conclusão.
- Manter decisões de projeto e hipóteses separadas dos requisitos confirmados.
- Quando o pedido mudar, versionar a especificação e identificar tarefas e testes afetados.
- Conferir rastreabilidade entre resultado solicitado, alteração entregue e verificação realmente executada antes de encerrar.

Aplicação LAI proposta:
Proposta LAI: manter especificações curtas e versionadas por missão, permitindo que planejador e executores compartilhem critérios estáveis e revisem mudanças de escopo de forma rastreável.

## T224:C03 — riscos_validacao

Armadilhas:
- Especificações podem ser ambíguas ou inconsistentes.
- Um teste que replica a mesma interpretação errada não resolve a ambiguidade.
- Burocracia excessiva reduz velocidade sem aumentar confiança.

Métricas sugeridas:
- Critérios cobertos por evidência; mudanças sem requisito associado; divergências abertas; retrabalho por ambiguidade; tempo de revisão.

Testes propostos:
- Introduzir uma mudança de requisito e verificar identificação dos módulos e testes afetados.
- Selecionar um critério ao acaso e percorrer tarefa, alteração e resultado de verificação.
- Testar uma especificação contraditória e exigir resolução explícita antes da implementação correspondente.

## T224:C04 — perguntas_proveniencia

Pergunta: A especificação precisa determinar cada linha de código?
Resposta: Não. Ela deve definir comportamento, restrições e critérios suficientes; detalhes de implementação podem permanecer no plano e evoluir.

Pergunta: Como lidar com uma descoberta que invalida o plano?
Resposta: Registrar a evidência, revisar a decisão afetada e atualizar tarefas e testes. Não declarar o requisito cumprido apenas porque o plano anterior terminou.

Pergunta: Uma tarefa concluída no plano prova requisito satisfeito?
Resposta: Somente se sua saída cumprir o critério e a evidência estiver vinculada à versão vigente do requisito.

Pergunta: O que fazer quando a implementação revela premissa falsa?
Resposta: Revisar a especificação com a decisão correspondente e propagar o impacto, em vez de ocultar a divergência no código.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T224:C05 — mecanismo_avancado

Uma especificação operacional liga requisito, decisão de projeto, tarefa e evidência de aceitação. Quando o requisito muda, essa ligação permite localizar os artefatos afetados; sem ela, o plano pode continuar executando uma versão antiga. Spec Kit fornece processos e templates, mas preencher documentos não comprova convergência. A proposta trata ambiguidades como questões explícitas e preserva a origem das decisões que as resolveram.

Condição de contorno:
Uma especificação extensa, porém contraditória ou desatualizada, pode produzir execução consistente com o documento e incompatível com a intenção vigente.

Contrato proposto:
- Entradas: Objetivo, requisitos identificados, restrições e decisões autorizadas.
- Saídas: Plano, tarefas e matriz de evidências por requisito.
- Estado: Versões da especificação, decisões e vínculos com alterações.
- Invariante: Critério alterado invalida ou reavalia evidências produzidas sob a versão anterior.

Compromissos de projeto:
- Rastreabilidade reduz interpretação implícita e aumenta manutenção documental.
- Especificação muito prescritiva restringe soluções melhores descobertas durante a implementação.

## T224:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar um requisito após testes aprovados e antes da entrega; exigir identificação dos testes e artefatos que precisam ser reavaliados.

Plano de avaliação proposto:
Comparar execução por prompt amplo e por especificação rastreável em tarefas equivalentes. Medir ambiguidades tardias, retrabalho e requisitos sem evidência. Avaliar documento e produto separadamente; quantidade de arquivos não é métrica de completude.

Comparações:
- T217 (complements): Testes materializam parte dos critérios de aceitação da especificação.
- T213 (complements): Micro-missões precisam de vínculo com resultados exigidos, evitando fragmentação sem finalidade.

Afirmação rastreável:
Spec Kit oferece processos estruturados, templates e resultados documentados para agentes de programação.
Suporte: direct; fontes: V2A-S023
Limite: O repositório é uma ferramenta de organização; a qualidade da especificação e das evidências depende da aplicação.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T224:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 conectava requisito, tarefa e evidência. A expansão transforma essa rastreabilidade em mecanismo de mudança controlada, com especificação mínima suficiente e resolução explícita de ambiguidades.

Especificação executável onde possível
Separe intenção de detalhes escolhidos pelo implementador. Converta requisitos objetivos em exemplos, invariantes ou contratos verificáveis. Texto que apenas descreve a solução favorita do agente não serve como critério independente de aceite. Quando a propriedade é subjetiva, declare avaliador e exemplos de fronteira em vez de simular precisão matemática.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V4C-S030.

Mudança de requisito
Ao revisar a especificação, identifique decisões, patches e testes afetados. Preserve a versão anterior para explicar resultados já obtidos, mas impeça publicar um candidato que só satisfaz o contrato antigo. Uma alteração aparentemente pequena de comportamento pode invalidar muitos consumidores; a rastreabilidade torna esse alcance visível antes de continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S034.

Granularidade útil
Uma especificação deve permitir começar trabalho verificável sem tentar prever cada linha. Requisitos grandes demais deixam o agente preencher lacunas; excesso de detalhe cria custo de manutenção e congela decisões que deveriam ser locais. Use contratos de fronteira e exemplos para permitir autonomia dentro das restrições, com questões abertas explicitamente listadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S002.

USO AVANÇADO — Feature entregue por modelos pequenos
Cenário: Uma funcionalidade possui entradas, saída e regras claras.
Estratégia: Defina casos de aceite antes de distribuir micro-missões. Gere implementação por módulo e mantenha uma matriz de requisito para teste e artefato. Se o agente encontra ambiguidade que muda comportamento, interrompa essa parte e obtenha decisão; não trate palpite como requisito aprovado.
Papel do modelo pequeno: 3–7B implementa unidades; 8–14B cria candidatos de teste; 15–30B verifica coerência do contrato.
Aceite proposto: Proposta: todos os requisitos obrigatórios têm evidência na versão final e nenhum teste contradiz a intenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S034.

USO AVANÇADO — Refatoração com comportamento preservado
Cenário: A arquitetura muda, mas o contrato externo deve permanecer.
Estratégia: Especifique propriedades que não podem mudar e variações permitidas. Use comparação de comportamento, testes existentes e invariantes estruturais. Se o teste depende de implementação antiga sem necessidade de domínio, revise-o com justificativa, mantendo evidência independente da compatibilidade externa.
Papel do modelo pequeno: 8–14B altera módulos; 15–30B analisa efeitos de fronteira.
Aceite proposto: Proposta: preservação dos contratos externos e redução mensurada da complexidade definida pelo projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Implementação de contratos pequenos e bem exemplificados, sem interpretação extensa de linguagem vaga.
8–14B: Transformação de requisitos em candidatos de teste e identificação de inconsistências locais.
15–30B: Revisão de escopo e dependências entre requisitos, preservando origem das decisões.
Requisitos de treino/runtime: Especificação versionada, matriz de rastreabilidade e avaliação independente de implementação.
Não aplicar quando: Não considerar documento preenchido ou número de páginas como evidência de qualidade da especificação.

## T224:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Verificações expressam critérios de engenharia, sem afirmar um processo integral spec-driven.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Harness Codex oferece invariantes e planos operacionais; não foi tomado como prova de adoção específica do Spec Kit nem de um método universal com este nome.
Consultas registradas: V4C-Q007, V4C-Q027.

## T224:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T224 → T213 [feeds]
Como combinar: Dividir requisitos em micro-missões com saídas e testes ligados à mesma versão de especificação.
Interface: ID do requisito, contrato e critério de aceite.
Condição: Dependências entre requisitos estão explícitas.
Aceite proposto: Integração não deixa requisito sem dono ou sem prova.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T224 → T217 [complements]
Como combinar: Testes de comportamento materializam parte do contrato e orientam ciclos de reparo.
Interface: Exemplo esperado, teste executável e revisão do candidato.
Condição: O teste falha pela propriedade correta.
Aceite proposto: Não ajustar requisito para justificar implementação que falhou.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Spec desatualizada pode produzir software coerente com o documento e errado para a intenção atual.
- Gerador e avaliador precisam consultar a origem do requisito, não apenas suas interpretações recíprocas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare entrega de requisitos delimitados com o mesmo conjunto de testes e revisão. Uma arquitetura rigorosa pode ampliar utilidade de 3–30B sem provar que compreendem requisitos inéditos como modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T208, T213, T217, T221

## Fontes primárias associadas

### V2A-S023 — Spec Kit

[https://github.com/github/spec-kit](https://github.com/github/spec-kit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo de especificação, plano, tarefas, implementação e convergência; exemplo concreto de desenvolvimento guiado por especificações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S021 — Plan-and-Execute Agents

[https://www.langchain.com/blog/planning-agents](https://www.langchain.com/blog/planning-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de planejamento e execução; retorno ao planejador para revisão do plano.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V3C-S002 — An LLM Compiler for Parallel Function Calling

[https://proceedings.mlr.press/v235/kim24y.html](https://proceedings.mlr.press/v235/kim24y.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejador de chamadas, despacho de tarefas e executor paralelo.

Limite: Resultados do estudo não foram reproduzidos; ganho depende do grafo e do custo das ferramentas.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# T226 — Heartbeat de progresso

**Nome canônico:** Heartbeat de progresso  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** protocol  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T226  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** progress heartbeat; batimento de progresso

## T226:C01 — conceito

Sinal periódico de uma atividade acompanhado, quando adequado, de um marcador de avanço. O recebimento de heartbeat demonstra comunicação recente; somente a evolução de um marcador confiável indica progresso. Temporal documenta heartbeats de atividades e recuperação de detalhes registrados, sujeitos às condições de entrega e persistência do runtime.

Como funciona:
- O worker envia identidade, etapa e último avanço confirmado ao supervisor.
- O supervisor avalia idade do sinal e evolução do marcador em janelas distintas.
- Ausência de sinal pode acionar timeout, enquanto sinal estático pode acionar investigação de estagnação.

## T226:C02 — aplicacao

Quando usar:
- Atividades demoradas, processamento em lotes e operações que precisam oferecer visibilidade entre início e conclusão.

Quando não usar:
- Usar a emissão do heartbeat como comprovação de que uma escrita externa terminou ou de que o objetivo da missão foi cumprido.

Implementação proposta:
- Proposta: incluir execution_id, sequência de progresso, etapa e referência ao último resultado persistido.
- Usar o horário de recebimento para expiração e evitar depender apenas de relógios de máquinas diferentes.
- Persistir avanço antes de anunciá-lo como confirmado; tratar sinais atrasados e duplicados com identidade e ordenação.
- Definir prazo de silêncio considerando latência e duração legítima das etapas.
- Manter o heartbeat pequeno e separar detalhes extensos em artefatos consultáveis.

Aplicação LAI proposta:
Proposta LAI: expor progresso de missões por marcos confirmados, permitindo ao supervisor distinguir worker acessível, trabalho em andamento e execução sem avanço.

## T226:C03 — riscos_validacao

Armadilhas:
- Um timer independente pode emitir sinais enquanto o trabalho está travado.
- Perda do sinal gera falso diagnóstico de falha.
- Detalhes emitidos imediatamente antes da queda podem não ter sido persistidos pelo serviço.

Métricas sugeridas:
- Idade do último sinal; atraso de entrega; tempo sem avanço; sequência confirmada; falsos timeouts.

Testes propostos:
- Manter o timer ativo e bloquear o trabalho para verificar detecção de marcador estacionário.
- Entregar sinais fora de ordem e impedir regressão do estado observado.
- Interromper entre persistência e envio e confirmar recuperação a partir do registro durável.

## T226:C04 — perguntas_proveniencia

Pergunta: Heartbeat e progresso são a mesma coisa?
Resposta: Não. O sinal informa presença recente; o marcador informa avanço definido pelo domínio. Os dois devem ser observados separadamente.

Pergunta: O último heartbeat sempre permite retomar exatamente?
Resposta: Não. Ele pode estar atrasado ou conter informação apenas parcial. A retomada precisa validar o checkpoint e reconciliar resultados externos pendentes.

Pergunta: Heartbeatar a cada item elimina perda de progresso?
Resposta: Não necessariamente, porque o SDK pode agrupar envios e o processo pode cair antes da transmissão.

Pergunta: Por que cancelamento pode demorar?
Resposta: Porque a atividade pode receber o sinal por heartbeat, cuja frequência e throttling influenciam a entrega.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T226:C05 — mecanismo_avancado

Heartbeat local e heartbeat persistido não são o mesmo evento. Temporal pode limitar a frequência de envio e manter apenas o detalhe mais recente antes da transmissão. Um crash nesse intervalo pode perder o avanço ainda não entregue. O cursor recuperável deve indicar uma fronteira cuja reexecução seja segura: registrar progresso antes do efeito pode pular trabalho; registrar depois pode exigir repetir uma operação já realizada.

Condição de contorno:
O heartbeat comprova comunicação, mas somente um marcador ligado a trabalho confirmado sustenta retomada correta.

Contrato proposto:
- Entradas: Identidade da atividade, cursor confirmado, heartbeat timeout e detalhes de progresso.
- Saídas: Sinal enviado, estado conhecido pelo serviço e informação para próxima tentativa.
- Estado: Último cursor local, último persistido conhecido e efeitos associados.
- Invariante: O cursor não avança além do trabalho durável que pode ser reconstruído ou repetido com segurança.

Compromissos de projeto:
- Heartbeats frequentes reduzem atraso de detecção e aumentam tráfego, sujeito a throttling.
- Lotes maiores economizam comunicação e ampliam a quantidade de trabalho potencialmente repetido.

## T226:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: concluir um lote e derrubar o worker antes de o heartbeat chegar ao serviço; exigir retomada sem pular itens e sem duplicar efeitos lógicos.

Plano de avaliação proposto:
Comparar periodicidade por tempo e por lote, controlando custo e idempotência. Medir atraso de falha, perda de cursor recente, repetição e latência de cancelamento. Escolher fronteira de progresso pela semântica do trabalho.

Comparações:
- T060 (complements): Detalhes de heartbeat podem funcionar como pequeno checkpoint de atividade, dentro do contrato do runtime.
- T162 (complements): Idempotência protege itens cuja confirmação e progresso podem divergir durante falha.

Afirmação rastreável:
Temporal documenta throttling de heartbeats e entrega de cancelamento associada a eles.
Suporte: direct; fontes: V2A-S010
Limite: O progresso só sobrevive se for entregue ao serviço; chamadas locais não confirmam persistência imediata.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T226:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciava heartbeat local e persistido. A expansão define marcadores de avanço por fase, interpreta silêncio e lida com resultados atrasados sem converter comunicação frequente em falsa prova de progresso.

Progresso mensurável por fase
Durante download, bytes confirmados podem ser sinal útil; durante teste, casos concluídos; durante edição, artefato validado. Um contador que avança por token gerado não demonstra aproximação do objetivo. Cada fase declara qual marcador representa trabalho retomável e qual é apenas atividade do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040, V4C-S001.

Silêncio com contexto
Uma fase de computação longa pode não emitir avanço incremental observável. Defina duração esperada e sinal auxiliar de vida sem inventar cursor. Não reinicie automaticamente porque um marcador ficou estável durante uma operação indivisível legítima. A política precisa distinguir ausência de transporte, fase longa e repetição sem avanço semântico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040, V2A-S011.

Marcador e efeito
O cursor deve apontar para uma fronteira cuja retomada seja segura. Emiti-lo antes do efeito pode pular trabalho; depois do efeito pode permitir repetição. Combine marcador com identidade da operação e estado de confirmação. A frequência de heartbeat reduz janela de incerteza, mas não substitui idempotência nem transação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S040.

USO AVANÇADO — Processamento por lotes
Cenário: Uma atividade transforma milhares de registros.
Estratégia: Emita último lote confirmado e referência de saída, após persistência. Na retomada, valide existência e integridade do lote e continue da próxima unidade. Se a plataforma agrupa heartbeats, aceite que o último progresso local possa precisar de repetição segura.
Papel do modelo pequeno: 3–7B processa registros; código registra lotes e cursor.
Aceite proposto: Proposta: nenhuma lacuna e repetição limitada ao trecho cuja confirmação não chegou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S040.

USO AVANÇADO — Subagente em tarefa extensa
Cenário: O supervisor quer acompanhar progresso sem receber toda a conversa.
Estratégia: Publique fase, artefatos aceitos, bloqueios e último avanço significativo. Um ping de conexão continua separado. Se o trabalhador retorna apenas texto dizendo que está trabalhando, o supervisor não deve renovar indefinidamente o prazo da missão.
Papel do modelo pequeno: 8–14B resume estado tipado; 15–30B usa mudanças reais para replanejar.
Aceite proposto: Proposta: detectar trabalhador estagnado sem interromper etapas longas válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar unidades com confirmação externa simples, sem emitir progresso por autodeclaração.
8–14B: Converter resultados em estados de fase e impedimentos concretos.
15–30B: Avaliar se progresso observado sustenta continuidade, respeitando duração e custo restantes.
Requisitos de treino/runtime: Transmissão e persistência observáveis, cursor por geração e contrato para retomada de unidades.
Não aplicar quando: Não usar heartbeat MCP de conectividade como prova de progresso cognitivo ou de conclusão de ferramenta.

## T226:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Heartbeat descobre presença de servidores, sem comprovar progresso semântico de tarefa.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Temporal documenta semântica de heartbeat; gateway Uber documenta conectividade. Esses conceitos foram mantidos distintos, sem contar ping como adoção exata de progresso.
Consultas registradas: V4C-Q002, V4C-Q009.

## T226:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T226 → T225 [feeds]
Como combinar: Entregar ao watchdog marcadores confirmados e sinais separados de vida para decidir recuperação.
Interface: Fase, cursor, timestamp e geração.
Condição: O marcador tem significado definido para aquela atividade.
Aceite proposto: Restart só ocorre pela política correspondente ao tipo de falha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T226 → T240 [complements]
Como combinar: Incluir no snapshot o progresso que foi efetivamente confirmado, junto do estado correspondente.
Interface: Cursor e referência dos resultados persistidos.
Condição: Captura consistente, sem cursor posterior ao estado.
Aceite proposto: Retomada não pula trabalho ainda não incluído no snapshot.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040, V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Heartbeat frequente pode esconder ciclo se só relata atividade, não avanço.
- Resultado atrasado de geração antiga não deve atualizar o cursor atual sem validação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare detecção de falhas e custo de retomada com atividades iguais. Um modelo maior não torna seus sinais de progresso confiáveis sem vínculo a artefatos ou efeitos observáveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T218, T060, T243

## Fontes primárias associadas

### V2A-S010 — Detecting Activity failures

[https://docs.temporal.io/encyclopedia/detecting-activity-failures](https://docs.temporal.io/encyclopedia/detecting-activity-failures)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Timeouts de atividades, heartbeats, detalhes de progresso e tentativas posteriores.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V2A-S011 — Configure Liveness, Readiness and Startup Probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Probes de vida, prontidão e inicialização possuem efeitos operacionais distintos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T227 — Health Checks — liveness, readiness e progresso

**Nome canônico:** Health Checks — liveness, readiness e progresso  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T227  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** liveness readiness progress; verificações de saúde

## T227:C01 — conceito

Conjunto de verificações que diferencia processo capaz de funcionar, instância pronta para atender e trabalho avançando. Kubernetes documenta liveness, readiness e startup probes. Progresso de uma missão é uma verificação de domínio adicional, não um quarto tipo nativo de probe que deva ser presumido universal.

Como funciona:
- Liveness identifica condições em que reiniciar pode recuperar o processo.
- Readiness controla se a instância deve receber tráfego ou novas tarefas.
- Startup oferece tolerância durante inicialização; progresso avalia evolução de uma tarefa ativa segundo critérios próprios.

## T227:C02 — aplicacao

Quando usar:
- Serviços com inicialização demorada, workers que dependem de filas e execução de missões com marcos observáveis.

Quando não usar:
- Usar uma chamada cara a todas as dependências como liveness ou considerar um worker ocioso como estagnado.

Implementação proposta:
- Proposta: definir respostas distintas para processo travado, indisponibilidade temporária e falta de avanço.
- Verificar readiness antes de atribuir trabalho e informar motivos úteis sem expor dados sensíveis.
- Criar tolerância de startup compatível com carregamento e migrações autorizadas.
- Avaliar progresso apenas quando existe missão ativa, com prazo específico para a etapa.
- Manter checks leves, limitar sua frequência e registrar mudanças de estado com timestamps.

Aplicação LAI proposta:
Proposta LAI: publicar saúde operacional dos workers e saúde das missões separadamente, fazendo o controlador reagir à causa observada com critérios verificáveis.

## T227:C03 — riscos_validacao

Armadilhas:
- Uma dependência indisponível pode causar reinícios em massa se liveness for mal definida.
- Readiness positiva não prova correção funcional.
- Um endpoint saudável pode coexistir com fila parada ou resultados incorretos.

Métricas sugeridas:
- Duração em cada estado; falhas por tipo; reinícios desnecessários; atraso de atribuição; missões sem avanço.

Testes propostos:
- Indisponibilizar uma dependência compartilhada e verificar retirada de readiness sem tempestade de restart.
- Bloquear o processo de trabalho mantendo o endpoint ativo e conferir alarme de progresso.
- Simular inicialização longa dentro do prazo e evitar reinício prematuro.

## T227:C04 — perguntas_proveniencia

Pergunta: Readiness falha reinicia o processo?
Resposta: No modelo documentado de Kubernetes, readiness regula disponibilidade para tráfego; ela não equivale por si só ao gatilho de reinício de liveness.

Pergunta: Como medir progresso sem tarefas ativas?
Resposta: Não há avanço de missão a exigir. O estado deve ser ocioso ou aguardando, acompanhado de checks de capacidade para receber trabalho.

Pergunta: Readiness falsa deve sempre causar restart?
Resposta: Não. Frequentemente significa apenas que a instância não deve receber tráfego enquanto recupera capacidade.

Pergunta: Liveness verdadeira prova que a tarefa avança?
Resposta: Não. O processo pode responder a uma sonda simples enquanto uma missão está estagnada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T227:C05 — mecanismo_avancado

Falha de readiness deve retirar a instância do tráfego que depende dessa sinalização; não implica automaticamente matar o processo. Uma startup probe protege inicialização lenta contra liveness prematura. Progresso do agente requer outro invariante: uma API saudável pode hospedar uma missão parada. A proposta separa saúde do servidor, capacidade de atender e estado de cada trabalho, evitando um endpoint único que misture todas as causas.

Condição de contorno:
Uma probe que verifica apenas resposta HTTP pode passar enquanto filas, modelo ou tarefas específicas estão bloqueados.

Contrato proposto:
- Entradas: Sinais de inicialização, capacidade de atendimento, vida do processo e avanço por missão.
- Saídas: Estados separados e ação de operação apropriada a cada um.
- Estado: Histórico de sondas, dependências observadas e cursor de progresso.
- Invariante: Indisponibilidade de uma missão não é automaticamente convertida em reinício de todas as missões da instância.

Compromissos de projeto:
- Sondas profundas detectam mais falhas e podem aumentar carga sobre dependências já degradadas.
- Sondas leves são baratas e fornecem evidência restrita de funcionamento.

## T227:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inicialização lenta, dependência temporariamente indisponível e missão sem progresso em processo responsivo; exigir três diagnósticos e respostas diferentes.

Plano de avaliação proposto:
Comparar endpoint único e sinais separados sob falhas controladas. Medir reinícios indevidos, tráfego enviado a instância incapaz e tempo para detectar missão parada. Dimensionar frequência pelos custos e tempos de recuperação relevantes.

Comparações:
- T225 (complements): O supervisor utiliza sinais de saúde para escolher se reinicia ou espera.
- T226 (complements): Heartbeat com cursor pode fornecer evidência de progresso de uma atividade.

Afirmação rastreável:
Kubernetes diferencia startup, liveness e readiness e documenta que readiness e liveness não dependem uma da outra.
Suporte: direct; fontes: V2A-S011
Limite: Sinal de progresso é requisito adicional da aplicação, sem equivalência automática a um tipo nativo de probe.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T227:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava liveness, readiness e avanço da missão. A expansão propõe checagens por capacidade e classe de trabalho, com inicialização controlada e respostas de recuperação proporcionais ao que falhou.

Readiness por capacidade
Um servidor pode aceitar texto curto e não ter recursos para multimodalidade ou contextos longos. Exponha capacidades elegíveis e suas dependências, em vez de um único booleano que promete tudo. O roteador precisa considerar essa informação junto da quota; estar pronto para um contrato não significa estar pronto para qualquer tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V4C-S018.

Inicialização e aquecimento
Carregamento de pesos, conexão e compilação podem levar mais tempo que uma chamada comum. Use fase explícita de startup e só admita tráfego quando recursos necessários estiverem disponíveis. Falha de readiness durante aquecimento não deve disparar repetição infinita do próprio aquecimento. Teste também a primeira chamada depois de deploy.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V2A-S012.

Cheque funcional delimitado
Uma checagem semântica pode validar parser, tokenizer e chamada mínima compatível, mas não representa toda distribuição de tarefas. Mantenha sondas baratas e limites para não competir com o serviço principal. Se a dependência externa cair, retire apenas capacidades afetadas quando o isolamento permitir, preservando funções saudáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S011, V3C-S009.

USO AVANÇADO — Servidor de modelos local
Cenário: O processo responde HTTP enquanto o modelo ainda carrega ou ficou indisponível.
Estratégia: Separe endpoint de vida do estado de carregamento e da elegibilidade por recurso. Antes de liberar tráfego, execute contrato mínimo e registre configuração. Se um modelo falhar, não marque todos os outros como mortos quando compartilham processo mas têm isolamento válido.
Papel do modelo pequeno: 3–7B e 15–30B têm perfis diferentes; checagem usa capacidade real, não só nome.
Aceite proposto: Proposta: nenhuma admissão prematura e recuperação sem ciclos de startup.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V2A-S011.

USO AVANÇADO — Agente com várias ferramentas
Cenário: Algumas integrações falham, mas outras permanecem úteis.
Estratégia: Publique disponibilidade por ferramenta e mantenha tarefas dependentes em estado bloqueado. Não matar o supervisor saudável para corrigir API remota. Se a missão não progride apesar de todas as dependências prontas, encaminhe diagnóstico de tarefa, não uma falha genérica de servidor.
Papel do modelo pequeno: 8–14B explica degradação; controlador decide capacidade e ações.
Aceite proposto: Proposta: isolamento de falha e continuidade de trabalho independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Serviços pequenos podem ter startup mais simples, mas ainda precisam de contrato funcional.
8–14B: Classificar dependências afetadas por missão e produzir diagnóstico estruturado.
15–30B: Replanejar trabalho durante degradação sem redefinir saúde por opinião textual.
Requisitos de treino/runtime: Probes com escopo, limiares e consequências definidos; métricas de primeira chamada e tráfego admitido.
Não aplicar quando: Não misturar health de processo com qualidade de resposta ou progresso da missão.

## T227:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Kubernetes fundamenta probes; fontes de serving e gateways apoiam capacidades. O desenho por classes para agentes é proposta, sem ganho operacional medido.
Consultas registradas: V4C-Q004, V4C-Q018.

## T227:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T227 → T138 [complements]
Como combinar: Falhas funcionais de uma dependência alimentam breaker específico sem declarar todo o processo morto.
Interface: Capacidade afetada, classe da falha e janela observada.
Condição: Sonda corresponde ao caminho que o breaker protege.
Aceite proposto: Funções independentes continuam disponíveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S026, V2A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T227 → T226 [complements]
Como combinar: Progresso por tarefa complementa saúde do serviço e detecta missão parada em servidor saudável.
Interface: Fase, último avanço e identidade da missão.
Condição: Progresso é definido por domínio.
Aceite proposto: Detectar tarefa sem avanço sem reiniciar outras tarefas válidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Probe pesada pode causar a sobrecarga que pretende detectar.
- Não interpretar readiness negativa como ordem universal de matar o processo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare disponibilidade funcional por classe e tempo de recuperação. Um modelo pequeno que cabe no recurso pode manter uma capacidade específica, sem substituir funcionalidades que não suporta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T226, T218

## Fontes primárias associadas

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

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

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

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S026 — Polly — Circuit breaker resilience strategy

[https://www.pollydocs.org/strategies/circuit-breaker.html](https://www.pollydocs.org/strategies/circuit-breaker.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abertura por amostra, mínimo de throughput, sondagem após duração e separação de circuit breaker e retry.

Limite: Opções e defaults são da biblioteca; regras de coordenação distribuída não são inferidas automaticamente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# T229 — Diff-Only Editing / Patch-Based Coding

**Nome canônico:** Diff-Only Editing / Patch-Based Coding  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T229  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** patch based coding; edição por patch

## T229:C01 — conceito

Edição expressa como alterações localizadas sobre uma base conhecida, em vez de substituir desnecessariamente o conteúdo completo. Um patch descreve intenção e facilita revisão do delta. O formato compacto pode reduzir material transmitido, mas não garante aplicação correta nem preservação do comportamento fora do trecho alterado.

Como funciona:
- O agente lê uma revisão e produz um conjunto explícito de mudanças.
- O aplicador verifica precondições e tenta aplicar o delta à base correspondente.
- A validação posterior inspeciona tanto o patch final quanto os efeitos sobre contratos e dependentes.

## T229:C02 — aplicacao

Quando usar:
- Correções pontuais, revisões de código e colaboração em arquivos existentes com necessidade de rastrear mudanças.

Quando não usar:
- Forçar patches textuais para arquivos binários ou aceitar aplicação aproximada quando o alvo ficou ambíguo.

Implementação proposta:
- Proposta: identificar revisão, caminhos autorizados e hashes dos arquivos que serão alterados.
- Escolher formato suportado pelo aplicador, como unified diff ou substituições literais com contexto suficiente.
- Aplicar primeiro em área isolada ou validar a aplicabilidade antes de gravar.
- Se a base mudou, reler e reconstruir o patch a partir do conteúdo atual, preservando alterações independentes.
- Revisar o delta resultante e executar verificações proporcionais ao comportamento modificado.

Aplicação LAI proposta:
Proposta LAI: entregar alterações como patches rastreáveis ligados à missão e à revisão inicial, com validação antes de integração ao repositório principal.

## T229:C03 — riscos_validacao

Armadilhas:
- Um patch pequeno pode causar efeito amplo em uma API compartilhada.
- Correspondência por contexto não equivale a verificação criptográfica da base.
- Mudanças de formatação podem ocultar alterações semânticas relevantes.

Métricas sugeridas:
- Arquivos e linhas alterados; rejeições por base divergente; alterações fora do escopo; falhas após aplicação.

Testes propostos:
- Alterar a base após geração e verificar rejeição ou reconstrução consciente.
- Inspecionar o diff final para identificar mudanças não solicitadas.
- Testar um consumidor afetado por uma alteração pequena em contrato compartilhado.

## T229:C04 — perguntas_proveniencia

Pergunta: Diff-only significa que o agente não precisa ler o arquivo?
Resposta: Não. O delta deve ser fundamentado no conteúdo e no contrato atuais. Ler trechos relevantes continua necessário para formular uma mudança correta.

Pergunta: Qual a diferença para Unified Diff?
Resposta: Patch-based coding é o padrão de edição. Unified Diff é um formato específico para representar alterações textuais dentro desse padrão.

Pergunta: Um patch aplicado sem erro pode estar errado?
Resposta: Sim. Pode alterar um local semanticamente inadequado ou produzir comportamento incorreto apesar da compatibilidade textual.

Pergunta: Um diff do Aider é sempre Unified Diff?
Resposta: Não. O formato chamado diff pelo Aider usa blocos search/replace; formato e aplicador precisam corresponder.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T229:C05 — mecanismo_avancado

Uma edição baseada em patch define o delta sobre uma base, mas o aplicador determina como usa contexto e resolve conflitos. Em Git, aplicar à árvore de trabalho, ao índice ou a ambos são operações diferentes. A opção de merge em três vias depende de identidades de blobs e disponibilidade da base; não é uma forma genérica de adivinhar qualquer patch. Após aplicação, o delta efetivo precisa ser inspecionado, pois contexto parecido pode ocultar alvo errado.

Condição de contorno:
Patches pequenos podem ser ambíguos em trechos repetidos e não garantem preservação de comportamento fora da alteração.

Contrato proposto:
- Entradas: Patch, revisão-base, destino e modo de aplicação declarado.
- Saídas: Delta aplicado ou conflito explícito, com revisão resultante.
- Estado: Base, índice quando usado, arquivos alterados e resultado do aplicador.
- Invariante: A alteração efetiva permanece dentro do escopo pretendido e referenciada à base correta.

Compromissos de projeto:
- Contexto amplo reduz ambiguidade e aumenta tamanho transmitido.
- Merge em três vias pode aproveitar base conhecida e deixar conflitos que exigem resolução semântica.

## T229:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aplicar o mesmo hunk a arquivo com dois blocos parecidos e base divergente; exigir falha ou identificação inequívoca, seguida de inspeção do delta real.

Plano de avaliação proposto:
Comparar substituição integral, search/replace e patch em mudanças localizadas. Medir taxa de aplicação correta, conflitos, tokens e alterações involuntárias. Separar sucesso de aplicação e testes de comportamento.

Comparações:
- T230 (complements): Unified Diff é um formato possível para representar mudanças localizadas; edição por patches também admite outras convenções.
- T233 (complements): Validação verifica base, escopo e comportamento antes de considerar a edição concluída.

Afirmação rastreável:
git-apply diferencia árvore e índice e condiciona merge em três vias à presença de identidades e blobs necessários.
Suporte: direct; fontes: V2A-S014
Limite: O sucesso do aplicador verifica compatibilidade textual, sem demonstrar correção funcional da mudança.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T229:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia destinos de aplicação e merge em três vias. A nova camada escolhe o delta mínimo verificável, controla escopo de patch e separa representação compacta de garantia semântica.

Delta com identidade de base
O patch deve declarar a revisão contra a qual foi produzido e os caminhos permitidos. Antes de aplicar, verifique base ou prepare uma adaptação explícita. Uma alteração pequena pode atingir o lugar errado em código repetido; contexto e hash ajudam a detectar divergência, mas não substituem revisão do resultado efetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

Escopo do candidato
Avalie adições, remoções, modos, renomes e arquivos gerados. Um modelo que deveria mudar uma função pode incluir alterações em configuração ou testes para facilitar o aceite. Defina limites por tarefa e rejeite mudanças não justificadas, sem confundir pequeno número de linhas com baixo impacto: uma linha pode alterar todo o sistema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S034.

Formato conforme capacidade
Diffs reduzem saída quando o arquivo é grande, mas exigem localizar corretamente os trechos. Em arquivos curtos ou modelos com baixa aderência ao formato, emissão completa pode ser mais confiável. Compare taxa de aplicação e correção final, incluindo reparo de formato, em vez de escolher diff apenas pela economia nominal de tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S042.

USO AVANÇADO — Edição local com 3–7B
Cenário: A mudança afeta poucas linhas num arquivo conhecido.
Estratégia: Forneça trecho suficiente e base identificada, peça delta limitado e aplique em cópia isolada. Inspecione diff efetivo e execute teste focado. Se o patch não encaixar, releia a base atual antes de pedir reparo; não aumentar tolerância automaticamente até encaixar em qualquer lugar.
Papel do modelo pequeno: 3–7B produz delta curto; 8–14B diagnostica conflito de contexto.
Aceite proposto: Proposta: menos tokens por patch aceito, sem aumento de aplicação no alvo errado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S034.

USO AVANÇADO — Campanha de limpeza
Cenário: Muitas alterações repetitivas precisam ser auditáveis.
Estratégia: Use ferramenta estrutural quando a transformação for formalizável e apresente diff para revisão. Agrupe candidatos por regra e execute validações de propriedade. A saída compacta permite revisar intenção, mas a preservação de comportamento continua dependendo dos testes e dos limites da regra.
Papel do modelo pequeno: 8–14B classifica exceções; 15–30B integra conflitos entre mudanças.
Aceite proposto: Proposta: rastrear cada delta à regra e rejeitar alterações fora do objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Patches pequenos com delimitadores estáveis e baixa ambiguidade de localização.
8–14B: Edições em alguns arquivos, usando diagnóstico de conflito e contexto adicional.
15–30B: Planejamento de mudanças maiores cuja execução continua dividida em deltas verificáveis.
Requisitos de treino/runtime: Aplicador com contrato conhecido, árvore isolada, base identificada e revisão do diff realmente aplicado.
Não aplicar quando: Não aceitar patch porque aplicou sem erro nem interpretar tamanho pequeno como prova de segurança semântica.

## T229:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: A transformação produz mudanças de código, sem documentar que a representação e aplicação sejam exclusivamente patches localizados.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Correções são produzidas e revisadas, mas o relato não documenta um protocolo específico de edição exclusivamente por diffs.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta representações; AutoClean e Getafix mostram reparos e transformações, sem provar que toda mudança usa exatamente este protocolo de patch.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q023.

## T229:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T229 → T233 [complements]
Como combinar: Validar base, aplicação e comportamento antes de promover o candidato.
Interface: Patch, árvore base e resultados de verificação.
Condição: Testes correspondem aos bytes que serão entregues.
Aceite proposto: Rejeitar patch aplicado em revisão diferente sem nova validação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T229 → T232 [alternative]
Como combinar: Para padrões estruturais, gerar transformação AST e revisar o delta produzido em vez de pedir texto livre.
Interface: Regra, símbolos elegíveis e patch derivado.
Condição: Parser e resolução cobrem a linguagem e o caso.
Aceite proposto: Alteração preserva propriedades e falha explicitamente em ambiguidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009, V4C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mudanças de fim de linha podem inflar o diff e esconder alteração real.
- Não reformatar arquivos inteiros sem necessidade da tarefa, dificultando revisão e integração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare formatos com o mesmo modelo e tarefas antes de comparar portes. A redução de saída ajuda modelos pequenos, mas um patch sintaticamente correto ainda pode implementar a intenção errada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T230, T231, T233, T239

## Fontes primárias associadas

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T230 — Unified Diff

**Nome canônico:** Unified Diff  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** format  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T230  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** diff unificado

## T230:C01 — conceito

Formato textual de diferenças organizado por arquivos e blocos chamados hunks. Cada hunk informa intervalos na versão anterior e na nova e apresenta linhas mantidas, removidas e adicionadas. Git produz e consome variantes com metadados adicionais; esses detalhes precisam ser interpretados pelo aplicador correto.

Como funciona:
- Cabeçalhos identificam os arquivos anterior e posterior.
- Um cabeçalho de hunk descreve posição e extensão dos intervalos antigos e novos.
- Prefixos distinguem contexto, remoção e adição; o contexto ajuda a localizar a região afetada.

## T230:C02 — aplicacao

Quando usar:
- Revisão de código, transporte de alterações textuais e aplicação controlada em ferramentas que aceitam o formato.

Quando não usar:
- Usar um parser simplista para qualquer saída de Git ou tratar o formato textual básico como representação completa de binários e renomeações.

Implementação proposta:
- Proposta: gerar patches com ferramenta confiável, preservando conteúdo literal e quebras de linha.
- Registrar separadamente a revisão-base ou hashes quando a integridade da base for necessária.
- Usar um aplicador compatível com os metadados emitidos e validar caminhos antes da gravação.
- Inspecionar alterações de modo, renomeação e marcadores de fim de arquivo quando presentes.
- Após aplicar, comparar o resultado esperado ao diff efetivamente produzido e verificar o comportamento afetado.

Aplicação LAI proposta:
Proposta LAI: adotar unified diff como um formato possível de entrega de mudanças, acompanhado de identidade da base e validação independente do conteúdo.

## T230:C03 — riscos_validacao

Armadilhas:
- Os números de linha ficam desatualizados após mudanças concorrentes.
- Tabs, finais de linha e ausência de newline final podem ser relevantes.
- Um patch sintaticamente válido pode alterar o arquivo errado se o mapeamento de caminhos for incorreto.

Métricas sugeridas:
- Hunks aplicados e rejeitados; divergência de contexto; mudanças de caminho; diferenças inesperadas após aplicação.

Testes propostos:
- Aplicar um exemplo com múltiplos hunks e conferir exatamente as linhas resultantes.
- Testar arquivo sem newline final e preservação do estado esperado.
- Introduzir caminho fora do escopo e verificar rejeição pelo aplicador autorizado.

## T230:C04 — perguntas_proveniencia

Pergunta: Unified Diff inclui sempre o hash da base?
Resposta: Não. Cabeçalhos de hunk e linhas de contexto não fornecem, sozinhos, uma garantia criptográfica. Algumas variantes Git incluem informações adicionais, mas a política deve verificar o que está presente.

Pergunta: Aplicar sem erro prova correção?
Resposta: Não. Prova apenas que o aplicador aceitou as alterações nas condições observadas. Correção semântica exige revisão e verificações do comportamento.

Pergunta: Uma linha +++ sempre representa conteúdo adicionado?
Resposta: Não. Pode ser o cabeçalho do arquivo novo; a interpretação depende do estado do parser.

Pergunta: As posições tornam o patch independente da base?
Resposta: Não. Contexto e conteúdo esperado ainda precisam corresponder à revisão em que a alteração será aplicada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T230:C05 — mecanismo_avancado

No cabeçalho @@ -l,s +l,s @@, os intervalos descrevem posição e quantidade de linhas das versões antiga e nova; contagens omitidas representam casos unitários do formato. Linhas de contexto participam dos dois lados, remoções somente do antigo e adições somente do novo. Metadados Git podem incluir modos, renomes e IDs de blobs. Combined diff de merges possui outra estrutura e não deve ser tratado como patch comum de dois lados.

Condição de contorno:
Um parser que reconhece apenas linhas iniciadas por mais e menos pode confundir cabeçalhos, conteúdo e mudanças de metadados.

Contrato proposto:
- Entradas: Diff, dialeto de formato, base e convenção de caminhos.
- Saídas: Hunks interpretados, mudanças de arquivo e diagnóstico de inconsistência.
- Estado: Contagens por lado, arquivo corrente e metadados de versão.
- Invariante: As contagens do hunk correspondem às linhas que cada lado realmente contém.

Compromissos de projeto:
- Metadados adicionais melhoram identificação e exigem parser compatível.
- Contexto mínimo reduz tamanho e aumenta fragilidade diante de alterações próximas.

## T230:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir criação, remoção, renome e marcador de ausência de newline; conferir que o parser distingue metadados de linhas editáveis e preserva conteúdo final.

Plano de avaliação proposto:
Comparar parser simples e aplicador oficial sobre patches com casos-limite. Medir rejeição de hunks malformados, equivalência dos bytes produzidos e tratamento de modos. Usar a base exata para não atribuir conflito legítimo a defeito do formato.

Comparações:
- T229 (complements): Patch-based coding escolhe a estratégia de edição; Unified Diff fornece uma representação específica.
- T231 (distinct_from): Search/replace identifica texto literal e usa outro contrato de localização.

Afirmação rastreável:
A documentação Git distingue patch de dois lados e combined diff, além de cabeçalhos estendidos.
Suporte: direct; fontes: V2A-S013
Limite: Nem todo texto visualmente parecido com diff é aceito pelo mesmo aplicador ou representa os mesmos metadados.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T230:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descrevia hunks e diferenças de metadados. A ampliação trata Unified Diff como linguagem de entrada não confiável, com parsing completo, política de caminhos e verificação de que a aplicação produziu o delta pretendido.

Parser antes de aplicação
Valide cabeçalhos, contagens e sequência de hunks antes de modificar arquivos. Linhas que parecem metadados podem fazer parte do conteúdo, e mensagens extras de um modelo não pertencem ao patch. Defina quais extensões do formato o aplicador aceita; rejeitar explicitamente um formato não suportado é melhor que interpretar parcialmente e continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V2A-S013.

Caminhos e tipos de objeto
Normalize caminhos segundo a semântica do aplicador e confira escopo permitido. Renome, symlink, permissão executável e arquivo binário não são simples mudanças de linhas. Uma tarefa de texto pode proibir essas operações; se forem necessárias, devem ter contrato próprio. O validador precisa examinar tanto cabeçalho quanto resultado no filesystem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

Aplicação observada
Depois de aplicar, recalcule o diff da árvore resultante e compare com intenção e escopo. Contexto deslocado, normalização de quebras de linha ou tolerância do aplicador podem alterar a interpretação. Se a base divergiu, faça merge suportado ou gere novo candidato com leitura atual; não trate números de linha como endereço absoluto independente de versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034.

USO AVANÇADO — Editor restrito por protocolo
Cenário: Um modelo pequeno retorna somente um patch para alteração local.
Estratégia: Forneça exemplo mínimo do formato aceito e proíba prosa dentro da saída consumida. Faça parsing e aplicação em sandbox, valide contagens e arquivo alvo e devolva erro estruturado em caso de rejeição. O reparo recebe a causa específica, sem executar fragmentos de patch válidos isoladamente.
Papel do modelo pequeno: 3–7B emite hunks pequenos; 8–14B corrige representação a partir do erro.
Aceite proposto: Proposta: nenhuma aplicação parcial silenciosa e alta taxa de formato válido sem reduzir teste semântico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S013, V3C-S034.

USO AVANÇADO — Mudança com vários arquivos
Cenário: Um patch inclui renome e edição de conteúdo.
Estratégia: Declare previamente se o fluxo aceita renomes e modos. Verifique que o destino não colide com arquivo existente e que o diff final corresponde à movimentação esperada. Rode testes sobre a árvore inteira resultante, não sobre cada hunk isolado.
Papel do modelo pequeno: 15–30B pode planejar relações; aplicador determinístico executa operação validada.
Aceite proposto: Proposta: caminhos corretos, metadados preservados e nenhuma alteração fora do conjunto autorizado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Hunks curtos e exemplos consistentes são mais tratáveis que patches extensos com metadados mistos.
8–14B: Reparo de formato e identificação de conflito de contexto em múltiplos arquivos.
15–30B: Planejamento de mudanças maiores, mantendo parsing e aplicação fora da LLM.
Requisitos de treino/runtime: Aplicador versionado, política de extensões, normalização conhecida e validação em árvore isolada.
Não aplicar quando: Não confundir Aider diff, udiff adaptado e Unified Diff padrão nem aceitar combined diff como patch comum.

## T230:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Formato udiff documentado é baseado em diffs, com convenção própria; não é edição AST.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação Git e Aider apoia formatos e distinções. Não foi inferida produção de Unified Diff apenas porque uma empresa usa controle de versões. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q023, V4C-Q015, V4D-Q024.

## T230:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T230 → T229 [complements]
Como combinar: Unified Diff pode representar o delta de uma estratégia de edição por patch, conforme o aplicador escolhido.
Interface: Hunks, metadados e revisão base.
Condição: Formato e extensões são explicitamente suportados.
Aceite proposto: Delta aplicado corresponde à intenção e ao escopo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S034, V2A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T230 → T233 [feeds]
Como combinar: Entregar a árvore candidata e a identidade da base para validação antes de publicação.
Interface: Patch parseado, árvore resultante e hashes.
Condição: Nenhum erro de aplicação foi ignorado.
Aceite proposto: Verificação final incide sobre o artefato exato a ser publicado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar extração ingênua de linhas com mais ou menos como parser.
- Marcadores de ausência de newline e mudanças CRLF precisam de tratamento conforme o aplicador real.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare aderência ao formato, sucesso de aplicação e correção separadamente. Modelos pequenos podem emitir diffs bons em casos curtos; isso não garante competência em mudanças arquiteturais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T233

## Fontes primárias associadas

### V2A-S013 — diff-format

[https://git-scm.com/docs/diff-format](https://git-scm.com/docs/diff-format)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estrutura de diferenças produzidas pelo Git; cabeçalhos e hunks de alterações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T231 — Search/Replace Editing

**Nome canônico:** Search/Replace Editing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T231  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** search replace blocks; edição por substituição literal

## T231:C01 — conceito

Edição por pares de texto a localizar e texto substituto, com escopo explícito. É apropriada para alterações literais quando o alvo pode ser identificado sem ambiguidade. Aider documenta formatos dessa família; diferenças de sintaxe entre ferramentas não devem ser ignoradas pelo agente que produz a edição.

Como funciona:
- O aplicador procura o texto original dentro de um arquivo conhecido.
- A operação confirma o número esperado de ocorrências e as precondições da base.
- Somente então substitui o trecho, preservando o conteúdo restante segundo o contrato do editor.

## T231:C02 — aplicacao

Quando usar:
- Rewording, correção de constantes e pequenos ajustes em blocos com contexto literal suficiente.

Quando não usar:
- Renomeação semântica que depende de escopo ou substituição global de uma palavra comum sem análise dos alvos.

Implementação proposta:
- Proposta: ler o trecho exato e registrar caminho, hash da base e quantidade esperada de correspondências.
- Incluir contexto inalterado suficiente para identificar uma ocorrência única, sem ampliar a mudança pretendida.
- Agrupar substituições independentes com semântica clara: todas sobre a base original ou sequenciais, conforme o aplicador.
- Se o alvo não existir ou houver duplicidade, reler e reconstruir a operação; não improvisar correspondência aproximada.
- Verificar o conteúdo final e o diff para confirmar que somente os alvos pretendidos mudaram.

Aplicação LAI proposta:
Proposta LAI: usar substituições literais protegidas por base para edições pequenas, preservando rastreabilidade do texto original e escalando transformações semânticas para análise estrutural.

## T231:C03 — riscos_validacao

Armadilhas:
- Espaços, escapes e finais de linha alteram a correspondência literal.
- Regras sequenciais podem fazer uma substituição afetar o resultado de outra.
- Uma ocorrência única ainda pode estar no módulo errado.

Métricas sugeridas:
- Correspondências esperadas e encontradas; rejeições por ambiguidade; alterações fora do alvo; conflitos de versão.

Testes propostos:
- Criar duas ocorrências do mesmo trecho e exigir desambiguação.
- Alterar a base entre leitura e escrita e conferir o guard de versão.
- Testar substituições que se sobrepõem e verificar rejeição ou ordenação expressamente definida.

## T231:C04 — perguntas_proveniencia

Pergunta: Search/replace é sempre regex?
Resposta: Não. O padrão desta entrada é literal. Expressões regulares adicionam outra linguagem e exigem escopo, escaping e critérios de correspondência próprios.

Pergunta: Posso substituir todas as ocorrências?
Resposta: Somente quando esse conjunto é o alvo intencional e foi verificado. Uma operação global não deve ser inferida a partir de uma ocorrência solicitada.

Pergunta: Nenhuma ocorrência deve provocar uma substituição aproximada automática?
Resposta: Não por padrão. Pode haver revisão incorreta; o erro precisa ser diagnosticado antes de relaxar a correspondência.

Pergunta: Duas ocorrências iguais podem ser ambas corretas?
Resposta: Sim, quando o objetivo exige alterar ambas e o contrato declara isso; igualdade textual sozinha não decide.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T231:C05 — mecanismo_avancado

O contrato de search/replace precisa declarar cardinalidade esperada: zero correspondências significa base divergente ou busca inadequada; várias podem indicar ambiguidade. Trocar todas as ocorrências é uma decisão semântica adicional. Espaços, quebras de linha e normalização influenciam matching; tolerância aumenta taxa de aplicação e pode atingir um bloco parecido que não era o alvo. No Aider, o formato diff usa esses blocos e não deve ser confundido com Unified Diff.

Condição de contorno:
Texto repetido ou código gerado pode inviabilizar localização única sem aumentar contexto ou usar estrutura sintática.

Contrato proposto:
- Entradas: Arquivo versionado, trecho de busca, substituição e quantidade esperada de ocorrências.
- Saídas: Alteração aplicada ou diagnóstico de ausência e ambiguidade.
- Estado: Hash-base, ocorrências localizadas e conteúdo resultante.
- Invariante: A cardinalidade e o escopo observados correspondem ao pedido antes da substituição.

Compromissos de projeto:
- Matching exato é previsível e sensível a pequenas mudanças de formatação.
- Matching tolerante aceita mais variações e exige confirmação mais forte do alvo semântico.

## T231:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir o mesmo trecho em duas funções e alterar whitespace em apenas uma; exigir rejeição da ambiguidade ou seleção por contexto explícito.

Plano de avaliação proposto:
Comparar matching exato, tolerante e edição estrutural em bases com repetição controlada. Medir aplicação correta, alterações fora do alvo e tokens necessários para desambiguar. Escolher o método por risco de colisão e complexidade da mudança.

Comparações:
- T230 (distinct_from): Unified Diff inclui hunks e intervalos; blocos search/replace localizam conteúdo literal.
- T232 (alternative): Edição sintática pode distinguir símbolos iguais em escopos diferentes.

Afirmação rastreável:
Aider descreve seu formato diff como uma série de blocos de busca e substituição.
Suporte: direct; fontes: V2A-S008
Limite: A semântica precisa de matching depende do aplicador; esta ficha propõe cardinalidade e validação explícitas.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T231:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definia cardinalidade e ambiguidade. A expansão organiza seleção de âncoras, múltiplas substituições dependentes e alternativas quando o formato textual não consegue localizar o alvo de forma inequívoca.

Âncora suficiente
A busca deve conter contexto capaz de distinguir o trecho sem copiar arquivo inteiro. Inclua estrutura envolvente quando nomes ou blocos se repetem. Uma âncora maior aumenta custo e pode ficar obsoleta após mudanças não relacionadas; escolha o menor trecho cuja unicidade foi verificada na revisão atual, e não apenas presumida pelo modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S033.

Ordem de substituições
Duas operações podem interagir: a primeira altera a âncora da segunda. Defina se todos os searches referem-se à base original ou ao estado sucessivo e aplique consistentemente. Quando o protocolo não garante atomicidade, prepare todas as mudanças em cópia e publique apenas após validar o conjunto, evitando arquivo parcialmente editado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S027.

Escalonamento da localização
Zero ou múltiplas correspondências devem gerar diagnóstico específico. Releia a região e amplie contexto; se continuar ambíguo, use símbolo e parser ou escolha outro formato. Tolerância a espaços precisa ser explícita e não pode transformar duas funções parecidas em alvos intercambiáveis. Localização é parte da correção da edição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S035.

USO AVANÇADO — Correção curta em arquivo grande
Cenário: Um 3–7B precisa alterar um bloco conhecido.
Estratégia: Forneça região atual, peça SEARCH exato e REPLACE completo, conte correspondências e aplique só quando a cardinalidade esperada for satisfeita. Mostre o diff efetivo e rode verificação local. Se falhar a busca, não pedir ao modelo para inventar uma versão provável do arquivo.
Papel do modelo pequeno: 3–7B produz blocos curtos; 8–14B escolhe contexto adicional para desambiguar.
Aceite proposto: Proposta: nenhuma substituição no bloco errado e menor saída que reemitir o arquivo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008.

USO AVANÇADO — Mudanças sequenciais relacionadas
Cenário: Uma assinatura e seus usos locais precisam mudar juntos.
Estratégia: Planeje substituições sobre uma base definida, verifique sobreposição e simule todas em árvore isolada. Se uma mudança invalida outra, regenere o conjunto a partir da revisão atual. Após aplicar, confirme que não sobraram consumidores incompatíveis no escopo relevante.
Papel do modelo pequeno: 8–14B organiza blocos; 15–30B analisa dependências entre arquivos.
Aceite proposto: Proposta: aplicação completa ou rejeição explícita, sem estados intermediários publicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Blocos curtos, âncoras únicas e poucos delimitadores favorecem aderência ao protocolo.
8–14B: Seleção de contexto e diagnóstico de correspondências ambíguas.
15–30B: Planejamento de alterações múltiplas; aplicar com ferramenta determinística e verificação de conjunto.
Requisitos de treino/runtime: Leitura atual do arquivo, contagem de matches, política de whitespace e staging isolado.
Não aplicar quando: Não substituir todas as ocorrências por padrão nem usar aproximação textual quando houver alvos semanticamente distintos.

## T231:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: SEARCH/REPLACE é formato explicitamente descrito.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta o formato como recurso; não foram encontrados dez deployments de bigtech com este protocolo exato, e udiff não foi confundido com SEARCH/REPLACE.
Consultas registradas: V4C-Q023, V4C-Q006.

## T231:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T231 → R019 [complements]
Como combinar: Usar o formato SEARCH/REPLACE documentado do Aider quando o modelo consegue seguir seus delimitadores.
Interface: Caminho, bloco SEARCH e bloco REPLACE.
Condição: Formato selecionado corresponde ao contrato do editor efetivo.
Aceite proposto: Rejeitar zero ou múltiplos alvos não autorizados e verificar diff.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S008, V3C-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T231 → T232 [alternative]
Como combinar: Trocar localização textual por seleção estrutural quando o símbolo e seu vínculo precisam de precisão adicional.
Interface: Nó, escopo e intenção de transformação.
Condição: Parser e resolução semântica cobrem o caso.
Aceite proposto: Mesmo nome em outro escopo permanece inalterado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não aplicar primeiro bloco e ignorar rejeição dos seguintes.
- Strings de código gerado podem repetir um trecho válido sem serem o alvo autorizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de localização correta, aplicação e testes entre formatos sob o mesmo modelo. Melhor aderência textual de 3–30B não demonstra equivalência em entender efeitos da mudança.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T232, T233

## Fontes primárias associadas

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V3C-S035 — LibCST — Codemods

[https://libcst.readthedocs.io/en/latest/codemods.html](https://libcst.readthedocs.io/en/latest/codemods.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework de transformações, metadata e passes para codemods sobre CST.

Limite: Transformação automatizada não comprova comportamento preservado; validação depende do contrato da mudança.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T232 — AST Editing

**Nome canônico:** AST Editing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T232  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** structural editing; codemod; CST Editing

## T232:C01 — conceito

Transformação de código por sua estrutura sintática, como nós de funções, chamadas ou declarações. Uma árvore abstrata de sintaxe, AST, pode omitir comentários e detalhes de formatação. Ferramentas de árvore concreta, CST, como LibCST para Python, preservam esses elementos e são úteis para mudanças estruturais com fidelidade textual.

Como funciona:
- O parser converte código em nós e relações estruturais.
- Um transformador seleciona nós por critérios explícitos e modifica propriedades definidas.
- A serialização reconstrói o código, seguido de análise sintática e verificação semântica adequada ao caso.

## T232:C02 — aplicacao

Quando usar:
- Migrações repetitivas de APIs, inserção de argumentos e refatorações que exigem compreender a estrutura do código.

Quando não usar:
- Assumir que uma transformação sintática conhece automaticamente resolução de nomes, comportamento dinâmico ou contratos externos.

Implementação proposta:
- Proposta: escolher parser compatível com a linguagem e versão do projeto.
- Definir o padrão estrutural alvo e condições de exclusão, incluindo escopo e importações quando necessários.
- Usar análise de bindings para distinguir símbolos homônimos; marcar casos dinâmicos para revisão.
- Transformar uma cópia, reanalisar o resultado e inspecionar o diff.
- Executar exemplos positivos, negativos e verificações do comportamento afetado antes de ampliar a migração.

Aplicação LAI proposta:
Proposta LAI: preparar codemods limitados por linguagem e padrão, com amostragem revisável e exceções explícitas para casos que a análise estrutural não resolve.

## T232:C03 — riscos_validacao

Armadilhas:
- Renomear por nome de nó pode atingir variáveis locais sem relação com a API.
- ASTs podem perder comentários importantes.
- Sintaxe válida não demonstra equivalência funcional nem compatibilidade de versões.

Métricas sugeridas:
- Alvos transformados; falsos alvos; alterações de formatação; arquivos que não parseiam; regressões por padrão migrado.

Testes propostos:
- Criar duas funções homônimas em escopos diferentes e transformar somente a pretendida.
- Verificar preservação de comentários quando essa propriedade for exigida.
- Aplicar novamente a transformação para testar idempotência, quando esse for o contrato desejado.
- Incluir uma chamada dinâmica e exigir indicação de cobertura incompleta.

## T232:C04 — perguntas_proveniencia

Pergunta: AST Editing e CST Editing são iguais?
Resposta: Não. Ambas operam sobre estrutura, mas a representação concreta retém detalhes textuais que uma AST frequentemente descarta.

Pergunta: Uma refatoração por AST dispensa testes?
Resposta: Não. Ela melhora a precisão da seleção sintática, mas não prova que os consumidores e efeitos do código preservam o comportamento esperado.

Pergunta: Uma árvore sintaticamente válida prova refatoração correta?
Resposta: Não. A mudança pode atingir outro vínculo ou alterar comportamento, apesar de preservar a gramática.

Pergunta: Posso reutilizar metadados depois de substituir nós?
Resposta: Somente conforme o contrato da ferramenta; referências por identidade podem pertencer à árvore anterior e precisar de nova resolução.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T232:C05 — mecanismo_avancado

Renomear um identificador exige resolver vínculo, não somente reconhecer um nó Name. O mesmo texto pode referir-se a importação, variável local ou símbolo sombreado. LibCST oferece metadados de escopo e nomes qualificados, inclusive múltiplos candidatos em situações condicionais. Uma transformação deve preservar ambiguidades não resolvidas em vez de escolher um vínculo arbitrário. Após mudar a árvore, metadados da versão anterior podem precisar ser recalculados.

Condição de contorno:
Reflexão, geração dinâmica de nomes e imports condicionais podem impedir resolução estática completa.

Contrato proposto:
- Entradas: Árvore da revisão atual, metadados de escopo, alvo semântico e regra de transformação.
- Saídas: Código transformado, locais alterados e casos não resolvidos.
- Estado: Versão do parser, árvore de origem e metadados associados.
- Invariante: Uma transformação usa metadados da mesma árvore cuja identidade está sendo analisada.

Compromissos de projeto:
- CST preserva comentários e formatação com maior complexidade de estrutura.
- Análise estática reduz colisões textuais e não cobre toda semântica dinâmica da linguagem.

## T232:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar o mesmo identificador em importação, parâmetro e variável sombreada, além de import condicional; alterar somente o vínculo especificado e reportar ambiguidade restante.

Plano de avaliação proposto:
Comparar substituição textual e codemod em casos com escopos variados. Medir mudanças corretas, preservação de comentários, parse após edição e comportamento. Testes funcionais continuam necessários mesmo quando a transformação produz sintaxe válida.

Comparações:
- T231 (alternative): Busca literal é mais simples quando o alvo é inequívoco; estrutura ajuda quando texto igual possui significados diferentes.
- T216 (complements): O mapa do repositório orienta descoberta de símbolos, mas não substitui metadados do trecho editado.

Afirmação rastreável:
QualifiedNameProvider do LibCST pode devolver múltiplos nomes possíveis para um nó em situações como imports condicionais.
Suporte: direct; fontes: V3C-S033
Limite: Os metadados são análise estática e não demonstram qual caminho foi executado em todos os ambientes.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T232:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava resolução de vínculos e metadados. A expansão seleciona regras estruturalmente elegíveis, separa transformação determinística de decisão semântica e usa recusa explícita para os casos que a análise não cobre.

Pré-condições da regra
Declare padrões aceitos, contexto de escopo e propriedades a preservar antes de transformar. Uma remoção de flag pode exigir conhecer seu valor definitivo e distinguir expressões com efeitos. Quando a pré-condição não pode ser comprovada, encaminhe exceção para análise em vez de aplicar a regra por similaridade de árvore.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S008, V4C-S009.

AST, CST e emissão
A árvore abstrata representa sintaxe relevante ao compilador, mas comentários e formatação podem exigir árvore concreta ou mecanismo de preservação. Escolha a representação conforme o objetivo, incluindo linguagem e parser. Após modificar, reanalise o resultado e atualize metadados; objetos de escopo calculados antes da mudança podem não continuar válidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S035, V4C-S006.

LLM como controlador de exceções
Use modelo para interpretar diagnóstico, selecionar regra ou analisar contexto que a ferramenta não resolveu. Não peça à LLM para reproduzir manualmente uma transformação mecânica bem definida sem necessidade. Essa divisão reduz geração livre, mas a decisão de que a regra se aplica continua exigindo evidência e teste.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S006.

USO AVANÇADO — Limpeza de feature flags
Cenário: Código tem caminhos mortos após decisão operacional confirmada.
Estratégia: Valide estado da flag e escopo dos repositórios, execute transformação estrutural e gere diff. Rode CI e verificações adicionais de intenção. Casos dinâmicos ou referências não resolvidas permanecem pendentes; a ferramenta não deve adivinhar o valor por nome ou frequência de uso.
Papel do modelo pequeno: 3–7B classifica resultados simples; 8–14B trata exceções; 15–30B integra impacto entre módulos.
Aceite proposto: Proposta: eliminar apenas caminhos elegíveis e rejeitar mudanças sem evidência da pré-condição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S008, V4C-S009.

USO AVANÇADO — Renome de API
Cenário: Um símbolo aparece em múltiplos escopos e linguagens.
Estratégia: Resolva referências no escopo suportado, transforme consumidores elegíveis e produza lista de ocorrências não classificadas. Teste imports, geração de código e acesso dinâmico separadamente. Um grep final ajuda a localizar resíduos, mas ausência textual não prova preservação de comportamento.
Papel do modelo pequeno: 8–14B analisa ocorrências não resolvidas; ferramentas fazem renome verificável.
Aceite proposto: Proposta: nenhuma alteração em símbolo sombreado e compatibilidade de consumidores testados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S035, V4C-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Seleção de regra estreita e interpretação de saída estruturada, sem simular parser por linguagem natural.
8–14B: Diagnóstico de exceções locais e proposta de pré-condições adicionais.
15–30B: Análise de mudanças entre módulos e decisão de quais casos exigem revisão mais forte.
Requisitos de treino/runtime: Parser compatível, resolução de escopo, fontes de pré-condição e testes sobre o resultado emitido.
Não aplicar quando: Não generalizar transformação estática a reflexão e código gerado sem procedimento específico.

## T232:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: A fonte identifica diferenças e modificações em AST para construir reparos.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Transformações determinísticas de código ficam no PolyglotPiranha.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Piranha/AutoClean e Getafix fornecem casos operacionais específicos. Transferência para bandas de parâmetros é proposta; ferramentas não são apresentadas como LLMs pequenas.
Consultas registradas: V4C-Q005, V4C-Q006.

## T232:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T232 → T140 [complements]
Como combinar: AutoClean expõe Piranha por MCP para que o agente invoque transformação estrutural.
Interface: Regra, argumentos e resultado da ferramenta.
Condição: A tarefa é elegível ao mecanismo determinístico.
Aceite proposto: Revisar o delta e tratar exceções sem alterar o objetivo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T232 → T217 [complements]
Como combinar: AutoClean executa CI e encaminha falhas a reparadores após a transformação.
Interface: Patch, logs e classe de falha.
Condição: Reparadores respeitam escopo e validam novamente.
Aceite proposto: Verde de CI não dispensa verificações de propriedade.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Mesmo identificador textual pode ter vínculos diferentes; preservar ambiguidade não resolvida.
- Aprovação por LLM de preservação semântica não equivale a prova formal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare LLM pequena com ferramenta estrutural e modelo de fronteira editando livremente usando os mesmos testes. O ganho pode vir da ferramenta e da restrição do problema, não de inteligência geral equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T231, T229, T217

## Fontes primárias associadas

### V2A-S015 — LibCST documentation

[https://libcst.readthedocs.io/en/latest/](https://libcst.readthedocs.io/en/latest/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore sintática concreta para transformações Python preservando formatação, comentários e parênteses.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V3C-S035 — LibCST — Codemods

[https://libcst.readthedocs.io/en/latest/codemods.html](https://libcst.readthedocs.io/en/latest/codemods.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework de transformações, metadata e passes para codemods sobre CST.

Limite: Transformação automatizada não comprova comportamento preservado; validação depende do contrato da mudança.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T233 — Patch Validation — incluindo verificação de hash-base

**Nome canônico:** Patch Validation — incluindo verificação de hash-base  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T233  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** base hash validation; validação de patch

## T233:C01 — conceito

Validação de um patch antes e depois de aplicá-lo, incluindo a identidade da base quando necessária. O hash-base detecta que os bytes ou a revisão observados mudaram desde a leitura. Ele não comprova autoria, legitimidade do conteúdo ou correção funcional; essas propriedades exigem controles e evidências diferentes.

Como funciona:
- A aplicação compara a base atual com a identidade esperada e verifica o escopo dos caminhos.
- Uma etapa de aplicabilidade detecta conflitos de contexto e formato.
- Depois da gravação, inspeção do delta e verificações semânticas avaliam o resultado produzido.

Nota de nomenclatura: Verificação criptográfica da base é uma recomendação de protocolo; não se presume que todo editor a faça automaticamente.

## T233:C02 — aplicacao

Quando usar:
- Edições concorrentes, patches gerados por agentes e integração de alterações em arquivos compartilhados.

Quando não usar:
- Aceitar um hash calculado depois da mudança como se fosse a precondição original ou tratar dry-run como prova de comportamento.

Implementação proposta:
- Proposta: registrar revisão e hashes dos arquivos lidos, usando a mesma definição de bytes em leitura e comparação.
- Validar caminhos, operações permitidas e aplicabilidade sem ultrapassar o escopo autorizado.
- Comparar novamente a base no momento da escrita para reduzir a janela entre verificação e uso.
- Aplicar em checkout isolado; operações em vários arquivos exigem estratégia explícita de integração, pois renomeação atômica de um arquivo não torna o lote inteiro atômico.
- Recalcular hashes finais, revisar o diff e associar os resultados de testes à revisão efetivamente validada.

Aplicação LAI proposta:
Proposta LAI: exigir precondições de base e recibos de aplicação na integração de patches, preservando revisões concorrentes e identificando resultados parciais.

## T233:C03 — riscos_validacao

Armadilhas:
- Normalização silenciosa de finais de linha pode invalidar a comparação.
- A base pode mudar após um check separado.
- Reaplicar patch parcialmente aplicado pode duplicar alterações.

Métricas sugeridas:
- Conflitos de base; hunks rejeitados; mudanças fora do escopo; resultados parciais; verificações vinculadas à revisão correta.

Testes propostos:
- Modificar o arquivo após leitura e exigir conflito antes da escrita.
- Interromper um lote e reconciliar quais arquivos foram alterados antes de retomar.
- Verificar que uma aprovação sintática não é reportada como teste funcional executado.

## T233:C04 — perguntas_proveniencia

Pergunta: O comando de check substitui hash-base?
Resposta: Não necessariamente. Aplicabilidade e identidade exata da base são verificações diferentes; o protocolo deve exigir cada uma conforme o risco.

Pergunta: O que fazer depois de um conflito?
Resposta: Reler a revisão atual, preservar alterações independentes e reconstruir apenas o delta ainda necessário. Nunca forçar a base antiga por conveniência.

Pergunta: Um hash-base lido anteriormente elimina concorrência?
Resposta: Não. A comparação precisa participar da guarda da escrita ou publicação, não ser apenas uma verificação separada.

Pergunta: Por que registrar hash do resultado testado?
Resposta: Para demonstrar que o artefato entregue corresponde à versão avaliada e não a uma edição posterior sem validação.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T233:C05 — mecanismo_avancado

Verificar hash e aplicar depois deixa uma janela de corrida: outro escritor pode alterar a base entre as duas operações. Uma proposta prepara a alteração em árvore isolada, verifica o resultado e publica uma referência somente se o destino ainda apontar para a revisão esperada. git-update-ref oferece comparação com old-oid para esse tipo de atualização de ref. Isso protege publicação da revisão; não torna efeitos de scripts ou bancos parte da mesma transação.

Condição de contorno:
Um teste aprovado em árvore diferente da publicada não sustenta a conclusão sobre o artefato entregue.

Contrato proposto:
- Entradas: Patch, revisão-base, critérios de validação e referência de destino.
- Saídas: Artefato validado identificado ou conflito de base/publicação.
- Estado: Hashes de entrada e saída, evidências dos testes e referência esperada.
- Invariante: O objeto publicado é exatamente aquele ao qual se referem as evidências de validação.

Compromissos de projeto:
- Preparação isolada reduz disputas e exige integração explícita.
- Revalidar após mudanças concorrentes custa tempo e evita publicar evidência obsoleta.

## T233:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aprovar um candidato e avançar a referência de destino antes da publicação; exigir rejeição condicional e nova integração, sem sobrescrever o avanço concorrente.

Plano de avaliação proposto:
Comparar check seguido de escrita livre e publicação condicionada à base. Medir conflitos detectados, revisões erradas publicadas e custo de revalidação. Separar integridade dos bytes, aplicação do patch e correção funcional.

Comparações:
- T229 (complements): A estratégia de patch precisa dessa ligação entre base, delta e resultado.
- T236 (complements): Commits podem identificar o artefato validado e seu ponto de integração.

Afirmação rastreável:
git-update-ref permite atualizar uma ref somente quando seu valor atual corresponde ao old-oid informado.
Suporte: direct; fontes: V3C-S037
Limite: A guarda cobre a referência Git; não é uma transação global de todo o ambiente de execução.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T233:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 eliminava corrida entre hash e aplicação. A expansão organiza um pacote de evidência de validação, seleciona verificadores conforme o delta e trata publicação como operação condicional sobre o artefato realmente testado.

Identidade do candidato
Vincule base, patch e árvore resultante a uma identidade imutável. Cada teste registra qual árvore e ambiente executou. Se o agente altera código depois do teste, o resultado não acompanha automaticamente a nova versão. O pacote de validação deve permitir reproduzir a ligação entre requisito, candidato e prova sem confiar na mensagem final do executor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

Portões por propriedade
Separe estrutura, aplicabilidade, escopo e comportamento. Parser pode aprovar sintaxe e teste pode não cobrir intenção; revisão de propriedade acrescenta evidência diferente, sem se tornar prova formal. Escolha testes de impacto pelo delta e por dependências, mantendo um conjunto mínimo obrigatório quando o alcance não puder ser calculado com confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S010.

Publicação condicionada
Prepare e valide em árvore isolada, depois atualize a referência apenas se o destino ainda corresponde à base esperada. Se alguém avançou a referência, rebase ou reconcilie e invalide as provas afetadas. Essa condição protege o código publicado; scripts executados durante testes podem ter efeitos fora da transação e exigem isolamento próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S027.

USO AVANÇADO — Agente editor com integração automática
Cenário: Um trabalhador entrega patch e afirma que os testes passaram.
Estratégia: O integrador verifica identidade de base, aplica em ambiente isolado e exige evidência de execução sobre a árvore candidata. Rode verificações essenciais e publique condicionalmente. Se o trabalhador não entregou prova válida, trate a informação como relato a confirmar, não como aprovação suficiente.
Papel do modelo pequeno: 3–7B pode gerar patch; 8–14B interpreta falhas; controlador valida identidade e publicação.
Aceite proposto: Proposta: nenhum artefato entregue com testes de outra revisão ou base inesperada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S009.

USO AVANÇADO — Vários candidatos paralelos
Cenário: Múltiplos agentes propõem soluções para o mesmo defeito.
Estratégia: Valide cada candidato em isolamento e compare qualidade, escopo e custo. Depois de escolher, confirme que a base de integração permanece válida; não misture trechos de candidatos aprovados sem testar a composição. O novo conjunto é outro artefato com riscos próprios.
Papel do modelo pequeno: 15–30B avalia tradeoffs; verificadores externos decidem requisitos objetivos.
Aceite proposto: Proposta: seleção reproduzível e regressões de composição detectadas antes da publicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerar deltas pequenos que possam ser rejeitados ou aceitos por critérios externos claros.
8–14B: Diagnosticar falhas e sugerir verificações relevantes, sem emitir prova textual substituta.
15–30B: Integrar candidatos e analisar intenção, mantendo isolamento e gates determinísticos.
Requisitos de treino/runtime: Hashes, revisão base, ambientes reproduzíveis, evidência por teste e atualização condicional de referência.
Não aplicar quando: Não aceitar código apenas porque aplica, compila ou recebeu aprovação de outro modelo.

## T233:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Análises são associadas à mudança de código antes da integração.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Patches são verificados antes de serem oferecidos para integração.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Linters e testes estruturais verificam invariantes.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: Uso de testes e revisão é relatado; o artigo não demonstra o contrato completo de validação de patch com identidade de base e publicação.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Há etapas de validação, sem demonstração integral do protocolo de hash-base da ficha.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes operacionais mostram partes de validação. Testes genéricos não foram usados como prova automática do contrato completo com hash-base e publicação condicional.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q007, V4C-Q027.

## T233:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T233 → T239 [complements]
Como combinar: Usar worktrees ou isolamento equivalente para manter candidato e testes separados de outras mudanças.
Interface: Árvore candidata, ambiente e recursos externos exclusivos.
Condição: Isolamento cobre bancos, portas e outputs além dos arquivos.
Aceite proposto: Teste não depende de alteração não incluída na entrega.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V2A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T233 → T236 [complements]
Como combinar: Transformar candidato aprovado em commit identificado, mantendo a árvore testada como alvo da entrega.
Interface: Tree ID, commit e pacote de validação.
Condição: Índice corresponde aos bytes aceitos.
Aceite proposto: Commit parcial não omite dependência usada no teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S036, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Hash-base sem exclusão ou publicação condicional deixa janela de corrida.
- Uma mudança posterior em teste, configuração ou código pode invalidar a prova anterior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare patches aceitos, regressões e custo de revisão com modelo de fronteira. O pequeno modelo pode gerar candidatos competitivos sob gates fortes; a validade pertence ao artefato verificado, não ao porte.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T230, T236, T239

## Fontes primárias associadas

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T234 — Persistent Project Memory File — incluindo memória por módulo

**Nome canônico:** Persistent Project Memory File — incluindo memória por módulo  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T234  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** project memory file; memória persistente por módulo

## T234:C01 — conceito

Arquivo persistente que fornece contexto reutilizável sobre um projeto e, quando necessário, seus módulos. As documentações de Claude Code e Codex descrevem arquivos de instruções e mecanismos próprios de carregamento. Um arquivo de memória pode reunir decisões e referências; seu conteúdo não é, por si só, um banco transacional ou controle de acesso.

Como funciona:
- O contexto é recuperado entre sessões por regras explícitas do produto ou do controlador.
- Uma camada geral descreve o projeto; arquivos locais acrescentam informação relevante ao módulo.
- Referências a documentos e decisões permitem expandir detalhes sem carregar todo o histórico.

## T234:C02 — aplicacao

Quando usar:
- Convenções estáveis, comandos verificados de desenvolvimento, decisões arquiteturais e orientação para novos agentes.

Quando não usar:
- Armazenar grandes logs, credenciais ou estados de operações externas que exigem atualização transacional.

Implementação proposta:
- Proposta: separar instruções vigentes, fatos verificados, decisões e pendências, com origem e data quando relevantes.
- Usar nomes e hierarquia realmente documentados pelo executor escolhido, como AGENTS.md ou CLAUDE.md, sem presumir regras idênticas.
- Manter o arquivo principal curto e distribuir detalhes por módulo com referências explícitas.
- Revisar entradas quando mudarem ferramentas, contratos ou estrutura do repositório.
- Confrontar memória antiga com a revisão atual antes de executar comandos ou modificar código.

Aplicação LAI proposta:
Proposta LAI: manter memória curta por projeto e módulo, vinculada a fontes e revisões, deixando estado operacional e histórico detalhado em registros próprios.

## T234:C03 — riscos_validacao

Armadilhas:
- Anotações antigas podem parecer instruções vigentes.
- Arquivos volumosos consomem contexto em toda sessão.
- Uma instrução escrita não garante que o runtime a carregou ou aplicou.

Métricas sugeridas:
- Entradas com proveniência; referências quebradas; conteúdo desatualizado; tokens carregados; erros causados por instruções antigas.

Testes propostos:
- Iniciar uma sessão no módulo e verificar quais instruções o executor realmente carregou.
- Alterar um comando do projeto e conferir revisão da memória associada.
- Inserir uma pendência como hipótese e verificar que ela não é apresentada como fato confirmado.

## T234:C04 — perguntas_proveniencia

Pergunta: AGENTS.md e CLAUDE.md funcionam da mesma forma?
Resposta: Não se deve presumir isso. Nomes, descoberta, escopo e precedência dependem da documentação e versão de cada executor.

Pergunta: O arquivo pode afirmar que uma tarefa terminou?
Resposta: Pode referenciar a evidência de conclusão, mas uma anotação isolada não substitui o estado confirmado, os artefatos e os resultados de verificação.

Pergunta: Colocar AGENTS.md em qualquer pasta garante leitura?
Resposta: Não. É necessário conhecer o caminho de descoberta, o diretório de execução e os limites do produto.

Pergunta: Memória de módulo deve copiar todas as regras globais?
Resposta: Não por padrão. Referências e responsabilidades claras reduzem divergência entre cópias que envelhecem separadamente.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T234:C05 — mecanismo_avancado

Memória por módulo depende de descoberta e escopo, não apenas de existir um arquivo no disco. No Codex documentado, arquivos de instrução são coletados ao longo do caminho até o diretório corrente, com precedência entre nomes e um limite de tamanho. Assim, um guia de módulo pode não ser carregado em uma execução iniciada noutro local. Uma proposta mantém decisões e fatos separados de instruções operacionais, incluindo revisão e referência à evidência.

Condição de contorno:
Um arquivo antigo pode continuar sendo carregado corretamente e ainda transmitir informação obsoleta sobre o projeto.

Contrato proposto:
- Entradas: Diretório de execução, política de descoberta, arquivos do projeto e revisão vigente.
- Saídas: Conjunto efetivamente carregado e referências de memória aplicáveis ao módulo.
- Estado: Versões, precedência e responsáveis por atualização das decisões.
- Invariante: Existência de um arquivo não é registrada como prova de que o agente o recebeu ou aplicou.

Compromissos de projeto:
- Arquivos locais ao módulo reduzem contexto irrelevante e podem fragmentar regras compartilhadas.
- Um arquivo central facilita governança e cresce até perder densidade ou ultrapassar limites de carregamento.

## T234:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar execuções em diretórios diferentes com instruções locais divergentes; conferir o conjunto carregado e a versão utilizada antes de avaliar comportamento.

Plano de avaliação proposto:
Comparar memória central e por módulo em tarefas que atravessam fronteiras do projeto. Medir contexto carregado, decisões obsoletas e contradições. Definir fonte canônica para regras compartilhadas e referências explícitas entre módulos.

Comparações:
- T211 (distinct_from): Handoff descreve uma transferência de trabalho; memória de projeto conserva conhecimento reutilizável.
- T155 (complements): Instruções enxutas podem apontar para detalhes de módulo carregados quando necessários.

Afirmação rastreável:
A documentação Codex descreve descoberta de AGENTS.md por caminho, arquivos de override e limite de tamanho combinado.
Suporte: direct; fontes: V2A-S017
Limite: Essas regras são do produto documentado; outros agentes podem carregar arquivos de modo diferente.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T234:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava descoberta e escopo de arquivos por módulo. A expansão organiza memória como conhecimento versionado com dono, separa instruções de fatos e cria uma rotina de manutenção vinculada a mudanças reais.

Mapa e conhecimento local
Mantenha entrada curta com estrutura do projeto e caminhos para detalhes. Regras específicas vivem perto do módulo correspondente, enquanto decisões transversais ficam numa fonte comum. A descoberta precisa ser testada no diretório e runtime usados; colocar um arquivo no repositório não garante que todos os agentes o lerão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S039.

Fatos, instruções e decisões
Identifique natureza e validade de cada registro. Comando de teste é instrução operacional; resultado de teste é evidência de uma revisão; escolha arquitetural é decisão com contexto. Misturá-los faz uma evidência antiga parecer autorização atual ou um plano parecer execução. Referencie artefatos para evitar duplicar detalhes que envelhecem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V4C-S026.

Manutenção por mudança
Quando código ou contrato muda, atualize a memória afetada ou marque-a para revisão. Um agente pode propor correções, mas o critério é aderência ao estado real do projeto. Checagens de links e estrutura ajudam, enquanto a validade semântica pode exigir testes ou revisão. Não acumule toda sessão como instrução permanente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

USO AVANÇADO — Projeto operado por modelos locais
Cenário: Agentes retomam trabalho em módulos sem carregar conversas anteriores.
Estratégia: Forneça mapa geral curto, contrato do módulo, comandos válidos e decisões que limitam a alteração. Na retomada, confirme revisão e leia arquivos atuais. Ao concluir, proponha só fatos estáveis ou lições verificadas para memória, deixando logs transitórios em artefatos próprios.
Papel do modelo pequeno: 3–7B executa unidade; 8–14B atualiza registros locais; 15–30B revisa decisões transversais.
Aceite proposto: Proposta: menor custo de orientação e ausência de instruções incompatíveis com o código atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

USO AVANÇADO — Onboarding técnico
Cenário: Uma pessoa ou agente precisa entender a origem de um comportamento.
Estratégia: Recupere decisão relevante e caminho de código, distinguindo justificativa histórica de implementação vigente. Se houver conflito, registre a divergência e investigue; não escolher o arquivo de memória apenas porque foi escrito com linguagem confiante.
Papel do modelo pequeno: 8–14B localiza documentação; 15–30B integra contexto e código.
Aceite proposto: Proposta: respostas com referências válidas e identificação de memória obsoleta em casos inseridos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V4C-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Instruções curtas por módulo e exemplos de comandos reduzem carga de descoberta.
8–14B: Atualizações localizadas e checagem de referências, com validação contra o repositório.
15–30B: Síntese de decisões entre módulos, sem transformar toda reflexão em regra global.
Requisitos de treino/runtime: Versionamento, escopo, dono da informação e testes de descoberta no runtime escolhido.
Não aplicar quando: Não armazenar segredos em arquivo de instrução nem considerar presença no disco como prova de carregamento.

## T234:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: CLAUDE.md fornece instruções e contexto de navegação.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: AGENTS.md curto e documentação versionada no repositório oferecem memória persistente do projeto; não é mera configuração CI.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Instruções do repositório são usadas como contexto.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Anthropic e OpenAI relatam uso interno de arquivos e conhecimento no repositório. O desenho por módulo e critérios de manutenção precisam ser validados no projeto do usuário.
Consultas registradas: V4C-Q024, V4C-Q027.

## T234:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T234 → T155 [complements]
Como combinar: Harness Codex substitui instrução monolítica por mapa curto com referências para conhecimento do projeto.
Interface: Entrada de instruções, índice e documentos versionados.
Condição: Fontes detalhadas estão acessíveis quando necessárias.
Aceite proposto: Agente recupera regra relevante sem receber todo o manual.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

2. T234 → T213 [complements]
Como combinar: Planos versionados e conhecimento do repositório acompanham decomposição em blocos verificáveis no harness.
Interface: Plano, decisão e contrato de módulo.
Condição: Mudanças de requisito atualizam tarefas afetadas.
Aceite proposto: Micro-missão não executa orientação antiga sem revalidar.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

CONTROLES DE FALHA
- Memória corretamente carregada pode continuar semanticamente errada.
- Não converter sucesso alegado em fato persistente sem evidência de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare continuidade e orientação por arquivo com histórico bruto sob o mesmo conjunto de tarefas. Memória externa pode aumentar utilidade de 3–30B sem alterar pesos ou garantir retenção factual interna.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T064, T238

## Fontes primárias associadas

### V2A-S016 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções persistentes em arquivos e memória automática; escopo e carregamento dependem da configuração.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S017 — Custom instructions with AGENTS.md

[https://developers.openai.com/codex/guides/agents-md/](https://developers.openai.com/codex/guides/agents-md/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta hierárquica de instruções de projeto pelo Codex e limites de carregamento.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T235 — Headless Mode em loop / Headless Controller

**Nome canônico:** Headless Mode em loop / Headless Controller  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T235  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** headless controller; execução programática de agente

## T235:C01 — conceito

Execução de um agente por interface programática, sem depender de uma conversa interativa visível, sob coordenação de um controlador externo. Codex e Claude Code documentam interfaces dessa natureza. Um controlador em loop acrescenta política de agendamento, orçamento, avaliação de resultado e recuperação; isso não é garantido apenas pelo modo headless.

Como funciona:
- O controlador fornece tarefa e contexto delimitados ao executor.
- O executor retorna eventos, saída e estado de processo conforme a interface documentada.
- O controlador interpreta o resultado, verifica critérios e decide encerrar, continuar ou registrar um bloqueio.

## T235:C02 — aplicacao

Quando usar:
- Jobs de automação, análise de código, tarefas em fila e missões repetíveis com entradas e resultados verificáveis.

Quando não usar:
- Um laço infinito que reinicia o agente sem verificar progresso, autorização, custo ou efeitos da tentativa anterior.

Implementação proposta:
- Proposta: escolher a interface oficial disponível e registrar a versão utilizada, sem inventar opções de linha de comando.
- Definir contrato de entrada, formato de resultado, prazo, limite de tentativas e orçamento total.
- Executar em diretório e ambiente apropriados, com permissões necessárias ao escopo já autorizado.
- Capturar saída e diagnóstico como artefatos, evitando depender de texto livre para todos os estados.
- Verificar evidências antes de declarar sucesso e reconciliar operações incertas antes de continuar após falha.

Aplicação LAI proposta:
Proposta LAI: orquestrar execuções programáticas por missão, preservando resultado verificável, orçamento e identidade da operação entre tentativas.

## T235:C03 — riscos_validacao

Armadilhas:
- Exit code zero pode representar execução normal do processo sem cumprimento do objetivo.
- Saída estruturada pode continuar semanticamente errada.
- Duas instâncias do controlador podem atribuir a mesma tarefa.

Métricas sugeridas:
- Tarefas concluídas com evidência; tentativas; duração; custo agregado; saídas inválidas; concorrência duplicada.

Testes propostos:
- Retornar processo bem-sucedido com critério de aceitação não atendido e impedir conclusão falsa.
- Interromper durante uma mutação e exigir reconciliação na retomada.
- Injetar resultado incompatível com o contrato e verificar encerramento controlado ou reparo limitado.

## T235:C04 — perguntas_proveniencia

Pergunta: Headless significa que o agente possui mais permissões?
Resposta: Não. A ausência de interface interativa não amplia autorização. O controlador deve respeitar as capacidades e controles configurados.

Pergunta: Quais flags devo usar?
Resposta: Consulte a documentação oficial da versão instalada de Codex ou Claude Code. Esta entrada descreve o padrão operacional e não prescreve flags não verificadas.

Pergunta: Uma resposta final válida em JSON confirma os testes?
Resposta: Não. Ela é uma declaração estruturada; testes e artefatos exigem recibos ou resultados verificáveis.

Pergunta: O que impede um loop headless infinito?
Resposta: Critérios de término, orçamento global e análise de progresso implementados no controlador, não a ausência de interface gráfica.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T235:C05 — mecanismo_avancado

Um controlador headless precisa distinguir eventos intermediários e resultado final. Em Codex, JSONL fornece eventos da execução, enquanto output-schema restringe a resposta final; são contratos diferentes. Um processo que termina tecnicamente pode ainda entregar tarefa inconclusiva. A retomada deve usar identidade da sessão e do objetivo, evitando iniciar nova missão somente porque um processo anterior caiu. O controlador também precisa de regra explícita para parar de agendar novas iterações.

Condição de contorno:
Modo não interativo não define por si critérios de sucesso, limite de custo ou repetição segura de efeitos.

Contrato proposto:
- Entradas: Objetivo identificado, sessão, eventos estruturados e orçamento de execução.
- Saídas: Estado final da missão, artefatos e decisão de retomar ou encerrar.
- Estado: Cursor do stream, sessão corrente, tentativas e evidências de conclusão.
- Invariante: Fim do processo não é convertido automaticamente em aceitação do objetivo.

Compromissos de projeto:
- Eventos detalhados permitem diagnóstico e exigem parser versionado e armazenamento.
- Resposta final estruturada simplifica integração e não contém necessariamente todo o histórico de ações.

## T235:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o processo após uma edição e antes da mensagem final; exigir recuperação dos artefatos e estado, sem assumir fracasso total ou repetir a missão do início.

Plano de avaliação proposto:
Comparar execução única e controlador com retomada em interrupções controladas. Medir duplicação, tempo de reorientação, custo e conclusão verificada. Testar ausência de evento final, evento de falha e final estruturalmente válido, mas inconclusivo.

Comparações:
- T210 (complements): Rotação e retomada precisam preservar o estado da missão entre processos.
- T225 (distinct_from): Watchdog restaura capacidade; controlador headless interpreta eventos e decide o próximo trabalho.

Afirmação rastreável:
Codex documenta JSONL para eventos e JSON Schema para a resposta final em execução não interativa.
Suporte: direct; fontes: V3C-S039
Limite: As opções foram verificadas na documentação; a CLI não foi executada nem encontrada no PATH local.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T235:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava eventos, resposta final e estado de processo. A expansão define controlador não interativo por contrato de missão, gestão de recursos e parada explícita, evitando confundir autonomia de processo com conclusão correta.

Controlador é autoridade de ciclo
O processo do agente executa uma unidade; o controlador decide agendar, continuar, interromper ou finalizar. Use estados como em execução, aguardando dependência, candidato pronto e aceito. Exit code e texto final são sinais, não critérios únicos. Um processo que termina sem artefato pode estar inconclusivo; um que permanece vivo pode estar sem progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, V4C-S016.

Eventos e artefatos
Consuma eventos com parser tolerante a versões conhecidas e preserve tipos desconhecidos para diagnóstico. O artefato final passa por contrato próprio e deve apontar à revisão de trabalho. Não transforme evento de ferramenta concluída em missão concluída: a ferramenta pode ter retornado erro ou apenas preparado um candidato ainda sem validação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, V4C-S030.

Recursos e encerramento
O controlador gerencia timeout, orçamento, logs, subprocessos e cancelamento cooperativo. Ao parar, classifica efeitos pendentes e preserva estado retomável. Agendar outro processo com o mesmo prompt não é retomada equivalente se a identidade da missão, diretório e revisão não forem conservados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S039, C-S026.

USO AVANÇADO — Pipeline de alterações em lote
Cenário: Um job dispara agentes para tarefas de programação repetitivas.
Estratégia: Crie entrada estruturada por tarefa e workspace isolado. Execute agente, valide artefato e testes, e publique candidato para integração. Rejeição retorna diagnóstico limitado; após teto, encerre com pendências. Não manter loop infinito até o modelo declarar sucesso.
Papel do modelo pequeno: 3–7B cobre tarefas mecânicas; 8–14B repara falhas; 15–30B analisa exceções.
Aceite proposto: Proposta: cada job termina em resultado classificado, com custo e evidência completos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S016, V3C-S039.

USO AVANÇADO — Pesquisa assíncrona
Cenário: Coleta e síntese precisam continuar sem interação contínua.
Estratégia: Defina perguntas, limites de pesquisa e artefatos esperados antes de iniciar. O controlador acompanha fontes recuperadas e cobertura, acionando nova etapa somente quando pré-condições forem satisfeitas. Na falta de evidência, o resultado é lacuna explícita, não consulta infinita por obrigação de preencher quota.
Papel do modelo pequeno: 8–14B extrai; 15–30B integra dentro de critério de suficiência.
Aceite proposto: Proposta: cobertura rastreável e término previsível mesmo quando uma fonte fica indisponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S039.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Jobs curtos, schema fixo e poucos estados facilitam execução não interativa confiável.
8–14B: Tratamento de erros locais e geração de candidatos com evidência recuperável.
15–30B: Coordenação de etapas amplas, com controlador determinístico mantendo limites e publicação.
Requisitos de treino/runtime: API ou CLI com eventos documentados, diretório e revisão fixados, captura de logs e política de parada.
Não aplicar quando: Não habilitar autoridade ilimitada só porque o modo não oferece prompts interativos.

## T235:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: O recurso executa trabalho em background com logs.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: GitHub e OpenAI documentam agentes e interfaces operacionais; recursos disponíveis não provam implantação deste controlador específico nem justificam loops ilimitados.
Consultas registradas: V4C-Q011, V4C-Q027.

## T235:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T235 → T225 [complements]
Como combinar: Watchdog recupera processo quando necessário, sem reiniciar automaticamente a missão lógica.
Interface: Estado do job, última evidência e geração.
Condição: Recuperação preserva identidade e orçamento acumulado.
Aceite proposto: Queda do processo não causa duplicação de efeitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T235 → T233 [feeds]
Como combinar: Resultado headless é candidato para validação, e só o gate decide aceite da alteração.
Interface: Artefato, base e registros de execução.
Condição: Contrato final foi satisfeito e os testes correspondem à revisão.
Aceite proposto: Texto de sucesso sem evidência é rejeitado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S039, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar JSONL de eventos como se todos os itens obedecessem ao schema da resposta final.
- Subprocessos e efeitos externos podem sobreviver ao encerramento do cliente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo por job aceito e taxa de intervenção com o mesmo controlador. Rodar um modelo pequeno sem UI não demonstra autonomia cognitiva equivalente à de um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T225, T228, T218, T243

## Fontes primárias associadas

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S006 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Claude Code programático pelo CLI ou SDK; controle explícito de entrada, saída e ciclo de execução.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T236 — Git Commit por etapa

**Nome canônico:** Git Commit por etapa  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T236  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** incremental commits; checkpoint de código em Git

## T236:C01 — conceito

Registro de alterações coerentes em commits Git associados a etapas de trabalho. Cada commit preserva uma árvore versionada e sua relação com o histórico, facilitando revisão e recuperação de código. Ele não captura automaticamente arquivos não versionados, processos, banco de dados ou efeitos enviados a serviços externos.

Como funciona:
- O conjunto escolhido de alterações é registrado em um commit com mensagem e identidade verificáveis.
- Uma etapa pode apontar para esse commit e para evidências de validação.
- Sessões posteriores consultam o histórico para localizar a última mudança relevante e compreender sua intenção.

## T236:C02 — aplicacao

Quando usar:
- Desenvolvimento em etapas, handoffs, revisão de alterações e recuperação de versões de código conhecidas.

Quando não usar:
- Criar um commit por cada pequena digitação ou considerar que um commit equivale a publicação, implantação ou checkpoint completo da aplicação.

Implementação proposta:
- Proposta: escolher uma unidade lógica revisável e inspecionar o diff antes de selecionar os arquivos.
- Incluir somente alterações pertencentes à etapa, preservando trabalho independente de outros colaboradores.
- Registrar na mensagem o problema e o comportamento resultante, com referência à missão quando útil.
- Associar testes à revisão efetivamente testada; declarar explicitamente verificações não executadas.
- Usar o commit local como ponto de referência; push, merge e implantação dependem do fluxo e da autorização correspondentes.

Aplicação LAI proposta:
Proposta LAI: vincular cada marco de código a um commit revisável e a seus resultados de verificação, usando o histórico para continuidade entre sessões.

## T236:C03 — riscos_validacao

Armadilhas:
- Um commit pode conter código defeituoso.
- Misturar mudanças sem relação dificulta revisão e reversão.
- Credenciais ou artefatos grandes podem entrar no histórico se a seleção não for inspecionada.

Métricas sugeridas:
- Escopo de cada commit; alterações sem relação; revisões com evidência; facilidade de localizar a mudança causadora de regressão.

Testes propostos:
- Conferir se a árvore do commit contém exatamente os arquivos da etapa.
- Retomar uma sessão a partir do histórico e verificar identificação do próximo trabalho pendente.
- Comparar a revisão testada com o commit entregue para detectar alterações posteriores sem validação.

## T236:C04 — perguntas_proveniencia

Pergunta: Commit por etapa garante que cada commit passa todos os testes?
Resposta: Não. Essa é uma política adicional. Se um commit representar trabalho intermediário, seu estado e as limitações precisam estar claros.

Pergunta: Reverter o commit desfaz uma chamada de API?
Resposta: Não. Git registra código versionado; efeitos externos exigem reconciliação ou compensação específica quando disponível e autorizada.

Pergunta: Testar antes de git commit basta?
Resposta: Somente se o estado testado corresponder ao índice/árvore que será registrado; staging parcial pode quebrar essa equivalência.

Pergunta: Um commit de checkpoint deve ser apresentado como pronto?
Resposta: Não. Pode preservar progresso incompleto, desde que esse estado e as pendências sejam explícitos.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T236:C05 — mecanismo_avancado

O commit usual registra o índice, que pode diferir da árvore de trabalho onde os testes foram executados. Com staging parcial, um teste verde pode depender de alteração não incluída no commit. A proposta verifica o delta preparado e identifica a árvore efetivamente aceita. Uma etapa incompleta ainda pode ser salva como checkpoint, mas seu status deve permanecer distinto de entrega aprovada; mensagens de commit não substituem evidência de execução.

Condição de contorno:
Um commit coerente de código não captura automaticamente migração aplicada, dados externos ou configuração não versionada.

Contrato proposto:
- Entradas: Alterações da etapa, índice preparado, objetivo e evidências de verificação.
- Saídas: Commit identificado, descrição do comportamento e status de aceitação.
- Estado: Revisão-base, árvore do commit e arquivos fora do escopo.
- Invariante: A evidência de teste corresponde à árvore que o commit efetivamente registra.

Compromissos de projeto:
- Commits pequenos facilitam revisão e podem dividir uma mudança que só funciona integrada.
- Commits amplos preservam uma entrega conjunta e dificultam localizar causa de regressão.

## T236:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deixar no working tree uma correção necessária, mas fora do índice; exigir detecção de que o commit preparado não corresponde ao estado testado.

Plano de avaliação proposto:
Comparar etapas por arquivo e por mudança funcional em revisões independentes. Medir capacidade de reverter, reproduzir testes e localizar regressões. Definir tamanho pela coerência do comportamento, sem impor um número universal de linhas ou arquivos.

Comparações:
- T233 (complements): Validação deve ligar resultado testado à revisão publicada.
- T240 (distinct_from): Commit captura uma árvore Git e metadados; snapshot operacional pode precisar de outros estados.

Afirmação rastreável:
A documentação Git informa que o commit padrão contém o estado atual do índice.
Suporte: direct; fontes: V3C-S036
Limite: Outras opções alteram seleção de conteúdo; o contrato precisa registrar o modo efetivamente utilizado.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T236:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrava diferença entre índice e árvore testada. A expansão define commits como fronteiras de aceitação e recuperação, organiza histórico de etapas e explicita o que continua fora do versionamento do código.

Checkpoint e entrega distintos
Uma etapa pode salvar trabalho incompleto para recuperação, mas seu status deve declarar que falta validação. Um commit aprovado precisa apontar ao artefato testado e ao requisito atendido. Mensagem descritiva não substitui esses vínculos; use metadados ou manifesto associado quando o histórico de validação não cabe no próprio commit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S036, V4C-S030.

Unidade revisável
Escolha commits por mudança coerente, evitando misturar reparo funcional, reformatação e atualização de documentação sem relação. Etapas pequenas ajudam bisect e revisão, mas uma sequência de commits quebrados pode dificultar recuperação. Defina se a campanha exige cada commit válido ou apenas pontos de integração explicitamente marcados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S021, V3C-S036.

Publicação e efeitos externos
Criar commit local não significa que foi integrado ou implantado. Registre branch, referência esperada e resultado da publicação; se a conexão cai, consulte a referência antes de repetir ações associadas. Migrações de banco, recursos criados e segredos fora do repositório precisam de ledger próprio, não de confiança na existência do commit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, C-S026.

USO AVANÇADO — Campanha longa por módulos
Cenário: Um agente precisa preservar progresso sem entregar tudo de uma vez.
Estratégia: Depois de cada unidade coerente, valide o conteúdo preparado e salve commit com vínculo ao requisito. Integre apenas etapas aceitas; checkpoints incompletos ficam separados do fluxo de entrega. Na retomada, leia árvore e estado de validação, não apenas a última mensagem de commit.
Papel do modelo pequeno: 3–7B edita módulo; 8–14B prepara resumo factual; 15–30B coordena integração.
Aceite proposto: Proposta: recuperação por etapa sem perder trabalho e sem promover checkpoint incompleto por engano.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S036.

USO AVANÇADO — Revisão de alternativas
Cenário: Vários candidatos resolvem o mesmo requisito em branches distintas.
Estratégia: Identifique a árvore de cada candidato, execute testes e registre decisão de seleção. Se combinar commits, valide a composição resultante; dois commits aprovados isoladamente podem conflitar semanticamente. Preserve candidatos descartados pelo prazo necessário à auditoria e limpe recursos associados depois.
Papel do modelo pequeno: 15–30B compara tradeoffs; modelos menores geram alternativas delimitadas.
Aceite proposto: Proposta: rastrear a solução escolhida e reproduzir a árvore realmente validada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Commits por alteração local coerente, com revisão determinística do índice.
8–14B: Agrupar mudanças relacionadas e redigir mensagens ancoradas no diff real.
15–30B: Planejar sequência de integração e recuperar regressões sem depender de narrativa do histórico.
Requisitos de treino/runtime: Git configurado, índice inspecionado, testes sobre árvore preparada e identidade de referência publicada.
Não aplicar quando: Não usar git commit como snapshot completo do ambiente nem assumir que staging parcial preserva todas as dependências testadas.

## T236:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Changesets versionam alterações mas não são git commit.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: A prática de etapas pequenas e revisadas é explícita, porém usa Sapling e não o comando Git commit.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Há commits e validação, mas não uma política de commit por etapa de agente.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: O sistema acompanha commits, mas não demonstra um agente criando commit por micro-missão.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: O agente publica mudanças como commits em draft PR.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Git documenta semântica; Windows Git, Sapling e Codex fornecem contextos operacionais distintos. Não foram contados como prova universal de commits validados a cada etapa.
Consultas registradas: V4C-Q015, V4C-Q016, V4C-Q027.

## T236:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T236 → T233 [complements]
Como combinar: Gate valida a árvore preparada antes de marcar o commit como aceito.
Interface: Tree ID, testes e requisito.
Condição: Conteúdo testado coincide com o commit.
Aceite proposto: Mudança fora do índice não sustenta teste aprovado do commit parcial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S036, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T236 → R027 [complements]
Como combinar: Usar objetos e referências Git para identificar etapas e publicar condicionalmente.
Interface: Commit, pais e valor anterior esperado da ref.
Condição: Operação escolhida respeita semântica documentada.
Aceite proposto: Conflito de avanço da ref provoca reconciliação, não sobrescrita silenciosa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Commit criado não significa push, merge ou deploy concluído.
- Sapling e Scion são sistemas distintos; seus changesets não provam comportamento específico do índice Git.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare produtividade por etapa aceita e custo de integração com modelos diferentes. Histórico bem formado favorece recuperação de qualquer porte, mas não valida automaticamente a qualidade do código.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T233, T239, T240

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T237 — Subagent Offloading

**Nome canônico:** Subagent Offloading  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T237  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** subagent delegation; delegação de contexto

## T237:C01 — conceito

Delegação de uma parte delimitada do trabalho a outro agente, que produz resultado aproveitável pelo agente principal. A documentação de Claude Code descreve subagentes e seus contextos próprios. A forma de inicialização pode variar: não se deve assumir que toda delegação começa vazia nem que todo o histórico é sempre compartilhado.

Como funciona:
- O coordenador define objetivo, entradas, restrições e saída esperada da subtarefa.
- O subagente trabalha com seu contexto e ferramentas disponíveis.
- O resultado retorna em forma compacta, acompanhado de evidências e referências para verificação e integração.

## T237:C02 — aplicacao

Quando usar:
- Investigações independentes, leitura de módulos distintos, revisão paralela e tarefas cujo resultado possa ser integrado com clareza.

Quando não usar:
- Delegar atividades fortemente dependentes sem coordenação ou permitir que vários agentes editem os mesmos arquivos sem estratégia de integração.

Implementação proposta:
- Proposta: estabelecer um contrato por subtarefa com escopo de arquivos, critérios de conclusão e formato de retorno.
- Enviar contexto suficiente para evitar suposições e limitar material irrelevante.
- Atribuir responsabilidade de escrita ou usar checkouts separados quando houver alterações concorrentes.
- Exigir referência à revisão, fontes e testes efetivamente executados no retorno.
- O coordenador revisa evidências, resolve inconsistências e realiza a integração final dentro do orçamento global.

Aplicação LAI proposta:
Proposta LAI: distribuir missões independentes entre especialistas, mantendo integração, orçamento e responsabilidade final no coordenador.

## T237:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir condições e ressalvas importantes.
- Contextos separados não isolam automaticamente filesystem, rede ou credenciais.
- Delegação pode aumentar tokens e trabalho duplicado.

Métricas sugeridas:
- Tempo total até integração; custo agregado; retrabalho por contrato incompleto; conflitos; qualidade das evidências retornadas.

Testes propostos:
- Delegar a mesma investigação com contratos claros e medir redundância desnecessária.
- Introduzir conflito entre resultados e verificar resolução por evidência, não por maioria.
- Confirmar que um subagente não altera arquivos pertencentes a outro escopo de escrita.

## T237:C04 — perguntas_proveniencia

Pergunta: Subagentes economizam tokens automaticamente?
Resposta: Não. Eles podem reduzir o contexto do coordenador, mas suas próprias chamadas também consomem recursos. O ganho depende da divisão e da quantidade de trabalho repetido.

Pergunta: O coordenador pode aceitar qualquer resumo como conclusão?
Resposta: Não. Deve verificar a evidência necessária ao risco e aos critérios da tarefa, especialmente quando o resultado implica mudança de código ou estado externo.

Pergunta: Qual resultado de pesquisa é melhor que um resumo solto?
Resposta: Uma síntese com fontes, alegações específicas, limitações e referências que o coordenador consiga conferir.

Pergunta: Quem responde pela qualidade após o merge?
Resposta: O coordenador ou integrador definido pelo contrato; sucesso de cada tarefa isolada não prova compatibilidade do conjunto.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T237:C05 — mecanismo_avancado

A delegação precisa transferir uma unidade de decisão suficiente, sem depender de contexto que só o coordenador conhece. O retorno também deve separar resultado, evidência e limitações. Um subagente que afirma ter testado algo precisa devolver o alvo, revisão e resultado correspondente. Delegar pesquisa pode reduzir contexto do coordenador; delegar uma edição exige ainda um contrato de integração e propriedade sobre arquivos ou revisões.

Condição de contorno:
Um subagente não consegue resolver uma dependência omitida apenas por possuir outro contexto ou mais chamadas de modelo.

Contrato proposto:
- Entradas: Objetivo delimitado, entradas versionadas, ferramentas necessárias e critério de entrega.
- Saídas: Artefatos, fontes, decisões tomadas e questões não resolvidas.
- Estado: Responsável, orçamento delegado, revisão-base e estado da entrega.
- Invariante: O coordenador valida o resultado integrado e não trata o resumo como prova automática de execução.

Compromissos de projeto:
- Delegação reduz carga de contexto local e acrescenta custo de inicialização e comunicação.
- Workers autônomos resolvem detalhes e podem divergir de premissas não explicitadas no contrato.

## T237:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: omitir uma dependência crítica e fornecer duas tarefas que editam a mesma interface; exigir lacuna explícita e conflito identificado antes de integrar.

Plano de avaliação proposto:
Comparar execução central e offloading em subtarefas independentes e acopladas. Medir economia de contexto, retrabalho, tempo final e qualidade das evidências. Contabilizar chamadas de todos os agentes e trabalho do coordenador.

Comparações:
- T169 (complements): Contextos isolados são uma forma de executar a delegação, mas não seu critério de sucesso.
- T211 (complements): O formato de handoff pode organizar entradas e devolução do subagente.

Afirmação rastreável:
Claude Code descreve subagentes que trabalham em contexto próprio e devolvem resultados ao agente principal.
Suporte: direct; fontes: V2A-S018
Limite: Ferramentas, contexto inicial e persistência dependem do tipo e configuração; não se presume um padrão universal de fork.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T237:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigia contexto suficiente e evidência no retorno. A expansão escolhe o que terceirizar, limita integração e acompanha trabalhadores para que redução de contexto do supervisor não vire perda de controle sobre a missão.

Delegar por valor líquido
Compare trabalho local com custo de preparar, executar e integrar a delegação. Busca independente e revisão por propriedade costumam ter fronteiras claras; decisões fortemente acopladas podem gerar mais coordenação que ganho. Escolha unidades cuja resposta altere uma decisão do supervisor e que possam terminar sem depender de conversa não fornecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Retorno escalonado
Peça resultado curto com artefatos, evidências e limitações, mantendo detalhes disponíveis sob demanda. O supervisor verifica suficiência antes de integrar e pode solicitar esclarecimento específico. Não retransmita toda a trajetória de cada trabalhador; isso elimina boa parte do benefício de contexto e multiplica ruído de hipóteses já descartadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Responsabilidade de integração
O supervisor continua responsável por conflitos de versão, duplicação de fontes e critérios globais. Um trabalhador não pode declarar missão inteira concluída porque sua parte terminou. Atribua dono de escrita, revisão e critério de aceite, e espere sinal de prontidão antes de consumir arquivos que ainda podem estar mudando.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, C-S030.

USO AVANÇADO — Pesquisa paralela verificável
Cenário: Vários tópicos precisam de fontes e comparação posterior.
Estratégia: Distribua perguntas independentes e IDs exclusivos. Cada trabalhador retorna evidência e limite, com casos identificados para deduplicação. O supervisor revisa alegações que atravessam tópicos e não soma relatos do mesmo deployment como confirmações independentes. Reabra apenas lacunas específicas.
Papel do modelo pequeno: 8–14B coleta e extrai; 15–30B integra e audita relações.
Aceite proposto: Proposta: cobertura integral com menos contexto no supervisor e custo de integração registrado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

USO AVANÇADO — Revisores especializados de patch
Cenário: O candidato precisa respeitar propriedades distintas.
Estratégia: Delegue uma propriedade por revisor e forneça o mesmo artefato imutável. Um revisor devolve evidência de violação ou limite de avaliação. Agregue por requisito obrigatório, sem votação que esconda falha crítica, e rode verificações executáveis em paralelo quando forem independentes.
Papel do modelo pequeno: 3–7B cobre regras estreitas; 8–14B analisa trechos; 15–30B resolve conflitos de intenção.
Aceite proposto: Proposta: detectar violações inseridas sem excesso de falsos bloqueios ou revisões redundantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefas pequenas com contrato explícito e poucas dependências ocultas.
8–14B: Especialistas por documento, módulo ou propriedade, com evidência recuperável.
15–30B: Supervisão e síntese entre trabalhadores; manter o número de agentes compatível com orçamento e integração.
Requisitos de treino/runtime: Fila de tarefas, IDs, versões, donos de escrita e retorno final validado antes de consolidação.
Não aplicar quando: Não delegar apenas para aumentar paralelismo quando o resultado precisa de contexto compartilhado indivisível.

## T237:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O líder delega pesquisa e recebe resultados condensados.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Subagentes são modelados como ferramentas especializadas.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Agentes revisam outros agentes no processo descrito.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Fixers e verificadores recebem papéis e escopos específicos.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e AutoClean demonstram delegação operacional. Não foi presumido que seus trabalhadores sejam modelos de 3–30B.
Consultas registradas: V4C-Q006, V4C-Q010.

## T237:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T237 → T147 [complements]
Como combinar: Claude Research usa subagentes paralelos e reúne resultados para a resposta do líder.
Interface: Perguntas, orçamento e artefatos retornados.
Condição: Trabalhos independentes com junção definida.
Aceite proposto: O líder integra resultados aceitos e identifica lacunas.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T237 → T200 [complements]
Como combinar: CodeCourt no AutoClean distribui avaliação por propriedades e usa os vereditos como gate do candidato.
Interface: Patch imutável, propriedade e parecer.
Condição: Critérios obrigatórios têm tratamento explícito de falha.
Aceite proposto: Um veredito negativo não desaparece na média dos demais.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Contexto isolado não garante arquivos ou efeitos isolados.
- Relato de teste de subagente precisa identificar alvo e revisão para ser aceito como evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare equipe pequena e agente de fronteira pelo orçamento total, incluindo supervisor e revisores. A especialização ajuda em tarefas verificáveis, mas integrações difíceis podem consumir toda a vantagem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T213, T239, T208

## Fontes primárias associadas

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

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

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T238 — Read On Demand com faixa de linhas

**Nome canônico:** Read On Demand com faixa de linhas  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T238  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** just in time file reading; leitura dirigida por linhas

## T238:C01 — conceito

Recuperação de trechos de arquivos somente quando a tarefa exige o conteúdo, usando intervalos de linhas e referências verificáveis. É uma aplicação de contexto sob demanda. A seleção deve preservar o contexto semântico necessário: uma linha isolada pode ocultar importações, condições, escopo e tratamento de erro relevantes.

Como funciona:
- Busca ou mapa do repositório localiza candidatos.
- Uma leitura limitada expande o trecho em torno do alvo.
- Referências à revisão e ao caminho mantêm a ligação entre a evidência lida e o arquivo que poderá ser alterado.

## T238:C02 — aplicacao

Quando usar:
- Repositórios extensos, logs volumosos e investigação de poucos símbolos em muitos arquivos.

Quando não usar:
- Tomar decisões com trechos incompletos sem reconhecer a limitação ou confiar indefinidamente em números de linha após edições.

Implementação proposta:
- Proposta: localizar o símbolo com busca e registrar caminho e revisão observada.
- Ler um intervalo que inclua a unidade relevante, como função, classe ou bloco de configuração.
- Expandir para chamadores, imports e testes somente quando uma hipótese depender deles.
- Marcar truncamento e distinguir ausência no trecho de ausência no arquivo inteiro.
- Depois de uma alteração, atualizar a posição ou resolver novamente o símbolo antes de reutilizar referências.
- Manter o original recuperável para conferência e revisão.

Aplicação LAI proposta:
Proposta LAI: combinar mapa do repositório com leituras por unidade de código e revisão, mantendo evidência suficiente para editar sem carregar arquivos inteiros indiscriminadamente.

## T238:C03 — riscos_validacao

Armadilhas:
- Linhas deslocam após inserções.
- Uma busca literal pode não encontrar nomes gerados dinamicamente.
- A redução excessiva transforma contexto incompleto em falsa certeza.

Métricas sugeridas:
- Bytes e tokens lidos; expansões por investigação; leituras redundantes; referências desatualizadas; hipóteses confirmadas por leitura.

Testes propostos:
- Inserir linhas antes do alvo e verificar atualização da referência.
- Apresentar erro cujo tratamento esteja fora do primeiro intervalo e exigir expansão antes da conclusão.
- Consultar texto ausente no trecho e impedir a alegação de ausência global sem busca apropriada.

## T238:C04 — perguntas_proveniencia

Pergunta: Faixa de linhas é uma referência estável?
Resposta: Somente em uma revisão determinada. Para trabalho entre revisões, use também identidade do arquivo, símbolo e contexto de busca.

Pergunta: Quando vale ler o arquivo completo?
Resposta: Quando suas relações internas são necessárias e ele cabe no orçamento. A técnica prioriza evidência adequada, não a menor leitura possível a qualquer custo.

Pergunta: O número da linha identifica uma função permanentemente?
Resposta: Não. Ele depende da revisão; símbolo, caminho e conteúdo ajudam a reidentificar o alvo após mudanças.

Pergunta: Quando ampliar a leitura?
Resposta: Quando faltarem definições, condições, chamadas ou erros necessários para interpretar o trecho e decidir a alteração.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T238:C05 — mecanismo_avancado

Uma faixa de linhas é endereço relativo a uma versão do arquivo. Inserções anteriores deslocam posições sem mudar o símbolo procurado; renomes e geração de código podem invalidar ainda mais a referência. Uma proposta combina caminho, revisão, intervalo e âncora sintática ou hash do trecho. Expandir a faixa deve responder a uma necessidade concreta, como obter definição de variável, condição envolvente ou contrato chamado.

Condição de contorno:
Um trecho pode parecer suficiente e omitir um guard, decorator, import ou tratamento de erro que muda seu significado.

Contrato proposto:
- Entradas: Arquivo e revisão, intervalo solicitado, símbolo e objetivo da leitura.
- Saídas: Trecho com limites claros, proveniência e indicação de contexto adicional necessário.
- Estado: Âncoras, hashes e faixas já lidas na mesma revisão.
- Invariante: Linha antiga não é reutilizada como localização exata após mudança de base sem verificação.

Compromissos de projeto:
- Faixas pequenas economizam contexto e aumentam chamadas de expansão.
- Faixas grandes preservam relações e podem introduzir material irrelevante.

## T238:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir linhas antes da função e alterar uma condição externa ao trecho original; exigir resolução da revisão e expansão suficiente para perceber a condição.

Plano de avaliação proposto:
Comparar leitura integral, faixa fixa e expansão por símbolo em tarefas de diagnóstico. Medir tokens, rodadas, localização correta e decisões que ignoraram contexto externo. Escolher a janela pela unidade semântica necessária, não apenas por tamanho.

Comparações:
- T216 (complements): Repo map ajuda a escolher arquivo e símbolo, mas a leitura precisa confirmar a revisão.
- T232 (complements): Metadados de posição e escopo podem ligar trechos à estrutura sintática.

Afirmação rastreável:
LibCST oferece metadados de posição e escopo associados a nós de uma árvore específica.
Suporte: related; fontes: V3C-S033
Limite: Leitura sob demanda por linha é uma política editorial; metadados antigos não acompanham automaticamente edições posteriores.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T238:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 associava faixa de linhas à revisão e âncora. A expansão escolhe unidades de leitura por hipótese, controla ampliação de contexto e registra o que não foi lido para evitar conclusões globais a partir de fragmentos.

Leitura guiada por decisão
Antes de abrir um trecho, explicite a dúvida que ele deve resolver: assinatura, guard, chamador ou comportamento de erro. A faixa inicial inclui contexto suficiente para essa decisão. Se surge dependência externa ao trecho, faça leitura adicional direcionada, sem presumir que ausência no fragmento significa ausência no arquivo ou projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

Âncora e revisão
Resolva símbolo ou padrão na revisão atual e obtenha a faixa a partir dessa resolução. Guardar números de linha continua útil para rastreabilidade, mas não como endereço permanente após edição. Para arquivos gerados ou renomeados, recupere também origem e processo de geração; editar a saída errada pode ser desfeito pelo próximo build.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V3C-S027.

Orçamento de expansão
Defina progressão de leitura: trecho, função, contexto de classe ou módulo, consumidores relevantes. Uma expansão deve responder a necessidade concreta e ser contabilizada. Quando muitas dependências cruzadas aparecem, pode ser mais barato ler uma unidade maior ou trocar a decomposição do que fazer dezenas de chamadas minúsculas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S027, V4C-S030.

USO AVANÇADO — Correção localizada
Cenário: Um erro aponta para função em arquivo grande.
Estratégia: Leia a função com assinatura, decorators e tratamento de erro, examine definição dos símbolos usados e teste que reproduz o defeito. Só então edite. Após a mudança, recalcule faixa e valide o código atual; não reutilize trechos anteriores como se fossem bytes vigentes.
Papel do modelo pequeno: 3–7B analisa funções curtas; 8–14B segue dependências; 15–30B decide quando ampliar escopo.
Aceite proposto: Proposta: localizar e corrigir com menos tokens sem omitir contexto que muda o significado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V3C-S033.

USO AVANÇADO — Revisão de patch em monorepo
Cenário: Um revisor precisa verificar alteração sem carregar todo o projeto.
Estratégia: Parta do diff e leia contexto ao redor, contratos chamados e consumidores afetados. Registre quais propriedades foram verificadas e quais exigiriam leitura maior. Materialização sob demanda pode reduzir I/O, mas não equivale a ter analisado tudo que permanece remoto.
Papel do modelo pequeno: 8–14B revisa partes; 15–30B integra propriedades que atravessam módulos.
Aceite proposto: Proposta: mesma detecção de falhas relevantes com leitura total e custo de recuperação contabilizados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S027, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Trechos semanticamente completos e poucas dependências reduzem carga de contexto.
8–14B: Navegação por símbolos e escolha da próxima faixa a partir de hipótese explícita.
15–30B: Análise de impacto e decisão de juntar contexto quando leitura fragmentada perde relações.
Requisitos de treino/runtime: Ferramenta de leitura com revisão, offsets e indicadores de truncamento; acesso ao conteúdo integral quando necessário.
Não aplicar quando: Não declarar propriedade global do repositório depois de ler somente linhas selecionadas.

## T238:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Scion fornece consulta e materialização seletiva de arquivos sob demanda; não demonstra especificamente a API de faixa de linhas.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: A infraestrutura lê versões pertinentes à mudança, mas não demonstra leitura LLM por faixas de linhas.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Materialização sob demanda inspira leitura seletiva, mas não é leitura LLM por faixa de linhas.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos operacionais de navegação e Scion apoiam leitura seletiva como família. A estratégia por linhas e seus critérios são proposta, sem contagem indevida de adoção exata.
Consultas registradas: V4C-Q024, V4C-Q027, V4C-Q023.

## T238:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T238 → T216 [complements]
Como combinar: Repo map fornece símbolos e relações para decidir quais faixas ler primeiro.
Interface: Caminho, símbolo, revisão e hipótese de localização.
Condição: Mapa corresponde à revisão ou é revalidado.
Aceite proposto: Trecho obtido contém a definição efetiva, não uma posição obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T238 → T233 [complements]
Como combinar: Leituras de contexto apoiam validação do patch, sem substituir teste da árvore completa quando necessário.
Interface: Diff, base e trechos de dependências.
Condição: Escopo da conclusão acompanha escopo da inspeção.
Aceite proposto: Revisor não afirma cobertura que não realizou.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Linhas omitidas podem conter guard, import ou efeito que altera a interpretação.
- Scion materializa conteúdo sob demanda; isso não prova a API específica de faixas de linhas proposta aqui.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare tokens lidos, chamadas de ferramenta e correção sob a mesma tarefa. Modelos pequenos podem aproveitar leitura dirigida, mas não inferem com segurança código que nunca foi observado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T216, T222, T214, T233

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T239 — Git Worktrees

**Nome canônico:** Git Worktrees  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T239  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** linked worktree; árvores de trabalho Git

## T239:C01 — conceito

Mecanismo Git para manter várias árvores de trabalho ligadas ao mesmo repositório. Cada worktree oferece diretório e estado de checkout próprios, enquanto compartilha objetos e partes da administração do repositório. Isso facilita trabalho paralelo em revisões distintas, mas não constitui isolamento de processos, serviços ou credenciais.

Como funciona:
- O repositório compartilha o banco de objetos entre árvores relacionadas.
- Cada árvore mantém arquivos de trabalho e estado próprio de checkout e índice.
- Branches e commits permitem revisar e integrar os resultados produzidos em cada área.

## T239:C02 — aplicacao

Quando usar:
- Agentes alterando módulos em paralelo, reprodução de uma regressão e comparação de versões sem trocar continuamente o checkout principal.

Quando não usar:
- Como sandbox de segurança ou garantia de que duas execuções não disputarão portas, banco de dados e serviços externos.

Implementação proposta:
- Proposta: criar uma árvore com branch ou revisão apropriada à missão, respeitando as restrições documentadas pelo Git.
- Atribuir diretório e responsabilidade de escrita ao executor correspondente.
- Separar configuração de testes, portas e dados temporários quando houver execução paralela.
- Concluir e revisar o delta antes de integrar à branch de destino.
- Inspecionar alterações não commitadas antes de remover uma árvore; preservar trabalho útil e limpar metadados pelo fluxo suportado.

Aplicação LAI proposta:
Proposta LAI: dar a cada missão de código uma área de trabalho identificada, com integração coordenada e recursos de teste separados quando necessário.

## T239:C03 — riscos_validacao

Armadilhas:
- Árvores diferentes podem usar o mesmo banco de testes.
- Integração textual sem conflito pode manter incompatibilidade semântica.
- Objetos compartilhados e referências comuns exigem cuidado com operações de manutenção e histórico.

Métricas sugeridas:
- Conflitos de integração; alterações fora da árvore atribuída; colisões de recursos; tempo de preparação; trabalho perdido na limpeza.

Testes propostos:
- Editar arquivos em uma árvore e confirmar que o checkout de outra não muda.
- Executar testes simultâneos com recursos separados e verificar ausência de interferência.
- Integrar duas mudanças compatíveis textualmente, mas conflitantes no contrato, e exigir validação funcional.

## T239:C04 — perguntas_proveniencia

Pergunta: Worktree é uma cópia independente do repositório inteiro?
Resposta: Não. Ele compartilha objetos e estruturas do repositório, embora ofereça uma árvore de arquivos e checkout separados.

Pergunta: Posso considerar toda integração segura se Git não apontar conflito?
Resposta: Não. Git detecta determinados conflitos de conteúdo; mudanças podem conflitar em APIs, comportamento ou dados sem conflito textual.

Pergunta: worktree lock impede outro agente de editar arquivos?
Resposta: Não. Seu propósito documentado é proteger a árvore administrativa contra certas operações de limpeza, movimento ou remoção.

Pergunta: Um teste em outro worktree pode alterar meu ambiente?
Resposta: Sim, se usar recursos compartilhados fora do checkout, como banco, porta, cache ou diretório de build.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T239:C05 — mecanismo_avancado

Worktrees mantêm HEAD e índice próprios, enquanto compartilham objetos e grande parte das refs. Isso explica por que mudanças de referências podem afetar a visão do repositório sem editar arquivos da outra árvore. O comando worktree lock protege metadados contra poda e remoção; não funciona como mutex de edição dos arquivos. Serviços, portas, bancos e outputs fora da árvore ainda exigem isolamento específico para execução paralela.

Condição de contorno:
Dois worktrees podem executar testes que escrevem no mesmo banco ou diretório externo e interferir apesar de seus arquivos de checkout estarem separados.

Contrato proposto:
- Entradas: Revisão-base, caminho da árvore, branch ou HEAD destacado e recursos externos.
- Saídas: Árvore identificada e contrato de integração do resultado.
- Estado: HEAD, índice, refs compartilhadas e recursos alocados por tarefa.
- Invariante: Isolamento de checkout não é anunciado como isolamento completo de processos ou efeitos.

Compromissos de projeto:
- Compartilhar objetos economiza armazenamento e mantém acoplamento administrativo do repositório.
- Separar árvores facilita paralelismo e exige limpeza e integração das revisões produzidas.

## T239:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar dois jobs em worktrees distintos usando o mesmo arquivo de saída externo; exigir detecção da colisão e atribuição de destinos separados.

Plano de avaliação proposto:
Comparar branches na mesma árvore e worktrees separados em alterações concorrentes. Medir conflitos de checkout, interferência de testes e custo de integração. Conferir também recursos externos, sem limitar a avaliação ao diff dos arquivos.

Comparações:
- T169 (complements): Agentes com contextos separados podem usar worktrees para também separar árvores de edição.
- T236 (complements): Commits identificam entregas que depois precisam ser integradas explicitamente.

Afirmação rastreável:
Git documenta HEAD e índice por worktree, refs compartilhadas e lock voltado à proteção administrativa.
Suporte: direct; fontes: V2A-S019
Limite: O mecanismo não fornece exclusão mútua geral para escrita nem isola dependências externas.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T239:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia objetos compartilhados e recursos externos. A expansão trata worktrees como unidades de experimento, organiza ambiente e limpeza e integra candidatos sem confundir isolamento de arquivos com isolamento completo de execução.

Ambiente por candidato
Além do checkout, associe portas, banco, diretórios temporários e observabilidade à identidade do candidato. O harness Codex relata aplicação e métricas por worktree; a transferência proposta replica esse princípio conforme o projeto. Se algum recurso precisa ser compartilhado, documente coordenação ou somente leitura, evitando testes concorrentes que alteram o mesmo estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V2A-S019.

Ciclo de vida recuperável
Registre criação, branch, tarefa, processos ativos e prazo de retenção. Remover diretório não encerra necessariamente servidor iniciado por um agente. Antes da limpeza, classifique tarefas e efeitos pendentes, preserve artefatos necessários e finalize recursos próprios. Não apagar worktree só porque o processo principal terminou com exit code zero.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S039.

Integração condicional
Candidatos partem de uma base identificada, mas a branch principal pode avançar enquanto os testes rodam. Escolher um candidato não elimina a necessidade de reconciliar essa diferença. Depois de rebase, merge ou combinação de patches, teste a árvore resultante; a aprovação antiga pertencia à versão isolada anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

USO AVANÇADO — Alternativas de reparo
Cenário: Vários modelos tentam resolver o mesmo defeito.
Estratégia: Crie worktree e recursos por candidato, aplique o patch e rode o mesmo teste reproduzível. Compare resultados e preserve só candidatos necessários à revisão. Evite que um trabalhador leia arquivos não confirmados do outro e transforme variantes em soluções correlacionadas inadvertidamente.
Papel do modelo pequeno: 3–7B gera reparos locais; 15–30B integra evidência e escolhe candidato.
Aceite proposto: Proposta: resultados reproduzíveis sem interferência entre testes ou servidores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V2A-S019.

USO AVANÇADO — Trabalho simultâneo por módulos
Cenário: Agentes executam micro-missões independentes no mesmo repositório.
Estratégia: Atribua worktree e branch por missão, fixe interfaces compartilhadas e integre por ordem de dependência. Use registro de tarefas para evitar alterações concorrentes incompatíveis; worktree não é mutex do domínio. Após integrar, limpe ambientes e mantenha evidência de validação.
Papel do modelo pequeno: 8–14B executa módulo; 15–30B coordena dependências de integração.
Aceite proposto: Proposta: nenhuma colisão de recurso externo e rastreabilidade da árvore testada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Isolamento permite testar patches pequenos sem arriscar alterações de outra tarefa.
8–14B: Executar módulo com ambiente próprio e devolver artefato identificado.
15–30B: Gerenciar combinação de candidatos e conflitos sem supor independência semântica por diretório.
Requisitos de treino/runtime: Git compatível, branches e recursos únicos, limpeza de subprocessos e registros de criação/retomada.
Não aplicar quando: Não usar worktree lock como trava de edição nem presumir bancos e portas isolados automaticamente.

## T239:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Artigo de harness usa uma aplicação e observabilidade isoladas por Git worktree.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Checkouts esparsos/virtualizados não são Git worktrees.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Virtualização de checkout não comprova uso de Git worktrees.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Ambiente isolado não é prova de uso do comando Git worktree.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: OpenAI oferece caso direto de worktrees; Git/GVFS, Sapling e Scion não foram convertidos em casos exatos deste mecanismo.
Consultas registradas: V4C-Q027, V4C-Q015, V4C-Q016.

## T239:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T239 → R021 [complements]
Como combinar: Harness interno OpenAI executa Codex com aplicação e observabilidade específicas por Git worktree.
Interface: Revisão candidata, instância da aplicação e logs correspondentes.
Condição: Recursos externos da tarefa são isolados conforme o projeto.
Aceite proposto: Agente valida comportamento na instância do próprio candidato.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

2. T239 → T233 [complements]
Como combinar: Fornecer árvore isolada para aplicar e testar antes de publicação condicionada.
Interface: Base, árvore final e evidência de testes.
Condição: Nenhuma mudança posterior invalida a prova sem nova verificação.
Aceite proposto: Artefato entregue corresponde ao candidato aceito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Refs e objetos compartilhados podem mudar mesmo sem alterações nos arquivos do outro worktree.
- Limpeza precisa tratar processos e recursos fora da árvore, não apenas remover o checkout.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare throughput de candidatos com custo de ambiente e validação incluídos. Paralelismo com modelos pequenos só ajuda quando CPU, memória e integração suportam a concorrência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T237, T236, T233

## Fontes primárias associadas

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T240 — Snapshot de estado

**Nome canônico:** Snapshot de estado  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T240  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** state snapshot; snapshot persistente

## T240:C01 — conceito

Representação persistida de um estado em um ponto ou fronteira definidos. Um snapshot reduz o custo de reconstrução e oferece uma base para comparação. Ele só representa o escopo que capturou. Um checkpoint de execução acrescenta informação suficiente para retomada segundo o runtime, como posição, tarefas pendentes e resultados relevantes.

Como funciona:
- O produtor captura um conjunto de dados com versão de esquema e identidade da origem.
- Uma marca de consistência, como sequência de eventos, identifica a fronteira representada.
- A recuperação carrega o estado e valida compatibilidade antes de utilizá-lo.

## T240:C02 — aplicacao

Quando usar:
- Reconstrução rápida de projeções, comparação de estado e recuperação de tarefas com representação serializável.

Quando não usar:
- Assumir que uma cópia de arquivos inclui memória de processos, estado de banco e efeitos externos ocorridos ao mesmo tempo.

Implementação proposta:
- Proposta: definir escopo, campos obrigatórios, revisão de código e versão do esquema.
- Capturar dados de forma consistente ou declarar quais partes foram observadas em momentos distintos.
- Registrar sequência confirmada, checksum e referências aos artefatos necessários.
- Validar integridade e compatibilidade durante restauração, preservando um caminho de recuperação quando o snapshot estiver inválido.
- Consultar sistemas externos para operações pendentes, pois o snapshot pode não refletir efeitos concluídos após sua fronteira.

Aplicação LAI proposta:
Proposta LAI: persistir snapshots identificados do estado das missões e projeções, vinculando cada um a revisão, esquema e fronteira de eventos confirmada.

## T240:C03 — riscos_validacao

Armadilhas:
- Um snapshot parcial pode parecer completo.
- Dados serializados podem depender de uma versão de código diferente.
- Restaurar arquivos não desfaz automaticamente efeitos de API ou alterações em serviços.

Métricas sugeridas:
- Tempo de captura e restauração; tamanho; idade; snapshots inválidos; distância entre estado capturado e log atual.

Testes propostos:
- Capturar durante uma atualização concorrente e verificar consistência declarada.
- Restaurar com versão de esquema incompatível e exigir migração validada ou rejeição.
- Comparar estado restaurado com reconstrução independente do mesmo ponto do histórico.

## T240:C04 — perguntas_proveniencia

Pergunta: Snapshot e checkpoint são sinônimos?
Resposta: Não em todos os sistemas. Snapshot descreve um estado capturado; checkpoint é um ponto de retomada definido pelo mecanismo de execução e pode exigir metadados adicionais.

Pergunta: Restaurar um snapshot volta o mundo externo no tempo?
Resposta: Não. A restauração afeta somente o escopo controlado. Operações externas precisam ser observadas e reconciliadas segundo seu estado real.

Pergunta: BEGIN garante que duas leituras vejam o mesmo instante?
Resposta: Não em todo nível de isolamento; é preciso conhecer a semântica da transação utilizada.

Pergunta: Qual é o risco de um cursor adiantado?
Resposta: A recuperação pode considerar já incorporados eventos que não estão no estado capturado, perdendo mudanças.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T240:C05 — mecanismo_avancado

Um snapshot composto precisa representar um corte consistente. Ler estado e cursor em momentos diferentes pode capturar estado anterior com cursor posterior, pulando eventos na recuperação. No PostgreSQL, duas consultas sob Read Committed podem observar versões diferentes mesmo dentro da mesma transação; portanto, apenas escrever BEGIN não define a consistência necessária. A captura deve usar isolamento, transação de gravação ou protocolo compatível com o armazenamento e seu invariante.

Condição de contorno:
Nenhum snapshot local inclui automaticamente estado de serviços externos ou arquivos modificados fora de sua fronteira.

Contrato proposto:
- Entradas: Estado a capturar, cursor, versões de schema e fronteira de consistência.
- Saídas: Snapshot identificado, manifesto e posição exata de reconstrução.
- Estado: Revisões dos membros, método de captura e confirmação de persistência.
- Invariante: Estado e cursor correspondem à mesma fronteira lógica declarada.

Compromissos de projeto:
- Captura coordenada melhora consistência e pode bloquear ou exigir mais armazenamento.
- Captura incremental reduz volume e acrescenta dependências entre versões para restaurar.

## T240:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atualizar estado entre leitura do conteúdo e leitura do cursor; exigir detecção da mistura ou captura que preserve o invariante.

Plano de avaliação proposto:
Comparar captura sem coordenação e captura consistente sob escrita concorrente. Medir divergência após restauração, duração da pausa e tamanho do artefato. Validar o escopo restaurável, incluindo componentes deliberadamente externos.

Comparações:
- T242 (complements): Recuperação híbrida depende de uma posição de snapshot coerente com os eventos restantes.
- T060 (distinct_from): Checkpoint acrescenta semântica de retomada do runtime ao estado capturado.

Afirmação rastreável:
PostgreSQL documenta que consultas sucessivas em Read Committed podem ver dados diferentes na mesma transação.
Suporte: direct; fontes: A-S029
Limite: Isolamento de banco resolve apenas a fronteira que ele controla, não um snapshot global de todos os sistemas.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T240:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigia corte consistente entre estado e cursor. A ampliação define composição de snapshot para agentes, valida restauração antes de confiar no backup e separa dados recuperáveis de recursos que precisam ser reconstruídos.

Manifesto de componentes
Liste plano, estado de tarefas, referências de artefatos, decisões e operações externas pendentes. Inclua versão dos schemas e do código que interpreta cada parte. Não presumir que salvar mensagens captura filesystem, banco e subprocessos; cada componente precisa de fronteira declarada e procedimento de restauração ou reconstrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S030.

Captura coordenada
Escolha pausar escritores, usar snapshot transacional ou publicar versões imutáveis com um manifesto consistente. A estratégia depende do armazenamento. Um arquivo de estado copiado enquanto muda pode ser sintaticamente válido e semanticamente misturar momentos; hashes dos componentes não corrigem um corte inconsistente entre eles.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V3C-S028.

Restauração como teste
Verifique integridade, compatibilidade e capacidade de retomar antes de declarar o snapshot útil. Faça restauração em ambiente isolado e confirme invariantes de tarefa e referências. Recursos efêmeros, como conexão ou cache KV, podem ser reconstruídos; efeitos externos exigem consulta atual, porque o snapshot descreve o que se sabia, não o mundo presente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

USO AVANÇADO — Missão longa interrompível
Cenário: Uma campanha precisa sobreviver a manutenção e falhas.
Estratégia: Capture fronteira após unidades aceitas, persistindo manifesto e cursores coerentes. Na restauração, reabra artefatos, valide revisão e reconcilie operações em andamento. Depois de confirmar o estado, retome pendências; não assumir que ausência no snapshot prova que nenhum efeito posterior ocorreu.
Papel do modelo pequeno: 3–7B executa unidades; 15–30B interpreta pendências complexas após recuperação.
Aceite proposto: Proposta: restauração reproduz estado aceito sem lacunas ou duplicações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S028.

USO AVANÇADO — Experimento de estratégias
Cenário: É necessário comparar dois planos a partir do mesmo ponto.
Estratégia: Crie snapshot de estado lógico e artefatos imutáveis, depois rode variantes em ambientes isolados. Requisições externas mutáveis precisam ser gravadas ou controladas para que as condições sejam comparáveis. Não tratar duas restaurações com fontes atualizadas em horários distintos como experimento idêntico.
Papel do modelo pequeno: 8–14B executa variante; avaliador externo compara resultados e custos.
Aceite proposto: Proposta: diferenças atribuíveis à estratégia, com condições de entrada documentadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Estados compactos por unidade tornam snapshot e verificação mais simples.
8–14B: Validar consistência de tarefas e referências após restauração.
15–30B: Reconciliar dependências complexas e decidir replanejamento quando ambiente mudou.
Requisitos de treino/runtime: Armazenamento com protocolo de corte consistente, manifesto versionado e ensaios de restauração.
Não aplicar quando: Não chamar cópia de chat ou arquivo isolado de snapshot integral da execução.

## T240:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Checkpoints de offsets não equivalem a snapshot completo e consistente de toda aplicação.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cadence e padrões de estado apoiam continuidade; Brooklin oferece offsets por tarefas, não prova snapshot global cognitivo. A composição proposta exige teste próprio.
Consultas registradas: V4C-Q002, V4C-Q020, V4C-Q027.

## T240:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T240 → T242 [complements]
Como combinar: Snapshot serve como base para aplicar eventos posteriores e reduzir tempo de recuperação.
Interface: Estado, cursor e versão do processador.
Condição: Cursor corresponde exatamente ao conteúdo capturado.
Aceite proposto: Resultado equivale à reconstrução de referência sob as mesmas regras.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S041. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T240 → T243 [complements]
Como combinar: Após restaurar estado local, consultar desfecho atual das intenções externas pendentes.
Interface: IDs de operação e último estado conhecido.
Condição: Snapshot não é tratado como rollback do serviço remoto.
Aceite proposto: Efeito ocorrido depois da captura é reconhecido antes de repetir.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Snapshot íntegro pode ser semanticamente incompatível com código novo.
- Teste de restauração precisa incluir referências externas aos bytes do manifesto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare tempo e correção de retomada separadamente da qualidade da LLM. Snapshots podem tornar modelos pequenos operacionalmente persistentes sem aumentar a informação que conseguem processar por chamada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T064, T242, T243

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S041 — Marten — Events Versioning

[https://martendb.io/events/versioning.html](https://martendb.io/events/versioning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evolução de schemas e upcasting permitem interpretar eventos históricos sem tratar mudança de representação como novo fato.

Limite: Mecanismos específicos do framework; conversão deve preservar semântica e não inventar informação histórica ausente.

### V4C-S024 — Open sourcing Brooklin: Near real-time data streaming at scale

[https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso operacional de Brooklin na LinkedIn para replicação e streaming, incluindo CDC; arquitetura técnica detalhada em fonte separada.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T241 — Event Replay

**Nome canônico:** Event Replay  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T241  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** event replay; reprodução de eventos

## T241:C01 — conceito

Reconstrução de estado pela aplicação ordenada de eventos previamente registrados. Em Event Sourcing, replay permite refazer uma projeção ou investigar uma versão histórica. Reaplicar fatos a uma função de estado não significa reenviar mensagens, pagamentos, deploys ou outras ações que os eventos descrevem.

Como funciona:
- O log fornece identidade, ordem e versão dos eventos.
- Um processador aplica cada fato à projeção segundo regras conhecidas.
- A recuperação registra a fronteira processada e evita contar duplicatas como novos acontecimentos.

## T241:C02 — aplicacao

Quando usar:
- Reconstrução de índices e projeções, diagnóstico histórico e comparação entre versões de lógica de domínio.

Quando não usar:
- Usar o mesmo caminho de execução para replay e efeitos externos sem uma separação explícita e verificável.

Implementação proposta:
- Proposta: separar decisões e efeitos de funções que apenas aplicam fatos ao estado.
- Preservar eventos originais e definir migração ou interpretação compatível para versões antigas.
- Ordenar pela sequência apropriada ao agregado ou partição, sem presumir que timestamp global fornece ordem causal.
- Reproduzir em ambiente de projeção com efeitos externos desabilitados por construção.
- Comparar resultados e registrar a última sequência aplicada; deduplicar pela identidade do evento quando necessário.

Aplicação LAI proposta:
Proposta LAI: reconstruir estado de missões a partir de eventos confirmados, preservando efeitos externos em registros próprios e mantendo a reconstrução livre de novas mutações.

## T241:C03 — riscos_validacao

Armadilhas:
- Código não determinístico produz projeções diferentes.
- Um evento antigo pode não conter dados exigidos pela lógica nova.
- Reexecutar efeitos transforma uma recuperação de estado em uma segunda operação de negócio.

Métricas sugeridas:
- Eventos processados por segundo; divergência de projeção; duplicatas; falhas por esquema; tempo para reconstruir uma fronteira.

Testes propostos:
- Reprocessar o mesmo histórico e comparar o estado final.
- Incluir eventos duplicados e fora de ordem e verificar a política declarada.
- Substituir clientes externos por observadores que falham em qualquer chamada e demonstrar que replay não os aciona.

## T241:C04 — perguntas_proveniencia

Pergunta: Replay pode reproduzir uma resposta antiga de ferramenta?
Resposta: Pode usar o resultado registrado como evidência histórica, desde que a identidade e o conteúdo estejam preservados. Isso não exige chamar novamente a ferramenta.

Pergunta: Reexecutar uma ação externa durante recuperação é sempre proibido?
Resposta: Não, mas é uma decisão separada, dependente de autorização, idempotência e reconciliação. Não deve ocorrer implicitamente por leitura do histórico.

Pergunta: Mesmo log sempre produz o mesmo estado?
Resposta: Somente sob regras, ordem e entradas auxiliares compatíveis; trocar o processador pode mudar a projeção.

Pergunta: Posso usar a data atual para completar um evento antigo?
Resposta: Não como se fosse um fato original. Isso introduz dependência externa e altera o significado histórico.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T241:C05 — mecanismo_avancado

Replay de eventos históricos exige compatibilidade de representação e significado. Um upcaster pode converter o schema antigo para o atual durante a leitura, mas não deve inventar informação que nunca foi registrada. Mudança de regra de projeção também pode produzir estado diferente a partir dos mesmos fatos; nesse caso, reconstrução atual e reprodução histórica são objetivos distintos. O contrato precisa declarar qual versão do processador será utilizada.

Condição de contorno:
Eventos incompletos, ordem incorreta ou transformações dependentes do relógio atual impedem reconstrução reproduzível.

Contrato proposto:
- Entradas: Eventos ordenados, cursor inicial, versão do reducer e conversões de schema.
- Saídas: Projeção reconstruída, cursor final e eventos não interpretáveis.
- Estado: Versões de processamento, IDs já aplicados e falhas de conversão.
- Invariante: Reconstrução da projeção não reenvia efeitos externos apenas porque encontra eventos antigos.

Compromissos de projeto:
- Upcasting evita regravar o histórico e aumenta trabalho de leitura e manutenção.
- Preservar processadores antigos permite reprodução histórica e amplia carga de compatibilidade.

## T241:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir evento antigo sem campo recém-exigido e converter usando um default que altera significado; exigir tratamento explícito da ausência, sem simular fato histórico inexistente.

Plano de avaliação proposto:
Comparar projeção antiga reproduzida e projeção nova reconstruída sobre o mesmo log. Medir divergências explicáveis, eventos rejeitados, tempo e efeitos externos indevidos. Separar regressão de mudança intencional de regra.

Comparações:
- T170 (complements): Evolução de schema também precisa de compatibilidade entre versões de eventos.
- T242 (complements): Replay a partir de snapshot aplica somente o sufixo ainda não incorporado.

Afirmação rastreável:
Marten descreve upcasting como transformação do schema antigo durante a leitura do evento.
Suporte: direct; fontes: V3C-S041
Limite: Conversão estrutural não prova preservação semântica; fatos ausentes continuam ausentes.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T241:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava reprodução histórica e projeção atual. A expansão define fronteiras de replay para agentes, bloqueia efeitos durante reconstrução e valida migrações com históricos representativos de falhas.

Decisões observadas versus geração nova
Uma chamada LLM gravada como decisão deve ser reproduzida pelo resultado registrado quando o objetivo é reconstruir a execução. Consultar novamente o modelo cria uma nova decisão, mesmo com temperatura baixa. Se a intenção é reavaliar com modelo novo, trate como experimento ou nova projeção, preservando o histórico original para comparação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

Reconstrução sem efeitos
Aplicadores de eventos devem atualizar projeções ou emitir comandos controlados, sem reenviar automaticamente efeitos já ocorridos. Separe modo de reconstrução e modo ativo, e teste fronteiras onde uma atividade foi enviada mas a confirmação local não chegou. Reconstruir intenção desconhecida não autoriza concluir que o efeito está ausente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S018.

Compatibilidade exercitada
Use históricos com timeout, cancelamento, concorrência e versão antiga, não apenas sucessos curtos. Upcasters preservam significado do que foi registrado; campos novos obrigatórios sem origem exigem migração explícita ou representação de ausência. A ordem causal e a identidade dos eventos precisam ser preservadas mesmo quando índices são reconstruídos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S001.

USO AVANÇADO — Atualização de runtime
Cenário: Uma nova versão deve retomar missões antigas.
Estratégia: Reproduza históricos selecionados em ambiente sem efeitos e compare comandos ou estados esperados conforme o contrato do runtime. Divergências legítimas precisam de plano de migração; divergências acidentais bloqueiam a publicação. Manter worker antigo pode ser necessário enquanto execuções anteriores terminam.
Papel do modelo pequeno: 3–30B continua em atividades externas ao replay determinístico; código controla reprodução.
Aceite proposto: Proposta: históricos compatíveis retomam e os incompatíveis falham de forma explícita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, V3C-S018.

USO AVANÇADO — Auditoria de decisão
Cenário: É necessário explicar como um agente chegou a um resultado.
Estratégia: Reconstrua observações, versões de ferramenta e decisões confirmadas, distinguindo dados disponíveis naquele momento dos atuais. Não preencher lacunas com uma narrativa nova da LLM. Quando o log não contém uma informação, a conclusão correta é limite de reconstrução.
Papel do modelo pequeno: 8–14B organiza evidência; 15–30B explica causalidade com referências ao log.
Aceite proposto: Proposta: cada explicação operacional aponta a evento ou artefato existente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atividades pequenas registradas facilitam replay porque a decisão fica delimitada.
8–14B: Interpretar logs reconstruídos e classificar falhas sem executar efeitos.
15–30B: Comparar versões e sugerir migração, preservando prova histórica independente.
Requisitos de treino/runtime: Log ordenado, schemas e processadores versionados, bloqueio de efeitos e artefatos externos disponíveis.
Não aplicar quando: Não chamar nova execução probabilística de replay fiel nem inventar fatos ausentes em upcast.

## T241:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: A fonte descreve replay/shadowing de históricos para detectar incompatibilidades.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Releitura de streams a partir de posições é relacionada a replay, sem provar reconstrução integral de estado de agente.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cadence oferece caso operacional de replay. Transporte de eventos Brooklin não foi considerado equivalente à reprodução determinística de decisões do agente.
Consultas registradas: V4C-Q002, V4C-Q020.

## T241:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T241 → T159 [complements]
Como combinar: Cadence utiliza histórico e replay para execução durável e validação de evolução.
Interface: Histórico, comandos e versão compatível.
Condição: Operações externas seguem a fronteira adequada do runtime.
Aceite proposto: Reconstrução não gera nova observação para explicar o passado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S001. Casos: V4C-C003.

2. T241 → T242 [complements]
Como combinar: Aplicar apenas eventos posteriores ao snapshot compatível, preservando a mesma semântica de redução.
Interface: Cursor, versão e sufixo do log.
Condição: Todos os eventos necessários continuam disponíveis.
Aceite proposto: Estado recuperado coincide com replay de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S041. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Replay que acessa relógio atual ou fonte mutável pode divergir sem erro de parsing.
- Deduplicar eventos requer identidade; textos parecidos podem representar intenções distintas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fidelidade e tempo de reconstrução entre arquiteturas, não entre capacidades linguísticas. O modelo pode explicar o replay, mas a correção depende do registro e do processador.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T240, T242, T243

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S041 — Marten — Events Versioning

[https://martendb.io/events/versioning.html](https://martendb.io/events/versioning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evolução de schemas e upcasting permitem interpretar eventos históricos sem tratar mudança de representação como novo fato.

Limite: Mecanismos específicos do framework; conversão deve preservar semântica e não inventar informação histórica ausente.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S024 — Open sourcing Brooklin: Near real-time data streaming at scale

[https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso operacional de Brooklin na LinkedIn para replicação e streaming, incluindo CDC; arquitetura técnica detalhada em fonte separada.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T242 — Recuperação híbrida por Snapshot + Event Sourcing

**Nome canônico:** Recuperação híbrida por Snapshot + Event Sourcing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T242  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** snapshot plus event sourcing; snapshot e replay incremental

## T242:C01 — conceito

Recuperação que carrega um snapshot válido e aplica apenas os eventos posteriores à sua fronteira. O padrão reduz trabalho de reconstrução sem transformar o snapshot na única fonte de verdade. Sua correção depende de alinhamento entre estado capturado, sequência confirmada e versão do processador de eventos.

Como funciona:
- O snapshot representa todos os eventos até uma sequência declarada.
- O recuperador inicia nesse estado e aplica o sufixo do log após a fronteira.
- Se o snapshot não puder ser validado, usa outro ponto consistente ou reconstrução integral compatível.

## T242:C02 — aplicacao

Quando usar:
- Históricos extensos, projeções custosas e tarefas duráveis cuja recuperação integral seria lenta.

Quando não usar:
- Combinar uma cópia parcial com um log de cobertura desconhecida ou apagar eventos necessários sem política de retenção e reconstrução definida.

Implementação proposta:
- Proposta: persistir snapshot com schema_version, processor_version, sequência e digest dos dados.
- Garantir que a fronteira não avance além dos eventos efetivamente incorporados ao estado.
- Carregar o snapshot validado, buscar eventos estritamente posteriores e aplicar a mesma lógica de reconstrução.
- Tratar duplicatas e gaps conforme a ordenação do log; um gap não deve ser silenciosamente ignorado.
- Comparar periodicamente a recuperação híbrida com replay integral em uma amostra e reconciliar efeitos externos à parte.

Aplicação LAI proposta:
Proposta LAI: acelerar retomadas de missões preservando um log verificável, snapshots versionados e uma política explícita de compatibilidade e retenção.

## T242:C03 — riscos_validacao

Armadilhas:
- Erro de uma unidade na fronteira duplica ou omite um evento.
- Mudanças no redutor podem tornar snapshots antigos incompatíveis.
- Um log incompleto impede a reconstrução mesmo quando o snapshot parece íntegro.

Métricas sugeridas:
- Tempo de recuperação; tamanho do sufixo; idade do snapshot; gaps; divergência contra replay integral; falhas de compatibilidade.

Testes propostos:
- Criar snapshot na sequência N e verificar aplicação a partir de N+1.
- Corromper o snapshot e confirmar fallback controlado.
- Remover um evento do sufixo e exigir diagnóstico de cobertura incompleta.
- Restaurar diferentes snapshots do mesmo histórico e comparar o estado final esperado.

## T242:C04 — perguntas_proveniencia

Pergunta: Snapshot torna Event Sourcing desnecessário?
Resposta: Não neste padrão. O snapshot é um atalho materializado; os eventos posteriores e a identidade da fronteira continuam necessários à recuperação.

Pergunta: Isso garante exatamente uma execução de efeitos externos?
Resposta: Não. O padrão reconstrói estado local. Garantias de efeitos dependem do protocolo com o sistema externo, da idempotência e da reconciliação de incertezas.

Pergunta: O snapshot permite apagar imediatamente todo o histórico?
Resposta: Não sem mudar o contrato de recuperação e auditoria; erros de snapshot ou novas projeções podem precisar dos eventos antigos.

Pergunta: Como verificar a fronteira do cursor?
Resposta: Comparar a recuperação híbrida com uma projeção de referência e incluir eventos imediatamente antes e depois da posição declarada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T242:C05 — mecanismo_avancado

O snapshot precisa declarar se seu cursor representa último evento incluído ou próximo evento a aplicar. Se incorpora até 100, o sufixo começa em 101; essa convenção evita dupla aplicação ou lacuna. Versão do reducer, schema e identidade do stream também precisam ser compatíveis. Um snapshot corrompido deve permitir recorrer a uma versão anterior ou ao replay integral, desde que o histórico necessário ainda exista.

Condição de contorno:
Apagar eventos antigos após snapshot elimina a recuperação integral e torna disponibilidade e compatibilidade desse snapshot mais críticas.

Contrato proposto:
- Entradas: Snapshot, cursor com semântica explícita, stream e processador compatível.
- Saídas: Estado restaurado, sufixo aplicado e evidência de continuidade.
- Estado: Versões, integridade do snapshot e intervalo disponível de eventos.
- Invariante: Nenhum evento lógico é omitido ou aplicado duas vezes na fronteira da recuperação.

Compromissos de projeto:
- Snapshots frequentes encurtam replay e consomem escrita e armazenamento.
- Retenção curta reduz volume e diminui opções de reconstrução após corrupção ou mudança de código.

## T242:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar o cursor em uma unidade e corromper o snapshot mais recente; exigir detecção da inconsistência e fallback para base recuperável sem repetir efeitos externos.

Plano de avaliação proposto:
Comparar replay integral e recuperação híbrida em históricos de tamanhos variados. Verificar igualdade do estado esperado, duração e custo de snapshots. Escolher frequência pela relação entre taxa de eventos, custo de projeção e objetivo de recuperação.

Comparações:
- T240 (requires): O mecanismo híbrido pressupõe uma base de snapshot válida ou retorna ao replay integral.
- T241 (requires): Aplicar os eventos posteriores é parte constitutiva da recuperação híbrida.

Afirmação rastreável:
Event sourcing usa histórico ordenado para reidratar estado, e snapshots podem reduzir o trabalho de reconstrução.
Suporte: direct; fontes: A-S027
Limite: A fonte apoia o padrão; convenção do cursor e fallback precisam ser definidos e verificados pela aplicação.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T242:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 fixava cursor e fallback para snapshot anterior. A expansão otimiza recuperação com verificação de compatibilidade, política de retenção e ensaios que distinguem dados perdidos de mero tempo de reconstrução.

Escolher base elegível
O snapshot mais recente nem sempre é utilizável: pode ter schema incompatível, artefato ausente ou versão de reducer indisponível. Selecione a base mais recente que satisfaça integridade e semântica, e declare o custo do sufixo restante. Não converter silenciosamente campos sem origem apenas para conseguir usar o checkpoint novo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V3C-S028.

Retenção como contrato
Decida por quanto tempo conservar eventos anteriores e snapshots compatíveis. Apagar o prefixo reduz armazenamento e elimina caminhos de recuperação; o snapshot passa a ser parte crítica do estado durável. Teste corrupção e perda antes de adotar essa política, incluindo referências a arquivos que não estão dentro do log.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S025.

Metas de recuperação
Meça tempo até serviço apto e até missão efetivamente reconciliada. Carregar um snapshot rapidamente não significa que efeitos externos e eventos atrasados foram resolvidos. Defina quais dados podem ser perdidos, se algum, e quais operações devem permanecer desconhecidas até consulta; não esconder incerteza atrás de uma métrica de startup.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

USO AVANÇADO — Missões com histórico extenso
Cenário: Reproduzir tudo a cada retomada fica caro.
Estratégia: Crie snapshots em fronteiras consistentes e aplique o sufixo em ambiente controlado. Compare o resultado com replay integral numa amostra de históricos que incluam falhas. Se a comparação divergir, preserve log e investigue antes de reduzir retenção.
Papel do modelo pequeno: 3–30B opera nas atividades; recuperação do estado fica em código verificável.
Aceite proposto: Proposta: estado equivalente à referência com tempo de recuperação menor e sem lacunas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S001.

USO AVANÇADO — Migração do formato de estado
Cenário: Um novo esquema muda como tarefas e evidências são representadas.
Estratégia: Mantenha processador antigo disponível ou gere snapshot migrado com manifesto de transformação. Verifique invariantes e referências antes de marcá-lo elegível. Se um campo não pode ser reconstruído, represente a lacuna ou refaça a etapa com nova intenção, sem atribuir dado inventado ao passado.
Papel do modelo pequeno: 8–14B auxilia mapeamento; 15–30B revisa casos ambíguos; código executa migração.
Aceite proposto: Proposta: migração auditável e fallback para base anterior enquanto houver compatibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V3C-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Unidades de atividade pequenas reduzem o estado que precisa ser recuperado por vez.
8–14B: Checagem de tarefas e referências após replay, sem modificar automaticamente o histórico.
15–30B: Análise de migração e reconciliação de exceções, mantendo lógica de recuperação determinística.
Requisitos de treino/runtime: Cursor inequívoco, identidade do stream, versão do reducer e política explícita de retenção.
Não aplicar quando: Não eliminar eventos antigos antes de demonstrar restauração e compatibilidade dos snapshots remanescentes.

## T242:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes de event sourcing e continuidade sustentam princípios. Não foi encontrado caso operacional que prove exatamente toda a composição editorial para agentes proposta aqui.
Consultas registradas: V4C-Q002, V4C-Q020.

## T242:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T242 → T240 [complements]
Como combinar: Capturar base consistente com manifesto e cursor para iniciar a recuperação.
Interface: Estado, cursor e referências de artefatos.
Condição: Base passou por teste de restauração.
Aceite proposto: Snapshot não incorpora cursor posterior ao estado gravado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T242 → T241 [complements]
Como combinar: Reproduzir sufixo com processador compatível e sem repetir efeitos externos.
Interface: Eventos posteriores e versão de redução.
Condição: Convenção de último incluído ou próximo a aplicar é explícita.
Aceite proposto: Nenhum evento perdido ou aplicado duas vezes na fronteira.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S041. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checkpoint de transporte por partição não prova corte global entre streams.
- Snapshot corrompido com prefixo apagado pode impedir recuperação; registrar esse limite antes de reduzir retenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare recuperação completa, incluindo reconciliação, em vez de carregar bytes. A estratégia aumenta continuidade de sistemas com modelos pequenos, mas não cria memória cognitiva nem resolve ausência de eventos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T240, T241, T243

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S041 — Marten — Events Versioning

[https://martendb.io/events/versioning.html](https://martendb.io/events/versioning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evolução de schemas e upcasting permitem interpretar eventos históricos sem tratar mudança de representação como novo fato.

Limite: Mecanismos específicos do framework; conversão deve preservar semântica e não inventar informação histórica ausente.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T243 — Reconciliação de operações externas

**Nome canônico:** Reconciliação de operações externas  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T243  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** external operation reconciliation; reconciliação de efeitos incertos

## T243:C01 — conceito

Processo de comparar a intenção registrada de uma operação com o estado observado no sistema externo e resolver divergências sem presumir que ausência de resposta significa ausência de efeito. É essencial quando um timeout, queda ou resposta perdida deixa incerto se a operação foi concluída.

Como funciona:
- O controlador registra identidade e intenção antes de iniciar a operação.
- A tentativa produz resultado confirmado ou estado incerto, preservando a distinção.
- O reconciliador consulta recibos, status ou recursos externos e decide confirmar, repetir com segurança ou manter a pendência.

## T243:C02 — aplicacao

Quando usar:
- Criação de recursos, envio de mensagens, gravações remotas e outras mutações cuja resposta possa se perder após execução.

Quando não usar:
- Marcar automaticamente timeout como falha sem efeito, repetir com nova identidade ou inventar uma garantia de exatamente uma vez.

Implementação proposta:
- Proposta: registrar operation_id, destino, parâmetros relevantes, chave idempotente suportada e estado inicial.
- Persistir identificadores externos e recibos assim que disponíveis; separar attempted, confirmed, failed e uncertain.
- Para uncertain, consultar o provedor usando identidade confiável e respeitar atrasos de consistência.
- Repetir apenas quando o protocolo permitir deduplicação ou houver evidência suficiente de não execução.
- Quando não for possível concluir, preservar a incerteza para decisão explícita; compensação é outra operação, não um rollback universal.

Aplicação LAI proposta:
Proposta LAI: manter um ledger de operações externas e reconciliar pendências antes de retomar missões, permitindo auditoria do que foi tentado e do que foi confirmado.

## T243:C03 — riscos_validacao

Armadilhas:
- Busca por payload parecido pode confundir operações legítimas diferentes.
- Chaves idempotentes podem ter escopo e validade limitados.
- Uma leitura desatualizada pode sugerir falsamente que o recurso não existe.

Métricas sugeridas:
- Operações incertas; tempo até resolução; duplicações; divergências persistentes; confirmações com recibo; compensações necessárias.

Testes propostos:
- Simular conclusão externa seguida de perda da resposta e verificar confirmação sem duplicar.
- Simular leitura temporariamente desatualizada e evitar retry prematuro.
- Reutilizar chave com intenção diferente e exigir rejeição ou novo processo conforme contrato.
- Testar provedor sem consulta confiável e manter estado incerto.

## T243:C04 — perguntas_proveniencia

Pergunta: Qual é a diferença entre retry e reconciliação?
Resposta: Retry tenta executar novamente. Reconciliação primeiro determina a relação entre intenção e estado observado para escolher uma ação segura.

Pergunta: Sempre é possível resolver automaticamente?
Resposta: Não. Sem identidade, recibo ou consulta confiável, pode restar ambiguidade. O sistema deve reportá-la em vez de fabricar sucesso ou falha definitiva.

Pergunta: Não encontrei o objeto: posso repetir imediatamente?
Resposta: Somente se a leitura e o contrato sustentarem ausência conclusiva; com consistência eventual, pode ser cedo demais.

Pergunta: Compensação é igual a rollback?
Resposta: Não. É outra operação de domínio, possivelmente com efeitos observáveis e falhas próprias, que precisa de identidade e verificação.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T243:C05 — mecanismo_avancado

Reconciliação precisa distinguir efeito observado e efeito desta intenção. Encontrar um objeto parecido não prova que a tentativa incerta o criou; correlação por chave, ID ou recibo é mais forte. Uma consulta pode ainda refletir consistência eventual e retornar ausência temporária. A proposta usa estados confirmado, ausente com evidência suficiente e desconhecido, mantendo prazo e política de nova observação antes de decidir repetir ou compensar.

Condição de contorno:
Se o sistema externo não oferece identidade consultável nem leitura com garantias adequadas, alguns desfechos permanecem desconhecidos.

Contrato proposto:
- Entradas: Intenção, tentativa, chave externa, resultado incerto e contrato de consulta.
- Saídas: Conclusão fundamentada, nova observação ou ação de recuperação elegível.
- Estado: Recibos, consultas realizadas, versões e janela de convergência.
- Invariante: Ausência de resposta ou de leitura imediata não é tratada automaticamente como ausência de efeito.

Compromissos de projeto:
- Observar mais vezes reduz algumas incertezas e aumenta atraso e custo.
- Compensar pode corrigir efeito indesejado e criar outro efeito que também exige rastreabilidade.

## T243:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: perder a resposta de uma escrita e atrasar sua visibilidade na consulta; exigir estado desconhecido inicial e reconhecimento posterior, sem criar um segundo objeto.

Plano de avaliação proposto:
Comparar retry imediato e reconciliação sob resposta perdida, duplicatas e leitura atrasada. Medir efeitos duplicados, tempo até conclusão e casos corretamente mantidos como desconhecidos. Usar o contrato real de idempotência e retenção do serviço.

Comparações:
- T162 (complements): A chave idempotente ajuda reconhecer uma intenção, dentro de seu escopo e prazo.
- T228 (complements): A fila deve conservar estado incerto para não converter reconciliação em nova execução cega.

Afirmação rastreável:
Kubernetes descreve controllers que observam estado atual e agem para aproximá-lo do estado desejado.
Suporte: related; fontes: V2A-S024
Limite: A identificação de efeitos externos incertos é aplicação editorial desse princípio, complementada por contratos concretos de idempotência.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T243:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia efeito desta intenção de objeto parecido. A expansão organiza um protocolo de incerteza, escalona observações e define quando repetir, compensar ou manter pendência sem fabricar certeza.

Ledger de intenção
Registre o que se pretendia fazer, chave externa, parâmetros, envio e último resultado conhecido. A reconciliação consulta a identidade da operação e confronta o efeito observado com a intenção. Encontrar recurso com nome semelhante não basta; pode pertencer a outra tentativa, usuário ou ação legítima independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S025.

Ausência tem força variável
Uma leitura vazia pode significar operação não executada, processamento em andamento ou atraso de visibilidade. Use garantias do destino e sinais de status para decidir quando a ausência é suficiente. Se não houver consulta confiável, mantenha desconhecido e limite novas ações; disponibilidade não deve ser obtida por duplicação silenciosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S028.

Compensação é nova operação
Desfazer um efeito externo não é restaurar memória local. A compensação possui pré-condições, identidade e possibilidade de falha próprias. Um recurso pode ter sido usado ou modificado depois da operação original; reverter cegamente pode apagar trabalho válido. Planeje compensações por contrato e registre seu resultado separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V4C-S002.

USO AVANÇADO — Criação com timeout
Cenário: O agente solicita um ambiente e perde a resposta.
Estratégia: Consulte pelo identificador da intenção e aguarde visibilidade conforme contrato. Se confirmado, continue com o recurso existente; se ausente com evidência suficiente, repita usando identidade apropriada. Se a chave expirou e não há correlação confiável, não assuma que é seguro criar outro automaticamente.
Papel do modelo pequeno: 3–7B preenche pedido; 8–14B interpreta estados tipados; runtime decide repetição segura.
Aceite proposto: Proposta: nenhum recurso duplicado em falhas antes, durante e depois da confirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

USO AVANÇADO — Deploy ou publicação interrompida
Cenário: Estado local diz pendente, mas o destino pode ter avançado.
Estratégia: Leia versão efetiva e histórico de operação, compare com versão desejada e verifique saúde do resultado. Se houve mudança concorrente, suspenda compensação automática e reconcilie autoridade. Um rollout parcialmente aplicado exige tratamento por etapa, não só marcar o workflow como falho.
Papel do modelo pequeno: 15–30B analisa alternativas; controlador preserva identidades e regras de publicação.
Aceite proposto: Proposta: convergir para estado aceito ou pendência explícita, sem sobrescrever mudança concorrente legítima.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir estados confirmado, ausente e desconhecido definidos pelo adaptador, sem inferir efeito pelo texto.
8–14B: Diagnosticar divergências de parâmetros e necessidade de nova observação.
15–30B: Planejar compensação ou revisão de intenção em situações complexas, submetida a contratos e evidências.
Requisitos de treino/runtime: Identidade consultável, ledger persistente, garantias de leitura conhecidas e orçamento de observação.
Não aplicar quando: Não prometer exatamente uma vez quando o serviço não oferece deduplicação nem correlação suficiente.

## T243:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Ações manuais são incorporadas à representação do estado efetivo.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: O relato discute a ambiguidade de recursos existentes e a necessidade de identificar a operação que os criou.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: EC2 e UpCD apoiam mecanismos de identidade e reconciliação em contextos específicos. A aplicação genérica a agentes é proposta com limites explícitos.
Consultas registradas: V4C-Q001, V4C-Q002, V4C-Q019.

## T243:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T243 → T162 [complements]
Como combinar: Chave idempotente liga tentativas à mesma intenção e permite interpretar resultados repetidos.
Interface: Chave, payload e horizonte de retenção.
Condição: Destino garante a semântica documentada da chave.
Aceite proposto: Repetição após timeout não cria efeito adicional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T243 → T225 [complements]
Como combinar: Antes de liberar o executor reiniciado, resolver operações cujo desfecho ficou incerto.
Interface: Geração anterior, intenções pendentes e observações atuais.
Condição: Restart não apaga o ledger nem renova a identidade da ação.
Aceite proposto: Nova instância não repete automaticamente tudo após o último snapshot.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Consulta de estado atual e repetição de intenção histórica são operações distintas.
- Compensação pode falhar ou ser inadequada após mudança concorrente; manter seu próprio estado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare integridade de efeitos e tempo de resolução sob falhas reproduzíveis. A LLM ajuda a interpretar casos, mas certeza operacional depende das garantias do destino e do registro local.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T228, T220, T225, T241, T240

## Fontes primárias associadas

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S024 — Controllers

[https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Laços de controle com observação do estado atual e aproximação ao estado desejado.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S025 — Stripe API — Idempotent requests

[https://docs.stripe.com/api/idempotent_requests](https://docs.stripe.com/api/idempotent_requests)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: API v1 guarda resposta após início de execução, compara parâmetros e possui retenção finita; API v2 tem semântica distinta explicitada.

Limite: Exemplo concreto de contrato; não generalizar política de retenção ou tratamento de erros a toda API.

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

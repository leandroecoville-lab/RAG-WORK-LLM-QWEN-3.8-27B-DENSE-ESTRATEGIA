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

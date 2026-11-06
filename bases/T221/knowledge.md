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

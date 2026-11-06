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

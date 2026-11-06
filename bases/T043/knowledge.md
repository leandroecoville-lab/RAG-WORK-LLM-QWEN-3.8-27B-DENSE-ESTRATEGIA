# T043 — Context Compaction

**Nome canônico:** Context Compaction  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T043  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compactação de contexto

## T043:C01 — conceito

Reorganiza um histórico extenso em uma representação operacional menor para continuar a execução. Pode combinar síntese, poda e externalização. Uma boa compactação conserva objetivo, decisões vigentes, pendências e referências; não deve fingir que todos os detalhes sobrevivem.

Como funciona:
- Capturar um ponto consistente do histórico e estado.
- Produzir pacote compacto com campos obrigatórios.
- Persistir originais e substituir a entrada ativa somente após validação.

## T043:C02 — aplicacao

Quando usar:
- Sessões que se aproximam do limite de contexto.
- Retomada de missões longas em nova chamada ou processo.

Quando não usar:
- Não usar compactação como substituto de log completo quando a tarefa exige auditabilidade.

Implementação proposta:
- Proposta: incluir versão, objetivo, concluído, pendente, riscos e evidências.
- Marcar explicitamente o que não foi lido ou foi truncado.
- Manter a compactação anterior até concluir a gravação da nova e verificar invariantes.

Aplicação LAI proposta:
Proposta LAI: gerar checkpoints compactos da Helena acompanhados dos eventos que os originaram; retomada exige ler esse estado antes de continuar.

## T043:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode converter suspeita em conclusão.
- IDs, versões ou proibições antigas podem desaparecer durante a reescrita.

Métricas sugeridas:
- Redução de tokens e retenção de campos críticos.
- Taxa de retomada correta após vários ciclos.

Testes propostos:
- Compactar um histórico com correção de decisão e exigir a versão vigente.
- Interromper a gravação e verificar disponibilidade do checkpoint anterior.

## T043:C04 — perguntas_proveniencia

Pergunta: Compactação é uma memória permanente?
Resposta: Não necessariamente. Ela é uma representação reduzida; persistência e recuperação precisam ser implementadas.

Pergunta: Posso confiar em uma compactação sem referências?
Resposta: Ela serve como pista, mas não como prova suficiente de execução ou resultado.

Pergunta: Uma compactação precisa ser textual?
Resposta: Não obrigatoriamente. Pode combinar campos estruturados, trechos literais e referências; a representação precisa ser consumível pelo runtime.

Pergunta: Como recuperar detalhe omitido?
Resposta: Use referências ao prefixo original e reabra o trecho necessário. A síntese deve orientar a busca, não substituir a evidência em casos ambíguos.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T043:C05 — mecanismo_avancado

Uma compactação pode ser tratada como uma nova projeção de um prefixo fechado do histórico. Ela deve declarar até qual evento cobre e quais mensagens posteriores permanecem literais; sem essa fronteira, o sistema pode duplicar fatos ou perder eventos que chegaram durante a síntese. A troca do contexto ativo deve publicar a projeção completa somente depois de verificar referências, pendências e cobertura.

Condição de contorno:
Se o histórico continua recebendo escritas sem uma fronteira identificável, não é possível saber com segurança o que a nova compactação já incorporou.

Contrato proposto:
- Entradas: Prefixo identificado, estado vigente, política de retenção e eventos posteriores separados.
- Saídas: Pacote compacto com marcador de cobertura, referências e incertezas preservadas.
- Estado: Versão anterior, fonte original, configuração do compactador e geração em preparação.
- Invariante: Toda informação posterior à fronteira continua disponível até ser incorporada explicitamente em outra revisão.

Compromissos de projeto:
- Compactar menos vezes preserva mais detalhes, mas pode aproximar a chamada do limite.
- Compactações frequentes reduzem pressão da janela e acumulam erros de síntese e custo de processamento.

## T043:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma correção durante a geração do resumo e publicar a compactação anterior a ela. A montagem seguinte deve incluir a correção literal, evitando que a síntese antiga prevaleça.

Plano de avaliação proposto:
Avaliação proposta: comparar compactação por tamanho e por fronteiras de tarefa com várias rodadas. Medir perda de correções, duplicação, cobertura de eventos e retomada; incluir custos de geração, releitura das fontes e invalidação de cache.

Comparações:
- T004 (complements): Resumos encadeados podem compor compactação, mas exigem controle de cobertura e propagação de erros.
- T016 (distinct_from): Truncar ou limpar um resultado remove conteúdo; não produz necessariamente uma representação resumida dele.

Afirmação rastreável:
A Anthropic descreve compactação por síntese do histórico e diferencia essa técnica de notas estruturadas e limpeza de resultados de ferramentas.
Suporte: direct; fontes: A-S006, V3A-S008
Limite: O protocolo de fronteira e publicação aqui descrito é uma proposta editorial; não é uma garantia de todo produto de compactação.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T043:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegeu commit de compactação. Aqui o resumo é um contrato de retomada adaptado ao próximo consumidor e à fase da tarefa.

Projeto e decomposição
Defina campos mínimos por tarefa: objetivo vigente, decisões confirmadas, evidências, pendências e próximos testes. A compactação deve produzir um estado utilizável, não apenas narrativa da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Controle adaptativo
Teste o resumo com um leitor diferente do autor antes de usá-lo em fluxos críticos. Se o consumidor não consegue identificar próximo passo e condições de parada, reabrir conteúdo específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Validação contrafactual
Compare retomada pelo mesmo modelo e por outro porte. Meça ações corretas após a fronteira, fatos reinterpretados e leituras adicionais; resumo que só seu autor entende é contrato frágil. Unidade de avaliação: ponto de retomada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Troca de modelo por custo
Cenário: Fronteira inicia e modelo local continua.
Estratégia: Gerar pacote com decisões explícitas e exemplos de formato, retirar pressupostos tácitos e validar uma etapa de retomada.
Papel do modelo pequeno: 3–7B executa subtarefa; 15–30B resume integração.
Aceite proposto: Consumidor deve reproduzir restrições sem inventar decisões omitidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Sessão longa de desenvolvimento
Cenário: Histórico contém tentativas descartadas.
Estratégia: Guardar tentativas rejeitadas com motivo verificável, para que nova sessão não repita caminho inútil. Separar falha observada de hipótese não testada.
Papel do modelo pequeno: 8–14B retoma diagnóstico.
Aceite proposto: Medir repetição de tentativas já refutadas e preservação do teste pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de estado estruturado com próximo passo delimitado.
8–14B: Autor e leitor de pacote de retomada por módulo.
15–30B: Integrador de decisões cruzadas e conflitos ainda abertos.
Requisitos de treino/runtime: Schema de retomada, revisão-base e teste de leitura por consumidor; preservar artefatos independentes do resumo.
Não aplicar quando: Não é possível representar obrigações essenciais e fontes no orçamento disponível.

## T043:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Compactação implementada no produto é explicitada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T043:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T043 → T211 [feeds]
Como combinar: Publicar pacote de retomada como handoff.
Interface: Objetivo, decisões, testes, artefatos e revisão.
Condição: Pacote corresponder à fronteira confirmada.
Aceite proposto: Retomar em sessão limpa sem acesso à conversa anterior.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T043 → T055 [complements]
Como combinar: Carregar procedimento específico para a fase seguinte.
Interface: Procedimento versionado e pré-condições.
Condição: Resumo não substituir contrato de execução.
Aceite proposto: Verificar que instrução operacional completa foi aberta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não condensar resultados de ferramenta incertos como sucesso.
- Não confundir reflexão interna com registro factual de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade após troca de consumidor; compactação não preserva automaticamente capacidade de planejamento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T006, T021, T060

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

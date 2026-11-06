# T021 — Context Compression On-the-Fly

**Nome canônico:** Context Compression On-the-Fly  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão dinâmica em execução

## T021:C01 — conceito

Aplica compressão durante a execução, quando novos dados ou crescimento do histórico ultrapassam um orçamento. O que a diferencia é o momento e a adaptação ao estado atual; não é uma nova classe universal de algoritmo de compressão.

Como funciona:
- Medir o contexto antes de cada chamada relevante.
- Acionar seleção ou síntese quando um limiar operacional é atingido.
- Validar o novo pacote e conservar a versão anterior recuperável.

Nota de nomenclatura: Variante operacional da família Context Compression; mantida para preservar o inventário.

## T021:C02 — aplicacao

Quando usar:
- Agentes de muitas etapas com volume imprevisível de ferramentas.
- Sessões cuja pergunta atual muda o que precisa permanecer ativo.

Quando não usar:
- Evitar compressor pesado por rodada quando o custo supera a economia de inferência.

Implementação proposta:
- Proposta: usar um limiar de alerta e outro de bloqueio.
- Comprimir blocos concluídos, preservando objetivo, pendências e vínculos de ferramentas.
- Registrar tamanho antes/depois, origem e versão para explicar decisões futuras.

Aplicação LAI proposta:
Proposta LAI: colocar o controle no runtime da Helena, com regras de orçamento, em vez de depender apenas de o modelo perceber que está ficando sem contexto.

## T021:C03 — riscos_validacao

Armadilhas:
- Recompressões sucessivas acumulam erro.
- Acionar compressão somente após estourar a janela pode impedir produzir a própria síntese.

Métricas sugeridas:
- Frequência de compactação e tempo gasto nela.
- Retenção de restrições ao longo de múltiplos ciclos.

Testes propostos:
- Executar histórico sintético longo com mudanças de objetivo e checar o estado vigente.
- Simular falha durante compressão e manter disponível o checkpoint anterior.

## T021:C04 — perguntas_proveniencia

Pergunta: Preciso retreinar o modelo para comprimir em tempo real?
Resposta: Não para seleção e síntese textual; métodos latentes específicos podem exigir treinamento.

Pergunta: Comprimir a cada turno é ideal?
Resposta: Não. A frequência deve equilibrar custo, volume e risco de perda acumulada.

Pergunta: A margem deve ser uma porcentagem fixa?
Resposta: Não necessariamente. Resultados de ferramentas e saídas variam em tamanho; uma reserva baseada nas próximas etapas pode ser mais informativa.

Pergunta: O que fazer se a compactação falhar?
Resposta: Preserve a versão anterior e registre a falha. Não avance com um resumo parcial como se tivesse conservado os requisitos indispensáveis.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T021:C05 — mecanismo_avancado

Compressão durante execução é um problema de controle com custo de intervenção. Um gatilho próximo demais do limite pode não deixar espaço para produzir a nova representação; acionamento frequente também perde tempo e cache. A política deve considerar tamanho provável do próximo resultado, margem para saída e uma condição de rearme, evitando compactar continuamente em torno do mesmo limiar.

Condição de contorno:
Se o próximo artefato indispensável exceder o orçamento disponível, compressão oportunista do histórico pode não resolver a incompatibilidade da tarefa.

Contrato proposto:
- Entradas: Contexto atual, próxima etapa, reservas e regiões protegidas.
- Saídas: Nova representação validada e manifesto do que foi substituído.
- Estado: Versões antes e depois, último gatilho e referências aos originais.
- Invariante: A nova versão só substitui a anterior após preservar o estado operacional necessário à próxima ação.

Compromissos de projeto:
- Gatilhos antecipados deixam margem, mas podem comprimir conteúdo que ainda seria útil.
- Reduções maiores amortizam intervenção, ao custo de retirar mais informação de uma vez.

## T021:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: simular crescimento abrupto por saída de ferramenta e, depois, pequenas oscilações de tamanho. Verificar reserva suficiente e ausência de repetidas compressões sem trabalho útil entre elas.

Plano de avaliação proposto:
Avaliação proposta: comparar limiar simples e política com margem e rearme sobre sequências equivalentes. Medir intervenções, tokens recuperados, perda de fatos, invalidações de cache e tempo total até concluir a tarefa.

Comparações:
- T006 (specializes): É uma política de aplicação temporal dos mecanismos de compressão.
- T212 (complements): Auto-Compact por gatilho pode implementar parte desta política, com comportamento próprio do executor.

Afirmação rastreável:
A documentação de context editing permite condicionar a limpeza a um ganho mínimo de tokens para justificar a invalidação de cache.
Suporte: direct; fontes: V3A-S008
Limite: O desenho de controlador aqui proposto é mais geral que as opções de um provedor específico.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T021:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 usou histerese. Aqui a decisão de comprimir considera previsão de crescimento e custo de interromper a execução.

Projeto e decomposição
Estime tamanho dos próximos resultados antes da chamada. Compressão preventiva pode evitar estouro, mas previsão pessimista demais desperdiça chamadas e destrói detalhes cedo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

Controle adaptativo
Escolha momento de compactar em fronteira estável: após confirmar resultado e antes de abrir nova fase. Se chegam eventos concorrentes, preservar fila posterior à revisão usada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

Validação contrafactual
Compare gatilho somente por ocupação e gatilho por crescimento previsto. Meça estouros, compressões inúteis e tempo parado. Unidade de avaliação: trajetória com crescimento. Teste dois resultados de ferramenta com tamanhos medianos iguais e caudas diferentes. A previsão deve distinguir risco de estouro, não apenas média histórica. Registre compactações acionadas sem necessidade e compactações tardias que interrompem a tarefa; ambos os erros precisam entrar na escolha do gatilho e da margem de reserva.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

USO AVANÇADO — Agente de investigação
Cenário: Uma próxima busca pode retornar material enorme.
Estratégia: Projetar tamanho por ferramenta, reservar margem e reduzir apenas blocos recuperáveis; ajustar previsão com uso observado.
Papel do modelo pequeno: 3–7B estima categoria; código contabiliza tokens.
Aceite proposto: Não exceder limite em cenários de cauda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

USO AVANÇADO — Sessão interativa
Cenário: Usuário precisa resposta com baixa demora.
Estratégia: Agendar compressão entre etapas, mantendo um pacote mínimo pronto para interrupções e novas instruções.
Papel do modelo pequeno: 8–14B produz estado resumido.
Aceite proposto: Nova instrução deve ser preservada sem aguardar resumo obsoleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de crescimento provável com contabilidade determinística externa.
8–14B: Resumidor preventivo de blocos encerrados.
15–30B: Controlador de alternativas entre resumir, expandir janela e decompor tarefa.
Requisitos de treino/runtime: Telemetria por ferramenta e política de revisão; medir custos no hardware e protocolo reais.
Não aplicar quando: Não há conteúdo dispensável e a próxima operação exige mais contexto que o limite útil.

## T021:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q024.

## T021:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T021 → T222 [requires]
Como combinar: Observar consumo e previsão por operação.
Interface: Ocupação, margem, tipo de ferramenta e quantis de resultado.
Condição: Previsão recalibrada com tráfego real.
Aceite proposto: Testar resultados maiores que o esperado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, V3A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T021 → T210 [alternative]
Como combinar: Rotacionar sessão quando compactação não preservar requisitos.
Interface: Handoff, revisão e pendências.
Condição: Novo contexto receber contrato completo.
Aceite proposto: Comparar continuidade e custo da rotação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, V3A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não comprimir repetidamente o mesmo texto sem ganho.
- Registrar divergência entre previsão e tamanho real.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar execução contínua sob pressão de contexto; evitar confundir menos estouros com respostas melhores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T043, T168

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

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

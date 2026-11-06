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

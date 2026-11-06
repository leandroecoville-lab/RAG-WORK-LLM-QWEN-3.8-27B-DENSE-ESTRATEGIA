# T176 — Token-Aware Planning

**Nome canônico:** Token-Aware Planning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T176  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejamento consciente de tokens

## T176:C01 — conceito

Planejamento que considera custo e espaço de contexto de cada etapa, além das dependências funcionais. O plano estima entradas, saídas, ferramentas e verificações e pode decompor trabalho quando necessário. Trata-se de política de orquestração; não existe uma fórmula universal que preveja todo consumo.

Como funciona:
- Estimar tokens e número de chamadas de cada etapa planejada.
- Reservar espaço para evidências, resultado e verificação.
- Atualizar estimativas com consumo observado antes de liberar próximas etapas.

## T176:C02 — aplicacao

Quando usar:
- Missões extensas com RAG, várias ferramentas ou subagentes.
- Contexto e custo são restrições reais do fluxo.

Quando não usar:
- Escolher o plano mais curto em tokens mesmo quando perde evidência ou qualidade necessária.

Implementação proposta:
- Manter estimativa central e margem de incerteza por tipo de etapa.
- Preferir referências a artefatos grandes e recuperar detalhes sob demanda.
- Planejar checkpoint antes de regiões com alto risco de expansão.

Aplicação LAI proposta:
Proposta: o planejador da Helena incluir orçamento por etapa, reservando capacidade para checagens e retomada em vez de consumir tudo no planejamento.

## T176:C03 — riscos_validacao

Armadilhas:
- Saída de ferramenta pode ser muito maior que o previsto.
- Decomposição excessiva repete instruções em várias chamadas e aumenta custo.

Métricas sugeridas:
- Erro de previsão de tokens por etapa.
- Taxa de conclusão dentro do orçamento e custo por tarefa aceita.

Testes propostos:
- Executar missões com documentos de tamanhos variados e comparar previsão versus uso.
- Fazer uma etapa exceder previsão e verificar replanejamento sem apagar restrições.

## T176:C04 — perguntas_proveniencia

Pergunta: Token-aware significa sempre usar prompt menor?
Resposta: Não. Um trecho maior pode evitar várias chamadas e reduzir custo total.

Pergunta: A estimativa é garantia?
Resposta: Não. Precisa de margem e revisão durante a execução.

Pergunta: Dividir sempre em tarefas menores economiza tokens?
Resposta: Não. Instruções repetidas, resumos e integração podem superar a economia de cada chamada.

Pergunta: Como planejar uma saída de ferramenta sem tamanho conhecido?
Resposta: Usar distribuição observada ou intervalo conservador e definir previamente como selecionar, paginar ou referenciar o excedente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T176:C05 — mecanismo_avancado

Planejamento sensível a tokens deve modelar crescimento de evidência, não apenas tamanho do prompt inicial. Uma etapa de busca pode expandir candidatos e tornar o passo seguinte inviável; uma etapa de síntese pode reduzir espaço e perder detalhes necessários à verificação. Estimativas por intervalo permitem planejar contingências: extrair por referência, dividir subtarefas ou reservar uma rodada de recuperação, mantendo custo de coordenação no orçamento.

Condição de contorno:
Quando o tamanho das observações é desconhecido, um plano com estimativas pontuais otimistas pode falhar mesmo sem nenhuma resposta excepcional.

Contrato proposto:
- Entradas: DAG de trabalho, intervalos de entrada/saída, janela e orçamento acumulado.
- Saídas: Plano viável, reservas e alternativas para etapas que ultrapassem a estimativa.
- Estado: Consumo real por tipo de operação e dependências informacionais.
- Invariante: Uma etapa não elimina informações exigidas por seu próprio critério de validação.

Compromissos de projeto:
- Dividir o trabalho reduz contexto por chamada e aumenta mensagens de integração.
- Carregar documentos completos evita novas buscas e pode expulsar evidência mais relevante.

## T176:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: uma pesquisa retorna muitos candidatos e a verificação exige trechos originais; exigir seleção rastreável e preservação de referências antes de continuar.

Plano de avaliação proposto:
Comparar plano sem custo, plano por estimativa média e plano com contingências. Controlar tarefas e ferramentas. Medir estouros, replanejamentos, perda de evidência e custo por conclusão; escolher a política pela variabilidade observada.

Comparações:
- T152 (complements): Alocação implementa as reservas que o plano estima.
- T143 (specializes): Acrescenta restrições de contexto e consumo ao planejamento antecipado.

Afirmação rastreável:
ReWOO reduz repetição de contexto ao separar planejamento e observações em sua arquitetura.
Suporte: direct; fontes: V3C-S012
Limite: Previsões por intervalos e contingências desta ficha são propostas; a economia do estudo não é transferida para LAI.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T176:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 estimava crescimento de evidência e contingências. A nova camada planeja a distribuição informacional entre chamadas, incluindo custo de integrar resultados e a reserva necessária para verificar o que foi produzido.

Grafo informacional
Para cada etapa, declare quais fatos precisa receber e quais deve preservar para seus sucessores. Uma saída curta pode omitir o detalhe necessário ao teste seguinte. Planeje interfaces por campos e referências, não apenas por número de tokens; a compressão é aceitável quando a informação excluída permanece recuperável no momento certo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S012, V4C-S013.

Custo de coordenação
Dividir uma tarefa reduz contexto local e acrescenta instruções repetidas, chamadas, resultados intermediários e síntese. Estime esse custo antes de criar especialistas. Quando a comunicação domina o trabalho útil, mantenha etapas juntas ou use funções determinísticas para filtrar dados, em vez de multiplicar agentes pequenos por princípio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Plano com gatilhos
Defina ações quando a observação ultrapassar a previsão: paginação, seleção de campos, nova subtarefa ou interrupção para handoff. O gatilho deve ocorrer antes de consumir a reserva de validação. Replanejamento altera somente etapas ainda abertas; artefatos já aceitos permanecem referenciados e podem ser invalidados apenas por mudança de requisito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V3C-S022.

USO AVANÇADO — Refatoração em repositório grande
Cenário: O contexto completo não cabe de forma útil no modelo local.
Estratégia: Comece com mapa de símbolos e dependências, leia trechos necessários e produza patch por unidade. Reserve leitura de consumidores e execução de testes antes de integrar. Se um tipo comum mudar, reabra o planejamento dos módulos afetados em vez de continuar com resumos antigos.
Papel do modelo pequeno: 3–7B aplica mudanças locais; 8–14B seleciona contexto; 15–30B integra contratos.
Aceite proposto: Proposta: nenhuma mudança aceita sem contexto de validação e menor consumo por tarefa concluída.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S012.

USO AVANÇADO — Síntese de fontes extensas
Cenário: Há documentos suficientes para exceder várias janelas.
Estratégia: Extraia tabelas de alegação, trecho e limite por fonte. Planeje a síntese sobre essas tabelas e reserve consultas pontuais aos originais para conflitos. Não conte apenas tokens de síntese: some extração, revisões e recuperações adicionais para comparar arquiteturas.
Papel do modelo pequeno: 8–14B realiza extração padronizada; 15–30B compara alegações apoiadas.
Aceite proposto: Proposta: cobertura de evidência e custo completo frente à leitura monolítica quando ela for viável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Nós de transformação estreitos, com saída curta e critério determinístico.
8–14B: Seleção e extração de contexto com referências que permitam recuperação posterior.
15–30B: Planejamento de dependências informacionais e integração de exceções sem carregar todos os intermediários.
Requisitos de treino/runtime: Contagem com tokenizer real, estimativas por etapa e medição do custo de reconsulta e integração.
Não aplicar quando: Não chamar de economia uma compressão que elimina a evidência necessária para verificar o resultado.

## T176:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: ReWOO e relatos de harness sustentam separação de fases; as estimativas e critérios propostos não foram executados nem tratados como benchmark.
Consultas registradas: V4C-Q009, V4C-Q014, V4C-Q027.

## T176:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T176 → T152 [feeds]
Como combinar: Converter previsão do plano em reservas de entrada, saída e validação por etapa.
Interface: Estimativas, variabilidade e prioridade informacional.
Condição: Reservas cabem na janela e no orçamento acumulado.
Aceite proposto: Estouro de uma ferramenta dispara contingência antes de invalidar a chamada seguinte.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T176 → T214 [complements]
Como combinar: Projetar campos de ferramentas conforme a necessidade da próxima etapa.
Interface: Schema da resposta e campos requeridos pelo contrato.
Condição: Dados omitidos permanecem recuperáveis por referência.
Aceite proposto: Poda não remove identificação, erro ou campo necessário ao teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mais trabalhadores podem aumentar tokens totais apesar de reduzir janela individual.
- Não iniciar síntese final sem reserva para conferir fontes e produzir estado de cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare arquitetura pequena e modelo de fronteira com custo de todas as fases e taxa de conclusão válida. Planejamento pode compensar contexto limitado em tarefas decomponíveis, sem garantir paridade em sínteses indivisíveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T152, T168

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S012 — ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

[https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre planejamento e observações reduz reenvio de contexto em trajetórias cuja estrutura pode ser antecipada.

Limite: Não elimina dependência semântica de resultados imprevistos nem comprova ganhos no domínio LAI.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

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

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

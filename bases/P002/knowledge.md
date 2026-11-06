# P002 — Context Manager

**Nome canônico:** Context Manager  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P002  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gestor proposto de contexto ativo

## P002:C01 — conceito

Context Manager é um nome editorial proposto para gerir o ciclo de vida da janela ativa: reservar tokens, acompanhar ocupação e decidir quais unidades entram, permanecem ou saem. O estado persistente da tarefa e o histórico arquivado seriam separados da mensagem enviada ao modelo. A proposta não corresponde a produto LAI verificado nem define uma nomenclatura universal.

Como funciona:
- Calcular limite útil a partir da capacidade do modelo, da reserva de saída e das instruções obrigatórias.
- Atribuir prioridades a objetivos, decisões vigentes, histórico recente e resultados recuperáveis, com cotas explícitas.
- Aplicar descarte FIFO a unidades elegíveis ou compactar segmentos antigos, preservando pares de chamada e resultado.

## P002:C02 — aplicacao

Quando usar:
- Sessões longas ou tarefas com resultados volumosos que precisam continuar sob um orçamento finito.

Quando não usar:
- Para apagar evidências de origem ou assumir que um resumo conserva integralmente o histórico.

Implementação proposta:
- Proposta: manter um ledger de ocupação por bloco com versão, custo estimado, prioridade e referência externa.
- Recontar tokens após montar a requisição e após trocar de modelo; reservas devem considerar resultados ainda esperados.
- Se até o conjunto obrigatório exceder o limite, reduzir a unidade de trabalho ou trocar a estratégia de recuperação; não prometer preservação impossível.

Aplicação LAI proposta:
Proposta LAI: controlar ocupação durante a execução e solicitar ao P001 uma nova montagem; persistência e política de retenção continuam sob contratos específicos de memória.

## P002:C03 — riscos_validacao

Armadilhas:
- Marcar tudo como obrigatório elimina qualquer capacidade real de gestão.
- Contagens aproximadas e cabeçalhos de ferramentas podem produzir estouro mesmo quando o texto visível parece caber.

Métricas sugeridas:
- Margem restante, estouros de limite, quantidade de recompressões e recuperação correta de obrigações antigas.

Testes propostos:
- Aceite proposto: gerar sequências acima do limite e verificar orçamento final e integridade dos turnos de ferramenta.
- Trocar para um modelo com janela menor e testar uma obrigação antiga fixada; a política deve explicitar o ajuste necessário.

## P002:C04 — perguntas_proveniencia

Pergunta: Uma mensagem fixada cabe sempre?
Resposta: Não. Fixação expressa prioridade, mas o limite físico permanece; conjuntos obrigatórios excessivos exigem replanejamento.

Pergunta: Quando medir tokens novamente?
Resposta: Depois da montagem final e sempre que mensagens, ferramentas, modelo ou reserva de saída forem alterados.

Pergunta: Persistir histórico resolve perda de contexto?
Resposta: Não sozinho. O próximo turno precisa receber a revisão e as informações corretas.

Pergunta: Qual condição impede sobrescrever uma correção?
Resposta: Confirmar a transformação contra a revisão de origem e reconciliar alterações posteriores antes do commit.

Escopo das fontes:
Fontes sustentam redução do histórico e contagem; ledger, fronteiras e testes são desenho proposto.

## P002:C05 — mecanismo_avancado

Context Manager é proposto como dono do ciclo de vida do contexto de uma sessão. Uma operação de compactação deve ler uma revisão, produzir uma candidata e confirmar somente se o estado de origem continuar compatível. Mensagens novas durante a compactação não podem desaparecer. O manager também precisa diferenciar objetivo vigente, decisões encerradas, pendências e referências externas, pois persistir todas as mensagens não garante que o próximo turno receba as informações certas.

Condição de contorno:
Uma sessão pode envolver atualizações concorrentes e resultados tardios de ferramentas. A ordem de chegada não representa necessariamente a ordem lógica das decisões.

Contrato proposto:
- Entradas: Identificador de sessão, revisão esperada, nova observação, objetivo e política de retenção do contexto.
- Saídas: Nova revisão confirmada, conflito explícito ou contexto preparado para a próxima etapa.
- Estado: Histórico de revisões, resumo ativo, referências de evidência e operações de compactação ainda pendentes.
- Invariante: Toda compactação deve preservar mensagens posteriores ao snapshot ou ser rejeitada por conflito de revisão.

Compromissos de projeto:
- Controle por revisão pode exigir recomputação após conflitos, porém evita sobrescrita silenciosa de fatos recentes.
- Reter histórico completo facilita auditoria, mas a janela ativa ainda precisa de limites e política de seleção.

## P002:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: iniciar compactação na revisão n, anexar nova instrução em n+1 e tentar confirmar o resumo antigo; exigir reconciliação ou rejeição, preservando a instrução recente.

Plano de avaliação proposto:
Comparar truncamento simples e gestão por revisão em conversas com correções, cancelamentos e resultados tardios. Medir perda de requisitos, conflitos, custo de compactação e continuidade após reinício. Não contar resumo bem formado como prova de preservação.

Comparações:
- T043 (complements): Compactação é uma operação do ciclo de vida.
- T154 (complements): Gestão de múltiplos turnos fornece eventos e estado da conversa.

Afirmação rastreável:
Checkpointers persistem estado de uma thread; stores mantêm dados que podem atravessar threads.
Suporte: related; fontes: V3D-S016
Limite: A distinção documental inspira o escopo, mas não implementa o controle de revisão proposto.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P002:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cuidou de revisão e ocupação. Aqui Context Manager é proposto como escalonador de orçamento entre sessões e fases.

Projeto e decomposição
Defina limite útil por modelo e condição de carga, preservando reserva de saída. Concorrência pode reduzir contexto viável por sessão mesmo quando a janela nominal permanece igual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006, V4A-S015.

Controle adaptativo
Escolha entre adiar, compactar, dividir tarefa e trocar consumidor. Cada opção tem custo e risco próprios; o controlador não deve compactar automaticamente tudo que ultrapassa um limiar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006, V4A-S015.

Validação contrafactual
Compare política fixa e política por fase sob carga variável. Meça estouros, latência de fila, qualidade após redução e sessões prejudicadas por outras; eficiência média não deve esconder starvation. Unidade de avaliação: sessão sob carga.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006, V4A-S015.

USO AVANÇADO — Servidor com vários agentes
Cenário: Sessões longas disputam memória.
Estratégia: Separar filas por necessidade, limitar trabalho ativo e reduzir contexto apenas onde requisitos permitem. Recontar após qualquer mudança de modelo.
Papel do modelo pequeno: 3–7B tarefas curtas; 15–30B fila de integração.
Aceite proposto: Nenhuma sessão pode exceder recursos ou perder obrigação silenciosamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006, V4A-S015.

USO AVANÇADO — Tarefa que cresce
Cenário: Nova evidência torna pacote maior que a janela.
Estratégia: Estimar expansão, escolher decomposição ou compactação de fase concluída e manter lacuna explícita quando conjunto obrigatório não couber.
Papel do modelo pequeno: 8–14B produz proposta de redução.
Aceite proposto: Redução só é aceita se campos obrigatórios permanecerem resolvíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006, V4A-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de tarefas pequenas com limite e saída previsíveis.
8–14B: Leitor de fases moderadas com retomada por pacote estruturado.
15–30B: Integrador reservado para fases que exigem relações mais amplas.
Requisitos de treino/runtime: Telemetria de tokens, memória, filas e perfil de tarefa; decisões de limite devem ser aplicadas por código.
Não aplicar quando: A aplicação exige que todas as sessões recebam contexto máximo simultaneamente sem recursos correspondentes.

## P002:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Gestão de janela inspira o componente proposto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q011.

## P002:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P002 → T222 [requires]
Como combinar: Receber ocupação e crescimento previsto.
Interface: Tokens atuais, reserva, próxima operação e quantis.
Condição: Contagem refletir protocolo real.
Aceite proposto: Injetar resultado volumoso e verificar prevenção de estouro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P002 → T043 [complements]
Como combinar: Compactar fase encerrada com contrato de retomada.
Interface: Revisão, fronteira e obrigações ativas.
Condição: Resumo preservar estado necessário.
Aceite proposto: Retomar em leitor menor e verificar condições do próximo passo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P002 → P001 [feeds]
Como combinar: Fornecer orçamento útil para montagem.
Interface: Modelo, cotas, prazo e decisão de insuficiência.
Condição: Builder respeitar conjunto obrigatório.
Aceite proposto: Solicitar pacote impossível e exigir replanejamento explícito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não descontar tokens cacheados da janela.
- Não trocar modelo sem recalcular tokenizer, contexto e compatibilidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade por sessão sob carga igual; política eficiente não torna modelo pequeno equivalente em toda tarefa.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T043, T050, T210, T222, P001, P005

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

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S015 — Context caching overview

[https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caching implícito e explícito, metadados de uso e duração; recurso disponível.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

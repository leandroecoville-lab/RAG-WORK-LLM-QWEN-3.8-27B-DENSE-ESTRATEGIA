# T003 — Sliding Window de contexto — incluindo descarte FIFO

**Nome canônico:** Janela deslizante do histórico com descarte FIFO  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T003  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Sliding Window de contexto; janela deslizante de histórico; descarte FIFO de contexto; histórico recente por tokens

## T003:C01 — conceito

Sliding Window de contexto mantém uma porção recente do histórico na entrada ativa do modelo. O descarte FIFO remove primeiro as unidades mais antigas elegíveis. Essa política opera antes da inferência; sliding-window attention limita conexões dentro do modelo e não é equivalente. Arquivar mensagens retiradas permite recuperá-las posteriormente sem consumir a janela em todas as chamadas.

Como funciona:
- Calcular orçamento disponível após reservar instruções fixas, resposta e resultados de ferramentas esperados.
- Ordenar unidades descartáveis por chegada e retirar as mais antigas até caber; uma unidade pode ser um turno completo ou um par chamada/resultado.
- Preservar fora da fila removível objetivos vigentes, decisões atuais e operações pendentes, com referências ao histórico original.

## T003:C02 — aplicacao

Quando usar:
- Conversas longas em que a maior parte do contexto relevante é recente e o histórico completo permanece recuperável.

Quando não usar:
- Como única memória para contratos, requisitos antigos ainda válidos ou fatos cuja importância não acompanha a idade.

Implementação proposta:
- Proposta: separar estado persistente da missão, histórico integral e janela enviada; contar tokens com o tokenizer do modelo escolhido.
- Definir FIFO por sequência de registro, sem presumir que a data mencionada no conteúdo corresponde à ordem de chegada.
- Se a mensagem mais recente sozinha exceder o orçamento, extrair trechos ou resumir com proveniência; não quebrar arbitrariamente o protocolo de ferramentas.

Aplicação LAI proposta:
Proposta LAI: manter objetivo e decisões em estado durável, usar FIFO apenas na área de histórico recente e registrar o intervalo arquivado em cada avanço da janela.

## T003:C03 — riscos_validacao

Armadilhas:
- FIFO não avalia relevância: uma restrição crítica antiga pode desaparecer.
- Cortar somente uma metade de uma interação com ferramenta produz histórico inválido ou interpretação incompleta.

Métricas sugeridas:
- Tokens ativos, quantidade de unidades removidas e proporção de perguntas históricas respondidas com evidência correta.

Testes propostos:
- Teste proposto: ultrapassar o limite com dez turnos e verificar ordem FIFO, preservação de pares e orçamento final.
- Introduzir uma obrigação antiga ainda vigente e exigir sua recuperação antes de uma ação incompatível.

## T003:C04 — perguntas_proveniencia

Pergunta: FIFO apaga automaticamente a memória persistente?
Resposta: Não. Nesta proposta ele remove a cópia do contexto ativo; retenção ou exclusão do arquivo histórico pertence a outra política.

Pergunta: Posso descartar uma tool call antiga mantendo seu resultado recente?
Resposta: Somente se o protocolo permitir uma representação independente. O padrão recomendado mantém chamada e resultado como unidade indivisível.

Pergunta: Arquivar torna o descarte sem perdas?
Resposta: Preserva o original no armazenamento, mas ainda pode falhar a recuperação no momento necessário. Perda operacional e perda física são propriedades diferentes.

Pergunta: E quando todos os blocos restantes forem obrigatórios?
Resposta: O montador deve declarar orçamento insuficiente e mudar a estratégia: reduzir tarefa, buscar outra representação válida ou usar capacidade compatível.

Escopo das fontes:
A-S003 fundamenta gestão e redução do histórico; A-S006 fundamenta engenharia do contexto. Proteções de estado, definição de FIFO e testes são escolhas editoriais propostas.

## T003:C05 — mecanismo_avancado

A unidade segura de descarte pode ser maior que uma mensagem: uma chamada e seu resultado formam uma dependência de protocolo. A janela também precisa preservar estados não resolvidos, como uma pergunta ainda sem resposta. Uma implementação robusta calcula um fechamento de dependências antes de cortar o histórico; recência define preferência, não validade semântica.

Condição de contorno:
A hipótese de que o passado é dispensável falha quando uma restrição antiga permanece vigente ou uma ação atual depende de identificadores removidos.

Contrato proposto:
- Entradas: Histórico ordenado, orçamento e grupos de mensagens dependentes.
- Saídas: Contexto válido com fronteira de descarte e referências ao arquivo completo.
- Estado: Cursor de arquivamento e conjunto de fatos protegidos ainda necessários.
- Invariante: Nenhum resultado de ferramenta fica associado a uma chamada inexistente no protocolo enviado.

Compromissos de projeto:
- FIFO é previsível e barato, mas ignora valor de informações antigas.
- Proteger dependências melhora continuidade, porém pode impedir que a janela caiba sem outra forma de redução.

## T003:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma chamada no limite da janela e seu resultado depois do corte. A montagem deve manter o par necessário ou externalizá-lo por um mecanismo compatível, sem histórico inválido.

Plano de avaliação proposto:
Avaliação proposta: comparar FIFO por mensagens e descarte por grupos completos. Variar tamanho das saídas e distância de restrições relevantes; medir erros de protocolo, recuperação posterior e sucesso das etapas dependentes.

Comparações:
- T041 (complements): Last-N escolhe tamanho por quantidade de mensagens; a janela genérica pode usar outras unidades.
- T039 (alternative): Seleção por importância pode preservar um fato antigo que FIFO retiraria.

Afirmação rastreável:
Context editing documenta remoção de resultados antigos com placeholders e opções de preservação.
Suporte: direct; fontes: V3A-S008
Limite: Isso apoia uma implementação específica de descarte; não demonstra que todo histórico admite FIFO sem perda.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T003:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou pares de ferramentas. Aqui a janela móvel ganha transições planejadas por fase e testes de retenção de obrigações.

Projeto e decomposição
Defina fronteiras de fase em vez de descartar continuamente. Ao terminar coleta, transforme resultados confirmados em tabela e remova apenas conversas de busca. A janela da fase seguinte começa com objetivos e pendências explícitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Controle adaptativo
Use duas filas: observações recentes e obrigações ainda abertas. FIFO governa a primeira; uma obrigação só sai por resolução identificada. Isso evita que repetição de logs empurre uma condição antiga necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Validação contrafactual
Variar tamanho dos logs sem mudar decisões permite medir sensibilidade da política ao volume incidental. Avalie obrigações recuperadas corretamente após mudanças de fase. Unidade de avaliação: trajetória de tarefa. Inclua uma mudança de fase com resultado tardio pertencente à fase anterior. O controlador deve registrar a observação, avaliar se ela invalida decisão atual e evitar reinseri-la como instrução recente. Medir separadamente quantidade de eventos preservados e quantidade de obrigações corretamente aplicadas impede confundir arquivo completo com contexto útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Triagem contínua
Cenário: Chamados chegam durante um incidente.
Estratégia: Agrupar observações por intervalo, persistir ações confirmadas e carregar pendências antigas antes de decidir próximo passo.
Papel do modelo pequeno: 3–7B classifica observações curtas.
Aceite proposto: Não perder restrição ativa quando o volume aumenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Extração em etapas
Cenário: Um arquivo exige várias leituras.
Estratégia: Manter cursor e campos faltantes fora da fila; trocar trechos a cada bloco sem reintroduzir páginas concluídas.
Papel do modelo pequeno: 8–14B reconcilia campos extraídos.
Aceite proposto: Cobrir todos os campos obrigatórios ou marcar ausência com referência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Janela curta por fase com obrigações enumeradas em campos.
8–14B: Janela com duas fontes simultâneas para comparar correções locais.
15–30B: Integração de fases complexas usando referências, sem carregar histórico integral.
Requisitos de treino/runtime: Estado explícito de obrigações e cursor; limites calculados no tokenizer do leitor.
Não aplicar quando: A tarefa requer dependências globais que não podem ser representadas num estado compacto.

## T003:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T003:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T003 → T040 [complements]
Como combinar: Separar conteúdo recente de estado vigente.
Interface: Fila de observações e lista versionada de obrigações.
Condição: Existir evento explícito de conclusão.
Aceite proposto: Introduzir logs irrelevantes e verificar estabilidade da decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T003 → T070 [feeds]
Como combinar: Arquivar unidades removidas para reconsulta.
Interface: Episódio, intervalo, cursor e motivo do descarte.
Condição: Armazenamento acessível após rotação.
Aceite proposto: Solicitar episódio antigo e conferir localização exata.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar silêncio recente como cancelamento.
- Aplicar descarte somente a grupos de protocolo completos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade em tarefas com ruído volumoso; manter mesma informação obrigatória no baseline.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T050, T063, T069, P002

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

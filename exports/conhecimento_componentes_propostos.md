# Componentes arquiteturais propostos

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

# P001 — Context Engine

**Nome canônico:** Context Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P001  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de preparação de contexto

## P001:C01 — conceito

Context Engine é um nome editorial proposto para a cadeia que transforma uma solicitação, seu estado e evidências recuperadas na entrada efetiva do modelo. Sua entrega seria um pacote de contexto acompanhado de manifesto: fontes, versões, trechos, prioridades e tokens. As fontes fundamentam engenharia de contexto e recuperação; não demonstram um componente LAI implementado com esse nome.

Como funciona:
- Receber objetivo atual, contrato de resposta, modelo escolhido e orçamento fornecido pelo gestor de contexto.
- Consultar fontes autorizadas, normalizar resultados e eliminar redundância sem apagar divergências relevantes.
- Ordenar instruções e evidências, reservando espaço para a resposta e preservando referências aos documentos originais.

## P001:C02 — aplicacao

Quando usar:
- Tarefas que combinam histórico, arquivos e ferramentas, exigindo uma entrada reconstruível e mensurável.

Quando não usar:
- Como substituto da persistência de memória, do roteamento de modelos ou da validação da resposta produzida.

Implementação proposta:
- Proposta: definir uma função build_context que recebe versões explícitas e devolve mensagens, manifesto e estado de completude.
- Dividir a preparação em recuperação, seleção, extração e empacotamento; atribuir orçamento de tokens a cada etapa.
- Quando uma evidência necessária não couber, buscar um trecho menor ou declarar contexto insuficiente; manter rastreável o descarte.

Aplicação LAI proposta:
Proposta LAI: usar P001 como pipeline de montagem, P002 para orçamento e P007 para busca, devolvendo ao executor um manifesto verificável antes da inferência.

## P001:C03 — riscos_validacao

Armadilhas:
- Uma apresentação organizada pode ocultar evidência incompleta; o manifesto deve indicar lacunas e conflitos.
- Reutilizar contexto montado para outro modelo pode ultrapassar seu limite ou alterar a contagem de tokens.

Métricas sugeridas:
- Tempo de preparação, tokens por fonte, cobertura das evidências necessárias e incidência de referências não resolvidas.

Testes propostos:
- Aceite proposto: reconstruir o mesmo pacote a partir das mesmas entradas versionadas, com ordem determinística quando aplicável.
- Testar fontes contraditórias e uma evidência que exceda a cota; conferir preservação do conflito e explicação da insuficiência.

## P001:C04 — perguntas_proveniencia

Pergunta: Qual artefato permitiria explicar o que o modelo recebeu?
Resposta: O manifesto do contexto, vinculado às mensagens efetivas e contendo IDs, versões, recortes e decisões de inclusão.

Pergunta: O Context Engine decidiria sozinho qual memória é verdadeira?
Resposta: Não. Ele deve carregar evidências e conflitos; reconciliação de memória e verificação possuem contratos próprios.

Pergunta: Como localizar um erro do motor?
Resposta: Compare candidatos recuperados, seleção e contexto final; uma fonte encontrada pode ter sido excluída na montagem.

Pergunta: O que aceitar como saída válida?
Resposta: Contexto dentro do orçamento com requisitos preservados, referências resolvíveis e decisões de exclusão observáveis.

Escopo das fontes:
Fontes apoiam montagem seletiva e recuperação; nome, interfaces e critérios de aceite são propostas editoriais.

## P001:C05 — mecanismo_avancado

Propõe-se que Context Engine produza um artefato de contexto, com versão e proveniência, antes da chamada ao modelo. A composição deve contabilizar instruções, schemas de ferramentas, histórico, evidências e reserva de saída. A seleção precisa tratar dependências: incluir uma conclusão sem sua condição ou uma alteração sem a versão de origem pode reduzir tokens e destruir o significado. O motor deve expor motivos de inclusão e exclusão, permitindo investigar falhas de recuperação e montagem separadamente.

Condição de contorno:
O orçamento calculado depende do tokenizer e do protocolo realmente usados pelo servidor. Uma estimativa local não substitui a contagem do provedor quando existe diferença de serialização.

Contrato proposto:
- Entradas: Tarefa, identidade autorizada, snapshot de memória, candidatos recuperados, ferramentas elegíveis e orçamento do modelo.
- Saídas: Contexto serializado, manifesto de evidências, contagem ou estimativa de tokens e justificativas de seleção.
- Estado: Versão da política de montagem, tokenizer, snapshot dos insumos e relações entre evidências e referências.
- Invariante: Nenhum trecho deve perder sua identidade de fonte; exclusões não podem remover silenciosamente requisitos obrigatórios da tarefa.

Compromissos de projeto:
- Montagem determinística facilita auditoria, enquanto seleção adaptativa pode melhorar relevância e introduzir variação.
- Preservar dependências consome mais tokens por evidência, mas evita trechos isolados que induzem interpretação errada.

## P001:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: fornecer duas versões contraditórias de um requisito e um limite insuficiente; exigir explicitação da versão escolhida ou insuficiência, sem combinar silenciosamente afirmações incompatíveis.

Plano de avaliação proposto:
Comparar montagem por ordem de chegada e composição com orçamento no mesmo conjunto de tarefas. Medir cobertura dos requisitos, fidelidade das citações, tokens e respostas aceitas. Avaliar exclusões manualmente em uma amostra reservada.

Comparações:
- T024 (complements): Context Broker e Builder podem realizar aquisição e composição.
- T152 (complements): A alocação de tokens fornece o limite de montagem.

Afirmação rastreável:
Engenharia de contexto abrange a seleção de informações disponíveis durante a inferência.
Suporte: related; fontes: V3D-S021
Limite: A fonte sustenta o problema; Context Engine e este contrato são uma proposta editorial própria.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P001:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu montagem e manifesto. Aqui Context Engine é proposto como compilador de necessidades de evidência em pacotes próprios para cada consumidor.

Projeto e decomposição
Receber tarefa e decompor saída em afirmações ou ações com requisitos. Cada requisito recebe tipo de suporte, prioridade e condição de insuficiência; o contexto deixa de ser simples concatenação de documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

Controle adaptativo
Montar uma representação conforme o leitor: campos explícitos para extrator pequeno, pares de evidência para comparador e panorama com referências para integrador. A transformação deve preservar identidade dos fatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

Validação contrafactual
Comparar pacote único e compilação por papel com mesmas fontes. Medir suporte por afirmação, tokens inúteis e diferenças introduzidas pela representação; organização não autoriza adicionar conhecimento. Unidade de avaliação: pacote de contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

USO AVANÇADO — Pipeline local de análise
Cenário: Extração e síntese usam modelos diferentes.
Estratégia: Compilar campos para 3–7B, consolidar resultados em código e fornecer ao integrador somente evidências e conflitos. Reabrir fonte quando campo não tiver suporte.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra.
Aceite proposto: Nenhuma afirmação final pode perder vínculo com evidência original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

USO AVANÇADO — Resposta sob prazo
Cenário: Nem todas as fontes chegam a tempo.
Estratégia: Priorizar requisitos essenciais, produzir pacote parcial explícito e bloquear conclusões que dependam de fonte pendente.
Papel do modelo pequeno: 8–14B responde escopo coberto.
Aceite proposto: Completude declarada deve coincidir com requisitos efetivamente sustentados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de pacotes tipados por campo, com pouca ambiguidade.
8–14B: Leitor de pacotes comparativos e exceções locais.
15–30B: Integrador de afirmações interdependentes com expansão dirigida.
Requisitos de treino/runtime: Modelo de requisitos, manifesto de transformações e perfis de consumidor; componente LAI é proposta editorial, não software verificado.
Não aplicar quando: A tarefa não pode ser decomposta sem perder significado e o pacote omite dependências essenciais.

## P001:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Inspira montagem de contexto; não comprova Context Engine LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q020.

## P001:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P001 → P007 [requires]
Como combinar: Solicitar evidência por requisito e escopo.
Interface: requirement_id, consulta, filtros e tipo de suporte.
Condição: Retriever devolver proveniência e lacunas.
Aceite proposto: Recuperar documento correto que não sustenta o requisito e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P001 → P002 [requires]
Como combinar: Negociar limite de contexto antes de compilar.
Interface: Perfil do modelo, reserva e cotas por requisito.
Condição: Conjunto obrigatório caber ou gerar insuficiência.
Aceite proposto: Trocar para modelo menor e recalcular pacote.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P001 → T200 [feeds]
Como combinar: Entregar manifesto à verificação da resposta.
Interface: Afirmações, fontes e transformações aplicadas.
Condição: Verificador acessar originais quando necessário.
Aceite proposto: Detectar citação que aponta fonte verdadeira mas não suporta a frase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir contexto bem organizado com evidência completa.
- Não promover texto recuperado a instrução da aplicação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar leitor pequeno com pacote compilado e fronteira com fontes equivalentes; não prometer paridade geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T009, T032, P002, P007, P009

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V3D-S021 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Curadoria iterativa de contexto, seleção de informações e restrições da janela.

Limite: Artigo de engenharia, não prova experimental dos componentes arquiteturais propostos neste pacote.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# P003 — Virtual Context Manager

**Nome canônico:** Virtual Context Manager  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P003  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gestor proposto de contexto virtual; paginação proposta de memória externa

## P003:C01 — conceito

Virtual Context Manager é um componente editorial proposto para mover informação entre uma janela pequena e armazenamento externo maior. Inspirado em gerência de memória virtual de agentes, usaria referências para carregar e descarregar blocos conforme a tarefa. Isso não aumenta fisicamente a janela, não equivale ao cache KV e não comprova que esse módulo esteja implementado na LAI.

Como funciona:
- Representar conteúdo externo por identificador, versão, localização, resumo de descoberta e tamanho estimado.
- Tratar uma referência necessária ausente da janela como solicitação de carregamento, sujeita ao orçamento ativo.
- Registrar alterações em armazenamento durável antes de remover a única cópia modificada de um bloco.

## P003:C02 — aplicacao

Quando usar:
- Projetos e conversas cujo acervo excede a janela, mas somente uma fração precisa estar presente em cada etapa.

Quando não usar:
- Quando o armazenamento externo é indisponível e a tarefa exige informações que nunca foram carregadas.

Implementação proposta:
- Proposta: separar tabelas de referências, conteúdo persistido e mapa de blocos residentes; não guardar apenas resumos sem origem.
- Implementar operações explícitas de localizar, carregar, atualizar e descarregar, com pré-condição de versão para escritas.
- Limitar carregamentos por etapa e detectar ciclos que alternam os mesmos blocos sem progresso.

Aplicação LAI proposta:
Proposta LAI: conectar P003 ao runtime de memória e ao gestor de janela, mantendo cada troca de bloco associada à necessidade concreta da tarefa.

## P003:C03 — riscos_validacao

Armadilhas:
- Paginação pode aumentar latência e falhar quando o índice descreve mal o conteúdo.
- Uma referência antiga pode apontar para conteúdo alterado; resolver sempre identidade e versão, sem presumir equivalência.
- Evicção do contexto e exclusão do armazenamento são operações distintas.

Métricas sugeridas:
- Latência por carregamento, acertos de residência, leituras repetidas e falhas de resolução de versões.

Testes propostos:
- Aceite proposto: executar uma tarefa maior que a janela recuperando evidências antigas por referência.
- Interromper uma atualização antes da persistência e exigir que o bloco modificado não seja perdido; testar referência obsoleta explicitamente.

## P003:C04 — perguntas_proveniencia

Pergunta: Contexto virtual significa memória ilimitada disponível ao modelo?
Resposta: Não. O acervo externo pode ser maior, mas cada chamada continua limitada e cada carregamento tem custo.

Pergunta: Quando um bloco modificado pode sair da janela?
Resposta: Quando houver confirmação de sua persistência ou outra cópia durável identificada; remoção antecipada perderia o único estado atualizado.

Pergunta: Uma referência ocupa o lugar do documento sem custo?
Resposta: Ela reduz tokens residentes, mas exige armazenamento acessível, resolução e nova leitura quando necessário.

Pergunta: Qual erro é específico deste componente?
Resposta: Resolver a referência para versão errada ou descartar evidência ainda necessária a uma operação ativa.

Escopo das fontes:
MemGPT fundamenta movimentação entre níveis; interfaces e garantias descritas são propostas, não capacidades LAI verificadas.

## P003:C05 — mecanismo_avancado

Virtual Context Manager propõe separar referências residentes e conteúdo externo carregável. Uma falta de informação deve gerar resolução de referência, carregamento e eventual substituição de conteúdo menos útil. Elementos indispensáveis à operação atual podem ser fixados temporariamente, evitando que a própria política de descarte remova um contrato ainda em uso. Ao contrário de paginação convencional de bytes, uma seleção semântica pode errar a relevância; essa incerteza precisa aparecer como falha recuperável.

Condição de contorno:
Referências podem expirar, mudar de versão ou perder autorização. Encontrar um identificador no contexto não garante que seu conteúdo permaneça disponível ou permitido.

Contrato proposto:
- Entradas: Tarefa, referências versionadas, orçamento ativo, política de fixação e identidade da sessão.
- Saídas: Trechos carregados, manifesto de residentes, faltas não resolvidas e decisões de substituição.
- Estado: Mapa entre referência, hash, versão, origem, custo estimado e estado de residência na janela.
- Invariante: Conteúdo fixado por uma operação ativa não pode ser removido sem encerrar ou replanejar essa operação.

Compromissos de projeto:
- Carregamento sob demanda economiza janela, mas acrescenta latência e risco de referência ausente.
- Fixar conteúdo evita descarte indevido, porém reduz espaço para novas evidências e pode exigir pausa explícita.

## P003:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: remover o documento externo após emitir a referência e depois exigir seu conteúdo; o controlador deve informar indisponibilidade e impedir que um resumo antigo seja tratado como original recuperado.

Plano de avaliação proposto:
Comparar janela fixa e política virtual em tarefas longas com reuso, documentos modificados e limites apertados. Medir faltas resolvidas, leituras redundantes, perda de condições e custo total, incluindo chamadas adicionais de recuperação.

Comparações:
- T063 (specializes): É um componente proposto para gerenciar contexto virtual.
- T078 (complements): Semantic Page Fault descreve o evento de falta a resolver.

Afirmação rastreável:
MemGPT estuda gestão em camadas para ampliar o acesso à informação além da janela imediata.
Suporte: related; fontes: A-S009
Limite: Analogia arquitetural; esta ficha não afirma compatibilidade ou implementação do sistema MemGPT.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P003:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu residentes e fixação. Aqui Virtual Context Manager é proposto como controlador de conjuntos de trabalho e custos de recarga.

Projeto e decomposição
Agrupe blocos que precisam coexistir para uma decisão. Se o conjunto inteiro não couber, decompor a decisão ou criar representação intermediária verificável; evicção individual pode causar alternância sem progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010, V3A-S039.

Controle adaptativo
Antecipe dependências explícitas e cancele prefetch quando o plano mudar. Registrar conteúdo carregado sem uso permite perceber quando antecipação desperdiça janela.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010, V3A-S039.

Validação contrafactual
Compare carga sob demanda, prefetch e grupos fixados. Meça recargas, avanço por chamada e perda de condições; uma falta semântica é hipótese operacional com critério, não falha de endereço universal. Unidade de avaliação: conjunto de trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010, V3A-S039.

USO AVANÇADO — Comparação de versões grandes
Cenário: Leitor alterna entre documentos.
Estratégia: Carregar pares de seções correspondentes e guardar diferenças estruturadas; manter referências aos originais para revisar conflito.
Papel do modelo pequeno: 8–14B compara pares.
Aceite proposto: Toda diferença relevante deve permanecer verificável sem releitura integral.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010, V3A-S039.

USO AVANÇADO — Procedimento com várias etapas
Cenário: Cada passo usa recursos distintos.
Estratégia: Carregar dependências do próximo passo, confirmar persistência do resultado atual e só então liberar blocos anteriores.
Papel do modelo pequeno: 3–7B executa; 15–30B replaneja.
Aceite proposto: Nenhuma unidade modificada pode sair sem cópia durável identificada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010, V3A-S039.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de blocos explicitamente escolhidos por controlador.
8–14B: Comparador local com conjunto de trabalho pequeno e estável.
15–30B: Planejador de decomposição quando dependências não cabem juntas.
Requisitos de treino/runtime: Mapa de residência, dependências, referências versionadas e confirmação de persistência; módulo permanece proposta.
Não aplicar quando: A informação necessária não pode ser recuperada ou conjunto indispensável não cabe e não admite decomposição.

## P003:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: Inspira paginação de contexto proposta.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## P003:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P003 → P002 [requires]
Como combinar: Obter limite de residência e reserva.
Interface: Orçamento útil, modelo e contratos fixados.
Condição: Contagem incluir dependências de cada bloco.
Aceite proposto: Adicionar bloco que excede conjunto e exigir decisão explícita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P003 → P006 [complements]
Como combinar: Carregar conteúdo e dependências por referência.
Interface: Recurso, revisão, seletor e custo.
Condição: Loader verificar identidade do corpo.
Aceite proposto: Renomear recurso e detectar referência incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P003 → T218 [requires]
Como combinar: Detectar alternância de cargas sem avanço.
Interface: Sequência de residentes, faltas e progresso.
Condição: Identidades dos blocos serem estáveis.
Aceite proposto: Forçar ciclo entre conjuntos e exigir mudança de estratégia.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir contexto virtual com KV cache.
- Não apagar armazenamento ao remover bloco da janela.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar progresso por custo de leitura em tarefas maiores que a janela; seleção imperfeita limita qualquer porte.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T063, T066, T074, P002, P004, P006

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

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

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S039 — Redis Key eviction

[https://redis.io/docs/latest/develop/reference/eviction/](https://redis.io/docs/latest/develop/reference/eviction/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Políticas de eviction, noeviction, LRU aproximado, LFU probabilístico e distinção entre expiração e pressão de capacidade.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V2B-S003 — Introducing Context Repositories: Git-based Memory for Coding Agents

[https://www.letta.com/blog/context-repositories/](https://www.letta.com/blog/context-repositories/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Origem do nome Context Repositories, memória em Git, divulgação progressiva e trabalho de subagentes em worktrees.

Limite: Anúncio histórico de fevereiro de 2026; descreve system/ e ativação antigos. Regras atuais de MemFS prevalecem. Não houve reprodução dos fluxos descritos.

### V3A-S046 — Letta Shared memory

[https://docs.letta.com/concepts/shared-memory](https://docs.letta.com/concepts/shared-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MemFS pertence a um agente; repositório compartilhado pertence à organização e requer commit, push e pull para sincronização entre checkouts.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P004 — LAI Memory Runtime

**Nome canônico:** LAI Memory Runtime  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** runtime proposto de memória LAI

## P004:C01 — conceito

LAI Memory Runtime é um nome editorial proposto para os serviços de persistência, consulta e evolução da memória do agente. Abrangeria escopos de sessão e de projeto, versões e referências às evidências. A proposta reúne princípios de stores, checkpoints e temporalidade; não representa uma plataforma existente comprovada pelas fontes nem pressupõe atualização dos pesos do modelo.

Como funciona:
- Separar estado de execução por sessão de informações reutilizáveis entre sessões, com namespaces explícitos.
- Registrar cada objeto com identidade, tipo, conteúdo, proveniência, versão e escopo de leitura e escrita.
- Quando o domínio exigir consultas históricas, distinguir tempo de validade do fato e tempo em que foi registrado.

## P004:C02 — aplicacao

Quando usar:
- Agentes que retomam trabalhos e precisam recordar decisões, artefatos e fatos sem depender da conversa atual.

Quando não usar:
- Como substituto de um índice de busca bem avaliado ou como evidência de que um fato extraído é correto.

Implementação proposta:
- Proposta: definir operações get, query, put e supersede com contratos diferentes para evidência, hipótese e decisão.
- Aplicar concorrência otimista às atualizações e preservar vínculos entre revisão anterior e nova, evitando sobrescrita silenciosa.
- Escolher armazenamento durável e política de retenção por tipo; publicar índices somente com a versão de origem identificada.

Aplicação LAI proposta:
Proposta LAI: fornecer a P005 uma camada única de contratos de memória, com implementação de armazenamento substituível e evidências preservadas por referência.

## P004:C03 — riscos_validacao

Armadilhas:
- Um checkpointer em memória volátil não demonstra recuperação após reinício do processo.
- Índice e registro canônico podem divergir; resultados devem informar versão e atrasos de indexação.
- Confundir a data do evento com a data de ingestão impede corrigir fatos recebidos tardiamente.

Métricas sugeridas:
- Durabilidade confirmada, conflitos de versão, atraso de indexação e consistência de consultas históricas.

Testes propostos:
- Aceite proposto: reiniciar o serviço após uma gravação confirmada e recuperar o mesmo objeto versionado.
- Testar duas atualizações concorrentes e um fato atrasado; exigir conflito explícito e respostas temporais coerentes.

## P004:C04 — perguntas_proveniencia

Pergunta: Persistir memória treina o modelo?
Resposta: Não. Nesta proposta os objetos ficam em armazenamento externo e precisam ser recuperados ou inseridos no contexto.

Pergunta: Por que separar sessão e projeto?
Resposta: Porque retomar um fluxo exige estado específico da sessão, enquanto decisões do projeto podem ser reutilizadas sob outro ciclo de execução.

Pergunta: O índice vetorial deve ser a única memória?
Resposta: A proposta mantém origem e histórico recuperáveis para reconstruir índices e explicar correções.

Pergunta: Uma correção apaga o erro anterior?
Resposta: Não por padrão: registra nova informação e permite consultar o que era conhecido em cada momento.

Escopo das fontes:
As fontes apoiam escopos, persistência e tempo; a combinação LAI e seus contratos permanecem propostas.

## P004:C05 — mecanismo_avancado

LAI Memory Runtime é aqui um nome de proposta para coordenar gravação, leitura temporal e proveniência de memórias. Cada atualização deve distinguir quando o fato vale no domínio e quando foi registrado. A promoção de uma observação para memória consolidada precisa apontar as evidências usadas e preservar contradições ainda não resolvidas. Recomenda-se tratar índices e resumos como projeções reconstruíveis, mantendo o registro autorizado de origem separado de conveniências de busca.

Condição de contorno:
Uma transação local não torna atômica a atualização de todo índice externo. A aplicação precisa declarar consistência, atraso tolerado e estratégia de reconstrução das projeções.

Contrato proposto:
- Entradas: Observação identificada, origem, escopo autorizado, tempos de validade e registro, versão esperada e política de retenção.
- Saídas: Memória versionada, referências de evidência, evento de atualização e resultado explícito de conflito ou deduplicação.
- Estado: Registro de memórias, histórico temporal, chaves de deduplicação e cursores das projeções de busca.
- Invariante: Toda memória promovida deve manter origem rastreável; corrigir um fato não pode reescrever silenciosamente o histórico de conhecimento.

Compromissos de projeto:
- Histórico temporal aumenta armazenamento, mas permite explicar decisões tomadas com informação disponível à época.
- Atualizar índices de forma assíncrona reduz acoplamento, porém exige controlar atraso e leituras de versões antigas.

## P004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: repetir o mesmo evento, inserir correção retroativa e interromper atualização do índice; verificar deduplicação, consultas temporais consistentes e reconstrução sem perda de origem.

Plano de avaliação proposto:
Avaliar uma sequência conhecida de fatos, correções e conflitos. Comparar armazenamento de último valor e memória versionada por acerto temporal, rastreabilidade, atraso de projeção e custo. Todos os testes de runtime descritos são propostos.

Comparações:
- T056 (complements): Bitemporalidade separa validade do fato e registro.
- T065 (complements): Transações delimitam confirmações locais.

Afirmação rastreável:
Transações agrupam operações locais; modelos temporais distinguem validade e registro de fatos.
Suporte: related; fontes: V3D-S020, A-S032
Limite: A composição LAI Memory Runtime é editorial; as fontes não comprovam sua existência ou implantação.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu persistência e projeções. Aqui LAI Memory Runtime é proposto com contratos explícitos de visibilidade após escrita e reconstrução.

Projeto e decomposição
Diferencie commit no registro canônico e visibilidade no índice. Uma escrita confirmada pode ainda não aparecer em busca; o cliente precisa receber revisão e cursor de projeção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

Controle adaptativo
Ofereça leitura por identidade para confirmar atualização recente e busca para descoberta. Exigir read-your-writes em toda busca pode custar mais; declare onde a garantia é necessária e como verificar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

Validação contrafactual
Compare leitura imediata, busca assíncrona e fallback ao canônico. Meça atraso de projeção, respostas obsoletas e tempo de reconstrução; durabilidade do banco não garante atualização do embedding. Unidade de avaliação: operação de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

USO AVANÇADO — Correção de memória ativa
Cenário: Usuário corrige fato usado no próximo turno.
Estratégia: Confirmar registro, retornar revisão e consultar diretamente a versão nova até índice alcançar cursor correspondente.
Papel do modelo pequeno: 3–7B extrai correção.
Aceite proposto: Próxima resposta não pode recuperar versão revogada como vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

USO AVANÇADO — Reconstrução de índice
Cenário: Embedding muda ou índice falha.
Estratégia: Reconstruir a partir do canônico em paralelo, validar amostra e trocar manifesto ativo sem interromper consultas pinadas.
Papel do modelo pequeno: 8–14B valida conteúdo; código reconstrói.
Aceite proposto: Nenhuma consulta pode combinar índices com versões incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S004, V4A-S007, V3A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de propostas tipadas e leitor de objetos identificados.
8–14B: Leitor de projeções com capacidade de detectar atraso e lacuna.
15–30B: Analista de conflitos entre registros e reconstruções, sem controlar transações livremente.
Requisitos de treino/runtime: Store canônico, cursor de projeção, versões e recuperação testável; componente LAI não está implementado neste pacote.
Não aplicar quando: O único registro é o índice vetorial ou o sistema não consegue dizer qual revisão foi lida.

## P004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Operador descreve migração real de todos os metadados e listagem fortemente consistente.
Mecanismo documentado: Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.
Correspondência com esta base: Inspira contrato de persistência; não demonstra runtime LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.
Limite: Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S007, V4A-S005.

V4A-C027 — Letta / Framework de agentes stateful
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.
Mecanismo documentado: Persistência do agente e ferramentas de memória externas ao modelo.
Correspondência com esta base: Inspira contratos do runtime proposto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.
Limite: Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S026, V2B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q023.

## P004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P004 → T065 [requires]
Como combinar: Confirmar registro e evento de atualização localmente.
Interface: Objeto, versão esperada, commit e evento.
Condição: Invariantes locais cobertos pela transação.
Aceite proposto: Interromper entre escrita e publicação e verificar recuperação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P004 → P007 [feeds]
Como combinar: Expor revisão e atraso para recuperação.
Interface: Objeto, index_revision e projection_cursor.
Condição: Retriever respeitar requisito de frescor.
Aceite proposto: Consultar logo após correção e detectar índice atrasado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P004 → T072 [requires]
Como combinar: Publicar manifesto coerente de projeções.
Interface: Store_revision, embedding e índices ativos.
Condição: Troca preservar leitores pinados.
Aceite proposto: Reconstruir índice e comparar objetos ausentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S004, V4A-S007, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar confirmação do índice em prova de verdade.
- Não presumir atomicidade entre todos os serviços externos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência percebida pelo leitor; modelos maiores também erram quando a camada de memória entrega revisão obsoleta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T056, T060, T072, T075, P003, P005

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### V3D-S020 — PostgreSQL — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade e confirmação de operações agrupadas numa transação local.

Limite: A garantia não se estende automaticamente a serviços externos ou outros armazenamentos independentes.

### V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services

[https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transações serializáveis em partições e experiência com serviços Google em produção.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency

[https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração efetiva dos metadados do Cloud Storage para Spanner e consistência de listagem.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V2B-S002 — Stateful agents

[https://docs.letta.com/concepts/stateful-agents](https://docs.letta.com/concepts/stateful-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade persistente, memória compartilhada entre conversas do mesmo agente e distinção entre agentes locais e com backup em nuvem.

Limite: Documentação atual consultada; não comprova isolamento ou durabilidade de uma implantação específica.

### V4A-S005 — Spanner: Google's Globally-Distributed Database

[https://research.google/pubs/spanner-googles-globally-distributed-database-2/](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco multiversão, transações externamente consistentes e incerteza temporal.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P005 — Context & Memory Controller

**Nome canônico:** Context & Memory Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador proposto de contexto e memória

## P005:C01 — conceito

Context & Memory Controller é um nome editorial proposto para coordenar políticas entre contexto ativo e memória persistente. Decidiria quando recuperar, resumir, promover ou reconciliar informações, delegando armazenamento e montagem a outros componentes. Essas fronteiras são escolhas arquiteturais propostas; as fontes não atestam um controlador LAI implementado nem uma taxonomia padronizada com esse nome.

Como funciona:
- Observar eventos da tarefa, ocupação da janela e candidatos a memória com suas evidências.
- Distinguir decisões vigentes, hipóteses, resultados confirmados e conteúdo temporário antes de escolher o destino.
- Emitir comandos versionados para montagem de contexto e atualização de memória, preservando a origem das decisões.

## P005:C02 — aplicacao

Quando usar:
- Fluxos com múltiplos agentes ou sessões em que resumos, decisões e recuperação precisam seguir a mesma política.

Quando não usar:
- Como escritor irrestrito capaz de transformar qualquer saída fluente em fato persistente confirmado.

Implementação proposta:
- Proposta: definir regras de promoção por tipo; uma preferência declarada, uma inferência e um resultado de ferramenta exigem evidências distintas.
- Associar cada decisão de política à versão do estado observado e recusar atualização quando essa base já tiver mudado.
- Ao compactar, solicitar resumo com referências; ao encontrar conflito, registrar versões concorrentes e aplicar reconciliação explícita.

Aplicação LAI proposta:
Proposta LAI: estabelecer P005 como coordenador de política; P004 persiste, P007 recupera, P002 administra a janela e P001 monta a entrada.

## P005:C03 — riscos_validacao

Armadilhas:
- Dois controladores independentes podem promover conclusões incompatíveis ou alternar continuamente versões.
- Ausência no resumo não significa revogação de uma decisão; exclusão e supersessão precisam de eventos próprios.
- Políticas excessivamente agressivas acumulam erros como se fossem conhecimento consolidado.

Métricas sugeridas:
- Promoções corrigidas posteriormente, conflitos pendentes, decisões sem origem e custo de recuperação por etapa útil.

Testes propostos:
- Aceite proposto: inserir hipótese posteriormente refutada e verificar que ela não permanece como fato ativo.
- Rodar duas propostas sobre a mesma versão e exigir resolução do conflito; testar redução de contexto preservando uma obrigação vigente.

## P005:C04 — perguntas_proveniencia

Pergunta: Quem decide o que vira memória reutilizável?
Resposta: Nesta arquitetura proposta, a política do controlador, aplicando critérios de evidência e escopo; o runtime executa a persistência.

Pergunta: Uma decisão que desapareceu do resumo deixa de valer?
Resposta: Não automaticamente. Deve existir revogação, supersessão ou condição de validade verificável no registro persistente.

Pergunta: Qual regra diferencia memória de contexto?
Resposta: Uma informação pode ser útil agora sem merecer persistência, ou ser durável sem precisar ocupar a janela atual.

Pergunta: O que registrar em cada decisão?
Resposta: Identidade, versão da política, origem, motivo e revisão dos dados usados para permitir auditoria.

Escopo das fontes:
Fontes apoiam memória seletiva e persistência; autoridade, regras de promoção e fronteiras são desenho editorial proposto.

## P005:C05 — mecanismo_avancado

Context & Memory Controller é proposto como coordenador entre o que pode ser lido, o que cabe no próximo turno e o que merece persistência. Uma resposta recém-gerada não deve virar fato durável só porque apareceu no diálogo. A admissão de memórias precisa distinguir observação, inferência e instrução, além de registrar fonte e validade. A admissão no contexto tem objetivo diferente: selecionar informação útil para a tarefa atual dentro de um orçamento.

Condição de contorno:
Unificar políticas não exige um único banco ou processo. Centralização excessiva pode criar gargalo e misturar decisões de relevância com regras de autorização.

Contrato proposto:
- Entradas: Tarefa, identidade, candidatos de leitura, propostas de gravação, limites de contexto e políticas de retenção.
- Saídas: Decisões justificadas de admitir, adiar, rejeitar ou revisar, com manifesto do contexto e da memória afetada.
- Estado: Versão das políticas, pendências de validação, referências de origem e métricas de pressão por sessão.
- Invariante: Uma decisão de relevância não pode ampliar permissão; conteúdo inferido precisa continuar identificado como inferência ao ser persistido.

Compromissos de projeto:
- Coordenação reduz divergências de política, mas exige interfaces claras para não concentrar toda execução em um componente.
- Validar promoção de memória custa tempo; aceitar tudo acelera escrita e pode acumular conclusões incorretas.

## P005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: recuperar documento sem autorização, gerar hipótese plausível e tentar promovê-la como fato confirmado; exigir bloqueio de escopo e preservação explícita da natureza inferida.

Plano de avaliação proposto:
Comparar gravação irrestrita e admissão por proveniência em tarefas com correções e fontes conflitantes. Medir fatos indevidamente promovidos, utilidade no turno seguinte, custo e atrasos. Separar falhas de autorização de falhas de relevância.

Comparações:
- P001 (complements): A montagem de contexto consome decisões de admissão.
- P004 (complements): O runtime de memória recebe gravações e consultas autorizadas.

Afirmação rastreável:
Persistência de sessão e armazenamento durável entre sessões têm escopos distintos na documentação de memória.
Suporte: related; fontes: V3D-S016
Limite: O controlador unificado é proposta própria e precisa de implementação e avaliação específicas.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou políticas de contexto e memória. Aqui Context & Memory Controller é proposto com regras de precedência e filas de decisões revisáveis.

Projeto e decomposição
Defina precedência entre elegibilidade, validade, utilidade e custo. Informação muito relevante mas revogada não deve vencer seleção; relevância não amplia permissão nem confirma verdade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

Controle adaptativo
Separe caminho rápido de leitura e caminho de manutenção. Promoção, reconciliação e consolidação podem ter fila própria, evitando que cada pergunta reavalie todo o acervo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

Validação contrafactual
Compare controlador único irrestrito e políticas tipadas com decisões registradas. Meça promoção indevida, bloqueios desnecessários e custo por consulta; centralização lógica não exige processo monolítico. Unidade de avaliação: decisão de política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

USO AVANÇADO — Memória com correções
Cenário: Nova evidência contradiz regra ativa.
Estratégia: Suspender uso da regra afetada, preservar evidência e enviar reconciliação à fila prioritária; liberar somente após decisão explícita.
Papel do modelo pequeno: 8–14B propõe reconciliação.
Aceite proposto: Nenhuma projeção pode continuar aplicando regra suspensa como vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

USO AVANÇADO — Carga alta de observações
Cenário: Nem tudo merece memória durável.
Estratégia: Admitir observações em camada temporária, consolidar por tipo e promover somente candidatos úteis e sustentados.
Papel do modelo pequeno: 3–7B classifica; 15–30B integra.
Aceite proposto: Taxa de fatos sem origem promovidos deve ser medida e bloqueada pelo critério local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e elegibilidade básica com regras externas.
8–14B: Revisor de suporte e conflitos locais antes de atualização.
15–30B: Planejador de manutenção complexa entre conjuntos de memória.
Requisitos de treino/runtime: Tabela de políticas, estados de decisão e trilha de motivos; nomes e fronteiras do controlador são proposta editorial.
Não aplicar quando: O controlador pode escrever irrestritamente ou a política mistura autorização e relevância numa pontuação única.

## P005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## P005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P005 → T071 [requires]
Como combinar: Aplicar promoção por tipo de candidato.
Interface: Fonte, tipo, escopo e critério de aceite.
Condição: Evidência satisfizer critério específico.
Aceite proposto: Propor hipótese como fato e exigir rejeição identificável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P005 → P004 [feeds]
Como combinar: Emitir comandos de memória com pré-condições.
Interface: Comando, revisão-base e decisão de política.
Condição: Runtime validar conflito antes de confirmar.
Aceite proposto: Mudar estado durante decisão e impedir sobrescrita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P005 → P001 [feeds]
Como combinar: Informar quais evidências são elegíveis.
Interface: IDs, validade, prioridade e motivos de exclusão.
Condição: Builder não reintroduzir conteúdo suspenso.
Aceite proposto: Recuperar fato revogado com score alto e impedir inclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar ausência no resumo como revogação.
- Não promover saída fluente sem origem verificável.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade das decisões de admissão e correção; política bem definida reduz erro acumulado, sem garantir raciocínio de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T058, T069, T071, T075, P001, P002, P004, P007

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P006 — Progressive Loader

**Nome canônico:** Progressive Loader  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** carregador progressivo proposto

## P006:C01 — conceito

Progressive Loader é um componente editorial proposto para expor primeiro metadados baratos e carregar conteúdo completo somente quando necessário. A ideia pode ser aplicada a skills, ferramentas, documentos e memória. Sua existência na LAI não foi verificada; as fontes descrevem divulgação progressiva e recuperação de definições, sem estabelecer este nome como padrão técnico universal.

Como funciona:
- Manter um catálogo de identificadores, descrições, versões e tamanhos, separado do conteúdo integral.
- Selecionar candidatos relevantes à tarefa, abrir o recurso principal e expandir dependências apenas quando necessárias.
- Reutilizar conteúdo carregado na mesma versão, respeitando orçamento total e limite de profundidade.

## P006:C02 — aplicacao

Quando usar:
- Acervos extensos de procedimentos e ferramentas em que enviar todas as definições consumiria a maior parte do contexto.

Quando não usar:
- Quando uma regra obrigatória para interpretar a tarefa seria omitida pelo catálogo ou quando a descoberta é insuficientemente confiável.

Implementação proposta:
- Proposta: definir estados descoberto, selecionado, carregado e invalidado, com manifesto por chamada.
- Preservar identificadores retornados pelo catálogo; validar acesso e versão ao resolver referências, sem fabricar caminhos por similaridade de nome.
- Carregar instruções específicas antes da ação que dependa delas; se faltar um recurso necessário, registrar dependência não satisfeita.

Aplicação LAI proposta:
Proposta LAI: oferecer descoberta leve a P001 e P003, carregar procedimentos sob demanda e registrar quais versões efetivamente orientaram cada ação.

## P006:C03 — riscos_validacao

Armadilhas:
- Uma descrição inadequada pode impedir que o recurso certo seja escolhido, apesar de existir.
- Referências circulares geram expansão infinita sem detecção de recursos já visitados.
- Catálogo e conteúdo podem mudar em momentos distintos; a mesma descrição não garante o mesmo procedimento.

Métricas sugeridas:
- Tokens iniciais e expandidos, acerto de seleção, latência de abertura e dependências ausentes.

Testes propostos:
- Aceite proposto: usar duas ferramentas com nomes próximos e verificar seleção e carregamento da definição correta.
- Testar recurso removido, atualização de versão e ciclo de referências; exigir parada finita e diagnóstico da dependência.

## P006:C04 — perguntas_proveniencia

Pergunta: Carregar metadados basta para executar uma ferramenta?
Resposta: Somente se o contrato completo necessário já estiver disponível; caso contrário, a definição deve ser carregada antes da execução.

Pergunta: Como evitar expansão recursiva sem fim?
Resposta: Registrar IDs e versões visitados, limitar profundidade e orçamento e interromper ciclos com uma dependência explícita.

Pergunta: Qual é o custo escondido do carregamento progressivo?
Resposta: Seleção errada, ida adicional ao armazenamento e expansão que consome o orçamento economizado.

Pergunta: Quando o recurso pode ser reutilizado?
Resposta: Quando versão, autorização e finalidade permanecem compatíveis com a requisição atual.

Escopo das fontes:
Fontes sustentam divulgação progressiva; estados, manifesto e limites são critérios de projeto propostos.

## P006:C05 — mecanismo_avancado

Progressive Loader propõe carregar primeiro descrições suficientes para selecionar um recurso e depois seu conteúdo específico. Metadados devem incluir versão e referência estável, permitindo verificar que o corpo carregado corresponde ao item escolhido. O loader precisa contabilizar o custo adicional de schemas e instruções após a seleção. Conteúdo recuperado de um arquivo ou ferramenta permanece dado de sua origem; o carregamento não lhe concede autoridade para alterar políticas da aplicação.

Condição de contorno:
Uma descrição ruim pode esconder o recurso correto. Se a seleção falhar, carregar menos conteúdo aumenta economia e também reduz capacidade de concluir a tarefa.

Contrato proposto:
- Entradas: Catálogo autorizado, consulta, descrições resumidas, referências versionadas e orçamento disponível para expansão.
- Saídas: Conteúdo necessário, identidade verificada, custo de carga e indicação de recurso ausente ou incompatível.
- Estado: Cache de descrições e corpos por versão, recursos ativos e histórico mínimo de decisões de seleção.
- Invariante: O corpo carregado deve corresponder à identidade selecionada; conteúdo novo não pode exceder silenciosamente o orçamento restante.

Compromissos de projeto:
- Descrições curtas reduzem tokens iniciais, mas precisam preservar sinais que distinguem recursos parecidos.
- Cache local reduz leituras repetidas, porém exige invalidação quando a versão ou autorização muda.

## P006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar um recurso entre seleção e leitura e incluir instruções maliciosas no corpo; exigir detecção de versão divergente e manutenção da hierarquia de instruções.

Plano de avaliação proposto:
Comparar catálogo integral e carregamento progressivo com tarefas que exigem ferramentas frequentes e raras. Medir seleção correta, tokens totais incluindo expansão, leituras extras e conclusão comprovada, não apenas redução do prompt inicial.

Comparações:
- T014 (specializes): Materializa divulgação progressiva de informação.
- T151 (complements): Pode carregar schemas de ferramentas somente quando necessários.

Afirmação rastreável:
Documentação de Agent Skills descreve divulgação progressiva de instruções e recursos.
Suporte: related; fontes: C-S052
Limite: O componente, suas verificações de versão e seu contrato são recomendações editoriais.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou seleção e identidade. Aqui Progressive Loader é proposto com carregamento de dependências, cancelamento e verificação de utilidade.

Projeto e decomposição
Mantenha grafo de dependências declaradas por recurso. Carregar procedimento pode exigir schema e definição; a carga deve retornar conjunto completo ou lista de faltas, não sucesso parcial oculto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

Controle adaptativo
Prefetch só ocorre para dependência provável e dentro de cota. Se objetivo mudar, cancelar cargas pendentes e impedir que resultado tardio seja anexado à tarefa errada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

Validação contrafactual
Compare catálogo integral, carga simples e carga por dependências. Meça escolhas incorretas, conteúdo nunca usado e faltas detectadas antes da execução; bytes lidos não equivalem a informação útil. Unidade de avaliação: carga de recurso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

USO AVANÇADO — Ferramentas numerosas
Cenário: A ação exige schema raro.
Estratégia: Selecionar capacidade por metadados, abrir schema e dependências, validar versão e somente então permitir argumentos.
Papel do modelo pequeno: 3–7B seleciona; 8–14B constrói chamada.
Aceite proposto: Nenhuma execução pode usar contrato apenas resumido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

USO AVANÇADO — Memória modular
Cenário: Uma tarefa referencia vários arquivos.
Estratégia: Abrir índice, resolver conjunto mínimo de módulos e registrar versões; interromper ciclo e devolver dependência não satisfeita.
Papel do modelo pequeno: 15–30B integra módulos.
Aceite proposto: Conjunto carregado deve preservar referências necessárias sem expansão infinita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Selector entre descritores contrastivos com carga controlada.
8–14B: Leitor que identifica dependências e solicita recursos adicionais.
15–30B: Planejador de carga entre módulos interdependentes com orçamento.
Requisitos de treino/runtime: Registry versionado, status de cargas e grafo de dependências; conteúdo recuperado conserva autoridade da origem.
Não aplicar quando: Descrições não discriminam recursos ou dependências não podem ser resolvidas dentro do limite útil.

## P006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q023.

## P006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P006 → T066 [requires]
Como combinar: Resolver recurso e versão antes de aceitar corpo.
Interface: resource_id, versão, digest e seletor.
Condição: Corpo corresponder ao item selecionado.
Aceite proposto: Alterar versão entre descoberta e carga e exigir nova validação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P006 → P002 [requires]
Como combinar: Reservar orçamento antes de expandir dependências.
Interface: Custo total previsto, cota e prioridade.
Condição: Reserva considerar conjunto completo.
Aceite proposto: Testar dependência transitiva que ultrapassa limite.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P006 → T045 [complements]
Como combinar: Aplicar busca de capacidade antes de carga pesada.
Interface: Descritores, efeitos e ferramentas candidatas.
Condição: Schema completo disponível antes de executar.
Aceite proposto: Selecionar ferramenta rara sem carregar catálogo inteiro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não anexar resultado tardio a objetivo revogado.
- Não permitir instrução do recurso alterar política superior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso de descoberta e custo total de expansão; economia do prompt inicial não basta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T044, T045, T151, T204, P001, P003

## Fontes primárias associadas

### C-S052 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills empacotam instruções e recursos carregados progressivamente.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S016 — Introducing advanced tool use on the Claude Developer Platform

[https://www.anthropic.com/research/advanced-tool-use](https://www.anthropic.com/research/advanced-tool-use)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas sob demanda evita inserir antecipadamente todos os schemas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S038 — Tool search tool

[https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas e carregamento adiado de schemas no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P007 — Memory Retriever

**Nome canônico:** Memory Retriever  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recuperador proposto de memória

## P007:C01 — conceito

Memory Retriever é um nome editorial proposto para localizar memórias relevantes e devolver evidências identificáveis, sem modificar o conhecimento armazenado. Poderia combinar filtros, busca lexical, vetorial e reranking. As fontes sustentam esses mecanismos individualmente; não confirmam um produto LAI com esse nome nem garantem que a combinação tenha qualidade suficiente para cada domínio.

Como funciona:
- Receber consulta, escopo de projeto, identidade do solicitante e instante de interesse quando a pergunta for temporal.
- Aplicar critérios de elegibilidade e recuperar candidatos por métodos adequados, combinando rankings sem tratar escores heterogêneos como probabilidades comparáveis.
- Reordenar, deduplicar e expandir filhos para pais quando necessário, devolvendo conteúdo e referências às versões originais.

## P007:C02 — aplicacao

Quando usar:
- Perguntas que dependem de decisões passadas, arquivos específicos ou fatos fora da janela ativa.

Quando não usar:
- Como mecanismo para converter similaridade semântica em veracidade, validade temporal ou autorização de acesso.

Implementação proposta:
- Proposta: definir um contrato search_memory com filtros explícitos e resultados contendo ID, versão, localização, evidência e motivo de seleção.
- Separar o conjunto de candidatos do contexto final; dimensionar a recuperação para que o reranker tenha alternativas úteis.
- Quando faltarem fontes elegíveis, devolver ausência ou insuficiência; não preencher o resultado com fatos apenas semanticamente próximos.

Aplicação LAI proposta:
Proposta LAI: fornecer a P001 evidências elegíveis e a P005 candidatos para reconciliação, mantendo a escrita sob contrato distinto.

## P007:C03 — riscos_validacao

Armadilhas:
- Filtrar somente depois de um top-k estreito pode eliminar todos os candidatos úteis.
- Uma memória revogada ainda pode ter alta similaridade; o estado de validade precisa ser considerado.
- Expandir um filho pode carregar um pai de outra versão se os vínculos não forem verificáveis.

Métricas sugeridas:
- Recall e ranking sobre perguntas rotuladas independentes, correção temporal, latência e proporção de evidências realmente utilizadas.

Testes propostos:
- Aceite proposto: perguntar por uma decisão substituída e exigir a versão válida no instante solicitado.
- Construir casos de código literal, paráfrase e ausência de resposta; avaliar recuperação e abstenção separadamente.

## P007:C04 — perguntas_proveniencia

Pergunta: O primeiro resultado é necessariamente o fato vigente?
Resposta: Não. Ranking mede adequação à consulta; vigência depende da versão, temporalidade e estado do registro.

Pergunta: Como avaliar um caso sem resposta no acervo?
Resposta: Rotular a ausência e verificar se o recuperador comunica insuficiência, em vez de entregar um candidato parecido como prova.

Pergunta: Score alto significa evidência verdadeira?
Resposta: Não. Ranking estima correspondência à consulta; validade e qualidade da fonte precisam de critérios próprios.

Pergunta: Por que testar o documento pai?
Resposta: Uma expansão pode reintroduzir conteúdo que a busca inicial filtrou corretamente.

Escopo das fontes:
Fontes apoiam recuperação, reranking e temporalidade; contrato e aceites são propostas editoriais.

## P007:C05 — mecanismo_avancado

Memory Retriever é proposto como interface de recuperação que recebe escopo, tempo e objetivo, além do texto da consulta. A filtragem precisa alcançar todas as rotas de busca e também a expansão de um trecho para seu documento pai. Combinar rankings lexicais e vetoriais pode ampliar cobertura, mas scores de origens diferentes não devem ser somados sem uma regra explícita. O retorno deve preservar por que cada evidência foi escolhida e qual versão estava disponível.

Condição de contorno:
Uma consulta histórica exige distinguir fatos válidos na data de interesse e fatos conhecidos na data da decisão. Recuperação recente por similaridade não responde automaticamente a essa pergunta temporal.

Contrato proposto:
- Entradas: Consulta, identidade autorizada, filtros temporais, tipos de memória, orçamento e versão dos índices.
- Saídas: Evidências com IDs, fontes, tempos, scores ou posições e indicação de cobertura insuficiente.
- Estado: Índices, mapeamento de documentos, versões de embeddings e políticas de fusão e expansão.
- Invariante: Filtrar apenas a lista final é insuficiente quando expansões ou etapas intermediárias podem expor conteúdo fora do escopo.

Compromissos de projeto:
- Busca híbrida melhora cobertura em alguns conjuntos, mas adiciona índices, latência e decisões de fusão.
- Reranking pode melhorar ordem dos candidatos, sem recuperar evidência que ficou fora da etapa inicial.

## P007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: criar documentos semanticamente iguais em escopos distintos e um pai com conteúdo restrito; verificar isolamento em busca lexical, vetorial, fusão e expansão de contexto.

Plano de avaliação proposto:
Comparar recuperação lexical, vetorial e híbrida com mesmas perguntas e filtros. Medir Recall@k, MRR, precisão das evidências, latência e violações de escopo; separar consultas temporais das perguntas factuais atuais.

Comparações:
- T027 (complements): Busca híbrida combina canais de candidatos.
- T032 (complements): Expansão parent-child exige manter escopo e proveniência.

Afirmação rastreável:
RRF funde rankings por posição; modelos temporais permitem distinguir validade e registro.
Suporte: related; fontes: A-S021, A-S032
Limite: A combinação, filtros e invariantes deste retriever são projeto editorial, não garantias dos produtos citados.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu filtros e ranking. Aqui Memory Retriever é proposto como serviço de evidência por requisito, com recuperação de apoio e contraposição.

Projeto e decomposição
Receba requisitos, não apenas uma string. O serviço deve distinguir localizar objeto exato, responder atributo, comparar alternativas e procurar evidência contrária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

Controle adaptativo
Distribua orçamento entre canais e fontes por contribuição exclusiva. Quando candidatos repetem mesma origem, ampliar diversidade pode ser mais útil que aumentar top-k do mesmo índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

Validação contrafactual
Compare busca global e recuperação por requisito. Meça cobertura de afirmações, evidências contraditórias encontradas e custo de expansão; não usar similaridade como substituto de validade. Unidade de avaliação: requisição de evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

USO AVANÇADO — Comparação de decisões
Cenário: Cada alternativa precisa suporte equivalente.
Estratégia: Criar consultas simétricas por critério, recuperar fontes independentes e devolver lacunas por alternativa antes da síntese.
Papel do modelo pequeno: 3–7B decompõe; 8–14B lê.
Aceite proposto: Nenhuma alternativa pode parecer melhor por ter sido mais pesquisada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

USO AVANÇADO — Correção de memória
Cenário: Fato antigo continua parecido com pergunta.
Estratégia: Aplicar validade e revisão antes de ranking, buscar também evento de correção e retornar conflito quando resolução ainda estiver pendente.
Papel do modelo pequeno: 15–30B integra histórico.
Aceite proposto: Resposta deve usar revisão elegível ou declarar insuficiência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V4A-S022, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reformulador de consultas fechadas e extrator de filtros.
8–14B: Leitor de candidatos com suporte e contradição rotulados.
15–30B: Planejador de busca multietapas para requisitos dependentes.
Requisitos de treino/runtime: Índices com origem, versões e elegibilidade; conjunto de consultas próprio para avaliar cobertura e abstenção.
Não aplicar quando: A fonte necessária não existe ou a recuperação é usada para modificar memória sem contrato de escrita.

## P007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Recuperador editorial pode adotar contrato semelhante, sem alegar adoção.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Inspira interface de recuperação; não comprova componente editorial.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q020.

## P007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P007 → T027 [complements]
Como combinar: Combinar canais conforme tipo de requisito.
Interface: Consulta, termos protegidos, filtros e orçamento.
Condição: Canais respeitarem mesma elegibilidade.
Aceite proposto: Testar código literal e paráfrase com orçamento igual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P007 → T028 [feeds]
Como combinar: Ordenar por capacidade de sustentar requisito.
Interface: Candidato, requisito, origem e tipo de suporte.
Condição: Contradições materiais não forem eliminadas.
Aceite proposto: Medir evidência suficiente na lista final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P007 → P001 [feeds]
Como combinar: Entregar evidências e lacunas à montagem.
Interface: requirement_id, trechos, referências e cobertura.
Condição: Builder preservar lacunas e conflitos.
Aceite proposto: Gerar pacote sem suporte para campo obrigatório e exigir insuficiência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V4A-S022, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não inferir ausência universal de resultado vazio.
- Não confundir múltiplos trechos da mesma fonte com corroboradores independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura por afirmação e fidelidade final; bom retriever amplia evidência disponível sem garantir capacidade geral do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T027, T032, T056, T067, P001, P004

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S020 — Retrieve & Re-Rank

[https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação inicial seguida de pontuação conjunta consulta-documento por cross-encoder.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S021 — Reciprocal rank fusion

[https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação por posições de múltiplos rankings, incluindo busca lexical e vetorial.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P008 — Event Store / Event Log

**Nome canônico:** Event Store / Event Log  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** armazenamento proposto de eventos; log proposto de eventos de estado

## P008:C01 — conceito

Event Store / Event Log é aqui o nome editorial de um componente arquitetural proposto. Armazenaria eventos duráveis usados para reconstruir estado e rastrear transições. Event sourcing é um padrão documentado, mas este componente LAI não foi verificado. Um log de diagnóstico só serve como origem de reconstrução se contiver todos os eventos e contratos necessários.

Como funciona:
- Representar cada mudança por evento com ID único, agregado, sequência, versão de schema e referências à causa e aos artefatos.
- Acrescentar eventos preservando o histórico lógico; correções de domínio entram como novos eventos que explicam a mudança.
- Reconstruir projeções por aplicação ordenada e usar snapshots vinculados a uma posição conhecida para acelerar a recuperação.

## P008:C02 — aplicacao

Quando usar:
- Fluxos que exigem retomada, explicação de decisões ou reconstrução do estado em pontos históricos.

Quando não usar:
- Quando apenas métricas agregadas são necessárias e o custo de evolução, retenção e replay não se justifica.

Implementação proposta:
- Proposta: estabelecer ordenação por agregado e controle de versão esperada; não assumir uma ordem global entre fontes independentes.
- Gravar estado local e evento de saída na mesma transação quando necessário, usando outbox para publicação posterior.
- Deduplicar consumidores por evento e testar migração de schemas; distinguir reprocessar projeções de reenviar efeitos externos.

Aplicação LAI proposta:
Proposta LAI: registrar transições do executor e versões de memória, oferecendo histórico e snapshots verificáveis aos componentes de continuidade.

## P008:C03 — riscos_validacao

Armadilhas:
- Entrega repetida pode duplicar projeções se o consumidor não for idempotente.
- Um snapshot sem sequência verificável pode pular eventos ou aplicá-los duas vezes.
- Append-only lógico não é, sozinho, garantia de proteção física contra alteração do armazenamento.

Métricas sugeridas:
- Atraso de consumo, eventos duplicados, lacunas de sequência e tempo de reconstrução por volume de histórico.

Testes propostos:
- Aceite proposto: reproduzir eventos até um cursor conhecido e comparar o estado com uma referência esperada.
- Entregar um evento duas vezes e interromper a publicação após o commit; a recuperação deve preservar uma única mudança lógica.

## P008:C04 — perguntas_proveniencia

Pergunta: Um arquivo de logs já é um event store suficiente?
Resposta: Somente se seus registros forem completos, duráveis, ordenáveis e interpretáveis para reconstruir o estado definido.

Pergunta: Replay deve executar novamente uma transferência externa?
Resposta: Não por padrão. Deve reconstruir o estado usando o resultado registrado; reexecutar efeitos requer protocolo próprio de reconciliação e idempotência.

Pergunta: Todo log permite replay?
Resposta: Não. Ele precisa conter os fatos necessários, sua ordem relevante e schemas interpretáveis.

Pergunta: O que torna a projeção recuperável?
Resposta: Eventos preservados, cursor consistente, projetor versionado e processamento repetível com deduplicação.

Escopo das fontes:
Fontes documentam eventos, replay e outbox; o componente e os requisitos LAI são propostos.

## P008:C05 — mecanismo_avancado

Event Store / Event Log é proposto como registro ordenado de fatos de execução, com ID do evento, entidade, sequência e versão de schema. Projeções devem guardar o último ponto aplicado e tolerar reentrega. Quando uma transação altera estado e precisa notificar outro sistema, uma outbox pode vincular a alteração ao evento pendente. A publicação posterior continua sujeita a duplicatas, portanto o consumidor precisa reconhecer eventos já processados.

Condição de contorno:
Um log de observabilidade não é automaticamente um histórico suficiente para reconstruir estado. Campos omitidos, eventos perdidos e mudanças de schema podem inviabilizar replay.

Contrato proposto:
- Entradas: Evento identificado, versão de schema, sequência por entidade, payload autorizado e revisão esperada.
- Saídas: Confirmação de gravação, posição no log e notificações ou projeções derivadas com seu próprio status.
- Estado: Eventos, offsets por consumidor, versões de projetores e chaves de deduplicação.
- Invariante: Uma projeção só avança o cursor quando aplica o evento de forma consistente; repetir o mesmo evento não deve duplicar seu efeito lógico.

Compromissos de projeto:
- Histórico completo facilita reconstrução e auditoria, mas aumenta custo e exige política de retenção compatível.
- Projeções assíncronas desacoplam consumidores e introduzem atraso que precisa ser exposto ao leitor.

## P008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: publicar o mesmo evento duas vezes, interromper consumidor após aplicar e antes de confirmar, e reaplicar desde snapshot; verificar estado final e cursor sem efeito duplicado.

Plano de avaliação proposto:
Comparar reconstrução integral e snapshot mais replay em sequência conhecida. Medir tempo de recuperação, atraso de projeções, divergências e compatibilidade após evolução de schema. Não afirmar exatamente uma vez para efeitos externos sem contrato adicional.

Comparações:
- T059 (complements): Event Sourcing utiliza eventos como fonte de reconstrução.
- T241 (complements): Replay consome o histórico com regras determinísticas e versionadas.

Afirmação rastreável:
A outbox grava alteração local e evento na mesma transação; consumidores ainda precisam tratar duplicatas.
Suporte: related; fontes: V3D-S018
Limite: O registro proposto exige decisões próprias de ordenação, retenção e evolução de schema.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P008:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a proposta Event Store com fronteira entre intenção e fato, causalidade parcial e replay sem repetir efeitos de negócio.

Envelope causal mínimo
Proposta: além da sequência por entidade, registrar causation_id, correlation_id e revisão observada. Esses campos permitem reconstruir dependências sem fingir uma ordem global de eventos simultâneos. Uma resposta de ferramenta pertence à intenção original mesmo se chegar em outra sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

Fato versus intenção
Usar tipos distintos para ação solicitada, envio iniciado, confirmação recebida e resultado reconciliado. A ausência de confirmação não é fato de falha. Esse desenho impede que um replay transforme um comando antigo em nova autorização para produzir efeito externo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

Projeções reexecutáveis
Versionar transformação e manter posição aplicada. Ensaiar reconstrução numa projeção separada antes de trocar consumidores. Eventos com dados sensíveis podem carregar referência e hash, preservando uma política explícita de retenção sem prometer apagar cópias fora do domínio controlado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

USO AVANÇADO — Memória de decisões do agente
Cenário: O sistema precisa explicar por que executou uma ação.
Estratégia: Persistir evidência e versão da política junto da transição; gerar resumo como projeção derivada.
Papel do modelo pequeno: 3–7B pode resumir a cadeia causal sem substituir o registro original.
Aceite proposto: Toda afirmação de ação concluída aponta para confirmação ou reconciliação registrada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

USO AVANÇADO — Reconstrução após bug de projeção
Cenário: Um extrator produziu estado derivado incorreto.
Estratégia: Corrigir a projeção, reproduzir eventos numa cópia e comparar diferenças antes de promover.
Papel do modelo pequeno: LLM revisa divergências sem criar novos fatos no histórico.
Aceite proposto: Replay não chama APIs mutantes e reconstrói estado segundo versão declarada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S018, V4C-S024, V4C-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: produzir eventos candidatos tipados; validação confirma o que pode ser persistido.
8–14B: 8–14B: interpretar cadeias curtas para diagnóstico e resumo com referências.
15–30B: 15–30B: análise de incidentes complexos, sem poder de reescrever o histórico factual.
Requisitos de treino/runtime: Persistência, schema e idempotência pertencem ao serviço; não dependem de parâmetros do modelo.
Não aplicar quando: Não usar texto de log livre como único contrato para reconstrução e auditoria.

## P008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Histórico e posições ilustram requisitos do event store editorial.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P008 é componente editorial. Brooklin e padrões de outbox sustentam analogias e partes do desenho, sem adoção de um produto LAI com esse nome.
Consultas registradas: V4C-Q002, V4C-Q020, V4C-Q019.

## P008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P008 → T059 [complements]
Como combinar: Definir quais eventos são fonte de verdade e quais são projeções.
Interface: Envelope versionado, sequência e identidade causal.
Condição: Estado precisa ser reconstruído.
Aceite proposto: Uma reconstrução completa tem critérios explícitos de equivalência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S018, V4C-S024, V4C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P008 → T241 [feeds]
Como combinar: Entregar eventos para reprodução em modo sem efeitos externos.
Interface: Histórico, cursor e versão da projeção.
Condição: Há recuperação ou correção de projeção.
Aceite proposto: Reexecução preserva fatos sem duplicar operações.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S018, V4C-S024, V4C-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir offset de transporte com confirmação de negócio.
- Não afirmar ordem causal total a partir apenas de timestamps.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas pela reconstrução correta e completude da evidência sob falhas. Mais memória textual não substitui eventos identificáveis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T162, T240, T241, T242, P011

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2C-S001 — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gravação de estado e evento de outbox na mesma transação; publicação posterior; duplicatas exigem consumidores idempotentes.

Limite: Fundamenta princípios de consistência. Não prova implementação, exatamente-uma-vez ponta a ponta ou resultado de desempenho na LAI.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### V3D-S018 — AWS — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alteração local e evento pendente na mesma transação; publicação posterior pode duplicar mensagens.

Limite: Outbox não torna toda chamada externa exatamente uma vez; consumidores precisam de idempotência.

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

# P009 — Inference Engine

**Nome canônico:** Inference Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P009  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de inferência

## P009:C01 — conceito

Inference Engine é um nome editorial proposto para a interface que executaria a geração no modelo selecionado. Sua responsabilidade seria transformar uma requisição válida em tokens, metadados de término e consumo observado. Implementações como vLLM ilustram princípios de serving, mas nenhuma integração LAI é afirmada; capacidades dependem do backend, versão, modelo e hardware escolhidos.

Como funciona:
- Validar compatibilidade entre modelo, tokenizer, template de conversa, limites e parâmetros de geração.
- Encaminhar requisições ao backend, que pode aplicar batching, cache KV e outros mecanismos suportados.
- Retornar texto ou eventos de streaming junto de motivo de término, contagem de tokens e identificador da execução.

## P009:C02 — aplicacao

Quando usar:
- Sistemas que precisam trocar backends mantendo um contrato uniforme de geração, cancelamento e observabilidade.

Quando não usar:
- Como substituto do roteador de modelos, da montagem de evidências ou da comprovação de correção da resposta.

Implementação proposta:
- Proposta: definir um adapter por backend com capacidades declaradas; rejeitar parâmetros incompatíveis em vez de ignorá-los silenciosamente.
- Encaminhar limite de saída, regras de parada e gramática somente quando suportados, preservando a diferença entre EOS, truncamento e cancelamento.
- Expor cancelamento e confirmar seu resultado; uma interrupção de streaming no cliente não prova liberação imediata do trabalho no servidor.

Aplicação LAI proposta:
Proposta LAI: consumir o pacote produzido por P001 e a escolha de P010, devolvendo ao executor resultados e razões de término verificáveis.

## P009:C03 — riscos_validacao

Armadilhas:
- Somar tempo de fila à geração sem identificá-los esconde a origem da latência.
- Cache compartilhado depende de compatibilidade de prefixo e configuração; não presumir acerto entre versões.
- JSON parcial após limite de tokens não deve ser tratado como resultado completo.

Métricas sugeridas:
- Tempo até primeiro token, intervalo entre tokens, duração em fila, throughput sob carga definida e taxa de término por limite.

Testes propostos:
- Aceite proposto: comparar resposta completa, saída truncada e geração cancelada, verificando estados e contabilização.
- Testar o mesmo contrato em dois backends e registrar diferenças de parâmetros e formatos, sem exigir igualdade literal entre amostras estocásticas.

## P009:C04 — perguntas_proveniencia

Pergunta: Streaming concluído significa resposta semanticamente correta?
Resposta: Não. Ele informa entrega e término; qualidade, evidência e correção dependem de verificações próprias.

Pergunta: Por que declarar capacidades por backend?
Resposta: Porque opções de gramática, cache, ferramentas e cancelamento variam; um contrato uniforme precisa expor essas diferenças.

Pergunta: Receber tokens significa que a tarefa terminou?
Resposta: Não. O término pode ser por limite, falha, cancelamento ou conclusão; o consumidor deve distingui-los.

Pergunta: Qual métrica evita confundir fila com geração?
Resposta: Registre tempos de admissão, início, primeiro token e término separadamente.

Escopo das fontes:
Fontes apoiam serving e controle de geração; adapter, contrato e integração LAI são propostas.

## P009:C05 — mecanismo_avancado

Inference Engine propõe uma interface que transforma uma requisição validada em geração observável. Deve distinguir aceitação na fila, início de execução, primeiro token, progresso, término e cancelamento. Tokens transmitidos antes de uma falha podem constituir saída parcial, não resposta concluída. O componente precisa manter separado o contrato comum da aplicação e as capacidades específicas de cada backend, incluindo schemas, ferramentas, cache e contagem de tokens.

Condição de contorno:
Um servidor com API semelhante pode interpretar parâmetros ou motivos de término de modo diferente. O adaptador precisa normalizar somente o que realmente compreende.

Contrato proposto:
- Entradas: Modelo e revisão, mensagens serializadas, parâmetros permitidos, limite de saída, deadline e identificador da requisição.
- Saídas: Eventos de geração, texto final ou parcial, motivo de término, uso e classificação de falha.
- Estado: Fila, requisições ativas, sessão do backend e mapa entre IDs internos e externos.
- Invariante: Cancelar ou falhar não pode produzir status de conclusão bem-sucedida; uso e saída parcial permanecem associados à tentativa correta.

Compromissos de projeto:
- Uma interface comum simplifica consumidores, mas pode ocultar recursos úteis se reduzir tudo ao menor denominador.
- Streaming reduz tempo até a primeira informação, sem eliminar necessidade de validar a resposta terminada.

## P009:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: derrubar a conexão após alguns tokens e atrasar o cancelamento; verificar classificação parcial, encerramento dos recursos e ausência de reenvio automático que duplique efeitos do consumidor.

Plano de avaliação proposto:
Comparar backends com mesmo contrato, checkpoint quando possível e carga controlada. Medir TTFT, latência entre tokens, total, erros, memória e respostas aceitas. Registrar campos não normalizáveis e capacidades indisponíveis.

Comparações:
- T153 (complements): Streaming com interrupção exige estados explícitos.
- R009 (complements): vLLM é uma implementação possível de serving, não o próprio contrato proposto.

Afirmação rastreável:
Servidores de inferência oferecem execução e agendamento com características dependentes do backend.
Suporte: related; fontes: V3D-S007, V3D-S012
Limite: A máquina de estados da interface é proposta editorial; não foi implantada neste trabalho.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P009:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu eventos e estados de geração. Esta proposta acrescenta qualificação de capacidades, orçamento de recursos e troca de backend com testes de contrato. O componente continua editorial, sem implantação LAI alegada.

Capabilities verificáveis
O engine proposto publica capacidades por modelo e versão: estrutura, ferramentas, cache, especulação, contexto e streaming. A presença de um campo na API não basta; um teste de integração deve confirmar comportamento. Recursos não suportados precisam gerar erro explícito ou alternativa documentada, sem degradação silenciosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012.

Orçamento por tentativa
Reserve prazo, saída máxima e recursos estimados antes de enviar. Registre fila, prefill, decode e cancelamento, mantendo tentativas separadas. Uma repetição pode gerar texto diferente e novo custo; o consumidor precisa saber se houve continuidade, reinício ou falha parcial.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012.

Backend como adaptador
Defina contrato comum mínimo e extensões específicas, evitando esconder diferenças semânticas de engines. vLLM, Transformers e llama.cpp ilustram implementações possíveis; os casos de seus operadores são analogias técnicas. A proposta LAI só ganha evidência de implementação depois de código, testes e execução próprios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012.

USO AVANÇADO — Serviço de modelos especializados
Cenário: Vários modelos 3–30B atendem tarefas diferentes.
Estratégia: Qualifique cada par modelo/backend, selecione por contrato e exponha estado completo. Preserve identidade de tokenizer, adapter e precisão para cache e métricas.
Papel do modelo pequeno: Um 3–7B pode assumir rotinas estreitas; modelos maiores ficam nos casos que justificam custo.
Aceite proposto: Nenhuma solicitação usa capacidade não comprovada e nenhum parcial é marcado concluído.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012.

USO AVANÇADO — Migração de runtime
Cenário: A equipe deseja trocar engine sem alterar consumidores.
Estratégia: Faça replay de contratos e testes de erro, depois compare carga. Mantenha compatibilidade explícita e rollback, registrando diferenças que exigem mudança do cliente.
Papel do modelo pequeno: Um 8–14B pode servir de candidato real; testes sintéticos não substituem sua execução.
Aceite proposto: Preservar semântica de término, cancelamento e ferramentas, além da qualidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Começar com uma réplica e contrato pequeno reduz complexidade sem impedir evolução.
8–14B: Adicionar cache, batching e quantização conforme gargalos medidos.
15–30B: Distribuição ou especulação só entram quando suporte e ganho líquido forem demonstrados.
Requisitos de treino/runtime: Proposta de camada de runtime; precisa de implementação e qualificação por ambiente, não treinamento em si.
Não aplicar quando: Não apresentar abstração editorial como engine já instalado nem prometer equivalência entre provedores.

## P009:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Deployment unit e saúde dos workers inspiram requisitos do engine proposto.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C010 — Hugging Face / HuggingChat — relato de 2023
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: O operador informou em 2023 que TGI alimentava HuggingChat e integrava seus serviços de inferência.
Mecanismo documentado: Servidor dedicado de geração com streaming e otimizações disponíveis na pilha; o relato identifica o runtime efetivamente usado.
Correspondência com esta base: Caso histórico de separação entre interface de chat e runtime de inferência.
Transferência proposta para modelo pequeno: Proposta: usar o caso como referência de migração e compatibilidade; novos serviços 3–30B devem considerar estado atual de manutenção e testar alternativas.
Limite: Não demonstra stack atual do HuggingChat. O maintenance mode documentado em 2026 é preservado, e disponibilidade histórica não é recomendação automática de nova adoção.
Fontes: V4B-S019, V3D-S006.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: Ilustra funções que a interface editorial Inference Engine poderia expor.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Ajuda a definir telemetria e capacidades distribuídas do componente editorial.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: Referência de contrato de transferência para um engine proposto.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: Ilustra capacidades que um adaptador de engine poderia negociar.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

V4B-C024 — Projeto llama.cpp / llama.cpp server
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.
Mecanismo documentado: Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.
Correspondência com esta base: Pode ser componente de uma proposta LAI; não é evidência de sua implantação.
Transferência proposta para modelo pequeno: Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.
Limite: README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.
Fontes: V3D-S012, B-S037.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014, V4B-Q026.

## P009:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P009 → R009 [alternative]
Como combinar: vLLM pode implementar parte do contrato de execução proposto.
Interface: Modelo, configuração e eventos normalizados.
Condição: Compatibilidade validada na versão real.
Aceite proposto: Testar casos normais, truncamento, falha e cancelamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P009 → R024 [alternative]
Como combinar: llama.cpp pode atender execução local quando suporta modelo e formato.
Interface: GGUF, build e limites de geração.
Condição: Contrato do cliente preservado.
Aceite proposto: Comparar memória, término e concorrência no dispositivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P009 → P016 [complements]
Como combinar: A avaliação proposta qualifica mudanças no engine antes da promoção.
Interface: Manifesto e resultados por caso.
Condição: Conjuntos separados de desenvolvimento e aceitação.
Aceite proposto: Rejeitar regressões de semântica mesmo com throughput maior.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4B-S010, V4B-S008, V4B-S014, V3D-S007, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter metadados de término obrigatórios no contrato.
- Não esconder fallback de precisão ou recurso em métricas agregadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a aplicação proposta com fronteira por tarefa, prazo e custo completo. Nenhuma combinação de runtimes prova paridade geral ou existência de uma implantação LAI.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T087, T088, T089, T102, T196, P001, P010

## Fontes primárias associadas

### B-S044 — vLLM — Welcome

[https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de inferência e serving com API, batching, gerenciamento KV e kernels especializados.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### D-S003 — Online Serving — vLLM

[https://docs.vllm.ai/en/latest/serving/online_serving/](https://docs.vllm.ai/en/latest/serving/online_serving/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: A documentação lista interfaces chat/completions e embeddings; geração exige modelo com chat template, embeddings exige modelo apropriado.

Limite: Confirma o contrato geral da interface; nenhum servidor real do usuário foi conectado ou homologado.

### B-S009 — Generation — GenerationConfig

[https://huggingface.co/docs/transformers/main_classes/text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Critérios de parada, limite de novos tokens e semântica específica de early_stopping em beam search.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S007 — TensorRT-LLM — Architecture Overview

[https://nvidia.github.io/TensorRT-LLM/latest/torch/arch_overview.html](https://nvidia.github.io/TensorRT-LLM/latest/torch/arch_overview.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: PyTorch como único backend atual, remoção do caminho legado e organização dos componentes de execução.

Limite: Página latest; versões históricas podem manter outra arquitetura. Não houve benchmark GPU.

### V3D-S012 — llama.cpp HTTP server — README

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor com caminhos CPU/GPU, geração paralela e batching contínuo.

Limite: Arquivo master; recursos dependem do build, backend e arquitetura do modelo.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### B-S037 — GGUF specification

[https://github.com/ggml-org/ggml/blob/master/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formato binário de modelos, tensores e metadados; não é por si só um algoritmo de quantização.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S006 — Text Generation Inference — maintenance status

[https://huggingface.co/docs/text-generation-inference/en/index](https://huggingface.co/docs/text-generation-inference/en/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estado de manutenção do TGI com correções menores, documentação e tarefas leves.

Limite: Estado documental verificado em 2026-11-05; não demonstra interrupção de serviço existente.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

### V4B-S019 — Open-Source Text Generation & LLM Ecosystem at Hugging Face

[https://huggingface.co/blog/os-llms](https://huggingface.co/blog/os-llms)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico do operador de TGI servindo HuggingChat e integração nos serviços de inferência.

Limite: Fonte histórica; não prova stack atual do HuggingChat nem cancela estado atual de manutenção do TGI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P010 — Routing Engine

**Nome canônico:** Routing Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P010  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de roteamento de modelos

## P010:C01 — conceito

Routing Engine é um nome editorial proposto para escolher uma rota de execução compatível com a tarefa e seu orçamento. Pode decidir modelo, endpoint e alternativa elegível. RouteLLM e cascatas fornecem fundamentos relacionados; não demonstram que este componente exista na LAI nem que um roteador aprendido supere uma política simples no acervo do usuário.

Como funciona:
- Eliminar rotas incompatíveis com tamanho de contexto, ferramentas, formato exigido e disponibilidade operacional.
- Entre as rotas elegíveis, considerar estimativas de qualidade, custo, latência e capacidade observada.
- Registrar a razão da escolha e os critérios para escalonamento ou fallback, sem formar ciclos de tentativas.

## P010:C02 — aplicacao

Quando usar:
- Cargas heterogêneas em que modelos ou serviços têm custos e desempenhos diferentes mensuráveis.

Quando não usar:
- Quando não há avaliação representativa para sustentar alegações de qualidade equivalente entre rotas.

Implementação proposta:
- Proposta: começar com uma política determinística baseada em capacidades e classes de tarefa, versionando cada decisão.
- Construir comparação offline com um baseline único antes de adotar roteamento aprendido ou limiares mais complexos.
- Se uma resposta falhar na verificação, permitir escalonamento com orçamento restante e transferir evidências suficientes para a nova rota.

Aplicação LAI proposta:
Proposta LAI: P010 escolhe a rota; P009 executa; P012 devolve sinais verificáveis de aceitação; P016 avalia a política em dados separados.

## P010:C03 — riscos_validacao

Armadilhas:
- Confiança declarada pelo próprio modelo não equivale a probabilidade calibrada de acerto.
- Um fallback mais barato pode perder suporte a ferramentas ou truncar o contexto.
- Rotear sem contabilizar tentativas anteriores pode aumentar custo total apesar de reduzir o preço por chamada.

Métricas sugeridas:
- Qualidade por classe de tarefa, custo por resultado aceito, latência final e taxa de escalonamento.

Testes propostos:
- Aceite proposto: tornar o endpoint preferido indisponível e exigir uma alternativa com as mesmas capacidades obrigatórias.
- Comparar política e baseline em conjunto separado por projeto ou período, incluindo perguntas difíceis e casos sem rota elegível.

## P010:C04 — perguntas_proveniencia

Pergunta: Modelo barato deve receber automaticamente toda tarefa curta?
Resposta: Não. Tamanho é apenas um sinal; uma tarefa curta pode exigir capacidade específica ou verificação rigorosa.

Pergunta: Como julgar economia real de uma rota?
Resposta: Pelo custo total até um resultado aceito, incluindo respostas rejeitadas, reruns, ferramentas e escalonamentos.

Pergunta: Qual objetivo otimizar?
Resposta: Custo e tempo para uma tarefa aceita, preservando requisitos e limites de erro.

Pergunta: Como impedir loops de fallback?
Resposta: Registre rotas visitadas, orçamento global, deadline e motivo final quando não resta opção válida.

Escopo das fontes:
Fontes sustentam roteamento, calibração e avaliação; política LAI e limiares exigem validação própria.

## P010:C05 — mecanismo_avancado

Routing Engine propõe escolher uma rota sob restrições de capacidade, orçamento, qualidade e disponibilidade. A decisão deve guardar quais candidatos foram elegíveis e por que um foi selecionado. Uma estimativa de dificuldade ou confiança precisa ser calibrada no domínio; um número alto emitido pelo próprio modelo não basta. Fallback deve consumir um orçamento global e preservar requisitos, evitando alternância infinita entre provedores que falham da mesma forma.

Condição de contorno:
Uma rota mais barata por chamada pode aumentar custo total se produzir mais respostas rejeitadas ou exigir escalonamento frequente. A métrica principal precisa considerar resultado aceito.

Contrato proposto:
- Entradas: Tarefa, capacidades exigidas, orçamento restante, deadline, saúde dos candidatos e versão da política de roteamento.
- Saídas: Rota escolhida ou impossibilidade explícita, justificativa, limite de tentativas e critério de escalonamento.
- Estado: Histórico de desempenho por tipo de tarefa, calibração, custos e tentativas já consumidas na operação.
- Invariante: Nenhuma troca de rota pode relaxar silenciosamente um requisito obrigatório nem reiniciar o orçamento de retries.

Compromissos de projeto:
- Um classificador adicional custa latência e pode compensar quando evita uso excessivo de modelos caros.
- Cascatas economizam em casos simples, mas acumulam custo e atraso quando a maioria exige escalonamento.

## P010:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: tornar indisponível a rota preferida e oferecer fallback sem a capacidade requerida; exigir rejeição clara, sem apresentar saída degradada como equivalente.

Plano de avaliação proposto:
Comparar roteador com uma rota fixa forte e outra econômica no mesmo conjunto reservado. Medir custo por tarefa aceita, erro, latência de cauda, taxa de escalonamento e calibração. Incluir períodos de indisponibilidade simulada.

Comparações:
- T133 (specializes): É um componente proposto para escolher modelos.
- T203 (complements): Roteamento por correção pode fornecer sinal de aceitação ou escalonamento.

Afirmação rastreável:
Pesquisas de roteamento e cascatas estudam trocas entre custo e qualidade; calibração exige avaliação.
Suporte: related; fontes: C-S001, C-S002, C-S050
Limite: O contrato aqui não reproduz um algoritmo específico nem promete ganhos dos artigos no domínio do usuário.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P010:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o roteador proposto com seleção sob restrições, aprendizado sem viés de sobreviventes e separação entre dificuldade estimada e falha de infraestrutura.

Elegibilidade antes do ranking
Proposta: filtrar modelos por contrato de ferramenta, tamanho de entrada, prazo e requisitos de dados antes de prever qualidade/custo. Um candidato barato porém incapaz do formato não é uma rota válida. Registrar o conjunto excluído ajuda a explicar decisões e detectar configurações desatualizadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

Feedback com censura
Guardar resultado de todas as tentativas, inclusive timeout, abstenção e escalada. Avaliar apenas tarefas aceitas pelo modelo pequeno cria seleção favorável. Amostras controladas em shadow, sem efeitos duplicados, podem estimar o desempenho das rotas não escolhidas; isso ainda exige desenho experimental adequado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

Razão de escalada
Separar erro estrutural, evidência insuficiente, tarefa fora do domínio e indisponibilidade. Cada razão sugere uma ação diferente: reparar contexto, trocar ferramenta, usar modelo maior ou aguardar capacidade. Trocar modelo para qualquer erro pode apenas repetir a falha compartilhada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

USO AVANÇADO — Extração de contratos com exceções
Cenário: Maioria dos documentos segue padrões; poucos exigem interpretação difícil.
Estratégia: Extrair com modelo pequeno, verificar campos e escalar apenas os casos de ambiguidade definidos.
Papel do modelo pequeno: 3–14B atende o fluxo comum com evidência por campo.
Aceite proposto: Medir cobertura, erro residual e custo total, incluindo casos escalados e revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

USO AVANÇADO — Serviço sob fila longa
Cenário: A rota habitual ultrapassa o prazo disponível.
Estratégia: Escolher somente alternativa que preserve requisito; caso contrário adiar ou recusar explicitamente.
Papel do modelo pequeno: Classificador pequeno estima tipo de tarefa; fila/deadline vêm da telemetria.
Aceite proposto: Nenhuma mudança silenciosa de qualidade contratada e p95 dentro do limite declarado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: tarefas estáveis e classificação de rota com calibração local.
8–14B: 8–14B: rota principal de tarefas especializadas com ferramentas e validação.
15–30B: 15–30B: escalada intermediária avaliada contra o custo de fronteira ou revisão humana.
Requisitos de treino/runtime: Calibrar usando resultados reais da política e controlar mudança de distribuição.
Não aplicar quando: Não usar autoconfiança verbal do modelo como probabilidade calibrada de sucesso.

## P010:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C013 — Uber / GenAI Gateway
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A Uber relata equipes internas utilizando o gateway para consultas a modelos externos e hospedados internamente.
Mecanismo documentado: Adaptadores expõem uma interface comum e integram autenticação, política de dados, métricas e atribuição de custos.
Correspondência com esta base: O gateway é referência para infraestrutura de rotas, não valida o motor editorial completo.
Transferência proposta para modelo pequeno: Proposta: centralizar adapters de 3–30B e registrar capacidades reais de cada endpoint; separar seleção do modelo da tradução de protocolos e da medição do custo por tarefa aceita.
Limite: Interface compatível não torna modelos semanticamente equivalentes. Não mapear automaticamente disponibilidade de múltiplos fornecedores a cascata ou fallback comprovado.
Fontes: V4C-S012.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Seleção por resultado é referência para o roteador editorial.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C012 — Amazon Web Services / Amazon Bedrock Intelligent Prompt Routing
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação disponibiliza um endpoint de roteamento que prevê qualidade e escolhe entre dois modelos compatíveis da mesma família.
Mecanismo documentado: Configuração define modelos, critério e fallback; resposta informa o modelo usado. A página é documentação de produto, não relato de implantação de um cliente.
Correspondência com esta base: O serviço oferece referência para um componente editorial de roteamento.
Transferência proposta para modelo pequeno: Proposta: comparar um roteador local 3–30B com regras simples, rotas fixas e escalonamento após validação. Rejeitar candidatos sem capacidade necessária antes de estimar qualidade.
Limite: Classificado como operational_product. Não conta para dez casos comprovados em produção; lista de modelos e regiões muda. Exemplos com modelos maiores não validam as bandas pequenas.
Fontes: V4C-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P010 é proposta. Bedrock oferece recurso de roteamento; relatos Uber têm escopos próprios e não comprovam automaticamente roteamento dinâmico por dificuldade.
Consultas registradas: V4C-Q008, V4C-Q009.

## P010:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P010 → T133 [complements]
Como combinar: Implementar a política de escolha como decisão rastreável.
Interface: Candidatos elegíveis, scores, motivo e orçamento.
Condição: Existe heterogeneidade real de tarefas e modelos.
Aceite proposto: Reproduzir a decisão a partir de entradas e versão da política.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V4C-S011, V4C-S012, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P010 → T203 [complements]
Como combinar: Usar verificação de correção para orientar nova rota.
Interface: Critério falho, evidência e tentativas anteriores.
Condição: Há verificador útil e escalada permitida.
Aceite proposto: A escalada reduz erro medido sem exceder orçamento de tarefa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V4C-S011, V4C-S012, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não treinar o roteador somente em sucessos publicados.
- Não contar economia por chamada ignorando retries e professor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar política completa contra modelo único nos mesmos pedidos, incluindo seleção e abstinência. Medir não inferioridade por subgrupo, custo por aceite e cauda de latência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T136, T198, T203, P009, P012, P016

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S002 — FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

[https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cascatas de modelos e decisões de encaminhamento podem ser otimizadas sob orçamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P011 — Execution Engine / Execution Controller

**Nome canônico:** Execution Engine / Execution Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P011  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** executor proposto de workflows; controlador proposto de execução

## P011:C01 — conceito

Execution Engine / Execution Controller é um nome editorial proposto para conduzir etapas de trabalho até estados verificáveis. Coordenaria dependências, execução de ferramentas, espera e retomada. Fontes de workflows duráveis sustentam esses princípios, mas não comprovam um executor LAI implementado; paralelismo e agentes adicionais só seriam utilizados quando o contrato da tarefa os permitisse.

Como funciona:
- Representar cada tarefa por estado, entradas versionadas, dependências, limites e resultado esperado.
- Liberar etapas cujas dependências estejam satisfeitas e registrar tentativas separadamente do efeito lógico solicitado.
- Persistir transições relevantes e resultados externos para retomar sem confundir histórico reconstruído com nova execução.

## P011:C02 — aplicacao

Quando usar:
- Processos com múltiplas etapas, chamadas demoradas, interrupções ou necessidade de continuidade entre sessões.

Quando não usar:
- Como substituto da definição de objetivo ou como licença para repetir automaticamente operações de resultado desconhecido.

Implementação proposta:
- Proposta: definir uma máquina de estados com planejado, pronto, executando, aguardando, confirmado, falho e resultado desconhecido.
- Associar cada efeito à sua chave de intenção e registrar checkpoint com cursor de eventos e versão de artefatos.
- Ao retomar, reconciliar recibos e estado remoto antes de repetir ações ambíguas; propagar cancelamento às tarefas filhas e registrar o alcance confirmado.

Aplicação LAI proposta:
Proposta LAI: P011 conecta contexto, inferência e ferramentas, usando P008 para histórico, P013 para recuperação e P015 para integridade dos efeitos.

## P011:C03 — riscos_validacao

Armadilhas:
- Um timeout local não informa se o serviço remoto realizou a operação.
- Paralelizar etapas que escrevem o mesmo recurso sem controle de concorrência pode invalidar ambas.
- Replay de workflow precisa tratar entradas não determinísticas e evolução do código conforme o runtime adotado.

Métricas sugeridas:
- Etapas concluídas por objetivo, retomadas corretas, efeitos duplicados e tempo gasto aguardando dependências.

Testes propostos:
- Aceite proposto: interromper uma etapa antes e depois da confirmação externa e verificar recuperação sem repetição indevida.
- Executar duas etapas concorrentes sobre a mesma versão de artefato; exigir conflito ou serialização prevista pelo contrato.

## P011:C04 — perguntas_proveniencia

Pergunta: Uma etapa em execução pode ser marcada concluída ao reconectar?
Resposta: Somente com evidência de seu resultado ou regra de conclusão satisfeita; falta de conexão não determina o desfecho.

Pergunta: Quando executar tarefas em paralelo?
Resposta: Quando suas dependências e efeitos forem independentes ou houver um protocolo explícito de concorrência para os recursos compartilhados.

Pergunta: Checkpoint permite repetir qualquer etapa?
Resposta: Não. Primeiro determine se a etapa já causou um efeito externo e como o destino trata repetição.

Pergunta: Quando declarar conclusão?
Resposta: Quando critérios e efeitos necessários estiverem confirmados, com pendências ambíguas explicitamente resolvidas.

Escopo das fontes:
Fontes apoiam workflows e idempotência; estados e integração do executor são propostas editoriais.

## P011:C05 — mecanismo_avancado

Execution Engine / Execution Controller propõe coordenar etapas duráveis com identidade e estado explícitos. Antes de um efeito externo, registra intenção e chave estável da operação; depois distingue confirmação, falha conhecida e resultado ambíguo. Reiniciar o processo não autoriza repetir automaticamente um efeito cujo sucesso é desconhecido. A retomada deve consultar o destino quando possível ou entrar em reconciliação, mantendo a decisão de negócio separada do mecanismo de replay.

Condição de contorno:
Durabilidade local e replay não garantem atomicidade com um serviço externo. APIs sem idempotência ou consulta de status podem exigir intervenção ou compensação definida pelo domínio.

Contrato proposto:
- Entradas: Plano versionado, etapas elegíveis, estado persistido, deadline, políticas e identificadores de operações externas.
- Saídas: Transições confirmadas, artefatos, pendências de reconciliação e resultado final verificável da tarefa.
- Estado: Histórico de execução, checkpoints, resultados registrados, leases e intenções ainda sem confirmação.
- Invariante: Retomada não pode transformar ausência de confirmação em autorização para repetir um efeito irreversível.

Compromissos de projeto:
- Persistir fronteiras reduz trabalho perdido, mas adiciona escrita e exige compatibilidade de versões do fluxo.
- Atividades pequenas facilitam retomada, porém podem aumentar coordenação e custo de armazenamento.

## P011:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: encerrar o worker após o serviço externo confirmar a ação, mas antes da gravação local; ao retomar, exigir consulta ou deduplicação e impedir segunda ação lógica.

Plano de avaliação proposto:
Comparar execução somente em memória e execução com fronteiras duráveis em pontos de falha definidos. Medir trabalho refeito, efeitos duplicados, tempo de recuperação e operações ambíguas resolvidas. Fixar as garantias reais do destino externo.

Comparações:
- T159 (complements): Execução durável fornece persistência e retomada.
- T243 (complements): Reconciliação resolve a fronteira entre intenção local e efeito externo.

Afirmação rastreável:
Temporal exige determinismo compatível com o histórico e separa operações externas em Activities.
Suporte: related; fontes: V3D-S019
Limite: O controlador proposto não herda garantias automaticamente; precisa respeitar contratos do runtime e dos destinos.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P011:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o executor proposto com posse temporária de tarefas, fencing e commits de resultado vinculados à revisão do plano.

Posse e fencing
Proposta: concessão temporária identifica o worker autorizado e recebe uma época monotônica. Após expiração, um worker antigo pode continuar vivo; o destino precisa validar a época antes de aceitar escrita. Um lease local sozinho não impede efeitos de um executor atrasado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S019, C-S026, V4C-S001, V4C-S004.

Commit de etapa
Separar produzir candidato, verificar candidato e publicar resultado. O commit inclui revisão do plano e do estado de entrada. Uma mudança de objetivo invalida trabalhos pendentes sem apagar sua evidência. Operações externas ainda exigem identidade estável e reconciliação própria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S019, C-S026, V4C-S001, V4C-S004.

Decomposição com barreiras
Executar em paralelo apenas etapas com dependências satisfeitas e recursos compatíveis. A barreira não significa simplesmente esperar todos os textos: precisa decidir quorum, resultados obrigatórios e tratamento de falha parcial conforme a tarefa. Cancelar um ramo não desfaz efeito já confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S019, C-S026, V4C-S001, V4C-S004.

USO AVANÇADO — Processamento de lotes documentais
Cenário: Workers podem cair durante extração e validação.
Estratégia: Conceder tarefas por lease, persistir candidato e confirmar somente com época vigente.
Papel do modelo pequeno: 3–7B extrai campos; controlador determina publicação.
Aceite proposto: Worker antigo não sobrescreve resultado novo após reatribuição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S019, C-S026, V4C-S001, V4C-S004.

USO AVANÇADO — Plano de manutenção com ações externas
Cenário: Algumas etapas apenas leem; outras alteram recursos.
Estratégia: Separar fases de preparação e commit e preservar resultado ambíguo para reconciliação.
Papel do modelo pequeno: 8–30B propõe etapas; contratos executáveis limitam transições e efeitos.
Aceite proposto: Falhas entre preparação e confirmação não duplicam ações nem marcam conclusão indevida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S019, C-S026, V4C-S001, V4C-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: trabalhadores estreitos com contrato explícito de entrada/saída.
8–14B: 8–14B: planos curtos e verificáveis, executados por máquina de estados externa.
15–30B: 15–30B: decomposição de maior alcance somente se invariantes e testes limitarem o erro.
Requisitos de treino/runtime: Lease, fencing e persistência dependem dos serviços participantes; não são garantias da LLM.
Não aplicar quando: Não paralelizar etapas que disputam o mesmo estado sem protocolo de concorrência.

## P011:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Orquestração de etapas inspira o executor editorial.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C016 — LinkedIn / Microsoft / Hiring Assistant
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.
Mecanismo documentado: Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.
Correspondência com esta base: Ciclo de vida e mailbox inspiram responsabilidades do executor proposto.
Transferência proposta para modelo pequeno: Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.
Limite: Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.
Fontes: V4C-S015.

V4C-C005 — Netflix / Timestone
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.
Mecanismo documentado: Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.
Correspondência com esta base: Admissão e exclusão por chave apoiam o desenho proposto do executor.
Transferência proposta para modelo pequeno: Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.
Limite: EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.
Fontes: V4C-S003.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: O motor inspira responsabilidades do executor editorial.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Plataforma de workflows é referência para o controlador editorial.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P011 permanece componente proposto. Cadence, Conductor e fluxos internos fornecem referências operacionais, não adoção literal deste controlador.
Consultas registradas: V4C-Q002, V4C-Q003, V4C-Q012.

## P011:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P011 → T159 [complements]
Como combinar: Persistir transições e resultados necessários à retomada.
Interface: Task_id, etapa, época, revisão e resultado.
Condição: Execução deve sobreviver ao processo.
Aceite proposto: Retomada identifica a última etapa confirmada sem confiar no texto final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S019, C-S026, V4C-S001, V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P011 → T243 [feeds]
Como combinar: Encaminhar efeitos sem confirmação para investigação de status.
Interface: Identidade da operação e provas de envio/retorno.
Condição: Destino externo pode completar após timeout.
Aceite proposto: O executor não resolve ambiguidade repetindo cegamente a ação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S019, C-S026, V4C-S001, V4C-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não afirmar fencing se o destino não valida o token.
- Não considerar cancelamento como compensação de efeito já ocorrido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar conclusão correta sob workers duplicados, atraso e mudança de plano. Medir trabalho descartado e efeitos indevidos além de throughput.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T159, T160, T162, P008, P013, P015

## Fontes primárias associadas

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S013 — Workflows and agents

[https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento e arestas condicionais selecionam fluxos conforme estado ou classificação da entrada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3D-S019 — Temporal — Workflow Definition

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Determinismo de comandos em relação ao histórico, versionamento e fronteira de Activities para operações externas.

Limite: Requisitos do runtime não garantem idempotência de efeitos externos sem contrato do destino.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S004 — Netflix Conductor: The Next Chapter

[https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operação de Conductor na Netflix, integração Timestone, avaliação assíncrona, dados de tarefas carregados sob demanda e sequenciamento por chave.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads

[https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filas por deadline e filas exclusivas usadas por Cosmos, Conductor e pipelines; consistência, atribuição de trabalho e persistência.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto em disponibilidade global com planner–executor, subagentes como ferramentas, mailbox e operações assíncronas.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P012 — Verification Engine / Verification Controller

**Nome canônico:** Verification Engine / Verification Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de verificação de resultados; controlador proposto de verificação

## P012:C01 — conceito

Verification Engine / Verification Controller é um nome editorial proposto para verificar um resultado concreto antes de aceitá-lo no fluxo. Reuniria verificadores adequados ao artefato: schema, evidência documental, execução e regras de domínio. As fontes fundamentam essas classes de teste; não comprovam um componente LAI existente nem um verificador universal capaz de demonstrar qualquer alegação.

Como funciona:
- Receber candidato, contrato de aceitação, versão das entradas e evidências necessárias à decisão.
- Aplicar verificações estruturais e semânticas separadas; executar testes quando houver um ambiente e um oráculo apropriados.
- Devolver aprovado, reprovado ou inconclusivo, com motivos, evidências e limites do que foi verificado.

## P012:C02 — aplicacao

Quando usar:
- Respostas factuais com fontes, patches de código, chamadas estruturadas e artefatos com critérios de correção definidos.

Quando não usar:
- Para declarar correto um resultado apenas porque outro modelo concordou ou porque o JSON passou na validação.

Implementação proposta:
- Proposta: selecionar verificadores por tipo de saída e registrar versões dos testes, dados e ferramentas utilizados.
- Separar o produtor do candidato dos critérios de avaliação; quando possível, usar casos que não tenham sido vistos durante sua construção.
- Quando faltar uma fonte ou um teste não puder executar, marcar a dimensão como inconclusiva em vez de fabricar aprovação.

Aplicação LAI proposta:
Proposta LAI: verificar saídas do P011 e alimentar escalonamento de P010, anexando um recibo de verificação ao artefato avaliado.

## P012:C03 — riscos_validacao

Armadilhas:
- Testes gerados a partir da mesma implementação podem reproduzir seu erro e passar sem verificar o requisito.
- Uma resposta pode ser estruturalmente válida e conter fatos falsos ou referências inexistentes.
- Aprovação parcial não deve ser apresentada como cobertura integral de todos os requisitos.

Métricas sugeridas:
- Falsas aceitações e rejeições em conjunto rotulado, cobertura de requisitos e frequência de resultados inconclusivos.

Testes propostos:
- Aceite proposto: fornecer JSON válido com um ID inexistente e exigir falha na verificação semântica.
- Introduzir um defeito conhecido e um teste indisponível; o relatório deve separar reprovação comprovada de dimensão não avaliada.

## P012:C04 — perguntas_proveniencia

Pergunta: Validar schema confirma a verdade do conteúdo?
Resposta: Não. Schema verifica restrições estruturais; existência, veracidade e cumprimento do requisito exigem verificadores adicionais.

Pergunta: O que fazer quando o ambiente de teste falha?
Resposta: Registrar que a verificação não foi concluída nessa dimensão; falha do teste não é evidência suficiente de aprovação ou defeito do artefato.

Pergunta: Uma aprovação pode ser reutilizada após editar o arquivo?
Resposta: Somente se o contrato provar equivalência relevante; por padrão a mudança exige nova verificação.

Pergunta: Como representar falta de evidência?
Resposta: Use estado não verificável e liste a lacuna, sem converter ausência de falha em aprovação.

Escopo das fontes:
Fontes apoiam verificadores e avaliação; agregação, estados e integração LAI são propostas editoriais.

## P012:C05 — mecanismo_avancado

Verification Engine / Verification Controller propõe produzir decisões acompanhadas de evidência, distinguindo aprovado, reprovado e não verificável. Cada verificação deve identificar o artefato exato, idealmente por hash, o critério, a versão do verificador e o resultado. Validar um objeto JSON só cobre as regras expressas pelo schema; não comprova execução de uma ação nem verdade factual. Verificadores independentes precisam reduzir dependência de premissas compartilhadas, não apenas repetir a mesma pergunta.

Condição de contorno:
Um verificador pode ter falsos positivos e negativos. Quando depende de modelo, sua concordância com o gerador não é prova suficiente de correção.

Contrato proposto:
- Entradas: Artefato identificado, critérios de aceite, evidências autorizadas, ambiente de teste e orçamento de verificação.
- Saídas: Decisão por critério, evidência reproduzível, lacunas e motivos de insuficiência ou rejeição.
- Estado: Versões de verificadores, resultados anteriores por hash e dependências usadas para avaliar o artefato.
- Invariante: Qualquer alteração no artefato ou critério invalida a aprovação que se referia à versão anterior.

Compromissos de projeto:
- Verificação por execução pode ser forte para propriedades testáveis, mas depende da cobertura e do ambiente.
- Múltiplos verificadores aumentam custo; correlação entre seus erros pode limitar o ganho real.

## P012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: validar um artefato, modificá-lo e tentar reutilizar o laudo antigo; exigir invalidação. Incluir saída com schema válido e regra de negócio violada para confirmar separação das verificações.

Plano de avaliação proposto:
Comparar verificação estrutural, testes executáveis e avaliação semântica em conjunto com defeitos conhecidos. Medir falsos aceites, rejeições indevidas, custo e cobertura por critério. Reservar casos que não orientaram a construção dos verificadores.

Comparações:
- T197 (complements): JSON Schema cobre uma parte estrutural do contrato.
- T200 (complements): Verificação independente pode reduzir erros compartilhados quando usa evidência distinta.

Afirmação rastreável:
JSON Schema define validação estrutural; estudos de avaliação de código mostram a necessidade de testes discriminativos.
Suporte: related; fontes: C-S049, C-S048
Limite: A composição de verificadores e o vínculo por hash são propostas de engenharia, não resultados experimentais apresentados aqui.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P012:C07 — estrategia_3_30b

NOVA CAMADA v4 — Avança além de cobertura, hashes e independência já tratados na v3: propõe cascatas de verificação por risco, auditoria amostral das respostas aceitas e testes contra exploração do próprio verificador.

Cascata com abstenção calibrada
Proposta: ordenar verificadores por custo e poder discriminativo medidos no domínio. Um teste barato pode reprovar cedo; sua aprovação não encerra automaticamente casos de alto risco. Calibrar limiares numa divisão de desenvolvimento e congelá-los antes da avaliação final. Medir curva de cobertura versus erro entre aceitos, incluindo o custo dos verificadores adicionais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

Auditoria depois do aceite
Revisar uma amostra dos itens que passaram, incluindo respostas de alta confiança. Amostrar apenas rejeições deixa os falsos aceites invisíveis. Se erros raros forem superamostrados, guardar probabilidades de inclusão e reportar estratos separadamente ou ponderar a estimativa; não apresentar a amostra enriquecida como frequência natural do tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

Exploração do juiz e testes discriminativos
Um gerador ajustado repetidamente ao mesmo juiz pode melhorar a pontuação sem melhorar o requisito. Manter testes finais fora do loop de ajuste e introduzir negativos conhecidos e transformações metamórficas cuja invariância seja justificada pelo domínio. Mutantes equivalentes ou transformações inválidas devem ser excluídos antes de julgar a qualidade do verificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

USO AVANÇADO — Leitor pequeno com escalada seletiva
Cenário: Grande volume de respostas factuais permite auditoria humana limitada.
Estratégia: Executar checagem barata, escalar classes difíceis e auditar aleatoriamente parte dos aceitos; revisar política apenas fora da avaliação congelada.
Papel do modelo pequeno: 3–14B gera ou classifica alegações; aceitação depende da política calibrada, não de autoconfiança verbal.
Aceite proposto: Estimar falsos aceites por classe e custo por resultado correto; publicar cobertura e quantidade enviada à revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

USO AVANÇADO — Código que aprende a passar no juiz
Cenário: Repetidos reparos usam retorno de testes conhecidos e podem explorar lacunas.
Estratégia: Separar feedback de desenvolvimento e testes finais; usar entradas metamórficas válidas e defeitos semânticos rotulados para medir discriminação.
Papel do modelo pequeno: Modelo pequeno propõe candidatos; um executor compara propriedades independentes da pontuação narrativa.
Aceite proposto: Detectar defeitos inseridos sem reprovar transformações equivalentes; congelar avaliação após escolhas de hiperparâmetros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, C-S050, V4C-S009, C-S049.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: primeiro estágio barato quando sua taxa de falsos aceites estiver medida; abstenção deve ser permitida.
8–14B: 8–14B: juiz especializado de evidência em domínio estreito, sujeito a auditoria de exemplos aceitos.
15–30B: 15–30B: estágio adicional para classes difíceis apenas se o ganho discriminativo compensar custo e correlação.
Requisitos de treino/runtime: Exige rótulos independentes, política versionada, amostragem conhecida e avaliação separada do ajuste.
Não aplicar quando: Não otimizar indefinidamente no mesmo juiz ou tratar taxa de aprovação como qualidade verdadeira.

## P012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: Compilação e testes exemplificam critérios de aceite.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Rubricas de avaliação ilustram verificações propostas, não o produto editorial LAI.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Validação vinculada à revisão e ao responsável inspira o gate editorial.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: A cadeia de verificações exemplifica o componente editorial.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Gates verificáveis inspiram o componente editorial.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Critérios de gate ilustram um verificador editorial.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: O gate de propriedades inspira o componente proposto, sem demonstrar um produto LAI.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P012 é proposta. AutoClean, Tricorder e reparadores industriais mostram mecanismos delimitados; não confirmam um verificador universal ou produto LAI.
Consultas registradas: V4C-Q005, V4C-Q007, V4C-Q011.

## P012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P012 → T198 [complements]
Como combinar: Usar calibração empírica para definir quando aceitar, verificar novamente ou abster-se.
Interface: Score, classe da tarefa, versão da calibração e rótulos externos.
Condição: Há dados representativos suficientes para avaliar erro entre aceitos.
Aceite proposto: Curvas por classe mostram cobertura e erro; limiares não são escolhidos no conjunto final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, C-S050, V4C-S009, C-S049. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P012 → T205 [complements]
Como combinar: Aplicar equivalências justificadas como testes metamórficos do candidato e do juiz.
Interface: Transformação, precondições e propriedade que deve permanecer.
Condição: O domínio oferece relações semânticas conhecidas.
Aceite proposto: O sistema distingue violações reais de mudanças equivalentes sem depender de igualdade textual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, C-S050, V4C-S009, C-S049. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar ausência de erro numa amostra pequena como risco zero.
- Não somar votos correlacionados como se fossem ensaios independentes.
- Não esconder timeouts e abstinências ao calcular custo e cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar candidato 3–30B e baseline na mesma política, depois ablar a cascata. Auditar falsos aceites também na rota de fronteira; medir qualidade observada e incerteza sem chamar maior aprovação de maior inteligência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T195, T197, T200, T205, T206, P010, P011, P016

## Fontes primárias associadas

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

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

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

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

# P013 — Resilience Engine / Reliability Controller

**Nome canônico:** Resilience Engine / Reliability Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de resiliência; controlador proposto de confiabilidade

## P013:C01 — conceito

Resilience Engine / Reliability Controller é um nome editorial proposto para aplicar uma política coerente de recuperação às chamadas e etapas. Coordenaria timeouts, tentativas, backoff, limites e circuit breaker. Esses mecanismos são documentados individualmente; as fontes não confirmam um serviço LAI implementado nem uma combinação automaticamente adequada a todas as dependências.

Como funciona:
- Classificar erros em temporários, permanentes e resultado desconhecido, usando o contrato da operação.
- Aplicar orçamento global de tempo e tentativas, combinando backoff com jitter e orientações Retry-After quando compatíveis.
- Abrir o circuito diante de falhas persistentes e liberar poucas sondas em half-open antes da recuperação normal.

## P013:C02 — aplicacao

Quando usar:
- Dependências sujeitas a indisponibilidade transitória, limites de capacidade e latência variável.

Quando não usar:
- Para repetir indefinidamente erros de contrato ou ações externas ambíguas sem idempotência e reconciliação.

Implementação proposta:
- Proposta: escolher uma camada responsável pelas tentativas, evitando multiplicação entre SDK, gateway e executor.
- Persistir retries adiados com deadline, próxima tentativa e chave da intenção original; cada tentativa recebe identificador próprio.
- Combinar limitação de concorrência com fila limitada e sinais de saúde; quando o orçamento acabar, devolver estado final ou inconclusivo ao executor.

Aplicação LAI proposta:
Proposta LAI: P013 administra mecanismos de recuperação do P011, enquanto P015 verifica identidade e confirmação dos efeitos externos.

## P013:C03 — riscos_validacao

Armadilhas:
- Jitter reduz sincronização, mas não cria capacidade no serviço indisponível.
- Half-open sem coordenação entre réplicas pode virar uma nova rajada.
- Trocar a chave de idempotência em cada retry transforma uma repetição lógica em nova solicitação.

Métricas sugeridas:
- Recuperações por classe de erro, amplificação de tentativas, ocupação da fila e tempo até detectar recuperação.

Testes propostos:
- Aceite proposto: simular falha transitória e recuperação gradual, observando limites de fila, deadline e número de sondas.
- Enviar erro permanente e timeout com efeito remoto confirmado posteriormente; exigir ausência de retry cego e preservação da intenção.

## P013:C04 — perguntas_proveniencia

Pergunta: Todas as camadas devem fazer três tentativas?
Resposta: Não. Tentativas aninhadas multiplicam chamadas; a política deve definir uma responsabilidade e orçamento comuns.

Pergunta: Um circuito fechado indica que o negócio funcionou?
Resposta: Não. Indica que chamadas estão permitidas pela política; conclusão da operação ainda depende de sua resposta e confirmação verificável.

Pergunta: O que caracteriza uma tempestade de retries?
Resposta: Tentativas em múltiplas camadas ampliam a carga justamente quando a dependência falha.

Pergunta: Reiniciar é sempre recuperação?
Resposta: Não. Sem corrigir a condição ou retomar com estado consistente, o restart pode repetir o mesmo erro.

Escopo das fontes:
Fontes fundamentam mecanismos de resiliência; coordenação, fila e aceites são desenho proposto.

## P013:C05 — mecanismo_avancado

Resilience Engine / Reliability Controller propõe coordenar timeout, retry, circuit breaker e fallback sob um orçamento por operação. Cada camada não deve multiplicar tentativas sem conhecer o limite global. Falhas permanentes, como entrada inválida, precisam de tratamento diferente de indisponibilidade transitória. O controlador também deve distinguir processo vivo, serviço apto a receber tráfego e trabalho progredindo, pois responder a um health check não prova avanço da tarefa.

Condição de contorno:
Reiniciar continuamente um worker que depende de um serviço indisponível pode ampliar a falha. Liveness não deve substituir um diagnóstico de dependência ou de ausência de progresso.

Contrato proposto:
- Entradas: Operação identificada, classificação do erro, deadline, tentativas consumidas, estado de dependências e política de degradação.
- Saídas: Decisão de repetir, aguardar, abrir circuito, trocar rota ou encerrar, com motivo e próximo instante elegível.
- Estado: Contadores por operação, estados de circuitos, leases, observações de progresso e orçamento restante.
- Invariante: Retries de qualquer camada consomem o mesmo orçamento lógico; uma falha não pode restaurar o limite inicial.

Compromissos de projeto:
- Backoff reduz pressão durante falha, mas aumenta o tempo até uma tentativa que poderia funcionar.
- Circuitos evitam insistência inútil, porém precisam de sondagem controlada para detectar recuperação sem tempestade.

## P013:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: combinar timeout em cliente e retry no worker durante indisponibilidade prolongada; verificar limite global, jitter e recuperação gradual sem pico sincronizado de novas chamadas.

Plano de avaliação proposto:
Comparar política isolada por camada e orçamento compartilhado sob falhas transitórias e permanentes. Medir amplificação de chamadas, tempo de recuperação, tarefas abandonadas e latência de cauda. Registrar o custo da degradação e do fallback.

Comparações:
- T138 (complements): Circuit breaker controla acesso a dependências falhas.
- T227 (complements): Checks distinguem prontidão, vida e sinais específicos de progresso.

Afirmação rastreável:
Circuit breaker controla falhas de dependências; readiness e liveness têm efeitos operacionais diferentes.
Suporte: related; fontes: C-S005, V3D-S017
Limite: A política global proposta precisa ser implementada; a documentação Kubernetes não define progresso semântico da tarefa.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P013:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a proposta de confiabilidade com isolamento por domínio de falha, teste controlado de recuperação e orçamento contra tempestade de retries.

Domínio de falha correto
Proposta: particionar circuitos por recurso e falha observável, evitando que um cliente inválido bloqueie todos os demais. Falhas de autenticação, sobrecarga e indisponibilidade têm respostas distintas. Preservar métricas por tenant e operação ajuda a evitar um circuito que apenas oculta defeitos de contrato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

Recuperação com carga limitada
Usar probes com orçamento e competição controlada. A volta de uma dependência não autoriza liberar toda a fila acumulada de uma vez. Reintroduzir tráfego gradualmente e observar p95, rejeições e sucesso; um teste simples de conexão pode passar enquanto a operação real ainda falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

Amplificação entre camadas
Calcular o máximo de tentativas efetivas considerando SDK, gateway, workflow e agente. Um teto por camada pode multiplicar carga. A política global distribui créditos e conserva identidade lógica; jitter reduz sincronização, mas não cria capacidade ausente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

USO AVANÇADO — Provedor de modelo degradado
Cenário: Latência aumenta e alguns pedidos retornam erro transitório.
Estratégia: Limitar concorrência, usar deadline residual e alternar apenas para rota compatível quando houver orçamento.
Papel do modelo pequeno: LLM pequena continua tarefas elegíveis; a política de falha usa telemetria externa.
Aceite proposto: Carga no provedor cai durante falha e retorno não dispara pico maior que a capacidade medida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

USO AVANÇADO — Ferramenta com erro permanente
Cenário: Argumentos ou credenciais inválidos geram repetição inútil.
Estratégia: Classificar erro e encerrar retry de transporte; reparar contrato somente em fluxo apropriado.
Papel do modelo pequeno: Modelo pode explicar o erro tipado sem receber segredo ou autoridade de ignorar política.
Aceite proposto: Erros permanentes não consomem toda a fila nem o orçamento de tentativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S005, C-S026, V3D-S017, V4C-S005.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: classificação auxiliar de mensagens, sem autoridade exclusiva sobre retry.
8–14B: 8–14B: reparo de argumentos dentro de schema e limite de tentativas.
15–30B: 15–30B: diagnóstico complexo sob demanda, sem ocupar o caminho crítico de cada requisição.
Requisitos de treino/runtime: Métricas, limites e estados do circuito pertencem ao runtime e precisam de testes de falha.
Não aplicar quando: Não usar fallback que viole o requisito da tarefa só para manter resposta disponível.

## P013:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C002 — Amazon Web Services / AWS SDK — retry throttling
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.
Mecanismo documentado: Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.
Correspondência com esta base: A coordenação proposta de resiliência pode reproduzir o princípio de um orçamento explícito.
Transferência proposta para modelo pequeno: Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.
Limite: A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.
Fontes: V2A-S012, V3C-S010.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Política de degradação é princípio do controlador editorial.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P013 é proposta. AWS, SRE Google e plataformas de fila sustentam mecanismos e limites, sem comprovar o controlador editorial completo.
Consultas registradas: V4C-Q001, V4C-Q003, V4C-Q004.

## P013:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P013 → T138 [complements]
Como combinar: Associar circuito ao recurso e classe de falha adequados.
Interface: Chave do circuito, estado, amostra e orçamento de probes.
Condição: Dependência apresenta falha correlacionada.
Aceite proposto: Erros de um escopo não derrubam escopos independentes sem evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S005, C-S026, V3D-S017, V4C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P013 → T163 [complements]
Como combinar: Distribuir esperas e tentativas dentro do teto lógico.
Interface: Deadline, retry_credit e identidade da operação.
Condição: Falha é transitória e repetição é segura.
Aceite proposto: Retries de todas as camadas respeitam o mesmo limite efetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S005, C-S026, V3D-S017, V4C-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar indiscriminadamente liveness para reiniciar serviço saudável dependente de outro indisponível.
- Não interpretar jitter como proteção suficiente contra sobrecarga.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso e custo em falhas injetadas, não apenas operação normal. Reportar rejeições controladas e tempo até recuperação sem mascarar falhas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T137, T138, T162, T163, T164, T165, T228, P011, P015

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S005 — Circuit Breaker Pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Circuito fechado, aberto e parcialmente aberto isolam dependências com falhas persistentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S027 — Timeouts, retries, and backoff with jitter

[https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retries limitados, timeouts e jitter reduzem amplificação de falhas transitórias.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S028 — RFC 9110: HTTP Semantics

[https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retry-After informa intervalo de espera e admite data HTTP ou atraso em segundos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S017 — Kubernetes — Liveness, readiness and startup probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Liveness e readiness produzem efeitos diferentes de reinício e elegibilidade para receber tráfego.

Limite: Não oferece por si só comprovação de progresso semântico de uma tarefa de agente.

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S010 — Retry behavior — AWS SDKs and Tools

[https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quota de retries usa token bucket e limita repetições, distinguindo tentativas da admissão inicial; modos variam.

Limite: Página consultada distingue comportamento 2026 com opt-in e comportamento anterior; nenhuma configuração local é afirmada.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P014 — Execution Resilience

**Nome canônico:** Execution Resilience  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** architecture  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P014  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** capacidade proposta de resiliência da execução

## P014:C01 — conceito

Execution Resilience é um rótulo editorial proposto para a capacidade transversal de continuar ou recuperar o trabalho após falhas. Nesta arquitetura, não designa um segundo motor equivalente ao P013: inclui persistência, retomada, idempotência, reconciliação e comportamento sob sobrecarga. As fontes apoiam princípios de resiliência; a capacidade LAI descrita ainda exige implementação e demonstração.

Como funciona:
- Definir quais objetivos e estados devem sobreviver a falhas de processo, dependência e infraestrutura.
- Combinar checkpoints, histórico de eventos e contratos de efeitos para recuperar uma posição consistente.
- Usar filas limitadas, backpressure e degradação explícita para evitar que uma falha local se espalhe pelo fluxo.

## P014:C02 — aplicacao

Quando usar:
- Trabalhos longos e operações que precisam retomar após reinício, perda de conexão ou indisponibilidade de um serviço.

Quando não usar:
- Como promessa de ausência de falhas ou como justificativa para continuar produzindo resultados inválidos quando dependências essenciais faltam.

Implementação proposta:
- Proposta: listar cenários de falha e definir objetivos mensuráveis de recuperação, incluindo perda de estado tolerável e tempo máximo de retomada.
- Documentar o ponto durável de cada etapa e a ação de recuperação correspondente; incluir versões de código e dados necessárias ao replay.
- Projetar degradação por requisito: adiar uma etapa dependente pode ser correto; substituí-la por evidência inventada não satisfaz o objetivo.

Aplicação LAI proposta:
Proposta LAI: tratar P014 como propriedade do conjunto P008, P011, P013 e P015, com cenários de falha documentados em vez de apenas um nome de módulo.

## P014:C03 — riscos_validacao

Armadilhas:
- Checkpoints frequentes não resolvem duplicação de efeitos externos.
- Um health check de processo vivo não comprova progresso da tarefa ou disponibilidade de dependências.
- Snapshots incompatíveis com o histórico podem acelerar uma reconstrução incorreta.

Métricas sugeridas:
- Tempo observado de recuperação, perda confirmada de estado, efeitos duplicados e objetivos concluídos após falha induzida.

Testes propostos:
- Aceite proposto: reiniciar o executor em pontos distintos e recuperar o mesmo estado lógico esperado.
- Simular dependência lenta e fila saturada; exigir limite de recursos e comunicação explícita das etapas adiadas ou inconclusivas.

## P014:C04 — perguntas_proveniencia

Pergunta: Ter retries basta para resiliência de execução?
Resposta: Não. Também é necessário preservar estado, identificar efeitos e recuperar de maneira consistente após interrupções.

Pergunta: Qual diferença prática existe para o Resilience Engine?
Resposta: P013 aplicaria mecanismos operacionais; P014 expressa o comportamento recuperável do sistema completo e seus critérios de demonstração.

Pergunta: Preciso criar outro microsserviço com este nome?
Resposta: Não. Primeiro defina responsabilidades e evidências; a capacidade pode estar distribuída nos componentes existentes.

Pergunta: Qual aceite demonstra resiliência?
Resposta: Injeções de falha com estado final correto, efeitos controlados e recuperação dentro do objetivo definido.

Escopo das fontes:
Princípios documentados sustentam a proposta transversal; nenhum resultado de recuperação LAI foi medido.

## P014:C05 — mecanismo_avancado

Execution Resilience é uma capacidade transversal proposta, não necessariamente um novo serviço. Ela resulta da combinação verificável de persistência, limites, detecção de falhas e recuperação. O projeto deve enumerar fronteiras: processo, armazenamento, fila, modelo e serviço externo. Para cada uma, declarar o que pode ser perdido, repetido ou ficar ambíguo. Um runbook útil associa o sinal observado a uma ação e a uma evidência de recuperação, sem depender apenas de logs de reinício.

Condição de contorno:
Disponibilidade do processo e conclusão correta da tarefa são objetivos distintos. Recuperar o worker pode deixar uma operação externa duplicada ou uma tarefa logicamente bloqueada.

Contrato proposto:
- Entradas: Matriz de falhas, estado persistido, critérios de serviço e de tarefa, limites de repetição e mecanismos de recuperação disponíveis.
- Saídas: Plano operacional, transições de recuperação e comprovação do estado final ou pendência explicitamente identificada.
- Estado: Checkpoints, eventos, versões de código, indicadores de progresso e inventário de operações externas em aberto.
- Invariante: Uma recuperação só encerra o incidente quando o estado e os efeitos exigidos pela tarefa estão reconciliados.

Compromissos de projeto:
- Cobrir mais fronteiras reduz pontos cegos, mas exige injeções de falha e manutenção de procedimentos.
- Recuperação automática acelera casos conhecidos; condições ambíguas precisam de decisão explícita para evitar dano repetido.

## P014:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: testar separadamente queda antes do commit, depois do commit e após efeito remoto sem confirmação local. Exigir classificação distinta e verificar que o runbook não aplica retry indiscriminado.

Plano de avaliação proposto:
Construir matriz com falhas e resultados esperados antes dos testes. Medir recuperação de tarefas, perda admissível, duplicatas e tempo de restauração. Relatar limites não cobertos em vez de resumir tudo a uma taxa genérica de disponibilidade.

Comparações:
- P013 (complements): O controlador fornece políticas de reação.
- T242 (complements): Snapshot mais eventos é um mecanismo possível de reconstrução.

Afirmação rastreável:
Persistência e repetição segura tratam problemas complementares de recuperação.
Suporte: related; fontes: V3D-S016, C-S026
Limite: Execution Resilience é uma capacidade editorial composta; não constitui tecnologia padronizada adicional.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P014:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a capacidade transversal de resiliência com invariantes durante recuperação, observabilidade de estagnação e testes por fronteira de falha.

Invariantes durante falha
Proposta: definir o que deve permanecer verdadeiro enquanto o sistema está degradado, não apenas depois de reiniciar. Exemplos incluem não confirmar efeito desconhecido, não perder tarefa aceita e não permitir dois donos ativos sobre a mesma mutação. Cada fronteira recebe um teste de violação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S016, V3D-S017, C-S026, V4C-S001.

Progresso semântico observável
Separar heartbeat do processo, avanço de cursor e conclusão de subtarefa. Um agente pode continuar emitindo tokens enquanto repete a mesma hipótese. Medir mudança de estado verificável e comparar com o orçamento esperado para detectar estagnação sem interromper trabalho legitimamente longo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S016, V3D-S017, C-S026, V4C-S001.

Recuperação em níveis
Escalar de nova tentativa local para retomada do checkpoint, reatribuição de worker e intervenção definida. Cada nível consome orçamento e preserva diagnóstico. Reiniciar toda a sessão ao primeiro erro pode descartar evidência e multiplicar chamadas sem corrigir a causa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S016, V3D-S017, C-S026, V4C-S001.

USO AVANÇADO — Agente preso em ciclos
Cenário: Chamadas seguem funcionando, mas a tarefa não avança.
Estratégia: Detectar repetição de estado/ação e testar uma mudança controlada de estratégia antes de escalar.
Papel do modelo pequeno: Modelo pequeno pode classificar padrões; detector mantém contador e estado externo.
Aceite proposto: Ciclo sintético é detectado; tarefa lenta com progresso válido não é encerrada indevidamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S016, V3D-S017, C-S026, V4C-S001.

USO AVANÇADO — Queda entre etapas duráveis
Cenário: Processo termina após gerar candidato, antes de publicar.
Estratégia: Retomar do estado persistido, verificar integridade e executar somente a parte ainda não confirmada.
Papel do modelo pequeno: LLM lê o pacote mínimo de retomada; não reconstrói histórico por adivinhação.
Aceite proposto: Falha injetada em cada fronteira preserva invariantes e evidencia a conclusão correta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S016, V3D-S017, C-S026, V4C-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: execução curta com progresso explícito e recuperação externa.
8–14B: 8–14B: tarefas em várias etapas com limites de repetição e checkpoints úteis.
15–30B: 15–30B: investigação de impasses complexos somente depois de preservar evidências e estado.
Requisitos de treino/runtime: A capacidade emerge de persistência, observação e políticas; não exige um novo modelo ou serviço monolítico.
Não aplicar quando: Não medir resiliência somente por uptime ou quantidade de reinícios.

## P014:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C008 — Google / Google Search — degradação sob sobrecarga
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.
Mecanismo documentado: O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.
Correspondência com esta base: Manter objetivos de serviço sob falha ilustra resiliência transversal.
Transferência proposta para modelo pequeno: Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.
Limite: Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.
Fontes: V4C-S005.

V4C-C023 — Google / Borg
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.
Mecanismo documentado: O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.
Correspondência com esta base: Isolamento e recuperação fornecem princípios de resiliência para a proposta.
Transferência proposta para modelo pequeno: Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.
Limite: O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.
Fontes: V4C-S023.

V4C-C006 — Netflix / Conductor — plataforma interna atualizada
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.
Mecanismo documentado: O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.
Correspondência com esta base: Recuperação de workflows é analogia da capacidade proposta.
Transferência proposta para modelo pequeno: Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.
Limite: Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.
Fontes: V4C-S004, V4C-S003.

V4C-C003 — Uber / Cadence — plataforma interna
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.
Mecanismo documentado: Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.
Correspondência com esta base: Retomada e isolamento sustentam uma analogia de resiliência, não implementação LAI.
Transferência proposta para modelo pequeno: Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.
Limite: Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.
Fontes: V4C-S001.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P014 é capacidade editorial transversal. Relatos de execução durável e práticas operacionais são referências, sem implantação literal de um componente com esse nome.
Consultas registradas: V4C-Q002, V4C-Q004, V4C-Q022.

## P014:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P014 → T225 [complements]
Como combinar: Permitir restart apenas com diagnóstico e estado recuperável.
Interface: Sinal de falha, orçamento, última etapa confirmada.
Condição: Processo ou worker deixou de atender seu contrato.
Aceite proposto: Restart não perde trabalho confirmado nem repete efeito ambíguo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S016, V3D-S017, C-S026, V4C-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P014 → T227 [complements]
Como combinar: Combinar saúde de processo, prontidão e progresso da tarefa.
Interface: Sinais separados e critérios por tipo de trabalho.
Condição: Um indicador isolado não distingue travamento de lentidão.
Aceite proposto: Os testes discriminam processo vivo sem progresso de tarefa avançando normalmente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S016, V3D-S017, C-S026, V4C-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não renovar indefinidamente o prazo apenas porque chegaram tokens.
- Não apagar diagnóstico no reinício que deveria investigá-lo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar custo e conclusão correta em matrizes de falha equivalentes entre modelos. Um sistema maior sem persistência pode falhar em continuidade; isso não prova menor capacidade cognitiva.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T159, T227, T240, T241, T242, P008, P011, P013, P015

## Fontes primárias associadas

### C-S003 — Transient Fault Handling

[https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de falhas temporárias exige classificação do erro, tentativas finitas e estratégia de recuperação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V3D-S017 — Kubernetes — Liveness, readiness and startup probes

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Liveness e readiness produzem efeitos diferentes de reinício e elegibilidade para receber tráfego.

Limite: Não oferece por si só comprovação de progresso semântico de uma tarefa de agente.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

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

### V4C-S005 — Service Best Practices — Overloads and Failure

[https://sre.google/sre-book/service-best-practices/](https://sre.google/sre-book/service-best-practices/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico de degradação do Google Search sob sobrecarga e práticas de validação de configurações.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S023 — Large-scale cluster management at Google with Borg

[https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Abstract confirma operação de Borg, admissão, alocação, isolamento e recuperação de cargas do Google.

Limite: Abertura efetiva do abstract; PDF completo bloqueado. Não usar para detalhes ausentes do resumo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P015 — Execution Integrity Controller

**Nome canônico:** Execution Integrity Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador proposto de integridade da execução

## P015:C01 — conceito

Execution Integrity Controller é um nome editorial proposto para vincular uma intenção autorizada ao artefato, versão e efeito realmente executados. Verificaria pré-condições e recibos para evitar que uma operação correta seja aplicada ao alvo errado ou a uma base obsoleta. As fontes apoiam identidade de intenção e versionamento; não atestam esse controlador LAI implementado.

Como funciona:
- Associar o comando ao objetivo vigente, destino exato, entradas versionadas e identificador único de intenção.
- Conferir pré-condições imediatamente antes da escrita, incluindo hash ou versão da base quando o backend oferecer esse controle.
- Registrar resultado confirmado, rejeição ou desfecho desconhecido, preservando recibos e referências à operação.

## P015:C02 — aplicacao

Quando usar:
- Aplicação de patches, atualização de documentos, execução de ferramentas e publicação de artefatos com risco de concorrência ou duplicação.

Quando não usar:
- Como substituto do controle de acesso do serviço ou como prova de correção funcional baseada somente em um hash.

Implementação proposta:
- Proposta: formar um envelope de execução com alvo, base esperada, alteração pretendida e chave de idempotência.
- Validar que o efeito solicitado corresponde às decisões atuais e enviar a escrita com a pré-condição nativa disponível.
- Após resposta incerta, consultar estado e recibos antes de decidir nova tentativa; o reaparecimento do conteúdo sozinho pode não provar autoria ou conclusão daquela operação.

Aplicação LAI proposta:
Proposta LAI: P015 confere a ligação entre decisão e efeito do P011, enquanto P012 avalia o resultado e P013 administra falhas operacionais.

## P015:C03 — riscos_validacao

Armadilhas:
- Hash igual verifica igualdade dos bytes representados, mas não demonstra que o conteúdo está correto ou que a ação foi autorizada.
- Ler a versão e escrever sem uma guarda atômica deixa uma janela de concorrência.
- Reconstruir IDs a partir de nomes parecidos pode direcionar o efeito a outro recurso.

Métricas sugeridas:
- Conflitos detectados antes da escrita, operações sem recibo, efeitos duplicados e correspondência entre intenção e alvo.

Testes propostos:
- Aceite proposto: alterar a base entre preparação e escrita; exigir rejeição da guarda ou reconciliação explícita.
- Simular timeout após aplicação e verificar que a intenção original é consultada antes de repetir o efeito.

## P015:C04 — perguntas_proveniencia

Pergunta: Um hash-base elimina toda disputa de concorrência?
Resposta: Somente quando a comparação e a escrita são protegidas pelo backend ou por protocolo equivalente; comparação local isolada não basta.

Pergunta: Qual estado registrar se a resposta da escrita se perdeu?
Resposta: Resultado desconhecido, com os IDs da intenção e da tentativa, até obter evidência suficiente para reconciliar o desfecho.

Pergunta: Hash correto significa implementação correta?
Resposta: Não. Ele identifica bytes; testes e critérios verificam propriedades e comportamento.

Pergunta: Quando uma operação fica pendente?
Resposta: Quando houve intenção ou envio, mas a confirmação não permite determinar com segurança o efeito externo.

Escopo das fontes:
Fontes apoiam idempotência, objetos versionados e transações; envelope e controlador são proposta editorial.

## P015:C05 — mecanismo_avancado

Execution Integrity Controller propõe vincular cada mutação à versão de origem, à intenção e à evidência de resultado. Em edição de código, o patch deve declarar o estado-base e ser recusado se esse estado mudou sem reconciliação. Em operações externas, uma intenção estável e uma chave idempotente ajudam a distinguir repetição de uma nova ação. Hash comprova identidade do conteúdo comparado, mas não prova que seu significado está correto ou que a ação remota foi concluída.

Condição de contorno:
Não existe uma transação local capaz de tornar automaticamente atômicos arquivo, banco, fila e API externa independentes. A fronteira de confirmação deve ser explicitada por sistema.

Contrato proposto:
- Entradas: Mutação proposta, identidade do alvo, hash ou revisão esperada, escopo autorizado e ID estável da operação.
- Saídas: Aceite ou conflito, nova revisão, registro de intenção e confirmação verificável ou pendência de reconciliação.
- Estado: Versões anteriores, resultados por operação, outbox quando aplicável e evidências vinculadas ao conteúdo efetivo.
- Invariante: Um resultado não pode ser atribuído a artefato diferente do verificado; repetição não deve converter a mesma intenção em novo efeito lógico.

Compromissos de projeto:
- Verificação de versão impede sobrescrita silenciosa, mas pode exigir recomposição do patch após concorrência.
- Registrar intenção e resultado melhora rastreabilidade, acrescentando armazenamento e contratos de retenção.

## P015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar o arquivo entre leitura e aplicação do patch e perder a confirmação de uma operação externa; exigir conflito no primeiro caso e consulta ou deduplicação no segundo.

Plano de avaliação proposto:
Comparar execução sem controle de versão e com precondições em cenários concorrentes conhecidos. Medir sobrescritas indevidas, efeitos duplicados, conflitos legítimos e recuperação. Verificar também que hashes são recalculados sobre o artefato realmente consumido.

Comparações:
- T233 (complements): Validação de patch verifica precondições e aplicabilidade.
- T162 (complements): Idempotência controla repetição de uma intenção.

Afirmação rastreável:
Identificadores idempotentes e outbox ajudam a controlar repetição e a fronteira entre alteração local e notificação.
Suporte: related; fontes: C-S026, V3D-S018
Limite: O controlador e o vínculo entre hashes e operações são uma proposta; não há garantia universal de exatamente uma vez.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P015:C07 — estrategia_3_30b

NOVA CAMADA v4 — Vai além do hash-base e da reconciliação já tratados: distingue igualdade de bytes de história de alterações, trata expiração da deduplicação e impede reutilizar uma identidade de operação com intenção diferente.

A→B→A: bytes iguais, história diferente
Proposta: quando a regra depende de nenhuma alteração intermediária, comparar somente conteúdo não detecta uma escrita seguida de restauração. Exigir revisão ou geração monotônica com comparação atômica no destino, incluindo identidade da criação quando uma chave pode ser apagada e recriada. Se o contrato depende apenas dos bytes atuais, a alteração histórica pode ser irrelevante; não impor bloqueio sem necessidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

Janela finita de idempotência
Persistir a semântica de retenção do destino junto da operação. Uma chave que já foi expurgada pode representar nova requisição; retomada muito tardia precisa consultar recibo/status ou permanecer em reconciliação. Manter registro local não obriga o servidor remoto a deduplicar. Versionar a política: comportamento de respostas falhas e retenção pode diferir entre versões de API.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

Identidade com impressão da intenção
Vincular operation_id a tenant, destino estável, versão da API e argumentos normalizados sob regra explícita. Reutilizar a chave com parâmetros diferentes deve ser conflito, não retry. Duas solicitações legítimas iguais em conteúdo precisam de identidades distintas quando representam duas intenções; deduplicar apenas pelo hash dos argumentos pode suprimir trabalho válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

USO AVANÇADO — Retomada após longa indisponibilidade
Cenário: O agente reaparece depois da janela de deduplicação remota.
Estratégia: Preservar a identidade original e verificar evidência do destino; não gerar chave nova para contornar estado desconhecido.
Papel do modelo pequeno: 3–14B interpreta status documentado; o controlador decide conforme contrato de retenção.
Aceite proposto: Simular expurgo da chave e confirmar que resultado incerto não dispara efeito duplicado automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

USO AVANÇADO — Configuração alterada e restaurada
Cenário: Outro processo modifica um recurso e devolve o conteúdo inicial antes do commit.
Estratégia: Usar comparação atômica da revisão de modificação e identidade da criação quando histórico importa; rejeitar guardas somente de conteúdo nesse contrato.
Papel do modelo pequeno: LLM propõe mudança; backend aplica precondição de revisão, sem delegar detecção ao texto.
Aceite proposto: Teste A→B→A é rejeitado quando o contrato exige ausência de intervenção; igualdade de bytes continua aceita quando for o requisito correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: emitir intenção estruturada sem fabricar IDs de recursos ou revisar sozinho as regras de deduplicação.
8–14B: 8–14B: interpretar respostas e conflitos documentados, mantendo decisão temporal no controlador.
15–30B: 15–30B: investigar casos ambíguos com evidências; capacidade maior não recupera recibo inexistente.
Requisitos de treino/runtime: Exige contratos de retenção, comparação atômica e namespace do destino; restauração de backend também precisa de política de épocas.
Não aplicar quando: Não confundir um hash de conteúdo, versão reiniciável ou chave expirada com garantia histórica permanente.

## P015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: Identidade, parâmetros e resposta exemplificam princípios do controlador editorial, sem existência do componente LAI.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Publicação e autoria por versão inspiram o componente editorial.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Vínculo entre revisão e implantação ilustra integridade de execução.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Revisões e controle de exposição apoiam integridade editorial.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P015 é proposta. APIs idempotentes, Git e controles de repositório são analogias delimitadas; não se atribui às empresas o controlador LAI completo.
Consultas registradas: V4C-Q001, V4C-Q005, V4C-Q015, V4C-Q022.

## P015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P015 → T162 [complements]
Como combinar: Aplicar deduplicação sob identidade de intenção, escopo e janela conhecidos.
Interface: Operation_id, fingerprint de argumentos, namespace, API_version e política de retenção.
Condição: Uma ação pode ser repetida ou retomada após interrupção longa.
Aceite proposto: Mesma chave/intenção retorna estado conhecido; chave com intenção diferente é recusada e chave expurgada não é presumida segura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P015 → T072 [complements]
Como combinar: Escolher revisão de estado capaz de representar o requisito de concorrência.
Interface: Content_hash, revisão de modificação, geração/criação e guarda atômica.
Condição: O efeito depende da história de alterações e não apenas de bytes atuais.
Aceite proposto: Teste de alteração e restauração distingue equivalência de conteúdo de continuidade da versão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não normalizar argumentos de modo a apagar diferenças semanticamente relevantes.
- Não inferir sucesso da própria operação pela existência de recurso semelhante.
- Não tratar restauração de snapshot do backend como continuidade automática da mesma época.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Injetar expiração de chaves, troca de parâmetros, exclusão/recriação e restauração A→B→A nos sistemas comparados. Medir duplicação e supressão indevida; essas falhas podem persistir mesmo com um gerador de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T072, T162, T200, T233, P011, P012, P013

## Fontes primárias associadas

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### V3D-S018 — AWS — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alteração local e evento pendente na mesma transação; publicação posterior pode duplicar mensagens.

Limite: Outbox não torna toda chamada externa exatamente uma vez; consumidores precisam de idempotência.

### V4D-S021 — Making retries safe with idempotent APIs — publicação atual no AWS Builder Center

[https://builder.aws.com/content/3Ev0BENTyBr0XxzRk5FDZzgNYos/m](https://builder.aws.com/content/3Ev0BENTyBr0XxzRk5FDZzgNYos/m)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade fornecida pelo cliente, equivalência de resposta, diferença entre mesma aparência e mesma intenção e limites de repetição em APIs.

Limite: Não fornece garantia universal entre APIs; conferir contrato, retenção e versão do destino. Novo URL mantém acessível a fonte do Builders Library.

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P016 — Evaluation Engine

**Nome canônico:** Evaluation Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de avaliação de versões

## P016:C01 — conceito

Evaluation Engine é um nome editorial proposto para comparar versões do sistema em conjuntos de tarefas e monitorar regressões. Sua unidade é a avaliação agregada de comportamento, enquanto P012 verifica um resultado concreto durante o fluxo. As fontes apoiam boas práticas de avaliação; não confirmam um motor LAI implementado nem resultados de benchmark deste pacote.

Como funciona:
- Definir objetivos, conjunto de casos, critérios de sucesso e métricas antes de comparar candidatos.
- Executar baseline e versão candidata sob condições documentadas, preservando entradas, saídas, custos e versões.
- Analisar desempenho por classe de tarefa e revisar divergências com avaliação humana ou oráculos adequados.

## P016:C02 — aplicacao

Quando usar:
- Mudanças em recuperação, prompts, roteamento, modelos e políticas de memória que podem introduzir regressões.

Quando não usar:
- Para apresentar perguntas produzidas a partir das próprias fichas como teste independente de cobertura ou generalização.

Implementação proposta:
- Proposta: separar desenvolvimento, ajuste e teste; evitar vazamento de documentos ou tarefas quase duplicadas entre divisões.
- Avaliar recuperação e resposta separadamente: recuperar o documento certo não implica responder corretamente, e uma resposta memorizada pode esconder recuperação ruim.
- Calibrar avaliadores automáticos contra rótulos revisados e apresentar tamanho da amostra, variabilidade e condições de medição.

Aplicação LAI proposta:
Proposta LAI: versionar datasets e critérios com os artefatos, alimentando decisões de P010 e P017; as duas QAs de cada ficha permanecem material didático.

## P016:C03 — riscos_validacao

Armadilhas:
- Uma média global pode ocultar regressões graves em tarefas raras.
- O julgador pode preferir respostas longas ou compartilhar o mesmo erro do produtor.
- Escolher o melhor limiar repetidamente sobre o teste transforma esse conjunto em material de ajuste.

Métricas sugeridas:
- Qualidade por estrato, recall de evidências, correção funcional, custo por sucesso e latências sob carga definida.

Testes propostos:
- Aceite proposto: inserir uma regressão conhecida em apenas uma classe e exigir sua identificação no relatório.
- Reservar um conjunto externo às fichas e verificar que alterações de limiares não o utilizem como treinamento.

## P016:C04 — perguntas_proveniencia

Pergunta: As QAs deste RAG comprovam sua qualidade?
Resposta: Não. Elas ajudam ensino e checagem interna, mas foram escritas a partir do conteúdo; um benchmark independente precisa de casos separados.

Pergunta: Como distinguir melhoria de custo de perda de qualidade?
Resposta: Comparar custo por resultado aceito sob os mesmos critérios e reportar a qualidade por classe, incluindo falhas e tentativas adicionais.

Pergunta: Posso chamar 100% de busca por nome de qualidade geral?
Resposta: Não. É um teste de cobertura literal, diferente de perguntas descritivas e de respostas corretas.

Pergunta: O que fazer após ver falhas na reserva?
Resposta: Registrar a primeira rodada; usar esses casos para desenvolvimento futuro e criar outra reserva antes do próximo ajuste.

Escopo das fontes:
Fontes apoiam avaliação e calibração; datasets, limiares e resultados LAI continuam pendentes de execução.

## P016:C05 — mecanismo_avancado

Evaluation Engine propõe manter avaliações separadas de recuperação, montagem de contexto, geração e execução. Um resultado de Hit@k indica presença de um alvo entre candidatos, sem provar que a resposta final usa a evidência corretamente. Consultas usadas para ajustar ranking pertencem ao desenvolvimento. Um conjunto reservado deve ser congelado antes da mudança avaliada e identificado por hash; após inspecionar falhas, ele perde o papel de reserva intocada para a próxima rodada.

Condição de contorno:
Um pequeno conjunto editorial pode revelar regressões, mas não representa automaticamente a distribuição de produção. Métricas agregadas podem esconder falhas em categorias raras ou importantes.

Contrato proposto:
- Entradas: Corpus e configuração identificados, consultas, critérios ou referências, partições e protocolo definido antes da execução.
- Saídas: Resultados por caso, agregações, falhas, artefatos de configuração e limites da interpretação.
- Estado: Versões de datasets, histórico de alterações, primeiras execuções reservadas e registros de decisões de ajuste.
- Invariante: Não alterar respostas esperadas depois de observar falhas para melhorar o score da mesma rodada; correções exigem nova versão justificada.

Compromissos de projeto:
- Casos sintéticos permitem cobertura dirigida, mas precisam ser complementados por exemplos reais autorizados.
- Juízes automáticos ampliam escala; custo, viés e correlação com o gerador precisam de controles próprios.

## P016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: mudar um documento, um parâmetro de ranking e uma referência esperada; verificar que cada alteração muda a identidade da avaliação e impede comparação sem qualificação.

Plano de avaliação proposto:
Executar baseline e candidato com mesmos dados, preservar rankings completos e examinar ganhos e regressões. Para geração, adicionar respostas reais e avaliação de suporte por evidência. Não inferir qualidade de geração a partir do teste lexical offline.

Comparações:
- T199 (complements): Aprendizagem por avaliação usa resultados sem contaminar a reserva.
- T205 (complements): Equivalência semântica pode ser uma dimensão específica do protocolo.

Afirmação rastreável:
A avaliação de RAG distingue qualidade de recuperação, fidelidade ao contexto e resposta.
Suporte: related; fontes: V3D-S002
Limite: O motor proposto não é implementação do Ragas; os testes deste pacote medem apenas os componentes efetivamente executados.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegeu conjunto reservado e separou recuperação de resposta. Esta proposta acrescenta diagnóstico causal, avaliação de seletores e governança das versões promovidas. Nenhum benchmark reservado foi consultado para escrever estas estratégias.

Métricas em camadas
Avalie entrada, recuperação, contexto, geração e ação separadamente, mantendo um resultado de tarefa final. Isso permite localizar se a falha veio de documento ausente, interpretação ou execução. Uma métrica intermediária não substitui sucesso de ponta a ponta; melhoria local pode piorar custo ou qualidade global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

Seleção também é sistema
Roteadores, juízes e políticas de parada precisam de avaliação própria. Meça se o conjunto contém solução correta e se o seletor a escolhe; registre abstenções e casos rejeitados. A precisão dos resultados aceitos deve ser acompanhada de cobertura e custo dos descartados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

Promoção reproduzível
Cada rodada registra hashes de dados, corpus, modelo e configuração, além das mudanças propostas. Mantenha desenvolvimento, calibração e aceitação separados. Depois que falhas de um conjunto reservado orientam alterações, ele passa a ser dado de desenvolvimento para versões futuras; a governança deve reconhecer essa mudança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

USO AVANÇADO — Escolher modelo 3–30B
Cenário: Há candidatos com custos e habilidades diferentes.
Estratégia: Defina tarefas e critérios antes da comparação, use ferramentas equivalentes e avalie por categoria. Inclua casos desconhecidos, abstinência e tempo completo.
Papel do modelo pequeno: Um modelo pequeno pode ser escolhido na região de competência demonstrada.
Aceite proposto: Qualidade suficiente, cobertura e custo por resultado correto dentro do objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

USO AVANÇADO — Validar otimização de runtime
Cenário: Cache ou quantização promete mais capacidade.
Estratégia: Compare semântica e qualidade primeiro, depois prefill, decode, fila e memória em carga representativa. Separe efeito do algoritmo de diferenças de modelo e template.
Papel do modelo pequeno: O porte orienta orçamento, mas não substitui ensaio do checkpoint real.
Aceite proposto: Nenhuma regressão relevante escondida por tokens por segundo ou média global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Testes de domínio e contratos fechados ajudam a identificar onde o 3–7B é útil.
8–14B: Para 8–14B, examine ganhos de especialização e falhas fora da distribuição.
15–30B: Para 15–30B, inclua custo de infraestrutura e vantagem marginal frente a opções menores.
Requisitos de treino/runtime: Proposta de avaliação, não execução realizada. Requer dados, critérios, instrumentação e ambiente adequados.
Não aplicar quando: Não ajustar ranking às consultas reservadas nem alterar gabarito depois de ver falha para melhorar o score.

## P016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Avaliação local pode inspirar a proposta LAI; o produto editorial não foi implantado.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: O scorer inspira avaliação de artefatos da proposta editorial.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## P016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P016 → T198 [feeds]
Como combinar: Calibração precisa de dados e métricas independentes na avaliação.
Interface: Evento de sucesso, score e divisão dos dados.
Condição: Amostra representa o caminho de uso.
Aceite proposto: Relatar confiabilidade e cobertura por categoria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P016 → T203 [feeds]
Como combinar: A avaliação mede roteamento completo, incluindo tentativas e escalonamento.
Interface: Decisões, contrafactuais amostrados e custos.
Condição: Comparações têm acesso equivalente a ferramentas e evidências.
Aceite proposto: Aceitar política pelo resultado final, não pela confiança prevista.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P016 → P017 [complements]
Como combinar: Destilação proposta usa avaliação para promover ou rejeitar aluno.
Interface: Checkpoint, dados e contrato de uso.
Condição: Teste final não participa do treino ou seleção.
Aceite proposto: Medir generalização e regressões depois da transferência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar percentuais relativos de preferência em multiplicadores de inteligência.
- Preservar resultados por caso e limitações, não somente um score composto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O engine proposto deve sustentar comparações delimitadas com fronteira. Um conjunto finito de tarefas não comprova supremacia universal; nenhuma medição inexistente deve ser apresentada como resultado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T195, T198, T200, T205, P007, P010, P012, P017

## Fontes primárias associadas

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S002 — Ragas: Automated Evaluation of Retrieval Augmented Generation

[https://arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Avaliar recuperação, fidelidade ao contexto e geração são dimensões distintas de um sistema RAG.

Limite: Página do artigo e abstract consultados, versão revisada indicada em 2025-04-28. Este pacote não executa Ragas nem afirma avaliação real de geração.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# P017 — Distillation Pipeline

**Nome canônico:** Distillation Pipeline  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P017  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** pipeline proposto de destilação

## P017:C01 — conceito

Distillation Pipeline é um componente editorial proposto para organizar transferência de comportamento ou conhecimento com artefatos explícitos. Seu caminho paramétrico gera exemplos com um professor e treina um aluno; o professor pode ser o mesmo modelo condicionado por contexto adicional. Também deve identificar separadamente transferências para memória externa. Nenhum pipeline LAI executado ou modelo treinado é afirmado.

Como funciona:
- Escolher a habilidade alvo, a configuração do professor e o formato de supervisão: respostas, rótulos ou distribuições quando disponíveis.
- Produzir dados, filtrar erros e separar avaliação antes do treino do aluno ou de adaptadores.
- Comparar aluno, baseline e professor quanto à tarefa, custo e necessidade de contexto em inferência.

## P017:C02 — aplicacao

Quando usar:
- Tarefas estáveis com exemplos suficientes e benefício esperado ao reduzir dependência de prompts extensos ou de modelos caros.

Quando não usar:
- Para corrigir rapidamente fatos voláteis que poderiam ser atualizados por recuperação ou para presumir que reduzir texto já modificou os pesos.

Implementação proposta:
- Proposta: registrar modelo professor, prompt, versões dos dados e critérios de seleção; separar casos de teste por origem ou período.
- No caminho paramétrico, guardar checkpoint inicial, receita de treino, artefato final e avaliação comparativa reproduzível.
- No caminho de memória externa, produzir objetos versionados e referências; classificá-lo como transferência sem treino, sem alegar internalização nos pesos.

Aplicação LAI proposta:
Proposta LAI: P017 gerencia receitas e proveniência; P016 decide aceitação comparativa. T069 permanece consolidação textual externa, T179 destilação paramétrica e T181 transferência hierárquica sem treino.

## P017:C03 — riscos_validacao

Armadilhas:
- O aluno pode aprender erros e vieses do professor.
- Fine-tuning é um procedimento de adaptação mais amplo; nem todo fine-tuning constitui destilação.
- Prompt distillation paramétrica, consolidação por resumos e Agent Memory Distillation não devem compartilhar uma definição indiferenciada.

Métricas sugeridas:
- Qualidade em teste separado, custo de preparação e treino, redução de contexto e custo por resultado correto.

Testes propostos:
- Aceite proposto: avaliar o aluno com o prompt reduzido em casos não utilizados na geração ou seleção dos exemplos.
- Inspecionar o artefato entregue: pesos ou adaptadores alterados versus memória externa; exigir classificação coerente com o processo real.

## P017:C04 — perguntas_proveniencia

Pergunta: Context distillation sempre exige um professor maior?
Resposta: Não. No trabalho Learning by Distilling Context, o mesmo modelo condicionado por instruções gera supervisão para treinar comportamento sem aquele contexto.

Pergunta: Agent Memory Distillation implica atualizar pesos?
Resposta: No estudo identificado em T181, não: trajetórias do professor originam memórias externas hierárquicas utilizadas pelo aluno.

Pergunta: Posso treinar apenas com respostas aprovadas pelo próprio professor?
Resposta: Isso mantém risco de erros correlacionados; use critérios independentes e casos difíceis reservados.

Pergunta: Qual artefato comprova a melhoria?
Resposta: Relatório comparativo por tarefa, com dados e configuração identificados, além do checkpoint treinado e seus limites.

Escopo das fontes:
Fontes distinguem treino paramétrico e transferência por memória; organização do pipeline LAI é proposta editorial.

## P017:C05 — mecanismo_avancado

Distillation Pipeline propõe transformar evidências de desempenho em um processo de treinamento reproduzível. Cada exemplo deve preservar versão do professor, prompt, contexto permitido, resposta e critérios usados para aceitá-la. A divisão de dados precisa evitar vazamento por documentos, sessões ou tarefas quase duplicadas. O artefato treinado deve ser avaliado com o contrato de uso pretendido, inclusive quando o contexto fornecido ao professor será removido na inferência do estudante.

Condição de contorno:
Treinar sobre respostas aparentemente boas não garante preservar comportamento em entradas fora da distribuição. Informação volátil nos pesos também exige estratégia explícita de atualização.

Contrato proposto:
- Entradas: Objetivo de comportamento, dados autorizados com proveniência, professor, estudante, partições e orçamento de treinamento.
- Saídas: Checkpoint ou adaptador versionado, manifesto de dados, configuração de treino e relatório comparativo de aceitação.
- Estado: Hashes dos datasets, critérios de filtragem, checkpoints intermediários e decisões de promoção ou rejeição.
- Invariante: Dados de avaliação reservada não participam da seleção de exemplos, ajuste do professor ou escolha do checkpoint final.

Compromissos de projeto:
- Filtragem rigorosa reduz exemplos ruins, porém pode estreitar cobertura e esconder casos difíceis.
- Destilar comportamento recorrente economiza contexto potencialmente, mas requer amortizar treino e manter atualização de políticas.

## P017:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: inserir um exemplo de avaliação na coleta e uma resposta errada muito confiante do professor; exigir detecção de contaminação e rejeição baseada em critério independente.

Plano de avaliação proposto:
Comparar base com contexto, base sem contexto e estudante sob as mesmas tarefas reservadas. Medir acerto, violações, tokens, custo amortizado e regressões em capacidades preservadas. Registrar resultados negativos e não promover apenas pelo loss de treinamento.

Comparações:
- T178 (complements): Distilação de conhecimento define a transferência de comportamento.
- T179 (complements): Context distillation paramétrica especifica o objetivo de internalização.

Afirmação rastreável:
Prompt distillation pode treinar um estudante para responder sem o prompt usado pelo professor.
Suporte: related; fontes: V3D-S008
Limite: O pipeline e seus critérios de promoção são proposta própria; nenhum treinamento foi executado neste pacote.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P017:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu proveniência e partições. Esta proposta acrescenta seleção da via de transferência, controle de qualidade dos professores e critérios de promoção que distinguem memória externa de atualização paramétrica.

Escolher o destino
Procedimentos estáveis podem virar exemplos de treinamento; fatos mutáveis e trajetórias condicionais podem permanecer em memória externa. Declare qual artefato muda: pesos, adapter, prompt ou acervo. AMD e destilação paramétrica são referências diferentes; agrupá-las no pipeline não torna seus mecanismos equivalentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

Professor falível
Registre versão, contexto e configuração do professor, mas também como sua resposta foi verificada. Consenso de professores não substitui referência quando compartilham erro. Dados multi-teacher podem ter objetivos distintos, como no ranking do LinkedIn; a combinação precisa de critérios e não apenas concatenação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

Promoção e manutenção
Compare aluno, base e professor na tarefa real, incluindo contexto retirado, ferramentas e quantização final. Rejeite versões com regressões relevantes e mantenha rollback. Quando o comportamento muda, atualize a relação entre dados, política e artefato, sem presumir que editar uma fonte atualiza pesos já treinados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

USO AVANÇADO — Especializar aluno de domínio
Cenário: Chamadas caras ao professor podem ocorrer offline.
Estratégia: Gere exemplos estratificados, filtre por verificadores e ajuste o aluno. Separe dados por origem e mantenha teste final intocado, incluindo casos em que o professor errou.
Papel do modelo pequeno: Um 3–7B pode assumir formato e procedimento estreitos com evidência externa.
Aceite proposto: Generalização, cobertura e custo amortizado por resultado aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

USO AVANÇADO — Transferir experiência de agente
Cenário: Trajetórias de sucesso contêm convenções de ferramentas.
Estratégia: Extraia memórias com pré-condições e versões; teste em novas situações antes de publicar. Só treine pesos se houver hipótese clara sobre comportamento estável.
Papel do modelo pequeno: Um 8–14B pode usar memória procedural sem depender de memorizar todos os detalhes.
Aceite proposto: Sucesso executável e rejeição de procedimentos incompatíveis com o ambiente atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Foco em habilidades delimitadas e dados verificados; volume sintético não substitui qualidade.
8–14B: Avalie on-policy quando falhas surgem nos estados visitados pelo aluno.
15–30B: Para 15–30B, compare benefício marginal com custo de professor, treino, exportação e manutenção.
Requisitos de treino/runtime: Proposta de pipeline: exige implementação e execução próprias. Caminho paramétrico requer treinamento; memória externa requer curadoria e recuperação.
Não aplicar quando: Não prometer transferir toda capacidade do professor nem afirmar que um aluno LAI foi treinado por esta entrega.

## P017:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4B-C017 — Anthropic / Claude — treinamento com constituição
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: treinamento de LLM.
Uso observado: A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.
Mecanismo documentado: Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.
Correspondência com esta base: Uma política LAI poderia inspirar dados próprios; não há implantação da proposta editorial.
Transferência proposta para modelo pequeno: Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.
Limite: Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.
Fontes: V4B-S021.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: Pipeline real inspira gestão de professores e artefatos da proposta LAI.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C009 — Microsoft / Bing — inferência BERT
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Microsoft relata que modelos BERT destilados e otimizações de inferência foram usados em produção no Bing para tarefas de linguagem e busca.
Mecanismo documentado: Redução do professor a encoder de três camadas e posterior otimização de execução; parte das melhorias foi disponibilizada no ONNX Runtime.
Correspondência com esta base: Demonstra uma separação entre compressão de comportamento e otimização do executor.
Transferência proposta para modelo pequeno: Proposta: testar um modelo especializado ou até um encoder menor antes de usar um gerador 3–30B para classificação/ranking.
Limite: Caso histórico de encoder, abaixo da escala e distinto do decode autoregressivo solicitado. Não atribuir ganhos de GPU/C++ à destilação isoladamente nem generalizar precisão de busca a geração aberta.
Fontes: V4B-S009.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: Pode inspirar uma proposta LAI, sem comprovar sua adoção.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: Fornece contratos de dados e checkpoints para um pipeline editorial proposto.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q008, V4B-Q009, V4B-Q023.

## P017:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P017 → T178 [feeds]
Como combinar: O caminho paramétrico organiza sinais de conhecimento ou comportamento do professor.
Interface: Dados, logits ou respostas e critérios de filtro.
Condição: Sinal disponível e objetivos explícitos.
Aceite proposto: Comparar aluno com referência independente em casos novos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P017 → T181 [alternative]
Como combinar: O caminho de memória preserva procedimentos externos em vez de atualizar necessariamente pesos.
Interface: Trajetórias, pré-condições e versões.
Condição: Memórias são recuperáveis e executáveis no ambiente.
Aceite proposto: Testar deriva de ferramenta e erros sem falha sintática.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P017 → P016 [requires]
Como combinar: Avaliação proposta decide promoção do artefato sob contrato de implantação.
Interface: Manifesto, métricas e casos reservados.
Condição: Sem vazamento de dados para geração ou seleção.
Aceite proposto: Rejeitar melhora apenas aparente por contaminação ou mudança de teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter dados de avaliação fora da seleção do professor e das memórias.
- Não chamar filtragem de respostas de treinamento quando nenhum estado persistente foi atualizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A proposta busca competência especializada com custo menor. A comparação com fronteira deve igualar tarefa e informação disponível e incluir limites do aluno; não há promessa de inteligência geral transferida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T069, T178, T179, T180, T181, R012, R015, P016

## Fontes primárias associadas

### C-S032 — Distilling the Knowledge in a Neural Network

[https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Destilação transfere comportamento de professor ou ensemble a modelo aluno.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

### V4B-S009 — Microsoft open sources breakthrough optimizations for transformer inference on GPU and CPU

[https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/](https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Bing usou destilação de BERT e otimizações de inferência em produção; integração posterior no ONNX Runtime.

Limite: Caso histórico de encoder, não LLM autoregressivo de 3–30B; não somar ganhos de hardware e algoritmo como efeito de destilação.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S021 — Claude's new constitution

[https://www.anthropic.com/news/claude-new-constitution](https://www.anthropic.com/news/claude-new-constitution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Constituição usada em treinamento e síntese de exemplos/rankings; método evoluiu desde Constitutional AI.

Limite: Texto de princípios e treinamento não garantem aderência de toda saída; parâmetros do modelo não são publicados nesta fonte.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

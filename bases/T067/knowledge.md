# T067 — Active Memory Retrieval

**Nome canônico:** Active Memory Retrieval  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T067  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recuperação ativa de memória

## T067:C01 — conceito

Consulta memória durante a execução conforme novas necessidades surgem, em vez de carregar tudo somente no início. A busca pode ser acionada por lacuna, dependência ou referência explícita. O agente precisa avaliar se obteve evidência suficiente e limitar buscas sem progresso.

Como funciona:
- Identificar informação ausente necessária à próxima ação.
- Selecionar consulta, índice ou referência exata.
- Incorporar resultado validado e atualizar a lista de lacunas.

## T067:C02 — aplicacao

Quando usar:
- Missões com objetivos que se desdobram em subtarefas.
- Recuperação de experiências anteriores durante diagnóstico.

Quando não usar:
- Não depender apenas de o modelo verbalizar dúvida para recuperar restrições obrigatórias.

Implementação proposta:
- Proposta: combinar gatilhos determinísticos e solicitações do modelo.
- Registrar consultas, resultados e uso posterior da evidência.
- Encerrar ou escalar quando repetidas buscas não acrescentam material relevante.

Aplicação LAI proposta:
Proposta LAI: antes de alterar um contrato, recuperar decisões vigentes, incidentes relacionados e versão do schema; o mecanismo não deve ficar restrito a similaridade de texto.

## T067:C03 — riscos_validacao

Armadilhas:
- O agente pode buscar confirmação e ignorar evidências contrárias.
- O custo de várias buscas pode superar uma carga inicial bem escolhida.

Métricas sugeridas:
- Cobertura de informações necessárias à ação.
- Buscas úteis por chamada e custo por missão concluída.

Testes propostos:
- Forçar dependência de um episódio antigo e observar recuperação antes da ação.
- Devolver resultados irrelevantes repetidos e exigir parada com lacuna declarada.

## T067:C04 — perguntas_proveniencia

Pergunta: Active retrieval precisa de um banco vetorial?
Resposta: Não. Uma leitura por ID ou consulta SQL também pode ser recuperação ativa.

Pergunta: Recuperar uma memória a torna verdadeira?
Resposta: Não. Origem, validade e evidência continuam necessárias após a recuperação.

Pergunta: Preciso ter acesso a probabilidades de tokens?
Resposta: Para reproduzir um gatilho baseado nelas, sim. Se a API não fornece o sinal, documente outra política em vez de alegar equivalência.

Pergunta: A busca deve substituir toda a resposta provisória?
Resposta: Não necessariamente. Reavalie os trechos dependentes da nova evidência e preserve rastreabilidade; mudanças locais também podem alterar conclusões posteriores.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T067:C05 — mecanismo_avancado

Recuperação ativa inclui duas decisões: quando consultar e o que formular como consulta. FLARE usa uma continuação antecipada para orientar busca quando tokens têm baixa confiança; Self-RAG aprende tokens de reflexão para decidir e avaliar recuperação. São mecanismos diferentes. Uma implementação que apenas pede ao modelo para dizer se está confiante não reproduz automaticamente o treinamento nem os sinais internos desses trabalhos.

Condição de contorno:
Baixa confiança pode refletir estilo ou token raro, e alta confiança pode coexistir com erro factual; um gatilho isolado não cobre todas as lacunas.

Contrato proposto:
- Entradas: Geração em andamento, dependências conhecidas, sinais disponíveis e memória elegível.
- Saídas: Busca motivada, evidências recuperadas e continuação revisada ou lacuna mantida.
- Estado: Consultas anteriores, origem dos gatilhos, orçamento e vínculos entre trechos gerados e suporte.
- Invariante: Recuperar informação nova não converte o texto provisório que motivou a busca em evidência.

Compromissos de projeto:
- Consultar durante a geração adapta a evidência ao que surge e aumenta latência sequencial.
- Gatilhos aprendidos podem melhorar seleção e dependem do modelo treinado; regras explícitas são menos flexíveis e mais observáveis.

## T067:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar uma afirmação errada com alta confiança e outra correta com termo raro. A avaliação deve mostrar os falsos negativos e positivos do gatilho, mantendo verificações obrigatórias de dependência.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação inicial, periódica e ativa com limites iguais de chamadas. Medir cobertura de suporte, buscas desnecessárias, correções após busca e custo total; avaliar acionamento e qualidade da consulta separadamente.

Comparações:
- T044 (complements): Expansão é a política de ampliar contexto; recuperação ativa fornece mecanismos de acionamento durante a execução.
- T036 (complements): Adaptação da consulta pode melhorar o conteúdo recuperado depois que o gatilho decide buscar.

Afirmação rastreável:
FLARE e Self-RAG propõem mecanismos distintos de recuperação adaptativa durante a produção de respostas.
Suporte: direct; fontes: V3A-S010, V3A-S009
Limite: A fonte não valida qualquer heurística verbal de autoconfiança como equivalente aos mecanismos treinados ou probabilísticos apresentados.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T067:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu sinais de FLARE e Self-RAG. Aqui recuperação ativa é guiada por falhas verificáveis de evidência e valor da próxima busca.

Projeto e decomposição
Defina gatilhos como campo obrigatório sem suporte, conflito de versões e necessidade de dado atual. Probabilidade de token e confiança verbal não são equivalentes a suficiência de evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S009, V3A-S010, V4A-S014, C-S030.

Controle adaptativo
Antes de buscar, registrar qual observação mudaria a resposta. Se a consulta retorna novamente conteúdo equivalente, mudar fonte ou encerrar com lacuna, evitando busca compulsiva.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S009, V3A-S010, V4A-S014, C-S030.

Validação contrafactual
Compare recuperação em toda etapa, uma vez e por gatilho. Meça buscas úteis, afirmações sem suporte e custo por resposta aceita; incluir tarefas em que nenhuma fonte contém resposta. Unidade de avaliação: decisão de recuperar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S009, V3A-S010, V4A-S014, C-S030.

USO AVANÇADO — Geração de relatório factual
Cenário: Uma frase exige número não presente.
Estratégia: Interromper preenchimento desse campo, consultar fonte estruturada e retomar com unidade e período; não inventar valor provisório.
Papel do modelo pequeno: 3–7B detecta campo; 8–14B redige.
Aceite proposto: Todo número final deve possuir origem e escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S009, V3A-S010, V4A-S014, C-S030.

USO AVANÇADO — Investigação iterativa
Cenário: Nova evidência altera hipótese.
Estratégia: Gerar consulta discriminante para hipótese alternativa e comparar suporte antes de continuar síntese.
Papel do modelo pequeno: 15–30B planeja sequência.
Aceite proposto: Nova busca deve produzir evidência diferente ou justificar parada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S009, V3A-S010, V4A-S014, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Detector de campos sem evidência em formato fechado.
8–14B: Leitor que identifica conflito e solicita uma busca específica.
15–30B: Planejador de recuperação dependente de descobertas anteriores.
Requisitos de treino/runtime: Sinais observáveis de suporte, orçamento de tentativas e registro de consultas; métodos com tokens especiais exigem modelo treinado.
Não aplicar quando: Não existe canal plausível de informação nova ou o controlador só usa autoconfiança não calibrada.

## T067:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Novas buscas dependem das descobertas intermediárias.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

V4A-C021 — Google DeepMind / DataGemma RIG/RAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto publica variantes para fundamentar geração em Data Commons.
Mecanismo documentado: RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.
Correspondência com esta base: RIG reconhece necessidade de consultar para corrigir número.
Transferência proposta para modelo pequeno: Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.
Limite: RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q010, V4A-Q017, V4A-Q020.

## T067:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T067 → T036 [feeds]
Como combinar: Transformar lacuna em consulta preservando restrições.
Interface: Campo, entidade, tempo e tipo de suporte.
Condição: Consulta direcionada à lacuna efetiva.
Aceite proposto: Testar reformulação que altera entidade e exigir correção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S009, V3A-S010, V4A-S014, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T067 → T218 [requires]
Como combinar: Interromper busca repetida sem informação nova.
Interface: Histórico de consultas e evidências únicas.
Condição: Identidade de resultados ser rastreável.
Aceite proposto: Repetir paráfrases e detectar estagnação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S009, V3A-S010, V4A-S014, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não citar texto gerado durante busca como evidência externa.
- Não penalizar abstenção correta em caso sem resposta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar decisões de quando buscar e fidelidade final; recuperação ativa pode aumentar custo sem melhorar qualidade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T036, T044, T066, T078

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S010 — Active Retrieval Augmented Generation

[https://arxiv.org/abs/2305.06983](https://arxiv.org/abs/2305.06983)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: FLARE usa previsão da próxima sentença e sinais de confiança para decidir consultas e regeneração.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S009 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

[https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação e crítica adaptativas aprendidas com tokens de reflexão; distingue arquitetura treinada de simples instrução de autocrítica.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

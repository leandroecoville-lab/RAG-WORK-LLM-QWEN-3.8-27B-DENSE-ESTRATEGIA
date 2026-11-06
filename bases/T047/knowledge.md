# T047 — Long-Term Memory — memória de longo prazo

**Nome canônico:** Long-Term Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T047  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória de longo prazo; Long-Term Memory

## T047:C01 — conceito

Informação persistente disponível entre sessões ou missões, como fatos, episódios e procedimentos. Sua existência no armazenamento não garante recuperação na hora correta. É necessário definir identidade, validade, escopo e como a memória será consultada e atualizada.

Como funciona:
- Capturar registros relevantes com origem e tempo.
- Persistir em armazenamento durável e indexável.
- Recuperar por tarefa e atualizar sem apagar a história necessária.

## T047:C02 — aplicacao

Quando usar:
- Agentes que acompanham projetos por longos períodos.
- Preferências e conhecimento que precisam sobreviver ao processo atual.

Quando não usar:
- Não salvar toda saída do modelo como fato comprovado nem usar pesos como banco exato de dados mutáveis.

Implementação proposta:
- Proposta: separar fatos observados, inferências e hipóteses.
- Armazenar namespace, fonte, versão e condição de expiração.
- Avaliar recuperação após nova sessão e corrigir memórias sem perder proveniência.

Aplicação LAI proposta:
Proposta LAI: construir memória externa da Helena como serviço auditável; importar conhecimento não significa treinamento automático dos pesos.

## T047:C03 — riscos_validacao

Armadilhas:
- Uma memória incorreta pode reforçar-se pela repetição.
- Armazenamento sem políticas de seleção cresce e dificulta achar o relevante.

Métricas sugeridas:
- Recall de fatos úteis entre sessões.
- Taxa de memórias falsas, obsoletas ou indevidamente compartilhadas.

Testes propostos:
- Encerrar o processo e recuperar uma decisão em nova execução.
- Inserir correção posterior e exigir que a resposta use a versão válida.

## T047:C04 — perguntas_proveniencia

Pergunta: O agente aprendeu porque um arquivo foi salvo?
Resposta: Ele ganhou informação persistida. Aprendizagem comportamental e recuperação confiável ainda precisam ser demonstradas.

Pergunta: Long-term memory precisa de banco vetorial?
Resposta: Não. Chaves, SQL, arquivos, grafos e busca lexical podem ser adequados conforme o tipo de informação.

Pergunta: Como saber se o problema está no banco ou na LLM?
Resposta: Teste se o fato foi registrado, se aparece entre candidatos elegíveis e se a resposta o usa corretamente. Cada etapa exige uma verificação própria.

Pergunta: Persistência em RAM basta para memória longa?
Resposta: Somente dentro da vida daquele processo. Para sobreviver a reinícios é necessário um armazenamento com durabilidade compatível com o contrato.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T047:C05 — mecanismo_avancado

A memória durável possui ao menos três pontos de perda: o escritor pode não registrar o fato, o recuperador pode não encontrá-lo e o leitor pode interpretá-lo incorretamente. Avaliar apenas a resposta final mistura esses erros. Também há diferença entre lembrar numa conversa antiga e transferir informação entre threads: a chave de sessão não identifica necessariamente o proprietário ou o escopo da memória compartilhável.

Condição de contorno:
Persistir mais dados não ajuda quando a política de escrita omite fatos necessários ou quando os filtros de identidade impedem recuperá-los no contexto correto.

Contrato proposto:
- Entradas: Eventos candidatos, identidade estável, escopo de compartilhamento e política de admissão.
- Saídas: Memórias duráveis com fonte e índice consultável, incluindo registro de correções posteriores.
- Estado: Revisão do escritor, namespace, índices e estado de processamento de cada evento.
- Invariante: Uma sessão nova pode consultar apenas memórias elegíveis ao mesmo proprietário e escopo autorizado.

Compromissos de projeto:
- Escrever fatos seletivos reduz leitura futura e pode perder detalhes ainda não considerados úteis.
- Guardar também eventos originais permite reprocessamento e aumenta custos de armazenamento e recuperação.

## T047:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: encerrar o processo, iniciar outra thread e perguntar por um fato alterado entre sessões. O sistema deve recuperar a versão apropriada com origem, sem confundir continuidade com histórico ativo.

Plano de avaliação proposto:
Avaliação proposta: separar avaliação de escrita, recuperação e leitura. Comparar histórico integral, memórias extraídas e combinação com originais; medir cobertura, atualização correta, abstinência quando falta evidência e custo acumulado ao longo de sessões.

Comparações:
- T064 (distinct_from): Estado persistente conserva execução; memória longa conserva conhecimento reutilizável que pode atravessar várias execuções.
- T068 (complements): A geração aumentada por memória é uma forma de consumir registros duráveis selecionados.

Afirmação rastreável:
Mem0 organiza extração, consolidação e recuperação; LongMemEval distingue etapas de indexação, recuperação e leitura.
Suporte: direct; fontes: V3A-S033, V3A-S002
Limite: A existência dessas arquiteturas não demonstra memória perfeita ou ganho automático no domínio do usuário.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T047:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou escrita, busca e leitura. Aqui memória de longo prazo é avaliada por utilidade futura e custo de correções.

Projeto e decomposição
Admitir memória deve responder qual tarefa futura ela pode melhorar. Informação disponível externamente e barata de buscar pode merecer referência, enquanto preferência explícita recorrente pode merecer registro curto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S026, V3A-S002.

Controle adaptativo
Meça benefício depois de várias sessões e correções. Uma memória útil inicialmente pode tornar-se prejudicial quando contexto muda; atualização e esquecimento precisam de evidência observável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S026, V3A-S002.

Validação contrafactual
Compare lembrar tudo, admissão seletiva e nenhuma memória entre sessões. Meça respostas melhoradas, fatos antigos indevidamente aplicados e custo de manutenção, não somente volume armazenado. Unidade de avaliação: sequência de sessões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S026, V3A-S002.

USO AVANÇADO — Preferências de projeto
Cenário: Usuário define convenções que evoluem.
Estratégia: Guardar preferência com escopo e data, solicitar ou observar correção explícita e aplicar apenas em tarefas elegíveis.
Papel do modelo pequeno: 3–7B extrai declaração explícita.
Aceite proposto: Não transformar preferência de um projeto em regra global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S026, V3A-S002.

USO AVANÇADO — Aprendizado operacional
Cenário: Incidentes revelam procedimento útil.
Estratégia: Registrar resultado e condições do incidente, testar transferência em novo caso antes de promover regra reutilizável.
Papel do modelo pequeno: 8–14B recupera; 15–30B compara contexto.
Aceite proposto: Nova recomendação deve citar condições compartilhadas e diferenças relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S026, V3A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de preferências explícitas e fatos estáveis em esquema simples.
8–14B: Recuperador e leitor de pequenas memórias por projeto.
15–30B: Comparador de experiências para decidir transferência entre contextos.
Requisitos de treino/runtime: Identidade, escopo, validade e caminho de correção; armazenamento externo não exige atualizar pesos.
Não aplicar quando: Memória não pode ser corrigida, atribuída à origem ou limitada ao contexto em que vale.

## T047:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Persistência entre sessões é afirmada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

V4A-C018 — OpenAI / ChatGPT Memory
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Produto documenta memórias salvas e uso de histórico para personalização.
Mecanismo documentado: Informações selecionadas podem atravessar conversas com controles próprios.
Correspondência com esta base: Persistência útil entre sessões é documentada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Criar memória externa pequena de preferências explícitas e testar correções e escopo.
Limite: Comportamento varia por conta; fonte não revela algoritmo nem prova precisão permanente. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S017.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q013, V4A-Q023.

## T047:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T047 → T071 [requires]
Como combinar: Promover apenas candidato com utilidade e evidência.
Interface: Candidato, origem, escopo e critério de promoção.
Condição: Critério variar por tipo de memória.
Aceite proposto: Inserir hipótese plausível e impedir promoção como fato.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S017, V4A-S026, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T047 → T075 [complements]
Como combinar: Reconciliar memória anterior após correção.
Interface: Versões concorrentes e evento de correção.
Condição: Regra de preferência não apagar histórico relevante.
Aceite proposto: Retomar sessão após correção e verificar uso da versão certa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S017, V4A-S026, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não prometer recordar tudo que foi salvo.
- Não confundir frequência de menção com validade permanente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade e correções ao longo de sessões; memória melhor não implica inteligência geral maior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T054, T055, T062

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S033 — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

[https://arxiv.org/abs/2504.19413](https://arxiv.org/abs/2504.19413)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração, consolidação e recuperação de memória conversacional; variante com grafo.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

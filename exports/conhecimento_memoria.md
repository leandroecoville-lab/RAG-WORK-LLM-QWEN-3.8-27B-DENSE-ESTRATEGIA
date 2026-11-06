# Memória, persistência e conhecimento

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

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


---

# T048 — Memory Management

**Nome canônico:** Memory Management  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T048  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gestão de memória

## T048:C01 — conceito

Conjunto de políticas para escrever, organizar, recuperar, corrigir, promover, compactar e remover informação de memória. Controla o ciclo de vida e a qualidade do acervo. Não é apenas escolher um banco de dados ou aumentar a quantidade armazenada.

Como funciona:
- Aplicar critérios de admissão e metadados na escrita.
- Escolher o que recuperar e em qual nível de detalhe.
- Reconciliar mudanças, expiração e uso do espaço disponível.

## T048:C02 — aplicacao

Quando usar:
- Agentes persistentes com fontes mutáveis.
- Múltiplas missões compartilham fatos e procedimentos.

Quando não usar:
- Não automatizar promoção de hipótese para fato somente com base na confiança textual do modelo.

Implementação proposta:
- Proposta: definir políticas separadas para eventos, fatos e skills.
- Registrar decisões de promoção, invalidação e remoção.
- Manter mecanismos de reconstrução e indicadores de memórias conflitantes ou sem fonte.

Aplicação LAI proposta:
Proposta LAI: centralizar regras de memória sob a orquestração da Helena, com autorização por domínio e testes de recuperação antes de declarar autoaprendizagem.

## T048:C03 — riscos_validacao

Armadilhas:
- Políticas de retenção podem apagar dados necessários para auditar decisões.
- Memória excessiva e mal indexada pode piorar seleção e custo.

Métricas sugeridas:
- Precisão da recuperação e taxa de obsolescência.
- Crescimento, latência e número de conflitos não resolvidos.

Testes propostos:
- Ingerir duplicatas e confirmar consolidação sem perder fontes.
- Revogar um fato e verificar propagação aos resumos e procedimentos dependentes.

## T048:C04 — perguntas_proveniencia

Pergunta: Gerenciar memória exige uma LLM?
Resposta: Não em todas as etapas. Integridade, versões, acesso e expiração podem ser determinísticos.

Pergunta: Qual é o melhor sinal de memória útil?
Resposta: Melhoria comprovada na execução de novas tarefas, com origem e validade das informações utilizadas.

Pergunta: É preciso apagar uma memória para esquecer seu uso?
Resposta: Não. Pode removê-la da seleção ativa, reduzir prioridade ou arquivar o índice, preservando o registro quando necessário.

Pergunta: Qual custo precisa entrar na decisão?
Resposta: Escrita, manutenção, indexação, recuperação, releitura e correção. Otimizar somente tokens da próxima resposta pode aumentar o custo total.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T048:C05 — mecanismo_avancado

Gerenciar memória envolve decisões acopladas: admitir tudo aumenta custo de recuperação, enquanto consolidar cedo pode apagar contexto antes que seu valor seja conhecido. Políticas devem distinguir validade factual, prioridade de leitura e retenção física. Uma memória pouco acessada pode continuar verdadeira e obrigatória; outra muito frequente pode estar obsoleta. Confundir essas dimensões transforma estatísticas de uso em decisões incorretas sobre conhecimento.

Condição de contorno:
Uma política uniforme costuma falhar quando o mesmo store contém preferências, evidência histórica, resultados transitórios e procedimentos com ciclos de atualização diferentes.

Contrato proposto:
- Entradas: Eventos de criação, acesso, correção e pressão de capacidade, com classe da memória.
- Saídas: Decisões de admissão, reorganização, revisão ou descarte, cada uma com motivo rastreável.
- Estado: Políticas versionadas, dependências entre derivados e fontes e fila de manutenção pendente.
- Invariante: Reduzir prioridade de recuperação não equivale a invalidar a afirmação nem autoriza apagar sua única evidência.

Compromissos de projeto:
- Automatizar organização reduz manutenção manual e introduz erros que podem se propagar entre notas.
- Políticas por classe preservam semântica de retenção e aumentam o número de contratos a operar.

## T048:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: marcar como raramente acessada uma regra ainda vigente e como popular uma regra revogada. A manutenção deve conservar a primeira e impedir que frequência restaure a validade da segunda.

Plano de avaliação proposto:
Avaliação proposta: comparar política fixa, recência e política por classes em uma sequência com mudanças. Medir qualidade posterior, custo de manutenção, atrasos de correção e perdas irreversíveis; contar consultas extras geradas por memória descartada cedo.

Comparações:
- T074 (complements): Eviction é uma operação de capacidade dentro de um ciclo de vida mais amplo.
- T058 (complements): Consolidação reorganiza conteúdo; a gestão decide quando e sob quais invariantes executar essa transformação.

Afirmação rastreável:
MemoryBank usa atualização inspirada em esquecimento e reforço; A-MEM permite que novas notas alterem representações de memórias anteriores.
Suporte: direct; fontes: V3A-S036, V3A-S034
Limite: São políticas de pesquisa distintas, sem prova de que uma imitação do esquecimento humano seja ótima para memória operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T048:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu ciclo de vida. Aqui gestão de memória usa orçamentos separados por tipo e mede custo de qualidade do acervo.

Projeto e decomposição
Separe orçamento de evidências, fatos, episódios e procedimentos. Remover detalhe episódico antigo pode ser aceitável; remover evidência de uma regra ativa pode quebrar auditabilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

Controle adaptativo
Crie fila de manutenção com prioridade por impacto: memória sem fonte, conflito ativo, índice atrasado e candidato redundante exigem tratamentos distintos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

Validação contrafactual
Compare políticas sob crescimento contínuo do acervo. Meça utilidade por consulta, registros inválidos recuperados e tempo de manutenção; custo de indexação e reparo entra junto com armazenamento. Unidade de avaliação: coleção de memórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

USO AVANÇADO — Assistente de múltiplos projetos
Cenário: Memórias competem por espaço.
Estratégia: Aplicar quotas por projeto e tipo, mantendo referências a evidências de decisões ativas. Evitar que projeto muito acessado elimine histórico necessário de outro.
Papel do modelo pequeno: 3–7B classifica tipo; regras aplicam quotas.
Aceite proposto: Nenhuma remoção pode quebrar decisão ainda ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

USO AVANÇADO — Acervo com correções frequentes
Cenário: Índices e resumos ficam atrasados.
Estratégia: Priorizar reparo de objetos usados em tarefas pendentes e suspender promoção quando manutenção estiver atrasada demais.
Papel do modelo pequeno: 8–14B identifica dependências afetadas.
Aceite proposto: Consulta sensível deve detectar projeção desatualizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo, duplicação e estado de manutenção.
8–14B: Revisor de conflitos e propostas de consolidação locais.
15–30B: Planejador de manutenção entre coleções com dependências complexas.
Requisitos de treino/runtime: Inventário por tipo, métricas de consulta e dependências; ações irreversíveis exigem política explícita do sistema.
Não aplicar quando: A mesma operação mistura relevância, retenção e exclusão sem estados separados.

## T048:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C009 — Meta / CacheLib em serviços Facebook
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Artigo de operadores relata adoção desde 2017 por múltiplos serviços.
Mecanismo documentado: Engine comum para desenvolvimento e operação de caches de dados e armazenamento.
Correspondência com esta base: Ciclo de vida físico inspira gestão, sem avaliar utilidade semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar política determinística de residência e estimativa de utilidade proposta pelo modelo.
Limite: Não afirma cache semântico, resumo, verdade da memória ou taxa de acerto de LLM. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q013, V4A-Q023.

## T048:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T048 → T058 [feeds]
Como combinar: Encaminhar redundâncias para consolidação verificável.
Interface: Conjunto candidato, dependências e escopo.
Condição: Consolidação preservar evidência e divergência.
Aceite proposto: Comparar respostas antes e depois da manutenção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S032, V4A-S010, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T048 → T074 [complements]
Como combinar: Gerenciar residência sem apagar memória canônica.
Interface: Objeto, custo de recarga e estado de retenção.
Condição: Evicção e exclusão terem operações distintas.
Aceite proposto: Remover da janela e recuperar da origem durável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S032, V4A-S010, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar tamanho do acervo como indicador de aprendizado.
- Não deixar manutenção apagar a única origem de uma conclusão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade da memória sob crescimento e correção; armazenamento maior não garante respostas melhores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T058, T071, T074, T075

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

### V3A-S036 — MemoryBank: Enhancing Large Language Models with Long-Term Memory

[https://arxiv.org/abs/2305.10250](https://arxiv.org/abs/2305.10250)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória recuperável e política de atualização inspirada em esquecimento e reforço por tempo e significância.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S034 — A-MEM: Agentic Memory for LLM Agents

[https://arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Notas estruturadas, conexão entre memórias e evolução das representações de notas anteriores.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T049 — Episodic Memory

**Nome canônico:** Episodic Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T049  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória episódica

## T049:C01 — conceito

Registra experiências situadas: objetivo, contexto, ações, resultados, tempo e evidências. Permite recuperar casos anteriores para orientar novas tarefas. Um episódio mostra o que ocorreu em determinadas condições; não prova sozinho uma regra geral nem garante que a mesma ação funcionará novamente.

Como funciona:
- Delimitar uma experiência e identificar participantes, ambiente e versão.
- Registrar sequência e resultados com evidências.
- Indexar por problema, condições e desfecho para recuperação futura.

## T049:C02 — aplicacao

Quando usar:
- Aprender procedimentos a partir de incidentes ou missões concluídas.
- Retomar casos semelhantes com contexto operacional verificável.

Quando não usar:
- Não reduzir uma experiência a uma frase de sucesso sem guardar condições e falhas.

Implementação proposta:
- Proposta: separar observações, ações propostas, ações executadas e resultados validados.
- Manter um resumo do episódio e referências ao log completo.
- Recuperar casos contrastantes, incluindo tentativas malsucedidas, para evitar confirmação seletiva.

Aplicação LAI proposta:
Proposta LAI: armazenar auditorias e correções da Helena como episódios verificáveis antes de promover seus aprendizados a skills.

## T049:C03 — riscos_validacao

Armadilhas:
- Relato do agente pode confundir intenção com execução.
- Um caso de outra versão pode induzir uma correção incompatível.

Métricas sugeridas:
- Recall de episódios relevantes e diversidade de resultados.
- Melhoria em tarefas novas comparada à execução sem memória.

Testes propostos:
- Buscar um incidente conhecido sem mencionar seu ID.
- Alterar versão do ambiente e exigir que a solução antiga seja revalidada.

## T049:C04 — perguntas_proveniencia

Pergunta: Episódio é a conversa inteira?
Resposta: Pode conter conversa, mas deve ter fronteiras, objetivo e resultado. Um histórico bruto não fornece automaticamente essa estrutura.

Pergunta: Uma correção que funcionou vira regra?
Resposta: Vira evidência de um caso. Generalização exige condições de aplicação e novas avaliações.

Pergunta: Qual é a unidade correta de episódio?
Resposta: A menor sequência que conserva objetivo, condições e desfecho interpretável. Pode atravessar sessões; uma sessão pode conter vários episódios.

Pergunta: Casos incompletos devem entrar no índice?
Resposta: Podem ser úteis, desde que a incompletude seja recuperável como campo. O leitor não deve interpretar ausência de resultado como resultado negativo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T049:C05 — mecanismo_avancado

Um episódio precisa preservar o que o agente sabia no momento da decisão. Acrescentar a solução descoberta depois à descrição inicial cria retrospectiva enganosa e ensina um procedimento impossível de reproduzir. Resultados também podem ser censurados: uma tarefa interrompida não é necessariamente fracasso, e sucesso sem verificação pode ser apenas ausência de erro observado. Esses estados devem sobreviver à síntese do caso.

Condição de contorno:
Casos históricos deixam de orientar bem quando foram selecionados somente por sucesso ou quando as condições anteriores à ação não podem ser reconstruídas.

Contrato proposto:
- Entradas: Sequência do episódio, evidências disponíveis por etapa e observações posteriores separadas.
- Saídas: Caso recuperável com contexto inicial, decisões, desfecho e limitações de observação.
- Estado: Versões do ambiente, fronteiras do episódio, participantes e proveniência dos resultados.
- Invariante: Informação conhecida depois não aparece como premissa disponível antes de sua observação.

Compromissos de projeto:
- Episódios completos melhoram análise de sequência e aumentam o custo de leitura.
- Resumos favorecem busca por problema e podem esconder tentativas malsucedidas que explicam o desfecho.

## T049:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: registrar uma tarefa encerrada antes da validação e adicionar a conclusão em data posterior. A consulta histórica deve distinguir resultado desconhecido naquele instante de resultado posteriormente confirmado.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação por objetivo e por condições iniciais usando casos positivos, negativos e interrompidos. Medir adequação da analogia, reconstrução temporal e confusão entre intenção e efeito; avaliar transferência entre versões separadamente.

Comparações:
- T070 (complements): O episodic store fornece armazenamento e índices; memória episódica define a unidade de experiência e sua interpretação.
- T057 (distinct_from): Uma sequência lembrada pode sugerir hipótese, mas não identifica por si só o efeito de uma intervenção.

Afirmação rastreável:
Generative Agents mantém experiências em um fluxo de memória e usa sua recuperação para orientar comportamento.
Suporte: direct; fontes: A-S008
Limite: A avaliação de plausibilidade em simulação não demonstra validade causal nem qualidade de procedimentos de produção.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T049:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou episódios e vazamento retrospectivo. Aqui recuperação usa semelhança de condições e resultados negativos para evitar transferência superficial.

Projeto e decomposição
Indexe condições iniciais, ação, resultado e fatores desconhecidos separadamente. Episódios com narrativa parecida podem exigir ações opostas quando uma pré-condição muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

Controle adaptativo
Recupere exemplos de sucesso e falha com condições próximas. Ausência de falhas no histórico pode refletir seleção de registros, não prova de segurança do procedimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

Validação contrafactual
Compare recuperação por texto integral e por condições estruturadas. Meça recomendações transferidas indevidamente, cobertura de falhas e qualidade em episódios com resultado ainda pendente. Unidade de avaliação: episódio completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

USO AVANÇADO — Diagnóstico recorrente
Cenário: Sintomas semelhantes tiveram causas diferentes.
Estratégia: Recuperar episódios por ambiente e versão, comparar testes discriminantes e evitar repetir ação que falhou nas mesmas condições.
Papel do modelo pequeno: 8–14B compara episódios.
Aceite proposto: Recomendação deve explicar condição compartilhada e diferença que pode invalidar transferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

USO AVANÇADO — Aprendizado de projeto
Cenário: Uma decisão anterior parece reutilizável.
Estratégia: Carregar contexto da escolha e alternativas rejeitadas; testar se restrições atuais ainda coincidem antes de aplicar.
Papel do modelo pequeno: 15–30B integra experiências.
Aceite proposto: Não usar resultado posterior que ainda não era conhecido na data avaliada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de condições, ações e resultados explícitos.
8–14B: Comparador de poucos episódios com esquema comum.
15–30B: Planejador de testes para adaptar experiência a contexto parcialmente diferente.
Requisitos de treino/runtime: Registro de episódios com estados pendente/concluído e documentação das condições observadas.
Não aplicar quando: Histórico registra somente casos bem-sucedidos ou omite condições que determinam o resultado.

## T049:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Experiências recuperáveis integram a arquitetura.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q008, V4A-Q023.

## T049:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T049 → T070 [requires]
Como combinar: Buscar episódios por campos e não apenas similaridade.
Interface: Condições, tempo, ação e estado do resultado.
Condição: Store permitir filtros e paginação verificável.
Aceite proposto: Recuperar também falha rara com mesmas pré-condições.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T049 → T055 [feeds]
Como combinar: Transformar experiência em procedimento candidato.
Interface: Episódios de suporte, limites e exceções.
Condição: Transferência validada antes de uso geral.
Aceite proposto: Aplicar a contexto com pré-condição ausente e exigir recusa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar correlação entre ação e resultado como causalidade.
- Não transformar resultado desconhecido em falha.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar transferência correta de experiência, não plausibilidade da narrativa recuperada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T058, T070, T071, T181

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T050 — Working Memory Window

**Nome canônico:** Working Memory Window  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T050  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela de memória de trabalho

## T050:C01 — conceito

Parte da informação operacional mantida ativamente para a etapa corrente: objetivo, próximos passos, dados recentes e dependências. Pode ser materializada em mensagens e campos estruturados. É memória de trabalho do sistema, não uma leitura dos estados internos ocultos da LLM.

Como funciona:
- Identificar a decisão ou ação da próxima etapa.
- Carregar estado e evidências necessárias.
- Remover ou arquivar conteúdo concluído mantendo ponteiros para reabertura.

## T050:C02 — aplicacao

Quando usar:
- Agentes de execução com orçamento restrito.
- Fluxos que alternam análise, ferramentas e verificação.

Quando não usar:
- Não confundir a janela ativa com todo o conhecimento persistido ou com a totalidade do histórico.

Implementação proposta:
- Proposta: manter objetivo, restrições, etapa e dúvidas em campos pequenos.
- Reservar uma parcela do orçamento para novas observações.
- Atualizar a janela apenas depois de persistir resultados que precisam sobreviver.

Aplicação LAI proposta:
Proposta LAI: usar um estado de missão compacto da Helena como núcleo e anexar evidência específica conforme a tarefa, sem prometer retenção ilimitada na janela.

## T050:C03 — riscos_validacao

Armadilhas:
- Um plano desatualizado pode continuar ocupando posição privilegiada.
- Reduzir demais a janela impede interpretar a próxima ferramenta.

Métricas sugeridas:
- Correção da próxima ação e retomada.
- Tokens ativos e referências abertas por rodada.

Testes propostos:
- Trocar a etapa do workflow e verificar mudança das informações carregadas.
- Remover detalhe já arquivado e recuperá-lo quando uma dependência reaparecer.

## T050:C04 — perguntas_proveniencia

Pergunta: Working memory é um arquivo ou um prompt?
Resposta: É um papel funcional. Pode usar arquivos, estado e prompt, desde que o necessário seja carregado para a decisão.

Pergunta: Ela deve guardar todas as tentativas anteriores?
Resposta: Não necessariamente. Tentativas podem ficar no registro episódico e ser recuperadas quando úteis.

Pergunta: O scratchpad inteiro deve ficar ativo?
Resposta: Não necessariamente. Mantenha os campos que condicionam a próxima decisão e referências para detalhes, verificando se as relações necessárias continuam disponíveis.

Pergunta: Uma referência ocupa menos tokens que seu conteúdo; por que não usar só referências?
Resposta: Porque o modelo precisa ler a informação relevante para decidir. Ponteiros economizam espaço apenas quando podem ser resolvidos a tempo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T050:C05 — mecanismo_avancado

A janela de trabalho é uma visão operacional derivada de estado e fontes, com vida útil ligada à etapa. Convém separar itens fixos, como objetivo vigente, de itens temporários, como uma observação que serve à próxima decisão. Após a etapa, parte do conteúdo pode ser promovida a memória durável e parte descartada. Essa rotação não corresponde a apagar parâmetros nem a modificar diretamente estados neurais ocultos.

Condição de contorno:
Se a tarefa exige relações entre muitos itens simultâneos, externalizar tudo sem uma representação de ligação pode impedir que o modelo compare as evidências necessárias.

Contrato proposto:
- Entradas: Objetivo atual, transição pretendida, observações recentes e referências a conteúdo disponível.
- Saídas: Visão compacta com dependências suficientes para a decisão e lacunas explicitamente abertas.
- Estado: Revisão da visão, conteúdo fixado, observações temporárias e orçamento reservado à próxima interação.
- Invariante: Toda decisão baseada na janela identifica a versão do estado e das evidências que estavam presentes.

Compromissos de projeto:
- Reduzir material temporário diminui ruído e pode aumentar consultas repetidas.
- Fixar conteúdo essencial protege continuidade e reduz espaço para novas evidências; o conjunto fixo também precisa revisão.

## T050:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: concluir uma subtarefa e mudar o objetivo mantendo uma hipótese anterior no bloco fixo. A reconstrução deve revisar a hipótese e carregar dependências do novo objetivo.

Plano de avaliação proposto:
Avaliação proposta: comparar janela recente e visão por etapa, mantendo o mesmo orçamento. Medir ações corretas, abertura repetida de fontes, uso de hipóteses obsoletas e custo de reconstrução; testar tarefas que exigem comparação simultânea.

Comparações:
- T063 (complements): Memória virtual move conteúdo entre níveis; a janela de trabalho especifica o conjunto ativo para a etapa.
- T043 (complements): Compactação pode reconstruir a visão, mas não é necessária a cada atualização pequena.

Afirmação rastreável:
MemGPT propõe mover informação entre níveis de memória para utilizar conteúdo além da janela ativa limitada.
Suporte: direct; fontes: A-S009
Limite: A janela de trabalho aqui descrita é uma política arquitetural; não é acesso ao raciocínio interno ou à memória biológica de um modelo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T050:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou vista e persistência. Aqui a memória de trabalho é organizada por hipóteses ativas e custo de alternar tarefas.

Projeto e decomposição
Mantenha quadro com objetivo, hipótese em teste, evidência necessária e próxima decisão. Conteúdo entra por função nessa etapa, não apenas por ter aparecido recentemente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

Controle adaptativo
Ao alternar tarefa, salve o quadro e carregue outro com identificação explícita. Misturar hipóteses de tarefas diferentes pode produzir respostas coerentes com o projeto errado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

Validação contrafactual
Compare janela cronológica e quadro por hipótese. Meça retomada após interrupção, repetição de testes e confusão de entidades entre tarefas, mantendo o mesmo limite de tokens. Unidade de avaliação: etapa de raciocínio operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

USO AVANÇADO — Depuração com interrupções
Cenário: Usuário muda prioridade durante investigação.
Estratégia: Persistir hipótese e teste pendente, suspender trabalho e retomar somente após confirmar que revisão do código continua compatível.
Papel do modelo pequeno: 8–14B administra hipótese local.
Aceite proposto: Não repetir teste concluído nem aplicar resultado a revisão diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

USO AVANÇADO — Leitura analítica
Cenário: Várias questões usam o mesmo corpus.
Estratégia: Manter quadro por questão com evidências específicas; compartilhar apenas fontes, não conclusões provisórias entre quadros.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra.
Aceite proposto: Cada resposta deve usar o quadro e o escopo corretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de uma hipótese ou campo por etapa, com estado estruturado externo.
8–14B: Analista de poucas hipóteses com identificação de evidência faltante.
15–30B: Integrador de hipóteses interdependentes quando alternância simples não basta.
Requisitos de treino/runtime: Quadro serializável, identidade de tarefa e revisão da origem; o modelo não precisa reter todo histórico.
Não aplicar quando: A tarefa depende de contexto implícito que o quadro não representa e não pode recuperar.

## T050:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T050:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T050 → T053 [complements]
Como combinar: Persistir quadro de trabalho entre chamadas.
Interface: task_id, hipótese, teste e referência de evidência.
Condição: Arquivo não misturar tarefas sem namespace.
Aceite proposto: Interromper processo e retomar quadro correto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T050 → T039 [requires]
Como combinar: Fixar evidência da hipótese ativa temporariamente.
Interface: Blocos necessários e condição de liberação.
Condição: Hipótese ainda estiver aberta.
Aceite proposto: Encerrar hipótese e conferir liberação de espaço.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover hipótese ativa automaticamente a memória durável.
- Não usar resumo de tarefa anterior como estado atual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade e precisão ao alternar tarefas; janela organizada não substitui capacidade de resolver a hipótese.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T039, T040, T053

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T051 — Graph-Based Memory

**Nome canônico:** Graph-Based Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T051  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória baseada em grafos

## T051:C01 — conceito

Organiza informação persistida como entidades e relações, permitindo consultar conexões e caminhos. A semântica das arestas deve ser explícita: depende de, pertence a e contradiz não significam a mesma coisa. Um grafo é representação; qualidade depende de identidade, proveniência e atualização.

Como funciona:
- Definir entidades, tipos de relação e escopo.
- Associar cada relação a fonte e estado de verificação.
- Consultar vizinhança ou caminhos relevantes e recuperar evidências.

## T051:C02 — aplicacao

Quando usar:
- Dependências entre softwares, contratos e componentes.
- Memórias em que relações são mais úteis que documentos isolados.

Quando não usar:
- Evitar transformar cada coocorrência de palavras em relação factual.

Implementação proposta:
- Proposta: resolver identidade usando chaves do domínio antes de similaridade.
- Manter relações extraídas separadas das confirmadas.
- Limitar profundidade de expansão e incluir origem de cada aresta no resultado.

Aplicação LAI proposta:
Proposta LAI: mapear serviços, eventos e schemas do ecossistema com versão e fonte; recomendações de mudança devem abrir o contrato original.

## T051:C03 — riscos_validacao

Armadilhas:
- Uma fusão errada de entidades contamina muitos caminhos.
- Caminhos longos podem parecer explicações causais sem evidência causal.

Métricas sugeridas:
- Precisão de nós e relações.
- Recall de caminhos úteis e tempo de atualização.

Testes propostos:
- Criar entidades homônimas e exigir distinção pelo domínio.
- Remover evidência de uma aresta e verificar invalidação de resultados dependentes.

## T051:C04 — perguntas_proveniencia

Pergunta: Grafo de memória exige Neo4j?
Resposta: Não. A representação pode existir em banco relacional, documentos ou bibliotecas de grafo.

Pergunta: Uma conexão no grafo prova causa?
Resposta: Não. Causalidade exige significado da relação e evidência compatível, não apenas um caminho.

Pergunta: Toda aresta precisa apontar a uma fonte?
Resposta: Para uso como evidência, deve ter suporte rastreável ou status explícito de hipótese. Arestas puramente organizacionais também precisam de tipo claro.

Pergunta: Um ciclo no grafo é sempre erro?
Resposta: Não. Relações sociais ou dependências informacionais podem formar ciclos. A validade depende da semântica do tipo de relação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T051:C05 — mecanismo_avancado

Em memória por grafo, duas operações precisam ser separadas: identificar a entidade e decidir se uma nova relação substitui, complementa ou contradiz outra. Um nome parecido não resolve identidade; uma relação mais recente não substitui automaticamente todas as anteriores. A evolução das notas pode atualizar descrições úteis à busca, mas essas descrições derivadas precisam manter vínculos com as evidências que motivaram a mudança.

Condição de contorno:
O grafo perde confiabilidade quando extração probabilística é tratada como fato confirmado ou quando mudanças de ontologia reinterpretam arestas antigas sem migração explícita.

Contrato proposto:
- Entradas: Observações com entidades candidatas, tipos de relação, origem e contexto temporal.
- Saídas: Nós e arestas identificados, com decisões de resolução e registros de derivação.
- Estado: Ontologia versionada, aliases, evidências ligadas e histórico de revisão das relações.
- Invariante: Uma aresta derivada permanece distinguível da observação que a sustenta e de uma relação apenas hipotética.

Compromissos de projeto:
- Grafo explicita conexões úteis a perguntas relacionais e aumenta custo de manutenção de identidade.
- Atualização incremental evita reconstrução completa e exige invalidar caminhos dependentes quando uma relação muda.

## T051:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas organizações homônimas e inserir fatos diferentes em cada uma. A resolução deve manter identidades separadas; uma fusão deliberadamente errada deve ser reversível com seus vínculos de origem.

Plano de avaliação proposto:
Avaliação proposta: comparar grafo e índice de passagens em perguntas relacionais com mesmo orçamento de leitura. Medir precisão de entidades, sustentação das arestas, custo de atualização e caminhos inválidos; não confundir caminho encontrado com explicação comprovada.

Comparações:
- T029 (complements): GraphRAG usa estrutura para recuperação; memória por grafo também exige políticas de escrita e evolução ao longo do tempo.
- T077 (complements): Adicionar validade temporal às relações é uma especialização que permite consultar diferentes estados históricos.

Afirmação rastreável:
A-MEM conecta notas e atualiza suas representações; Graphiti mantém relações temporais ligadas aos episódios de origem.
Suporte: direct; fontes: V3A-S034, A-S035, V3A-S035
Limite: Essas implementações usam organizações distintas; nenhuma transforma ligações extraídas em causalidade identificada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T051:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou identidade e ontologia. Aqui memória em grafo mantém perspectivas por agente e caminhos de evidência sem confundir crença com mundo.

Projeto e decomposição
Separe grafo de fatos observados e grafo de crenças ou hipóteses do agente. Uma relação pode existir como crença sem estar confirmada no domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

Controle adaptativo
Faça consultas exigirem tipo de perspectiva e validade. Agregação de memórias de vários agentes deve preservar quem observou, quem inferiu e quem apenas repetiu a informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

Validação contrafactual
Compare grafo unificado e perspectivas separadas. Meça fusões incorretas, propagação de inferências e respostas que atribuem a um agente conhecimento que ele ainda não possuía. Unidade de avaliação: afirmação em grafo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

USO AVANÇADO — Equipe de agentes
Cenário: Trabalhadores veem subconjuntos distintos.
Estratégia: Registrar observações por origem e compartilhar evidências confirmadas; não fundir hipóteses contraditórias em uma relação única.
Papel do modelo pequeno: 3–7B extrai relações; 15–30B reconcilia.
Aceite proposto: Uma crença individual não pode virar consenso sem suporte adicional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

USO AVANÇADO — Investigação histórica
Cenário: É necessário explicar decisões passadas.
Estratégia: Consultar perspectiva e informações disponíveis ao decisor na época, distinguindo fatos descobertos posteriormente.
Papel do modelo pequeno: 8–14B lê subgrafo restrito.
Aceite proposto: Resposta deve evitar conhecimento retrospectivo na explicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S034, V4A-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de relações em vocabulário fechado e origem explícita.
8–14B: Leitor de subgrafo pequeno com perspectiva fixada.
15–30B: Reconciliador de perspectivas e contradições entre agentes.
Requisitos de treino/runtime: Entidades estáveis, campos de perspectiva e proveniência por aresta; expansão deve respeitar escopo.
Não aplicar quando: O sistema não consegue distinguir observação, inferência e repetição de outra fonte.

## T051:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C013 — Google / Knowledge Graph na busca Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Anúncio relata início da implantação a usuários da busca.
Mecanismo documentado: Entidades e relações permitem desambiguação e apresentação de fatos relacionados.
Correspondência com esta base: Grafo de conhecimento operacional; memória de agente não demonstrada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.
Limite: Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S018.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: TAO pertence à família de armazenamento em grafo, sem provar memória de agente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Grafo de evidência não implica memória episódica completa.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q021, V4A-Q023.

## T051:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T051 → T056 [requires]
Como combinar: Restringir conhecimento por perspectiva temporal.
Interface: valid_time, recorded_time e observador.
Condição: Consulta declarar o instante de conhecimento.
Aceite proposto: Inserir descoberta tardia e impedir vazamento retrospectivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S034, V4A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T051 → T075 [complements]
Como combinar: Reconciliar relações concorrentes sem apagar origem.
Interface: Arestas conflitantes, versões e fontes.
Condição: Critério de reconciliação ser explícito.
Aceite proposto: Preservar conflito quando evidência não decidir.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S034, V4A-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não deduzir causalidade de caminho no grafo.
- Não contar agentes que repetem uma origem como fontes independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar atribuição correta de conhecimento e relações; densidade do grafo pode amplificar erro de extração.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T029, T057, T077

## Fontes primárias associadas

### A-S035 — Graphiti: Build Real-Time Knowledge Graphs for AI Agents

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grafo temporal de entidades, relações e episódios com rastreabilidade.

Limite: README consultado; sem auditoria de código, teste de escala ou confirmação de promessas comerciais.

### V3A-S034 — A-MEM: Agentic Memory for LLM Agents

[https://arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Notas estruturadas, conexão entre memórias e evolução das representações de notas anteriores.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S035 — Zep: A Temporal Knowledge Graph Architecture for Agent Memory

[https://arxiv.org/abs/2501.13956](https://arxiv.org/abs/2501.13956)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura temporal Graphiti para integração de conversas e dados estruturados com relações históricas.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S018 — Introducing the Knowledge Graph: things, not strings

[https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação gradual de entidades e relações na busca Google; não é GraphRAG moderno.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T052 — Latent Context

**Nome canônico:** Latent Context  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T052  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** contexto latente

## T052:C01 — conceito

Rótulo amplo para informação representada em vetores ou estados internos em vez de texto comum. Pode referir-se a tokens latentes, embeddings ou estados de memória especializados. É necessário especificar qual representação e qual consumidor foram treinados para utilizá-la.

Como funciona:
- Codificar informação em uma representação compatível.
- Armazenar ou transportar essa representação com sua versão.
- Decodificar ou condicioná-la no modelo apropriado.

Nota de nomenclatura: Termo ambíguo; cada uso precisa declarar representação, treinamento e interface. Não há um único recurso chamado Latent Context.

## T052:C02 — aplicacao

Quando usar:
- Pesquisa de compressão e memória em arquiteturas adaptadas.
- Reutilização de representações quando produtor e consumidor são controlados.

Quando não usar:
- Não tratar um embedding de busca como cópia perfeita do documento nem como prompt diretamente interpretável por qualquer LLM.

Implementação proposta:
- Proposta: registrar modelo codificador, dimensão, tokenizer e esquema de integração.
- Conservar conteúdo original para auditoria e reconstrução.
- Medir tarefas de detalhe exato além de similaridade semântica.

Aplicação LAI proposta:
Proposta LAI: priorizar texto e referências auditáveis para memória operacional; contexto latente seria um experimento de arquitetura, não funcionalidade presumida do servidor atual.

## T052:C03 — riscos_validacao

Armadilhas:
- Representações podem ficar inválidas após mudança de modelo.
- Compressão latente pode perder números e relações difíceis de inspecionar.

Métricas sugeridas:
- Retenção de informação por tipo de pergunta.
- Custo de codificação, memória e incompatibilidades entre versões.

Testes propostos:
- Trocar o consumidor e exigir checagem explícita de compatibilidade.
- Perguntar por um identificador exato ausente da reconstrução e registrar falha, sem inventá-lo.

## T052:C04 — perguntas_proveniencia

Pergunta: Um vetor consegue armazenar todo o histórico sem perda?
Resposta: Não há essa garantia. Representações compactas preservam informação conforme o treinamento e têm limites.

Pergunta: Embedding e memória latente são a mesma coisa?
Resposta: Embedding é um tipo de representação; memória latente pode envolver outras estruturas e interfaces especializadas.

Pergunta: Posso enviar esses slots para qualquer API de chat?
Resposta: Não sem uma interface documentada que aceite e interprete a representação. Um endpoint de texto comum não oferece isso implicitamente.

Pergunta: Como auditar uma resposta baseada em slots?
Resposta: Mantenha as fontes e versões acessíveis, avalie a resposta contra elas e registre o caminho de codificação. O vetor isolado não fornece uma citação legível.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T052:C05 — mecanismo_avancado

Latent Context precisa ser qualificado pela operação que o consumidor consegue realizar. Um embedding de busca localiza texto; slots de memória aprendidos condicionam um decodificador treinado; estados de atenção pertencem a uma arquitetura e a uma posição de inferência. Vetores com a mesma dimensão podem ter semânticas incompatíveis. A especificação deve descrever essa interface, não apenas anunciar quantidade de tokens comprimidos.

Condição de contorno:
Sem treinamento ou integração compatível, transmitir um vetor não fornece ao modelo textual capacidade de interpretar seu conteúdo como memória.

Contrato proposto:
- Entradas: Representação original, codificador identificado e contrato do consumidor que aceitará os estados.
- Saídas: Slots ou vetores com metadados de forma, revisão e reconstrução ou leitura prevista.
- Estado: Pesos do codificador e consumidor, tokenizer, parâmetros de compressão e origem do conteúdo.
- Invariante: Compatibilidade dimensional nunca é usada como prova suficiente de compatibilidade semântica entre modelos.

Compromissos de projeto:
- Representação latente pode reduzir sequências ativas e dificulta inspeção, edição pontual e citação.
- Treinar um consumidor especializado melhora a interface e cria custo de adaptação quando o modelo muda.

## T052:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o consumidor por outro de mesma dimensão sem adaptar os pesos. A avaliação deve detectar perda de interpretação, mesmo quando a transmissão aceita o formato.

Plano de avaliação proposto:
Avaliação proposta: comparar texto, compressão extrativa e slots aprendidos com tarefas equivalentes. Medir preservação de detalhes, custo de codificação, memória computacional e transferência entre domínios; separar tamanho serializado de capacidade efetiva de leitura.

Comparações:
- T006 (complements): Representações latentes podem implementar compressão, mas nem todo vetor constitui uma versão comprimida consumível pelo gerador.
- R003 (complements): LongMem usa uma interface neural de memória específica, distinta de armazenar embeddings para busca textual.

Afirmação rastreável:
ICAE aprende slots de memória por treinamento e adaptação para comprimir contexto e utilizá-lo em tarefas posteriores.
Suporte: direct; fontes: V3A-S004
Limite: Latent Context é um rótulo abrangente; ICAE sustenta uma implementação específica, não um formato universal interoperável.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T052:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu sentidos de contexto latente. Aqui cada representação é avaliada por intervenções e compatibilidade com o consumidor.

Projeto e decomposição
Declare qual objeto está sendo usado: vetor de busca, tokens latentes treinados ou estados de atenção. O mesmo nome editorial não torna essas interfaces substituíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S004, V3A-S047, A-S012.

Controle adaptativo
Teste dependência causal funcional removendo, trocando e perturbando a representação enquanto mantém texto constante. Se a saída não muda onde deveria, o consumidor pode ignorar a memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S004, V3A-S047, A-S012.

Validação contrafactual
Compare texto equivalente, representação latente e memória trocada entre exemplos. Meça resposta correta, sensibilidade a troca e compatibilidade após quantização; proximidade entre estados não basta como sucesso. Unidade de avaliação: representação e consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S004, V3A-S047, A-S012.

USO AVANÇADO — Compressão neural de documentos
Cenário: Modelo aberto recebe slots aprendidos.
Estratégia: Treinar encoder e consumidor compatíveis, comparar com extração textual e registrar quando a representação não preserva campos raros.
Papel do modelo pequeno: 15–30B consumidor experimental.
Aceite proposto: Troca controlada de memória deve alterar somente fatos correspondentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S004, V3A-S047, A-S012.

USO AVANÇADO — Busca vetorial local
Cenário: Embeddings localizam memórias textuais.
Estratégia: Usar vetor apenas para escolher evidências; devolver texto original ao leitor e medir recuperação separadamente da geração.
Papel do modelo pequeno: 3–7B lê trechos; embedding pode ser menor.
Aceite proposto: Nenhum fato pode ser inferido diretamente do número do vetor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S004, V3A-S047, A-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor textual após busca vetorial, sem supor leitura direta de embeddings.
8–14B: Consumidor treinado de representação específica quando houver dados e interface estável.
15–30B: Modelo aberto instrumentado para experimentos de memória neural e adapters.
Requisitos de treino/runtime: Identidade do encoder, camada, dimensão, normalização e consumidor; acesso a treino para formas neurais.
Não aplicar quando: Representações vêm de arquitetura incompatível ou não há modo de verificar seu efeito na resposta.

## T052:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo e código estudam memória neural recuperável para contexto extenso.
Mecanismo documentado: Representações em memória e módulo adaptado de leitura são componentes treinados.
Correspondência com esta base: Memória latente como um sentido delimitado do rótulo.
Transferência proposta para modelo pequeno: Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.
Limite: Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S013, V3A-S047.

V4A-C033 — Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan, Zhou Xiao / SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda adaptação de contexto por alinhamento de estados.
Mecanismo documentado: Distilação aproxima estados em interface de blocos de atenção usando adapters.
Correspondência com esta base: Estados neurais são representação latente, com compatibilidade arquitetural.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar modelo aberto em faixa permitida com instrumentação de estados e teste funcional separado.
Limite: Nenhuma produção bigtech exata estabelecida; alinhamento interno não garante resposta correta. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q018, V4A-Q023, V4A-Q024.

## T052:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T052 → T068 [complements]
Como combinar: Conectar representação ao mecanismo de leitura correspondente.
Interface: Tensor, máscara, versão e semântica da interface.
Condição: Consumidor treinado para esse formato.
Aceite proposto: Trocar tensor por outro exemplo e medir mudança factual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S004, V3A-S047, A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T052 → T020 [complements]
Como combinar: Aprender representação para tarefa e consumidor fixados.
Interface: Corpus, objetivo e checkpoint dos dois lados.
Condição: Avaliação separar treino e fontes.
Aceite proposto: Comparar com texto sob mesmo orçamento de memória.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S004, V3A-S047, A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar embedding de memória comprimida universal.
- Não transportar métricas de SADA ou ICAE para implementação distinta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefa e interface específicas; alinhamento interno não demonstra equivalência geral ao modelo professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T020, T068, R003

## Fontes primárias associadas

### A-S033 — Learning to Compress Prompts with Gist Tokens

[https://arxiv.org/abs/2304.08467](https://arxiv.org/abs/2304.08467)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações compactas de prompt treinadas com alterações de máscara de atenção.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S013 — Augmenting Language Models with Long-Term Memory

[https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: LongMem: backbone congelado como codificador e rede lateral treinada para recuperação e leitura.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S047 — LongMem External_Memory implementation

[https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco de chaves e valores por cabeça, indexação da média das chaves em chunks e recuperação dos estados dos chunks selecionados.

Limite: Leitura do código na branch main, sem execução. Detalhes representam esta implementação de pesquisa e não garantem compatibilidade com qualquer modelo ou ambiente.

### A-S012 — SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters

[https://aclanthology.org/2026.acl-long.1046/](https://aclanthology.org/2026.acl-long.1046/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapeamento contexto-parâmetros e alinhamento de estados para adaptadores.

Limite: Leitura do resumo e metadados; código não auditado e resultados não reproduzidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T053 — Scratchpad em arquivo

**Nome canônico:** Scratchpad em Arquivo  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T053  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** scratchpad persistente; notas operacionais externas; Scratchpad em Arquivo

## T053:C01 — conceito

Externaliza estado operacional explícito da missão em arquivos: objetivo, plano, decisões, hipóteses, resultados e referências. A próxima chamada carrega somente o necessário. Não equivale a extrair integralmente o raciocínio interno oculto da LLM; registra informações úteis e verificáveis para continuidade.

Como funciona:
- Escrever estado e notas após etapas relevantes.
- Persistir com versão e indicação de conclusão da gravação.
- Reler estado compacto e abrir detalhes por referência.

## T053:C02 — aplicacao

Quando usar:
- Missões longas, auditorias e desenvolvimento com interrupções.
- Agentes que precisam separar contexto ativo de acervo operacional.

Quando não usar:
- Não usar um único arquivo editável como prova exclusiva de que uma ação ocorreu.

Implementação proposta:
- Proposta: separar estado atual, decisões, hipóteses e evidências.
- Gravar arquivo temporário e promover por operação atômica quando suportada.
- Usar controle de versão ou compare-and-swap para evitar sobrescritas concorrentes.

Aplicação LAI proposta:
Proposta LAI: tornar o estado da Helena explícito e recuperável, mantendo logs e resultados de ferramentas como evidência independente das notas.

## T053:C03 — riscos_validacao

Armadilhas:
- O agente pode dizer que salvou sem a gravação ter sido confirmada.
- Dois processos podem sobrescrever o mesmo estado.

Métricas sugeridas:
- Taxa de retomada fiel e perda de estado.
- Quantidade de leituras necessárias por etapa.

Testes propostos:
- Interromper após gravação e reconstruir próxima ação em novo processo.
- Simular dois escritores e exigir detecção de conflito.

## T053:C04 — perguntas_proveniencia

Pergunta: O arquivo deve conter todo o raciocínio do modelo?
Resposta: Não. Deve guardar decisões, justificativas concisas, evidências e estado operacional necessário.

Pergunta: Guardar uma referência economiza contexto sempre?
Resposta: Somente se a recuperação seletiva custar menos que reenviar o material e mantiver a qualidade necessária.

Pergunta: O arquivo precisa conter raciocínio interno completo?
Resposta: Não. Registre decisões, motivos verificáveis, resultados, pendências e referências necessários à continuidade, sem alegar extrair estados internos ocultos.

Pergunta: Como saber qual nota prevalece?
Resposta: Use revisão publicada e regras de autoridade. Data de modificação do filesystem pode refletir cópia ou sincronização, e não a ordem lógica das decisões.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T053:C05 — mecanismo_avancado

Um scratchpad em arquivo funciona como protocolo entre execuções: alguém escreve um estado explícito e outro processo o interpreta posteriormente. O contrato precisa distinguir alteração no buffer, gravação no disco, revisão publicada e cópia sincronizada. Um arquivo legível pode estar incompleto ou ser de uma execução antiga. Por isso, identidade da missão, revisão e marcador de conclusão têm utilidade operacional além do formato Markdown.

Condição de contorno:
Arquivos deixam de ser uma solução simples quando muitos escritores precisam alterar simultaneamente o mesmo estado sem coordenação ou quando não existe armazenamento persistente.

Contrato proposto:
- Entradas: Estado explícito da tarefa, referências verificáveis e revisão que o escritor pretende substituir.
- Saídas: Arquivo completo publicado com identidade, versão e confirmação de gravação observada.
- Estado: Revisão anterior, alterações pendentes, posição de sincronização e conflitos não resolvidos.
- Invariante: Um leitor usa apenas revisões completas e não interpreta nota de intenção como confirmação de execução.

Compromissos de projeto:
- Arquivos são inspecionáveis e interoperáveis, mas não oferecem transações entre recursos por padrão.
- Versionamento facilita revisão e recuperação; sincronização remota adiciona estados intermediários e conflitos.

## T053:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper uma escrita no meio e reiniciar o leitor em outro processo. Ele deve recuperar a última revisão válida ou detectar incompletude, sem usar a metade nova como estado definitivo.

Plano de avaliação proposto:
Avaliação proposta: comparar notas livres e protocolo com campos mínimos em retomadas interrompidas. Medir estado reconstruído, perdas de correções, conflitos de escritor e latência de publicação; incluir gravação local confirmada com sincronização remota falha.

Comparações:
- T064 (complements): O arquivo pode representar parte do estado persistente, desde que tenha identidade e semântica de retomada.
- T076 (complements): Git acrescenta histórico de versões; não transforma automaticamente cada arquivo em estado transacional do agente.

Afirmação rastreável:
MemFS distingue edições locais de memória comprometida e sincronizada por Git entre computadores.
Suporte: direct; fontes: A-S010
Limite: É um exemplo de implementação; um scratchpad comum não herda automaticamente commit, push ou resolução de conflitos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T053:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou estados de persistência. Aqui scratchpad vira um documento de trabalho com seções de autoridade e leitura econômica.

Projeto e decomposição
Separe fatos observados, hipóteses, decisões e tarefas em seções identificadas. Atualizações do modelo não devem transformar hipótese em decisão apenas por mover uma linha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

Controle adaptativo
Use índice curto no início e detalhes referenciados por seção. O consumidor pequeno lê primeiro estado e pendências, abrindo justificativas somente quando a ação depender delas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

Validação contrafactual
Compare arquivo narrativo e seções tipadas. Meça erros de retomada, repetição de trabalho e alterações concorrentes em seções diferentes; verificar também crescimento do arquivo. Unidade de avaliação: revisão de arquivo de trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

USO AVANÇADO — Projeto longo de código
Cenário: Estado precisa sobreviver à sessão.
Estratégia: Registrar revisão do código, teste executado e próximo teste; manter resultado de execução distinto de intenção de executar.
Papel do modelo pequeno: 3–7B atualiza campos; 8–14B retoma.
Aceite proposto: Nenhum teste planejado pode aparecer como aprovado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

USO AVANÇADO — Pesquisa colaborativa
Cenário: Agentes acrescentam descobertas.
Estratégia: Cada agente escreve proposta com fonte e área de responsabilidade; integrador confirma decisões e resolve conflito entre seções.
Papel do modelo pequeno: 15–30B integra evidências.
Aceite proposto: Alteração deve preservar autoria e evidência de cada afirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atualizador de campos curtos com operações restritas por seção.
8–14B: Leitor de estado e justificativas locais para retomar tarefa.
15–30B: Integrador de contribuições com conflitos e dependências cruzadas.
Requisitos de treino/runtime: Formato de seções, revisão-base e escrita atômica; arquivo continua artefato externo, não treino de pesos.
Não aplicar quando: Scratchpad é a única cópia de evidências extensas ou cresce sem índice e política de manutenção.

## T053:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Notas externas são família relacionada; não demonstra todos os contratos desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q026.

## T053:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T053 → T076 [complements]
Como combinar: Versionar alterações de seções e decisões.
Interface: Arquivo, diff, revisão-base e autoria.
Condição: Conflitos semânticos revisados após merge textual.
Aceite proposto: Introduzir duas decisões incompatíveis em seções distintas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T053 → T044 [complements]
Como combinar: Ler justificativas sob demanda.
Interface: Índice, section_id e requisito da tarefa.
Condição: Seção manter referência ao conteúdo completo.
Aceite proposto: Retomar com índice apenas e abrir suporte necessário.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não salvar segredos incidentais em notas reutilizáveis.
- Não confundir presença no arquivo com confirmação externa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retomada em sessão limpa; modelos pequenos precisam de campos mais explícitos que narrativa livre.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T050, T060, T064

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T054 — Semantic Memory

**Nome canônico:** Semantic Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T054  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória semântica

## T054:C01 — conceito

Armazena fatos e conceitos organizados para uso além de um episódio específico, como definições, relações e decisões vigentes. Memória semântica não significa obrigatoriamente busca por embeddings. Uma afirmação precisa manter origem, validade e estado de verificação.

Como funciona:
- Extrair uma afirmação de evidências identificadas.
- Representá-la com entidades, escopo e validade.
- Recuperar ou corrigir a afirmação conforme a tarefa.

## T054:C02 — aplicacao

Quando usar:
- Conhecimento técnico estável e convenções de um projeto.
- Fatos reutilizáveis entre diferentes missões.

Quando não usar:
- Não transformar uma inferência do agente em fato confirmado sem evidência adicional.

Implementação proposta:
- Proposta: armazenar afirmação, sujeito, fonte e intervalo de validade.
- Distinguir observada, inferida e contestada.
- Quando houver conflito, preservar as versões e resolver pela autoridade e pelo tempo aplicáveis.

Aplicação LAI proposta:
Proposta LAI: manter definições e contratos vigentes separados dos episódios de auditoria; uma ficha técnica deve apontar ao documento ou código de origem.

## T054:C03 — riscos_validacao

Armadilhas:
- Resumos podem retirar condições e generalizar demais.
- Fatos de versões diferentes podem ser misturados.

Métricas sugeridas:
- Precisão factual e proporção com fonte acessível.
- Taxa de respostas usando fatos obsoletos.

Testes propostos:
- Consultar uma definição e recuperar a fonte que a sustenta.
- Corrigir um fato e verificar que a versão antiga deixa de ser apresentada como atual.

## T054:C04 — perguntas_proveniencia

Pergunta: Semântica quer dizer vetor?
Resposta: Não. Refere-se ao tipo de conhecimento armazenado; SQL, grafos e arquivos também podem representá-lo.

Pergunta: Posso apagar versões antigas de um fato?
Resposta: Depende da política de retenção; para auditoria e consultas históricas, preservar versões costuma ser necessário.

Pergunta: Duas frases parecidas devem ser fundidas?
Resposta: Somente se sujeito, relação, qualificadores e validade forem compatíveis. Similaridade pode aproximar afirmações opostas ou referentes a versões distintas.

Pergunta: Uma afirmação com muitas fontes é mais confiável?
Resposta: Depende da independência e qualidade das fontes. Dez republicações da mesma origem não equivalem a dez observações independentes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T054:C05 — mecanismo_avancado

Uma memória semântica útil separa a proposição de suas evidências e qualificadores. “O componente aceita o formato” pode depender de versão, configuração e ambiente; retirar esses campos transforma uma afirmação local em regra geral. Também é necessário separar identidade lógica da proposição e identidade de uma versão, permitindo associar novas evidências sem reescrever silenciosamente o histórico de como o conhecimento mudou.

Condição de contorno:
Generalizações a partir de poucos episódios falham quando as condições determinantes não foram registradas; maior repetição textual não corrige falta de escopo.

Contrato proposto:
- Entradas: Afirmações candidatas, entidades, qualificadores e evidências identificadas com suas revisões.
- Saídas: Proposições consultáveis com escopo, status e relações de derivação ou contestação.
- Estado: Histórico de versões, evidências independentes e regras para revisão ou invalidação.
- Invariante: Uma afirmação não perde condições necessárias ao ser transformada em memória reutilizável.

Compromissos de projeto:
- Normalizar proposições melhora comparação e atualização, mas exige decisões de equivalência semântica.
- Guardar múltiplos suportes aumenta robustez e requer distinguir cópias de observações independentes.

## T054:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: extrair a mesma frase de duas versões de manual com compatibilidades diferentes. O sistema deve conservar os qualificadores e impedir que a busca retorne uma regra universal inexistente.

Plano de avaliação proposto:
Avaliação proposta: comparar passagens originais e proposições estruturadas em perguntas de escopo e exceção. Medir precisão de qualificadores, sustentação, atualização após correção e independência das evidências; testar consulta exata e busca semântica separadamente.

Comparações:
- T049 (distinct_from): Episódio conserva uma experiência situada; memória semântica abstrai uma proposição sem eliminar seu escopo.
- T058 (complements): Consolidação pode produzir proposições candidatas, que ainda precisam de verificação e controle de versões.

Afirmação rastreável:
PROV-DM representa entidades, atividades e relações de derivação que permitem rastrear a origem de um registro produzido.
Suporte: related; fontes: V3A-S037
Limite: Proveniência descreve produção e responsabilidade; não certifica a verdade da proposição nem define sozinha sua equivalência semântica.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T054:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu qualificação e fonte. Aqui memória semântica organiza regras de aplicabilidade e revisões motivadas por contraexemplos.

Projeto e decomposição
Guarde proposição com predicados de aplicabilidade, não somente uma frase geral. Uma convenção pode valer para um projeto, idioma ou versão específica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S018, V3A-S037.

Controle adaptativo
Quando aparecer contraexemplo, primeiro verificar se ele invalida o fato ou apenas restringe seu escopo. Atualização deve poder dividir uma regra em casos, preservando a origem da mudança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S018, V3A-S037.

Validação contrafactual
Compare fatos planos e fatos condicionados. Meça aplicação fora de escopo, exceções ignoradas e custo de resolver ambiguidade; respostas fluentes não indicam memória correta. Unidade de avaliação: proposição reutilizável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S018, V3A-S037.

USO AVANÇADO — Convenções de engenharia
Cenário: Projetos usam padrões diferentes.
Estratégia: Registrar convenção por projeto e versão, recuperar junto ao contexto atual e rejeitar transferência automática para repositório novo.
Papel do modelo pequeno: 3–7B escolhe regra elegível.
Aceite proposto: Não aplicar convenção local como regra universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S018, V3A-S037.

USO AVANÇADO — Conhecimento de produto
Cenário: Propriedades mudam entre versões.
Estratégia: Representar propriedade por intervalo e variante; manter explicação de supersessão para perguntas históricas.
Papel do modelo pequeno: 8–14B compara versões.
Aceite proposto: Resposta deve indicar quando o fato vale e origem da informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S017, V4A-S018, V3A-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de proposições curtas com filtros de aplicabilidade.
8–14B: Resolvedor de exceções entre poucas regras condicionais.
15–30B: Integrador de conjuntos de regras com escopos sobrepostos.
Requisitos de treino/runtime: Schema de sujeito, relação, valor, escopo e fonte; extrações do modelo entram como candidatas.
Não aplicar quando: O sistema não consegue preservar qualificadores ou verificar fonte de proposição consolidada.

## T054:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C013 — Google / Knowledge Graph na busca Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Anúncio relata início da implantação a usuários da busca.
Mecanismo documentado: Entidades e relações permitem desambiguação e apresentação de fatos relacionados.
Correspondência com esta base: Fatos estruturados se aproximam de memória semântica externa.
Transferência proposta para modelo pequeno: Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.
Limite: Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S018.

V4A-C018 — OpenAI / ChatGPT Memory
Evidência: produto/recurso disponível; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Produto documenta memórias salvas e uso de histórico para personalização.
Mecanismo documentado: Informações selecionadas podem atravessar conversas com controles próprios.
Correspondência com esta base: Preferências são informação semântica, sem revelar formato interno.
Transferência proposta para modelo pequeno: Proposta de engenharia: Criar memória externa pequena de preferências explícitas e testar correções e escopo.
Limite: Comportamento varia por conta; fonte não revela algoritmo nem prova precisão permanente. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S017.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Reflexões são abstrações, não fatos automaticamente validados.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q013, V4A-Q015, V4A-Q022.

## T054:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T054 → T056 [complements]
Como combinar: Representar validade histórica das proposições.
Interface: Fato, intervalo de validade e momento de registro.
Condição: Domínio exigir distinção temporal.
Aceite proposto: Consultar antes e depois de correção retroativa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S017, V4A-S018, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T054 → T071 [requires]
Como combinar: Promover afirmação somente após validar suporte e escopo.
Interface: Candidato, fonte e regra de admissão.
Condição: Fonte sustentar a proposição integral.
Aceite proposto: Remover qualificador e exigir rejeição da promoção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S017, V4A-S018, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar quantidade de repetições como prova independente.
- Não interpretar exceção como revogação total sem evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar aplicação correta de fatos condicionados; memória semântica extensa pode aumentar erros fora de escopo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T055, T056, T075

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S018 — Introducing the Knowledge Graph: things, not strings

[https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação gradual de entidades e relações na busca Google; não é GraphRAG moderno.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T055 — Procedural Memory

**Nome canônico:** Procedural Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T055  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória procedural; memória de procedimentos

## T055:C01 — conceito

Armazena como executar atividades: sequências, condições, ferramentas, critérios de conclusão e estratégias. Pode ser representada por workflows ou skills recuperáveis. Não é apenas uma descrição conceitual; precisa de passos aplicáveis e condições nas quais o procedimento foi validado.

Como funciona:
- Identificar um procedimento a partir de especificação ou experiências.
- Definir pré-condições, ações e verificações.
- Recuperar a versão adequada e avaliar o resultado de sua aplicação.

## T055:C02 — aplicacao

Quando usar:
- Tarefas recorrentes de diagnóstico, extração ou validação.
- Padronização do trabalho entre agentes e modelos.

Quando não usar:
- Não promover uma sequência que funcionou uma vez a procedimento universal.

Implementação proposta:
- Proposta: associar skill a versão de ferramenta e ambiente.
- Incluir tratamento de falha, efeitos e critérios de parada.
- Manter exemplos de uso correto e situações em que o procedimento não se aplica.

Aplicação LAI proposta:
Proposta LAI: transformar correções comprovadas da Helena em skills com contrato e avaliação; conhecimento textual sozinho não prova execução competente.

## T055:C03 — riscos_validacao

Armadilhas:
- Procedimento pode envelhecer quando uma API muda.
- Um agente pode seguir etapas mecanicamente apesar de pré-condições falsas.

Métricas sugeridas:
- Conclusão correta por procedimento e versão.
- Falhas de pré-condição detectadas antes da execução.

Testes propostos:
- Executar em cenário compatível e em cenário incompatível conhecido.
- Alterar schema da ferramenta e exigir bloqueio ou migração do procedimento.

## T055:C04 — perguntas_proveniencia

Pergunta: Uma skill é aprendizado nos pesos?
Resposta: Não necessariamente. Ela pode ser memória procedural externa carregada sob demanda.

Pergunta: Procedimentos precisam explicar por quê?
Resposta: Uma justificativa curta e limites de aplicação ajudam a reconhecer quando adaptar ou interromper os passos.

Pergunta: Um procedimento deve incluir rollback?
Resposta: Quando aplicável, descreva compensação e limites. Nem todo efeito pode ser revertido, e executar uma compensação também exige verificar o estado externo.

Pergunta: Como aprender com um único sucesso?
Resposta: Registre uma receita candidata com escopo estreito. Amplie sua recomendação somente depois de testar variações e situações em que não deve ser usada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T055:C05 — mecanismo_avancado

Memória procedural pode armazenar receita, política de decisão ou código executável; essas representações exigem controles diferentes. Uma sequência textual ensina o agente a escolher ações, enquanto um workflow implementado restringe transições. Promover uma experiência a procedimento exige identificar quais pré-condições causaram seu sucesso e quais passos foram apenas circunstanciais. Compatibilidade deve ser verificada no momento de uso, não apenas na data de publicação.

Condição de contorno:
Um procedimento perde aplicabilidade quando depende de permissão, versão ou estado externo diferente daquele em que foi validado, mesmo que seu objetivo permaneça igual.

Contrato proposto:
- Entradas: Objetivo, pré-condições, ferramentas compatíveis, passos e evidências de validação do procedimento.
- Saídas: Versão selecionada com critérios de sucesso, pontos de decisão e tratamento de falhas.
- Estado: Histórico de revisão, dependências e registros de execução sob condições conhecidas.
- Invariante: Selecionar uma receita não autoriza efeitos externos nem prova que suas pré-condições estão satisfeitas.

Compromissos de projeto:
- Receitas flexíveis transferem conhecimento e deixam decisões ao modelo.
- Workflows explícitos facilitam validação e exigem manutenção quando mudam ferramentas, contratos ou condições de operação.

## T055:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o schema de uma ferramenta mantendo o nome. A seleção deve detectar a dependência incompatível e exigir adaptação validada, sem continuar reproduzindo argumentos antigos.

Plano de avaliação proposto:
Avaliação proposta: comparar orientação livre, procedimento textual e workflow em tarefas equivalentes. Medir cumprimento das pré-condições, conclusão verificável, falhas recuperadas e custo de adaptação; separar sucesso por execução correta de sucesso por acaso.

Comparações:
- T046 (complements): Demonstrações mostram casos; procedimentos explicitam condições e sequência reutilizável que os casos podem ilustrar.
- T071 (complements): Promoção decide quando um aprendizado candidato pode tornar-se procedimento recomendado.

Afirmação rastreável:
A especificação Agent Skills organiza instruções e recursos que podem ser carregados progressivamente para tarefas especializadas.
Suporte: related; fontes: V3A-S018
Limite: Esse formato fornece embalagem e descoberta; não garante execução correta, autorização ou validade permanente do procedimento.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T055:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu receita e workflow. Aqui procedimentos são recuperados por pré-condição e adaptados somente em pontos explicitamente variáveis.

Projeto e decomposição
Divida procedimento em invariantes e parâmetros. Caminhos, versões e limites podem variar; uma verificação obrigatória não deve desaparecer durante adaptação para outro projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

Controle adaptativo
Antes de executar, comparar ambiente observado com pré-condições. Quando incompatível, registrar necessidade de adaptação e testar em contexto limitado, evitando improvisar uma nova receita sob o mesmo nome.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

Validação contrafactual
Compare seleção por título e por pré-condições. Meça procedimento inadequado escolhido, adaptações indevidas e conclusão verificada; instrução lida não equivale a execução bem-sucedida. Unidade de avaliação: procedimento em contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

USO AVANÇADO — Rotina de manutenção
Cenário: Mesma tarefa ocorre em versões distintas.
Estratégia: Recuperar procedimento compatível, preencher parâmetros com dados observados e testar passo reversível antes de continuar.
Papel do modelo pequeno: 3–7B preenche parâmetros; 8–14B verifica.
Aceite proposto: Nenhuma etapa pode usar parâmetro inventado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

USO AVANÇADO — Aprendizado de nova rotina
Cenário: Um incidente gerou solução candidata.
Estratégia: Extrair pré-condições e falhas conhecidas, repetir em caso controlado e promover somente após evidência de transferência.
Papel do modelo pequeno: 15–30B analisa adaptação.
Aceite proposto: Não generalizar solução de um caso para todos os ambientes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de procedimento curto com parâmetros e verificações explícitas.
8–14B: Avaliador de compatibilidade do ambiente e exceções locais.
15–30B: Adaptador de rotina com mudanças justificadas e validação independente.
Requisitos de treino/runtime: Procedimento versionado, precondições verificáveis e registro do que foi executado; ajuste de pesos é opcional.
Não aplicar quando: Ambiente não satisfaz pré-condições ou faltam ferramentas necessárias ao teste de aceite.

## T055:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T055:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T055 → T045 [requires]
Como combinar: Carregar ferramentas compatíveis com a rotina.
Interface: Capacidades, schemas e versões exigidas.
Condição: Ferramentas disponíveis no ambiente atual.
Aceite proposto: Substituir ferramenta por versão incompatível e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V2A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T055 → T195 [complements]
Como combinar: Verificar resultado por execução observável.
Interface: Passo, saída esperada e resultado real.
Condição: Teste medir propriedade relevante.
Aceite proposto: Detectar rotina que termina sem produzir artefato correto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V2A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir memória de procedimento com autorização para efeitos.
- Não ocultar adaptação sob identidade da versão original.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar execução fiel em ambientes novos; decorar passos não demonstra capacidade de adaptação geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T071, T204

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V2A-S016 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções persistentes em arquivos e memória automática; escopo e carregamento dependem da configuração.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T056 — Bitemporal Memory

**Nome canônico:** Bitemporal Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T056  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória bitemporal; valid time e system time

## T056:C01 — conceito

Registra dois eixos: quando um fato vale no domínio e quando o sistema o conheceu ou registrou. Permite responder tanto o que hoje sabemos sobre o passado quanto o que acreditávamos naquele momento. Bitemporalidade é independente do número de camadas de memória.

Como funciona:
- Armazenar intervalo de validade e intervalo de registro.
- Inserir correções sem apagar a história de conhecimento.
- Consultar com os dois tempos declarados.

## T056:C02 — aplicacao

Quando usar:
- Dados atrasados, correções retroativas e auditoria.
- Avaliação histórica que não pode usar informação conhecida somente depois.

Quando não usar:
- Não confundir data de ingestão com data em que o fato passou a valer.

Implementação proposta:
- Proposta: usar intervalos consistentes, preferencialmente semiabertos, e timezone explícito.
- Distinguir tempo do evento, validade de negócio e registro quando não coincidem.
- Na recuperação, aplicar filtros temporais antes de apresentar os fatos à LLM.

Aplicação LAI proposta:
Proposta LAI: avaliar decisões antigas da Helena usando somente dados disponíveis na data da decisão; manter correções posteriores em uma visão distinta.

## T056:C03 — riscos_validacao

Armadilhas:
- Misturar os eixos introduz vazamento de futuro em backtests.
- Correções podem criar sobreposições de validade sem resolução clara.

Métricas sugeridas:
- Correção de consultas as-of nos dois eixos.
- Quantidade de conflitos de intervalo e registros sem tempo confiável.

Testes propostos:
- Registrar hoje um fato válido desde ontem e comparar duas consultas históricas.
- Executar replay com corte de conhecimento e impedir uso da correção futura.

## T056:C04 — perguntas_proveniencia

Pergunta: Dois timestamps tornam qualquer memória bitemporal?
Resposta: Não. Os tempos precisam representar e suportar consultas de validade e conhecimento, com semântica definida.

Pergunta: Bitemporal significa cinco camadas?
Resposta: Não. Camadas organizam tipos de memória; bitemporalidade descreve eixos temporais dos registros.

Pergunta: Tempo do evento é sempre valid-time?
Resposta: Não. O evento pode informar uma alteração que só valerá depois, ou corrigir uma validade passada. A semântica vem do domínio.

Pergunta: Qual perspectiva usar para auditoria de uma decisão?
Resposta: A informação conhecida na hora da decisão, com validade adequada à pergunta. Uma análise retrospectiva corrigida responde a outra questão e deve ser identificada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T056:C05 — mecanismo_avancado

Consultar memória bitemporal exige fixar a perspectiva de conhecimento e a validade de domínio em todas as relações usadas. Uma consulta pode filtrar corretamente o fato principal e ainda juntar uma entidade pela versão atual, introduzindo informação futura. A base de leitura também precisa ser consistente entre consultas sucessivas: “agora” e “último estado processado” podem mudar enquanto um relatório está sendo montado.

Condição de contorno:
Dois timestamps numa linha não bastam se as operações não preservam intervalos históricos ou se consultas e joins ignoram um dos eixos temporais.

Contrato proposto:
- Entradas: Instante de conhecimento, instante ou intervalo de validade e entidades a consultar.
- Saídas: Fatos e relações válidos sob a mesma perspectiva, com limites temporais explícitos.
- Estado: Revisões bitemporais, base de leitura e política para correções recebidas tardiamente.
- Invariante: Nenhuma evidência posterior ao limite de conhecimento entra silenciosamente numa reconstrução histórica.

Compromissos de projeto:
- Dois eixos permitem auditoria e correção retroativa, aumentando armazenamento e complexidade das consultas.
- Fixar uma base de leitura melhora consistência e pode apresentar um estado ligeiramente anterior às atualizações em curso.

## T056:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir hoje um fato válido no mês passado e mudar também sua entidade associada. A consulta “como sabíamos antes” deve usar versões antigas em ambos os lados da relação.

Plano de avaliação proposto:
Avaliação proposta: comparar consulta atual, por validade e bitemporal em dados com chegada tardia. Medir correção das junções, intervalos sobrepostos indevidos e vazamento temporal; repetir relatórios com base fixa durante atualizações concorrentes.

Comparações:
- T009 (complements): RAG temporal precisa recuperar fatos segundo a perspectiva temporal correta antes de gerar texto.
- T077 (complements): Relações de um grafo podem carregar os dois eixos para reconstrução histórica consistente.

Afirmação rastreável:
XTDB distingue filtros de valid-time e system-time e uma base de consulta composta por snapshot e clock time.
Suporte: direct; fontes: A-S032, V3A-S042
Limite: Os nomes e recursos pertencem ao XTDB consultado; outra implementação precisa definir seus próprios contratos equivalentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T056:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cuidou de joins temporais. Aqui bitemporalidade suporta auditoria de decisões e comparação justa de políticas sob informação disponível.

Projeto e decomposição
Defina consulta de auditoria com dois instantes: quando o fato valeu e o que o sistema sabia ao decidir. Misturar essas perspectivas pode punir uma decisão por informação que chegou depois.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

Controle adaptativo
Correções retroativas devem gerar nova versão de conhecimento e permitir recalcular projeções sem apagar a resposta histórica. O resultado recalculado precisa ser rotulado como reavaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

Validação contrafactual
Compare política original e nova usando o mesmo corte de conhecimento. Meça diferenças atribuíveis à política versus dados tardios; testar fatos com validade futura declarada e observação atrasada. Unidade de avaliação: decisão histórica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

USO AVANÇADO — Explicação de decisão
Cenário: Usuário pergunta por que recomendação mudou.
Estratégia: Recuperar evidências conhecidas em cada data, mostrar qual correção alterou o entendimento e separar erro anterior de informação nova.
Papel do modelo pequeno: 8–14B explica duas perspectivas.
Aceite proposto: Cada justificativa deve usar somente fatos disponíveis naquele corte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

USO AVANÇADO — Avaliação de memória
Cenário: Nova política de consolidação parece melhor.
Estratégia: Reprocessar histórico com cortes consistentes, sem entregar ao modelo correções futuras; comparar erros evitados e antecipações indevidas.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra auditoria.
Aceite proposto: Não contabilizar vantagem causada por vazamento temporal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de datas com rótulos de validade e registro separados.
8–14B: Leitor de consultas temporais já executadas por banco.
15–30B: Explicador de mudanças de decisão entre perspectivas históricas.
Requisitos de treino/runtime: Banco ou camada que preserve ambos os tempos, política de intervalos e identificação de correções.
Não aplicar quando: Datas são inferidas sem fonte ou aplicação só armazena último valor e tenta reconstruir passado por suposição.

## T056:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q025.

## T056:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T056 → T077 [complements]
Como combinar: Aplicar cortes temporais às relações do grafo.
Interface: Aresta, valid_time, recorded_time e perspectiva.
Condição: Todos os elos respeitarem corte comum.
Aceite proposto: Consultar caminho com elo conhecido apenas posteriormente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S032, V3A-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T056 → T059 [feeds]
Como combinar: Registrar correção como evento interpretável.
Interface: Evento, tempos, origem e versão do esquema.
Condição: Replay preservar distinção dos dois tempos.
Aceite proposto: Reproduzir decisão histórica sem incorporar correção futura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S032, V3A-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar timestamp de ingestão como data do fato.
- Não apresentar reavaliação atual como resposta que existia no passado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência temporal das justificativas; nenhum porte de modelo corrige retrospectivamente um histórico inexistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T054, T072, T077

## Fontes primárias associadas

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S042 — XTDB SQL Queries

[https://docs.xtdb.com/reference/main/sql/queries.html](https://docs.xtdb.com/reference/main/sql/queries.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filtros temporais por tabela e basis de leitura; snapshot e clock time como dimensões do contexto de consulta.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T057 — Causal Memory

**Nome canônico:** Causal Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T057  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória causal

## T057:C01 — conceito

Rótulo arquitetural para guardar hipóteses causais, intervenções, condições, estimativas e evidências de resultados. Não transforma associações em causas. É necessário distinguir relato de sequência temporal, mecanismo proposto e efeito causal identificado sob premissas explícitas.

Como funciona:
- Representar hipótese, tratamento ou ação e resultado de interesse.
- Registrar desenho de comparação e premissas de identificação.
- Guardar estimativa, incerteza, testes e limites de transferência.

Nota de nomenclatura: Não foi identificado um padrão único com esse nome; a fonte sustenta princípios de inferência causal, não uma implementação universal de memória.

## T057:C02 — aplicacao

Quando usar:
- Reutilizar aprendizados de experimentos e decisões anteriores.
- Evitar repetir interpretações causais já refutadas.

Quando não usar:
- Não concluir que uma ação causou melhora somente porque a melhora veio depois dela.

Implementação proposta:
- Proposta: separar efeito observado de efeito estimado por método causal.
- Guardar variáveis de ajuste e critérios de inclusão.
- Recuperar também evidências contrárias e condições em que a conclusão deixou de valer.

Aplicação LAI proposta:
Proposta LAI: guardar hipóteses e resultados de campanhas em estrutura causal verificável; a memória orienta investigação, sem garantir efeitos em novas campanhas.

## T057:C03 — riscos_validacao

Armadilhas:
- Confundimento e seleção podem criar efeito aparente.
- Transportar resultado entre públicos ou versões pode invalidar a interpretação.

Métricas sugeridas:
- Proporção de alegações com desenho e premissas explícitas.
- Estabilidade de estimativas e desempenho em validação externa quando disponível.

Testes propostos:
- Apresentar uma correlação sem identificação e exigir rótulo de hipótese.
- Usar um experimento com resultado nulo e impedir promoção de narrativa favorável como fato.

## T057:C04 — perguntas_proveniencia

Pergunta: Um grafo direcionado já é causal?
Resposta: Não. As arestas precisam de interpretação causal e de premissas sustentadas.

Pergunta: O agente pode aprender causa com logs?
Resposta: Logs ajudam, mas a identificação depende do desenho, das variáveis observadas e das hipóteses, não apenas do volume.

Pergunta: Uma LLM pode escolher o grafo causal?
Resposta: Pode propor hipóteses para revisão. Conhecimento de domínio, desenho de estudo e restrições observáveis precisam sustentar a escolha.

Pergunta: Uma estimativa pode ser lembrada após mudança de população?
Resposta: Pode ser recuperada como referência, preservando seu escopo. Transportá-la exige justificar compatibilidade dos mecanismos e das condições relevantes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T057:C05 — mecanismo_avancado

O conteúdo mínimo de uma memória causal inclui a pergunta estimada, a população, a intervenção, o desfecho e as premissas de identificação. Guardar somente “A causa B” apaga as condições que tornam a inferência defensável. Também convém separar o grafo assumido, o estimando identificado, a estimativa calculada e os testes de robustez: mudar uma dessas partes pode invalidar a conclusão sem alterar os dados brutos.

Condição de contorno:
Um efeito não identificado pelas hipóteses e dados disponíveis não se torna identificado por armazená-lo num grafo, aumentar o histórico ou pedir explicações à LLM.

Contrato proposto:
- Entradas: Hipótese causal, desenho de estudo, dados, premissas, estimando e procedimento de estimação.
- Saídas: Registro da conclusão com incerteza, testes, limites de transporte e evidências rastreáveis.
- Estado: Versões de dados, grafo assumido, estimador e resultados de análises de sensibilidade.
- Invariante: Associação, sequência temporal e efeito causal identificado permanecem categorias distintas na memória.

Compromissos de projeto:
- Registrar premissas torna conclusões revisáveis e aumenta o esforço de modelagem.
- Testes de robustez detectam fragilidades, mas aprovação em testes não prova ausência de confundimento ou identificação correta.

## T057:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar um confundidor plausível e repetir análise de sensibilidade. A memória deve registrar alteração e condições de fragilidade, sem manter a afirmação antiga como verdade incondicional.

Plano de avaliação proposto:
Avaliação proposta: avaliar recuperação de estimando, premissas e limites junto da conclusão. Comparar registro textual simples e ficha estruturada; medir confusão causal, reprodução da análise e comportamento diante de populações diferentes, sem inferir causalidade de acerto preditivo.

Comparações:
- T051 (distinct_from): Um grafo de memória organiza relações; um grafo causal exige interpretação e hipóteses adicionais.
- T049 (complements): Episódios podem fornecer observações e hipóteses, mas precisam de desenho apropriado para estimar efeitos.

Afirmação rastreável:
DoWhy distingue controles negativos, validação de grafo e sensibilidade à violação de premissas nas refutações de estimativas.
Suporte: direct; fontes: V3A-S041
Limite: Refutações são diagnósticos; passar nelas não constitui prova de que todas as premissas causais sejam verdadeiras.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T057:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou hipótese, estimando e identificação. Aqui memória causal guarda condições de transporte e revisões motivadas por novos ambientes.

Projeto e decomposição
Registre intervenção, desfecho, população e pressupostos junto da estimativa. Um efeito observado num ambiente pode não transportar para outro com mecanismo ou composição diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

Controle adaptativo
Use a memória para propor experimentos discriminantes, não para declarar causalidade por semelhança. Arestas representam hipóteses ou conclusões condicionadas; armazenar relações em grafo não identifica efeito causal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

Validação contrafactual
Compare recomendações com e sem verificação de transportabilidade. Avalie se o sistema detecta mudança de população, tratamento ou confundidor; um teste de refutação aprovado não prova todos os pressupostos. Unidade de avaliação: hipótese causal com pressupostos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

USO AVANÇADO — Otimização de pipeline
Cenário: Mudanças anteriores reduziram latência.
Estratégia: Recuperar experimento com hardware, carga e configuração; propor repetição controlada antes de atribuir ganho à mesma alteração no novo ambiente.
Papel do modelo pequeno: 3–7B extrai condições; código estima.
Aceite proposto: Separar efeito da mudança de variação de carga e hardware.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

USO AVANÇADO — Investigação de regressão
Cenário: Vários componentes mudaram juntos.
Estratégia: Construir hipóteses alternativas e planejar ablações isoladas; preservar resultado inconclusivo quando intervenções não forem identificáveis.
Papel do modelo pequeno: 15–30B organiza desenho; análise estatística externa.
Aceite proposto: Não chamar associação temporal de causa confirmada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S041, A-S036.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de variáveis, intervenções e condições explicitadas.
8–14B: Comparador de pressupostos entre estudos ou ambientes.
15–30B: Planejador de ablações e explicador de limites, sem substituir estimador causal.
Requisitos de treino/runtime: Dados adequados, desenho de identificação e ferramentas estatísticas; memória armazena evidência, não cria identificação.
Não aplicar quando: Não há suporte para pressupostos ou intervenção relevante não pode ser distinguida de mudanças simultâneas.

## T057:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q021, V4A-Q025.

## T057:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T057 → T049 [requires]
Como combinar: Recuperar condições do episódio que originou hipótese.
Interface: Ambiente, intervenção, resultado e incertezas.
Condição: Episódio não omitir fatores relevantes.
Aceite proposto: Comparar caso semelhante com confundidor diferente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S041, A-S036. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T057 → T195 [complements]
Como combinar: Executar experimento ou cálculo que avalia hipótese.
Interface: Plano de ablação, dados e estimador.
Condição: Execução autorizada e desenho adequado.
Aceite proposto: Testar hipótese alternativa e registrar resultado nulo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S041, A-S036. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar plausibilidade linguística como evidência causal.
- Não exportar efeito estimado sem verificar população e intervenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar identificação de pressupostos e qualidade do desenho; modelo de fronteira também não extrai causalidade de dados insuficientes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T051, T056

## Fontes primárias associadas

### A-S036 — DoWhy

[https://github.com/py-why/dowhy](https://github.com/py-why/dowhy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelagem explícita e testes de premissas causais.

Limite: Fundamenta a distinção entre associação e identificação causal; não define uma técnica universal chamada Causal Memory.

### V3A-S041 — DoWhy Refuting Effect Estimates

[https://www.pywhy.org/dowhy/main/user_guide/refuting_causal_estimates/refuting_effect_estimates/index.html](https://www.pywhy.org/dowhy/main/user_guide/refuting_causal_estimates/refuting_effect_estimates/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles negativos, testes de robustez, validação de grafo e sensibilidade a pressupostos causais.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T058 — Memory Consolidation

**Nome canônico:** Memory Consolidation  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T058  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** consolidação de memória

## T058:C01 — conceito

Reorganiza memórias dispersas em representações mais úteis, como sínteses, fatos candidatos e procedimentos. Pode deduplicar e relacionar experiências, mas deve conservar os registros que sustentam a consolidação. Repetição de uma mesma afirmação não equivale a confirmação independente.

Como funciona:
- Selecionar memórias relacionadas com origem identificada.
- Distinguir redundância, complementação e contradição.
- Criar uma representação derivada vinculada às fontes.

## T058:C02 — aplicacao

Quando usar:
- Muitos episódios sobre o mesmo problema.
- Acervo que cresce mais rápido que a capacidade de recuperação útil.

Quando não usar:
- Não fundir afirmações incompatíveis ou de tempos diferentes apenas por alta similaridade.

Implementação proposta:
- Proposta: agrupar por identidade, tema e validade antes de resumir.
- Contar fontes independentes separadamente de cópias.
- Registrar processo e versão da consolidação para regenerar quando uma fonte for corrigida.

Aplicação LAI proposta:
Proposta LAI: consolidar lições de auditorias em candidatos a procedimentos; promover somente após validação em novas tarefas.

## T058:C03 — riscos_validacao

Armadilhas:
- Uma generalização pode apagar exceções importantes.
- Consolidar várias cópias da mesma hipótese cria falsa impressão de evidência abundante.

Métricas sugeridas:
- Redução de redundância e manutenção de fatos críticos.
- Número de conclusões derivadas invalidadas por correções de fonte.

Testes propostos:
- Ingerir dez cópias da mesma notícia e manter apenas uma origem independente.
- Consolidar episódios com resultados opostos e preservar as condições que os diferenciam.

## T058:C04 — perguntas_proveniencia

Pergunta: Consolidação pode apagar os originais?
Resposta: O desenho recomendado conserva evidências conforme a retenção e guarda a síntese como derivação.

Pergunta: É fine-tuning automático?
Resposta: Não. Consolidar registros externos não modifica os pesos; isso exige outra etapa de treinamento.

Pergunta: Toda consolidação deve apagar os registros originais?
Resposta: Não. Apagar impede auditoria e reprocessamento; retenção dos originais é uma decisão separada, com custo e finalidade próprios.

Pergunta: Como lidar com duas fontes incompatíveis?
Resposta: Conserve as versões e o conflito, delimitando tempo, identidade e autoridade. A síntese deve comunicar a divergência quando não há base para resolvê-la.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T058:C05 — mecanismo_avancado

Consolidar cria dependências entre uma representação derivada e várias fontes. A atualização de uma origem deve marcar derivados afetados, inclusive resumos de resumos. Há também um problema de concorrência: uma consolidação iniciada antes de uma correção pode terminar depois e publicar uma versão obsoleta. Um manifesto de entradas e revisões permite verificar se o conjunto ainda era válido no momento da publicação.

Condição de contorno:
Sem referências e versões das entradas, é difícil distinguir síntese desatualizada de conflito real entre fontes ou reconstruir o conhecimento após uma correção.

Contrato proposto:
- Entradas: Conjunto de memórias relacionadas com identidade, revisão, fonte e status de verificação.
- Saídas: Representação derivada, mapa de sustentação e conflitos que não foram resolvidos.
- Estado: Manifesto das entradas, algoritmo, revisão em preparação e descendentes dependentes.
- Invariante: Consolidar não aumenta automaticamente confiança nem remove discordâncias só para produzir uma narrativa uniforme.

Compromissos de projeto:
- Sínteses reduzem custo de leitura repetida e exigem atualização de dependências.
- Consolidação incremental economiza processamento e pode acumular decisões antigas; reconstrução integral custa mais e oferece outra perspectiva.

## T058:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir uma fonte durante a consolidação de um grupo. Antes de publicar, o processo deve detectar mudança na revisão e recalcular ou marcar o resultado como desatualizado.

Plano de avaliação proposto:
Avaliação proposta: comparar consolidação incremental e reconstrução a partir das fontes após sequências de correção. Medir sustentação, preservação de exceções, atraso de invalidação e custo; controlar a quantidade de cópias derivadas de uma única origem.

Comparações:
- T069 (complements): Resumo externo é uma forma específica de consolidação; consolidar também pode produzir relações e fatos candidatos.
- T072 (complements): Versionamento identifica quais fontes e derivados pertencem à mesma revisão publicável.

Afirmação rastreável:
A-MEM permite que novas memórias atualizem atributos e contexto de notas anteriores; PROV-DM oferece relações para registrar derivação.
Suporte: related; fontes: V3A-S034, V3A-S037
Limite: A verificação de manifesto e a publicação condicional são propostas editoriais, não garantias atribuídas a esses trabalhos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T058:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou linhagem e concorrência. Aqui consolidação é liberada por comparação funcional entre memórias anteriores e candidatas.

Projeto e decomposição
Mantenha versão candidata separada e consulte ambas em perguntas representativas do conteúdo alterado. A consolidação pode reduzir redundância e simultaneamente apagar exceção rara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S033, V3A-S034, V4A-S002.

Controle adaptativo
Promova por tipo: fatos exigem suporte; procedimentos exigem condições e resultados; hipóteses podem ser agrupadas sem virar conclusões. Uma política única de resumo é insuficiente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S033, V3A-S034, V4A-S002.

Validação contrafactual
Compare versões pelo conjunto de decisões que elas sustentam. Meça respostas alteradas justificadamente, perdas de fonte e exceções esquecidas; não avaliar só semelhança textual do resumo. Unidade de avaliação: lote de consolidação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S033, V3A-S034, V4A-S002.

USO AVANÇADO — Memória de projeto acumulada
Cenário: Notas repetidas ocupam recuperação.
Estratégia: Agrupar por entidade e período, criar candidato com divergências preservadas e testar consultas sobre mudanças antes de publicar.
Papel do modelo pequeno: 8–14B consolida; 3–7B extrai campos.
Aceite proposto: Nenhuma decisão ativa pode perder sua condição ou evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S033, V3A-S034, V4A-S002.

USO AVANÇADO — Procedimentos derivados de incidentes
Cenário: Várias experiências sugerem mesma regra.
Estratégia: Extrair condições comuns e exceções, manter casos negativos e promover somente escopo que os dados sustentam.
Papel do modelo pequeno: 15–30B integra casos.
Aceite proposto: Procedimento deve recusar contexto fora do escopo validado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S033, V3A-S034, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Agrupador de duplicatas e extrator de alterações explícitas.
8–14B: Autor de consolidação local com referências por afirmação.
15–30B: Revisor de abstrações entre episódios e procedimentos candidatos.
Requisitos de treino/runtime: Versões paralelas, linhagem e consultas de validação próprias; não usar perguntas do benchmark final como conteúdo.
Não aplicar quando: Não existe forma de recuperar versões anteriores ou avaliar perda de detalhes relevantes.

## T058:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C004 — Google / Percolator no índice web
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo afirma implantação do processamento incremental na construção do índice da busca Google.
Mecanismo documentado: Transações distribuídas e notificações organizam pequenas atualizações.
Correspondência com esta base: Atualização incremental inspira consolidação, mas não é consolidação semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Delegar extração a 3–7B e confirmar alterações por transações determinísticas.
Limite: Relato histórico; não prova event sourcing, checkpoints de agentes ou resumo incremental correto. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S003.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Reflexões consolidam observações.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q013, V4A-Q023.

## T058:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T058 → T072 [requires]
Como combinar: Publicar candidato com retorno possível à versão anterior.
Interface: Manifesto antigo, candidato e dependências.
Condição: Mudanças permanecerem reversíveis na camada de memória.
Aceite proposto: Reverter candidato que removeu exceção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S033, V3A-S034, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T058 → T071 [feeds]
Como combinar: Encaminhar abstração para promoção por tipo.
Interface: Candidato, suporte, limites e resultados de comparação.
Condição: Promoção exigir evidência apropriada.
Aceite proposto: Impedir hipótese agrupada de virar fato confirmado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S033, V3A-S034, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar várias paráfrases da mesma origem como confirmação.
- Não destruir episódios originais após produzir resumo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar utilidade futura e correção após mudanças; consolidação bem escrita não significa aprendizado verdadeiro.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T054, T071, T075

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S034 — A-MEM: Agentic Memory for LLM Agents

[https://arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Notas estruturadas, conexão entre memórias e evolução das representações de notas anteriores.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S033 — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

[https://arxiv.org/abs/2504.19413](https://arxiv.org/abs/2504.19413)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração, consolidação e recuperação de memória conversacional; variante com grafo.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S003 — Large-scale Incremental Processing Using Distributed Transactions and Notifications

[https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Percolator implantado no índice web; processamento incremental com transações.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T059 — Event Sourcing

**Nome canônico:** Event Sourcing  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T059  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** estado derivado de eventos

## T059:C01 — conceito

Mantém a sequência de eventos de domínio como registro de referência e deriva o estado atual por projeções. Permite reconstrução e auditoria, ao custo de lidar com ordem, versões e reprocessamento. Um arquivo de logs arbitrários não constitui automaticamente event sourcing.

Como funciona:
- Registrar eventos com identidade e semântica de domínio.
- Aplicar eventos a projeções de estado.
- Reconstruir projeções a partir do histórico autorizado.

## T059:C02 — aplicacao

Quando usar:
- Fluxos em que reconstruir decisões e estado é requisito central.
- Sistemas com múltiplas projeções do mesmo histórico.

Quando não usar:
- Evitar complexidade desnecessária quando CRUD com trilha de auditoria já satisfaz o problema.

Implementação proposta:
- Proposta: definir aggregate_id, sequência, event_id e schema_version.
- Tornar projeções idempotentes e separar replay de efeitos externos.
- Evoluir schemas com migrações explícitas, preservando interpretação de eventos antigos.

Aplicação LAI proposta:
Proposta LAI: usar eventos para ações relevantes e evidências da Helena; geração de mensagem ou chamada externa precisa de controle próprio de idempotência.

## T059:C03 — riscos_validacao

Armadilhas:
- Reexecutar um evento pode disparar novamente um efeito externo.
- Mudanças de significado em schemas tornam replays inconsistentes.

Métricas sugeridas:
- Tempo de reconstrução e atraso das projeções.
- Divergência entre estado materializado e replay.

Testes propostos:
- Reaplicar o mesmo evento e exigir estado final igual.
- Reconstruir uma missão do zero e comparar com o snapshot persistido.

## T059:C04 — perguntas_proveniencia

Pergunta: Event sourcing garante exatamente uma execução?
Resposta: Não. Entrega, processamento e efeitos externos precisam de estratégias explícitas de idempotência e reconciliação.

Pergunta: Todo log é evento de domínio?
Resposta: Não. Um evento precisa ter significado, identidade e contrato suficientes para reconstruir estado.

Pergunta: Replay deve usar o relógio atual?
Resposta: Somente se a projeção foi definida assim. Reconstrução determinística costuma precisar do tempo do evento ou de valores persistidos, evitando depender de agora.

Pergunta: Como corrigir um evento já registrado?
Resposta: Use eventos corretivos ou interpretação versionada conforme o domínio. Sobrescrever o passado silenciosamente destrói a explicação do estado anteriormente conhecido.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T059:C05 — mecanismo_avancado

Reconstrução por eventos depende tanto da sequência persistida quanto da versão do projetor que interpreta essa sequência. Uma mudança de regra pode produzir outro estado a partir dos mesmos eventos, mesmo sem corrupção. Snapshots aceleram reidratação e precisam declarar posição do stream e compatibilidade do projetor. Eles são derivados substituíveis; o histórico continua necessário para reconstruir e diagnosticar diferenças entre projeções.

Condição de contorno:
Um broker com retenção limitada e ordenação parcial não oferece automaticamente todas as garantias de um event store por entidade.

Contrato proposto:
- Entradas: Eventos identificados, ordem por agregado, versões de schema e regra de projeção.
- Saídas: Estado materializado com posição consumida, revisão do projetor e erros de interpretação explícitos.
- Estado: Stream autoritativo, checkpoints de projeção, snapshots e registros de deduplicação.
- Invariante: Reproduzir eventos para reconstruir estado não reenvia mensagens nem repete efeitos de negócio por padrão.

Compromissos de projeto:
- Eventos permitem novas projeções e tornam evolução semântica mais trabalhosa.
- Snapshots reduzem tempo de reconstrução e exigem política de compatibilidade para não ocultar erros do projetor atual.

## T059:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar a interpretação de um evento antigo e tentar usar snapshot produzido pelo projetor anterior. A reconstrução deve detectar incompatibilidade ou aplicar migração conhecida, sem combinar silenciosamente duas semânticas.

Plano de avaliação proposto:
Avaliação proposta: comparar projeção incremental, replay integral e replay após snapshot no mesmo stream. Medir equivalência de estado, tempo, eventos duplicados ignorados e tratamento de versões antigas; executar a avaliação com efeitos externos desabilitados.

Comparações:
- T060 (complements): Um checkpoint pode registrar posição e estado do consumidor; event sourcing define o histórico autoritativo do domínio.
- T072 (complements): Versionar projetores e schemas permite explicar por que a mesma sequência produz representações diferentes.

Afirmação rastreável:
A documentação Microsoft descreve snapshots como otimização de reconstrução, mantendo o eventstream como fonte de referência.
Suporte: direct; fontes: A-S027
Limite: Adotar esse padrão exige contratos de ordenação, concorrência e evolução; um log genérico não os fornece automaticamente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T059:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou replay e efeitos. Aqui Event Sourcing sustenta evolução de esquema e reconstrução de memórias com projetores alternativos.

Projeto e decomposição
Eventos devem representar fatos de domínio, não frases livres do agente. Campos de intenção, tentativa e confirmação precisam ser distintos para reconstruir estado sem inventar sucesso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

Controle adaptativo
Versione schema e projetor. Upcasting pode adaptar formato antigo, mas não deve criar informação que nunca existiu; marcar ausência preserva honestidade da reconstrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

Validação contrafactual
Compare projeção atual e nova sobre o mesmo log, sem emitir efeitos externos. Meça divergências por tipo de evento e decisões afetadas; verificar eventos desconhecidos e fora de ordem. Unidade de avaliação: stream de eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

USO AVANÇADO — Migração de memória
Cenário: Novo schema separa hipóteses de decisões.
Estratégia: Reprocessar eventos em projeção paralela, comparar consultas e publicar somente após explicar diferenças materiais.
Papel do modelo pequeno: 3–7B classifica candidatos; código projeta.
Aceite proposto: Nenhum evento ambíguo pode ser reinterpretado silenciosamente como confirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

USO AVANÇADO — Auditoria de tarefa
Cenário: É necessário explicar sequência de ações.
Estratégia: Reconstruir estado com versão histórica do projetor e separar reavaliação atual em outro artefato.
Papel do modelo pequeno: 8–14B explica sequência.
Aceite proposto: Explicação deve apontar eventos que realmente ocorreram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S027, V4A-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de campos para propostas de evento, com validação externa.
8–14B: Leitor e explicador de projeção determinística.
15–30B: Analista de divergências entre projetores, sem controlar aplicação irrestrita de eventos.
Requisitos de treino/runtime: Log append-only, esquema versionado, ordenação definida e projetores determinísticos quando possível.
Não aplicar quando: Operações externas são repetidas no replay ou o histórico mistura intenção e confirmação.

## T059:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008.

## T059:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T059 → T072 [complements]
Como combinar: Versionar projetor e schema como parte da memória.
Interface: Stream, projector_version e migration_id.
Condição: Reconstrução declarar interpretação usada.
Aceite proposto: Reprocessar evento antigo com campo ausente e preservar desconhecido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S027, V4A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T059 → T075 [feeds]
Como combinar: Enviar divergências de projeção para reconciliação.
Interface: Estado anterior, novo estado e eventos causadores.
Condição: Reconciliação não apagar log de origem.
Aceite proposto: Detectar diferença material antes de trocar projeção ativa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S027, V4A-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não executar novamente pagamentos, mensagens ou gravações externas no replay.
- Não usar timestamp de chegada como ordem causal universal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar explicações sobre log idêntico; reconstrução determinística deve ficar em código, não depender do porte do LLM.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T064, T162

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T060 — Agent Checkpointing / Checkpoint & Resume — incluindo checkpoints transacionais

**Nome canônico:** Agent Checkpointing com retomada e checkpoint transacional  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T060  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Checkpointing; ponto de retomada; snapshot de execução; Agent Checkpointing; Checkpoint & Resume; checkpoint transacional

## T060:C01 — conceito

Agent Checkpointing salva estado suficiente para retomar uma execução após pausa ou falha. Um checkpoint transacional grava conjuntamente os elementos que precisam representar o mesmo avanço, como estado, cursor de eventos e intenções pendentes, dentro de uma transação. A garantia cobre esse limite de atomicidade; uma chamada externa não se torna atômica apenas por existir um snapshot local.

Como funciona:
- Escolher uma fronteira consistente: tarefas concluídas, tarefas pendentes, versões e resultados duráveis conhecidos.
- Persistir estado e cursor associados em uma única confirmação; falhas antes do commit não devem publicar um avanço parcial.
- Ao retomar, validar compatibilidade e reconciliar efeitos com resultado desconhecido antes de repetir operações.

## T060:C02 — aplicacao

Quando usar:
- Workflows longos, aprovações humanas e execuções sujeitas a reinício nas quais recomputar tudo é caro ou perigoso.

Quando não usar:
- Como substituto de idempotência, backup completo ou transação distribuída entre serviços independentes.

Implementação proposta:
- Proposta: definir mission_id, checkpoint_id, schema_version, state_version, event_cursor, artefatos referenciados e operações com chave de idempotência.
- Quando houver publicação de eventos, gravar a intenção em outbox na mesma transação do estado; um publicador posterior confirma o envio.
- Manter último checkpoint íntegro e testar migração de schema. Armazenamento apenas em RAM não permite retomada após perda do processo.
- Tratar resposta perdida depois de uma ação externa como resultado incerto: consultar recibo ou estado remoto antes de reexecutar.

Aplicação LAI proposta:
Proposta LAI: consolidar checkpoint, cursor e outbox no mesmo armazenamento transacional e deixar a reconciliação explícita no controlador de execução.

## T060:C03 — riscos_validacao

Armadilhas:
- Salvar o cursor antes dos resultados pode fazer a retomada pular trabalho que nunca foi concluído.
- Replay de código com efeitos não controlados pode duplicar alterações mesmo quando o checkpoint está íntegro.

Métricas sugeridas:
- Tempo de recuperação, trabalho repetido, checkpoints inválidos e efeitos duplicados nos cenários de falha.

Testes propostos:
- Teste proposto: interromper antes e depois do commit; estado e cursor devem reaparecer juntos ou nenhum deles.
- Interromper após efeito externo e antes do recibo local; a retomada deve reconciliar a mesma operação, sem criar outra intenção.

## T060:C04 — perguntas_proveniencia

Pergunta: Um arquivo JSON salvo é checkpoint transacional?
Resposta: Pode ser um snapshot, mas o nome transacional exige atomicidade definida para todos os elementos associados e uma estratégia verificável de recuperação.

Pergunta: Commit local garante exatamente uma chamada externa?
Resposta: Não. Outbox, idempotência e reconciliação tratam a fronteira externa; o commit protege somente os dados participantes da transação.

Pergunta: Salvar todas as variáveis garante retomada?
Resposta: Não. Também são necessários fluxo de controle, identidade de operações, compatibilidade do código e acesso aos artefatos referenciados.

Pergunta: Retornar a um checkpoint desfaz uma publicação externa?
Resposta: Não. Isso altera a execução local. É necessário observar o serviço externo e, se apropriado, executar uma compensação explicitamente autorizada.

Escopo das fontes:
LangGraph fundamenta checkpoints; PostgreSQL, atomicidade local; AWS, outbox e idempotência. O contrato de checkpoint LAI e seus testes são propostos.

## T060:C05 — mecanismo_avancado

É útil distinguir snapshot de dados, checkpoint de execução e gravações parciais de tarefas concluídas. Um snapshot mostra valores; a retomada também precisa saber o que executar depois. No LangGraph, checkpoints completos ficam em fronteiras de super-step, enquanto pending writes preservam resultados de nós concluídos quando outro nó falha. Essas gravações intermediárias não são, por si, checkpoints completos para qualquer ponto de retorno.

Condição de contorno:
Um ponto persistido não restaura arquivos temporários, credenciais expiradas ou serviços externos ao mesmo instante; a execução precisa verificar suas dependências ao retomar.

Contrato proposto:
- Entradas: Estado, agenda de execução, resultados duráveis de tarefas e referências a artefatos necessários.
- Saídas: Checkpoint validado com ponto de retomada e operações externas cujo resultado ainda é incerto.
- Estado: Identidade da thread, revisão de schema, tarefas pendentes e mecanismo de durabilidade.
- Invariante: Retomar trabalho computacional nunca implica que efeitos externos ocorridos depois do checkpoint foram desfeitos.

Compromissos de projeto:
- Salvar mais frequentemente reduz recomputação e aumenta escrita e sincronização.
- Persistir resultados por tarefa evita repetir trabalho concluído e exige distinguir recuperação parcial de retorno a um snapshot integral.

## T060:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar dois nós paralelos, concluir um e falhar no outro. A retomada deve reutilizar o resultado persistido do primeiro conforme o contrato; uma chamada externa sem recibo deve permanecer desconhecida.

Plano de avaliação proposto:
Avaliação proposta: comparar reinício integral e recuperação por checkpoint em falhas entre fronteiras. Medir trabalho repetido, perda de resultados, validade da agenda e efeitos duplicados; testar queda do processo, não apenas exceção capturada.

Comparações:
- T059 (distinct_from): Snapshot de projeção acelera reconstrução de domínio; checkpoint inclui informações para continuar a execução.
- T075 (complements): Reconciliação determina efeitos externos incertos que o checkpoint local não consegue comprovar.

Afirmação rastreável:
LangGraph distingue checkpoints por super-step e pending writes de tarefas concluídas para recuperação após falhas parciais.
Suporte: direct; fontes: V3A-S031
Limite: Durabilidade depende do saver e configuração; referências no estado não tornam seus recursos externos duráveis automaticamente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T060:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu snapshot, checkpoint e efeitos incertos. Aqui retomada inclui compatibilidade do executável e migração do contrato de estado.

Projeto e decomposição
Um checkpoint precisa identificar código, modelo, schema e referências necessárias à próxima etapa. Estado serializado válido pode ser incompatível com nova versão do executor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

Controle adaptativo
Restaure em modo de inspeção antes de liberar efeitos quando houve mudança de ambiente. Migração deve preservar operações pendentes e seus identificadores, sem convertê-las em novas tentativas automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

Validação contrafactual
Compare retomada na mesma versão e após atualização controlada. Meça etapas refeitas, operações duplicadas e estados bloqueados corretamente; snapshot isolado não prova capacidade de continuar o fluxo. Unidade de avaliação: ponto de retomada durável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

USO AVANÇADO — Atualização do agente
Cenário: Runtime muda enquanto tarefas estão pausadas.
Estratégia: Validar schema, migrar campos conhecidos e marcar operação externa incerta para reconciliação antes de continuar.
Papel do modelo pequeno: 3–7B explica incompatibilidade; código migra.
Aceite proposto: Nenhuma operação pendente pode ganhar novo identificador sem decisão explícita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

USO AVANÇADO — Falha durante coleta
Cenário: Alguns resultados já estão persistidos.
Estratégia: Restaurar fronteira confirmada e reexecutar somente trabalho sem confirmação, usando os mesmos contratos de deduplicação.
Papel do modelo pequeno: 8–14B retoma tarefa.
Aceite proposto: Artefatos confirmados devem ser reutilizados e resultados ausentes identificados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V3A-S031, A-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de etapa curta após checkpoint validado por código.
8–14B: Leitor de estado migrado com testes de pré-condição.
15–30B: Replanejador quando ambiente mudou e continuidade direta deixou de ser válida.
Requisitos de treino/runtime: Backend durável, manifestos de versão e protocolo de efeitos; checkpoint em memória não cobre reinício do processo.
Não aplicar quando: Referências essenciais expiraram ou não é possível determinar status das operações externas.

## T060:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: O sistema utiliza checkpoints regulares e retomada após erros.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C024 — LinkedIn / Microsoft / Brooklin
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.
Mecanismo documentado: Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.
Correspondência com esta base: Estado e offsets/checkpoints sustentam retomada de tarefas.
Transferência proposta para modelo pequeno: Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.
Limite: Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.
Fontes: V4C-S024, V4C-S025.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Tolerância a falhas de fluxo é relacionada à retomada, mas não prova checkpoint LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008.

## T060:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T060 → T243 [requires]
Como combinar: Reconciliar efeitos sem confirmação antes de retomar.
Interface: operation_id, intenção, tentativa e recibo observado.
Condição: Serviço permitir consulta ou resolução explícita.
Aceite proposto: Simular sucesso externo com ACK perdido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V3A-S031, A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T060 → T064 [complements]
Como combinar: Serializar estado portátil e dependências.
Interface: Checkpoint, schema, código e referências duráveis.
Condição: Objetos não dependerem de handles efêmeros.
Aceite proposto: Restaurar em processo novo sem sessão original.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V3A-S031, A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir salvar um arquivo com checkpoint transacional completo.
- Não repetir efeitos para descobrir se a primeira tentativa funcionou.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade correta após falha; LLM maior não resolve ausência de protocolo de confirmação.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T162, T240, T242, P011, P015

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

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

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3A-S031 — LangGraph Checkpointers

[https://docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints por super-step, StateSnapshot e pending writes de tarefas concluídas; estado de execução e retomada.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

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

# T061 — Content-Addressable Storage

**Nome canônico:** Content-Addressable Storage  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T061  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** armazenamento endereçado por conteúdo; CAS

## T061:C01 — conceito

Endereça objetos pelo hash de seu conteúdo em vez de depender apenas de nome ou localização. Conteúdo idêntico produz o mesmo identificador sob o mesmo esquema; alteração produz outro. O hash verifica identidade dos bytes, mas não prova a verdade nem a autoria do que eles dizem.

Como funciona:
- Definir serialização ou bytes canônicos.
- Calcular o identificador e persistir o objeto.
- Verificar o hash ao recuperar e ligar referências à versão imutável.

## T061:C02 — aplicacao

Quando usar:
- Evidências e artefatos reutilizados em muitas missões.
- Deduplicação e rastreio de alterações de documentos.

Quando não usar:
- Não usar o hash como autorização de acesso nem como certificado de que um teste foi executado.

Implementação proposta:
- Proposta: usar algoritmo declarado e manifestos com tamanho e tipo.
- Separar objetos imutáveis de aliases como versão atual.
- Controlar coleta de lixo por referências para não apagar conteúdo ainda necessário.

Aplicação LAI proposta:
Proposta LAI: identificar logs e contratos por conteúdo para ligar cada achado à evidência examinada; preservar controles de acesso separados.

## T061:C03 — riscos_validacao

Armadilhas:
- Mesmo conteúdo serializado de forma diferente pode produzir hashes distintos.
- Deduplicação pode criar compartilhamento indevido se permissões não forem verificadas.

Métricas sugeridas:
- Falhas de integridade e taxa de deduplicação.
- Referências quebradas após retenção ou limpeza.

Testes propostos:
- Modificar um byte e exigir falha de verificação contra o identificador antigo.
- Apagar objeto ainda referenciado e detectar inconsistência do manifesto.

## T061:C04 — perguntas_proveniencia

Pergunta: Um hash comprova que a afirmação do arquivo é verdadeira?
Resposta: Não. Comprova identidade ou alteração dos bytes em relação ao hash esperado.

Pergunta: É preciso usar Git?
Resposta: Não. Git exemplifica esse modelo, mas ele pode ser implementado em bancos ou armazenamento de objetos.

Pergunta: Mesmo CID garante que o objeto estará disponível?
Resposta: Não. O identificador permite conferir o conteúdo encontrado, mas alguém ainda precisa armazenar e servir os blocos necessários.

Pergunta: Posso usar latest num store por conteúdo?
Resposta: Pode manter um alias mutável separado. Para reproduzir uma decisão, registre também o identificador imutável para o qual o alias foi resolvido.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T061:C05 — mecanismo_avancado

O endereço por conteúdo depende da representação efetivamente hasheada. Em IPFS, um CID inclui informações de codec e hash, e um arquivo pode ser dividido em blocos ligados por um DAG. Portanto, o CID raiz não é simplesmente o SHA-256 dos bytes do arquivo completo. Configurações de chunking e codificação podem mudar o identificador sem mudar o conteúdo lógico interpretado pelo usuário.

Condição de contorno:
Identidade por bytes não resolve equivalência semântica, disponibilidade, autenticidade do produtor ou permissão de acesso ao objeto compartilhado.

Contrato proposto:
- Entradas: Bytes ou estrutura serializada, algoritmo de hash, codec e parâmetros de segmentação.
- Saídas: Identificador verificável, manifesto de representação e objeto recuperável conforme a política de retenção.
- Estado: Objetos, referências vivas, aliases mutáveis e configuração de produção dos identificadores.
- Invariante: A verificação usa exatamente a representação e o esquema declarados, sem confundir um checksum simples com outro tipo de identificador.

Compromissos de projeto:
- Deduplicação economiza armazenamento de objetos iguais e exige rastrear referências antes de coletá-los.
- Representações estruturadas permitem reutilizar partes e tornam a reprodução do identificador dependente de mais parâmetros.

## T061:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ingerir o mesmo arquivo com dois esquemas de blocos e comparar os identificadores. O sistema deve reconhecer a diferença de representação e verificar cada objeto segundo seu contrato, sem acusar corrupção apenas por IDs distintos.

Plano de avaliação proposto:
Avaliação proposta: comparar endereçamento por nome e conteúdo em revisões, deduplicação e recuperação. Medir integridade detectada, reprodução dos IDs, custo de manifestos e objetos órfãos; testar indisponibilidade separadamente de alteração de bytes.

Comparações:
- T007 (complements): Canonicalização define quais bytes representam uma requisição; CAS endereça o objeto resultante pelo conteúdo.
- T073 (distinct_from): Endereço verificável detecta alteração; retenção imutável controla possibilidade de sobrescrever ou excluir versões.

Afirmação rastreável:
A documentação IPFS explica que CIDs incluem hash e codec e não equivalem necessariamente ao hash do arquivo inteiro.
Suporte: direct; fontes: V3A-S038
Limite: A descrição é específica do esquema IPFS; outros stores podem usar um hash direto sobre bytes canônicos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T061:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu CID e hash bruto. Aqui CAS sustenta deduplicação verificável, coleta de lixo e manifestos de proveniência.

Projeto e decomposição
Armazene manifesto que liga bytes, interpretação e origem. Conteúdos iguais podem ter proveniências distintas; deduplicar armazenamento não deve fundir automaticamente autoridade ou identidade documental.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

Controle adaptativo
Faça coleta de lixo por referências alcançáveis a partir de raízes declaradas. Um artefato não acessado recentemente pode continuar necessário para auditoria ou reconstrução de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

Validação contrafactual
Compare armazenamento por caminho e CAS com manifestos. Meça deduplicação, referências quebradas e recuperação após limpeza; hash correto não comprova autoria nem verdade. Unidade de avaliação: artefato endereçado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

USO AVANÇADO — Evidências compartilhadas
Cenário: Vários agentes usam o mesmo documento.
Estratégia: Guardar bytes uma vez, criar referências de proveniência separadas e transportar digest para verificar leituras.
Papel do modelo pequeno: 3–7B consome trechos; código verifica hash.
Aceite proposto: Cada citação deve preservar origem mesmo quando bytes forem iguais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

USO AVANÇADO — Índices reconstruíveis
Cenário: Embeddings e resumos derivam de arquivos.
Estratégia: Registrar DAG de dependências e manter raízes da versão ativa; remover apenas artefatos sem dependentes protegidos.
Papel do modelo pequeno: 8–14B explica linhagem.
Aceite proposto: Reconstrução da versão ativa deve continuar possível após limpeza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de manifestos e referências, sem responsabilidade pelo cálculo criptográfico.
8–14B: Analista de dependências de artefatos e falhas de resolução.
15–30B: Integrador de evidências de múltiplas origens com identidade física compartilhada.
Requisitos de treino/runtime: Hash/codec definidos, armazenamento disponível e raízes de retenção; autenticação da origem é camada separada.
Não aplicar quando: Conteúdo precisa ser mutável sob o mesmo identificador ou política de retenção não distingue raízes protegidas.

## T061:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q006, V4A-Q026.

## T061:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T061 → T073 [complements]
Como combinar: Vincular evidência preservada a bytes verificáveis.
Interface: Digest, origem, retenção e manifestação de autoria.
Condição: Imutabilidade e autenticidade serem avaliadas separadamente.
Aceite proposto: Substituir conteúdo sob caminho e detectar divergência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S038, A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T061 → T072 [feeds]
Como combinar: Versionar manifesto de artefatos derivados.
Interface: Raiz, dependências e versões de produtores.
Condição: Manifesto declarar conjunto completo da revisão.
Aceite proposto: Eliminar objeto referenciado e exigir falha explícita de integridade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S038, A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar consistent hashing de endereçamento por conteúdo.
- Não deduplicar direitos ou proveniência apenas porque bytes coincidem.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar verificabilidade e recuperação; CAS melhora identidade dos artefatos, não entendimento semântico do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T007, T015, T073

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T062 — Hierarchical Memory

**Nome canônico:** Hierarchical Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T062  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória hierárquica

## T062:C01 — conceito

Organiza memória em níveis com diferentes papéis, custos e graus de detalhe: contexto ativo, estado, episódios, fatos, procedimentos e arquivos originais. Essa organização é uma decisão arquitetural; não existe obrigação universal de ter cinco ou seis níveis.

Como funciona:
- Definir responsabilidade e critérios de admissão de cada nível.
- Mover ou recuperar informação conforme necessidade da tarefa.
- Preservar ligações entre sínteses e fontes originais.

## T062:C02 — aplicacao

Quando usar:
- Agentes que precisam operar por longos períodos com contexto limitado.
- Acervos que combinam fatos, experiências e procedimentos.

Quando não usar:
- Não confundir múltiplas pastas com uma hierarquia funcional sem política de acesso e atualização.

Implementação proposta:
- Proposta: separar contexto ativo de armazenamento durável.
- Declarar quais dados são autoritativos e quais são projeções.
- Avaliar promoção, invalidação e recuperação em todos os níveis, sem depender somente de resumos.

Aplicação LAI proposta:
Proposta LAI: combinar estado da missão, episódios, conhecimento e skills com fontes originais; escolher o número de camadas por necessidade, não por rótulo.

## T062:C03 — riscos_validacao

Armadilhas:
- Uma correção na fonte pode não alcançar o resumo ativo.
- Muitos níveis aumentam complexidade e latência de recuperação.

Métricas sugeridas:
- Tempo e precisão para chegar à evidência original.
- Consistência entre níveis após mudanças.

Testes propostos:
- Corrigir um fato e verificar propagação às memórias derivadas.
- Recuperar uma informação antiga sem carregar o acervo inteiro.

## T062:C04 — perguntas_proveniencia

Pergunta: Hierarquia é sempre do recente para o antigo?
Resposta: Não. Pode refletir função, abstração, persistência ou custo de acesso.

Pergunta: Ela amplia fisicamente a janela da LLM?
Resposta: Não. Gerencia o que entra na janela e mantém o restante recuperável fora dela.

Pergunta: Toda camada precisa de uma cópia do fato?
Resposta: Não. Pode conter apenas índice ou referência. Cópias e resumos criam obrigações adicionais de atualização e controle de versão.

Pergunta: Como decidir onde manter um item?
Resposta: Considere custo de acesso, frequência, criticidade e capacidade de reconstrução. Frequência alta não autoriza ignorar validade ou proveniência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T062:C05 — mecanismo_avancado

Há duas hierarquias diferentes: níveis de armazenamento com latência distinta e níveis de abstração com detalhe distinto. Um resumo pode estar no armazenamento lento, e um trecho original pode permanecer ativo; misturar essas dimensões dificulta políticas de atualização. Para cada passagem entre níveis, declare se ocorre cópia, seleção ou transformação, e qual versão continua sendo a referência quando as representações divergem.

Condição de contorno:
Adicionar camadas pode piorar o sistema quando buscas atravessam muitos níveis, os índices não representam exceções ou a atualização de derivados fica atrasada.

Contrato proposto:
- Entradas: Memórias classificadas por função, custo de acesso, detalhe e origem autoritativa.
- Saídas: Representações distribuídas em níveis com vínculos explícitos e caminhos de recuperação.
- Estado: Políticas de promoção, invalidação, retenção e posição de atualização de cada projeção.
- Invariante: Uma correção na origem torna detectável a obsolescência de qualquer derivado que ainda não foi reconstruído.

Compromissos de projeto:
- Hierarquias reduzem leitura recorrente e acrescentam decisões de roteamento que podem falhar.
- Mais níveis favorecem especialização e ampliam custo de coerência, observabilidade e recuperação de falhas.

## T062:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir uma exceção no registro original enquanto um resumo superior continua ativo. A consulta deve detectar a revisão pendente ou reabrir a origem, sem usar o resumo antigo como vigente.

Plano de avaliação proposto:
Avaliação proposta: comparar store único e hierarquia com carga de leituras e correções controlada. Medir latência por nível, fontes abertas, atraso de invalidação e respostas obsoletas; incluir tarefas que precisam de detalhe ausente no índice superior.

Comparações:
- T008 (complements): Resumos hierárquicos organizam abstração; memória hierárquica também pode organizar custo e persistência.
- T063 (complements): Gerência virtual de contexto é uma aplicação de níveis de memória orientada à janela ativa limitada.

Afirmação rastreável:
MemGPT organiza níveis de memória para mover informação entre armazenamento externo e contexto limitado.
Suporte: related; fontes: A-S009
Limite: A fonte sustenta essa arquitetura específica; não exige número fixo de camadas nem valida todas as taxonomias de memória.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T062:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou armazenamento e abstração. Aqui hierarquia é otimizada por custo de movimento e localidade de tarefa.

Projeto e decomposição
Meça quanto custa mover e interpretar cada unidade entre arquivo, índice e janela. Um resumo curto pode ser barato de carregar e caro de desambiguar; latência física não é custo total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

Controle adaptativo
Promova residência temporária por fase da tarefa, não por popularidade global. Múltiplas tarefas concorrentes podem ter conjuntos de trabalho distintos e competir por níveis rápidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

Validação contrafactual
Compare política estática, por recência e por fase. Meça recargas, latência de leitura e decisões erradas por usar abstração inadequada; separar nível físico do nível semântico na telemetria. Unidade de avaliação: trajetória de acessos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

USO AVANÇADO — Projeto com módulos ativos
Cenário: Somente parte do repositório muda.
Estratégia: Manter contratos dos módulos ativos na janela, descritores no nível intermediário e originais externos; rebaixar após encerrar fase.
Papel do modelo pequeno: 3–7B usa contratos; 8–14B abre detalhe.
Aceite proposto: Mudança de módulo deve carregar versão correta antes de agir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

USO AVANÇADO — Pesquisa em acervo extenso
Cenário: Consulta alterna visão geral e detalhe.
Estratégia: Usar síntese para navegação e originais para afirmações precisas; contabilizar custo de expandir cada nível.
Papel do modelo pequeno: 15–30B integra níveis.
Aceite proposto: Detalhe factual deve continuar verificável no original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de nível intermediário explícito com referências simples.
8–14B: Controlador de expansão entre poucos níveis por necessidade.
15–30B: Integrador global que decide quais detalhes precisam subir à janela.
Requisitos de treino/runtime: Catálogo de níveis, custo de recarga e dependências; não pressupor equivalência entre RAM, contexto e resumo.
Não aplicar quando: Custo de movimentar níveis excede benefício ou a abstração perde informação indispensável sem recuperação.

## T062:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Hierarquia de KV é analogia de camadas de memória, não memória semântica do agente.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T062:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T062 → T074 [complements]
Como combinar: Escolher residência por fase e custo de retorno.
Interface: Objeto, nível, custo e condição de fixação.
Condição: Evicção não alterar retenção canônica.
Aceite proposto: Medir oscilações entre os mesmos dois níveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T062 → T008 [complements]
Como combinar: Criar abstrações para navegação, separadas da localização física.
Interface: Resumo, nível semântico e referências.
Condição: Originais permanecerem disponíveis.
Aceite proposto: Comparar resposta detalhada com resumo e com folha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar disco de memória semântica apenas por ser durável.
- Não usar resumo como substituto literal da evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo total de acesso e leitura; mais níveis podem aumentar complexidade sem melhorar respostas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T048, T050, T063, T071

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S039 — Redis Key eviction

[https://redis.io/docs/latest/develop/reference/eviction/](https://redis.io/docs/latest/develop/reference/eviction/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Políticas de eviction, noeviction, LRU aproximado, LFU probabilístico e distinção entre expiração e pressão de capacidade.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T063 — Virtual Context Management — memória virtual de contexto, estilo MemGPT

**Nome canônico:** Virtual Context Management — MemGPT  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T063  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gerenciamento de contexto virtual; Virtual Context Management — MemGPT

## T063:C01 — conceito

Estratégia proposta no MemGPT, inspirada em memória virtual de sistemas operacionais: informação se move entre contexto limitado e armazenamento externo, com controle explícito da execução. A analogia não implica acesso automático e perfeito a tudo que está armazenado.

Como funciona:
- Distinguir informação ativa de memória externa recuperável.
- Usar operações de memória para carregar e preservar conteúdo.
- Controlar a continuação da tarefa conforme necessidade de nova informação.

## T063:C02 — aplicacao

Quando usar:
- Conversas entre sessões e análise documental extensa.
- Pesquisa de agentes que gerenciam sua própria seleção de contexto.

Quando não usar:
- Não tratar a capacidade externa como atenção simultânea sobre todo o histórico.

Implementação proposta:
- Proposta: definir ferramentas de leitura e escrita com contratos curtos.
- Manter memória essencial fixada e orçamento para novos resultados.
- Medir quando o agente deixa de recuperar algo necessário e oferecer regras de recuperação obrigatória.

Aplicação LAI proposta:
Proposta LAI: adotar princípios de contexto virtual na Helena sem afirmar reprodução do MemGPT; a implantação precisa de avaliação própria.

## T063:C03 — riscos_validacao

Armadilhas:
- O modelo pode não perceber a ausência de uma informação.
- Operações frequentes de memória podem aumentar latência e custo.

Métricas sugeridas:
- Recall de informações fora do contexto ativo.
- Sucesso de tarefa e custo de movimentação entre níveis.

Testes propostos:
- Colocar um fato relevante apenas na memória externa e pedir tarefa que dependa dele.
- Simular indisponibilidade da memória e exigir resposta com lacuna explícita.

## T063:C04 — perguntas_proveniencia

Pergunta: MemGPT fornece contexto infinito?
Resposta: Não literalmente. Usa memória externa e movimentação de informação para trabalhar além do contexto ativo.

Pergunta: É a mesma coisa que simplesmente aumentar max_context?
Resposta: Não. A estratégia organiza recuperação e persistência, enquanto a configuração altera o limite de entrada suportado.

Pergunta: A janela física do modelo aumenta?
Resposta: Não por esse mecanismo. O sistema altera qual informação entra na janela e pode executar várias chamadas para trabalhar com um acervo maior.

Pergunta: É necessário modificar pesos para esse padrão?
Resposta: A ideia pode ser implementada com ferramentas e controle externo. O desempenho depende da capacidade do modelo de usar essas operações corretamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T063:C05 — mecanismo_avancado

A analogia com memória virtual funciona melhor para entender movimentação do que garantias. Sistemas operacionais identificam endereços ausentes de forma precisa; um agente pode não perceber que precisa de uma lembrança. Ferramentas de busca, escrita e controle de execução ampliam o contexto utilizável, mas a política de acionamento continua sujeita a falhas. Há custo tanto para localizar conteúdo quanto para decidir quando fazê-lo.

Condição de contorno:
Sem índices descobríveis, regras de recuperação ou sinais de dependência, o agente pode responder com a janela atual mesmo quando existe evidência decisiva armazenada fora dela.

Contrato proposto:
- Entradas: Estado essencial, contexto ativo, ferramentas de memória e limites de orçamento por chamada.
- Saídas: Movimentações de conteúdo, referências resolvidas e continuidade da execução com lacunas registradas.
- Estado: Memórias externas, histórico de buscas, regiões fixadas e limites de controle do agente.
- Invariante: A disponibilidade de informação externa não é apresentada como se todo esse conteúdo tivesse sido lido simultaneamente.

Compromissos de projeto:
- Mover dados sob demanda permite sessões maiores e adiciona turnos de ferramenta.
- Autogerência oferece flexibilidade e exige limites para evitar busca circular ou gravação de memórias incorretas.

## T063:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: armazenar uma restrição antiga fora da janela e criar uma ação que dependa dela. Compare acionamento espontâneo e regra explícita de consulta; falha de recuperação deve impedir alegação de cobertura completa.

Plano de avaliação proposto:
Avaliação proposta: comparar janela fixa, recuperação inicial e gerência durante a execução. Medir acertos de recuperação, leituras redundantes, custo de controle e retenção entre sessões; incluir lacunas que não produzem baixa confiança aparente.

Comparações:
- R001 (complements): MemGPT é a proposta concreta que introduz e demonstra esse desenho de gerência virtual de contexto.
- T078 (complements): Semantic Page Fault nomeia uma analogia para dependência ausente, cuja detecção não é garantida pelo modelo.

Afirmação rastreável:
MemGPT propõe virtual context management com diferentes níveis de memória e interrupções para controle de fluxo.
Suporte: direct; fontes: A-S009
Limite: O artigo demonstra tarefas específicas; a analogia não garante memória ilimitada efetiva nem detecção perfeita de informação ausente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T063:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou limites da analogia com sistema operacional. Aqui contexto virtual usa prefetch condicionado e detecção de thrashing semântico.

Projeto e decomposição
Antecipe carregamento de dependências explícitas do próximo passo, como schema ou definição citada. Prefetch especulativo amplo pode ocupar a janela antes de saber o que será útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Controle adaptativo
Detecte alternância repetida entre blocos que se expulsam mutuamente. A solução pode ser decompor a tarefa ou fixar conjunto mínimo, não apenas aumentar frequência de recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Validação contrafactual
Compare carga sob demanda e prefetch limitado. Meça acertos de antecipação, conteúdo carregado sem uso e ciclos de recarga; falta semântica continua inferida, não falha de endereço exata. Unidade de avaliação: sequência de cargas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Execução de procedimento
Cenário: Próxima etapa tem dependências conhecidas.
Estratégia: Carregar schema e parâmetros antes da etapa, mantendo evidência da atual até confirmar conclusão. Liberar conjunto anterior pela transição.
Papel do modelo pequeno: 3–7B executa etapa delimitada.
Aceite proposto: Não expulsar condição necessária antes de concluir ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Comparação de arquivos grandes
Cenário: Leitor alterna continuamente entre versões.
Estratégia: Construir quadro de diferenças com referências e carregar pares correspondentes, evitando reler arquivos completos.
Papel do modelo pequeno: 8–14B compara pares.
Aceite proposto: Reduzir recargas sem perder diferenças relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de blocos pequenos selecionados por controlador explícito.
8–14B: Gerente de comparação local com prefetch de dependências.
15–30B: Planejador que reorganiza tarefa quando conjunto de trabalho não cabe.
Requisitos de treino/runtime: Mapa de residência, referências versionadas e telemetria de cargas; nenhum aumento físico da janela é presumido.
Não aplicar quando: Conjunto indispensável excede orçamento e não pode ser dividido sem perder relações essenciais.

## T063:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa avalia gestão de contexto virtual em documentos e conversas.
Mecanismo documentado: Ferramentas movimentam informação entre janela e armazenamento externo.
Correspondência com esta base: Virtual context management é o mecanismo estudado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.
Limite: Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T063:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T063 → T078 [requires]
Como combinar: Representar falta específica que precisa de carga.
Interface: Requisito ausente, referência e decisão bloqueada.
Condição: Falta ter critério de resolução verificável.
Aceite proposto: Carregar trecho parecido e manter falta aberta se não responder.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T063 → T218 [complements]
Como combinar: Detectar thrashing de blocos sem avanço.
Interface: Histórico de cargas, descarte e progresso.
Condição: Repetição ser medida por identidade e revisão.
Aceite proposto: Forçar alternância A/B e exigir replanejamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir paginação de texto com KV cache do modelo.
- Não prometer memória ilimitada disponível em uma chamada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas maiores que a janela com igual custo total; paginação útil depende da política de seleção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T062, T067, T078, R001

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T064 — Persistent Agent State

**Nome canônico:** Persistent Agent State  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T064  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** estado persistente de agente

## T064:C01 — conceito

Estado de execução do agente que sobrevive a chamadas, sessões e reinícios: missão, etapa, valores intermediários, ações pendentes e referências. É distinto de conhecimento geral do agente. Persistir texto de conversa sem controle de execução pode ser insuficiente para retomar corretamente.

Como funciona:
- Modelar os campos necessários à próxima transição.
- Gravar mudanças confirmadas com identidade e versão.
- Recarregar e reconciliar o estado antes de continuar.

## T064:C02 — aplicacao

Quando usar:
- Missões duráveis e workflows com ferramentas.
- Retomada após crash, pausa ou troca de modelo.

Quando não usar:
- Não guardar segredos ou objetos de conexão diretamente em snapshots se bastam referências seguras.

Implementação proposta:
- Proposta: persistir campos serializáveis e migráveis.
- Separar sessão do usuário, missão e tentativa de execução.
- Registrar estado de cada efeito externo para não confundir planejado, iniciado e confirmado.

Aplicação LAI proposta:
Proposta LAI: a Helena deve reabrir o estado da missão antes de agir; prompts novos não devem recriar o progresso a partir de suposições.

## T064:C03 — riscos_validacao

Armadilhas:
- Estado persistido pode apontar a artefatos temporários já desaparecidos.
- Atualizações parciais podem combinar etapas incompatíveis.

Métricas sugeridas:
- Taxa de retomada sem perda ou duplicação.
- Falhas de migração e referências inválidas.

Testes propostos:
- Reiniciar processo em cada transição de um workflow e conferir continuidade.
- Mudar schema de estado e testar migração de um snapshot antigo.

## T064:C04 — perguntas_proveniencia

Pergunta: Estado persistente significa memória de longo prazo?
Resposta: É uma forma de persistência operacional. Memória de conhecimento tem finalidade e política de recuperação diferentes.

Pergunta: Salvar após a resposta final basta?
Resposta: Não para missões longas. Falhas podem ocorrer antes; pontos críticos precisam de confirmação durante a execução.

Pergunta: O estado deve guardar credenciais diretamente?
Resposta: Prefira referências a mecanismos apropriados de resolução. A persistência precisa permitir renovar acesso sem transformar um segredo expirado em dependência irrecuperável.

Pergunta: Posso identificar execução apenas pelo usuário?
Resposta: Não quando há missões ou tentativas simultâneas. Identifique proprietário, missão, thread e tentativa conforme as unidades reais de concorrência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T064:C05 — mecanismo_avancado

Persistir estado exige distinguir valores reconstruíveis de recursos efêmeros: um caminho, socket ou objeto cliente não equivale ao recurso que representa. O estado também precisa identificar código e schema capazes de interpretá-lo após atualização. Uma retomada pode restaurar dados perfeitamente e ainda executar uma transição diferente porque o programa mudou. Migrações e verificação de dependências pertencem ao contrato de persistência, além da serialização.

Condição de contorno:
O estado deixa de ser retomável quando contém referências sem duração compatível, segredos expirados ou versões que o novo runtime não sabe interpretar.

Contrato proposto:
- Entradas: Campos serializáveis, referências duráveis, identidade de execução e versão de schema ou workflow.
- Saídas: Estado confirmado e carregável com dependências verificadas ou bloqueios de migração explícitos.
- Estado: Histórico de revisões, migrações aplicadas, agenda e operações externas pendentes.
- Invariante: Carregar bytes válidos não é declarado como retomada bem-sucedida antes de verificar compatibilidade e dependências.

Compromissos de projeto:
- Persistir informação mínima reduz custo e pode aumentar reconstrução após falha.
- Persistir intermediários acelera retomada e torna migração mais difícil quando mudam tipos e contratos de ferramentas.

## T064:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reiniciar com nova versão do workflow e remover um artefato referenciado. O carregamento deve detectar ambos os problemas e não marcar a missão como pronta apenas porque o JSON foi lido.

Plano de avaliação proposto:
Avaliação proposta: comparar retomada na mesma versão e após migração com falhas de dependência. Medir estados recuperáveis, tempo de reconstrução, transições inválidas e perdas de artefatos; testar também separação entre threads de um mesmo usuário.

Comparações:
- T047 (distinct_from): Memória longa conserva conhecimento reutilizável; estado persistente determina continuidade de uma execução identificada.
- T060 (complements): Checkpoint publica um ponto específico do estado com semântica de retomada.

Afirmação rastreável:
LangGraph separa estado de thread preservado por checkpointers de dados compartilháveis mantidos em stores.
Suporte: direct; fontes: V3A-S031, V3A-S032
Limite: Essa separação não fornece automaticamente migração de qualquer schema customizado ou durabilidade de arquivos externos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T064:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu serialização e migração. Aqui estado persistente inclui fronteiras de portabilidade e prova de restauração em ambiente novo.

Projeto e decomposição
Separe estado lógico da tarefa e conexões ao ambiente. Tokens de sessão, descritores de arquivo e clientes de API devem ser reconstruídos, não tratados como objetos duráveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

Controle adaptativo
Manifesto de restauração declara recursos necessários e quais podem ser substituídos. Trocar modelo ou ferramenta pode exigir revalidação do plano, mesmo quando dados persistidos continuam legíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

Validação contrafactual
Compare reinício no mesmo processo, processo novo e ambiente novo. Meça recursos ausentes, decisões indevidamente preservadas e retomada correta; gravar JSON não prova portabilidade. Unidade de avaliação: estado restaurável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

USO AVANÇADO — Migração de executor
Cenário: Tarefa sai de uma máquina para outra.
Estratégia: Restaurar dados e artefatos, reabrir conexões e verificar versões antes de liberar próxima etapa.
Papel do modelo pequeno: 3–7B interpreta estado; código valida recursos.
Aceite proposto: Nenhuma referência efêmera deve ser aceita como recurso disponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

USO AVANÇADO — Troca de modelo
Cenário: Modelo local substitui provedor remoto.
Estratégia: Manter fatos e progresso, reconstruir contexto no template do novo modelo e validar comportamento em etapa reversível.
Papel do modelo pequeno: 8–14B retoma contrato explícito.
Aceite proposto: Não assumir compatibilidade de prompt, tokenizer ou ferramenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de tarefa estreita a partir de estado estruturado completo.
8–14B: Leitor de estado restaurado que identifica lacunas e incompatibilidades.
15–30B: Replanejador quando recursos ou capacidade do consumidor mudarem.
Requisitos de treino/runtime: Schema versionado, referências duráveis e verificação de dependências; persistência externa não modifica pesos.
Não aplicar quando: O estado depende de recursos que desapareceram e não há procedimento de reconstrução.

## T064:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C005 — Google / Megastore em serviços interativos
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores relatam serviços Google em produção sobre Megastore.
Mecanismo documentado: Partições recebem semântica ACID serializável e replicação síncrona.
Correspondência com esta base: Estado durável de serviços, não estado completo de um agente LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher agregado transacional por sessão/projeto e manter decisões do LLM como propostas.
Limite: A atomicidade não atravessa automaticamente partições e APIs externas; relato de 2011. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S004.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Estado de processamento é durável; não define serialização de um agente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

V4A-C027 — Letta / Framework de agentes stateful
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.
Mecanismo documentado: Persistência do agente e ferramentas de memória externas ao modelo.
Correspondência com esta base: Estado persistente de agentes é recurso explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.
Limite: Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S026, V2B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q023.

## T064:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T064 → T060 [complements]
Como combinar: Vincular estado à fronteira executável de retomada.
Interface: Estado, etapa, revisão e operações pendentes.
Condição: Checkpoint preservar contexto de continuidade.
Aceite proposto: Restaurar estado sem cursor e exigir diagnóstico de incompletude.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V3A-S032, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T064 → T066 [requires]
Como combinar: Resolver recursos após restauração.
Interface: Referências, versões e status de disponibilidade.
Condição: Resolver respeitar ambiente e escopo atuais.
Aceite proposto: Testar recurso removido e impedir uso presumido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V3A-S032, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não persistir segredo efêmero como memória reutilizável.
- Não confundir estado legível com plano ainda válido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retomada entre ambientes; capacidade do modelo não substitui recursos e contratos ausentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T040, T053, T059, T060, T065

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S031 — LangGraph Checkpointers

[https://docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints por super-step, StateSnapshot e pending writes de tarefas concluídas; estado de execução e retomada.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

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

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services

[https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transações serializáveis em partições e experiência com serviços Google em produção.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T065 — Transactional State Manager

**Nome canônico:** Transactional State Manager  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T065  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gerenciador transacional de estado

## T065:C01 — conceito

Componente que atualiza estado e registros relacionados com garantias de atomicidade e isolamento adequadas. Evita que duas etapas concorrentes confirmem estados incompatíveis. O termo descreve uma responsabilidade de runtime, não uma tecnologia específica de LLM.

Como funciona:
- Ler estado e versão com semântica de concorrência definida.
- Validar pré-condições e aplicar mudanças em transação.
- Confirmar ou rejeitar integralmente a atualização e registrar o resultado.

## T065:C02 — aplicacao

Quando usar:
- Vários trabalhadores operam sobre uma missão.
- Estado, eventos e filas precisam permanecer coerentes.

Quando não usar:
- Não presumir que uma transação local engloba automaticamente APIs externas ou mensagens já enviadas.

Implementação proposta:
- Proposta: usar versão esperada e comparação na atualização.
- Definir política de retry para conflitos sem repetir efeitos não idempotentes.
- Para comunicação externa, considerar outbox e reconciliação em vez de alegar transação distribuída inexistente.

Aplicação LAI proposta:
Proposta LAI: proteger estado da Helena por um escritor controlado ou versionamento otimista, mantendo especialistas consultivos sem sobrescrita livre.

## T065:C03 — riscos_validacao

Armadilhas:
- Nível de isolamento inadequado permite anomalias de concorrência.
- Repetir transação após erro pode duplicar ações fora do banco.

Métricas sugeridas:
- Conflitos detectados, atualizações perdidas e abortos.
- Invariantes violados e tempo de contenção.

Testes propostos:
- Dois processos tentam concluir a mesma etapa a partir da mesma versão; apenas atualização válida deve vencer.
- Falhar entre estado e evento e exigir commit de ambos ou de nenhum.

## T065:C04 — perguntas_proveniencia

Pergunta: Um arquivo JSON comum é transacional?
Resposta: Não por si só. É necessário projetar gravação atômica, concorrência e recuperação.

Pergunta: Serializable elimina toda necessidade de retry?
Resposta: Não. Sistemas podem abortar transações para manter isolamento, e o cliente precisa tratar isso corretamente.

Pergunta: Compare-and-swap resolve todas as invariantes?
Resposta: Não. Protege uma condição de versão definida; regras envolvendo várias entidades podem exigir outra coordenação ou isolamento.

Pergunta: Uma LLM deve permanecer dentro de uma transação longa?
Resposta: É uma escolha de arquitetura com custo de contenção. Pode ser preferível gerar fora e validar versão e pré-condições ao aplicar o resultado.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T065:C05 — mecanismo_avancado

Atomicidade e isolamento resolvem problemas diferentes: gravar vários campos juntos evita atualização parcial, mas transações concorrentes ainda podem violar regras se o nível de isolamento for insuficiente. Em PostgreSQL, falhas de serialização exigem repetir a transação inteira com nova leitura. Reutilizar uma decisão calculada antes do conflito pode reaplicar pressupostos que já não valem, mesmo que a nova escrita seja aceita.

Condição de contorno:
A transação do banco não inclui automaticamente inferência remota, arquivos externos ou publicação em outro serviço; a garantia termina no seu domínio de coordenação.

Contrato proposto:
- Entradas: Comando, versão esperada, pré-condições de domínio e registros que devem mudar conjuntamente.
- Saídas: Estado confirmado e intenções de publicação persistidas, ou conflito sem avanço parcial.
- Estado: Revisões, chaves de operação, outbox e política limitada de repetição por conflito.
- Invariante: Uma decisão abortada não produz efeito externo irreversível apenas porque foi calculada dentro do bloco transacional.

Compromissos de projeto:
- Isolamento mais forte simplifica certas invariantes e pode aumentar abortos e repetição.
- Outbox evita perda da intenção junto do estado, mas admite entrega repetida e exige consumidores compatíveis.

## T065:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: duas transações leem a mesma condição e tentam consumir a última capacidade. Uma delas deve falhar ou ser reavaliada; repetir não pode enviar duas notificações equivalentes ao mesmo destinatário.

Plano de avaliação proposto:
Avaliação proposta: comparar atualização simples, versão esperada e isolamento adequado sob concorrência controlada. Medir invariantes violadas, abortos, custo de repetição e publicações duplicadas; simular queda entre persistir outbox e confirmar entrega.

Comparações:
- T060 (complements): Um checkpoint transacional pode usar o gerenciador para publicar estado e posição de execução de forma coerente.
- T075 (complements): Reconciliação trata divergências e confirmações externas que continuam fora da atomicidade local.

Afirmação rastreável:
PostgreSQL documenta repetição integral após falhas de serialização; o padrão outbox da AWS reconhece possibilidade de mensagens duplicadas.
Suporte: direct; fontes: A-S029, V2C-S001
Limite: Essas garantias não equivalem a uma transação distribuída universal nem a efeitos externos executados exatamente uma vez.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T065:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou atomicidade e isolamento. Aqui transações protegem propostas semânticas calculadas fora do banco contra estado obsoleto.

Projeto e decomposição
O modelo lê snapshot e produz proposta com pré-condições. A transação verifica versões e invariantes antes de escrever; executar inferência longa segurando locks aumenta contenção sem melhorar verdade da proposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V4A-S003, V4A-S004.

Controle adaptativo
Quando o estado mudar, diferencie conflito irrelevante e conflito que invalida raciocínio. Reaplicar cegamente o mesmo texto após retry pode confirmar conclusão baseada em dados antigos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V4A-S003, V4A-S004.

Validação contrafactual
Compare confirmação por última escrita e por pré-condições semânticas explícitas. Meça atualizações perdidas, retries e propostas aceitas com base obsoleta; isolar tempo de inferência do tempo de transação. Unidade de avaliação: proposta de atualização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V4A-S003, V4A-S004.

USO AVANÇADO — Atualização de memória compartilhada
Cenário: Dois agentes corrigem a mesma decisão.
Estratégia: Cada proposta inclui versão observada e afirmações afetadas; commit rejeita conflito e solicita nova leitura antes de reconciliar.
Papel do modelo pequeno: 3–7B extrai alteração; 8–14B reconcilia.
Aceite proposto: Nenhuma proposta obsoleta pode apagar correção mais recente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V4A-S003, V4A-S004.

USO AVANÇADO — Planejamento com recursos limitados
Cenário: Agentes disputam cota ou tarefa.
Estratégia: Selecionar intenção fora da transação, reservar recurso atomicamente e somente depois iniciar execução autorizada.
Papel do modelo pequeno: 15–30B planeja; código reserva.
Aceite proposto: Uma tarefa não pode receber duas reservas incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S029, V4A-S003, V4A-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de atualização tipada com campos e revisão esperada.
8–14B: Reconciliador local após conflito, sem controlar locks.
15–30B: Planejador de operações cujo commit continua determinístico.
Requisitos de treino/runtime: Banco com isolamento adequado, invariantes executáveis e identificadores de operação; transação local não cobre APIs externas.
Não aplicar quando: A operação exige atomicidade entre serviços sem protocolo apropriado ou inferência fica dentro de lock prolongado.

## T065:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 3. Lacuna: 7. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C004 — Google / Percolator no índice web
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo afirma implantação do processamento incremental na construção do índice da busca Google.
Mecanismo documentado: Transações distribuídas e notificações organizam pequenas atualizações.
Correspondência com esta base: Confirma gerenciamento transacional de alterações; adaptação para agentes é adicional.
Transferência proposta para modelo pequeno: Proposta de engenharia: Delegar extração a 3–7B e confirmar alterações por transações determinísticas.
Limite: Relato histórico; não prova event sourcing, checkpoints de agentes ou resumo incremental correto. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S003.

V4A-C005 — Google / Megastore em serviços interativos
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores relatam serviços Google em produção sobre Megastore.
Mecanismo documentado: Partições recebem semântica ACID serializável e replicação síncrona.
Correspondência com esta base: Transações serializáveis delimitadas por partição.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher agregado transacional por sessão/projeto e manter decisões do LLM como propostas.
Limite: A atomicidade não atravessa automaticamente partições e APIs externas; relato de 2011. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S004.

V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Operador descreve migração real de todos os metadados e listagem fortemente consistente.
Mecanismo documentado: Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.
Correspondência com esta base: Uso operacional de banco transacional consistente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.
Limite: Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S007, V4A-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q006.

## T065:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T065 → T075 [complements]
Como combinar: Reconciliar proposta rejeitada após nova leitura.
Interface: Proposta, revisão antiga, estado atual e motivo do conflito.
Condição: Reconciliador preservar mudanças concorrentes válidas.
Aceite proposto: Simular correções independentes e uma correção incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S029, V4A-S003, V4A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T065 → T162 [requires]
Como combinar: Associar confirmação à identidade estável da operação.
Interface: operation_id e resultado confirmado.
Condição: Retry não criar nova intenção.
Aceite proposto: Repetir mesma solicitação e verificar único efeito lógico.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S029, V4A-S003, V4A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar commit bem-sucedido como prova de verdade semântica.
- Não repetir chamada externa dentro de retry transacional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar propostas corretas confirmadas sob concorrência; o banco protege invariantes, não substitui julgamento sobre evidência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T064, T162

## Fontes primárias associadas

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S001 — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gravação de estado e evento de outbox na mesma transação; publicação posterior; duplicatas exigem consumidores idempotentes.

Limite: Fundamenta princípios de consistência. Não prova implementação, exatamente-uma-vez ponta a ponta ou resultado de desempenho na LAI.

### V4A-S003 — Large-scale Incremental Processing Using Distributed Transactions and Notifications

[https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Percolator implantado no índice web; processamento incremental com transações.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services

[https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transações serializáveis em partições e experiência com serviços Google em produção.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S005 — Spanner: Google's Globally-Distributed Database

[https://research.google/pubs/spanner-googles-globally-distributed-database-2/](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco multiversão, transações externamente consistentes e incerteza temporal.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency

[https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração efetiva dos metadados do Cloud Storage para Spanner e consistência de listagem.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T066 — Memory Resolver / Reference Resolver

**Nome canônico:** Memory Resolver / Reference Resolver  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T066  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** resolvedor de memória; resolvedor de referências

## T066:C01 — conceito

Resolve um identificador de memória ou artefato para a versão e o conteúdo corretos. Centraliza validação de acesso, integridade, existência e leitura parcial. Não deve interpretar um caminho recebido como autorização para acessar qualquer arquivo.

Como funciona:
- Receber referência com escopo e versão.
- Verificar autorização e localizar o objeto.
- Entregar conteúdo ou intervalo com metadados de completude.

## T066:C02 — aplicacao

Quando usar:
- Arquiteturas que passam referências entre agentes.
- Memórias externas em múltiplos armazenamentos.

Quando não usar:
- Não aceitar URLs ou caminhos arbitrários sem regras de resolução e escopo.

Implementação proposta:
- Proposta: definir formato de ID e schema de resposta.
- Distinguir not_found, forbidden, stale_version e partial.
- Validar hash quando exigido e retornar meios de continuar leitura de um objeto grande.

Aplicação LAI proposta:
Proposta LAI: construir um resolvedor comum para evidências e estado da Helena, usando referências estáveis em relatórios e checkpoints.

## T066:C03 — riscos_validacao

Armadilhas:
- Um alias como latest pode mudar entre etapas.
- Erro genérico pode ser confundido com memória inexistente, induzindo recriação indevida.

Métricas sugeridas:
- Referências resolvidas na versão pedida.
- Tempo de resolução e taxa de conteúdo parcial mal interpretado.

Testes propostos:
- Tentar resolver ID de outro namespace e exigir rejeição.
- Pedir versão antiga existente e retornar exatamente aquela versão ou erro explícito.

## T066:C04 — perguntas_proveniencia

Pergunta: O resolvedor também decide relevância?
Resposta: Pode integrar-se à busca, mas sua função principal é obter o objeto exato pedido com garantias de identidade e acesso.

Pergunta: Posso retornar só texto?
Resposta: Metadados de versão, origem e completude ajudam a evitar interpretações incorretas e devem acompanhar o texto.

Pergunta: Um recurso encontrado já foi lido?
Resposta: Não. Descoberta fornece metadados ou referência. A resposta deve distinguir recurso listado, conteúdo aberto e conteúdo parcialmente consumido.

Pergunta: Posso recuperar por similaridade após not_found?
Resposta: Pode iniciar outra busca, mas devolva candidatos como alternativas. Não finja que um registro parecido é a versão exata que estava referenciada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T066:C05 — mecanismo_avancado

Resolver uma memória envolve transformar um nome lógico em uma versão concreta e depois obter seus bytes. Essas etapas podem observar estados diferentes se o alias mudar entre consultas. Uma resolução reproduzível devolve a versão efetiva junto do conteúdo e mantém leituras parciais ancoradas nela. Busca semântica pode sugerir outro registro quando a referência falha, mas não deve substituir silenciosamente a identidade originalmente solicitada.

Condição de contorno:
O resolvedor não consegue garantir disponibilidade de objetos apagados ou comprovar autoria apenas por encontrar bytes cujo hash corresponde ao identificador.

Contrato proposto:
- Entradas: Referência, versão ou política de alias, escopo de acesso e faixa de leitura desejada.
- Saídas: Conteúdo identificado, versão efetiva, integridade verificável e status explícito de completude.
- Estado: Mapeamento de aliases, revisões de acesso, referências já resolvidas e cursores vinculados à versão.
- Invariante: Todas as partes de uma leitura compõem a mesma revisão, salvo solicitação explícita de atualização.

Compromissos de projeto:
- Fixar versão favorece reprodução e pode impedir acesso à informação mais recente.
- Resolver aliases automaticamente simplifica uso e exige tornar visível a revisão realmente consultada.

## T066:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar latest entre duas páginas de leitura. O resolvedor deve manter o objeto original ou invalidar o cursor, evitando entregar um documento composto de versões diferentes.

Plano de avaliação proposto:
Avaliação proposta: comparar referências versionadas e aliases mutáveis sob atualizações concorrentes. Medir leituras mistas, erros corretamente classificados, latência e recuperação de conteúdo; testar ausência, acesso negado e corrupção como estados distintos.

Comparações:
- T015 (complements): O uso de referências depende de um componente que consiga materializar conteúdo com identidade e escopo conhecidos.
- T061 (complements): Endereçamento por conteúdo oferece verificação de identidade para objetos resolvidos, sem garantir disponibilidade.

Afirmação rastreável:
MCP Resources define recursos identificados por URI e operações de leitura; IPFS distingue identificação por conteúdo de localização.
Suporte: related; fontes: V3A-S019, V3A-S038
Limite: Imutabilidade de versão, autorização e cursores consistentes são contratos adicionais da implementação proposta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T066:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu resolução pinada. Aqui referências são resolvidas em duas fases para distinguir identidade, disponibilidade e conteúdo efetivamente lido.

Projeto e decomposição
Primeiro resolver identidade e versão; depois abrir o recorte e verificar integridade. Um recurso encontrado pode estar indisponível, parcial ou exigir conversão que altera offsets.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

Controle adaptativo
Use alias apenas para descoberta. Ao iniciar tarefa dependente, fixe revisão e registre atualização detectada; seguir alias latest silenciosamente pode misturar evidências de momentos diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

Validação contrafactual
Compare resolução direta e fallback semântico em referências quebradas. Meça substituições indevidas, falsos sucessos e tempo de recuperação; fallback deve retornar candidato, não fingir identidade exata. Unidade de avaliação: resolução de referência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

USO AVANÇADO — Handoff entre agentes
Cenário: Referências viajam sem conteúdo integral.
Estratégia: Resolver cada artefato, verificar recortes e construir lista de faltas antes de aceitar tarefa. Pedir substituição explícita quando origem sumiu.
Papel do modelo pequeno: 3–7B interpreta manifesto.
Aceite proposto: Nenhuma referência ausente pode aparecer como evidência lida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

USO AVANÇADO — Documentação renomeada
Cenário: Caminhos mudam entre versões.
Estratégia: Usar mapa de renomeação e digest para confirmar continuidade; se conteúdo divergir, tratar como nova versão e reavaliar conclusão.
Papel do modelo pequeno: 8–14B compara significado.
Aceite proposto: Alias novo não pode ocultar alteração material.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de referências estruturadas com erro tipado.
8–14B: Revisor de candidatos de substituição e diferenças locais.
15–30B: Integrador de evidências quando múltiplas resoluções produzem versões incompatíveis.
Requisitos de treino/runtime: Registry de aliases, versões e estados de abertura; integridade e autorização são verificações distintas.
Não aplicar quando: Identidade só pode ser aproximada e a tarefa exige documento exato.

## T066:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C013 — Google / Knowledge Graph na busca Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Anúncio relata início da implantação a usuários da busca.
Mecanismo documentado: Entidades e relações permitem desambiguação e apresentação de fatos relacionados.
Correspondência com esta base: Desambiguação de entidades inspira resolução, sem contrato de versão desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.
Limite: Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q019.

## T066:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T066 → T015 [requires]
Como combinar: Receber referência com seletor e revisão.
Interface: URI, versão, intervalo e tipo esperado.
Condição: Produtor declarar se conteúdo foi realmente aberto.
Aceite proposto: Testar referência correta com seletor inválido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V3A-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T066 → T072 [feeds]
Como combinar: Fixar conjunto resolvido numa revisão de trabalho.
Interface: Manifesto de recursos e revisões observadas.
Condição: Tarefa não misturar latest de momentos diferentes.
Aceite proposto: Atualizar alias durante carga e detectar incompatibilidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V3A-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir nome parecido com mesmo objeto.
- Não apresentar resultado parcial como abertura integral.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar integridade de citações e custo de resolução; modelo maior não torna alias ambíguo uma identidade comprovada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T053, T061, T067

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S018 — Introducing the Knowledge Graph: things, not strings

[https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação gradual de entidades e relações na busca Google; não é GraphRAG moderno.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# T068 — Memory-Augmented Generation

**Nome canônico:** Memory-Augmented Generation  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T068  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** geração aumentada por memória; MAG

## T068:C01 — conceito

Família de geração apoiada por memória externa ou componentes de memória específicos. Pode usar texto recuperado por ferramentas ou arquiteturas treinadas para ler representações armazenadas, como LongMem. O nome precisa vir acompanhado da forma de memória e da interface de leitura.

Como funciona:
- Persistir informação em representação adequada.
- Selecionar memória relevante durante a tarefa.
- Condicionar a geração ao conteúdo ou estado recuperado.

## T068:C02 — aplicacao

Quando usar:
- Tarefas que exigem histórico maior que o contexto ativo.
- Reutilização de experiências e conhecimento entre sessões.

Quando não usar:
- Não presumir que qualquer modelo aceita diretamente estados de memória de outra arquitetura.

Implementação proposta:
- Proposta: começar por memória textual com proveniência e ferramentas claras.
- Separar escrita, consolidação e leitura em componentes observáveis.
- Se experimentar memória integrada ao modelo, verificar treinamento, versões e custo adicional.

Aplicação LAI proposta:
Proposta LAI: combinar memória externa auditável e geração pelo modelo configurado; LongMem é referência de pesquisa, não um recurso automaticamente habilitado no Qwen.

## T068:C03 — riscos_validacao

Armadilhas:
- Memória antiga pode ser incompatível com fatos atuais.
- Falhas de recuperação podem parecer falhas de raciocínio e dificultar diagnóstico.

Métricas sugeridas:
- Qualidade com memória correta, irrelevante e ausente.
- Recall, latência e custo total de manutenção da memória.

Testes propostos:
- Comparar o mesmo problema com e sem um episódio relevante.
- Injetar uma memória contraditória com fonte fraca e exigir tratamento de conflito.

## T068:C04 — perguntas_proveniencia

Pergunta: Memory-Augmented Generation é sempre RAG?
Resposta: Há sobreposição, mas arquiteturas com memória integrada podem operar de forma diferente de um pipeline textual de RAG.

Pergunta: Sempre exige treinamento?
Resposta: Não. Memória via ferramentas pode ser engenharia de runtime; arquiteturas especializadas podem exigir adaptação do modelo.

Pergunta: Uma resposta melhor prova que a memória foi usada?
Resposta: Não. Faça ablações com memória removida, trocada ou corrigida e observe o comportamento. Acerto isolado pode vir do conhecimento paramétrico.

Pergunta: Como evitar que o gerador ignore correções recuperadas?
Resposta: Inclua status e versões, teste conflitos entre conhecimento anterior e evidência atual e avalie se a resposta respeita o escopo atualizado.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T068:C05 — mecanismo_avancado

O ponto de integração da memória muda o experimento. Recuperar texto adiciona tokens a um gerador comum; recuperar estados neurais exige componentes capazes de lê-los. Em LongMem, o backbone congelado codifica memória e uma rede lateral adaptativa aprende recuperação e leitura. Avaliar essas opções exige contabilizar treinamento e construção da memória, além da latência de consulta, sem tratar ambas como simples troca de banco vetorial.

Condição de contorno:
Uma memória neural não pode ser conectada a qualquer modelo apenas porque ele aceita texto, e memória textual não corrige um recuperador incapaz de encontrar a evidência.

Contrato proposto:
- Entradas: Memória identificada, consulta ou estado gerador e interface de leitura explicitamente definida.
- Saídas: Resposta condicionada e registro das memórias efetivamente fornecidas ao componente leitor.
- Estado: Versões do escritor, índice, representação, leitor e políticas de atualização.
- Invariante: A avaliação separa erro de recuperação, incompatibilidade de representação e interpretação incorreta pelo gerador.

Compromissos de projeto:
- Texto recuperado facilita auditoria e consome espaço na janela.
- Representações especializadas podem reduzir esse consumo aparente e acrescentam dependências de arquitetura, treinamento e reconstrução do índice.

## T068:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar a representação da memória sem atualizar seu leitor. O sistema deve detectar incompatibilidade ou a avaliação revelar degradação, mesmo que a busca retorne candidatos com pontuação alta.

Plano de avaliação proposto:
Avaliação proposta: comparar ausência de memória, memória textual e interface neural somente em condições compatíveis. Medir sustentação, recuperação, custo de construção, latência e atualização; reporte separadamente treinamento amortizado e custo por consulta.

Comparações:
- T047 (complements): Memória longa define persistência e escopo; geração aumentada especifica como essa informação influencia a saída.
- T052 (complements): Interfaces latentes são uma forma de representação possível, cuja interpretação precisa de consumidor compatível.

Afirmação rastreável:
LongMem separa backbone congelado como codificador de uma rede lateral adaptativa para recuperar e ler memória.
Suporte: direct; fontes: A-S013
Limite: O mecanismo é arquitetural e treinado; o artigo não demonstra compatibilidade direta com APIs arbitrárias de modelos fechados.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T068:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou memória textual e neural. Aqui o uso da memória é testado por intervenção para distinguir acesso de influência real.

Projeto e decomposição
Encontrar e inserir memória não prova que o gerador a utilizou. Compare resposta com memória correta, removida e trocada por versão incompatível, mantendo pergunta igual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

Controle adaptativo
Defina política para conflito entre memória e conhecimento paramétrico. Para tarefas sobre documentos privados, o modelo deve citar a evidência fornecida e sinalizar conflito, não substituir silenciosamente por lembrança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

Validação contrafactual
Meça fidelidade, sensibilidade à troca e abstenção quando memória fica insuficiente. Separar falha de recuperação, falha de leitura e adesão indevida a fonte errada evita atribuição enganosa de ganho. Unidade de avaliação: resposta condicionada à memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

USO AVANÇADO — Assistente de produto privado
Cenário: Fatos não aparecem no pré-treino.
Estratégia: Recuperar documentação versionada, exigir suporte por afirmação e testar nomes fictícios controlados que impedem acerto por familiaridade.
Papel do modelo pequeno: 8–14B leitor especializado.
Aceite proposto: Resposta deve acompanhar mudança documentada do atributo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

USO AVANÇADO — Memória neural experimental
Cenário: Modelo aberto lê estados externos.
Estratégia: Instrumentar contribuição da memória e comparar com RAG textual sob recursos equivalentes; não avaliar apenas perda de linguagem.
Papel do modelo pequeno: 15–30B consumidor treinável.
Aceite proposto: Memória errada deve ser detectável na avaliação, sem ocultar dependência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor extrativo de texto recuperado com citações e campos ausentes.
8–14B: Leitor contextual especializado para integrar poucas memórias conflitantes.
15–30B: Consumidor neural ou integrador complexo quando houver treino e instrumentação.
Requisitos de treino/runtime: Interface de memória definida, versão do consumidor e testes contrafactuais próprios; texto e tensores exigem contratos distintos.
Não aplicar quando: O consumidor ignora memória ou segue conteúdo irrelevante sem capacidade de abster.

## T068:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo e código estudam memória neural recuperável para contexto extenso.
Mecanismo documentado: Representações em memória e módulo adaptado de leitura são componentes treinados.
Correspondência com esta base: Geração aumentada por memória neural.
Transferência proposta para modelo pequeno: Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.
Limite: Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S013, V3A-S047.

V4A-C021 — Google DeepMind / DataGemma RIG/RAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto publica variantes para fundamentar geração em Data Commons.
Mecanismo documentado: RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.
Correspondência com esta base: Geração é aumentada por dados externos.
Transferência proposta para modelo pequeno: Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.
Limite: RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S014.

V4A-C022 — Salesforce / SFR-RAG 9B
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa apresenta modelo de nove bilhões especializado em fidelidade contextual.
Mecanismo documentado: Pós-treino privilegia leitura de evidência, citações e reconhecimento de insuficiência.
Correspondência com esta base: Uso de memória textual externa; não arquitetura neural LongMem.
Transferência proposta para modelo pequeno: Proposta de engenharia: Considerar leitor 8–14B especializado e comparar com modelo geral do mesmo porte.
Limite: Resultados experimentais publicados não garantem produção nem superioridade universal; nenhuma pergunta de benchmark foi incorporada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q010, V4A-Q016, V4A-Q018, V4A-Q020, V4A-Q023.

## T068:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T068 → T009 [complements]
Como combinar: Separar busca de evidência e leitura gerativa.
Interface: Consulta, documentos, referências e status de cobertura.
Condição: Memória textual elegível estar disponível.
Aceite proposto: Trocar evidência mantendo consulta e medir dependência correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S047, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T068 → T052 [requires]
Como combinar: Especificar interface quando memória for latente.
Interface: Encoder, estados, máscaras e versão.
Condição: Consumidor treinado para a representação.
Aceite proposto: Testar incompatibilidade após troca de checkpoint.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S047, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não atribuir ao componente memória acerto que ocorreria sem ele.
- Não tratar texto recuperado como autoridade de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar fidelidade com a mesma evidência; sucesso num domínio privado não demonstra paridade geral com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T047, T052, T062, R003

## Fontes primárias associadas

### A-S013 — Augmenting Language Models with Long-Term Memory

[https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: LongMem: backbone congelado como codificador e rede lateral treinada para recuperação e leitura.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S047 — LongMem External_Memory implementation

[https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco de chaves e valores por cabeça, indexação da média das chaves em chunks e recuperação dos estados dos chunks selecionados.

Limite: Leitura do código na branch main, sem execução. Detalhes representam esta implementação de pesquisa e não garantem compatibilidade com qualquer modelo ou ambiente.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T069 — Consolidação por resumos — anteriormente chamada de “Context Distillation”

**Nome canônico:** Consolidação por resumos  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T069  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Context Distillation como memória resumida; correção de context distillation; destilação não é resumo; memória resumida externa; consolidação textual sem treino

## T069:C01 — conceito

Consolidação por resumos transforma histórico extenso em memória textual menor, persistida fora dos pesos do modelo. O resumo é lido ou recuperado em chamadas futuras e continua sendo uma representação sujeita a perdas. O nome anterior “Context Distillation” é mantido para corrigir a terminologia; T069 tem identidade própria e não redireciona para T179.

Como funciona:
- Selecionar um intervalo de eventos e separar fatos, decisões vigentes, hipóteses e pendências.
- Produzir síntese com referências às evidências originais, preservando datas, responsáveis, negações e condições.
- Publicar nova versão do resumo e manter acesso ao histórico para verificar ou expandir afirmações.

Nota de nomenclatura: T069 não redireciona para T179.

## T069:C02 — aplicacao

Quando usar:
- Continuidade de sessões extensas, memória de projeto e redução de entrada repetida quando o histórico integral permanece consultável.

Quando não usar:
- Como prova literal de contrato, substituto de evidência original ou alegação de que o modelo aprendeu permanentemente.

Implementação proposta:
- Proposta: definir esquema de resumo com objetivo, estado atual, decisões, restrições e trabalho pendente; registrar event_range, source_ids, versão e data de consolidação.
- Gerar a atualização a partir de novas evidências e do resumo anterior, verificando itens alterados contra os originais; evitar cadeias ilimitadas de resumo de resumo.
- Preservar conflitos sem resolvê-los por omissão. Quando uma decisão mudar, registrar substituição e intervalo de vigência.
- Regerar a síntese a partir do histórico em marcos definidos, comparando perdas com um conjunto de fatos críticos conhecido.

Aplicação LAI proposta:
Proposta LAI: manter uma memória de projeto resumida, versionada e recuperável, com links aos eventos e confirmação explícita de que não houve treino de pesos.

## T069:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode converter hipótese em fato, apagar exceções ou perpetuar um erro de versões anteriores.
- Reduzir tokens sem medir preservação factual pode piorar a continuidade apesar do arquivo ficar menor.

Métricas sugeridas:
- Retenção de decisões e restrições, afirmações sem fonte, compressão em tokens e custo para recuperar detalhes omitidos.

Testes propostos:
- Teste proposto: resumir um histórico com decisão revogada, negação e pendência; conferir cada item com seus eventos de origem.
- Perguntar por um detalhe omitido e exigir expansão da fonte, sem reconstrução inventada.

## T069:C04 — perguntas_proveniencia

Pergunta: Qual a diferença operacional entre T069 e T179?
Resposta: T069 escreve e relê memória externa. T179 destila comportamento de contexto para parâmetros por treinamento; os artefatos e a avaliação são diferentes.

Pergunta: O resumo pode substituir definitivamente o histórico?
Resposta: Não como regra geral. A proposta conserva evidência original para auditoria, correção e recuperação de detalhes que a síntese perdeu.

Pergunta: Posso desfazer uma consolidação?
Resposta: Se mantiver originais e versões, pode substituir a síntese e reindexar derivados. Isso não desfaz respostas ou efeitos externos já produzidos.

Pergunta: O resumo precisa ser incluído em toda chamada?
Resposta: Somente quando relevante. Armazená-lo não altera o modelo; sua influência depende de leitura, recuperação ou outro caminho explícito de condicionamento.

Escopo das fontes:
Fontes distinguem sumarização externa e treino paramétrico; implementação e testes são propostos.

## T069:C05 — mecanismo_avancado

A consolidação por resumos mantém o conhecimento em um artefato externo que precisa entrar novamente no contexto para influenciar o modelo. Seu custo reaparece em leitura e atualização. Já a destilação paramétrica usa treinamento para internalizar comportamento condicionado a contexto. Essa distinção muda reversibilidade: editar ou trocar um resumo é uma operação de dados; corrigir comportamento internalizado exige outro processo e não oferece citação automática da origem.

Condição de contorno:
Uma sequência de resumos pode conservar coerência narrativa e perder detalhes raros; a qualidade percebida do texto não mede completude factual.

Contrato proposto:
- Entradas: Histórico delimitado, resumo anterior opcional, alterações recentes e fontes recuperáveis.
- Saídas: Síntese externa versionada com cobertura, fatos candidatos, decisões vigentes e lacunas.
- Estado: Origem dos fatos resumidos, revisões, substituições e critério de reconstrução a partir dos originais.
- Invariante: T069 permanece memória externa; nenhum resumo salvo é apresentado como mudança nos parâmetros do modelo.

Compromissos de projeto:
- Atualizar resumo incrementalmente economiza leitura do histórico e acumula dependência de decisões anteriores de seleção.
- Reconstruir do original reduz essa dependência e custa mais tokens e processamento.

## T069:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um detalhe raro, omiti-lo numa primeira síntese e depois formular uma tarefa que dependa dele. O sistema deve reabrir a origem ou declarar a lacuna, sem inventar o detalhe perdido.

Plano de avaliação proposto:
Avaliação proposta: comparar resumo incremental, recomputação integral e recuperação de trechos com orçamento semelhante. Medir fatos raros, correções, suporte e custo ao longo de ciclos; usar casos novos independentes dos exemplos usados para ajustar o resumidor.

Comparações:
- T179 (distinct_from): Destilação paramétrica altera pesos; este registro continua síntese textual externa lida em chamadas futuras.
- T058 (specializes): Resumir é uma forma de consolidação, enquanto consolidação também pode produzir relações ou procedimentos.

Afirmação rastreável:
Recursively Summarizing Enables Long-Term Dialogue Memory propõe atualizar memória por resumos; Learning by Distilling Context usa fine-tuning para internalizar ganhos do contexto.
Suporte: direct; fontes: V3A-S005, A-S040
Limite: Os trabalhos tratam mecanismos diferentes; o uso informal da palavra distillation não elimina essa diferença.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T069:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 corrigiu o nome para consolidação externa por resumos. Aqui o resumo é uma vista de consulta por finalidade, mantendo separação de T179.

Projeto e decomposição
Produza vistas diferentes para localizar informação, retomar tarefa e explicar decisão. Um único resumo universal tende a misturar detalhes irrelevantes e omitir condições úteis a um consumidor específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

Controle adaptativo
Considere o resumo como projeção reconstruível. Quando a finalidade mudar, gerar nova vista a partir das fontes; não empilhar resumos de finalidades diferentes até perder a ligação com origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

Validação contrafactual
Compare resumo único e vistas por finalidade. Meça decisões sustentadas, custo de reconstrução e dependência do texto original; nenhum desses processos atualiza pesos do modelo. Unidade de avaliação: vista resumida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

USO AVANÇADO — Retomada de projeto
Cenário: Equipe precisa estado operacional curto.
Estratégia: Gerar vista de pendências e decisões confirmadas, com referências para justificativas. Não incluir hipótese descartada como regra ativa.
Papel do modelo pequeno: 3–7B lê vista operacional.
Aceite proposto: Próxima ação deve respeitar decisão vigente e evidência necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

USO AVANÇADO — Consulta histórica
Cenário: Usuário quer entender mudança de posição.
Estratégia: Criar vista cronológica a partir de versões originais, preservando o que era desconhecido em cada etapa.
Papel do modelo pequeno: 15–30B explica evolução.
Aceite proposto: Não reescrever passado usando conclusão atual como se sempre fosse conhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de resumos estruturados por tarefa e campos.
8–14B: Autor de síntese local com fontes por afirmação.
15–30B: Integrador de vistas históricas ou contraditórias.
Requisitos de treino/runtime: Origens preservadas, finalidade e versão da vista; distilação paramétrica é outro processo, identificado por T179.
Não aplicar quando: Resumo vira única cópia do conhecimento ou é reutilizado para finalidade que exige detalhes omitidos.

## T069:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Resumo de gravação é analogia de artefato externo, sem prova de consolidação de memória de agente.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q013, V4A-Q023.

## T069:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T069 → T179 [alternative]
Como combinar: Escolher internalização em pesos somente como projeto distinto.
Interface: Corpus, objetivo e critério de atualização.
Condição: Houver dados e treino apropriados, não mera escrita de resumo.
Aceite proposto: Verificar mudança de pesos antes de chamar processo de destilação paramétrica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, A-S040, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T069 → T072 [requires]
Como combinar: Versionar vista e finalidade junto da origem.
Interface: Resumo, purpose_id, fontes e revisão.
Condição: Dependências permitirem reconstrução.
Aceite proposto: Mudar finalidade e detectar vista incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, A-S040, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não afirmar aprendizado paramétrico por ter salvo resumo.
- Não converter hipótese sintetizada em fato confirmado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar utilidade da vista para tarefa específica; resumir externamente melhora acesso, não aumenta por si só conhecimento dos pesos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T058, T072, T179, P004

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S005 — Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

[https://arxiv.org/abs/2308.15022](https://arxiv.org/abs/2308.15022)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização recursiva de memória a partir do resumo anterior e novos diálogos, sem equivaler a mudança dos pesos.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4D-S005 — Pixel December 2023 feature drop

[https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Lançamento de Gemini Nano em Pixel 8 Pro e resumo offline no Recorder.

Limite: Não identifica o checkpoint nem sua contagem de parâmetros. Smart Reply no Gboard era developer preview; não confundir resumo com cadeia hierárquica ou destilação.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T070 — Episodic Store

**Nome canônico:** Episodic Store  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T070  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repositório de episódios

## T070:C01 — conceito

Componente de armazenamento de episódios com índices, versões, relações e evidências. A memória episódica é o conceito; o store é sua implementação persistente. Precisa permitir recuperar o resumo de uma experiência e, quando necessário, abrir ações e artefatos originais.

Como funciona:
- Receber episódio com fronteiras e schema definidos.
- Persistir resumo, eventos associados e referências.
- Oferecer consultas por identidade, tempo, problema e resultado.

## T070:C02 — aplicacao

Quando usar:
- Muitas missões precisam reaproveitar experiências anteriores.
- Auditoria requer distinguir resultado relatado e resultado comprovado.

Quando não usar:
- Não tratar um índice vetorial de resumos como armazenamento completo dos episódios.

Implementação proposta:
- Proposta: usar episode_id, mission_id, environment_version e outcome_status.
- Manter eventos de origem imutáveis e resumos como projeções.
- Indexar fracassos e condições de aplicação, não apenas casos de sucesso.

Aplicação LAI proposta:
Proposta LAI: criar um store para missões da Helena com estado de verificação explícito; decisões de reutilização devem considerar versão e condições.

## T070:C03 — riscos_validacao

Armadilhas:
- Uma experiência pode ser fragmentada em episódios inconsistentes.
- Referências a logs temporários podem deixar o resumo sem evidência.

Métricas sugeridas:
- Episódios completos e referências resolvíveis.
- Precisão da recuperação de casos comparáveis.

Testes propostos:
- Reconstruir um episódio a partir do índice e abrir todas as evidências citadas.
- Consultar pelo tipo de falha e recuperar tanto correção quanto tentativa malsucedida relevante.

## T070:C04 — perguntas_proveniencia

Pergunta: Qual banco devo usar?
Resposta: O contrato e a carga orientam a escolha; armazenamento relacional com índice lexical pode ser suficiente inicialmente.

Pergunta: Devo guardar só o resumo para economizar?
Resposta: Mantenha originais conforme retenção. Sem eles, o episódio perde capacidade de auditoria e reinterpretação.

Pergunta: Timestamp de conclusão é uma boa chave de ordenação única?
Resposta: Pode haver empates, atrasos e episódios reabertos. Use critério determinístico adicional e semântica definida para atualizações.

Pergunta: O resumo deve ser o registro autoritativo?
Resposta: Somente se esse for um contrato conscientemente limitado. Para reconstrução, preserve eventos e artefatos que permitem verificar o que o resumo afirma.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T070:C05 — mecanismo_avancado

O store episódico precisa suportar operações com semânticas diferentes: localizar casos semelhantes, listar episódios de uma missão e reconstruir todos os eventos de um caso. Um top-k semântico atende à primeira operação, mas não comprova completude das outras. Paginação, ordenação estável e fronteiras de leitura tornam-se essenciais quando uma auditoria ou consolidação precisa percorrer todo o conjunto, inclusive registros pouco relevantes lexicalmente.

Condição de contorno:
Um banco de exemplos com apenas resumos e links expirados pode servir à orientação, mas não consegue comprovar a sequência operacional que os resumos descrevem.

Contrato proposto:
- Entradas: Episódios identificados, eventos de origem, estado do desfecho e metadados de missão e ambiente.
- Saídas: Resultados de busca ou enumeração com modo declarado, paginação e referências recuperáveis.
- Estado: Índices, revisões de ingestão, posição de atualização e política de ordenação por operação.
- Invariante: Busca ranqueada limitada nunca é apresentada como inventário completo de episódios elegíveis.

Compromissos de projeto:
- Índices por problema facilitam analogias e podem esconder casos raros sem uma via de enumeração.
- Guardar detalhes completos melhora auditoria e amplia armazenamento, manutenção e custos de leitura.

## T070:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar mais episódios que o limite padrão de busca, deixando uma falha relevante além da primeira página. A enumeração deve recuperá-la ou informar incompletude, sem concluir que todos os casos tiveram sucesso.

Plano de avaliação proposto:
Avaliação proposta: comparar busca semântica e enumeração filtrada nas respectivas tarefas. Medir recall de casos úteis, completude, estabilidade de paginação, recuperação dos artefatos e atraso de indexação; testar mudanças concorrentes durante a listagem.

Comparações:
- T049 (complements): A memória episódica define o conteúdo de uma experiência; o store oferece persistência e operações de acesso.
- T059 (complements): Eventos podem constituir a origem reconstruível dos episódios, enquanto resumos são projeções para busca.

Afirmação rastreável:
A documentação de stores do LangGraph explicita limites de listagem, paginação e ordenação dependente do backend.
Suporte: related; fontes: V3A-S032
Limite: É suporte para contratos de armazenamento; a fonte não implementa automaticamente o modelo episódico proposto aqui.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T070:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou top-k e enumeração. Aqui o store permite amostragem controlada e análise de cobertura sem enviesar avaliação pela recuperação.

Projeto e decomposição
Mantenha consultas de busca e de auditoria separadas. A primeira prioriza relevância; a segunda precisa enumerar ou amostrar população com probabilidades conhecidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

Controle adaptativo
Registre episódios pendentes, fracassados e incompletos. Excluir esses registros pode transformar o store numa coleção de sucessos e produzir procedimentos excessivamente otimistas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

Validação contrafactual
Compare resultados sobre episódios recuperados e sobre amostra independente. Meça viés de seleção, cobertura de falhas e perda por paginação; um top-k não define distribuição da população. Unidade de avaliação: população de episódios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

USO AVANÇADO — Revisão de desempenho
Cenário: Equipe quer saber quais falhas se repetem.
Estratégia: Consultar episódios por intervalo e status, amostrar de forma reproduzível e agregar causas somente quando sustentadas.
Papel do modelo pequeno: 3–7B categoriza; código agrega.
Aceite proposto: Contagens devem refletir população ou amostra explicitada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

USO AVANÇADO — Memória para decisão atual
Cenário: É preciso recuperar caso parecido.
Estratégia: Buscar por condições, incluir exemplos negativos elegíveis e preservar referência ao episódio completo.
Papel do modelo pequeno: 8–14B compara contexto.
Aceite proposto: Não inferir frequência de sucesso pela ordem de similaridade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S002, V3A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de episódios com campos e status explícitos.
8–14B: Leitor de pequenos conjuntos relevantes com casos negativos.
15–30B: Analista de padrões de experiências com estatísticas calculadas externamente.
Requisitos de treino/runtime: IDs estáveis, paginação consistente, filtros temporais e estados de conclusão; índices são projeções do store.
Não aplicar quando: Não há forma de distinguir episódio ausente, incompleto ou excluído da consulta.

## T070:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Operador descreve migração real de todos os metadados e listagem fortemente consistente.
Mecanismo documentado: Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.
Correspondência com esta base: Listagem completa inspira enumeração de episódios; objeto não é episódio.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.
Limite: Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S007, V4A-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q008, V4A-Q023.

## T070:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T070 → T049 [feeds]
Como combinar: Retornar experiência com contexto suficiente.
Interface: Condições, ações, resultado e campos desconhecidos.
Condição: Recuperação preservar episódio completo ou link.
Aceite proposto: Testar episódio sem resultado e impedir preenchimento por suposição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S002, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T070 → T056 [requires]
Como combinar: Aplicar corte de conhecimento em auditoria histórica.
Interface: Tempos de ocorrência e registro.
Condição: Amostra usar perspectiva temporal declarada.
Aceite proposto: Inserir episódio atrasado e comparar consultas antes e depois.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S002, V3A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não calcular taxa de sucesso usando apenas top-k.
- Não confundir deduplicação de relato com remoção de episódio distinto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de decisão com amostragem e busca adequadas; tamanho do store não mede memória efetivamente utilizável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T059, T060, T066

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

### V4A-S005 — Spanner: Google's Globally-Distributed Database

[https://research.google/pubs/spanner-googles-globally-distributed-database-2/](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco multiversão, transações externamente consistentes e incerteza temporal.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency

[https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração efetiva dos metadados do Cloud Storage para Spanner e consistência de listagem.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T071 — Memory Promotion

**Nome canônico:** Memory Promotion  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T071  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** promoção de memória

## T071:C01 — conceito

Processo de admitir informação em uma categoria de maior reutilização ou confiança, por exemplo de observação para fato candidato, de episódios para procedimento e de procedimento para skill. A promoção é uma decisão de qualidade; mover um arquivo de pasta não comprova aprendizado.

Como funciona:
- Definir destino, requisitos e evidências necessárias.
- Verificar origem, repetibilidade e limites de aplicação.
- Registrar decisão de promoção com versão e possibilidade de reversão.

Nota de nomenclatura: Política arquitetural proposta; não existe limiar universal de evidência aplicável a toda memória.

## T071:C02 — aplicacao

Quando usar:
- Agentes que transformam experiências em conhecimento reutilizável.
- Curadoria de skills a partir de resultados de execução.

Quando não usar:
- Não promover por número de repetições quando todas derivam da mesma afirmação inicial.

Implementação proposta:
- Proposta: estabelecer critérios diferentes para fato, regra e procedimento.
- Exigir testes novos para procedimentos e evidência independente quando cabível.
- Manter dependências para rebaixar ou invalidar uma memória se suas fontes mudarem.

Aplicação LAI proposta:
Proposta LAI: promover episódios da Helena a procedimentos somente após validação fora do caso original; hipóteses continuam utilizáveis como hipóteses.

## T071:C03 — riscos_validacao

Armadilhas:
- A autoconfirmação pode promover erros com aparência de consenso.
- Critérios rígidos demais podem impedir reutilização útil de hipóteses claramente rotuladas.

Métricas sugeridas:
- Precisão das memórias promovidas em tarefas posteriores.
- Taxa de reversão e tempo até detectar generalização errada.

Testes propostos:
- Apresentar cinco cópias do mesmo relato e não tratá-las como cinco confirmações.
- Invalidar a evidência de uma skill e exigir revisão de seu status.

## T071:C04 — perguntas_proveniencia

Pergunta: Promoção precisa alterar pesos?
Resposta: Não. Pode mudar estado editorial e disponibilidade de uma memória externa.

Pergunta: É possível reverter uma promoção?
Resposta: O desenho deve permitir: correções e novos resultados podem exigir rebaixar confiança ou retirar um procedimento de uso.

Pergunta: Toda hipótese precisa ser promovida para ser útil?
Resposta: Não. Pode orientar investigação com seu status explícito. O erro é tratá-la como premissa confirmada sem a mudança de evidência necessária.

Pergunta: Como rebaixar um procedimento sem apagar aprendizado?
Resposta: Preserve histórico e motivo, suspenda recomendação no escopo afetado e mantenha acesso aos casos que ainda explicam quando ele funcionou.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T071:C05 — mecanismo_avancado

Promover memória altera sua autoridade de uso, não apenas seu endereço. Um fato candidato pode ser útil para busca exploratória antes de ser aceito como premissa operacional. Um procedimento testado em ambiente específico pode ser recomendado apenas naquele escopo. A decisão de promoção deve registrar critérios satisfeitos e dependências; quando uma fonte é corrigida, o sistema precisa reavaliar a promoção e os consumidores derivados.

Condição de contorno:
A promoção é frágil quando validação usa os mesmos casos que originaram a regra ou quando uma revisão bem escrita substitui evidência de aplicabilidade.

Contrato proposto:
- Entradas: Memória candidata, evidências, escopo pretendido e critérios proporcionais à consequência do uso.
- Saídas: Status de promoção com justificativa, limites e pendências de validação.
- Estado: Histórico de decisões, revisores ou verificadores, dependências e condições de rebaixamento.
- Invariante: Aumento de autoridade exige evidência adequada; frequência de repetição ou consenso entre cópias não basta.

Compromissos de projeto:
- Critérios explícitos reduzem propagação de erros e acrescentam tempo até reutilização ampla.
- Manter candidatos acessíveis favorece descoberta e exige que o leitor respeite seus estados de incerteza.

## T071:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: promover uma regra apoiada por duas notas que derivam da mesma origem, depois corrigir essa origem. A política deve reconhecer dependência comum e reavaliar a regra promovida.

Plano de avaliação proposto:
Avaliação proposta: comparar promoção imediata e promoção com validação independente em casos novos. Medir falsos conhecimentos aceitos, utilidade perdida por bloqueio, tempo de revisão e propagação de correções; separar fatos, hipóteses e procedimentos.

Comparações:
- T058 (distinct_from): Consolidação produz uma representação; promoção decide quais usos e grau de confiança ela pode receber.
- T055 (complements): Procedimentos podem ser promovidos para reutilização sob pré-condições verificadas e versões compatíveis.

Afirmação rastreável:
PROV-DM permite registrar derivação e responsabilidade de entidades, fornecendo estrutura para rastrear a origem de memórias candidatas.
Suporte: related; fontes: V3A-S037
Limite: Os critérios de promoção são proposta editorial; o padrão de proveniência não certifica conteúdo nem prescreve aprovação de memórias.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T071:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou promoção e mudança de pasta. Aqui promoção exige período de uso observado e critérios diferentes por tipo de memória.

Projeto e decomposição
Crie estados candidato, validado para escopo e ativo. Preferência explícita pode ter caminho curto; regra inferida de episódios precisa de suporte e teste de transferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

Controle adaptativo
Antes de promoção ampla, usar candidato em modo de comparação sem alterar decisões reais. Registrar quando ele ajudaria, conflitaria ou ampliaria incorretamente o escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

Validação contrafactual
Compare admissão imediata e promoção por evidência. Meça falsos fatos ativos, utilidade futura e tempo até corrigir promoção indevida; mais candidatos aprovados não indica melhor aprendizado. Unidade de avaliação: candidato promovido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

USO AVANÇADO — Preferência declarada
Cenário: Usuário define padrão para um projeto.
Estratégia: Registrar fonte explícita, escopo e condição de revisão; recuperar em tarefa elegível e evitar generalização para outros projetos.
Papel do modelo pequeno: 3–7B extrai declaração.
Aceite proposto: Escopo armazenado deve corresponder ao pedido literal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

USO AVANÇADO — Regra operacional inferida
Cenário: Vários incidentes sugerem recomendação.
Estratégia: Consolidar evidências independentes, testar em caso novo e promover apenas condições verificadas. Manter exceções junto da regra.
Papel do modelo pequeno: 15–30B compara casos.
Aceite proposto: Regra deve recusar aplicação fora das condições validadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de candidatos explícitos com tipo e origem.
8–14B: Revisor de suporte local e compatibilidade de escopo.
15–30B: Analista de abstrações entre episódios, com validação externa.
Requisitos de treino/runtime: Estados de promoção, critérios por tipo e caminho de revogação; autoridade não deriva do texto produzido pelo modelo.
Não aplicar quando: Não há fonte para o candidato ou o único suporte é repetição da mesma inferência.

## T071:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C018 — OpenAI / ChatGPT Memory
Evidência: produto/recurso disponível; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Produto documenta memórias salvas e uso de histórico para personalização.
Mecanismo documentado: Informações selecionadas podem atravessar conversas com controles próprios.
Correspondência com esta base: Seleção do que lembrar não prova política de promoção desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Criar memória externa pequena de preferências explícitas e testar correções e escopo.
Limite: Comportamento varia por conta; fonte não revela algoritmo nem prova precisão permanente. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S017.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q013, V4A-Q023.

## T071:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T071 → T058 [requires]
Como combinar: Receber candidato consolidado com divergências preservadas.
Interface: Proposição, fontes, exceções e limites.
Condição: Consolidação não apagar evidência contrária.
Aceite proposto: Testar candidato aparentemente consensual derivado de uma única origem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S037, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T071 → T075 [complements]
Como combinar: Revisar promoção após evidência nova.
Interface: Memória ativa, correção e dependentes.
Condição: Revogação alcançar projeções e resumos.
Aceite proposto: Corrigir regra e verificar que uso futuro deixa de aplicá-la.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S037, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover conclusão pelo grau de confiança verbal.
- Não interpretar frequência de uso como confirmação independente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de memórias ativas no futuro; promoção controlada reduz erro acumulado sem tornar o modelo infalível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T048, T055, T058, T204

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T072 — Versioned Memory

**Nome canônico:** Versioned Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T072  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória versionada

## T072:C01 — conceito

Preserva revisões de registros para saber qual conteúdo foi usado e como mudou. Versionamento pode ser ordinal, por commit ou por hash. É diferente de bitemporalidade: ter versões não informa automaticamente quando um fato valia no mundo ou quando ficou conhecido.

Como funciona:
- Atribuir identidade e versão a cada revisão.
- Vincular alterações às versões anteriores e às fontes.
- Consultar versão específica ou resolver qual é vigente por política explícita.

## T072:C02 — aplicacao

Quando usar:
- Memórias e procedimentos alterados ao longo do tempo.
- Reprodução de decisões e correção de conhecimento.

Quando não usar:
- Não usar apenas um campo updated_at quando é necessário reconstruir conteúdo antigo.

Implementação proposta:
- Proposta: guardar autor, motivo, fonte e mudança de status.
- Manter um alias atual separado do histórico imutável.
- Usar versão esperada em escrita para detectar alterações concorrentes.

Aplicação LAI proposta:
Proposta LAI: versionar fatos, prompts e skills da Helena, permitindo indicar exatamente o conhecimento utilizado em cada missão.

## T072:C03 — riscos_validacao

Armadilhas:
- A versão mais recente pode ser menos confiável que uma anterior.
- Referências sem versão podem mudar de significado depois de uma decisão.

Métricas sugeridas:
- Cobertura histórica e conflitos de atualização.
- Proporção de decisões ligadas a versões exatas.

Testes propostos:
- Reproduzir uma consulta com o mesmo snapshot e obter a mesma evidência.
- Tentar sobrescrever com versão antiga e exigir conflito explícito.

## T072:C04 — perguntas_proveniencia

Pergunta: Versionar é igual a não poder apagar?
Resposta: Não. Retenção e imutabilidade são políticas separadas.

Pergunta: Git resolve toda memória versionada?
Resposta: Ajuda com arquivos, mas concorrência, acesso, validade temporal e grandes volumes ainda precisam de desenho específico.

Pergunta: Uma versão numérica basta para reproduzir uma resposta?
Resposta: Somente se resolve todos os componentes relevantes. Também podem importar modelo, configuração de recuperação e fontes externas lidas depois.

Pergunta: Reverter memória desfaz decisões anteriores?
Resposta: Não. Reverte o conteúdo utilizado em chamadas futuras. Decisões e alterações já aplicadas precisam permanecer no histórico e, quando cabível, ser reconciliadas.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T072:C05 — mecanismo_avancado

Versionar cada arquivo individualmente não garante uma visão consistente do conjunto. Uma memória pode depender de um resumo, índice e documento original produzidos em momentos distintos. Um manifesto de publicação identifica quais revisões formam uma versão utilizável e permite detectar misturas. O alias vigente deve apontar a esse conjunto completo, sem confundir edição mais recente com revisão validada para consumo.

Condição de contorno:
Se consumidores resolvem latest independentemente para cada componente, podem combinar versões incompatíveis mesmo quando todos os objetos possuem histórico correto.

Contrato proposto:
- Entradas: Revisões de memórias, dependências, resultados de validação e conjunto que será publicado.
- Saídas: Manifesto consistente e alias de versão utilizável, mantendo acesso às revisões anteriores.
- Estado: Histórico, relações entre versões, alterações pendentes e consumidores que fixaram uma revisão.
- Invariante: Uma resposta reproduzível identifica o conjunto efetivamente lido, incluindo índice e representações derivadas.

Compromissos de projeto:
- Fixar revisões torna diagnóstico possível e aumenta armazenamento e gestão de referências.
- Atualizar aliases simplifica descoberta e exige publicação coordenada para impedir leitura parcial do conjunto.

## T072:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: publicar um índice novo antes de disponibilizar o documento correspondente. O leitor deve continuar na versão anterior ou detectar indisponibilidade; não deve combinar índice novo com fonte antiga.

Plano de avaliação proposto:
Avaliação proposta: comparar revisões independentes e publicação por manifesto durante atualizações. Medir combinações inválidas, tempo até disponibilidade, reprodução de respostas e custo de retenção; testar rollback de dados sem repetir efeitos externos.

Comparações:
- T056 (distinct_from): Revisão registra evolução do artefato; bitemporalidade define validade no domínio e perspectiva de conhecimento.
- T061 (complements): Identificadores por conteúdo podem fixar precisamente os objetos incluídos em um manifesto.

Afirmação rastreável:
Git organiza objetos de conteúdo e commits que referenciam uma árvore e a história de revisões.
Suporte: related; fontes: A-S028
Limite: Usar um manifesto consistente para índices e memórias externos é uma proposta; um commit não inclui recursos que não foram incorporados ao seu contrato.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T072:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu manifesto coerente. Aqui versionamento suporta branches de memória e comparação de políticas antes de publicação.

Projeto e decomposição
Mantenha branch candidato para mudanças de consolidação ou ontologia. Consultas experimentais podem apontar a ele sem alterar memória usada por tarefas em andamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, V3A-S037.

Controle adaptativo
Defina merge semântico além do merge de arquivos: fatos com mesmo sujeito e valores diferentes, escopos sobrepostos e versões de índice incompatíveis exigem decisão explícita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, V3A-S037.

Validação contrafactual
Compare revisões com conjunto de perguntas próprio e diffs de afirmações. Meça regressões, fontes perdidas e respostas mudadas sem evidência nova; rollback precisa restaurar manifesto e projeções compatíveis. Unidade de avaliação: revisão de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, V3A-S037.

USO AVANÇADO — Nova política de resumo
Cenário: Equipe quer reduzir memória ativa.
Estratégia: Criar branch, gerar vistas candidatas e comparar respostas antes de mover referência ativa. Manter tarefas existentes pinadas à revisão inicial.
Papel do modelo pequeno: 8–14B revisa diferenças.
Aceite proposto: Nenhuma tarefa pode receber metade da revisão antiga e metade da nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, V3A-S037.

USO AVANÇADO — Colaboração entre agentes
Cenário: Trabalhadores atualizam áreas relacionadas.
Estratégia: Produzir mudanças por escopo, detectar conflito de significado e integrar somente após validar dependências cruzadas.
Papel do modelo pequeno: 15–30B reconcilia; código confirma.
Aceite proposto: Merge textual limpo não pode ocultar afirmações incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, V3A-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de diferenças de campos entre revisões.
8–14B: Revisor de mudanças locais e compatibilidade de fontes.
15–30B: Integrador de branches com conflitos semânticos e escopos cruzados.
Requisitos de treino/runtime: Manifestos imutáveis, referência ativa e política de pinning; índices precisam declarar revisão de origem.
Não aplicar quando: As versões são apenas nomes sem conteúdo recuperável ou rollback não restaura dependências.

## T072:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C007 — Amazon / Dynamo em serviços Amazon
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores descrevem adoção de Dynamo por serviços centrais da Amazon.
Mecanismo documentado: Versionamento de objetos e resolução de conflitos assistida pela aplicação.
Correspondência com esta base: Versões de dados são precursor de memória versionada, sem semântica do agente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Apresentar versões concorrentes ao reconciliador pequeno sem permitir que ele descarte evidência sozinho.
Limite: Dynamo histórico não equivale a todos os produtos DynamoDB; particionamento por hash não é CAS. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q006, V4A-Q007, V4A-Q013, V4A-Q026.

## T072:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T072 → T076 [complements]
Como combinar: Usar Git para transportar diferenças e revisões.
Interface: Commit, branch, arquivos e manifesto.
Condição: Semântica ser validada fora do merge textual.
Aceite proposto: Criar conflito lógico em arquivos diferentes e exigir revisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S040, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T072 → T075 [requires]
Como combinar: Reconciliar afirmações concorrentes antes de publicar.
Interface: Diffs, fontes e escopos afetados.
Condição: Decisão preservar histórico e incerteza.
Aceite proposto: Rejeitar união automática de fatos incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S040, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar latest em cada recurso durante uma tarefa pinada.
- Não chamar backup isolado de histórico versionado completo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar regressões por revisão; bom versionamento torna mudanças auditáveis, sem garantir que sejam melhorias.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T056, T065, T073, T076

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S040 — Git git-update-ref Documentation

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional por old-oid e transações de referências; leitores concorrentes ainda podem observar subconjuntos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S006 — Dynamo: Amazon’s highly available key-value store

[https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso em serviços Amazon; versões de objetos e resolução de conflitos pela aplicação.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T073 — Immutable Evidence Store

**Nome canônico:** Immutable Evidence Store  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T073  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repositório imutável de evidências; evidence store

## T073:C01 — conceito

Armazena evidências de modo que versões confirmadas não sejam alteradas silenciosamente. Imutabilidade depende de permissões, retenção e implementação; um arquivo chamado imutável não oferece essa garantia. O registro deve separar conteúdo, identificação e prova de origem.

Como funciona:
- Capturar evidência com metadados de origem e integridade.
- Persistir uma versão protegida conforme a política definida.
- Criar novas versões ou registros de correção sem sobrescrever a evidência anterior.

## T073:C02 — aplicacao

Quando usar:
- Logs de testes, contratos examinados e relatórios de auditoria.
- Necessidade de reconstruir o suporte de uma decisão.

Quando não usar:
- Não reter indiscriminadamente dados sensíveis ou temporários sem finalidade e política de retenção.

Implementação proposta:
- Proposta: usar IDs e hashes com controle de escrita e exclusão.
- Definir retenção e quem pode administrar o armazenamento.
- Verificar periodicamente integridade e possibilidade real de recuperar os objetos.

Aplicação LAI proposta:
Proposta LAI: guardar saídas originais de testes e snapshots usados em auditorias; conclusões derivadas ficam em registros separados e corrigíveis.

## T073:C03 — riscos_validacao

Armadilhas:
- Hash guardado ao lado de arquivo alterável pode ser substituído junto com ele.
- Imutabilidade não prova que o conteúdo foi produzido pela ferramenta alegada.

Métricas sugeridas:
- Integridade dos objetos e referências acessíveis.
- Tentativas de alteração detectadas e cobertura de origem.

Testes propostos:
- Tentar modificar uma versão protegida e exigir rejeição.
- Inserir evidência nova contraditória e preservar ambas com relação explícita de correção.

## T073:C04 — perguntas_proveniencia

Pergunta: Um commit Git é imutabilidade absoluta?
Resposta: Não. Objetos podem ter hashes estáveis, mas referências e retenção dependem do controle do repositório.

Pergunta: WORM comprova a veracidade do arquivo?
Resposta: Não. Protege contra determinadas alterações; qualidade, autoria e contexto da evidência continuam exigindo validação.

Pergunta: Um objeto protegido pode ter informação errada?
Resposta: Sim. Guarde correção separada com vínculo à evidência e impeça que a consulta atual use o registro errado sem seu status.

Pergunta: Guardar o hash no mesmo local resolve autenticidade?
Resposta: Não. Um administrador que controla ambas as partes pode substituir a narrativa de origem. A cadeia de confiança exige controles apropriados ao produtor e ao armazenamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T073:C05 — mecanismo_avancado

Imutabilidade deve ser descrita por versão, duração e autoridade capaz de alterar a política. No S3 Object Lock, retenção se aplica a versões de objeto e os modos têm poderes administrativos diferentes. Proteger bytes não impede publicar uma versão nova ou alterar um alias para apontar a outra evidência. Um consumidor precisa fixar a versão protegida e verificar a cadeia de origem, não apenas confiar no nome do bucket.

Condição de contorno:
Armazenamento WORM não prova que o conteúdo inicial era verdadeiro, completo ou produzido pelo agente alegado; integridade e autenticidade são propriedades diferentes.

Contrato proposto:
- Entradas: Evidências, identificadores de versão, política de retenção e informação sobre o produtor.
- Saídas: Versões protegidas e recuperáveis com manifesto de integridade e proveniência associada.
- Estado: Retenção vigente, permissões administrativas, aliases e verificações de disponibilidade.
- Invariante: Uma nova versão ou mudança de ponteiro não substitui silenciosamente a evidência citada numa decisão anterior.

Compromissos de projeto:
- Proteção contra alteração reduz risco de reescrita e limita correções destrutivas.
- Retenção prolongada preserva auditabilidade e aumenta custo; informações derivadas podem ser corrigidas sem apagar o original.

## T073:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter uma versão protegida e trocar o alias para outro objeto. A auditoria da decisão anterior deve recuperar a versão original e detectar a mudança de referência.

Plano de avaliação proposto:
Avaliação proposta: avaliar controles com versões de teste e permissões distintas. Medir resistência à sobrescrita, detecção de ponteiros trocados e recuperação por versão; verificar também proveniência, pois um hash correto pode acompanhar uma evidência falsa.

Comparações:
- T061 (complements): Hash verifica identidade de conteúdo; retenção protege a existência e impossibilidade de alteração sob uma política.
- T072 (complements): Histórico versionado permite corrigir interpretação sem reescrever a evidência originalmente registrada.

Afirmação rastreável:
S3 Object Lock oferece retenção e legal holds por versão, com modos governance e compliance de proteção distinta.
Suporte: direct; fontes: A-S034
Limite: A garantia depende da configuração e do modo; não equivale a certificação factual ou a durabilidade de qualquer sistema chamado imutável.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T073:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu retenção WORM e autoridade. Aqui evidências imutáveis recebem verificação periódica de legibilidade e preservação de contexto.

Projeto e decomposição
Preserve artefato, metadados de captura e informação necessária para interpretá-lo. Bytes íntegros de uma tabela sem schema ou unidade podem ser inúteis na auditoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

Controle adaptativo
Verifique disponibilidade e legibilidade periodicamente, sem alterar o objeto original. Migrações de formato devem produzir novos derivados com vínculo explícito e comparação de conteúdo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

Validação contrafactual
Compare armazenamento de arquivo isolado e pacote interpretável. Meça restauração, integridade e reprodução de extrações; retenção imutável não garante que o formato continue utilizável. Unidade de avaliação: pacote de evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

USO AVANÇADO — Auditoria de resposta
Cenário: É preciso comprovar o que foi consultado.
Estratégia: Guardar recorte e documento de origem com revisão, data de captura e parser; permitir reconstruir o contexto efetivamente enviado.
Papel do modelo pequeno: 3–7B lê manifesto; 8–14B explica.
Aceite proposto: Citação deve resolver exatamente a evidência usada na decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

USO AVANÇADO — Mudança de parser
Cenário: Novo extrator altera tabelas antigas.
Estratégia: Manter original, gerar extração nova e comparar células e relações antes de substituí-la na busca.
Papel do modelo pequeno: 15–30B revisa divergências sem alterar original.
Aceite proposto: Nenhuma conversão pode apagar evidência da interpretação anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de manifestos e verificações de integridade feitas por código.
8–14B: Comparador de extrações antigas e novas em blocos pequenos.
15–30B: Analista de divergências materiais entre interpretações do mesmo artefato.
Requisitos de treino/runtime: Retenção, hashes, metadados e leitores de formato; autenticidade exige evidência adicional à imutabilidade.
Não aplicar quando: A política impede correção de dados ativos e mistura evidência histórica com verdade vigente.

## T073:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q025, V4A-Q026.

## T073:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T073 → T061 [requires]
Como combinar: Verificar identidade física de cada artefato.
Interface: Digest, codec, tamanho e localização.
Condição: Verificação usar bytes efetivamente recuperados.
Aceite proposto: Corromper objeto e exigir falha antes da leitura pelo modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S034, V3A-S038, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T073 → T072 [feeds]
Como combinar: Versionar derivados e interpretações sem substituir origem.
Interface: Original, extração, parser e manifesto.
Condição: Relação de derivação permanecer rastreável.
Aceite proposto: Reproduzir resposta usando a versão histórica correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S034, V3A-S038, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar WORM como prova de que o conteúdo é verdadeiro.
- Não confundir exclusão da janela com eliminação do arquivo de evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar auditabilidade das respostas; modelo de fronteira não recupera contexto que nunca foi preservado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T061, T072

## Fontes primárias associadas

### A-S034 — Locking objects with Object Lock

[https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Armazenamento WORM e proteção de versões de objetos contra alteração e exclusão.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T074 — Memory Eviction

**Nome canônico:** Memory Eviction  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T074  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** expulsão de memória; descarregamento de memória

## T074:C01 — conceito

Remove informação de uma camada de memória quando ela excede orçamento ou deixa de ser útil. É essencial declarar se a remoção ocorre só do contexto ativo, de um cache ou do armazenamento durável. Essas operações têm consequências muito diferentes.

Como funciona:
- Definir camada, limite e unidades elegíveis.
- Escolher itens por recência, uso, validade ou prioridade.
- Preservar referências ou realizar descarte conforme a política aplicável.

## T074:C02 — aplicacao

Quando usar:
- Contexto ativo e caches com capacidade limitada.
- Acervos com material redundante ou vencido.

Quando não usar:
- Não apagar a única evidência de uma decisão sem considerar retenção e dependências.

Implementação proposta:
- Proposta: fixar objetivos e restrições vigentes contra expulsão automática.
- Distinguir arquivamento, invalidação e exclusão definitiva.
- Registrar o motivo e verificar se objetos expulsos ainda são referenciados por memórias ativas.

Aplicação LAI proposta:
Proposta LAI: começar por expulsar detalhes do contexto ativo para arquivo; exclusão durável exige política própria, não apenas escore de relevância.

## T074:C03 — riscos_validacao

Armadilhas:
- Um item pouco usado pode tornar-se crítico em uma tarefa rara.
- Remover memória repetidamente recuperada causa thrashing e aumenta latência.

Métricas sugeridas:
- Taxa de recarregamento após expulsão.
- Falhas por informação removida e uso do orçamento.

Testes propostos:
- Expulsar um detalhe do contexto e recuperá-lo por referência quando necessário.
- Tentar apagar evidência ainda usada por uma decisão e exigir tratamento de dependência.

## T074:C04 — perguntas_proveniencia

Pergunta: Eviction significa esquecimento permanente?
Resposta: Depende da camada. Em contexto ou cache pode significar apenas descarregar algo recuperável.

Pergunta: É igual a KV Cache Eviction?
Resposta: Não. KV cache contém estados de inferência; memória de agente pode conter fatos, arquivos e episódios.

Pergunta: Noeviction elimina risco de perda?
Resposta: Evita expulsão automática por essa política, mas novas escritas podem falhar. O aplicativo precisa detectar e tratar a falha, além de garantir persistência.

Pergunta: Devo conservar tudo que é caro de reconstruir?
Resposta: É um critério forte, mas deve ser combinado com validade, uso esperado e retenção. A decisão não pode depender só de frequência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T074:C05 — mecanismo_avancado

Eviction por pressão de capacidade e expiração por tempo são mecanismos diferentes. No Redis, LRU e LFU usam aproximações; a frequência pode decair para acompanhar mudanças de acesso. Esses critérios preveem reutilização, não importância factual. Se uma camada contém a única cópia de uma memória necessária, tratá-la como cache converte uma otimização de desempenho em perda de conhecimento.

Condição de contorno:
A política falha quando assume que todo objeto removido pode ser reconstruído, mas fontes, operações ou artefatos originais já não estão disponíveis.

Contrato proposto:
- Entradas: Ocupação, acessos, classe da memória, custo de reconstrução e referências ainda ativas.
- Saídas: Objetos elegíveis removidos da camada e registro de destino ou possibilidade de reconstrução.
- Estado: Contadores, prioridade, TTL quando aplicável e vínculos com a cópia autoritativa.
- Invariante: Eviction de cache não apaga a única evidência de um fato sem uma política de retenção separada.

Compromissos de projeto:
- LRU acompanha recência e pode expulsar itens raros caros de recuperar.
- LFU preserva itens frequentes e precisa adaptar-se quando o padrão muda; ambas exigem avaliar misses e custo de reconstrução.

## T074:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar duas coleções maiores que a capacidade e manter uma evidência crítica pouco acessada. A política deve expor thrashing e impedir que a evidência autoritativa seja tratada como cópia descartável.

Plano de avaliação proposto:
Avaliação proposta: comparar LRU, LFU e política por classe com a mesma capacidade. Medir hit rate, latência de misses, custo de recomputação e perdas irrecuperáveis; separar expulsões por capacidade de expiração e invalidação.

Comparações:
- T031 (distinct_from): Invalidação remove elegibilidade por mudança de estado; eviction libera capacidade mesmo para conteúdo ainda válido.
- T048 (complements): Gestão de memória decide quais classes podem ser descartadas e sob quais condições.

Afirmação rastreável:
Redis documenta LRU aproximado, LFU com contadores probabilísticos e política noeviction que pode rejeitar novas escritas.
Suporte: direct; fontes: V3A-S039
Limite: Essas políticas controlam recursos do store; não definem a relevância ou verdade das memórias de um agente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T074:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu expiração e capacidade. Aqui evicção usa custo de reconstituição e dependências ativas para reduzir trabalho repetido.

Projeto e decomposição
Calcule custo de recarga, reconstrução e verificação. Dois blocos do mesmo tamanho podem ter custos muito diferentes se um vem de arquivo local e outro de investigação longa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

Controle adaptativo
Evite evictar fragmentos de um conjunto necessário em breve. A unidade de substituição pode ser grupo de dependências, desde que a reserva não torne toda memória permanentemente fixa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

Validação contrafactual
Compare LRU, LFU e política por custo de reconstrução. Meça latência total, trabalho repetido e falhas de disponibilidade após evicção; hit rate isolado pode favorecer objetos baratos. Unidade de avaliação: decisão de evicção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

USO AVANÇADO — Agente local com pouca memória
Cenário: Contexto alterna entre módulos.
Estratégia: Manter contratos caros de reconstruir e remover logs reabríveis; liberar grupo quando a fase encerrar.
Papel do modelo pequeno: 3–7B classifica recuperabilidade.
Aceite proposto: Nenhum bloco removido pode ser a única cópia de uma decisão ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

USO AVANÇADO — Cache de artefatos derivados
Cenário: Resumos grandes competem com extrações pequenas.
Estratégia: Priorizar valor por custo evitado e demanda prevista, usando tamanho e tempo de reconstrução medidos.
Papel do modelo pequeno: 8–14B sugere categorias; código aplica política.
Aceite proposto: Reduzir custo de recarga sem aumentar respostas obsoletas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e disponibilidade de origem.
8–14B: Avaliador de dependências de curto prazo por fase.
15–30B: Planejador de reorganização quando conjunto ativo exceder capacidade.
Requisitos de treino/runtime: Medição de custo, referência à cópia canônica e condição de liberação de conteúdo fixado.
Não aplicar quando: Evicção é usada para apagar histórico ou a origem não pode ser recuperada confiavelmente.

## T074:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C009 — Meta / CacheLib em serviços Facebook
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Artigo de operadores relata adoção desde 2017 por múltiplos serviços.
Mecanismo documentado: Engine comum para desenvolvimento e operação de caches de dados e armazenamento.
Correspondência com esta base: Gerência de cache é família relacionada à evicção de memória externa.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar política determinística de residência e estimativa de utilidade proposta pelo modelo.
Limite: Não afirma cache semântico, resumo, verdade da memória ou taxa de acerto de LLM. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q007.

## T074:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T074 → T039 [requires]
Como combinar: Receber prioridade e custo de reconstrução.
Interface: Objeto, valor, dependências e condição de fixação.
Condição: Estimativas atualizadas pela fase atual.
Aceite proposto: Comparar recargas após mudança de objetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S039, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T074 → T063 [complements]
Como combinar: Acionar recarga identificada quando bloco voltar a ser necessário.
Interface: Referência, revisão e status de residência.
Condição: Evicção não invalidar identidade do conteúdo.
Aceite proposto: Evictar e recarregar verificando mesmos bytes e escopo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S039, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apagar metadados de versão necessários à reconciliação.
- Não tratar conteúdo pouco acessado como dispensável sem verificar obrigações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo útil e continuidade sob memória limitada; evicção sofisticada pode ser pior que LRU em carga simples.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T048, T062, T105

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

### V3A-S039 — Redis Key eviction

[https://redis.io/docs/latest/develop/reference/eviction/](https://redis.io/docs/latest/develop/reference/eviction/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Políticas de eviction, noeviction, LRU aproximado, LFU probabilístico e distinção entre expiração e pressão de capacidade.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T075 — Memory Reconciliation

**Nome canônico:** Memory Reconciliation  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T075  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reconciliação de memória

## T075:C01 — conceito

Reconcilia registros duplicados, divergentes ou temporariamente incompatíveis. O objetivo é determinar o que pode ser apresentado como vigente e o que permanece em disputa. Similaridade textual não basta para resolver autoridade, identidade ou tempo.

Como funciona:
- Detectar afirmações que se referem à mesma entidade e propriedade.
- Comparar origem, validade, versão e evidência.
- Criar resolução explícita ou manter conflito pendente sem apagar as fontes.

## T075:C02 — aplicacao

Quando usar:
- Ingestão de vários sistemas sobre a mesma entidade.
- Correções tardias e memórias produzidas por múltiplos agentes.

Quando não usar:
- Não escolher automaticamente o texto mais recente quando uma fonte antiga é a autoridade aplicável.

Implementação proposta:
- Proposta: separar duplicata exata, atualização temporal e contradição real.
- Definir prioridades de fontes por domínio e campo.
- Invalidar sínteses dependentes quando a resolução alterar o conhecimento vigente.

Aplicação LAI proposta:
Proposta LAI: decisões atuais de Leandro devem ter validade e origem explícitas; informações históricas permanecem rastreáveis e não substituem automaticamente a decisão vigente.

## T075:C03 — riscos_validacao

Armadilhas:
- Entidades homônimas podem ser fundidas indevidamente.
- Uma maioria de cópias pode vencer uma fonte primária se independência não for considerada.

Métricas sugeridas:
- Conflitos detectados e resoluções corretas.
- Tempo de propagação de correções e taxa de fusões indevidas.

Testes propostos:
- Apresentar duas informações válidas em períodos diferentes e evitar falso conflito.
- Apresentar duas fontes incompatíveis sem autoridade suficiente e exigir incerteza explícita.

## T075:C04 — perguntas_proveniencia

Pergunta: Reconciliar significa apagar a versão perdedora?
Resposta: Não necessariamente. Manter o histórico ajuda a explicar por que a conclusão mudou.

Pergunta: Um modelo pode resolver todos os conflitos?
Resposta: Não. Alguns exigem fonte adicional ou decisão autorizada; o sistema deve representar esse bloqueio.

Pergunta: A memória mais recente deve sempre vencer?
Resposta: Não. Ela pode ser uma cópia atrasada, hipótese ou erro. Compare autoridade, validade, identidade e evidências antes de decidir.

Pergunta: Posso repetir usando uma nova chave de operação?
Resposta: Uma nova chave pode representar outra ação e duplicar o efeito. Reutilize identidade conforme o contrato do provedor e investigue o resultado anterior.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T075:C05 — mecanismo_avancado

Reconciliação envolve observações incompletas, além de contradições textuais. Uma operação externa pode ter sido aplicada enquanto sua confirmação se perdeu; o estado local fica desconhecido, não fracassado. A reconciliação busca recibo ou estado remoto usando identidade estável da operação, registra o resultado observado e só então decide continuidade. Para conhecimento, a mesma disciplina separa correção temporal, disputa de fonte e simples duplicação.

Condição de contorno:
Sem identificador correlacionável ou interface de consulta do serviço, pode ser impossível determinar automaticamente se um efeito ocorreu; a incerteza deve permanecer explícita.

Contrato proposto:
- Entradas: Registros divergentes, identidades, versões, tempos e observações de fontes autoritativas.
- Saídas: Estado reconciliado ou disputa persistente, com justificativa e evidências da decisão.
- Estado: Tentativas, chaves de operação, revisões corrigidas e derivados que precisam invalidação.
- Invariante: Ausência de confirmação local nunca é convertida automaticamente em prova de não execução externa.

Compromissos de projeto:
- Consultar a fonte autoritativa reduz duplicação e acrescenta latência e dependência de disponibilidade.
- Resolução automática acelera convergência e precisa ser limitada quando autoridade ou identidade permanecem ambíguas.

## T075:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: simular sucesso remoto seguido de perda da resposta e reinício local. A reconciliação deve consultar o efeito pela identidade conhecida, evitando reenviar cegamente ou compensar algo cujo resultado ainda não foi confirmado.

Plano de avaliação proposto:
Avaliação proposta: comparar última escrita vence e reconciliação por identidade e evidência em duplicatas, atualizações e resultados incertos. Medir convergência correta, efeitos duplicados, conflitos preservados e tempo; incluir fontes indisponíveis e recibos atrasados.

Comparações:
- T065 (complements): Transações protegem estado local; reconciliação observa o que ocorreu fora dessa fronteira.
- T058 (complements): Consolidações dependentes devem ser reavaliadas quando a reconciliação muda o conhecimento vigente.

Afirmação rastreável:
A documentação de tolerância a falhas do LangGraph orienta tratar confirmação perdida como resultado desconhecido e consultar o provedor.
Suporte: direct; fontes: V3A-S030
Limite: Isso não fornece uma solução automática para qualquer serviço; deduplicação e consulta dependem das garantias da API externa.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T075:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou ACK perdido. Aqui reconciliação separa conflito epistemológico, conflito de versão e efeito externo incerto.

Projeto e decomposição
Cada classe exige evidência diferente. Versões concorrentes pedem regra de atualização; afirmações contraditórias pedem fontes; efeito externo incerto pede consulta ao sistema que executou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

Controle adaptativo
Não resolva tudo por última escrita ou votação. Uma correção tardia pode ser mais válida que relato recente; várias cópias da mesma origem não constituem consenso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

Validação contrafactual
Compare reconciliador genérico e rotas tipadas. Meça duplicação de efeitos, perda de correções e conflitos encerrados sem evidência; incluir estado explicitamente inconclusivo. Unidade de avaliação: conflito ou operação incerta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

USO AVANÇADO — Memórias contraditórias
Cenário: Agentes registram fatos incompatíveis.
Estratégia: Agrupar pelo mesmo sujeito e escopo, comparar fontes e preservar alternativas quando não houver critério decisivo.
Papel do modelo pequeno: 8–14B explica conflito.
Aceite proposto: Não escolher fato apenas por formulação mais confiante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

USO AVANÇADO — Operação sem recibo
Cenário: A chamada externa pode ter concluído.
Estratégia: Consultar por identificador estável; se status não for determinável, suspender retry e registrar resolução necessária. Compensação também é novo efeito controlado.
Papel do modelo pequeno: 3–7B classifica status; controlador decide.
Aceite proposto: Nenhum reenvio cego pode criar efeito duplicado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipos de conflito e estados observados.
8–14B: Reconciliador de afirmações com fontes e escopos explícitos.
15–30B: Planejador de resolução complexa, mantendo efeitos sob protocolo determinístico.
Requisitos de treino/runtime: Identidade de operação, versões e evidência externa consultável; registrar desconhecido como estado válido.
Não aplicar quando: A aplicação exige conclusão definitiva sem acesso a informação que decide o conflito.

## T075:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C007 — Amazon / Dynamo em serviços Amazon
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores descrevem adoção de Dynamo por serviços centrais da Amazon.
Mecanismo documentado: Versionamento de objetos e resolução de conflitos assistida pela aplicação.
Correspondência com esta base: Conflitos de objetos são resolvidos pela aplicação; não confirma reconciliação de efeitos LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Apresentar versões concorrentes ao reconciliador pequeno sem permitir que ele descarte evidência sozinho.
Limite: Dynamo histórico não equivale a todos os produtos DynamoDB; particionamento por hash não é CAS. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S006.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: Detecção de versões divergentes fundamenta reconciliação de estado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q006, V4A-Q007.

## T075:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T075 → T243 [requires]
Como combinar: Tratar efeitos incertos pelo protocolo do serviço.
Interface: operation_id, consulta de status e recibos.
Condição: Serviço oferecer mecanismo ou intervenção definida.
Aceite proposto: Simular efeito concluído com resposta perdida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S006, V4A-S011, V2A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T075 → T056 [complements]
Como combinar: Separar recência do relato e validade do fato.
Interface: Tempos de validade, registro e fonte.
Condição: Escopos temporais serem comparáveis.
Aceite proposto: Inserir correção tardia e impedir vitória automática do último relato.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S006, V4A-S011, V2A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter timeout em falha confirmada.
- Não executar compensação antes de saber qual efeito ocorreu.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar resolução correta e preservação de incerteza; eloquência não resolve estado externo desconhecido.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T054, T056, T058, T072

## Fontes primárias associadas

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S035 — Graphiti: Build Real-Time Knowledge Graphs for AI Agents

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grafo temporal de entidades, relações e episódios com rastreabilidade.

Limite: README consultado; sem auditoria de código, teste de escala ou confirmação de promessas comerciais.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S006 — Dynamo: Amazon’s highly available key-value store

[https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso em serviços Amazon; versões de objetos e resolução de conflitos pela aplicação.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T076 — Git-Backed Memory

**Nome canônico:** Git-Backed Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T076  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória versionada em Git

## T076:C01 — conceito

Usa um repositório Git para versionar arquivos de memória, possibilitando histórico, comparação, revisão e sincronização. Letta MemFS é uma implementação concreta desse tipo. Git organiza revisões dos arquivos; não verifica por si só a verdade dos fatos ou a adequação de uma memória.

Como funciona:
- Representar memórias em arquivos com identidade estável.
- Registrar alterações em commits e manter referências de versão.
- Sincronizar e resolver conflitos antes de usar a memória como vigente.

## T076:C02 — aplicacao

Quando usar:
- Memória textual e procedural revisada por pessoas ou agentes.
- Necessidade de comparar alterações e reverter versões.

Quando não usar:
- Não tratar Git como substituto automático de banco transacional para eventos de alta frequência.

Implementação proposta:
- Proposta: separar arquivos essenciais de referências carregadas sob demanda.
- Usar commits pequenos com motivo e fonte das mudanças.
- Evitar sobrescrita concorrente e definir como resolver conflitos sem escolher texto arbitrariamente.

Aplicação LAI proposta:
Proposta LAI: usar versionamento de arquivos para skills e decisões textuais, enquanto eventos de execução podem ficar em armazenamento mais apropriado à carga.

## T076:C03 — riscos_validacao

Armadilhas:
- Uma edição local não sincronizada pode não existir para outro agente.
- Histórico pode reter conteúdo que deveria ter política de retenção específica.

Métricas sugeridas:
- Conflitos de sincronização e tempo até disponibilidade.
- Proporção de memórias ligadas a commits e evidências.

Testes propostos:
- Editar em dois checkouts e exigir resolução explícita da divergência.
- Retomar por commit conhecido e obter o mesmo conjunto de arquivos.

## T076:C04 — perguntas_proveniencia

Pergunta: Commit local significa que todos os agentes já recebem a mudança?
Resposta: Não. Sincronização e atualização do checkout do consumidor precisam ocorrer.

Pergunta: Git impede uma memória falsa?
Resposta: Não. Ele permite rastrear a introdução e a correção, mas a validação factual é outra responsabilidade.

Pergunta: Commit local significa que outro agente recebeu a memória?
Resposta: Não. É necessário publicar e atualizar o checkout consumidor conforme o fluxo de sincronização; registre ambos os estados quando a continuidade depender disso.

Pergunta: Uma branch antiga pode continuar sendo útil?
Resposta: Sim, para reprodução ou experimentação. Identifique seu propósito e impeça que seja confundida com a revisão vigente para decisões operacionais.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T076:C05 — mecanismo_avancado

Git fornece objetos versionados e referências mutáveis; a memória visível depende de qual commit foi publicado e de qual checkout o leitor usa. Atualizações condicionais de referência podem detectar concorrência verificando o identificador anterior. Mesmo transações de múltiplas referências não devem ser confundidas com uma visão atômica de todos os arquivos e serviços externos para qualquer leitor concorrente. A fronteira de consistência precisa ser explicitada.

Condição de contorno:
Git não resolve conflitos semânticos: duas alterações sem conflito textual podem introduzir regras incompatíveis, duplicar fatos ou remover uma condição importante.

Contrato proposto:
- Entradas: Arquivos de memória, commit de base, alterações justificadas e política de publicação.
- Saídas: Commit revisável, referência atualizada sob condição conhecida e estado de sincronização registrado.
- Estado: Branches, worktrees, histórico, conflitos e revisões usadas por cada consumidor.
- Invariante: Integração bem-sucedida de texto não é declarada como validação factual da memória resultante.

Compromissos de projeto:
- Diffs permitem revisão precisa e podem ocultar mudanças de sentido em pequenas edições.
- Worktrees isolam trabalho paralelo e exigem integração explícita e avaliação de conflitos entre conclusões.

## T076:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois agentes alteram cláusulas diferentes que juntas tornam um procedimento contraditório. O merge pode ser textualmente limpo, mas a validação semântica deve impedir sua promoção como procedimento confirmado.

Plano de avaliação proposto:
Avaliação proposta: comparar edição compartilhada direta e branches com revisão em mudanças concorrentes. Medir sobrescritas, conflitos detectados, tempo até sincronização e inconsistências semânticas; verificar quais commits cada agente realmente leu.

Comparações:
- T053 (complements): Notas em arquivo ganham histórico e integração; ainda precisam de contrato de estado e interpretação.
- R013 (complements): MemFS aplica Git à memória de agentes com organização e carregamento próprios.

Afirmação rastreável:
git-update-ref permite verificar old-oid antes de alterar uma referência; a documentação distingue atomicidade individual e observações de leitores concorrentes.
Suporte: direct; fontes: V3A-S040
Limite: Essa primitiva não substitui validação de conteúdo, sincronização remota ou uma transação distribuída entre Git e outros serviços.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T076:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou compare-and-set e worktrees. Aqui Git organiza propostas de memória em commits com semântica revisável e escopo limitado.

Projeto e decomposição
Cada commit deve representar mudança compreensível: fato corrigido, procedimento validado ou índice atualizado. Misturar grandes reorganizações com mudança de significado dificulta auditoria e rollback.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, A-S028, A-S010.

Controle adaptativo
Use revisão-base na proposta e validação semântica após merge. Git resolve texto; relações entre arquivos podem permanecer inconsistentes mesmo quando nenhum conflito textual aparece.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, A-S028, A-S010.

Validação contrafactual
Compare commits por etapa e grandes snapshots periódicos. Meça localização de regressões, reversões seguras e perda de proveniência; histórico extenso não garante que cada conclusão tenha suporte. Unidade de avaliação: commit de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, A-S028, A-S010.

USO AVANÇADO — Memória colaborativa
Cenário: Agentes editam módulos distintos.
Estratégia: Trabalhar em branches separados, validar links cruzados e integrar por manifesto que fixa versões dos módulos.
Papel do modelo pequeno: 8–14B revisa diffs.
Aceite proposto: Merge deve detectar decisões incompatíveis em arquivos diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, A-S028, A-S010.

USO AVANÇADO — Experimento de consolidação
Cenário: Nova síntese pode perder informação.
Estratégia: Criar branch candidato, comparar consultas e revisar diff de afirmações antes de atualizar referência ativa.
Papel do modelo pequeno: 15–30B integra; 3–7B extrai diferenças.
Aceite proposto: Reversão deve restaurar memória e índices coerentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S040, A-S028, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de mudanças em diffs curtos por seção.
8–14B: Revisor de alterações locais e referências quebradas.
15–30B: Integrador de conflitos semânticos entre vários arquivos.
Requisitos de treino/runtime: Repositório, manifesto e política de commits; Git não fornece sozinho autorização, busca semântica ou verdade.
Não aplicar quando: Histórico contém dados que não deveriam ser persistidos ou merge é tratado como confirmação factual.

## T076:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: Versionamento Git explicitado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q019, V4A-Q023, V4A-Q026.

## T076:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T076 → T072 [feeds]
Como combinar: Publicar revisão de memória com manifesto completo.
Interface: Commit, árvore e versões de índices.
Condição: Leitor pinado à revisão adequada.
Aceite proposto: Consultar durante troca de branch e impedir mistura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S040, A-S028, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T076 → T075 [requires]
Como combinar: Reconciliar conflito de significado após merge.
Interface: Diffs, fontes e invariantes entre arquivos.
Condição: Revisão examinar relações, não só linhas conflitantes.
Aceite proposto: Criar duas regras contraditórias em arquivos separados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S040, A-S028, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar commit como prova de execução de tarefa.
- Não presumir que apagar arquivo remove suas versões históricas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar rastreabilidade e custo de revisão; Git melhora colaboração, não capacidade de julgamento do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T053, T055, T072, R002

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S040 — Git git-update-ref Documentation

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional por old-oid e transações de referências; leitores concorrentes ainda podem observar subconjuntos.

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

# T077 — Temporal Knowledge Graphs

**Nome canônico:** Temporal Knowledge Graphs  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T077  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** grafos de conhecimento temporais

## T077:C01 — conceito

Grafos em que entidades ou relações têm validade temporal e, quando necessário, histórico de registro. Permitem perguntar quais relações valiam em determinado momento e como mudaram. Um timestamp de criação isolado não fornece toda essa semântica.

Como funciona:
- Modelar entidades e relações com intervalos e proveniência.
- Registrar mudanças sem confundir correção com evento novo.
- Aplicar filtros temporais durante busca e travessia.

## T077:C02 — aplicacao

Quando usar:
- Dependências e fatos que mudam com versões ou períodos.
- Auditoria de relações históricas entre sistemas e decisões.

Quando não usar:
- Não misturar relações de épocas diferentes em um caminho apresentado como simultaneamente válido.

Implementação proposta:
- Proposta: definir se cada consulta usa tempo de validade, de conhecimento ou ambos.
- Exigir interseção temporal coerente ao compor caminhos.
- Manter evidências e estado de verificação nas arestas, não somente data.

Aplicação LAI proposta:
Proposta LAI: representar qual software consumia qual schema em cada versão; verificar intervalos antes de recomendar compatibilidade.

## T077:C03 — riscos_validacao

Armadilhas:
- Relações antigas podem aparecer em respostas atuais por falta de filtro.
- Expansões do grafo podem combinar versões incompatíveis.

Métricas sugeridas:
- Precisão de consultas históricas e atuais.
- Arestas sem validade e caminhos temporalmente inconsistentes.

Testes propostos:
- Criar uma dependência substituída e consultar antes e depois da mudança.
- Registrar correção tardia e comparar o que era conhecido em duas datas.

## T077:C04 — perguntas_proveniencia

Pergunta: Temporal graph é sempre bitemporal?
Resposta: Não. Pode registrar um único eixo. Bitemporalidade exige distinguir validade e conhecimento ou registro.

Pergunta: Preciso usar um produto específico?
Resposta: Não. Graphiti é uma referência de implementação, mas a modelagem temporal pode existir em outras tecnologias.

Pergunta: Um timestamp de criação resolve validade?
Resposta: Não. Ele indica registro ou criação do objeto. O fato pode ter começado antes, valer depois ou não ter ocorrência confirmada.

Pergunta: Um caminho temporal é causal?
Resposta: Não. Compatibilidade de tempos permite compor relações segundo a consulta; causalidade ainda exige hipóteses e evidências adicionais de identificação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T077:C05 — mecanismo_avancado

A semântica de um caminho temporal depende da pergunta. Para relações simultâneas, os intervalos das arestas precisam ter interseção: com intervalos semiabertos, o maior início deve ser menor que o menor fim. Para uma trajetória ao longo do tempo, pode ser necessário apenas respeitar a ordem dos eventos. Além disso, promessa atual sobre evento futuro não equivale a ocorrência futura já confirmada.

Condição de contorno:
Aplicar a mesma regra temporal a toda consulta pode excluir trajetórias válidas ou produzir relações simultâneas que nunca coexistiram.

Contrato proposto:
- Entradas: Entidades, arestas com validade e origem, perspectiva de conhecimento e tipo de consulta temporal.
- Saídas: Caminhos ou relações com intervalos compatíveis e evidências que distinguem planos de fatos ocorridos.
- Estado: Histórico de invalidação, referência temporal dos episódios e regras de interpretação dos campos.
- Invariante: O sistema não transforma intenção, prazo ou promessa em evidência de que o evento descrito aconteceu.

Compromissos de projeto:
- Arestas temporais permitem reconstrução precisa e aumentam complexidade de filtros e junções.
- Preservar relações invalidadas facilita auditoria e exige que consultas atuais excluam as versões inadequadas.

## T077:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar uma promessa hoje para uma entrega futura e depois registrar cancelamento. A consulta sobre compromissos deve reconhecer a promessa; a consulta sobre entregas realizadas não pode contar essa ocorrência.

Plano de avaliação proposto:
Avaliação proposta: comparar consultas de snapshot e trajetórias ordenadas em dados com intervalos não sobrepostos. Medir coerência temporal, atualização após cancelamento e recuperação de proveniência; incluir fatos descobertos tardiamente para testar o eixo de conhecimento.

Comparações:
- T056 (complements): Bitemporalidade acrescenta a perspectiva do que era conhecido às relações válidas no domínio.
- T051 (specializes): O grafo temporal especializa a representação relacional com regras explícitas de validade e evolução.

Afirmação rastreável:
EntityEdge no Graphiti diferencia valid_at, invalid_at, expired_at e reference_time e documenta tratamento específico para planos futuros.
Suporte: direct; fontes: V3A-S043
Limite: Os nomes e interpretações são da revisão consultada; não constituem padrão universal para todo grafo temporal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T077:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu intervalos e jornadas temporais. Aqui grafos temporais modelam incerteza de datas e respostas condicionadas à resolução disponível.

Projeto e decomposição
Represente datas aproximadas como intervalos ou limites, sem inventar dia exato. Relação que vale em algum ponto do mês não prova simultaneidade com outra relação de data desconhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

Controle adaptativo
Separe tempo do evento, validade da relação e momento de conhecimento. Caminhos precisam declarar se buscam coexistência, sequência possível ou sequência comprovada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

Validação contrafactual
Compare datas pontuais imputadas e intervalos explícitos. Meça relações temporais falsas, respostas inconclusivas corretas e vazamento de conhecimento futuro; ordem temporal não implica causalidade. Unidade de avaliação: caminho temporal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

USO AVANÇADO — Histórico de responsabilidades
Cenário: Documentos informam mudanças com datas incompletas.
Estratégia: Construir relações com intervalos sustentados e responder quem podia ser responsável, distinguindo certeza de possibilidade.
Papel do modelo pequeno: 3–7B extrai datas; banco calcula.
Aceite proposto: Não afirmar responsável único quando intervalos permitem alternativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

USO AVANÇADO — Rastreio de dependências
Cenário: É preciso explicar cadeia de mudanças.
Estratégia: Consultar sequência de eventos com ordenação confirmada e marcar trechos cuja ordem não é decidível.
Papel do modelo pequeno: 8–14B explica caminho.
Aceite proposto: Cada salto temporal deve respeitar relações de ordem observadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de expressões temporais com indicação de precisão.
8–14B: Leitor de caminhos já filtrados por lógica temporal.
15–30B: Analista de alternativas quando intervalos e perspectivas produzem múltiplas histórias possíveis.
Requisitos de treino/runtime: Álgebra temporal, campos de precisão e identidade de relações; LLM não deve decidir sozinho interseções de intervalos.
Não aplicar quando: A aplicação exige cronologia exata a partir de fontes que só fornecem datas aproximadas.

## T077:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Tempo lógico orienta processamento; não é grafo temporal de conhecimento.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q015, V4A-Q025.

## T077:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T077 → T056 [requires]
Como combinar: Aplicar perspectiva de conhecimento ao grafo.
Interface: Validade, registro e instante da pergunta.
Condição: Consulta declarar os dois tempos.
Aceite proposto: Adicionar descoberta posterior e impedir alteração da história conhecida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S035, V3A-S043, A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T077 → T057 [conflicts]
Como combinar: Evitar converter sequência em causa.
Interface: Caminho temporal e hipótese causal separada.
Condição: Causalidade exigir identificação adicional.
Aceite proposto: Apresentar eventos ordenados sem mecanismo e exigir ressalva causal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S035, V3A-S043, A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não preencher data desconhecida com data de ingestão.
- Não confundir plano futuro com evento ocorrido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar raciocínio temporal sobre intervalos; modelos maiores também podem inventar precisão se schema não preservar incerteza.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T029, T051, T056, T072

## Fontes primárias associadas

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S035 — Graphiti: Build Real-Time Knowledge Graphs for AI Agents

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grafo temporal de entidades, relações e episódios com rastreabilidade.

Limite: README consultado; sem auditoria de código, teste de escala ou confirmação de promessas comerciais.

### V3A-S043 — Graphiti EntityEdge implementation

[https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py](https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campos valid_at, invalid_at, expired_at, reference_time, episódios e contrato temporal das relações; código lido, não executado.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V3A-S035 — Zep: A Temporal Knowledge Graph Architecture for Agent Memory

[https://arxiv.org/abs/2501.13956](https://arxiv.org/abs/2501.13956)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura temporal Graphiti para integração de conversas e dados estruturados com relações históricas.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T078 — Semantic Page Fault

**Nome canônico:** Semantic Page Fault  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T078  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** falta semântica de página; lacuna de contexto

## T078:C01 — conceito

Analogia de engenharia para o momento em que uma ação precisa de informação que não está no contexto ativo. Diferentemente de uma falta de página convencional, a ausência semântica pode não ser detectável de forma exata: o modelo pode desconhecer o que está faltando. Não é um padrão universal estabelecido.

Como funciona:
- Detectar uma dependência, referência ou campo necessário ausente.
- Solicitar recuperação da informação externa correspondente.
- Revalidar suficiência do contexto antes de continuar a ação.

Nota de nomenclatura: Analogia arquitetural relacionada à memória virtual do MemGPT; não se afirma que o paper padroniza esse rótulo ou garante detecção de toda lacuna.

## T078:C02 — aplicacao

Quando usar:
- Agentes com memória hierárquica e referências externas.
- Diagnóstico de falhas causadas por informação não carregada.

Quando não usar:
- Não interpretar confiança do modelo como prova de que nenhuma informação necessária está ausente.

Implementação proposta:
- Proposta: criar pré-condições verificáveis para ações críticas.
- Manter campos unknown e missing_reference explícitos no estado.
- Limitar tentativas de recuperação e retornar bloqueio ou incerteza quando a lacuna não puder ser resolvida.

Aplicação LAI proposta:
Proposta LAI: usar o conceito como evento de observabilidade da Helena, por exemplo falta de versão do schema, sem apresentá-lo como capacidade automática do Qwen.

## T078:C03 — riscos_validacao

Armadilhas:
- O sistema pode não reconhecer que há uma dependência omitida.
- Uma busca irrelevante pode ser tratada como resolução da lacuna.

Métricas sugeridas:
- Lacunas relevantes detectadas antes da execução.
- Taxa de recuperação suficiente e falsos sinais de resolução.

Testes propostos:
- Remover uma referência obrigatória de contrato e impedir a ação dependente.
- Fornecer resultado de busca sem a informação pedida e manter a lacuna aberta.

## T078:C04 — perguntas_proveniencia

Pergunta: Semantic page fault é um recurso nativo da LLM?
Resposta: Não como propriedade universal. É uma analogia que precisa de detecção e recuperação implementadas no sistema.

Pergunta: Por que a analogia com sistema operacional é limitada?
Resposta: O endereço de uma página faltante é explícito; a informação semântica necessária pode depender de interpretação e ser desconhecida do agente.

Pergunta: A falta pode ser resolvida por um resumo?
Resposta: Sim, se o resumo contém suporte suficiente e verificável para a dependência. Quando exige detalhe exato, é necessário abrir a fonte correspondente.

Pergunta: O que fazer quando nenhuma busca resolve?
Resposta: Preserve o estado desconhecido, registre tentativas e encerre a etapa conforme sua política. Não transforme esgotamento de orçamento em evidência de ausência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T078:C05 — mecanismo_avancado

Semantic Page Fault é uma analogia útil para distinguir dependência identificável e lacuna semântica. A primeira pode ser verificada por contrato: falta uma versão, um resultado ou uma evidência obrigatória. A segunda depende de perceber que algo relevante está ausente, tarefa sujeita a falsos negativos. O controlador deve registrar a razão da busca e a condição observável que permitirá declarar a lacuna resolvida.

Condição de contorno:
Não existe detector universal que saiba tudo que o modelo deixou de considerar; ausência de alarme não comprova suficiência do contexto.

Contrato proposto:
- Entradas: Ação pretendida, pré-condições, contexto ativo e referências potencialmente necessárias.
- Saídas: Pedido de recuperação com critério de resolução, ou bloqueio explícito por dependência não satisfeita.
- Estado: Lacunas abertas, tentativas, evidências obtidas e orçamento de expansão.
- Invariante: Encontrar qualquer resultado parecido não basta para marcar como satisfeita a dependência originalmente ausente.

Compromissos de projeto:
- Regras determinísticas cobrem dependências conhecidas e não detectam todos os pressupostos implícitos.
- Sinais do modelo ampliam cobertura e podem gerar alarmes falsos ou buscas sem progresso.

## T078:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: retornar um documento semanticamente próximo que não contém a versão exigida pela ação. O controlador deve manter a falta aberta e impedir que o agente trate similaridade como resolução.

Plano de avaliação proposto:
Avaliação proposta: comparar gatilho apenas verbal, pré-condições explícitas e combinação dos dois. Medir dependências ausentes detectadas, alarmes falsos, custo de busca e ações indevidas; incluir casos de confiança alta sem evidência suficiente.

Comparações:
- T063 (complements): Gerência virtual fornece operações para trazer conteúdo; a analogia trata a decisão de perceber e resolver sua ausência.
- T044 (complements): Expansão progressiva pode executar a busca motivada por uma lacuna identificada.

Afirmação rastreável:
MemGPT usa níveis externos e operações explícitas de recuperação para trabalhar com conteúdo além da janela ativa.
Suporte: related; fontes: A-S009
Limite: A fonte sustenta a inspiração arquitetural, não estabelece Semantic Page Fault como padrão formal nem garante detecção de faltas semânticas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T078:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu Semantic Page Fault como analogia. Aqui o evento recebe critérios de detecção e resolução específicos por contrato de tarefa.

Projeto e decomposição
Detecte falta por requisito explícito: referência não aberta, campo obrigatório ausente ou conflito não resolvido. Não existe detector universal que saiba toda informação que o modelo deveria ter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Controle adaptativo
Uma carga resolve a falta apenas se satisfizer o requisito registrado. Conteúdo parecido pode aumentar tokens sem remover o bloqueio; manter estado aberto evita falso progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Validação contrafactual
Compare detecção por autoconfiança e por contrato. Meça faltas reais detectadas, alarmes indevidos e conclusões emitidas antes da resolução; incluir perguntas sem fonte disponível. Unidade de avaliação: lacuna semântica registrada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Resposta com citação
Cenário: Modelo possui título mas não conteúdo.
Estratégia: Gerar falta de evidência, resolver referência e ler trecho antes de redigir afirmação factual. Se indisponível, declarar lacuna.
Papel do modelo pequeno: 3–7B verifica campos.
Aceite proposto: Nenhuma citação pode ser validada só pelo nome do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Execução de procedimento
Cenário: Falta pré-condição para próxima ação.
Estratégia: Suspender etapa, buscar dado específico e testar condição; se fonte retornar algo inconclusivo, manter bloqueio.
Papel do modelo pequeno: 8–14B identifica necessidade.
Aceite proposto: Ação só avança quando a pré-condição observável estiver satisfeita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Detector de campos obrigatórios ausentes em schema fechado.
8–14B: Detector de contradição ou referência insuficiente em pacote curto.
15–30B: Planejador de como resolver lacunas interdependentes, com orçamento e parada.
Requisitos de treino/runtime: Contrato de tarefa, estados aberto/resolvido/indisponível e ferramenta de resolução; nomenclatura é editorial.
Não aplicar quando: A aplicação trata confiança subjetiva como prova de completude ou não possui fonte capaz de resolver a falta.

## T078:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa avalia gestão de contexto virtual em documentos e conversas.
Mecanismo documentado: Ferramentas movimentam informação entre janela e armazenamento externo.
Correspondência com esta base: Semantic Page Fault é rótulo editorial inspirado em necessidade de informação.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.
Limite: Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T078:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T078 → T066 [requires]
Como combinar: Resolver identidade e abrir conteúdo faltante.
Interface: Requisito, referência, versão e seletor.
Condição: Abertura verificar o conteúdo esperado.
Aceite proposto: Retornar recurso homônimo e manter falta aberta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T078 → T044 [feeds]
Como combinar: Expandir contexto com objetivo de resolver lacuna.
Interface: Lacuna, candidatos e orçamento restante.
Condição: Expansão vinculada à decisão bloqueada.
Aceite proposto: Carregar trecho irrelevante e impedir marcação como resolvido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar analogia como padrão universal de memória virtual.
- Não chamar toda baixa confiança de page fault.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar completude verificável por contrato; esse mecanismo organiza necessidades, não descobre automaticamente todos os desconhecidos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T044, T062, T063, T067

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

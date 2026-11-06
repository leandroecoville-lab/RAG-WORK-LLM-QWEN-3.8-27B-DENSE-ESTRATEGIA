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

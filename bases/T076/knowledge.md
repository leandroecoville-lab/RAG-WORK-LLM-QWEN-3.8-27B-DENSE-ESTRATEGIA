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

# R014 — Letta Context Repositories

**Nome canônico:** Letta MemFS — Context Repositories  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Letta context repository; Context Repositories da Letta

## R014:C01 — conceito

Context Repositories é o nome apresentado pela Letta para memória do agente organizada em repositório Git e arquivos locais. A documentação de MemFS declara explicitamente a equivalência de nomes. Esta entrada preserva a referência solicitada no inventário e destaca colaboração e versionamento; não representa um produto independente adicional ao MemFS.

Como funciona:
- O repositório permite inspecionar mudanças de memória por diff e manter histórico de revisões.
- O anúncio descreve subagentes em worktrees separados, com alterações posteriormente integradas ao repositório compartilhado.
- Hierarquia, descrições e índices orientam a seleção de contexto, enquanto o conteúdo aprofundado permanece disponível para consulta.

Nota de nomenclatura: Alias relacionado explicitamente ao canonical_id R013. O blog é histórico; regras operacionais atuais devem ser verificadas na documentação de MemFS.

## R014:C02 — aplicacao

Quando usar:
- Comparação de padrões de memória colaborativa e rastreamento de decisões textuais.
- Projetos com vários agentes contribuindo para conhecimento persistente sobre o mesmo código.

Quando não usar:
- Para contabilizar duas soluções distintas quando MemFS e Context Repositories aparecem na mesma lista.

Implementação proposta:
- Proposta: mapear este nome para R013 no catálogo e conservar a origem do anúncio como referência histórica.
- Distribuir assuntos por escritor, criar worktrees e exigir fonte e justificativa em cada mudança de memória.
- Revisar conflitos semânticos após o merge: dois arquivos podem discordar mesmo quando o Git não apresenta conflito textual.

Aplicação LAI proposta:
Proposta LAI: usar esta ficha para esclarecer nomenclatura e avaliar escrita paralela de memória, com integração condicionada à validação das evidências.

## R014:C03 — riscos_validacao

Armadilhas:
- O anúncio descreve uma organização antiga com system/; implementar a estrutura da documentação correspondente à versão instalada.
- Merge sem conflito não comprova coerência, atualidade ou isolamento entre clientes; duplicar aliases pode inflar a recuperação.

Métricas sugeridas:
- Duplicação de fichas canônicas, divergências de fatos, tempo de integração e precisão da memória recuperada.

Testes propostos:
- Proposta: pesquisar ambos os nomes e confirmar a resolução ao mesmo conceito, preservando as duas referências.
- Criar conclusões incompatíveis em worktrees separados e testar se a revisão detecta a contradição após integrar os arquivos.

## R014:C04 — perguntas_proveniencia

Pergunta: Context Repositories é um produto autônomo?
Resposta: A fonte atual o apresenta como outro nome de MemFS; esta base não cria um terceiro produto.

Pergunta: Worktrees resolvem contradições de memória?
Resposta: Eles isolam alterações. Resolver contradições exige comparar significado, evidência e validade temporal, além de integrar o Git.

Pergunta: Por que manter duas fichas se são aliases?
Resposta: Para preservar o inventário solicitado e permitir busca pelos dois nomes. A identidade canônica impede contabilizar duas tecnologias onde há uma equivalência nominal.

Pergunta: Merge sem conflito significa memória correta?
Resposta: Não. Git verifica compatibilidade textual de mudanças. Regras contraditórias, escopo errado ou fontes frágeis precisam de validação do conteúdo.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R014:C05 — mecanismo_avancado

Esta entrada é um alias de R013, não um segundo produto. Seu foco complementar é a colaboração: worktrees podem isolar alterações de memória, mas integrar texto não valida conclusões. Também é necessário distinguir o context repository individual do agente de um shared memory repository organizacional. Ambos usam Git, porém propriedade, leitores e sincronização são contratos diferentes; compartilhar o mesmo formato não torna o escopo automaticamente comum.

Condição de contorno:
Colaboração perde coerência quando agentes leem commits diferentes sem registrar a revisão, ou quando uma integração textual limpa combina conclusões incompatíveis.

Contrato proposto:
- Entradas: Repositório e proprietário, commits de base, mudanças de agentes e política de integração.
- Saídas: Revisão integrada com conflitos resolvidos explicitamente e registro de publicação aos consumidores.
- Estado: Worktrees, branches, commits lidos, revisões pendentes e associação de agentes aos repositórios.
- Invariante: Alias R014 resolve para R013; colaboração não aumenta a contagem de mecanismos independentes de memória.

Compromissos de projeto:
- Worktrees permitem pesquisa paralela e tornam necessárias integração e revisão de dependências.
- Repositórios compartilhados reduzem duplicação de conhecimento e ampliam o impacto de uma memória incorreta publicada.

## R014:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois agentes alteram regras em arquivos distintos, produzindo incompatibilidade sem conflito de linhas. A revisão deve detectar o problema antes de publicar uma versão recomendada aos demais agentes.

Plano de avaliação proposto:
Avaliação proposta: comparar manutenção por um agente e trabalho paralelo com integração em tarefas equivalentes. Medir conflitos semânticos, tempo até convergência, revisões efetivamente lidas e correções propagadas; controlar a quantidade total de trabalho para não confundir paralelismo com qualidade.

Comparações:
- R013 (complements): É a mesma referência canônica; esta ficha acrescenta o recorte de colaboração e publicação.
- T076 (specializes): O uso de Git para memória concretiza versionamento e sincronização, mantendo necessidade de revisão factual.

Afirmação rastreável:
MemFS é chamado context repository; Letta distingue memória individual e repositórios compartilhados e documenta commit, push e pull entre checkouts.
Suporte: direct; fontes: A-S010, V3A-S046
Limite: A equivalência de nomes não torna repositórios individuais e organizacionais idênticos em propriedade ou acesso.

Nota de pesquisa:
Alias preservado: R014 → R013 conforme declaração explícita de MemFS na documentação Letta. O anúncio Context Repositories foi reaberto e a página atual Shared memory foi consultada para separar colaboração em memória individual de repositórios organizacionais. Nenhum produto independente foi inventado; contratos e testes são propostas.

## R014:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 registrou R014 como alias de R013. Aqui a novidade é controlar esse alias no catálogo e evitar duplicação de memória, métricas e casos.

Projeto e decomposição
Mantenha uma identidade canônica para MemFS/Context Repositories no escopo editorial adotado. Consultas pelos dois nomes devem chegar à mesma implementação e às mesmas versões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Controle adaptativo
Apresente diferenças de terminologia como metadados, sem criar um segundo pipeline de memória. Duplicar catálogos pelo alias pode gerar duas cópias divergentes da mesma regra.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Validação contrafactual
Compare resolução com e sem normalização de alias. Meça resultados duplicados, referências inconsistentes e contagem inflada de casos; nomes distintos não demonstram implantações independentes. Unidade de avaliação: alias de componente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Migração de documentação
Cenário: Equipe usa nomes diferentes para a mesma família.
Estratégia: Resolver nomes antigos para identidade canônica, preservar histórico e exibir fonte que fixa escopo. Não alterar conteúdo só para adequar rótulo.
Papel do modelo pequeno: 3–7B normaliza termos.
Aceite proposto: Consulta por qualquer alias deve retornar mesma revisão elegível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Grafo de combinações
Cenário: Catálogo precisa mostrar relações entre técnicas.
Estratégia: Colapsar alias antes de calcular cobertura e impedir aresta que sugira composição entre cópias do mesmo componente.
Papel do modelo pequeno: 8–14B explica equivalência editorial.
Aceite proposto: Não contar R013 e R014 como dois casos ou duas camadas técnicas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Resolvedor de nomes para IDs canônicos em vocabulário fechado.
8–14B: Leitor que explica diferenças de nomenclatura sem inventar capacidades.
15–30B: Revisor de migrações de catálogo com versões históricas e escopos diferentes.
Requisitos de treino/runtime: Tabela de aliases e escopo editorial explícito; revisar se documentação futura passar a distinguir produtos materialmente.
Não aplicar quando: Fonte nova indicar produtos diferentes e o catálogo insistir em colapsá-los sem revisão.

## R014:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: Alias editorial da mesma família; não segundo caso.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R014:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R014 → R013 [alternative]
Como combinar: Resolver este nome para a ficha canônica, sem etapa adicional.
Interface: canonical_id=R013, alias e revisão do catálogo.
Condição: Escopo continuar equivalente ao adotado na base.
Aceite proposto: Consultar ambos os nomes e comparar identidade e fontes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R014 → T066 [requires]
Como combinar: Normalizar nome antes de abrir memória correspondente.
Interface: Alias, identidade canônica e versão.
Condição: Resolver preservar histórico de renomeação.
Aceite proposto: Detectar alias apontando para objeto diferente sem evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar dois rótulos para inflar meta de produção.
- Não atribuir a nome editorial capacidades ausentes das fontes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência de resolução e clareza do catálogo; alias não altera capacidade de modelo nem qualidade de memória.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R002, R013, R027, T075, T076, T237, T239

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

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

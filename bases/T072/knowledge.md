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

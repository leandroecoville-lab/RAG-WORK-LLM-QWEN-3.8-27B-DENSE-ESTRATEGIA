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

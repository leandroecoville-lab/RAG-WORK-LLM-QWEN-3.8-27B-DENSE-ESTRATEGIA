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

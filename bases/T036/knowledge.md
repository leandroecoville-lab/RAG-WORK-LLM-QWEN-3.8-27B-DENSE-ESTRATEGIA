# T036 — Query-Aware RAG

**Nome canônico:** Query-Aware RAG  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T036  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RAG orientado à consulta

## T036:C01 — conceito

Adapta recuperação e montagem do contexto à pergunta atual. Pode reescrever a consulta, decompô-la em subperguntas, escolher índices ou selecionar trechos. É uma família de desenhos; a simples existência de uma consulta já condiciona a busca, portanto é preciso especificar qual adaptação adicional foi implementada.

Como funciona:
- Identificar entidades, intenção, data e escopo da pergunta.
- Produzir consultas direcionadas e combinar evidências.
- Verificar se cada parte da pergunta possui suporte antes de gerar resposta.

## T036:C02 — aplicacao

Quando usar:
- Perguntas com múltiplas condições ou dependências.
- Vocabulário do usuário diferente do utilizado nos documentos.

Quando não usar:
- Não reescrever de modo a apagar negação, identidade, intervalo temporal ou requisito de acesso.

Implementação proposta:
- Proposta: guardar consulta original e consultas derivadas.
- Aplicar filtros obrigatórios fora da reescrita probabilística.
- Medir a utilidade de cada expansão, evitando buscas circulares sem nova evidência.

Aplicação LAI proposta:
Proposta LAI: decompor comparações entre técnicas e pedir evidência separada para mecanismo, limites e compatibilidade com o runtime.

## T036:C03 — riscos_validacao

Armadilhas:
- O agente pode buscar apenas confirmação da hipótese inicial.
- Muitas consultas ampliam ruído e custo sem elevar cobertura.

Métricas sugeridas:
- Cobertura das subperguntas e precisão da evidência.
- Custo por resposta correta e número de buscas redundantes.

Testes propostos:
- Perguntar por diferença entre dois conceitos e exigir fonte para ambos.
- Usar uma pergunta negativa ou temporal e confirmar que a reescrita preserva a condição.

## T036:C04 — perguntas_proveniencia

Pergunta: É um algoritmo específico?
Resposta: Não. O nome precisa vir acompanhado das regras concretas de adaptação.

Pergunta: Como evitar confirmação seletiva?
Resposta: Buscar evidências que poderiam refutar a hipótese e registrar lacunas e fontes conflitantes.

Pergunta: A hipótese deve aparecer na resposta?
Resposta: Somente se identificada como hipótese e útil ao raciocínio comunicado. Não deve ser citada como descoberta documental.

Pergunta: Uma expansão pode adicionar filtros?
Resposta: Pode propor filtros opcionais, mas não trocar restrições explícitas. Identidade, período e autorização devem ser controlados fora da geração livre.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T036:C05 — mecanismo_avancado

Uma adaptação concreta é HyDE: gerar um documento hipotético para a pergunta, codificá-lo e buscar documentos reais próximos. O texto gerado pode conter falsidades; sua função é oferecer uma representação de busca. A decisão final precisa voltar às fontes recuperadas. Preservar consulta original e expansões permite diagnosticar deriva, especialmente quando a hipótese acrescenta uma entidade ou solução que o usuário não informou.

Condição de contorno:
A expansão tende a prejudicar quando a pergunta depende de identificador exato, versão específica ou exceção que o gerador substitui por uma resposta típica.

Contrato proposto:
- Entradas: Pergunta original, restrições obrigatórias e política de geração de consultas derivadas.
- Saídas: Consultas ou hipóteses de busca e evidências reais recuperadas separadamente.
- Estado: Origem de cada candidato, filtros aplicados e revisão dos modelos de expansão.
- Invariante: Conteúdo sintético de expansão nunca serve como prova da própria resposta.

Compromissos de projeto:
- A hipótese amplia correspondência semântica, mas pode aproximar a busca de uma solução errada.
- Buscar também a consulta original aumenta custo e oferece uma comparação útil contra deriva da expansão.

## T036:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: formular pergunta sobre uma versão antiga enquanto a hipótese gerada descreve a atual. Os filtros devem manter a versão solicitada; ausência de evidência deve continuar explícita.

Plano de avaliação proposto:
Avaliação proposta: comparar consulta original, reescrita e HyDE com mesmo orçamento de candidatos. Medir recall elegível, deriva de entidades, preservação de restrições e custo total; inspecionar respostas corretas por acaso apoiadas em documentação incompatível.

Comparações:
- T037 (distinct_from): Adaptar a busca muda candidatos; comprimir para a pergunta seleciona informação depois da recuperação.
- T025 (complements): Um roteador pode decidir quando a expansão compensa, sem alterar filtros obrigatórios.

Afirmação rastreável:
HyDE utiliza um documento hipotético gerado para construir uma representação de consulta e recuperar documentos reais.
Suporte: direct; fontes: V3A-S028
Limite: A codificação da hipótese não oferece garantia de remover toda informação falsa ou recuperar suporte suficiente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T036:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu deriva em HyDE. Aqui a consulta é decomposta em requisitos preserváveis e estratégias de recuperação por requisito.

Projeto e decomposição
Extraia entidades, período, relação pedida e formato esperado antes de reformular. Marque elementos que nenhuma expansão pode alterar, como versão e quantificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

Controle adaptativo
Use consultas diferentes para suporte e contradição. Buscar somente textos que parecem confirmar a hipótese favorece respostas coerentes e incompletas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

Validação contrafactual
Compare consulta original, reformulação única e decomposição por requisito. Meça cobertura e deriva semântica com casos de negação, comparação e restrição temporal. Unidade de avaliação: consulta decomposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

USO AVANÇADO — Pergunta comparativa
Cenário: Usuário pede diferenças com mesma condição.
Estratégia: Criar subconsultas simétricas por item e atributo; impedir que uma opção receba evidência mais ampla que outra.
Papel do modelo pequeno: 3–7B decompõe campos; 8–14B lê respostas.
Aceite proposto: Cobertura deve ser equivalente nos atributos comparados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

USO AVANÇADO — Verificação de afirmação
Cenário: Há suspeita de regra revogada.
Estratégia: Buscar versão vigente, histórico de mudança e fontes contrárias; separar não encontrado de refutado.
Papel do modelo pequeno: 15–30B integra conflito temporal.
Aceite proposto: Conclusão deve refletir escopo e data das evidências.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reformulador controlado com termos protegidos e saídas estruturadas.
8–14B: Decompositor de perguntas compostas com poucas dependências.
15–30B: Planejador de consultas sequenciais quando resposta anterior determina a próxima.
Requisitos de treino/runtime: Esquema de intenção e comparação da reformulação com pedido original; exemplos de negativos ajudam especialização.
Não aplicar quando: Reformulação remove requisitos ou cria documentos hipotéticos tratados como prova.

## T036:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Relevância de cada fonte varia com a consulta.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C008 — Microsoft / Bing: transformers na busca global
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Operador afirma modelos transformer aplicados às consultas Bing globais no período descrito.
Mecanismo documentado: Compreensão contextual de consultas e páginas com inferência otimizada.
Correspondência com esta base: Consulta orienta compreensão e seleção; não comprova leitor RAG específico.
Transferência proposta para modelo pequeno: Proposta de engenharia: Empregar modelo compacto para julgar pares consulta-trecho, medindo custo e ordenação.
Limite: BERT destilado do relato não é um gerador 3–30B; números de infraestrutura não são transportáveis. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S008.

V4A-C023 — IBM / Granite RAG LoRAs experimentais
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Anúncio distingue modelos disponíveis de adaptadores publicados no Granite Experiments.
Mecanismo documentado: Adaptadores para subtarefas como reescrita de consultas e detecção de alucinação.
Correspondência com esta base: Reescrita específica de consulta é subtarefa nomeada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir especialização de 8B por papel sem ativar o mesmo adaptador em tarefas incompatíveis.
Limite: Experimentos não são implantação; não transferir compatibilidade KV de aLoRA a qualquer LoRA. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q010, V4A-Q017, V4A-Q020.

## T036:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T036 → T027 [feeds]
Como combinar: Distribuir subconsultas para canais adequados.
Interface: Termos literais, intenção e filtros comuns.
Condição: Canais preservarem restrições originais.
Aceite proposto: Testar versão alterada durante paráfrase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S009, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T036 → T037 [complements]
Como combinar: Comprimir contexto conforme requisito específico.
Interface: Subconsulta, requisito e trechos recuperados.
Condição: Retorno manter ligação ao pedido global.
Aceite proposto: Conferir que compressões locais não eliminam ponte entre requisitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S009, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar consulta sintetizada como evidência factual.
- Registrar cada reformulação para rastrear perda de condição.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura de requisitos com mesmo acervo; bom planejamento de busca não garante síntese geral superior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T025, T027, T028, T037

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S017 — Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity

[https://aclanthology.org/2024.naacl-long.389/](https://aclanthology.org/2024.naacl-long.389/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Classificador seleciona ausência de busca, busca única ou recuperação iterativa conforme complexidade.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S028 — Precise Zero-Shot Dense Retrieval without Relevance Labels

[https://arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: HyDE gera um documento hipotético para orientar busca em documentos reais; o texto hipotético pode conter falsidades.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S008 — Bing delivers its largest improvement in search experience using Azure GPUs

[https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos transformer aplicados às consultas Bing; inferência otimizada e compreensão da consulta.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

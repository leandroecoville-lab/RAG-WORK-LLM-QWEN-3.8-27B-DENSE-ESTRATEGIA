# Casos públicos e limites de transferência

Um caso pode mapear vários mecanismos; não são implantações independentes. Só produção documentada, correspondência exata e organização do núcleo Big Tech contam na meta estrita. Não há exigência de que todo sistema histórico seja um agente LLM: a transferência para LLM é identificada como proposta.

## V4A-C001 — Google / MapReduce nos clusters Google

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

Artigo dos operadores descreve execução recorrente de jobs nos clusters Google.

**Mecanismo confirmado:** Map por pares, agrupamento por chave e reduce distribuído.

**Transferência proposta:** Proposta de engenharia: Usar extratores pequenos independentes e reduzir registros estruturados; verificar cobertura antes da síntese.

**Limites:** Relato de 2004; não é implantação de redução linguística nem comprovação de escala atual. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T001 | exact | Mesmo modelo de programação map/shuffle/reduce; a adaptação com LLM continua proposta. |

**Fontes:**

- [A-S001 — MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/)

## V4A-C002 — Anthropic / Research multi-agent system

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

A equipe descreve passagem do protótipo à produção do recurso Research.

**Mecanismo confirmado:** Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.

**Transferência proposta:** Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.

**Limites:** Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

**Mesmo caso canônico:** V4C-C007. Não somado novamente por base.

| Base | Correspondência | Justificativa |
|---|---|---|
| T001 | family | Distribuição e agregação de pesquisa, sem garantia de semântica MapReduce. |
| T024 | family | Coordena aquisição e síntese de contexto; não usa o nome editorial como produto. |
| T067 | exact | Novas buscas dependem das descobertas intermediárias. |
| P001 | analogy | Inspira montagem de contexto; não comprova Context Engine LAI. |

**Fontes:**

- [C-S030 — How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system)

## V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.

**Mecanismo confirmado:** Redução da conversa e persistência de informação reutilizável fora da janela.

**Transferência proposta:** Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.

**Limites:** Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T043 | exact | Compactação implementada no produto é explicitada. |
| T047 | exact | Persistência entre sessões é afirmada. |
| T053 | family | Notas externas são família relacionada; não demonstra todos os contratos desta ficha. |
| P002 | analogy | Gestão de janela inspira o componente proposto. |

**Fontes:**

- [V4A-S002 — Context engineering: memory, compaction, and tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [A-S006 — Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

## V4A-C004 — Google / Percolator no índice web

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Artigo afirma implantação do processamento incremental na construção do índice da busca Google.

**Mecanismo confirmado:** Transações distribuídas e notificações organizam pequenas atualizações.

**Transferência proposta:** Proposta de engenharia: Delegar extração a 3–7B e confirmar alterações por transações determinísticas.

**Limites:** Relato histórico; não prova event sourcing, checkpoints de agentes ou resumo incremental correto. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T065 | exact | Confirma gerenciamento transacional de alterações; adaptação para agentes é adicional. |
| T058 | analogy | Atualização incremental inspira consolidação, mas não é consolidação semântica. |

**Fontes:**

- [V4A-S003 — Large-scale Incremental Processing Using Distributed Transactions and Notifications](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)

## V4A-C005 — Google / Megastore em serviços interativos

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Autores relatam serviços Google em produção sobre Megastore.

**Mecanismo confirmado:** Partições recebem semântica ACID serializável e replicação síncrona.

**Transferência proposta:** Proposta de engenharia: Escolher agregado transacional por sessão/projeto e manter decisões do LLM como propostas.

**Limites:** A atomicidade não atravessa automaticamente partições e APIs externas; relato de 2011. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T065 | exact | Transações serializáveis delimitadas por partição. |
| T064 | family | Estado durável de serviços, não estado completo de um agente LLM. |

**Fontes:**

- [V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

## V4A-C006 — Google / Cloud Storage: metadados migrados para Spanner

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Operador descreve migração real de todos os metadados e listagem fortemente consistente.

**Mecanismo confirmado:** Metadados em banco distribuído consistente sustentam observação completa de objetos confirmados.

**Transferência proposta:** Proposta de engenharia: Usar manifesto de artefatos confirmados para que redutor pequeno não conclua com lote incompleto.

**Limites:** Não é uma segunda contagem da mesma implantação F1; não se infere bitemporalidade ou escrita externa atômica. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T065 | exact | Uso operacional de banco transacional consistente. |
| T070 | analogy | Listagem completa inspira enumeração de episódios; objeto não é episódio. |
| P004 | analogy | Inspira contrato de persistência; não demonstra runtime LAI. |

**Fontes:**

- [V4A-S007 — Spanner: The secret to Cloud Storage strong list consistency](https://cloud.google.com/blog/products/gcp/how-google-cloud-storage-offers-strongly-consistent-object-listing-thanks-to-spanner/)
- [V4A-S005 — Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/)

## V4A-C007 — Amazon / Dynamo em serviços Amazon

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Autores descrevem adoção de Dynamo por serviços centrais da Amazon.

**Mecanismo confirmado:** Versionamento de objetos e resolução de conflitos assistida pela aplicação.

**Transferência proposta:** Proposta de engenharia: Apresentar versões concorrentes ao reconciliador pequeno sem permitir que ele descarte evidência sozinho.

**Limites:** Dynamo histórico não equivale a todos os produtos DynamoDB; particionamento por hash não é CAS. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T072 | family | Versões de dados são precursor de memória versionada, sem semântica do agente. |
| T075 | family | Conflitos de objetos são resolvidos pela aplicação; não confirma reconciliação de efeitos LLM. |

**Fontes:**

- [V4A-S006 — Dynamo: Amazon’s highly available key-value store](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store)

## V4A-C008 — Microsoft / Bing: transformers na busca global

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** NLP não generativo; não é LLM autoregressiva 3–30B.

Operador afirma modelos transformer aplicados às consultas Bing globais no período descrito.

**Mecanismo confirmado:** Compreensão contextual de consultas e páginas com inferência otimizada.

**Transferência proposta:** Proposta de engenharia: Empregar modelo compacto para julgar pares consulta-trecho, medindo custo e ordenação.

**Limites:** BERT destilado do relato não é um gerador 3–30B; números de infraestrutura não são transportáveis. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

**Mesmo caso canônico:** V4B-C009. Não somado novamente por base.

| Base | Correspondência | Justificativa |
|---|---|---|
| T028 | family | Ranking neural é relacionado; fonte não especifica integralmente o pipeline desta ficha. |
| T036 | family | Consulta orienta compreensão e seleção; não comprova leitor RAG específico. |

**Fontes:**

- [V4A-S008 — Bing delivers its largest improvement in search experience using Azure GPUs](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/)

## V4A-C009 — Meta / CacheLib em serviços Facebook

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

Artigo de operadores relata adoção desde 2017 por múltiplos serviços.

**Mecanismo confirmado:** Engine comum para desenvolvimento e operação de caches de dados e armazenamento.

**Transferência proposta:** Proposta de engenharia: Separar política determinística de residência e estimativa de utilidade proposta pelo modelo.

**Limites:** Não afirma cache semântico, resumo, verdade da memória ou taxa de acerto de LLM. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T074 | family | Gerência de cache é família relacionada à evicção de memória externa. |
| T048 | analogy | Ciclo de vida físico inspira gestão, sem avaliar utilidade semântica. |

**Fontes:**

- [V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale](https://www.usenix.org/conference/osdi20/presentation/berg)

## V4A-C010 — Meta / TAO e observabilidade Polaris

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.

**Mecanismo confirmado:** Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.

**Transferência proposta:** Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.

**Limites:** Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T031 | family | Invalidação de cache convencional, não proximidade semântica. |
| T075 | family | Detecção de versões divergentes fundamenta reconciliação de estado. |
| T051 | family | TAO pertence à família de armazenamento em grafo, sem provar memória de agente. |

**Fontes:**

- [V4A-S011 — Cache made consistent](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

## V4A-C011 — Google / MillWheel: detector contínuo de anomalias

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

Artigo relata detector em uso e adoção do framework no Google.

**Mecanismo confirmado:** Grafo de computação sobre registros, estado persistente e tempo lógico.

**Transferência proposta:** Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.

**Limites:** Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T064 | family | Estado de processamento é durável; não define serialização de um agente. |
| T060 | family | Tolerância a falhas de fluxo é relacionada à retomada, mas não prova checkpoint LLM. |
| T077 | analogy | Tempo lógico orienta processamento; não é grafo temporal de conhecimento. |

**Fontes:**

- [V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

## V4A-C012 — Amazon / Rufus shopping assistant

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Amazon descreve assistente em uso no aplicativo de compras.

**Mecanismo confirmado:** RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.

**Transferência proposta:** Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.

**Limites:** Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

**Mesmo caso canônico:** V4B-C008. Não somado novamente por base.

| Base | Correspondência | Justificativa |
|---|---|---|
| T009 | exact | Recuperação antecede geração e inclui múltiplas fontes. |
| T036 | exact | Relevância de cada fonte varia com a consulta. |
| T024 | family | Seleção de fontes inspira broker, sem confirmar componente LAI. |
| P007 | analogy | Recuperador editorial pode adotar contrato semelhante, sem alegar adoção. |

**Fontes:**

- [V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

## V4A-C013 — Google / Knowledge Graph na busca Google

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** NLP não generativo; não é LLM autoregressiva 3–30B.

Anúncio relata início da implantação a usuários da busca.

**Mecanismo confirmado:** Entidades e relações permitem desambiguação e apresentação de fatos relacionados.

**Transferência proposta:** Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.

**Limites:** Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T051 | family | Grafo de conhecimento operacional; memória de agente não demonstrada. |
| T054 | family | Fatos estruturados se aproximam de memória semântica externa. |
| T066 | family | Desambiguação de entidades inspira resolução, sem contrato de versão desta ficha. |

**Fontes:**

- [V4A-S018 — Introducing the Knowledge Graph: things, not strings](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

## V4A-C014 — Microsoft / Azure AI Search semantic ranker

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

Documentação descreve recurso comercial disponível.

**Mecanismo confirmado:** Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.

**Transferência proposta:** Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.

**Limites:** Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T027 | exact | Documenta canal híbrido com RRF como entrada elegível. |
| T028 | exact | Segundo ranking explícito. |
| T037 | family | Redução de entrada é relacionada, sem igualdade ao RECOMP. |

**Fontes:**

- [V4A-S009 — Semantic ranking in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

## V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

Manual lista modos de ingestão e recuperação disponíveis.

**Mecanismo confirmado:** Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.

**Transferência proposta:** Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.

**Limites:** Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T010 | exact | Tamanho fixo configurável. |
| T011 | exact | Fronteiras por distância semântica. |
| T032 | exact | Recuperação de filhos seguida da substituição por pais. |
| T033 | family | Respeita limites lógicos em conteúdo analisado, sem todos os parsers desta ficha. |

**Fontes:**

- [V4A-S013 — How content chunking works for knowledge bases](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

## V4A-C016 — Google Cloud / Gemini context caching

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

Manual disponibiliza caches implícitos e explícitos de contexto.

**Mecanismo confirmado:** Reuso de prefixos, referências a objetos de cache e contabilidade de tokens.

**Transferência proposta:** Proposta de engenharia: Agrupar chamadas pequenas com prefixo estável quando runtime suportar e medir custo líquido.

**Limites:** Modelos e condições de serviço variam; caching não aumenta janela nem reduz obrigação de evidência. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T002 | exact | Reaproveitamento documentado de contexto comum. |
| T015 | family | Nome de recurso referencia conteúdo cacheado, não referência semântica genérica. |

**Fontes:**

- [V4A-S015 — Context caching overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

## V4A-C017 — Microsoft / API Management semantic response cache

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

Política disponível busca respostas em cache externo por proximidade.

**Mecanismo confirmado:** Embedding, limiar e particionamento de cache por expressões.

**Transferência proposta:** Proposta de engenharia: Aceitar somente domínio estável e validar pares quase iguais com entidades ou negações diferentes.

**Limites:** Não comprova implantação nem taxa de falsos acertos; limiares do serviço não são probabilidades. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T005 | exact | Retorno de resposta por similaridade semântica explicitado. |
| T031 | family | Particionamento protege escopo, mas política de invalidação completa é desenho adicional. |

**Fontes:**

- [V4A-S016 — Get cached responses of large language model API requests](https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy)

## V4A-C018 — OpenAI / ChatGPT Memory

**Classe:** produto/recurso disponível · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

Produto documenta memórias salvas e uso de histórico para personalização.

**Mecanismo confirmado:** Informações selecionadas podem atravessar conversas com controles próprios.

**Transferência proposta:** Proposta de engenharia: Criar memória externa pequena de preferências explícitas e testar correções e escopo.

**Limites:** Comportamento varia por conta; fonte não revela algoritmo nem prova precisão permanente. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T047 | exact | Persistência útil entre sessões é documentada. |
| T054 | family | Preferências são informação semântica, sem revelar formato interno. |
| T071 | family | Seleção do que lembrar não prova política de promoção desta ficha. |

**Fontes:**

- [V4A-S017 — Memory in ChatGPT](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

## V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Documentação oferece índice semântico para Chat e cloud agent.

**Mecanismo confirmado:** Busca de seções de código por significado e atualização do índice.

**Transferência proposta:** Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.

**Limites:** Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T009 | exact | Contexto recuperado do repositório orienta respostas. |
| T044 | family | Busca sob demanda relacionada à expansão. |
| P007 | analogy | Inspira interface de recuperação; não comprova componente editorial. |

**Fontes:**

- [V4A-S023 — Indexing repositories for GitHub Copilot](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

## V4A-C020 — Google / NotebookLM com fontes multimodais

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Produto oferece análise de documentos, áudio e vídeo com citações.

**Mecanismo confirmado:** Conteúdo de fontes e transcrições fundamenta respostas referenciadas.

**Transferência proposta:** Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.

**Limites:** Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T009 | family | Fundamentação em fontes é relacionada, sem pipeline interno publicado. |
| T015 | family | Citações retornam às fontes; formato de Reference Passing não é especificado. |
| T033 | analogy | Transcrições permitem endereçar trechos, sem comprovar splitter estrutural próprio. |

**Fontes:**

- [V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

## V4A-C021 — Google DeepMind / DataGemma RIG/RAG

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Projeto publica variantes para fundamentar geração em Data Commons.

**Mecanismo confirmado:** RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.

**Transferência proposta:** Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.

**Limites:** RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T009 | exact | Recuperação contextual é objetivo explícito. |
| T067 | exact | RIG reconhece necessidade de consultar para corrigir número. |
| T068 | exact | Geração é aumentada por dados externos. |

**Fontes:**

- [V4A-S014 — DataGemma](https://deepmind.google/models/gemma/datagemma/)

## V4A-C022 — Salesforce / SFR-RAG 9B

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Pesquisa apresenta modelo de nove bilhões especializado em fidelidade contextual.

**Mecanismo confirmado:** Pós-treino privilegia leitura de evidência, citações e reconhecimento de insuficiência.

**Transferência proposta:** Proposta de engenharia: Considerar leitor 8–14B especializado e comparar com modelo geral do mesmo porte.

**Limites:** Resultados experimentais publicados não garantem produção nem superioridade universal; nenhuma pergunta de benchmark foi incorporada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T009 | exact | Leitor especializado para RAG. |
| T068 | family | Uso de memória textual externa; não arquitetura neural LongMem. |

**Fontes:**

- [V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG](https://www.salesforce.com/blog/sfr-rag/)

## V4A-C023 — IBM / Granite RAG LoRAs experimentais

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Anúncio distingue modelos disponíveis de adaptadores publicados no Granite Experiments.

**Mecanismo confirmado:** Adaptadores para subtarefas como reescrita de consultas e detecção de alucinação.

**Transferência proposta:** Proposta de engenharia: Medir especialização de 8B por papel sem ativar o mesmo adaptador em tarefas incompatíveis.

**Limites:** Experimentos não são implantação; não transferir compatibilidade KV de aLoRA a qualquer LoRA. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T036 | exact | Reescrita específica de consulta é subtarefa nomeada. |
| T020 | family | Especialização aprendida é relacionada, mas não comprova compressor de prompts. |

**Fontes:**

- [V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

## V4A-C024 — Microsoft Research / Project GraphRAG

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Projeto de pesquisa publica combinação de extração, análise de redes e geração.

**Mecanismo confirmado:** Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.

**Transferência proposta:** Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.

**Limites:** Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T029 | exact | Trabalho específico GraphRAG. |
| T008 | exact | Síntese hierárquica faz parte da abordagem. |
| T051 | family | Grafo de evidência não implica memória episódica completa. |

**Fontes:**

- [V4A-S024 — Project GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/)
- [A-S024 — Welcome to GraphRAG](https://microsoft.github.io/graphrag/)

## V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

Documentação expõe ferramenta de compressão utilizável em fluxo.

**Mecanismo confirmado:** Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.

**Transferência proposta:** Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.

**Limites:** Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R005 | exact | Integração do projeto identificado. |
| T006 | exact | Compressão textual explícita. |
| T038 | family | Seleção de tokens pertence à família; mecanismo específico depende da versão. |

**Fontes:**

- [V4A-S027 — LLMLingua Prompt Compression — Prompt flow](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

## V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Pesquisa avalia gestão de contexto virtual em documentos e conversas.

**Mecanismo confirmado:** Ferramentas movimentam informação entre janela e armazenamento externo.

**Transferência proposta:** Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.

**Limites:** Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R001 | exact | Identidade do artigo original. |
| T063 | exact | Virtual context management é o mecanismo estudado. |
| T078 | analogy | Semantic Page Fault é rótulo editorial inspirado em necessidade de informação. |

**Fontes:**

- [A-S009 — MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)

## V4A-C027 — Letta / Framework de agentes stateful

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** ferramenta/framework para LLM.

Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.

**Mecanismo confirmado:** Persistência do agente e ferramentas de memória externas ao modelo.

**Transferência proposta:** Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.

**Limites:** Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R002 | exact | Fornecedor e framework identificados. |
| T064 | exact | Estado persistente de agentes é recurso explícito. |
| P004 | analogy | Inspira contratos do runtime proposto. |

**Fontes:**

- [V4A-S026 — MemGPT Is Now Part of Letta](https://www.letta.com/blog/memgpt-and-letta/)
- [V2B-S002 — Stateful agents](https://docs.letta.com/concepts/stateful-agents)

## V4A-C028 — Letta / MemFS e Context Repositories

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** ferramenta/framework para LLM.

Documentação descreve memória em arquivos e repositórios de contexto.

**Mecanismo confirmado:** Conteúdo seletivamente residente, edição de arquivos e versionamento Git.

**Transferência proposta:** Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.

**Limites:** Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R013 | exact | MemFS é referência principal. |
| R014 | exact | Alias editorial da mesma família; não segundo caso. |
| T076 | exact | Versionamento Git explicitado. |
| P003 | analogy | Inspira paginação de contexto proposta. |

**Fontes:**

- [A-S010 — MemFS](https://docs.letta.com/concepts/memfs)
- [V2B-S003 — Introducing Context Repositories: Git-based Memory for Coding Agents](https://www.letta.com/blog/context-repositories/)
- [V3A-S046 — Letta Shared memory](https://docs.letta.com/concepts/shared-memory)

## V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Artigo e código estudam memória neural recuperável para contexto extenso.

**Mecanismo confirmado:** Representações em memória e módulo adaptado de leitura são componentes treinados.

**Transferência proposta:** Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.

**Limites:** Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R003 | exact | Projeto e código específicos. |
| T052 | exact | Memória latente como um sentido delimitado do rótulo. |
| T068 | exact | Geração aumentada por memória neural. |

**Fontes:**

- [A-S013 — Augmenting Language Models with Long-Term Memory](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)
- [V3A-S047 — LongMem External_Memory implementation](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

## V4A-C030 — Autores Generative Agents / Generative Agents / Smallville

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Estudo constrói agentes simulados que registram experiências e refletem.

**Mecanismo confirmado:** Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.

**Transferência proposta:** Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.

**Limites:** Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R004 | exact | Trabalho identificado. |
| T049 | exact | Experiências recuperáveis integram a arquitetura. |
| T058 | exact | Reflexões consolidam observações. |
| T054 | family | Reflexões são abstrações, não fatos automaticamente validados. |

**Fontes:**

- [A-S008 — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)

## V4A-C031 — Microsoft Research / LLMLingua-2

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Pesquisa formula compressão como classificação de tokens treinada com dados destilados.

**Mecanismo confirmado:** Compressor especializado seleciona texto para um leitor posterior.

**Transferência proposta:** Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.

**Limites:** Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R005 | family | Variante da família, distinta do original. |
| T020 | exact | Compressão aprendida explícita. |
| T018 | family | Seleção aprendida especializa poda de contexto. |

**Fontes:**

- [V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression](https://aclanthology.org/2024.findings-acl.57/)
- [V4A-S028 — LLMLingua Series](https://www.microsoft.com/en-us/research/project/llmlingua/)

## V4A-C032 — Eshita Jha, Mingxian Wang, Andrei Barbu, Chetan Aggarwal / PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Artigo identificado estuda internalização seletiva de componente de prompt.

**Mecanismo confirmado:** Diagnóstico distingue padrões e procedimentos; dados derivados do professor treinam LoRA.

**Transferência proposta:** Proposta de engenharia: Comparar adapter 3–30B ao mesmo modelo com instrução completa e medir custo de atualização.

**Limites:** Não encontrada implantação bigtech exata nesta pesquisa; resultados não legitimam trocar de PRISM homônimo. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R006 | exact | Título e autores preservam identidade da sigla. |
| T022 | family | Internalização de instrução se relaciona à redução de prompt, mas não é simples abreviação. |

**Fontes:**

- [A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights](https://aclanthology.org/2026.emnlp-main.2431/)

## V4A-C033 — Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan, Zhou Xiao / SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Artigo identificado estuda adaptação de contexto por alinhamento de estados.

**Mecanismo confirmado:** Distilação aproxima estados em interface de blocos de atenção usando adapters.

**Transferência proposta:** Proposta de engenharia: Avaliar modelo aberto em faixa permitida com instrumentação de estados e teste funcional separado.

**Limites:** Nenhuma produção bigtech exata estabelecida; alinhamento interno não garante resposta correta. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R007 | exact | Título e autores fixam escopo da sigla. |
| T052 | family | Estados neurais são representação latente, com compatibilidade arquitetural. |

**Fontes:**

- [A-S012 — SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters](https://aclanthology.org/2026.acl-long.1046/)

## V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.

**Mecanismo confirmado:** N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.

**Transferência proposta:** Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.

**Limites:** Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.

| Base | Correspondência | Justificativa |
|---|---|---|
| T079 | exact | O artigo afirma uso real de speculative decoding. |
| T130 | exact | O proponente escolhido usa correspondências por n-gramas, sem modelo auxiliar. |
| T082 | exact | O relato de serving explicita reuso de prefixos comuns no Hiring Assistant. |
| T088 | exact | O operador descreve batching por iteração para o mesmo workload. |
| R009 | exact | vLLM é identificado como runtime do serviço. |
| P009 | analogy | Ilustra funções que a interface editorial Inference Engine poderia expor. |

**Fontes:**

- [V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)
- [V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

## V4B-C002 — Perplexity / Engine de inferência com KV Messenger

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.

**Mecanismo confirmado:** Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.

**Transferência proposta:** Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.

**Limites:** Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.

| Base | Correspondência | Justificativa |
|---|---|---|
| T102 | exact | Separação de pools e transporte de KV são descritos na implementação do operador. |
| T122 | exact | O caminho de dados usa RDMA com EFA e ConnectX compatíveis. |
| T081 | family | O decode consome estado recebido, mas o caso não demonstra todo tipo de reuso entre requisições. |
| P009 | analogy | Referência de contrato de transferência para um engine proposto. |

**Fontes:**

- [V4B-S002 — Disaggregated Prefill and Decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

## V4B-C003 — Meta / Infraestrutura de inferência Meta AI

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.

**Mecanismo confirmado:** Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.

**Transferência proposta:** Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.

**Limites:** Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.

| Base | Correspondência | Justificativa |
|---|---|---|
| T118 | exact | O operador descreve implementação e otimização de tensor parallelism. |
| T117 | exact | Particionamento de contexto é explicitamente implementado. |
| T101 | family | Pass-KV/Pass-Q são descritos como variantes frequentemente chamadas ring attention, sem identificar toda implementação com o paper específico. |
| T184 | family | Expert parallelism é discutido para modelos MoE, sem demonstrar cada arquitetura do inventário. |
| P009 | analogy | Ajuda a definir telemetria e capacidades distribuídas do componente editorial. |

**Fontes:**

- [V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

## V4B-C004 — Cloudflare / Workers AI

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.

**Mecanismo confirmado:** Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.

**Transferência proposta:** Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.

**Limites:** A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.

| Base | Correspondência | Justificativa |
|---|---|---|
| T082 | exact | O operador afirma que o serviço usa prefix caching. |
| T084 | family | Afinidade por sessão aumenta chance de cache, mas não demonstra todo o contrato de revisão de sessão da ficha. |
| T120 | family | Roteamento busca a mesma instância, sem comprovar consulta dinâmica a blocos KV de todos os workers. |
| T121 | family | Admissão assíncrona usa capacidade observada, sem expor todos os detalhes do scheduler GPU. |

**Fontes:**

- [V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5](https://blog.cloudflare.com/workers-ai-large-models/)

## V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.

**Mecanismo confirmado:** Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.

**Transferência proposta:** Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.

**Limites:** O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.

| Base | Correspondência | Justificativa |
|---|---|---|
| T178 | exact | Destilação de conhecimento é explicitamente usada no pipeline de produção. |
| T177 | exact | Professores são ajustados e o aluno é treinado para o domínio. |
| T087 | exact | O relato de serving de query understanding identifica batching no cliente e servidor. |
| R009 | exact | vLLM serve o componente de interpretação de consultas. |
| P017 | analogy | Pipeline real inspira gestão de professores e artefatos da proposta LAI. |

**Fontes:**

- [V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)
- [V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

## V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** treinamento de LLM.

Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.

**Mecanismo confirmado:** Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.

**Transferência proposta:** Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.

**Limites:** Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.

| Base | Correspondência | Justificativa |
|---|---|---|
| T177 | exact | O fluxo interno executa ajuste de modelos e gerencia resultados. |
| R023 | exact | Transformers integra explicitamente a pilha de treino. |
| R009 | exact | O scorer offline implementado utiliza servidores vLLM. |
| T182 | family | LoRA é avaliada, sem afirmar que toda configuração é modelo de produto lançado. |
| T183 | family | QLoRA é configuração estudada na infraestrutura; métricas são experimentais. |
| P016 | analogy | O scorer inspira avaliação de artefatos da proposta editorial. |

**Fontes:**

- [V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

## V4B-C007 — Meta / Experimentos EAGLE para Llama

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

Autores apresentam otimizações de treinamento e inferência de EAGLE para Llama em condições descritas como production scale.

**Mecanismo confirmado:** Atenção em árvore, verificação em múltiplas rodadas e otimizações de execução do proponente/target.

**Transferência proposta:** Proposta: avaliar a viabilidade de treinamento de um draft compatível com um alvo 8–30B antes de investigar grandes lotes.

**Limites:** A página aberta não identifica implantação comercial específica; production scale não é convertido em production_documented. Ganhos em Llama grande e múltiplas H100 não são transferidos ao ambiente do usuário.

| Base | Correspondência | Justificativa |
|---|---|---|
| T128 | exact | O trabalho estuda EAGLE explicitamente. |
| T079 | exact | O mecanismo é speculative decoding com verificação pelo alvo. |
| T132 | family | Há componente de draft aprendido, com acoplamento específico que difere de qualquer modelo auxiliar genérico. |

**Fontes:**

- [V4B-S007 — Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions](https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/)

## V4B-C008 — Amazon / Rufus

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.

**Mecanismo confirmado:** Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.

**Transferência proposta:** Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.

**Limites:** Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.

| Base | Correspondência | Justificativa |
|---|---|---|
| R009 | exact | vLLM é parte explícita do runtime lançado. |
| T088 | exact | Continuous batching é aplicado pelo scheduler do líder. |
| T118 | exact | Tensor parallelism integra as estratégias híbridas descritas. |
| T117 | exact | O prefill divide entrada pela dimensão de sequência. |
| T122 | exact | Operações entre nós usam EFA/RDMA com seleção por topologia. |
| P009 | analogy | Deployment unit e saúde dos workers inspiram requisitos do engine proposto. |

**Fontes:**

- [V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

## V4B-C009 — Microsoft / Bing — inferência BERT

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** NLP não generativo; não é LLM autoregressiva 3–30B.

Microsoft relata que modelos BERT destilados e otimizações de inferência foram usados em produção no Bing para tarefas de linguagem e busca.

**Mecanismo confirmado:** Redução do professor a encoder de três camadas e posterior otimização de execução; parte das melhorias foi disponibilizada no ONNX Runtime.

**Transferência proposta:** Proposta: testar um modelo especializado ou até um encoder menor antes de usar um gerador 3–30B para classificação/ranking.

**Limites:** Caso histórico de encoder, abaixo da escala e distinto do decode autoregressivo solicitado. Não atribuir ganhos de GPU/C++ à destilação isoladamente nem generalizar precisão de busca a geração aberta.

| Base | Correspondência | Justificativa |
|---|---|---|
| T178 | exact | Destilação de conhecimento é descrita antes da implantação. |
| T177 | exact | Bing ajusta modelos de representação para tarefas próprias. |
| P017 | analogy | Demonstra uma separação entre compressão de comportamento e otimização do executor. |

**Fontes:**

- [V4B-S009 — Microsoft open sources breakthrough optimizations for transformer inference on GPU and CPU](https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/)

## V4B-C010 — Hugging Face / HuggingChat — relato de 2023

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** aplicação com LLM.

O operador informou em 2023 que TGI alimentava HuggingChat e integrava seus serviços de inferência.

**Mecanismo confirmado:** Servidor dedicado de geração com streaming e otimizações disponíveis na pilha; o relato identifica o runtime efetivamente usado.

**Transferência proposta:** Proposta: usar o caso como referência de migração e compatibilidade; novos serviços 3–30B devem considerar estado atual de manutenção e testar alternativas.

**Limites:** Não demonstra stack atual do HuggingChat. O maintenance mode documentado em 2026 é preservado, e disponibilidade histórica não é recomendação automática de nova adoção.

| Base | Correspondência | Justificativa |
|---|---|---|
| R010 | exact | A fonte do operador afirma TGI como backend de HuggingChat naquele período. |
| T088 | family | É recurso do TGI, mas a fonte não detalha a configuração exata de batching desse deployment. |
| P009 | analogy | Caso histórico de separação entre interface de chat e runtime de inferência. |

**Fontes:**

- [V4B-S019 — Open-Source Text Generation & LLM Ecosystem at Hugging Face](https://huggingface.co/blog/os-llms)
- [V3D-S006 — Text Generation Inference — maintenance status](https://huggingface.co/docs/text-generation-inference/en/index)

## V4B-C011 — NVIDIA / TensorRT-LLM

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.

**Mecanismo confirmado:** Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.

**Transferência proposta:** Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.

**Limites:** É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.

| Base | Correspondência | Justificativa |
|---|---|---|
| R011 | exact | Produto e arquitetura do runtime são descritos diretamente. |
| T123 | exact | FP8 consta entre os formatos suportados. |
| T124 | exact | INT4/AWQ consta no conjunto de otimizações. |
| T128 | exact | EAGLE é recurso documentado. |
| T129 | exact | MTP é recurso documentado para modelos compatíveis. |

**Fontes:**

- [V4B-S011 — NVIDIA TensorRT LLM](https://developer.nvidia.com/tensorrt-llm)

## V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação

**Classe:** pesquisa; não comprova produção · laboratório de IA — contado separadamente

**Domínio observado:** pesquisa sobre LLM.

A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.

**Mecanismo confirmado:** LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.

**Transferência proposta:** Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.

**Limites:** Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.

| Base | Correspondência | Justificativa |
|---|---|---|
| T178 | exact | Experimentos são de transferência professor-aluno. |
| T179 | exact | Receita de prompt distillation transfere comportamento condicionado por contexto. |
| T180 | exact | A receita específica reduz instruções na entrada do aluno. |
| R012 | exact | É a referência Tinker para prompt distillation. |
| P017 | analogy | Fornece contratos de dados e checkpoints para um pipeline editorial proposto. |

**Fontes:**

- [V4B-S012 — Model Distillation — Tinker Documentation](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)
- [V4B-S013 — On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)
- [V3D-S008 — Prompt Distillation — Tinker Cookbook](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

## V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.

**Mecanismo confirmado:** Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.

**Transferência proposta:** Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.

**Limites:** Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.

| Base | Correspondência | Justificativa |
|---|---|---|
| R023 | exact | O recurso faz parte da biblioteca Transformers documentada. |
| T088 | exact | Recomposição de batch a cada geração é o mecanismo descrito. |
| T093 | exact | A documentação inclui gerenciamento paginado do cache. |
| T082 | exact | Prefix caching integra os recursos descritos. |
| P009 | analogy | Ilustra capacidades que um adaptador de engine poderia negociar. |

**Fontes:**

- [V4B-S014 — Continuous batching — Transformers](https://huggingface.co/docs/transformers/en/continuous_batching)

## V4B-C014 — MLC / XGrammar / XGrammar structural tags

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** ferramenta/framework para LLM.

A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.

**Mecanismo confirmado:** Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.

**Transferência proposta:** Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.

**Limites:** Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.

| Base | Correspondência | Justificativa |
|---|---|---|
| R025 | exact | É a implementação XGrammar documentada. |
| T196 | exact | Restringe geração por gramática durante decoding. |
| T197 | family | JSON Schema pode alimentar a gramática, mas isso não substitui validação posterior independente. |
| T089 | family | Delimitadores e estados de término participam do formato, sem decidir sucesso da tarefa. |

**Fontes:**

- [V4B-S015 — Structural Tag Usage — XGrammar](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)
- [V4B-S016 — Tool Calling and Reasoning — XGrammar](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

## V4B-C015 — Guidance / Guidance — geração programática

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** ferramenta/framework para LLM.

Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.

**Mecanismo confirmado:** Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.

**Transferência proposta:** Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.

**Limites:** Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.

| Base | Correspondência | Justificativa |
|---|---|---|
| R026 | exact | É o comportamento documentado da biblioteca Guidance. |
| T196 | exact | Restrições são aplicadas durante geração em backends compatíveis. |
| T081 | family | Objetos de modelo podem compartilhar estado, sem comprovar todos os cenários de cache distribuído. |

**Fontes:**

- [V4B-S030 — Token healing — Guidance](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html)
- [V3D-S015 — Guidance — Introduction](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)
- [V3D-S014 — Guidance — guidance.json](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

## V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** treinamento de LLM.

O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.

**Mecanismo confirmado:** Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.

**Transferência proposta:** Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.

**Limites:** Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.

| Base | Correspondência | Justificativa |
|---|---|---|
| R022 | exact | Fonte oficial identifica a família e seus checkpoints. |
| T184 | exact | Variantes MoE são explicitamente publicadas. |
| T100 | exact | Tabela Q/KV documenta agrupamento nas variantes pertinentes. |
| T106 | family | Configuração permite dimensionar KV, mas economia física depende do executor. |

**Fontes:**

- [V4B-S020 — Qwen3: Think Deeper, Act Faster](https://qwenlm.github.io/blog/qwen3/)

## V4B-C017 — Anthropic / Claude — treinamento com constituição

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** treinamento de LLM.

A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.

**Mecanismo confirmado:** Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.

**Transferência proposta:** Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.

**Limites:** Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.

| Base | Correspondência | Justificativa |
|---|---|---|
| T185 | exact | Princípios constitucionais são usados no treinamento por feedback de IA. |
| T177 | family | O processo inclui treinamento do modelo, mas a publicação não revela todos os detalhes da receita. |
| P017 | analogy | Uma política LAI poderia inspirar dados próprios; não há implantação da proposta editorial. |

**Fontes:**

- [V4B-S021 — Claude's new constitution](https://www.anthropic.com/news/claude-new-constitution)

## V4B-C018 — PyTorch / FlexAttention para inferência

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.

**Mecanismo confirmado:** Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.

**Transferência proposta:** Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.

**Limites:** Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.

| Base | Correspondência | Justificativa |
|---|---|---|
| T098 | exact | Interface eficiente de atenção com caminhos especializados. |
| T097 | exact | Máscaras por blocos representam esparsidade explorável pelo kernel. |
| T090 | family | Relaciona implementação da família FlashAttention; FA4 não prova adoção específica de FA1, FA2 ou FA3. |

**Fontes:**

- [V4B-S017 — FlexAttention Part II: FlexAttention for Inference](https://pytorch.org/blog/flexattention-for-inference/)
- [V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

## V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.

**Mecanismo confirmado:** Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.

**Transferência proposta:** Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.

**Limites:** Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.

| Base | Correspondência | Justificativa |
|---|---|---|
| T190 | exact | Candidatos recebem avaliação e alimentam novas propostas. |
| T195 | exact | Execução e avaliadores de código produzem sinais verificáveis. |
| T199 | family | Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação. |
| T201 | family | Há busca entre candidatos, mas não é simplesmente best-of-N independente. |
| T205 | family | Há verificação de funcionalidade e desempenho, sem equivaler a qualquer receita de treinamento por recompensas. |
| T217 | family | O sistema modifica programas com avaliação; não demonstra todos os mecanismos de aplicação de patch. |
| P016 | analogy | Avaliação local pode inspirar a proposta LAI; o produto editorial não foi implantado. |

**Fontes:**

- [V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- [V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields](https://deepmind.google/blog/alphaevolve-impact/)

## V4B-C020 — Meta / ACH — Automated Compliance Hardening

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.

**Mecanismo confirmado:** LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.

**Transferência proposta:** Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.

**Limites:** Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.

| Base | Correspondência | Justificativa |
|---|---|---|
| T195 | exact | Testes executáveis validam candidatos. |
| T199 | family | Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação. |
| T200 | family | A detecção exige evidência específica, mas o oráculo continua limitado ao comportamento modelado. |
| T217 | family | Geração de testes é parte da engenharia de código, não prova qualquer mecanismo de patch. |

**Fontes:**

- [V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)
- [V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

## V4B-C021 — Meta / TestGen-LLM

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.

**Mecanismo confirmado:** Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.

**Transferência proposta:** Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.

**Limites:** Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.

| Base | Correspondência | Justificativa |
|---|---|---|
| T195 | exact | Testes são executados para aceitar candidatos. |
| T199 | family | Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação. |
| T190 | family | Há geração e crítica por ferramentas; isso não implica refinamento livre multiagente. |
| T217 | family | Ampliação de suíte se relaciona a engenharia de código com escopo específico. |

**Fontes:**

- [V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/abs/2402.09171)

## V4B-C022 — Amazon Web Services / Bedrock Automated Reasoning checks

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

A documentação descreve uma funcionalidade disponível de verificação por raciocínio automatizado para respostas em linguagem natural vinculadas a políticas.

**Mecanismo confirmado:** Políticas são expressas formalmente e a tradução de texto para afirmações é analisada. O recurso é de detecção e possui restrições de idioma e resposta completa.

**Transferência proposta:** Proposta: usar um 3–30B para redigir respostas e um verificador externo para políticas formalizáveis, encaminhando traduções ambíguas para revisão.

**Limites:** Disponibilidade não comprova adoção específica. Validade em uma política não garante verdade externa, atualização dos fatos ou correção da tradução de linguagem natural.

| Base | Correspondência | Justificativa |
|---|---|---|
| T193 | exact | Guardrail verifica uma política expressa formalmente. |
| T200 | exact | A aceitação é sustentada por um verificador externo dentro do escopo da política. |

**Fontes:**

- [V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

## V4B-C023 — Snowflake / Suffix Decoding

**Classe:** pesquisa; não comprova produção · outro operador de tecnologia

**Domínio observado:** pesquisa sobre LLM.

A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.

**Mecanismo confirmado:** Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.

**Transferência proposta:** Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.

**Limites:** Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.

| Base | Correspondência | Justificativa |
|---|---|---|
| T131 | exact | O mecanismo é suffix decoding. |
| T079 | exact | Os candidatos são usados em decodificação especulativa. |
| R009 | family | Integração com runtime não comprova toda configuração de vLLM. |

**Fontes:**

- [B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

## V4B-C024 — Projeto llama.cpp / llama.cpp server

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.

**Mecanismo confirmado:** Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.

**Transferência proposta:** Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.

**Limites:** README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.

| Base | Correspondência | Justificativa |
|---|---|---|
| R024 | exact | Referência ao runtime llama.cpp. |
| T127 | exact | GGUF é o contêiner consumido. |
| P009 | analogy | Pode ser componente de uma proposta LAI; não é evidência de sua implantação. |

**Fontes:**

- [V3D-S012 — llama.cpp HTTP server — README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [B-S037 — GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

## V4B-C025 — Google DeepMind / RETRO

**Classe:** pesquisa; não comprova produção · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** pesquisa sobre LLM.

O trabalho avalia um modelo treinado para consumir trechos recuperados por uma arquitetura específica de atenção.

**Mecanismo confirmado:** Codificação de vizinhos recuperados e cross-attention por trechos fazem parte da função treinada.

**Transferência proposta:** Proposta: estudar custo e benefício de arquitetura treinada versus RAG externo antes de escolher uma intervenção em 3–30B.

**Limites:** Pesquisa não comprova produto implantado. Alterar um checkpoint convencional para reproduzir RETRO requer treinamento e compatibilidade; não é uma opção intercambiável de serving.

| Base | Correspondência | Justificativa |
|---|---|---|
| T112 | exact | Recuperação participa da arquitetura de atenção. |
| T009 | family | A família usa conhecimento recuperado, mas não equivale a anexar trechos a um prompt comum. |

**Fontes:**

- [B-S026 — Improving language models by retrieving from trillions of tokens](https://arxiv.org/abs/2112.04426)

## V4B-C026 — Autores de Agent Memory Distillation / AMD

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.

**Mecanismo confirmado:** Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.

**Transferência proposta:** Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.

**Limites:** Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.

| Base | Correspondência | Justificativa |
|---|---|---|
| T181 | exact | A referência trata de Agent Memory Distillation. |
| T204 | family | Memórias procedurais se relacionam a habilidades recuperáveis. |
| P017 | analogy | Pode inspirar uma proposta LAI, sem comprovar sua adoção. |

**Fontes:**

- [V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory](https://agent-memory-distillation.github.io/)
- [C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory](https://arxiv.org/abs/2608.07169)

## V4C-C001 — Amazon Web Services / EC2 RunInstances

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.

**Mecanismo confirmado:** O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.

**Transferência proposta:** Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.

**Limites:** Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.

| Base | Correspondência | Justificativa |
|---|---|---|
| T162 | exact | O contrato documentado controla repetição da mesma intenção no RunInstances. |
| T243 | family | O relato discute a ambiguidade de recursos existentes e a necessidade de identificar a operação que os criou. |
| P015 | analogy | Identidade, parâmetros e resposta exemplificam princípios do controlador editorial, sem existência do componente LAI. |

**Fontes:**

- [C-S026 — Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

## V4C-C002 — Amazon Web Services / AWS SDK — retry throttling

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A AWS relata introdução de token bucket de retries nos SDKs e uso operacional de backoff com jitter para evitar amplificação.

**Mecanismo confirmado:** Uma camada controla tentativas, consome quota de repetição e espaça chamadas; falhas em camadas aninhadas podem multiplicar carga.

**Transferência proposta:** Proposta: usar o SDK como único dono do retry de transporte; o controlador de agente reserva um orçamento de tarefa acima dele e contabiliza tentativas reais antes de escalar o modelo.

**Limites:** A documentação não prova uso de LLMs pequenas nem autoriza aplicar o mesmo número de retries a qualquer API. Quota de retries não é quota global de negócio.

| Base | Correspondência | Justificativa |
|---|---|---|
| T163 | exact | Backoff e jitter são descritos como mecanismos utilizados nos clientes. |
| T167 | exact | O texto identifica token bucket para limitar retries dos SDKs. |
| T137 | exact | Quota de repetição limita tráfego de recuperação, distinta da chamada inicial. |
| P013 | analogy | A coordenação proposta de resiliência pode reproduzir o princípio de um orçamento explícito. |

**Fontes:**

- [V2A-S012 — Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [V3C-S010 — Retry behavior — AWS SDKs and Tools](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)

## V4C-C003 — Uber / Cadence — plataforma interna

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A Uber relata Cadence em serviços internos de diferentes criticidades e em processos longos, orquestração e pipelines.

**Mecanismo confirmado:** Histórico persistente, workers, retomada e compatibilidade de workflows em andamento são tratados junto de isolamento e observabilidade operacional.

**Transferência proposta:** Proposta: manter chamadas a modelos 3–30B em atividades com saída persistida e usar o histórico para reconstruir decisões; testar evolução do código com execuções antigas antes de migrar workers.

**Limites:** Escala e disponibilidade citadas pelo operador pertencem à publicação e não são projetadas para LAI. Cadence não é Temporal, apesar de princípios relacionados.

| Base | Correspondência | Justificativa |
|---|---|---|
| T159 | exact | Execução durável de workflows é o mecanismo central relatado. |
| T160 | family | Orquestração coordena dependências, embora nem todo workflow seja um DAG estático. |
| T241 | exact | A fonte descreve replay/shadowing de históricos para detectar incompatibilidades. |
| P011 | analogy | Plataforma de workflows é referência para o controlador editorial. |
| P014 | analogy | Retomada e isolamento sustentam uma analogia de resiliência, não implementação LAI. |

**Fontes:**

- [V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability](https://www.uber.com/us/en/blog/announcing-cadence/)

## V4C-C004 — Uber / Up CD

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.

**Mecanismo confirmado:** Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.

**Transferência proposta:** Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.

**Limites:** Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.

| Base | Correspondência | Justificativa |
|---|---|---|
| T148 | exact | Gates condicionam a transição entre estágios de deployment. |
| T160 | exact | Etapas e gates coordenam dependências da implantação. |
| T236 | family | O sistema acompanha commits, mas não demonstra um agente criando commit por micro-missão. |
| T243 | exact | Ações manuais são incorporadas à representação do estado efetivo. |
| P012 | analogy | Critérios de gate ilustram um verificador editorial. |
| P015 | analogy | Vínculo entre revisão e implantação ilustra integridade de execução. |

**Fontes:**

- [V4C-S002 — Continuous deployment for large monorepos](https://www.uber.com/us/en/blog/continuous-deployment/)

## V4C-C005 — Netflix / Timestone

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A Netflix relata Timestone como fila operacional de Cosmos, Conductor e pipelines internos.

**Mecanismo confirmado:** Mensagens recebem deadlines para seleção EDF; filas exclusivas impedem processamento simultâneo do trabalho identificado como não paralelizável.

**Transferência proposta:** Proposta: pedidos 3–30B de leitura podem concorrer; edições na mesma base usam uma chave exclusiva. Comparar vazão útil e conflitos sem presumir que prioridade elimina starvation.

**Limites:** EDF não demonstra aging nem justiça por tenant. Uma fila consistente não garante exatamente uma vez dos efeitos feitos pelo worker.

| Base | Correspondência | Justificativa |
|---|---|---|
| T149 | exact | Fila de prioridade seleciona mensagens por deadlines. |
| T174 | exact | Seleção de trabalho respeita prioridade e restrições de concorrência. |
| T147 | family | O sistema limita paralelismo onde ele violaria estado; não é fan-out de ferramentas LLM. |
| P011 | analogy | Admissão e exclusão por chave apoiam o desenho proposto do executor. |

**Fontes:**

- [V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

## V4C-C006 — Netflix / Conductor — plataforma interna atualizada

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A Netflix descreve Conductor em pipelines de mídia e anúncios, com Timestone, persistência de tarefas e mecanismos de reparação operacional.

**Mecanismo confirmado:** O motor avalia um blueprint e carrega dados específicos; a fila assíncrona e regras de estado reduzem disputas, enquanto estratégias sequenciais serializam execuções por chave.

**Transferência proposta:** Proposta: orquestrar chamadas pequenas com payloads externos por referência, lendo apenas resultados necessários à decisão; manter transições e concorrência fora do modelo.

**Limites:** Um único caso de plataforma, sem contar cada pipeline como caso adicional. Recursos explicitamente descritos como roadmap não são tratados como já implantados.

| Base | Correspondência | Justificativa |
|---|---|---|
| T159 | exact | O relato inclui recuperação de processos distribuídos longos. |
| T147 | exact | Workflows incluem forks paralelos e junções. |
| T148 | exact | O DSL representa condicionais e outras transições. |
| T160 | exact | Blueprint e avaliação coordenam dependências e tarefas elegíveis. |
| T228 | family | Filas atrasadas e reparação apoiam retomada, sem provar uma política única de backoff exponencial. |
| P011 | analogy | O motor inspira responsabilidades do executor editorial. |
| P014 | analogy | Recuperação de workflows é analogia da capacidade proposta. |

**Fontes:**

- [V4C-S004 — Netflix Conductor: The Next Chapter](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649)
- [V4C-S003 — Timestone: Netflix’s High-Throughput, Low-Latency Priority Queueing System with Built-in Support for Non-Parallelizable Workloads](https://netflixtechblog.com/timestone-netflixs-high-throughput-low-latency-priority-queueing-system-with-built-in-support-1abf249ba95f)

## V4C-C007 — Anthropic / Claude Research — sistema multiagente

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.

**Mecanismo confirmado:** O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.

**Transferência proposta:** Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.

**Limites:** A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.

| Base | Correspondência | Justificativa |
|---|---|---|
| T169 | exact | Subagentes possuem contextos próprios no sistema relatado. |
| T237 | exact | O líder delega pesquisa e recebe resultados condensados. |
| T139 | exact | O relato identifica chamadas paralelas de ferramentas. |
| T147 | exact | O líder cria subagentes em paralelo e agrega suas saídas. |
| T208 | exact | Responsabilidades de líder planejador e trabalhadores são explícitas. |
| T155 | exact | Prompt engineering e simulações foram usados para corrigir falhas de delegação. |
| T060 | exact | O sistema utiliza checkpoints regulares e retomada após erros. |
| P012 | analogy | Rubricas de avaliação ilustram verificações propostas, não o produto editorial LAI. |

**Fontes:**

- [C-S030 — How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system)

## V4C-C008 — Google / Google Search — degradação sob sobrecarga

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

O livro de SRE descreve Google Search reduzindo a fração pesquisada do índice e desativando recursos em sobrecarga, além de testes acima da capacidade nominal.

**Mecanismo confirmado:** O sistema reduz trabalho e funcionalidades para preservar serviço útil; a degradação é específica do produto.

**Transferência proposta:** Proposta: sob saturação de um servidor 3–30B, reduzir ramos opcionais de exploração e preservar verificações obrigatórias; informar cobertura reduzida em vez de chamar a saída de equivalente.

**Limites:** Relato histórico; recursos citados, como Instant, não devem ser interpretados como estado atual do Search. Nenhuma equivalência de qualidade de respostas LLM foi demonstrada.

| Base | Correspondência | Justificativa |
|---|---|---|
| T136 | family | Resposta degradada é alternativa operacional, sem ser necessariamente troca de modelo. |
| T146 | analogy | Reduzir trabalho em busca é analogia para adaptar esforço de inferência. |
| T175 | family | Controle de sobrecarga combinado com degradação é relacionado a fallback por limite. |
| P013 | analogy | Política de degradação é princípio do controlador editorial. |
| P014 | analogy | Manter objetivos de serviço sob falha ilustra resiliência transversal. |

**Fontes:**

- [V4C-S005 — Service Best Practices — Overloads and Failure](https://sre.google/sre-book/service-best-practices/)

## V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** análise/reparo de software sem LLM demonstrada.

A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.

**Mecanismo confirmado:** Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.

**Transferência proposta:** Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.

**Limites:** Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.

| Base | Correspondência | Justificativa |
|---|---|---|
| T232 | exact | A fonte identifica diferenças e modificações em AST para construir reparos. |
| T229 | family | Correções são produzidas e revisadas, mas o relato não documenta um protocolo específico de edição exclusivamente por diffs. |
| T217 | exact | Candidatos são avaliados e iterados com compilação e testes. |
| T233 | exact | Patches são verificados antes de serem oferecidos para integração. |
| T200 | family | Validação separada da geração e revisão humana fornecem sinais adicionais, sem independência estatística demonstrada. |
| P012 | analogy | A cadeia de verificações exemplifica o componente editorial. |

**Fontes:**

- [V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)
- [V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

## V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** aplicação com LLM.

A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.

**Mecanismo confirmado:** Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.

**Transferência proposta:** Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.

**Limites:** O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.

| Base | Correspondência | Justificativa |
|---|---|---|
| T140 | exact | PolyglotPiranha é exposto ao agente por MCP. |
| T232 | exact | Transformações determinísticas de código ficam no PolyglotPiranha. |
| T217 | exact | Atualizações do diff são reavaliadas por CI até sucesso ou limite de tentativas. |
| T237 | exact | Fixers e verificadores recebem papéis e escopos específicos. |
| T190 | exact | Verificadores avaliam propriedades após geração e CI. |
| T195 | exact | Compilação e testes contribuem para validação do resultado. |
| T200 | exact | CodeCourt separa propriedades de aceitação do agente que fez a limpeza. |
| T206 | family | Propriedades como ausência de desvio de intenção verificam requisitos do processo, sem prova formal. |
| P012 | analogy | O gate de propriedades inspira o componente proposto, sem demonstrar um produto LAI. |
| T147 | exact | CodeCourt executa revisores por propriedade em paralelo e agrega todos os resultados antes de encaminhar o diff. |

**Fontes:**

- [V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code](https://www.uber.com/us/en/blog/piranha/)
- [V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber](https://www.uber.com/us/en/blog/ai-code-cleanup/)

## V4C-C011 — Google / Tricorder integrado a Critique

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** análise/reparo de software sem LLM demonstrada.

O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.

**Mecanismo confirmado:** Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.

**Transferência proposta:** Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.

**Limites:** Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.

| Base | Correspondência | Justificativa |
|---|---|---|
| T233 | exact | Análises são associadas à mudança de código antes da integração. |
| T238 | family | A infraestrutura lê versões pertinentes à mudança, mas não demonstra leitura LLM por faixas de linhas. |
| T224 | family | Verificações expressam critérios de engenharia, sem afirmar um processo integral spec-driven. |
| P012 | analogy | Validação vinculada à revisão e ao responsável inspira o gate editorial. |

**Fontes:**

- [V4C-S010 — Software Engineering at Google — Static Analysis](https://abseil.io/resources/swe-book/html/ch20.html)

## V4C-C012 — Amazon Web Services / Amazon Bedrock Intelligent Prompt Routing

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura de inferência de LLM.

A documentação disponibiliza um endpoint de roteamento que prevê qualidade e escolhe entre dois modelos compatíveis da mesma família.

**Mecanismo confirmado:** Configuração define modelos, critério e fallback; resposta informa o modelo usado. A página é documentação de produto, não relato de implantação de um cliente.

**Transferência proposta:** Proposta: comparar um roteador local 3–30B com regras simples, rotas fixas e escalonamento após validação. Rejeitar candidatos sem capacidade necessária antes de estimar qualidade.

**Limites:** Classificado como operational_product. Não conta para dez casos comprovados em produção; lista de modelos e regiões muda. Exemplos com modelos maiores não validam as bandas pequenas.

| Base | Correspondência | Justificativa |
|---|---|---|
| T133 | exact | Escolha de modelo por consulta é o recurso documentado. |
| T173 | family | Fallback do roteador é definido por critério de qualidade, não equivale automaticamente a recuperação por indisponibilidade. |
| P010 | analogy | O serviço oferece referência para um componente editorial de roteamento. |

**Fontes:**

- [V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

## V4C-C013 — Uber / GenAI Gateway

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

A Uber relata equipes internas utilizando o gateway para consultas a modelos externos e hospedados internamente.

**Mecanismo confirmado:** Adaptadores expõem uma interface comum e integram autenticação, política de dados, métricas e atribuição de custos.

**Transferência proposta:** Proposta: centralizar adapters de 3–30B e registrar capacidades reais de cada endpoint; separar seleção do modelo da tradução de protocolos e da medição do custo por tarefa aceita.

**Limites:** Interface compatível não torna modelos semanticamente equivalentes. Não mapear automaticamente disponibilidade de múltiplos fornecedores a cascata ou fallback comprovado.

| Base | Correspondência | Justificativa |
|---|---|---|
| T133 | family | A plataforma oferece acesso a diferentes modelos, sem provar roteador de qualidade por pergunta nesta publicação. |
| T170 | analogy | Tradução de interfaces ilustra compatibilidade, mas a fonte não demonstra versionamento integral de schemas de ferramentas. |
| P010 | analogy | O gateway é referência para infraestrutura de rotas, não valida o motor editorial completo. |

**Fontes:**

- [V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway](https://www.uber.com/us/en/blog/genai-gateway/)

## V4C-C014 — Uber / MCP Gateway e Omni MCP

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** aplicação com LLM.

A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.

**Mecanismo confirmado:** Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.

**Transferência proposta:** Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.

**Limites:** Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.

| Base | Correspondência | Justificativa |
|---|---|---|
| T134 | exact | Descoberta de servidor utiliza intenção da consulta. |
| T140 | exact | O gateway traduz e executa chamadas MCP para serviços. |
| T151 | exact | Schemas são obtidos progressivamente em vez de carregar o catálogo inteiro. |
| T158 | exact | MCP Registry mantém ferramentas, schemas, propriedade e habilitação. |
| T170 | family | O gateway documenta diffs, revisão e rollback de configuração/descritores; isso não prova uma política completa de versionamento e compatibilidade semântica de entrada e saída. |
| T214 | exact | Response Projection reduz respostas aos campos selecionados. |
| T226 | family | Heartbeat descobre presença de servidores, sem comprovar progresso semântico de tarefa. |
| P015 | analogy | Revisões e controle de exposição apoiam integridade editorial. |

**Fontes:**

- [V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

## V4C-C015 — Uber / Harnesses da Software Factory

**Classe:** produção documentada · outro operador de tecnologia

**Domínio observado:** aplicação com LLM.

A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.

**Mecanismo confirmado:** Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.

**Transferência proposta:** Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.

**Limites:** Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.

| Base | Correspondência | Justificativa |
|---|---|---|
| T133 | family | A fonte descreve seleção por workload, modelo principal e padrão de subagentes; estratégias mais amplas de routing são discutidas como direção futura, não decisão preditiva por consulta demonstrada. |
| T169 | exact | Subagentes delimitados usam modelo padrão mais econômico que o principal. |
| T212 | exact | Compactação automática é configurada nos harnesses interativos. |
| T222 | exact | Métricas de tokens por requisição e sessão orientam controle de contexto. |
| T171 | exact | Política de cache distingue sessões interativas e subagentes de duração curta. |
| T214 | exact | Code-mode mantém polling e dados intermediários fora do contexto da LLM. |
| R020 | family | Medições incluem sessões Claude Code, sem demonstrar todos os recursos do produto. |
| P010 | analogy | Seleção por resultado é referência para o roteador editorial. |

**Fontes:**

- [V4C-S014 — Running a Software Factory Efficiently at Uber Scale](https://www.uber.com/us/en/blog/efficient-software-factory/)

## V4C-C016 — LinkedIn / Microsoft / Hiring Assistant

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

A engenharia do LinkedIn descreve o produto levado à disponibilidade global, com instâncias por recrutador, identidade, mailbox e supervisão.

**Mecanismo confirmado:** Um planejador produz plano estruturado; o executor usa ciclo ReAct local. Subagentes são ferramentas, e mensagens/eventos conectam conversa, trabalho em background e atualizações da interface.

**Transferência proposta:** Proposta: usar 3–30B em classificação de tarefas, execução de buscas e extração de critérios dentro de escopos fechados; manter estado, aprovação e integração de eventos fora da LLM.

**Limites:** Fonte de arquitetura de produto, não autorização para automatizar decisões de contratação. Não estabelece paridade de modelos pequenos nem confirma LangGraph ou LangChain apenas por usar agentes.

**Mesmo caso canônico:** V4B-C001. Não somado novamente por base.

| Base | Correspondência | Justificativa |
|---|---|---|
| T143 | exact | Planejamento estruturado antecede execução de tarefas. |
| T144 | exact | O executor utiliza ReAct dentro do plano. |
| T208 | exact | Planner e executor têm responsabilidades explícitas. |
| T237 | exact | Subagentes são modelados como ferramentas especializadas. |
| T154 | exact | Instância e mailbox conservam continuidade da interação. |
| T172 | family | Canal por sessão e transmissão parcial são documentados, mas não todo o contrato de controle de fluxo, backpressure e cancelamento desta ficha. |
| T207 | family | Memória cognitiva conserva contexto, sem comprovar o mesmo algoritmo do Memory Stream. |
| P011 | analogy | Ciclo de vida e mailbox inspiram responsabilidades do executor proposto. |

**Fontes:**

- [V4C-S015 — Building the agentic future of recruiting: how we engineered LinkedIn’s Hiring Assistant](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant)

## V4C-C017 — GitHub / Microsoft / Copilot coding agent

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.

**Mecanismo confirmado:** A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.

**Transferência proposta:** Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.

**Limites:** Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.

| Base | Correspondência | Justificativa |
|---|---|---|
| T235 | exact | O recurso executa trabalho em background com logs. |
| T236 | exact | O agente publica mudanças como commits em draft PR. |
| T234 | exact | Instruções do repositório são usadas como contexto. |
| T233 | family | Há etapas de validação, sem demonstração integral do protocolo de hash-base da ficha. |
| T239 | analogy | Ambiente isolado não é prova de uso do comando Git worktree. |
| R027 | exact | Clonagem, commits e pull requests compõem o fluxo documentado. |

**Fontes:**

- [V4C-S016 — GitHub Copilot: Meet the new coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

## V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.

**Mecanismo confirmado:** Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.

**Transferência proposta:** Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.

**Limites:** Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.

| Base | Correspondência | Justificativa |
|---|---|---|
| T143 | exact | Transformação apresenta plano de dependências e substituições. |
| T213 | exact | Campanhas são decompostas em aplicações e ondas de dependências. |
| T217 | family | A fonte descreve testes e builds na transformação Java; não demonstra explicitamente o ciclo orientado por falha exigido nesta ficha. |
| T229 | family | A transformação produz mudanças de código, sem documentar que a representação e aplicação sejam exclusivamente patches localizados. |
| T174 | family | Ordem por dependência e valor orienta campanha, sem demonstrar um scheduler genérico de prioridade. |
| P011 | analogy | Orquestração de etapas inspira o executor editorial. |
| P012 | analogy | Compilação e testes exemplificam critérios de aceite. |

**Fontes:**

- [V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

## V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.

**Mecanismo confirmado:** O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.

**Transferência proposta:** Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.

**Limites:** Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.

| Base | Correspondência | Justificativa |
|---|---|---|
| T145 | family | O modelo controla orçamento de thinking interno; isso é relacionado, mas não comprova profundidade de rodadas ou etapas do agente. |
| T146 | family | Orçamento de reasoning controla uma dimensão de computação, não alocação geral. |
| T156 | exact | A model card distingue configurações de amostragem por modo. |
| T168 | exact | Limiar de thinking e limite final de geração têm semânticas diferentes. |
| T140 | exact | Há integração documentada de tool calling com parser específico. |

**Fontes:**

- [V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)
- [V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

## V4C-C020 — Microsoft / Windows — Git/GVFS

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.

**Mecanismo confirmado:** Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.

**Transferência proposta:** Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.

**Limites:** Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.

| Base | Correspondência | Justificativa |
|---|---|---|
| R027 | exact | O operador confirma migração e uso de Git. |
| T236 | family | Há commits e validação, mas não uma política de commit por etapa de agente. |
| T238 | analogy | Materialização sob demanda inspira leitura seletiva, mas não é leitura LLM por faixa de linhas. |
| T239 | analogy | Virtualização de checkout não comprova uso de Git worktrees. |

**Fontes:**

- [V4C-S020 — The largest Git repo on the planet](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

## V4C-C021 — Meta / Sapling — fluxo interno de commits

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.

**Mecanismo confirmado:** Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.

**Transferência proposta:** Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.

**Limites:** Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.

| Base | Correspondência | Justificativa |
|---|---|---|
| T236 | family | A prática de etapas pequenas e revisadas é explícita, porém usa Sapling e não o comando Git commit. |
| T213 | analogy | Decomposição de uma feature em mudanças revisáveis inspira micro-missões. |
| T211 | analogy | Histórico e commits ajudam transferência de trabalho, sem provar handoff de agentes. |
| R027 | family | Fonte descreve um sistema de versionamento relacionado e diferenças para Git, não adoção interna integral de Git. |

**Fontes:**

- [V4C-S021 — Sapling: Source control that’s user-friendly and scalable](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

## V4C-C022 — Cloudflare / CDN — request collapsing

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

A documentação descreve cache lock para solicitações simultâneas do mesmo asset em um data center.

**Mecanismo confirmado:** A primeira solicitação busca a origem; as demais aguardam e recebem a resposta compartilhada. O escopo é por localização, não exclusão global de todas as chamadas.

**Transferência proposta:** Proposta: coalescer leitura idêntica de documentos ou inferência determinística com escopo e versões iguais, separando cancelamento de um consumidor do trabalho compartilhado.

**Limites:** Operational_product: documentação de comportamento do serviço sem deployment específico de cliente. Cache HTTP não demonstra equivalência de respostas probabilísticas de LLM.

| Base | Correspondência | Justificativa |
|---|---|---|
| T150 | exact | Há coalescência explícita de solicitações simultâneas por chave de asset. |
| T172 | family | A resposta é transmitida aos aguardantes, sem descrever um controlador completo de streaming LLM. |

**Fontes:**

- [V4C-S022 — Default Cache Behavior — Request collapsing](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)

## V4C-C023 — Google / Borg

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

O artigo dos operadores descreve Borg executando aplicações e jobs nos clusters do Google ao longo de experiência operacional.

**Mecanismo confirmado:** O resumo aberto combina admissão, empacotamento, compartilhamento de máquinas, isolamento e recuperação de falhas.

**Transferência proposta:** Proposta: separar classes interativas e batch para 3–30B e medir memória e concorrência reais, conservando isolamento e uma política explícita para falta de capacidade.

**Limites:** O PDF completo ficou inacessível nesta consulta; detalhes finos de prioridade, fairness ou preempção não são atribuídos ao abstract. Nenhum ganho de inferência foi medido.

| Base | Correspondência | Justificativa |
|---|---|---|
| T174 | family | Há políticas de scheduling operacionais, mas o abstract não detalha todos os algoritmos de prioridade. |
| T137 | family | Admissão de cargas é relacionada a controle de capacidade, sem especificar o rate limiter da ficha. |
| P014 | analogy | Isolamento e recuperação fornecem princípios de resiliência para a proposta. |

**Fontes:**

- [V4C-S023 — Large-scale cluster management at Google with Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

## V4C-C024 — LinkedIn / Microsoft / Brooklin

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** sistema de dados distribuído; transferência para LLM é proposta.

O LinkedIn relata Brooklin em produção para mover dados e replicar Kafka entre clusters; a documentação oficial detalha estado de tarefas e checkpoints.

**Mecanismo confirmado:** Streams são particionados em tarefas atribuídas a instâncias; coordenadores e offsets preservam posições e permitem retomar processamento conforme o contrato dos conectores.

**Transferência proposta:** Proposta: ingerir eventos de tarefas 3–30B com cursor por partição, deduplicação e referências de artefatos; reconstruir projeções sem reenviar efeitos externos durante replay.

**Limites:** Caso de plataforma de dados; garantias variam por conector e não são elevadas a exactly-once global. Não há implantação de memória cognitiva LAI demonstrada.

| Base | Correspondência | Justificativa |
|---|---|---|
| T060 | exact | Estado e offsets/checkpoints sustentam retomada de tarefas. |
| T241 | family | Releitura de streams a partir de posições é relacionada a replay, sem provar reconstrução integral de estado de agente. |
| T240 | family | Checkpoints de offsets não equivalem a snapshot completo e consistente de toda aplicação. |
| T207 | analogy | Fluxo de eventos pode abastecer memória, mas Brooklin não implementa por isso o algoritmo cognitivo Memory Stream. |
| P008 | analogy | Histórico e posições ilustram requisitos do event store editorial. |

**Fontes:**

- [V4C-S024 — Open sourcing Brooklin: Near real-time data streaming at scale](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source)
- [V4C-S025 — Brooklin Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

## V4C-C025 — Anthropic / Claude Code em equipes internas

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.

**Mecanismo confirmado:** Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.

**Transferência proposta:** Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.

**Limites:** Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.

**Mesmo caso canônico:** V4A-C003. Não somado novamente por base.

| Base | Correspondência | Justificativa |
|---|---|---|
| R020 | exact | O operador descreve uso de Claude Code. |
| T234 | exact | CLAUDE.md fornece instruções e contexto de navegação. |
| T233 | family | Uso de testes e revisão é relatado; o artigo não demonstra o contrato completo de validação de patch com identidade de base e publicação. |
| T217 | family | Correções e refatorações concretas, sem protocolo genérico de patch comprovado. |

**Fontes:**

- [V4C-S026 — How Anthropic teams use Claude Code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

## V4C-C026 — Anthropic / Scion

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** infraestrutura geral; transferência para LLM é proposta.

Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.

**Mecanismo confirmado:** Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.

**Transferência proposta:** Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.

**Limites:** Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.

| Base | Correspondência | Justificativa |
|---|---|---|
| T238 | family | Scion fornece consulta e materialização seletiva de arquivos sob demanda; não demonstra especificamente a API de faixa de linhas. |
| T236 | family | Changesets versionam alterações mas não são git commit. |
| R027 | analogy | Sistema substituiu Git naquele ambiente; não comprova comportamento Git atual. |
| T239 | analogy | Checkouts esparsos/virtualizados não são Git worktrees. |
| P015 | analogy | Publicação e autoria por versão inspiram o componente editorial. |

**Fontes:**

- [V4C-S027 — Redesigning source control at Anthropic](https://www.anthropic.com/research/redesigning-source-control)

## V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** aplicação com LLM.

Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.

**Mecanismo confirmado:** LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.

**Transferência proposta:** Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.

**Limites:** Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.

| Base | Correspondência | Justificativa |
|---|---|---|
| R008 | exact | Fonte nomeia LangGraph na arquitetura. |
| T134 | family | Roteamento entre tarefas é relatado, sem protocolo exato de seleção de ferramentas. |
| T155 | exact | Adaptação e otimização de prompts são descritas. |
| T169 | family | Arquitetura multiagente é mencionada sem especificação de isolamento. |

**Fontes:**

- [V4C-S028 — How Klarna's AI assistant redefined customer support at scale](https://www.langchain.com/blog/customers-klarna)

## V4C-C028 — Aider / Architect/editor e formatos de edição

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** ferramenta/framework para LLM.

Documentação disponibiliza modo architect e formatos whole, diff e udiff.

**Mecanismo confirmado:** Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.

**Transferência proposta:** Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.

**Limites:** Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.

| Base | Correspondência | Justificativa |
|---|---|---|
| R019 | exact | Recurso nativo documentado do Aider. |
| T231 | exact | SEARCH/REPLACE é formato explicitamente descrito. |
| T230 | family | Formato udiff documentado é baseado em diffs, com convenção própria; não é edição AST. |
| T143 | family | Architect antecipa proposta antes da edição. |

**Fontes:**

- [V3C-S042 — Chat modes — Architect mode and the editor model](https://aider.chat/docs/usage/modes.html)
- [V2A-S008 — Edit formats](https://aider.chat/docs/more/edit-formats.html)

## V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** aplicação com LLM.

Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.

**Mecanismo confirmado:** Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.

**Transferência proposta:** Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.

**Limites:** Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| R021 | exact | Uso interno de Codex confirmado pelo operador. |
| T239 | exact | Artigo de harness usa uma aplicação e observabilidade isoladas por Git worktree. |
| T213 | exact | Operador relata decompor metas em blocos de design, código, revisão e testes com planos versionados. |
| T155 | exact | Instrução monolítica foi substituída por mapa curto. |
| T233 | exact | Linters e testes estruturais verificam invariantes. |
| T234 | exact | AGENTS.md curto e documentação versionada no repositório oferecem memória persistente do projeto; não é mera configuração CI. |
| T237 | exact | Agentes revisam outros agentes no processo descrito. |
| T217 | family | Há ciclos de implementação e testes, mas não fica provado test-first para todas as alterações. |
| R027 | exact | Git e worktrees sustentam o ambiente. |
| P012 | analogy | Gates verificáveis inspiram o componente editorial. |

**Fontes:**

- [V4C-S029 — How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [V4C-S030 — Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

## V4C-C030 — JetBrains Research / autores / SWE-agent com políticas de contexto

**Classe:** pesquisa; não comprova produção · grupo de pesquisa

**Domínio observado:** pesquisa sobre LLM.

Estudo compara estratégias de contexto em tarefas SWE-bench Verified.

**Mecanismo confirmado:** Masking oculta observações anteriores; sumarização substitui histórico por texto sintetizado; avaliação considera resolução e custo.

**Transferência proposta:** Proposta: avaliar remoção seletiva antes de acrescentar um resumidor 3–30B, preservando observações necessárias ao próximo teste.

**Limites:** Pesquisa controlada não conta como produção; não generalizar comparação para todo domínio ou modelo.

| Base | Correspondência | Justificativa |
|---|---|---|
| T215 | exact | Observation masking é objeto central do experimento. |
| T212 | family | Sumarização de trajetória é avaliada, sem provar uma política universal de gatilho de compactação. |

**Fontes:**

- [V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management](https://arxiv.org/html/2508.21433v1)

## V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.

**Mecanismo confirmado:** A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.

**Transferência proposta:** Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.

**Limites:** Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.

| Base | Correspondência | Justificativa |
|---|---|---|
| T079 | exact | O daemon combina especulação com geração guiada. |
| T085 | exact | A descrição técnica especifica quantização do modelo local. |
| T086 | exact | KV do modelo local é quantizado a 8 bits. |
| T140 | exact | Tool calling integra o framework descrito. |
| T141 | exact | Tipos gerados são restringidos por geração guiada. |
| T196 | exact | Geração guiada compila restrições sobre a saída. |
| T182 | family | Adaptadores de baixo rank são documentados, mas não se deve universalizar o treino para qualquer LoRA externa. |

**Fontes:**

- [V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)
- [V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)
- [V4D-S011 — New Apple Intelligence features are available today](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

## V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Click to Do integra Phi Silica para operações locais sobre texto selecionado.

**Mecanismo confirmado:** A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.

**Transferência proposta:** Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.

**Limites:** Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.

| Base | Correspondência | Justificativa |
|---|---|---|
| T079 | exact | Runtime NPU documenta especulação; não generalizar para GPU ou revisão histórica. Escopo: capacidade NPU da documentação consultada em 2026-11-05; não é inferida para GPU ou para a versão histórica de 2024. |
| T132 | exact | A API explica o modelo de rascunho menor verificado pelo principal na NPU. Escopo: capacidade NPU da documentação consultada em 2026-11-05; não é inferida para GPU ou para a versão histórica de 2024. |
| T085 | exact | Pilha Phi Silica publicada descreve quantização de pesos, com ressalva de revisão. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual. |
| T125 | exact | Implementação publicada usa GPTQ em pesos rotacionados; não afirmar que todo backend atual é idêntico. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual. |
| T094 | exact | Processamento do prompt em blocos de 64 preserva histórico KV na configuração publicada. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual. |
| T153 | family | Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento. |
| T006 | family | Compressão de prompt é recurso do runtime NPU; a fonte não prova sua ativação em toda ação Click to Do. |

**Fontes:**

- [V4D-S003 — Get started with Phi Silica in the Windows App SDK](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)
- [V4D-S004 — Manage Click to Do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)
- [V4D-S009 — Phi Silica, small but mighty on-device SLM](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

## V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano

**Classe:** produção documentada · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.

**Mecanismo confirmado:** Aplicação específica de um modelo local para condensar transcrições.

**Transferência proposta:** Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.

**Limites:** Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.

| Base | Correspondência | Justificativa |
|---|---|---|
| T006 | family | Resumo é redução de conteúdo, mas não comprova algoritmo específico de compressão contextual. |
| T004 | family | Há sumarização; não está documentada uma cadeia de resumos. |
| T069 | analogy | Resumo de gravação é analogia de artefato externo, sem prova de consolidação de memória de agente. |

**Fontes:**

- [V4D-S005 — Pixel December 2023 feature drop](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

## V4D-C004 — Google / Chrome built-in AI / Summarizer API

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** ferramenta/framework para LLM.

A documentação lista a Summarizer API no Chrome estável desde a versão 138.

**Mecanismo confirmado:** Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.

**Transferência proposta:** Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.

**Limites:** Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.

| Base | Correspondência | Justificativa |
|---|---|---|
| T006 | family | Sumarização acessível via API; não demonstra técnica particular de poda/compressão. |
| T004 | family | Não documenta cadeia de sumarização por trás da API. |
| T140 | analogy | API de aplicação não equivale a function calling aprendido pelo modelo. |

**Fontes:**

- [V4D-S007 — Built-in AI APIs](https://developer.chrome.com/docs/ai/built-in-apis)

## V4D-C005 — DeepSeek-AI / DeepSeek-R1-Distill 7B/8B/14B

**Classe:** pesquisa; não comprova produção · laboratório de IA — contado separadamente

**Domínio observado:** pesquisa sobre LLM.

Autores disponibilizam modelos menores afinados com amostras do professor e publicam avaliações.

**Mecanismo confirmado:** SFT/destilação de respostas de um modelo maior para modelos densos menores.

**Transferência proposta:** Proposta: selecionar tarefas verificáveis, filtrar demonstrações por teste externo, isolar famílias entre treino/teste e comparar custo total incluindo o professor.

**Limites:** Pesquisa, não produção. Comparadores são versões históricas; 32B/70B não pertencem à faixa solicitada. Mais amostras têm custo e consenso não elimina erros correlacionados.

| Base | Correspondência | Justificativa |
|---|---|---|
| T177 | exact | Os modelos menores foram afinados com exemplos gerados pelo professor. |
| T178 | exact | O projeto descreve explicitamente destilação para modelos menores. |
| T201 | family | Avaliação inclui diferentes regimes de amostragem; não prova política ótima de compute adaptativo em produção. |

**Fontes:**

- [V4D-S008 — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)
- [V4D-S010 — DeepSeek-R1 official model repository](https://github.com/deepseek-ai/DeepSeek-R1)

## V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA

**Classe:** produto/recurso disponível · Big Tech — núcleo definido nesta curadoria

**Domínio observado:** aplicação com LLM.

Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.

**Mecanismo confirmado:** Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.

**Transferência proposta:** Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.

**Limites:** Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.

| Base | Correspondência | Justificativa |
|---|---|---|
| T177 | exact | Ajuste para uma tarefa educacional delimitada. |
| T178 | exact | Professor gera exemplos para treinar o modelo menor. |
| T182 | exact | Especialização realizada por adaptadores LoRA. |
| T183 | family | Treino contra modelo quantizado não comprova todos os detalhes do método QLoRA original. |
| T155 | exact | Especialização permitiu reduzir o prompt mantendo instrução explícita de formato. |
| T180 | exact | Parte das instruções foi absorvida no adaptador; avaliação continua necessária. |
| T193 | exact | Restrições verificáveis rejeitam saídas inadequadas antes da exibição. |
| T186 | exact | Reviewer/Critic/Meta-Reviewer apoiam avaliação offline. |
| T200 | family | Estudo humano confronta os julgamentos, mas não demonstra independência causal de todo erro. |
| T153 | family | Entrega incremental documentada; a fonte consultada não especifica propagação de interrupção/cancelamento ao processamento. |
| T172 | family | Guardas controlam liberação de perguntas; não se documenta o ciclo completo do controlador, com pressão reversa e encerramento. |

**Fontes:**

- [V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)
- [V4D-S013 — Application card: AI in Microsoft 365 Education](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

## V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** infraestrutura de inferência de LLM.

Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.

**Mecanismo confirmado:** Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.

**Transferência proposta:** Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.

**Limites:** 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.

| Base | Correspondência | Justificativa |
|---|---|---|
| T102 | exact | A seção de deployment separa explicitamente prefill e decoding. |
| T118 | exact | Atenção usa tensor parallelism no deployment descrito. |
| T122 | exact | Perfil do runtime descreve comunicação RDMA no decode, distinguindo o perfil simplificado da carga completa. |
| T184 | exact | O deployment distribui especialistas e ajusta redundância com estatísticas online. |
| T129 | family | MTP faz parte da pesquisa/treino do modelo; a fonte não comprova que a especulação MTP esteja ativa em toda implantação online. |

**Fontes:**

- [V4D-S014 — Profiling Data in DeepSeek Infra](https://github.com/deepseek-ai/profile-data/blob/main/README.md)
- [V4D-S015 — DeepSeek-V3 Technical Report — v2](https://arxiv.org/html/2412.19437v2)

## V4D-C008 — Moonshot AI / Kimi / Mooncake serving

**Classe:** produção documentada · laboratório de IA — contado separadamente

**Domínio observado:** infraestrutura de inferência de LLM.

Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.

**Mecanismo confirmado:** Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.

**Transferência proposta:** Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.

**Limites:** O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.

| Base | Correspondência | Justificativa |
|---|---|---|
| T081 | exact | A arquitetura reutiliza KV como recurso compartilhado do serving. |
| T102 | exact | A descrição operacional separa clusters de prefill e decode. |
| T120 | exact | Seção 5.1/Algoritmo 1 de Mooncake v1 escolhe worker usando prefixo reutilizável, fila, transferência prevista e TTFT/SLO. |
| T121 | exact | Scheduler equilibra throughput e SLO de requisições. |
| T122 | exact | Seção 3 de Mooncake v1 identifica Messenger baseado em (GPUDirect) RDMA para transferir blocos KV entre CPUs/GPUs. Não se generaliza a todos os backends posteriores. |
| T082 | exact | Seção 3, passos 1–2: recuperar prefixo KV existente e executar apenas prefill incremental. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B. |
| T088 | exact | Seção 3, passo 4: requisição entra no próximo lote de decode por continuous batching. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B. |
| T094 | exact | Seção 3, passo 2, e seção 4.1: prefill longo é dividido em chunks conforme limiar e processado em pipeline. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B. |
| T157 | exact | Seção 5.1/Algoritmo 1: chave de bloco combina tokens locais e hash do bloco anterior. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B. |

**Fontes:**

- [V4D-S016 — Mooncake — serving platform for Kimi](https://kvcache-ai.github.io/Mooncake/)
- [V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving](https://arxiv.org/html/2407.00079v1)

## V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake

**Classe:** produto/recurso disponível · outro operador de tecnologia

**Domínio observado:** infraestrutura de inferência de LLM.

Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.

**Mecanismo confirmado:** HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.

**Transferência proposta:** Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.

**Limites:** Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.

| Base | Correspondência | Justificativa |
|---|---|---|
| T081 | exact | Blocos KV podem ser reutilizados entre requisições elegíveis. |
| T082 | exact | Prefixos comuns reutilizam os mesmos nós de KV. |
| T083 | exact | Hierarquia e prefetch ampliam a política de reutilização de prefixos descrita. |
| T103 | exact | HiRadixTree organiza spans de tokens e seus locais de armazenamento. |
| T104 | exact | HiCache estende explicitamente RadixAttention. |
| T122 | exact | O backend disponibiliza transferência RDMA entre buffers registrados, conforme suporte e configuração. |
| T062 | analogy | Hierarquia de KV é analogia de camadas de memória, não memória semântica do agente. |

**Fontes:**

- [V4D-S017 — Mooncake x SGLang HiCache System Design](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)
- [V4D-S018 — Mooncake Architecture](https://kvcache-ai.github.io/Mooncake/design/architecture.html)
- [V4D-S019 — Mooncake Transfer Engine](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)


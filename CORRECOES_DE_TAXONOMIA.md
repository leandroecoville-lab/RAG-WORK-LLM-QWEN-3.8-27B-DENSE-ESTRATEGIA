# Taxonomia e equivalências

Os IDs T001–T206 foram preservados e T207–T243 foram acrescentados. R e P ficam fora da contagem de 243. IDs canônicos indicam equivalência editorial; relações indicam proximidade, não identidade. T069 agora define consolidação externa por resumos; a destilação paramétrica permanece em T179.

| ID | Nome atual | Nome canônico | Referência canônica | Nota |
|---|---|---|---|---|
| T007 | Response Caching por Hash | Response Caching por Hash | T007 | Padrão de engenharia formado por cache exato e endereçamento por conteúdo; não é um algoritmo específico de LLM. |
| T015 | Reference Passing | Reference Passing | T015 | Padrão de engenharia aplicado a agentes; não identifica um método científico exclusivo. |
| T019 | Few-Shot Pruning | Few-Shot Pruning | T019 | Rótulo descritivo de seleção de exemplos, não método único; a fonte documenta uma ferramenta de seleção relacionada. |
| T021 | Context Compression On-the-Fly | Context Compression On-the-Fly | T006 | Variante operacional da família Context Compression; mantida para preservar o inventário. |
| T023 | Recursive Summarization Tree | Recursive Summarization Tree | T008 | Representação estrutural da sumarização hierárquica; não deve ser contada como tecnologia independente. |
| T024 | Context Broker e Context Builder | Context Broker / Context Builder | T024 | Nome arquitetural descritivo; implementação e critérios propostos são editoriais. |
| T034 | Agentic Chunking | Agentic Chunking | T034 | Termo descritivo sem implementação única identificada; fontes fornecem os conceitos de segmentação relacionados, não validam um método exclusivo. |
| T035 | Contextual Chunking | Contextual Chunking | T035 | O nome original é amplo; o mecanismo específico documentado pela Anthropic é Contextual Retrieval, não um splitter universal. |
| T038 | Selective Context Pruning | Selective Context Pruning | T018 | Entrada mantida como variante do conceito geral T018; o método científico específico deve ser citado pelo título da fonte. |
| T039 | Importance-Aware Window | Importance-Aware Window | T039 | Nome descritivo de uma política de seleção, não algoritmo universal ou benchmark estabelecido. |
| T052 | Latent Context | Latent Context | T052 | Termo ambíguo; cada uso precisa declarar representação, treinamento e interface. Não há um único recurso chamado Latent Context. |
| T057 | Causal Memory | Causal Memory | T057 | Não foi identificado um padrão único com esse nome; a fonte sustenta princípios de inferência causal, não uma implementação universal de memória. |
| T069 | Consolidação por resumos — anteriormente chamada de “Context Distillation” | Consolidação por resumos | T069 | T069 não redireciona para T179. |
| T071 | Memory Promotion | Memory Promotion | T071 | Política arquitetural proposta; não existe limiar universal de evidência aplicável a toda memória. |
| T078 | Semantic Page Fault | Semantic Page Fault | T078 | Analogia arquitetural relacionada à memória virtual do MemGPT; não se afirma que o paper padroniza esse rótulo ou garante detecção de toda lacuna. |
| T083 | Advanced Prefix Caching | Advanced Prefix Caching | T082 | Mantido o nome do inventário; classificado como extensão editorial de Prefix Caching. |
| T104 | Radix Attention | RadixAttention | T104 | Normalização do nome original do inventário; preservado como técnica específica do SGLang. |
| T109 | Local / Window Attention | Local / Window Attention | T095 | Sobreposição de nomenclatura preservada; a equivalência vale para a variante de janela local contígua. |
| T112 | Retrieval-Based Attention | Retrieval-Based Attention | T112 | RETRO é exemplo documentado. O registro não identifica toda a família com uma implementação específica. |
| T115 | Activation Checkpointing | Activation Checkpointing | T115 | Classificação original em inferência foi preservada por ID; aplicação principal explicada como treinamento. |
| T122 | RDMA para inferência distribuída | RDMA para inferência distribuída | T122 | RDMA é família de mecanismos de comunicação; GPUDirect RDMA é uma variante específica, não sinônimo irrestrito. |
| T127 | GGUF — formato de modelos, não método único de quantização | GGUF — contêiner binário de modelos | T127 | Correção terminológica do inventário original |
| T173 | Model Fallback Controlado | Model Fallback Controlado | T136 | Especialização de T136; não contar como um mecanismo independente. |
| T180 | Prompt Distillation | Prompt Distillation | T179 | Variante próxima de T179; os dois nomes não devem ser contados como tecnologias inteiramente independentes. |
| T181 | Agent Memory Distillation | Agent Memory Distillation | T181 | Identificação confirmada em arXiv:2608.07169; não confundir com qualquer método chamado genericamente memory distillation. |
| T199 | Aprendizagem por avaliação | Aprendizagem por Avaliação | T199 | Rótulo editorial amplo; o mecanismo de aprendizagem precisa ser declarado em cada implementação. |
| T218 | Loop Detection / detecção de estagnação e ciclos | Loop Detection / detecção de estagnação e ciclos | T218 | Política editorial de supervisão; não é apresentada como algoritmo universal de um produto. |
| T221 | Goal Reminder Injection | Goal Reminder Injection | T221 | Nome operacional proposto. As fontes apoiam contexto seletivo e continuidade; não comprovam uma política universal de injeção. |
| T223 | Constitutional Self-Check | Constitutional Self-Check | T223 | Adaptação editorial durante inferência; manter distinção explícita de Constitutional AI como método de treinamento. |
| T233 | Patch Validation — incluindo verificação de hash-base | Patch Validation — incluindo verificação de hash-base | T233 | Verificação criptográfica da base é uma recomendação de protocolo; não se presume que todo editor a faça automaticamente. |
| R002 | Letta | Letta — plataforma de agentes com estado | R002 | Atualiza R002: a antiga ficha combinava Letta e MemFS. O detalhamento de MemFS passa a R013 e seu nome relacionado a R014. |
| R005 | LLMLingua | LLMLingua — compressão de prompts em múltiplas etapas | R005 | LLMLingua pode designar uma família de ferramentas. As variantes têm mecanismos e requisitos próprios; esta ficha não trata todas como um único algoritmo. |
| R006 | PRISM | PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights | R006 | Nome desambiguado pelo título completo e pela fonte A-S011; não confundir com outros projetos PRISM. |
| R007 | SADA | SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters | R007 | SADA está desambiguado pelo título completo da publicação; o nome sozinho não define compatibilidade com outros modelos. |
| R010 | Hugging Face TGI | Hugging Face TGI | R010 | Estado do projeto verificado em documentação oficial em 2026-11-05; revisar antes de decisão futura. |
| R011 | NVIDIA TensorRT-LLM | NVIDIA TensorRT-LLM | R011 | Evitar aplicar descrição de versões antigas à documentação atual; snapshot factual consultado em 2026-11-05. |
| R013 | Letta MemFS | Letta MemFS — memória versionada em arquivos | R013 | O nome combinado da edição anterior é preservado como alias histórico. Não houve instalação nem teste de sincronização real. |
| R014 | Letta Context Repositories | Letta MemFS — Context Repositories | R013 | Alias relacionado explicitamente ao canonical_id R013. O blog é histórico; regras operacionais atuais devem ser verificadas na documentação de MemFS. |
| R015 | Learning by Distilling Context | Learning by Distilling Context | R015 | Distinguir esta referência de consolidação por resumos, registrada em T069. Não transportar resultados publicados para Qwen ou português sem avaliação. |
| R016 | Lost in the Middle | Lost in the Middle: How Language Models Use Long Contexts | R016 | Primeira submissão em 2023; não é benchmark atual do checkpoint ou servidor do usuário. |
| R017 | LangChain | LangChain | R017 | A ficha usa a documentação atual de create_agent; exemplos de APIs antigas precisam ser conferidos antes de migração. |
| R018 | Temporal | Temporal | R018 | A garantia sobre o histórico não deve ser apresentada como exactly-once de qualquer serviço externo. |
| R019 | Aider | Aider — programação assistida no terminal | R019 | Nenhuma chamada ao Aider ou modelo foi executada. Formatos e recursos devem corresponder à versão instalada. |
| R020 | Claude Code | Claude Code — agente de programação da Anthropic | R020 | Não houve instalação, autenticação ou execução real do Claude Code. A ficha não fixa modelo, plano ou compatibilidade local. |
| R021 | OpenAI Codex | OpenAI Codex — agente e CLI de programação | R021 | A documentação consultada informa que --full-auto deixou de ser suportado; não reutilizar flags antigas sem conferir a CLI. Não fixa modelo, plano ou versão instalada. |
| R022 | Qwen | Qwen — família de modelos | R022 | As páginas consultadas incluem exemplos Qwen3; eles não são declarados como geração mais recente nem como modelo instalado. Nenhum checkpoint do usuário foi inspecionado. |
| R023 | Hugging Face Transformers | Hugging Face Transformers — biblioteca de modelos | R023 | Não fixa a versão mais recente como requisito. O uso de outras bibliotecas ou backends precisa ser testado com a mesma revisão de modelo. |
| R024 | llama.cpp | llama.cpp — inferência em C/C++ | R024 | Documentação do repositório oficial consultada, sem compilação ou benchmark local. Não afirma compatibilidade do Qwen ou da GPU instalada do usuário. |
| R025 | XGrammar | XGrammar — motor de geração estruturada | R025 | Não promete suporte a toda construção de schema ou a qualquer checkpoint. Nenhum backend foi configurado ou testado nesta entrega. |
| R026 | Guidance | Guidance — programação controlada de geração | R026 | Limitações de JSON Schema são atribuídas à API documentada, não à impossibilidade teórica de representar toda restrição em qualquer sistema. |
| R027 | Git | Git — controle distribuído de versões | R027 | Referência ao Git, sem confundir com um serviço específico de hospedagem. Nenhum commit, branch ou worktree do usuário foi criado ou alterado. |

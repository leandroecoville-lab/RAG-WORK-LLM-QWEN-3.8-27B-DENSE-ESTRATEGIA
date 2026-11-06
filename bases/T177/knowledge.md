# T177 — Fine-Tuning

**Nome canônico:** Fine-Tuning  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T177  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ajuste fino

## T177:C01 — conceito

Treinamento adicional de um modelo pré-treinado para ajustar seu comportamento a dados ou tarefas. Pode atualizar todos os pesos ou apenas parâmetros selecionados. Salvar documentos em RAG não é fine-tuning: a consulta muda o contexto, enquanto o treinamento modifica parâmetros ou adaptadores.

Como funciona:
- Preparar exemplos e objetivo de treinamento adequados à tarefa.
- Calcular perda e atualizar parâmetros permitidos.
- Avaliar o checkpoint em dados separados antes de distribuí-lo.

## T177:C02 — aplicacao

Quando usar:
- Comportamento recorrente e estável não resolvido satisfatoriamente por prompt e ferramentas.
- Há dataset representativo e critério objetivo de sucesso.

Quando não usar:
- Usar pesos como banco exato de fatos voláteis ou treinar sobre respostas não verificadas.

Implementação proposta:
- Deduplicar dados e separar treino, validação e teste por origem ou período.
- Fixar tokenizer, template, base e configuração para reprodutibilidade.
- Comparar com baseline sem treino e manter possibilidade de rollback.

Aplicação LAI proposta:
Proposta: treinar comportamentos específicos da Helena somente após identificar falhas repetidas e reunir exemplos de resultado comprovado.

## T177:C03 — riscos_validacao

Armadilhas:
- Vazamento de exemplos de teste produz ganho ilusório.
- Adaptação pode melhorar tarefa-alvo e degradar capacidades gerais.

Métricas sugeridas:
- Desempenho no alvo e regressões fora dele.
- Custo de treinamento, inferência e manutenção por versão.

Testes propostos:
- Avaliar casos novos e adversos sem permitir memorização do teste.
- Testar checkpoint revertido e carregamento em ambiente limpo.

## T177:C04 — perguntas_proveniencia

Pergunta: Fine-tuning faz o modelo aprender automaticamente em cada conversa?
Resposta: Não. É necessário um processo explícito de coleta, treinamento e avaliação.

Pergunta: RAG e fine-tuning competem?
Resposta: Podem se complementar: fatos recuperáveis e habilidades treinadas têm funções distintas.

Pergunta: Mais tokens no dataset significam mais supervisão?
Resposta: Não quando muitos estão mascarados; registre tokens efetivamente usados na loss e sua distribuição.

Pergunta: Treinar documentos substitui RAG atualizado?
Resposta: Não. Pesos não oferecem automaticamente proveniência, remoção de fatos ou atualização imediata de conteúdo variável.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T177:C05 — mecanismo_avancado

O objetivo é definido pelos tokens que recebem supervisão, não apenas pelos exemplos textuais. Em ajuste conversacional, calcular loss sobre respostas, mensagens de usuário ou todos os tokens produz problemas diferentes. Templates e máscaras precisam corresponder; um rótulo deslocado incorretamente pode treinar cópia ou previsão da posição errada. A divisão de dados também deve agrupar variantes da mesma origem para evitar validação artificialmente fácil.

Condição de contorno:
Loss menor pode refletir memorização de templates ou conteúdo repetido sem melhorar a tarefa que será executada.

Contrato proposto:
- Entradas: Checkpoint, exemplos versionados, template, máscara de supervisão e conjunto de validação independente.
- Saídas: Pesos ou adaptadores atualizados e relatório de tarefas preservadas e modificadas.
- Estado: Otimizador, scheduler, contador de tokens supervisionados e proveniência dos dados.
- Invariante: Nenhum exemplo de validação influencia seleção de alvos ou ajustes durante o treinamento final.

Compromissos de projeto:
- Supervisão mais específica concentra o aprendizado e pode reduzir cobertura geral.
- Mais épocas reforçam exemplos e aumentam risco de memorização ou regressão.

## T177:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir exemplos com respostas curtas e prompts longos, inspecionando quais posições recebem loss. Introduzir uma máscara errada e exigir detecção antes de treinar o conjunto inteiro.

Plano de avaliação proposto:
Plano proposto: comparar base, prompt melhorado e ajuste fino com tarefas iguais. Controlar origem dos dados, contabilizar tokens supervisionados e medir qualidade, regressões e custo; aprovar apenas ganhos fora do conjunto usado para escolher hiperparâmetros.

Comparações:
- T182 (complements): LoRA restringe os parâmetros treináveis; definição dos alvos e avaliação continuam necessárias ao ajuste.

Afirmação rastreável:
O SFT Trainer documenta opções distintas de loss sobre respostas do assistente e sobre completions.
Suporte: direct; fontes: V3B-S015
Limite: A existência dessas opções não confirma que o template do usuário produz máscaras corretas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T177:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou supervisão por token e separação de dados. A nova camada orienta a decisão de ajustar, o desenho de releases e a identificação de falhas que treinamento não resolve.

Diagnóstico antes do treino
Classifique erros em formato, procedimento, conhecimento ausente, recuperação e ferramenta. Ajuste é plausível para comportamento estável e habilidade recorrente; fatos voláteis ou documentos não recuperados podem exigir outra intervenção. Construa exemplos contrastivos que isolam a falha, em vez de ampliar indiscriminadamente o dataset.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012.

Release com identidade
Um modelo ajustado é uma nova versão de comportamento. Registre base, dados, máscara, hiperparâmetros e avaliação. Mantenha baseline e possibilidade de retorno; adapters, quantização e template usados na implantação devem ser testados juntos, porque a qualidade do checkpoint isolado não descreve o serviço final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012.

Custo de manutenção
Especialização pode reduzir prompts e tentativas, mas cria necessidade de atualizar dados e revalidar regressões. Meça frequência de mudança do domínio e custo de curadoria. O relato da plataforma Uber demonstra infraestrutura operacional de treinamento, sem provar que toda combinação experimental de LoRA/QLoRA virou produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012.

USO AVANÇADO — Extração de domínio
Cenário: O modelo erra formato e terminologia em tarefas repetidas.
Estratégia: Crie exemplos corretos e negativos, ajuste em dados autorizados e teste em origens novas. Mantenha validação estrutural e factual fora do modelo.
Papel do modelo pequeno: Um 3–7B pode assumir extração estreita com critérios de aceite claros.
Aceite proposto: Medir precisão por campo e falhas graves, incluindo entradas fora do domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012.

USO AVANÇADO — Procedimento com ferramentas
Cenário: O agente conhece as ferramentas, mas aplica sequência inadequada.
Estratégia: Treine trajetórias revisadas com estados e resultados reais, incluindo falhas e recuperação. Evite ensinar comandos que dependem de um ambiente já obsoleto.
Papel do modelo pequeno: Um 8–14B pode aprender padrões de procedimento, com execução controlada.
Aceite proposto: Avaliar conclusão verificável da tarefa e ações indevidas, não semelhança textual à trajetória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize poucos comportamentos estáveis e dados de alta qualidade; capacidades amplas não surgem de exemplos repetidos.
8–14B: Use tarefas variadas do domínio e regressões de capacidades que devem permanecer.
15–30B: Maior porte aumenta custo de ciclo; compare adaptação eficiente com ajuste completo conforme a hipótese.
Requisitos de treino/runtime: Exige treino e validação independente. Infraestrutura de serving e quantização devem ser incluídas no teste final.
Não aplicar quando: Não usar ajuste como substituto de atualização de fatos, controle de acesso ou verificação de ações.

## T177:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: Professores são ajustados e o aluno é treinado para o domínio.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C009 — Microsoft / Bing — inferência BERT
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Microsoft relata que modelos BERT destilados e otimizações de inferência foram usados em produção no Bing para tarefas de linguagem e busca.
Mecanismo documentado: Redução do professor a encoder de três camadas e posterior otimização de execução; parte das melhorias foi disponibilizada no ONNX Runtime.
Correspondência com esta base: Bing ajusta modelos de representação para tarefas próprias.
Transferência proposta para modelo pequeno: Proposta: testar um modelo especializado ou até um encoder menor antes de usar um gerador 3–30B para classificação/ranking.
Limite: Caso histórico de encoder, abaixo da escala e distinto do decode autoregressivo solicitado. Não atribuir ganhos de GPU/C++ à destilação isoladamente nem generalizar precisão de busca a geração aberta.
Fontes: V4B-S009.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: O fluxo interno executa ajuste de modelos e gerencia resultados.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4B-C017 — Anthropic / Claude — treinamento com constituição
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: treinamento de LLM.
Uso observado: A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.
Mecanismo documentado: Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.
Correspondência com esta base: O processo inclui treinamento do modelo, mas a publicação não revela todos os detalhes da receita.
Transferência proposta para modelo pequeno: Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.
Limite: Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.
Fontes: V4B-S021.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Ajuste para uma tarefa educacional delimitada.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

V4D-C005 — DeepSeek-AI / DeepSeek-R1-Distill 7B/8B/14B
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores disponibilizam modelos menores afinados com amostras do professor e publicam avaliações.
Mecanismo documentado: SFT/destilação de respostas de um modelo maior para modelos densos menores.
Correspondência com esta base: Os modelos menores foram afinados com exemplos gerados pelo professor.
Transferência proposta para modelo pequeno: Proposta: selecionar tarefas verificáveis, filtrar demonstrações por teste externo, isolar famílias entre treino/teste e comparar custo total incluindo o professor.
Limite: Pesquisa, não produção. Comparadores são versões históricas; 32B/70B não pertencem à faixa solicitada. Mais amostras têm custo e consenso não elimina erros correlacionados.
Fontes: V4D-S008, V4D-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q007, V4B-Q008.

## T177:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T177 → T178 [complements]
Como combinar: Um professor pode produzir sinais de treino, desde que revisados e rastreáveis.
Interface: Exemplos, origem e filtros.
Condição: Dados representam o uso e não vazam avaliação.
Aceite proposto: Comparar com rótulos humanos e casos que o professor erra.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T177 → T182 [alternative]
Como combinar: LoRA permite testar especialização sem atualizar todos os pesos.
Interface: Módulos-alvo, posto e identidade da base.
Condição: Capacidade da adaptação atende a hipótese.
Aceite proposto: Comparar qualidade, custo e manutenção com ajuste completo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S015, C-S031, V4B-S006, V4B-S005, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Agrupar divisões por origem e tempo para evitar variantes do mesmo caso em treino e teste.
- Não selecionar repetidamente hiperparâmetros sobre o conjunto final de aceitação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a especialização com fronteira em tarefas de negócio previamente definidas. Vencer num conjunto estreito não prova capacidade geral; inclua casos desconhecidos e custo de manutenção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T178, T179, T182, T183

## Fontes primárias associadas

### C-S031 — Fine-tuning — Transformers

[https://huggingface.co/docs/transformers/training](https://huggingface.co/docs/transformers/training)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adaptação de modelo pré-treinado com dataset, tokenização, treino e avaliação.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S015 — SFT Trainer

[https://huggingface.co/docs/trl/main/en/sft_trainer](https://huggingface.co/docs/trl/main/en/sft_trainer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mascaramento da loss, supervisão assistant-only/completion-only e tokenização em SFT.

Limite: Documentação main dinâmica; comportamento e requisitos devem ser conferidos na versão instalada.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4B-S009 — Microsoft open sources breakthrough optimizations for transformer inference on GPU and CPU

[https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/](https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Bing usou destilação de BERT e otimizações de inferência em produção; integração posterior no ONNX Runtime.

Limite: Caso histórico de encoder, não LLM autoregressivo de 3–30B; não somar ganhos de hardware e algoritmo como efeito de destilação.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S021 — Claude's new constitution

[https://www.anthropic.com/news/claude-new-constitution](https://www.anthropic.com/news/claude-new-constitution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Constituição usada em treinamento e síntese de exemplos/rankings; método evoluiu desde Constitutional AI.

Limite: Texto de princípios e treinamento não garantem aderência de toda saída; parâmetros do modelo não são publicados nesta fonte.

### V4D-S008 — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesquisa sobre RL de raciocínio e transferência de capacidades a modelos menores.

Limite: Pesquisa e benchmarks, não evidência de implantação de cada variante. Registro atual é v2, revisado em 2026-01-04; comparação histórica não define fronteira de novembro de 2026.

### V4D-S010 — DeepSeek-R1 official model repository

[https://github.com/deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints destilados 7B, 8B e 14B dentro da faixa pedida; tabelas de avaliação com configuração de amostragem e modelos comparadores identificados.

Limite: 32B e 70B estão fora da faixa 3–30B. Pass@1 e consenso@64 não são a mesma métrica. Benchmarks históricos e resultados do autor não demonstram paridade geral ou produção.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

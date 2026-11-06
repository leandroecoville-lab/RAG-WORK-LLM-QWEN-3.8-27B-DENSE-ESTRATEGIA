# Verificação, treinamento e especialização

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

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


---

# T178 — Knowledge Distillation

**Nome canônico:** Knowledge Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T178  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** destilação de conhecimento

## T178:C01 — conceito

Família de métodos que transfere comportamento de um professor para um aluno. A supervisão pode usar respostas, probabilidades ou representações, conforme acesso e objetivo. O aluno costuma ser menor, mas isso não é requisito lógico; a transferência não garante copiar toda competência do professor.

Como funciona:
- Selecionar tarefas e executar professor com configuração conhecida.
- Construir sinais de supervisão e filtrar exemplos inadequados.
- Treinar aluno para aproximar o comportamento desejado e avaliar generalização.

## T178:C02 — aplicacao

Quando usar:
- Especialização de modelo mais barato em tarefas repetitivas.
- Professor produz sinais úteis que exemplos humanos sozinhos não oferecem em escala.

Quando não usar:
- Imitar erros ou resultados sem direito de uso dos dados e do serviço envolvido.

Implementação proposta:
- Definir se supervisionará respostas finais ou distribuições disponíveis.
- Medir qualidade do professor nos dados antes de gerar grande volume.
- Separar avaliação do aluno de semelhança textual com o professor.

Aplicação LAI proposta:
Proposta: usar APIs mais capazes como professoras de procedimentos verificáveis para o Qwen, mantendo dados rastreáveis e avaliações independentes.

## T178:C03 — riscos_validacao

Armadilhas:
- Aluno pode reproduzir vícios e erros do professor.
- Cobertura estreita de exemplos não transfere capacidades ausentes no dataset.

Métricas sugeridas:
- Resultado do aluno por custo de inferência.
- Retenção de qualidade em tarefas e distribuições novas.

Testes propostos:
- Comparar aluno treinado, aluno base e professor em teste reservado.
- Inserir exemplos defeituosos no pipeline de curadoria e conferir se são filtrados.

## T178:C04 — perguntas_proveniencia

Pergunta: Destilação exige logits do professor?
Resposta: Não. Pode usar exemplos de saída, embora o sinal de treinamento seja diferente.

Pergunta: O aluno precisa ser menor?
Resposta: Não, mas redução de custo é uma motivação comum.

Pergunta: Temperatura alta sempre melhora?
Resposta: Não. Pode dar mais peso a alternativas pouco informativas; é um hiperparâmetro para validação.

Pergunta: Professor e aluno precisam ter tamanhos diferentes?
Resposta: Não. A distinção é o papel de supervisão; podem até compartilhar arquitetura e checkpoint inicial.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T178:C05 — mecanismo_avancado

Soft targets preservam relações entre alternativas que desaparecem quando se guarda apenas a classe ou token vencedor. A temperatura suaviza essas distribuições, mas também muda a escala do gradiente. O trabalho clássico discute compensação por T² ao combinar objetivos suaves e rótulos, sob sua análise. Em LLMs, acesso somente ao texto gerado permite destilação de sequências, mas não reconstrói integralmente a distribuição do professor.

Condição de contorno:
Um professor incorreto ou descalibrado transmite seus erros; concordância com ele não é um critério independente de verdade.

Contrato proposto:
- Entradas: Entradas de transferência, respostas ou logits do professor e alvos corretos quando disponíveis.
- Saídas: Aluno ajustado e avaliação independente de qualidade e custo.
- Estado: Configuração do professor, temperatura, filtros e mistura de objetivos.
- Invariante: O sinal de supervisão mantém registro de como foi produzido e do que realmente contém.

Compromissos de projeto:
- Logits fornecem informação adicional e custam armazenamento e compatibilidade de vocabulário.
- Textos são mais portáveis e descartam probabilidades das alternativas não amostradas.

## T178:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir exemplos em que o professor erra com alta confiança e variar temperatura mantendo a mistura controlada. Esperar que avaliação externa revele erros herdados, mesmo com boa imitação.

Plano de avaliação proposto:
Plano proposto: comparar aluno base, treino com rótulos e destilação usando o mesmo orçamento. Medir qualidade contra referência, divergência do professor quando observável e latência; aprovar por competência e custo, sem confundir similaridade com correção.

Comparações:
- T179 (complements): Destilação de contexto é uma aplicação da transferência com informação privilegiada restrita ao professor.

Afirmação rastreável:
O método clássico usa distribuições suavizadas e combina sua supervisão com rótulos conhecidos quando disponíveis.
Suporte: direct; fontes: V3B-S017
Limite: O comportamento em classificação não garante transferência completa das capacidades de um LLM.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T178:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou soft targets e destilação textual. Esta camada separa políticas de amostragem, professores múltiplos e limites de capacidade do aluno, usando casos industriais com seus portes efetivos.

Dados do aluno ou do professor
Na destilação on-policy, o professor avalia trajetórias que o aluno tende a produzir, aproximando treino das situações de implantação. Dados apenas do professor podem conter caminhos que o aluno raramente consegue seguir. A receita Tinker e o estudo associado descrevem essa diferença; o sinal disponível continua dependendo de logits ou texto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012.

Professores com papéis
Combinar professores de relevância, engajamento ou embedding exige normalizar objetivos e resolver conflitos. O caso de busca de vagas do LinkedIn descreve esse desenho para um aluno de ranking de 0,6B. É evidência de mecanismo industrial, não demonstração de um gerador 3–30B equivalente nem do mesmo componente que interpreta consultas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012.

Capacidade e cobertura
O aluno pode reproduzir padrões frequentes e falhar em exceções ou raciocínios longos. Meça cobertura de tipos de tarefa, não só concordância média. Uma política proposta mantém rótulos corretos e exemplos difíceis revisados, para que imitar o professor não se torne o único objetivo mesmo quando ele erra.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012.

USO AVANÇADO — Professor offline, aluno online
Cenário: Chamadas caras são aceitáveis na criação de dados.
Estratégia: Gere exemplos por categorias, filtre erros com verificadores e ajuste o aluno. Compare custo de construir e atualizar o dataset com economia no uso recorrente.
Papel do modelo pequeno: Um 3–7B pode executar uma tarefa estreita que não exige toda a capacidade do professor.
Aceite proposto: Qualidade em casos novos e custo total por resposta aceita após amortizar treinamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012.

USO AVANÇADO — Aluno que sai do caminho esperado
Cenário: Trajetórias livres produzem estados não vistos no treino.
Estratégia: Colete estados do aluno em ambiente controlado e obtenha correções do professor ou de ferramentas. Inclua falhas reais, mantendo um conjunto final intocado.
Papel do modelo pequeno: Um 8–14B pode melhorar execução de procedimentos mediante supervisão compatível.
Aceite proposto: Avaliar sucesso de ponta a ponta e recuperação, não somente loss de imitação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Adequado a habilidades e formatos delimitados; limites de capacidade devem aparecer na avaliação.
8–14B: Pode absorver repertório maior, mas ainda precisa de evidência externa para fatos variáveis.
15–30B: Compare destilar com adaptar diretamente o 15–30B; o custo de professor não é gratuito.
Requisitos de treino/runtime: Treinamento com proveniência do sinal; textos não reconstituem logits completos. Receitas e modelos disponíveis mudam entre versões.
Não aplicar quando: Não inferir porte de produção a partir de exemplos BERT ou ranking menores que 3B.

## T178:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: Destilação de conhecimento é explicitamente usada no pipeline de produção.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C009 — Microsoft / Bing — inferência BERT
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Microsoft relata que modelos BERT destilados e otimizações de inferência foram usados em produção no Bing para tarefas de linguagem e busca.
Mecanismo documentado: Redução do professor a encoder de três camadas e posterior otimização de execução; parte das melhorias foi disponibilizada no ONNX Runtime.
Correspondência com esta base: Destilação de conhecimento é descrita antes da implantação.
Transferência proposta para modelo pequeno: Proposta: testar um modelo especializado ou até um encoder menor antes de usar um gerador 3–30B para classificação/ranking.
Limite: Caso histórico de encoder, abaixo da escala e distinto do decode autoregressivo solicitado. Não atribuir ganhos de GPU/C++ à destilação isoladamente nem generalizar precisão de busca a geração aberta.
Fontes: V4B-S009.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Professor gera exemplos para treinar o modelo menor.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

V4D-C005 — DeepSeek-AI / DeepSeek-R1-Distill 7B/8B/14B
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores disponibilizam modelos menores afinados com amostras do professor e publicam avaliações.
Mecanismo documentado: SFT/destilação de respostas de um modelo maior para modelos densos menores.
Correspondência com esta base: O projeto descreve explicitamente destilação para modelos menores.
Transferência proposta para modelo pequeno: Proposta: selecionar tarefas verificáveis, filtrar demonstrações por teste externo, isolar famílias entre treino/teste e comparar custo total incluindo o professor.
Limite: Pesquisa, não produção. Comparadores são versões históricas; 32B/70B não pertencem à faixa solicitada. Mais amostras têm custo e consenso não elimina erros correlacionados.
Fontes: V4D-S008, V4D-S010.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: Experimentos são de transferência professor-aluno.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q008, V4B-Q009.

## T178:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T178 → T182 [complements]
Como combinar: Learning Zone descreve dados do professor usados na especialização por LoRA.
Interface: Exemplos filtrados e adapter treinado.
Condição: Escopo é a tarefa educacional documentada.
Aceite proposto: Confrontar avaliação automática com resultados humanos.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T178 → T199 [complements]
Como combinar: Erros avaliados podem selecionar novos exemplos para o próximo ciclo.
Interface: Resultado verificado, categoria e versão.
Condição: Aprendizagem persistente exige uma atualização explícita.
Aceite proposto: Medir melhora em casos novos após a atualização.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S017, V4B-S005, V4B-S009, V4B-S012, V4B-S013, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não treinar apenas sobre respostas que parecem convincentes sem checagem.
- Registrar limitações de licença, acesso e fidelidade do sinal do professor no manifest operacional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A meta razoável é igualar ou superar um baseline em uma distribuição estreita com custo menor. A destilação não transfere automaticamente toda a inteligência, conhecimento ou robustez do professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T179, T180, T181

## Fontes primárias associadas

### C-S032 — Distilling the Knowledge in a Neural Network

[https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Destilação transfere comportamento de professor ou ensemble a modelo aluno.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S017 — Distilling the Knowledge in a Neural Network — full text

[https://arxiv.org/html/1503.02531v1](https://arxiv.org/html/1503.02531v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Soft targets, temperatura e escala do sinal de distilação.

Limite: Texto do método consultado; extensões para LLMs e contratos de produção são propostas editoriais.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S009 — Microsoft open sources breakthrough optimizations for transformer inference on GPU and CPU

[https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/](https://opensource.microsoft.com/blog/2020/01/21/microsoft-onnx-open-source-optimizations-transformer-inference-gpu-cpu/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Bing usou destilação de BERT e otimizações de inferência em produção; integração posterior no ONNX Runtime.

Limite: Caso histórico de encoder, não LLM autoregressivo de 3–30B; não somar ganhos de hardware e algoritmo como efeito de destilação.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

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


---

# T179 — Context Distillation Paramétrica

**Nome canônico:** Context Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T179  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** destilação paramétrica de contexto

## T179:C01 — conceito

Treinamento para reproduzir comportamentos obtidos com contexto privilegiado sem precisar fornecer todo esse contexto em inferência. Instruções ou exemplos condicionam o professor; o aluno aprende a tarefa com entrada reduzida. Isso modifica parâmetros e é distinto de resumir texto ou guardá-lo em memória externa.

Como funciona:
- Executar professor com contexto extenso e entradas representativas.
- Associar entradas reduzidas às respostas verificadas produzidas.
- Ajustar o aluno e avaliar sua execução sem o contexto privilegiado.

## T179:C02 — aplicacao

Quando usar:
- Regras de comportamento estáveis e repetidas em grande volume.
- Prompt longo contém habilidades que podem ser aprendidas por exemplos.

Quando não usar:
- Fatos mutáveis, permissões obrigatórias ou registros exatos que precisam de atualização imediata.

Implementação proposta:
- Definir claramente o que será removido do prompt após treinamento.
- Curar exemplos que cubram exceções e conflitos das instruções.
- Avaliar retenção e regressão sempre que o contexto original mudar.

Aplicação LAI proposta:
Proposta: destilar habilidades estáveis da Helena depois que memória externa e avaliações já estiverem funcionando; manter dados atuais recuperáveis.

## T179:C03 — riscos_validacao

Armadilhas:
- Desempenho pode depender de instruções que o treino não internalizou.
- Mudar política depois exige adaptação ou controles explícitos fora dos pesos.

Métricas sugeridas:
- Qualidade com prompt completo versus aluno com prompt reduzido.
- Tokens economizados e custo total do ciclo de treinamento e manutenção.

Testes propostos:
- Usar casos inéditos que dependem de partes distintas do contexto original.
- Alterar uma regra e verificar se comportamento antigo permanece no adaptador.

## T179:C04 — perguntas_proveniencia

Pergunta: É uma forma de resumo?
Resposta: Não no sentido textual: aqui a compressão pretendida ocorre por aprendizado paramétrico.

Pergunta: O professor precisa ser outra LLM?
Resposta: Não. O mesmo modelo com contexto adicional pode gerar supervisão.

Pergunta: Destilar é guardar uma cópia recuperável do contexto?
Resposta: Não. O efeito fica distribuído nos parâmetros e não oferece consulta literal ou proveniência automática.

Pergunta: Quando manter RAG junto?
Resposta: Quando fatos precisam de atualização, auditoria ou acesso condicionado à consulta, além do comportamento estável aprendido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T179:C05 — mecanismo_avancado

O professor recebe informação privilegiada C e entrada X, enquanto o aluno opera somente com X. Se a resposta depende de uma variável de C que muda entre consultas e não pode ser inferida de X, não há como garantir reprodução exata em todos os casos. A destilação pode internalizar regularidades e procedimentos, mas não cria um canal para fatos futuros ou mudanças que nunca chegaram aos pesos.

Condição de contorno:
Contexto variável indispensável precisa continuar disponível por entrada, ferramenta ou recuperação; removê-lo pode tornar a tarefa subdeterminada.

Contrato proposto:
- Entradas: Pares de entrada reduzida e contexto privilegiado, saídas revisadas e distribuição de implantação.
- Saídas: Aluno capaz de executar o comportamento aprendido com o contexto reduzido declarado.
- Estado: Versões de contexto, pesos e exemplos usados na transferência.
- Invariante: A avaliação retira do aluno exatamente a informação que será ausente na implantação.

Compromissos de projeto:
- Contexto menor reduz custo por consulta e aumenta dependência da atualização dos pesos.
- Comprimir comportamento dificulta localizar ou remover uma regra específica posteriormente.

## T179:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter X igual e variar em C um fato decisivo, produzindo respostas corretas diferentes. Esperar identificação da ambiguidade, em vez de prometer que o aluno sem C reproduzirá ambas.

Plano de avaliação proposto:
Plano proposto: comparar professor com contexto, aluno base sem contexto e aluno destilado. Separar tarefas de procedimento estável e fatos variáveis; medir generalização e custo, aceitando apenas capacidades demonstradas sem vazamento do contexto privilegiado.

Comparações:
- T181 (distinct_from): AMD fornece memórias externas ao aluno; esta variante modifica parâmetros para reduzir contexto explícito.

Afirmação rastreável:
Learning by Distilling Context treina o aluno com entrada da tarefa sem as instruções ou scratchpad usados para produzir a supervisão.
Suporte: direct; fontes: C-S033
Limite: O estudo demonstra tarefas específicas; não prova compressão sem perda de informação arbitrária.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T179:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 estabeleceu o limite da informação privilegiada. Esta camada trata o que escolher para internalizar, como testar redução de dependência do contexto e como atualizar um comportamento que ficou nos pesos.

Decompor o contexto
Classifique o material do professor em procedimento estável, exemplos, fatos mutáveis e dados de acesso restrito. Internalizar procedimentos pode reduzir instruções; fatos dinâmicos continuam precisando de entrada ou recuperação. Dados que variam por usuário não devem desaparecer sem um identificador autorizado que preserve a distinção entre casos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

Teste de informação removida
Compare professor com contexto, aluno sem contexto e aluno com um resumo mínimo. Use casos em que a informação omitida muda a resposta para revelar limites de identificabilidade. Se o aluno acerta apenas por correlações do dataset, uma troca de entidade ou de versão pode expor a dependência indevida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

Atualização e revogação
Depois de incorporar um comportamento nos pesos, editar o documento de origem não atualiza o modelo. Versione a relação entre contexto e checkpoint e defina quando retreinar ou voltar a fornecer instruções explícitas. Remover um arquivo do RAG também não demonstra remoção de informação internalizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

USO AVANÇADO — Procedimento estável de classificação
Cenário: Um manual extenso define categorias duráveis.
Estratégia: Produza exemplos contrastivos, incluindo fronteiras e exceções, e ajuste um aluno que recebe somente os campos variáveis. Mantenha a versão do manual no manifest e no teste.
Papel do modelo pequeno: Um 3–7B pode classificar casos estreitos sem reler o manual inteiro a cada pedido.
Aceite proposto: Avaliar casos novos e mudanças controladas de regra, com abstenção quando faltam dados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

USO AVANÇADO — Rotina de ferramentas
Cenário: O professor usa contexto com convenções de uma API.
Estratégia: Destile padrões estáveis, mas mantenha schema, versão e credenciais fora dos pesos. Teste execução contra a API atual e simule mudanças de contrato.
Papel do modelo pequeno: Um 8–14B pode aprender procedimento sem memorizar valores de sessão.
Aceite proposto: Medir sucesso executável e capacidade de reconhecer contrato incompatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S033, V4B-S012, V4B-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize regras simples e estáveis, com exceções claramente testáveis.
8–14B: Procedimentos mais extensos podem ser estudados, mas não presuma retenção completa de um manual.
15–30B: Compare com recuperação do contexto: maior capacidade pode tornar desnecessário internalizar fatos difíceis de atualizar.
Requisitos de treino/runtime: Exige treinamento e pares que removam do aluno exatamente a informação ausente no uso real.
Não aplicar quando: Não destilar variáveis secretas ou futuras como se o aluno pudesse inferi-las sem um canal de entrada.

## T179:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: Receita de prompt distillation transfere comportamento condicionado por contexto.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## T179:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T179 → T180 [complements]
Como combinar: A decomposição do contexto identifica quais instruções do prompt podem virar comportamento.
Interface: Regras estáveis e parâmetros que permanecem explícitos.
Condição: Sem ambiguidade entre regimes de tarefa.
Aceite proposto: Testar mudanças de parâmetro que devem alterar a saída.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S033, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T179 → T009 [complements]
Como combinar: Recuperação mantém fatos variáveis fora dos pesos enquanto procedimentos são aprendidos.
Interface: Documento vigente e versão do comportamento.
Condição: Aluno distingue evidência atual de padrão aprendido.
Aceite proposto: Testar contradições entre memória paramétrica e documento atualizado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S033, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Avaliar por origem e tempo, evitando que exemplos quase iguais ocultem falta de informação.
- Não afirmar que redução de prompt preservou todos os detalhes sem testar as exceções.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare com fronteira recebendo a mesma informação disponível na implantação. O aluno pode executar uma rotina específica com menos contexto, mas não reproduzir informação privada que foi retirada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T069, T177, T178, T180

## Fontes primárias associadas

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T180 — Prompt Distillation

**Nome canônico:** Prompt Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T179  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** destilação de prompt

## T180:C01 — conceito

Especialização de destilação de contexto orientada a substituir instruções extensas por comportamento treinado. O professor recebe o prompt detalhado e gera exemplos; o aluno é ajustado para resolver a tarefa com instrução reduzida. Neste catálogo o termo se refere a treinamento, não a compressor textual de prompts.

Como funciona:
- Selecionar o comportamento repetitivo descrito pelo prompt.
- Gerar e revisar exemplos com professor condicionado por essas instruções.
- Treinar aluno e comparar com versões que ainda recebem o prompt completo.

Nota de nomenclatura: Variante próxima de T179; os dois nomes não devem ser contados como tecnologias inteiramente independentes.

## T180:C02 — aplicacao

Quando usar:
- Classificação ou extração com critérios estáveis.
- Prompt repetido representa parcela importante do custo de inferência.

Quando não usar:
- Instruções mudam frequentemente ou contêm restrições que precisam ser garantidas pelo runtime.

Implementação proposta:
- Versionar prompt-professor e dataset derivados como uma unidade.
- Separar dados sintéticos de avaliação independente.
- Planejar troca e reversão de adaptadores quando a instrução mudar.

Aplicação LAI proposta:
Proposta: considerar uma receita de destilação para tarefas padronizadas da Helena, sem presumir que ela ensina fatos atualizados sobre clientes.

## T180:C03 — riscos_validacao

Armadilhas:
- Dados sintéticos podem cobrir mal casos limítrofes do prompt.
- Reduzir prompt sem medir retenção pode perder exceções importantes.

Métricas sugeridas:
- Acerto com instrução curta e retenção das regras.
- Economia líquida após geração de dados, treino e manutenção.

Testes propostos:
- Testar exemplos novos que exigem cada exceção relevante da instrução.
- Comparar aluno treinado com aluno base usando o mesmo prompt curto.

## T180:C04 — perguntas_proveniencia

Pergunta: Prompt Distillation dispensa treino?
Resposta: Na acepção usada aqui, não; o comportamento é incorporado aos parâmetros ou adaptadores.

Pergunta: É independente de Context Distillation?
Resposta: É uma forma próxima e mais específica; mantemos o nome para recuperação.

Pergunta: Pode apagar o prompt original depois?
Resposta: Preserve-o como especificação versionada; ele ajuda a auditar e reconstruir o comportamento pretendido.

Pergunta: Um rótulo válido basta para avaliar?
Resposta: Não. Valide também sua correspondência com a entrada e as regras, especialmente exceções raras não cobertas pela geração sintética.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T180:C05 — mecanismo_avancado

Um prompt extenso costuma misturar regras estáveis, exemplos e parâmetros variáveis. Antes de destilar, é útil separar o que deverá virar comportamento dos valores que ainda precisam chegar a cada consulta. Instruções incompatíveis podem exigir identificador explícito de tarefa; treinar as mesmas entradas com saídas contraditórias não ensina ao aluno qual regime escolher. O contrato de saída também deve ser validado fora da própria geração do professor.

Condição de contorno:
Quando a política muda frequentemente, o custo de gerar dados, treinar e revalidar pode superar a economia de tokens.

Contrato proposto:
- Entradas: Prompt versionado, consultas representativas, parâmetros variáveis e respostas verificadas.
- Saídas: Modelo ajustado e instrução mínima necessária para selecionar o comportamento.
- Estado: Versão do comportamento, conjunto sintético e critérios de validação.
- Invariante: Parâmetros que variam por consulta não desaparecem sem outra forma de identificá-los.

Compromissos de projeto:
- Menos instruções repetidas reduzem contexto e aumentam custo de manutenção do modelo.
- Exemplos sintéticos amplificam cobertura e podem repetir erros sistemáticos do professor.

## T180:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas políticas que produzem rótulos diferentes para a mesma entrada, sem identificador de regime. Esperar falha diagnosticada; depois acrescentar a variável necessária e reavaliar.

Plano de avaliação proposto:
Plano proposto: comparar prompt integral, prompt reduzido sem treino e aluno destilado. Medir cumprimento de regras, casos limítrofes, custo total de manutenção e inferência; aprovar economia somente quando o comportamento necessário permanece demonstrável.

Comparações:
- T179 (specializes): Foca transferência de instruções recorrentes, mantendo explícita a informação variável indispensável.

Afirmação rastreável:
A receita Tinker gera respostas com um prompt no professor e treina o aluno para prevê-las sem receber esse prompt.
Suporte: direct; fontes: C-S034
Limite: A receita ilustrativa não garante internalização completa de regras extensas ou contraditórias.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T180:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou regras e parâmetros variáveis. A nova camada trata compressão de instruções como contrato de interface, com testes de seleção de regime, atualização e interação com o template.

Prompt mínimo explícito
Reduzir o prompt não significa eliminar toda instrução. Preserve identificador da tarefa, parâmetros variáveis e formato que ainda precisa ser selecionado. Defina o conjunto mínimo por ablação, removendo blocos separadamente; uma redução grande de tokens pode ocultar regressões em casos raros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

Contrato de comportamento
O adapter ou checkpoint passa a carregar parte das regras. Versione essa política junto ao endpoint e evite combinar um prompt antigo com pesos novos sem teste. Templates e tokens de sistema podem ativar comportamentos diferentes; a destilação deve ser avaliada no caminho de chat usado pelo produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

Economia real
Menos tokens de entrada pode reduzir prefill e custo, mas respostas mais longas, retries ou validações adicionais podem consumir a economia. Meça o pedido completo e o custo de atualizar dados. Learning Zone descreve especialização com prompt reduzido e guardrails; isso não equivale a multiplicação geral de inteligência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

USO AVANÇADO — Objetos de domínio repetidos
Cenário: O serviço sempre gera o mesmo tipo de estrutura.
Estratégia: Treine exemplos variados e mantenha schema explícito ou decodificação restrita. Remova instruções apenas depois de verificar formato e conteúdo em casos inéditos.
Papel do modelo pequeno: Um 3–7B pode produzir objetos estreitos com baixa carga de prompt.
Aceite proposto: Reduzir tokens de entrada sem elevar rejeição ou erro por campo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

USO AVANÇADO — Múltiplas rotinas especializadas
Cenário: O mesmo aluno executa contratos parecidos.
Estratégia: Use identificadores de tarefa e exemplos que distinguem situações próximas. Se houver conflito persistente, separe adapters ou endpoints em vez de esconder a ambiguidade.
Papel do modelo pequeno: Um 8–14B pode compartilhar capacidade entre rotinas relacionadas, com seleção verificável.
Aceite proposto: Testar troca de tarefa e resistência a instruções que contradizem o contrato vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Boa hipótese para formatos e procedimentos fixos; fatos por usuário continuam externos.
8–14B: Avalie interferência entre tarefas e escolha explícita do comportamento.
15–30B: Compare economia de prefill com custo de manutenção de modelos e adapters adicionais.
Requisitos de treino/runtime: Exige ajuste de pesos/adapters; encurtar manualmente um prompt sem treino é outra intervenção.
Não aplicar quando: Não remover campos que distinguem respostas corretas apenas porque o dataset usa valores quase constantes.

## T180:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Parte das instruções foi absorvida no adaptador; avaliação continua necessária.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: A receita específica reduz instruções na entrada do aluno.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## T180:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T180 → T182 [complements]
Como combinar: A especialização por LoRA pode absorver parte das instruções, como no caso Learning Zone.
Interface: Adapter, prompt reduzido e versão da tarefa.
Condição: Escopo documentado é especializado e continua sujeito a validação.
Aceite proposto: Comparar resposta e rejeição com a versão de prompt completo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T180 → T193 [complements]
Como combinar: Guardrails verificam restrições que não devem depender da memória do modelo.
Interface: Saída estruturada e regras externas.
Condição: Critérios explícitos e atualizados.
Aceite proposto: Testar casos adversos que o treino não cobriu.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S034, V3D-S008, V4B-S012, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Acompanhar tokens de saída e retries para não anunciar economia só de entrada.
- Manter baseline com instruções completas para diagnosticar regressões.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a rotina destilada com um modelo de fronteira usando o mesmo contrato de saída. Redução de prompt pode melhorar custo e consistência local, sem comprovar paridade fora da rotina.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T155, T179, R012

## Fontes primárias associadas

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T181 — Agent Memory Distillation

**Nome canônico:** Agent Memory Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T181  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** AMD; destilação de memória de agentes

## T181:C01 — conceito

No trabalho de Kim, Kim e Hwang identificado como AMD, conhecimento de trajetórias bem-sucedidas de um agente professor é organizado em memórias de workflow, subtarefa e função. O aluno recupera essas memórias durante a execução, sem atualização dos pesos no método descrito.

Como funciona:
- Extrair estratégias, exemplos intermediários e convenções de chamada de trajetórias do professor.
- Fornecer memórias de workflow e subtarefa antes da execução.
- Recuperar memória de função quando surgirem erros de uso de ferramentas.

Nota de nomenclatura: Identificação confirmada em arXiv:2608.07169; não confundir com qualquer método chamado genericamente memory distillation.

## T181:C02 — aplicacao

Quando usar:
- Aluno tem dificuldade de produzir trajetórias próprias bem-sucedidas.
- Procedimentos podem ser representados em exemplos e guias recuperáveis.

Quando não usar:
- Assumir que memória de ferramenta antiga continua aplicável após mudança de API ou ambiente.

Implementação proposta:
- Conservar trajetória original, versão de ferramenta e evidência de sucesso.
- Separar memória procedural da verdade factual e da autorização de ação.
- Avaliar recuperação e transferência em tarefas não vistas pelo professor.

Aplicação LAI proposta:
Proposta: criar memória procedural da Helena a partir de missões comprovadas por modelos fortes e avaliar no modelo local antes de considerar treinamento.

## T181:C03 — riscos_validacao

Armadilhas:
- Procedimento do professor pode exigir capacidade que o aluno não possui.
- Memórias sem condições de aplicação podem induzir ações inadequadas.

Métricas sugeridas:
- Sucesso de uso de ferramentas com e sem memória.
- Ganho por granularidade de memória e custo de recuperação.

Testes propostos:
- Comparar aluno base, memória genérica e memória hierárquica no mesmo conjunto reservado.
- Mudar versão de função e testar invalidação de guias incompatíveis.

## T181:C04 — perguntas_proveniencia

Pergunta: AMD modifica os pesos do aluno?
Resposta: O trabalho identificado usa transferência por memória externa, sem treinamento do aluno.

Pergunta: Resultados em modelos pequenos provam ganho no meu Qwen?
Resposta: Não. Essa combinação precisa de avaliação própria.

Pergunta: Por que sucesso do professor não basta?
Resposta: Pode depender de ferramentas, contexto ou habilidades que o aluno não possui; condições de execução precisam acompanhar a memória.

Pergunta: AMD é necessariamente fine-tuning?
Resposta: Não no método identificado por esta ficha: trata-se de framework training-free que fornece memórias ao aluno.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T181:C05 — mecanismo_avancado

A separação entre memórias proativas e reativas cria pontos diferentes de falha. Estratégias e exemplos introduzidos no início podem enviesar todo o plano; convenções de função recuperadas apenas após erro ajudam a corrigir chamadas, mas podem não aparecer quando a ferramenta retorna sucesso estrutural com conteúdo semanticamente errado. A utilidade da trajetória do professor depende de o aluno conseguir executar o procedimento no ambiente atual.

Condição de contorno:
Uma memória extraída de sucesso antigo pode ficar inválida após mudanças na API, permissões ou semântica da ferramenta.

Contrato proposto:
- Entradas: Trajetórias bem-sucedidas com evidências, contratos de ferramentas e tarefa do aluno.
- Saídas: Memórias hierárquicas com origem e sugestões aplicáveis à execução atual.
- Estado: Versões de workflow, subtarefa, função e eventos que acionam recuperação.
- Invariante: A memória preserva condições de validade e não transforma uma trajetória em regra universal.

Compromissos de projeto:
- Memórias detalhadas aumentam orientação e consumo de contexto.
- Recuperação somente após falha poupa tokens e pode perder erros sem exceção explícita.

## T181:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar um parâmetro da ferramenta e fazer outra chamada retornar sucesso com efeito errado. Esperar detecção por contrato externo; observar se a memória reativa cobre apenas o primeiro caso.

Plano de avaliação proposto:
Plano proposto: comparar aluno sem memória, memórias próprias e hierarquia do professor em tarefas novas. Medir sucesso verificado, chamadas, recuperação e tokens; realizar ablações por nível e validar atualização após mudança do ambiente.

Comparações:
- T179 (distinct_from): No AMD identificado, transferência ocorre por memória externa, sem atualização de pesos.

Afirmação rastreável:
O paper AMD descreve workflow e subtarefa proativos, com memória de função recuperada reativamente após erros de chamada.
Suporte: direct; fontes: C-S035
Limite: O trabalho consultado consta como sob revisão; seus resultados não certificam generalização para ferramentas do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T181:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu memória proativa e reativa. Esta camada organiza a memória como artefato executável versionado, com seleção por pré-condições, avaliação de transferência e expiração de procedimentos.

Memória com pré-condições
Uma trajetória bem-sucedida só é reutilizável quando ferramentas, permissões e estado do problema são compatíveis. Extraia pré-condições e resultados observados junto ao procedimento. Memória de workflow orienta o plano; memória de função deve preservar argumentos, efeitos e erros conhecidos, sem transformar valores de uma sessão em constantes universais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

Recuperação antes do erro
Falha sintática é um gatilho fácil, mas uma ferramenta pode retornar sucesso com conteúdo inadequado. Acrescente verificações de pós-condição e divergência de estado para acionar memória reativa. O aluno deve poder rejeitar uma recomendação quando suas condições não se aplicam, em vez de segui-la como instrução absoluta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

Validade temporal
Mudanças de API e ambiente podem tornar memórias antigas nocivas. Versione fonte, data e contrato, e suspenda exemplos que falham em reexecução controlada. O projeto AMD apresenta pesquisa em agentes pequenos; isso não comprova funcionamento contínuo em produção nem elimina manutenção do acervo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

USO AVANÇADO — Agente em API especializada
Cenário: As falhas se concentram em convenções pouco intuitivas.
Estratégia: Colete trajetórias autorizadas com resultados verificáveis, extraia padrões de função e recupere somente os compatíveis com a versão atual. Teste erros que exigem abandonar a receita.
Papel do modelo pequeno: Um 3–7B pode receber instrução procedural concreta em vez de inferir tudo do nome da ferramenta.
Aceite proposto: Medir conclusão de tarefa e ações incorretas, incluindo casos novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

USO AVANÇADO — Workflow com muitas etapas
Cenário: O aluno se perde entre subtarefas recorrentes.
Estratégia: Recupere um esqueleto de workflow, depois detalhe apenas a etapa atual. Preserve estado real fora do texto e verifique cada transição relevante.
Papel do modelo pequeno: Um 8–14B pode usar memória hierárquica para reduzir carga de planejamento.
Aceite proposto: Avaliar execução completa, adaptação a desvios e custo de recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S035, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Memórias curtas e condicionais podem ajudar tarefas limitadas; excesso de exemplos compete pela janela.
8–14B: Explore hierarquia e seleção por etapa, evitando inserir todo o acervo em cada prompt.
15–30B: Compare benefício marginal com capacidade própria do 15–30B e custo de manter memórias.
Requisitos de treino/runtime: No método descrito, memória externa não exige necessariamente atualizar pesos; não confundir com destilação paramétrica.
Não aplicar quando: Não reaproveitar credenciais, caminhos ou dados de clientes contidos em trajetórias sem tratamento apropriado.

## T181:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: A referência trata de Agent Memory Distillation.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q023.

## T181:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T181 → T204 [complements]
Como combinar: Memórias de função podem virar habilidades com contrato de entrada, saída e versão.
Interface: Procedimento, pré-condições e pós-condições.
Condição: Execução atual satisfaz o contrato.
Aceite proposto: Reexecutar em casos novos e detectar incompatibilidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S035, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T181 → T195 [requires]
Como combinar: Ferramentas e testes verificam se a trajetória transferida realmente funcionou.
Interface: Resultados de execução e estado final.
Condição: Oráculo de sucesso independente da narrativa do agente.
Aceite proposto: Rejeitar trajetórias que apenas declaram sucesso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S035, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar recomendações do professor de resultados efetivamente observados.
- Testar memórias obsoletas e instruções conflitantes antes de liberar o acervo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare agentes na mesma tarefa, ferramentas e orçamento. Benchmarks AMD não demonstram equivalência geral; o benefício depende de o procedimento ser recuperado e executável no ambiente atual.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T055, T062, T178, T204

## Fontes primárias associadas

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T182 — LoRA

**Nome canônico:** Low-Rank Adaptation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T182  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Low-Rank Adaptation; adaptação de baixo posto

## T182:C01 — conceito

Adaptação por matrizes de baixo posto: uma base congelada recebe atualização treinável ΔW = B × A. Em vez de ajustar toda uma matriz, treina-se sua fatoração com posto reduzido. LoRA diminui parâmetros treináveis, mas não elimina memória necessária à base, às ativações e ao otimizador.

Como funciona:
- Escolher módulos-alvo compatíveis com a arquitetura.
- Congelar pesos base e treinar fatores de baixo posto.
- Carregar adaptador junto da base correta ou fundi-lo quando o formato permitir.

## T182:C02 — aplicacao

Quando usar:
- Especialização recorrente com orçamento limitado de treinamento.
- Necessidade de manter adaptações separadas por tarefa ou domínio.

Quando não usar:
- Assumir que qualquer adaptador funciona com checkpoint, tokenizer ou arquitetura diferentes.

Implementação proposta:
- Registrar hash da base, módulos-alvo, posto e escala.
- Avaliar cobertura das tarefas antes de aumentar o posto.
- Medir latência e memória do modo de serving escolhido.

Aplicação LAI proposta:
Proposta: usar LoRA para habilidades estáveis da Helena quando avaliação mostrar vantagem sobre apenas melhorar prompt e recuperação.

## T182:C03 — riscos_validacao

Armadilhas:
- Base incompatível pode carregar sem representar comportamento válido.
- Vários adaptadores simultâneos exigem controle de roteamento e capacidade no runtime.

Métricas sugeridas:
- Qualidade por número de parâmetros treináveis.
- Memória de treino e latência de inferência com adaptador.

Testes propostos:
- Carregar a combinação exata em processo limpo e repetir avaliação.
- Remover adaptador e confirmar comparação com a base sem alterar outros fatores.

## T182:C04 — perguntas_proveniencia

Pergunta: LoRA é uma base de conhecimento factual?
Resposta: Não. É um mecanismo de treinamento de parâmetros adicionais.

Pergunta: Pode compartilhar adaptador entre modelos diferentes?
Resposta: Só quando existe compatibilidade explicitamente demonstrada; não deve ser presumida.

Pergunta: Pode aplicar a qualquer base da mesma dimensão?
Resposta: Dimensão compatível não garante significado compatível; preserve identidade exata da base e módulos.

Pergunta: Merge seguido de quantização é exato?
Resposta: A soma em maior precisão pode ser equivalente antes da nova quantização; arredondamento adicional pode alterar o resultado.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T182:C05 — mecanismo_avancado

Para W de dimensão d×k e posto r, os fatores treináveis usam r(d+k) parâmetros, antes de bias e módulos adicionais. A inicialização original usa um fator aleatório e outro zero, mantendo a atualização inicial nula. Inicializar ambos em zero pode bloquear seus gradientes por dependência multiplicativa. A escala da atualização também faz parte do adaptador e precisa acompanhar os pesos no carregamento ou fusão.

Condição de contorno:
Um adaptador pequeno não torna barata toda a etapa: base, ativações e estados do otimizador continuam relevantes.

Contrato proposto:
- Entradas: Base identificada, módulos-alvo, fatores A/B, posto e escala.
- Saídas: Atualização treinada e artefato que registra sua base compatível.
- Estado: Pesos congelados, parâmetros treináveis e convenção de orientação das matrizes.
- Invariante: A atualização é aplicada uma única vez, com a escala e a base corretas.

Compromissos de projeto:
- Posto maior amplia liberdade e custo de treinamento e armazenamento.
- Fusão reduz operações auxiliares, mas exige cuidados ao alternar adaptadores ou requantizar.

## T182:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inicializar ambos os fatores em zero e observar ausência de aprendizado; também carregar um adaptador já fundido como se ainda fosse separado. Esperar detecção de gradientes bloqueados e aplicação duplicada.

Plano de avaliação proposto:
Plano proposto: comparar postos com os mesmos dados, módulos e orçamento. Medir parâmetros treináveis, memória, gradientes, qualidade e latência fundida/separada; escolher pelo desempenho externo, sem presumir que posto maior sempre melhora.

Comparações:
- T183 (complements): QLoRA mantém base quantizada durante o treinamento dos fatores, acrescentando outra fonte de erro e economia.

Afirmação rastreável:
O LoRA original inicializa A aleatoriamente e B em zero, usando atualização escalada de baixo posto.
Suporte: direct; fontes: C-S036
Limite: Outras variantes podem escolher inicializações e escalas diferentes; o contrato deve registrar qual foi usado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T182:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu fatores, inicialização e escala. O aprofundamento cobre seleção de módulos, composição de adapters e consistência entre treinamento, fusão e serving.

Capacidade onde importa
Posto maior aumenta parâmetros treináveis, mas o efeito depende dos módulos escolhidos. Compare projeções de atenção, MLP e outras opções suportadas mediante uma hipótese de erro. Alterar todos os módulos e o posto simultaneamente impede entender qual intervenção ajudou; mantenha uma matriz pequena de ablações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S036, V4B-S006, V4D-S012.

Composição e identidade
Adapters podem ser alternados, combinados ou fundidos, mas essas operações não garantem compatibilidade semântica. Registre base, escala e ordem. Um adapter de formato e outro de domínio podem interferir; avalie a combinação explicitamente e inclua identidade do adapter em cache de prefixo e roteamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S036, V4B-S006, V4D-S012.

Fusão e precisão
Fundir a atualização aos pesos pode reduzir overhead de execução, mas exige evitar aplicação dupla. Se a base está quantizada, desquantizar, fundir e requantizar pode introduzir erro adicional. Teste o caminho final de distribuição, não somente o adapter separado no ambiente de treinamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S036, V4B-S006, V4D-S012.

USO AVANÇADO — Especialização por cliente
Cenário: Clientes compartilham base, mas possuem contratos distintos.
Estratégia: Mantenha adapters versionados e seleção autorizada por pedido. Valide isolamento e evite cache reutilizado entre configurações diferentes. Compare custo de servir vários adapters com réplicas especializadas.
Papel do modelo pequeno: Um 8–14B pode compartilhar base mantendo adaptações pequenas.
Aceite proposto: Nenhuma mistura de comportamento ou cache entre clientes; qualidade medida por contrato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S036, V4B-S006, V4D-S012.

USO AVANÇADO — Professor cria dados para aluno
Cenário: Uma tarefa possui respostas verificáveis.
Estratégia: Use exemplos filtrados para LoRA e mantenha validação externa. Learning Zone documenta essa combinação em escopo educacional, com limites de disponibilidade e avaliação humana.
Papel do modelo pequeno: Um 3–7B pode aprender formato e terminologia sem ajuste completo.
Aceite proposto: Melhora em origens novas e manutenção de capacidades necessárias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S036, V4B-S006, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Posto pequeno não é garantia de suficiência; testar erros do domínio e exceções.
8–14B: Vários adapters exigem governança de identidade e avaliação de interferência.
15–30B: Economia de parâmetros treináveis não elimina memória de ativações nem custo da base 15–30B.
Requisitos de treino/runtime: Treinamento de fatores e runtime compatível; módulos-alvo e orientação devem corresponder ao checkpoint real.
Não aplicar quando: Não aplicar adapter a uma base apenas porque nome e dimensões parecem semelhantes.

## T182:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: LoRA é avaliada, sem afirmar que toda configuração é modelo de produto lançado.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Especialização realizada por adaptadores LoRA.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: Adaptadores de baixo rank são documentados, mas não se deve universalizar o treino para qualquer LoRA externa.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q007.

## T182:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T182 → T178 [complements]
Como combinar: Learning Zone descreve dados do professor alimentando especialização LoRA.
Interface: Dados filtrados e configuração de adaptação.
Condição: Escopo especializado, sem equivalência geral.
Aceite proposto: Confrontar avaliação automática e humana.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T182 → T082 [requires]
Como combinar: Cache de prefixo precisa distinguir adapters que alteram os estados.
Interface: Identificador e versão do adapter.
Condição: Reúso somente com identidade completa igual.
Aceite proposto: Executar o mesmo prompt com adapters diferentes e verificar isolamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S036, V4B-S006, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Detectar atualização aplicada duas vezes depois de fusão.
- Comparar saídas antes e depois de exportar, fundir ou requantizar.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
LoRA pode tornar um pequeno modelo competitivo numa tarefa delimitada. O número de parâmetros treinados não mede o conhecimento transferido nem assegura ausência de regressões.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T179, T183

## Fontes primárias associadas

### C-S036 — LoRA: Low-Rank Adaptation of Large Language Models

[https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesos base congelados recebem atualização treinável fatorada de baixo posto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T183 — QLoRA

**Nome canônico:** QLoRA  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T183  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ajuste fino com LoRA sobre base quantizada

## T183:C01 — conceito

Método de ajuste fino que mantém a base quantizada e congelada enquanto treina adaptadores LoRA. A proposta original combina quantização de quatro bits, NF4, dupla quantização e gerenciamento de memória por otimizadores paginados. Não equivale a qualquer treino ou inferência com pesos INT4.

Como funciona:
- Carregar base em representação quantizada compatível com a implementação de treino.
- Propagar gradientes através das operações para atualizar adaptadores.
- Avaliar adaptador com o caminho real de inferência e quantização adotado.

## T183:C02 — aplicacao

Quando usar:
- Treinamento de adaptação limitado por memória da GPU.
- Há stack compatível e dataset com qualidade suficiente para justificar o treino.

Quando não usar:
- Supor que checkpoint AWQ, GPTQ ou outro formato de serving pode ser treinado pela mesma receita sem adaptação.

Implementação proposta:
- Confirmar suporte do modelo, módulos e bibliotecas antes de estimar VRAM.
- Controlar tamanho de sequência, batch e acumulação de gradiente.
- Comparar memória alocada, qualidade e estabilidade com alternativas viáveis.

Aplicação LAI proposta:
Proposta: estimar viabilidade de QLoRA no hardware real da LAI por medição; o número de parâmetros sozinho não determina se o treino cabe.

## T183:C03 — riscos_validacao

Armadilhas:
- Memória de ativações cresce com comprimento e pode dominar a economia dos pesos.
- Exportação ou troca de quantização pode alterar resultado do adaptador.

Métricas sugeridas:
- Pico de VRAM, velocidade de treinamento e qualidade reservada.
- Diferença entre avaliação durante treino e no servidor final.

Testes propostos:
- Executar pequeno treino de compatibilidade com dados conhecidos antes de ampliar.
- Recarregar checkpoint exportado e verificar regressão em formato e conteúdo.

## T183:C04 — perguntas_proveniencia

Pergunta: QLoRA significa treinar todos os pesos em quatro bits?
Resposta: Não. A base fica congelada; os adaptadores recebem as atualizações.

Pergunta: Rodar modelo INT4 prova que consigo treiná-lo?
Resposta: Não. Treino exige memória e operadores adicionais.

Pergunta: O checkpoint final necessariamente é NF4?
Resposta: Não. A estratégia de exportação e serviço pode usar outra representação, exigindo avaliação após a conversão.

Pergunta: Quatro bits no peso significam quatro bits no cálculo?
Resposta: Não. Desquantização e acumulação podem usar precisão maior; inspecione o caminho efetivo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T183:C05 — mecanismo_avancado

A base quantizada permanece congelada, mas o gradiente atravessa a operação que a utiliza para chegar aos adaptadores. NF4 é uma representação de quatro bits com níveis próprios, não sinônimo de inteiro uniforme INT4. Double quantization comprime constantes de quantização; otimizadores paginados tratam picos de memória de treinamento. Nenhum desses componentes descreve automaticamente o cache KV ou o caminho final do servidor.

Condição de contorno:
A memória reduzida da base não elimina ativações extensas, temporários e estados dos parâmetros treináveis.

Contrato proposto:
- Entradas: Base quantizada, configuração NF4 ou alternativa declarada, adaptadores e dados de ajuste.
- Saídas: Adaptador treinado e avaliação no caminho exato de implantação.
- Estado: Escalas quantizadas, base congelada, otimizador e dtype de computação.
- Invariante: Somente os parâmetros autorizados recebem atualização; representação da base permanece identificável.

Compromissos de projeto:
- Base menor permite ajuste em menos memória e introduz aproximação numérica.
- Exportar e requantizar pode acrescentar erro além daquele observado durante treino.

## T183:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: verificar que pesos base não mudam enquanto fatores recebem gradientes; depois comparar adaptador separado, fusão e requantização. Esperar diferenças explicitamente medidas, não equivalência presumida.

Plano de avaliação proposto:
Plano proposto: comparar LoRA em base de maior precisão e QLoRA com mesmos dados e módulos. Medir memória de cada parcela, estabilidade e qualidade final; repetir a avaliação após exportação no runtime de destino antes de aprovar implantação.

Comparações:
- T093 (distinct_from): Paged optimizers gerenciam memória de treinamento; PagedAttention organiza KV de inferência.

Afirmação rastreável:
QLoRA combina base quantizada congelada, adaptadores, NF4, quantização de constantes e otimizadores paginados.
Suporte: direct; fontes: C-S037
Limite: Esses mecanismos descrevem o método original; uma implementação chamada QLoRA pode selecionar opções diferentes.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T183:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou base congelada e NF4. A nova camada separa memória de treinamento de memória de serving, compara caminhos de exportação e trata qualidade como propriedade da composição final.

Contabilidade completa
QLoRA reduz armazenamento da base durante adaptação, mas ativações, gradientes dos adapters e estados do otimizador continuam existindo. Contexto, lote e módulos-alvo alteram o pico. Meça fases de forward, backward e atualização, pois um número único de memória média pode ocultar o limite real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

Treino não é entrega
O adapter treinado sobre base quantizada pode ser servido com outra representação somente após validação. Fundir em pesos de maior precisão e requantizar muda o caminho numérico. Preserve uma referência do treino e compare todas as rotas candidatas, incluindo templates e versões de kernels.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

Intervenções separadas
NF4, double quantization, otimizador paginado e checkpointing atuam em componentes diferentes. Documente quais estão ativos. O estudo da plataforma Uber explora combinações, mas isso não prova que qualquer receita funciona em toda GPU ou que cada configuração experimental virou produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

USO AVANÇADO — Adaptação sob memória limitada
Cenário: O checkpoint cabe quantizado, mas ajuste completo é inviável no orçamento.
Estratégia: Selecione módulos e lote, meça picos e acrescente checkpointing apenas quando ativações forem o problema. Teste estabilidade e compare com LoRA em precisão maior numa escala controlada.
Papel do modelo pequeno: Um 8–14B pode ser adaptado com menos memória de pesos, sem prometer uma placa específica.
Aceite proposto: Atingir qualidade-alvo com memória e tempo registrados no ambiente real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

USO AVANÇADO — Entrega em outro runtime
Cenário: O treinamento e o servidor usam bibliotecas distintas.
Estratégia: Planeje conversão e teste antes de investir no treino. Valide base, adapter, fusão e quantização final por etapas para localizar a origem de perdas.
Papel do modelo pequeno: Um 15–30B exige atenção ao custo de manter cópias temporárias durante a exportação.
Aceite proposto: Reproduzir respostas e métricas de tarefa no caminho de implantação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Pode facilitar experimentação, mas curadoria e avaliação continuam sendo custos centrais.
8–14B: Contextos longos podem tornar ativações dominantes apesar da base em quatro bits.
15–30B: Planeje recursos de exportação e validação, além do pico do treinamento.
Requisitos de treino/runtime: Treinamento eficiente com base quantizada e adapters; NF4 não é sinônimo de INT4 uniforme ou GGUF.
Não aplicar quando: Não afirmar que economia de treino garante latência menor ou o mesmo formato na inferência.

## T183:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: QLoRA é configuração estudada na infraestrutura; métricas são experimentais.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Treino contra modelo quantizado não comprova todos os detalhes do método QLoRA original.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q007, V4B-Q017.

## T183:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T183 → T115 [complements]
Como combinar: Checkpointing reduz ativações enquanto QLoRA reduz custo da base congelada.
Interface: Fronteiras de recomputação e configuração de quantização.
Condição: Gradientes dos adapters continuam corretos.
Aceite proposto: Comparar picos e convergência, isolando cada técnica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S037, V4B-S006, V4B-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T183 → T126 [alternative]
Como combinar: Uma rota de entrega pode quantizar novamente com método suportado pelo servidor.
Interface: Modelo adaptado e nova calibração.
Condição: Exportação explícita e qualidade reavaliada.
Aceite proposto: Medir perda adicional da requantização e execução final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S037, V4B-S006, V4B-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar dtype de computação e precisão dos parâmetros treináveis.
- Evitar comparar lotes ou contextos diferentes como se a memória poupada viesse só de QLoRA.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O resultado a comparar é o modelo adaptado no servidor final. QLoRA viabiliza um processo de treinamento; não demonstra por si mesma paridade de qualidade ou custo com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T124, T177, T182

## Fontes primárias associadas

### C-S037 — QLoRA: Efficient Finetuning of Quantized LLMs

[https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treina adaptadores através de base quantizada e congelada; NF4, dupla quantização e otimizadores paginados fazem parte da proposta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S036 — LoRA: Low-Rank Adaptation of Large Language Models

[https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesos base congelados recebem atualização treinável fatorada de baixo posto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

### V4B-S028 — Current and New Activation Checkpointing Techniques in PyTorch

[https://pytorch.org/blog/activation-checkpointing-techniques/](https://pytorch.org/blog/activation-checkpointing-techniques/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoint seletivo por operação e políticas de memória/recomputação para forward/backward.

Limite: Disponibilidade e estado experimental variam com versão; não demonstra aceleração de decode nem aplicação local.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T184 — Mixture of Experts — MoE

**Nome canônico:** Mixture of Experts — MoE  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T184  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** MoE; mistura de especialistas

## T184:C01 — conceito

Arquitetura de rede com especialistas internos e um roteador que seleciona quais processarão cada entrada ou token. Em variantes esparsas, apenas parte dos especialistas é ativada por token. Isso difere de chamar agentes ou APIs externas e normalmente exige arquitetura e treinamento próprios.

Como funciona:
- Computar escores de roteamento para os especialistas.
- Encaminhar representações ao subconjunto selecionado.
- Combinar saídas e controlar distribuição de carga entre especialistas.

## T184:C02 — aplicacao

Quando usar:
- Modelo já foi projetado e treinado com especialistas.
- Infraestrutura consegue armazenar e executar seus pesos e comunicação.

Quando não usar:
- Tentar transformar modelo denso em MoE apenas por prompt ou adicionando um roteador de ferramentas.

Implementação proposta:
- Conferir parâmetros totais e ativos, além de arquitetura exata.
- Medir memória de todos os pesos e comunicação entre dispositivos.
- Avaliar desempenho com carga e comprimentos representativos.

Aplicação LAI proposta:
Proposta: ao comparar alternativas locais para Helena, avaliar capacidade total, parâmetros ativos e runtime, sem equiparar MoE a uma equipe de agentes.

## T184:C03 — riscos_validacao

Armadilhas:
- Poucos parâmetros ativos não significam que só esses pesos precisam de armazenamento.
- Roteamento desequilibrado ou comunicação pode reduzir eficiência.

Métricas sugeridas:
- Qualidade, throughput e latência por carga.
- Utilização dos especialistas e volume de comunicação.

Testes propostos:
- Comparar modelo sob lotes e distribuições diferentes de entradas.
- Testar limites de memória considerando todos os pesos e o KV cache.

## T184:C04 — perguntas_proveniencia

Pergunta: MoE é conjunto de especialistas LLM conversando?
Resposta: Não. No sentido técnico principal, são módulos internos da rede.

Pergunta: Posso ativar MoE em qualquer Qwen denso?
Resposta: Não por configuração simples; é uma característica arquitetural.

Pergunta: Especialista corresponde a um assunto nomeado?
Resposta: Não necessariamente. Especialização emerge do treino e precisa ser investigada; IDs de especialistas não garantem domínio semântico.

Pergunta: Pode carregar somente os ativos de cada token sem custo?
Resposta: Não. Trazer pesos sob demanda introduz transporte e sincronização que precisam entrar na avaliação de latência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T184:C05 — mecanismo_avancado

Parâmetros ativos por token e parâmetros totais medem custos distintos. Especialistas não selecionados podem continuar ocupando memória, enquanto dispatch e combinação geram comunicação. No Switch, a capacidade de cada especialista depende dos tokens do lote, número de especialistas e fator de capacidade; roteamento desigual pode excedê-la. A política para excedentes integra a função do modelo e precisa ser explicitada.

Condição de contorno:
Poucos especialistas ativos não garantem baixa latência quando carga desigual ou tráfego entre dispositivos domina a execução.

Contrato proposto:
- Entradas: Representações, escores do roteador, capacidade dos especialistas e regra de overflow.
- Saídas: Saídas combinadas e métricas de distribuição e tokens excedentes.
- Estado: Pesos totais, filas por especialista e mapas de dispatch.
- Invariante: Cada token segue a política declarada de seleção, combinação e tratamento de capacidade.

Compromissos de projeto:
- Capacidade maior reduz overflow e aumenta padding ou reservas.
- Balanceamento forte distribui carga e pode competir com a especialização aprendida.

## T184:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: construir entradas que concentram escolhas em um especialista e variar tamanho do lote. Esperar contagem explícita de overflow e resultado coerente com a política prevista.

Plano de avaliação proposto:
Plano proposto: comparar cargas uniformes e concentradas com mesmo modelo. Medir memória total, tokens ativos, distribuição, comunicação e qualidade; comparações com modelos densos devem declarar orçamento e treinamento, não apenas parâmetros ativos.

Comparações:
- T203 (distinct_from): Roteamento entre modelos externos decide qual sistema responderá; MoE roteia representações dentro de uma arquitetura treinada.

Afirmação rastreável:
No Switch Transformer, capacidade limitada pode provocar excedentes; aumentar o fator de capacidade reduz esse risco com custos adicionais.
Suporte: direct; fontes: V3B-S016
Limite: A política particular do Switch não é obrigatória em todos os modelos MoE.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T184:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu parâmetros totais, ativos e capacidade dos especialistas. O aprofundamento trata seleção de modelos MoE, distribuição entre dispositivos e diagnóstico de especialização sem inferências pelo nome do expert.

Dois orçamentos
Parâmetros ativos aproximam parte da computação por token; parâmetros totais continuam relevantes para armazenamento e residência. Qwen3-30B-A3B possui cerca de 30B totais e 3B ativos conforme sua nomenclatura publicada. Não deve ser dimensionado como um dense 3B nem confundido com um dense 32B fora da faixa estrita solicitada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S016, C-S038, V4B-S020, V4B-S003.

Comunicação de especialistas
Distribuir experts adiciona dispatch, combinação e possíveis desequilíbrios. Modelos pequenos em contexto de MoE ainda podem carregar muitos pesos. Meça tráfego por token, ocupação e grupos quentes; balanceamento observado em um perfil sintético não garante comportamento de tráfego real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S016, C-S038, V4B-S020, V4B-S003.

Especialização observada
Um expert frequentemente selecionado em código não é automaticamente um módulo confiável de programação. Analise padrões de roteamento e faça ablações controladas antes de atribuir significado. Mudança de domínio pode concentrar carga ou alterar qualidade, exigindo avaliação conjunta de sistema e modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S016, C-S038, V4B-S020, V4B-S003.

USO AVANÇADO — Escolher dense ou MoE
Cenário: Há candidatos com orçamento de computação parecido.
Estratégia: Compare qualidade, pesos residentes, custo de comunicação e latência em prompts reais. Não reduza a escolha a parâmetros ativos ou a um benchmark agregado.
Papel do modelo pequeno: Um modelo total 15–30B com poucos parâmetros ativos pode ser opção, sujeito à memória e ao domínio.
Aceite proposto: Selecionar pelo custo completo e pelas falhas relevantes à tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S016, C-S038, V4B-S020, V4B-S003.

USO AVANÇADO — Servir domínios heterogêneos
Cenário: A carga alterna código, texto e documentos técnicos.
Estratégia: Monitore distribuição de experts e filas, mantendo testes de deriva. Ajuste posicionamento ou capacidade somente quando houver evidência de gargalo e suporte do runtime.
Papel do modelo pequeno: Um MoE 8–30B total pode precisar de política distinta de um dense do mesmo porte.
Aceite proposto: Medir picos de comunicação e qualidade por domínio, sem mascarar classes raras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S016, C-S038, V4B-S020, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Se a faixa se refere a parâmetros totais, um MoE com 3B ativos e 30B totais pertence ao limite superior, não ao inferior.
8–14B: Modelos totais intermediários exigem inspeção de configuração e pesos realmente disponíveis.
15–30B: A faixa 15–30B inclui certos MoEs, mas não autoriza extrapolar suporte do runtime ou memória local.
Requisitos de treino/runtime: Arquitetura treinada com roteador e experts; não se cria MoE apenas agrupando checkpoints e escolhendo um por prompt.
Não aplicar quando: Não comparar parâmetros ativos com parâmetros totais como se fossem a mesma medida.

## T184:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: O deployment distribui especialistas e ajusta redundância com estatísticas online.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Expert parallelism é discutido para modelos MoE, sem demonstrar cada arquitetura do inventário.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Variantes MoE são explicitamente publicadas.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q016, V4B-Q003.

## T184:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T184 → T118 [complements]
Como combinar: Tensor parallelism e expert parallelism podem coexistir, com custos distintos.
Interface: Mapa de experts, shards e grupos.
Condição: Runtime suporta a combinação do checkpoint.
Aceite proposto: Medir comunicação e memória por dispositivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S016, C-S038, V4B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T184 → T177 [requires]
Como combinar: Adaptação de MoE precisa considerar roteador, experts e distribuição de dados.
Interface: Módulos treináveis e métricas de roteamento.
Condição: Política de overflow e capacidade explícita.
Aceite proposto: Avaliar qualidade e balanceamento depois do treino.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S016, C-S038, V4B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Informar parâmetros totais e ativos lado a lado.
- Não inferir desempenho local a partir do número no nome do modelo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
MoE pode oferecer outra relação entre computação e capacidade, mas a comparação com fronteira continua dependente de tarefa, memória, comunicação e qualidade observada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T146, T169

## Fontes primárias associadas

### C-S038 — Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer

[https://arxiv.org/abs/1701.06538](https://arxiv.org/abs/1701.06538)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteador treinado ativa um subconjunto de especialistas dentro da rede.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S016 — Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity — full text

[https://arxiv.org/html/2101.03961v3](https://arxiv.org/html/2101.03961v3)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento esparso, capacidade de especialistas e balanceamento de carga.

Limite: Uma variante de MoE; não universalizar política de overflow ou ganhos de treinamento.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

### V4D-S014 — Profiling Data in DeepSeek Infra

[https://github.com/deepseek-ai/profile-data/blob/main/README.md](https://github.com/deepseek-ai/profile-data/blob/main/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descrição de sobreposição computação/comunicação, RDMA e configurações ligadas ao deployment online V3/R1.

Limite: Os traces publicados simulam roteamento MoE perfeitamente balanceado; não são reprodução integral de tráfego real. EP32/EP128 deste perfil e EP32/EP320 do relatório são contextos/revisões diferentes.

### V4D-S015 — DeepSeek-V3 Technical Report — v2

[https://arxiv.org/html/2412.19437v2](https://arxiv.org/html/2412.19437v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seção 3.4 descreve deployment de inferência com prefill/decode separados, TP/EP e redundância de especialistas guiada por carga.

Limite: Modelo de 671B totais, fora de 3–30B. Custos publicados de treino não incluem toda a pesquisa. MTP especulativo avaliado não prova ativação em todo serviço online.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T185 — Constitutional AI

**Nome canônico:** Constitutional AI  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T185  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** IA constitucional

## T185:C01 — conceito

Método de treinamento que usa princípios explícitos para orientar crítica, revisão e feedback produzido por IA. A proposta original inclui etapas supervisionadas e por reforço. Adicionar regras ao prompt pode ser útil, mas não reproduz automaticamente o processo de treinamento denominado Constitutional AI.

Como funciona:
- Definir princípios que servirão como referência para feedback.
- Gerar críticas, revisões ou preferências baseadas nesses princípios.
- Usar os sinais no treinamento e avaliar comportamentos resultantes.

## T185:C02 — aplicacao

Quando usar:
- Há objetivo de alinhamento comportamental e infraestrutura de treinamento.
- Princípios podem ser avaliados em casos claros e conflitantes.

Quando não usar:
- Tratar uma lista de regras textual como substituta de controles obrigatórios de acesso e execução.

Implementação proposta:
- Versionar princípios e exemplos de conflitos.
- Auditar amostras do feedback de IA para evitar avaliação circular.
- Medir fidelidade às tarefas legítimas junto com cumprimento das regras.

Aplicação LAI proposta:
Proposta: usar princípios explícitos nas avaliações da Helena, mantendo autorização e contratos no runtime; isso por si só não significa que seu modelo foi treinado com Constitutional AI.

## T185:C03 — riscos_validacao

Armadilhas:
- Princípios vagos podem produzir avaliações inconsistentes.
- Juiz e modelo podem compartilhar vieses e reforçar erros.

Métricas sugeridas:
- Cumprimento de critérios por categoria de caso.
- Falsas restrições, violações e consistência em conflitos de princípios.

Testes propostos:
- Construir conjunto reservado com casos em que dois princípios competem.
- Comparar avaliação de IA com referência humana ou verificador independente quando possível.

## T185:C04 — perguntas_proveniencia

Pergunta: Constitutional AI é só system prompt?
Resposta: Não. O nome do trabalho se refere a um processo de treinamento com feedback orientado por princípios.

Pergunta: Princípios garantem comportamento perfeito?
Resposta: Não. Aderência precisa ser medida.

Pergunta: Sem rótulos humanos significa sem escolhas humanas?
Resposta: Não. A escolha dos princípios, dados, critérios e avaliação continua definindo o comportamento pretendido.

Pergunta: Como mudar uma regra depois do treino?
Resposta: Versione a política e avalie a intervenção escolhida; um novo prompt pode influenciar respostas, mas não apaga automaticamente o comportamento aprendido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T185:C05 — mecanismo_avancado

Princípios geram sinais de supervisão, mas a passagem de texto normativo para preferências envolve interpretação do avaliador. Regras conflitantes ou vagas podem criar rótulos inconsistentes; otimizar o reward model pode amplificar esses padrões. Portanto, é necessário separar adesão aos princípios, utilidade e correção factual. Uma resposta alinhada à preferência aprendida ainda pode conter informação falsa ou falhar em um contrato operacional.

Condição de contorno:
Alterar apenas a constituição em inferência não equivale a refazer o treinamento supervisionado e por reforço do método publicado.

Contrato proposto:
- Entradas: Princípios versionados, exemplos, críticas, revisões e preferências com proveniência.
- Saídas: Modelo treinado e avaliação por critérios independentes do gerador de preferências.
- Estado: Versões dos avaliadores, dataset de preferências e sinais de recompensa.
- Invariante: A mudança observada é atribuída à etapa efetivamente realizada, sem confundir prompting e treinamento.

Compromissos de projeto:
- Feedback automático amplia escala e herda vieses do avaliador.
- Princípios detalhados ajudam consistência e podem entrar em conflito em situações novas.

## T185:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar pares de princípios incompatíveis e exemplos factualmente errados que pareçam obedientes. Esperar detecção de conflito e reprovação factual independente da preferência automática.

Plano de avaliação proposto:
Plano proposto: comparar modelo inicial, etapa supervisionada e etapa com feedback de IA em conjuntos separados. Medir adesão, utilidade, factualidade e regressões; revisar casos discordantes com critérios explícitos antes de atribuir melhoria global.

Comparações:
- T192 (distinct_from): Autorrevisão em tempo de execução não reproduz, sozinha, as etapas de treinamento de Constitutional AI.

Afirmação rastreável:
O trabalho original inclui fine-tuning com revisões e reinforcement learning orientado por preferências geradas por IA.
Suporte: direct; fontes: C-S039
Limite: A fonte não demonstra que a constituição seja completa nem que preferências automáticas garantam verdade.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T185:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu interpretação e reward hacking. Esta camada propõe governança de princípios, testes de conflitos e separação entre norma treinada e regra operacional que precisa mudar imediatamente.

Princípios como especificação
Defina prioridade e exemplos de fronteira para regras que podem conflitar. Um princípio abstrato não determina sozinho a resposta correta em cada situação. Registre justificativa e versão dos rótulos produzidos por avaliadores, para detectar se uma mudança de interpretação alterou o dataset sem alteração explícita da política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

Treino versus controle externo
Comportamento aprendido pode persistir após uma regra mudar. Políticas que exigem atualização imediata devem ter uma camada externa verificável, além do treinamento. A constituição atual da Anthropic é descrita como parte do processo de treino; colocá-la num prompt de um modelo comum é uma intervenção diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

Avaliar utilidade e erro
Uma resposta pode seguir estilo e princípios enquanto fornece fatos errados ou recusa tarefas válidas. Meça adesão, utilidade, correção e recusas excessivas separadamente. Avaliadores baseados no mesmo texto de princípios podem compartilhar pontos cegos; inclua revisão humana e casos que tensionem prioridades.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

USO AVANÇADO — Assistente de domínio regulado internamente
Cenário: A empresa possui regras de atendimento claras.
Estratégia: Traduza regras em exemplos revisados, mantenha controles externos para requisitos objetivos e avalie conflitos. Não apresente o treinamento como garantia de conformidade universal.
Papel do modelo pequeno: Um 3–7B pode executar uma rotina de atendimento estreita com limites verificáveis.
Aceite proposto: Aceitação por regra e categoria, incluindo respostas úteis que não devem ser recusadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

USO AVANÇADO — Política que evolui
Cenário: Novas regras tornam parte do comportamento anterior inadequada.
Estratégia: Versione dados e avaliadores, aplique controle externo enquanto prepara atualização e teste regressões. Preserve casos que distingam versões para verificar se a mudança ocorreu.
Papel do modelo pequeno: Um 8–14B pode ser atualizado por adaptação, sujeito à validação de comportamento.
Aceite proposto: Confirmar mudança desejada sem ampliar erros factuais ou recusas fora do escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Princípios simples e exemplos consistentes são preferíveis a constituições extensas sem cobertura de teste.
8–14B: Capacidade de seguir nuances precisa ser medida; aumentar texto normativo não garante compreensão.
15–30B: Maior porte pode melhorar interpretação, mas não elimina conflitos nem necessidade de governança.
Requisitos de treino/runtime: Constitutional AI envolve processo de treinamento/feedback; prompting constitucional isolado não é reprodução integral do método.
Não aplicar quando: Não usar concordância de um juiz com a política como prova de verdade externa ou de cumprimento perfeito.

## T185:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C017 — Anthropic / Claude — treinamento com constituição
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: treinamento de LLM.
Uso observado: A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.
Mecanismo documentado: Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.
Correspondência com esta base: Princípios constitucionais são usados no treinamento por feedback de IA.
Transferência proposta para modelo pequeno: Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.
Limite: Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.
Fontes: V4B-S021.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q010.

## T185:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T185 → T193 [complements]
Como combinar: Guardrails externos implementam requisitos verificáveis e atualizáveis.
Interface: Política versionada e resultados de checagem.
Condição: Norma externa não contradiz silenciosamente o comportamento treinado.
Aceite proposto: Testar conflitos e registrar qual regra determinou o resultado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S039, V4B-S021, V3B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T185 → T198 [complements]
Como combinar: Confiança e abstenção devem ser avaliadas separadamente da adesão normativa.
Interface: Predições, rótulos e razões de recusa.
Condição: Conjunto cobre casos permitidos e proibidos.
Aceite proposto: Medir erro e recusa por categoria, sem recompensa por estilo apenas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S039, V4B-S021, V3B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir política do operador com consenso moral universal.
- Auditar exemplos sintéticos para evitar repetição sistemática de interpretações erradas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare adesão e utilidade no domínio definido. Uma constituição pode orientar comportamento, mas não transmite automaticamente conhecimento ou raciocínio de um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T193, T194

## Fontes primárias associadas

### C-S039 — Constitutional AI: Harmlessness from AI Feedback

[https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinamento usa princípios para crítica/revisão e feedback de IA em fases supervisionada e por reforço.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S021 — Claude's new constitution

[https://www.anthropic.com/news/claude-new-constitution](https://www.anthropic.com/news/claude-new-constitution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Constituição usada em treinamento e síntese de exemplos/rankings; método evoluiu desde Constitutional AI.

Limite: Texto de princípios e treinamento não garantem aderência de toda saída; parâmetros do modelo não são publicados nesta fonte.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T186 — Debate entre agentes

**Nome canônico:** Debate entre Agentes  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T186  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multiagent debate; Debate entre Agentes

## T186:C01 — conceito

Procedimento em que várias instâncias produzem propostas e depois confrontam argumentos, evidências ou críticas em rodadas. Pode revelar erros e alternativas, mas consenso não é prova. Agentes semelhantes podem compartilhar o mesmo erro e persuadir os demais sem informação nova.

Como funciona:
- Coletar propostas iniciais separadas para reduzir ancoragem.
- Trocar críticas específicas e pedir evidências para pontos contestados.
- Escolher resultado por critério explícito, preferindo verificação externa quando disponível.

## T186:C02 — aplicacao

Quando usar:
- Problema admite alternativas e comparação por critérios.
- Há valor em identificar objeções e hipóteses concorrentes.

Quando não usar:
- Questão já pode ser resolvida por cálculo ou teste determinístico mais barato.

Implementação proposta:
- Definir papéis, número de rodadas e orçamento total.
- Preservar propostas originais e mapear quais críticas alteraram conclusões.
- Usar árbitro com rubrica e acesso a fontes, sem votação automática por eloquência.

Aplicação LAI proposta:
Proposta: usar especialistas consultivos para contestar escolhas de arquitetura da Helena, mantendo um decisor e um critério de aceitação observável.

## T186:C03 — riscos_validacao

Armadilhas:
- Debate pode transformar diversidade inicial em erro consensual.
- Custo cresce com agentes, rodadas e contexto compartilhado.

Métricas sugeridas:
- Correções verificadas após debate versus regressões.
- Custo por decisão correta e diversidade inicial dos candidatos.

Testes propostos:
- Inserir argumento persuasivo porém falso e verificar resistência baseada em evidência.
- Comparar debate com o mesmo orçamento em candidatos independentes e teste externo.

## T186:C04 — perguntas_proveniencia

Pergunta: Três agentes concordando provam um fato?
Resposta: Não. Fontes e erros podem ser compartilhados.

Pergunta: Debate exige modelos diferentes?
Resposta: Não, mas diversidade de modelo ou evidência pode alterar correlação dos erros.

Pergunta: Agentes com nomes diferentes são diversos?
Resposta: Não necessariamente. Diversidade relevante envolve fontes, estratégias e padrões de erro, não apenas personas.

Pergunta: O árbitro deve escolher o argumento mais longo?
Resposta: Não. Deve aplicar critérios de evidência e correção; comprimento ou confiança verbal podem favorecer um erro persuasivo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T186:C05 — mecanismo_avancado

Uma rodada de debate pode acrescentar informação ou apenas redistribuir a mesma crença. Como proposta experimental, preserve respostas iniciais independentes antes de expor argumentos, registre quais alegações mudaram e exija evidência para a mudança. Agentes com pesos, fontes e prompts semelhantes tendem a compartilhar falhas; multiplicar instâncias não equivale a obter observações independentes. A ordem de exposição também pode induzir ancoragem.

Condição de contorno:
Consenso crescente pode esconder contágio de uma premissa falsa, especialmente quando um participante escreve de maneira mais persuasiva.

Contrato proposto:
- Entradas: Problema, propostas iniciais isoladas, regras de interação e evidências acessíveis.
- Saídas: Resposta selecionada com divergências e mudanças justificadas.
- Estado: Histórico por rodada, origem das alegações e orçamento de chamadas.
- Invariante: Nenhuma afirmação ganha validade apenas por ser repetida por vários participantes.

Compromissos de projeto:
- Rodadas adicionais ampliam oportunidade de crítica e custo de coordenação.
- Diversidade pode revelar erros e produzir conflitos que exigem adjudicação externa.

## T186:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma justificativa convincente com premissa falsa em um participante e variar sua posição na rodada. Esperar detecção por evidência independente e medir propagação do erro.

Plano de avaliação proposto:
Plano proposto: comparar resposta única, votação sem interação e debate com orçamento de tokens equivalente. Medir correção externa, erros compartilhados, mudanças corretas/incorretas e custo; aprovar debate quando seu ganho supera alternativas igualmente custosas.

Comparações:
- T187 (alternative): Votação agrega propostas; debate permite que participantes revisem suas próprias respostas após interação.

Afirmação rastreável:
O estudo de debate multiagente usa múltiplas instâncias que propõem e discutem respostas em rodadas.
Suporte: direct; fontes: C-S040
Limite: Melhorias experimentais não provam independência dos agentes nem tornam consenso um certificado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T186:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou respostas iniciais e destacou erros correlacionados. O aprofundamento diferencia debate, revisão paralela e arbitragem, e propõe medir se a interação acrescenta evidência ou só persuasão.

Papéis com informação distinta
Separar agentes por nomes não cria independência. Dê a cada papel um critério verificável ou fonte distinta, como contrato, execução e risco de regressão. Se todos recebem o mesmo texto e não acessam evidência adicional, a rodada pode apenas amplificar uma hipótese inicial convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

Mudança rastreável
Registre alegações, contraexemplos e motivo de cada revisão. Uma conclusão deve mudar por evidência identificada ou violação demonstrada, não porque um agente falou por último. Limite rodadas e permita manter desacordo; obrigar consenso pode apagar sinais úteis de incerteza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

Custo e juiz
Um árbitro pode herdar os mesmos vieses dos participantes. Learning Zone descreve papéis de revisão e comparação com humanos em avaliação; AutoClean usa revisores por propriedade. Esses casos apoiam desenhos delimitados, sem provar que debate livre melhora qualquer tarefa ou que todos os modelos pequenos julgam corretamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

USO AVANÇADO — Revisão de objeto de negócio
Cenário: Uma saída precisa atender conteúdo, formato e consistência.
Estratégia: Faça avaliações separadas por critério e peça discussão somente sobre conflitos concretos. Use validadores determinísticos quando o critério puder ser formalizado.
Papel do modelo pequeno: Modelos 3–7B podem revisar aspectos estreitos, preservando um árbitro externo para casos difíceis.
Aceite proposto: Medir defeitos adicionais detectados por rodada e custo de falsos alarmes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

USO AVANÇADO — Planejamento com hipóteses concorrentes
Cenário: Há duas estratégias plausíveis para resolver uma tarefa.
Estratégia: Peça planos independentes, busque evidências que os discriminem e use debate para atualizar pressupostos. Pare quando o orçamento acabar ou a evidência for suficiente.
Papel do modelo pequeno: Um 8–14B pode explorar alternativas com ferramentas, sem ser tratado como especialista universal.
Aceite proposto: Comparar decisão final com baseline de uma chamada sob orçamento equivalente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S040, V4D-S012, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Papéis estreitos e verificadores externos reduzem exigência cognitiva de cada participante.
8–14B: Diversidade de fontes e critérios importa mais que multiplicar instâncias idênticas.
15–30B: Um 15–30B pode arbitrar casos mais complexos, mas deve ser avaliado contra julgamentos independentes.
Requisitos de treino/runtime: Orquestração em runtime; não implica treinamento. Resultados dependem de prompts, fontes, juiz e tarefa.
Não aplicar quando: Não interpretar unanimidade como probabilidade calibrada nem confundir revisão paralela sem interação com debate.

## T186:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Reviewer/Critic/Meta-Reviewer apoiam avaliação offline.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T186:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T186 → T200 [complements]
Como combinar: Uma verificação externa pode resolver desacordos sem depender da retórica.
Interface: Alegação contestada e evidência reproduzível.
Condição: Verificador possui critério independente.
Aceite proposto: Injetar argumento persuasivo falso e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S040, V4D-S012, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T186 → T193 [complements]
Como combinar: Critérios verificáveis podem funcionar como barreiras antes da discussão.
Interface: Resultados por regra e motivos de falha.
Condição: Guardrail cobre apenas o que realmente consegue verificar.
Aceite proposto: Evitar gastar debate em erros estruturais já decidíveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S040, V4D-S012, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar respostas iniciais para medir influência e ancoragem.
- Não ajustar o juiz até concordar com a conclusão desejada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare debate com uma chamada e com amostragem adicional sob o mesmo orçamento. Mais agentes podem ajudar numa tarefa, mas não equivalem a mais inteligência independente por definição.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T187, T188, T200

## Fontes primárias associadas

### C-S040 — Improving Factuality and Reasoning in Language Models through Multiagent Debate

[https://arxiv.org/abs/2305.14325](https://arxiv.org/abs/2305.14325)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instâncias debatem propostas em rodadas; concordância não é garantia universal de correção.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T187 — Ensemble Voting

**Nome canônico:** Ensemble Voting  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T187  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** votação de ensemble

## T187:C01 — conceito

Agregação das previsões de vários modelos ou executores por votação. Hard voting combina rótulos; soft voting combina probabilidades, que precisam ser comparáveis e preferencialmente calibradas. Para respostas livres, antes de votar é necessário definir equivalência semântica e tratamento de abstenções.

Como funciona:
- Obter previsões independentes ou tão diversas quanto o desenho permitir.
- Normalizar rótulos ou respostas equivalentes.
- Aplicar regra de voto, pesos e desempate definidos previamente.

## T187:C02 — aplicacao

Quando usar:
- Classificação com espaço de respostas claro.
- Modelos apresentam erros parcialmente complementares.

Quando não usar:
- Respostas dependem da mesma fonte incorreta ou probabilidades têm escalas incompatíveis.

Implementação proposta:
- Medir correlação de erros entre componentes.
- Ajustar pesos apenas em validação e reservar teste final.
- Permitir abstenção quando não houver margem suficiente.
- Incluir custo de todos os componentes na comparação com o baseline.

Aplicação LAI proposta:
Proposta: testar votação para classificações específicas da Helena com referência observável, sem usar contagem de opiniões como substituto de evidência.

## T187:C03 — riscos_validacao

Armadilhas:
- Muitos modelos redundantes só repetem o mesmo viés.
- Maioria pode ser errada mesmo com alta concordância.

Métricas sugeridas:
- Acerto do ensemble comparado ao melhor componente.
- Calibração, discordância e custo por previsão aceita.

Testes propostos:
- Criar casos em que dois componentes compartilham erro e um está correto.
- Testar empates e probabilidades não calibradas antes de usar soft voting.

## T187:C04 — perguntas_proveniencia

Pergunta: Soft voting é sempre superior?
Resposta: Não. Probabilidades mal calibradas podem dar peso excessivo a um modelo confiante e errado.

Pergunta: Votar exige vários modelos?
Resposta: Pode agregar execuções, mas a independência e diversidade precisam ser avaliadas.

Pergunta: Maioria de três cópias iguais aumenta evidência?
Resposta: Não. Repetir o mesmo erro não acrescenta informação independente.

Pergunta: Como lidar com abstenção?
Resposta: Defina se ela reduz o peso disponível ou provoca escalonamento; não converta ausência de evidência em voto por uma classe arbitrária.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T187:C05 — mecanismo_avancado

Antes de somar probabilidades, todos os participantes precisam usar o mesmo espaço de classes e a mesma ordem. Uma permutação silenciosa de rótulos pode produzir um ensemble numericamente válido e semanticamente errado. Pesos de votação devem ser ajustados em dados separados da avaliação final. Para respostas livres, a normalização que agrupa equivalentes também vira parte do sistema e pode errar.

Condição de contorno:
Erros correlacionados limitam o benefício de adicionar modelos; soft voting não corrige automaticamente probabilidades mal calibradas.

Contrato proposto:
- Entradas: Predições, rótulos canônicos, probabilidades disponíveis e política de pesos/empates.
- Saídas: Decisão agregada com votos, abstenções e proveniência.
- Estado: Mapas de classes, pesos escolhidos e versão do normalizador.
- Invariante: Cada coluna de probabilidade representa a mesma classe em todos os participantes.

Compromissos de projeto:
- Hard voting perde intensidade de preferência e exige menos informação.
- Soft voting usa mais sinal e exige comparabilidade probabilística e alinhamento rigoroso.

## T187:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inverter a ordem de classes de um modelo sem alterar seus números e inserir empate. Esperar detecção do desalinhamento e aplicação explícita da regra de desempate.

Plano de avaliação proposto:
Plano proposto: comparar membros individuais e ensemble em dados independentes. Medir correção, calibração, correlação de erros e custo; avaliar pesos sem reutilizar o conjunto final e aceitar agregação somente quando melhora o objetivo definido.

Comparações:
- T188 (alternative): Self-consistency agrega amostras de soluções, frequentemente do mesmo modelo, em vez de pressupor classificadores distintos.

Afirmação rastreável:
A documentação scikit-learn define soft voting pela agregação ponderada de probabilidades e escolha da classe com maior média.
Suporte: direct; fontes: C-S041
Limite: O procedimento matemático não garante calibração nem trata automaticamente equivalência de respostas abertas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T187:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou espaço de classes e normalização. A nova camada quantifica o valor da diversidade, considera abstenções e separa votação de sistemas que apenas usam vários modelos em etapas distintas.

Erros conjuntos
Avalie a matriz de erros compartilhados, não somente a precisão isolada de cada participante. Um terceiro modelo que repete os erros dos dois primeiros pode adicionar pouco valor. Diversidade útil precisa ser medida no domínio; marcas, prompts ou seeds diferentes não demonstram independência estatística.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

Abstenção e empate
Defina como votos ausentes, respostas inválidas e empates afetam a decisão. Forçar todos a escolher pode produzir maioria artificial em casos sem informação suficiente. Uma política proposta só publica quando há suporte válido e um verificador de requisitos passa; caso contrário, busca evidência ou encaminha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

Vários modelos não implica votação
AlphaEvolve usa modelos com papéis na busca de programas, mas isso não comprova decisão por maioria. Registre o mecanismo exato de agregação: votação de classe, média de probabilidades, ranking por juiz ou evolução. Essas formas têm custos e garantias diferentes e não devem compartilhar um rótulo genérico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

USO AVANÇADO — Classificação com rótulos fechados
Cenário: Erros de uma classe específica têm custo elevado.
Estratégia: Escolha participantes com falhas complementares, ajuste pesos em desenvolvimento e teste abstenção. Use probabilidades somente quando significado e calibração forem comparáveis.
Papel do modelo pequeno: Modelos 3–7B especializados podem compor uma decisão estreita, se a diversidade compensar o custo.
Aceite proposto: Medir erro por classe, cobertura e custo adicional frente ao melhor participante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

USO AVANÇADO — Extração de campos
Cenário: Há discordância sobre valores recuperáveis em documentos.
Estratégia: Peça extrações independentes e confronte divergências com a evidência original. Não vote sobre strings sem normalização de unidade e identidade.
Papel do modelo pequeno: Um 8–14B pode ser um dos extratores; o documento é a referência decisiva.
Aceite proposto: Avaliar campos corretos e erros compartilhados, incluindo ausência de informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S041, V4B-S022, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Vários modelos baratos podem custar mais que uma chamada melhor; comparar orçamento total.
8–14B: Especialização complementar é hipótese mais concreta que duplicar o mesmo prompt.
15–30B: Um 15–30B pode funcionar como participante ou árbitro, mas arbitrar não é votar.
Requisitos de treino/runtime: Orquestração de inferência; pesos de votação exigem dados separados. Não implica atualização dos modelos.
Não aplicar quando: Não converter proporção de votos em probabilidade de verdade sem calibração na distribuição relevante.

## T187:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de sistemas com múltiplos modelos consultada. Casos como AlphaEvolve não são classificados automaticamente como ensemble voting; não foi confirmado caso exato adicional de votação em produção neste recorte.
Consultas registradas: V4B-Q011.

## T187:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T187 → T198 [requires]
Como combinar: Probabilidades e limiares de abstenção precisam de avaliação de confiabilidade.
Interface: Votos, scores e resultados rotulados.
Condição: Conjunto final independente dos pesos escolhidos.
Aceite proposto: Medir calibração e cobertura por domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S041, V4B-S022, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T187 → T200 [complements]
Como combinar: Evidência independente pode resolver discordâncias que a maioria não decide corretamente.
Interface: Campos contestados e fontes originais.
Condição: Verificador não recebe a maioria como resposta esperada.
Aceite proposto: Incluir casos em que todos os participantes erram igual.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S041, V4B-S022, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar votos individuais para detectar correlação e mudança de comportamento.
- Não agrupar respostas semanticamente distintas apenas para aumentar consenso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o ensemble com uma chamada de fronteira sob custo e prazo equivalentes. Um ganho em classificação fechada não prova capacidade geral nem justifica votar sobre fatos sem evidência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T186, T188, T198, T205

## Fontes primárias associadas

### C-S041 — Voting Classifier — scikit-learn

[https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hard voting usa votos de classe e soft voting agrega probabilidades.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T188 — Self-Consistency

**Nome canônico:** Self-Consistency  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T188  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** autoconsistência

## T188:C01 — conceito

Estratégia que amostra diferentes soluções para a mesma tarefa e agrega a resposta final mais consistente entre elas. O trabalho original considera caminhos de resolução diversos. Consistência amostral pode melhorar seleção, mas não transforma concordância em certeza nem substitui evidência externa.

Como funciona:
- Gerar múltiplos candidatos com diversidade de amostragem apropriada.
- Extrair e normalizar respostas finais comparáveis.
- Agregar respostas equivalentes e sinalizar falta de consenso suficiente.

## T188:C02 — aplicacao

Quando usar:
- Problema tem resposta final comparável, como cálculo ou classificação.
- Uma única amostra é instável e existe orçamento para várias tentativas.

Quando não usar:
- Resposta aberta sem critério confiável de equivalência ou todos os candidatos compartilham a mesma premissa falsa.

Implementação proposta:
- Definir número máximo de amostras e método de normalização.
- Avaliar efeito da temperatura sem alterar outras variáveis simultaneamente.
- Comparar com seleção por verificador sob o mesmo orçamento.

Aplicação LAI proposta:
Proposta: usar self-consistency em subtarefas bem delimitadas da Helena, preservando o verificador externo como referência quando existir.

## T188:C03 — riscos_validacao

Armadilhas:
- Normalização inadequada separa respostas equivalentes ou une respostas diferentes.
- Várias amostras podem reforçar erro comum.

Métricas sugeridas:
- Acerto versus número de amostras e custo.
- Margem do voto e erro condicional à concordância.

Testes propostos:
- Testar variações equivalentes de unidades e formato da mesma resposta.
- Incluir perguntas com premissa falsa e verificar se o sistema abstém ou contesta.

## T188:C04 — perguntas_proveniencia

Pergunta: É o mesmo que pedir para o modelo revisar uma vez?
Resposta: Não. Há amostragem de caminhos e agregação de respostas.

Pergunta: Exige guardar pensamentos internos completos?
Resposta: Não. A aplicação pode operar com soluções e resultados observáveis.

Pergunta: Usar a mesma seed em todas as chamadas ajuda?
Resposta: Pode eliminar diversidade útil; registre como a amostragem realmente varia e verifique duplicatas.

Pergunta: Pode parar quando uma resposta lidera?
Resposta: É uma política possível, mas precisa considerar incerteza da contagem e risco de viés introduzido pela parada adaptativa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T188:C05 — mecanismo_avancado

Agregar respostas exige uma função de equivalência anterior à contagem: 0,5 e 1/2 podem representar o mesmo número, mas 1 metro e 1 centímetro não. A diversidade dos caminhos amostrados também depende de temperatura, seeds e formulação da tarefa. Se todos convergem ao mesmo erro por conhecimento compartilhado, aumentar amostras estabiliza uma maioria incorreta em vez de corrigi-la.

Condição de contorno:
Frequência de uma resposta entre amostras não é automaticamente probabilidade calibrada de que ela esteja correta.

Contrato proposto:
- Entradas: Problema, política de amostragem, orçamento e normalizador de respostas.
- Saídas: Resposta agregada com contagens, candidatos rejeitados e possíveis ambiguidades.
- Estado: Amostras independentes de execução, unidades, equivalências e critérios de validade.
- Invariante: Somente respostas semanticamente equivalentes e válidas participam da mesma classe de votos.

Compromissos de projeto:
- Mais amostras reduzem ruído de contagem e aumentam custo.
- Normalização agressiva pode fundir respostas distintas; normalização literal pode separar equivalentes.

## T188:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar respostas numericamente equivalentes com formatos distintos e respostas iguais com unidades diferentes. Esperar agrupamento correto e preservação das diferenças de unidade.

Plano de avaliação proposto:
Plano proposto: comparar uma amostra, maioria literal e maioria normalizada em tarefas com referência externa. Controlar orçamento e amostragem; medir correção, diversidade efetiva, erros do normalizador e custo, sem aprovar apenas pelo aumento de concordância.

Comparações:
- T189 (alternative): Best-of-N usa uma nota de qualidade; self-consistency seleciona pela massa de respostas equivalentes.

Afirmação rastreável:
O trabalho original amostra caminhos diversos e agrega as respostas resultantes para selecionar a mais consistente.
Suporte: direct; fontes: C-S042
Limite: A intuição sobre múltiplos caminhos não garante que a resposta dominante seja verdadeira em toda distribuição.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T188:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu equivalência e erros de maioria. Esta camada analisa orçamento adaptativo de amostragem, dependência entre respostas e critérios de parada que não fabricam certeza.

Amostras informativas
Temperatura mais alta pode aumentar diversidade e também produzir saídas inválidas. Meça quantas amostras trazem soluções distintas e corretas, não apenas variação de redação. Se o modelo repete o mesmo erro estrutural, aumentar N pode estabilizar uma resposta errada com aparente confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

Parada adaptativa
Interromper cedo quando uma resposta lidera reduz custo, mas muda a distribuição de casos que recebem mais computação. Avalie a política inteira num conjunto separado, incluindo casos em que a liderança inicial estava errada. Uma margem de votos escolhida a olho não é uma garantia estatística universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

Resposta e raciocínio
O agrupamento deve priorizar o resultado verificável, preservando detalhes relevantes como unidade e condições. Não é necessário tratar explicações longas como prova de raciocínio correto. Quando existe um executor ou cálculo independente, use-o para distinguir candidatos que parecem diferentes mas representam o mesmo resultado válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

USO AVANÇADO — Problemas com resposta verificável
Cenário: Uma tarefa admite número, classe ou solução curta.
Estratégia: Amostre com orçamento limitado, normalize respostas e valide restrições. Compare maioria com seleção por verificador para saber qual mecanismo realmente agrega valor.
Papel do modelo pequeno: Um 3–7B pode melhorar em problemas que já resolve em parte das tentativas.
Aceite proposto: Medir probabilidade de incluir e selecionar a resposta correta separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

USO AVANÇADO — Decisão com custo variável
Cenário: Casos fáceis são frequentes e difíceis são raros.
Estratégia: Use uma primeira amostra e sinais calibrados para decidir se ampliar o conjunto. Se faltar evidência, busque-a em vez de repetir geração.
Papel do modelo pequeno: Um 8–14B pode gastar computação adicional apenas em situações justificadas.
Aceite proposto: Comparar política adaptativa com N fixo sob o mesmo orçamento médio e prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S042, V3B-S020, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Amostragem ajuda apenas se existe massa de probabilidade em soluções corretas.
8–14B: Teste tarefas distintas; uma política útil em matemática pode não ajudar extração factual.
15–30B: Um 15–30B pode precisar de menos amostras, mas isso deve ser medido por tarefa.
Requisitos de treino/runtime: Runtime de amostragem e agregação; não é treinamento. Normalização e política de parada fazem parte do sistema.
Não aplicar quando: Não apresentar consistência como calibração nem supor independência porque as seeds diferem.

## T188:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T188:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T188 → T189 [alternative]
Como combinar: Um verificador pode selecionar candidatos quando frequência não corresponde a correção.
Interface: Conjunto de respostas e evidências.
Condição: Critério externo suficientemente informativo.
Aceite proposto: Comparar escolha por maioria e por verificação no mesmo conjunto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S042, V3B-S020, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T188 → T202 [complements]
Como combinar: Discordância pode acionar aquisição de informação, não apenas mais amostras.
Interface: Tipos de divergência e lacunas identificadas.
Condição: A ação adicional reduz uma incerteza relevante.
Aceite proposto: Medir se a observação muda a decisão corretamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S042, V3B-S020, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Guardar respostas inválidas no denominador do custo, sem contá-las como votos úteis.
- Separar amostras de desenvolvimento das usadas para avaliar a regra de parada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sucesso e custo frente a fronteira sob orçamento total explícito. Self-consistency pode melhorar tarefas específicas, mas não cria conhecimento que todas as amostras desconhecem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T156, T187, T189, T205

## Fontes primárias associadas

### C-S042 — Self-Consistency Improves Chain of Thought Reasoning in Language Models

[https://arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Amostra caminhos diversos e agrega respostas finais equivalentes.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T189 — Best-of-N Verification

**Nome canônico:** Best-of-N Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T189  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** seleção do melhor de N

## T189:C01 — conceito

Geração de N candidatos seguida da seleção daquele com maior nota de um verificador. O critério é qualidade avaliada, não popularidade entre candidatos. A confiabilidade depende do avaliador e de sua resistência a soluções que parecem boas, mas exploram falhas da métrica.

Como funciona:
- Gerar candidatos com diversidade suficiente.
- Avaliar cada um com testes, rubrica ou modelo verificador.
- Selecionar o melhor candidato admissível ou abster se nenhum atende ao mínimo.

## T189:C02 — aplicacao

Quando usar:
- Resultado possui teste objetivo ou avaliador confiável.
- Gerar alternativas é barato em relação ao valor de acertar.

Quando não usar:
- O avaliador apenas prefere estilo convincente ou foi ajustado nos mesmos candidatos de teste.

Implementação proposta:
- Separar geração e critério de avaliação.
- Contabilizar custo de N gerações e N verificações.
- Conservar candidatos rejeitados para analisar por que a seleção errou.

Aplicação LAI proposta:
Proposta: selecionar patches ou consultas produzidos pela Helena por execução e contratos, com orçamento limitado de alternativas.

## T189:C03 — riscos_validacao

Armadilhas:
- Quanto maior N, maior chance de explorar defeitos de um juiz imperfeito.
- Selecionar sempre um candidato força resposta mesmo quando todos estão errados.

Métricas sugeridas:
- Taxa de candidato correto presente versus taxa de seleção correta.
- Ganho de qualidade por custo adicional de N.

Testes propostos:
- Construir conjunto com candidato correto de estilo simples e incorreto muito eloquente.
- Variar N e medir se o verificador melhora seleção ou só aumenta confiança aparente.

## T189:C04 — perguntas_proveniencia

Pergunta: Best-of-N é votação?
Resposta: Não. Um avaliador escolhe; o candidato mais frequente não precisa vencer.

Pergunta: N maior sempre melhora?
Resposta: Não. Custo cresce e o verificador pode selecionar erros cada vez mais persuasivos.

Pergunta: Se há solução correta entre cem, o sistema acertou?
Resposta: Somente se a identificar e entregar; cobertura do conjunto não é precisão da seleção.

Pergunta: Pode avaliar usando o mesmo verificador?
Resposta: Isso mede alinhamento ao seletor; qualidade final precisa de evidência ou referência independente para detectar exploração do score.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T189:C05 — mecanismo_avancado

Gerar mais candidatos melhora a chance de incluir uma solução correta somente sob hipóteses sobre a distribuição. Mesmo que exista um candidato correto, o seletor pode preferir outro. Maximizar um score imperfeito também seleciona extremos de seu erro: respostas que exploram o avaliador podem vencer com notas altas. Por isso, qualidade do conjunto de candidatos e qualidade da seleção devem ser medidas separadamente.

Condição de contorno:
O melhor score observado não é uma estimativa imparcial de qualidade, principalmente quando N aumenta e o avaliador tem ruído.

Contrato proposto:
- Entradas: N candidatos, verificador versionado, regra de seleção e orçamento total.
- Saídas: Candidato selecionado com notas, empates e evidências disponíveis.
- Estado: Todos os candidatos, configuração de geração e resultados independentes de avaliação.
- Invariante: A nota usada para escolher não substitui a referência independente usada para medir acerto.

Compromissos de projeto:
- Mais candidatos ampliam cobertura e custo de geração/verificação.
- Seleção mais forte pode elevar qualidade e favorecer exploração de falhas da métrica.

## T189:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir candidato incorreto que satisfaz sinais superficiais do avaliador e candidato correto menos persuasivo. Esperar que a avaliação externa revele a seleção errada.

Plano de avaliação proposto:
Plano proposto: variar N com orçamento e comparadores declarados. Medir presença de solução correta, acerto da escolha, score proxy e resultado externo; aprovar escalabilidade somente quando a qualidade real acompanha o custo adicional.

Comparações:
- T188 (alternative): A seleção por nota não depende de uma resposta formar maioria entre amostras.

Afirmação rastreável:
O estudo de overoptimization examina deterioração do objetivo de referência ao otimizar excessivamente um reward proxy, incluindo best-of-N.
Suporte: direct; fontes: V3B-S018
Limite: O experimento usa um ambiente sintético de reward models; não fornece um limiar universal seguro para N.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T189:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou cobertura dos candidatos e seleção. Esta camada trata diversidade dirigida, custo do verificador e avaliação de exploração da métrica conforme o número de candidatos cresce.

Cobertura controlada
Gere alternativas que diferem em decisões relevantes, não apenas estilo. Para código, varie algoritmo ou decomposição; para extração, varie hipótese de evidência. Registre se o conjunto contém uma solução correta com um oráculo independente, permitindo localizar falha de geração versus falha de seleção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

Seleção sob pressão
Quanto mais candidatos, maior a chance de encontrar uma resposta que explora defeitos do score. Compare qualidade independente ao aumentar N. Se a nota sobe enquanto o acerto cai, o seletor está escolhendo extremos de seu erro; reduzir orçamento ou melhorar o critério pode ser melhor que gerar mais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

Verificador caro
Nem todos os candidatos precisam receber a checagem mais cara. Use filtros baratos que não eliminem soluções válidas sistematicamente, depois verificação aprofundada nos sobreviventes. Registre custo e falsos negativos de cada estágio. Um pipeline de filtros deve ser avaliado como composição, não por precisão isolada do último juiz.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

USO AVANÇADO — Geração de funções pequenas
Cenário: Há testes e restrições de interface.
Estratégia: Gere candidatos com abordagens distintas, compile, execute testes e examine propriedades não cobertas. Escolha pelo critério de tarefa, mantendo empates e falhas de infraestrutura explícitos.
Papel do modelo pequeno: Um 3–7B pode produzir candidatos úteis quando a solução correta aparece com frequência suficiente.
Aceite proposto: Medir cobertura do conjunto, acerto da seleção e custo total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

USO AVANÇADO — Resposta com evidências alternativas
Cenário: Uma consulta admite várias sínteses.
Estratégia: Gere versões com cobertura diferente, verifique alegações contra fontes e selecione a que cumpre requisitos. Não premiar comprimento ou tom de certeza.
Papel do modelo pequeno: Um 8–14B pode propor sínteses enquanto um verificador checa citações e cobertura.
Aceite proposto: Avaliar fidelidade e utilidade, inclusive quando nenhum candidato é aceitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S018, C-S043, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Pode compensar instabilidade em tarefas estreitas, mas N alto não resolve ausência de capacidade.
8–14B: O verificador deve ser mais confiável que o critério implícito usado pelo gerador.
15–30B: Compare N candidatos de 15–30B com uma chamada mais forte, incluindo custo de julgar e esperar.
Requisitos de treino/runtime: Orquestração de inferência; treinamento do verificador é etapa opcional separada.
Não aplicar quando: Não chamar busca evolutiva inteira de best-of-N independente nem assumir que maior score significa maior verdade.

## T189:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T189:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T189 → T195 [complements]
Como combinar: Execução fornece sinais objetivos para selecionar código ou planos executáveis.
Interface: Artefato, entradas e resultados esperados.
Condição: Ambiente e oráculo são confiáveis dentro do escopo.
Aceite proposto: Separar erro de infraestrutura de reprovação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S018, C-S043, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T189 → T201 [feeds]
Como combinar: Best-of-N é uma forma de investir orçamento em largura.
Interface: Custo por candidato e qualidade marginal.
Condição: Política de parada observa retorno útil.
Aceite proposto: Comparar largura com refinamento sequencial no mesmo orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S018, C-S043, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Permitir rejeitar todos os candidatos.
- Avaliar robustez do juiz a respostas que imitam a rubrica sem satisfazer a tarefa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O alvo é obter mais respostas corretas por orçamento em tarefas verificáveis. Um grande conjunto e um juiz fraco podem piorar resultados; não há equivalência geral com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T188, T190, T195

## Fontes primárias associadas

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T190 — Verifier Loop

**Nome canônico:** Verifier Loop  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T190  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ciclo de verificação

## T190:C01 — conceito

Ciclo de produzir, verificar e corrigir até satisfazer um critério ou atingir limite. O verificador pode ser teste executável, validação de dados, checagem de fonte ou modelo com rubrica. É essencial separar evidência de correção de uma simples declaração do gerador de que revisou a resposta.

Como funciona:
- Produzir candidato e associar requisitos verificáveis.
- Executar verificador e registrar falhas específicas.
- Corrigir apenas problemas identificados e repetir dentro de um orçamento.

## T190:C02 — aplicacao

Quando usar:
- Geração de código, objetos estruturados ou respostas com fontes.
- Erros podem ser localizados e corrigidos de forma objetiva.

Quando não usar:
- Verificador não observa o resultado real ou aprova qualquer justificativa textual.

Implementação proposta:
- Definir estados aprovado, rejeitado e inconclusivo.
- Detectar oscilação e repetição de tentativas equivalentes.
- Preservar melhor candidato e não perder teste anteriormente aprovado.

Aplicação LAI proposta:
Proposta: a Helena validar artefatos e recibos antes de declarar conclusão, guardando resultados de cada correção para auditoria.

## T190:C03 — riscos_validacao

Armadilhas:
- Gerador pode adaptar-se ao teste sem resolver o requisito real.
- Loop sem condição de parada consome recursos indefinidamente.

Métricas sugeridas:
- Correções aceitas por tentativa e regressões.
- Falsos positivos do verificador e custo por resultado aprovado.

Testes propostos:
- Introduzir falha conhecida e verificar que o ciclo a detecta e corrige.
- Usar tarefa impossível com recursos disponíveis e exigir término inconclusivo explícito.

## T190:C04 — perguntas_proveniencia

Pergunta: O mesmo modelo pode verificar?
Resposta: Pode, mas isso reduz independência e exige medir falsos positivos.

Pergunta: Passar no verificador prova tudo?
Resposta: Prova apenas os critérios cobertos e a confiabilidade daquele verificador.

Pergunta: Passou uma vez, está resolvido para sempre?
Resposta: Não. Mudança de conteúdo, dependências ou ambiente pode invalidar o resultado anterior.

Pergunta: O próprio gerador pode verificar?
Resposta: Pode contribuir com crítica, mas seus erros podem ser correlacionados; critérios objetivos e fontes independentes fortalecem a evidência.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T190:C05 — mecanismo_avancado

Cada veredito deve vincular-se à revisão exata do artefato inspecionado. Uma correção posterior pode invalidar testes anteriores, inclusive quando tenta resolver outro problema. Como proposta de controle, mantenha hash ou revisão, lista de falhas e critérios de progresso; repetições sem melhoria e ciclos entre duas versões precisam encerrar com diagnóstico. Um timeout do verificador é desconhecimento, não aprovação.

Condição de contorno:
O ciclo pode nunca convergir quando requisitos são inconsistentes, o gerador não tem capacidade ou o verificador produz falsos negativos.

Contrato proposto:
- Entradas: Artefato versionado, critérios executáveis ou rubrica, orçamento e evidências anteriores.
- Saídas: Versão aprovada para critérios definidos ou relatório explícito de pendências.
- Estado: Histórico de revisões, vereditos, falhas e consumo de tentativas.
- Invariante: Aprovação sempre referencia o mesmo conteúdo que será entregue ou executado.

Compromissos de projeto:
- Mais iterações oferecem correções e ampliam custo e risco de regressão.
- Verificador estrito pode rejeitar alternativas válidas quando o contrato é incompleto.

## T190:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aprovar uma versão, modificá-la e reutilizar deliberadamente o veredito antigo. Esperar invalidação; injetar também alternância entre duas correções para testar parada por ciclo.

Plano de avaliação proposto:
Plano proposto: comparar geração única e loop limitado em casos com defeitos conhecidos. Medir taxa de correção, regressões, falsos aceites, custo e não convergência; aprovar apenas se o ganho externo justificar o esforço adicional.

Comparações:
- T195 (complements): Execução pode fornecer evidência objetiva para alguns critérios do loop, sem cobrir toda a especificação.

Afirmação rastreável:
Verificadores treinados podem classificar soluções e orientar seleção de candidatos, como no estudo de problemas matemáticos.
Suporte: related; fontes: C-S043
Limite: O protocolo de revisão, progresso e parada desta ficha é proposta de engenharia; o paper não o padroniza.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T190:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculou vereditos a revisões. O aprofundamento acrescenta classificação das falhas, reparos mínimos e condições de parada que preservam progresso sem transformar o loop em geração ilimitada.

Falha acionável
O verificador deve devolver critério, evidência e localização do defeito. Separe erro do artefato, requisito ambíguo e falha do executor. Cada classe pede ação distinta: corrigir, esclarecer ou repetir infraestrutura. Passar a mesma mensagem genérica ao gerador tende a criar mudanças grandes e pouco controladas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

Reparo com escopo
Uma correção deve declarar quais partes pode alterar e quais propriedades precisam ser preservadas. Reexecute testes afetados e barreiras obrigatórias na revisão final. O AutoClean descreve fixers e verificações por propriedade; a proposta transferível é reduzir superfície de mudança e manter evidência ligada ao conteúdo entregue.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

Progresso e encerramento
Use uma medida explícita de falhas remanescentes e detecte ciclos de revisões. Se a correção de uma propriedade quebra outra repetidamente, a hipótese ou o escopo pode estar errado. Encerre com pendências verificáveis quando o orçamento acabar, sem converter exaustão em aprovação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

USO AVANÇADO — Correção de código localizada
Cenário: Um teste falha num conjunto pequeno de arquivos.
Estratégia: Forneça ao modelo o erro mínimo e o contrato, gere patch restrito e valide. Amplie o contexto somente quando a falha indicar dependência externa ao escopo.
Papel do modelo pequeno: Um 3–7B pode reparar padrões simples; um 8–14B pode tratar relações maiores, conforme teste.
Aceite proposto: Entregar revisão que passa critérios e preserva invariantes, com custo e tentativas registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

USO AVANÇADO — Objeto estruturado com regras
Cenário: A saída viola formato ou uma regra de negócio.
Estratégia: Corrija apenas campos apontados e revalide o objeto completo. Se a regra depende de fato ausente, busque evidência em vez de inventar um valor para satisfazer o schema.
Papel do modelo pequeno: Um pequeno modelo funciona como proponente, não como autoridade de aceitação.
Aceite proposto: Nenhuma alteração silenciosa em campos já verificados; resultado final consistente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S043, V4C-S009, V4B-S022, V4B-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Loops curtos e critérios estreitos favorecem modelos pequenos sem prometer reparo geral.
8–14B: Use contexto incremental e ferramentas para reduzir adivinhação em dependências.
15–30B: Um 15–30B pode justificar problemas mais difíceis, mas continua sujeito ao orçamento e ao mesmo verificador.
Requisitos de treino/runtime: Runtime de geração, checagem e revisão; não implica aprendizagem persistente do modelo.
Não aplicar quando: Não considerar timeout, erro de teste ou ausência de feedback como aprovação.

## T190:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Candidatos recebem avaliação e alimentam novas propostas.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Verificadores avaliam propriedades após geração e CI.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Há geração e crítica por ferramentas; isso não implica refinamento livre multiagente.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T190:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T190 → T195 [requires]
Como combinar: AutoClean combina propostas e verificações executáveis antes de prosseguir.
Interface: Revisão, resultados e falhas localizadas.
Condição: Verificação ligada ao conteúdo que será entregue.
Aceite proposto: Introduzir defeitos conhecidos e confirmar bloqueio.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T190 → T200 [complements]
Como combinar: Revisores por propriedade acrescentam checagem antes de revisão humana no AutoClean.
Interface: Artefato e relatórios separados.
Condição: Critérios e limites da revisão são explícitos.
Aceite proposto: Medir falhas detectadas e discordâncias.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Preservar última versão válida e rejeitar regressões.
- Registrar conclusão inconclusiva quando o orçamento ou infraestrutura impede verificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de tarefas concluídas corretamente e custo do loop com uma chamada de fronteira. Verificação pode amplificar utilidade de um modelo pequeno, desde que o critério cubra a falha relevante.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T189, T192, T195, T200

## Fontes primárias associadas

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S051 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback verbal e memória episódica podem melhorar tentativas posteriores sem atualizar pesos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T191 — Chain-of-Verification

**Nome canônico:** Chain-of-Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T191  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** CoVe; cadeia de verificação

## T191:C01 — conceito

Método de checagem que parte de uma resposta inicial, formula perguntas de verificação, responde a essas perguntas de forma separada e revisa o texto final. A separação busca reduzir influência do rascunho sobre a checagem. Não garante factualidade quando a verificação depende do mesmo conhecimento incorreto.

Como funciona:
- Produzir rascunho e identificar afirmações que precisam ser verificadas.
- Formular checagens e respondê-las com contexto separado quando apropriado.
- Revisar a resposta de acordo com os resultados e manter lacunas explícitas.

## T191:C02 — aplicacao

Quando usar:
- Respostas factuais compostas por várias alegações.
- Listas e textos em que um erro pontual compromete o conjunto.

Quando não usar:
- Trocar verificação de fonte por uma simples pergunta ao mesmo modelo se ele tem certeza.

Implementação proposta:
- Decompor alegações em itens verificáveis e não apenas frases inteiras.
- Usar fontes externas quando a tarefa depende de fatos atuais.
- Vincular cada correção à pergunta de checagem e à evidência correspondente.

Aplicação LAI proposta:
Proposta: a Helena usar checagens por alegação nos relatórios técnicos e comerciais, preservando fontes e separando inferência de fato.

## T191:C03 — riscos_validacao

Armadilhas:
- Checagens podem confirmar apenas partes fáceis e ignorar a alegação central.
- Rascunho completo nas perguntas pode induzir respostas ancoradas.

Métricas sugeridas:
- Alegações corretas antes e depois da revisão.
- Cobertura de checagem e número de falsos fatos introduzidos na revisão.

Testes propostos:
- Inserir fato falso entre fatos verdadeiros e testar sua identificação.
- Remover fonte essencial e exigir que a conclusão seja rebaixada para inconclusiva.

## T191:C04 — perguntas_proveniencia

Pergunta: CoVe prova uma afirmação só porque fez perguntas?
Resposta: Não. A qualidade depende das respostas de verificação e suas evidências.

Pergunta: Exige outro modelo?
Resposta: Não na formulação básica, embora verificadores distintos possam ser avaliados.

Pergunta: Perguntas neutras garantem verdade?
Resposta: Não. Elas reduzem indução, mas o respondente ainda pode desconhecer o fato ou consultar fonte errada.

Pergunta: Pode retornar só o texto final?
Resposta: Pode, mas preservar internamente o mapa de cobertura permite auditar quais afirmações receberam evidência e quais continuam incertas.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T191:C05 — mecanismo_avancado

Uma pergunta de checagem pode carregar a própria conclusão que deveria verificar. Formular “por que X aconteceu em 2020?” já pressupõe evento e data. Como proposta, transforme afirmações em questões neutras sobre entidades, relações e tempo, preserve um mapa entre alegações e verificações e marque o que não foi coberto. Responder em contextos separados reduz cópia do rascunho, mas não elimina conhecimento compartilhado incorreto.

Condição de contorno:
Alegações omitidas pelo planejador permanecem sem verificação mesmo quando todas as perguntas produzidas foram respondidas.

Contrato proposto:
- Entradas: Rascunho, inventário de alegações, perguntas neutras e fontes quando disponíveis.
- Saídas: Texto revisado e mapa de cada correção ou incerteza.
- Estado: Relações alegação-pergunta-resposta, contextos separados e proveniência.
- Invariante: Nenhuma alegação é declarada verificada apenas por estar perto de outra que foi checada.

Compromissos de projeto:
- Fatorar perguntas reduz interferência e aumenta número de chamadas.
- Adicionar busca amplia evidência e exige avaliar qualidade e atualidade das fontes.

## T191:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir data falsa na formulação de uma pergunta e deixar outra alegação sem pergunta correspondente. Esperar detecção de pressuposição e indicação de cobertura incompleta.

Plano de avaliação proposto:
Plano proposto: comparar checagem conjunta e fatorada com o mesmo rascunho. Medir cobertura, correções válidas, erros introduzidos e custo; avaliar factualidade por referências externas, sem considerar respostas do próprio modelo como certificado suficiente.

Comparações:
- T200 (complements): Independência de contexto ajuda a reduzir contaminação, mas verificação externa acrescenta outra dimensão de independência.

Afirmação rastreável:
Na variante fatorada de CoVe, perguntas são respondidas separadamente sem o rascunho original no contexto de resposta.
Suporte: direct; fontes: C-S044
Limite: O trabalho publicado estudou uso do próprio LLM; integrar fontes externas é uma extensão proposta.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T191:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 propôs perguntas neutras por alegação. A nova camada trata cobertura, evidência contraditória e atualização do texto, distinguindo autoquestionamento de verificação apoiada em fontes externas.

Inventário verificável
Extraia alegações atômicas com entidade, relação, tempo e escopo. Uma frase pode conter várias afirmações e qualificações; checar só o nome principal deixa datas e causalidade sem cobertura. Mantenha ligação entre cada alegação e a versão do rascunho para atualizar o mapa depois de revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

Busca que pode refutar
Formule consultas que permitam encontrar contradição e priorize fontes primárias adequadas ao tipo de fato. Preserve resultados conflitantes e data de validade. Pedir ao mesmo modelo que confirme sua frase sem nova evidência pode reduzir alguns erros, mas não constitui independência nem garantia factual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

Revisão com rastreabilidade
Quando uma checagem muda uma alegação, revise trechos dependentes dela, inclusive conclusões. Não substitua uma afirmação precisa por linguagem vaga apenas para escapar do teste. Marque o que continua não verificado e remova conclusões cuja base foi invalidada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

USO AVANÇADO — Relatório factual
Cenário: O modelo produz texto com datas, produtos e capacidades.
Estratégia: Extraia alegações, consulte fontes e reescreva somente depois de consolidar evidência. Priorize fatos que sustentam decisões, sem fingir cobertura integral quando o orçamento é limitado.
Papel do modelo pequeno: Um 3–7B pode estruturar alegações; recuperação e revisão externas sustentam a validade.
Aceite proposto: Medir cobertura de alegações relevantes e taxa de correções válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

USO AVANÇADO — Resposta sobre política formal
Cenário: Há regras documentadas e exceções.
Estratégia: Use perguntas de verificação para localizar fatos e um verificador formal para relações cobertas pela política. Separe erro de tradução, regra ausente e inconsistência.
Papel do modelo pequeno: Um 8–14B pode redigir a explicação, mantendo o alcance da prova explícito.
Aceite proposto: Nenhuma afirmação de verdade além do escopo das fontes ou da política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Decomposição curta e fontes explícitas reduzem carga de memória; o modelo não deve inventar respostas de checagem.
8–14B: Pode organizar verificações mais complexas, desde que entidades e datas sejam resolvidas.
15–30B: Maior porte não elimina necessidade de fontes atualizadas nem problemas de premissas falsas.
Requisitos de treino/runtime: Workflow em runtime; pesquisa externa e verificadores são complementos distintos do CoVe original.
Não aplicar quando: Não contar perguntas respondidas como fatos verificados sem avaliar evidência e cobertura.

## T191:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T191:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T191 → T200 [complements]
Como combinar: Checagem independente reduz dependência do rascunho como fonte.
Interface: Alegações neutras e evidências originais.
Condição: Verificador não recebe conclusão esperada como prova.
Aceite proposto: Testar alegações plausíveis, mas falsas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S044, V4B-S027, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T191 → T197 [complements]
Como combinar: Um schema pode organizar o mapa de alegações e estados de verificação.
Interface: IDs, fonte, status e trecho afetado.
Condição: Validade estrutural não substitui validade da evidência.
Aceite proposto: Detectar alegações sem fonte ou com checagem pendente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S044, V4B-S027, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar perguntas que pressupõem o fato contestado.
- Rever conclusões dependentes quando uma premissa é corrigida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fidelidade factual e cobertura com um baseline de fronteira sob acesso equivalente a fontes. O número de etapas de verificação não é uma medida de correção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T190, T200, T206

## Fontes primárias associadas

### C-S044 — Chain-of-Verification Reduces Hallucination in Large Language Models

[https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rascunho, perguntas de checagem, respostas independentes e revisão final compõem CoVe.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T192 — Self-Refine

**Nome canônico:** Self-Refine  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T192  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** autorefino

## T192:C01 — conceito

Refinamento iterativo em que o mesmo modelo gera uma saída, produz feedback e a revisa. O método estudado não exige treinamento adicional durante o ciclo. Pode corrigir problemas visíveis no texto, mas o crítico pode compartilhar os mesmos erros e critérios incompletos do gerador.

Como funciona:
- Gerar versão inicial com objetivo e restrições explícitos.
- Pedir feedback específico sobre defeitos observáveis.
- Produzir revisão e comparar com os critérios e a versão anterior.

## T192:C02 — aplicacao

Quando usar:
- Textos, planos ou artefatos que admitem melhoria por crítica localizada.
- Há rubrica capaz de distinguir melhora de mera reescrita.

Quando não usar:
- Tratar autocrítica como prova independente de fatos ou de execução.

Implementação proposta:
- Usar rubrica curta com critérios verificáveis.
- Limitar rodadas e conservar melhor versão avaliada.
- Encerrar quando não houver melhoria específica ou surgirem regressões.

Aplicação LAI proposta:
Proposta: usar autorefino para clareza e organização de artefatos da Helena, combinando testes e fontes externos para critérios objetivos.

## T192:C03 — riscos_validacao

Armadilhas:
- Revisão pode remover informação correta ou tornar texto apenas mais convincente.
- Modelo pode inventar defeitos para justificar uma nova rodada.

Métricas sugeridas:
- Melhorias aceitas por critério e regressões introduzidas.
- Custo por revisão útil e número de rodadas sem progresso.

Testes propostos:
- Fornecer versão inicial já correta e testar se ela permanece preservada.
- Inserir defeito conhecido e verificar se feedback o localiza e a revisão o corrige.

## T192:C04 — perguntas_proveniencia

Pergunta: Self-Refine treina o modelo?
Resposta: Não no procedimento descrito; modifica saídas dentro da execução.

Pergunta: É auditoria independente?
Resposta: Não. O mesmo modelo pode repetir seus próprios pontos cegos.

Pergunta: Mais rodadas significam mais inteligência útil?
Resposta: Não. Elas podem gerar oscilação, redundância ou regressão; acompanhe mudança real no objetivo.

Pergunta: Como detectar ausência de progresso?
Resposta: Compare defeitos pendentes e resultados externos entre versões; paráfrases e aumento de detalhes não contam automaticamente como melhoria.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T192:C05 — mecanismo_avancado

Feedback útil precisa identificar um defeito acionável e um critério de melhoria. Comentários genéricos podem apenas alongar a próxima resposta. Como proposta, conserve a versão anterior, registre mudanças e rejeite revisões que perdem requisitos já satisfeitos. O mesmo modelo pode alternar preferências entre rodadas; repetir até declarar satisfação não demonstra convergência para correção.

Condição de contorno:
Em tarefas que exigem informação nova, revisão sem ferramenta ou fonte adicional pode reorganizar o mesmo erro com mais confiança.

Contrato proposto:
- Entradas: Saída inicial, rubrica, limites de revisão e evidências acessíveis.
- Saídas: Versão escolhida acompanhada das mudanças relevantes e pendências.
- Estado: Histórico, críticas específicas, requisitos preservados e orçamento.
- Invariante: Nenhuma revisão é considerada melhor apenas porque é posterior ou mais longa.

Compromissos de projeto:
- Iterações podem corrigir defeitos locais e aumentar custo.
- Guardar versões permite regressão controlada e exige comparação por critérios consistentes.

## T192:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: começar com resposta correta e fornecer uma crítica equivocada produzida pelo próprio modelo. Esperar que a avaliação independente identifique a regressão e preserve ou restaure a versão anterior.

Plano de avaliação proposto:
Plano proposto: comparar geração única, revisão livre e revisão com rubrica em problemas independentes. Medir melhorias, regressões, comprimento e custo; aceitar o procedimento apenas quando o saldo de correção externa supera os danos introduzidos.

Comparações:
- T190 (alternative): Verifier loop exige critério de aceitação explícito; Self-Refine pode operar somente com feedback do mesmo modelo.

Afirmação rastreável:
Self-Refine utiliza o mesmo LLM para gerar, criticar e refinar saídas sem treinamento adicional durante o procedimento.
Suporte: direct; fontes: C-S045
Limite: A fonte relata resultados de tarefas específicas, não uma garantia de autoavaliação confiável.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T192:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu críticas acionáveis e preservação da versão anterior. Esta camada distingue melhoria de apresentação de correção factual e define quando incorporar evidência externa ao refinamento.

Critério antes da crítica
Defina o que pode melhorar: clareza, cobertura de requisitos, correção ou concisão. O mesmo modelo pode editar estilo de modo útil e continuar incapaz de detectar um erro factual. Não misture essas dimensões num pedido genérico para 'melhorar tudo', que dificulta medir progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

Feedback com evidência
Peça localização do defeito e motivo verificável. Quando a crítica exige conhecimento ausente, busque fonte ou ferramenta antes da revisão. O trabalho sobre limites de autocorreção alerta que feedback interno não substitui sinal externo; uma nova resposta mais confiante pode ser apenas outra hipótese.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

Seleção entre versões
Conserve versões e escolha pela rubrica, permitindo manter a inicial. Uma revisão pode satisfazer um requisito e perder outro; avalie o conjunto completo no fim. Limite alterações ao escopo autorizado e pare quando mudanças adicionais não oferecem benefício observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

USO AVANÇADO — Texto de domínio
Cenário: A informação já foi verificada, mas a apresentação está ruim.
Estratégia: Forneça uma rubrica de clareza e requisitos imutáveis. Peça revisão e compare se fatos, números e citações foram preservados.
Papel do modelo pequeno: Um 3–7B pode melhorar forma de textos curtos com conteúdo estável.
Aceite proposto: Medir preservação factual e cumprimento de requisitos, sem premiar comprimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

USO AVANÇADO — Resposta parcialmente correta
Cenário: O avaliador externo aponta falhas específicas.
Estratégia: Use feedback localizado para revisar o mínimo necessário e reexecute checagens. Se não houver sinal externo, registre a revisão como hipótese.
Papel do modelo pequeno: Um 8–14B pode refinar soluções especializadas com ferramentas, sujeito à validação.
Aceite proposto: A versão escolhida deve corrigir falha observada sem criar regressões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Bom candidato para ajustes de forma e erros estreitos; autocorreção geral não é presumida.
8–14B: Contexto suficiente para requisitos e diferenças entre versões ajuda a reduzir regressões.
15–30B: Um 15–30B pode revisar problemas maiores, mas continua sujeito a vieses compartilhados com a geração.
Requisitos de treino/runtime: Workflow em runtime, sem atualização persistente de pesos. Aprendizagem exige outro ciclo explícito.
Não aplicar quando: Não tratar a declaração 'agora está correto' do próprio modelo como evidência de melhoria.

## T192:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Pesquisa de refinamento e casos de revisão industrial consultados. AutoClean fornece exemplo de feedback externo; não é classificado como prova de autocorreção puramente interna.
Consultas registradas: V4B-Q011.

## T192:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T192 → T190 [complements]
Como combinar: Um loop com verificador externo transforma críticas em condições de aceite.
Interface: Versões e falhas específicas.
Condição: Verificador examina a revisão final.
Aceite proposto: Comparar refinamento interno e refinamento com evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S045, V3B-S019, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T192 → T205 [complements]
Como combinar: Testes de equivalência ajudam a preservar significado durante edição.
Interface: Observáveis, tolerâncias e versões.
Condição: Critério de equivalência adequado à tarefa.
Aceite proposto: Detectar mudanças de números, unidades ou efeitos laterais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S045, V3B-S019, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter a opção de rejeitar a revisão e conservar o original.
- Não interpretar maior fluência como maior correção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare revisões com avaliação cega e critérios separados. Self-Refine pode melhorar uma resposta específica, mas não demonstra que repetição interna aproxima indefinidamente um modelo pequeno da fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T190, T199, T200

## Fontes primárias associadas

### C-S045 — Self-Refine: Iterative Refinement with Self-Feedback

[https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: O próprio modelo gera, critica e revisa sem treino adicional no procedimento descrito.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T193 — Guardrails

**Nome canônico:** Guardrails  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T193  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controles de execução e saída

## T193:C01 — conceito

Conjunto de controles que limita entradas, saídas e ações conforme contratos e políticas. Pode incluir validação determinística, autorização, filtros e modelos classificadores. É uma família de mecanismos; uma frase no prompt ou um filtro isolado não constitui garantia completa de execução correta.

Como funciona:
- Definir invariantes da tarefa e pontos onde precisam ser aplicadas.
- Validar entrada e intenção antes de ações com efeito.
- Conferir saída e registrar rejeição, correção ou aprovação com motivo.

## T193:C02 — aplicacao

Quando usar:
- Agentes acessam ferramentas, dados de clientes ou fluxos com regras claras.
- Saídas precisam respeitar schema, escopo ou restrição operacional.

Quando não usar:
- Usar guardrail como substituto de correção do código, isolamento de dados ou avaliação de qualidade.

Implementação proposta:
- Aplicar autorização no backend, fora do texto gerado pela LLM.
- Separar controles obrigatórios de recomendações ajustáveis.
- Medir falsos bloqueios e manter diagnóstico sem vazar conteúdo sensível.

Aplicação LAI proposta:
Proposta: implementar contratos e permissões da Helena no runtime e avaliar controles de linguagem como complementos mensuráveis.

## T193:C03 — riscos_validacao

Armadilhas:
- Controles em apenas uma camada deixam outros caminhos de execução abertos.
- Classificador imperfeito pode bloquear uso legítimo ou aprovar violação.

Métricas sugeridas:
- Violações detectadas e não detectadas em testes.
- Taxa de bloqueio indevido e latência adicionada.

Testes propostos:
- Tentar acessar recurso fora do escopo e conferir bloqueio no executor.
- Testar pedido legítimo próximo da fronteira para medir falsos positivos.

## T193:C04 — perguntas_proveniencia

Pergunta: Guardrail é igual a censura textual?
Resposta: Não. Inclui regras operacionais como autorização, limite de custo e validação de argumentos.

Pergunta: Um framework de guardrails garante segurança total?
Resposta: Não. A cobertura e os caminhos de execução precisam ser verificados.

Pergunta: Prompt com regras é um guardrail completo?
Resposta: Não. Pode orientar o modelo, mas efeitos operacionais exigem controles no caminho que realmente os executa.

Pergunta: Falha do verificador significa saída inválida?
Resposta: Significa que a checagem não concluiu; a política deve decidir como proceder sem rotular desconhecimento como sucesso.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T193:C05 — mecanismo_avancado

O ponto em que um controle atua determina o que ele consegue impedir. Validar uma resposta textual depois que uma ferramenta já executou não desfaz o efeito produzido. Controles de ação precisam receber argumentos reais antes da execução e avaliar o resultado depois, enquanto controles de saída tratam o conteúdo entregue. Falhas de infraestrutura do verificador exigem política explícita, em vez de serem confundidas com aprovação.

Condição de contorno:
Um guardrail probabilístico pode ter falsos positivos e negativos; controles determinísticos também dependem da completude do contrato.

Contrato proposto:
- Entradas: Entrada, ação proposta, argumentos concretos, política versionada e resultado quando existente.
- Saídas: Decisão de permitir, bloquear ou corrigir, com motivo rastreável.
- Estado: Estado da operação, evidências, versão da regra e tentativas.
- Invariante: Uma ação sujeita a controle não contorna o ponto de validação por outro caminho.

Compromissos de projeto:
- Mais controles aumentam cobertura e latência.
- Regras rígidas simplificam auditoria e podem rejeitar casos legítimos não previstos.

## T193:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fazer a ferramenta ser chamada por uma rota alternativa sem passar no controlador e interromper o classificador. Esperar identificação do caminho descoberto e comportamento conforme a política de indisponibilidade.

Plano de avaliação proposto:
Plano proposto: avaliar casos permitidos, proibidos e ambíguos por ponto de aplicação. Medir falsos aceites, bloqueios indevidos, latência e cobertura de rotas; aprovar controles pelo comportamento observado e não apenas pela presença de configuração.

Comparações:
- T197 (complements): Schema valida forma dos argumentos, enquanto regras adicionais avaliam autorização e significado operacional.

Afirmação rastreável:
NeMo Guardrails distingue controles de entrada, diálogo, recuperação, execução de ferramentas e saída.
Suporte: direct; fontes: C-S046
Limite: Configurar uma biblioteca não prova que todas as rotas da aplicação passam pelos controles.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T193:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 localizou controles antes e depois de ações. O aprofundamento trata composição de regras, semântica de bloqueio e observabilidade de falsos positivos e lacunas.

Camadas com escopo
Separe validação estrutural, autorização, regra de negócio e avaliação de conteúdo. Cada camada deve declarar o que prova e o que não examina. Bedrock Automated Reasoning verifica relações numa política formal; isso não equivale a checar toda verdade do mundo nem a tornar correta a tradução de texto automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

Composição sem brechas
Todos os caminhos que executam uma ação precisam passar pela mesma decisão de autorização e pelo contrato aplicável. Uma alternativa de ferramenta ou retry não pode contornar a regra. Preserve identidade, argumentos efetivos e versão da política para que a decisão auditada corresponda à operação real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

Falhas e experiência
Defina resultados permitidos, bloqueados e inconclusivos. Falha do serviço de verificação pode exigir suspensão, redução de escopo ou encaminhamento conforme a operação, mas não aprovação silenciosa. Meça rejeições indevidas e explique ao fluxo de produto qual dado ou condição falta para continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

USO AVANÇADO — Geração de questões educacionais
Cenário: A saída precisa obedecer formato e restrições de conteúdo.
Estratégia: Use modelo especializado para propor e filtros antes de exibir. Learning Zone descreve a combinação, mas a configuração e escala atuais não são assumidas a partir do artigo de preparação.
Papel do modelo pequeno: Um 3–7B pode produzir objetos delimitados que passam por critérios externos.
Aceite proposto: Avaliar rejeição, correção e utilidade com revisão humana.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

USO AVANÇADO — Ação de negócio com efeitos
Cenário: O agente propõe alterar um registro.
Estratégia: Valide schema, identidade, permissão e pré-condição sobre o estado atual; execute somente após confirmação da decisão. Verifique pós-condição observada.
Papel do modelo pequeno: Um 8–14B pode interpretar intenção, enquanto controles determinísticos decidem a operação.
Aceite proposto: Nenhuma ação fora do contrato e distinção explícita entre falha e sucesso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Controles externos permitem tarefas estreitas, mas não compensam toda incapacidade do modelo.
8–14B: Especialização deve ser acompanhada de testes de cobertura e falsos bloqueios.
15–30B: Mesmo 15–30B continua sujeito às mesmas regras de autorização e validação.
Requisitos de treino/runtime: Runtime e serviços externos; pode coexistir com treinamento, sem ser equivalente a alinhamento dos pesos.
Não aplicar quando: Não chamar validação de JSON de verificação factual nem verificação formal de política de garantia universal.

## T193:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C022 — Amazon Web Services / Bedrock Automated Reasoning checks
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação descreve uma funcionalidade disponível de verificação por raciocínio automatizado para respostas em linguagem natural vinculadas a políticas.
Mecanismo documentado: Políticas são expressas formalmente e a tradução de texto para afirmações é analisada. O recurso é de detecção e possui restrições de idioma e resposta completa.
Correspondência com esta base: Guardrail verifica uma política expressa formalmente.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para redigir respostas e um verificador externo para políticas formalizáveis, encaminhando traduções ambíguas para revisão.
Limite: Disponibilidade não comprova adoção específica. Validade em uma política não garante verdade externa, atualização dos fatos ou correção da tradução de linguagem natural.
Fontes: V4B-S027.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Restrições verificáveis rejeitam saídas inadequadas antes da exibição.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T193:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T193 → T182 [complements]
Como combinar: Learning Zone combina especialização LoRA e guardrails antes da exibição.
Interface: Adapter, contrato de saída e resultado dos filtros.
Condição: Escopo especializado documentado.
Aceite proposto: Comparar qualidade e rejeição com avaliação humana.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T193 → T197 [requires]
Como combinar: Schema valida o contrato estrutural antes de regras semânticas.
Interface: Objeto parseado e schema versionado.
Condição: Recursos usados são suportados pelo validador.
Aceite proposto: Testar campos ausentes, extras e tipos incorretos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S046, V4B-S027, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar qual camada bloqueou e qual propriedade foi realmente verificada.
- Não permitir bypass por retry, ferramenta alternativa ou saída parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de resultados úteis e incorretos entregues, incluindo rejeições indevidas. Guardrails podem tornar uma aplicação pequena mais confiável no escopo, sem torná-la genericamente mais inteligente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T185, T197

## Fontes primárias associadas

### C-S046 — NeMo Guardrails

[https://github.com/NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ferramentas programáveis para impor controles a sistemas conversacionais; uso não substitui autorização no backend.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T194 — Process Supervision

**Nome canônico:** Process Supervision  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T194  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** supervisão de processo

## T194:C01 — conceito

Supervisão de treinamento que fornece sinais sobre etapas intermediárias, em vez de avaliar somente o resultado final. Pode ensinar um avaliador a identificar erros de processo ou fornecer sinal de aprendizagem ao modelo. Exige definição de etapas e rótulos confiáveis; texto longo não implica processo correto.

Como funciona:
- Coletar soluções ou trajetórias com passos observáveis.
- Rotular validade ou qualidade de passos segundo critérios consistentes.
- Treinar com esses sinais e avaliar se a conclusão melhora em tarefas novas.

## T194:C02 — aplicacao

Quando usar:
- Erros intermediários importam e podem ser identificados por anotadores ou verificadores.
- Resultado final sozinho não revela onde o procedimento falhou.

Quando não usar:
- Anotações apenas reproduzem plausibilidade linguística ou penalizam caminhos alternativos válidos.

Implementação proposta:
- Definir unidade de passo e rubrica de anotação.
- Medir concordância entre avaliadores e resolver conflitos.
- Comparar supervisão de processo e de resultado com dados e orçamento controlados.

Aplicação LAI proposta:
Proposta: registrar passos e evidências de tarefas verificáveis da Helena como candidatos a dados de supervisão, sem chamar todo trace de exemplo correto.

## T194:C03 — riscos_validacao

Armadilhas:
- Custo de anotação pode ser alto e rótulos inconsistentes ensinam critérios ruins.
- Passos aparentemente corretos podem terminar em resultado errado.

Métricas sugeridas:
- Precisão de detecção de erros intermediários.
- Qualidade final em teste reservado e custo de anotação.

Testes propostos:
- Inserir erro em etapa intermediária mantendo final plausível e testar localização.
- Incluir solução alternativa válida e verificar que não é rejeitada pelo estilo.

## T194:C04 — perguntas_proveniencia

Pergunta: Process supervision é só revisar uma resposta?
Resposta: Não. Refere-se ao sinal de treinamento sobre etapas; revisão em inferência é outro uso.

Pergunta: Exige acesso a pensamentos privados?
Resposta: Não. Pode supervisionar ações, resultados e passos explicitamente observáveis.

Pergunta: Resposta final correta basta como rótulo de todas as etapas?
Resposta: Não. Ela pode resultar de cancelamento de erros ou acerto casual.

Pergunta: Como evitar premiar enrolação?
Resposta: Avalie progresso e requisitos por etapa, distinguindo passos válidos úteis de repetições neutras sem avanço.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T194:C05 — mecanismo_avancado

A unidade de supervisão precisa ser definida: uma linha textual pode conter várias inferências, e uma inferência pode atravessar linhas. Rótulos de etapas ajudam a localizar erro, mas dependem da informação anterior e de critérios sobre progresso. Uma conclusão correta por coincidência não torna cada transição válida; inversamente, etapas neutras podem ser corretas sem avançar a solução. O dataset deve representar essas distinções.

Condição de contorno:
Rótulos inconsistentes ou segmentação inadequada podem ensinar o avaliador a preferir estilo e comprimento em vez de validade.

Contrato proposto:
- Entradas: Trajetórias segmentadas, contexto por etapa, critérios de rótulo e anotadores ou verificadores.
- Saídas: Modelo avaliador ou sinal de treinamento com feedback localizado.
- Estado: Proveniência dos rótulos, discordâncias e separação por problema de origem.
- Invariante: Etapas do mesmo problema não vazam entre treino e avaliação final sem controle explícito.

Compromissos de projeto:
- Feedback fino melhora atribuição de erro e custa anotação.
- Selecionar erros convincentes pode ser informativo e alterar a distribuição dos exemplos.

## T194:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir solução com resposta final correta e etapa intermediária inválida, além de sequência longa de passos neutros. Esperar avaliação diferenciada de validade e progresso.

Plano de avaliação proposto:
Plano proposto: comparar supervisão de resultado e de processo com orçamento de anotação declarado. Medir localização de erros, qualidade final, consistência entre anotadores e custo; usar problemas inéditos, não somente novas trajetórias dos mesmos enunciados.

Comparações:
- T206 (distinct_from): Supervisão de processo treina com sinais intermediários; verificação de processo pode apenas inspecionar uma execução.

Afirmação rastreável:
Let’s Verify Step by Step utiliza rótulos positivos, negativos e neutros para etapas intermediárias de soluções.
Suporte: direct; fontes: C-S047
Limite: A evidência estudada é principalmente matemática; não certifica que toda narrativa textual represente o processo interno real.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T194:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu unidades e rótulos de etapa. Esta camada examina qualidade do sinal local, custo de anotação e diferença entre supervisionar processo no treino e verificar uma execução em runtime.

O que uma etapa demonstra
Um passo pode ser válido, irrelevante, incompleto ou depender de premissa falsa. Use rótulos que preservem essas distinções quando úteis ao objetivo. Julgar somente fluência ou plausibilidade pode ensinar o avaliador a premiar explicações elegantes, sem detectar o primeiro erro que compromete a solução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

Trajetórias parciais
Para treinar um avaliador de processo, mantenha contexto suficiente e não forneça o resultado futuro como pista indevida. Inclua erros próximos de passos corretos e trajetórias que chegam à resposta certa por coincidência. Separe problemas de origem entre treino e teste para evitar memorização de soluções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

Processo e execução observável
Relatos de busca como AlphaEvolve usam avaliadores de programas e desempenho, mas isso não comprova supervisão de cada passo interno de raciocínio. Em agentes, estados de ferramenta e transições oferecem observáveis mais concretos que uma narrativa retrospectiva. Escolha a unidade de supervisão conforme o que pode ser validado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

USO AVANÇADO — Resolução técnica segmentada
Cenário: Uma tarefa possui etapas com critérios locais verificáveis.
Estratégia: Anote o primeiro erro e requisitos por transição, treine ou avalie o verificador e use-o para orientar revisão. Confirme se aprovação local leva a sucesso final.
Papel do modelo pequeno: Um 8–14B pode aprender procedimentos com feedback específico, sem presumir generalização irrestrita.
Aceite proposto: Medir detecção do primeiro erro e resultado final em problemas novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

USO AVANÇADO — Agente com ferramentas
Cenário: O workflow exige pré-condições antes de cada ação.
Estratégia: Use estados reais e resultados das ferramentas como sinais de etapa. Não aceite um texto dizendo que a condição foi satisfeita sem observação correspondente.
Papel do modelo pequeno: Um 3–7B pode executar etapas estreitas sob supervisão externa.
Aceite proposto: Verificar transições válidas e ausência de efeitos fora do plano.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Critérios locais simples podem tornar feedback mais útil que uma nota final genérica.
8–14B: Avaliar processos mais longos exige cobertura de dependências e erros acumulados.
15–30B: Maior porte pode produzir trajetórias mais complexas, elevando custo e ambiguidade da anotação.
Requisitos de treino/runtime: Supervisão de processo é treino ou avaliação de etapas; verificação em runtime é uso relacionado, não reprodução automática do método.
Não aplicar quando: Não equiparar cadeia de pensamento escrita a registro fiel de todos os mecanismos internos do modelo.

## T194:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T194:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T194 → T206 [complements]
Como combinar: Eventos observáveis podem fornecer unidades de processo verificáveis.
Interface: Estado anterior, ação e pós-condição.
Condição: Logs representam operações reais e possuem identidade.
Aceite proposto: Comparar narrativa com estado externo observado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S047, V3B-S018, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T194 → T199 [feeds]
Como combinar: Falhas localizadas podem orientar novos dados ou mudanças persistentes.
Interface: Etapa, tipo de erro e versão do componente.
Condição: Atualização explícita e avaliação independente.
Aceite proposto: Medir melhora em trajetórias novas, não só nos exemplos corrigidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S047, V3B-S018, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar validade local, progresso e correção final.
- Auditar discordâncias de anotadores antes de transformar rótulos em recompensa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare competência em processos definidos e verificáveis. Supervisão mais granular pode ajudar, mas não garante que um modelo pequeno tenha a capacidade necessária para todos os passos de uma tarefa de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T190, T206

## Fontes primárias associadas

### C-S047 — Let's Verify Step by Step

[https://arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão por etapas difere de rotular apenas o resultado final.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T195 — Verificação baseada em execução

**Nome canônico:** Verificação Baseada em Execução  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T195  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** execution-based verification; Verificação Baseada em Execução

## T195:C01 — conceito

Avaliação de uma proposta por executá-la em ambiente controlado e observar efeitos, saídas ou testes. É especialmente útil para código, consultas e transformações de dados. Passar em testes fornece evidência limitada à cobertura e ao ambiente, sem provar ausência de todos os defeitos.

Como funciona:
- Converter requisitos em entradas, invariantes e resultados esperados.
- Executar candidato em ambiente reproduzível com recursos limitados.
- Comparar comportamento observado e preservar logs ou artefatos de evidência.

## T195:C02 — aplicacao

Quando usar:
- Código ou transformação pode ser testado sem afetar produção.
- Há propriedade objetiva que o resultado deve cumprir.

Quando não usar:
- Executar conteúdo não confiável com acesso irrestrito a segredos ou sistemas reais.

Implementação proposta:
- Isolar ambiente e controlar rede, tempo e recursos necessários.
- Separar testes públicos de testes reservados relevantes.
- Registrar versão do código, dependências e dados usados.

Aplicação LAI proposta:
Proposta: a Helena sustentar declarações de funcionamento com comandos, resultados e testes pertinentes, separando validação local de operação real.

## T195:C03 — riscos_validacao

Armadilhas:
- Teste superficial pode aprovar solução incorreta.
- Ambiente de teste diferente do alvo pode esconder falha de integração.

Métricas sugeridas:
- Cobertura funcional relevante e taxa de falso aceite.
- Reprodutibilidade da execução e regressões encontradas.

Testes propostos:
- Introduzir mutações conhecidas que violam requisitos e conferir se testes falham.
- Reexecutar artefato em ambiente limpo para verificar dependências não declaradas.

## T195:C04 — perguntas_proveniencia

Pergunta: Passar em todos os testes prova perfeição?
Resposta: Não. Prova apenas comportamento nos casos e propriedades cobertos.

Pergunta: Só serve para código?
Resposta: Não. Pode verificar cálculos, schemas, arquivos e efeitos de workflows controlados.

Pergunta: Um exit code zero prova sucesso?
Resposta: Somente se o programa e o harness definem esse código de forma confiável e os critérios necessários foram realmente executados.

Pergunta: Como testar o próprio verificador?
Resposta: Use casos com resultados conhecidos, mutações que deveriam falhar e falhas de infraestrutura deliberadas para conferir a classificação dos resultados.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T195:C05 — mecanismo_avancado

A execução verifica uma relação entre artefato, entradas, ambiente e oráculo. Se o oráculo contém o mesmo erro do gerador, passar nos testes oferece falsa segurança. É preciso distinguir falha da proposta, falha da infraestrutura e caso não coberto. Para código, entradas de fronteira, efeitos laterais e limites de recursos fazem parte do comportamento; retorno correto em exemplos comuns não demonstra equivalência completa.

Condição de contorno:
Um conjunto finito de testes geralmente refuta defeitos encontrados, mas não prova correção para todas as entradas possíveis.

Contrato proposto:
- Entradas: Artefato identificado, ambiente controlado, casos, resultados esperados e limites de execução.
- Saídas: Observações reproduzíveis com estado aprovado, reprovado ou inconclusivo por critério.
- Estado: Versões de dependências, entradas, logs e identidade exata do artefato.
- Invariante: Erro do executor ou timeout nunca é convertido silenciosamente em teste aprovado.

Compromissos de projeto:
- Mais casos ampliam cobertura e tempo de avaliação.
- Ambiente isolado melhora controle e pode diferir das condições reais de implantação.

## T195:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar implementação correta nos exemplos originais, mas errada em entrada vazia, overflow ou repetição. Acrescentar casos independentes e exigir que o verificador detecte a falha.

Plano de avaliação proposto:
Plano proposto: comparar suíte inicial e ampliada com defeitos conhecidos e versões corretas. Medir falsos aceites, falsos alarmes, cobertura relevante e custo; reportar explicitamente domínio testado e ambiente, sem extrapolar para prova universal.

Comparações:
- T205 (complements): Comparação diferencial executa duas versões para investigar se preservam o comportamento especificado.

Afirmação rastreável:
EvalPlus ampliou casos de teste e identificou programas incorretos que passavam em suítes anteriores.
Suporte: direct; fontes: C-S048
Limite: A evidência mostra insuficiência de certas suítes, não que expansão automática garanta cobertura completa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T195:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu execução, ambiente e oráculo. Esta camada trata qualidade dos próprios testes, cobertura de efeitos e desenho de um executor que produz evidência reproduzível para seleção ou reparo.

Testar o verificador
Uma suíte que sempre passa pode estar vazia, desabilitada ou incapaz de detectar o defeito relevante. Use alterações deliberadas e mutações plausíveis para verificar sensibilidade. ACH documenta geração orientada por mutações; matar um mutante demonstra discriminação daquele comportamento, sem provar cobertura de todos os defeitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

Efeitos observáveis
Além de retorno, registre arquivos alterados, chamadas externas, recursos consumidos e exceções quando fazem parte do contrato. Um teste pode aprovar um valor enquanto a implementação modifica dados indevidamente. Limites de tempo e memória devem produzir estado inconclusivo ou reprovado conforme a regra, nunca sucesso por ausência de saída.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

Ambiente reproduzível
Fixe dependências, entradas e versão do artefato; preserve logs suficientes para reproduzir falhas. Isole execução de propostas de ambientes com efeitos reais não autorizados. Resultados em um simulador só sustentam o que ele modela; diferenças de integração precisam de checagem específica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

USO AVANÇADO — Geração de testes úteis
Cenário: Um modelo propõe ampliar uma suíte existente.
Estratégia: Exija que testes executem de forma estável e detectem uma alteração relevante. TestGen-LLM relata filtros industriais de compilação, execução e cobertura; preserve limites desses critérios.
Papel do modelo pequeno: Um 3–7B pode propor testes locais quando recebe contrato e exemplos.
Aceite proposto: Medir defeitos detectados e testes frágeis, não apenas linhas cobertas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

USO AVANÇADO — Busca de algoritmo
Cenário: Há muitas propostas com custo ou comportamento mensurável.
Estratégia: Execute em entradas representativas e adversas, filtre incorretas e compare desempenho somente entre válidas. AlphaEvolve é um caso de busca com avaliadores, em configurações próprias.
Papel do modelo pequeno: Um 8–14B pode explorar variantes pequenas dentro de um domínio executável.
Aceite proposto: Aceitar melhoria reproduzível sem regressão nos observáveis definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Critérios estreitos e ambientes rápidos tornam tentativa e verificação economicamente plausíveis.
8–14B: A dificuldade de produzir candidato correto e a qualidade do oráculo continuam limitantes.
15–30B: Modelos maiores podem gerar mais complexidade; orçamento de execução precisa acompanhar essa complexidade.
Requisitos de treino/runtime: Runtime de execução e avaliação; pode alimentar treino depois, mas executar testes não atualiza pesos.
Não aplicar quando: Não chamar cobertura alta de prova de correção nem executar código gerado em produção por mera aprovação textual.

## T195:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 3. Lacuna: 7. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 3. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Execução e avaliadores de código produzem sinais verificáveis.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Testes executáveis validam candidatos.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Testes são executados para aceitar candidatos.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Compilação e testes contribuem para validação do resultado.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T195:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T195 → T190 [feeds]
Como combinar: AutoClean usa resultados de verificações para controlar progressão de correções.
Interface: Revisão e evidência de execução.
Condição: Resultados correspondem à versão final.
Aceite proposto: Injetar falhas e verificar bloqueio ou reparo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T195 → T205 [complements]
Como combinar: Comparação diferencial e propriedades metamórficas ampliam testes quando não há resposta única.
Interface: Entradas, referência e observáveis.
Condição: Normalização não apaga diferenças relevantes.
Aceite proposto: Gerar contraexemplos e reduzi-los para reprodução.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S048, V4B-S022, V4B-S024, V4B-S025, V4B-S026, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Confirmar que os testes foram efetivamente descobertos e executados.
- Separar defeito do candidato de indisponibilidade do ambiente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Execução pode tornar modelos pequenos úteis em tarefas com bons oráculos. A comparação com fronteira deve incluir custo de candidatos descartados e falhas que a suíte não observa.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T189, T190, T200, T205

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T196 — Constrained Decoding / Grammar-Constrained Decoding

**Nome canônico:** Decodificação restrita por gramática  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T196  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Constrained Decoding; decodificação restrita; grammar-guided decoding; Grammar-Constrained Decoding; grammar-constrained generation

## T196:C01 — conceito

Constrained Decoding restringe tokens durante a geração para manter o prefixo dentro de uma linguagem permitida. Grammar-Constrained Decoding é sua forma orientada por gramática, útil para JSON, DSLs e estruturas de chamadas. Pode reduzir erros de sintaxe, mas não demonstra verdade factual, autorização ou correção de domínio. Um JSON válido ainda pode conter valores incorretos.

Como funciona:
- Compilar gramática ou restrições suportadas em um estado que acompanha o prefixo emitido.
- A cada passo, calcular continuações permitidas e mascarar tokens que tornariam a conclusão inválida.
- Permitir término somente em estado aceitável, ou retornar falha/incompletude quando orçamento e restrições impedirem a conclusão.

## T196:C02 — aplicacao

Quando usar:
- Interfaces que exigem saída parseável, enumerações limitadas ou linguagem formal com contrato previamente conhecido.

Quando não usar:
- Como único verificador de cálculos, fatos, permissões ou efeitos de uma ação externa.

Implementação proposta:
- Proposta: declarar a gramática e o subconjunto de JSON Schema aceito pelo engine; nem toda restrição semântica vira gramática.
- Testar compatibilidade com tokenizer, tokens especiais, Unicode e escapes; reservar orçamento para encerrar a estrutura.
- Versionar schema e gramática juntos, invalidando artefatos compilados quando mudarem.
- Após decodificar, executar parser, validação de schema e regras de domínio; registrar recusa, truncamento e ausência de continuação admissível como estados distintos.

Aplicação LAI proposta:
Proposta LAI: restringir formato de comandos candidatos e exigir verificações externas antes da execução; a gramática compõe o contrato de saída, sem substituir o controlador de integridade.

## T196:C03 — riscos_validacao

Armadilhas:
- Uma gramática inconsistente pode bloquear a geração; uma excessivamente permissiva pode aceitar estruturas inúteis.
- Aplicar uma sequência de parada antes do fechamento da estrutura pode produzir prefixo válido, porém documento incompleto.

Métricas sugeridas:
- Taxa de parse válido, violações de domínio, latência de compilação, overhead de decodificação e saídas sem término válido.

Testes propostos:
- Teste proposto: gerar strings com aspas, barras, Unicode e valores enumerados, incluindo casos próximos dos limites.
- Forçar truncamento e gramática incompatível e verificar que o consumidor não executa argumentos parciais.

## T196:C04 — perguntas_proveniencia

Pergunta: Grammar-Constrained Decoding valida só depois da geração?
Resposta: Não. Restringe escolhas durante a geração; validação posterior permanece útil para integridade final e regras de domínio.

Pergunta: Uma gramática garante um identificador real e autorizado?
Resposta: Não. Pode garantir a forma do identificador; existência e autorização precisam de consulta e verificação externas.

Pergunta: Token estruturalmente permitido pode estar errado?
Resposta: Sim. Um número ou identificador pode obedecer à gramática e designar um valor incorreto.

Pergunta: EOS sempre significa JSON completo?
Resposta: Somente se o protocolo de término exige completude; truncamento e políticas de parada externas precisam ser tratados separadamente.

Escopo das fontes:
XGrammar fundamenta restrição por gramática; JSON Schema fundamenta validação estrutural. Contrato LAI e testes são propostas.

## T196:C05 — mecanismo_avancado

Uma gramática válida para caracteres precisa ser relacionada aos tokens reais do modelo, que podem conter fragmentos ou vários símbolos estruturais. O estado do matcher deve avançar pelo token escolhido e produzir a máscara da etapa seguinte. Tamanho de vocabulário do tokenizer e dimensão dos logits também podem diferir por padding. Um prefixo ainda extensível não é uma estrutura concluída quando o orçamento termina.

Condição de contorno:
Restrições incompatíveis podem deixar nenhum token permitido; remover a máscara silenciosamente violaria o contrato estrutural.

Contrato proposto:
- Entradas: Gramática ou schema suportado, tokenizer, dimensão dos logits e estado de geração.
- Saídas: Tokens permitidos e resultado com estado de conclusão explícito.
- Estado: Gramática compilada, matcher por sequência e máscaras alinhadas ao vocabulário.
- Invariante: A máscara corresponde exatamente ao prefixo confirmado daquela sequência.

Compromissos de projeto:
- Restringir tokens reduz erros estruturais e adiciona custo de compilação ou matching.
- Gramáticas rígidas podem excluir representações válidas que o contrato não descreveu.

## T196:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reutilizar matcher de outra sequência e encerrar a geração antes do fechamento de um objeto. Esperar detecção do estado incompatível e indicação de estrutura incompleta, sem fallback irrestrito.

Plano de avaliação proposto:
Plano proposto: comparar geração livre e restrita sob o mesmo schema e modelo. Medir validade completa, conteúdo correto, latência e casos sem continuação; exigir validação final independente e separar sucesso sintático de factualidade.

Comparações:
- T197 (complements): Schema validation examina o objeto produzido; constrained decoding restringe o caminho enquanto ele é produzido.

Afirmação rastreável:
O workflow XGrammar vincula compilação ao tokenizer e mantém um matcher que aceita tokens e gera máscaras subsequentes.
Suporte: direct; fontes: V3B-S025
Limite: O suporte de grammar/schema e término depende da implementação; estrutura permitida não prova fatos externos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T196:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou matcher e alinhamento de tokens. O aprofundamento trata regiões livres e estruturadas, interação com ferramentas e especulação e confirmação do objeto completo antes de uso.

Estrutura por regiões
XGrammar documenta structural tags para combinar texto livre e regiões com formato restrito. Isso permite tratar raciocínio, texto e chamada de ferramenta com estados distintos, mas exige delimitadores compatíveis com o formato do modelo. Não aplique uma gramática de um template a outro apenas porque ambos parecem JSON.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

Conclusão e entrega
Um prefixo permitido pode terminar por limite de tokens antes de formar objeto completo. O serviço deve comunicar término, validar estrutura final e impedir que fragmentos sejam executados como chamada de ferramenta. Streaming pode exibir progresso, mas não autoriza tratar uma chamada incompleta como ação confirmada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

Especulação e máscara
Propostas especulativas precisam respeitar o estado correto da gramática durante verificação e rollback. A Apple descreve combinação de geração guiada e especulação no framework local. Essa evidência sustenta a combinação naquela pilha, sem garantir suporte de qualquer runtime, tokenizer ou versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

USO AVANÇADO — Chamada de ferramenta tipada
Cenário: O modelo precisa produzir nome e argumentos válidos.
Estratégia: Compile restrições compatíveis, mantenha matcher por sequência e valide argumentos completos antes da autorização. Regras de negócio e permissões continuam externas.
Papel do modelo pequeno: Um 3–7B pode preencher contratos estreitos com menos falhas sintáticas.
Aceite proposto: Medir validade estrutural, campos semanticamente corretos e chamadas indevidas separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

USO AVANÇADO — Saída mista
Cenário: A resposta contém explicação e um objeto que será consumido por software.
Estratégia: Use regiões estruturadas explícitas e mantenha o parser alinhado ao template. Teste delimitadores dentro de strings e encerramento prematuro.
Papel do modelo pequeno: Um 8–14B pode explicar e estruturar, sem que texto livre seja interpretado como comando.
Aceite proposto: Nenhum objeto parcial aceito e nenhuma confusão entre texto e ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Restringir formato ajuda utilização prática, mas não ensina o significado dos campos.
8–14B: Schemas complexos podem reduzir liberdade útil ou elevar custo de compilação; medir.
15–30B: Maior porte não dispensa gramática quando a interface exige estrutura exata.
Requisitos de treino/runtime: Runtime com integração de logits e tokenizer; treino não é obrigatório para a restrição, mas o modelo precisa compreender a tarefa.
Não aplicar quando: Não confundir saída sintaticamente válida com dados verdadeiros ou autorização de ação.

## T196:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: Geração guiada compila restrições sobre a saída.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: Restrições são aplicadas durante geração em backends compatíveis.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: Restringe geração por gramática durante decoding.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## T196:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T196 → T079 [complements]
Como combinar: O framework Apple documenta geração guiada combinada com especulação.
Interface: Estado de restrição e tokens confirmados.
Condição: Suporte da pilha descrita, sem extrapolação para outros backends.
Aceite proposto: Testar aceitação e conclusão com gramática ativa.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S002. Casos: V4D-C001.

2. T196 → T197 [requires]
Como combinar: Validação final confirma o objeto no dialeto e regras adotados pelo consumidor.
Interface: Objeto completo e schema versionado.
Condição: Recursos do gerador e validador são compatíveis.
Aceite proposto: Testar limites de geração, campos extras e regras não suportadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Invalidar matcher ao reiniciar uma sequência com outro prefixo.
- Não interpretar encerramento por limite como conclusão válida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve medir conteúdo correto dentro do contrato. Gramática pode equalizar parte da confiabilidade de interface, sem equalizar conhecimento ou capacidade de decisão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T197, T195, P012, P015

## Fontes primárias associadas

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S025 — Workflow of XGrammar

[https://xgrammar.mlc.ai/docs/latest/start/workflow_of_xgrammar.html](https://xgrammar.mlc.ai/docs/latest/start/workflow_of_xgrammar.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compilação vinculada ao tokenizer, máscara de vocabulário, avanço e término do matcher.

Limite: Documentação dinâmica consultada; gramática limita estrutura e não verifica fatos externos.

### V4B-S015 — Structural Tag Usage — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de formatos, tags, regiões livres/estruturadas e delimitadores de tokens.

Limite: Restrições formais não validam autorização, conteúdo factual nem sucesso de ferramenta.

### V4B-S016 — Tool Calling and Reasoning — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas específicas de formato de modelo e escolhas auto/required/forced/none para chamadas de ferramenta.

Limite: Lista de estilos não verifica checkpoint do usuário; interoperabilidade precisa ensaio por tokenizer e backend.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V3D-S014 — Guidance — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contrato da geração JSON e limitações de suporte a recursos de JSON Schema.

Limite: Suporte depende da versão; saída final e regras de domínio precisam de validação própria.

### V3D-S015 — Guidance — Introduction

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo programático e diferenças de capacidade entre backends locais e remotos.

Limite: Compartilhamento interno de recursos não implica fronteira de segurança ou equivalência de provedores.

### V4B-S030 — Token healing — Guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de fronteiras de tokenização por recuo e prefixo restrito; integração documentada com LlamaCpp/Transformers.

Limite: Exemplos não comprovam qualidade de domínio nem implementação eficiente em todo provedor remoto.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T197 — JSON Schema Validation

**Nome canônico:** JSON Schema Validation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T197  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** validação de JSON Schema

## T197:C01 — conceito

Validação de um documento JSON contra um schema com tipos, campos obrigatórios, enums e outras restrições. É uma verificação determinística de contrato estrutural dentro do dialeto e configuração usados. Não confirma existência de um cliente, verdade de uma afirmação ou autorização para uma ação.

Como funciona:
- Escolher dialeto e validar o próprio schema.
- Analisar JSON e aplicar as restrições ao documento.
- Devolver erros com localização antes de qualquer consumo ou efeito dependente.

## T197:C02 — aplicacao

Quando usar:
- Fronteiras entre agentes, ferramentas e serviços.
- Ingestão de dados com contrato estável e erros que precisam ser explicáveis.

Quando não usar:
- Assumir que toda regra de negócio pode ser expressa apenas no schema.

Implementação proposta:
- Declarar campos obrigatórios e política de campos extras.
- Diferenciar campo ausente, null e string vazia.
- Conferir comportamento de format e referências no validador escolhido.

Aplicação LAI proposta:
Proposta: todos os eventos e resultados de ferramentas da Helena passarem por schema versionado, seguido de verificação das regras de negócio.

## T197:C03 — riscos_validacao

Armadilhas:
- Defaults descritos no schema nem sempre são inseridos pelo validador.
- Configurações de format podem somente anotar, sem rejeitar valor inválido.

Métricas sugeridas:
- Rejeições corretas e aceitações incorretas do contrato.
- Erros por versão e localização de falhas nos documentos.

Testes propostos:
- Testar fronteiras numéricas, tipos errados e propriedades desconhecidas.
- Usar payload estruturalmente válido com referência inexistente e exigir validação de domínio adicional.

## T197:C04 — perguntas_proveniencia

Pergunta: Schema valida a veracidade do valor?
Resposta: Não. Valida restrições especificadas; fatos precisam de outra verificação.

Pergunta: Required impede null?
Resposta: Não sozinho. É preciso também definir um tipo que exclua null.

Pergunta: format email confirma que a caixa existe?
Resposta: Não. Mesmo uma checagem sintática de formato não confirma existência, titularidade ou capacidade de entrega.

Pergunta: Schema válido prova argumento autorizado?
Resposta: Não. Autorização depende do solicitante, recurso e operação, além da forma dos dados enviados.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T197:C05 — mecanismo_avancado

Declarar uma propriedade não a torna obrigatória: presença é controlada por required. Em composição, additionalProperties observa o subschema em que foi declarado e pode rejeitar extensões pretendidas; unevaluatedProperties permite considerar propriedades avaliadas por outras partes, conforme o dialeto. O keyword format também pode funcionar como anotação, sem checagem de validade, se a configuração não exigir o vocabulário de asserção correspondente.

Condição de contorno:
Dois validadores com dialetos ou suporte de format diferentes podem discordar sem que os mesmos bytes do JSON tenham mudado.

Contrato proposto:
- Entradas: JSON parseado, schema identificado, dialeto e configuração explícita do validador.
- Saídas: Resultado com caminhos dos erros e indicação de recursos não suportados.
- Estado: Versões do schema, resoluções de referências e política de formatos.
- Invariante: Uma restrição obrigatória desconhecida nunca é tratada como se tivesse sido verificada.

Compromissos de projeto:
- Schemas fechados detectam campos inesperados e dificultam evolução.
- Composição facilita reúso e exige compreender o escopo de cada restrição.

## T197:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover campo declarado mas não required, acrescentar propriedade por allOf e usar format inválido. Esperar resultados coerentes com o dialeto e a configuração documentados, sem supor validação inexistente.

Plano de avaliação proposto:
Plano proposto: criar casos válidos e inválidos por restrição, comparar implementações quando necessário e verificar mensagens de erro. Medir cobertura do contrato e compatibilidade entre produtores/consumidores; adicionar checagens externas para fatos e autorização.

Comparações:
- T196 (complements): Uma gramática de geração pode impor parte do schema, mas o objeto final ainda precisa ser validado.

Afirmação rastreável:
A documentação JSON Schema diferencia propriedades declaradas, obrigatórias, adicionais e propriedades avaliadas através de composição.
Suporte: direct; fontes: V3B-S024
Limite: A evidência cobre estrutura; existência de registros e significado dos valores dependem de validações de domínio.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T197:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou required e dialetos. A nova camada trata schemas como versões de interface, limites de resolução e a separação entre validação de forma e invariantes que dependem de estado externo.

Evolução do contrato
Adicionar um campo opcional pode ser compatível para alguns consumidores e quebrar outros que rejeitam propriedades extras. Versione schema e política de compatibilidade, incluindo defaults aplicados fora da validação. Teste produtor antigo com consumidor novo e a direção inversa antes de anunciar uma mudança transparente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

Referências e recursos
Resolução de referências precisa ser previsível e limitada. Prefira schemas conhecidos e cacheados, com limites de profundidade e tamanho quando entradas não são confiáveis. Um validador pode ser correto no dialeto e ainda consumir recursos excessivos em estruturas complexas; faça essa avaliação separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

Semântica além da forma
Schema pode garantir que valor é número e campo existe, mas não que saldo está atualizado, entidade pertence ao usuário ou citação sustenta a frase. Encaminhe essas condições a regras de negócio e fontes. Uma validação formal de política, como no Bedrock, é outra camada com alcance próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

USO AVANÇADO — API consumida por modelo pequeno
Cenário: O serviço exige argumentos tipados.
Estratégia: Use schema restrito ao que o gerador e o validador suportam, valide o objeto completo e gere erros por caminho. Reparo deve preservar campos já corretos e revalidar o conjunto.
Papel do modelo pequeno: Um 3–7B pode preencher contratos simples com ajuda de geração restrita.
Aceite proposto: Medir campos corretos e falhas de negócio, além da taxa de JSON parseável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

USO AVANÇADO — Migração de interface
Cenário: Uma ferramenta passa a exigir novos dados.
Estratégia: Crie adaptador explícito ou nova versão, mantendo testes cruzados. Não preencha automaticamente um valor de negócio desconhecido só para satisfazer required.
Papel do modelo pequeno: Um 8–14B pode explicar ou coletar o dado ausente, sem inventar defaults.
Aceite proposto: Detectar incompatibilidades e impedir execução com dados fabricados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Schemas pequenos e campos claros reduzem carga de seleção e reparo.
8–14B: Composição complexa exige cobertura de teste e diagnóstico de erros compreensível.
15–30B: Mesmo 15–30B deve ter validação determinística na fronteira da interface.
Requisitos de treino/runtime: Biblioteca de validação, dialeto e recursos suportados explicitamente; não exige treinamento.
Não aplicar quando: Não assumir que annotation format foi validada nem que campos presentes são factualmente corretos.

## T197:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: JSON Schema pode alimentar a gramática, mas isso não substitui validação posterior independente.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013, V4B-Q019.

## T197:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T197 → T196 [complements]
Como combinar: Decodificação restrita pode reduzir saídas estruturalmente inválidas antes da checagem final.
Interface: Schema suportado e objeto completo.
Condição: Conjunto de recursos aceitos por ambos é conhecido.
Aceite proposto: Testar casos que a gramática não consegue expressar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S049, V3B-S024, V4B-S015, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T197 → T193 [feeds]
Como combinar: Resultado estrutural é uma entrada para controles de negócio e autorização.
Interface: Objeto validado, versão e erros.
Condição: Nenhuma regra externa é presumida pela aprovação estrutural.
Aceite proposto: Submeter objeto válido com valor não autorizado e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S049, V3B-S024, V4B-S015, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar keywords obrigatórios desconhecidos como verificados.
- Manter testes negativos para campos extras, tipos, limites e referências.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Validação determinística pode tornar a interface de um modelo pequeno confiável quanto à estrutura. Compare qualidade dos dados separadamente; schema não é uma medida de inteligência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T141, T170, T196

## Fontes primárias associadas

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S024 — JSON Schema — Object reference

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campos obrigatórios, propriedades adicionais e composição com unevaluatedProperties.

Limite: Validação estrutural depende do dialeto e implementação; não demonstra fatos externos ou autorização.

### V4B-S015 — Structural Tag Usage — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de formatos, tags, regiões livres/estruturadas e delimitadores de tokens.

Limite: Restrições formais não validam autorização, conteúdo factual nem sucesso de ferramenta.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4B-S016 — Tool Calling and Reasoning — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas específicas de formato de modelo e escolhas auto/required/forced/none para chamadas de ferramenta.

Limite: Lista de estilos não verifica checkpoint do usuário; interoperabilidade precisa ensaio por tokenizer e backend.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T198 — Calibrated Confidence

**Nome canônico:** Calibrated Confidence  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T198  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** confiança calibrada

## T198:C01 — conceito

Confiança calibrada é uma estimativa de probabilidade cuja frequência observada de acerto corresponde aproximadamente aos valores previstos no domínio avaliado. Uma LLM declarar alta confiança não estabelece calibração. É necessário definir o evento de acerto e comparar previsões com resultados em dados separados.

Como funciona:
- Coletar escores e resultados verdadeiros em tarefas representativas.
- Ajustar transformação de calibração quando apropriado.
- Avaliar confiabilidade por faixa de escore e monitorar mudança de distribuição.

## T198:C02 — aplicacao

Quando usar:
- Decisões precisam de limiares de aceitação ou escalada.
- Existe referência suficiente para medir acertos e erros.

Quando não usar:
- Transformar linguagem de certeza em probabilidade sem validação ou extrapolar calibração entre domínios.

Implementação proposta:
- Separar dados de ajuste e teste da calibração.
- Medir Brier score, curvas de confiabilidade e cobertura de abstenção.
- Recalibrar após troca de modelo, prompt ou distribuição quando necessário.

Aplicação LAI proposta:
Proposta: a Helena usar probabilidades apenas quando vinculadas a avaliação de evento definido; nos demais casos, declarar evidência e incerteza qualitativa.

## T198:C03 — riscos_validacao

Armadilhas:
- ECE depende de divisão em faixas e pode esconder erros locais.
- Modelo calibrado globalmente pode falhar em subgrupos ou tarefas específicas.

Métricas sugeridas:
- Brier score e erro de calibração com tamanho de amostra.
- Erro dos casos aceitos em cada limiar de cobertura.

Testes propostos:
- Avaliar em período posterior ao utilizado no ajuste.
- Criar deslocamento de distribuição e verificar se confiança perde aderência aos acertos.

## T198:C04 — perguntas_proveniencia

Pergunta: Noventa por cento dito pelo modelo é probabilidade real?
Resposta: Não sem calibração observada.

Pergunta: Temperatura de calibração altera criatividade?
Resposta: É outro uso da escala de logits, aplicado a confiança; não se confunde com temperatura de geração.

Pergunta: Confiança de 90% certifica um caso individual?
Resposta: Não. O significado é frequencial em casos comparáveis, condicionado ao evento e à distribuição avaliados.

Pergunta: Aumentar temperatura sempre calibra?
Resposta: Não. O parâmetro deve ser ajustado e validado; uma transformação adequada em um conjunto pode falhar sob mudança de distribuição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T198:C05 — mecanismo_avancado

Calibração é uma propriedade estatística de previsões e resultados em uma distribuição. Agrupar exemplos por confiança e comparar frequência de acerto revela desvios, mas a escolha dos bins pode ocultar erros locais. Uma pontuação própria, como Brier, avalia probabilidades contra eventos observados sem depender apenas do rótulo vencedor. Para respostas abertas, o evento de acerto precisa ser definido antes de produzir o número.

Condição de contorno:
Calibração em um domínio não se preserva automaticamente após mudança de modelo, prompt, ferramenta ou população de consultas.

Contrato proposto:
- Entradas: Predições probabilísticas, critério de correção e dados de calibração separados da avaliação.
- Saídas: Estimador calibrado e relatório por faixa, domínio e cobertura.
- Estado: Transformação aprendida, versões e distribuição de referência.
- Invariante: Nenhum resultado usado para ajustar a calibração conta como evidência independente de sua qualidade final.

Compromissos de projeto:
- Calibrar pode melhorar decisões sem aumentar acurácia do classificador.
- Abster-se reduz cobertura e pode diminuir erro entre respostas entregues.

## T198:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter confiança constante enquanto muda a frequência real de acerto em outro domínio. Esperar detecção de descalibração e revisão da política de decisão.

Plano de avaliação proposto:
Plano proposto: comparar probabilidades originais e calibradas em dados novos. Medir Brier, curvas de confiabilidade, acurácia e risco versus cobertura; escolher limites de abstenção conforme custo dos erros, sem limiar universal inventado.

Comparações:
- T203 (complements): Estimativas calibradas podem orientar quando encaminhar uma tarefa a outro executor.

Afirmação rastreável:
O estudo de calibração avalia discrepâncias entre confiança e acerto e métodos de ajuste, incluindo temperature scaling.
Suporte: direct; fontes: C-S050
Limite: Resultados de classificação não tornam confiança verbal de uma LLM automaticamente uma probabilidade válida.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T198:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu calibração estatística e Brier. Esta camada orienta definição do evento, avaliação de cobertura e manutenção de limiares quando modelo, domínio ou política de seleção mudam.

Evento mensurável
Escolha o que significa sucesso: campo correto, teste passado, resposta sustentada ou tarefa concluída. Um único número para toda resposta pode esconder componentes com riscos diferentes. Para linguagem aberta, rotule com critérios consistentes e preserve discordâncias; sem evento definido, a confiança não possui interpretação operacional estável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

Seleção altera distribuição
Um roteador pode mandar apenas casos difíceis ao modelo maior e apenas casos fáceis ao menor. Calibração medida antes dessa seleção pode deixar de valer. Avalie por caminho efetivo, incluindo abstenções e rejeições. A precisão dos casos respondidos deve ser acompanhada da fração de casos que o sistema aceita responder.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

Mudanças de versão
Quantização, adapter, prompt e ferramenta podem alterar a relação entre score e acerto. Monitore deriva e reavalie limiares com dados recentes separados. Não ajuste continuamente sobre a mesma amostra que será usada para anunciar melhoria; registre quais dados informaram cada versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

USO AVANÇADO — Roteamento com abstenção
Cenário: Uma aplicação aceita automatizar apenas casos de baixo risco.
Estratégia: Calibre um sinal contra resultado verificável, escolha limiar no desenvolvimento e avalie cobertura/erro em dados independentes. Encaminhe ou busque evidência quando o sinal não basta.
Papel do modelo pequeno: Um 3–7B pode atender a região em que foi validado, sem fingir confiança universal.
Aceite proposto: Medir erro entre aceitos e custo dos encaminhamentos por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

USO AVANÇADO — Extração com revisão humana
Cenário: Alguns campos exigem mais certeza que outros.
Estratégia: Calibre por tipo de campo e contexto, usando evidência do documento e sinais do modelo. Mostre incerteza útil para revisão, evitando um percentual decorativo.
Papel do modelo pequeno: Um 8–14B pode produzir valores e sinais, mas o número final depende de validação.
Aceite proposto: Reduzir trabalho de revisão sem aumentar erros importantes omitidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V3B-S019, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Confiança verbal do 3–7B não é uma probabilidade calibrada; usar dados de resultado.
8–14B: Modelos intermediários precisam de avaliação por domínio e tipo de tarefa.
15–30B: Maior porte pode melhorar acerto sem melhorar calibração na mesma proporção.
Requisitos de treino/runtime: Etapa estatística sobre resultados observados; não basta pedir ao modelo uma nota de certeza.
Não aplicar quando: Não interpretar aprovação de schema ou de política formal como probabilidade de verdade de toda resposta.

## T198:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019, V4B-Q024.

## T198:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T198 → T203 [feeds]
Como combinar: Estimativas calibradas ajudam a escolher executores e escalonamento.
Interface: Probabilidade do evento definido, custo e domínio.
Condição: Distribuição de implantação compatível ou monitorada.
Aceite proposto: Comparar correção e cobertura por destino.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V3B-S019, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T198 → T202 [complements]
Como combinar: Incerteza pode orientar qual observação adicional adquirir.
Interface: Lacuna e efeito esperado de obter evidência.
Condição: Sinal tem interpretação validada.
Aceite proposto: Medir se a ação reduz erro, não apenas aumenta confiança.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V3B-S019, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Avaliar subgrupos em que a média global esconde falhas.
- Manter abstenções e casos rejeitados no relatório de cobertura.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas de erro e cobertura sob o mesmo critério de sucesso. Uma confiança calibrada permite decidir onde usar um modelo pequeno; não amplia sua capacidade nem garante cada resposta individual.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T156, T187, T202, T203

## Fontes primárias associadas

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T199 — Aprendizagem por avaliação

**Nome canônico:** Aprendizagem por Avaliação  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T199  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** evaluation-driven improvement; Aprendizagem por Avaliação

## T199:C01 — conceito

Rótulo geral para melhoria orientada por resultados de avaliações. O feedback pode alterar prompt, recuperação, memória procedural, política de roteamento ou pesos, dependendo do mecanismo implementado. Rodar um teste e guardar seu resultado não significa que o agente mudou seu comportamento.

Como funciona:
- Executar tarefas com critério de sucesso observável.
- Classificar falhas e escolher intervenção específica.
- Aplicar mudança versionada e avaliar novamente em casos separados.

Nota de nomenclatura: Rótulo editorial amplo; o mecanismo de aprendizagem precisa ser declarado em cada implementação.

## T199:C02 — aplicacao

Quando usar:
- Erros recorrentes têm diagnóstico e intervenção possíveis.
- Existe histórico de tarefas com resultados verificáveis.

Quando não usar:
- Avaliar no mesmo conjunto repetidamente e chamar memorização de melhoria geral.

Implementação proposta:
- Manter conjunto de desenvolvimento e teste reservado.
- Associar cada mudança a hipótese, métrica e evidência de efeito.
- Impedir promoção automática de memória inferida para fato comprovado.

Aplicação LAI proposta:
Proposta: usar episódios auditáveis da Helena para melhorar procedimentos e depois decidir, com métricas, se algum deles deve alimentar fine-tuning.

## T199:C03 — riscos_validacao

Armadilhas:
- Feedback incorreto pode consolidar um comportamento pior.
- Ajustar várias partes ao mesmo tempo impede identificar a causa do ganho.

Métricas sugeridas:
- Ganho em tarefas novas por intervenção.
- Regressões, repetição de erros e custo do ciclo de melhoria.

Testes propostos:
- Comparar versão nova e anterior em amostra temporal não usada na correção.
- Injetar feedback errado e verificar revisão ou quarentena antes da promoção.

## T199:C04 — perguntas_proveniencia

Pergunta: É sinônimo de reinforcement learning?
Resposta: Não. Pode haver melhoria sem gradiente, como memória e revisão de procedimento.

Pergunta: Avaliar sozinho faz aprender?
Resposta: Não. É preciso uma alteração concreta e provar seu efeito posterior.

Pergunta: Salvar resultados já é aprender?
Resposta: É registrar evidência; falta uma regra que altere comportamento persistente e uma avaliação dessa alteração.

Pergunta: Por que separar validação e teste final?
Resposta: Escolher repetidamente com a validação adapta decisões a ela; uma reserva independente estima melhor o desempenho após essa seleção.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T199:C05 — mecanismo_avancado

O ciclo de avaliação só produz aprendizagem quando modifica um componente persistente identificável: prompt, exemplos, roteador, recuperação, procedimento ou pesos. Otimizar repetidamente contra a mesma suíte transforma essa suíte em dado de desenvolvimento. O conjunto final precisa permanecer separado, inclusive de decisões manuais sobre quais mudanças manter. Uma métrica proxy pode ser explorada por respostas que aparentam sucesso sem cumprir a tarefa.

Condição de contorno:
Melhora no conjunto consultado a cada tentativa pode representar adaptação ao teste, sem generalização para novas tarefas.

Contrato proposto:
- Entradas: Casos de desenvolvimento, métrica, componente editável, orçamento e avaliação final reservada.
- Saídas: Nova versão do componente com diferenças e evidência independente.
- Estado: Histórico de experimentos, dados vistos e critérios de seleção.
- Invariante: Toda alegação de melhoria aponta para a alteração concreta que será reutilizada em execuções futuras.

Compromissos de projeto:
- Mais buscas de configuração ampliam oportunidades e risco de sobreajuste.
- Métricas baratas aceleram iteração e podem perder aspectos relevantes do objetivo.

## T199:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar um atalho que reconhece exemplos de desenvolvimento sem resolver variantes novas. Esperar ganho local e reprovação na avaliação independente, expondo o sobreajuste.

Plano de avaliação proposto:
Plano proposto: comparar versão inicial e selecionada em casos inéditos agrupados por origem. Medir qualidade, custo e regressões; reportar número de tentativas e mudanças avaliadas, aceitando ganhos somente fora do processo de seleção.

Comparações:
- T177 (distinct_from): A melhoria pode otimizar prompts ou exemplos sem atualizar pesos; fine-tuning é somente um mecanismo possível.

Afirmação rastreável:
DSPy descreve módulos parametrizados e otimização de pipelines para uma métrica especificada.
Suporte: direct; fontes: C-S020
Limite: A métrica escolhida não garante representar integralmente o objetivo de negócio ou correção factual.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T199:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu alteração persistente e teste reservado. Esta camada organiza o ciclo como experimentação causal, com seleção de falhas, prevenção de regressão e controle da dívida criada por ajustes sucessivos.

Uma mudança identificável
Associe cada hipótese a um componente: prompt, exemplo, índice, roteador, procedimento ou pesos. Registre diferença e critério esperado antes de testar. Alterar vários componentes simultaneamente pode melhorar a métrica sem explicar causa, dificultando manutenção e reversão quando a distribuição muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

Falhas representativas
Priorize erros por impacto e frequência, mas inclua classes raras relevantes. Transformar cada falha observada num exemplo quase idêntico pode produzir memorização de incidentes. Gere variações legítimas e teste em novas origens; preserve uma lista de problemas ainda não resolvidos em vez de remover casos difíceis da suíte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

Aprender não é só filtrar
Executar testes e rejeitar candidatos melhora a saída daquela execução; aprendizagem exige reutilizar uma mudança depois. AlphaEvolve mantém uma busca com avaliações e histórico, enquanto testes industriais podem apenas selecionar propostas. Descreva exatamente qual estado persiste antes de chamar o sistema de autoaperfeiçoamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

USO AVANÇADO — Melhorar extração recorrente
Cenário: Uma versão erra categorias específicas de documento.
Estratégia: Agrupe falhas, escolha uma intervenção pequena e compare com controle. Atualize exemplos ou recuperação quando a causa estiver neles, evitando fine-tuning automático para todo erro.
Papel do modelo pequeno: Um 3–7B pode ganhar utilidade especializada por melhoria do sistema ao redor dele.
Aceite proposto: Avaliar casos novos, regressões e custo por resultado correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

USO AVANÇADO — Evoluir procedimento de agente
Cenário: Execuções mostram uma sequência de ações desnecessária.
Estratégia: Crie uma nova skill ou política, valide pré-condições e compare em replay ou ambiente de teste. Promova somente a versão que mantém resultados e reduz custo observado.
Papel do modelo pequeno: Um 8–14B pode executar o procedimento melhorado sem precisar atualizar pesos.
Aceite proposto: Comprovar alteração persistente e ganho em tarefas fora das trajetórias usadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S020, V4B-S022, V4B-S023, V4B-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Melhorias de dados, ferramentas e contratos podem superar mudanças de pesos no início.
8–14B: Use um histórico de experimentos para evitar ciclos de correções contraditórias.
15–30B: Em 15–30B, custo de treino torna diagnóstico causal ainda mais importante.
Requisitos de treino/runtime: Pode modificar runtime, conteúdo ou pesos; declare qual componente mudou e como foi promovido.
Não aplicar quando: Não contar avaliação repetida como aprendizagem nem usar o teste final como guia contínuo de desenvolvimento.

## T199:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4B-C021 — Meta / TestGen-LLM
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Os autores relatam test-a-thons e integração de testes gerados aceitos por engenheiros. A classificação se apoia nessa descrição explícita de uso, não no fato de existir um paper.
Mecanismo documentado: Geração de testes a partir de código e suítes existentes, seguida de filtros de compilação, execução confiável e aumento de cobertura.
Correspondência com esta base: Avaliação orienta seleção ou revisão de candidatos; isso não prova aprendizagem persistente do modelo por essa avaliação.
Transferência proposta para modelo pequeno: Proposta: um 3–30B especializado pode propor testes pequenos, aproveitando compilador e suíte como verificadores externos.
Limite: Uso industrial delimitado, com avaliação humana. Cobertura de linhas não equivale a correção semântica; resultados publicados não são uma previsão para o repositório do usuário.
Fontes: V4B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T199:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T199 → T177 [feeds]
Como combinar: Falhas verificadas podem alimentar um próximo ajuste quando a causa é comportamento aprendível.
Interface: Exemplos revisados e categoria de erro.
Condição: Separação entre dados de desenvolvimento e avaliação.
Aceite proposto: Medir generalização após o ajuste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S020, V4B-S022, V4B-S023, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T199 → T204 [feeds]
Como combinar: Procedimentos bem-sucedidos podem ser consolidados em skills versionadas.
Interface: Pré-condições, passos e evidência de resultado.
Condição: Generalização preserva parâmetros variáveis.
Aceite proposto: Reexecutar em situações novas e manter rollback.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S020, V4B-S022, V4B-S023, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não remover casos difíceis para melhorar o número agregado.
- Registrar mudanças rejeitadas e seus efeitos, evitando redescobrir regressões.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare versões da aplicação e um baseline de fronteira em tarefas novas. Um ciclo de melhoria pode reduzir lacunas específicas, sem estabelecer crescimento ilimitado ou inteligência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T071, T177, T190

## Fontes primárias associadas

### C-S051 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback verbal e memória episódica podem melhorar tentativas posteriores sem atualizar pesos.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S020 — DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines

[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Otimização de pipelines de chamadas de LLM com objetivo mensurável.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T200 — Independent Verification

**Nome canônico:** Independent Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T200  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** verificação independente

## T200:C01 — conceito

Verificação feita por processo que reduz dependência dos mesmos pressupostos, fontes ou artefatos usados pelo gerador. Independência é uma propriedade do desenho, não do nome auditor. Um segundo agente com o mesmo contexto e modelo pode reproduzir exatamente o primeiro erro.

Como funciona:
- Extrair requisitos e artefatos finais sem depender apenas da justificativa do autor.
- Construir checagens com evidências ou métodos distintos quando possível.
- Relatar achados, escopo e limites sem transformar ausência de achado em prova absoluta.

## T200:C02 — aplicacao

Quando usar:
- Entrega de código, relatório ou integração precisa de validação adicional.
- Custo de erro justifica revisão separada.

Quando não usar:
- Revisor apenas confirma a narrativa do gerador sem inspecionar o resultado.

Implementação proposta:
- Separar autoria e revisão de testes críticos.
- Dar ao verificador acesso às fontes originais e critérios de aceite.
- Registrar o que foi efetivamente checado e quais áreas ficaram sem cobertura.

Aplicação LAI proposta:
Proposta: especialista consultivo revisar evidências da Helena com autonomia de método, enquanto decisão e execução permanecem explicitamente coordenadas.

## T200:C03 — riscos_validacao

Armadilhas:
- Modelos distintos ainda podem compartilhar a mesma fonte errada.
- Revisão com pouco contexto pode perder requisito relevante.

Métricas sugeridas:
- Defeitos encontrados que o autor não detectou.
- Falsos achados e cobertura dos critérios de aceite.

Testes propostos:
- Introduzir erro plausível com justificativa convincente e verificar detecção.
- Fornecer artefato que contradiz o resumo do autor e exigir preferência pela evidência.

## T200:C04 — perguntas_proveniencia

Pergunta: Outro agente basta para ser independente?
Resposta: Não. Precisa avaliar compartilhamento de modelo, dados, contexto e critérios.

Pergunta: Verificação independente é infalível?
Resposta: Não. Seu alcance deve ser descrito e medido.

Pergunta: Outro agente já é auditor independente?
Resposta: Não necessariamente. Verifique o que ele recebeu, quais fontes usa e como decide.

Pergunta: Um verificador formal resolve tudo?
Resposta: Pode provar propriedades de uma formalização sob hipóteses; a correspondência entre essa formalização e a necessidade real ainda precisa ser examinada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T200:C05 — mecanismo_avancado

Independência possui eixos diferentes: fonte, método, implementação e informação disponível. Um verificador de outra marca pode reutilizar a mesma fonte errada; dois programas podem compartilhar a mesma biblioteca defeituosa. Como proposta, derive casos da especificação, mantenha checagem cega quando possível e use métodos complementares. Divergência precisa de adjudicação por evidência, em vez de ser resolvida automaticamente pela confiança verbal.

Condição de contorno:
Uma checagem independente pode discordar por interpretar outro requisito; alinhar a especificação continua necessário.

Contrato proposto:
- Entradas: Artefato, especificação, evidências de origem e métodos de checagem com dependências registradas.
- Saídas: Veredito limitado aos critérios examinados e divergências documentadas.
- Estado: Mapa de fontes e componentes compartilhados entre gerador e verificador.
- Invariante: O verificador não recebe a conclusão esperada como substituto da evidência que deveria examinar.

Compromissos de projeto:
- Diversidade de métodos reduz alguns erros comuns e aumenta custo.
- Checagem cega reduz ancoragem e pode exigir explicitar melhor o contexto necessário.

## T200:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer a ambos a mesma fonte adulterada e depois incluir uma fonte independente ou teste derivado da especificação. Esperar identificação de que concordância inicial não demonstrava validade.

Plano de avaliação proposto:
Plano proposto: medir detecção de defeitos conhecidos, falsos alarmes e correlação de erros entre verificadores. Comparar métodos com orçamento declarado; aceitar independência pela redução observada de falhas compartilhadas, não pelo número de agentes.

Comparações:
- T191 (complements): Fatorar perguntas reduz contaminação contextual, enquanto diversificar fontes e métodos aborda dependências adicionais.

Afirmação rastreável:
O estudo de autocorreção intrínseca observou limitações e regressões quando modelos tentavam corrigir raciocínio sem feedback externo.
Suporte: direct; fontes: V3B-S019
Limite: Esse resultado empírico não prova incapacidade universal; sustenta a necessidade de avaliar dependências e fontes de feedback.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T200:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu eixos de independência. Esta camada define uma matriz de evidências, resolução de conflitos e testes que verificam se o revisor é sensível ao erro sem depender da conclusão do gerador.

Dependências compartilhadas
Mapeie modelo, fonte, código, biblioteca e dados usados pelo gerador e pelo verificador. Independência numa dimensão pode coexistir com dependência em outra. Dois revisores que consultam a mesma tabela errada não oferecem duas evidências independentes sobre o fato; um compilador pode verificar sintaxe sem verificar a intenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

Checagem cega quando útil
Forneça especificação e artefato, evitando apresentar a aprovação anterior como resultado esperado. Em tarefas factuais, peça busca da evidência original; em código, derive testes do contrato. Compare resultados com e sem a narrativa do gerador para medir ancoragem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

Conflito e alcance
Quando métodos discordam, examine contraexemplos e premissas antes de votar. O veredito deve indicar critérios cobertos e pendentes. AutoClean descreve revisores por propriedade antes da revisão humana; isso é um desenho operacional delimitado, não uma garantia de independência total nem ausência de erro compartilhado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

USO AVANÇADO — Revisar alteração de código
Cenário: O gerador declara que a mudança está pronta.
Estratégia: Execute testes derivados do contrato e revise efeitos laterais em uma etapa separada. Preserve artefato e evidências para que o humano examine divergências reais.
Papel do modelo pequeno: Um 3–7B pode gerar ou revisar partes estreitas; ferramentas decidem propriedades executáveis.
Aceite proposto: Detectar defeitos deliberados sem depender do texto de autoavaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

USO AVANÇADO — Resposta com política e fatos
Cenário: Uma explicação combina regras e dados externos.
Estratégia: Use verificador formal para a política e fontes para os fatos. Não deixe a aprovação de uma camada legitimar alegações que ela não examinou.
Papel do modelo pequeno: Um 8–14B pode redigir a resposta e organizar evidências com limites explícitos.
Aceite proposto: Cada afirmação relevante deve ter suporte apropriado ao seu tipo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S019, C-S048, V4C-S009, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Dividir trabalho por critérios verificáveis é mais concreto que pedir ao mesmo modelo para 'ser crítico'.
8–14B: Modelos intermediários podem revisar contexto maior, mas dependências precisam continuar visíveis.
15–30B: Um 15–30B como juiz não substitui referência independente nem garante resistência a persuasão.
Requisitos de treino/runtime: Arquitetura de verificação em runtime; independência é propriedade das evidências e métodos, não do nome do agente.
Não aplicar quando: Não tratar consenso entre revisores ou troca de marca de modelo como prova automática de independência.

## T200:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: CodeCourt separa propriedades de aceitação do agente que fez a limpeza.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

V4B-C020 — Meta / ACH — Automated Compliance Hardening
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A Meta relata aplicação em Facebook Feed, Instagram, Messenger e WhatsApp e descreve um ensaio industrial delimitado, com revisão por engenheiros.
Mecanismo documentado: LLMs produzem mutações que representam comportamentos indesejados e testes capazes de detectar essas mudanças; compilação, execução e revisão restringem os candidatos.
Correspondência com esta base: A detecção exige evidência específica, mas o oráculo continua limitado ao comportamento modelado.
Transferência proposta para modelo pequeno: Proposta: para modelos pequenos, restringir mutações a uma classe de risco e exigir que o teste passe no original e falhe no mutante correspondente.
Limite: Ensaio industrial não significa implantação irrestrita em todo código. Matar um mutante não demonstra ausência de outros defeitos nem equivalência a modelos maiores.
Fontes: V4B-S024, V4B-S025.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Validação separada da geração e revisão humana fornecem sinais adicionais, sem independência estatística demonstrada.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4B-C022 — Amazon Web Services / Bedrock Automated Reasoning checks
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação descreve uma funcionalidade disponível de verificação por raciocínio automatizado para respostas em linguagem natural vinculadas a políticas.
Mecanismo documentado: Políticas são expressas formalmente e a tradução de texto para afirmações é analisada. O recurso é de detecção e possui restrições de idioma e resposta completa.
Correspondência com esta base: A aceitação é sustentada por um verificador externo dentro do escopo da política.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para redigir respostas e um verificador externo para políticas formalizáveis, encaminhando traduções ambíguas para revisão.
Limite: Disponibilidade não comprova adoção específica. Validade em uma política não garante verdade externa, atualização dos fatos ou correção da tradução de linguagem natural.
Fontes: V4B-S027.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Estudo humano confronta os julgamentos, mas não demonstra independência causal de todo erro.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q019.

## T200:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T200 → T190 [complements]
Como combinar: AutoClean usa avaliações por propriedade para controlar o fluxo de correção e revisão.
Interface: Artefato e relatórios de critérios.
Condição: Critérios ligados à revisão exata.
Aceite proposto: Medir falhas e discordâncias antes da liberação.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T200 → T195 [complements]
Como combinar: Execução oferece um método diferente de julgamento textual.
Interface: Contrato, testes e ambiente.
Condição: Oráculo não replica cegamente o erro do gerador.
Aceite proposto: Usar casos adversos e mutações conhecidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S019, C-S048, V4C-S009, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não fornecer a conclusão desejada como parte do critério de avaliação.
- Registrar lacunas de cobertura mesmo quando todos os critérios executados passam.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Verificação independente pode tornar uma solução pequena mais confiável em propriedades observáveis. A comparação com fronteira deve considerar falhas não cobertas e custo de toda a checagem.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T169, T186, T190, T195

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S044 — Chain-of-Verification Reduces Hallucination in Large Language Models

[https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rascunho, perguntas de checagem, respostas independentes e revisão final compõem CoVe.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T201 — Agent Test-Time Scaling

**Nome canônico:** Agent Test-Time Scaling  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T201  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalada de computação em execução de agentes

## T201:C01 — conceito

Aumento de recursos durante a execução de um agente: mais candidatos, ferramentas, buscas, verificações ou especialistas. Diferencia-se de ampliar o treinamento. O ganho depende da qualidade das ações extras e do mecanismo de seleção; repetir a mesma falha não cria capacidade nova.

Como funciona:
- Identificar gargalo observável da tentativa inicial.
- Alocar recurso adicional à busca, geração ou verificação que possa resolvê-lo.
- Selecionar resultado e parar quando benefício adicional não justificar custo.

## T201:C02 — aplicacao

Quando usar:
- Tarefas difíceis e verificáveis que respondem a tentativas alternativas.
- Há evidências de que orçamento extra melhora a taxa de sucesso.

Quando não usar:
- Usar mais agentes ou tokens como substituto de ferramenta ausente ou requisito impossível.

Implementação proposta:
- Definir orçamento total, incluindo coordenação e verificações.
- Comparar escalada serial, paralela e recuperação adicional.
- Medir curvas de resultado versus custo em vez de apenas o melhor exemplo.

Aplicação LAI proposta:
Proposta: a Helena aumentar esforço onde testes indicarem retorno, preservando limites e evidências de que a computação extra ajudou.

## T201:C03 — riscos_validacao

Armadilhas:
- Verificador fraco pode escolher a pior de muitas soluções.
- Latência e custo podem crescer mais rápido que a qualidade.

Métricas sugeridas:
- Sucesso por orçamento e tempo até resultado aceito.
- Ganho marginal e proporção de tentativas redundantes.

Testes propostos:
- Comparar políticas sob o mesmo custo total.
- Aplicar tarefas sem resposta disponível e verificar abstenção em vez de geração infinita.

## T201:C04 — perguntas_proveniencia

Pergunta: Mais tempo transforma modelo pequeno em modelo de fronteira?
Resposta: Não há equivalência garantida; algumas capacidades podem continuar ausentes.

Pergunta: É a mesma coisa que treinar por mais épocas?
Resposta: Não. O recurso é gasto durante execução da tarefa.

Pergunta: Mais tokens é igual a mais computação útil?
Resposta: Não. Podem ser redundantes ou produzir candidatos que o verificador não sabe distinguir.

Pergunta: Como decidir parar?
Resposta: Use orçamento e evidência de progresso mensurável; satisfação verbal do agente não basta como critério de utilidade marginal.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T201:C05 — mecanismo_avancado

O orçamento extra pode ser investido em largura, como candidatos paralelos, ou profundidade, como revisões sequenciais. Essas escolhas têm latências diferentes mesmo com número parecido de tokens. A utilidade marginal depende da dificuldade e do verificador: se falta uma informação externa, mais tentativas sem buscá-la podem repetir a mesma falha. Uma política adaptativa precisa estimar quando o próximo passo provavelmente acrescentará evidência ou capacidade.

Condição de contorno:
Aumento de computação não garante melhoria monótona, sobretudo quando seleção e feedback são imperfeitos.

Contrato proposto:
- Entradas: Tarefa, orçamento de tokens/tempo/chamadas, ações adicionais e sinais de progresso.
- Saídas: Resultado selecionado ou abstenção com custo e razão de parada.
- Estado: Candidatos, evidências, avaliações e orçamento restante.
- Invariante: O sistema contabiliza custo de geração, ferramentas e verificação, sem esconder trabalho descartado.

Compromissos de projeto:
- Paralelismo reduz tempo de parede e aumenta recursos simultâneos.
- Revisão sequencial usa feedback intermediário e impõe dependências de latência.

## T201:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer tarefa sem dado indispensável e permitir muitas tentativas internas. Esperar que a política busque o dado ou declare a lacuna, em vez de contar repetição como progresso.

Plano de avaliação proposto:
Plano proposto: comparar resposta única, amostragem paralela, revisão e busca com orçamento equivalente. Estratificar dificuldade; medir qualidade externa, latência e custo total. Aprovar a política pela curva de benefício marginal e pelos prazos de uso.

Comparações:
- T189 (complements): Best-of-N é uma alocação possível do orçamento adicional, dependente da qualidade do seletor.

Afirmação rastreável:
O estudo de test-time compute encontra dependência da estratégia eficiente em relação à dificuldade do prompt.
Suporte: direct; fontes: V3B-S020
Limite: Os resultados não definem política ótima universal para agentes, ferramentas ou cargas do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T201:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou largura, profundidade e custo de ferramentas. Esta camada propõe alocação marginal de orçamento, controle de caminhos improdutivos e comparação entre busca e obtenção de nova informação.

Valor da próxima ação
Decida entre gerar outro candidato, revisar, executar teste ou buscar evidência conforme a falha atual. Se todos os candidatos usam a mesma premissa falsa, mais geração tem pouco valor. Uma política proposta estima benefício esperado e custo, mas precisa ser validada; a estimativa do próprio modelo não é uma probabilidade confiável por definição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

Portfólio de busca
Combine algumas alternativas independentes com refinamento dos candidatos promissores, preservando diversidade relevante. AlphaEvolve usa busca evolutiva com avaliadores, em um domínio executável. A transferência para um agente pequeno exige oráculos e representações adequados, sem transportar automaticamente os resultados da infraestrutura Google.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

Custo e parada
Inclua tokens, ferramentas, filas e verificadores no orçamento. Pare por sucesso verificado, benefício marginal baixo ou limite explícito; não apenas quando o agente se declara satisfeito. Guarde a melhor solução válida e pendências, evitando que uma última tentativa pior destrua progresso anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

USO AVANÇADO — Otimização de função pequena
Cenário: Há desempenho mensurável e testes de correção.
Estratégia: Gere diversidade inicial, elimine incorretas e refine soluções válidas. Use entradas reservadas para evitar explorar particularidades do benchmark de desenvolvimento.
Papel do modelo pequeno: Um 8–14B pode explorar um espaço local com avaliações baratas.
Aceite proposto: Melhora reproduzível em entradas novas e custo total de busca conhecido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

USO AVANÇADO — Tarefa de pesquisa delimitada
Cenário: Uma resposta depende de poucas evidências ainda ausentes.
Estratégia: Invista chamadas em localizar e confrontar fontes antes de aumentar amostras de redação. Reavalie necessidade de refinamento quando a informação estiver completa.
Papel do modelo pequeno: Um 3–7B pode organizar trabalho e síntese curta com recuperação confiável.
Aceite proposto: Cobertura factual e tempo até resposta sustentada, não número de pensamentos produzidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Computação adicional ajuda quando o modelo já produz candidatos úteis ou consegue usar ferramentas.
8–14B: Aumente orçamento por dificuldade observada e capacidade do verificador.
15–30B: Compare custo de várias tentativas 15–30B com uma chamada mais forte, incluindo latência serial.
Requisitos de treino/runtime: Orquestração em inferência; pode usar modelos fixos. Treinamento para aproveitar orçamento é outra intervenção.
Não aplicar quando: Não assumir que dobrar tokens duplica qualidade nem chamar repetição sem evidência de raciocínio superior.

## T201:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Há busca entre candidatos, mas não é simplesmente best-of-N independente.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4D-C005 — DeepSeek-AI / DeepSeek-R1-Distill 7B/8B/14B
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores disponibilizam modelos menores afinados com amostras do professor e publicam avaliações.
Mecanismo documentado: SFT/destilação de respostas de um modelo maior para modelos densos menores.
Correspondência com esta base: Avaliação inclui diferentes regimes de amostragem; não prova política ótima de compute adaptativo em produção.
Transferência proposta para modelo pequeno: Proposta: selecionar tarefas verificáveis, filtrar demonstrações por teste externo, isolar famílias entre treino/teste e comparar custo total incluindo o professor.
Limite: Pesquisa, não produção. Comparadores são versões históricas; 32B/70B não pertencem à faixa solicitada. Mais amostras têm custo e consenso não elimina erros correlacionados.
Fontes: V4D-S008, V4D-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T201:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T201 → T189 [complements]
Como combinar: Best-of-N investe orçamento em alternativas selecionadas por verificação.
Interface: Candidatos e custos marginais.
Condição: Verificador distingue qualidade real.
Aceite proposto: Comparar largura com profundidade em orçamento equivalente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S020, V4B-S022, V4B-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T201 → T202 [complements]
Como combinar: Planejamento por incerteza decide quando observar em vez de gerar.
Interface: Lacunas e ações de aquisição de informação.
Condição: Observações são acessíveis e relevantes.
Aceite proposto: Medir redução de erro por ação adicional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S020, V4B-S022, V4B-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cobrar no custo tentativas descartadas e verificações inconclusivas.
- Não ajustar a política de busca sobre os casos finais de avaliação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie curvas de sucesso versus custo e prazo. Em tarefas verificáveis, busca pode reduzir uma lacuna específica; fora delas, mais computação pode apenas ampliar erro e custo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T145, T146, T169, T189

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T202 — Uncertainty-Aware Planning

**Nome canônico:** Uncertainty-Aware Planning  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T202  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** planejamento com incerteza

## T202:C01 — conceito

Planejamento que representa explicitamente o que é conhecido, estimado e desconhecido e considera a utilidade de obter informação antes de agir. A incerteza pode estar na entrada, nas ferramentas ou na chance de sucesso. Não deve ser reduzida a um número arbitrário declarado pelo modelo.

Como funciona:
- Mapear premissas e consequências das alternativas.
- Identificar qual observação reduziria incerteza relevante à decisão.
- Escolher entre agir, investigar, escalar ou encerrar conforme custo e viabilidade.

## T202:C02 — aplicacao

Quando usar:
- Há informação incompleta que pode mudar a escolha de ação.
- Ferramentas têm confiabilidade ou disponibilidade variáveis.

Quando não usar:
- Adicionar checagens sem relação com decisão material ou com custo maior que seu benefício esperado.

Implementação proposta:
- Distinguir falta de dado, ambiguidade e falha de capacidade.
- Usar estimativas calibradas quando houver dados e faixas explícitas nos demais casos.
- Atualizar plano após observação, preservando hipóteses descartadas com motivo.

Aplicação LAI proposta:
Proposta: a Helena consultar versão, evidência ou estado real antes de ações cuja escolha depende desses dados, evitando escalar apenas por linguagem insegura.

## T202:C03 — riscos_validacao

Armadilhas:
- Probabilidade inventada cria falsa precisão.
- Planejador pode investigar indefinidamente sem uma regra de término.

Métricas sugeridas:
- Decisões corrigidas por informação adicional.
- Custo de investigação e taxa de ações inviáveis evitadas.

Testes propostos:
- Criar cenário em que uma consulta muda a ação ótima e verificar sua escolha.
- Criar informação irrelevante e conferir que o agente não gasta recursos desnecessários.

## T202:C04 — perguntas_proveniencia

Pergunta: Planejar com incerteza exige probabilidades exatas?
Resposta: Não. Pode usar intervalos e estados de desconhecimento explícitos.

Pergunta: SayCan prova isso para software?
Resposta: Não. A transferência do princípio de viabilidade para ferramentas é proposta de engenharia.

Pergunta: Uma probabilidade por ação basta para o plano?
Resposta: Não se ações compartilham falhas ou mudam o estado; dependências precisam entrar na avaliação.

Pergunta: Quando perguntar ao usuário?
Resposta: Quando a informação ausente depende de sua intenção e altera materialmente a escolha; outras lacunas podem ser resolvidas por observação autorizada.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T202:C05 — mecanismo_avancado

A incerteza pode estar na interpretação do objetivo, no estado do ambiente ou no resultado da ação. Cada fonte pede uma resposta diferente: esclarecer objetivo, observar o ambiente ou testar uma ação reversível. Um plano deve distinguir utilidade para a tarefa de viabilidade operacional. Combinar scores sem calibração ou hipóteses claras produz um ranking, não necessariamente uma probabilidade válida de sucesso do plano inteiro.

Condição de contorno:
Uma ação pode ser linguisticamente plausível e impossível no estado atual, mesmo quando descrita com alta confiança.

Contrato proposto:
- Entradas: Objetivo, observações, ações disponíveis, estimativas e custos de adquirir informação.
- Saídas: Próxima ação ou observação com justificativa baseada na lacuna relevante.
- Estado: Crenças, pré-condições verificadas e origem de cada estimativa.
- Invariante: O plano não trata uma hipótese desconhecida como pré-condição satisfeita.

Compromissos de projeto:
- Observar antes reduz alguns erros e consome tempo ou recursos.
- Planos conservadores podem ser confiáveis e deixar de explorar alternativas úteis.

## T202:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer uma ferramenta mencionada na documentação, mas indisponível na sessão, e outra disponível com efeito incerto. Esperar distinção entre falta de acesso e incerteza sobre resultado.

Plano de avaliação proposto:
Plano proposto: comparar planejamento direto e planejamento com aquisição de informação em ambientes controlados. Medir sucesso, ações inválidas, custo de observação e arrependimento frente às opções disponíveis; definir política conforme consequências e reversibilidade.

Comparações:
- T198 (complements): Calibração ajuda quando existe evento de sucesso bem definido, mas não substitui representar estados desconhecidos.

Afirmação rastreável:
SayCan combina conhecimento procedural de linguagem com funções de valor associadas a habilidades no ambiente físico.
Suporte: related; fontes: C-S053
Limite: A fonte apoia distinguir utilidade e viabilidade; o contrato geral de incerteza desta ficha é proposta editorial.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T202:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou fontes de incerteza. O aprofundamento transforma essa distinção em ações de observação, atualizações de plano e critérios para evitar que confiança verbal substitua pré-condições.

Lacuna localizada
Registre qual variável falta e qual decisão depende dela. Incerteza sobre identidade pede consulta ou confirmação; sobre estado pede observação; sobre efeito pode pedir teste reversível. Uma nota global de confiança não informa qual ação reduz o risco nem se a tarefa pode prosseguir parcialmente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

Valor de informação
Compare custo de observar com impacto de decidir errado. Nem toda busca adicional é útil: a fonte pode repetir informação já conhecida ou não resolver a ambiguidade relevante. Uma política proposta só solicita observação quando ela pode alterar a decisão ou confirmar uma pré-condição importante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

Atualização coerente
Depois de receber evidência, revise premissas e ações dependentes, preservando o que permanece válido. Se observações se contradizem, mantenha o estado como incerto até adjudicar fonte e tempo. Não multiplique scores de linguagem e viabilidade como probabilidades do plano inteiro sem hipóteses e calibração apropriadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

USO AVANÇADO — Agente de operação
Cenário: Uma ação depende do estado atual de um recurso.
Estratégia: Consulte o recurso, confirme versão e pré-condição, e planeje a ação sobre essa observação. Se houver mudança concorrente, reavalie antes de executar.
Papel do modelo pequeno: Um 3–7B pode seguir um fluxo estreito quando a API fornece estado verificável.
Aceite proposto: Nenhuma pré-condição desconhecida tratada como satisfeita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

USO AVANÇADO — Pesquisa com entidades ambíguas
Cenário: A consulta pode se referir a produtos ou versões diferentes.
Estratégia: Faça uma busca discriminante ou solicite o detalhe mínimo necessário. Evite redigir uma resposta longa sobre uma entidade escolhida por suposição.
Papel do modelo pequeno: Um 8–14B pode comparar hipóteses e selecionar a observação mais informativa.
Aceite proposto: Resolver ambiguidade com menos chamadas e manter proveniência da escolha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S053, C-S050, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Planos curtos com estados explícitos são mais adequados que estimativas abstratas de confiança.
8–14B: Use ferramentas para observar variáveis, preservando limites quando a evidência não existe.
15–30B: Maior porte pode explorar hipóteses complexas, mas não torna observações desatualizadas válidas.
Requisitos de treino/runtime: Runtime de planejamento com fontes e estado; probabilidades exigem avaliação empírica quando usadas numericamente.
Não aplicar quando: Não interpretar confiança alta como permissão para ignorar uma condição externa não observada.

## T202:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019, V4B-Q024.

## T202:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T202 → T198 [feeds]
Como combinar: Calibração permite interpretar sinais usados para decidir observar ou encaminhar.
Interface: Evento de sucesso e score validado.
Condição: Distribuição compatível com a decisão.
Aceite proposto: Comparar erro e cobertura após a política.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S053, C-S050, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T202 → T203 [complements]
Como combinar: Roteamento pode escolher executor ou busca adicional conforme a lacuna.
Interface: Tipo de incerteza, elegibilidade e custo.
Condição: Encaminhar realmente oferece capacidade ou informação nova.
Aceite proposto: Medir resolução de falhas, não apenas troca de modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S053, C-S050, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não repetir buscas que não podem mudar a decisão.
- Registrar hipóteses revogadas para evitar que retornem silenciosamente ao plano.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare decisões corretas e custo de observação com fronteira sob o mesmo acesso ao ambiente. Planejamento explícito ajuda a administrar limites; não cria informação inexistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T143, T198, T203

## Fontes primárias associadas

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S053 — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

[https://arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Planejamento pode combinar adequação linguística com estimativas de viabilidade das habilidades.

Limite: Fonte primária sobre robótica; aplicação a ferramentas de software é uma analogia de engenharia, não resultado demonstrado pelo artigo.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T203 — Correctness-Based Routing

**Nome canônico:** Correctness-Based Routing  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T203  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** roteamento por correção

## T203:C01 — conceito

Roteamento orientado à chance de cumprir um critério de correção da tarefa, e não somente ao custo, tamanho ou tema do pedido. Pode usar resultados de verificadores após tentativa ou previsões calibradas antes dela. É uma especialização de política de roteamento, sem algoritmo universal associado ao nome.

Como funciona:
- Definir o que conta como resultado correto para a tarefa.
- Estimar capacidade por modelo usando avaliações e sinais disponíveis.
- Escolher destino ou escalar quando a verificação rejeitar a resposta.

## T203:C02 — aplicacao

Quando usar:
- Critérios de qualidade podem ser medidos por domínio.
- Modelos apresentam competências distintas, não apenas preços diferentes.

Quando não usar:
- Usar autoconfiança verbal como única evidência de que a resposta está correta.

Implementação proposta:
- Construir matriz modelo × tarefa com resultados observados.
- Incluir abstenção e custo de verificações na política.
- Reavaliar rotas após mudança de modelo, prompt ou ferramentas.

Aplicação LAI proposta:
Proposta: a Helena selecionar modelos por evidência de competência na subtarefa, usando nomes comerciais apenas como identificação do backend.

## T203:C03 — riscos_validacao

Armadilhas:
- Preferência humana por estilo pode não representar correção factual.
- Dados antigos podem estimar mal a capacidade da versão atual.

Métricas sugeridas:
- Taxa de resultado correto por rota.
- Custo por tarefa aceita e erro entre previsão de capacidade e resultado.

Testes propostos:
- Testar tarefas de igual tamanho, mas dificuldade e requisitos distintos.
- Apresentar resposta fluente incorreta e exigir escalada pelo critério de conteúdo.

## T203:C04 — perguntas_proveniencia

Pergunta: É melhor que roteamento por tamanho?
Resposta: Pode ser, se o sinal de correção for confiável; precisa de comparação.

Pergunta: RouteLLM mede exatamente toda correção?
Resposta: Não. A fonte usa sinais de preferência; a política proposta deve definir seus próprios critérios.

Pergunta: Pode chamar o maior modelo em todo caso difícil?
Resposta: É uma política possível, mas dificuldade prevista e capacidade real precisam ser medidas, incluindo erros do modelo maior.

Pergunta: Por que guardar o resultado depois do roteamento?
Resposta: Ele permite verificar calibração e detectar mudança de desempenho; guardar apenas a decisão impede avaliar se a escolha cumpriu o contrato.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T203:C05 — mecanismo_avancado

Para prever correção, o roteador precisa de um evento verificável, como passar um contrato ou resolver um caso com referência. Preferência humana entre respostas é outro alvo e pode valorizar estilo. Se dados registram somente o modelo escolhido anteriormente, faltam resultados contrafactuais dos demais, criando viés de seleção. Avaliação offline deve comparar candidatos em uma amostra apropriada ou declarar essa limitação.

Condição de contorno:
Um classificador de tema ou tamanho de prompt não estima automaticamente a chance de cada modelo cumprir a tarefa.

Contrato proposto:
- Entradas: Tarefa, executores elegíveis, custos e sinais calibrados contra um critério de correção.
- Saídas: Destino, regra de escalonamento e resultado verificado quando disponível.
- Estado: Histórico de decisões, versões dos modelos e dados de desempenho por domínio.
- Invariante: Preferência, confiança e correção observada permanecem métricas distintas.

Compromissos de projeto:
- Modelos menores podem resolver parte da carga e reduzir custo.
- Escalonar após falha adiciona latência e depende de detectar a falha corretamente.

## T203:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: construir respostas de estilo preferido, mas factualmente erradas, e alterar o modelo de destino sem recalibrar. Esperar identificação do desalinhamento entre proxy e critério real.

Plano de avaliação proposto:
Plano proposto: comparar roteamento fixo, por custo e por correção em tarefas novas. Medir acerto externo, custo, latência e erros de escalonamento por classe; validar novamente após troca de modelos ou distribuição.

Comparações:
- T184 (distinct_from): Seleciona executores de tarefas; MoE seleciona especialistas internos de uma rede.

Afirmação rastreável:
RouteLLM aprende roteadores a partir de preferências para equilibrar custo e qualidade entre modelos.
Suporte: related; fontes: C-S001
Limite: A fonte é relacionada: preferência não é rótulo universal de correção, e o nome desta ficha não designa algoritmo padronizado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T203:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou viés de seleção e definição de correção. Esta camada propõe roteamento como política versionada, com experimentos contrafactuais, custo de escalonamento e limites de elegibilidade antes da otimização.

Elegibilidade primeiro
Antes de estimar acerto, filtre executores por acesso, ferramentas, contexto, formato e prazo. Um modelo forte sem acesso à evidência necessária pode ser uma escolha pior que outro com ferramentas adequadas. Capacidade e autorização não devem ser comprimidas numa única nota de confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

Contrafactuais medidos
Numa amostra autorizada, execute candidatos sob condições equivalentes para estimar quais casos cada um resolve. Dados históricos do roteador anterior refletem suas escolhas e podem ocultar alternativas melhores. Registre custo de produzir essa amostra e mantenha avaliação final independente da política aprendida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

Escalonar tem custo
Uma tentativa pequena seguida de modelo maior soma fila, geração e verificação. Se o primeiro caminho raramente resolve uma classe, encaminhar diretamente pode ser mais econômico. Além disso, o modelo maior precisa receber evidências e falhas relevantes, sem herdar como verdade a resposta incorreta anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

USO AVANÇADO — Automação com modelo pequeno
Cenário: Grande parte dos pedidos é rotineira e verificável.
Estratégia: Use executor 3–7B nas classes validadas, aplique verificador e escale falhas com diagnóstico. Compare com encaminhamento direto para evitar dupla cobrança sem benefício.
Papel do modelo pequeno: O pequeno modelo assume a região de competência demonstrada, não todos os pedidos por padrão.
Aceite proposto: Medir correção, cobertura, custo e prazo por caminho completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

USO AVANÇADO — Escolha entre especialista e generalista
Cenário: Há modelos com capacidades complementares.
Estratégia: Colete resultados por domínio e evidência disponível, calibre a política e monitore deriva. Mantenha opção de buscar dados ou abster-se quando nenhum executor é adequado.
Papel do modelo pequeno: Um 8–14B especializado pode ser preferível em tarefas estreitas mesmo diante de modelo maior.
Aceite proposto: Comparar contrafactuais e evitar regressões em classes raras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S001, C-S050, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize contratos fechados com checagem barata para automatização seletiva.
8–14B: Especialização deve ser demonstrada com dados de resultado e não pelo nome do checkpoint.
15–30B: Um 15–30B pode ser destino intermediário; o número de etapas precisa justificar custo e latência.
Requisitos de treino/runtime: Runtime com política e sinais calibrados; treino do roteador é opcional. Preferência humana não é idêntica a correção.
Não aplicar quando: Não encaminhar indefinidamente para modelos maiores quando falta informação ou a tarefa é mal definida.

## T203:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T203:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T203 → T198 [requires]
Como combinar: A política usa sinais avaliados contra o evento de sucesso definido.
Interface: Scores, domínio e resultados observados.
Condição: Calibração válida para o caminho de implantação.
Aceite proposto: Medir erro e cobertura após seleção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S001, C-S050, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T203 → T195 [complements]
Como combinar: Execução pode confirmar resultado e decidir escalonamento em tarefas verificáveis.
Interface: Artefato, testes e falhas.
Condição: Oráculo cobre a propriedade relevante.
Aceite proposto: Comparar sucesso completo e custo de duas tentativas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S001, C-S050, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não treinar o roteador apenas com resultados dos destinos escolhidos historicamente sem declarar o viés.
- Preservar contexto e evidências ao escalar, sem validar automaticamente a resposta anterior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a política inteira com um baseline de fronteira, incluindo tentativas pequenas que falharam. A vantagem possível é custo em uma distribuição específica, sem promessa de equivalência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T135, T190, T198

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T204 — Skills / Procedural Learning

**Nome canônico:** Skills / Procedural Learning  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T204  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** habilidades procedurais; aprendizagem procedural

## T204:C01 — conceito

Skills são pacotes reutilizáveis de instruções, recursos e eventualmente scripts para um procedimento. Aprendizagem procedural é o processo de transformar experiências verificadas em procedimentos aplicáveis. Criar um arquivo de skill não altera pesos nem comprova que o agente executará corretamente o procedimento.

Como funciona:
- Extrair uma tarefa recorrente e suas condições de aplicação.
- Empacotar objetivo, entradas, passos, saídas e referências.
- Descobrir e carregar o procedimento quando a missão corresponder ao seu escopo.

## T204:C02 — aplicacao

Quando usar:
- Procedimentos repetidos com contratos relativamente estáveis.
- Especialidades que devem ser acessíveis sem carregar todo material de início.

Quando não usar:
- Generalizar uma experiência isolada sem considerar condições que permitiram seu sucesso.

Implementação proposta:
- Definir gatilhos e limites de uso em metadados claros.
- Separar instrução principal de referências volumosas.
- Versionar scripts e validar exemplos representativos antes de promover a skill.

Aplicação LAI proposta:
Proposta: converter episódios comprovados da Helena em procedimentos recuperáveis, preservando evidências e condições antes de pensar em destilação paramétrica.

## T204:C03 — riscos_validacao

Armadilhas:
- Skill desatualizada pode orientar chamadas incompatíveis.
- Catálogo com descrições vagas impede descoberta e aumenta seleção incorreta.

Métricas sugeridas:
- Acerto de seleção e conclusão correta do procedimento.
- Economia de contexto e regressões por versão de skill.

Testes propostos:
- Apresentar tarefas dentro e fora do escopo e verificar seleção.
- Atualizar uma dependência e exigir revalidação dos exemplos afetados.

## T204:C04 — perguntas_proveniencia

Pergunta: Criar skill significa treinar GPT?
Resposta: Não no sentido de atualizar pesos; fornece instruções e ferramentas reutilizáveis.

Pergunta: Skill substitui RAG?
Resposta: Pode usar RAG para recuperar referências e exemplos necessários ao procedimento.

Pergunta: Uma skill é memória paramétrica?
Resposta: Não. É um artefato externo consumido durante execução; aprendizado de pesos seria outro mecanismo.

Pergunta: Como evitar regras frágeis?
Resposta: Documente pré-condições e parâmetros, teste variantes relevantes e preserve evidência dos limites encontrados em vez de transformar um exemplo em regra universal.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T204:C05 — mecanismo_avancado

Uma skill executável precisa separar condições de aplicação, instruções centrais e recursos carregados sob demanda. Metadados ajudam a selecionar o procedimento, mas não demonstram que seus scripts, caminhos e dependências estão válidos. Aprender um procedimento a partir de uma execução exige generalizar somente o que se repete, deixando parâmetros variáveis explícitos. Copiar a trajetória inteira pode cristalizar atalhos ou suposições locais.

Condição de contorno:
Um procedimento que funcionou uma vez pode depender de estado, permissões ou versões ausentes em outra tarefa.

Contrato proposto:
- Entradas: Experiência verificada, objetivo recorrente, pré-condições e recursos necessários.
- Saídas: Pacote de procedimento versionado e critérios para ativar ou interromper sua execução.
- Estado: Instruções, scripts, referências, exemplos e histórico de alterações.
- Invariante: Recursos necessários são carregados e validados antes da etapa que deles depende.

Compromissos de projeto:
- Carregamento progressivo reduz contexto inicial e exige referências confiáveis.
- Procedimentos específicos facilitam execução e podem generalizar mal fora de suas condições.

## T204:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ativar a skill com dependência ausente e com caso semelhante, mas fora do domínio declarado. Esperar diagnóstico de pré-condição ou não aplicação, sem improvisar uma execução supostamente equivalente.

Plano de avaliação proposto:
Plano proposto: comparar execução sem skill e com skill em tarefas novas da mesma classe e em casos fora dela. Medir sucesso verificado, chamadas, contexto e ativações indevidas; aprovar somente reutilização que preserve condições e critérios.

Comparações:
- T199 (complements): Avaliações podem justificar atualização da skill, mas o pacote precisa mudar de fato para alterar comportamento futuro.

Afirmação rastreável:
A especificação Agent Skills define SKILL.md com metadados/instruções e carregamento progressivo de recursos conforme necessidade.
Suporte: direct; fontes: V3B-S021
Limite: O formato organiza conteúdo; não treina pesos nem comprova que o procedimento está correto ou autorizado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T204:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu pacote e pré-condições. A nova camada aborda descoberta de habilidades, invalidação de recursos e aprendizado procedural que mantém argumentos variáveis e evidência de execução.

Seleção por contrato
Descrições de skills devem distinguir objetivo, pré-condições e resultado esperado. Similaridade textual pode recuperar um procedimento inadequado porque compartilha vocabulário. Antes de executar, verifique ambiente, versão e permissões; carregar uma skill é uma decisão de planejamento, não prova de que ela se aplica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

Recursos sob demanda
Mantenha instruções centrais curtas e carregue scripts ou referências quando a etapa exige. Isso reduz competição por contexto, mas a execução precisa confirmar que o recurso existe e corresponde à versão descrita. Um link antigo ou script quebrado invalida a habilidade mesmo que o texto continue convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

Generalização de trajetória
Converta uma execução bem-sucedida em procedimento somente depois de separar constantes, parâmetros e contingências. Inclua caminhos de falha e critérios de interrupção. AMD oferece pesquisa sobre memória procedural hierárquica; transferir seu padrão para uma skill é proposta de engenharia, não implantação comprovada do pacote LAI.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

USO AVANÇADO — Rotina técnica repetida
Cenário: O agente precisa executar uma sequência conhecida com variações.
Estratégia: Empacote passos, argumentos e verificações; teste em múltiplas instâncias e preserve evidências. Deixe o modelo selecionar e preencher parâmetros, enquanto scripts fazem operações determinísticas.
Papel do modelo pequeno: Um 3–7B pode executar uma rotina estreita com menos improvisação.
Aceite proposto: Medir sucesso em casos novos e detectar pré-condições ausentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

USO AVANÇADO — Acervo de procedimentos crescente
Cenário: Muitas skills competem pela atenção do agente.
Estratégia: Organize metadados por tarefa e ambiente, avalie recuperação e rejeite candidatos incompatíveis. Carregue apenas o trecho necessário e registre qual versão orientou a ação.
Papel do modelo pequeno: Um 8–14B pode coordenar subtarefas sem inserir todo o acervo no prompt.
Aceite proposto: Avaliar seleção correta, recurso carregado e resultado final separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S021, C-S052, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Procedimentos curtos com scripts confiáveis reduzem exigência de planejamento aberto.
8–14B: Bibliotecas maiores exigem testes de seleção e conflitos entre skills.
15–30B: Um 15–30B pode compor rotinas, mas composição demanda novos testes de interfaces e estado.
Requisitos de treino/runtime: Memória procedural externa pode ser atualizada sem treinar pesos; aprendizagem paramétrica é outra rota.
Não aplicar quando: Não tratar uma trajetória copiada como procedimento universal nem texto da skill como prova de execução.

## T204:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: Memórias procedurais se relacionam a habilidades recuperáveis.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q023.

## T204:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T204 → T181 [complements]
Como combinar: Memórias hierárquicas podem informar criação e seleção de procedimentos.
Interface: Trajetória, pré-condições e resultados.
Condição: Generalização remove dados de sessão e preserva validade.
Aceite proposto: Testar aplicação em ambiente distinto e versão compatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S021, C-S052, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T204 → T206 [requires]
Como combinar: Verificação de processo confirma que etapas e recursos foram efetivamente usados.
Interface: Eventos, versão da skill e pós-condições.
Condição: Observabilidade cobre ações relevantes.
Aceite proposto: Comparar plano declarado com execução real.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S021, C-S052, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Suspender skills cujo recurso ou contrato mudou até revalidar.
- Não ocultar parâmetros variáveis em exemplos fixos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare execução de rotinas com fronteira usando as mesmas ferramentas. Uma biblioteca procedural pode ampliar utilidade especializada de um modelo pequeno, sem conferir compreensão geral de tarefas desconhecidas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T055, T071, T181

## Fontes primárias associadas

### C-S052 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills empacotam instruções e recursos carregados progressivamente.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S021 — Agent Skills Specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estrutura SKILL.md, metadados, recursos e carregamento progressivo.

Limite: Especificação de formato não prova correção do procedimento nem autorização universal de ferramentas.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T205 — Semantic Equivalence Testing

**Nome canônico:** Semantic Equivalence Testing  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T205  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** teste de equivalência semântica

## T205:C01 — conceito

Verificação de que duas representações preservam o comportamento ou significado relevante para uma tarefa. O critério depende do domínio: programas podem ser comparados por execução, objetos por regras normalizadas e textos por alegações preservadas. Similaridade de embeddings sozinha não prova equivalência.

Como funciona:
- Definir quais propriedades precisam permanecer iguais.
- Aplicar normalização admissível e comparação adequada ao domínio.
- Registrar divergências e limites da cobertura do teste.

## T205:C02 — aplicacao

Quando usar:
- Comparação entre versões de prompt, resumo, código ou schema.
- Validação de compactação de contexto e mudanças de formato.

Quando não usar:
- Declarar equivalência geral de programas arbitrários com base em poucos exemplos.

Implementação proposta:
- Construir casos positivos equivalentes e negativos próximos.
- Usar execução diferencial para código e checagem de alegações para textos.
- Separar diferenças cosméticas de mudanças com efeito observável.

Aplicação LAI proposta:
Proposta: avaliar se resumos e procedimentos da Helena preservam restrições, identificadores e condições essenciais antes de substituir versões anteriores.

## T205:C03 — riscos_validacao

Armadilhas:
- Paráfrase pode inverter negação ou prazo mantendo alta similaridade.
- Casos de teste finitos não cobrem todos os comportamentos possíveis.

Métricas sugeridas:
- Falsas equivalências e falsas divergências.
- Cobertura de propriedades e taxa de regressão detectada.

Testes propostos:
- Comparar frases que diferem apenas por negação e exigir rejeição.
- Testar programas com mesmo resultado comum, mas divergentes em condição de borda.

## T205:C04 — perguntas_proveniencia

Pergunta: Embeddings provam que dois textos dizem a mesma coisa?
Resposta: Não. Proximidade semântica pode esconder contradição.

Pergunta: Teste de equivalência prova todos os casos?
Resposta: Só se existir prova formal apropriada; testes comuns têm cobertura limitada.

Pergunta: Similaridade de embeddings prova equivalência textual?
Resposta: Não. Textos semanticamente próximos podem inverter uma condição, quantidade ou negação decisiva.

Pergunta: Round-trip perfeito prova um codec correto?
Resposta: Não sozinho. Encoder e decoder podem compartilhar o mesmo erro; compare também com especificação ou implementação independente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T205:C05 — mecanismo_avancado

Equivalência precisa declarar quais observáveis importam: valor retornado, efeitos laterais, exceções, ordem, precisão ou tempo. Duas funções podem devolver o mesmo resultado e modificar entradas de modo diferente. Comparação diferencial usa uma referência independente; propriedades metamórficas verificam relações entre entradas e saídas quando não existe resposta completa conhecida. A normalização deve preservar distinções relevantes, como unidades, ordem ou multiplicidade.

Condição de contorno:
Testes amostrais podem encontrar contraexemplos, mas ausência deles não prova equivalência para todo o domínio.

Contrato proposto:
- Entradas: Duas representações, domínio válido, observáveis e tolerâncias justificadas.
- Saídas: Contraexemplos reproduzíveis ou evidência limitada de equivalência nos casos examinados.
- Estado: Geradores de entradas, referências e regras de normalização.
- Invariante: Nenhuma diferença relevante é apagada pela normalização antes de ser avaliada.

Compromissos de projeto:
- Comparação estrita detecta diferenças e pode rejeitar variações aceitáveis.
- Tolerâncias amplas acomodam precisão finita e podem esconder erros significativos.

## T205:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar implementações iguais em listas sem duplicatas, mas diferentes quando há repetição, NaN ou mutação da entrada. Esperar contraexemplo no domínio realmente permitido.

Plano de avaliação proposto:
Plano proposto: combinar casos de fronteira, geração por propriedades e comparação diferencial. Medir defeitos detectados, reprodutibilidade e cobertura das classes de entrada; aceitar equivalência somente no escopo declarado, preservando casos descobertos para regressão.

Comparações:
- T195 (complements): Execução fornece observações para comparar comportamento entre versões, dentro do domínio declarado.

Afirmação rastreável:
A documentação Hypothesis apresenta testes por propriedades e comparação de implementação otimizada com referência, usando entradas geradas.
Suporte: direct; fontes: V3B-S022
Limite: O mecanismo explora entradas; uma prova geral exigiria argumento ou ferramenta formal compatível com a propriedade.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T205:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu observáveis e propriedades metamórficas. A nova camada considera domínio de equivalência, geração de contraexemplos e uso responsável de evidência empírica versus prova formal.

Domínio explícito
Declare entradas válidas, estados iniciais e tolerâncias. Duas implementações podem coincidir em números pequenos e divergir em overflow, Unicode, valores vazios ou concorrência. Excluir uma classe de entradas só é legítimo se o contrato também a exclui; não estreite o domínio depois de observar uma falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

Contraexemplo útil
Quando houver divergência, reduza a entrada preservando o defeito para facilitar correção. Mantenha sementes e ambiente para reprodução. Testes por propriedades e metamorfismo são úteis quando não existe uma resposta completa para cada entrada, mas a própria propriedade pode estar errada ou ser fraca.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

Força da evidência
Passar uma suíte finita oferece evidência limitada; prova formal tem alcance definido pelo modelo e premissas. AlphaEvolve relata verificação de funcionalidade em uma alteração de circuito, enquanto ACH usa mutações para testar detecção. Não use esses exemplos para declarar equivalência universal de qualquer patch gerado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

USO AVANÇADO — Refatoração automatizada
Cenário: Um modelo altera estrutura mantendo comportamento.
Estratégia: Defina retornos, efeitos, exceções e ordenação relevantes; compare com referência e adicione propriedades. Teste entradas de fronteira e mudanças concorrentes quando aplicáveis.
Papel do modelo pequeno: Um 3–7B pode propor refatorações locais, com aceitação externa.
Aceite proposto: Nenhuma divergência no domínio testado, com limites de cobertura registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

USO AVANÇADO — Normalização de respostas
Cenário: Várias representações podem expressar o mesmo resultado.
Estratégia: Use parser de domínio para números, unidades ou estruturas; preserve distinções como ordem e multiplicidade quando importam. Encaminhe ambiguidades em vez de forçar equivalência.
Papel do modelo pequeno: Um 8–14B pode produzir candidatos, mas a regra de equivalência deve ser auditável.
Aceite proposto: Detectar exemplos aparentemente iguais com semântica diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Mudanças pequenas e contratos claros tornam verificação mais viável.
8–14B: Para transformações maiores, amplie cobertura e revise premissas do normalizador.
15–30B: Um 15–30B não dispensa equivalência; pode produzir alterações mais complexas que exigem verificadores melhores.
Requisitos de treino/runtime: Ferramentas de teste, referências ou métodos formais conforme o domínio. Não exige treinamento do gerador.
Não aplicar quando: Não apagar diferenças relevantes com arredondamento, ordenação ou remoção de campos apenas para fazer testes passarem.

## T205:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Há verificação de funcionalidade e desempenho, sem equivaler a qualquer receita de treinamento por recompensas.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## T205:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T205 → T195 [complements]
Como combinar: Execução fornece observações para comparação diferencial.
Interface: Artefatos, entradas e efeitos registrados.
Condição: Ambientes comparáveis e referência confiável.
Aceite proposto: Reproduzir e minimizar divergências.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T205 → T188 [feeds]
Como combinar: Agregação de respostas precisa agrupar somente equivalentes semanticamente.
Interface: Forma canônica e regras de unidade.
Condição: Normalizador validado no domínio.
Aceite proposto: Testar frações, unidades e respostas condicionais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S022, V4B-S022, V4B-S024, V4B-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar os casos que revelaram divergência como regressões de desenvolvimento.
- Distinguir ausência de contraexemplo encontrado de prova completa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare transformações corretas e custo de verificação. Equivalência de uma função ou resposta não demonstra competência geral do modelo que a produziu.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T019, T043, T188, T195

## Fontes primárias associadas

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S022 — Introduction to Hypothesis

[https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Testes baseados em propriedades, geração de entradas de domínio e comparação diferencial/round-trip.

Limite: Amostragem de entradas e contraexemplos não constituem prova geral de equivalência.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S024 — Revolutionizing software testing: Introducing LLM-powered bug catchers

[https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ACH gera mutantes e testes, com aplicação explícita a plataformas Meta e evidência de detecção de falhas especificadas.

Limite: Garantia limitada a mutantes/testes verificados; não é prova universal de software correto ou conformidade completa.

### V4B-S025 — LLMs Are the Key to Mutation Testing and Better Compliance

[https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Detalha implantação experimental industrial de ACH no fim de 2024 e revisão humana de testes; problema do oráculo permanece aberto.

Limite: Trial industrial será identificado como tal; não afirmar rollout irrestrito, autonomia total ou todos os idiomas de programação.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T206 — Process Verification

**Nome canônico:** Process Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T206  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** verificação de processo

## T206:C01 — conceito

Verificação de que as etapas observáveis de uma execução cumprem precondições, ordem, invariantes e resultados esperados. Complementa a verificação da saída final. Neste catálogo é um rótulo amplo de engenharia, distinto de Process Supervision, que fornece sinais para treinamento.

Como funciona:
- Definir transições válidas e evidências exigidas por etapa.
- Conferir eventos e resultados contra essas regras durante ou depois da execução.
- Rejeitar conclusão quando houver lacuna material ou transição inválida.

## T206:C02 — aplicacao

Quando usar:
- Workflows com dependências, permissões ou resultados intermediários críticos.
- Um resultado final plausível pode esconder etapa não executada.

Quando não usar:
- Julgar processo apenas por narrativa de intenção produzida pelo próprio agente.

Implementação proposta:
- Registrar eventos com identificador de etapa e vínculo ao artefato.
- Definir invariantes como não concluir sem recibo ou não consumir saída inexistente.
- Reconciliar estado final com histórico e evidências externas.

Aplicação LAI proposta:
Proposta: a Helena separar planejado, executado, testado e comprovado por eventos e recibos vinculados, sem depender da eloquência do relatório.

## T206:C03 — riscos_validacao

Armadilhas:
- Logs incompletos podem parecer processo correto por ausência de erro.
- Procedimento correto em etapas isoladas pode falhar no requisito global.

Métricas sugeridas:
- Violações de transição e etapas sem evidência.
- Cobertura de invariantes e divergência entre estado e histórico.

Testes propostos:
- Remover evento de conclusão e conferir que missão não é marcada comprovada.
- Reordenar etapas dependentes e exigir detecção da violação.

## T206:C04 — perguntas_proveniencia

Pergunta: Process Verification é Process Supervision?
Resposta: Não. Uma verifica execução; a outra treina usando feedback sobre etapas.

Pergunta: Log escrito pelo agente prova que a ferramenta rodou?
Resposta: Não sozinho; o registro precisa estar ligado a evidência da execução.

Pergunta: Pode reconstruir ordem apenas pelo relógio?
Resposta: Nem sempre. Relógios diferentes e concorrência exigem relações causais e identificadores, além dos horários.

Pergunta: Processo correto garante objetivo correto?
Resposta: Pode cumprir uma especificação errada ou incompleta; valide também se critérios e pós-condições correspondem à necessidade real.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T206:C05 — mecanismo_avancado

Um registro de execução oferece observabilidade, mas verificar o processo exige regras sobre transições permitidas e evidências que sustentem cada etapa. Em sistemas concorrentes, timestamps sozinhos não definem causalidade; IDs, relações entre operações e versões ajudam a reconstruir o que ocorreu. Uma mensagem “sucesso” emitida pela própria ação não prova que sua pós-condição se realizou no recurso externo.

Condição de contorno:
Traces incompletos ou amostrados podem omitir a etapa que violou o contrato; ausência de evento não demonstra ausência de ação.

Contrato proposto:
- Entradas: Eventos correlacionados, versões de estado, pré/pós-condições e regras de transição.
- Saídas: Relatório de invariantes atendidas, violações e lacunas de evidência.
- Estado: Identidades de operações, vínculos causais, resultados observados e política de retenção.
- Invariante: Toda conclusão de processo indica quais eventos e estados realmente a sustentam.

Compromissos de projeto:
- Mais instrumentação melhora diagnóstico e acrescenta custo e volume.
- Checagem de resultado externo fortalece evidência e pode exigir consultas adicionais.

## T206:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: registrar sucesso antes de uma gravação que falha, duplicar uma operação e remover um evento intermediário. Esperar distinção entre violação, duplicidade e evidência insuficiente.

Plano de avaliação proposto:
Plano proposto: comparar execuções corretas e falhas injetadas com traces completos e parciais. Medir detecção, falsos alarmes e capacidade de localizar a transição inválida; aprovar somente conclusões proporcionais à cobertura observada.

Comparações:
- T194 (distinct_from): Verificação inspeciona execução; process supervision usa sinais de etapas para treinamento.

Afirmação rastreável:
OpenTelemetry representa operações por spans e oferece vínculos, eventos e contexto para correlacionar trabalho distribuído.
Suporte: related; fontes: V3B-S023
Limite: A fonte define observabilidade; o verificador de invariantes é uma camada adicional proposta, não garantia automática do tracing.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T206:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou causalidade dos eventos e pós-condições. Esta camada trata completude do registro, reconstrução de tentativas e limites do que pode ser certificado quando parte do processo ocorre fora do sistema.

Evidência ausente
Um trace sem erro não prova que todas as etapas ocorreram; pode faltar instrumentação ou ter havido perda de eventos. Defina eventos obrigatórios e estados terminais, distinguindo sucesso, falha, cancelamento e desconhecido. A validação deve detectar lacunas, não preenchê-las com a narrativa do agente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

Tentativas e efeitos
Retries podem criar múltiplas tentativas para a mesma operação lógica. Registre identificadores distintos e vínculo causal, preservando qual tentativa produziu o efeito confirmado. Um evento de envio e um timeout não permitem concluir se a ação externa ocorreu; reconciliação precisa consultar estado ou recibo confiável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

Processo versus resultado
Cumprir etapas não garante que o objetivo final foi atingido, e um resultado correto por acaso não legitima etapas proibidas. Avalie ambos. Revisores e barreiras como os descritos no AutoClean oferecem um padrão operacional, mas a evidência deve declarar exatamente quais propriedades e transições foram checadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

USO AVANÇADO — Workflow de atualização
Cenário: O agente deve consultar, propor, validar e alterar um recurso.
Estratégia: Modele estados permitidos, exija pré-condições observadas e relacione cada ação a sua decisão. Verifique estado final no sistema externo e mantenha pendências de reconciliação.
Papel do modelo pequeno: Um 3–7B pode executar uma máquina de estados estreita com ferramentas.
Aceite proposto: Nenhuma transição sem evidência obrigatória nem sucesso sem pós-condição observada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

USO AVANÇADO — Revisão de execução longa
Cenário: Um agente declara ter concluído muitas etapas.
Estratégia: Reconstrua cadeia causal a partir dos eventos e artefatos, confronte com o plano e identifique passos não observados. Não considere texto de progresso como recibo.
Papel do modelo pequeno: Um 8–14B pode resumir evidências; validação de invariantes deve ser determinística quando possível.
Aceite proposto: Detectar etapas omitidas, versões incorretas e efeitos duplicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S023, C-S047, V4C-S009, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Estados explícitos reduzem dependência de memória textual em modelos pequenos.
8–14B: Fluxos concorrentes exigem IDs e regras de causalidade além de timestamps.
15–30B: Um 15–30B pode planejar mais etapas, mas isso aumenta a necessidade de auditoria de processo.
Requisitos de treino/runtime: Instrumentação, armazenamento de eventos e regras de transição; não implica supervisão de raciocínio interno do modelo.
Não aplicar quando: Não declarar uma ação concluída só porque a ferramenta foi chamada ou o agente escreveu 'feito'.

## T206:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Propriedades como ausência de desvio de intenção verificam requisitos do processo, sem prova formal.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q019.

## T206:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T206 → T194 [complements]
Como combinar: Eventos verificáveis podem apoiar feedback sobre etapas de um procedimento.
Interface: Transições, resultados e falhas localizadas.
Condição: Rótulos descrevem observações, não inferências inventadas.
Aceite proposto: Comparar supervisão com evidência real do ambiente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S023, C-S047, V4C-S009, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T206 → T200 [complements]
Como combinar: Auditoria independente confronta execução declarada e registros externos.
Interface: Trace, artefatos e recibos.
Condição: Fontes não dependem apenas do narrador.
Aceite proposto: Injetar eventos ausentes e contradições para testar detecção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S023, C-S047, V4C-S009, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter estado desconhecido quando não há evidência para decidir.
- Não usar ordem de chegada de logs como causalidade universal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare tarefas concluídas com processo permitido e evidência suficiente. Observabilidade ajuda a confiar numa aplicação pequena; não aumenta diretamente a capacidade do modelo nem prova o que não foi observado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T159, T194, T200

## Fontes primárias associadas

### C-S047 — Let's Verify Step by Step

[https://arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão por etapas difere de rotular apenas o resultado final.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S023 — OpenTelemetry — Traces

[https://opentelemetry.io/docs/concepts/signals/traces/](https://opentelemetry.io/docs/concepts/signals/traces/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Spans, relações de causalidade, eventos e metadados observáveis de execução.

Limite: Tracing registra operações; checagem de invariantes e interpretação de sucesso são contratos adicionais propostos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

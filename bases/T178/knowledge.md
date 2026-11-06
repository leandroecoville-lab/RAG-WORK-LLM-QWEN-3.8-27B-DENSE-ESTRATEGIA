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

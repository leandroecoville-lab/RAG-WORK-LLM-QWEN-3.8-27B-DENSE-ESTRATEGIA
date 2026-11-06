# P017 — Distillation Pipeline

**Nome canônico:** Distillation Pipeline  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P017  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** pipeline proposto de destilação

## P017:C01 — conceito

Distillation Pipeline é um componente editorial proposto para organizar transferência de comportamento ou conhecimento com artefatos explícitos. Seu caminho paramétrico gera exemplos com um professor e treina um aluno; o professor pode ser o mesmo modelo condicionado por contexto adicional. Também deve identificar separadamente transferências para memória externa. Nenhum pipeline LAI executado ou modelo treinado é afirmado.

Como funciona:
- Escolher a habilidade alvo, a configuração do professor e o formato de supervisão: respostas, rótulos ou distribuições quando disponíveis.
- Produzir dados, filtrar erros e separar avaliação antes do treino do aluno ou de adaptadores.
- Comparar aluno, baseline e professor quanto à tarefa, custo e necessidade de contexto em inferência.

## P017:C02 — aplicacao

Quando usar:
- Tarefas estáveis com exemplos suficientes e benefício esperado ao reduzir dependência de prompts extensos ou de modelos caros.

Quando não usar:
- Para corrigir rapidamente fatos voláteis que poderiam ser atualizados por recuperação ou para presumir que reduzir texto já modificou os pesos.

Implementação proposta:
- Proposta: registrar modelo professor, prompt, versões dos dados e critérios de seleção; separar casos de teste por origem ou período.
- No caminho paramétrico, guardar checkpoint inicial, receita de treino, artefato final e avaliação comparativa reproduzível.
- No caminho de memória externa, produzir objetos versionados e referências; classificá-lo como transferência sem treino, sem alegar internalização nos pesos.

Aplicação LAI proposta:
Proposta LAI: P017 gerencia receitas e proveniência; P016 decide aceitação comparativa. T069 permanece consolidação textual externa, T179 destilação paramétrica e T181 transferência hierárquica sem treino.

## P017:C03 — riscos_validacao

Armadilhas:
- O aluno pode aprender erros e vieses do professor.
- Fine-tuning é um procedimento de adaptação mais amplo; nem todo fine-tuning constitui destilação.
- Prompt distillation paramétrica, consolidação por resumos e Agent Memory Distillation não devem compartilhar uma definição indiferenciada.

Métricas sugeridas:
- Qualidade em teste separado, custo de preparação e treino, redução de contexto e custo por resultado correto.

Testes propostos:
- Aceite proposto: avaliar o aluno com o prompt reduzido em casos não utilizados na geração ou seleção dos exemplos.
- Inspecionar o artefato entregue: pesos ou adaptadores alterados versus memória externa; exigir classificação coerente com o processo real.

## P017:C04 — perguntas_proveniencia

Pergunta: Context distillation sempre exige um professor maior?
Resposta: Não. No trabalho Learning by Distilling Context, o mesmo modelo condicionado por instruções gera supervisão para treinar comportamento sem aquele contexto.

Pergunta: Agent Memory Distillation implica atualizar pesos?
Resposta: No estudo identificado em T181, não: trajetórias do professor originam memórias externas hierárquicas utilizadas pelo aluno.

Pergunta: Posso treinar apenas com respostas aprovadas pelo próprio professor?
Resposta: Isso mantém risco de erros correlacionados; use critérios independentes e casos difíceis reservados.

Pergunta: Qual artefato comprova a melhoria?
Resposta: Relatório comparativo por tarefa, com dados e configuração identificados, além do checkpoint treinado e seus limites.

Escopo das fontes:
Fontes distinguem treino paramétrico e transferência por memória; organização do pipeline LAI é proposta editorial.

## P017:C05 — mecanismo_avancado

Distillation Pipeline propõe transformar evidências de desempenho em um processo de treinamento reproduzível. Cada exemplo deve preservar versão do professor, prompt, contexto permitido, resposta e critérios usados para aceitá-la. A divisão de dados precisa evitar vazamento por documentos, sessões ou tarefas quase duplicadas. O artefato treinado deve ser avaliado com o contrato de uso pretendido, inclusive quando o contexto fornecido ao professor será removido na inferência do estudante.

Condição de contorno:
Treinar sobre respostas aparentemente boas não garante preservar comportamento em entradas fora da distribuição. Informação volátil nos pesos também exige estratégia explícita de atualização.

Contrato proposto:
- Entradas: Objetivo de comportamento, dados autorizados com proveniência, professor, estudante, partições e orçamento de treinamento.
- Saídas: Checkpoint ou adaptador versionado, manifesto de dados, configuração de treino e relatório comparativo de aceitação.
- Estado: Hashes dos datasets, critérios de filtragem, checkpoints intermediários e decisões de promoção ou rejeição.
- Invariante: Dados de avaliação reservada não participam da seleção de exemplos, ajuste do professor ou escolha do checkpoint final.

Compromissos de projeto:
- Filtragem rigorosa reduz exemplos ruins, porém pode estreitar cobertura e esconder casos difíceis.
- Destilar comportamento recorrente economiza contexto potencialmente, mas requer amortizar treino e manter atualização de políticas.

## P017:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: inserir um exemplo de avaliação na coleta e uma resposta errada muito confiante do professor; exigir detecção de contaminação e rejeição baseada em critério independente.

Plano de avaliação proposto:
Comparar base com contexto, base sem contexto e estudante sob as mesmas tarefas reservadas. Medir acerto, violações, tokens, custo amortizado e regressões em capacidades preservadas. Registrar resultados negativos e não promover apenas pelo loss de treinamento.

Comparações:
- T178 (complements): Distilação de conhecimento define a transferência de comportamento.
- T179 (complements): Context distillation paramétrica especifica o objetivo de internalização.

Afirmação rastreável:
Prompt distillation pode treinar um estudante para responder sem o prompt usado pelo professor.
Suporte: related; fontes: V3D-S008
Limite: O pipeline e seus critérios de promoção são proposta própria; nenhum treinamento foi executado neste pacote.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P017:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu proveniência e partições. Esta proposta acrescenta seleção da via de transferência, controle de qualidade dos professores e critérios de promoção que distinguem memória externa de atualização paramétrica.

Escolher o destino
Procedimentos estáveis podem virar exemplos de treinamento; fatos mutáveis e trajetórias condicionais podem permanecer em memória externa. Declare qual artefato muda: pesos, adapter, prompt ou acervo. AMD e destilação paramétrica são referências diferentes; agrupá-las no pipeline não torna seus mecanismos equivalentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

Professor falível
Registre versão, contexto e configuração do professor, mas também como sua resposta foi verificada. Consenso de professores não substitui referência quando compartilham erro. Dados multi-teacher podem ter objetivos distintos, como no ranking do LinkedIn; a combinação precisa de critérios e não apenas concatenação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

Promoção e manutenção
Compare aluno, base e professor na tarefa real, incluindo contexto retirado, ferramentas e quantização final. Rejeite versões com regressões relevantes e mantenha rollback. Quando o comportamento muda, atualize a relação entre dados, política e artefato, sem presumir que editar uma fonte atualiza pesos já treinados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

USO AVANÇADO — Especializar aluno de domínio
Cenário: Chamadas caras ao professor podem ocorrer offline.
Estratégia: Gere exemplos estratificados, filtre por verificadores e ajuste o aluno. Separe dados por origem e mantenha teste final intocado, incluindo casos em que o professor errou.
Papel do modelo pequeno: Um 3–7B pode assumir formato e procedimento estreitos com evidência externa.
Aceite proposto: Generalização, cobertura e custo amortizado por resultado aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

USO AVANÇADO — Transferir experiência de agente
Cenário: Trajetórias de sucesso contêm convenções de ferramentas.
Estratégia: Extraia memórias com pré-condições e versões; teste em novas situações antes de publicar. Só treine pesos se houver hipótese clara sobre comportamento estável.
Papel do modelo pequeno: Um 8–14B pode usar memória procedural sem depender de memorizar todos os detalhes.
Aceite proposto: Sucesso executável e rejeição de procedimentos incompatíveis com o ambiente atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Foco em habilidades delimitadas e dados verificados; volume sintético não substitui qualidade.
8–14B: Avalie on-policy quando falhas surgem nos estados visitados pelo aluno.
15–30B: Para 15–30B, compare benefício marginal com custo de professor, treino, exportação e manutenção.
Requisitos de treino/runtime: Proposta de pipeline: exige implementação e execução próprias. Caminho paramétrico requer treinamento; memória externa requer curadoria e recuperação.
Não aplicar quando: Não prometer transferir toda capacidade do professor nem afirmar que um aluno LAI foi treinado por esta entrega.

## P017:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4B-C017 — Anthropic / Claude — treinamento com constituição
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: treinamento de LLM.
Uso observado: A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.
Mecanismo documentado: Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.
Correspondência com esta base: Uma política LAI poderia inspirar dados próprios; não há implantação da proposta editorial.
Transferência proposta para modelo pequeno: Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.
Limite: Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.
Fontes: V4B-S021.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: Pipeline real inspira gestão de professores e artefatos da proposta LAI.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C009 — Microsoft / Bing — inferência BERT
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Microsoft relata que modelos BERT destilados e otimizações de inferência foram usados em produção no Bing para tarefas de linguagem e busca.
Mecanismo documentado: Redução do professor a encoder de três camadas e posterior otimização de execução; parte das melhorias foi disponibilizada no ONNX Runtime.
Correspondência com esta base: Demonstra uma separação entre compressão de comportamento e otimização do executor.
Transferência proposta para modelo pequeno: Proposta: testar um modelo especializado ou até um encoder menor antes de usar um gerador 3–30B para classificação/ranking.
Limite: Caso histórico de encoder, abaixo da escala e distinto do decode autoregressivo solicitado. Não atribuir ganhos de GPU/C++ à destilação isoladamente nem generalizar precisão de busca a geração aberta.
Fontes: V4B-S009.

V4B-C026 — Autores de Agent Memory Distillation / AMD
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: O projeto apresenta avaliação de agentes de 4–8B com memória derivada de trajetórias de um professor.
Mecanismo documentado: Memórias de workflow, subtarefa e função apoiam recuperação proativa e reativa a falhas, sem exigir que toda a memória seja absorvida por atualização dos pesos.
Correspondência com esta base: Pode inspirar uma proposta LAI, sem comprovar sua adoção.
Transferência proposta para modelo pequeno: Proposta: extrair procedimentos de trajetórias autorizadas, validar executabilidade e recuperar somente passos compatíveis com o ambiente atual.
Limite: Benchmarks de pesquisa não demonstram implantação em bigtech nem equivalência geral a modelos maiores. Memória externa continua dependente de seleção, validade temporal e ferramentas.
Fontes: V4B-S032, C-S035.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: Fornece contratos de dados e checkpoints para um pipeline editorial proposto.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q008, V4B-Q009, V4B-Q023.

## P017:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P017 → T178 [feeds]
Como combinar: O caminho paramétrico organiza sinais de conhecimento ou comportamento do professor.
Interface: Dados, logits ou respostas e critérios de filtro.
Condição: Sinal disponível e objetivos explícitos.
Aceite proposto: Comparar aluno com referência independente em casos novos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P017 → T181 [alternative]
Como combinar: O caminho de memória preserva procedimentos externos em vez de atualizar necessariamente pesos.
Interface: Trajetórias, pré-condições e versões.
Condição: Memórias são recuperáveis e executáveis no ambiente.
Aceite proposto: Testar deriva de ferramenta e erros sem falha sintática.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P017 → P016 [requires]
Como combinar: Avaliação proposta decide promoção do artefato sob contrato de implantação.
Interface: Manifesto, métricas e casos reservados.
Condição: Sem vazamento de dados para geração ou seleção.
Aceite proposto: Rejeitar melhora apenas aparente por contaminação ou mudança de teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013, V4B-S005, V4B-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter dados de avaliação fora da seleção do professor e das memórias.
- Não chamar filtragem de respostas de treinamento quando nenhum estado persistente foi atualizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A proposta busca competência especializada com custo menor. A comparação com fronteira deve igualar tarefa e informação disponível e incluir limites do aluno; não há promessa de inteligência geral transferida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T069, T178, T179, T180, T181, R012, R015, P016

## Fontes primárias associadas

### C-S032 — Distilling the Knowledge in a Neural Network

[https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Destilação transfere comportamento de professor ou ensemble a modelo aluno.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S035 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://arxiv.org/abs/2608.07169](https://arxiv.org/abs/2608.07169)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AMD transfere trajetórias bem-sucedidas em memórias de workflow, subtarefa e função, sem atualizar pesos.

Limite: Método identificado em fonte primária; resultados não reproduzidos nem extrapolados ao Qwen/Helena. A versão arXiv consultada diz under review; outra versão consta na ACL Anthology.

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

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S032 — Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory

[https://agent-memory-distillation.github.io/](https://agent-memory-distillation.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias de workflow, subtarefa e função de trajetórias do professor, injeção proativa/reativa e experimentos com alunos pequenos sem treino.

Limite: Pesquisa, sem implantação industrial comprovada nesta fonte; paridade é restrita a tarefas avaliadas.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

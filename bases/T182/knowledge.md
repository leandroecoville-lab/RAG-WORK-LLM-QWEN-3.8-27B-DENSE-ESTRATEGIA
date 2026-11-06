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

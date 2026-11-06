# T079 — Speculative Decoding

**Nome canônico:** Speculative Decoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T079  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** decodificação especulativa; speculative sampling

## T079:C01 — conceito

Acelera geração autorregressiva usando candidatos baratos e verificação paralela pelo modelo alvo. O alvo continua determinando a distribuição final quando se aplica corretamente o algoritmo exato de aceitação e correção. O benefício depende da concordância entre candidatos e alvo e do custo de verificá-los.

Como funciona:
- Um proponente produz vários tokens candidatos para o mesmo prefixo.
- O alvo avalia as posições em uma execução agrupada e aceita um prefixo válido.
- Na primeira rejeição, corrige a amostragem; estados KV posteriores ao trecho aceito são descartados.

## T079:C02 — aplicacao

Quando usar:
- Decode com baixa concorrência e alto custo por token.
- Tarefas repetitivas que produzam boa taxa de aceitação.

Quando não usar:
- Quando a verificação, o proponente e a memória extra custarem mais que o decode convencional.

Implementação proposta:
- Fixar modelo alvo, tokenizer, template e parâmetros de amostragem no comparativo.
- Experimentar comprimentos de rascunho pequenos e registrar custo de cada etapa.
- Manter caminho convencional para desligar especulação quando o ganho desaparecer.

Aplicação LAI proposta:
Proposta LAI: medir primeiro em saídas longas do Qwen; não confundir aceleração de decode com melhoria de inteligência ou redução de prefill.

## T079:C03 — riscos_validacao

Armadilhas:
- Aceitar tokens apenas por semelhança altera a distribuição; não é o algoritmo exato.
- Mesma distribuição não implica mesma sequência com a mesma seed, pois o consumo aleatório pode mudar.

Métricas sugeridas:
- Tokens aceitos por chamada do alvo e tempo por token.
- Latência p95, throughput e VRAM com concorrência crescente.

Testes propostos:
- Comparar distribuições empíricas em um modelo pequeno e prefixos controlados; rejeitar desvios além da tolerância definida.
- Forçar candidatos ruins e confirmar correção e ausência de KV inválido após rejeição.

## T079:C04 — perguntas_proveniencia

Pergunta: A especulação muda a qualidade?
Resposta: A variante exata preserva a distribuição do alvo sob suas premissas; implementações aproximadas precisam avaliação própria.

Pergunta: Sempre fica mais rápido?
Resposta: Não. Baixa aceitação ou concorrência alta pode tornar a execução mais lenta.

Pergunta: Aceitação alta garante aceleração?
Resposta: Não. O custo de produzir e verificar candidatos pode exceder o trabalho economizado, sobretudo em lotes grandes.

Pergunta: Por que descartar o sufixo rejeitado?
Resposta: Sua distribuição foi condicionada a uma continuação que deixou de existir; reutilizá-lo corrompe o estado autoregressivo.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T079:C05 — mecanismo_avancado

A correção estatística exige usar distribuições efetivas depois dos filtros de amostragem: para proposta x de q, aceitar com min(1,p(x)/q(x)); uma rejeição exige a distribuição residual proporcional a max(p−q,0). Reamostrar diretamente de p nessa rejeição altera a marginal. O alvo verifica vários candidatos, porém somente o prefixo aceito pode atualizar o histórico confirmado; estados dos candidatos posteriores precisam ser descartados.

Condição de contorno:
A equivalência pressupõe condicionamentos idênticos, normalização consistente e implementação correta; aproximações numéricas e filtros divergentes precisam de análise própria.

Contrato proposto:
- Entradas: Prefixo tokenizado e distribuições alvo e rascunho com configuração de amostragem registrada.
- Saídas: Tokens confirmados, ponto de rejeição e custos separados de proposta e verificação.
- Estado: Caches separados, gerador aleatório e extensão ainda provisória.
- Invariante: Nenhum candidato rejeitado influencia a próxima distribuição condicional.

Compromissos de projeto:
- Mais propostas podem aumentar trabalho desperdiçado e memória temporária.
- Preservar distribuição não significa reproduzir a sequência da mesma seed.

## T079:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar vocabulário de três símbolos com probabilidades conhecidas, injetar reamostragem incorreta após rejeição e comparar as marginais enumeradas. A versão defeituosa deve ser detectada.

Plano de avaliação proposto:
Plano proposto: comparar com geração exclusiva pelo alvo, controlando prompts, distribuição e comprimentos. Medir tempo por token confirmado, custo do rascunho e taxa de aceitação; aprovar somente com equivalência verificada e ganho no cenário pretendido.

Comparações:
- T132 (complements): Um draft externo fornece propostas; a regra de aceitação continua sendo o mecanismo de correção.

Afirmação rastreável:
O algoritmo publicado combina aceitação por razão de probabilidades e correção residual para preservar a distribuição do alvo.
Suporte: direct; fontes: B-S048
Limite: A prova idealizada não certifica kernels, filtros ou caches de qualquer servidor.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T079:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou aceitação e correção da distribuição. A nova camada decide onde especular dentro de um serviço compartilhado, como contabilizar trabalho descartado e como promover uma configuração sem confundir equivalência estatística com igualdade textual.

Economia por requisição
Trate o caminho especulativo como uma opção com custo de oportunidade. Estime tempo de draft, verificação, manutenção de KV e espera que ele impõe às demais requisições. Um lote que confirma mais tokens pode ainda piorar a cauda do serviço; registre economia por token confirmado e por tarefa concluída, incluindo recusas e cancelamentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S048, V3B-S001, V4B-S001, V4B-S002.

Fronteira de confirmação
Separe estados propostos, verificados e entregues ao cliente. Apenas o prefixo confirmado avança o contador de saída; cancelamento durante verificação deve liberar o trecho especulativo sem publicar candidatos. Quando prefill e decode estiverem separados, transporte também os metadados exigidos pelo método, não somente tensores KV.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S048, V3B-S001, V4B-S001, V4B-S002.

Promoção por regime
Mantenha perfis distintos para baixa concorrência, saturação e prompts com muita repetição. Use tráfego de sombra para escolher o perfil e registre a versão do amostrador. Preserve um caminho sem especulação acionável por aumento de custo, falha de compatibilidade ou perda de qualidade, sem alterar silenciosamente a temperatura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S048, V3B-S001, V4B-S001, V4B-S002.

USO AVANÇADO — Extração com evidências repetidas
Cenário: Relatórios estruturados reutilizam entidades do material fornecido.
Estratégia: Compare proponente por n-gramas com draft neural usando a mesma distribuição alvo. Escolha por custo completo; desabilite especulação quando o trecho livre reduzir a aceitação. Publique somente resultados verificados.
Papel do modelo pequeno: Um alvo de 3–30B resolve a tarefa; o proponente economiza execução, sem acrescentar conhecimento.
Aceite proposto: Aceitar apenas com preservação validada da distribuição e melhora de latência sob o mesmo SLO.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S048, V3B-S001, V4B-S001, V4B-S002.

USO AVANÇADO — Agente com ferramentas lentas
Cenário: A geração textual está no caminho crítico entre chamadas.
Estratégia: Meça primeiro a fração do tempo atribuída ao decode. Aplique especulação apenas às chamadas suficientemente longas; em respostas curtas, evite inicialização de draft que custa mais que o trabalho poupado.
Papel do modelo pequeno: O modelo pequeno pode ser alvo ou draft; as duas funções precisam de avaliação separada.
Aceite proposto: Comparar tempo por missão, tokens confirmados e incidência de fallback, sem esconder latência de ferramentas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S048, V3B-S001, V4B-S001, V4B-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em alvos 3–7B, o custo do draft pode consumir a vantagem; testar proposta sem pesos antes de carregar outro modelo.
8–14B: Em 8–14B, comparar assistente especializado e n-gramas por tarefa, reservando memória para ambos os caches.
15–30B: Em 15–30B, maior custo do alvo pode favorecer especulação, mas pressão de KV e concorrência continuam determinantes.
Requisitos de treino/runtime: Runtime precisa implementar verificação correta; EAGLE/MTP acrescentam requisitos de treino ou arquitetura específicos.
Não aplicar quando: Não usar modo aproximado como se preservasse distribuição, nem ativar quando o gargalo está fora da geração.

## T079:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O artigo afirma uso real de speculative decoding.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Runtime NPU documenta especulação; não generalizar para GPU ou revisão histórica. Escopo: capacidade NPU da documentação consultada em 2026-11-05; não é inferida para GPU ou para a versão histórica de 2024.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: O daemon combina especulação com geração guiada.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

V4B-C007 — Meta / Experimentos EAGLE para Llama
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores apresentam otimizações de treinamento e inferência de EAGLE para Llama em condições descritas como production scale.
Mecanismo documentado: Atenção em árvore, verificação em múltiplas rodadas e otimizações de execução do proponente/target.
Correspondência com esta base: O mecanismo é speculative decoding com verificação pelo alvo.
Transferência proposta para modelo pequeno: Proposta: avaliar a viabilidade de treinamento de um draft compatível com um alvo 8–30B antes de investigar grandes lotes.
Limite: A página aberta não identifica implantação comercial específica; production scale não é convertido em production_documented. Ganhos em Llama grande e múltiplas H100 não são transferidos ao ambiente do usuário.
Fontes: V4B-S007.

V4B-C023 — Snowflake / Suffix Decoding
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: pesquisa sobre LLM.
Uso observado: A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.
Mecanismo documentado: Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.
Correspondência com esta base: Os candidatos são usados em decodificação especulativa.
Transferência proposta para modelo pequeno: Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.
Limite: Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.
Fontes: B-S040.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T079:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T079 → T130 [complements]
Como combinar: Usar repetição do prompt como proponente barato, mantendo o verificador do alvo.
Interface: Tokens candidatos e extensão máxima do prefixo proposto.
Condição: Há repetição suficiente e isolamento dos históricos.
Aceite proposto: Comparar taxa de aceitação, custo CPU e distribuição final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S048, V3B-S001, V4B-S001, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T079 → T102 [complements]
Como combinar: Transferir estados necessários antes de admitir o decode especulativo no worker destino.
Interface: KV, logits ou características conforme método e revisão do modelo.
Condição: Conector conhece o estado adicional do proponente.
Aceite proposto: Interromper transferência e confirmar que nenhum token não verificado é emitido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S048, V3B-S001, V4B-S001, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contabilizar tokens descartados como custo, não throughput útil.
- Reconciliar contadores de saída após cancelamento, rejeição e troca de worker.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar uma tarefa delimitada com um modelo de fronteira usando qualidade e custo por resultado aceito. Especulação pode aproximar a responsividade, mas não aumenta a capacidade de raciocínio ou conhecimento do alvo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T080, T128, T130, T131, T132

## Fontes primárias associadas

### B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://arxiv.org/abs/2211.17192](https://arxiv.org/abs/2211.17192)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rascunhos verificados em paralelo e amostragem especulativa exata, sob o algoritmo descrito.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S048 — Accelerating Large Language Model Decoding with Speculative Sampling

[https://arxiv.org/abs/2302.01318](https://arxiv.org/abs/2302.01318)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo auxiliar barato gera continuações e amostragem por rejeição modificada preserva a distribuição do alvo dentro das condições numéricas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM

[https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvores de sufixos sobre tokens anteriores produzem candidatos especulativos sem modelo auxiliar.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S007 — Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions

[https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/](https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Engenharia de EAGLE para Llama, incluindo atenção em árvore e grandes lotes.

Limite: Production scale descreve escala de experimento; página não identifica implantação comercial específica suficiente para contagem de produção.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

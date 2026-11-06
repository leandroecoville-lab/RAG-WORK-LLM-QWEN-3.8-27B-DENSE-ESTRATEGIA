# Inferência, atenção, GPU e cache

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

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


---

# T080 — Adaptive Speculative Decoding

**Nome canônico:** Adaptive Speculative Decoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T080  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** dynamic speculation lookahead; especulação adaptativa

## T080:C01 — conceito

Ajusta durante a geração quanto trabalho especulativo realizar. Em vez de propor sempre o mesmo número de tokens, um controlador usa confiança do assistente, aceitação recente ou custo observado. É uma família de políticas sobre a especulação, e não uma garantia adicional de exatidão.

Como funciona:
- Observar sinais de facilidade do trecho e resultados das últimas propostas.
- Encerrar ou ampliar o rascunho dentro de limites definidos.
- Submeter todo candidato à mesma verificação exigida pelo método base.

## T080:C02 — aplicacao

Quando usar:
- Tarefas que alternam texto previsível e decisões difíceis.
- Pares assistente/alvo cuja concordância varia muito entre prompts.

Quando não usar:
- Controlador sem telemetria ou com custo superior ao trabalho economizado.

Implementação proposta:
- Começar com comprimento fixo como baseline e registrar tempo do assistente e do alvo.
- Adicionar limite mínimo/máximo e uma regra de ajuste gradual por janela.
- Separar calibração do controlador e avaliação em tarefas novas.

Aplicação LAI proposta:
Proposta LAI: comparar controlador adaptativo e rascunho fixo em tarefas de código, extração e conversa antes de adotar uma política comum.

## T080:C03 — riscos_validacao

Armadilhas:
- Confiança alta do assistente não demonstra que o alvo aceitará o token.
- Reagir a uma única rejeição pode produzir oscilação e piorar a latência de cauda.

Métricas sugeridas:
- Comprimento proposto versus aceito por trecho.
- Tempo líquido economizado e frequência de recuo ao modo convencional.

Testes propostos:
- Alternar entradas repetitivas e imprevisíveis; exigir melhoria média sem ultrapassar o orçamento de cauda.
- Injetar queda de concordância e verificar que o controlador limita rapidamente o desperdício.

## T080:C04 — perguntas_proveniencia

Pergunta: Confiança do assistente pode dispensar o alvo?
Resposta: Não em especulação exata. Ela orienta o tamanho do rascunho, não autoriza aceitar seu conteúdo.

Pergunta: Qual comprimento é ideal?
Resposta: É específico da carga, par de modelos e hardware; deve ser ajustado por ganho líquido medido.

Pergunta: É necessário treinar o assistente novamente?
Resposta: Não para adaptar o horizonte; atualizar pesos online seria uma intervenção distinta, com outros custos e controles.

Pergunta: Qual unidade orienta a decisão?
Resposta: Milissegundos por token confirmado, condicionados à carga, são mais úteis que a fração aceita observada isoladamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T080:C05 — mecanismo_avancado

O tamanho do rascunho deve minimizar tempo por token confirmado, e não maximizar isoladamente sua taxa de aceitação. Um controlador pode observar duração das propostas, verificação e quantidade aceita, mantendo limites e suavização para evitar oscilações. Confiança do assistente é apenas um sinal para decidir quanto especular; um assistente confiante também pode discordar sistematicamente do alvo.

Condição de contorno:
Quando a carga muda mais rapidamente que a adaptação, estatísticas antigas podem produzir decisões piores que uma política fixa.

Contrato proposto:
- Entradas: Sinais por iteração, orçamento de latência e limites permitidos para propostas.
- Saídas: Próximo tamanho do rascunho e motivo observável da decisão.
- Estado: Estatísticas móveis por classe de carga e configuração do par de modelos.
- Invariante: A adaptação altera quantidade proposta, mantendo a mesma regra correta de verificação.

Compromissos de projeto:
- Horizontes longos amortizam verificações, mas elevam desperdício após rejeição.
- Controladores muito sensíveis podem reagir ao ruído do escalonador.

## T080:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar trechos fáceis e divergentes, injetando atrasos no assistente. Esperar redução do horizonte quando o custo aumenta, sem aceitar tokens pela confiança sozinha.

Plano de avaliação proposto:
Plano proposto: comparar horizonte constante, regra heurística e adaptação, com mesmos modelos e chegadas. Medir latência por token confirmado, variância, custo adicional e tempo de recuperação após mudanças; escolher pela distribuição real de serviço.

Comparações:
- T079 (complements): A política escolhe esforço; o algoritmo de aceitação continua responsável pela exatidão.

Afirmação rastreável:
A implementação documentada pela Hugging Face pode interromper propostas usando a confiança do assistente.
Suporte: direct; fontes: B-S002
Limite: O limiar é uma heurística de execução; não equivale a calibração de correção factual ou concordância garantida.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T080:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou horizonte variável e estabilidade do controlador. Aqui a adaptação considera censura por encerramento, prazo restante e mudança de carga, permitindo aprender uma política sem confundir facilidade do texto com capacidade disponível do servidor.

Sinais que não enviesam a decisão
Uma sequência encerrada por EOS não fornece a mesma observação que um rascunho rejeitado. Marque passos censurados por término, cancelamento ou limite. Mantenha histogramas por posição proposta e classe de tarefa, pois a média global pode esconder aceitação alta no primeiro token e quase nula no restante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

Controle em dois tempos
Use uma política rápida para escolher o próximo horizonte a partir do prefixo recente e uma política lenta para ajustar limites conforme fila e memória. A rápida não deve aumentar candidatos quando a lenta identifica saturação. Registre ambas as decisões para distinguir mudança de texto de mudança de capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

Aprendizado com exploração limitada
Reserve uma parcela controlada de tráfego elegível para comparar horizontes alternativos. Sem exploração, a política só observa os regimes que ela própria escolheu e pode ficar presa em uma configuração ruim. A exploração deve respeitar prazo, orçamento KV e disponibilidade do caminho convencional, com desligamento imediato se o SLO piorar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

USO AVANÇADO — Saída heterogênea
Cenário: Uma mesma resposta alterna enumerações previsíveis e explicações abertas.
Estratégia: Use segmentos observáveis do formato como sinais auxiliares, sem presumir que JSON sempre é fácil. Reduza o horizonte após divergências consecutivas e recupere lentamente quando tokens confirmados por custo voltarem a crescer.
Papel do modelo pequeno: Alvos pequenos podem beneficiar-se principalmente nos segmentos repetitivos.
Aceite proposto: Aprovar por tempo total e cauda; exigir que adaptação não altere critérios de aceitação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

USO AVANÇADO — Tráfego com rajadas
Cenário: O servidor atende agentes durante picos de requisições.
Estratégia: Imponha limite global de trabalho especulativo. Ao crescer a fila, compare horizonte menor e desligamento temporário; reative com histerese quando a pressão cair. Não use um limiar único de confiança para todos os modelos.
Papel do modelo pequeno: Um 8–30B pode compartilhar GPU com outros trabalhos; a política preserva capacidade útil.
Aceite proposto: Medir tempo de recuperação após rajada, preempções e latência dos pedidos que não especulam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, exigir evidência de que a própria instrumentação e decisão custam menos que a economia obtida.
8–14B: Em 8–14B, perfilar transições entre formatos e idiomas para evitar uma política dominada pelo tráfego mais frequente.
15–30B: Em 15–30B, controlar horizonte conjuntamente com reserva KV e trabalho de verificação concorrente.
Requisitos de treino/runtime: A adaptação é runtime; confiança do proponente precisa ser acessível e qualquer aprendizado de política exige dados separados.
Não aplicar quando: Não aplicar política treinada em baixa carga diretamente à saturação, nem interpretar EOS como rejeição.

## T080:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T080:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T080 → T079 [requires]
Como combinar: Adaptar apenas a quantidade proposta, preservando o algoritmo de verificação do mecanismo base.
Interface: Horizonte escolhido, candidatos e máscara de posições válidas.
Condição: A proposta variável é suportada pelo backend.
Aceite proposto: Testar todos os horizontes contra o mesmo alvo convencional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S002, V3B-S001, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T080 → T121 [complements]
Como combinar: Combinar orçamento especulativo com admissão por GPU para proteger requisições já ativas.
Interface: Fila, prazo restante, bytes KV e custo por passo.
Condição: O scheduler informa pressão em tempo útil.
Aceite proposto: Reproduzir rajadas e verificar ausência de oscilação persistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S002, V3B-S001, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Versionar política e manter histórico das decisões para detectar drift.
- Separar observações censuradas e impor um horizonte máximo verificável.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O experimento com fronteira deve comparar custo por resposta correta em diferentes níveis de carga. Adaptar horizonte melhora utilização quando funciona; não transforma um modelo menor em especialista mais competente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T145, T146

## Fontes primárias associadas

### B-S002 — Faster Assisted Generation with Dynamic Speculation

[https://huggingface.co/blog/dynamic_speculation_lookahead](https://huggingface.co/blog/dynamic_speculation_lookahead)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comprimento adaptativo do rascunho e interrupção por confiança do modelo assistente.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T081 — KV Cache Reuse

**Nome canônico:** KV Cache Reuse  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T081  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reuso de cache de chaves e valores

## T081:C01 — conceito

Reutiliza tensores de chaves e valores já calculados para tokens anteriores, evitando repetir parte do processamento autorregressivo. Há reuso dentro da própria geração e reuso de prefixos entre chamadas. Esses estados computacionais não são memória semântica, histórico textual nem uma resposta pronta.

Como funciona:
- No prefill, calcular estados KV das posições válidas.
- Em cada passo de decode, acrescentar os novos estados sem recalcular todo o prefixo.
- Ao reutilizar entre chamadas, conferir identidade do modelo, sequência e condições de execução.

## T081:C02 — aplicacao

Quando usar:
- Geração de vários tokens com arquitetura que oferece cache.
- Continuação de um prefixo realmente idêntico.

Quando não usar:
- Reusar estados após alterar pesos, adaptador, tokens anteriores ou configuração posicional incompatível.

Implementação proposta:
- Inventariar quais camadas possuem KV e quais usam outros estados recorrentes.
- Estimar memória por sequência e concorrência, incluindo overhead de alocação.
- Registrar revisão do modelo e invalidação do cache no ciclo de deploy.

Aplicação LAI proposta:
Proposta LAI: tratar KV como aceleração descartável do runtime; manter estado de missão e documentos em memória persistente separada.

## T081:C03 — riscos_validacao

Armadilhas:
- Textos visualmente semelhantes podem tokenizar de maneira diferente.
- Duplicar ou anexar incorretamente o último token ao retomar altera posições e saída.

Métricas sugeridas:
- Memória KV por sequência e tokens efetivamente reaproveitados.
- Tempo por token com cache ligado e desligado em entrada igual.

Testes propostos:
- Retomar uma sequência com cache e comparar logits com recomputação completa dentro da tolerância numérica.
- Mudar um token antigo e exigir invalidação do trecho afetado e de seus sucessores.

## T081:C04 — perguntas_proveniencia

Pergunta: KV guarda o conhecimento da empresa?
Resposta: Não. Guarda representações dependentes de uma execução específica do modelo.

Pergunta: Posso reutilizar em outro modelo?
Resposta: Não de forma geral; formato e significado dos estados dependem dos pesos e da arquitetura.

Pergunta: Cache elimina todo custo quadrático?
Resposta: Evita refazer o prefixo a cada passo; o prefill denso ainda possui interações quadráticas entre tokens.

Pergunta: Texto idêntico basta para reutilizar?
Resposta: Não. Tokenização, posições, máscara e estado do modelo precisam corresponder, inclusive quando o template de conversa muda.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T081:C05 — mecanismo_avancado

O cache evita recalcular projeções de tokens anteriores, mas a consulta nova ainda interage com as chaves preservadas. Portanto, atenção densa no decode mantém custo dependente do contexto. Em um loop incremental, devem entrar somente tokens ainda não processados, enquanto a máscara representa a extensão anterior mais a nova. Posições, pesos e adaptadores fazem parte da identidade lógica desse estado.

Condição de contorno:
Prefixos editados, máscaras diferentes ou mudança de modelo invalidam estados mesmo quando parte do texto visível permanece igual.

Contrato proposto:
- Entradas: Tokens incrementais, posições, máscara completa e identidade do modelo.
- Saídas: Logits atuais e cache estendido com comprimento lógico explícito.
- Estado: Chaves e valores por camada, posições válidas e revisão do prefixo.
- Invariante: O cache representa exatamente o mesmo prefixo usado para calcular os logits.

Compromissos de projeto:
- Menos recomputação exige memória crescente em atenção global.
- Pré-alocação facilita estabilidade de formas, mas pode reservar capacidade ociosa.

## T081:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar continuação com padding e depois alterar um token inicial sem invalidar o cache. Comparar logits com recomputação integral; a reutilização incompatível deve falhar na validação.

Plano de avaliação proposto:
Plano proposto: controlar pesos, dtype, máscara e sequência; comparar execução incremental com recomputação completa. Registrar erro numérico tolerado pelo backend, bytes por camada e latência por comprimento; avaliar separadamente prefill e decode.

Comparações:
- T116 (alternative): Recomputação recupera estados ausentes ao custo de trabalho adicional de inferência.

Afirmação rastreável:
A documentação de cache exige máscara cobrindo tokens passados e atuais no loop incremental.
Suporte: direct; fontes: V3B-S005
Limite: O contrato concreto depende da arquitetura; atenção bidirecional não herda automaticamente a propriedade causal.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T081:C07 — estrategia_3_30b

NOVA CAMADA v4 — Além da identidade dos estados explicada na v3, esta ficha trata KV como artefato de execução com ciclo de vida: aquisição, validação, empréstimo, migração e reconstrução. A prioridade é evitar que otimização torne recuperação operacional frágil.

Manifesto de estado
Associe ao cache um manifesto com revisão de pesos, adaptador, tokenizer, posições, formato numérico e comprimento confirmado. O manifesto deve ser verificável antes de anexar novos tokens. Um blob legível pode estar semanticamente incompatível; checksum prova integridade de bytes, não equivalência da configuração que os produziu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

Empréstimo e propriedade
Distingua uma referência compartilhada somente para leitura de uma continuação que pode escrever. Ao criar ramificações, use referências contadas ou cópia controlada para as regiões mutáveis. Uma requisição cancelada não pode liberar blocos ainda consumidos por outra; a contabilidade deve acompanhar o ciclo completo do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

Recuperação desacoplada
Projete o serviço para reconstruir KV a partir dos tokens confirmados quando a afinidade se perder. Persistir todos os tensores pode ser mais caro que recalcular um prefixo curto. A decisão de persistência deve considerar tempo de retomada, bytes transferidos, taxa de falha e frequência real de revisita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

USO AVANÇADO — Continuação após mudança de worker
Cenário: Um agente retorna à conversa depois de expiração ou reinício.
Estratégia: Negocie compatibilidade do manifesto; se for exata, transfira o estado suportado. Caso contrário, reproduza os tokens confirmados no destino. Diferencie retomar a computação de repetir ações externas já realizadas.
Papel do modelo pequeno: Modelos 3–30B podem reconstruir contexto local sem depender de memória KV durável.
Aceite proposto: Aceitar com mesmo histórico lógico e sem duplicação de efeitos; medir custo de reconstrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

USO AVANÇADO — Comparação de alternativas
Cenário: Um planejador abre duas continuações do mesmo prefixo.
Estratégia: Compartilhe o prefixo imutável, mantenha sufixos independentes e descarte o ramo perdedor após seleção. Não misture tokens de ramos diferentes ao consolidar a conversa, mesmo que os prompts tenham o mesmo texto inicial.
Papel do modelo pequeno: Um modelo pequeno pode explorar alternativas dentro de um orçamento explícito de memória.
Aceite proposto: Verificar independência dos ramos e bytes adicionais realmente alocados por continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, reconstrução pode ser simples o bastante para dispensar transferência persistente de grandes blobs.
8–14B: Em 8–14B, comparar retenção local de sessões ativas com recomputação de sessões raras.
15–30B: Em 15–30B, projetar migração conforme volume KV e capacidade de cada worker, evitando reservar memória inutilizada.
Requisitos de treino/runtime: Reuso é runtime; mudanças de adaptador, posição ou representação exigem invalidação ou conversão formalmente suportada.
Não aplicar quando: Não usar KV como histórico auditável nem recuperar conversa a partir de estado sem tokens e configuração de origem.

## T081:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: A arquitetura reutiliza KV como recurso compartilhado do serving.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: O decode consome estado recebido, mas o caso não demonstra todo tipo de reuso entre requisições.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Blocos KV podem ser reutilizados entre requisições elegíveis.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: Objetos de modelo podem compartilhar estado, sem comprovar todos os cenários de cache distribuído.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002, V4B-Q003.

## T081:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T081 → T116 [alternative]
Como combinar: Recalcular quando custo ou incompatibilidade tornam transferência inadequada.
Interface: Tokens confirmados, máscara e manifesto de execução.
Condição: O histórico original é reconstruível.
Aceite proposto: Comparar logits e saída sob tolerância definida do backend.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, B-S003, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T081 → T060 [complements]
Como combinar: Salvar progresso lógico independentemente do cache computacional.
Interface: Revisão da sessão, resultados aceitos e referências de artefatos.
Condição: Checkpoint distingue efeitos concluídos de geração parcial.
Aceite proposto: Reiniciar sem KV e verificar continuidade da missão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, B-S003, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Nunca aceitar comprimento confirmado maior que os tokens disponíveis.
- Testar liberação concorrente e cache perdido durante uma ramificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar retomada de uma tarefa real contra um serviço de fronteira com o mesmo contexto. Menor tempo de prefill pode melhorar custo e experiência, mas não resolve lacunas de entendimento do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T084, T086, T105, T116

## Fontes primárias associadas

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

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

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T082 — Prefix Caching

**Nome canônico:** Prefix Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T082  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** automatic prefix caching; cache de prefixos

## T082:C01 — conceito

Reaproveita o processamento de um início idêntico de sequência entre requisições. O cache pode guardar blocos KV desse prefixo e reduzir o trabalho de prefill. Não reutiliza automaticamente a resposta anterior e não retira os tokens da janela lógica do modelo.

Como funciona:
- Tokenizar o prompt completo com a mesma política usada no servidor.
- Encontrar o maior prefixo já calculado e compatível.
- Recuperar estados correspondentes e calcular apenas o sufixo ausente.

## T082:C02 — aplicacao

Quando usar:
- Instruções estáveis compartilhadas por muitas chamadas.
- Perguntas diferentes sobre o mesmo documento inicial longo.

Quando não usar:
- Prompts cujo início muda constantemente ou quando a persistência do cache não compensa seu custo.

Implementação proposta:
- Colocar instruções estáveis antes dos dados variáveis sem alterar o sentido da tarefa.
- Medir separadamente chamadas frias e quentes com concorrência representativa.
- Definir escopo de isolamento e invalidar por versão de modelo, template e adaptador.

Aplicação LAI proposta:
Proposta LAI: estabilizar o prefixo das ferramentas e regras recorrentes da Helena e medir a economia antes de expandir o cache.

## T082:C03 — riscos_validacao

Armadilhas:
- Timestamps e ordem variável de ferramentas no início podem destruir os acertos.
- Um acerto reduz computação de entrada; não implica redução proporcional da duração total.

Métricas sugeridas:
- Taxa de tokens de prefixo reaproveitados, além da taxa de requisições com hit.
- Tempo até o primeiro token e latência final em cache frio/quente.

Testes propostos:
- Enviar dois prompts com prefixo igual e sufixos diferentes; verificar redução de prefill sem troca de respostas.
- Alterar o primeiro token e confirmar que o runtime não reutiliza estados incompatíveis.

## T082:C04 — perguntas_proveniencia

Pergunta: Prefix cache aumenta a janela?
Resposta: Não. Reaproveita cálculo; o prefixo continua fazendo parte da sequência atendida.

Pergunta: É igual a response caching?
Resposta: Não. Response caching devolve saída armazenada; prefix caching ainda gera uma nova resposta.

Pergunta: Prefix caching acelera automaticamente o decode?
Resposta: Não. Seu benefício direto é evitar construção repetida de estados do prefixo; a atenção sobre eles continua necessária.

Pergunta: Como comparar caches com blocos diferentes?
Resposta: Use tokens e tempo realmente poupados, além da memória ocupada; uma taxa bruta de hits não é comparável.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T082:C05 — mecanismo_avancado

Um hit de prefixo economiza parte do prefill, mas as consultas do sufixo ainda atendem ao prefixo reutilizado. O benefício depende dos tokens efetivamente cobertos e do custo evitado, não apenas da quantidade de requisições com algum hit. Em caches por blocos completos, um prefixo quase coincidente pode reutilizar menos tokens que seu comprimento textual sugere.

Condição de contorno:
Prompts com conteúdo variável no início ou poucas repetições podem consumir memória de cache sem amortizar sua construção.

Contrato proposto:
- Entradas: Tokens de entrada, identidade do modelo, domínio de compartilhamento e tamanho dos blocos.
- Saídas: Extensão reutilizada e sufixo que ainda necessita processamento.
- Estado: Blocos completos indexados com ancestralidade do prefixo.
- Invariante: O hit termina antes da primeira divergência efetiva de tokens ou identidade.

Compromissos de projeto:
- Reservar prefixos aumenta reúso, mas reduz espaço para sequências ativas.
- Reorganizar prompts só é aceitável quando preserva significado e instruções.

## T082:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: variar um token próximo à fronteira de bloco e alternar templates de chat. Esperar hits apenas nos blocos anteriores compatíveis, com saída equivalente à execução fria.

Plano de avaliação proposto:
Plano proposto: comparar cache frio e aquecido sob a mesma mistura de prompts. Variar tamanho do prefixo e do sufixo, medir tokens reutilizados, TTFT, ocupação e caudas; aprovar pela redução de custo end-to-end sem divergência.

Comparações:
- T088 (complements): O escalonador pode aproveitar menos trabalho de prefill sem eliminar contenção entre requisições.

Afirmação rastreável:
O projeto de prefix caching do vLLM identifica blocos com ancestralidade e armazena somente blocos completos.
Suporte: direct; fontes: B-S005
Limite: Esse detalhe descreve o projeto documentado; outros servidores podem adotar granularidades diferentes.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T082:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mediu hits por tokens e discutiu prefixos comuns. O aprofundamento passa a desenhar famílias de prompts, políticas de retenção e experimentos econômicos, mantendo separados benefício do cache, mudança editorial do prompt e qualidade da tarefa.

Famílias estáveis de prompts
Crie versões explícitas de um prefixo por produto, idioma e conjunto de ferramentas. Coloque conteúdo variável após a região realmente compartilhável, preservando a ordem exigida pelo modelo. Não reúna instruções incompatíveis só para aumentar hits: prefixo mais longo também ocupa contexto e pode aumentar o decode.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

Valor de retenção
Estime valor de um prefixo por custo de prefill evitado vezes probabilidade de revisita, descontando memória ocupada e pressão sobre sequências ativas. Um prefixo popular e barato de reconstruir pode merecer menos espaço que outro caro e recorrente. Atualize a estimativa por classe de tráfego e não por média única.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

Experimento sem confusão causal
Mantenha duas comparações: mesmo prompt com cache ligado/desligado e prompt reorganizado com cache equivalente. A primeira isola o mecanismo; a segunda mede mudança de instruções e posicionamento. Relate cache frio, aquecido e após invalidação, porque o resultado de uma demonstração aquecida não representa implantação recém-iniciada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

USO AVANÇADO — Análise de muitos documentos
Cenário: O mesmo contrato de extração processa documentos independentes.
Estratégia: Versione instruções e exemplos fixos, deixando cada documento no sufixo. Distribua chamadas considerando afinidade e fila. Invalide o prefixo quando mudar schema ou adaptador, mesmo se o texto principal continuar parecido.
Papel do modelo pequeno: Um especialista 3–14B pode atender extração repetitiva com verificação de campos.
Aceite proposto: Aprovar pela combinação de custo por documento válido, TTFT e ausência de mistura entre clientes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

USO AVANÇADO — Chat com ferramentas estáveis
Cenário: As definições de ferramentas se repetem entre turnos.
Estratégia: Canonize a serialização das ferramentas e evite reordenar propriedades sem necessidade. Preserve o tokenizador e template; calcule quanto do prefixo é reutilizado depois de cada resposta. Limite retenção de sessões que não retornam.
Papel do modelo pequeno: Um 15–30B mantém contexto útil sem recalcular tudo a cada turno.
Aceite proposto: Comparar tokens reutilizados e latência nas revisitas, incluindo custo de retenção ociosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, prefira prefixos curtos e frequentes; não infle instruções para criar uma economia artificial de cache.
8–14B: Em 8–14B, organizar famílias por ferramenta e tarefa pode melhorar reutilização sem misturar contratos.
15–30B: Em 15–30B, medir a disputa entre prefixos residentes e KV de conversas longas antes de ampliar retenção.
Requisitos de treino/runtime: É otimização runtime; cache exige identidade de tokens e condições de execução, não similaridade semântica.
Não aplicar quando: Não esperar redução de tokens lógicos na janela nem reuso automático entre workers sem suporte explícito.

## T082:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: O operador afirma que o serviço usa prefix caching.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O relato de serving explicita reuso de prefixos comuns no Hiring Assistant.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passos 1–2: recuperar prefixo KV existente e executar apenas prefill incremental. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: Prefix caching integra os recursos descritos.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Prefixos comuns reutilizam os mesmos nós de KV.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T082:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T082 → T120 [complements]
Como combinar: Encaminhar para um worker com prefixo compatível somente se o ganho superar espera adicional.
Interface: Hash de identidade, comprimento reutilizável e estimativa de fila.
Condição: Métricas estão atualizadas e respeitam isolamento.
Aceite proposto: Comparar afinidade com balanceamento de carga sob rajadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S004, B-S005, V4B-S001, V4B-S004, V4B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T082 → T088 [complements]
Como combinar: Compartilhar prefixos em lotes contínuos sem bloquear admissões por cache ocioso.
Interface: Referências KV e orçamento por iteração.
Condição: Scheduler e cache contabilizam blocos compartilhados uma única vez.
Aceite proposto: Medir concorrência útil e verificar liberação após cancelamento.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Separar taxa de hit de economia efetiva em tokens e tempo.
- Invalidar por revisão do template e testar início frio após implantação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar extração ou atendimento com uma fronteira sob o mesmo nível de qualidade verificável. Prefix caching pode reduzir custo da solução pequena; não recupera conhecimento ausente nem melhora automaticamente a exatidão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T002, T007, T081, T083, T103, T171

## Fontes primárias associadas

### B-S004 — Automatic Prefix Caching

[https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reaproveitamento de prefixos idênticos para evitar prefill repetido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T083 — Advanced Prefix Caching

**Nome canônico:** Advanced Prefix Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Correção terminológica do inventário original  
**ID canônico:** T082  
**Data da curadoria:** 2026-11-05

## T083:C01 — conceito

Rótulo descritivo para variantes sofisticadas de prefix caching, não uma técnica única padronizada. Pode reunir identificação de blocos, compartilhamento entre requisições, isolamento por domínio, políticas de retenção e roteamento. Deve ser decomposto em funcionalidades verificáveis para evitar contar a mesma capacidade várias vezes.

Como funciona:
- Associar cada bloco ao prefixo precedente, tokens e metadados que afetam os estados.
- Compartilhar somente blocos compatíveis dentro do escopo autorizado.
- Gerenciar referências e remoção sem invalidar sequências ainda em uso.

Nota de nomenclatura: Mantido o nome do inventário; classificado como extensão editorial de Prefix Caching.

## T083:C02 — aplicacao

Quando usar:
- Múltiplas sessões usam grandes prefixos repetidos.
- A taxa de acerto local depende de placement e retenção.

Quando não usar:
- Usar o adjetivo avançado como requisito sem especificar comportamento, isolamento e métrica.

Implementação proposta:
- Documentar uma matriz: chave, granularidade, validade, política de despejo e recuperação.
- Incluir modelo, LoRA e modalidade na identidade quando alterarem o cálculo.
- Comparar cada extensão isoladamente contra o prefix caching básico.

Aplicação LAI proposta:
Proposta LAI: usar este registro como checklist de extensões de T082, sem lançar uma segunda infraestrutura com nome diferente.

## T083:C03 — riscos_validacao

Armadilhas:
- Mesmo hash não é prova universal de identidade; serialização e colisões exigem tratamento.
- Compartilhamento entre usuários pode introduzir canais de inferência por tempo, mesmo sem retornar conteúdo alheio.

Métricas sugeridas:
- Economia de prefill por unidade de memória retida.
- Erros de identidade, acertos úteis e custo de manutenção do índice.

Testes propostos:
- Trocar adaptador mantendo o texto e garantir ausência de reaproveitamento incompatível.
- Executar namespaces distintos com prefixo igual e verificar a política explícita de isolamento.

## T083:C04 — perguntas_proveniencia

Pergunta: Existe um algoritmo único chamado Advanced Prefix Caching?
Resposta: Não foi identificado como denominação única; o registro organiza extensões operacionais do cache de prefixos.

Pergunta: Salt resolve autorização inteira?
Resposta: Não. Restringe reutilização no cache compatível; autenticação e autorização continuam necessárias no serviço.

Pergunta: Hash forte elimina todos os erros?
Resposta: Não. Omissão de campos da identidade e referências expiradas são defeitos lógicos independentes de colisões criptográficas.

Pergunta: Uma colisão simulada deve ser ignorada?
Resposta: Não. Ela testa a política de conflito ou a validação secundária, explicitando o comportamento seguro previsto pelo contrato.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T083:C05 — mecanismo_avancado

O índice precisa identificar o contexto que produziu cada bloco, incluindo ancestralidade, adaptadores e entradas multimodais relevantes. Dois prompts com o mesmo token marcador de imagem podem conter imagens diferentes; comparar apenas IDs de tokens produz um falso hit. Como proposta de implementação, referências de blocos devem ser adquiridas antes de sua possível expulsão, com geração de identificador que detecte reutilização de slots.

Condição de contorno:
A designação advanced prefix caching não especifica um protocolo universal; consistência e isolamento devem ser definidos por implementação.

Contrato proposto:
- Entradas: Tokens, hashes de conteúdo multimodal, identidade do adaptador e domínio de cache.
- Saídas: Referências válidas a blocos e explicação verificável dos hits.
- Estado: Índice, contadores de referência e versões de alocação.
- Invariante: Igualdade de chave implica compatibilidade de todo estado que afeta as projeções.

Compromissos de projeto:
- Chaves mais completas exigem computação e metadados adicionais.
- Verificação defensiva reduz falsos hits, porém pode converter possíveis reutilizações em misses.

## T083:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter marcadores iguais e trocar a imagem ou adaptador; também simular referência expirada. Esperar miss ou rejeição explícita, nunca uso silencioso do bloco incompatível.

Plano de avaliação proposto:
Plano proposto: comparar índice simples e identidade completa com entradas multimodais e trocas de adaptador. Medir falsos hits, misses, bytes de metadados e TTFT; exigir ausência de mistura de estados no conjunto controlado.

Comparações:
- T082 (specializes): Acrescenta identidade e ciclo de vida ao reúso básico de prefixos.

Afirmação rastreável:
O desenho do vLLM inclui hashes extras para adaptadores, multimodalidade e salt de cache.
Suporte: direct; fontes: B-S005
Limite: Essa lista documenta uma implementação; não demonstra isolamento completo de qualquer implantação.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T083:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu identidade completa e aquisição segura de referências. Esta ficha transforma o rótulo amplo em uma política multinível de admissão, retenção e observabilidade, para que advanced corresponda a capacidades demonstráveis e não a duplicação de nomes.

Camadas com custo explícito
Separe blocos ativos na GPU, prefixos ociosos retidos e eventual armazenamento secundário. Cada promoção precisa declarar bytes movidos, tempo e compatibilidade. Não presuma que copiar KV da CPU sempre vence recomputar; a comparação depende do comprimento, interconexão, disponibilidade do worker e urgência da requisição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

Admissão resistente à poluição
Um cliente pode enviar muitos prefixos únicos e deslocar conteúdo útil. Adote cotas por domínio, frequência mínima ou retenção limitada para entradas de uma só utilização. A política deve proteger sequências ativas e manter estatísticas por origem, sem transformar um prefixo compartilhado em canal de acesso a conteúdo de outro domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

Métricas por etapa do cache
Exponha busca de identidade, hit lógico, disponibilidade física e tempo de aquisição separadamente. Um índice pode anunciar um bloco que já foi removido ou que ainda está sendo transferido. Registre miss por incompatibilidade, expiração e capacidade; isso permite corrigir a política certa sem atribuir todo fracasso à taxa de hit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

USO AVANÇADO — Serviço com vários adaptadores
Cenário: Clientes usam a mesma base com comportamentos especializados.
Estratégia: Inclua adaptador e revisão na chave, reserve orçamento por grupo e compartilhe somente estados cuja equivalência esteja comprovada. Evite usar o ID do modelo base como chave universal. Teste promoção e invalidação enquanto pedidos antigos ainda executam.
Papel do modelo pequeno: Modelos 3–30B podem compartilhar infraestrutura, mantendo seus estados computacionais separados.
Aceite proposto: Exigir zero falso hit nos testes e custo menor que caches totalmente isolados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

USO AVANÇADO — Retenção entre reinícios
Cenário: Prompts institucionais são caros de reconstruir e muito recorrentes.
Estratégia: Avalie armazenamento secundário para um conjunto pequeno de prefixos validados. Carregue sob demanda, confirme manifesto e descarte artefatos de revisão incompatível. Use TTL como política econômica, não como prova de validade.
Papel do modelo pequeno: Um alvo 15–30B pode economizar prefill se transferência for efetivamente mais barata.
Aceite proposto: Medir retomada fria, bytes transferidos e impacto nas requisições sem reuso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, começar com cache local simples; múltiplas camadas podem adicionar mais coordenação que economia.
8–14B: Em 8–14B, quotas por adaptador e observabilidade de misses tendem a ser prioridades antes de tiering.
15–30B: Em 15–30B, investigar armazenamento secundário somente após medir a pressão KV e a frequência de revisitas.
Requisitos de treino/runtime: Requer recursos concretos do runtime; nome advanced não implica transferência, isolamento ou persistência já implementados.
Não aplicar quando: Não usar índice de similaridade textual para reutilizar tensores exatos nem prometer todas as funções sob um único nome.

## T083:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Hierarquia e prefetch ampliam a política de reutilização de prefixos descrita.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T083:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T083 → T105 [complements]
Como combinar: Aplicar remoção por valor e referência ativa em cada camada de armazenamento.
Interface: Uso recente, custo de reconstrução, bytes e contagem de referências.
Condição: A remoção não toca estado necessário a um decode em andamento.
Aceite proposto: Injetar pressão e verificar que sequências ativas permanecem corretas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S005, V3D-S004, V4B-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T083 → T157 [requires]
Como combinar: Identificar prefixos e versões antes de consultar níveis de cache.
Interface: Hash encadeado, metadados multimodais e domínio de isolamento.
Condição: A serialização da identidade é determinística.
Aceite proposto: Alterar um componente por vez e exigir miss apropriado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S005, V3D-S004, V4B-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Distinguir hit de índice de estado realmente pronto para consumo.
- Limitar promoção de prefixos únicos e testar concorrência na invalidação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo e SLO de workloads recorrentes com uma API de fronteira que ofereça cache documentado. O resultado caracteriza eficiência operacional, sem inferir equivalência de capacidades cognitivas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T104, T105, T120

## Fontes primárias associadas

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S004 — Automatic Prefix Caching — vLLM design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos, hash do prefixo anterior, tokens e fatores adicionais como adaptador, multimodalidade e cache_salt.

Limite: Documentação latest; não comprova configuração instalada nem ganho local.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T084 — Session-Based Caching

**Nome canônico:** Session-Based Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T084  
**Data da curadoria:** 2026-11-05

## T084:C01 — conceito

Padrão de aplicação que associa estados reutilizáveis a uma sessão de conversa. Pode reter KV, resultados ou ambos, mas cada tipo possui validade diferente. Aqui o foco é a continuidade computacional do diálogo; a sessão deve continuar recuperável mesmo que o cache desapareça.

Como funciona:
- Identificar sessão, revisão do histórico e versão do modelo.
- Verificar se a nova entrada realmente continua o prefixo anterior.
- Reusar estados válidos ou reconstruí-los a partir do histórico persistido.

## T084:C02 — aplicacao

Quando usar:
- Conversas com muitos turnos que acrescentam conteúdo ao final.
- Sessões frequentes cujo custo de prefill domina o tempo de resposta.

Quando não usar:
- Usar a sessão como única chave mesmo quando o histórico foi editado ou compactado.

Implementação proposta:
- Separar armazenamento durável da conversa e armazenamento descartável dos estados.
- Adicionar TTL, limite de memória e política de invalidação por revisão.
- Serializar atualizações concorrentes ou usar revisão otimista para impedir bifurcações acidentais.

Aplicação LAI proposta:
Proposta LAI: manter a conversa e o estado de missão fora do cache e usar a sessão apenas como domínio de continuidade e isolamento.

## T084:C03 — riscos_validacao

Armadilhas:
- Afinidade rígida a um worker pode desequilibrar carga.
- Reuso após resumo da conversa é inválido quando os tokens de entrada mudaram.

Métricas sugeridas:
- Acerto por sessão e custo de reconstrução depois de expiração.
- Consumo de memória por sessão ociosa e tempo até primeiro token.

Testes propostos:
- Expirar o cache entre turnos e exigir continuação correta a partir dos dados persistidos.
- Enviar turnos concorrentes e confirmar que revisões não se misturam.

## T084:C04 — perguntas_proveniencia

Pergunta: Fechar o servidor deve apagar a conversa?
Resposta: Não. A conversa deve sobreviver na persistência; somente a aceleração computacional pode ser perdida.

Pergunta: Uma sessão autoriza reuso após edição?
Resposta: Não. A revisão do histórico e a identidade dos tokens também precisam coincidir.

Pergunta: Pode salvar apenas o cache como memória?
Resposta: Isso dificulta auditoria e migração; preserve também o histórico necessário para reconstruir estados compatíveis.

Pergunta: O cancelamento apaga todos os tokens gerados?
Resposta: O contrato precisa distinguir tokens já confirmados dos provisórios e definir precisamente qual revisão permanece válida.

Escopo das fontes:
A fonte cobre objetos de cache e reuso; gestão de sessão, revisões e TTL são arquitetura editorial proposta.

## T084:C05 — mecanismo_avancado

O estado de sessão precisa distinguir histórico confirmado de geração em andamento. Uma edição de mensagem ou ramificação muda a ancestralidade, enquanto uma resposta atrasada ainda pode tentar gravar no cache antigo. Um contrato editorial robusto associa sessão, revisão e identidade do modelo, confirmando atualizações apenas quando a revisão esperada permanece válida. Mensagens persistidas são a fonte de reconstrução; o cache é descartável.

Condição de contorno:
Persistência de conversa não implica persistência de tensores; reinícios e mudanças de configuração podem exigir reconstrução integral.

Contrato proposto:
- Entradas: Identificador da sessão, revisão esperada, histórico tokenizado e extensão solicitada.
- Saídas: Nova revisão confirmada ou conflito explícito, com continuação correspondente.
- Estado: Histórico durável separado dos estados de atenção e operações pendentes.
- Invariante: Uma operação atrasada nunca sobrescreve silenciosamente uma ramificação mais recente.

Compromissos de projeto:
- Manter várias ramificações aumenta memória, mas evita reconstruções frequentes.
- Serializar todas as operações simplifica consistência e pode reduzir concorrência útil.

## T084:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar duas continuações, editar a mensagem anterior e concluir a primeira por último. Esperar conflito de revisão ou cache isolado, sem associar sua resposta à nova conversa.

Plano de avaliação proposto:
Plano proposto: comparar execução sem cache e cache por revisão em sessões lineares e ramificadas. Medir reconstruções, bytes residentes, latência e conflitos; aceitar apenas respostas equivalentes para o mesmo histórico confirmado.

Comparações:
- T081 (complements): A consistência de sessão controla quando o estado incremental pode ser reutilizado.

Afirmação rastreável:
O cache armazena estados derivados de tokens processados, permitindo continuação sem refazer suas projeções.
Suporte: related; fontes: V3B-S005
Limite: A documentação sustenta o mecanismo de cache; revisão transacional de sessão é proposta de integração, não API padronizada.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T084:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculou cache à revisão do histórico. A nova proposta explicita leases, tentativas concorrentes e políticas de mobilidade, evitando que afinidade de sessão se torne dependência permanente de um worker ou uma fonte de resultados atrasados.

Lease de continuação
Associe a execução em andamento a uma revisão esperada e a um lease de duração limitada. A conclusão só confirma o novo estado se ambos continuarem válidos. Um pedido lento que retorna depois de edição do usuário deve ser registrado como tentativa obsoleta, sem sobrescrever a ramificação atual da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

Afinidade com saída de emergência
Afinidade melhora a chance de encontrar KV, mas precisa poder ceder a indisponibilidade ou fila excessiva. Guarde o histórico confirmado fora do worker e defina quando vale reconstruir em outro destino. Uma sessão pode manter identidade estável enquanto seu estado computacional muda de localização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

Contabilidade de sessão ociosa
Faça retenção depender do intervalo de revisita, do tamanho do cache e da prioridade da sessão. Sessões curtas e frequentes podem ser baratas de manter; uma conversa longa abandonada pode expulsar várias sessões úteis. Registre retomadas e reconstruções para ajustar a política, preservando a possibilidade de voltar sem o cache.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

USO AVANÇADO — Assistente interrompido pelo usuário
Cenário: O usuário cancela uma resposta e envia correção imediatamente.
Estratégia: Cancele a tentativa antiga, confirme somente tokens que a política de conversa considera aceitos e abra nova revisão. Não reutilize automaticamente o trecho gerado e não entregue uma conclusão tardia como se respondesse à correção.
Papel do modelo pequeno: Um modelo 3–14B pode manter interação rápida com estado lógico pequeno e explícito.
Aceite proposto: Testar corridas entre cancelamento, fim da geração e nova mensagem sem mistura de revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

USO AVANÇADO — Sessão móvel entre máquinas
Cenário: Um serviço precisa drenar workers para atualização.
Estratégia: Pare novas admissões no worker antigo, preserve estados confirmados e escolha transferência suportada ou replay dos tokens. Permita concluir requisições em voo ou cancelar com razão explícita; nunca tratar cache ausente como perda da sessão.
Papel do modelo pequeno: Um modelo 15–30B pode exigir reconstrução planejada para manter a cauda aceitável.
Aceite proposto: Medir sucesso de retomada, duplicação de respostas e tempo de drenagem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, replay de uma conversa curta pode ser mais simples que infraestrutura de migração de KV.
8–14B: Em 8–14B, manter cache de sessões ativas e externalizar histórico permite mobilidade com custo previsível.
15–30B: Em 15–30B, planejar retenção e drenagem por bytes KV, não somente por quantidade de sessões.
Requisitos de treino/runtime: Runtime fornece cache e cancelamento; aplicação fornece revisão, histórico durável e semântica de confirmação.
Não aplicar quando: Não presumir afinidade garantida pelo balanceador nem usar ID de sessão como autorização suficiente.

## T084:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Afinidade por sessão aumenta chance de cache, mas não demonstra todo o contrato de revisão de sessão da ficha.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T084:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T084 → T064 [requires]
Como combinar: Persistir histórico confirmado e artefatos antes de depender do cache de sessão.
Interface: ID estável, revisão e resultados aceitos.
Condição: Estado durável pode reconstruir a entrada exata.
Aceite proposto: Excluir todo KV e retomar sem repetir ferramentas concluídas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, V4B-S004, V3D-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T084 → T120 [complements]
Como combinar: Escolher destino com afinidade enquanto fila e saúde permanecem adequadas.
Interface: Localização preferida, validade do lease e atraso previsto.
Condição: Roteador dispõe de fallback e não confunde afinidade com exclusividade.
Aceite proposto: Derrubar o destino preferido e verificar retomada controlada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, V4B-S004, V3D-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Rejeitar commit de tentativa com revisão vencida.
- Testar perda de worker durante streaming e não publicar fragmentos obsoletos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar continuidade de uma missão em condições de falha frente a uma baseline de fronteira. Cache reduz recomputação; qualidade da recuperação depende dos contratos de estado e não do número de parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T082, T154, T064

## Fontes primárias associadas

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T085 — Quantization

**Nome canônico:** Quantization  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T085  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** quantização

## T085:C01 — conceito

Família de representações numéricas que usa menos bits para pesos, ativações ou cache. Reduz armazenamento e pode reduzir tráfego de memória, mas ganho de velocidade depende de kernels compatíveis. Precisão do peso, precisão do cálculo e precisão do KV são decisões distintas.

Como funciona:
- Escolher tensores e grupos que receberão representação de menor precisão.
- Definir escalas, arredondamento e eventual ponto zero ou formato flutuante.
- Executar kernels que interpretem o formato, mantendo algumas operações em precisão maior quando necessário.

## T085:C02 — aplicacao

Quando usar:
- Modelo ou concorrência limitados por memória.
- Hardware com execução eficiente para o esquema escolhido.

Quando não usar:
- Escolher a menor quantidade de bits sem avaliar erro de tarefa e suporte real do runtime.

Implementação proposta:
- Criar baseline em precisão de referência e um conjunto de tarefas representativas.
- Quantizar com dados de calibração quando o método exigir e registrar sua procedência.
- Comparar arquivos, memória real, throughput e acerto no mesmo ambiente.

Aplicação LAI proposta:
Proposta LAI: escolher a quantização pelo custo de uma missão correta, incluindo retries e fallback, e não apenas por tokens por segundo.

## T085:C03 — riscos_validacao

Armadilhas:
- Arquivo pequeno não garante pequena memória total: KV, buffers e desquantização continuam existindo.
- Perplexidade semelhante pode esconder piora em ferramentas, números ou respostas estruturadas.

Métricas sugeridas:
- Memória de pico, tamanho do artefato e tempo por token.
- Taxa de acerto por tarefa e erros críticos frente ao baseline.

Testes propostos:
- Executar casos de extração exata e chamadas de ferramenta; exigir limite de regressão previamente definido.
- Testar maior contexto e concorrência pretendidos, incluindo aquecimento e operações temporárias.

## T085:C04 — perguntas_proveniencia

Pergunta: INT4 sempre é quatro vezes mais rápido que FP16?
Resposta: Não. A relação de bits dos pesos não determina a velocidade de todo o sistema.

Pergunta: Quantizar é treinar novas habilidades?
Resposta: Não. Em geral é reduzir a precisão de uma habilidade já aprendida, com possível perda.

Pergunta: Menos bits significam menos latência?
Resposta: Somente quando o caminho de execução explora a representação e a economia supera conversões e outros gargalos.

Pergunta: Uma escala serve para todos os contextos?
Resposta: Pode servir ao contrato escolhido, mas sua adequação deve ser testada também em distribuições diferentes da calibração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T085:C05 — mecanismo_avancado

O orçamento de armazenamento depende de dados e metadados. Para N valores, b bits por valor, grupos de g valores e m bytes de escala ou zero por grupo, uma estimativa é N·b/8 + ceil(N/g)·m, antes de alinhamento e tensores mantidos em precisão maior. O dtype de armazenamento também não determina sozinho o dtype da multiplicação ou a velocidade do kernel.

Condição de contorno:
Reduzir bits pode apenas liberar capacidade quando descompactação, conversões ou operadores não quantizados dominam o tempo total.

Contrato proposto:
- Entradas: Pesos, dados de calibração quando exigidos, granularidade e kernel pretendido.
- Saídas: Artefato quantizado e relatório de erro, tamanho e operadores efetivamente usados.
- Estado: Escalas, zeros, layout, versão do artefato e tensores preservados.
- Invariante: A avaliação identifica precisamente quais valores foram quantizados e onde ocorre arredondamento.

Compromissos de projeto:
- Grupos menores adaptam melhor escalas, mas aumentam metadados.
- Calibração representativa custa trabalho e pode não cobrir mudanças de domínio.

## T085:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir ativações com outliers ausentes da calibração e verificar saturação, erro de logits e tarefa final. O simples carregamento do modelo não deve aprovar a conversão.

Plano de avaliação proposto:
Plano proposto: comparar com o mesmo checkpoint em maior precisão, controlando amostragem e backend. Separar memória de pesos, cache e temporários; medir qualidade, prefill e decode. Aceitar pela fronteira observada entre custo e perda tolerável.

Comparações:
- T086 (distinct_from): Quantizar pesos e quantizar cache modificam tensores e erros diferentes.

Afirmação rastreável:
SmoothQuant usa uma transformação equivalente para deslocar dificuldade de quantização das ativações para os pesos.
Suporte: direct; fontes: V3B-S003
Limite: A equivalência antecede a quantização; o arredondamento posterior continua sendo aproximado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T085:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 contabilizou metadados e distinguiu armazenamento de cálculo. Agora a decisão usa orçamento de erro por componente, mudança de domínio e qualidade pós-integração, tratando compressão como uma sequência de experimentos reversíveis e não como escolha isolada de bits.

Orçamento de erro composto
Separe os efeitos de quantizar pesos, ativações e KV. Teste cada alteração individualmente antes de combinar, pois pequenas perdas podem interagir em respostas longas ou raras. Defina quais erros são toleráveis por tarefa: falha de sintaxe, troca de entidade, omissão de exceção e erro numérico não têm o mesmo custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

Calibração como amostragem do uso
Construa um conjunto de calibração que represente comprimentos, idiomas e padrões de ferramentas. Reserve domínios e períodos posteriores para validação. Uma conversão excelente em texto geral pode distorcer canais importantes para código, números ou terminologia especializada; nenhum pequeno conjunto comprova robustez universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

Escolha pelo sistema final
Meça peso carregado, buffers temporários, cache e tempo de desquantização no runtime de destino. Uma representação mais compacta pode perder para outra com kernel melhor. Avalie também tempo de carregamento e capacidade de manter réplicas, porque o benefício operacional pode vir de maior concorrência, mesmo sem acelerar uma requisição isolada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

USO AVANÇADO — Especialista local de extração
Cenário: O modelo precisa caber em um dispositivo com orçamento fixo.
Estratégia: Compare uma base menor em maior precisão e uma base maior quantizada. Preserve o mesmo conjunto de documentos e verificador de campos. Escolha por resultados válidos dentro de prazo, incluindo entradas longas e categorias raras.
Papel do modelo pequeno: A faixa 3–7B pode vencer pela simplicidade; 8–14B só merece compressão se acrescentar qualidade mensurável.
Aceite proposto: Aceitar perda dentro do limite pré-definido por classe, sem ocultar regressões na média.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

USO AVANÇADO — Serviço de múltiplos especialistas
Cenário: Vários modelos ou adaptadores disputam memória de GPU.
Estratégia: Quantize primeiro componentes que liberam capacidade suficiente para aumentar réplicas ou reduzir preempção. Depois verifique comportamento combinado com cache e batching. Mantenha artefato de referência para reverter conversões problemáticas.
Papel do modelo pequeno: Um 15–30B pode tornar-se viável, mas memória total continua incluindo estados e temporários.
Aceite proposto: Comparar custo por tarefa aceita e SLO sob carga, não apenas tamanho do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preservar qualidade em tarefas estreitas pode importar mais que obter a menor representação possível.
8–14B: Em 8–14B, comparar técnicas com calibração do domínio e kernels realmente disponíveis no executor escolhido.
15–30B: Em 15–30B, quantização pode decidir viabilidade de memória; incluir margem para contexto e concorrência.
Requisitos de treino/runtime: PTQ usa calibração quando o método exige; QAT demanda treinamento; formatos e kernels devem ser compatíveis.
Não aplicar quando: Não reduzir bits de todos os tensores por padrão nem anunciar economia de memória como ganho equivalente de velocidade.

## T085:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Pilha Phi Silica publicada descreve quantização de pesos, com ressalva de revisão. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: A descrição técnica especifica quantização do modelo local.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006.

## T085:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T085 → T198 [complements]
Como combinar: Recalibrar o critério de confiança após a conversão, pois probabilidades podem mudar.
Interface: Predições, rótulos independentes e revisão do artefato quantizado.
Condição: Há dados de validação fora da calibração numérica.
Aceite proposto: Comparar risco seletivo e taxa de abstenção antes/depois.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S006, V3B-S003, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T085 → T107 [complements]
Como combinar: Verificar se a redução de tráfego desloca o gargalo para cálculo ou conversão.
Interface: Bytes movimentados, kernels e latência por fase.
Condição: Profiler mede a execução real do formato escolhido.
Aceite proposto: Explicar a diferença entre ganho de capacidade e ganho de tempo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S006, V3B-S003, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Guardar base, receita de conversão e hashes do conjunto de calibração.
- Testar combinações de precisão, inclusive respostas longas e valores extremos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas especializadas contra a fronteira com o mesmo critério de correção. Compressão pode reduzir custo mantendo qualidade suficiente naquele recorte; não demonstra equivalência geral nem imunidade a erros raros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T086, T123, T124, T125, T126, T127

## Fontes primárias associadas

### B-S006 — Quantization — Overview

[https://huggingface.co/docs/transformers/main/en/quantization/overview](https://huggingface.co/docs/transformers/main/en/quantization/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Redução de bits para pesos e eventualmente ativações; necessidade de escolher formato e método compatíveis.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S003 — SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models

[https://arxiv.org/abs/2211.10438](https://arxiv.org/abs/2211.10438)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reescala equivalente antes da quantização e migração de dificuldade das ativações para pesos.

Limite: Resumo consultado; equivalência da reparametrização não elimina erro de arredondamento posterior.

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


---

# T086 — Quantized KV Cache

**Nome canônico:** Quantized KV Cache  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T086  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** quantização de cache KV

## T086:C01 — conceito

Armazena chaves e valores da atenção com menos bits que a representação de referência. O objetivo principal é reduzir memória por token, podendo acomodar mais sequências ou contexto. Isso é independente de quantizar os pesos e introduz erro numérico nos estados consultados pela atenção.

Como funciona:
- Converter KV para o formato configurado usando escalas adequadas.
- Guardar os estados comprimidos e seus metadados necessários.
- Consumir o cache em kernel compatível, com cálculo quantizado ou conversão conforme backend.

## T086:C02 — aplicacao

Quando usar:
- KV domina o consumo de memória por contexto ou concorrência.
- Avaliações mostram tolerância do modelo à precisão escolhida.

Quando não usar:
- Modelo, tipo de atenção ou backend não suporta o formato com correção comprovada.

Implementação proposta:
- Medir separadamente memória de pesos, KV e buffers antes da mudança.
- Calibrar escalas com entradas do domínio quando o caminho escolhido permitir.
- Comparar tarefas longas e curtas, especialmente recuperação de detalhes distantes.

Aplicação LAI proposta:
Proposta LAI: testar KV quantizado apenas se o perfil de memória revelar esse gargalo; preservar a configuração validada do checkpoint como baseline.

## T086:C03 — riscos_validacao

Armadilhas:
- Ganhar capacidade de cache não implica acelerar a latência de uma requisição.
- Escalas ruins podem deteriorar atenção; pesos INT4 não tornam KV automaticamente INT4.

Métricas sugeridas:
- Bytes por token e máximo de sequências estáveis.
- Acerto em detalhes de contexto longo e latência sob carga.

Testes propostos:
- Executar a mesma tarefa com KV de referência e KV quantizado em vários comprimentos; avaliar regressões por faixa.
- Forçar valores extremos e verificar ausência de NaN e saturações anormais.

## T086:C04 — perguntas_proveniencia

Pergunta: Preciso quantizar os pesos também?
Resposta: Não. As decisões são separadas, desde que o runtime aceite a combinação.

Pergunta: KV menor aumenta o contexto treinado do modelo?
Resposta: Não. Aumenta capacidade operacional de armazenamento; não cria competência para posições não validadas.

Pergunta: Redução teórica de bits basta para estimar capacidade?
Resposta: Não. Escalas, alinhamento, cópias temporárias e partes não quantizadas também ocupam memória.

Pergunta: Por que medir qualidade em contexto longo?
Resposta: A atenção pode depender de poucos estados distantes; erro pequeno médio pode ocultar falha relevante de recuperação.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T086:C05 — mecanismo_avancado

Erros nas chaves alteram produtos consulta-chave e a distribuição do softmax; erros nos valores alteram a combinação ponderada resultante. Por isso, os eixos de quantização podem ser diferentes. A análise do KIVI favorece chaves por canal e valores por token nos cenários estudados. O custo real inclui escalas, agrupamento, conversões e eventual região recente mantida em precisão maior.

Condição de contorno:
Contextos curtos ou lotes pequenos podem não amortizar quantização e desquantização, mesmo que o número de bytes diminua.

Contrato proposto:
- Entradas: Estados K e V, agrupamento, escalas e política para a região recente.
- Saídas: Cache comprimido acompanhado de metadados suficientes para leitura correta.
- Estado: Posições lógicas, fronteiras de grupos e dtype por segmento.
- Invariante: Nunca interpretar metadados de uma camada ou grupo como pertencentes a outro.

Compromissos de projeto:
- Menos memória permite mais concorrência, mas essa concorrência pode elevar latência individual.
- Granularidade fina reduz erro local e aumenta custo de escalas.

## T086:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um valor extremo e uma evidência importante distante no contexto. Comparar recuperação e logits com cache de maior precisão, verificando se a degradação se concentra em posições específicas.

Plano de avaliação proposto:
Plano proposto: manter pesos e prompts fixos e variar somente a representação KV. Medir bytes completos, tempo de conversão, TTFT, latência entre tokens e qualidade em diferentes comprimentos; aprovar conforme orçamento e perda previamente definidos.

Comparações:
- T085 (complements): A quantização de pesos pode coexistir, mas seus ganhos não devem ser multiplicados sem medição.

Afirmação rastreável:
O KIVI propõe tratamento assimétrico dos eixos de quantização de chaves e valores.
Suporte: direct; fontes: V3B-S002
Limite: A observação dos autores não garante que o mesmo agrupamento seja ótimo para toda arquitetura.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T086:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou eixos de quantização de chaves e valores. O novo desenho considera qualidade conforme idade dos tokens, admissão de sessões e propagação de erro, separando aumento de capacidade do cache de melhora perceptível ao usuário.

Erro ao longo da conversa
Avalie o cache em turnos sucessivos, não somente em uma resposta isolada. Um detalhe antigo pode ser consultado muito depois de sua quantização. Organize testes por distância entre evidência e pergunta, incluindo correções contraditórias, entidades parecidas e instruções que mudam o significado de uma passagem anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S002, B-S007, V4D-S002.

Reserva recente e promoção
Quando o backend suportar região recente em maior precisão, trate seu tamanho como parâmetro de serviço. Uma região maior protege interações recentes, mas consome memória e adiciona conversão ao envelhecer. Meça esse custo de promoção; não conclua que manter o último trecho exato preserva toda a resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S002, B-S007, V4D-S002.

Capacidade entregue
Use bytes economizados para uma decisão observável: aumentar contexto admitido, concorrência ou margem contra preempção. Escolha apenas uma variável por experimento inicial. Se todas crescerem ao mesmo tempo, a análise não distinguirá piora de qualidade numérica de aumento de interferência e pressão de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S002, B-S007, V4D-S002.

USO AVANÇADO — Conversas com evidência distante
Cenário: Um assistente precisa recuperar condições citadas muitos turnos antes.
Estratégia: Fixe pesos e política de contexto, altere somente o formato KV e faça perguntas em diferentes distâncias. Rejeite formatos que perdem exceções relevantes mesmo se a pontuação média permanecer estável.
Papel do modelo pequeno: Um 3–14B deve manter evidências externas disponíveis para conferir respostas quando a memória computacional é aproximada.
Aceite proposto: Comparar exatidão por distância e tipo de informação, juntamente com bytes efetivamente poupados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S002, B-S007, V4D-S002.

USO AVANÇADO — Pico de sessões simultâneas
Cenário: A memória KV limita novas admissões antes de saturar o cálculo.
Estratégia: Quantize o cache suportado e aumente concorrência em etapas. Observe conversão, preempção e intervalos de streaming. Se o ganho de capacidade provocar cauda pior, mantenha parte da economia como reserva.
Papel do modelo pequeno: Um 15–30B pode atender mais sessões, sem que isso implique decode individual mais rápido.
Aceite proposto: Aprovar pelo número de sessões que cumprem qualidade e prazo, não pela ocupação máxima.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S002, B-S007, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, o cache pode superar pesos em contextos longos; medir a composição antes de priorizar peso quantizado.
8–14B: Em 8–14B, testar variações de contexto e idiomas com o mesmo checkpoint para localizar regressões de longo alcance.
15–30B: Em 15–30B, projetar admissão com bytes reais por token, incluindo escalas e regiões não quantizadas.
Requisitos de treino/runtime: É runtime apenas quando há cache e kernel compatíveis; a política assimétrica do KIVI não é propriedade de qualquer FP8.
Não aplicar quando: Não aplicar redução de precisão sem medir tarefas que dependem de tokens antigos ou quando o executor recopia tudo em alta precisão.

## T086:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: KV do modelo local é quantizado a 8 bits.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006.

## T086:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T086 → T088 [complements]
Como combinar: Converter economia KV em um limite controlado de sequências ativas.
Interface: Memória livre, crescimento por token e limites de admissão.
Condição: Scheduler reconhece o tamanho físico do formato.
Aceite proposto: Comparar sessões dentro do SLO com a mesma mistura de comprimentos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S002, B-S007, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T086 → T085 [complements]
Como combinar: Validar combinação de pesos e cache quantizados depois dos experimentos isolados.
Interface: Receitas de conversão e matriz de resultados por precisão.
Condição: Nenhuma mudança simultânea de modelo ou prompt.
Aceite proposto: Detectar perdas conjuntas que os testes separados não previram.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S002, B-S007, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Incluir escalas, buffers e promoção nas contas de memória.
- Não usar perplexidade média como único teste de manutenção de evidências.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar atendimento com contexto longo diante de uma fronteira, igualando tarefa e evidência disponível. KV menor amplia capacidade operacional; aproximar estados não cria capacidade cognitiva nem corrige alucinações.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T085, T123, T100

## Fontes primárias associadas

### B-S007 — Quantized KV Cache

[https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: KV em baixa precisão e calibração de escalas; suporte condicionado ao backend.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S002 — KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache

[https://arxiv.org/abs/2402.02750](https://arxiv.org/abs/2402.02750)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quantização assimétrica de chaves por canal e valores por token.

Limite: Resumo e metadados consultados; resultados dependem dos modelos e configurações estudados.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T087 — Batching — Static Batching e Dynamic Batching

**Nome canônico:** Static Batching e Dynamic Batching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T087  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Batching; processamento em lotes; lote estático; lote dinâmico

## T087:C01 — conceito

Batching reúne entradas compatíveis para executar operações conjuntamente. Static Batching forma um lote definido antes da execução, frequentemente pelo cliente ou por uma fila de trabalho. Dynamic Batching reúne requisições que chegam ao servidor conforme capacidade e espera permitida. Continuous Batching, descrito em T088, muda a composição durante os passos de geração e merece avaliação separada.

Como funciona:
- No lote estático, selecionar previamente as entradas, executar e mapear cada saída ao seu identificador.
- No lote dinâmico, acumular requisições elegíveis e despachar ao atingir tamanho, disponibilidade ou prazo de espera.
- Manter compatibilidade de modelo, shapes e opções exigidas pelo backend; tamanhos maiores podem exigir mais memória e padding.

## T087:C02 — aplicacao

Quando usar:
- Processamento offline de muitas entradas ou tráfego concorrente suficiente para aproveitar execução conjunta dentro do orçamento de latência.

Quando não usar:
- Quando esperar outras requisições viola o prazo ou entradas incompatíveis não podem compartilhar a execução.

Implementação proposta:
- Proposta: começar com limite de lote e espera zero; medir a curva de throughput e latência antes de aumentar a janela de agregação.
- Separar tempo na fila de tempo de inferência e testar distribuição real de comprimentos; agrupar comprimentos próximos quando padding dominar o custo.
- Definir fila máxima, cancelamento e identificação de respostas; garantir que um item não receba a saída de outro.
- Para modelos stateful, confirmar suporte ao agrupamento de sequências; o batcher dinâmico genérico do Triton destina-se a modelos stateless.

Aplicação LAI proposta:
Proposta LAI: escolher separadamente batching offline para ingestão e batching do servidor para inferência interativa; os limites dependem de medições locais ainda não realizadas.

## T087:C03 — riscos_validacao

Armadilhas:
- Um benchmark com lote sempre cheio não representa tráfego esparso.
- Aumento do throughput pode coexistir com piora de p95 e pico de memória.

Métricas sugeridas:
- Requisições por segundo, tamanho efetivo dos lotes, tempo em fila, p95/p99 e utilização de memória.

Testes propostos:
- Teste proposto: comparar lote estático fixo com chegadas esparsas e em rajada no dinâmico, mantendo modelo e entradas.
- Cancelar um item enfileirado e conferir correspondência, completude e isolamento das respostas restantes.

## T087:C04 — perguntas_proveniencia

Pergunta: Dynamic Batching é automaticamente Continuous Batching?
Resposta: Não. O primeiro forma lotes a partir de chegadas; o segundo admite e retira sequências entre passos de geração.

Pergunta: Um lote maior sempre é melhor?
Resposta: Não. Pode aumentar espera, padding e memória. A configuração deve atender simultaneamente throughput e metas de latência.

Pergunta: Lote maior é sempre mais eficiente?
Resposta: Não. Memória, formas, preenchimento e custo das operações podem mudar a região eficiente.

Pergunta: Qual throughput contabilizar?
Resposta: Trabalho útil concluído, acompanhado de erros e tempo de espera; posições de padding não representam serviço entregue.

Escopo das fontes:
Triton fundamenta formação dinâmica e controles de fila. Comparação e critérios LAI são propostas.

## T087:C05 — mecanismo_avancado

A latência observada combina espera na fila e serviço do lote. Aumentar a janela de agregação pode melhorar utilização e simultaneamente piorar respostas em tráfego esparso. Em um lote retangular com padding, sum(comprimentos)/(número_de_sequências·maior_comprimento) estima a fração de posições úteis; essa conta descreve desperdício estrutural, não prevê diretamente o tempo de um kernel com caminhos especializados.

Condição de contorno:
Agregação dinâmica de requisições independentes não resolve automaticamente o estado autoregressivo nem substitui escalonamento por iteração.

Contrato proposto:
- Entradas: Requisições com identidade, forma, prazo e instante de chegada.
- Saídas: Lotes compatíveis e respostas associadas aos solicitantes corretos.
- Estado: Fila, deadline original, limites de tamanho e cancelamentos.
- Invariante: Novas chegadas não reiniciam indefinidamente o prazo da requisição mais antiga.

Compromissos de projeto:
- Esperar mais aumenta oportunidades de agregação e custo de fila.
- Agrupar por comprimento reduz padding, mas pode postergar classes pouco frequentes.

## T087:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar rajadas e longos intervalos, incluindo uma requisição extensa e cancelamentos. Esperar cumprimento do limite de espera e ausência de troca de respostas após reordenação.

Plano de avaliação proposto:
Plano proposto: comparar execução individual, lotes fixos e agregação dinâmica com mesma chegada e hardware. Medir espera, serviço, throughput útil, padding e latências de cauda; aceitar configuração apenas dentro do objetivo de serviço de cada classe.

Comparações:
- T088 (distinct_from): Continuous batching altera participantes entre iterações, além de formar lotes na entrada.

Afirmação rastreável:
O Triton permite limitar o atraso para juntar requisições e envia o lote disponível quando o prazo termina.
Suporte: direct; fontes: B-S047
Limite: A documentação recomenda esse batcher para modelos sem estado; integração autoregressiva exige cuidados adicionais.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T087:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou espera de lote e desperdício de padding. A expansão concentra-se em controle de admissão, mistura de prioridades e medição sob chegadas realistas, para que throughput alto não esconda filas crescentes ou resultados entregues fora de prazo.

Tráfego aberto versus fechado
Um ensaio que envia a próxima requisição somente após receber a anterior limita artificialmente a fila. Para avaliar serviço, reproduza chegadas independentes, rajadas e períodos esparsos. Mantenha também um teste fechado para capacidade individual, mas não use sua latência como promessa de comportamento sob demanda externa crescente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

Lotes por compatibilidade real
Agrupe por modelo, formato de entrada e restrições do backend, preservando identificadores individuais. Separar comprimentos pode reduzir desperdício, mas criar filas demais deixa lotes pequenos esperando. Escolha poucas classes justificadas por distribuição observada e imponha prazo máximo de espera mesmo quando o lote ideal não se completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

Contabilidade de entrega
Meça itens concluídos corretamente por unidade de tempo, com contagem de rejeições, expirados e cancelados. O throughput do acelerador pode crescer enquanto a taxa de resultados úteis cai. Para jobs offline, registre progresso durável por item; repetir um lote após falha não deve duplicar gravações já confirmadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

USO AVANÇADO — Enriquecimento de catálogo
Cenário: Milhões de registros independentes precisam de classificação ou extração.
Estratégia: Use lotes estáticos para partições conhecidas, ordene por comprimento quando permitido e grave saída vinculada ao ID original. Faça retries apenas dos itens sem conclusão verificável. Preserve uma amostra temporal fora da otimização.
Papel do modelo pequeno: Um 3–14B especializado pode executar grande volume com validação determinística de campos.
Aceite proposto: Aprovar por custo por registro válido e prazo do job, incluindo retrabalho e persistência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

USO AVANÇADO — Endpoint com demanda irregular
Cenário: Chamadas interativas chegam em picos curtos.
Estratégia: Use agregação dinâmica com janela limitada por prazo. Se a fila crescer, rejeite ou encaminhe antes de acumular atraso irrecuperável. Separe pedidos urgentes de processamento adiado somente quando houver capacidade garantida para ambos.
Papel do modelo pequeno: Um 15–30B pode amortizar pesos com lotes, mas não deve atrasar indefinidamente requisições pequenas.
Aceite proposto: Comparar distribuição de espera e serviço por classe, com carga aberta e cancelamentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S047, V4B-S008, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, overhead de rede e tokenização pode dominar; medir lotes pequenos antes de buscar máxima ocupação.
8–14B: Em 8–14B, poucas faixas de comprimento ajudam a explorar eficiência sem fragmentar excessivamente a demanda.
15–30B: Em 15–30B, aumentar lote exige reservar KV e buffers, além de caberem os pesos.
Requisitos de treino/runtime: Batching é runtime; embeddings, classificação e geração têm perfis diferentes e não compartilham automaticamente o mesmo scheduler.
Não aplicar quando: Não usar lote fixo para tarefas com prazos incompatíveis nem comparar throughput offline com latência interativa.

## T087:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: O relato de serving de query understanding identifica batching no cliente e servidor.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T087:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T087 → T088 [alternative]
Como combinar: Trocar o lote fechado por composição por iteração quando comprimentos de geração variam muito.
Interface: Fila de requisições e estados independentes.
Condição: O runtime suporta entrada e saída de sequências ativas.
Aceite proposto: Comparar utilidade entregue com a mesma chegada e orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S047, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T087 → T162 [complements]
Como combinar: Confirmar cada resultado por chave idempotente antes de marcar o lote concluído.
Interface: ID do item, revisão da entrada e hash da saída.
Condição: Há armazenamento com deduplicação de commits.
Aceite proposto: Falhar após gravação parcial e verificar que nenhum efeito é repetido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S047, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não excluir timeouts da estatística principal de latência.
- Preservar correspondência entre item e saída após reordenação por comprimento.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar classificação ou extração em lote com uma fronteira usando o mesmo conjunto e orçamento de erro. Batching permite economia operacional do pequeno modelo; não corrige categorias que ele não aprende.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T137, P009

## Fontes primárias associadas

### B-S047 — Batchers — NVIDIA Triton Inference Server

[https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Batching dinâmico agrupa requisições compatíveis e permite controlar espera e filas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T088 — Continuous Batching

**Nome canônico:** Continuous Batching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T088  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** iteration-level scheduling; in-flight batching

## T088:C01 — conceito

Escalonamento que recompõe o lote durante a geração: sequências terminadas saem e novas requisições entram entre iterações. Evita esperar o texto mais longo de um lote fixo para admitir trabalho novo. Exige gerenciamento independente do estado de cada sequência.

Como funciona:
- Executar uma iteração das sequências admitidas.
- Remover finalizadas ou canceladas e reservar memória para novas admissões.
- Montar a próxima iteração respeitando orçamento de tokens e estados ativos.

## T088:C02 — aplicacao

Quando usar:
- Servidor recebe requisições com comprimentos muito diferentes.
- Vários usuários compartilham um modelo com geração autorregressiva.

Quando não usar:
- Admitir sequências além da memória disponível esperando que todas terminem rapidamente.

Implementação proposta:
- Definir limites de sequências, tokens por passo e reserva para crescimento de KV.
- Medir carga com chegadas reais, não somente um lote enviado de uma vez.
- Separar métricas de espera, prefill e decode e preservar cancelamento por requisição.

Aplicação LAI proposta:
Proposta LAI: validar capacidade simultânea de atendimento com distribuição real de duração, preservando um orçamento mais restrito para interação por voz.

## T088:C03 — riscos_validacao

Armadilhas:
- Mais sequências podem aumentar throughput e piorar o intervalo entre tokens.
- Uma política voltada apenas a throughput pode deixar requisições longas esperando indefinidamente.

Métricas sugeridas:
- Goodput: requisições concluídas dentro dos limites de latência.
- Taxa de preempção, espera p95 e ocupação de KV.

Testes propostos:
- Intercalar respostas curtas e longas e confirmar que vagas são reutilizadas antes do término de todas.
- Aplicar sobrecarga e verificar fila limitada e ausência de starvation conforme a política definida.

## T088:C04 — perguntas_proveniencia

Pergunta: É apenas aumentar batch_size?
Resposta: Não. O conjunto de sequências muda entre iterações; batch_size fixo não descreve toda a política.

Pergunta: Qual a métrica principal?
Resposta: Throughput dentro do prazo exigido, acompanhado de latência de cauda e preempções.

Pergunta: Mais sequências ativas significa mais trabalho útil?
Resposta: Não quando a pressão provoca preempções repetidas e reconstrução do mesmo contexto.

Pergunta: Por que versionar o slot?
Resposta: Após cancelamento e reutilização, uma resposta atrasada poderia ser aplicada à sequência errada sem essa distinção.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T088:C05 — mecanismo_avancado

O recurso escasso muda durante a execução: uma sequência admitida ganha tokens e amplia seu estado, enquanto outra termina e libera espaço. Um escalonador precisa contabilizar tokens processados, capacidade KV e prazos, além do número de requisições. Prefills longos introduzidos entre decodes podem aumentar o intervalo entre tokens; a política de admissão determina quem suporta esse atraso.

Condição de contorno:
Melhor ocupação média não garante boa latência de cauda quando crescimento do cache causa preempções ou reconstruções.

Contrato proposto:
- Entradas: Fila de entrada, sequências ativas, orçamento de tokens e blocos disponíveis.
- Saídas: Conjunto de trabalho por iteração e eventos de admissão, término ou preempção.
- Estado: Slots com identificadores de geração, estado KV e prazos individuais.
- Invariante: Resultado assíncrono só atualiza a sequência que ainda possui aquele slot e geração.

Compromissos de projeto:
- Admitir mais sequências aproveita recursos e eleva pressão de memória.
- Priorizar decodes reduz interrupções, mas pode aumentar espera por primeiro token.

## T088:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir prompt muito longo entre várias gerações curtas e cancelar uma delas antes do retorno do kernel. Esperar preservação de identidade e registro explícito das interrupções.

Plano de avaliação proposto:
Plano proposto: comparar lotes fixos e escalonamento por iteração com mesmos comprimentos e chegadas. Medir tokens úteis por segundo, TTFT, intervalos entre tokens, preempções e falhas; escolher uma política que satisfaça os objetivos por classe.

Comparações:
- T094 (complements): Dividir prefills limita o trabalho que uma admissão longa introduz em cada rodada.

Afirmação rastreável:
O Orca propõe escalonamento na granularidade de uma iteração do modelo, permitindo mudanças no lote.
Suporte: direct; fontes: B-S008
Limite: O princípio publicado não determina sozinho reserva de memória, prioridades ou comportamento de um servidor específico.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T088:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cobriu crescimento KV e admissão entre iterações. Agora o foco é justiça temporal, cancelamento e capacidade efetivamente entregue, incluindo diferença entre uma política que maximiza tokens e outra que preserva a experiência de cada usuário.

Justiça em unidades de trabalho
Uma sequência longa pode consumir muitas iterações enquanto outras aguardam. Monitore atraso acumulado, tokens já recebidos e custo estimado restante, sem exigir estimativa perfeita do tamanho final. Projete envelhecimento de prioridade e limites por cliente; dar preferência permanente a solicitações curtas pode excluir tarefas longas necessárias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

Cancelamento com prazo
Quando um cliente abandona a requisição, interrompa geração e libere recursos assim que o backend puder fazê-lo com segurança. Registre a diferença entre pedido de cancelamento e confirmação de liberação. Jobs mortos que continuam decodificando reduzem capacidade e contaminam throughput aparente com tokens que ninguém utilizará.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

Capacidade sob SLO
Defina capacidade como a maior taxa de chegada que mantém qualidade, TTFT e intervalos entre tokens dentro dos limites escolhidos. Não basta encontrar a saturação de tokens por segundo. Teste long tails de prompt e resposta, pois uma pequena fração de pedidos extremos pode alterar a política ótima do restante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

USO AVANÇADO — Assistentes com fan-out
Cenário: Uma tarefa abre muitas análises independentes de candidatos ou documentos.
Estratégia: Adicione limite por missão e reúna as subrequisições pelo scheduler contínuo. Cancele ramos que se tornaram desnecessários depois de seleção antecipada; preserve a contabilização do custo consumido por eles.
Papel do modelo pequeno: Um 8–30B pode atender análises especializadas em paralelo sem carregar uma cópia por ramo.
Aceite proposto: Aprovar por tempo da missão e justiça entre clientes, mantendo resultados associados ao ramo correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

USO AVANÇADO — Serviço misto online e offline
Cenário: Classificações adiáveis disputam o acelerador com conversas.
Estratégia: Use admissão prioritária para o fluxo interativo e aproveite folga para o offline. Reserve uma cota mínima ao offline para evitar inanição. Reavalie quando prompts ou comprimentos médios mudarem.
Papel do modelo pequeno: Um 3–14B pode manter alta utilização em períodos ociosos, desde que jobs adiáveis aceitem pausa.
Aceite proposto: Medir SLO interativo e progresso offline simultaneamente; nenhum pode desaparecer da avaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, verificar se orquestração CPU e montagem do lote limitam o ganho antes do cálculo GPU.
8–14B: Em 8–14B, ajustar admissão por comprimento e tipo de tarefa costuma ser mais informativo que apenas aumentar sequências.
15–30B: Em 15–30B, pressão de KV exige limites claros e avaliação de preempção/recomputação.
Requisitos de treino/runtime: Runtime deve manter estados por sequência, remoção segura e métricas por requisição; lista de prompts numa API não prova batching contínuo.
Não aplicar quando: Não ativar grandes limites sem margem para crescimento da saída e sem mecanismo de cancelamento verificável.

## T088:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Continuous batching é aplicado pelo scheduler do líder.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O operador descreve batching por iteração para o mesmo workload.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passo 4: requisição entra no próximo lote de decode por continuous batching. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C010 — Hugging Face / HuggingChat — relato de 2023
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: O operador informou em 2023 que TGI alimentava HuggingChat e integrava seus serviços de inferência.
Mecanismo documentado: Servidor dedicado de geração com streaming e otimizações disponíveis na pilha; o relato identifica o runtime efetivamente usado.
Correspondência com esta base: É recurso do TGI, mas a fonte não detalha a configuração exata de batching desse deployment.
Transferência proposta para modelo pequeno: Proposta: usar o caso como referência de migração e compatibilidade; novos serviços 3–30B devem considerar estado atual de manutenção e testar alternativas.
Limite: Não demonstra stack atual do HuggingChat. O maintenance mode documentado em 2026 é preservado, e disponibilidade histórica não é recomendação automática de nova adoção.
Fontes: V4B-S019, V3D-S006.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: Recomposição de batch a cada geração é o mecanismo descrito.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T088:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T088 → T094 [complements]
Como combinar: Dividir prefills extensos para reduzir interrupções do decode de sequências admitidas.
Interface: Orçamento de tokens novos e estados de prefill parcial.
Condição: Scheduler intercala fases mantendo causalidade.
Aceite proposto: Medir TTFT e maior intervalo de streaming por classe.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S008, V3B-S004, V4B-S008, V4B-S010, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T088 → T082 [complements]
Como combinar: Reutilizar prefixos comuns no fan-out antes de preencher novas posições do lote.
Interface: Blocos compartilhados e tokens novos por pedido.
Condição: Estados possuem a mesma identidade de execução.
Aceite proposto: Comparar memória compartilhada e capacidade dentro do SLO.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Registrar tokens produzidos após cancelamento como desperdício.
- Expor métricas por cliente e comprimento para detectar inanição mascarada pela média.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar um fluxo completo contra a fronteira sob a mesma taxa de chegada. Continuous batching melhora utilização; a comparação de qualidade continua exigindo testes de domínio independentes do scheduler.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T087, T093, T094, T121

## Fontes primárias associadas

### B-S008 — Orca: A Distributed Serving System for Transformer-Based Generative Models

[https://www.usenix.org/conference/osdi22/presentation/yu](https://www.usenix.org/conference/osdi22/presentation/yu)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por iteração e batching seletivo para geração autorregressiva.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S004 — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[https://arxiv.org/abs/2403.02310](https://arxiv.org/abs/2403.02310)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre prefill e decode; chunked prefills e escalonamento para reduzir interrupções.

Limite: Resumo consultado; não extrapolar ganhos de sistemas ou hardware publicados para implantação local.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V3D-S006 — Text Generation Inference — maintenance status

[https://huggingface.co/docs/text-generation-inference/en/index](https://huggingface.co/docs/text-generation-inference/en/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estado de manutenção do TGI com correções menores, documentação e tarefas leves.

Limite: Estado documental verificado em 2026-11-05; não demonstra interrupção de serviço existente.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S019 — Open-Source Text Generation & LLM Ecosystem at Hugging Face

[https://huggingface.co/blog/os-llms](https://huggingface.co/blog/os-llms)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico do operador de TGI servindo HuggingChat e integração nos serviços de inferência.

Limite: Fonte histórica; não prova stack atual do HuggingChat nem cancela estado atual de manutenção do TGI.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T089 — Early Stopping — EOS, stop sequences, limites e parada semântica

**Nome canônico:** Critérios de término da geração  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T089  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Early Stopping; parada antecipada; EOS; stop sequences; parada semântica

## T089:C01 — conceito

Early Stopping nesta ficha cobre término de inferência por EOS, sequências de parada, limites operacionais ou condição semântica validada. EOS é um token especial; stop sequences são padrões configurados; limite de tokens ou tempo é interrupção por orçamento. A opção early_stopping em beam search tem semântica própria e não indica que uma tarefa arbitrária foi resolvida.

Como funciona:
- Identificar término normal emitido pelo modelo e distinguir essa condição de truncamento, timeout e cancelamento.
- Monitorar a geração incremental para detectar sequências de parada, inclusive padrões divididos entre tokens ou fragmentos de streaming.
- Para parada semântica, usar um verificador externo definido para a tarefa, como objeto completo validado ou teste executável satisfeito.

## T089:C02 — aplicacao

Quando usar:
- Saídas estruturadas, respostas com delimitador explícito ou ciclos de agente com condição verificável de conclusão.

Quando não usar:
- Para considerar o trabalho completo apenas porque o modelo escreveu “concluído” ou porque o orçamento acabou.

Implementação proposta:
- Proposta: declarar motivos de término distintos e propagar finish_reason até o consumidor; validar integridade antes de aceitar a saída.
- Testar a política exata do servidor para inclusão ou remoção da sequência de parada e compatibilidade com tokenizer.
- Reservar tamanho suficiente para fechar estruturas. JSON truncado deve produzir resultado incompleto, sem executar argumentos parciais de ferramenta.
- Avaliar detectores semânticos com casos positivos e negativos; escolher um critério observável e limitar o custo das verificações adicionais.

Aplicação LAI proposta:
Proposta LAI: encerrar uma etapa somente quando seu contrato estiver satisfeito; usar limites como proteção operacional e registrar pendências quando interromper.

## T089:C03 — riscos_validacao

Armadilhas:
- Um delimitador pode aparecer legitimamente dentro de texto, string JSON ou código.
- Limites de tempo da biblioteca podem ser verificados somente ao concluir um passo, sem interrupção instantânea.

Métricas sugeridas:
- Tokens poupados, conclusões prematuras, saídas truncadas, falsos términos semânticos e latência do detector.

Testes propostos:
- Teste proposto: emitir delimitador dividido em fragmentos e também dentro de uma string permitida, conferindo o comportamento especificado.
- Forçar EOS, limite e cancelamento sobre a mesma tarefa e verificar que seus estados finais permanecem diferentes.

## T089:C04 — perguntas_proveniencia

Pergunta: Atingir max_new_tokens conta como sucesso?
Resposta: Não por si só. É um limite operacional; o consumidor precisa verificar se a saída e a tarefa ficaram completas.

Pergunta: Como tornar parada semântica verificável?
Resposta: Defina antes um predicado externo, como schema válido mais campos obrigatórios conferidos, e teste seus falsos positivos.

Pergunta: EOS prova que a tarefa acabou?
Resposta: Apenas indica o término escolhido pelo modelo; a aplicação ainda precisa verificar seu contrato de resultado.

Pergunta: early_stopping tem uma única semântica?
Resposta: Não. Em APIs de geração, esse nome pode se referir especificamente à conclusão da busca com beams.

Escopo das fontes:
Transformers documenta EOS, limites, stop strings e beam search. Detector semântico e critérios LAI são propostas.

## T089:C05 — mecanismo_avancado

Uma condição de parada precisa operar na unidade correta: EOS é um token, uma sequência textual pode atravessar fronteiras de tokens e uma restrição semântica depende do artefato produzido. Em streaming, o detector deve conservar o sufixo necessário para reconhecer padrões repartidos. A parada por orçamento encerra computação, mas não transforma um JSON parcial ou uma prova incompleta em resultado concluído.

Condição de contorno:
Marcadores podem aparecer legitimamente dentro de conteúdo citado; uma regra textual cega pode interromper a tarefa cedo demais.

Contrato proposto:
- Entradas: Tokens decodificados, padrões de parada, orçamento e contrato de completude.
- Saídas: Saída entregue, razão terminal e indicação separada de validação semântica.
- Estado: Sufixo de detecção, contador e estado terminal por sequência.
- Invariante: Término de uma sequência não conclui outras sequências ainda ativas no lote.

Compromissos de projeto:
- Bufferizar caracteres facilita detectar padrões e adiciona atraso ao streaming.
- Paradas muito permissivas desperdiçam tokens; paradas agressivas podem cortar evidências necessárias.

## T089:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dividir o marcador entre chunks, usar padrões sobrepostos e atingir orçamento antes de fechar um objeto. Esperar detecção consistente e marcação explícita de truncamento no último caso.

Plano de avaliação proposto:
Plano proposto: comparar saída integral e streaming com mesmas sequências controladas. Medir detecções incorretas, tokens excedentes, atraso e completude estrutural; aprovar quando regras terminam consistentemente sem confundir limite computacional com sucesso.

Comparações:
- T197 (complements): Um validador pode rejeitar uma estrutura interrompida, mesmo quando a geração terminou normalmente no transporte.

Afirmação rastreável:
A configuração de geração diferencia limites de novos tokens, strings de parada e early stopping de métodos com beams.
Suporte: direct; fontes: B-S009
Limite: Essas opções controlam geração; nenhuma constitui prova geral de que a resposta está correta.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T089:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu EOS, sequência textual e truncamento. Esta expansão define término como evento de protocolo: produção encerrada, artefato completo, validação concluída e resultado publicável são estados distintos que precisam de critérios próprios.

Estados de conclusão
Mantenha razões separadas para EOS, stop configurado, limite, cancelamento e erro. Depois do encerramento, valide o artefato antes de declarar sucesso. Uma resposta pode terminar normalmente e falhar no contrato, ou ser interrompida após já produzir um objeto completo; a aplicação precisa decidir sem apagar a causa real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

Streaming e fronteira de publicação
Quando texto parcial não pode ser consumido com segurança, acumule uma região mínima até que o parser reconheça uma unidade completa. Não retenha a resposta inteira se campos independentes podem ser publicados. Porém, uma validação final pode invalidar o conjunto; deixe explícito ao consumidor quais fragmentos são provisórios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

Parada orientada à tarefa
Use um critério externo para encerrar busca ou refinamento quando a tarefa observável estiver satisfeita. Um modelo afirmar pronto não basta. Se o critério é teste executável, registre qual teste passou e qual cobertura ele fornece; se depende de evidência faltante, termine com abstenção ou encaminhamento explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

USO AVANÇADO — Extração de objeto estruturado
Cenário: Um endpoint deve devolver um registro com campos obrigatórios.
Estratégia: Combine gramática com parser incremental e limite de tamanho. Ao concluir o objeto, valide schema e regras de domínio; pare geração de texto residual apenas se o formato do modelo permitir. Não conserte silenciosamente chaves ou valores importantes.
Papel do modelo pequeno: Um 3–7B pode produzir a estrutura, enquanto código determinístico decide completude.
Aceite proposto: Exigir término classificado e rejeição de truncamentos, objetos duplicados ou campos inválidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

USO AVANÇADO — Revisão de código com orçamento
Cenário: Um agente tenta corrigir um defeito verificável.
Estratégia: Encerre ao passar o conjunto de critérios ou ao atingir limite de tentativas/tempo. Preserve a melhor versão válida e o histórico de falhas. Não trate esgotamento de orçamento como aprovação do último patch.
Papel do modelo pequeno: Um 8–30B pode propor alterações; o ambiente de testes determina quando cessar tentativas.
Aceite proposto: Medir custo por correção aceita e taxa de encerramento indevido, com falhas deliberadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, formatos curtos e critérios determinísticos reduzem geração desnecessária sem depender de autocrítica sofisticada.
8–14B: Em 8–14B, separar resposta final e regiões auxiliares evita cortar delimitadores exigidos pelo template.
15–30B: Em 15–30B, controlar saídas longas por orçamento explícito e checkpoint de artefatos já válidos.
Requisitos de treino/runtime: É runtime/aplicação; EOS e convenções de template pertencem ao checkpoint, enquanto sucesso pertence ao domínio.
Não aplicar quando: Não usar uma palavra comum como stop global nem assumir que fim do stream significa resultado íntegro.

## T089:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: Delimitadores e estados de término participam do formato, sem decidir sucesso da tarefa.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## T089:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T089 → T196 [complements]
Como combinar: Restringir a linguagem de saída e reconhecer término permitido pelo matcher.
Interface: Estado do parser, delimitadores e token de término.
Condição: Gramática e tokenizer representam a mesma convenção.
Aceite proposto: Testar limites em cada posição e objetos incompletos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S009, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T089 → T190 [feeds]
Como combinar: Enviar razão de encerramento e artefato ao verificador antes de publicar sucesso.
Interface: Conteúdo, finish reason, tentativa e critérios satisfeitos.
Condição: O verificador distingue falha, incompletude e validade.
Aceite proposto: Interromper em limites artificiais e conferir classificação correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S009, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar razões originais de término em logs e respostas.
- Testar padrões stop dentro de valores escapados e nas fronteiras de fragmentos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo por artefato completo e correto com a fronteira, incluindo recusas e truncamentos. Parar cedo economiza trabalho somente quando preserva o objetivo; não compensa capacidade insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T153, T195, T196, P012

## Fontes primárias associadas

### B-S009 — Generation — GenerationConfig

[https://huggingface.co/docs/transformers/main_classes/text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Critérios de parada, limite de novos tokens e semântica específica de early_stopping em beam search.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T090 — FlashAttention

**Nome canônico:** FlashAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T090  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção com otimização de IO

## T090:C01 — conceito

Algoritmo de atenção exata que reorganiza cálculo e acesso à memória para evitar materializar toda a matriz de atenção na memória global. Usa blocos e estados intermediários compactos. Na versão densa, continua calculando as interações exigidas pela atenção; economia de memória não transforma automaticamente o custo aritmético quadrático em linear.

Como funciona:
- Carregar blocos de consultas, chaves e valores em memória mais próxima do processamento.
- Acumular resultados com normalização estável sem guardar todos os scores globais.
- Escrever a saída consolidada e apenas os intermediários necessários.

## T090:C02 — aplicacao

Quando usar:
- Atenção ocupa parcela relevante do custo com sequências longas.
- Backend e dimensões do modelo são suportados pelo kernel.

Quando não usar:
- Esperar ganho relevante quando o gargalo dominante está em rede, ferramentas ou outras camadas.

Implementação proposta:
- Confirmar pelo profiler qual kernel foi escolhido; não confiar apenas na flag.
- Comparar com atenção de referência usando mesma máscara e precisão.
- Medir prefill, decode e memória de pico separadamente para o tamanho real da carga.

Aplicação LAI proposta:
Proposta LAI: verificar se o runtime já usa atenção otimizada antes de propor uma segunda instalação; medir contribuição no tempo total da missão.

## T090:C03 — riscos_validacao

Armadilhas:
- Exato matematicamente não significa bit a bit igual, devido à ordem das operações em ponto flutuante.
- Pedir todos os pesos de atenção pode exigir outro caminho e eliminar parte da economia.

Métricas sugeridas:
- Tempo de kernel e bytes de memória global movimentados.
- Memória de pico e diferença numérica da saída contra referência.

Testes propostos:
- Cobrir máscaras causais, padding e comprimentos não múltiplos do bloco; exigir erro numérico limitado.
- Verificar que entradas não suportadas falham claramente ou usam fallback conhecido.

## T090:C04 — perguntas_proveniencia

Pergunta: FlashAttention é atenção esparsa?
Resposta: A versão densa original é exata e não remove pares de tokens; variantes esparsas são uma extensão distinta.

Pergunta: Dobra automaticamente a velocidade?
Resposta: Não. O ganho depende do kernel, formas, hardware e parcela da atenção no custo total.

Pergunta: Cabe menos matriz intermediária significa menos cache KV?
Resposta: Não necessariamente. Intermediários de atenção e estados persistentes KV são parcelas diferentes.

Pergunta: Pode validar apenas perplexidade?
Resposta: Não. Compare também saídas e máscaras em casos controlados; qualidade agregada pode ocultar um erro de fronteira.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T090:C05 — mecanismo_avancado

A economia central aparece quando a matriz de probabilidades de atenção deixa de ser gravada integralmente na memória externa. Isso reduz intermediários e tráfego, mas não transforma atenção densa em uma operação linear no comprimento. No treinamento, estratégias de recomputação podem reconstruir intermediários no backward; na inferência, o benefício depende da forma das consultas, especialmente da diferença entre prefill com muitas consultas e decode com poucas.

Condição de contorno:
Exatidão algorítmica permite diferenças de ponto flutuante decorrentes da ordem das reduções; não implica identidade bit a bit.

Contrato proposto:
- Entradas: Q, K, V, máscara, escala e regra de dropout explicitamente definidas.
- Saídas: Saída equivalente à atenção especificada e, quando aplicável, gradientes.
- Estado: Acumuladores de normalização e blocos temporários, sem matriz global persistente.
- Invariante: Toda posição permitida participa da normalização; nenhuma posição proibida contribui.

Compromissos de projeto:
- Menos tráfego externo pode exigir recomputar valores no backward.
- Um kernel rápido em prefill pode não ser o melhor para consultas unitárias.

## T090:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar com referência de alta precisão em logits extremos, máscara causal e comprimentos não múltiplos do tile. Esperar ausência de vazamento futuro e erros compatíveis com o dtype escolhido.

Plano de avaliação proposto:
Plano proposto: controlar forma, máscara, dtype e dropout; medir memória intermediária, tráfego e duração separada de forward e backward. Aprovar pela equivalência numérica e benefício no caminho efetivamente utilizado, incluindo custos de despacho.

Comparações:
- T096 (distinct_from): Sparsity muda quais interações existem; FlashAttention pode executar a atenção densa original.

Afirmação rastreável:
FlashAttention reduz acessos entre memória externa e memória próxima ao processamento por uma execução consciente de IO.
Suporte: direct; fontes: B-S010
Limite: O artigo não garante aceleração universal nem remove o custo aritmético quadrático da atenção densa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T090:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou economia de intermediários e diferença prefill/decode. A nova camada trata seleção de backend como contrato de compatibilidade, validação numérica e atribuição causal de ganhos, evitando avaliar um kernel isolado e prometer desempenho de serviço.

Contrato completo do operador
Liste máscara causal, offsets, comprimentos variáveis, dimensão de cabeça, dtype e política de dropout antes de trocar backend. Verifique se o executor selecionou o kernel esperado ou fez fallback. Uma API com o mesmo nome pode escolher caminhos diferentes conforme a forma; registre essa decisão no ensaio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

Equivalência útil à tarefa
Compare saídas e, no treinamento, gradientes com uma referência apropriada. Pequenas diferenças numéricas são esperadas por ordem de redução; o limite aceitável depende da precisão e do uso. Além do erro tensorial, teste se classificações ou campos sensíveis mudam, sobretudo perto de empates entre tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

Benefício além do kernel
Separe tempo de atenção de tokenização, projeções, comunicação e sampling. O ganho total é limitado pela parcela otimizada. Quando a memória liberada permitir lote maior, faça um segundo experimento: o primeiro mede troca de kernel, o segundo mede a nova configuração de serviço, preservando atribuição clara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

USO AVANÇADO — Prefill de documentos extensos
Cenário: O processamento de entrada domina o tempo inicial.
Estratégia: Escolha um backend compatível, aqueça compilação e varie comprimentos reais. Preserve o mesmo padrão de atenção. Depois avalie se memória liberada pode servir mais pedidos sem piorar a cauda do decode.
Papel do modelo pequeno: Um 3–30B de atenção densa pode aproveitar a implementação sem alterar pesos, quando suportado.
Aceite proposto: Aceitar somente com erro dentro da tolerância e ganho end-to-end, incluindo fallback.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

USO AVANÇADO — Ajuste fino com contexto longo
Cenário: Ativações de atenção limitam o microbatch.
Estratégia: Valide backward, máscaras de padding e fronteiras entre exemplos empacotados. Aumente microbatch somente após comparar gradientes com a configuração original. Meça memória no pico do treino inteiro, não apenas durante atenção.
Papel do modelo pequeno: Um 8–14B com adaptadores pode ganhar margem de ativações, sem reduzir a memória da base automaticamente.
Aceite proposto: Exigir estabilidade de treinamento e ausência de atenção entre exemplos independentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, outros operadores podem dominar; confirmar que atenção ocupa parcela relevante antes de otimizar.
8–14B: Em 8–14B, ganhos de memória podem facilitar contexto ou microbatch, avaliados separadamente.
15–30B: Em 15–30B, verificar coexistência com quantização, paralelismo e kernels de decode específicos.
Requisitos de treino/runtime: Troca de kernel é runtime quando semântica é preservada; suporte ao backward e arquitetura precisa ser confirmado.
Não aplicar quando: Não usar uma máscara esparsa nova como se fosse apenas substituição exata de implementação.

## T090:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Relaciona implementação da família FlashAttention; FA4 não prova adoção específica de FA1, FA2 ou FA3.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T090:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T090 → T107 [complements]
Como combinar: Medir quanto tráfego e tempo de atenção representam no caminho crítico.
Interface: Perfil por operador e bytes de intermediários.
Condição: Formas e precisão são idênticas na comparação.
Aceite proposto: Relacionar ganho local ao limite de ganho total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S010, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T090 → T115 [complements]
Como combinar: Combinar redução de intermediários com recomputação seletiva no treinamento.
Interface: Política de checkpoint e operadores de atenção recompostos.
Condição: Backward e RNG são preservados.
Aceite proposto: Comparar memória de pico e tempo por passo com gradientes equivalentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S010, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar fallback de backend como resultado, não excluí-lo.
- Testar padding, offsets causais e sequências de comprimento extremo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo de uma tarefa com fronteira mantendo qualidade fixa. FlashAttention melhora execução de atenção existente; não amplia o conhecimento nem transforma contexto numericamente suportado em compreensão confiável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T091, T092, T097, T098, T113, T114

## Fontes primárias associadas

### B-S010 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

[https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atenção exata com blocos e menor tráfego entre memória da GPU e SRAM.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T091 — FlashAttention-2

**Nome canônico:** FlashAttention-2  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T091  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Flash Attention 2

## T091:C01 — conceito

Evolução da implementação de atenção exata com melhor divisão de trabalho entre blocos e warps da GPU. Reduz operações e comunicação que limitavam a utilização do hardware. É um algoritmo/kernel, não um novo modelo de linguagem nem uma expansão automática de contexto.

Como funciona:
- Reorganizar operações para reduzir trabalho fora das multiplicações matriciais.
- Distribuir uma cabeça de atenção por mais blocos quando isso melhora ocupação.
- Particionar o trabalho entre warps para reduzir comunicação interna desnecessária.

## T091:C02 — aplicacao

Quando usar:
- Modelo e GPU possuem backend FA2 suportado e a atenção é um gargalo.
- Comparação de kernels em prefill e treino de sequências extensas.

Quando não usar:
- Ativar FA2 só pelo número da versão quando outro backend otimizado já é superior na carga.

Implementação proposta:
- Fixar versão do pacote, CUDA e dimensões de cabeça no experimento.
- Registrar o kernel efetivo e comparar contra o backend padrão do mesmo runtime.
- Ensaiar vários comprimentos e tamanhos de lote para identificar regiões de ganho.

Aplicação LAI proposta:
Proposta LAI: conservar o backend já validado como baseline e testar FA2 apenas em uma cópia controlada da configuração de inferência.

## T091:C03 — riscos_validacao

Armadilhas:
- Um benchmark de kernel isolado não equivale ao ganho de ponta a ponta.
- Mudança silenciosa de dtype, máscara ou padding invalida a comparação.

Métricas sugeridas:
- Ocupação, tempo por chamada e proporção de operações não matriciais.
- TTFT, throughput e memória com o mesmo workload.

Testes propostos:
- Comparar logits e saída da atenção com referência em tolerância definida por dtype.
- Testar casos curtos e longos para garantir que a escolha automática não cria regressões materiais.

## T091:C04 — perguntas_proveniencia

Pergunta: FA2 altera os pesos?
Resposta: Não. A otimização implementa o cálculo de atenção sem exigir ensinar uma nova habilidade ao modelo.

Pergunta: É sempre melhor que FA1?
Resposta: O projeto melhora paralelismo, mas desempenho real ainda depende de formas e hardware.

Pergunta: O maior tile é o melhor?
Resposta: Não. Registradores e memória compartilhada limitam quantos blocos podem executar simultaneamente e podem causar spill.

Pergunta: Backward tem exatamente a mesma vantagem?
Resposta: Não. As dependências entre gradientes exigem coordenação adicional; meça o caminho de treinamento separadamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T091:C05 — mecanismo_avancado

No particionamento descrito para o forward, dividir consultas entre warps permite que cada grupo produza sua própria fatia de saída. Dividir chaves entre warps pode exigir somar resultados parciais com comunicação adicional. A seleção de tiles também envolve registradores: aumentar o bloco reduz certas transferências, porém pode provocar spilling ou impedir que blocos suficientes permaneçam simultaneamente ativos no dispositivo.

Condição de contorno:
Formas pequenas podem não oferecer paralelismo suficiente; a configuração eficiente varia com dimensão da cabeça e recursos disponíveis.

Contrato proposto:
- Entradas: Tensores, máscara e configuração de tiles compatível com o dispositivo.
- Saídas: Resultado da atenção e informações sobre o kernel realmente selecionado.
- Estado: Registradores, memória compartilhada e distribuição de linhas de consulta.
- Invariante: Cada linha recebe contribuições de todas as chaves permitidas exatamente uma vez.

Compromissos de projeto:
- Tiles maiores podem reduzir tráfego e diminuir ocupação ao mesmo tempo.
- Menos operações escalares ajuda quando essas operações limitam o kernel.

## T091:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: variar dimensões próximas aos limites de especialização e registrar spilling ou fallback. Comparar numericamente com referência e exigir que configurações não suportadas falhem de modo explícito.

Plano de avaliação proposto:
Plano proposto: comparar implementações sob mesmas formas e precisão, separando prefill e decode. Medir tempo, ocupação e tráfego compartilhado quando disponíveis; escolher pelo tempo total, sem usar utilização teórica isolada como critério de sucesso.

Comparações:
- T090 (specializes): Mantém a atenção e melhora sua distribuição de trabalho entre recursos da GPU.

Afirmação rastreável:
O artigo descreve dividir Q entre warps para reduzir comunicação que surgia no esquema com K repartido.
Suporte: direct; fontes: V3B-S006
Limite: O detalhamento refere-se ao algoritmo publicado; kernels posteriores podem escolher outras decomposições.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T091:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou divisão de trabalho e registradores. Aqui o foco é escolher FA2 dentro de um conjunto de backends, lidar com comprimentos variáveis e distinguir ganhos da atenção de efeitos introduzidos por empacotamento ou compilação.

Forma de entrada como distribuição
Colete distribuição de batch, comprimento e dimensão de cabeça. Um único tensor grande pode favorecer a configuração escolhida e esconder degradações nas formas pequenas predominantes em produção. Construa uma grade baseada no uso e pese resultados por frequência, mantendo casos raros críticos separados da média.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

Remoção de padding com fronteiras
Quando usar representação de comprimento variável, preserve os offsets cumulativos e a máscara de cada sequência. Remover padding altera layout, não autoriza atenção entre documentos. Valide exemplos com tamanhos extremos e lotes reordenados; uma saída plausível pode esconder mistura de contexto difícil de perceber visualmente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

Ciclo de vida do backend
Fixe pacote, compilador e dispositivo do ensaio e registre o fallback disponível. Não selecione FA2 apenas pelo nome conhecido nem descarte uma implementação nova sem teste. Após atualização, reavalie formas efetivamente utilizadas, porque mudanças no despacho ou em máscaras podem ter mais impacto que o microbenchmark principal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Lote de documentos desiguais
Cenário: Um classificador recebe textos curtos e longos juntos.
Estratégia: Compare padding convencional com caminho varlen suportado, mantendo exemplos idênticos e mapeamento de IDs. Só então compare FA2 com outros backends. Isso evita atribuir à versão do kernel uma economia causada pela remoção de padding.
Papel do modelo pequeno: Um especialista 3–14B pode se beneficiar de menos trabalho inútil nos prefills.
Aceite proposto: Aprovar com independência entre exemplos e redução de tempo ponderada pelo tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Migração de runtime
Cenário: Um modelo já funciona em um executor de referência.
Estratégia: Monte testes diferenciais de máscara, posições e sampling, aqueça todas as formas relevantes e faça rollout gradual. Se houver backend ausente, falhe com diagnóstico ou use fallback conhecido; não ignore silenciosamente o padrão da arquitetura.
Papel do modelo pequeno: Um 15–30B precisa preservar compatibilidade junto de TP, GQA e dtype selecionados.
Aceite proposto: Exigir qualidade equivalente e picos de memória dentro do orçamento do serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, medir formatos curtos e overhead de despacho para não escolher pelo cenário mais favorável ao kernel.
8–14B: Em 8–14B, avaliar varlen e empacotamento com testes de isolamento dos exemplos.
15–30B: Em 15–30B, incluir formas resultantes do particionamento por dispositivo, não apenas tensores do modelo inteiro.
Requisitos de treino/runtime: Runtime deve suportar a arquitetura, dtype e máscara; versão FA2 não é configuração universal de todo checkpoint.
Não aplicar quando: Não forçar FA2 quando o backend perde um recurso do modelo ou realiza conversões caras não medidas.

## T091:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T091:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T091 → T087 [complements]
Como combinar: Avaliar lote e layout juntamente, mantendo compatibilidade e identidade por sequência.
Interface: Comprimentos, offsets cumulativos e IDs dos exemplos.
Condição: Kernel varlen é suportado e não mistura sequências.
Aceite proposto: Comparar resultados com processamento independente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S011, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T091 → T098 [alternative]
Como combinar: Selecionar outro kernel eficiente quando oferecer melhor cobertura das formas reais.
Interface: Contrato de atenção e matriz de compatibilidade.
Condição: Ambas implementações preservam a mesma semântica.
Aceite proposto: Escolher por distribuição de latência e memória, não por nome de versão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S011, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar lotes reordenados e comprimentos unitários.
- Separar melhoria por unpadding, compilação e troca de kernel no relatório.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar uma aplicação de modelo pequeno com fronteira usando custo e prazo do serviço. FA2 pode melhorar eficiência; qualquer diferença de qualidade decorre do modelo ou da execução e deve ser investigada separadamente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T092, T098, T113

## Fontes primárias associadas

### B-S011 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning

[https://arxiv.org/abs/2307.08691](https://arxiv.org/abs/2307.08691)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Melhor particionamento de trabalho e paralelismo na atenção exata.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S006 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning — full text

[https://arxiv.org/html/2307.08691v1](https://arxiv.org/html/2307.08691v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento entre blocos e warps, custo de operações não matriciais.

Limite: Texto técnico consultado; velocidade depende de formas, dtype e arquitetura do dispositivo.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T092 — FlashAttention-3

**Nome canônico:** FlashAttention-3  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T092  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Flash Attention 3

## T092:C01 — conceito

Versão de atenção otimizada cujo trabalho original explora recursos de GPUs Hopper, incluindo assincronia, sobreposição entre movimentação e cálculo e caminhos de baixa precisão. O nome não garante disponibilidade nem vantagem em qualquer GPU NVIDIA. Cada backend e formato precisam ser identificados.

Como funciona:
- Sobrepor transferência de blocos e operações dos Tensor Cores.
- Intercalar multiplicações e normalização para reduzir espera.
- Aplicar estratégia específica de baixa precisão quando o caminho escolhido a suporta.

## T092:C02 — aplicacao

Quando usar:
- Hardware e runtime oferecem implementação compatível com as características exploradas.
- Atenção limita desempenho e há oportunidade de melhorar sobreposição de operações.

Quando não usar:
- Tratar resultados publicados em H100 como previsão direta para uma RTX 5090 ou outro acelerador.

Implementação proposta:
- Consultar a matriz de suporte da versão efetivamente instalada.
- Separar ensaios em FP16/BF16 e FP8 para não atribuir todo ganho ao mesmo fator.
- Guardar configuração e profiler que comprovem o caminho executado.

Aplicação LAI proposta:
Proposta LAI: manter compatibilidade com o hardware real como condição de entrada; o pacote RAG não afirma FA3 funcionando no servidor do usuário.

## T092:C03 — riscos_validacao

Armadilhas:
- Nome de GPU mais recente não significa suporte automático a todas as instruções e kernels de outro projeto.
- FP8 pode exigir escalas e avaliação numérica distintas da variante de maior precisão.

Métricas sugeridas:
- Sobreposição de cópia/cálculo, tempo de kernel e utilização computacional.
- Erro da atenção, acerto de tarefa e latência final por precisão.

Testes propostos:
- Comparar referência e kernel em entradas extremas e máscaras usadas pelo modelo.
- Confirmar que formato não suportado produz erro explícito, sem presumir ganho por uma flag aceita.

## T092:C04 — perguntas_proveniencia

Pergunta: FA3 serve automaticamente na 5090?
Resposta: Não se pode concluir pelo nome; é necessário verificar backend, versão, build e formatos suportados.

Pergunta: FP8 e FA3 são a mesma técnica?
Resposta: Não. Um é formato/estratégia numérica; o outro é uma implementação de atenção que pode explorá-lo.

Pergunta: Ter suporte a FP8 basta para usar o kernel?
Resposta: Não. O caminho pode depender de instruções, layouts e software adicionais.

Pergunta: Pipeline mais ocupado prova menor latência?
Resposta: Não. Coordenação e pressão de recursos podem compensar a sobreposição; compare duração real do trabalho completo.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T092:C05 — mecanismo_avancado

A execução assíncrona exige distinguir transferência iniciada de dados já disponíveis para consumo. Sobrepor movimento, multiplicação e normalização cria mais trabalho em andamento, mas também introduz dependências de buffers e barreiras. A variante de baixa precisão adiciona outro eixo: formato, escalas e tratamento de outliers precisam ser avaliados separadamente da vantagem do pipeline, evitando atribuir toda diferença a uma única mudança.

Condição de contorno:
As técnicas do artigo exploram recursos de Hopper; o nome da família não certifica suporte em qualquer GPU posterior ou doméstica.

Contrato proposto:
- Entradas: Forma, dtype, recursos suportados e política de quantização quando usada.
- Saídas: Atenção calculada e identificação do caminho assíncrono ou fallback.
- Estado: Buffers alternados, eventos de disponibilidade e escalas por bloco.
- Invariante: Um buffer não é sobrescrito enquanto algum consumidor ainda depende dele.

Compromissos de projeto:
- Mais sobreposição pode aumentar pressão sobre registradores e memória compartilhada.
- Baixa precisão reduz tráfego, mas acrescenta erro e trabalho de escalonamento numérico.

## T092:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar comprimentos irregulares e repetidas alternâncias de buffers, comparando com referência. Uma sincronização removida deve ser detectada por divergência ou ferramenta de verificação, não aceita como ganho.

Plano de avaliação proposto:
Plano proposto: avaliar primeiro caminhos de mesma precisão e depois variar precisão isoladamente. Controlar formas e backend; medir latência, erro de saída e uso de recursos. Aprovar somente configurações suportadas com qualidade dentro do requisito definido.

Comparações:
- T123 (complements): FP8 pode participar da implementação, mas precisão e assincronia são decisões independentes.

Afirmação rastreável:
FlashAttention-3 explora assincronia, especialização de warps e intercalamento de multiplicações com softmax em GPUs Hopper.
Suporte: direct; fontes: B-S012
Limite: A fonte apresenta uma arquitetura específica; não verifica a placa, o driver ou o servidor do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T092:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou pipeline assíncrono e baixa precisão. Esta ficha acrescenta gestão de compatibilidade de hardware, controle de regressão por forma e decisão de upgrade, sem transformar uma versão otimizada para uma arquitetura em recomendação universal.

Matriz de elegibilidade
Antes de habilitar um caminho FA3, registre arquitetura do dispositivo, dtype, dimensão de cabeça e recursos exigidos pelo pacote. Separe suporte declarado de execução verificada. Uma GPU da mesma marca ou uma versão recente do driver não prova que o caminho assíncrono original esteja disponível ou seja selecionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

Dupla linha de base
Compare primeiro o caminho de mesma precisão com o backend atual; depois avalie caminhos de precisão reduzida. Mantenha a máscara e os dados constantes. Essa separação permite localizar se um ganho veio da organização do cálculo ou de mudança numérica, e se uma regressão pertence ao kernel ou à quantização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

Política de atualização
Versione o artefato de compilação e mantenha rollback. A existência de backends mais novos, como a integração documentada de FA4 em FlexAttention, reforça a necessidade de medir, não de atualizar automaticamente. O backend escolhido deve vencer no conjunto de formas do serviço e passar o mesmo contrato de exatidão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

USO AVANÇADO — Pool com hardware heterogêneo
Cenário: Workers de diferentes gerações servem o mesmo checkpoint.
Estratégia: Defina perfil de backend por classe de dispositivo. Compare resultados por precisão e evite encaminhar um artefato compilado para destino incompatível. Exponha o perfil usado em cada requisição para diagnosticar divergências e caudas.
Papel do modelo pequeno: Um 8–30B pode manter pesos comuns com execução específica por dispositivo.
Aceite proposto: Exigir fallback previsível e ausência de erro silencioso em workers não elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

USO AVANÇADO — Prefill de alta intensidade
Cenário: Sequências longas consomem parcela relevante do tempo GPU.
Estratégia: Teste FA3 no intervalo de shapes de produção e meça aquecimento, sincronização e pico de memória. Avalie low precision como experimento adicional, com corpus de valores extremos e consultas sensíveis a pequenas mudanças.
Papel do modelo pequeno: Um 3–14B só justifica a troca se atenção realmente dominar o perfil.
Aceite proposto: Aceitar por tempo total, tolerância numérica e qualidade por segmento, sem portar speedups publicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, o overhead restante pode limitar benefício; priorizar medição do caminho completo.
8–14B: Em 8–14B, variar contexto e batch para identificar onde o caminho otimizado realmente compensa.
15–30B: Em 15–30B, testar compatibilidade com sharding, GQA e formatos quantizados do restante da rede.
Requisitos de treino/runtime: Exige runtime e hardware adequados; não é atualização de pesos nem aumento de contexto treinado.
Não aplicar quando: Não alegar compatibilidade com uma GPU específica do usuário sem identificar e testar dispositivo, build e backend.

## T092:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T092:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T092 → T123 [complements]
Como combinar: Avaliar o caminho FP8 separadamente da reorganização assíncrona.
Interface: Escalas, dtype e erros por camada ou saída.
Condição: Implementação oferece o caminho numérico no hardware selecionado.
Aceite proposto: Comparar primeiro mesma precisão e depois baixa precisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S012, V4B-S018, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T092 → T107 [requires]
Como combinar: Localizar se espera de memória, cálculo ou sincronização domina cada forma.
Interface: Perfil de kernels e tempo no serviço.
Condição: Instrumentação não altera materialmente o regime observado.
Aceite proposto: Repetir com aquecimento e relatar variância e custos externos à atenção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S012, V4B-S018, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar a implementação realmente selecionada em cada worker.
- Manter fallback e testes numéricos após recompilação ou upgrade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve usar tarefa, qualidade e custo observados. Uma otimização específica de hardware pode melhorar latência local, sem sustentar alegação de inteligência equivalente ou superior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T123, T086

## Fontes primárias associadas

### B-S012 — FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision

[https://arxiv.org/abs/2407.08608](https://arxiv.org/abs/2407.08608)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto centrado em Hopper, assincronia e variantes de baixa precisão.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T093 — PagedAttention

**Nome canônico:** PagedAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T093  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção paginada

## T093:C01 — conceito

Gerencia o cache KV em blocos físicos que não precisam estar contíguos e usa uma tabela para traduzir posições lógicas. Reduz desperdício por reserva e fragmentação no serving. A paginação reorganiza armazenamento; por si só não remove tokens nem substitui atenção densa por esparsa.

Como funciona:
- Dividir o KV de cada sequência em blocos lógicos.
- Mapeá-los para blocos físicos disponíveis conforme a sequência cresce.
- Permitir compartilhamento compatível e liberar blocos quando nenhuma sequência precisar deles.

## T093:C02 — aplicacao

Quando usar:
- Muitas requisições concorrentes com comprimentos imprevisíveis.
- Geração com ramificações que compartilham prefixos.

Quando não usar:
- Esperar que paginação sozinha resolva falta de memória dos pesos ou aumente qualidade do modelo.

Implementação proposta:
- Usar o gerenciador do runtime, evitando implementar tabelas KV independentes na aplicação.
- Observar capacidade alocada, ocupada e desperdiçada em cargas variadas.
- Verificar limpeza após cancelamento, erro e encerramento de sequência.

Aplicação LAI proposta:
Proposta LAI: considerar paginação como recurso interno do servidor de inferência; a Helena deve observar capacidade e pressão, não manipular blocos diretamente.

## T093:C03 — riscos_validacao

Armadilhas:
- Blocos menores reduzem desperdício interno, mas podem elevar overhead de metadados e acesso.
- Compartilhar blocos mutáveis sem controle pode corromper ramificações de geração.

Métricas sugeridas:
- Fragmentação interna, blocos livres e sequências simultâneas.
- Throughput com prazo de latência fixo e eventos de preempção.

Testes propostos:
- Criar sequências de diferentes tamanhos, cancelar parte delas e confirmar recuperação da memória.
- Bifurcar um prefixo e verificar que escrever em uma continuação não altera a outra.

## T093:C04 — perguntas_proveniencia

Pergunta: PagedAttention comprime o conteúdo?
Resposta: Não. Organiza o armazenamento dos estados; quantização e poda são decisões distintas.

Pergunta: É igual ao paging do sistema operacional?
Resposta: Usa inspiração semelhante, mas gerencia estruturas específicas do cache KV do modelo.

Pergunta: Paginação comprime os valores?
Resposta: Não. Ela reorganiza alocação e compartilhamento; quantização é uma transformação separada da representação.

Pergunta: Pode liberar ao terminar uma resposta?
Resposta: Somente depois de remover sua referência e confirmar que nenhum outro consumidor utiliza aquele bloco físico.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T093:C05 — mecanismo_avancado

Compartilhar blocos físicos requer separar referência lógica de propriedade da escrita. Quando duas continuações compartilham um bloco parcialmente preenchido, a próxima escrita pode exigir cópia antes de modificar o conteúdo. A fragmentação restante depende da granularidade: para uma sequência com T tokens e blocos de B tokens, a capacidade alocada é ceil(T/B)·B, salvo compartilhamento e reservas adicionais.

Condição de contorno:
A paginação reduz desperdício de alocação; não reduz por si só a quantidade matemática de estados necessários à atenção.

Contrato proposto:
- Entradas: Comprimento lógico, tabela de blocos, referências compartilhadas e solicitação de crescimento.
- Saídas: Mapeamento atualizado e blocos privados quando houver escrita divergente.
- Estado: Contadores de referência, ocupação parcial e lista de blocos livres.
- Invariante: Nenhuma sequência observa uma escrita privada realizada por outra continuação.

Compromissos de projeto:
- Blocos menores reduzem sobra final e aumentam metadados e indireções.
- Compartilhamento economiza memória, mas requer contagem e cópia consistentes.

## T093:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: bifurcar duas gerações no meio de um bloco, escrever tokens diferentes e cancelar uma delas. Esperar preservação da outra saída e liberação somente quando não restarem referências.

Plano de avaliação proposto:
Plano proposto: comparar alocação contígua e paginada em comprimentos e ramificações controlados. Medir bytes úteis, reservados, cópias, falhas de alocação e throughput; decidir pela capacidade entregue e latência, incluindo custo de gestão.

Comparações:
- T082 (complements): Compartilhamento físico pode sustentar reúso de prefixos, mas identidade do conteúdo continua necessária.

Afirmação rastreável:
O projeto de PagedAttention usa contagem de referências e cópia na escrita para blocos compartilhados que divergem.
Suporte: direct; fontes: V3B-S009
Limite: A evidência descreve o desenho original; tamanho de bloco e políticas atuais dependem do runtime.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T093:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou fragmentação e cópia na escrita. O aprofundamento concentra-se na escolha do tamanho de bloco, isolamento de falhas e admissão por crescimento futuro, conectando o alocador de KV ao comportamento real do serviço.

Granularidade como compromisso
Blocos menores reduzem sobra no fim de sequências, mas ampliam tabelas, metadados e trabalho de tradução. Blocos maiores simplificam gestão e podem favorecer acesso, ao custo de desperdício. Escolha pelo perfil de comprimentos e ramificações, incluindo overhead do kernel; não maximize eficiência de bytes ignorando o tempo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

Reserva para crescimento
Uma sequência admitida precisa continuar crescendo até seu limite autorizado. Defina margem ou política explícita de preempção antes de esgotar páginas. Contar apenas o prompt inicial pode admitir pedidos demais e gerar recomputação repetida, aumentando o atraso justamente quando a memória parece estar bem utilizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

Diagnóstico por invariantes
Mantenha relação verificável entre blocos lógicos, páginas físicas e referências ativas. Uma página reciclada precisa de identificação que impeça referências antigas de ler novo conteúdo. Teste estados de limite, cancelamento e compartilhamento; falhas no alocador podem produzir texto plausível de outra sequência sem um crash evidente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

USO AVANÇADO — Muitas respostas curtas
Cenário: Um endpoint recebe grande quantidade de extrações pequenas.
Estratégia: Meça sobra por sequência e custo das tabelas para diferentes granularidades suportadas. Compare capacidade útil mantendo o mesmo limite de saída. Não aumente simultaneamente batch e contexto ao avaliar o tamanho do bloco.
Papel do modelo pequeno: Um 3–14B pode ganhar concorrência quando desperdício do cache domina a capacidade.
Aceite proposto: Exigir memória útil maior sem piora relevante no tempo de serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

USO AVANÇADO — Exploração com ramos
Cenário: Um agente avalia continuações alternativas de um prefixo.
Estratégia: Compartilhe páginas imutáveis, aplique cópia controlada na parte mutável e libere ramos descartados. A contabilidade deve reconhecer compartilhamento e impedir dupla liberação. Teste o ramo sobrevivente após cancelar os demais.
Papel do modelo pequeno: Um 15–30B pode explorar alternativas sem replicar todo o prefixo.
Aceite proposto: Verificar equivalência com ramos independentes e custo incremental de cada continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, grande número de sequências curtas pode tornar metadados e fragmentação mais relevantes que pesos.
8–14B: Em 8–14B, medir tamanho de bloco junto da distribuição de saída e taxa de cancelamento.
15–30B: Em 15–30B, reservar crescimento evita ciclos de preempção que anulam a capacidade obtida.
Requisitos de treino/runtime: Paginação é runtime e precisa de kernel/alocador compatíveis; não altera o padrão lógico de atenção.
Não aplicar quando: Não interpretar páginas como chunking semântico nem remover páginas ainda necessárias para manter uma falsa meta de ocupação.

## T093:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: A documentação inclui gerenciamento paginado do cache.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T093:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T093 → T105 [complements]
Como combinar: Expulsar apenas blocos ociosos ou preemptar conforme política explícita de reconstrução.
Interface: Referências, prioridade e custo de recomputação.
Condição: A validade de páginas ativas é protegida.
Aceite proposto: Simular pressão e comprovar ausência de leitura após reciclagem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S009, V4B-S014, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T093 → T118 [complements]
Como combinar: Alinhar gestão de páginas com shards de KV e conclusão dos ranks.
Interface: Mapeamentos por rank, comprimentos e confirmação coletiva.
Condição: Todos os participantes reconhecem a mesma sequência lógica.
Aceite proposto: Cancelar um pedido durante comunicação e verificar liberação consistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S009, V4B-S014, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar reutilização agressiva de páginas com conteúdo sentinela.
- Contar memória de tabelas e reservas, não apenas tensores preenchidos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar capacidade de atender tarefas corretas com uma fronteira sob carga equivalente. PagedAttention reduz desperdício de armazenamento; não aumenta o conhecimento ou o alcance lógico da atenção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T088, T105, T116, R009

## Fontes primárias associadas

### B-S013 — Efficient Memory Management for Large Language Model Serving with PagedAttention

[https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Blocos não contíguos de KV, menor fragmentação e compartilhamento no serving.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S009 — Efficient Memory Management for Large Language Model Serving with PagedAttention — full text

[https://arxiv.org/html/2309.06180v1](https://arxiv.org/html/2309.06180v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Blocos lógicos/físicos, compartilhamento, contagem de referências e cópia na escrita.

Limite: Texto do projeto original; medições publicadas não são resultados da implantação do usuário.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T094 — Chunked Prefill

**Nome canônico:** Chunked Prefill  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T094  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** prefill em partes

## T094:C01 — conceito

Divide o processamento inicial de um prompt longo em partes escalonáveis. Preserva a sequência lógica e seus estados; não resume nem retira conteúdo. A finalidade é controlar interferência entre entradas longas e sequências que já estão produzindo tokens.

Como funciona:
- Reservar um orçamento de tokens de trabalho por iteração.
- Processar somente uma parte do prefill quando o prompt excede o orçamento.
- Continuar o restante em iterações seguintes junto de outros trabalhos compatíveis.

## T094:C02 — aplicacao

Quando usar:
- Prompts longos chegam enquanto outras conversas estão em decode.
- Latência entre tokens sofre picos causados por grandes prefills.

Quando não usar:
- Confundir o mecanismo com cortar documentos em chamadas independentes sem preservar o estado do modelo.

Implementação proposta:
- Medir separadamente TTFT das novas entradas e ITL das sequências ativas.
- Varrer alguns orçamentos de tokens mantendo a mesma carga e limites de memória.
- Verificar qual política prioriza decode e como ela impede espera indefinida de prefill.

Aplicação LAI proposta:
Proposta LAI: usar como candidato de ajuste quando ingestão ou contexto longo prejudica atendimento; não copiar um tamanho de chunk sem ensaio.

## T094:C03 — riscos_validacao

Armadilhas:
- Partes pequenas demais aumentam overhead e podem atrasar muito o primeiro token.
- Partes grandes demais preservam throughput mas ainda interrompem a fluidez de conversas ativas.

Métricas sugeridas:
- TTFT e ITL por faixa de comprimento do prompt.
- Tempo de fila e tokens de prefill processados por iteração.

Testes propostos:
- Injetar um prompt longo durante vários streams; exigir ITL dentro da meta escolhida.
- Comparar logits após prefill integral e dividido, preservando tokens e máscara, com tolerância numérica.

## T094:C04 — perguntas_proveniencia

Pergunta: Chunked prefill reduz a quantidade de tokens do contexto?
Resposta: Não. Distribui o cálculo no tempo mantendo o prompt lógico.

Pergunta: Qual tamanho devo usar?
Resposta: Aquele que equilibra TTFT e ITL no perfil de carga e hardware medidos.

Pergunta: O cache reinicia em cada trecho?
Resposta: Não quando o objetivo é preservar a mesma atenção; o estado permitido anterior precisa continuar acessível.

Pergunta: Chunk menor sempre reduz TTFT?
Resposta: Não. Mais rodadas e sobrecarga podem alongar a conclusão do prefill, embora melhorem a cadência de outras respostas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T094:C05 — mecanismo_avancado

Dividir um prefill não significa tratar cada trecho como uma sequência independente. As consultas do trecho atual precisam acessar todos os estados anteriores permitidos pela arquitetura e respeitar a causalidade dentro do próprio trecho. O orçamento deve contar trabalho novo e interferência com decodes ativos. Trechos muito pequenos podem multiplicar lançamentos e reduzir eficiência matricial; trechos grandes podem provocar pausas longas entre tokens.

Condição de contorno:
O tamanho ideal depende de mistura de comprimentos, contexto já processado, backend e objetivo de latência; não existe número universal.

Contrato proposto:
- Entradas: Prompt completo, offset processado, KV anterior e orçamento da rodada.
- Saídas: Cache estendido e offset confirmado, mantendo ordem causal.
- Estado: Trechos pendentes, posições absolutas e sequências de decode concorrentes.
- Invariante: Divisão de execução não altera o contexto visível definido pelo modelo.

Compromissos de projeto:
- Menores trechos favorecem intercalamento e podem aumentar custo total.
- Priorizar decode melhora cadência, mas pode elevar TTFT de novas entradas.

## T094:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar evidência no fim de um trecho e consulta no início do seguinte, variando fronteiras. Esperar resultado compatível com prefill integral e ausência de reset posicional.

Plano de avaliação proposto:
Plano proposto: comparar prefill inteiro e vários tamanhos de trecho com mesma chegada. Medir TTFT, intervalo entre tokens, duração de prefill e interrupções; selecionar pela combinação de objetivos de serviço, sem confundir throughput agregado com responsividade.

Comparações:
- T095 (distinct_from): Chunking organiza execução; uma janela altera a conectividade permitida pela atenção.

Afirmação rastreável:
Sarathi-Serve combina prefills divididos e escalonamento para reduzir interrupções das sequências em decode.
Suporte: direct; fontes: V3B-S004
Limite: O método publicado não fixa um tamanho ótimo válido para todos os modelos e cargas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T094:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou causalidade entre chunks e compromisso de granularidade. Agora a política considera prazo de primeiro token, regularidade de streaming e estimativa de custo por forma, para decidir quanto prefill admitir sem prejudicar sessões já abertas.

Dois relógios de serviço
O novo pedido espera seu primeiro token, enquanto pedidos antigos esperam o próximo. Reserve orçamento entre esses dois compromissos em vez de priorizar indefinidamente apenas um deles. Uma política que protege todo decode pode deixar prefills longos sem progresso; o inverso gera pausas visíveis nas conversas ativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

Orçamento em custo observado
Igual número de tokens novos não garante duração igual quando contextos e arquiteturas diferem. Use observações por faixa de comprimento e forma para limitar tempo aproximado da iteração, mantendo teto conservador. Reavalie a estimativa após quantização, troca de backend ou alteração de batch, pois o gargalo pode mudar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

Aquecimento e formas recorrentes
Um conjunto pequeno de tamanhos de chunk pode facilitar compilação e reutilização de grafos, se o runtime suportar. Muitos tamanhos adaptativos podem causar aquecimento repetido e consumir memória de grafos. Meça esse efeito antes de adotar uma política aparentemente mais fina; flexibilidade tem custo de engenharia e execução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

USO AVANÇADO — Documento longo durante chat ativo
Cenário: Um usuário envia um arquivo extenso enquanto outros recebem streaming.
Estratégia: Processe o arquivo com orçamento por iteração e progresso mínimo garantido. Reduza chunks quando o intervalo de streaming exceder a meta, mas aplique envelhecimento para que o arquivo avance. Registre separadamente tempo em fila e tempo de prefill.
Papel do modelo pequeno: Um 8–30B pode compartilhar GPU entre leitura longa e diálogos curtos.
Aceite proposto: Aprovar pela combinação de TTFT do arquivo e regularidade do streaming existente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

USO AVANÇADO — Importação seguida de perguntas
Cenário: Muitos documentos serão consultados após ingestão.
Estratégia: Prepare prefills oportunisticamente apenas para conteúdos com probabilidade de uso, preservando orçamento de pedidos ativos. Combine com prefix caching quando houver reuso exato. Se a demanda não vier, contabilize prefill antecipado como custo desperdiçado.
Papel do modelo pequeno: Um 3–14B pode reduzir espera percebida sem exigir um modelo maior.
Aceite proposto: Medir economia nas consultas reais e custo dos prefills nunca consumidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, B-S014, V4B-S002, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, chunks muito pequenos podem ser dominados por lançamentos e controle CPU.
8–14B: Em 8–14B, escolher poucas faixas de tamanho por objetivo de latência facilita operação e diagnóstico.
15–30B: Em 15–30B, considerar pressão KV e duração das operações distribuídas ao fixar orçamento.
Requisitos de treino/runtime: É scheduling runtime; preserva contexto lógico e requer suporte correto ao prefill parcial.
Não aplicar quando: Não tratar chunks como documentos independentes nem usá-los para contornar o limite de contexto do checkpoint.

## T094:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Processamento do prompt em blocos de 64 preserva histórico KV na configuração publicada. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3, passo 2, e seção 4.1: prefill longo é dividido em chunks conforme limiar e processado em pipeline. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T094:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T094 → T088 [complements]
Como combinar: Reservar trabalho de prefill dentro de cada iteração do lote contínuo.
Interface: Tokens novos, decodes ativos e prazos de cada pedido.
Condição: O scheduler mantém estados de prefill parcial.
Aceite proposto: Comparar piores intervalos entre tokens e progresso de pedidos longos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, B-S014, V4B-S002, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T094 → T102 [alternative]
Como combinar: Separar fases em pools quando interferência persistir e transferência compensar.
Interface: Custo de prefill, volume KV e atraso de transporte.
Condição: Carga e infraestrutura justificam uma segunda camada de coordenação.
Aceite proposto: Comparar goodput com todas as transferências e filas incluídas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, B-S014, V4B-S002, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Garantir progresso mínimo para entradas longas.
- Testar variação de chunks com mesma máscara e saída de referência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar experiência de leitura e conversa contra uma fronteira usando os mesmos documentos e perguntas. Melhor escalonamento pode reduzir espera, mas não prova que o modelo pequeno compreende todo o documento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T102, T121

## Fontes primárias associadas

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S004 — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[https://arxiv.org/abs/2403.02310](https://arxiv.org/abs/2403.02310)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre prefill e decode; chunked prefills e escalonamento para reduzir interrupções.

Limite: Resumo consultado; não extrapolar ganhos de sistemas ou hardware publicados para implantação local.

### V3B-S007 — Mistral 7B — full text

[https://arxiv.org/html/2310.06825v1](https://arxiv.org/html/2310.06825v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campo receptivo em camadas, cache circular e chunking com janela.

Limite: Refere-se à arquitetura publicada; não prova qualidade para contexto arbitrário nem compatibilidade com checkpoint do usuário.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

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

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T095 — Sliding Window Attention

**Nome canônico:** Sliding Window Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T095  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção de janela deslizante

## T095:C01 — conceito

Restrição da atenção a uma vizinhança de posições, geralmente uma janela recente em decoders causais. É propriedade da arquitetura ou do padrão de atenção, diferente de descartar mensagens na aplicação. Reduz as interações por camada, mas limita acesso direto a posições fora da janela.

Como funciona:
- Definir quais posições são visíveis para cada consulta.
- Aplicar máscara e kernel compatíveis com a janela.
- Reter apenas os estados que o modelo ainda pode usar, considerando camadas locais e globais.

## T095:C02 — aplicacao

Quando usar:
- Checkpoint foi treinado ou validado para atenção local.
- Sequências extensas possuem dependências predominantemente locais.

Quando não usar:
- Impor uma janela arbitrária a modelo denso e presumir equivalência sem reavaliação.

Implementação proposta:
- Inspecionar configuração por camada, tamanho da janela e sentido causal.
- Testar dependências antes e depois da fronteira da janela.
- Preservar mecanismo externo de recuperação para informação que precise voltar ao contexto.

Aplicação LAI proposta:
Proposta LAI: verificar a arquitetura do checkpoint antes de usar a janela como justificativa para um limite de memória; combinar com recuperação explícita quando necessário.

## T095:C03 — riscos_validacao

Armadilhas:
- Atenção local em uma camada não prova que todo o modelo usa memória limitada ao mesmo tamanho.
- Um resumo ou fato distante pode não ser diretamente acessível no passo atual.

Métricas sugeridas:
- KV efetivamente retido por camada e custo por comprimento.
- Acerto em tarefas que exigem dependências além da janela.

Testes propostos:
- Variar distância entre instrução e pergunta para localizar degradação de acesso.
- Comparar alocação real de cache com a configuração e verificar camadas de atenção plena.

## T095:C04 — perguntas_proveniencia

Pergunta: É igual a manter apenas as últimas mensagens?
Resposta: Não. Uma técnica opera dentro da atenção; a outra altera o texto enviado ao modelo.

Pergunta: Posso ligar isso em qualquer modelo?
Resposta: Não sem suporte e avaliação. Mudar o padrão pode alterar o comportamento aprendido.

Pergunta: O índice circular pode substituir a posição absoluta?
Resposta: Não. O slot é armazenamento; a posição lógica determina relações causais e informação posicional.

Pergunta: Janela é uma flag neutra em modelo global?
Resposta: Não. Restringir conectividade muda a função do modelo e exige validação de qualidade e compatibilidade.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T095:C05 — mecanismo_avancado

Uma janela por camada não limita necessariamente toda influência histórica ao mesmo tamanho. Informações podem propagar-se por camadas sucessivas, ampliando o campo receptivo teórico. Isso não equivale a recuperar fielmente qualquer detalhe antigo. Em cache circular, o slot físico pode ser posição módulo capacidade, mas a posição lógica continua absoluta; confundir as duas afeta máscaras e codificação posicional.

Condição de contorno:
A remoção de estados só é válida nas camadas cuja atenção realmente deixou de consultá-los; camadas globais exigem tratamento distinto.

Contrato proposto:
- Entradas: Posições lógicas, largura da janela, configuração por camada e tokens novos.
- Saídas: Atenção local correta e atualização dos slots que podem ser substituídos.
- Estado: Mapa de posições para slots, idade dos estados e políticas por camada.
- Invariante: Nenhuma chave fora da janela é reutilizada como se fosse um token recente.

Compromissos de projeto:
- Memória limitada reduz acesso direto a detalhes distantes.
- Janelas maiores preservam mais conexões e elevam tráfego e capacidade necessária.

## T095:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar além de duas voltas do buffer e colocar fatos nas fronteiras. Comparar com implementação de máscara local explícita; erros de wraparound devem aparecer sem alterar o modelo de referência.

Plano de avaliação proposto:
Plano proposto: manter arquitetura e pesos fixos, variando somente a implementação do cache. Medir equivalência, memória estabilizada e latência; avaliar capacidade de dependência distante em conjunto separado, sem tratá-la como garantia arquitetural.

Comparações:
- T109 (specializes): A janela deslizante especifica como a vizinhança avança com a posição.

Afirmação rastreável:
O Mistral publicado descreve propagação de informação entre camadas e armazenamento circular para a janela.
Suporte: direct; fontes: V3B-S007
Limite: O campo receptivo teórico não demonstra desempenho uniforme em qualquer comprimento.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T095:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu campo receptivo e posição lógica do cache circular. Agora a aplicação considera a distância das dependências, arquitetura híbrida e recuperação externa, para selecionar um modelo com janela local sem prometer acesso fiel a qualquer detalhe remoto.

Mapa de dependências da tarefa
Antes de escolher a janela, identifique quais respostas dependem de evidências distantes e quais precisam apenas da vizinhança recente. Construa exemplos que movem a mesma evidência pelo documento. A qualidade deve ser medida por distância e tipo de relação, pois bom desempenho em resumos não garante recuperação de exceções antigas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

Camadas locais e globais
Em modelos híbridos, mantenha políticas KV diferentes por camada. A economia das camadas locais pode ser real enquanto as globais continuam crescendo com o contexto. Dimensione o serviço pela soma concreta dessas camadas e não pela largura nominal de uma janela publicada como característica geral do modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

Reconexão por artefatos externos
Quando a tarefa exigir detalhe fora do alcance efetivo, recupere o trecho original e reapresente-o no contexto permitido. Essa estratégia opera na aplicação e precisa de proveniência; não transforma atenção local em global. Meça se a recuperação trouxe a evidência correta antes de atribuir falha ao gerador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

USO AVANÇADO — Assistente para fluxo temporal
Cenário: Eventos recentes dominam a decisão, mas algumas regras permanecem estáveis.
Estratégia: Mantenha os eventos recentes no contexto local e carregue regras relevantes sob demanda. Teste mudanças de regra e referências a eventos antigos. Use armazenamento externo para fatos que precisam sobreviver, sem confiar em influência difusa entre camadas.
Papel do modelo pequeno: Um 3–7B local pode interpretar eventos recentes com custo limitado, dentro de uma tarefa estreita.
Aceite proposto: Aceitar por acerto em dependências recentes e recuperação correta das exceções antigas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

USO AVANÇADO — Análise de arquivo extenso
Cenário: Há seções independentes e relações pontuais entre elas.
Estratégia: Selecione um checkpoint treinado com padrão compatível. Faça leitura por seções com referências para trechos distantes, verificando relações cruzadas. Se o modelo híbrido já oferecer alcance global, teste esse caminho antes de acrescentar orquestração.
Papel do modelo pequeno: Um 8–30B pode combinar processamento local e consultas dirigidas sem ingerir tudo repetidamente.
Aceite proposto: Comparar erros por distância e custo total, incluindo recuperação e múltiplas chamadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preferir tarefas com dependências locais e memória externa explícita para fatos persistentes.
8–14B: Em 8–14B, testar modelos híbridos por camada e evitar inferir qualidade pelo tamanho anunciado do contexto.
15–30B: Em 15–30B, avaliar se camadas globais tornam KV dominante apesar da janela local.
Requisitos de treino/runtime: Padrão pertence à arquitetura e ao treinamento; runtime deve implementar máscara e descarte compatíveis com cada camada.
Não aplicar quando: Não impor janela nova a um checkpoint denso como otimização supostamente equivalente.

## T095:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T095:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T095 → T009 [complements]
Como combinar: Recuperar a evidência antiga e inseri-la como novo contexto quando necessário.
Interface: Trecho original, fonte e posição documental.
Condição: Recuperação pode localizar a dependência e respeita o orçamento.
Aceite proposto: Mover evidências para fora da janela e verificar recuperação antes da resposta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S007, V4B-S017, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T095 → T106 [complements]
Como combinar: Calcular memória pelo padrão de retenção e cabeças de cada camada.
Interface: Configuração local/global, heads KV e dtype.
Condição: A configuração do checkpoint foi inspecionada.
Aceite proposto: Comparar estimativa com alocação real em diferentes comprimentos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S007, V4B-S017, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar fatos antigos contraditos por mensagens recentes.
- Separar limite de cache, alcance arquitetural e competência demonstrada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas com dependências locais e remotas contra a fronteira. Eficiência local pode ser suficiente para o domínio, mas não sustenta paridade em síntese global ou raciocínio sobre documentos arbitrários.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T096, T109, T110

## Fontes primárias associadas

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S007 — Mistral 7B — full text

[https://arxiv.org/html/2310.06825v1](https://arxiv.org/html/2310.06825v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campo receptivo em camadas, cache circular e chunking com janela.

Limite: Refere-se à arquitetura publicada; não prova qualidade para contexto arbitrário nem compatibilidade com checkpoint do usuário.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T096 — Sparse Attention

**Nome canônico:** Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T096  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa

## T096:C01 — conceito

Família de padrões que calcula atenção apenas sobre parte dos pares possíveis de posições. A seleção pode ser local, fixa, por blocos ou dependente do conteúdo. Economia aritmética teórica só vira menor tempo quando o kernel evita efetivamente o trabalho omitido.

Como funciona:
- Definir uma conectividade esparsa entre consultas e chaves.
- Calcular e normalizar scores apenas sobre posições permitidas.
- Propagar informação pelas conexões restantes e pela profundidade do modelo.

## T096:C02 — aplicacao

Quando usar:
- Sequências longas permitem explorar estrutura de dependências.
- Existe checkpoint ou procedimento validado para o padrão escolhido.

Quando não usar:
- Aplicar máscara esparsa em kernel que ainda calcula toda a matriz e esperar aceleração automática.

Implementação proposta:
- Especificar padrão, densidade, limites de conexão e necessidade de treinamento.
- Comparar tempo real e qualidade contra atenção densa no mesmo regime.
- Avaliar casos em que a informação importante está em posições raras ou distantes.

Aplicação LAI proposta:
Proposta LAI: tratar atenção esparsa como escolha de arquitetura ou backend especializado, não como otimização universal que a Helena ativa por prompt.

## T096:C03 — riscos_validacao

Armadilhas:
- Remover conexões pode eliminar a única rota útil para uma evidência.
- Operações irregulares podem perder eficiência apesar de fazerem menos multiplicações.

Métricas sugeridas:
- Densidade de pares atendidos e tempo de kernel.
- Acerto por distância e tipo de dependência no documento.

Testes propostos:
- Construir tarefa com evidência distante e medir falhas conforme a densidade diminui.
- Perfil de execução deve mostrar trabalho reduzido, não apenas valores mascarados depois do cálculo.

## T096:C04 — perguntas_proveniencia

Pergunta: Sparse Attention é sinônimo de FlashAttention?
Resposta: Não. A primeira reduz conectividade; a versão densa de FlashAttention reorganiza a mesma atenção.

Pergunta: Menos FLOPs garante menor latência?
Resposta: Não. Acesso irregular, seleção e overhead podem anular a economia.

Pergunta: Muitos pesos próximos de zero bastam para acelerar?
Resposta: Não se o kernel ainda calcula todos os scores e executa a mesma redução densa.

Pergunta: O resultado esparso pode ser exato?
Resposta: Sim em relação à máscara declarada; isso não o torna idêntico à atenção original sem essa máscara.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T096:C05 — mecanismo_avancado

Esparsidade tem dois significados que precisam ser separados: pesos de atenção pequenos após softmax e conexões deliberadamente ausentes antes da normalização. Apenas o segundo define um padrão de cálculo que pode dispensar operações. Zerar valores depois de calcular a matriz densa não recupera o custo já pago. Além disso, normalizar sobre um subconjunto produz outra distribuição, salvo casos especiais de contribuição originalmente nula.

Condição de contorno:
Um padrão com poucas conexões pode executar lentamente se sua irregularidade impedir agrupamento eficiente ou exigir seleção cara.

Contrato proposto:
- Entradas: Padrão permitido, tensores QKV, máscara causal e regra para linhas sem conexões.
- Saídas: Saída normalizada apenas sobre posições admitidas pelo padrão.
- Estado: Índices ou estrutura do padrão e metadados necessários ao kernel.
- Invariante: A exclusão ocorre antes da normalização e respeita as restrições causais.

Compromissos de projeto:
- Conectividade menor economiza trabalho e restringe rotas de informação.
- Padrões regulares favorecem kernels, mas podem representar pior dependências específicas.

## T096:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: excluir uma chave com score dominante e comparar referência densa mascarada com kernel esparso. Também criar linha totalmente excluída e exigir comportamento definido, sem NaNs silenciosos.

Plano de avaliação proposto:
Plano proposto: comparar kernel esparso com máscara densa equivalente para correção, depois avaliar contra modelo de conectividade completa para qualidade. Medir custo de seleção, execução e tarefa final; aprovar somente a troca explicitamente escolhida.

Comparações:
- T090 (distinct_from): Atenção exata eficiente em IO pode preservar todas as conexões; sparsity seleciona quais permanecem.

Afirmação rastreável:
Longformer combina atenção local e global para oferecer uma estrutura esparsa de conexões.
Suporte: direct; fontes: B-S015
Limite: A fonte sustenta esse padrão específico, não a preservação de qualidade para qualquer poda.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T096:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu conexões ausentes de pesos pequenos. O novo desenho exige escolher um grafo de comunicação adequado à tarefa, contabilizar o seletor e avaliar adaptação dos pesos, tornando explícito quando esparsidade é arquitetura e quando é aproximação experimental.

Cobertura do grafo
Analise se o padrão permite que dependências relevantes se encontrem ao longo das camadas. Um grafo conectado teoricamente pode ainda exigir muitos passos ou comprimir informação em poucos intermediários. Crie testes de ponte entre seções e compare padrões com o mesmo número aproximado de conexões, evitando avaliar somente tamanho de contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

Custo antes da atenção
Inclua construção de índices, seleção, ordenação e movimentação de dados na medição. Um padrão barato no papel pode produzir acessos irregulares ou gastar muito para decidir o que ignorar. Registre economia efetiva de operações e bytes separadamente, usando o mesmo kernel denso como referência sem alterar outras otimizações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

Adaptação e regressão
Se a máscara não faz parte do treinamento original, trate a mudança como nova variante do modelo. Compare sem adaptação e com treino adicional quando houver recursos e dados autorizados. Preserve um conjunto de tarefas com dependências raras para impedir que a redução média de custo esconda perda sistemática de informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

USO AVANÇADO — Documentos com estrutura previsível
Cenário: Seções possuem vínculos locais e algumas referências globais conhecidas.
Estratégia: Desenhe uma máscara por blocos/seções, preserve conexões de referência e verifique ausência de acesso futuro. Use um protótipo para medir viabilidade antes de treinar. Se precisar construir matriz densa para escolher conexões, contabilize esse custo integral.
Papel do modelo pequeno: Um 3–14B pode ser adaptado ao domínio, mas não recebe a capacidade apenas por trocar uma flag.
Aceite proposto: Aceitar por qualidade em dependências cruzadas e redução end-to-end, incluindo construção da máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

USO AVANÇADO — Pesquisa de contexto extenso
Cenário: O objetivo é explorar arquitetura dentro de orçamento limitado.
Estratégia: Compare padrões local, global e conteúdo-dependente com dados e compute controlados. Registre custo de treino e inferência. Não apresentar um único checkpoint melhor em um benchmark como superioridade causal de toda a família esparsa.
Papel do modelo pequeno: Um 15–30B pode ser candidato experimental se treino e kernels forem viáveis.
Aceite proposto: Exigir avaliações fora do domínio de ajuste e relatório das relações que deixaram de ser recuperadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, a capacidade representacional menor recomenda padrões simples e tarefas delimitadas antes de seleção complexa.
8–14B: Em 8–14B, investigar padrões estruturados com kernels regulares e avaliação de longo alcance.
15–30B: Em 15–30B, incluir custo de treinamento/adaptação e integração distribuída no orçamento de projeto.
Requisitos de treino/runtime: Arquitetura esparsa normalmente exige pesos compatíveis; esparsificação pós-treino é aproximação a validar.
Não aplicar quando: Não zerar scores após cálculo denso e apresentar isso como economia aritmética de sparse attention.

## T096:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T096:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T096 → T097 [complements]
Como combinar: Organizar conectividade em blocos para que o executor possa pular regiões inteiras.
Interface: Máscara lógica e índices de blocos presentes.
Condição: Padrão mantém esparsidade também na granularidade física.
Aceite proposto: Comparar conexões úteis, blocos processados e tempo total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, B-S016, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T096 → T110 [complements]
Como combinar: Adicionar canais globais limitados para dependências que a vizinhança não cobre.
Interface: Posições globais e regra de seleção.
Condição: Causalidade e treinamento autorizam essas conexões.
Aceite proposto: Testar relações distantes e crescimento do custo ao aumentar globais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, B-S016, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Relatar custo do seletor e casos sem ganho real.
- Não confundir conectividade teórica com recuperação fiel de detalhes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve abranger tarefas locais e globais, mantendo transparência sobre treino adicional. Esparsidade pode ampliar contexto viável; não garante compreensão equivalente do conteúdo removido.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T097, T111, T112

## Fontes primárias associadas

### B-S016 — Generating Long Sequences with Sparse Transformers

[https://arxiv.org/abs/1904.10509](https://arxiv.org/abs/1904.10509)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fatorações esparsas da atenção e kernels para sequências longas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T097 — Block-Sparse Attention

**Nome canônico:** Block-Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T097  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa por blocos

## T097:C01 — conceito

Atenção esparsa organizada em blocos de posições, permitindo pular regiões inteiras da matriz. A granularidade facilita kernels regulares, mas pode computar pares desnecessários dentro de um bloco mantido. Não se confunde com blocos de armazenamento KV usados por PagedAttention.

Como funciona:
- Particionar a matriz lógica em tiles e selecionar quais são atendidos.
- Executar cálculo somente nos tiles presentes, respeitando a máscara causal.
- Normalizar considerando todos os blocos selecionados para cada consulta.

## T097:C02 — aplicacao

Quando usar:
- Documentos com estrutura em segmentos ou dependências previsíveis.
- Backend possui kernels eficientes para o padrão de blocos.

Quando não usar:
- Usar uma matriz quase densa ou blocos muito pequenos que tornem o overhead dominante.

Implementação proposta:
- Escolher bloco conforme formas do kernel e padrões de acesso, não apenas limites de parágrafo.
- Registrar a máscara lógica e reproduzir o experimento com densidade controlada.
- Comparar com referência densa mascarada para validar semântica antes de medir velocidade.

Aplicação LAI proposta:
Proposta LAI: estudar para um modelo ou kernel que já suporte a técnica; priorizar ajustes de serving mais simples quando não houver justificativa arquitetural.

## T097:C03 — riscos_validacao

Armadilhas:
- Permitir um bloco parcialmente futuro sem máscara interna cria vazamento causal.
- Um bloco removido pode conter uma informação crítica isolada.

Métricas sugeridas:
- Percentual de blocos ativos e pares computados dentro deles.
- Tempo de atenção, acerto de tarefa e overhead de construir a máscara.

Testes propostos:
- Comparar saída com atenção densa usando a mesma máscara exata.
- Inserir tokens futuros em blocos de fronteira e confirmar que não afetam saídas anteriores.

## T097:C04 — perguntas_proveniencia

Pergunta: Blocos do KV tornam atenção esparsa?
Resposta: Não. Paginação pode armazenar atenção densa; sparsity define quais interações são calculadas.

Pergunta: Qual tamanho de bloco é melhor?
Resposta: Depende do kernel e padrão; mede-se equilíbrio entre trabalho redundante e overhead.

Pergunta: Mudar máscara sempre exige recompilar?
Resposta: Não necessariamente; mudar metadados e recompilar código são operações distintas, mas os metadados precisam representar o novo padrão.

Pergunta: Por que testar fronteiras de documentos?
Resposta: Um bloco parcialmente válido pode conter posições de documentos diferentes; marcá-lo como completo cria vazamento de contexto.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T097:C05 — mecanismo_avancado

A representação em blocos distingue regiões completamente excluídas, completamente presentes e parcialmente mascaradas. Essa classificação permite pular blocos e evitar testes individuais onde toda conexão é válida. O custo de construir a estrutura também importa: uma máscara que muda por exemplo ou camada precisa ser atualizada, enquanto uma máscara estável pode amortizar sua construção entre chamadas compatíveis.

Condição de contorno:
Esparsidade por elemento pode deixar quase todos os blocos parcialmente ocupados, produzindo pouca economia na granularidade escolhida.

Contrato proposto:
- Entradas: Predicado de conectividade, forma, tamanho de bloco e tensores de atenção.
- Saídas: Metadados de blocos e saída equivalente à máscara declarada.
- Estado: Versão do padrão, índices presentes e classificação de blocos parciais.
- Invariante: Reutilizar metadados somente quando a conectividade e as dimensões continuam compatíveis.

Compromissos de projeto:
- Blocos maiores reduzem metadados e podem desperdiçar cálculo dentro de blocos parciais.
- Construir padrões dinâmicos pode consumir o tempo economizado na atenção.

## T097:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reutilizar propositalmente uma máscara de documentos após trocar suas fronteiras. Esperar invalidação; comparar saída com referência que proíbe atenção entre documentos distintos.

Plano de avaliação proposto:
Plano proposto: medir construção e execução separadamente, variando densidade, regularidade e frequência de mudança. Usar máscara densa equivalente como controle; aprovar pelo tempo total amortizado e equivalência, não apenas pela fração de elementos removidos.

Comparações:
- T096 (specializes): Organiza as conexões esparsas em unidades adequadas aos kernels.

Afirmação rastreável:
FlexAttention usa BlockMask para identificar blocos puláveis e distinguir blocos completos dos parcialmente mascarados.
Suporte: direct; fontes: V3B-S008
Limite: A API documentada pode evoluir; o princípio não garante ganho para padrões arbitrários.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T097:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 classificou blocos presentes, ausentes e parciais. Aqui a estratégia avalia alinhamento documental, amortização de metadados e empacotamento, distinguindo economia no kernel de uma mudança semântica no que cada token pode consultar.

Alinhamento com documentos
Ao empacotar exemplos, mantenha fronteiras documentais independentes do tamanho físico do bloco. Um bloco pode atravessar duas sequências sem autorizar conexões entre elas; a máscara parcial deve preservar isolamento. Avalie o custo dos blocos de fronteira e compare com layouts que reduzem essas regiões parcialmente ocupadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

Reuso seguro de metadados
Armazene a máscara compilada somente quando forma e conectividade forem idênticas. Um template de mesma largura pode ter limites documentais diferentes. A chave precisa representar esses limites e versões do padrão; caso contrário, um cache de metadados rápido pode criar uma ligação que a tarefa nunca autorizou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

Planejamento de granularidade
Escolha tamanho de bloco em conjunto com distribuição de comprimentos e regularidade do padrão. Reduzir blocos pode revelar mais esparsidade, mas aumentar overhead de índices e scheduling. Faça comparação com o mesmo predicado de conectividade para isolar granularidade; mudar máscara e bloco ao mesmo tempo impede explicar o resultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

USO AVANÇADO — Treino com exemplos empacotados
Cenário: Muitos textos pequenos são combinados para ocupar melhor o acelerador.
Estratégia: Construa máscara por documento e comprimentos reais, compile padrões recorrentes e valide gradientes contra exemplos separados. Só depois ajuste granularidade e packing. Exclua qualquer ganho obtido por permitir atenção entre exemplos independentes.
Papel do modelo pequeno: Um 3–14B em ajuste fino pode reduzir desperdício sem aprender vazamento entre amostras.
Aceite proposto: Aceitar com isolamento comprovado, gradientes consistentes e menor custo por token útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

USO AVANÇADO — Inferência de estrutura modular
Cenário: Um documento contém grupos que podem atender a poucos outros grupos.
Estratégia: Codifique relações permitidas em blocos e preserve uma referência densa com a mesma máscara lógica. Meça custo de construção para cada nova estrutura; só mantenha cache quando houver revisitas suficientes.
Papel do modelo pequeno: Um 15–30B compatível pode explorar padrões regulares, mediante validação de qualidade e suporte.
Aceite proposto: Comparar tempo total por documento e falhas nas referências que cruzam blocos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preferir padrões simples que não adicionem um seletor mais caro que a atenção economizada.
8–14B: Em 8–14B, packing e máscaras documentais oferecem um problema concreto para avaliar granularidade.
15–30B: Em 15–30B, testar layouts produzidos por paralelismo e sua compatibilidade com o backend.
Requisitos de treino/runtime: Requer kernel que pule blocos; mudança do padrão de atenção exige pesos compatíveis ou adaptação validada.
Não aplicar quando: Não confundir blocos de computação esparsa com páginas físicas de cache KV.

## T097:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Máscaras por blocos representam esparsidade explorável pelo kernel.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T097:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T097 → T096 [complements]
Como combinar: Materializar um padrão esparso em representação que permita omitir trabalho.
Interface: Predicado de conexões, índices e blocos parciais.
Condição: A representação corresponde exatamente à máscara pretendida.
Aceite proposto: Comparar saída com referência densa mascarada e contar blocos processados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S008, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T097 → T090 [complements]
Como combinar: Usar execução em tiles para blocos presentes, preservando normalização sobre o conjunto permitido.
Interface: Blocos QKV e acumuladores de softmax.
Condição: Backend combina corretamente esparsidade e kernel fundido.
Aceite proposto: Testar linhas com poucos blocos e diferentes ordens de processamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S008, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Incluir documentos de comprimento não múltiplo do bloco.
- Invalidar metadados quando mudar qualquer fronteira de sequência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar capacidade e qualidade em documentos estruturados com a fronteira. A implementação pode reduzir custo de relações autorizadas; não demonstra que eliminar outras relações preserve qualquer tarefa aberta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T093, T096, T113

## Fontes primárias associadas

### B-S016 — Generating Long Sequences with Sparse Transformers

[https://arxiv.org/abs/1904.10509](https://arxiv.org/abs/1904.10509)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fatorações esparsas da atenção e kernels para sequências longas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S010 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

[https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atenção exata com blocos e menor tráfego entre memória da GPU e SRAM.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S008 — FlexAttention: The Flexibility of PyTorch with the Performance of FlashAttention

[https://pytorch.org/blog/flexattention/](https://pytorch.org/blog/flexattention/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: BlockMask, blocos completos/parciais e custo de construção da máscara.

Limite: Artigo oficial técnico; APIs e recomendações de compilação devem ser conferidas na versão instalada.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T098 — Memory-Efficient Attention

**Nome canônico:** Memory-Efficient Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T098  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção eficiente em memória

## T098:C01 — conceito

Nome de família e de implementações que reduzem memória temporária no cálculo de atenção. Pode incluir kernels fundidos e processamento por blocos. O termo isolado não identifica uma única versão, nem informa se há aproximação, suporte a GQA ou alteração de padrão.

Como funciona:
- Evitar guardar intermediários de tamanho proporcional à matriz completa quando possível.
- Escolher kernel segundo forma, dtype, máscara e hardware.
- Manter fallback explícito quando a implementação otimizada não suporta a entrada.

## T098:C02 — aplicacao

Quando usar:
- Memória temporária da atenção limita o tamanho de entrada ou lote.
- Framework oferece implementação otimizada testada para o caso.

Quando não usar:
- Assumir que a configuração solicitada foi respeitada sem observar dispatch e profiler.

Implementação proposta:
- Registrar nome e versão do backend efetivo junto da configuração de atenção.
- Testar máscara, dropout, precisão e número de cabeças usados pelo modelo.
- Separar memória temporária de atenção e memória persistente de KV na medição.

Aplicação LAI proposta:
Proposta LAI: documentar o kernel efetivo dentro do inventário de runtime, evitando registrar o mesmo ganho como Memory-Efficient Attention e FlashAttention independentes.

## T098:C03 — riscos_validacao

Armadilhas:
- Solicitar mapas completos de atenção pode obrigar materialização de intermediários.
- Mudança de backend pode alterar ligeiramente valores numéricos e determinismo.

Métricas sugeridas:
- Memória de pico além dos pesos e KV.
- Latência por forma e frequência de fallback ao backend matemático.

Testes propostos:
- Comparar saída com referência e cobrir máscaras vazias, padding e comprimentos pequenos.
- Forçar uma forma não suportada e verificar diagnóstico ou fallback correto.

## T098:C04 — perguntas_proveniencia

Pergunta: É outro algoritmo além de FlashAttention?
Resposta: Pode ser uma implementação diferente ou apenas um rótulo amplo; é necessário identificar o backend.

Pergunta: Diminui a memória dos pesos?
Resposta: Não diretamente. O foco é o cálculo de atenção e seus intermediários.

Pergunta: Menor pico de memória prova mesma função?
Resposta: Não. A implementação pode ter mudado precisão, máscara ou conexões; compare a operação e seus resultados.

Pergunta: Por que registrar fallback?
Resposta: Sem isso, uma configuração aparentemente otimizada pode executar outro kernel e invalidar a interpretação de desempenho.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T098:C05 — mecanismo_avancado

A escolha de backend faz parte do comportamento operacional: um dispatcher pode selecionar caminhos distintos conforme forma, máscara, dtype e dispositivo. A memória economizada precisa ser atribuída à eliminação de intermediários, à aproximação ou à alteração de precisão, porque essas decisões têm garantias diferentes. Na API funcional documentada do PyTorch, dropout depende do argumento fornecido, mesmo quando o módulo chamador está em avaliação.

Condição de contorno:
Comparações entre implementações perdem sentido se uma delas aplica dropout, máscara ou escala diferentes sem registro.

Contrato proposto:
- Entradas: Tensores, semântica explícita de máscara, escala, dropout e backends permitidos.
- Saídas: Saída e identificação observável da implementação escolhida.
- Estado: Configuração de despacho, compilação e temporários necessários.
- Invariante: Troca de backend preserva a operação contratada dentro da tolerância numérica definida.

Compromissos de projeto:
- Fallback amplia cobertura e pode alterar bruscamente memória e latência.
- Precisão de acumulação maior melhora estabilidade com possível custo de execução.

## T098:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: chamar o caminho funcional com módulo em avaliação e dropout não zero; depois corrigir o argumento. Esperar variabilidade no primeiro caso e consistência compatível com o backend no segundo.

Plano de avaliação proposto:
Plano proposto: usar formas representativas e limites de especialização, fixando máscaras e precisão. Medir pico de memória, fallback e erro numérico; comparar prefill e decode separadamente e aprovar somente o caminho realmente despachado.

Comparações:
- T090 (complements): FlashAttention pode ser um backend eficiente, mas o rótulo amplo não especifica qual algoritmo foi executado.

Afirmação rastreável:
A documentação funcional do PyTorch exige dropout_p igual a zero para desativar dropout durante avaliação.
Suporte: direct; fontes: B-S017
Limite: O detalhe é específico da API consultada; outras interfaces podem administrar esse argumento automaticamente.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T098:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 advertiu sobre dispatch e dropout. A expansão organiza uma camada de negociação de capacidades, um fallback explícito e uma matriz de testes de semântica, para que memory-efficient seja uma propriedade medida da execução completa.

Negociação antes de servir
Construa uma tabela de recursos exigidos pelo modelo e oferecidos por cada backend: GQA, máscaras, offsets, gradientes e formatos numéricos. Rejeite combinações impossíveis no carregamento. Um fallback aceitável deve ser explícito e observado, pois usar um caminho denso pode ultrapassar memória apesar de produzir resultados corretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

Medição de pico e vida útil
Registre quando temporários são alocados e liberados em relação a KV, logits e comunicação. Economizar memória em uma operação não garante redução do pico global se outro buffer cresce ao mesmo tempo. Compare o perfil temporal, especialmente quando compilação, grafos ou múltiplas streams mantêm artefatos residentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

Semântica de máscaras
Use testes pequenos com resultados inspecionáveis para confirmar convenções de máscara, causalidade e escala. APIs distintas podem interpretar um booleano de modo diferente. Uma máscara válida por tipo pode inverter permissões sem erro; compare também atenção permitida em sequências unitárias, padding e fronteiras de documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

USO AVANÇADO — Backend portátil
Cenário: O mesmo produto precisa executar em CPU e diferentes GPUs.
Estratégia: Defina contrato de atenção independente do fornecedor, selecione implementação por capacidade e mantenha referência lenta para testes. Capture o backend efetivo nos logs. Não prometa números iguais entre dispositivos nem o mesmo conjunto de formatos.
Papel do modelo pequeno: Um 3–7B pode ter execução local simples; maiores modelos precisam de perfis de memória específicos.
Aceite proposto: Exigir ausência de fallback silencioso e qualidade consistente no conjunto de compatibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

USO AVANÇADO — Treino com margem apertada
Cenário: Um ajuste fino falha por pico de memória intermitente.
Estratégia: Meça vida útil de buffers e experimente atenção eficiente, checkpointing e limites de batch separadamente. Procure o pico verdadeiro antes de reduzir a tarefa. Se o fallback materializar matriz densa, trate-o como erro de configuração operacional.
Papel do modelo pequeno: Um 8–30B com adaptadores ainda precisa acomodar ativações e buffers da base.
Aceite proposto: Aprovar por redução do pico completo e estabilidade de passos com comprimentos extremos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, portabilidade e previsibilidade podem valer mais que um kernel especializado para um único acelerador.
8–14B: Em 8–14B, combinar métricas de pico com distribuição de contextos permite evitar OOMs esporádicos.
15–30B: Em 15–30B, avaliar buffers transitórios e comunicação, que podem consumir a margem liberada.
Requisitos de treino/runtime: Troca de implementação é runtime quando preserva a operação; aproximações ou máscaras novas mudam o contrato.
Não aplicar quando: Não escolher backend apenas pelo nome nem assumir que modo de avaliação desliga dropout em toda API funcional.

## T098:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Interface eficiente de atenção com caminhos especializados.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T098:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T098 → T090 [alternative]
Como combinar: Selecionar FlashAttention quando ele cobrir todos os requisitos e vencer na carga real.
Interface: Contrato de atenção, shapes e precisão.
Condição: Semântica é preservada e o kernel está disponível.
Aceite proposto: Comparar saída, pico global e tempo end-to-end.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S017, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T098 → T193 [complements]
Como combinar: Bloquear configuração incompatível antes que uma requisição alcance o acelerador.
Interface: Matriz de capacidades e manifesto do checkpoint.
Condição: Validação conhece os recursos obrigatórios.
Aceite proposto: Injetar combinações inválidas e exigir erro legível sem execução parcial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S017, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar convenções de máscara com casos mínimos de verdade conhecida.
- Registrar fallback e alocação de temporários em produção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar uma tarefa especializada em diferentes runtimes com a fronteira. Economia de memória pode viabilizar execução local; não transforma compatibilidade de API em equivalência de competência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T093, T113

## Fontes primárias associadas

### B-S017 — torch.nn.functional.scaled_dot_product_attention

[https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de implementações de atenção, máscaras e suporte dependente de backend.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T099 — Multi-Query Attention — MQA

**Nome canônico:** Multi-Query Attention — MQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T099  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-query attention; atenção multi-query

## T099:C01 — conceito

Arquitetura em que várias cabeças de consulta compartilham uma única cabeça de chaves e valores. Isso reduz armazenamento e leitura de KV em comparação com MHA equivalente. O compartilhamento faz parte dos pesos e do treinamento; não é simplesmente uma flag de compressão aplicável a todo checkpoint.

Como funciona:
- Projetar consultas em múltiplas cabeças.
- Produzir um conjunto compartilhado de chaves e valores por posição.
- Cada cabeça de consulta calcula seus scores contra o KV compartilhado.

## T099:C02 — aplicacao

Quando usar:
- Escolha de checkpoint prioriza eficiência de decode e memória.
- Projeto de modelo permite avaliar o compromisso entre compartilhamento e qualidade.

Quando não usar:
- Substituir cabeças de um modelo MHA por uma só sem conversão e treinamento apropriados.

Implementação proposta:
- Ler número de cabeças Q e KV na configuração do modelo.
- Confirmar que o kernel não materializa cópias desnecessárias do KV compartilhado.
- Comparar modelos ou variantes controlando capacidade e qualidade, não só VRAM.

Aplicação LAI proposta:
Proposta LAI: usar MQA como atributo na seleção de modelos; a decisão de runtime deve respeitar a arquitetura existente do Qwen escolhido.

## T099:C03 — riscos_validacao

Armadilhas:
- Menor número de cabeças KV não garante desempenho superior em toda tarefa.
- Uma implementação ingênua pode expandir KV e perder parte do benefício de armazenamento.

Métricas sugeridas:
- Bytes KV por token e banda de memória durante decode.
- Acerto do checkpoint em tarefas relevantes e latência por usuário.

Testes propostos:
- Verificar shapes reais dos tensores e compartilhamento sem cópia persistente indevida.
- Avaliar ferramentas e contexto longo antes de selecionar o modelo apenas por eficiência.

## T099:C04 — perguntas_proveniencia

Pergunta: Posso converter MHA em MQA apenas configurando num_kv_heads=1?
Resposta: Não. Isso muda a arquitetura e a interpretação dos pesos; uma conversão válida requer método e avaliação.

Pergunta: MQA é memória externa?
Resposta: Não. É organização interna das projeções da atenção.

Pergunta: A dimensão das consultas também cai?
Resposta: Não necessariamente. Múltiplas cabeças Q podem permanecer, enquanto o conjunto de K e V é compartilhado.

Pergunta: A fórmula representa toda a memória do servidor?
Resposta: Não. Pesos, temporários, reservas, tabelas e cópias distribuídas são parcelas adicionais que precisam ser medidas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T099:C05 — mecanismo_avancado

O compartilhamento de K e V preserva múltiplas consultas, mas reduz a diversidade dos espaços de chave e valor. Para camadas homogêneas, o cache idealizado ocupa 2·L·B·T·Hkv·d·s bytes, com camadas L, sequências B, tokens T, cabeças KV Hkv, dimensão d e bytes por valor s. Em MQA, Hkv é um, antes de replicações, padding e metadados.

Condição de contorno:
Essa redução é arquitetural; um checkpoint MHA não se converte de forma equivalente simplesmente descartando suas cabeças KV.

Contrato proposto:
- Entradas: Pesos compatíveis com MQA, consultas múltiplas e KV compartilhado.
- Saídas: Saídas por cabeça de consulta usando o mesmo conjunto KV.
- Estado: Cache com uma cabeça KV lógica por camada e sequência.
- Invariante: Compartilhamento não modifica a correspondência entre posições e estados do histórico.

Compromissos de projeto:
- Menor tráfego KV pode favorecer decode com contexto extenso.
- Capacidade representacional diferente pode exigir treinamento ou adaptação para preservar qualidade.

## T099:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar kernel compartilhado com referência que expande virtualmente K e V para todas as consultas. Injetar mapeamento posicional errado e esperar divergência detectável.

Plano de avaliação proposto:
Plano proposto: validar equivalência entre implementações do mesmo modelo antes de comparar arquiteturas treinadas. Medir bytes reais, replicações, latência por comprimento e qualidade; não atribuir diferenças de checkpoint somente ao número de cabeças.

Comparações:
- T100 (alternative): GQA mantém mais de um grupo KV e oferece outra troca entre compartilhamento e capacidade.

Afirmação rastreável:
O artigo de MQA compartilha chaves e valores entre cabeças para reduzir tráfego no decode incremental.
Suporte: direct; fontes: B-S018
Limite: A redução de tráfego é motivação arquitetural, não uma previsão universal de tempo end-to-end.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T099:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 quantificou a cabeça KV única. Agora a estratégia compara MQA como escolha de checkpoint e examina replicações físicas, conversão arquitetural e inferência em diferentes regimes, sem atribuir ao compartilhamento ganhos que vieram de outro modelo.

Seleção de modelo com controle
Comparar dois checkpoints diferentes mistura dados, treinamento, tokenizer e arquitetura. Use esse ensaio para escolher produto, mas não como prova causal de MQA. Se a pergunta for arquitetural, é preciso controlar o restante ou declarar a limitação. Memória menor é verificável pelo layout, enquanto qualidade depende do conjunto completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

Replicação distribuída
Uma cabeça KV lógica pode ser replicada em vários ranks para alimentar consultas particionadas. Some bytes em todos os dispositivos e observe comunicação necessária. A conta de uma única cópia não descreve automaticamente o sistema distribuído; aumentar TP pode reduzir pesos por rank sem reduzir KV na mesma proporção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

Ponto de equilíbrio da leitura
Meça quanto do decode vem de ler KV, de ler pesos e de executar outros operadores. MQA beneficia o primeiro componente, mas sua contribuição varia com contexto e batch. Para prompts curtos, a diferença pode ser pequena; em sessões extensas, o benefício potencial precisa ser confrontado com qualidade de dependências remotas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

USO AVANÇADO — Escolha para atendimento longo
Cenário: Há muitos turnos e poucas respostas simultâneas.
Estratégia: Compare modelos treinados com MQA e alternativas adequadas à tarefa, medindo memória e qualidade por comprimento. Preserve fatos distantes no teste e não escolha apenas pelo maior contexto que cabe. Inclua custo de recuperação quando ela for necessária.
Papel do modelo pequeno: Um 3–14B com MQA pode ser eficiente para uma tarefa estreita se mantiver qualidade suficiente.
Aceite proposto: Aprovar por respostas corretas dentro do orçamento e bytes reais por sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

USO AVANÇADO — Distribuição de modelo maior
Cenário: Um alvo não cabe confortavelmente em um dispositivo.
Estratégia: Inspecione como o backend distribui a cabeça KV e escolha TP considerando replicação. Compare com uma instância quantizada ou outra arquitetura suportada. Não reescreva pesos MHA descartando cabeças para simular MQA.
Papel do modelo pequeno: Um 15–30B pode precisar de distribuição, mas ganhos de memória devem ser medidos por rank.
Aceite proposto: Exigir contabilidade de memória total e latência de comunicação no caminho crítico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, avaliar se um checkpoint MQA já treinado atende o domínio antes de planejar conversão.
8–14B: Em 8–14B, comparar tamanho efetivo de cache e qualidade de atenção em conversas prolongadas.
15–30B: Em 15–30B, verificar replicação KV em TP e orçamento de cada dispositivo.
Requisitos de treino/runtime: MQA é arquitetura treinada; qualquer conversão de MHA exige método de adaptação e validação próprios.
Não aplicar quando: Não prometer a mesma qualidade ao trocar número de cabeças KV nem inferir economia física apenas da configuração lógica.

## T099:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005, V4B-Q016.

## T099:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T099 → T100 [alternative]
Como combinar: Comparar checkpoint GQA quando uma cabeça compartilhada comprometer qualidade ou distribuição.
Interface: Número de grupos, qualidade por tarefa e bytes medidos.
Condição: Modelos são avaliados como produtos, com diferenças declaradas.
Aceite proposto: Escolher pela fronteira qualidade/custo sem alegar causalidade isolada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S018, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T099 → T118 [complements]
Como combinar: Planejar replicação da cabeça compartilhada junto do particionamento de consultas.
Interface: Mapeamento de heads por rank e buffers de comunicação.
Condição: Backend suporta o layout corretamente.
Aceite proposto: Somar memória por rank e testar paridade com execução de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S018, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contar réplicas físicas e não somente cabeças lógicas.
- Registrar diferenças de treino ao comparar checkpoints com arquiteturas distintas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar atendimento longo com uma fronteira no mesmo domínio. MQA reduz custo de estado em modelos compatíveis; não oferece garantia de raciocínio, factualidade ou recuperação de contexto equivalentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T100, T106, T108

## Fontes primárias associadas

### B-S018 — Fast Transformer Decoding: One Write-Head is All You Need

[https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MQA compartilha chaves e valores entre cabeças de consulta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T100 — Grouped-Query Attention — GQA

**Nome canônico:** Grouped-Query Attention — GQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T100  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** grouped-query attention; atenção com consultas agrupadas

## T100:C01 — conceito

Arquitetura intermediária entre MHA e MQA: grupos de cabeças de consulta compartilham cabeças KV. Reduz o volume de KV sem usar necessariamente uma única cabeça compartilhada. O número de grupos é característica do checkpoint; o artigo de referência também investiga conversão com treinamento adicional.

Como funciona:
- Projetar várias cabeças de consulta e um conjunto menor de cabeças KV.
- Associar cada grupo de consultas à cabeça KV correspondente.
- Executar a atenção preservando esse mapeamento em treino e inferência.

## T100:C02 — aplicacao

Quando usar:
- Modelos precisam equilibrar capacidade da atenção e custo de decode.
- Planejamento de memória de um checkpoint que já utiliza GQA.

Quando não usar:
- Interpretar GQA como solução de cache que pode ser ativada sem mudar um checkpoint MHA incompatível.

Implementação proposta:
- Registrar num_attention_heads, num_key_value_heads e dimensão de cada cabeça.
- Estimar KV convencional como aproximadamente 2 × camadas × tokens × cabeças_KV × dimensão × bytes, ajustando arquitetura e batch.
- Medir memória real, pois alinhamento, paginação e outros estados alteram a estimativa.

Aplicação LAI proposta:
Proposta LAI: incluir o número real de cabeças KV no cálculo de concorrência do modelo local, em vez de estimar apenas pelo total de parâmetros.

## T100:C03 — riscos_validacao

Armadilhas:
- A divisão de cabeças precisa respeitar requisitos do modelo e kernel.
- A fórmula convencional não cobre automaticamente arquiteturas híbridas, compressão latente ou todas as camadas locais.

Métricas sugeridas:
- Memória observada versus estimativa para diferentes comprimentos.
- Latência de decode e acerto de tarefas do checkpoint.

Testes propostos:
- Conferir mapeamento de grupos com uma implementação de referência.
- Aumentar contexto e batch e verificar se a projeção de capacidade prevê a saturação.

## T100:C04 — perguntas_proveniencia

Pergunta: GQA é igual a MQA?
Resposta: MQA representa o caso de uma cabeça KV; GQA geralmente usa um número intermediário de grupos.

Pergunta: GQA reduz a quantidade de tokens de entrada?
Resposta: Não. Reduz parte dos estados por token, mantendo a sequência.

Pergunta: Mudar Hkv no arquivo de configuração basta?
Resposta: Não. Formas e significado dos pesos precisam corresponder; editar metadados não produz pesos corretamente adaptados.

Pergunta: Por que medir memória por GPU?
Resposta: A redução lógica pode ser parcialmente anulada por replicação necessária ao particionamento ou por expansões introduzidas no kernel.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T100:C05 — mecanismo_avancado

Com Hq consultas e Hkv grupos KV, cada consulta precisa apontar para o grupo correto. Nas configurações uniformes comuns, Hq é múltiplo de Hkv; o layout físico pode ainda repartir ou replicar grupos entre dispositivos. O número intermediário de grupos permite ajustar memória e diversidade de representação, mas constitui escolha de arquitetura e de pesos, não apenas uma política de alocação de cache.

Condição de contorno:
Uma implementação que expande materialmente todas as cabeças pode manter correção e perder parte da economia pretendida.

Contrato proposto:
- Entradas: Configuração de cabeças, pesos treinados ou adaptados e mapa consulta-grupo.
- Saídas: Saídas das consultas e cache com agrupamento consistente.
- Estado: Layout KV, shard por dispositivo e eventual replicação declarada.
- Invariante: O mesmo mapa de grupos é preservado no carregamento, prefill e decode.

Compromissos de projeto:
- Mais grupos podem aumentar diversidade e custo de cache.
- Distribuição entre GPUs pode introduzir replicação quando grupos não se repartem adequadamente.

## T100:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: permutar duas associações de grupos somente no decode. Comparar logits com prefill e referência expandida; a transição deve revelar a inconsistência.

Plano de avaliação proposto:
Plano proposto: primeiro comparar kernels com pesos idênticos; depois comparar arquiteturas com treinamento e avaliação controlados. Medir qualidade, bytes físicos por dispositivo e tempos de prefill/decode; aceitar a troca segundo o orçamento definido para a aplicação.

Comparações:
- T099 (alternative): MQA é o extremo com um grupo KV; GQA preserva múltiplos grupos.

Afirmação rastreável:
O trabalho de GQA apresenta grupos KV intermediários e uma receita de adaptação de checkpoints multi-head.
Suporte: direct; fontes: B-S019
Limite: Os resultados de adaptação do artigo não garantem qualidade de uma conversão arbitrária ou sem treinamento.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T100:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou mapeamento entre consultas e grupos. Esta ficha trata GQA na seleção de modelos e no planejamento distribuído, incluindo validação de layouts e separação entre mudança arquitetural, implementação de kernel e qualidade do checkpoint.

Grupos como restrição de implantação
Use números de heads Q/KV para verificar divisibilidade e estratégia de particionamento admitida pelo runtime. Quando grupos não se distribuem uniformemente, o backend pode replicar ou restringir TP. Essa escolha afeta memória e comunicação; valide antes de reservar máquinas com uma divisão que o modelo não suporta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

Conversão com orçamento completo
O trabalho de GQA investiga adaptação de checkpoints, mas isso não torna conversão gratuita. Planeje dados, treinamento adicional, validação e artefatos de rollback. Para um projeto aplicado, escolher um checkpoint já treinado com GQA pode ser mais simples; compare essa opção antes de investir em modificar arquitetura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

Qualidade versus implementação
Teste primeiro se o kernel preserva o mapeamento correto; depois avalie a qualidade do modelo. Um bug de expansão ou shard pode parecer perda inerente de GQA. Use referência que materializa grupos para comparar numericamente, mesmo que seja lenta, e só use o caminho compacto no serving após equivalência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

USO AVANÇADO — Servidor com memória limitada
Cenário: É necessário escolher entre modelos de porte semelhante.
Estratégia: Compare tarefas reais, tamanho de cache por comprimento e suporte do executor. Dê preferência ao candidato que entrega qualidade dentro do SLO, não ao menor número de grupos isoladamente. Registre tokenizer e treino como fatores de confusão.
Papel do modelo pequeno: Um 8–14B GQA pode oferecer equilíbrio útil entre cache e qualidade, sujeito a teste.
Aceite proposto: Aprovar por custo por resposta aceita e regressões por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

USO AVANÇADO — Portabilidade entre runtimes
Cenário: O checkpoint muda de biblioteca sem trocar pesos.
Estratégia: Valide ordem de heads, reshape e offsets com entradas curtas e longas. Compare prefill e decode separadamente. Se a nova biblioteca expande KV permanentemente, registre perda de memória mesmo quando as saídas permanecem corretas.
Papel do modelo pequeno: Um 3–30B precisa conservar o compartilhamento no layout físico para obter a economia pretendida.
Aceite proposto: Exigir erro numérico tolerado e bytes KV compatíveis com o layout documentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, V4B-S017, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, uma arquitetura já treinada com GQA permite experimentar baixo custo sem projeto de conversão.
8–14B: Em 8–14B, verificar qualidade por tarefa e eficiência do kernel antes de escolher o número de grupos.
15–30B: Em 15–30B, planejar TP pelo layout KV e possíveis réplicas, não só pelo tamanho das matrizes.
Requisitos de treino/runtime: A escolha de grupos pertence ao checkpoint; implementar compartilhamento é runtime, converter grupos exige adaptação.
Não aplicar quando: Não comparar modelos diferentes e atribuir toda diferença de desempenho exclusivamente a GQA.

## T100:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Tabela Q/KV documenta agrupamento nas variantes pertinentes.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005, V4B-Q016.

## T100:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T100 → T106 [feeds]
Como combinar: Fornecer o layout por camada para dimensionar cache e admissão.
Interface: Heads Q/KV, dimensões, dtype e política de retenção.
Condição: Configuração corresponde à revisão carregada.
Aceite proposto: Conferir estimativa com memória real por sequência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T100 → T090 [complements]
Como combinar: Executar atenção agrupada com backend fundido que preserve compartilhamento.
Interface: Q com múltiplas heads e KV agrupado.
Condição: Kernel suporta GQA sem expansão persistente desnecessária.
Aceite proposto: Comparar com referência expandida e medir temporários.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar correspondência de grupos após conversão de pesos e sharding.
- Manter referência numérica independente do caminho otimizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas específicas contra a fronteira sob orçamento total equivalente. GQA ajuda eficiência arquitetural, mas não permite concluir que um modelo pequeno alcança capacidades gerais de outro maior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T106, T108

## Fontes primárias associadas

### B-S019 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

[https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grupos de consultas compartilham cabeças KV; conversão proposta envolve treinamento.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T101 — Ring Attention

**Nome canônico:** Ring Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T101  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção em anel

## T101:C01 — conceito

Método para distribuir atenção de sequências extensas entre dispositivos. Mantém partes da sequência em GPUs diferentes e circula blocos KV em um anel, sobrepondo comunicação e cálculo quando possível. Não torna contexto ilimitado nem elimina a necessidade de conectividade e suporte do modelo.

Como funciona:
- Particionar consultas e estados por trechos da sequência.
- Enviar blocos KV entre dispositivos vizinhos no anel.
- Acumular atenção à medida que os blocos necessários passam por cada dispositivo.

## T101:C02 — aplicacao

Quando usar:
- Uma sequência excede memória operacional de um dispositivo.
- Existe infraestrutura multi-GPU com comunicação adequada e workload longo.

Quando não usar:
- Máquina de uma GPU ou contexto curto cujo custo de comunicação supera qualquer benefício.

Implementação proposta:
- Mapear topologia, banda e latência de comunicação antes da implementação.
- Preservar posições globais e máscara causal através das partições.
- Comparar atenção distribuída e referência local em sequências que cabem nas duas configurações.

Aplicação LAI proposta:
Proposta LAI: considerar somente em laboratório distribuído com necessidade demonstrada de uma sequência muito longa; não é otimização imediata para uma única 5090.

## T101:C03 — riscos_validacao

Armadilhas:
- Carga desigual por partição pode deixar dispositivos ociosos.
- Atrasos na comunicação podem impedir a sobreposição esperada e dominar o tempo total.

Métricas sugeridas:
- Memória por GPU, tempo de comunicação e tempo sobreposto.
- Eficiência ao aumentar número de dispositivos para uma sequência fixa.

Testes propostos:
- Comparar logits contra referência preservando dtype e tolerância numérica.
- Testar sequência irregular e falha de um participante; exigir erro controlado em vez de saída incompleta.

## T101:C04 — perguntas_proveniencia

Pergunta: Ring Attention aumenta a capacidade aprendida de contexto?
Resposta: Não por si só. Distribui o cálculo; posições e comportamento do checkpoint continuam limitando a utilidade.

Pergunta: Elimina o tráfego de rede?
Resposta: Não. Organiza a circulação de KV e tenta sobrepor o tráfego ao cálculo.

Pergunta: O anel reduz o número de pares atendidos?
Resposta: Não necessariamente. Pode preservar a atenção densa e apenas distribuir onde suas interações são calculadas.

Pergunta: Por que posições globais importam?
Resposta: A causalidade deve acompanhar a sequência original; índices locais de cada shard não determinam quais tokens estão no futuro.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T101:C05 — mecanismo_avancado

Sobrepor comunicação e computação não elimina bytes transmitidos: oculta parte do tempo quando existe trabalho suficiente enquanto o próximo bloco chega. Um limite simplificado por rodada é o maior entre duração de cálculo e transferência, acrescido de sincronização não ocultada. O primeiro carregamento e a drenagem final continuam relevantes. Blocos menores aumentam frequência de mensagens; maiores exigem mais memória temporária.

Condição de contorno:
Sequências curtas ou interconexão lenta podem tornar a comunicação dominante, frustrando a sobreposição assumida pelo projeto.

Contrato proposto:
- Entradas: Partições de consultas, blocos KV, topologia e máscara com posições globais.
- Saídas: Saídas locais normalizadas sobre todos os blocos globalmente permitidos.
- Estado: Buffers de envio/recepção, identificadores de rodada e acumuladores estáveis.
- Invariante: Cada bloco necessário contribui uma vez, independentemente da ordem de chegada.

Compromissos de projeto:
- Distribuir contexto reduz memória por dispositivo e adiciona comunicação.
- Mais dispositivos podem aumentar capacidade sem diminuir latência de uma requisição.

## T101:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar um elo e permutar a ordem de recebimento preservando os identificadores. Esperar espera controlada e resultado equivalente; duplicar um bloco deve ser detectado.

Plano de avaliação proposto:
Plano proposto: comparar implementação local e distribuída para casos que caibam em ambas. Controlar sequência, precisão e máscara; medir bytes transferidos, tempo exposto de comunicação e duração total, separando ganho de capacidade de ganho de velocidade.

Comparações:
- T117 (specializes): É uma organização específica da comunicação para distribuir o contexto entre dispositivos.

Afirmação rastreável:
Ring Attention propõe sobrepor comunicação de blocos KV com cálculo de atenção em blocos.
Suporte: direct; fontes: B-S020
Limite: O grau efetivo de sobreposição depende da relação entre cálculo, tamanho dos blocos e banda disponível.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T101:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu sobreposição e buffers do anel. O aprofundamento passa a planejar topologia, tolerância a falhas e limites econômicos, distinguindo processamento distribuído do contexto de simples aumento nominal da janela de entrada.

Topologia observada
Meça bandas e latências entre os dispositivos realmente usados, incluindo saltos entre hosts e contenção de outros jobs. Um anel lógico pode atravessar enlaces muito diferentes. Ordene ranks considerando a topologia e compare comunicação efetiva com trabalho por bloco, sem usar banda de catálogo como se fosse atingível na aplicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

Falha como unidade coletiva
Uma rodada incompleta não pode produzir um resultado silenciosamente parcial. Defina timeout e cancelamento coordenado para todos os participantes, preservando o pedido para recomputação. Registre qual bloco e rank faltaram; retornar atenção sobre um subconjunto muda a função e não é um fallback exato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

Custo de reservar o grupo
Mesmo que um prompt longo execute mais rápido, vários dispositivos ficam comprometidos com uma única entrada. Compare a redução de latência com a quantidade de outras tarefas que poderiam ser atendidas. Para tráfego misto, reserve paralelismo de contexto a pedidos que ultrapassem um limiar de custo observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

USO AVANÇADO — Leitura excepcionalmente longa
Cenário: Algumas entradas não cabem ou excedem o prazo em um dispositivo.
Estratégia: Selecione somente essas entradas para o grupo distribuído e mantenha o restante em réplicas locais. Teste acesso a evidências distantes e valide máscara global. Se não houver benefício líquido, reduza contexto via recuperação em vez de distribuir automaticamente.
Papel do modelo pequeno: Um 15–30B pode precisar de CP por contexto, mesmo quando seus pesos cabem localmente.
Aceite proposto: Aceitar por qualidade, prazo e custo de ocupação do grupo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

USO AVANÇADO — Experimento arquitetural
Cenário: Um estudo precisa validar atenção completa com sequência extensa.
Estratégia: Compare anel e referência em tamanhos menores, depois aumente comprimento e número de ranks. Teste falhas de comunicação e desbalanceamento. Preserve logs de posições e normalizadores para localizar perda ou duplicação de blocos.
Papel do modelo pequeno: Modelos 3–14B podem servir como protótipos controlados antes de ampliar recursos.
Aceite proposto: Exigir equivalência numérica e ausência de saída parcial quando um rank falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, múltiplos dispositivos raramente se justificam sem contexto extremo ou objetivo experimental explícito.
8–14B: Em 8–14B, medir se CP resolve memória de sequência melhor que outra estratégia de contexto.
15–30B: Em 15–30B, considerar ocupação do grupo e interação com TP antes de combinar paralelismos.
Requisitos de treino/runtime: Requer runtime distribuído, topologia adequada e modelo que suporte o contexto; não amplia treinamento posicional por si só.
Não aplicar quando: Não usar anel quando transferência domina ou quando a tarefa pode recuperar poucos trechos suficientes.

## T101:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Pass-KV/Pass-Q são descritos como variantes frequentemente chamadas ring attention, sem identificar toda implementação com o paper específico.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003.

## T101:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T101 → T117 [complements]
Como combinar: Implementar uma estratégia de comunicação para contexto particionado.
Interface: Blocos, posições globais e estado de normalização.
Condição: Todos os ranks compartilham a mesma semântica de atenção.
Aceite proposto: Comparar Pass-KV/alternativas com referência e medir custo coletivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T101 → T122 [complements]
Como combinar: Transportar blocos usando caminho de baixa intervenção CPU quando suportado.
Interface: Buffers registrados, eventos de conclusão e ordem de rodadas.
Condição: Hardware e biblioteca garantem visibilidade correta dos dados.
Aceite proposto: Injetar atrasos e verificar que consumo espera a transferência completa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Nunca publicar resultado de uma rodada incompleta.
- Relatar custo total de dispositivos e comunicação, além da latência isolada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perguntas de contexto extenso com fronteira incluindo custo de todos os dispositivos. Ring Attention viabiliza cálculo distribuído; não prova entendimento confiável de toda a informação acessível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T117, T118, T122

## Fontes primárias associadas

### B-S020 — Ring Attention with Blockwise Transformers for Near-Infinite Context

[https://arxiv.org/abs/2310.01889](https://arxiv.org/abs/2310.01889)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sequência distribuída e circulação de blocos KV com computação sobreposta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T102 — Disaggregated Inference / Disaggregated Prefill-Decode

**Nome canônico:** Inferência com prefill e decode desagregados  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T102  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Disaggregated Inference / Prefill-Decode; prefill-decode disaggregation; inferência desagregada; Disaggregated Prefill-Decode; PD disaggregation

## T102:C01 — conceito

Disaggregated Inference, no escopo desta ficha, separa prefill e decode em instâncias ou conjuntos de recursos distintos. Prefill processa a entrada e produz estados KV; decode reutiliza esses estados para gerar tokens. A arquitetura permite ajustar capacidade e latência por fase, mas acrescenta transferência, coordenação e compatibilidade de estados. Separar recursos não demonstra ganho automático de throughput.

Como funciona:
- Encaminhar a entrada para um worker de prefill e produzir o KV correspondente à sequência tokenizada.
- Transferir ou disponibilizar o KV por um conector compatível e encaminhar a continuação ao worker de decode.
- Dimensionar os grupos considerando filas, comprimento de entrada, duração da geração e custo da interconexão.

## T102:C02 — aplicacao

Quando usar:
- Cargas mistas nas quais prompts longos interferem no intervalo entre tokens de gerações já em andamento.

Quando não usar:
- Quando o custo de movimentar KV supera o benefício, há pouca concorrência ou o backend não suporta a configuração pretendida.

Implementação proposta:
- Proposta: medir uma instalação integrada como baseline e separar TTFT, latência entre tokens, transferência de KV e filas de cada fase.
- Fixar revisão de pesos, tokenizer, tokens de entrada, dtype e layout compatíveis; validar também adaptadores e opções de paralelismo.
- Definir timeout e limpeza para transferência incompleta e cancelamento; liberar buffers que perderam seu consumidor.
- Comparar desagregação com chunked prefill sob a mesma carga antes de escolher a topologia.

Aplicação LAI proposta:
Proposta LAI: avaliar desagregação apenas depois de medir interferência entre fases e validar o conector no hardware escolhido; não há implantação demonstrada neste corpus.

## T102:C03 — riscos_validacao

Armadilhas:
- Repetir tokenização ou usar revisões diferentes pode tornar o KV inválido.
- Um grupo ocioso e outro saturado elevam custo sem reduzir latência; tráfego de KV pode virar gargalo.

Métricas sugeridas:
- TTFT e ITL p95/p99, bytes e tempo de transferência, utilização de cada pool e custo por solicitação completa.

Testes propostos:
- Teste proposto: comparar saídas equivalentes com execução integrada e rastrear IDs de sequência através da transferência.
- Interromper a conexão durante envio de KV e confirmar falha explícita, limpeza e ausência de continuação com estado incorreto.

## T102:C04 — perguntas_proveniencia

Pergunta: Desagregar significa executar duas cópias completas da mesma geração?
Resposta: Não. As fases são separadas e compartilham os estados necessários; duplicar o trabalho eliminaria parte do benefício esperado.

Pergunta: O recurso do vLLM promete mais throughput?
Resposta: A documentação consultada o apresenta para ajustar TTFT e ITL e declara que não melhora throughput; resultados de outras arquiteturas exigem medição própria.

Pergunta: Goodput é igual a tokens por segundo?
Resposta: Não. Aqui interessa trabalho concluído atendendo aos prazos definidos, não apenas produção bruta.

Pergunta: É suficiente enviar o tensor?
Resposta: Não. O destino também precisa saber posições, formas, dtype, identidade dos pesos e qual continuação aquele estado representa.

Escopo das fontes:
vLLM fundamenta a separação e suas limitações; Dynamo apoia gestão de KV. Topologia e testes são propostas.

## T102:C05 — mecanismo_avancado

A separação de fases introduz uma transferência de propriedade do estado KV. Como proposta de contrato, o worker de decode só deve iniciar após receber todos os segmentos necessários e verificar identidade, comprimento e layout. O tempo mínimo de transporte inclui bytes divididos pela banda efetiva, além de latência e serialização. Separar filas permite alocação diferente para prefill e decode, mas não elimina essa conta.

Condição de contorno:
Quando prompts são pequenos ou o transporte é caro, a perda de localidade pode superar a redução de interferência entre fases.

Contrato proposto:
- Entradas: Tokens processados, estado KV versionado, destino e configuração compatível dos workers.
- Saídas: Confirmação de transferência e ponto de continuação inequívoco.
- Estado: Manifesto de segmentos, offsets recebidos e proprietário atual do pedido.
- Invariante: Decode nunca usa cache parcial nem mistura segmentos de revisões distintas.

Compromissos de projeto:
- Pools independentes permitem dimensionar fases conforme suas cargas.
- Transferência adiciona falhas parciais, memória transitória e pressão na rede.

## T102:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper o envio após algumas camadas e duplicar uma confirmação. Esperar retomada idempotente ou reconstrução explícita, sem geração baseada em estado incompleto.

Plano de avaliação proposto:
Plano proposto: comparar colocação conjunta e separada com mesmos recursos totais e chegadas. Medir TTFT, tempo por token, goodput dentro dos prazos e tráfego KV; aceitar somente quando os objetivos conjuntos melhoram no cenário real.

Comparações:
- T122 (complements): RDMA pode reduzir custos de transferência, mas não substitui o contrato de consistência.

Afirmação rastreável:
DistServe separa prefill e decode e considera banda de comunicação ao escolher alocação e posicionamento.
Suporte: direct; fontes: V3B-S010
Limite: O estudo não garante benefício com qualquer rede ou número de GPUs.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T102:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu entrega íntegra do KV antes do decode. A expansão aborda filas independentes, transferência por camada, cancelamento e ponto de equilíbrio, para dimensionar a arquitetura por demanda real e não por promessa abstrata de separação.

Capacidade em duas filas
Estime chegadas de tokens de entrada e de saída separadamente. Um pool de prefill rápido pode inundar decode com estados que não cabem; um pool de decode amplo pode ficar ocioso se não receber prompts prontos. Use controle de admissão que considere vagas no destino antes de produzir KV caro de transportar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

Transferência progressiva
Um sistema pode começar a transferir camadas já prontas enquanto o restante do prefill executa, como no relato da Perplexity. A aplicação precisa de manifesto e confirmação por segmento, com início do decode condicionado à prontidão exigida. Sobreposição reduz espera possível, mas não elimina bytes nem necessidade de consistência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

Cancelamento e propriedade
Se o cliente cancelar durante transporte, coordene liberação na origem e no destino. Uma confirmação tardia não pode reativar a requisição. Use identificador de tentativa e geração do estado para impedir que uma transferência antiga seja anexada a uma repetição posterior do mesmo pedido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

USO AVANÇADO — Entradas longas e saídas interativas
Cenário: Prefills extensos interrompem frequentemente o streaming.
Estratégia: Compare chunked prefill local com pools separados. Inclua banda, buffers, filas e falhas no ensaio. Escolha separação apenas se aumentar tarefas dentro do SLO; alocar mais máquinas sem igualar custo não demonstra superioridade da arquitetura.
Papel do modelo pequeno: Um 15–30B pode justificar separação em volume alto, sem que isso seja necessário em um único servidor.
Aceite proposto: Aprovar por goodput e custo completo, com TTFT e intervalos de saída separados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

USO AVANÇADO — Fleet com recursos diferentes
Cenário: Há dispositivos adequados a cálculo e outros com maior memória disponível.
Estratégia: Planeje perfis de prefill/decode compatíveis em pesos, layout e dtype. Valide transferência antes de experimentar hardware heterogêneo. Se for necessária conversão de KV, meça erro e tempo; não suponha interoperabilidade binária.
Papel do modelo pequeno: Um 3–14B só merece essa complexidade se demanda e custo de fila compensarem.
Aceite proposto: Exigir continuidade numérica e recuperação sem duplicação após falha de worker.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S010, V4B-S002, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, começar pelo serviço agregado; overhead de transporte pode superar interferência evitada.
8–14B: Em 8–14B, avaliar separação apenas após medir mistura de comprimentos e demanda sustentada.
15–30B: Em 15–30B, perfilar crescimento KV e dimensionar pools pela distribuição de entrada/saída.
Requisitos de treino/runtime: Requer runtime/conector compatíveis, transferência de estados e coordenação; não altera pesos nem competência do modelo.
Não aplicar quando: Não adotar em baixa demanda apenas por ser usado em infraestruturas de grande escala.

## T102:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: A seção de deployment separa explicitamente prefill e decoding.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: A descrição operacional separa clusters de prefill e decode.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: Separação de pools e transporte de KV são descritos na implementação do operador.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003.

## T102:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T102 → T122 [complements]
Como combinar: Transferir KV por camada com conclusão observável antes do consumo.
Interface: Páginas KV, metadados e sinalização entre workers.
Condição: Caminho RDMA e registro de memória são suportados.
Aceite proposto: Medir transporte e impedir decode com estado parcial.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S002. Casos: V4B-C002.

2. T102 → T094 [alternative]
Como combinar: Reduzir interferência mantendo fases no mesmo worker quando transporte não compensa.
Interface: Orçamento de chunks e SLO por fase.
Condição: Runtime local consegue intercalar trabalho corretamente.
Aceite proposto: Comparar custo igualado e caudas nas mesmas chegadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S010, V4B-S002, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Impor backpressure quando decode não possui capacidade para novo KV.
- Testar cancelamento, replay e transferência atrasada com IDs de tentativa diferentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar responsividade de uma tarefa contra a fronteira incluindo todos os nós e rede. Separação pode melhorar eficiência do serviço; não amplia conhecimento, raciocínio ou precisão do checkpoint.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T094, T120, P009

## Fontes primárias associadas

### B-S021 — Disaggregated Prefilling (experimental)

[https://docs.vllm.ai/en/latest/features/disagg_prefill/](https://docs.vllm.ai/en/latest/features/disagg_prefill/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação de prefill e decode em instâncias; ajuste independente de latências; recurso experimental na página consultada.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S010 — DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

[https://arxiv.org/abs/2401.09670](https://arxiv.org/abs/2401.09670)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interferência entre prefill/decode, objetivos TTFT/TPOT e alocação considerando banda de comunicação.

Limite: Resumo consultado; regras de transferência e testes de falha das fichas são propostas editoriais.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

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

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T103 — Prefix Tree / Trie de prefixos

**Nome canônico:** Prefix Tree / Trie de Prefixos  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T103  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** prefix trie; árvore de prefixos; Prefix Tree / Trie de Prefixos

## T103:C01 — conceito

Estrutura de dados que organiza sequências pelo início compartilhado. Em um índice de cache, cada caminho pode apontar para estados associados ao prefixo. Uma radix tree comprime caminhos de filho único em arestas mais longas; a estrutura sozinha não executa atenção.

Como funciona:
- Percorrer tokens em ordem para localizar o maior prefixo comum.
- Criar ou dividir caminhos quando novas sequências divergem.
- Associar referências de estado aos trechos e atualizar o índice após remoções.

## T103:C02 — aplicacao

Quando usar:
- Muitas sequências compartilham segmentos iniciais extensos.
- É útil localizar o maior prefixo disponível em vez de somente um hash de prompt inteiro.

Quando não usar:
- Usar similaridade semântica como se significasse identidade de tokens para cache KV exato.

Implementação proposta:
- Definir chaves com tokens e escopo de modelo, adaptador e tenant.
- Separar nós do índice de alocações físicas para permitir remoção segura.
- Documentar operações atômicas de inserir, consultar, dividir e invalidar.

Aplicação LAI proposta:
Proposta LAI: estudar a estrutura para entender o runtime e o roteamento; evitar construir uma trie paralela na Helena sem necessidade operacional.

## T103:C03 — riscos_validacao

Armadilhas:
- Índice stale pode apontar para memória já liberada.
- Textos com o mesmo início visível podem ter tokens diferentes devido ao template ou espaços.

Métricas sugeridas:
- Tamanho do índice, custo de busca e comprimento do prefixo encontrado.
- Taxa de referências inválidas e memória liberada após remoções.

Testes propostos:
- Inserir sequências com prefixos comuns em ordens diferentes e exigir resultados equivalentes de busca.
- Remover uma folha sem afetar irmãos e remover o último uso sem deixar referências pendentes.

## T103:C04 — perguntas_proveniencia

Pergunta: Trie é igual a árvore de resumos?
Resposta: Não. Organiza prefixos de sequências exatas, não níveis de abstração semântica.

Pergunta: Radix tree é outra família de cache?
Resposta: É uma variação compactada da estrutura de prefixos, usada por algumas implementações de cache.

Pergunta: Pode indexar pelo texto decodificado?
Resposta: Somente com um contrato que preserve identidade de tokenização; textos aparentes iguais não garantem os mesmos IDs.

Pergunta: Dividir uma aresta exige copiar todo o KV?
Resposta: Não necessariamente. A divisão lógica pode alterar referências para segmentos existentes quando o armazenamento permite compartilhamento.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T103:C05 — mecanismo_avancado

A árvore representa ancestralidade exata: compartilhar um sufixo textual não torna dois caminhos equivalentes se seus prefixos anteriores diferem. Numa radix tree, uma aresta pode carregar vários tokens; uma divergência no meio dessa aresta exige divisão sem perder a correspondência entre posições e referências KV. A complexidade de busca depende dos tokens comparados e da representação das arestas, não somente do número de nós.

Condição de contorno:
Uma árvore de strings normalizadas pode produzir identidade diferente da tokenização realmente usada pelo modelo.

Contrato proposto:
- Entradas: Sequências de token IDs, domínio de identidade e referências dos estados disponíveis.
- Saídas: Maior prefixo compatível e ponto exato para inserir ou dividir caminhos.
- Estado: Rótulos de arestas, ligações, comprimentos e referências de cache.
- Invariante: O caminho completo desde a raiz identifica o contexto; um nó isolado não basta.

Compromissos de projeto:
- Arestas comprimidas reduzem nós e complicam divisões parciais.
- Índice maior melhora cobertura potencial e aumenta manutenção e memória de CPU.

## T103:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir sequências que divergem dentro da mesma aresta e outras com sufixos iguais. Esperar divisão correta e nenhum hit baseado apenas na igualdade dos últimos tokens.

Plano de avaliação proposto:
Plano proposto: comparar trie simples e radix tree com as mesmas sequências. Medir tokens comparados, nós, memória e tempo de atualização; exigir que todas as buscas concordem com uma referência linear de maior prefixo.

Comparações:
- T104 (complements): RadixAttention usa a estrutura para organizar estados; a árvore sozinha não executa atenção.

Afirmação rastreável:
O SGLang descreve radix tree com arestas que podem representar sequências de tokens de comprimentos variados.
Suporte: direct; fontes: V3B-S011
Limite: A estrutura de dados não determina política de escalonamento, memória física ou validade dos pesos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T103:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou ancestralidade e divisão de arestas. Esta camada trata o trie como catálogo de disponibilidade distribuída: possuir um caminho lógico não significa que seus tensores estejam prontos para consumo.

Identidade versus residência
Separe a chave lógica, formada pelo prefixo tokenizado e sua configuração, do descritor de residência. Um nó pode apontar para GPU, RAM, armazenamento ou reconstrução pendente. A consulta deve retornar comprimento reutilizável e custo estimado de materialização; considerar todo nó encontrado um hit rápido mascara transferências e pode piorar a primeira resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Publicação de caminhos
Insira referências inicialmente privadas e publique apenas estados completos. Se o produtor for cancelado durante prefill, o caminho não pode anunciar um bloco parcialmente escrito. Um protocolo proposto marca geração, quantidade válida e confirmação; consumidores leem uma visão consistente enquanto divisões de arestas e remoções avançam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Granularidade de persistência
Uma árvore pode comprimir arestas em tokens, enquanto o armazenamento transfere páginas maiores. Mantenha o deslocamento entre ambas as unidades e contabilize bytes úteis versus transportados. Prefixos ligeiramente divergentes podem multiplicar páginas mesmo quando a representação lógica permanece compacta; a cardinalidade dos nós não estima sozinha o consumo físico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Biblioteca de ferramentas estável
Cenário: Agentes compartilham descrições extensas de ferramentas.
Estratégia: Ordene componentes por estabilidade, versione o template e mantenha dados voláteis após a região compartilhada. Consulte a árvore antes de reservar a cópia física, preservando isolamento entre locatários.
Papel do modelo pequeno: Um 3–7B consome um contrato de ferramentas consistente sem depender de memória paramétrica adicional.
Aceite proposto: Comparar tokens reutilizados e bytes transferidos, além de testar revogação de ferramentas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Auditoria de divergência
Cenário: Duas versões do serviço perdem reutilização inesperadamente.
Estratégia: Instrumente o primeiro token divergente, a versão do tokenizer e o template. Produza um diagnóstico agregado sem registrar segredos presentes nos prompts.
Papel do modelo pequeno: Um modelo pequeno pode explicar relatórios já sanitizados; o cálculo da divergência é determinístico.
Aceite proposto: Localizar mudanças introduzidas deliberadamente e não confundir divergência legítima com erro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize poucos prefixos de alta repetição; uma árvore ampla pode custar mais que recomputar prompts curtos.
8–14B: Teste várias famílias de prompts e limite a retenção por família, evitando que um fluxo domine o catálogo.
15–30B: Modele residência por dispositivo: encontrar um prefixo de um 30B pode exigir transferência incompatível com o prazo.
Requisitos de treino/runtime: Recurso de runtime; tokenizer, pesos, adapters e posições participam da identidade.
Não aplicar quando: Não reutilizar caminhos entre configurações incompatíveis ou usar semântica textual aproximada como igualdade KV.

## T103:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: HiRadixTree organiza spans de tokens e seus locais de armazenamento.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T103:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T103 → T104 [feeds]
Como combinar: A árvore fornece candidatos de prefixo para a política de Radix Attention.
Interface: Comprimento compatível, referências, residência e custo.
Condição: O escalonador interpreta somente estados confirmados.
Aceite proposto: Cancelar produtores e verificar que consumidores não leem estados incompletos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T103 → T105 [complements]
Como combinar: Expulsão física atualiza disponibilidade sem apagar necessariamente a descrição lógica.
Interface: Estado de presença e plano de reconstrução.
Condição: Não existir consumidor ativo sem referência protegida.
Aceite proposto: Comparar resultado após restore com execução fria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não exportar tokens de prompts privados em métricas de divergência.
- Testar split, merge e remoção concorrentes com prefixos que terminam dentro de uma página.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o serviço completo em uma coleção fixa de consultas repetidas. O trie pode reduzir recomputação; não melhora a resposta de um modelo pequeno a uma pergunta que ele não consegue resolver.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T104, T120

## Fontes primárias associadas

### B-S022 — SGLang: Efficient Execution of Structured Language Model Programs

[https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention reutiliza KV com estrutura de prefixos.

Limite: Resumo e versão HTML abertos; foco no mecanismo de reuso. Resultados publicados não reproduzidos.

### V3B-S011 — SGLang: Efficient Execution of Structured Language Model Programs — full text

[https://arxiv.org/html/2312.07104v2](https://arxiv.org/html/2312.07104v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention, busca de prefixos e ciclo de vida/remoção de cache em árvore.

Limite: Texto do projeto consultado; não representa garantia de compatibilidade de implantação ou reprodução de resultados.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T104 — Radix Attention

**Nome canônico:** RadixAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T104  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RadixAttention

## T104:C01 — conceito

RadixAttention é o mecanismo apresentado pelo SGLang para reutilização sistemática de cache KV por meio de uma radix tree. Relaciona prefixos de tokens a estados disponíveis. Seu nome pode sugerir uma nova fórmula de atenção, mas o foco é reuso e gerenciamento dos estados.

Como funciona:
- Encontrar o maior prefixo compatível na árvore de estados.
- Reaproveitar o trecho disponível e calcular a continuação ausente.
- Atualizar referências e política de remoção conforme novas requisições usam o cache.

Nota de nomenclatura: Normalização do nome original do inventário; preservado como técnica específica do SGLang.

## T104:C02 — aplicacao

Quando usar:
- Workflows repetem exemplos, instruções ou prefixos de conversação.
- Existe runtime que implementa o mecanismo com telemetria adequada.

Quando não usar:
- Esperar benefício quando prompts quase não compartilham início ou quando retenção reduz capacidade útil do batch.

Implementação proposta:
- Construir uma amostra com padrões reais de repetição, não somente prompts sintéticos idênticos.
- Comparar execução fria e aquecida e medir impacto em admissão de novas sequências.
- Avaliar justiça entre requisições com muito e pouco prefixo reutilizável.

Aplicação LAI proposta:
Proposta LAI: avaliar RadixAttention ao comparar runtimes em missões com prefixos reutilizados, mantendo igual modelo e conjunto de tarefas.

## T104:C03 — riscos_validacao

Armadilhas:
- Priorizar somente afinidade de cache pode aumentar espera de entradas novas.
- Cache aquecido em um worker não garante hit após roteamento para outro.

Métricas sugeridas:
- Proporção de tokens reaproveitados e tempo de prefill evitado.
- Tempo de espera por grupo e custo de manter a árvore.

Testes propostos:
- Repetir prefixos com continuações distintas e verificar saídas corretas e estados compartilhados válidos.
- Misturar tráfego sem repetição e exigir que a política não o prive de serviço.

## T104:C04 — perguntas_proveniencia

Pergunta: RadixAttention substitui o Transformer?
Resposta: Não. É uma técnica de runtime para aproveitar estados já calculados.

Pergunta: É sinônimo de todo prefix caching?
Resposta: Não. É uma implementação específica; cache de prefixos também pode usar outras estruturas.

Pergunta: Pode usar hits como único objetivo?
Resposta: Não. Eles ignoram quem está esperando e o custo de memória imposto às sequências ativas.

Pergunta: RadixAttention altera os pesos de atenção?
Resposta: Seu mecanismo de reúso organiza estados já calculados; uma implementação correta preserva a operação do modelo.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T104:C05 — mecanismo_avancado

O escalonamento orientado por afinidade de prefixo busca amortizar a construção do estado ao atender pedidos relacionados próximos no tempo. Isso cria uma tensão com justiça: pedidos sem prefixos populares podem esperar enquanto novas consultas compatíveis continuam chegando. Como proposta de integração, idade e prazo devem limitar essa preferência. O cache compartilhado também compete por memória com sequências ativas e seus tokens futuros.

Condição de contorno:
Uma boa taxa de hits pode coexistir com starvation ou piora da latência de classes pouco frequentes.

Contrato proposto:
- Entradas: Pedidos, afinidade de prefixo, idade, prioridades e capacidade KV disponível.
- Saídas: Ordem de execução com justificativa de afinidade e limites de espera.
- Estado: Árvore de estados, referências ativas e fila com tempos originais.
- Invariante: A política de reúso não altera conteúdo do pedido nem perde sua identidade.

Compromissos de projeto:
- Ordenar por afinidade reduz prefill repetido e pode prejudicar equidade.
- Reter históricos libera trabalho futuro e ocupa capacidade que poderia admitir novas sequências.

## T104:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alimentar continuamente um prefixo popular enquanto um pedido sem hit aguarda. Esperar execução dentro da regra de envelhecimento proposta, sem exigir que o pedido mude seu prompt.

Plano de avaliação proposto:
Plano proposto: comparar ordem de chegada e afinidade limitada por prazo com a mesma carga. Medir tokens recalculados, TTFT por classe, pior espera e throughput útil; aceitar economia de trabalho somente com equidade previamente definida.

Comparações:
- T103 (complements): A radix tree fornece correspondências; a política decide quando usar essa afinidade.

Afirmação rastreável:
O artigo do SGLang discute escalonamento por maior prefixo compartilhado e reconhece risco de starvation.
Suporte: direct; fontes: V3B-S011
Limite: A propriedade de reúso descrita para lotes não vira garantia geral de justiça em tráfego online.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T104:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu afinidade e justiça. O aprofundamento acrescenta seleção entre recuperar, transferir e recomputar, considerando que o prefixo pode estar disponível em diferentes níveis de memória.

Hit com custo
Na hierarquia HiCache, localizar um prefixo não encerra a decisão: restaurá-lo consome banda e pode disputar recursos com decodes ativos. Proponha comparar tempo estimado de restauração com prefill restante. Um prefixo maior em armazenamento pode ser menos vantajoso que um prefixo menor já residente; registre qual alternativa foi escolhida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Afinidade sob mudança de carga
Preferência por uma família de prompts precisa reagir à taxa de chegada. Popularidade passada pode manter estados sem utilidade e concentrar fila num worker. Use janelas de observação e idade do pedido, mas evite recalcular prioridades a cada token: essa oscilação pode tornar a política mais cara que a economia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Estado adicional
Modelos híbridos e mecanismos especulativos podem demandar estados além de KV convencional. Não restaure apenas a parcela que o índice conhece. A interface de cache deve enumerar componentes necessários, suas versões e o ponto até o qual representam o mesmo prefixo; caso contrário, trate o reúso como incompleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Sessões com retomada
Cenário: Um usuário retorna a uma conversa longa depois de minutos.
Estratégia: Conserve metadados leves, coloque tensores em camada mais barata e restaure sob prazo. Se a previsão de transferência falhar, recalcule a partir de tokens confirmados sem misturar duas histórias.
Papel do modelo pequeno: Modelos 8–14B podem sustentar diálogos especializados com sessões intermitentes.
Aceite proposto: Medir tempo de retomada e consistência após expiração, sem contar restore como hit instantâneo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Lote com prefixos heterogêneos
Cenário: Consultas analíticas compartilham documentos diferentes.
Estratégia: Agrupe por afinidade apenas até o limite de espera e intercale famílias pouco populares. Limite quanto cada família pode manter residente.
Papel do modelo pequeno: Um 15–30B recebe contexto específico sem exigir que todos os documentos permaneçam na GPU.
Aceite proposto: Avaliar espera por família e total de trabalho concluído dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em prompts curtos, compare contra recomputação simples antes de adicionar armazenamento remoto.
8–14B: Busque equilíbrio entre sessões ativas e prefixos adormecidos; ambos competem pela mesma capacidade.
15–30B: Considere custo de restaurar várias camadas ou partições, e não apenas tamanho agregado.
Requisitos de treino/runtime: Runtime e formato de estado devem suportar o modelo escolhido; HiCache documentado não prova qualquer arquitetura.
Não aplicar quando: Não aplicar afinidade rígida quando uma família mantém fila permanentemente congestionada.

## T104:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: HiCache estende explicitamente RadixAttention.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T104:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T104 → T083 [complements]
Como combinar: A política consulta a hierarquia para escolher o melhor prefixo realmente materializável.
Interface: Residência, previsão de transferência e orçamento de banda.
Condição: Estimativas atualizadas e limite para restauração.
Aceite proposto: Induzir saturação da camada inferior e observar mudança para recomputação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T104 → T121 [requires]
Como combinar: O agendamento deve considerar custo e justiça além do tamanho do prefixo.
Interface: Idade original, deadline e afinidade.
Condição: Prioridade não reiniciada após reencaminhamento.
Aceite proposto: Verificar ausência de starvation em mistura de prompts.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar taxa de localização lógica da taxa de reutilização efetivamente consumida.
- Restaurar metadados e tensores como uma unidade consistente ou invalidar o candidato.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com um serviço de fronteira deve usar retomadas e concorrência equivalentes. Radix Attention otimiza execução; não compensa uma janela treinada insuficiente nem assegura compreensão de documentos extensos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T105, T171

## Fontes primárias associadas

### B-S022 — SGLang: Efficient Execution of Structured Language Model Programs

[https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention reutiliza KV com estrutura de prefixos.

Limite: Resumo e versão HTML abertos; foco no mecanismo de reuso. Resultados publicados não reproduzidos.

### V3B-S011 — SGLang: Efficient Execution of Structured Language Model Programs — full text

[https://arxiv.org/html/2312.07104v2](https://arxiv.org/html/2312.07104v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention, busca de prefixos e ciclo de vida/remoção de cache em árvore.

Limite: Texto do projeto consultado; não representa garantia de compatibilidade de implantação ou reprodução de resultados.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T105 — KV Cache Eviction

**Nome canônico:** KV Cache Eviction  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T105  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** despejo de cache KV

## T105:C01 — conceito

Remoção de estados KV para liberar memória. É preciso separar descarte de cache reutilizável ocioso, preempção com recomputação e poda de tokens ainda necessários à atenção. As duas primeiras podem preservar a semântica; a última normalmente altera o que o modelo consegue consultar.

Como funciona:
- Determinar quais blocos estão em uso e quais são candidatos a remoção.
- Aplicar política de retenção e atualizar todas as referências ao bloco.
- Recomputar quando necessário ou declarar explicitamente a mudança de contexto se houver poda.

## T105:C02 — aplicacao

Quando usar:
- Cache de prefixos compete com novas sequências pela mesma memória.
- Há política definida para pressão e recuperação sem corrupção de estado.

Quando não usar:
- Descartar KV ativo silenciosamente e continuar como se o contexto permanecesse completo.

Implementação proposta:
- Classificar cada evento como remoção ociosa, preempção recuperável ou compressão com perda.
- Proteger estados referenciados e impedir uso após liberação.
- Limitar ciclos de despejo e recomputação que produzem thrashing.

Aplicação LAI proposta:
Proposta LAI: alertar sobre thrashing do runtime e reduzir admissão antes de permitir que uma política de memória altere silenciosamente o contexto da missão.

## T105:C03 — riscos_validacao

Armadilhas:
- Alta taxa de acerto pode esconder alto custo de recomputar sequências preemptadas.
- Remover por idade é inadequado se o objeto antigo ainda está em uso.

Métricas sugeridas:
- Evictions por classe, recomputações e bytes recuperados.
- Latência de cauda e trabalho repetido por pressão de memória.

Testes propostos:
- Reduzir memória disponível e verificar que todas as saídas continuam corretas no modo sem perda.
- Retomar uma sequência preemptada e comparar com referência sem preempção.

## T105:C04 — perguntas_proveniencia

Pergunta: Apagar KV sempre faz o modelo esquecer?
Resposta: Não se o estado for reconstruído antes do uso; poda sem reconstrução é uma operação diferente.

Pergunta: Eviction libera memória de pesos?
Resposta: Não. Atua nos estados de atenção, não no checkpoint carregado.

Pergunta: Eviction é equivalente a esquecer informação?
Resposta: Só quando o estado deixa de ser reconstruído antes de necessário; um cache dispensável pode ser removido sem perda semântica.

Pergunta: Qual métrica revela thrashing?
Resposta: Recomputações repetidas dos mesmos tokens, associadas a transferências ou preempções, além de baixa progressão efetiva da geração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T105:C05 — mecanismo_avancado

Expulsar cache pode significar remover uma cópia reconstruível de prefixo inativo ou eliminar estados ainda necessários ao contexto de uma sequência. O primeiro caso muda custo; o segundo muda a função do modelo, salvo reconstrução antes do uso. Uma política de memória precisa declarar qual semântica pratica. Custo de reconstrução e probabilidade de reúso podem orientar retenção, mas são estimativas sujeitas a mudanças de carga.

Condição de contorno:
Uma política aparentemente econômica pode gerar thrashing quando estados expulsos são reconstruídos repetidamente antes de terminar a requisição.

Contrato proposto:
- Entradas: Pressão de memória, referências ativas, estimativas de reúso e custo de reconstrução.
- Saídas: Blocos removidos, bytes liberados e plano para futuros acessos.
- Estado: Disponibilidade física, histórico reconstruível e dependências dos consumidores.
- Invariante: Nenhum estado necessário desaparece silenciosamente do contexto lógico prometido.

Compromissos de projeto:
- Reter estados caros economiza cálculo futuro e limita admissões.
- Políticas sofisticadas custam metadados e podem reagir mal a estimativas desatualizadas.

## T105:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: forçar pressão durante duas continuações que compartilham um ancestral e acessá-lo novamente após remoção permitida. Esperar proteção de referências ativas ou reconstrução correta, sem contexto reduzido ocultamente.

Plano de avaliação proposto:
Plano proposto: comparar LRU e uma política baseada em custo sob sequências de acesso controladas. Medir bytes liberados, recomputação, misses, preempções e latência; escolher pelo custo total preservando a semântica contratada.

Comparações:
- T116 (complements): Recomputação pode restaurar estado removido quando o histórico necessário permanece disponível.

Afirmação rastreável:
O desenho de RadixAttention protege nós usados por requisições ativas e remove folhas elegíveis.
Suporte: direct; fontes: V3B-S011
Limite: A política documentada não representa todas as variantes de poda ou compressão de contexto.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T105:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou expulsão reconstruível de remoção semântica. Esta estratégia acrescenta custo de oportunidade, proteção durante transferências e experimentos que medem o prejuízo futuro da decisão.

Valor por recurso escasso
Uma política proposta estima benefício de reúso dividido pelo recurso que bloqueia: bytes de GPU, banda de restore ou espaço de armazenamento. O recurso dominante muda durante a carga. Um prefixo popular pode merecer retenção na RAM sem merecer GPU; usar somente frequência mistura decisões de níveis distintos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

Estados em trânsito
Evicção, cópia e cancelamento podem se cruzar. Dê a cada transferência uma referência temporária e um destino ainda não publicável; a remoção da origem só é segura quando existe cópia confirmada ou reconstrução possível. Contadores de referências devem sobreviver a retries e não depender exclusivamente do término normal do pedido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

Custo contrafactual
Conte misses causados por expulsão recente e tempo gasto em reconstrução, preservando uma amostra de decisões. Isso permite distinguir uma política agressiva demais de uma mudança genuína de demanda. Não atribua toda queda de hit rate à evicção: versões de templates, adapters e distribuição de usuários também alteram os prefixos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

USO AVANÇADO — Picos de conversas novas
Cenário: Uma campanha aumenta sessões sem histórico compartilhado.
Estratégia: Reduza retenção de prefixos inativos antes de limitar sequências em execução. Preserve uma margem para crescimento dos decodes e revise a pressão depois do pico.
Papel do modelo pequeno: Um 3–7B pode aceitar mais sessões sem alterar a semântica do contexto ativo.
Aceite proposto: Confirmar ausência de OOM e registrar reconstruções posteriores causadas pela intervenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

USO AVANÇADO — Cache com documentos sensíveis
Cenário: Uma fonte é revogada ou expira.
Estratégia: Propague invalidação por versão e domínio de acesso, tornando cópias antigas inelegíveis mesmo antes de sua remoção física. Não confunda liberação de memória com revogação lógica.
Papel do modelo pequeno: O modelo pequeno continua recebendo somente contexto autorizado na nova versão.
Aceite proposto: Testar revogação em GPU, RAM e armazenamento, incluindo transferências já iniciadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031, B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Use políticas simples quando o custo de manutenção superar o prefill evitado; não deduza isso só do número de parâmetros.
8–14B: Meça o conjunto de sessões simultâneas e o crescimento das respostas antes de reservar cache inativo.
15–30B: Uma política favorável ao reúso pode impedir o carregamento de novos pedidos grandes; trate capacidade como orçamento explícito.
Requisitos de treino/runtime: Runtime precisa expor referências, cancelamento e residência. Remover tokens do contexto requer método aproximado separado.
Não aplicar quando: Não expulsar estados ativos sem reconstrução antes do próximo uso.

## T105:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T105:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T105 → T084 [complements]
Como combinar: A validade de prefixos inclui expiração e revogação, além de pressão de memória.
Interface: Versão, domínio de acesso e marcador de invalidação.
Condição: Workers observam a mesma regra de elegibilidade.
Aceite proposto: Repetir um pedido após revogação e provar que não ocorreu reúso antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031, B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T105 → T086 [alternative]
Como combinar: Comparar compactação KV com evicção permite escolher entre perda numérica e recomputação.
Interface: Bytes liberados, erro observado e custo de restore.
Condição: Experimentos separam as duas intervenções.
Aceite proposto: Conferir qualidade e latência em ensaios isolados e depois combinados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031, B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contabilizar memória ainda referenciada como capacidade imediatamente recuperada.
- Simular cancelamento durante cópia e reinício do worker com restauração incompleta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A política deve ser comparada pelo custo de servir respostas válidas, incluindo reconstrução. Aumentar cache hit não estabelece vantagem de qualidade frente a um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T093, T104, T116

## Fontes primárias associadas

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S011 — SGLang: Efficient Execution of Structured Language Model Programs — full text

[https://arxiv.org/html/2312.07104v2](https://arxiv.org/html/2312.07104v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention, busca de prefixos e ciclo de vida/remoção de cache em árvore.

Limite: Texto do projeto consultado; não representa garantia de compatibilidade de implantação ou reprodução de resultados.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T106 — Otimização de KV com MQA/GQA

**Nome canônico:** Otimização do armazenamento KV em modelos MQA/GQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T106  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** GQA/MQA KV Optimization; KV cache com cabeças compartilhadas; MQA/GQA KV optimization

## T106:C01 — conceito

Otimização de KV com MQA/GQA significa preservar no serving o compartilhamento de cabeças definido pelo modelo. MQA usa uma cabeça KV compartilhada; GQA usa grupos com menos cabeças KV que cabeças de consulta. Isso reduz o volume lógico do cache comparado a MHA, mantendo as demais dimensões. Não é uma terceira arquitetura nem um botão que converte qualquer checkpoint sem consequências.

Como funciona:
- Ler no checkpoint os números de cabeças de consulta e KV, dimensão por cabeça, camadas e dtype do cache.
- Armazenar cabeças KV compartilhadas sem duplicação persistente desnecessária e mapear consultas aos grupos corretos.
- Usar kernels e layouts compatíveis para evitar que uma expansão materializada elimine a economia de memória.

## T106:C02 — aplicacao

Quando usar:
- Servir checkpoints MQA/GQA sob restrição de memória ou largura de banda, especialmente com contextos longos e múltiplas sequências.

Quando não usar:
- Para inferir o consumo total da GPU apenas pelo número de cabeças ou alterar a arquitetura declarada de um modelo arbitrariamente.

Implementação proposta:
- Proposta: estimar KV como 2 × camadas × sequências × tokens × cabeças_KV × dimensão_cabeça × bytes, quando K e V têm a mesma dimensão.
- Tratar a fórmula como estimativa lógica: adicionar páginas, fragmentação, reservas, replicação entre dispositivos e outros buffers.
- Comparar buffers físicos e shapes com o desenho esperado; verificar suporte de backend, dtype e distribuição de cabeças no paralelismo escolhido.
- Validar logits ou respostas contra uma execução de referência; conversão de MHA para MQA/GQA é outro procedimento, podendo exigir treinamento.

Aplicação LAI proposta:
Proposta LAI: dimensionar concorrência usando as cabeças KV reais do modelo e medições do executor, mantendo separado o orçamento dos pesos.

## T106:C03 — riscos_validacao

Armadilhas:
- Confundir redução do cache com redução proporcional da memória dos pesos.
- Replicar cabeças para compatibilidade de um kernel pode reduzir ou anular a economia prática.

Métricas sugeridas:
- Bytes de KV por token e sequência, pico de memória, largura de banda e latência de decode.

Testes propostos:
- Teste proposto: dobrar o comprimento e conferir crescimento esperado do cache, separando memória reservada de efetivamente usada.
- Comparar múltiplos grupos e sequências para detectar mistura de cabeças ou contaminação entre requisições.

## T106:C04 — perguntas_proveniencia

Pergunta: MQA e GQA são técnicas de compressão textual?
Resposta: Não. Alteram o compartilhamento de chaves e valores na atenção; o texto da entrada pode continuar idêntico.

Pergunta: Por que T106 não usa apenas T100 como canônico?
Resposta: Este registro trata a operação de serving aplicável a MQA e GQA; T099 e T100 descrevem as arquiteturas específicas.

Pergunta: Como considerar camadas locais e globais?
Resposta: Use comprimentos retidos por camada, em vez de multiplicar todas por um único comprimento total.

Pergunta: Menos bytes por token garante mais usuários?
Resposta: Apenas se KV for o limitante relevante e outros recursos, prazos e reservas também suportarem a concorrência adicional.

Escopo das fontes:
Papers MQA/GQA e documentação de atenção fundamentam o mecanismo; dimensionamento operacional e testes são propostas.

## T106:C05 — mecanismo_avancado

O orçamento KV deve ser calculado por camada e dispositivo, pois arquiteturas híbridas podem ter números de cabeças ou comprimentos retidos diferentes. Uma soma útil é Σcamadas 2·B·Tcamada·Hkv_camada·dcamada·scamada bytes, antes de padding e réplicas. MQA/GQA reduzem Hkv lógico; o runtime precisa manter essa economia no layout físico, evitando materializar cópias persistentes para cada cabeça de consulta.

Condição de contorno:
Replicação por paralelismo, kernels incompatíveis ou camadas de atenção global podem tornar a economia menor que a previsão simplificada.

Contrato proposto:
- Entradas: Configuração por camada, comprimentos retidos, dtype e plano de particionamento.
- Saídas: Estimativa detalhada e medição de bytes KV por dispositivo.
- Estado: Grupos lógicos, réplicas físicas, reservas e buffers temporários.
- Invariante: Toda economia declarada distingue valores úteis de memória realmente alocada.

Compromissos de projeto:
- Mais grupos preservam diversidade com maior custo por token.
- Repartir grupos exige comunicação ou replicação conforme o plano distribuído.

## T106:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: instrumentar alocações ao alternar entre um kernel com broadcast e outro que materializa expansão. Esperar mesma saída, mas detectar explicitamente a diferença de bytes físicos.

Plano de avaliação proposto:
Plano proposto: comparar previsão por camada com medições em vários comprimentos e concorrências. Separar pesos, KV e temporários; investigar divergências antes de estimar capacidade máxima e validar limites sob crescimento real de saídas.

Comparações:
- T100 (complements): A arquitetura define grupos; o planejamento operacional verifica sua representação física.

Afirmação rastreável:
GQA usa um número de cabeças KV intermediário entre MQA e MHA convencional.
Suporte: direct; fontes: B-S019
Limite: A contagem arquitetural não inclui automaticamente réplicas, alinhamento ou reservas do servidor.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T106:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou KV por camada e dispositivo. A nova camada liga esse orçamento ao limite de concorrência, à arquitetura efetiva do checkpoint e ao caminho de execução que pode desperdiçar a economia lógica.

Do checkpoint à reserva
Extraia número de cabeças KV, dimensões, tipos de camada e limites de retenção do checkpoint real. Converta a estimativa em reserva por sequência usando comprimento de entrada e crescimento permitido da saída. Dividir VRAM apenas pelo tamanho dos pesos ignora justamente o benefício e o custo que MQA/GQA pretendem controlar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

Representação versus expansão
Algumas interfaces aceitam grupos de consultas mas expandem K/V temporariamente para atender um kernel. Isso pode preservar resultados e ainda aumentar pico de memória ou tráfego. Examine o caminho selecionado, incluindo fallback, para saber se a redução arquitetural chega ao armazenamento e às leituras relevantes durante decode.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

Comparação de modelos
Dois checkpoints com igual quantidade de parâmetros podem ter largura, profundidade e grupos KV distintos. A comparação operacional deve incluir bytes por token e custo de atenção, além de pesos. Qwen3 publica configurações diferentes; sua família não autoriza presumir a configuração ou o backend do modelo existente no servidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

USO AVANÇADO — Dimensionamento de sessões
Cenário: Um serviço precisa suportar conversas de tamanhos variados.
Estratégia: Construa classes de reserva por contexto e libere margem ao terminar cada pedido. Use configuração real e medição física para calibrar o estimador.
Papel do modelo pequeno: Um 8–14B pode ser escolhido por equilíbrio entre qualidade especializada e custo por sessão.
Aceite proposto: Estimativas devem prever pico por dispositivo sem subestimar réplicas ou buffers.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

USO AVANÇADO — Seleção de checkpoint
Cenário: Há candidatos 3–30B com respostas semelhantes no domínio.
Estratégia: Compare qualidade, memória dos pesos, KV por token e latência sob a mesma distribuição de contexto. Evite converter um MHA existente apenas para obter uma linha melhor na planilha.
Papel do modelo pequeno: O modelo menor assume tarefas cujo conhecimento vem de evidência recuperada.
Aceite proposto: Selecionar pelo serviço dentro do orçamento, com testes de dependência longa preservados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma redução de KV pode ampliar concorrência mesmo quando pesos já cabem; confirme que o trabalho é limitado por cache.
8–14B: Com grupos KV suficientes, particionamento pode ser conveniente, mas divisibilidade deve ser verificada.
15–30B: Em 15–30B, atenção, pesos e comunicação competem; reduzir KV não elimina o restante do consumo.
Requisitos de treino/runtime: Arquitetura requer pesos compatíveis. Otimização de layout e kernels é de runtime, mantendo a estrutura treinada.
Não aplicar quando: Não trocar número de cabeças KV em configuração e esperar preservação automática da função.

## T106:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Configuração permite dimensionar KV, mas economia física depende do executor.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q016, V4B-Q005.

## T106:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T106 → T100 [requires]
Como combinar: A economia GQA depende da razão entre cabeças de consulta e KV do checkpoint.
Interface: Configuração por camada e layout físico.
Condição: Carregamento confirma grupos e projeções corretos.
Aceite proposto: Comparar logits e bytes com implementação de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, B-S018, V4B-S020, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T106 → T087 [feeds]
Como combinar: O orçamento de cache informa admissão de sequências no lote contínuo.
Interface: Reserva por sequência e capacidade livre real.
Condição: Crescimento futuro incluído na admissão.
Aceite proposto: Submeter mistura de contextos e observar falta de memória e espera.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, B-S018, V4B-S020, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar parâmetros ativos de MoE como tamanho dos pesos residentes.
- Relatar separadamente memória útil, alocada e pico de temporários.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Um modelo pequeno com GQA pode servir mais contexto simultâneo que outro candidato, mas isso não demonstra raciocínio superior. Compare tarefas cuja evidência cabe na janela e que tenham resposta verificável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T100, T081, P009

## Fontes primárias associadas

### B-S018 — Fast Transformer Decoding: One Write-Head is All You Need

[https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MQA compartilha chaves e valores entre cabeças de consulta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S019 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

[https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grupos de consultas compartilham cabeças KV; conversão proposta envolve treinamento.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S017 — torch.nn.functional.scaled_dot_product_attention

[https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de implementações de atenção, máscaras e suporte dependente de backend.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T107 — Roofline Analysis

**Nome canônico:** Roofline Analysis  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T107  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** análise Roofline; intensidade aritmética

## T107:C01 — conceito

Modelo de desempenho que relaciona operações por byte movimentado à capacidade de cálculo e à banda da memória. O limite idealizado é P ≤ min(P_pico, B × I), em que I é intensidade aritmética. Ajuda a distinguir gargalo de memória e de computação; não prevê sozinho toda a latência de um serviço.

Como funciona:
- Estimar ou medir operações e bytes movimentados no nível de memória relevante.
- Situar o kernel frente aos limites de banda e cálculo do hardware.
- Investigar a distância entre desempenho observado e teto aplicável.

## T107:C02 — aplicacao

Quando usar:
- Decidir se reduzir bytes ou aumentar paralelismo computacional pode ajudar.
- Comparar fases de prefill e decode em vez de usar uma média única.

Quando não usar:
- Usar FLOPs de marketing e banda nominal para prometer latência de ponta a ponta.

Implementação proposta:
- Medir kernels representativos com profiler e excluir aquecimento da comparação estável.
- Usar banda sustentada e precisão correspondentes à operação real.
- Adicionar ao diagnóstico custos de CPU, sincronização, lançamentos e rede que o modelo simplificado omite.

Aplicação LAI proposta:
Proposta LAI: antes de comprar hardware ou trocar modelos, identificar se a missão espera por memória da GPU, cálculo, ferramentas, CPU ou rede.

## T107:C03 — riscos_validacao

Armadilhas:
- Intensidade calculada com bytes teóricos pode ignorar releituras e cache misses.
- Um kernel próximo do teto ainda pode ser caro por executar trabalho desnecessário.

Métricas sugeridas:
- FLOP/s observados, bytes/s e intensidade aritmética.
- Parcela do tempo em memória, cálculo e overhead fora dos kernels.

Testes propostos:
- Reduzir tráfego em um kernel diagnosticado como limitado por banda e verificar se o tempo responde como previsto.
- Repetir análise por fase e batch; rejeitar explicação única que não descreva as mudanças observadas.

## T107:C04 — perguntas_proveniencia

Pergunta: GPU a 100% significa cálculo no limite?
Resposta: Não. Utilização agregada não revela qual recurso limita o kernel.

Pergunta: Roofline prevê qualidade da resposta?
Resposta: Não. É análise de execução; a qualidade precisa de avaliações separadas.

Pergunta: Bytes reservados servem como tráfego?
Resposta: Não. Um buffer pode ser lido várias vezes ou permanecer em cache; capacidade e movimentação são medidas diferentes.

Pergunta: Baixa utilização prova falta de trabalho paralelo?
Resposta: Não exclusivamente. Dependências, comunicação, latência de memória ou instruções distintas também podem limitar a execução.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T107:C05 — mecanismo_avancado

Um ponto de roofline só é interpretável quando operações e bytes correspondem ao mesmo nível de memória e caminho de instruções. Reúso em cache pode reduzir tráfego externo sem reduzir leituras internas. O teto de computação também depende de dtype e uso real das unidades matriciais. Distância ao teto sugere espaço para investigação, mas não identifica sozinha latência de lançamentos, dependências ou comunicação entre dispositivos.

Condição de contorno:
Medir durante profiling pode alterar concorrência, aquecimento de cache e duração; comparar diretamente com tráfego normal exige cautela.

Contrato proposto:
- Entradas: Contadores de operações e tráfego, duração, dtype e configuração de profiling.
- Saídas: Ponto de intensidade aritmética e hipóteses sobre o teto aplicável.
- Estado: Metadados de dispositivo, frequências, repetição e estado de cache.
- Invariante: Numerador, denominador e tempo descrevem a mesma região de execução.

Compromissos de projeto:
- Mais métricas esclarecem gargalos e podem exigir replay adicional.
- Uma otimização local pode deslocar o gargalo para outra fase do serviço.

## T107:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: calcular intensidade usando bytes alocados em vez de bytes transferidos e comparar com contadores. Esperar discrepância detectável que impeça concluir o gargalo com a estimativa incorreta.

Plano de avaliação proposto:
Plano proposto: separar medição de latência sem profiler e investigação de kernels selecionados. Controlar aquecimento, formas e dtype; cruzar contadores com implementação e decidir por melhorias end-to-end reproduzíveis, não por aproximação isolada ao teto.

Comparações:
- T090 (complements): Reduzir tráfego intermediário pode mudar a posição do kernel no roofline.

Afirmação rastreável:
O guia Nsight Compute relaciona desempenho a intensidade aritmética e tetos de banda e computação, alertando para efeitos de profiling.
Suporte: direct; fontes: V3B-S012
Limite: O modelo é diagnóstico de execução; não prevê integralmente filas, rede ou qualidade de respostas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T107:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 fixou a interpretação dos eixos do roofline. O aprofundamento propõe usar medições para escolher intervenções, observando fases, concorrência e os custos que o gráfico não representa.

Uma carga, vários pontos
Separe projeções, atenção, comunicação e amostragem; prefill e decode produzem regimes distintos mesmo no mesmo modelo. Um ponto médio pode ocultar atenção limitada por tráfego e projeções limitadas por computação. Colete formas dos tensores e duração junto aos contadores para não otimizar uma região de pouca importância.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S023, V3B-S012, V4B-S003.

Mudança com o lote
Aumentar lote pode elevar reúso dos pesos e mudar intensidade aritmética, mas também elevar fila e KV. Faça a análise em lotes que realmente ocorrem no serviço, não somente no maior lote possível. A melhor utilização do dispositivo pode coexistir com pior tempo de resposta individual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S023, V3B-S012, V4B-S003.

Custo fora do kernel
Lançamentos, sincronização, cópias e coletivas podem dominar depois de otimizar um operador. Um kernel mais perto do teto não prova redução proporcional do pedido. Relacione o perfil ao caminho crítico e confirme se o tempo economizado não foi simplesmente deslocado para preparação, descompactação ou comunicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S023, V3B-S012, V4B-S003.

USO AVANÇADO — Decidir entre quantizar e agrupar
Cenário: Decode apresenta baixa utilização aparente.
Estratégia: Meça tráfego de pesos e KV, depois varie lote e precisão separadamente. Use o perfil para decidir se reduzir bytes tem possibilidade de afetar o gargalo observado.
Papel do modelo pequeno: Um 3–7B pode ser limitado por lançamentos ou baixa concorrência, não necessariamente por capacidade computacional.
Aceite proposto: A intervenção deve reduzir duração do caminho crítico sem degradar o contrato de resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S023, V3B-S012, V4B-S003.

USO AVANÇADO — Justificar múltiplas GPUs
Cenário: Um 15–30B cabe em um dispositivo, mas parece lento.
Estratégia: Compare perfil local com particionado, incluindo coletivas e volume por token. Se comunicação consome a economia de computação, mantenha uma réplica inteira ou teste outro grau de paralelismo.
Papel do modelo pequeno: O porte menor permite explorar réplicas independentes antes de distribuir um único modelo.
Aceite proposto: Registrar latência e custo por resposta sob a mesma chegada de pedidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S023, V3B-S012, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Examine overheads fixos e kernels pequenos; um teto teórico alto pode ser irrelevante.
8–14B: Compare prefill longo e decode curto, que podem pedir intervenções diferentes.
15–30B: Inclua banda interconexão e custo de partição quando o modelo atravessa dispositivos.
Requisitos de treino/runtime: Ferramenta de profiling deve suportar o dispositivo e medir a região correta; coleta pode perturbar execução.
Não aplicar quando: Não usar FLOPs teóricos, tokens por segundo e bytes de níveis diferentes na mesma inferência.

## T107:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020.

## T107:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T107 → T085 [feeds]
Como combinar: O perfil identifica se quantização de pesos ataca tráfego relevante.
Interface: Contadores por operador e caminho de desquantização.
Condição: Formato possui kernel executável no ambiente.
Aceite proposto: Comparar perfil antes e depois, além da qualidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S023, V3B-S012, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T107 → T113 [feeds]
Como combinar: Fusão é priorizada quando materializações ou lançamentos estão no caminho crítico.
Interface: Sequência de operadores, temporários e dependências.
Condição: Fusão mantém semântica e não eleva pressão excessiva de registradores.
Aceite proposto: Medir pedido completo e operador isolado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S023, V3B-S012, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar aquecimento, frequências e concorrência para permitir reprodução.
- Não transformar proximidade ao teto em diagnóstico causal único.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Use roofline para explicar custo computacional da solução pequena. A comparação de competência exige outro ensaio: ele não informa se o modelo tomou uma decisão correta ou se precisou de mais tentativas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T087, T090, T118, T121

## Fontes primárias associadas

### B-S023 — The Roofline Model: Visualizing and Optimizing Performance

[https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/](https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites de desempenho pela intensidade aritmética, banda de memória e capacidade de cálculo.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S012 — Nsight Compute Profiling Guide

[https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roofline, intensidade aritmética, níveis de memória e perturbações causadas por profiling/replay.

Limite: Documentação dinâmica consultada; fórmulas de planejamento nas fichas são modelos simplificados, não medições locais.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T108 — Multi-Head Attention — MHA

**Nome canônico:** Multi-Head Attention — MHA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T108  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-head attention; atenção multicabeças

## T108:C01 — conceito

Mecanismo de atenção com múltiplas projeções de consultas, chaves e valores. Cada cabeça produz uma combinação de valores segundo compatibilidade entre consultas e chaves; os resultados são combinados. Na MHA convencional, cada cabeça tem seu próprio KV, diferentemente do compartilhamento de MQA/GQA.

Como funciona:
- Projetar a entrada em Q, K e V por cabeça.
- Calcular softmax(QKᵀ/√d) com a máscara adequada e aplicar aos valores.
- Combinar as saídas das cabeças por concatenação e projeção.

## T108:C02 — aplicacao

Quando usar:
- Entender e dimensionar checkpoints que usam MHA.
- Construir referência para comparar implementações alternativas de atenção.

Quando não usar:
- Tratar cada cabeça como especialista interpretável ou agente independente sem evidência.

Implementação proposta:
- Identificar número de cabeças, dimensão, máscara e esquema posicional.
- Conferir tensor shapes e evitar trocar eixos de batch, sequência e cabeça.
- Usar referência simples para validar um kernel otimizado ou nova forma de cache.

Aplicação LAI proposta:
Proposta LAI: usar MHA como fundamento para entender custos e como contraste com o esquema real do modelo local, sem tentar redesenhar o checkpoint em produção.

## T108:C03 — riscos_validacao

Armadilhas:
- Atenção causal incorreta permite acesso a tokens futuros.
- A quantidade de cabeças isolada não mede inteligência nem qualidade do modelo.

Métricas sugeridas:
- Memória KV por token e custo da atenção por comprimento.
- Erro numérico da implementação e desempenho de tarefa do modelo completo.

Testes propostos:
- Modificar apenas tokens futuros e exigir que posições anteriores permaneçam invariantes no modo causal.
- Comparar execução em lote e individual removendo diferenças de padding.

## T108:C04 — perguntas_proveniencia

Pergunta: Cada cabeça é um agente?
Resposta: Não. É um conjunto de projeções e operações internas treinadas conjuntamente.

Pergunta: Trocar MHA por GQA preserva o modelo automaticamente?
Resposta: Não. A mudança requer uma conversão válida e avaliação, normalmente com treinamento adicional.

Pergunta: Uma cabeça corresponde sempre a uma função humana?
Resposta: Não. Especializações podem surgir, mas precisam de evidência; a numeração sozinha não carrega significado.

Pergunta: A escala garante boa calibração?
Resposta: Não. Ela regula magnitude dos scores de atenção, não a probabilidade de uma resposta factual estar correta.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T108:C05 — mecanismo_avancado

A escala 1/√d controla a magnitude dos produtos entre consultas e chaves sob hipóteses usuais sobre seus componentes. Sem escala adequada, o softmax pode concentrar massa e produzir gradientes pouco informativos. A interpretação de uma cabeça também depende da projeção final: permutar cabeças juntamente com a permutação inversa nos blocos da projeção pode preservar a função, mostrando que números de cabeça não têm significado sem os pesos associados.

Condição de contorno:
Mapa de atenção visual não constitui prova causal de que determinado token sustentou a conclusão textual do modelo.

Contrato proposto:
- Entradas: Projeções QKV, dimensão por cabeça, máscara, escala e projeção de saída.
- Saídas: Representações combinadas preservando ordem e layout das cabeças.
- Estado: Pesos de projeção e convenção de concatenação dos resultados.
- Invariante: Carregamento e execução usam a mesma correspondência entre cabeças e projeção final.

Compromissos de projeto:
- Mais cabeças repartem capacidade em subespaços e afetam formas dos kernels.
- MHA convencional mantém KV separado, aumentando memória frente a compartilhamento arquitetural.

## T108:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: permutar cabeças com compensação na projeção final e depois sem compensação. Esperar equivalência no primeiro caso e divergência no segundo, isolando um erro de layout.

Plano de avaliação proposto:
Plano proposto: validar a operação contra implementação explícita em formas pequenas e diferentes máscaras. Medir erro de saída, estabilidade e custo, mantendo pesos idênticos; comparações de qualidade entre arquiteturas precisam controlar treinamento e capacidade.

Comparações:
- T099 (distinct_from): MQA compartilha K e V; isso muda a parametrização, não apenas a concatenação final.

Afirmação rastreável:
O Transformer original combina múltiplas projeções de atenção e uma projeção final de suas saídas.
Suporte: direct; fontes: B-S024
Limite: A interpretação sobre permutações é uma derivação algébrica do layout, não um resultado experimental relatado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T108:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou escala e correspondência das cabeças. A nova camada considera interoperabilidade de pesos, contribuições funcionais e alternativas de adaptação sem confundir inspeção visual com causalidade.

Convenções de carregamento
QKV pode estar fundido, intercalado por cabeça ou separado; a projeção final também possui ordem específica. Ao converter pesos, documente reshape, transposição, posição e dtype. Teste entradas curtas e longas, pois um erro de posição pode passar em exemplos mínimos mesmo quando as dimensões são válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

Cabeças como componentes
Mapas de atenção revelam pesos de mistura, não uma explicação completa da decisão. Para investigar uma cabeça, use ablação controlada e observe efeito na tarefa e em exemplos próximos. A projeção de saída, resíduos e demais camadas podem compensar alterações; uma visualização chamativa não prova especialização universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

Ajustar sem redesenhar
Quando o objetivo é domínio novo, adapters nas projeções podem ser uma intervenção mais controlada que remover cabeças. Identifique se o problema exige novas associações, formato ou evidência externa antes de alterar arquitetura. Reduzir cabeças modifica capacidade e demanda treinamento e avaliação, não apenas um parâmetro de serving.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

USO AVANÇADO — Migração de formato
Cenário: Pesos precisam passar entre ferramentas de treinamento e inferência.
Estratégia: Crie uma comparação progressiva de projeções e saídas por camada. Investigue o primeiro ponto divergente em vez de confiar somente numa resposta textual final aparentemente correta.
Papel do modelo pequeno: Um 3–7B permite validar a cadeia de conversão com custo menor antes de modelos maiores.
Aceite proposto: Logits devem obedecer tolerâncias declaradas e a máscara causal deve permanecer correta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

USO AVANÇADO — Diagnóstico de informação ignorada
Cenário: Um modelo recebe fatos no contexto mas não os usa.
Estratégia: Varie distância, distratores e posição da evidência; depois teste ablações ou adaptações pequenas. Use recuperação e organização do contexto como alternativas mensuráveis.
Papel do modelo pequeno: Um 8–14B pode melhorar num domínio restrito sem acrescentar capacidade arbitrária de memória.
Aceite proposto: A melhora deve sobreviver à troca de entidades e à inserção de informações contraditórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Prefira preservar arquitetura conhecida e investir em contexto ou adaptação antes de redesenhar cabeças.
8–14B: Use adapters para hipóteses específicas; não atribua toda melhora à atenção se o treino modifica outros módulos.
15–30B: Conversões maiores ampliam custo de validar tensores e checkpoints; mantenha testes em amostras representativas.
Requisitos de treino/runtime: MHA é arquitetura treinada; kernels podem mudar sem mudar seu grafo matemático, dentro das tolerâncias numéricas.
Não aplicar quando: Não usar pesos de atenção como prova direta da fonte factual de uma resposta.

## T108:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T108:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T108 → T098 [complements]
Como combinar: Uma interface de atenção eficiente executa a operação com máscaras e layouts explícitos.
Interface: QKV, escala, máscara e convenção de eixos.
Condição: Backend suporta forma e dtype usados.
Aceite proposto: Comparar forward e, se houver treino, gradientes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S024, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T108 → T182 [complements]
Como combinar: Adapters nas projeções permitem testar uma adaptação limitada.
Interface: Lista de módulos, posto e checkpoint base.
Condição: Pesos e nomes dos módulos correspondem ao modelo real.
Aceite proposto: Ablacionar módulos-alvo e validar retenção de capacidades.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S024, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não aceitar conversão só porque tensores têm dimensões compatíveis.
- Tratar explicações produzidas por visualização como hipóteses a serem testadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Atenção com várias cabeças não é uma medida de inteligência. Compare a solução especializada com fronteira em localização e uso de evidência, incluindo casos em que a informação é insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T100, T106, T090

## Fontes primárias associadas

### B-S024 — Attention Is All You Need

[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transformer e mecanismo multi-head como referência arquitetural.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T109 — Local / Window Attention

**Nome canônico:** Local / Window Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T095  
**Data da curadoria:** 2026-11-05

## T109:C01 — conceito

Família de padrões em que uma posição atende a uma região local. Neste inventário, a variante de janela contígua sobrepõe-se a Sliding Window Attention. Uma janela de encoder pode ser bidirecional, enquanto um decoder causal atende apenas a posições permitidas no passado.

Como funciona:
- Escolher vizinhança local e orientação causal ou bidirecional.
- Aplicar conectividade correspondente em cada camada.
- Combinar várias camadas ou conexões adicionais quando a tarefa exigir maior alcance.

Nota de nomenclatura: Sobreposição de nomenclatura preservada; a equivalência vale para a variante de janela local contígua.

## T109:C02 — aplicacao

Quando usar:
- Dados possuem estrutura local forte e modelo foi preparado para esse padrão.
- Análise de documentos ou sequências em arquiteturas com atenção local explícita.

Quando não usar:
- Chamar de local qualquer sistema que apenas recupere um subconjunto de documentos por RAG.

Implementação proposta:
- Anotar a definição exata de janela, incluindo se o tamanho conta passado, futuro e posição atual.
- Testar fronteiras e padding com sequências pequenas inspecionáveis.
- Documentar quais camadas mantêm conexões de alcance maior.

Aplicação LAI proposta:
Proposta LAI: manter esta entrada como alias explicativo da família local e consultar T095 para o caso comum de janela deslizante no decode.

## T109:C03 — riscos_validacao

Armadilhas:
- Janelas com mesmo número podem ter semânticas diferentes entre bibliotecas.
- Não existe garantia de que empilhar camadas recupere perfeitamente toda dependência distante.

Métricas sugeridas:
- Alcance efetivo necessário para as tarefas e densidade de conexões.
- Memória por camada e acerto conforme a distância de evidências.

Testes propostos:
- Construir matriz de máscara esperada para pequena sequência e comparar todos os pares permitidos.
- Mover a mesma evidência para fora da vizinhança e medir a resposta do sistema.

## T109:C04 — perguntas_proveniencia

Pergunta: Local é necessariamente causal?
Resposta: Não. Encoders podem ver vizinhos dos dois lados; decoders causais precisam impedir futuro.

Pergunta: É técnica independente de Sliding Window Attention?
Resposta: A janela contígua frequentemente é a mesma ideia; outros padrões locais precisam ser definidos explicitamente.

Pergunta: Largura W define a máscara completamente?
Resposta: Não. É preciso saber se inclui o centro, quantos tokens ficam em cada direção e quais fronteiras existem.

Pergunta: Pode reutilizar uma máscara em todo o lote?
Resposta: Somente quando posições, comprimentos e separação documental produzem a mesma conectividade ou broadcasting corretamente definido.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T109:C05 — mecanismo_avancado

Vizinhança local precisa declarar orientação, inclusão da própria posição e tratamento de limites. Uma janela bidirecional em encoder e uma janela causal em decoder podem ter a mesma largura nominal e conjuntos visíveis diferentes. Em sequências empacotadas, a proximidade física de tokens não permite cruzar fronteiras documentais. O padrão local também pode ser combinado com dilatação, alterando quais distâncias são acessíveis por camada.

Condição de contorno:
Usar máscara local em pesos treinados com outro padrão altera a função e pode reduzir qualidade mesmo quando o kernel é correto.

Contrato proposto:
- Entradas: Comprimentos, fronteiras de documentos, orientação da janela e alcance por camada.
- Saídas: Máscara ou metadados que representam exatamente a vizinhança permitida.
- Estado: Posições lógicas e identificação documental independente do offset físico.
- Invariante: Nenhuma conexão atravessa limites sem autorização explícita da arquitetura.

Compromissos de projeto:
- Vizinhanças curtas reduzem trabalho e aumentam a distância de propagação entre fatos.
- Empacotar exemplos economiza padding, mas exige isolamento rigoroso das máscaras.

## T109:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar dois documentos adjacentes e modificar somente o segundo. Em configuração causal ou isolada, esperar que a representação das posições não autorizadas do primeiro permaneça inalterada.

Plano de avaliação proposto:
Plano proposto: comparar implementação local com referência densa mascarada, incluindo bordas e comprimentos curtos. Depois medir tarefas com dependências em distâncias diferentes; separar correção do kernel de adequação do padrão à aplicação.

Comparações:
- T095 (complements): As fichas se sobrepõem na janela contígua; orientação e fronteiras precisam ser declaradas para comparar implementações.

Afirmação rastreável:
Longformer combina conexões locais com mecanismos globais para tarefas de documentos extensos.
Suporte: direct; fontes: B-S015
Limite: A fonte descreve uma arquitetura; suas propriedades não tornam qualquer janela local adequada a decoders.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T109:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu orientação e fronteiras da janela. A nova análise distingue dependência alcançável em várias camadas, retenção efetiva de estados e posicionamento da informação relevante no fluxo.

Alcance efetivo
Camadas locais sucessivas podem transmitir informação além da janela de uma camada, mas isso não equivale a acesso direto a cada token remoto. O efeito depende de profundidade, resíduos e treinamento. Teste relações que exigem copiar um detalhe antigo, combinar fatos e revisar uma conclusão: cada tarefa expõe uma limitação diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

Janela e estado físico
Uma máscara local economiza trabalho apenas se o kernel explora o padrão e o runtime limita estados quando a arquitetura permite. Guardar todo KV enquanto mascara posições antigas pode preservar facilidade de implementação, mas não entrega a mesma economia de memória. Em modelos híbridos, algumas camadas continuam exigindo histórico maior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

Organização do contexto
Mover fatos recentes para perto da pergunta pode ajudar uma arquitetura local, mas resumo não preserva todos os detalhes. Uma estratégia proposta mantém uma lista pequena de fatos verificáveis e recupera a origem quando necessário. A política de atualização deve detectar correções, não simplesmente acrescentar versões contraditórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

USO AVANÇADO — Assistente de eventos recentes
Cenário: O sistema acompanha uma operação com histórico extenso.
Estratégia: Use janela para o fluxo recente e um registro externo para decisões duráveis. Ao consultar um fato antigo, recupere a evidência e reinsira-a no contexto disponível.
Papel do modelo pequeno: Um 3–7B atua sobre eventos e consultas delimitadas, com memória externa auditável.
Aceite proposto: Testar eventos antigos relevantes e medir omissões após várias rotações da janela.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

USO AVANÇADO — Extração de documentos segmentados
Cenário: A tarefa encontra informações locais em documentos longos.
Estratégia: Segmente respeitando estrutura, sobreponha fronteiras e consolide resultados com identificadores de origem. Use uma etapa adicional para relações entre segmentos.
Papel do modelo pequeno: Um 8–14B resolve trechos; uma agregação explícita trata dependências distantes.
Aceite proposto: Cobertura deve incluir fatos nas bordas e relações que cruzam seções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Contextos locais e respostas curtas reduzem exigências, mas exigem mecanismo externo para fatos duráveis.
8–14B: Janelas por camada e tokens recuperados precisam entrar na avaliação de leitura longa.
15–30B: Um 15–30B não recupera automaticamente informação que sua máscara torna inacessível.
Requisitos de treino/runtime: Adotar janela diferente exige suporte arquitetural e validação; implementação do kernel não substitui treinamento.
Não aplicar quando: Não truncar contexto de um modelo denso e chamar o resultado de comportamento equivalente.

## T109:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T109:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T109 → T110 [complements]
Como combinar: Posições globais podem criar caminhos para informação que a janela não alcança diretamente.
Interface: Máscara global e identificadores de documentos.
Condição: Arquitetura treinada com a combinação.
Aceite proposto: Avaliar dependências remotas sem permitir leitura de tokens futuros.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V3B-S007, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T109 → T009 [complements]
Como combinar: Recuperação externa reinsere fatos relevantes numa janela limitada.
Interface: Trechos, proveniência e versão.
Condição: Recuperador encontra a evidência necessária.
Aceite proposto: Separar falhas de recuperação de falhas de interpretação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V3B-S007, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar comportamento no primeiro e último token de cada documento empacotado.
- Não tratar resumo como cópia semanticamente perfeita do histórico removido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie uma tarefa em que a evidência necessária é local ou recuperável. Uma vantagem de custo nesse cenário não demonstra equivalência em raciocínio sobre todo o histórico original.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T096, T110

## Fontes primárias associadas

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S007 — Mistral 7B — full text

[https://arxiv.org/html/2310.06825v1](https://arxiv.org/html/2310.06825v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campo receptivo em camadas, cache circular e chunking com janela.

Limite: Refere-se à arquitetura publicada; não prova qualidade para contexto arbitrário nem compatibilidade com checkpoint do usuário.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T110 — Global Token Attention

**Nome canônico:** Global Token Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T110  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção em tokens globais

## T110:C01 — conceito

Padrão em que algumas posições selecionadas têm conexões de alcance amplo, complementando atenção local. No Longformer, tokens definidos conforme a tarefa participam de atenção global. Isso difere de dar atenção plena a todos os pares e de declarar uma instrução prioritária no prompt.

Como funciona:
- Selecionar posições especiais que precisam reunir ou distribuir informação.
- Adicionar conexões globais à máscara local de acordo com a arquitetura.
- Manter limites causais quando o modelo for um decoder autorregressivo.

## T110:C02 — aplicacao

Quando usar:
- Arquitetura foi treinada com tokens globais para classificação, pergunta ou estrutura documental.
- Poucos pontos de agregação podem conectar segmentos distantes.

Quando não usar:
- Marcar arbitrariamente tokens como globais em um checkpoint sem implementação ou treino correspondente.

Implementação proposta:
- Definir regra de seleção dependente da tarefa e manter seu número limitado.
- Avaliar posições de perguntas, títulos ou marcadores com um conjunto separado.
- Inspecionar máscara para impedir que uma conexão global burle causalidade.

Aplicação LAI proposta:
Proposta LAI: estudar como escolha de arquitetura; não confundir com inserir palavras especiais que supostamente aumentariam a atenção do Qwen por instrução.

## T110:C03 — riscos_validacao

Armadilhas:
- Muitos tokens globais aproximam o custo da atenção densa.
- Um token global pode virar gargalo de representação e não preservar todos os detalhes.

Métricas sugeridas:
- Quantidade de tokens globais e custo adicional por sequência.
- Acerto em dependências entre segmentos e sensibilidade à seleção de posições.

Testes propostos:
- Comparar apenas atenção local com local mais posições globais em tarefa de evidência distante.
- No modo causal, perturbar futuro e verificar ausência de influência em saídas anteriores.

## T110:C04 — perguntas_proveniencia

Pergunta: Token global significa maior prioridade de instrução?
Resposta: Não. Descreve conexões de atenção da arquitetura, não autoridade de uma mensagem.

Pergunta: Todo modelo permite isso por máscara?
Resposta: Não. Há requisitos de arquitetura, implementação e treinamento.

Pergunta: Token global é uma instrução prioritária?
Resposta: Não. Global descreve conexões de atenção, enquanto prioridade de instruções depende de treinamento e comportamento do sistema.

Pergunta: Uma camada permite todos trocarem informação via global?
Resposta: As atualizações usam estados da camada anterior; reunir e redistribuir informação pode exigir etapas sucessivas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T110:C05 — mecanismo_avancado

Um token global pode reunir informação distante e distribuí-la em camadas seguintes, encurtando caminhos no grafo de atenção. Isso não torna automaticamente todos os pares diretamente conectados na mesma camada. Com n tokens, janela de alcance w e g posições globais, o número de conexões pode ser modelado por O(nw+ng), conforme a máscara. Se g cresce proporcionalmente a n, a economia pode desaparecer.

Condição de contorno:
A interpretação bidirecional típica de encoders não pode ser transplantada para geração causal permitindo acesso a informação futura.

Contrato proposto:
- Entradas: Posições globais selecionadas, máscara local, direção permitida e tensores do modelo.
- Saídas: Representações que combinam caminhos locais e globais autorizados.
- Estado: Identidade das posições globais e regra de seleção específica da tarefa.
- Invariante: A seleção global nunca elimina restrições causais ou documentais exigidas.

Compromissos de projeto:
- Mais posições globais ampliam conectividade e custo.
- Escolhas fixas simplificam execução, mas podem concentrar informação em poucos estados.

## T110:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: marcar como global uma posição futura num decoder e perturbar seu conteúdo. A implementação causal correta deve impedir influência sobre logits anteriores.

Plano de avaliação proposto:
Plano proposto: comparar diferentes seleções globais com custo e treinamento controlados. Medir qualidade por distância da evidência, memória e tempo; usar referência mascarada para verificar conectividade antes de atribuir ganhos ao mecanismo.

Comparações:
- T109 (complements): Conexões globais acrescentam rotas longas a uma base local.

Afirmação rastreável:
Longformer usa atenção global motivada pela tarefa junto da janela local.
Suporte: direct; fontes: B-S015
Limite: A relação de complexidade é uma modelagem da conectividade; não prevê tempo de kernel nem garante transmissão fiel de fatos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T110:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou caminhos e complexidade dos tokens globais. Esta camada examina seleção de posições, capacidade de agregação e avaliação de gargalos que permanecem mesmo com conectividade ampla.

Seleção orientada à tarefa
Escolher posições globais é uma decisão de representação: pergunta, delimitadores ou resumos podem ter papéis diferentes. Defina a regra antes da avaliação e teste mudanças na posição dos fatos. Escolher globais depois de conhecer a resposta produz uma vantagem artificial que não estará disponível durante uso real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

Gargalo de agregação
Poucos tokens globais precisam condensar muitas relações. Acesso ao documento inteiro não garante retenção de todos os detalhes: largura e treinamento limitam o que é transmitido. Aumentar posições globais pode reduzir esse gargalo, mas acrescenta computação e memória; procure um compromisso medido na tarefa concreta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

Direção e causalidade
Em geração autoregressiva, uma posição global também deve obedecer à disponibilidade temporal. Uma máscara bidirecional de encoder não pode ser transferida diretamente para decoder. Para streaming, especifique quando um resumo global é atualizado e se tokens posteriores dependem de sua versão antiga ou nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

USO AVANÇADO — Pergunta sobre documento longo
Cenário: Uma arquitetura compatível precisa relacionar seções distantes.
Estratégia: Designe a pergunta e marcadores estruturais como candidatos globais, mantendo a seleção independente da resposta. Compare com recuperação segmentada sob o mesmo orçamento.
Papel do modelo pequeno: Um 8–14B treinado para o padrão pode executar leitura especializada com menos conexões que atenção densa.
Aceite proposto: Testar resposta, localização da evidência e resistência a trechos irrelevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

USO AVANÇADO — Síntese de fluxo delimitado
Cenário: Eventos locais precisam alimentar um estado resumido.
Estratégia: Use posições de agregação apenas na arquitetura que permita atualizá-las corretamente; fora dela, implemente resumo externo explícito, sem apresentar essa alternativa como o mesmo mecanismo.
Papel do modelo pequeno: Um 3–7B pode manter sínteses de domínio estreito apoiadas em registros originais.
Aceite proposto: Medir quais fatos deixam de sobreviver quando aumenta o número de eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucos globais podem virar gargalo severo; comece com tarefas de baixa entropia e evidência curta.
8–14B: Explore seleção estrutural e número de globais separadamente, evitando trocar vários fatores ao mesmo tempo.
15–30B: Maior capacidade não elimina crescimento de custo quando a quantidade de globais acompanha o contexto.
Requisitos de treino/runtime: Exige modelo e máscara compatíveis; adicionar um token especial ao prompt de um LLM comum não cria atenção global arquitetural.
Não aplicar quando: Não prometer cobertura integral apenas porque existe um caminho no grafo de atenção.

## T110:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T110:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T110 → T109 [complements]
Como combinar: Conexões globais suplementam vizinhanças locais na arquitetura prevista.
Interface: Máscaras por camada e posições selecionadas.
Condição: Treinamento e inferência compartilham semântica.
Aceite proposto: Testar fronteiras, causalidade e relações distantes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T110 → T097 [complements]
Como combinar: Blocos podem representar o padrão misto e evitar materialização densa.
Interface: Metadados de blocos locais e globais.
Condição: Granularidade não introduz conexões proibidas.
Aceite proposto: Comparar máscara realizada com a máscara de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não selecionar tokens globais usando rótulos ou informação da resposta.
- Registrar crescimento do número de conexões quando aumentar a quantidade de globais.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve avaliar relações distantes e detalhes omitidos, não somente tamanho aceito de entrada. Conectividade e compreensão são propriedades distintas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T109, T096

## Fontes primárias associadas

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T111 — Dynamic Sparse Attention

**Nome canônico:** Dynamic Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T111  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa dinâmica

## T111:C01 — conceito

Família de atenção esparsa cuja seleção de posições depende do conteúdo ou do estado da execução. Em vez de uma máscara fixa, um roteador ou seletor decide quais interações calcular. Routing Transformer é uma referência específica, não a definição de todas as variantes.

Como funciona:
- Produzir sinais de seleção a partir de consultas, chaves ou representações compactas.
- Escolher grupos ou posições relevantes para cada consulta.
- Calcular atenção somente no conjunto selecionado e contabilizar custo de seleção.

## T111:C02 — aplicacao

Quando usar:
- Conteúdo relevante muda muito entre entradas longas.
- Há método validado cujo seletor é mais barato que a atenção evitada.

Quando não usar:
- Seletor precisa calcular todos os scores caros para descobrir quais scores deveria evitar.

Implementação proposta:
- Definir orçamento de posições e política para incluir conexões essenciais.
- Comparar com máscara fixa de igual custo para demonstrar valor do dinamismo.
- Avaliar seleção fora da distribuição de treino e o efeito de entradas adversas.

Aplicação LAI proposta:
Proposta LAI: tratar como pesquisa ou backend especializado; primeiro exigir ganho demonstrado sobre mecanismos estáticos mais simples.

## T111:C03 — riscos_validacao

Armadilhas:
- Erros de seleção retiram evidências antes de o modelo poder usá-las.
- Agrupamentos desequilibrados podem gerar picos de memória e trabalho.

Métricas sugeridas:
- Tempo do seletor, densidade e equilíbrio de grupos.
- Recall de posições úteis e qualidade final frente à atenção de referência.

Testes propostos:
- Inserir uma evidência rara mas decisiva e verificar se o seletor a preserva.
- Medir custo total em entradas repetitivas e aleatórias, incluindo o roteamento.

## T111:C04 — perguntas_proveniencia

Pergunta: É o mesmo que escolher documentos por RAG?
Resposta: Não. Opera nas conexões internas de atenção, embora ambos selecionem informação.

Pergunta: Exige sempre retreinar?
Resposta: Depende da variante; modelos com roteador aprendido e métodos de poda em inferência têm requisitos distintos.

Pergunta: Top-k após scores densos elimina O(n²)?
Resposta: Não o custo de produzir esses scores; é necessário examinar onde a seleção realmente acontece.

Pergunta: Mais confiança do roteador prova relevância?
Resposta: Não. Compare candidatos selecionados com evidência necessária e avalie falhas por mudança de domínio.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T111:C05 — mecanismo_avancado

O custo de selecionar conexões integra o orçamento da atenção. Um seletor que calcula todos os produtos QK antes de escolher top-k pode economizar armazenamento posterior sem eliminar o cálculo denso inicial. Roteamento por agrupamentos procura evitar essa etapa, mas enfrenta grupos desequilibrados e seleção instável: pequenas alterações de representação podem mover uma chave entre conjuntos e mudar abruptamente o contexto consultado.

Condição de contorno:
A seleção baseada em conteúdo pode perder uma evidência importante sem produzir erro de execução ou sinal explícito de baixa confiança.

Contrato proposto:
- Entradas: Representações para seleção, capacidade dos grupos e restrições causais.
- Saídas: Conjunto de conexões selecionadas e atenção normalizada nesse conjunto.
- Estado: Centroides ou índice, alocações de grupos e metadados de capacidade.
- Invariante: A seleção e a atenção usam posições compatíveis e não introduzem acesso futuro.

Compromissos de projeto:
- Seleção adaptativa pode encontrar dependências distantes e custa computação própria.
- Limitar capacidade controla memória e pode descartar candidatos relevantes.

## T111:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar um grupo muito popular e colocar evidência rara em sua fronteira. Perturbar levemente a consulta e verificar estabilidade, candidatos perdidos e comportamento ao exceder capacidade.

Plano de avaliação proposto:
Plano proposto: comparar padrão fixo, seleção dinâmica e referência densa com o mesmo orçamento declarado. Separar tempo de roteamento e atenção; medir cobertura da evidência, qualidade e distribuição de tamanhos de grupos.

Comparações:
- T097 (complements): Seleção dinâmica pode produzir blocos, mas o custo de construir seus metadados precisa ser contabilizado.

Afirmação rastreável:
Routing Transformer aprende padrões esparsos dependentes do conteúdo usando um módulo baseado em k-means online.
Suporte: direct; fontes: B-S025
Limite: Essa realização não define todas as técnicas de atenção dinâmica nem garante seleção ótima.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T111:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou custo de seleção e instabilidade dos grupos. Esta camada acrescenta distribuição do orçamento de conexões, sinais de omissão e avaliação separada do seletor e do operador de atenção.

Orçamento por consulta
Dar o mesmo número de conexões a cada consulta pode desperdiçar trabalho em regiões previsíveis e faltar em relações difíceis. Uma política adaptativa precisa estimar dificuldade sem calcular a atenção densa inteira. Defina um limite máximo e contabilize custo do estimador, roteamento, ordenação e padding, não apenas dos produtos finalmente selecionados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

Omissão versus cálculo
Uma resposta pode falhar porque a chave relevante não foi selecionada ou porque o modelo não usou corretamente uma chave acessível. Em um conjunto pequeno, compare conexões selecionadas com uma referência densa e meça cobertura da evidência anotada. Esse diagnóstico orienta aumentar orçamento, mudar seletor ou revisar treinamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

Robustez de distribuição
Agrupamentos aprendidos em textos comuns podem se comportar diferente em código, números ou documentos multilíngues. Teste desequilíbrio, grupos vazios e concentração adversarial de tokens. Uma política de capacidade deve declarar se descarta, reroteia ou amplia processamento quando um grupo excede o limite; essas escolhas alteram custo e semântica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

USO AVANÇADO — Leitura longa especializada
Cenário: O domínio possui dependências recorrentes que podem ser aprendidas.
Estratégia: Treine ou adapte um seletor compatível, mantenha uma amostra densa de controle e compare qualidade por tipo de relação. Use fallback quando sinais operacionais mostram saturação.
Papel do modelo pequeno: Um 8–14B pode explorar sparsity treinada em tarefas bem delimitadas.
Aceite proposto: O seletor deve manter cobertura de evidência enquanto reduz trabalho total medido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

USO AVANÇADO — Investigação de latência irregular
Cenário: Poucos pedidos geram picos apesar de tamanho semelhante.
Estratégia: Correlacione distribuição de grupos, quantidade de conexões e temporários. Separe desbalanceamento do seletor de problemas do kernel ou da fila.
Papel do modelo pequeno: Um 15–30B exige orçamento por dispositivo, inclusive para grupos excepcionais.
Aceite proposto: Reproduzir os picos com entradas controladas e confirmar a causa antes de alterar a máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma implementação dinâmica pode custar mais que atenção densa otimizada em sequências pequenas.
8–14B: O benefício depende de contexto longo e seletor barato, não somente do porte do modelo.
15–30B: Considere memória de índices e buffers, além da matriz de atenção evitada.
Requisitos de treino/runtime: Seleção arquitetural geralmente exige treinamento; substituir arbitrariamente a atenção de um checkpoint é aproximação a validar.
Não aplicar quando: Não apresentar redução de conexões como aceleração se o seletor ou padding dominam o tempo.

## T111:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T111:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T111 → T097 [feeds]
Como combinar: Conexões selecionadas são convertidas em blocos processáveis.
Interface: Índices, ocupação e máscaras de borda.
Condição: A conversão não amplia indevidamente o campo visível.
Aceite proposto: Comparar lista lógica e máscara realmente executada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S025, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T111 → T107 [complements]
Como combinar: Profiling mede seleção, movimentação e computação conjuntamente.
Interface: Tempo por fase e bytes transportados.
Condição: Mesmo conjunto de consultas e contexto.
Aceite proposto: Confirmar redução no caminho crítico, não apenas em FLOPs estimados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S025, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Incluir casos raros em que uma única chave distante determina a resposta.
- Registrar descartes por capacidade como intervenção semântica, não detalhe invisível.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare com fronteira em documentos com evidência marcada e dependências variadas. Sparsity pode economizar execução e simultaneamente perder relações; a avaliação deve tornar essa troca visível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T096, T097, T112

## Fontes primárias associadas

### B-S025 — Efficient Content-Based Sparse Attention with Routing Transformers

[https://arxiv.org/abs/2003.05997](https://arxiv.org/abs/2003.05997)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento esparso dependente do conteúdo com agrupamento online.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T112 — Retrieval-Based Attention

**Nome canônico:** Retrieval-Based Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T112  
**Data da curadoria:** 2026-11-05

## T112:C01 — conceito

Termo amplo para mecanismos em que recuperação seleciona representações consultadas pela atenção. Pode designar memória interna recuperável ou arquiteturas como RETRO, que usam trechos externos com cross-attention. É necessário identificar a variante; anexar documentos ao prompt por RAG não equivale a modificar a atenção.

Como funciona:
- Construir consulta e recuperar candidatos de um índice de representações.
- Codificar ou preparar os candidatos para o mecanismo de atenção.
- Combinar a informação recuperada com os estados do modelo no ponto previsto pela arquitetura.

Nota de nomenclatura: RETRO é exemplo documentado. O registro não identifica toda a família com uma implementação específica.

## T112:C02 — aplicacao

Quando usar:
- Modelo e runtime foram projetados para integrar recuperação internamente.
- Pesquisa compara memória recuperável com ampliar parâmetros ou contexto.

Quando não usar:
- Presumir que qualquer checkpoint aceita cross-attention adicional sem treino e novos pesos.

Implementação proposta:
- Especificar se a memória é externa, KV interno ou blocos codificados.
- Versionar retriever, corpus e modelo conjuntamente para reproduzir resultados.
- Comparar com RAG textual convencional antes de adotar integração mais profunda.

Aplicação LAI proposta:
Proposta LAI: começar pelo RAG externo deste pacote; tratar atenção baseada em recuperação como opção arquitetural que exige integração e avaliação próprias.

## T112:C03 — riscos_validacao

Armadilhas:
- Erro do retriever pode excluir informações necessárias antes da geração.
- Atualizar o índice pode mudar a distribuição dos conteúdos vistos pela arquitetura treinada.

Métricas sugeridas:
- Recall dos candidatos e latência de recuperação.
- Qualidade final, custo de atenção adicional e sensibilidade a corpus desatualizado.

Testes propostos:
- Retirar a evidência correta do índice e verificar comportamento de abstinência ou degradação explícita.
- Trocar o corpus mantendo modelo fixo e medir impacto em tarefas previamente corretas.

## T112:C04 — perguntas_proveniencia

Pergunta: RETRO é igual a colocar texto recuperado no prompt?
Resposta: Não. Sua arquitetura inclui recuperação, codificação e cross-attention por trechos.

Pergunta: O nome descreve um único algoritmo?
Resposta: Não. É uma família; cada implementação deve informar o que recupera e onde usa a informação.

Pergunta: Mudar o banco atualiza os pesos?
Resposta: Não. Atualiza memória externa; o modelo ainda depende de suas capacidades treinadas de utilizar o material recuperado.

Pergunta: Boa recuperação garante resposta correta?
Resposta: Não. O conteúdo pode ser mal interpretado, e o índice também pode conter evidência conflitante ou desatualizada.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T112:C05 — mecanismo_avancado

Recuperar conteúdo para uma camada de atenção requer compatibilidade entre índice, codificador e mecanismo que consome seus estados. Atualizar somente os documentos pode mudar distribuição e latência; atualizar embeddings sem reconstruir o índice pode quebrar a correspondência geométrica. No RETRO, recuperação externa participa de uma arquitetura com codificação e cross-attention por trechos, portanto não equivale a anexar texto a um modelo convencional.

Condição de contorno:
A recuperação pode falhar mesmo quando a cross-attention é correta; o modelo não consegue atender a candidatos que o índice deixou de fornecer.

Contrato proposto:
- Entradas: Consulta de recuperação, índice versionado, candidatos e codificador compatível.
- Saídas: Representações externas e sua integração nos pontos previstos da arquitetura.
- Estado: Versões de corpus, embeddings, índice e política de atualização.
- Invariante: Cada candidato mantém proveniência e correspondência com a versão usada para codificá-lo.

Compromissos de projeto:
- Memória externa amplia conteúdo acessível e adiciona consulta, codificação e transporte.
- Mais candidatos aumentam cobertura e custo, podendo introduzir material irrelevante.

## T112:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o codificador das consultas mantendo o índice antigo e inserir documentos duplicados. Esperar detecção de incompatibilidade e avaliação explícita da perda de cobertura.

Plano de avaliação proposto:
Plano proposto: separar qualidade de recuperação da utilização pelo modelo. Controlar corpus e versões; medir recall de evidência, latência por etapa e qualidade final com candidatos corretos e incorretos; aprovar pelo benefício total com proveniência preservada.

Comparações:
- T111 (distinct_from): Selecionar estados internos e recuperar trechos externos têm diferentes identidades, custos e atualizações.

Afirmação rastreável:
RETRO combina recuperador congelado, codificador diferenciável e cross-attention por trechos.
Suporte: direct; fontes: B-S026
Limite: O artigo apresenta uma arquitetura treinada para essa integração, não uma função universal disponível em qualquer checkpoint.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T112:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu compatibilidade de índice e cross-attention. O aprofundamento separa atualizações de conhecimento, atualizações da arquitetura e requisitos de avaliação que detectam dependência indevida do banco recuperado.

Conhecimento versionado
Mudar o banco externo pode modificar respostas sem mudar pesos. Registre a versão do índice junto à versão do modelo e preserve snapshots para reproduzir erros. Uma retirada de documento precisa impedir sua recuperação futura; a presença de informação semelhante nos pesos é outro problema, não resolvido pela remoção do índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

Contaminação de avaliação
Recuperação sobre corpus que contém respostas de teste pode inflar resultados sem demonstrar generalização. Deduplicate exemplos e vizinhos próximos por origem, não só por igualdade literal. Registre quais trechos foram recuperados e diferencie conhecimento disponível legitimamente de vazamento do conjunto usado para medir capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

Alternativa externa
Antes de treinar atenção com recuperação, compare um RAG textual no checkpoint existente. A arquitetura integrada pode oferecer vantagens específicas, mas exige acoplamento de codificador, treino e runtime. A decisão deve considerar atualização do acervo, custo de manutenção e possibilidade de inspecionar evidências, além da métrica principal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

USO AVANÇADO — Acervo técnico mutável
Cenário: Manuais mudam com frequência e o modelo precisa consultar detalhes.
Estratégia: Construa primeiro uma referência com recuperação textual, meça falhas e só investigue integração arquitetural quando houver hipótese clara sobre a limitação encontrada.
Papel do modelo pequeno: Um 3–7B pode executar o baseline de domínio; não se presume que suporte RETRO.
Aceite proposto: Comparar atualização de fatos, latência de busca e qualidade em versões históricas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

USO AVANÇADO — Pesquisa de modelo especializado
Cenário: Há orçamento para treinar uma arquitetura que consome vizinhos.
Estratégia: Controle corpus, codificador e frequência de recuperação. Faça ablação sem vizinhos, com vizinhos relevantes e com vizinhos errados para medir dependência.
Papel do modelo pequeno: Um 8–14B pode ser objeto de pesquisa controlada; porte isolado não define custo do treinamento.
Aceite proposto: A melhora deve sobreviver à remoção de duplicatas e a mudanças de distribuição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: RAG textual costuma ser uma hipótese inicial operacional mais simples; medir antes de redesenhar o modelo.
8–14B: Arquiteturas de recuperação podem ser estudadas com treino específico e corpus governado.
15–30B: O custo do codificador e de buscas repetidas pode dominar mesmo quando o gerador é maior.
Requisitos de treino/runtime: RETRO exige pesos e runtime específicos; Qwen ou outro decoder convencional não recebe essa arquitetura por configuração.
Não aplicar quando: Não apresentar cross-attention de recuperação como funcionalidade genérica de qualquer endpoint.

## T112:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C025 — Google DeepMind / RETRO
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: O trabalho avalia um modelo treinado para consumir trechos recuperados por uma arquitetura específica de atenção.
Mecanismo documentado: Codificação de vizinhos recuperados e cross-attention por trechos fazem parte da função treinada.
Correspondência com esta base: Recuperação participa da arquitetura de atenção.
Transferência proposta para modelo pequeno: Proposta: estudar custo e benefício de arquitetura treinada versus RAG externo antes de escolher uma intervenção em 3–30B.
Limite: Pesquisa não comprova produto implantado. Alterar um checkpoint convencional para reproduzir RETRO requer treinamento e compatibilidade; não é uma opção intercambiável de serving.
Fontes: B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T112:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T112 → T009 [alternative]
Como combinar: Comparar recuperação textual e integração arquitetural sob o mesmo corpus.
Interface: Consultas, evidências e versões do índice.
Condição: Protocolos de teste evitam vazamento e igualam acesso a conhecimento.
Aceite proposto: Medir resposta correta com evidência e custo de atualizar o acervo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S026, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T112 → T177 [requires]
Como combinar: Arquitetura integrada precisa aprender a consumir os estados externos.
Interface: Pesos do codificador, módulos de atenção e dados de treino.
Condição: Objetivo e entrada refletem uso posterior.
Aceite proposto: Ablacionar recuperação e verificar comportamento com ausência de vizinhos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S026, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir acesso ao documento correto com uso correto da informação.
- Manter logs de proveniência sem expor conteúdo protegido a usuários não autorizados.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação deve igualar acesso ao acervo e considerar atualizações. Um modelo especializado pode vencer numa coleção específica sem possuir conhecimento ou capacidade geral equivalentes aos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T067, T096, T111

## Fontes primárias associadas

### B-S026 — Improving language models by retrieving from trillions of tokens

[https://arxiv.org/abs/2112.04426](https://arxiv.org/abs/2112.04426)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RETRO combina recuperação, codificador e cross-attention por trechos.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T113 — FlashAttention Tiling

**Nome canônico:** FlashAttention Tiling  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T113  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** blocagem de FlashAttention

## T113:C01 — conceito

Decomposição em blocos usada dentro de implementações de FlashAttention para manter dados próximos do processamento e evitar a matriz completa em memória global. É um componente do algoritmo, não outra capacidade independente de recuperação ou compressão de conhecimento.

Como funciona:
- Escolher blocos de consultas e de chaves/valores que se ajustem aos recursos do kernel.
- Atualizar acumuladores e normalização enquanto percorre blocos.
- Gravar resultados consolidados em vez de intermediários completos de todos os pares.

## T113:C02 — aplicacao

Quando usar:
- Desenvolvimento ou análise de kernels de atenção.
- Diagnóstico de ocupação, tráfego de memória e limite de registradores.

Quando não usar:
- Alterar tamanho de bloco sem considerar dimensão de cabeça, dtype, máscara e recursos da GPU.

Implementação proposta:
- Usar implementação de referência e testes numéricos antes de autotuning.
- Varrer poucos tiles candidatos em formas representativas e separar custo de compilação.
- Registrar registradores, memória compartilhada e eventuais spills no profiler.

Aplicação LAI proposta:
Proposta LAI: manter como conhecimento para auditoria de performance; preferir kernels mantidos pelo runtime a patches locais sem necessidade comprovada.

## T113:C03 — riscos_validacao

Armadilhas:
- Tile grande pode exceder recursos e reduzir ocupação ou causar spills.
- Tile pequeno pode aumentar leitura redundante e número de iterações.

Métricas sugeridas:
- Bytes globais movimentados, ocupação e tempo de execução.
- Memória compartilhada, registradores por thread e erro numérico.

Testes propostos:
- Testar comprimentos que não são múltiplos do bloco e validar a máscara de fronteira.
- Comparar todas as configurações de tile com uma referência para evitar aceitar um ganho incorreto.

## T113:C04 — perguntas_proveniencia

Pergunta: Tiling é chunking de documento?
Resposta: Não. Divide operações numéricas dentro do kernel; o conteúdo lógico do prompt permanece igual.

Pergunta: Posso somar o ganho ao de FlashAttention?
Resposta: Não automaticamente. Tiling é parte do mecanismo que já produz aquele ganho.

Pergunta: Tiling torna a atenção esparsa?
Resposta: Não por si só. Todos os blocos permitidos ainda podem ser visitados; sparsity exige excluir conexões.

Pergunta: Por que testar strides não contíguos?
Resposta: Um kernel que pressupõe layout incorreto pode ler endereços errados mesmo com shapes aparentemente compatíveis.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T113:C05 — mecanismo_avancado

Os tiles de consulta e de chave podem ter tamanhos diferentes porque seus papéis no reúso são distintos. O acumulador de saída e estatísticas de normalização precisam sobreviver ao percurso dos blocos KV. Nas bordas, posições físicas extras devem ser mascaradas sem afetar máximos e somas. A disposição dos dados também influencia coalescência e pressão de registradores, além do simples número de operações.

Condição de contorno:
Um tile que cabe nominalmente em memória compartilhada pode executar mal por registradores, sincronização ou baixa ocupação.

Contrato proposto:
- Entradas: Formas QKV, strides, máscara e dimensões dos tiles.
- Saídas: Blocos de saída consolidados e estatísticas necessárias ao backward quando aplicável.
- Estado: Acumuladores persistentes no kernel e buffers temporários com limites válidos.
- Invariante: Padding de tile nunca entra no normalizador nem contribui para a saída.

Compromissos de projeto:
- Tiles maiores aumentam reúso e podem reduzir paralelismo residente.
- Layouts especializados melhoram acesso e podem exigir conversões antes da atenção.

## T113:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar sequências com comprimento um acima e um abaixo do múltiplo do tile, preenchendo padding com valores extremos. Esperar saída independente desses valores inválidos.

Plano de avaliação proposto:
Plano proposto: comparar configurações com entradas, precisão e máscara fixas. Medir duração incluindo conversão de layout, memória temporária e correção nas bordas; selecionar por famílias de formas, evitando assumir um tile ótimo para todo serviço.

Comparações:
- T114 (complements): A normalização incremental permite combinar contribuições dos tiles sem armazenar todos os scores.

Afirmação rastreável:
O tutorial oficial de atenção fundida do Triton percorre blocos KV enquanto atualiza acumuladores de saída e normalização.
Suporte: direct; fontes: B-S027
Limite: O exemplo é uma implementação didática otimizada; configurações adequadas dependem de dispositivo e versão.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T113:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou tiles e acumuladores. Esta camada liga a escolha de tile ao regime de execução, aos limites de compilação e à validação de formas que não aparecem nos casos ideais.

Tile dependente da fase
Prefill oferece muitas consultas; decode frequentemente possui poucas consultas e KV crescente. Um tamanho favorável ao primeiro pode deixar pouca ocupação no segundo. Selecione variantes por forma e dtype, considerando cabeças agrupadas e comprimentos reais, em vez de fixar uma configuração por número de parâmetros do modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

Reúso versus recursos locais
Aumentar tile pode reduzir leituras repetidas e elevar uso de registradores ou memória compartilhada. Esse consumo pode reduzir blocos residentes e causar spills. O resultado é uma curva de compromisso; a melhor configuração não se deduz somente de quantos bytes deixam de ir para a memória global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

Compilação e variedade
Formas variáveis podem produzir múltiplas especializações e custo de compilação. Defina classes de comprimento e um caminho correto para casos raros. O aquecimento precisa cobrir classes relevantes; uma medida que exclui todo custo de compilação não descreve pedidos ocasionais nem atualização frequente do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Serviço com duas fases dominantes
Cenário: Documentos longos geram respostas curtas.
Estratégia: Escolha variantes para prefill e decode separadamente e acompanhe transição entre elas. Evite otimizar decode quase inexistente enquanto prefill ocupa a maior parte do pedido.
Papel do modelo pequeno: Um 8–14B pode oferecer leitura especializada com uma política de kernels adequada às formas.
Aceite proposto: Reduzir tempo da fase dominante mantendo logits dentro da tolerância definida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Auditoria de kernel customizado
Cenário: Uma implementação promete economia superior ao backend padrão.
Estratégia: Teste comprimentos não múltiplos, masks, strides e grupos KV. Compare com referência simples e depois avalie carga representativa.
Papel do modelo pequeno: Um 3–7B facilita exploração, mas os testes devem incluir dimensões reais do checkpoint alvo.
Aceite proposto: Nenhum ganho é aceito antes de passar bordas e equivalência numérica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Overhead de lançamento e compilação pode superar economia em sequências curtas.
8–14B: Varie contexto e lote para encontrar pontos de transição entre variantes.
15–30B: Considere competição por recursos locais com comunicação e outros kernels, quando presentes.
Requisitos de treino/runtime: Otimização de runtime, sem treino se a operação for preservada. Backend e GPU precisam suportar a variante.
Não aplicar quando: Não tratar tiling como sparse attention: todos os pares permitidos podem continuar sendo calculados.

## T113:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020, V4B-Q005.

## T113:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T113 → T114 [requires]
Como combinar: Estatísticas de softmax permitem combinar tiles sem materializar a matriz inteira.
Interface: Máximos, somas e numeradores parciais.
Condição: Mesma máscara e escala em todas as parcelas.
Aceite proposto: Comparar combinação em ordens diferentes sob tolerância numérica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S027, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T113 → T107 [complements]
Como combinar: Profiling verifica se maior tile reduz tráfego sem criar spills ou baixa ocupação.
Interface: Contadores e tempo por forma.
Condição: Medições do mesmo kernel e dispositivo.
Aceite proposto: Demonstrar efeito no tempo do pedido, além do microbenchmark.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S027, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar linhas totalmente mascaradas conforme a semântica declarada do backend.
- Fixar versão do compilador e registrar seleção efetiva de kernel.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Tiling não muda a capacidade cognitiva do modelo. Na comparação com fronteira, seu efeito aparece no custo e na latência de uma tarefa cuja qualidade já foi medida separadamente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T114, T097

## Fontes primárias associadas

### B-S027 — Fused Attention

[https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html](https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de referência de atenção em blocos com kernel fundido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S006 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning — full text

[https://arxiv.org/html/2307.08691v1](https://arxiv.org/html/2307.08691v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento entre blocos e warps, custo de operações não matriciais.

Limite: Texto técnico consultado; velocidade depende de formas, dtype e arquitetura do dispositivo.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T114 — Online Softmax

**Nome canônico:** Online Softmax  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T114  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** softmax incremental; normalização online

## T114:C01 — conceito

Cálculo incremental e numericamente estável do normalizador de softmax, útil quando scores chegam em blocos. Mantém máximo e soma reescalada em vez de exigir todas as posições simultaneamente. É uma peça algorítmica usada por implementações eficientes, não uma aproximação obrigatória da distribuição.

Como funciona:
- Guardar máximo corrente m e soma l dos exponenciais reescalados.
- Ao receber novo bloco, atualizar m e reescalar a soma anterior para o novo máximo.
- Acrescentar contribuições do bloco e normalizar os acumuladores ao final.

## T114:C02 — aplicacao

Quando usar:
- Atenção fundida calcula scores por partes.
- Uma operação precisa reduzir passes ou armazenamento de intermediários.

Quando não usar:
- Somar exponenciais brutos sem controle de escala e chamar isso de implementação estável.

Implementação proposta:
- Especificar dtype dos acumuladores e política para posições mascaradas.
- Construir referência em maior precisão com valores extremos.
- Se também acumular valores da atenção, aplicar o mesmo reescalonamento ao numerador.

Aplicação LAI proposta:
Proposta LAI: usar para compreender por que kernels eficientes preservam atenção com menos memória; não é função que a aplicação precisa reimplementar.

## T114:C03 — riscos_validacao

Armadilhas:
- Combinar blocos com máximos diferentes sem reescalar produz resultado errado.
- Linha totalmente mascarada exige tratamento explícito para evitar NaN.

Métricas sugeridas:
- Erro absoluto e relativo contra referência e ocorrência de NaN.
- Número de leituras/escritas e tempo da operação fundida.

Testes propostos:
- Testar scores muito grandes, muito pequenos, repetidos e blocos vazios/mascarados.
- Mudar tamanho e ordem de agrupamento de blocos e verificar consistência dentro da tolerância numérica.

## T114:C04 — perguntas_proveniencia

Pergunta: Online Softmax elimina a normalização?
Resposta: Não. Computa o normalizador de maneira incremental com reescalonamento.

Pergunta: A saída é bit a bit igual?
Resposta: Não é garantia geral em ponto flutuante; o algoritmo é matematicamente equivalente sob suas condições.

Pergunta: Pode normalizar cada tile e somar?
Resposta: Somente se conservar e aplicar as massas relativas corretas; somar distribuições locais sem pesos produz outra distribuição.

Pergunta: Por que guardar o máximo?
Resposta: Subtrair uma referência evita exponenciais excessivas e permite reescalar blocos quando surge um score maior.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T114:C05 — mecanismo_avancado

Para blocos A e B, mantenha máximo m e soma l de exp(score−m). A combinação usa m=max(mA,mB) e l=exp(mA−m)·lA+exp(mB−m)·lB. O numerador ponderado pelos valores exige a mesma reescala antes da soma. Combinar médias locais diretamente é incorreto: blocos com massas de probabilidade diferentes não devem receber pesos iguais.

Condição de contorno:
Linhas totalmente mascaradas precisam de regra explícita, pois operações com máximos negativos infinitos podem gerar formas indefinidas.

Contrato proposto:
- Entradas: Scores em blocos, máscara e valores quando houver atenção ponderada.
- Saídas: Normalizador estável e resultado equivalente à redução global especificada.
- Estado: Máximo, soma reescalada e numerador parcial por linha.
- Invariante: Todas as parcelas são expressas na mesma referência exponencial antes de serem combinadas.

Compromissos de projeto:
- Acumulação em maior precisão reduz erro e ocupa mais recursos.
- Ordem de blocos preserva álgebra real, mas pode alterar arredondamento finito.

## T114:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: combinar blocos com máximos muito diferentes e substituir a reescala por média de saídas locais. A versão defeituosa deve divergir da referência; testar também linha vazia.

Plano de avaliação proposto:
Plano proposto: usar referência de alta precisão, permutar ordens e variar amplitudes dos scores. Medir erro absoluto/relativo e presença de valores não finitos; definir tolerância segundo dtype e uso, sem exigir igualdade bit a bit entre reduções distintas.

Comparações:
- T101 (complements): Estados de normalização podem combinar contribuições recebidas de diferentes partições do contexto.

Afirmação rastreável:
O cálculo online do normalizador busca computar o softmax clássico com menos acessos à memória.
Suporte: direct; fontes: B-S028
Limite: A estabilidade numérica não torna arbitrariamente pequena a perda de precisão de qualquer dtype.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T114:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 deu a regra de combinação estável. O aprofundamento trata identidade de redução, máscaras extremas, precisão acumulada e uso dessa operação em paralelismo.

Identidade e linhas vazias
A implementação precisa representar um bloco sem chaves válidas sem produzir operações indefinidas entre infinitos. Defina explicitamente estado vazio, transição para a primeira contribuição válida e comportamento de linha inteiramente mascarada. Retornar zero, erro ou outro valor deve seguir o contrato da operação, não surgir por acidente numérico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

Ordem de redução
A combinação é matematicamente associativa sob aritmética exata, mas arredondamentos tornam ordens diferentes numericamente distintas. Particionamento, tile e topologia podem mudar a ordem sem mudar a fórmula. Compare tolerâncias por dtype e comprimento; exigir igualdade bit a bit pode rejeitar uma implementação correta ou ocultar tolerâncias mal escolhidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

Normalizador e diagnóstico
Log-sum-exp e estatísticas parciais ajudam a investigar saturação e divergências, mas não são confiança factual da resposta. Um token pode receber probabilidade alta dentro de uma distribuição equivocada. Mantenha métricas numéricas separadas de métricas de qualidade do modelo e da decisão de encaminhar uma tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

USO AVANÇADO — Redução distribuída de atenção
Cenário: Blocos de KV residem em partições diferentes.
Estratégia: Combine máximos, massas e numeradores na mesma referência exponencial. Preserve posições e máscaras globais, incluindo partições sem contribuição válida.
Papel do modelo pequeno: Um modelo 15–30B com contexto longo pode usar o mecanismo se a comunicação compensar.
Aceite proposto: Comparar com referência não particionada e testar partições vazias ou desbalanceadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

USO AVANÇADO — Diagnóstico de NaNs
Cenário: Uma otimização falha apenas em entradas extremas.
Estratégia: Construa scores controlados com grande amplitude, mascaramento e comprimentos variados. Localize se a falha nasce na projeção, na exponencial ou na combinação.
Papel do modelo pequeno: Modelos pequenos permitem reproduzir o defeito com tensores sintéticos sem expor dados privados.
Aceite proposto: Eliminar não finitos sem alterar silenciosamente escala ou máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Útil como operação interna de kernels; não precisa ser exposto como configuração de produto.
8–14B: A extensão do contexto e dtype determinam sensibilidade, não apenas os parâmetros totais.
15–30B: Reduções distribuídas exigem verificar comunicação e precisão acumulada conjuntamente.
Requisitos de treino/runtime: Runtime/kernel; pode participar de treinamento e inferência. Precisão dos acumuladores deve ser explicitada.
Não aplicar quando: Não combinar médias locais com pesos iguais nem tratar softmax como verificador de verdade.

## T114:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020, V4B-Q005.

## T114:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T114 → T101 [feeds]
Como combinar: A redução de estados parciais permite agregar atenção distribuída.
Interface: Tripla de estatísticas e identidade da consulta.
Condição: Todos os blocos representam a mesma consulta e escala.
Aceite proposto: Comparar diferentes ordens de comunicação com referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S028, B-S027, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T114 → T113 [complements]
Como combinar: Tiles usam a redução para manter saída e normalização incrementalmente.
Interface: Estado parcial por linha.
Condição: Padding excluído antes das estatísticas.
Aceite proposto: Testar bordas, máscaras e sequências com comprimentos díspares.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S028, B-S027, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar overflow nos scores de erro na redução; a estabilização não corrige tudo que ocorreu antes.
- Evitar clamps silenciosos que mudam probabilidades sem registro.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Essa técnica protege execução numérica e memória, sem acrescentar conhecimento. Um serviço pequeno deve demonstrar qualidade por testes externos, mesmo que seu softmax seja perfeitamente estável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T113

## Fontes primárias associadas

### B-S028 — Online normalizer calculation for softmax

[https://arxiv.org/abs/1805.02867](https://arxiv.org/abs/1805.02867)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cálculo online do normalizador de softmax com menos acessos à memória.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S027 — Fused Attention

[https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html](https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de referência de atenção em blocos com kernel fundido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T115 — Activation Checkpointing

**Nome canônico:** Activation Checkpointing  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T115  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gradient checkpointing; checkpointing de ativações

## T115:C01 — conceito

Técnica principalmente de treinamento que troca cálculo adicional por menor memória de ativações. Guarda alguns pontos do forward e recomputa intermediários durante o backward. Não é checkpoint de uma missão do agente nem persistência de KV para retomar uma conversa.

Como funciona:
- Escolher segmentos da rede cujas ativações não serão todas preservadas.
- Guardar entradas e informações necessárias para reconstrução.
- Reexecutar o segmento quando o cálculo de gradientes precisar dos intermediários.

Nota de nomenclatura: Classificação original em inferência foi preservada por ID; aplicação principal explicada como treinamento.

## T115:C02 — aplicacao

Quando usar:
- Fine-tuning ou treinamento é limitado por memória de ativações.
- Cálculo extra é aceitável para aumentar sequência ou batch útil.

Quando não usar:
- Esperar aceleração da inferência comum sem backward apenas ativando gradient checkpointing.

Implementação proposta:
- Medir pesos, estados do otimizador, gradientes e ativações separadamente.
- Escolher segmentos custosos em memória e toleráveis em recomputação.
- Verificar preservação de aleatoriedade, efeitos colaterais e compatibilidade com o treinamento adotado.

Aplicação LAI proposta:
Proposta LAI: considerar em experimentos de LoRA/QLoRA quando ativações forem o gargalo; não registrar como melhoria comprovada do servidor de inferência.

## T115:C03 — riscos_validacao

Armadilhas:
- Funções com efeitos colaterais podem se comportar diferentemente quando reexecutadas.
- Economizar ativações não resolve automaticamente memória de otimizador ou pesos.

Métricas sugeridas:
- Memória máxima por passo de treino e duração do passo.
- Tokens de treino úteis por segundo e diferença de gradientes frente à referência.

Testes propostos:
- Em um modelo pequeno, comparar perdas e gradientes com e sem checkpointing sob controle de aleatoriedade.
- Executar treino até completar passos representativos sem OOM e medir custo extra.

## T115:C04 — perguntas_proveniencia

Pergunta: É o mesmo que salvar state.json?
Resposta: Não. Um é técnica numérica de treino; o outro é persistência operacional do agente.

Pergunta: Checkpointing acelera o treino?
Resposta: Geralmente adiciona recomputação; pode viabilizar uma configuração maior, mas o resultado deve ser medido.

Pergunta: Checkpointing reduz diretamente a latência de geração?
Resposta: Não é esse seu objetivo; atua no armazenamento de ativações durante treinamento com retropropagação.

Pergunta: Igualdade de loss em uma etapa basta?
Resposta: Não. Gradientes podem divergir apesar de uma saída forward semelhante; compare também o caminho de atualização dos parâmetros.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T115:C05 — mecanismo_avancado

Reexecutar um segmento no backward pressupõe que ele represente a mesma função do forward original. Aleatoriedade, buffers mutáveis e efeitos colaterais podem violar essa hipótese: avançar um contador ou consumir outra máscara de dropout altera a recomputação. O mecanismo precisa administrar estados aleatórios suportados e distinguir variantes de autograd; economizar ativações não é equivalente a comprimir pesos ou cache de inferência.

Condição de contorno:
Funções com dependência de estado externo ou transferência para dispositivos não contemplados podem produzir gradientes diferentes silenciosamente.

Contrato proposto:
- Entradas: Segmento diferenciável, entradas, política de preservação aleatória e variante de checkpoint.
- Saídas: Saída forward e gradientes consistentes com o cálculo sem checkpoint.
- Estado: Entradas preservadas, estado RNG necessário e metadados do autograd.
- Invariante: A recomputação mantém a função e os efeitos numéricos exigidos pelo treinamento.

Compromissos de projeto:
- Menos ativações residentes exige mais computação no backward.
- Preservar RNG custa trabalho, mas evita diferenças causadas por amostragem repetida.

## T115:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir dropout e um contador mutável no segmento. Comparar gradientes com execução sem checkpoint; o efeito colateral deve ser removido ou explicitamente controlado antes da aprovação.

Plano de avaliação proposto:
Plano proposto: controlar lote, seed, pesos e dtype, medindo pico de memória, duração da etapa e erro de gradientes. Avaliar vários segmentos; aceitar economia somente quando a trajetória de treinamento respeita o requisito de equivalência definido.

Comparações:
- T116 (distinct_from): Recomposição de KV ocorre na inferência; activation checkpointing economiza intermediários exigidos pelo backward.

Afirmação rastreável:
A documentação PyTorch descreve preservação de RNG e limitações quando dispositivos ou aleatoriedade não estão cobertos.
Suporte: direct; fontes: B-S029
Limite: O mecanismo não torna qualquer função com efeitos colaterais segura para recomputação.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T115:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou equivalência da recomputação. Esta camada introduz seleção de ativações pelo custo, interação com adapters e avaliação do verdadeiro limitante de memória no treinamento.

Memória que permanece
Checkpointing reduz ativações salvas, mas não remove pesos, estados do otimizador, gradientes ou buffers de comunicação. Faça uma decomposição do pico antes de habilitá-lo. Em um treino com poucos parâmetros ajustáveis, as ativações ainda podem dominar com contextos longos; em outro, a economia pode ser pequena.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

Política seletiva
As opções descritas pelo PyTorch permitem escolher quais operações recomputar e quais resultados preservar. Uma política proposta evita repetir operações muito caras quando uma ativação relativamente pequena basta. A decisão depende da forma e do hardware, e recursos de compilação ou orçamento de memória devem ser verificados na versão instalada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

Throughput útil do treinamento
Liberar memória pode permitir lote ou contexto maior, mas recomputação acrescenta trabalho por passo. Compare tokens úteis processados até atingir um critério de validação, não somente número de passos por segundo. Aumentar lote pode mudar a dinâmica da otimização e demandar ajuste de hiperparâmetros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

USO AVANÇADO — LoRA em contexto longo
Cenário: O checkpoint cabe, mas ativações estouram o orçamento.
Estratégia: Meça picos por segmento, ative checkpointing onde há melhor relação entre bytes e recomputação e valide gradientes. Preserve estado aleatório necessário.
Papel do modelo pequeno: Um 8–14B pode adaptar comportamento em contexto longo sem ajustar todos os pesos.
Aceite proposto: Completar passos estáveis e atingir validação equivalente dentro do orçamento total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

USO AVANÇADO — Comparar redução de memória
Cenário: Há opções de offload, checkpointing e quantização do modelo base.
Estratégia: Teste uma variável por vez, depois composições justificadas. Inclua tráfego de CPU, recomputação e precisão dos parâmetros treináveis.
Papel do modelo pequeno: Um 15–30B exige contabilizar estados além dos pesos antes de escolher a combinação.
Aceite proposto: Relatar pico real e tempo até qualidade-alvo, sem inferir capacidade a partir de memória nominal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Otimização pode ser dispensável em sequências curtas; manter caminho simples facilita depuração.
8–14B: Boa hipótese quando comprimento e lote tornam ativações relevantes, sujeita à medição.
15–30B: Combine com particionamento ou quantização somente depois de identificar o componente dominante do pico.
Requisitos de treino/runtime: É técnica de treinamento/backward. Não equivale a recomputar KV de uma conversa em inferência.
Não aplicar quando: Não aplicar a segmentos com efeitos colaterais ou aleatoriedade não preservada sem uma política correta.

## T115:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q017.

## T115:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T115 → T182 [complements]
Como combinar: Adapters reduzem parâmetros treináveis, enquanto checkpointing atua sobre ativações.
Interface: Módulos treináveis e fronteiras de recomputação.
Condição: Autograd mantém caminhos necessários aos adapters.
Aceite proposto: Comparar gradientes e convergência com referência pequena sem checkpoint.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S029, V4B-S028, V4B-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T115 → T183 [complements]
Como combinar: QLoRA e checkpointing atacam componentes diferentes da memória.
Interface: Base quantizada, ativações e configuração do otimizador.
Condição: Backend suporta a combinação específica.
Aceite proposto: Medir pico e estabilidade sem atribuir toda economia a uma técnica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S029, V4B-S028, V4B-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar dropout e buffers mutáveis durante recomputação.
- Registrar precisão, acumulação de gradientes e lote efetivo ao comparar configurações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie o modelo ajustado numa tarefa especializada e o custo para treiná-lo. Economizar memória de treinamento não demonstra que o modelo alcançou capacidade geral de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T116, T183

## Fontes primárias associadas

### B-S029 — torch.utils.checkpoint

[https://docs.pytorch.org/docs/2.15/checkpoint.html](https://docs.pytorch.org/docs/2.15/checkpoint.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing de ativações economiza memória e recompõe tensores durante backward.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S028 — Current and New Activation Checkpointing Techniques in PyTorch

[https://pytorch.org/blog/activation-checkpointing-techniques/](https://pytorch.org/blog/activation-checkpointing-techniques/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoint seletivo por operação e políticas de memória/recomputação para forward/backward.

Limite: Disponibilidade e estado experimental variam com versão; não demonstra aceleração de decode nem aplicação local.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T116 — KV Cache Recomputation

**Nome canônico:** KV Cache Recomputation  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T116  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recomputação de KV

## T116:C01 — conceito

Reconstrói estados KV que deixaram de estar disponíveis, reprocessando os tokens necessários com a mesma configuração do modelo. Pode ocorrer após preempção, expiração ou perda de cache. É troca de memória por trabalho repetido; não significa regenerar arbitrariamente a resposta já aceita.

Como funciona:
- Preservar sequência lógica e posição de progresso fora do cache descartável.
- Reexecutar prefill ou trecho necessário para reconstruir os estados.
- Retomar geração a partir do ponto aceito, sem duplicar conteúdo publicado.

## T116:C02 — aplicacao

Quando usar:
- Pressão de memória exige preemptar algumas sequências.
- Cache perdido pode ser reconstruído mais barato que armazenado ou transferido.

Quando não usar:
- Repetir recomputação continuamente sem reduzir a carga que causa a pressão.

Implementação proposta:
- Registrar tokens aceitos, versão do modelo e revisão de template para reconstrução.
- Distinguir o tempo de recomputação do tempo de progresso útil nas métricas.
- Definir limite de tentativas e política de admissão para conter thrashing.

Aplicação LAI proposta:
Proposta LAI: monitorar recomputação como sinal de saturação do runtime; não confundir ausência de OOM com operação eficiente.

## T116:C03 — riscos_validacao

Armadilhas:
- Reprocessar texto retokenizado de forma diferente pode produzir estados incompatíveis.
- Publicar novamente tokens anteriores gera duplicação mesmo que o estado interno esteja correto.

Métricas sugeridas:
- Tokens recomputados por token novo útil.
- Preempções, latência de retomada e tempo sem progresso.

Testes propostos:
- Eliminar deliberadamente um cache e comparar continuação com uma execução sem perda dentro das condições definidas.
- Provocar pressão sustentada e exigir progresso limitado e erro claro quando não houver capacidade.

## T116:C04 — perguntas_proveniencia

Pergunta: Recomputation altera os pesos?
Resposta: Não. Executa novamente parte do mesmo modelo para recuperar estados temporários.

Pergunta: É igual a recuperar memória episódica?
Resposta: Não. Recuperação episódica seleciona registros; recomputação KV refaz representações numéricas de tokens.

Pergunta: Recomputar é o mesmo que fazer nova resposta?
Resposta: Não. Deve processar tokens confirmados como entrada e retomar somente onde ainda falta gerar.

Pergunta: Pode restaurar com outro adaptador?
Resposta: Isso altera as projeções e possivelmente a distribuição futura; exige uma mudança declarada de configuração, não simples recuperação de cache.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T116:C05 — mecanismo_avancado

Reconstruir KV exige repetir o processamento do histórico confirmado, não repetir decisões de amostragem que já produziram tokens publicados. O cursor da resposta e o cursor do cache devem ser distintos: reconstrução avança estado interno sem emitir novamente a conversa. Se pesos ou adaptadores mudaram, recomputar produz outro estado e requer uma política explícita de migração, em vez de fingir continuidade idêntica.

Condição de contorno:
Sem os token IDs e posições originais, o texto salvo pode não reconstruir exatamente o prefixo esperado.

Contrato proposto:
- Entradas: Histórico confirmado, identidade do modelo, posição de retomada e orçamento disponível.
- Saídas: Cache restaurado e continuação a partir do primeiro token ainda não confirmado.
- Estado: Cursor de emissão, cursor reconstruído e tentativas de preempção.
- Invariante: Tokens já entregues não são reamostrados nem duplicados no transporte.

Compromissos de projeto:
- Liberar memória permite atender outros pedidos e adiciona prefill repetido.
- Preempções frequentes podem transformar capacidade aparente em trabalho improdutivo.

## T116:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: expulsar cache após alguns tokens enviados e reiniciar a reconstrução após interrupção. Esperar uma única sequência publicada e logits compatíveis com execução contínua, usando os mesmos pesos.

Plano de avaliação proposto:
Plano proposto: comparar execução sem preempção com pressões de memória controladas. Medir tokens recalculados, progresso útil, latência e repetições de preempção; ajustar admissão quando a reconstrução impede satisfazer os objetivos do serviço.

Comparações:
- T105 (complements): A política de remoção precisa preservar dados suficientes para reconstruir os estados necessários.

Afirmação rastreável:
O vLLM documenta recomputação de requisições preemptadas quando volta a existir espaço suficiente para KV.
Suporte: direct; fontes: B-S014
Limite: A documentação não garante que recomputação seja mais barata que transferência em qualquer arquitetura.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T116:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou reconstrução de cache e emissão de tokens. A nova camada formula recomputação como escolha de recuperação, com orçamento, pontos seguros e prevenção de trabalho repetido em cascata.

Reconstruir versus restaurar
Se houver cópia em memória inferior, compare seu custo com prefill do histórico confirmado. Um caminho longo com baixa banda pode favorecer recomputação; um histórico caro pode favorecer transferência. Estime ambos com medições da fase relevante e use margem para erro, evitando decisões baseadas só em bytes ou tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

Preempção repetida
Sob pressão, a mesma sequência pode ser reconstruída e novamente preemptada antes de avançar. Conte trabalho descartado e proteja temporariamente pedidos que já pagaram esse custo, dentro de limites de justiça. Sem esse controle, o serviço pode consumir recursos intensamente e entregar poucos tokens novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

Recuperação após falha
Persistir tokens confirmados e identidade do modelo permite reconstruir estado depois de perder um worker, mas não recupera automaticamente chamadas de ferramenta ou efeitos externos. O protocolo de resposta precisa distinguir texto emitido, ação solicitada e ação concluída; retomar a geração não autoriza repetir uma operação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

USO AVANÇADO — Sessão longa pouco ativa
Cenário: Manter KV residente custa mais que o padrão de uso justifica.
Estratégia: Descarte a cópia reconstruível após inatividade e mantenha histórico autorizado e versão. Na retomada, aplique limite de custo e informe estado de carregamento no serviço.
Papel do modelo pequeno: Um 3–7B pode oferecer sessões esporádicas com capacidade reduzida de cache.
Aceite proposto: Retomada deve preservar tokens anteriores e não duplicar eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

USO AVANÇADO — Falha de worker
Cenário: Uma resposta é interrompida antes de terminar.
Estratégia: Reatribua a sequência com cursor confirmado; reconstrua até esse ponto e gere somente a continuação faltante. Se a versão não estiver disponível, aplique política explícita de reinício.
Papel do modelo pequeno: Um 8–14B pode ter réplicas independentes mais econômicas que cache distribuído complexo.
Aceite proposto: Injetar falha em vários pontos e verificar entrega única e histórico coerente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S014, V3B-S005, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Históricos curtos podem favorecer recomputação simples, mas frequência de retomada importa.
8–14B: Compare restore e prefill sob concorrência, incluindo impacto em outros usuários.
15–30B: Recomputar contextos extensos em 15–30B pode consumir capacidade significativa; reserve orçamento e evite ciclos.
Requisitos de treino/runtime: Runtime precisa manter tokens confirmados, versão e estado das ações. Isso não exige novo treinamento.
Não aplicar quando: Não reamostrar prefixos publicados nem reconstruir com adapter diferente fingindo continuidade idêntica.

## T116:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T116:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T116 → T105 [complements]
Como combinar: Evicção só pode escolher recomputação se houver histórico e identidade suficientes.
Interface: Tokens confirmados e motivo de remoção.
Condição: Custo futuro estimado e estado reconstruível.
Aceite proposto: Medir quantas evicções levam a trabalho repetido sem progresso.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S014, V3B-S005, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T116 → T120 [feeds]
Como combinar: Roteamento escolhe worker considerando prefill restante e disponibilidade real.
Interface: Cursor e custo estimado de reconstrução.
Condição: Destino consegue executar a mesma identidade do modelo.
Aceite proposto: Comparar decisões com tempos observados na retomada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S014, V3B-S005, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar o número de reconstruções consecutivas sem avanço.
- Separar idempotência de ações externas da reconstrução de estado matemático.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O benefício é operacional em sessões interrompidas. Compare tempo e custo de recuperação com a mesma qualidade de modelo; recomputar histórico não acrescenta evidência nova nem corrige respostas anteriores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T105, T115, T121

## Fontes primárias associadas

### B-S014 — Optimization and Tuning

[https://docs.vllm.ai/en/latest/configuration/optimization/](https://docs.vllm.ai/en/latest/configuration/optimization/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Prefill em partes, orçamento de tokens e preempção com recomputação.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T117 — Context Parallelism

**Nome canônico:** Context Parallelism  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T117  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** paralelismo de contexto

## T117:C01 — conceito

Distribui o processamento de uma mesma sequência entre dispositivos, particionando a dimensão de contexto. É útil quando ativações e estados de uma entrada extensa ultrapassam a capacidade local. Não deve ser confundido com enviar documentos independentes a agentes paralelos ou com tensor parallelism.

Como funciona:
- Dividir posições da sequência mantendo identidade posicional global.
- Executar operações locais e comunicar dependências de atenção entre partições.
- Combinar resultados de forma consistente com o modelo completo.

## T117:C02 — aplicacao

Quando usar:
- Treino ou inferência suportada precisa processar uma sequência muito extensa.
- Há múltiplos dispositivos e interconexão adequada à comunicação.

Quando não usar:
- A carga é pequena e comunicação custa mais que o cálculo distribuído.

Implementação proposta:
- Definir se o runtime particiona prefill, decode, ativações ou KV, pois implementações diferem.
- Verificar interação com TP, PP e máscaras do modelo.
- Começar em entrada que caiba numa GPU para criar referência numérica.

Aplicação LAI proposta:
Proposta LAI: considerar após demonstrar necessidade de uma sequência maior que a capacidade local; RAG e contexto seletivo continuam alternativas de aplicação.

## T117:C03 — riscos_validacao

Armadilhas:
- Context parallelism não cria capacidade posicional ausente no checkpoint.
- Sequence parallelism pode nomear divisão de apenas certas ativações; os termos não são universalmente intercambiáveis.

Métricas sugeridas:
- Memória por GPU, tráfego e eficiência de escala.
- Tempo por sequência e desequilíbrio entre partições.

Testes propostos:
- Comparar saída distribuída e referência local em comprimentos e partições variados.
- Testar posições que atravessam fronteiras de partição e preservar causalidade.

## T117:C04 — perguntas_proveniencia

Pergunta: É simplesmente aumentar max_model_len?
Resposta: Não. Exige distribuição real de estados e operações, além de compatibilidade do modelo.

Pergunta: Uma GPU usa context parallelism entre seus agentes?
Resposta: Não nesse sentido distribuído; agentes paralelos e partição de uma sequência são mecanismos distintos.

Pergunta: CP é igual a TP?
Resposta: Não. CP divide posições do contexto; TP divide operações ou parâmetros dentro das camadas, podendo coexistir.

Pergunta: Mais contexto distribuído prova melhor compreensão?
Resposta: Não. A capacidade de executar a sequência e a capacidade do modelo de utilizar informação distante precisam ser avaliadas separadamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T117:C05 — mecanismo_avancado

Particionar o eixo de contexto muda a localização de ativações e dependências de atenção, mas posições continuam pertencendo a uma sequência global. Uma partição causal ingênua pode deixar os primeiros segmentos com menos trabalho que os últimos, pois há menos passado permitido. Balanceamento precisa considerar conexões efetivamente calculadas, além de distribuir quantidades iguais de tokens. Comunicação torna acessíveis estados que residem em outras partições.

Condição de contorno:
Dividir contexto entre dispositivos não significa que cada trecho possa ser executado independentemente sem combinar dependências.

Contrato proposto:
- Entradas: Sequência, partição por posições, plano de comunicação e máscara global.
- Saídas: Representações locais equivalentes ao modelo não particionado.
- Estado: Mapas de posições, ativações por camada e buffers de troca.
- Invariante: Cada consulta recebe exatamente as chaves permitidas na sequência global.

Compromissos de projeto:
- Mais dispositivos reduzem memória local e introduzem transferências e sincronizações.
- Balancear tokens pode não balancear cálculo sob máscaras causais.

## T117:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repartir sequência causal em segmentos desiguais e verificar tokens nas fronteiras. Comparar com referência única e registrar o trabalho por dispositivo para detectar desequilíbrio.

Plano de avaliação proposto:
Plano proposto: controlar pesos, comprimento, dtype e máscara, medindo memória por dispositivo, comunicação exposta e duração. Comparar capacidade e velocidade separadamente; aprovar somente quando a divisão atende ao objetivo sem alterar os resultados.

Comparações:
- T101 (complements): Ring Attention pode realizar a troca de blocos em uma implementação de contexto distribuído.

Afirmação rastreável:
O guia Megatron distingue context parallelism, aplicado às ativações de todas as camadas, de sequence parallelism em camadas específicas.
Suporte: direct; fontes: B-S045
Limite: A terminologia depende do framework; suporte de treinamento não implica caminho idêntico no servidor de inferência.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T117:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou posições e balanceamento causal. Esta camada considera quando paralelizar contexto é apropriado, como interage com GQA e quais aspectos de implantação foram efetivamente descritos pelos operadores.

Escopo de aplicação
Context parallelism ajuda a distribuir trabalho ou estados associados ao comprimento, especialmente em prefill longo. Decode com uma consulta nova possui outra relação entre computação e comunicação. Uma topologia adequada para uma fase não precisa ser mantida em todas; qualquer transição deve considerar redistribuição do estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

Partição composta
Combinar contexto e tensor parallelism cria eixos de comunicação distintos. Registre qual grupo possui cada posição e cada conjunto de cabeças, incluindo réplicas KV quando necessário. Uma redução de memória por eixo não se multiplica automaticamente pela outra se buffers ou estados forem replicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

Evidência operacional delimitada
Meta descreve caminhos de paralelismo de contexto em sua infraestrutura e Amazon descreve prefill distribuído no Rufus. Esses relatos sustentam viabilidade operacional nas configurações publicadas, sem demonstrar benefício para um 3–30B ou para a interconexão local. A política precisa ser reavaliada no tamanho de contexto realmente usado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Contexto excepcionalmente longo
Cenário: Poucos pedidos ultrapassam o orçamento de uma réplica.
Estratégia: Crie uma classe de execução distribuída e mantenha pedidos comuns no caminho simples. Inclua tempo de formar grupo e mover estado no orçamento da solicitação.
Papel do modelo pequeno: Um 15–30B pode precisar dessa classe por comprimento, mesmo cabendo em pesos numa GPU.
Aceite proposto: Validar equivalência e medir espera da classe longa sem bloquear consultas curtas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Estudo de seleção de topologia
Cenário: A carga mistura documentos e conversas curtas.
Estratégia: Compare réplicas, TP e CP em entradas estratificadas por comprimento. Evite concluir a partir do maior contexto suportado, que pode ser raro.
Papel do modelo pequeno: Modelos 8–14B oferecem uma faixa útil para avaliar se comunicação supera a economia.
Aceite proposto: Escolher pelo conjunto real de chegadas e respostas válidas dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S045, V4B-S003, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: CP pode ser excesso de complexidade para contextos usuais; testar réplica inteira primeiro.
8–14B: Considere CP apenas quando comprimento ou throughput de prefill justificam múltiplos dispositivos.
15–30B: Modele partição por camada e comunicação, incluindo o espaço necessário para buffers.
Requisitos de treino/runtime: Runtime e kernels devem suportar a arquitetura e topologia. Não exige novo treino se a operação for equivalente.
Não aplicar quando: Não usar CP como promessa de aumentar a janela treinada ou a capacidade de compreender contexto distante.

## T117:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: O prefill divide entrada pela dimensão de sequência.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Particionamento de contexto é explicitamente implementado.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003, V4B-Q004.

## T117:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T117 → T101 [complements]
Como combinar: Troca de blocos em anel é uma possível implementação do eixo de contexto.
Interface: Posições, blocos KV e estatísticas parciais.
Condição: Máscara global e ordenação corretas.
Aceite proposto: Comparar contra atenção não particionada em comprimentos variados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T117 → T118 [complements]
Como combinar: Os eixos de contexto e tensor podem compor uma malha.
Interface: Mapa de posições, shards e grupos de coletivas.
Condição: Interconexão e divisibilidade sustentam o plano.
Aceite proposto: Medir buffers replicados e custo de comunicação por fase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar distribuição causal desbalanceada e comprimentos não divisíveis.
- Não atribuir prefill distribuído automaticamente a todas as fases ou versões de um produto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira precisa igualar contexto útil e medir compreensão. Distribuir uma sequência permite executá-la; não prova que o modelo pequeno aproveita todas as informações presentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T101, T118, T119, T169

## Fontes primárias associadas

### B-S045 — Parallelisms Guide — Megatron Bridge

[https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html](https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Context parallelism particiona dimensão de sequência; distinto do sequence parallelism descrito no guia.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### B-S020 — Ring Attention with Blockwise Transformers for Near-Infinite Context

[https://arxiv.org/abs/2310.01889](https://arxiv.org/abs/2310.01889)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sequência distribuída e circulação de blocos KV com computação sobreposta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T118 — Tensor Parallelism

**Nome canônico:** Tensor Parallelism  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T118  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** paralelismo tensorial

## T118:C01 — conceito

Divide matrizes e operações de uma camada entre dispositivos, que cooperam para produzir o resultado da mesma inferência. Ajuda a acomodar modelos maiores ou acelerar operações suficientemente grandes, mas adiciona comunicação frequente. Não agrega VRAM como memória uniforme sem custo.

Como funciona:
- Particionar parâmetros e operações segundo um plano consistente.
- Calcular partes da mesma camada em paralelo.
- Realizar coletivas ou trocas necessárias para combinar resultados entre camadas.

## T118:C02 — aplicacao

Quando usar:
- Modelo não cabe em um dispositivo e o runtime suporta particionamento.
- Interconexão e tamanho das operações permitem amortizar comunicação.

Quando não usar:
- Modelo cabe numa GPU e a comunicação lenta supera o trabalho que seria dividido.

Implementação proposta:
- Registrar topologia física e benchmark de coletivas antes de escolher o grau de TP.
- Checar divisibilidade de cabeças, dimensões e suporte à quantização.
- Comparar TP com réplicas independentes quando a meta principal for atender mais usuários.

Aplicação LAI proposta:
Proposta LAI: antes de comprar outra GPU, comparar benefício para um modelo particionado versus dois workers e medir a interconexão disponível.

## T118:C03 — riscos_validacao

Armadilhas:
- Duas GPUs podem aumentar capacidade sem reduzir a latência individual.
- Interconexão PCIe ou rede pode virar o gargalo a cada token.

Métricas sugeridas:
- Tempo de coletivas, memória por dispositivo e tokens por segundo.
- Latência por usuário e goodput com capacidade total equivalente.

Testes propostos:
- Comparar logits contra modelo sem partição em caso que caiba na referência.
- Aumentar grau de TP e verificar se ganhos superam comunicação; registrar regressões.

## T118:C04 — perguntas_proveniencia

Pergunta: TP é igual a usar dois modelos diferentes?
Resposta: Não. Dispositivos cooperam no mesmo modelo e na mesma passagem.

Pergunta: Posso somar a VRAM e ignorar rede?
Resposta: Não. Pesos e estados podem ser divididos, mas a comunicação e buffers fazem parte do custo.

Pergunta: Dividir por duas GPUs divide a latência por dois?
Resposta: Não. Comunicação, partes não paralelizáveis e formas menores alteram o custo.

Pergunta: Como validar um checkpoint repartido?
Resposta: Reconstrua ou compare a função global em exemplos controlados, conferindo offsets e orientação das matrizes, não apenas seus tamanhos.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T118:C05 — mecanismo_avancado

Uma multiplicação linear pode ser repartida por colunas de saída ou por dimensões contraídas de entrada. No segundo caso, os produtos parciais precisam ser somados; no primeiro, o consumidor pode operar com saídas repartidas ou exigir reunião posterior. A localização das coletivas determina custo e dependências. Mais shards reduzem a parte de pesos por dispositivo, mas podem tornar a comunicação dominante em pequenos lotes.

Condição de contorno:
Dimensões, cabeças e grupos KV nem sempre são divisíveis pelo grau escolhido sem padding, replicação ou implementação específica.

Contrato proposto:
- Entradas: Pesos, plano de shards, topologia e convenções das coletivas.
- Saídas: Saída equivalente à camada completa, repartida ou reunida conforme o próximo operador.
- Estado: Mapa global de parâmetros, grupos de comunicação e buffers parciais.
- Invariante: Cada contribuição é somada ou concatenada uma única vez, na ordem semântica correta.

Compromissos de projeto:
- Maior grau reduz memória de pesos local e aumenta sincronização.
- Sobrepor comunicação ajuda apenas quando existem operações independentes suficientes.

## T118:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: carregar uma fatia de pesos na posição errada e atrasar um participante da coletiva. Esperar divergência detectada no primeiro caso e timeout controlado no segundo.

Plano de avaliação proposto:
Plano proposto: comparar graus de paralelismo com modelo e orçamento total explícitos. Medir memória, tempo de coletivas, prefill e decode por lote; escolher pela capacidade e latência reais, evitando inferir speedup linear.

Comparações:
- T119 (complements): Particionar dentro da camada pode coexistir com distribuição de conjuntos de camadas em estágios.

Afirmação rastreável:
Megatron-LM apresenta paralelismo intra-camada com operações de comunicação para combinar o trabalho distribuído.
Suporte: direct; fontes: B-S030
Limite: A receita do artigo é uma arquitetura de treinamento; cada implementação de inferência precisa validar seu plano.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T118:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou shards e coletivas. A nova camada aborda seleção econômica do grau de paralelismo, consistência de carregamento e comportamento quando o conjunto de dispositivos deixa de progredir junto.

Paralelismo mínimo suficiente
Mais shards podem permitir carregar pesos e reduzir computação local, mas acrescentam sincronizações. Compare o menor grau que atende memória com graus maiores sob a carga real. Para modelos que cabem inteiros, réplicas podem oferecer melhor capacidade total, enquanto TP pode ser útil para um prazo individual específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

Carregamento verificável
Uma distribuição errada de pesos pode produzir tensores válidos e resultados incorretos. Versione o plano de shards, nomes, offsets e configuração de quantização. Confirme checksums dos artefatos e compare camadas selecionadas com uma referência não distribuída, especialmente após conversões de layout.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

Falha e progresso
Uma coletiva atrasada pode prender todo o grupo. A saúde de uma GPU isolada não prova saúde da réplica distribuída. Observe progresso de passos, watchdogs e falhas de comunicação; ao reiniciar, trate o conjunto como unidade consistente e reconstrua cache a partir de estado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Modelo que excede uma GPU
Cenário: O checkpoint especializado precisa de mais memória de pesos.
Estratégia: Escolha topologia com comunicação adequada, distribua pesos e reserve espaço para KV e temporários. Não ocupe toda a memória só porque a divisão dos pesos parece caber.
Papel do modelo pequeno: Um 15–30B pode usar TP quando quantização adequada não atende o objetivo.
Aceite proposto: Carregar, completar contexto alvo e manter qualidade e latência sob concorrência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

USO AVANÇADO — Menor latência por pedido
Cenário: Uma única réplica atende pouco tráfego, mas há prazo rígido.
Estratégia: Compare TP com réplica inteira usando lote pequeno, incluindo sincronização. Se TP não reduzir o caminho crítico, prefira capacidade independente.
Papel do modelo pequeno: Um 8–14B deve justificar a distribuição por medição, não por associação com infraestrutura de bigtech.
Aceite proposto: Medir percentis de latência e custo reservado por resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S030, B-S045, V4B-S003, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, comunicação e overhead podem dominar; réplicas independentes são uma hipótese inicial.
8–14B: Teste divisibilidade de cabeças e layouts quantizados antes de escolher o grau.
15–30B: Inclua falha conjunta, buffers e KV no dimensionamento; pesos são apenas uma parcela.
Requisitos de treino/runtime: Runtime distribuído, coletivas e checkpoint compatíveis; TP preserva a arquitetura quando implementado corretamente.
Não aplicar quando: Não inferir aceleração a partir da quantidade de GPUs nem da soma nominal de suas capacidades.

## T118:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 2. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Tensor parallelism integra as estratégias híbridas descritas.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: Atenção usa tensor parallelism no deployment descrito.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: O operador descreve implementação e otimização de tensor parallelism.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003, V4B-Q004.

## T118:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T118 → T117 [complements]
Como combinar: Contexto e tensor podem ser particionados em eixos diferentes.
Interface: Malha e propriedade de tensores.
Condição: Plano consistente em todas as camadas.
Aceite proposto: Comparar memória real com estimativa e validar resultados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S030, B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T118 → T122 [complements]
Como combinar: Interconexão de baixa sobrecarga pode transportar dados das coletivas quando suportada.
Interface: Buffers, grupos e eventos de conclusão.
Condição: Stack e topologia efetivamente habilitam o caminho.
Aceite proposto: Medir comunicação e testar falhas sem consumidores de dados parciais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S030, B-S045, V4B-S003, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checar versões e layouts idênticos em todos os ranks.
- Não servir resultados de um grupo com estado divergente após recuperação parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
TP pode tornar um modelo especializado executável ou mais rápido, sem alterar sua competência. Compare custo por tarefa concluída e inclua recursos ociosos reservados ao grupo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T117, T119, T122, T107

## Fontes primárias associadas

### B-S030 — Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

[https://arxiv.org/abs/1909.08053](https://arxiv.org/abs/1909.08053)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Paralelismo dentro de camadas, complementar ao pipeline.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S045 — Parallelisms Guide — Megatron Bridge

[https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html](https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Context parallelism particiona dimensão de sequência; distinto do sequence parallelism descrito no guia.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

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

# T119 — Pipeline Parallelism

**Nome canônico:** Pipeline Parallelism  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T119  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** paralelismo de pipeline

## T119:C01 — conceito

Divide grupos de camadas em estágios executados por dispositivos diferentes. Microbatches ou requisições distintas ocupam vários estágios ao mesmo tempo. Ajuda a acomodar redes extensas e aumentar aproveitamento, mas uma única sequência ainda atravessa os estágios em ordem.

Como funciona:
- Particionar camadas em estágios com custo e memória equilibrados.
- Transferir ativações de um estágio ao seguinte.
- Intercalar microbatches ou requisições para preencher o pipeline.

## T119:C02 — aplicacao

Quando usar:
- Modelo excede memória por dispositivo e camadas podem ser distribuídas.
- Há concorrência suficiente para reduzir ociosidade dos estágios.

Quando não usar:
- Esperar baixa latência de um único decode apenas aumentando o número de estágios.

Implementação proposta:
- Balancear por tempo medido e memória, não somente por número de camadas.
- Configurar limites de microbatches, transferência e estados por requisição.
- Comparar com tensor parallelism ou combinação suportada para o mesmo orçamento de GPUs.

Aplicação LAI proposta:
Proposta LAI: considerar como estratégia de capacidade distribuída, com ensaio de concorrência; não presumir aceleração de uma única chamada de atendimento.

## T119:C03 — riscos_validacao

Armadilhas:
- Estágio lento cria gargalo para todo o pipeline.
- Bolhas de início/fim e baixa concorrência deixam GPUs ociosas.

Métricas sugeridas:
- Ociosidade por estágio e duração do caminho completo.
- Throughput, tempo de transferência e memória de ativações em trânsito.

Testes propostos:
- Executar entradas com comprimentos diferentes e medir desequilíbrio dos estágios.
- Falhar um estágio e exigir encerramento coerente da requisição sem resposta parcial considerada válida.

## T119:C04 — perguntas_proveniencia

Pergunta: Pipeline divide tokens entre GPUs?
Resposta: Primariamente divide camadas; context parallelism divide a dimensão de sequência.

Pergunta: Por que surgem bolhas?
Resposta: Um estágio pode esperar dados do anterior ou ficar sem trabalho enquanto o pipeline preenche e esvazia.

Pergunta: Mais microbatches sempre ajudam?
Resposta: Não. Menores operações podem perder eficiência e mais itens pendentes ampliam filas e temporários.

Pergunta: Pipeline acelera uma única sequência curta?
Resposta: Pode apenas permitir que o modelo caiba; a travessia serial e a dependência autoregressiva continuam presentes.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T119:C05 — mecanismo_avancado

Com p estágios equilibrados e m microbatches, um forward idealizado ocupa m+p−1 intervalos; a fração útil do pipeline é m/(m+p−1), ignorando comunicação e diferenças de custo. Essa conta explica bolhas de preenchimento e drenagem, mas não prevê diretamente decode autoregressivo: uma sequência depende do token anterior antes de iniciar o próximo. Concorrência entre sequências pode preencher parte dessas lacunas.

Condição de contorno:
Um estágio mais lento determina a cadência; dividir camadas igualmente não garante equilíbrio de tempo ou memória.

Contrato proposto:
- Entradas: Camadas por estágio, microbatches ou requisições e protocolo de transporte.
- Saídas: Saídas ordenadas com identidade de sequência preservada entre estágios.
- Estado: Filas intermediárias, créditos de capacidade e identificadores de passo.
- Invariante: Um estágio nunca combina ativações de tokens ou requisições diferentes.

Compromissos de projeto:
- Mais estágios reduzem pesos locais e aumentam travessias e bolhas.
- Mais trabalho em andamento melhora utilização e pode elevar latência e memória de ativações.

## T119:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar o estágio central e cancelar uma sequência enquanto outras atravessam o pipeline. Esperar backpressure e remoção consistente, sem reaproveitar ativação cancelada em outro pedido.

Plano de avaliação proposto:
Plano proposto: comparar partições com os mesmos pesos e carga. Medir duração por estágio, bolhas, tráfego e latência por sequência; aceitar balanceamento pela cadência efetiva e objetivos de serviço, não pelo número igual de camadas.

Comparações:
- T118 (complements): Tensor parallelism pode reduzir o custo de um estágio sem eliminar dependências entre estágios.

Afirmação rastreável:
GPipe particiona redes em sequências de camadas e divide lotes para preencher o pipeline.
Suporte: direct; fontes: B-S031
Limite: A fórmula apresentada é um modelo idealizado de forward; treinamento e decode exigem cronogramas próprios.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T119:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 apresentou bolhas e dependência autoregressiva. A nova camada considera particionamento por custo real, controle de filas entre estágios e distinção entre objetivos de treinamento e serving interativo.

Balanceamento por perfil
Dividir igual quantidade de camadas não garante estágios equilibrados: embeddings, projeção de saída e tipos de camada podem ter custos diferentes. Meça tempo e pico de memória por estágio nas formas reais. Um estágio lento limita fluxo inteiro, enquanto outro pode ficar ocioso com memória reservada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S031, B-S045, V3B-S010.

Créditos entre estágios
Filas intermediárias precisam de limites e backpressure. Sem créditos, um produtor rápido acumula ativações que o consumidor não consegue processar. Cada mensagem deve carregar identidade da sequência, posição e versão; cancelamento libera recursos em todos os estágios sem entregar saídas de uma tentativa antiga.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S031, B-S045, V3B-S010.

Objetivo de serviço
Treinamento pode preencher pipeline com microbatches relativamente previsíveis; geração interativa mistura tamanhos e depende de tokens anteriores. Uma agenda que maximiza ocupação pode aumentar tempo individual. Declare se o objetivo é throughput de um lote offline, prazo de streaming ou viabilizar memória de pesos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S031, B-S045, V3B-S010.

USO AVANÇADO — Processamento offline
Cenário: Há muitos documentos independentes e prazos flexíveis.
Estratégia: Agrupe requisições por custo aproximado, alimente o pipeline com créditos e drene resultados sem perder identidade. Inclua falhas e reexecuções na capacidade planejada.
Papel do modelo pequeno: Um 15–30B pode ser dividido quando pesos ou ativações não cabem como desejado.
Aceite proposto: Comparar custo total do lote e resultados completos, incluindo bolhas e drenagem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S031, B-S045, V3B-S010.

USO AVANÇADO — Serving com restrição de interconexão
Cenário: TP exige comunicação frequente que não atende o ambiente.
Estratégia: Teste PP como alternativa de posicionamento, mantendo expectativas realistas de latência. Modele transporte entre estágios e concorrência necessária para ocupação.
Papel do modelo pequeno: Um 8–14B só justifica a complexidade se houver uma restrição concreta.
Aceite proposto: Aceitar se o serviço atende prazo e memória melhor que alternativas medidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S031, B-S045, V3B-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Para modelos pequenos que cabem inteiros, a fragmentação costuma exigir uma justificativa operacional específica.
8–14B: Avalie poucas divisões e custos de filas; não use quantidade de camadas como único balanceador.
15–30B: Em 15–30B, PP pode resolver capacidade, mas o ritmo de decode continua dependente do caminho completo.
Requisitos de treino/runtime: Runtime ou treinamento distribuído com plano de estágios; preserva arquitetura se transporta ativações corretas.
Não aplicar quando: Não transferir fórmulas ideais de microbatch de treinamento diretamente para latência autoregressiva.

## T119:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Buscas de paralelismo e serving consultadas. As fontes selecionadas sustentam mecanismos e pesquisa; não foi confirmado neste recorte um caso exato adicional de PP implantado em bigtech para 3–30B.
Consultas registradas: V4B-Q003.

## T119:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T119 → T118 [alternative]
Como combinar: Comparar PP e TP separa transporte entre estágios de coletivas por camada.
Interface: Plano de partição e perfil de comunicação.
Condição: Mesma qualidade e distribuição de pedidos.
Aceite proposto: Medir latência, capacidade e recursos reservados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S031, B-S045, V3B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T119 → T121 [requires]
Como combinar: A agenda controla admissão e créditos para evitar filas intermediárias ilimitadas.
Interface: Capacidade por estágio, identidade e cancelamento.
Condição: Todos os estágios propagam backpressure.
Aceite proposto: Induzir um estágio lento e verificar limites de memória.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S031, B-S045, V3B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Invalidar mensagens atrasadas de tentativas canceladas.
- Não contar ocupação de um estágio como utilização útil do pipeline inteiro.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
PP modifica o custo de executar o mesmo modelo. Uma comparação com fronteira deve avaliar tarefas e prazos, sem atribuir ganho de qualidade ao uso de vários estágios.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T118, T117, T102

## Fontes primárias associadas

### B-S031 — GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism

[https://arxiv.org/abs/1811.06965](https://arxiv.org/abs/1811.06965)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento de camadas em estágios e execução por microbatches.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S045 — Parallelisms Guide — Megatron Bridge

[https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html](https://docs.nvidia.com/nemo/megatron-bridge/latest/parallelisms.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Context parallelism particiona dimensão de sequência; distinto do sequence parallelism descrito no guia.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S010 — DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

[https://arxiv.org/abs/2401.09670](https://arxiv.org/abs/2401.09670)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interferência entre prefill/decode, objetivos TTFT/TPOT e alocação considerando banda de comunicação.

Limite: Resumo consultado; regras de transferência e testes de falha das fichas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T120 — KV Cache Routing

**Nome canônico:** KV Cache Routing  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T120  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cache-aware routing; roteamento consciente de KV

## T120:C01 — conceito

Escolhe o worker de inferência considerando quais estados KV já estão disponíveis e quanto trabalho ele tem em andamento. Busca reduzir prefill repetido sem concentrar tráfego num servidor saturado. Seleção de destino e transporte de estados são funções relacionadas, mas separadas.

Como funciona:
- Consultar um índice de prefixos ou estados disponíveis por worker.
- Combinar afinidade de cache com carga, elegibilidade e custo previsto.
- Encaminhar a requisição e atualizar o índice com eventos de criação ou remoção.

## T120:C02 — aplicacao

Quando usar:
- Várias réplicas atendem prompts ou conversas com prefixos reutilizáveis.
- Cache local faz diferença material no custo de prefill.

Quando não usar:
- Um único worker atende tudo ou a informação de cache fica tão stale que prejudica decisões.

Implementação proposta:
- Definir identidade de blocos e escopo de isolamento consistente entre roteador e workers.
- Manter caminho de fallback para worker válido sem cache.
- Penalizar carga projetada e medir o equilíbrio entre localidade e fila.

Aplicação LAI proposta:
Proposta LAI: adotar somente quando houver várias réplicas; manter identidade de tenant e checkpoint no contrato para evitar afinidade indevida.

## T120:C03 — riscos_validacao

Armadilhas:
- Preferir sempre o maior cache hit pode criar um ponto de saturação.
- Eventos perdidos podem anunciar blocos já removidos e levar a decisões ruins.

Métricas sugeridas:
- Prefixo efetivamente reutilizado após roteamento e acertos previstos versus reais.
- Tempo de fila, distribuição de carga e TTFT por worker.

Testes propostos:
- Simular cache quente em worker ocupado e confirmar escolha coerente com a meta de latência.
- Excluir estados sem atualizar imediatamente o índice e verificar recuperação segura de cache miss.

## T120:C04 — perguntas_proveniencia

Pergunta: Roteamento de KV escolhe o melhor modelo?
Resposta: Não necessariamente. Em geral escolhe uma instância compatível; model routing decide entre modelos.

Pergunta: Cache hit deve sempre ganhar?
Resposta: Não. Espera e carga podem tornar um worker sem cache mais rápido no custo total.

Pergunta: Roteamento transfere automaticamente o KV?
Resposta: Não necessariamente. A decisão de posicionamento e o mecanismo de transporte têm contratos separados.

Pergunta: Por que reservar carga ao decidir?
Resposta: Sem contabilizar decisões simultâneas, vários pedidos podem escolher o mesmo worker aparentemente livre e criar uma fila inesperada.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T120:C05 — mecanismo_avancado

O índice de localização é uma previsão de disponibilidade, não uma reserva irrevogável. Entre seleção e execução, um prefixo pode ser expulso ou o worker receber nova carga. Como proposta operacional, o destino confirma identidade e disponibilidade antes de reutilizar; um miss real deve provocar prefill explícito ou nova decisão, preservando o pedido. A função de custo precisa incluir trabalho já comprometido, não somente a fila observada.

Condição de contorno:
Enviar sempre ao maior prefixo pode criar um ponto quente e piorar latência apesar de economizar tokens de prefill.

Contrato proposto:
- Entradas: Tokens normalizados, elegibilidade dos workers, afinidade de cache e carga projetada.
- Saídas: Destino escolhido com estimativa de custo e confirmação do hit real.
- Estado: Índice de eventos, decisões pendentes e carga já atribuída.
- Invariante: A localização sugerida nunca autoriza reutilizar estado incompatível ou ausente.

Compromissos de projeto:
- Afinidade economiza reconstrução e pode concentrar carga.
- Índices mais frequentes reduzem defasagem e aumentam tráfego de controle.

## T120:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover o prefixo logo após o roteamento e atrasar seu evento de exclusão. Esperar miss reconhecido e recuperação correta, sem assumir que o índice garantiu presença.

Plano de avaliação proposto:
Plano proposto: comparar round-robin, carga e custo com cache sob chegadas idênticas. Medir hits confirmados, erro da previsão, TTFT e distribuição de carga; aceitar benefício sem degradar classes de pedidos menos reutilizáveis.

Comparações:
- T102 (complements): Em fases separadas, escolher workers e transferir estado são responsabilidades distintas.

Afirmação rastreável:
O Dynamo combina sobreposição de prefixo com carga ativa de prefill e decode para escolher workers.
Suporte: direct; fontes: B-S032
Limite: O teste de índice defasado é uma proposta editorial; não declara um defeito observado no produto.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T120:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu localização prevista de disponibilidade confirmada. A nova análise introduz custo de remanejamento, incerteza da observação e efeitos de afinidade na distribuição de capacidade.

Índice com atraso
Eventos de cache chegam depois de mudanças no worker. Guarde idade da observação e confiança da estimativa, em vez de tratar todos os hits anunciados como equivalentes. Uma confirmação negativa deve atualizar o índice e permitir prefill normal; repetir roteamento indefinidamente pode consumir o prazo sem executar trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

Afinidade versus fila
Um worker com prefixo pode ser pior destino que outro livre que precisa recomputar. Compare economia de prefill com espera, transferências e reservas já comprometidas. Session affinity, como documentada no Workers AI, é um mecanismo útil, mas não equivale por si só a otimização global baseada em inventário de KV.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

Evitar oscilação
Mover pedidos entre destinos conforme pequenas mudanças de fila pode gerar tráfego e decisões contraditórias. Aplique histerese e limite de reatribuições, mantendo uma decisão estável após reserva confirmada. Se houver migração de estado, o destino só assume propriedade depois de verificar completude e identidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

USO AVANÇADO — Chat com prefixo recorrente
Cenário: Sessões compartilham um contexto estável e alternam atividade.
Estratégia: Use afinidade como sinal, junto com custo atual e prazo. Quando a réplica estiver congestionada, permita execução fria em outra sem alterar o conteúdo da conversa.
Papel do modelo pequeno: Um 3–7B pode ser replicado para isolar picos e manter uma política simples.
Aceite proposto: Comparar ganho de reúso com aumento de espera por sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

USO AVANÇADO — Roteamento de documentos longos
Cenário: Pedidos próximos reutilizam documentos distintos.
Estratégia: Indexe prefixos por versão e domínio, estime prefill evitado e limite concentração por família. Não mova contexto sensível para um destino inelegível.
Papel do modelo pequeno: Um 15–30B pode economizar prefill caro quando o padrão de reúso é estável.
Aceite proposto: Medir hits consumidos, transferências inúteis e cumprimento de prazos por família.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S032, V4B-S004, V4B-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Recomputar prompts curtos pode custar menos que manter um roteador sofisticado.
8–14B: Use observações por réplica e meça a divergência entre custo previsto e real.
15–30B: Quando um pedido ocupa vários dispositivos, destino significa um grupo saudável, não apenas uma GPU.
Requisitos de treino/runtime: Runtime precisa publicar disponibilidade e carga; arquitetura do modelo permanece a mesma.
Não aplicar quando: Não usar afinidade de sessão como autorização de acesso nem semântica aproximada para reutilizar KV.

## T120:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 5.1/Algoritmo 1 de Mooncake v1 escolhe worker usando prefixo reutilizável, fila, transferência prevista e TTFT/SLO.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Roteamento busca a mesma instância, sem comprovar consulta dinâmica a blocos KV de todos os workers.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002, V4B-Q022.

## T120:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T120 → T082 [feeds]
Como combinar: O roteamento aumenta chance de consumir prefixos já calculados.
Interface: Identidade completa do prefixo e comprimento.
Condição: Hit confirmado no destino.
Aceite proposto: Atribuir economia apenas a tokens realmente reutilizados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S032, V4B-S004, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T120 → T102 [complements]
Como combinar: Em serviço desagregado, escolha de destino inclui quem fará prefill e quem manterá decode.
Interface: Plano de transferência e reserva em ambos os pools.
Condição: Custo do transporte entra na decisão.
Aceite proposto: Testar saturação de rede e fallback sem duplicar pedido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S032, V4B-S004, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Limitar retries de roteamento e preservar idade original do pedido.
- Separar misses de índice obsoleto, evicção e incompatibilidade de configuração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação deve avaliar o serviço distribuído completo. Roteamento de cache pode baixar custo, mas não altera a informação ou capacidade disponíveis ao modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T102, T103, T133, T171

## Fontes primárias associadas

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T121 — GPU Scheduling

**Nome canônico:** GPU Scheduling  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T121  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalonamento de GPU

## T121:C01 — conceito

Família de políticas que decide qual trabalho ocupará o acelerador e quando. No serving de LLMs, inclui admissão de sequências, prioridade entre prefill/decode e controle de pressão KV. Difere do agendamento interno de warps pelo hardware; ambos influenciam desempenho em níveis distintos.

Como funciona:
- Observar fila, recursos disponíveis e prazos das requisições.
- Selecionar trabalho para a próxima unidade de execução.
- Atualizar uso de memória e progresso, reconsiderando prioridades sem perder estado.

## T121:C02 — aplicacao

Quando usar:
- Atendimento interativo compartilha GPU com tarefas longas ou em lote.
- Picos de demanda produzem OOM, preempções ou cauda de latência alta.

Quando não usar:
- Admitir tudo imediatamente com objetivo de manter utilização aparente alta.

Implementação proposta:
- Definir objetivos por classe de serviço e orçamento de memória para crescimento de KV.
- Adicionar limites de fila e envelhecimento para impedir starvation.
- Separar métricas do scheduler de aplicação, runtime e kernels.

Aplicação LAI proposta:
Proposta LAI: estabelecer prioridade de interação humana e limites para tarefas em lote, com quotas medidas e sem prometer que ambas cabem simultaneamente.

## T121:C03 — riscos_validacao

Armadilhas:
- Prioridade absoluta para tarefas curtas pode impedir conclusão das longas.
- GPU ocupada recomputando estados pode parecer eficiente enquanto o trabalho útil cai.

Métricas sugeridas:
- Goodput por classe, espera p95 e tempo de starvation.
- Preempções, memória livre e tokens úteis versus recomputados.

Testes propostos:
- Misturar fluxos curtos, longos e cancelados; exigir prazos e progresso mínimo definidos para cada classe.
- Exceder a capacidade e verificar backpressure previsível em vez de falha em cascata.

## T121:C04 — perguntas_proveniencia

Pergunta: Utilização máxima é sempre o objetivo?
Resposta: Não. O objetivo útil é concluir trabalho correto dentro dos prazos e do orçamento.

Pergunta: Scheduler de GPU é só uma fila FIFO?
Resposta: Pode usar FIFO, mas LLMs também exigem considerar memória, fases e duração variável.

Pergunta: Token é uma unidade uniforme de custo?
Resposta: Não. Seu custo depende da fase, contexto, modelo e lote; estimativas precisam ser calibradas na carga.

Pergunta: Pode prometer prazo pelo tamanho do prompt?
Resposta: Não sozinho. Saída, fila, cache e comunicação também influenciam a conclusão.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T121:C05 — mecanismo_avancado

Uma fila de inferência contém trabalhos com custos heterogêneos: prefill longo, decode curto e crescimento futuro de KV não são equivalentes. Como proposta de escalonamento, use custos estimados e prioridades envelhecidas, reavaliando após cada unidade permitida de execução. Interromper uma requisição entre iterações é diferente de preemptar arbitrariamente um kernel já em execução; a granularidade oferecida pelo backend limita a política real.

Condição de contorno:
Ocupação alta pode ocultar trabalho repetido, esperas injustas ou violações de prazo; utilização isolada não mede serviço útil.

Contrato proposto:
- Entradas: Fila, estimativas de trabalho, memória, prazos e pontos permitidos de decisão.
- Saídas: Plano da próxima rodada e justificativas de admissão, espera ou preempção.
- Estado: Idades, custos previstos, progresso confirmado e reservas de crescimento.
- Invariante: O escalonador respeita recursos e não confunde trabalho iniciado com trabalho concluído.

Compromissos de projeto:
- Favorecer trabalhos curtos pode reduzir média e prejudicar longos sem envelhecimento.
- Reservar margem de memória reduz falhas e pode deixar capacidade momentaneamente ociosa.

## T121:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: misturar fluxo contínuo de pedidos curtos com um longo, além de saídas maiores que a previsão. Esperar progresso do longo e política explícita para pressão de memória.

Plano de avaliação proposto:
Plano proposto: comparar políticas com a mesma sequência de chegadas e comprimentos. Medir goodput, deadlines, TTFT, intervalos entre tokens e recomputação; aceitar apenas melhorias que preservem os requisitos por classe definidos previamente.

Comparações:
- T088 (complements): Continuous batching oferece pontos de decisão; a política define quais sequências participam.

Afirmação rastreável:
Sarathi-Serve explora a separação de características entre prefill e decode para reduzir interferência no escalonamento.
Suporte: related; fontes: V3B-S004
Limite: O artigo apoia esse princípio; política de envelhecimento e reservas desta ficha é proposta, não configuração universal.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T121:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu unidades heterogêneas e pontos de decisão. O aprofundamento acrescenta erro de previsão, contratos de justiça e estratégias de admissão que tornam o serviço estável em sobrecarga.

Previsões revisáveis
Comprimento de saída raramente é conhecido antes de gerar. Reserve margem inicial e atualize estimativas conforme o pedido avança, sem contar memória futura como gratuita. Registre erro da previsão por classe; uma classe com respostas longas pode consumir capacidade muito além do custo estimado na admissão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

Justiça observável
Prioridade de negócio precisa de limite de espera e de capacidade ocupada. Meça distribuição de atraso por classe e por tamanho, não só média global. Uma política pode melhorar números agregados deixando pedidos longos sem progresso; envelhecimento e cotas oferecem controles, mas devem ser testados sob chegada contínua.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

Sobrecarga explícita
Quando a chegada excede capacidade, fila ilimitada não cria throughput. Use admissão, deadlines e cancelamento para evitar gastar GPU em respostas que o cliente já abandonou. Distinga rejeição antecipada de falha depois de consumir recursos, e exponha causas para que o cliente não multiplique retries agressivos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

USO AVANÇADO — Assistente interativo e lote interno
Cenário: As duas cargas compartilham a mesma frota.
Estratégia: Reserve capacidade para o interativo e permita ao lote usar sobra com checkpoints ou reexecução delimitada. Defina quais unidades podem ser interrompidas e o custo dessa decisão.
Papel do modelo pequeno: Um 3–7B pode assumir tarefas de lote enquanto um modelo maior atende casos complexos, se houver roteamento validado.
Aceite proposto: Medir prazos das duas classes e custo de trabalho descartado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

USO AVANÇADO — Pico de demanda imprevisível
Cenário: Pedidos novos têm tamanho muito variável.
Estratégia: Adote orçamento por tokens e memória, revise durante execução e cancele trabalho expirado. Aumente capacidade com réplicas somente após separar gargalo de fila, prefill e decode.
Papel do modelo pequeno: Modelos 8–14B podem oferecer capacidade especializada sob limites explícitos.
Aceite proposto: Estabilidade da fila e proporção de respostas úteis dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S004, V4B-S008, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Muitas sequências pequenas podem ser limitadas por overhead; política simples pode ser suficiente.
8–14B: Separar prefill e decode no orçamento ajuda a lidar com documentos longos.
15–30B: Reservas maiores precisam incluir crescimento de KV e grupo de dispositivos quando distribuído.
Requisitos de treino/runtime: Runtime deve oferecer pontos seguros de agendamento e cancelamento; não há preempção arbitrária garantida de kernels.
Não aplicar quando: Não maximizar tokens por segundo ignorando tempo de espera, abandono ou respostas truncadas.

## T121:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Scheduler equilibra throughput e SLO de requisições.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Admissão assíncrona usa capacidade observada, sem expor todos os detalhes do scheduler GPU.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T121:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T121 → T094 [complements]
Como combinar: Prefill em blocos permite intercalar trabalho longo e decodes.
Interface: Custo do próximo bloco e prazo das sequências.
Condição: Backend suporta a granularidade escolhida.
Aceite proposto: Verificar melhora de prazos sem excesso de fragmentação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T121 → T087 [requires]
Como combinar: Continuous batching executa a agenda com entrada e saída dinâmica.
Interface: Lote ativo e reservas por sequência.
Condição: Admissão respeita memória e crescimento.
Aceite proposto: Aplicar carga aberta para observar saturação real.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S004, V4B-S008, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar idade e deadline ao reenfileirar ou migrar.
- Medir cancelamento efetivo na GPU, não apenas desconexão do cliente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare respostas válidas por orçamento sob a mesma chegada de usuários. Um serviço rápido em teste fechado pode falhar sob sobrecarga real; isso precisa ser separado de qualidade do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T088, T094, T149, T166, T174

## Fontes primárias associadas

### B-S008 — Orca: A Distributed Serving System for Transformer-Based Generative Models

[https://www.usenix.org/conference/osdi22/presentation/yu](https://www.usenix.org/conference/osdi22/presentation/yu)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por iteração e batching seletivo para geração autorregressiva.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S047 — Batchers — NVIDIA Triton Inference Server

[https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Batching dinâmico agrupa requisições compatíveis e permite controlar espera e filas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S004 — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[https://arxiv.org/abs/2403.02310](https://arxiv.org/abs/2403.02310)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre prefill e decode; chunked prefills e escalonamento para reduzir interrupções.

Limite: Resumo consultado; não extrapolar ganhos de sistemas ou hardware publicados para implantação local.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T122 — RDMA para inferência distribuída

**Nome canônico:** RDMA para inferência distribuída  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** protocol  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T122  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Remote Direct Memory Access; GPUDirect RDMA

## T122:C01 — conceito

Remote Direct Memory Access permite transferências entre memórias com menor intervenção da CPU no caminho de dados, conforme a tecnologia usada. GPUDirect RDMA é um caso em que dispositivo peer pode acessar memória de GPU compatível. É infraestrutura de comunicação, não aceleração automática de qualquer modelo.

Como funciona:
- Registrar regiões de memória e estabelecer recursos de transporte autorizados.
- Transferir dados por interface e drivers compatíveis com a topologia.
- Sincronizar conclusão antes de o consumidor utilizar o buffer.

Nota de nomenclatura: RDMA é família de mecanismos de comunicação; GPUDirect RDMA é uma variante específica, não sinônimo irrestrito.

## T122:C02 — aplicacao

Quando usar:
- Inferência distribuída transfere KV ou coletivas em volume que justifica otimização de rede.
- GPU, NIC, drivers e plataforma têm suporte confirmado.

Quando não usar:
- Presumir que qualquer placa de rede e GPU de consumo oferecem GPUDirect RDMA funcional.

Implementação proposta:
- Inventariar NIC, drivers, caminho PCIe, firmware e suporte oficial de cada componente.
- Medir banda e latência com buffers e tamanhos representativos da inferência.
- Comparar transporte com e sem caminho direto e verificar correção dos dados.

Aplicação LAI proposta:
Proposta LAI: exigir evidência de suporte para a combinação exata de hardware antes de contar RDMA no plano de duas ou mais GPUs/servidores.

## T122:C03 — riscos_validacao

Armadilhas:
- Topologia PCIe e restrições de plataforma podem bloquear o caminho esperado.
- Transferência rápida isolada não resolve custos de serialização, sincronização e filas.

Métricas sugeridas:
- Banda sustentada, latência por tamanho de mensagem e uso de CPU.
- Tempo de handoff KV e participação da comunicação na latência total.

Testes propostos:
- Transferir padrões conhecidos e verificar integridade após sincronização.
- Interromper um peer e exigir timeout e liberação de recursos, sem consumo de buffer incompleto.

## T122:C04 — perguntas_proveniencia

Pergunta: RDMA e NVLink são a mesma coisa?
Resposta: Não. São tecnologias e caminhos de comunicação distintos, embora ambos possam participar de sistemas distribuídos.

Pergunta: Ter uma 5090 comprova GPUDirect RDMA?
Resposta: Não. O suporte precisa ser confirmado para GPU, NIC, drivers e plataforma específicos.

Pergunta: RDMA significa zero latência?
Resposta: Não. Existem transferência física, filas, registro e sincronização, mesmo quando cópias intermediárias são evitadas.

Pergunta: Checksum resolve ordenação?
Resposta: Pode detectar corrupção, mas não torna válida uma leitura concorrente antes da disponibilidade; sincronização continua necessária.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T122:C05 — mecanismo_avancado

Conclusão da transferência no dispositivo de rede não substitui automaticamente a ordenação necessária para um kernel consumidor na GPU. A documentação GPUDirect distingue visibilidade e sincronização, incluindo o risco de leitura concorrente de dados parcialmente escritos. Um contrato de transporte precisa ligar conclusão de DMA, evento de disponibilidade e submissão do consumidor, além de manter a região registrada válida durante toda a operação.

Condição de contorno:
Topologia, memória registrada, drivers e suporte do transporte condicionam o caminho direto; o nome RDMA não garante ausência de cópias.

Contrato proposto:
- Entradas: Regiões registradas, destino, tamanho, identificação da transferência e protocolo de conclusão.
- Saídas: Dados disponíveis para consumo ordenado e confirmação verificável.
- Estado: Registros de memória, buffers em voo, eventos e propriedade dos slots.
- Invariante: Nenhum consumidor lê ou libera um buffer antes da conclusão e ordenação exigidas.

Compromissos de projeto:
- Caminho direto pode reduzir cópias de CPU e aumenta exigências de sincronização.
- Registro e reutilização de buffers amortizam custos, mas exigem ciclo de vida correto.

## T122:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar consumo antes da confirmação de transferência e depois aplicar o protocolo correto. O caso inválido deve ser rejeitado pelo controle, sem depender de corrupção aparecer aleatoriamente.

Plano de avaliação proposto:
Plano proposto: comparar transporte com staging e caminho direto sob mesmos tamanhos e topologia. Medir latência, banda efetiva, CPU, registro e integridade; aprovar o caminho completo, incluindo sincronização, não apenas tempo bruto da NIC.

Comparações:
- T102 (complements): Transferência KV entre fases exige esse cuidado quando usa comunicação direta com memória de GPU.

Afirmação rastreável:
O guia GPUDirect RDMA alerta que kernels concorrentes podem observar dados antigos ou parcialmente escritos sem ordenação adequada.
Suporte: direct; fontes: B-S033
Limite: A fonte descreve requisitos CUDA/GPUDirect; outros transportes podem oferecer abstrações adicionais que devem ser verificadas.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T122:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou ordenação entre DMA e consumidores. A nova camada considera integração do transporte ao ciclo de vida da requisição, congestionamento e transferência de estado além dos tensores principais.

Objeto transferido
Uma transferência de inferência pode incluir páginas KV, metadados e estados auxiliares. A Perplexity descreve transporte ligado a prefill/decode e componentes adicionais quando necessários. Defina um manifesto por sequência e versão; o destino não deve iniciar só porque recebeu a maior parcela dos bytes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S033, V4B-S002, V4B-S008.

Pipeline de transporte
Transferir camadas conforme ficam prontas pode sobrepor comunicação e computação, mas depende da ordem em que o consumidor precisará delas. Meça caminho crítico e buffers em voo. Uma sobreposição aparente pode apenas deslocar espera para o final, especialmente quando a rede atende muitos produtores simultaneamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S033, V4B-S002, V4B-S008.

Congestionamento e custo
RDMA reduz certas sobrecargas, mas não elimina banda finita, registro de memória, topologia ou contenção. Compare tempo de transferência e prefill evitado sob carga. Em estado pequeno, preparação pode dominar; em estado grande, transporte pode aumentar TTFT apesar de liberar capacidade de computação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S033, V4B-S002, V4B-S008.

USO AVANÇADO — Pools separados de prefill e decode
Cenário: Os recursos de cada fase são dimensionados independentemente.
Estratégia: Reserve destino, transfira estado com manifesto e publique disponibilidade somente após confirmação. Cancele ou recupere transferências interrompidas sem liberar buffers prematuramente.
Papel do modelo pequeno: Um 15–30B pode se beneficiar se a carga justificar a separação; não é requisito por porte.
Aceite proposto: Medir latência completa e capacidade de cada pool, incluindo rede saturada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S033, V4B-S002, V4B-S008.

USO AVANÇADO — Teste de recuperação do transporte
Cenário: Falhas ocorrem durante troca de estado.
Estratégia: Injete interrupções antes e depois de confirmação, registre propriedade e invalide destinos incompletos. Retome por transferência íntegra ou recomputação explícita.
Papel do modelo pequeno: Um modelo menor permite exercitar protocolo com custos controlados antes da escala.
Aceite proposto: Nenhum consumo parcial, duplicação de propriedade ou vazamento de memória após falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S033, V4B-S002, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Para 3–7B e contextos curtos, reexecução ou transferência convencional podem ser alternativas suficientes.
8–14B: Em 8–14B, determine se o volume KV e concorrência justificam infraestrutura especializada.
15–30B: Contextos longos elevam bytes transferidos; ganho de computação precisa superar custos de rede e coordenação.
Requisitos de treino/runtime: Requer hardware, drivers e stack compatíveis; fonte de outro operador não confirma GPUDirect ou EFA no servidor local.
Não aplicar quando: Não presumir que conclusão da rede significa visibilidade ordenada para qualquer kernel consumidor.

## T122:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: Operações entre nós usam EFA/RDMA com seleção por topologia.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: Perfil do runtime descreve comunicação RDMA no decode, distinguindo o perfil simplificado da carga completa.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 3 de Mooncake v1 identifica Messenger baseado em (GPUDirect) RDMA para transferir blocos KV entre CPUs/GPUs. Não se generaliza a todos os backends posteriores.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: O caminho de dados usa RDMA com EFA e ConnectX compatíveis.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: O backend disponibiliza transferência RDMA entre buffers registrados, conforme suporte e configuração.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003, V4B-Q004.

## T122:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T122 → T102 [complements]
Como combinar: A Perplexity descreve RDMA/libfabric como transporte de estado em serving desagregado.
Interface: Páginas KV, metadados e confirmação de disponibilidade.
Condição: Configuração específica suporta o transporte.
Aceite proposto: Verificar conclusão antes do decode e incluir TTFT no resultado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S002. Casos: V4B-C002.

2. T122 → T118 [complements]
Como combinar: Coletivas de TP podem depender de transporte entre dispositivos.
Interface: Grupos, buffers e eventos.
Condição: Backend de comunicação habilita o caminho adequado.
Aceite proposto: Medir tempo e detectar falhas de rank sem aceitar resultados parciais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S033, V4B-S002, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não registrar ou reutilizar uma região de memória depois de liberada enquanto há operações em voo.
- Separar throughput de rede de throughput de respostas válidas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
RDMA é infraestrutura de movimentação de dados. Sua contribuição à comparação com fronteira aparece em custo e latência da solução completa, sem aumentar capacidade de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T102, T118, T120

## Fontes primárias associadas

### B-S033 — GPUDirect RDMA — Overview

[https://docs.nvidia.com/cuda/gpudirect-rdma/](https://docs.nvidia.com/cuda/gpudirect-rdma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caminho direto entre GPU e dispositivo peer; restrições de topologia PCIe e drivers.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

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

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T123 — FP8 Quantization

**Nome canônico:** FP8 Quantization  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T123  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** quantização FP8

## T123:C01 — conceito

Uso de representações de ponto flutuante de oito bits, com escalas apropriadas, para reduzir armazenamento ou acelerar operações suportadas. E4M3 e E5M2 têm compromissos diferentes de precisão e faixa dinâmica. Pesos, ativações e KV podem usar decisões independentes; FP8 não significa INT8.

Como funciona:
- Escolher formato e granularidade de escala para cada tipo de tensor.
- Converter valores com tratamento de amplitude e operações sensíveis.
- Executar kernels compatíveis e acumular em precisão adequada ao algoritmo.

## T123:C02 — aplicacao

Quando usar:
- Acelerador e runtime oferecem kernels úteis para a forma e precisão desejadas.
- Memória ou banda limita a execução e a qualidade tolera a conversão.

Quando não usar:
- Apenas converter dtype sem escalas ou sem confirmar que há execução eficiente no hardware.

Implementação proposta:
- Registrar quais tensores usam FP8 e quais permanecem em precisão superior.
- Comparar escalas calibradas e comportamento em entradas fora do conjunto de calibração.
- Avaliar custo de conversão junto da operação, não apenas throughput nominal do Tensor Core.

Aplicação LAI proposta:
Proposta LAI: avaliar FP8 por tensor e por backend; não presumir que aumentar precisão dos pesos ou reduzir precisão do KV tenha o mesmo efeito.

## T123:C03 — riscos_validacao

Armadilhas:
- Valores fora da faixa podem saturar e degradar camadas sensíveis.
- Formato, layout e escalas incompatíveis impedem intercâmbio direto entre checkpoints e runtimes.

Métricas sugeridas:
- Saturações, erro de tarefa e diferença numérica frente à referência.
- Memória, tempo de conversão e latência real sob carga.

Testes propostos:
- Testar entradas com amplitudes extremas e verificar NaN e saturação.
- Executar tarefas estruturadas e contexto longo com limiar explícito de regressão.

## T123:C04 — perguntas_proveniencia

Pergunta: FP8 é igual a INT8?
Resposta: Não. FP8 representa expoente e mantissa; INT8 usa inteiros com esquema de escala.

Pergunta: FP8 sempre reduz pela metade toda a VRAM?
Resposta: Não. Parte dos dados continua em outros formatos e existem buffers, escalas e overhead.

Pergunta: E4M3 e E5M2 são intercambiáveis?
Resposta: Não sem considerar escala, alcance e erro; os mesmos bits representam valores de forma diferente.

Pergunta: Escala global basta sempre?
Resposta: Não. Distribuições muito heterogêneas podem exigir outra granularidade, avaliada junto do custo de metadados.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T123:C05 — mecanismo_avancado

FP8 reúne formatos com compromissos diferentes entre amplitude e precisão: mais bits de expoente ampliam alcance e deixam menos bits para distinguir valores próximos. A escala conecta unidades reais aos códigos armazenados. Em delayed scaling, estatísticas anteriores orientam a próxima escala, criando dependência temporal; uma mudança brusca de amplitude pode invalidar a previsão. Essa política difere de escalas atuais ou por blocos.

Condição de contorno:
Reduzir armazenamento não garante que toda operação acumule em FP8; acumulação e conversões precisam ser identificadas separadamente.

Contrato proposto:
- Entradas: Tensor, formato, granularidade, regra de escala e precisão de acumulação.
- Saídas: Representação reduzida, escalas e indicadores de saturação ou valores não finitos.
- Estado: Histórico de máximos quando usado e identidade de cada escala.
- Invariante: Escala aplicada na leitura corresponde exatamente à usada para codificar o tensor.

Compromissos de projeto:
- Maior alcance reduz resolução numérica em um formato de oito bits.
- Escalas locais adaptam amplitude e acrescentam metadados e operações.

## T123:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar distribuições com amplitudes muito diferentes e congelar indevidamente o histórico. Esperar detecção de saturação e degradação comparada à referência, além de recuperação com a política correta.

Plano de avaliação proposto:
Plano proposto: controlar pesos e entradas, separando mudanças de formato e escala. Medir erro, saturação, memória total e tempo de conversão; avaliar treinamento e inferência em protocolos distintos, pois suas distribuições e estados diferem.

Comparações:
- T086 (distinct_from): Aplicar FP8 a KV é uma decisão sobre cache; FP8 também pode representar outros tensores.

Afirmação rastreável:
Transformer Engine documenta formatos E4M3/E5M2 e estratégias de escala que usam máximos atuais ou históricos.
Suporte: direct; fontes: B-S034
Limite: A disponibilidade de receitas na documentação não comprova suporte da instalação nem compatibilidade de todos os operadores.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T123:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou formatos e escalas FP8. Esta camada distingue quantização de pesos, ativações e KV, além de propor diagnóstico de erro por operador antes de avaliar o serviço completo.

Precisão por componente
Dizer que um modelo usa FP8 pode esconder componentes em precisões distintas. Registre formato dos pesos, ativações, cache e acumuladores separadamente. Uma operação pode armazenar em FP8 e acumular em precisão maior; outra pode converter antes de executar. A economia e o erro dependem desse caminho real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S034, V4B-S011, V3B-S003.

Calibração e mudança
Escalas escolhidas em uma distribuição podem saturar em textos com amplitudes diferentes. Monitore valores fora da faixa em amostras representativas e compare comportamento em código, números e múltiplos idiomas quando esses dados fazem parte do uso. Uma taxa média baixa pode ocultar uma camada crítica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S034, V4B-S011, V3B-S003.

Causalidade do desempenho
FP8 pode reduzir bytes e usar instruções especializadas quando hardware e kernel suportam. Se o backend cai para conversões ou kernels inadequados, menor arquivo não implica menor latência. Compare a mesma configuração de batch e contexto antes de mudar outros fatores como cache ou paralelismo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S034, V4B-S011, V3B-S003.

USO AVANÇADO — Quantização com risco localizado
Cenário: Um modelo perde qualidade em poucas categorias.
Estratégia: Compare erros por camada e por tipo de entrada; mantenha componentes sensíveis em precisão maior se o runtime permitir. Registre a política mista como parte do artefato.
Papel do modelo pequeno: Um 8–14B especializado pode preservar tarefas críticas sem exigir uma configuração uniforme.
Aceite proposto: Validar categorias afetadas e medir o custo da exceção de precisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S034, V4B-S011, V3B-S003.

USO AVANÇADO — Aumentar capacidade de serving
Cenário: A frota é limitada por tráfego ou memória.
Estratégia: Teste FP8 isoladamente, confira o kernel utilizado e depois reavalie concorrência. Inclua escalas, buffers e cache no dimensionamento.
Papel do modelo pequeno: Um 15–30B pode usar a economia para mais sessões, se qualidade e suporte forem confirmados.
Aceite proposto: Comparar respostas válidas por recurso reservado, além de throughput bruto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S034, V4B-S011, V3B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, overheads fixos podem limitar benefícios; o objetivo pode ser memória, não velocidade.
8–14B: Teste qualidade por domínio e picos de ativação, especialmente após fine-tuning.
15–30B: Distribuição entre dispositivos e precisão de coletivas podem interagir com formato local.
Requisitos de treino/runtime: Exige suporte do backend e artefato apropriado. Receitas de treino FP8 não são automaticamente quantização pós-treino equivalente.
Não aplicar quando: Não confundir FP8 com INT8 nem assumir que todo hardware executa o formato de modo nativo.

## T123:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: FP8 consta entre os formatos suportados.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020, V4B-Q025.

## T123:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T123 → T085 [complements]
Como combinar: FP8 é uma escolha concreta dentro de uma política de quantização de pesos e operações.
Interface: Formatos, escalas e precisão de acumulação.
Condição: Compatibilidade confirmada no caminho real.
Aceite proposto: Testar erro por operador e qualidade da tarefa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S034, V4B-S011, V3B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T123 → T086 [complements]
Como combinar: Quantizar KV é uma decisão separada de quantizar pesos em FP8.
Interface: Dtype e escalas de cada componente.
Condição: Experimentos isolam as intervenções.
Aceite proposto: Medir degradação em contextos longos antes de combinar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S034, V4B-S011, V3B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Detectar saturação e não finitos sem substituir silenciosamente resultados.
- Guardar metadados de calibração e versão do runtime junto ao checkpoint.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie o modelo quantizado contra sua própria referência e depois contra fronteira na tarefa. Economizar precisão não demonstra nem impede por si só desempenho especializado competitivo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T086, T092

## Fontes primárias associadas

### B-S034 — Using FP8 and FP4 with Transformer Engine

[https://nvidia.github.io/TransformerEngine/examples/fp8_primer.html](https://nvidia.github.io/TransformerEngine/examples/fp8_primer.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações FP8 E4M3/E5M2 e escalas para controlar faixa dinâmica.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

### V3B-S003 — SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models

[https://arxiv.org/abs/2211.10438](https://arxiv.org/abs/2211.10438)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reescala equivalente antes da quantização e migração de dificuldade das ativações para pesos.

Limite: Resumo consultado; equivalência da reparametrização não elimina erro de arredondamento posterior.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T124 — INT4 / W4A16 Quantization

**Nome canônico:** INT4 / W4A16 Quantization  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T124  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** weight-only INT4; pesos 4 bits ativações 16 bits

## T124:C01 — conceito

W4A16 indica, em geral, pesos representados em quatro bits e ativações em dezesseis bits. INT4 descreve o formato inteiro de quatro bits; o esquema completo também precisa especificar grupos, escalas, pontos zero e layout. Não define por si só o algoritmo usado para quantizar.

Como funciona:
- Agrupar pesos e estimar parâmetros da representação reduzida.
- Empacotar códigos de quatro bits junto dos metadados necessários.
- Usar kernel compatível para combinar pesos comprimidos e ativações de maior precisão.

## T124:C02 — aplicacao

Quando usar:
- Modelo local é limitado pela memória dos pesos ou pela banda de leitura.
- Há checkpoint e kernel suportados para o esquema exato.

Quando não usar:
- Esperar que W4A16 reduza automaticamente KV ou todas as ativações para quatro bits.

Implementação proposta:
- Guardar método de quantização, group size, simetria, dtype de cálculo e versão do formato.
- Validar calibração do domínio quando o método a utilizar.
- Medir pico de carregamento e execução, pois o arquivo final não representa toda a memória necessária.

Aplicação LAI proposta:
Proposta LAI: identificar precisamente a receita do checkpoint local antes de comparar outro INT4; mesma quantidade de bits não implica mesmo comportamento.

## T124:C03 — riscos_validacao

Armadilhas:
- Dois arquivos chamados INT4 podem ter layouts incompatíveis.
- Desquantização, escalas e operações não quantizadas reduzem o ganho frente ao cálculo ideal de 0,5 byte por peso.

Métricas sugeridas:
- Memória de pesos e memória total em execução.
- Latência por batch e acerto em tarefas que exigem números e ferramenta.

Testes propostos:
- Carregar o artefato no runtime pretendido e confirmar método detectado, sem fallback silencioso de formato.
- Comparar com referência usando tarefas de domínio e medir erros além de perplexidade.

## T124:C04 — perguntas_proveniencia

Pergunta: W4A16 significa todo o modelo em quatro bits?
Resposta: Não. O nome separa pesos e ativações; outras estruturas podem usar precisões diferentes.

Pergunta: W4A16 é sinônimo de GPTQ?
Resposta: Não. GPTQ é um método que pode produzir esse regime; outros métodos também podem fazê-lo.

Pergunta: A16 significa acumulador de dezesseis bits?
Resposta: Não necessariamente. Ativações, multiplicação e acumulação têm tipos que precisam ser inspecionados separadamente.

Pergunta: INT4 reduz também o KV?
Resposta: Não por definição. O cache pode continuar em outro dtype, exigindo orçamento independente por contexto e concorrência.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T124:C05 — mecanismo_avancado

W4A16 descreve pesos com códigos de quatro bits e ativações em dezesseis bits, sem definir sozinho escalas, zeros, agrupamento ou precisão do acumulador. Dois artefatos com esse rótulo podem exigir kernels incompatíveis. Empacotar dois códigos por byte reduz dados de pesos, mas escalas e tensores preservados elevam o tamanho real. Durante execução, descompactação e conversão precisam ser amortizadas pelo trabalho útil.

Condição de contorno:
Se um operador desquantiza todo o peso para uma cópia persistente maior, a economia de armazenamento não descreve a memória de execução.

Contrato proposto:
- Entradas: Pesos empacotados, escalas, zeros quando presentes, tamanho dos grupos e layout.
- Saídas: Operação linear com representação compatível e erro quantificado.
- Estado: Metadados por grupo, código de kernel e temporários de desquantização.
- Invariante: O leitor interpreta ordem dos códigos e parâmetros de quantização exatamente como o produtor.

Compromissos de projeto:
- Menos tráfego de pesos pode favorecer decode limitado por memória.
- Prefill com muitas ativações pode ter outro gargalo e outra vantagem relativa.

## T124:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: carregar códigos corretos com escala de grupo deslocada e comparar com desquantização de referência. Esperar divergência detectável antes de avaliar qualidade final.

Plano de avaliação proposto:
Plano proposto: comparar FP16/BF16 e W4A16 do mesmo checkpoint, distinguindo arquivo, memória residente e temporários. Medir prefill, decode e qualidade em domínios representativos; aprovar o compromisso apenas no backend que realmente executará o artefato.

Comparações:
- T125 (distinct_from): GPTQ é um algoritmo de quantização de pesos; W4A16 especifica precisões, não o procedimento de obtenção.

Afirmação rastreável:
O texto de AWQ distingue weight-only de baixa precisão, incluindo W4A16, da quantização simultânea de pesos e ativações.
Suporte: direct; fontes: V3B-S014
Limite: O rótulo não garante equivalência entre formatos de arquivo ou implementações de kernel.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T124:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu o contrato W4A16. O aprofundamento trata quantização mista, escolhas de kernel por lote e o processo de entrega de um artefato que precisa continuar interpretável entre ferramentas.

Quatro bits não em tudo
Uma política pode quantizar matrizes grandes e preservar embeddings, normalizações ou projeções sensíveis. Calcule tamanho real e descreva exceções. O rótulo W4 não basta para reproduzir o modelo; grupos, zeros, escalas, ordem de canais e tensores preservados precisam acompanhar os códigos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S046, V3B-S014, V4B-S011, V4D-S009.

Regime de execução
Desempacotar e desquantizar pode ser amortizado de forma diferente em prefill e decode. Um kernel favorável a lote pequeno pode perder vantagem em multiplicações maiores. Valide variantes no workload esperado e não transfira números entre CPU, GPU e NPU; o blog Phi Silica descreve uma receita própria, não uma garantia universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S046, V3B-S014, V4B-S011, V4D-S009.

Cadeia de artefatos
O produtor de pesos e o consumidor precisam concordar sobre layout e semântica. Faça uma inspeção de metadados e teste uma camada isolada antes de carregar o modelo inteiro. Uma conversão que muda agrupamento ou ordem requer transformação explícita, não apenas renomear o arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S046, V3B-S014, V4B-S011, V4D-S009.

USO AVANÇADO — Distribuição local especializada
Cenário: Um modelo precisa caber num orçamento de memória limitado.
Estratégia: Escolha formato suportado, calibre com dados representativos e teste tarefas críticas. Meça memória total com contexto e servidor, além do tamanho em disco.
Papel do modelo pequeno: Um 3–7B pode atender tarefas locais com evidência externa e validação determinística.
Aceite proposto: Aceitar somente se a economia física e a qualidade forem medidas no ambiente real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S046, V3B-S014, V4B-S011, V4D-S009.

USO AVANÇADO — Comparar W4 e precisão maior
Cenário: Há capacidade para várias configurações.
Estratégia: Fixe checkpoint, prompts e política de geração; compare erro, prefill e decode separadamente. Depois avalie se a memória liberada permite mais sessões úteis.
Papel do modelo pequeno: Um 15–30B pode trocar precisão por capacidade, mas isso exige decisão de produto mensurada.
Aceite proposto: Relatar falhas por categoria e custo de respostas completas, não só tokens por segundo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S046, V3B-S014, V4B-S011, V4D-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: O ganho mais claro pode ser viabilidade de carregamento, sem aceleração garantida.
8–14B: Verifique kernels para formas reais e efeitos de contexto longo na memória total.
15–30B: Inclua réplicas, escalas e buffers temporários ao dimensionar modelos maiores.
Requisitos de treino/runtime: Quantização pós-treino ou treinamento específico conforme método; W4A16 é uma descrição de precisões, não uma receita única.
Não aplicar quando: Não atribuir o mesmo comportamento a artefatos GPTQ, AWQ e GGUF apenas porque usam quatro bits.

## T124:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: INT4/AWQ consta no conjunto de otimizações.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006, V4B-Q025.

## T124:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T124 → T125 [alternative]
Como combinar: GPTQ é uma possível forma de produzir pesos de baixa precisão com reconstrução calibrada.
Interface: Pesos, grupos e metadados.
Condição: Runtime entende o formato gerado.
Aceite proposto: Comparar qualidade e execução com outras receitas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S046, V3B-S014, V4B-S011, V4D-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T124 → T126 [alternative]
Como combinar: AWQ usa informação das ativações para proteger canais relevantes antes de quantizar.
Interface: Escalas e transformações associadas.
Condição: Compensações preservadas na exportação.
Aceite proposto: Validar camadas e tarefas após conversão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S046, V3B-S014, V4B-S011, V4D-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não estimar VRAM como parâmetros multiplicados por meio byte sem demais componentes.
- Testar entradas fora da calibração, inclusive idiomas e formatos relevantes ao produto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare especialização e economia junto com a perda introduzida pela quantização. Um modelo que cabe em menos memória não adquiriu capacidade adicional por esse motivo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T125, T126, T127

## Fontes primárias associadas

### B-S046 — INT4 W4A16

[https://github.com/vllm-project/vllm/blob/main/docs/features/quantization/llm_compressor/int4.md](https://github.com/vllm-project/vllm/blob/main/docs/features/quantization/llm_compressor/int4.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesos em quatro bits e ativações em dezesseis; receita exige calibração e formato compatível.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S014 — AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration — full text

[https://arxiv.org/html/2306.00978v6](https://arxiv.org/html/2306.00978v6)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por canal baseado em ativações, quantização weight-only e distinção de mixed precision.

Limite: Texto consultado na revisão v6 disponível em 2026-11-05; nenhuma versão de servidor foi presumida.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T125 — GPTQ

**Nome canônico:** GPTQ  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T125  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** post-training weight quantization GPTQ

## T125:C01 — conceito

Método de quantização de pesos após treinamento que usa informação aproximada de segunda ordem para controlar o erro introduzido na conversão. É um algoritmo, distinto de bibliotecas e formatos que o implementam. Exige considerar calibração e compatibilidade do artefato com o kernel de inferência.

Como funciona:
- Observar entradas representativas das camadas para estimar sensibilidade.
- Quantizar grupos de pesos com compensação do erro no procedimento escolhido.
- Salvar os pesos empacotados e metadados requeridos pelo runtime.

## T125:C02 — aplicacao

Quando usar:
- Há modelo de referência e necessidade de reduzir armazenamento de pesos.
- Existe implementação GPTQ mantida e compatível com o modelo/hardware.

Quando não usar:
- Utilizar apenas o nome GPTQ como garantia de qualidade ou de compatibilidade entre ferramentas.

Implementação proposta:
- Separar conjunto de calibração e avaliação, mantendo textos e tarefas representativos.
- Registrar bits, group size, ordenação e demais parâmetros da implementação.
- Comparar com outro método sob memória, runtime e conjunto de tarefas equivalentes.

Aplicação LAI proposta:
Proposta LAI: comparar GPTQ e a receita já usada no modelo local com dados reais de tarefa e custo de fallback; não escolher pela sigla.

## T125:C03 — riscos_validacao

Armadilhas:
- Calibração estreita pode favorecer um domínio e degradar outro.
- Diferenças de layout e versão podem impedir carregamento mesmo com o mesmo número de bits.

Métricas sugeridas:
- Erro de tarefa, tamanho dos pesos e memória máxima.
- Tempo por token e custo de quantização, registrados separadamente.

Testes propostos:
- Validar o checkpoint quantizado no runtime de destino e comparar saídas em casos de ferramenta e extração.
- Avaliar dados fora da calibração para detectar deterioração que uma avaliação sobre os mesmos textos esconderia.

## T125:C04 — perguntas_proveniencia

Pergunta: GPTQ é um modelo?
Resposta: Não. É um método para reduzir precisão dos pesos de um modelo já treinado.

Pergunta: O resultado mantém todas as habilidades?
Resposta: Não há garantia universal; depende do checkpoint, calibração, configuração e avaliação do domínio.

Pergunta: Por que magnitude do peso não basta?
Resposta: O efeito do erro depende de quais entradas o multiplicam e de suas correlações.

Pergunta: PTQ significa nenhum dado?
Resposta: Não. O método pode dispensar treino por gradientes do modelo completo e ainda exigir ativações representativas para calibração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T125:C05 — mecanismo_avancado

O objetivo de reconstrução por camada pondera erro de pesos pelas entradas observadas: minimizar uma expressão como ||WX−WqX||² difere de minimizar apenas ||W−Wq||². A aproximação de curvatura depende de XXᵀ, portanto correlações da calibração influenciam compensações. O procedimento atualiza pesos ainda não quantizados para absorver parte do erro introduzido, exigindo estabilidade numérica na representação da informação de segunda ordem.

Condição de contorno:
Calibração estreita pode preservar bem suas ativações e representar mal entradas com correlações diferentes.

Contrato proposto:
- Entradas: Pesos da camada, ativações de calibração, agrupamento e estabilização numérica.
- Saídas: Pesos quantizados com metadados e erro de reconstrução registrado.
- Estado: Informação aproximada de curvatura, ordem de processamento e compensações pendentes.
- Invariante: A compensação usa estatísticas correspondentes à camada e às entradas realmente calibradas.

Compromissos de projeto:
- Calibração mais diversa custa coleta e pode melhorar cobertura.
- Aproximação de segunda ordem adiciona trabalho offline e não remove erro de quantização.

## T125:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: calibrar em entradas quase colineares e avaliar um domínio com outras correlações. Verificar estabilidade da fatoração, erro de reconstrução e degradação fora da amostra.

Plano de avaliação proposto:
Plano proposto: comparar arredondamento simples e GPTQ com mesmo orçamento de bits, grupos e dados. Separar erro local, qualidade final e custo de conversão; aceitar pelo conjunto de validação independente e pelo kernel de destino.

Comparações:
- T126 (alternative): AWQ orienta reescala por ativações; GPTQ usa compensações ligadas à reconstrução de camada.

Afirmação rastreável:
O GPTQ utiliza informação aproximada de segunda ordem e atualiza pesos restantes durante a quantização.
Suporte: direct; fontes: V3B-S013
Limite: A qualidade de reconstrução em uma camada não garante desempenho de toda tarefa ou de domínios não vistos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T125:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou reconstrução ponderada por ativações. Esta camada trata curadoria de calibração, composição dos erros entre camadas e rastreabilidade de escolhas numéricas.

Calibração por comportamento
Selecione exemplos que representem tarefas, formatos e comprimentos reais, sem contaminar avaliação. Uma coleção genérica pode deixar módulos pouco exercitados no domínio. Registre tokens processados e distribuição por categoria; quantidade de exemplos não informa sozinha a cobertura de ativações relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

Erro que se propaga
Baixo erro local de reconstrução não garante baixo erro na saída final. Camadas quantizadas alteram entradas das seguintes, e avaliação autoregressiva acumula diferenças nas continuações. Compare reconstrução por camada, logits e tarefas completas; nenhuma dessas medidas substitui as outras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

Estabilidade e escolhas
Agrupamento, ordem de processamento e estabilização influenciam o artefato. Preserve parâmetros e logs, incluindo falhas de fatoração ou fallback. Ajustar esses valores para melhorar um conjunto pequeno de testes pode gerar sobreajuste do processo de quantização; reserve uma validação independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

USO AVANÇADO — Modelo de domínio numérico
Cenário: Pequenos erros afetam respostas estruturadas ou cálculo.
Estratégia: Calibre com dados de formato semelhante e use ferramentas externas para verificar resultados. Examine categorias sensíveis antes de decidir se certas camadas ficam em precisão maior.
Papel do modelo pequeno: Um 8–14B pode continuar útil quando cálculo e validação são delegados a ferramentas.
Aceite proposto: Comparar taxa de erro por categoria com referência de maior precisão e com o mesmo verificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

USO AVANÇADO — Pipeline reproduzível de distribuição
Cenário: Várias versões do modelo serão quantizadas.
Estratégia: Versione base, calibração, parâmetros, código e formato de saída. Automatize inspeção de metadados e teste de carregamento; aprove cada versão com uma avaliação separada.
Papel do modelo pequeno: Modelos 3–7B permitem ciclos de validação rápidos, sem dispensar cobertura de casos críticos.
Aceite proposto: Reproduzir artefatos ou explicar diferenças com manifests completos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: A economia pode facilitar implantação local; avalie se o processo de calibração compensa o objetivo.
8–14B: Mantenha variedade de tarefas e comprimentos; um único domínio textual estreito pode esconder perdas.
15–30B: Quantização de 15–30B exige recursos para calibração e buffers, não somente para o arquivo final.
Requisitos de treino/runtime: Método pós-treino com dados de calibração e runtime compatível. A menção no Phi Silica não fixa uma receita aplicável a outro modelo.
Não aplicar quando: Não usar métricas de reconstrução como prova de correção factual ou de compatibilidade de kernel.

## T125:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Implementação publicada usa GPTQ em pesos rotacionados; não afirmar que todo backend atual é idêntico. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006.

## T125:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T125 → T124 [feeds]
Como combinar: GPTQ pode gerar uma representação de pesos de quatro bits com metadados próprios.
Interface: Códigos, escalas, grupos e layout.
Condição: Consumidor implementa a representação específica.
Aceite proposto: Conferir saída de camadas após exportação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S013, V4D-S009, B-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T125 → T198 [complements]
Como combinar: Perdas de quantização podem alterar calibração de confiança e precisam de nova medição.
Interface: Predições e resultados rotulados por versão.
Condição: Conjunto independente do usado para calibrar pesos.
Aceite proposto: Comparar confiabilidade por faixa sem presumir preservação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S013, V4D-S009, B-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter conjunto de avaliação fora da calibração e da escolha de hiperparâmetros.
- Registrar exceções de precisão e fallback para não rotular artefatos diferentes como idênticos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação correta primeiro mede a diferença causada por GPTQ e depois a adequação à tarefa frente a fronteira. Um bom erro de reconstrução não estabelece equivalência de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T124, T126

## Fontes primárias associadas

### B-S035 — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

[https://arxiv.org/abs/2210.17323](https://arxiv.org/abs/2210.17323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quantização de pesos pós-treino usando aproximação de informação de segunda ordem.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S013 — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers — full text

[https://arxiv.org/html/2210.17323v2](https://arxiv.org/html/2210.17323v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetivo quadrático de reconstrução por camada, Hessiana aproximada, compensação de erro e estabilidade.

Limite: Seções metodológicas consultadas; calibração e resultados publicados não validam checkpoints locais.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T126 — AWQ

**Nome canônico:** AWQ  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T126  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Activation-aware Weight Quantization

## T126:C01 — conceito

Activation-aware Weight Quantization é um método de quantização de pesos que usa estatísticas de ativações para identificar canais importantes e escolher escalas. O objetivo é reduzir erro de baixa precisão. O nome não significa quantizar as ativações nem manter obrigatoriamente uma fração dos pesos em FP16.

Como funciona:
- Coletar estatísticas de ativação com exemplos representativos.
- Escolher transformações e escalas que protejam canais relevantes.
- Produzir pesos quantizados e metadados para kernels compatíveis.

## T126:C02 — aplicacao

Quando usar:
- É necessário reduzir pesos mantendo qualidade de modelos instruídos.
- O runtime suporta a variante e o layout de checkpoint AWQ escolhidos.

Quando não usar:
- Usar a existência de um arquivo AWQ como prova de que o hardware executará seu kernel eficientemente.

Implementação proposta:
- Registrar revisão do modelo e dados usados para calibração.
- Inspecionar quais camadas foram convertidas e quais foram preservadas.
- Comparar AWQ, GPTQ e referência com o mesmo tokenizer, template e tarefas.

Aplicação LAI proposta:
Proposta LAI: avaliar uma versão AWQ somente contra baseline reproduzível do modelo local, considerando qualidade e memória suficientes para KV.

## T126:C03 — riscos_validacao

Armadilhas:
- Nome igual pode encobrir empacotamento diferente entre bibliotecas.
- Bom resultado em texto genérico pode não representar ferramentas, código ou termos do domínio.

Métricas sugeridas:
- Taxa de acerto por tarefa e memória total em execução.
- Tempo por token, throughput por batch e custo de conversões adicionais.

Testes propostos:
- Executar casos de saída estruturada e uso de ferramentas fora do conjunto de calibração.
- Confirmar carregamento no backend pretendido e registrar qual kernel foi efetivamente selecionado.

## T126:C04 — perguntas_proveniencia

Pergunta: Activation-aware significa que as ativações são INT4?
Resposta: Não. As ativações orientam a quantização dos pesos; o regime numérico completo precisa ser especificado.

Pergunta: AWQ substitui fine-tuning?
Resposta: Não. Comprime um modelo existente; não ensina por si só um novo procedimento.

Pergunta: Activation-aware quantiza as ativações?
Resposta: O nome descreve informação usada para quantizar pesos; a variante weight-only pode manter ativações em maior precisão.

Pergunta: Escala equivalente garante saída idêntica?
Resposta: A equivalência é anterior ao arredondamento; quantização e aritmética finita ainda alteram a operação.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T126:C05 — mecanismo_avancado

Proteger canais salientes por reescala não significa manter obrigatoriamente uma fração dos pesos em FP16. A transformação redistribui amplitude entre pesos e entradas preservando a operação antes do arredondamento; depois, a grade quantizada introduz erro. A saliência depende das ativações observadas, portanto um canal de peso numericamente pequeno pode ser importante quando multiplicado por entradas grandes.

Condição de contorno:
Mudar domínio ou modalidade pode alterar quais canais são salientes; ausência de backpropagation não elimina essa dependência estatística.

Contrato proposto:
- Entradas: Pesos, estatísticas de ativações, grupos e busca de escalas definida.
- Saídas: Pesos quantizados e transformações necessárias para executar a operação compatível.
- Estado: Escalas por canal, agrupamento e proveniência dos exemplos de calibração.
- Invariante: A compensação de escala permanece consistente entre pesos e operações associadas.

Compromissos de projeto:
- Reescala melhora resolução de canais escolhidos e pode deslocar erro para outros.
- Grades compatíveis com kernels favorecem execução e limitam liberdade de representação.

## T126:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: omitir a transformação compensatória ao carregar o artefato e trocar o domínio de entrada. Esperar detecção separada do erro de integração e da perda de generalização.

Plano de avaliação proposto:
Plano proposto: comparar quantização ingênua e AWQ no mesmo checkpoint e formato, incluindo dados fora da calibração. Medir erro de camada, qualidade, memória e tempo real; não atribuir ganho do kernel exclusivamente ao método de escalas.

Comparações:
- T125 (alternative): A escolha entre AWQ e GPTQ envolve diferentes objetivos de calibração e caminhos de execução.

Afirmação rastreável:
O AWQ usa estatísticas de ativações para escolher reescala de canais, evitando exigir uma representação mista dos pesos protegidos.
Suporte: direct; fontes: V3B-S014
Limite: Resultados publicados não eliminam a necessidade de avaliar a distribuição de uso e o empacotamento do servidor.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T126:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou reescala e saliência por ativações. O aprofundamento considera mudanças após adaptação, escolha entre métodos e verificação da exportação como parte da validade do resultado.

Saliência dependente do uso
Canais relevantes numa distribuição podem mudar com domínio, idioma ou fine-tuning. Se adapters alteram ativações, quantizar antes ou depois da adaptação não precisa produzir o mesmo comportamento. Trate ordem das operações como escolha experimental e registre qual combinação foi efetivamente avaliada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S014, B-S036, V4B-S011.

Busca de escalas e critério
A reescala preserva a operação antes do arredondamento, mas a busca procura uma boa distribuição de erro depois da quantização. Verifique a métrica usada e sua relação com a tarefa. Melhor reconstrução numa amostra não garante melhor geração, sobretudo quando a resposta exige detalhes raros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S014, B-S036, V4B-S011.

Entrega do modelo
As transformações de escala devem ser incorporadas ou executadas consistentemente. Exportações entre backends podem alterar fusões, layout e kernels. Faça comparação camada a camada em entradas controladas e confirme que o servidor carrega o artefato pretendido, sem fallback silencioso para outra precisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S014, B-S036, V4B-S011.

USO AVANÇADO — Assistente especializado com adapter
Cenário: A base será adaptada e distribuída em memória limitada.
Estratégia: Compare base quantizada com adapter separado e modelo adaptado seguido de quantização, quando as ferramentas suportarem ambas as rotas. Preserve dados de avaliação independentes.
Papel do modelo pequeno: Um 8–14B pode combinar especialização e economia, mas a composição precisa ser medida.
Aceite proposto: Verificar tarefa, retenção de capacidades e pico de memória em cada rota.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S014, B-S036, V4B-S011.

USO AVANÇADO — Seleção entre receitas de quatro bits
Cenário: Há opções GPTQ, AWQ e formatos distintos.
Estratégia: Use o mesmo checkpoint e orçamento de avaliação. Separe diferença de método de diferença de kernel, reportando qualidade e desempenho de ambos os componentes.
Papel do modelo pequeno: Um 15–30B pode ganhar viabilidade de serving sem uma receita universalmente superior.
Aceite proposto: Escolher pelo serviço completo e por falhas toleráveis, não por um ranking genérico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S014, B-S036, V4B-S011.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma implementação suportada e bem validada pode ser mais útil que otimizações adicionais de escala.
8–14B: Avalie reescala com prompts representativos e efeitos dos adapters de domínio.
15–30B: Medições devem incluir custo de carregar e manter múltiplas variantes, além do arquivo quantizado.
Requisitos de treino/runtime: Quantização pós-treino guiada por ativações; suporte anunciado por TensorRT-LLM não comprova configuração local.
Não aplicar quando: Não afirmar que AWQ mantém necessariamente uma porcentagem fixa de pesos em FP16.

## T126:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q025.

## T126:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T126 → T182 [complements]
Como combinar: Adapters podem mudar a distribuição que orientou a quantização.
Interface: Base, adapter, ordem de aplicação e escalas.
Condição: Ferramentas suportam a composição específica.
Aceite proposto: Comparar qualidade e ativações antes e depois da adaptação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S014, B-S036, V4B-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T126 → T124 [feeds]
Como combinar: AWQ produz uma política concreta de baixa precisão que exige metadados e kernels adequados.
Interface: Pesos, grupos e reescalas.
Condição: Exportador e runtime concordam.
Aceite proposto: Comparar camada de referência e medição física de memória.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S014, B-S036, V4B-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar atribuir ganho de kernel ao algoritmo de quantização sem ablação.
- Não reutilizar calibração antiga automaticamente depois de mudar domínio ou pesos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a versão AWQ com a base e com um serviço de fronteira na tarefa específica. Qualidade preservada em um domínio não comprova ausência de perdas em todos os tipos de pergunta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T124, T125

## Fontes primárias associadas

### B-S036 — AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration

[https://arxiv.org/abs/2306.00978](https://arxiv.org/abs/2306.00978)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estatísticas de ativações orientam escalas para proteger canais relevantes na quantização de pesos.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S014 — AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration — full text

[https://arxiv.org/html/2306.00978v6](https://arxiv.org/html/2306.00978v6)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Escalonamento por canal baseado em ativações, quantização weight-only e distinção de mixed precision.

Limite: Texto consultado na revisão v6 disponível em 2026-11-05; nenhuma versão de servidor foi presumida.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T127 — GGUF — formato de modelos, não método único de quantização

**Nome canônico:** GGUF — contêiner binário de modelos  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** format  
**Estado da evidência:** Correção terminológica do inventário original  
**ID canônico:** T127  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** GGUF / formatos de quantização; GGUF; formato GGUF; GGUF não é algoritmo de quantização

## T127:C01 — conceito

GGUF é um formato binário para armazenar modelos destinados à inferência em executores compatíveis com GGML. Reúne tensores e metadados e pode conter diferentes tipos numéricos, inclusive representações não quantizadas. A extensão do arquivo identifica o contêiner; não identifica sozinha um único método de quantização, sua qualidade ou a velocidade de execução.

Como funciona:
- Converter arquitetura, nomes e formas dos tensores e metadados necessários para o formato aceito pelo executor.
- Registrar tipos de tensor e informações como tokenizer e configuração do modelo.
- Carregar os dados com suporte aos tipos numéricos e à arquitetura presentes no arquivo.

## T127:C02 — aplicacao

Quando usar:
- Distribuição e execução local em ambientes compatíveis, especialmente quando carregamento, metadados e opções de representação precisam acompanhar o artefato.

Quando não usar:
- Como garantia de que qualquer modelo será aceito ou que todos os tensores usam a mesma precisão.

Implementação proposta:
- Proposta: registrar checkpoint de origem, revisão, conversor, versão do executor e hash do GGUF produzido.
- Inspecionar tipos por tensor e metadados; distinguir tamanho do arquivo, memória residente e memória de contexto durante geração.
- Comparar uma versão de referência e uma quantizada no mesmo conjunto de tarefas, com tokenizer e chat template corretos.
- Verificar suporte da combinação arquitetura/tipo/backend antes de decidir a distribuição; manter o artefato de referência para reproduzir diferenças.

Aplicação LAI proposta:
Proposta LAI: tratar cada GGUF como artefato versionado de modelo, com rastreabilidade e avaliação próprias, sem declarar que a mera conversão produziu compressão ou melhoria.

## T127:C03 — riscos_validacao

Armadilhas:
- Usar o nome comercial de uma quantização como se descrevesse integralmente todos os tensores.
- Atribuir erros de template ou tokenizer à quantização, sem isolar a causa.

Métricas sugeridas:
- Tamanho em disco, tempo de carga, memória de execução, throughput e diferença de qualidade frente à referência.

Testes propostos:
- Teste proposto: conferir magic/header e metadados com ferramenta compatível; carregar no executor de destino e gerar com entradas conhecidas.
- Testar texto multilíngue, tokens especiais e contexto longo, separando incompatibilidade de arquivo de degradação numérica.

## T127:C04 — perguntas_proveniencia

Pergunta: Todo arquivo GGUF é quantizado em quatro bits?
Resposta: Não. GGUF admite múltiplas representações e pode armazenar tensores sem quantização de quatro bits.

Pergunta: Dois GGUF do mesmo modelo têm desempenho equivalente?
Resposta: Não necessariamente. Tipos de tensor, conversão, template, revisão e kernels do executor podem mudar memória, velocidade e qualidade.

Pergunta: Extensão .gguf prova que foi quantizado?
Resposta: Não. É necessário inspecionar os tipos dos tensores e o histórico de conversão.

Pergunta: Um hash correto prova conversão correta?
Resposta: Prova integridade do arquivo identificado, não que pesos, tokenizer e metadados correspondam semanticamente ao modelo pretendido.

Escopo das fontes:
A especificação oficial sustenta formato e metadados. O protocolo de comparação e a aplicação são propostas editoriais.

## T127:C05 — mecanismo_avancado

O contêiner precisa preservar mais que valores numéricos: nomes, dimensões, tipos, offsets e metadados da arquitetura determinam como os bytes viram operações. Na especificação GGUF, offsets de tensores são relativos à região de dados e obedecem ao alinhamento declarado. Interpretar o offset como relativo ao começo do arquivo é um erro de leitura, mesmo quando o cabeçalho parece válido.

Condição de contorno:
Um arquivo estruturalmente válido pode representar arquitetura, tokenizer ou tipo de tensor que o executor não suporta.

Contrato proposto:
- Entradas: Arquivo, versão de estrutura reconhecida, descritores de tensor e capacidades do leitor.
- Saídas: Inventário validado e modelo carregado com interpretação explícita dos metadados.
- Estado: Mapa de regiões, alinhamento, tokenizer e tipos por tensor.
- Invariante: Nenhuma dimensão, offset ou tamanho leva a leitura fora da região válida.

Compromissos de projeto:
- Metadados autocontidos facilitam transporte e exigem compatibilidade semântica do leitor.
- Tipos mistos podem melhorar qualidade e tornam inadequada uma única estimativa de bits por parâmetro.

## T127:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar alinhamento, truncar dados e deslocar um offset mantendo o cabeçalho legível. Esperar rejeição estrutural antes da inferência; testar tokenizer incompatível em etapa separada.

Plano de avaliação proposto:
Plano proposto: validar integridade e formas, depois comparar tokenização e logits com o artefato de origem sob transformação documentada. Medir tamanho por tipo de tensor e desempenho no executor real; distinguir erro de conversão de erro de quantização.

Comparações:
- T124 (distinct_from): W4A16 descreve uma escolha numérica; GGUF organiza dados e metadados de diversas representações.

Afirmação rastreável:
A especificação GGUF define alinhamento global e offsets relativos ao início da região de dados dos tensores.
Suporte: direct; fontes: B-S037
Limite: O formato não certifica qualidade, compatibilidade universal ou um método único de quantização.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T127:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou estrutura e offsets do contêiner. A nova camada aborda proveniência do artefato, paridade de tokenização e controle de mudanças entre conversão, quantização e carregamento.

Manifesto de origem
Um arquivo válido pode conter pesos de origem diferente da esperada. Associe hash, checkpoint base, licença aplicável, ferramenta de conversão e política de quantização. A inspeção do cabeçalho verifica estrutura; não prova autoria, qualidade nem correspondência com uma versão anunciada pelo nome do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

Template como parte do comportamento
Tokenizer, tokens especiais e template de chat afetam a entrada efetivamente vista pelo modelo. Compare sequências de token IDs produzidas no caminho original e no consumidor GGUF. Uma migração pode parecer perda de quantização quando o erro real é duplicação de marcadores, papel de mensagens ou encerramento incorreto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

Compatibilidade evolutiva
Uma versão do contêiner e um tipo de tensor reconhecidos não garantem suporte à arquitetura inteira. Verifique tipos de camada, posições e recursos exigidos pelo checkpoint. O carregador deve rejeitar uma interpretação desconhecida em vez de assumir defaults que produzem respostas plausíveis e incorretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

USO AVANÇADO — Pacote local reproduzível
Cenário: Um modelo será distribuído para execução offline.
Estratégia: Entregue manifesto, configuração de chat, exemplos mínimos e verificações de integridade. Valide o carregamento no build escolhido e meça memória com contexto real.
Papel do modelo pequeno: Um 3–7B pode oferecer extração ou classificação local com contratos explícitos.
Aceite proposto: Reproduzir tokenização e respostas de controle sem depender do nome comercial do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

USO AVANÇADO — Comparação de quantizações
Cenário: Vários arquivos GGUF representam o mesmo checkpoint.
Estratégia: Inspecione tipos por tensor e metadados antes de comparar. Fixe runtime, template e geração; diferencie ganho do método de ganho do backend.
Papel do modelo pequeno: Um 8–14B pode ser selecionado conforme orçamento de RAM/VRAM e qualidade medida.
Aceite proposto: Relatar tamanho, memória em execução e erros por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Boa faixa para prototipação local, sujeita ao suporte da arquitetura e ao contexto desejado.
8–14B: CPU/GPU offload e precisão mista precisam de medição no dispositivo real.
15–30B: Arquivos de 15–30B podem caber em armazenamento sem caber no orçamento de execução; incluir KV e buffers.
Requisitos de treino/runtime: GGUF é contêiner, não método único. Conversão de formato e quantização são operações distintas.
Não aplicar quando: Não interpretar extensão .gguf como prova de compatibilidade, segurança ou ausência de perda numérica.

## T127:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C024 — Projeto llama.cpp / llama.cpp server
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.
Mecanismo documentado: Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.
Correspondência com esta base: GGUF é o contêiner consumido.
Transferência proposta para modelo pequeno: Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.
Limite: README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.
Fontes: V3D-S012, B-S037.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de uso de llama.cpp/GGUF consultada. A documentação comprova recursos; não foi confirmado nesta pesquisa um caso específico novo de implantação de bigtech para cada método de quantização.
Consultas registradas: V4B-Q026.

## T127:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T127 → R024 [requires]
Como combinar: llama.cpp é um consumidor relevante de GGUF, com suporte específico por build.
Interface: Arquivo, arquitetura e parâmetros de carregamento.
Condição: Leitor reconhece todos os componentes usados.
Aceite proposto: Executar validação de carregamento e tokenização.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S037, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T127 → T124 [complements]
Como combinar: Alguns tensores podem usar quatro bits, mas o formato permite várias políticas.
Interface: Tipos por tensor e metadados de quantização.
Condição: Comparação identifica a receita concreta.
Aceite proposto: Medir qualidade e memória, sem chamar todo GGUF de W4A16.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S037, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar hashes antes de carregar artefatos transferidos.
- Não ocultar perda de tokenizer ou template sob uma comparação genérica de modelos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a solução local completa com fronteira numa tarefa delimitada. Um formato portátil facilita entrega; não demonstra competência nem torna quantizações diferentes equivalentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T124, T125, P009

## Fontes primárias associadas

### B-S037 — GGUF specification

[https://github.com/ggml-org/ggml/blob/master/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formato binário de modelos, tensores e metadados; não é por si só um algoritmo de quantização.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S012 — llama.cpp HTTP server — README

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor com caminhos CPU/GPU, geração paralela e batching contínuo.

Limite: Arquivo master; recursos dependem do build, backend e arquitetura do modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T128 — EAGLE / EAGLE-3

**Nome canônico:** EAGLE / EAGLE-3  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T128  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** EAGLE; EAGLE-3

## T128:C01 — conceito

Família de métodos de especulação com componente auxiliar treinado e acesso a características do modelo alvo. EAGLE original trabalha com predição de características; EAGLE-3 usa fusão de características de múltiplas camadas para predizer tokens diretamente. Versões e checkpoints auxiliares não são intercambiáveis por nome.

Como funciona:
- Obter características do alvo no formato esperado pelo componente auxiliar.
- Gerar candidatos usando o módulo treinado para aquela configuração.
- Verificar candidatos no alvo conforme o algoritmo e modo de amostragem suportados.

## T128:C02 — aplicacao

Quando usar:
- Há draft compatível com o checkpoint alvo e workload favorável.
- Ganho de decode compensa memória e processamento adicionais.

Quando não usar:
- Usar qualquer draft EAGLE com um alvo diferente sem evidência de compatibilidade e avaliação.

Implementação proposta:
- Fixar revisões de alvo, draft, tokenizer e runtime.
- Medir aceitação por domínio e custo total, incluindo extração de características.
- Avaliar baixa e alta concorrência para identificar quando desativar o recurso.

Aplicação LAI proposta:
Proposta LAI: testar apenas se existir draft compatível com o Qwen escolhido; caso contrário, começar por métodos sem modelo auxiliar.

## T128:C03 — riscos_validacao

Armadilhas:
- Resultados publicados em outro hardware não predizem o ganho local.
- Alterar pesos ou LoRA do alvo pode reduzir concordância ou quebrar premissas do draft.

Métricas sugeridas:
- Tokens aceitos por verificação, custo do auxiliar e VRAM adicional.
- Latência p95 e throughput com o mesmo orçamento de recursos.

Testes propostos:
- Comparar distribuição ou comportamento conforme a garantia declarada do modo implementado.
- Testar incompatibilidade de revisão e exigir bloqueio ou diagnóstico antes de gerar resultados inválidos.

## T128:C04 — perguntas_proveniencia

Pergunta: EAGLE-3 é apenas trocar uma flag de EAGLE?
Resposta: Não. A versão muda o método do auxiliar e requer pesos e suporte correspondentes.

Pergunta: O draft substitui o modelo alvo?
Resposta: Não. Produz candidatos; a verificação do alvo continua sendo parte central.

Pergunta: Treinar um bom proponente garante exatidão?
Resposta: Não. A garantia de distribuição depende também do algoritmo de aceitação e do tratamento de rejeições.

Pergunta: Pode reutilizar após fine-tuning do alvo?
Resposta: É necessário validar compatibilidade e concordância; pesos alterados podem mudar as características que o auxiliar aprendeu a consumir.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T128:C05 — mecanismo_avancado

As variantes EAGLE não devem ser descritas como um mecanismo imutável: o artigo EAGLE-3 distingue sua predição direta de tokens da restrição anterior de prever características, usando fusão de características de várias camadas. Isso torna a interface entre alvo e módulo auxiliar parte do artefato treinado. Alterar camadas de origem, dimensões ou normalização pode quebrar o proponente mesmo quando seu arquivo carrega.

Condição de contorno:
Aceleração depende da qualidade das propostas e do custo do caminho integrado, não apenas de adicionar um módulo auxiliar.

Contrato proposto:
- Entradas: Alvo identificado, módulo auxiliar compatível, características esperadas e política de verificação.
- Saídas: Candidatos e tokens confirmados com contagem de aceitação.
- Estado: Estados do proponente, seleção de características e cache provisório.
- Invariante: Somente a verificação correta do alvo autoriza confirmar candidatos no histórico.

Compromissos de projeto:
- Treinar proponente especializado pode elevar concordância e aumenta preparação e manutenção.
- Acoplar características reduz portabilidade entre checkpoints e implementações.

## T128:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o checkpoint alvo por outro de mesma dimensão ou permutar camadas de características. Esperar falha de compatibilidade ou queda detectada de aceitação, sem assumir que shapes iguais bastam.

Plano de avaliação proposto:
Plano proposto: comparar alvo sozinho e proponente compatível sob mesmos prompts, lotes e amostragem. Medir custo de características, propostas e verificação, além de distribuição de saída; aprovar somente aceleração observada e sem alteração indevida da regra de aceitação.

Comparações:
- T132 (alternative): O proponente integrado usa características do alvo, enquanto um draft externo pode produzir propostas independentemente.

Afirmação rastreável:
EAGLE-3 abandona a restrição de predição de características em favor de tokens e combina características de múltiplas camadas.
Suporte: direct; fontes: B-S038
Limite: A fonte descreve a variante publicada; não confirma suporte no checkpoint ou hardware do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T128:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou a interface de características do EAGLE-3. Esta camada trata ciclo de vida do proponente, métricas de aceitação e seleção de horizonte sob carga, sem transformar escala experimental em produção comprovada.

Proponente versionado
O módulo auxiliar depende do alvo e de sua interface interna. Mudanças de quantização, adapters ou camadas expostas podem alterar concordância mesmo quando a forma dos tensores continua válida. Versione o par e execute um teste de compatibilidade após qualquer mudança; não avalie apenas se ambos carregam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011.

Métrica interpretável
As métricas atuais do vLLM distinguem tokens aceitos de tokens adicionais produzidos na rodada. Comprimento médio de aceitação que inclui bônus não é a mesma medida que taxa de propostas aceitas. Registre tentativas, posições e comprimento, mantendo denominadores explícitos para comparar políticas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011.

Horizonte sob concorrência
Gerar mais candidatos aumenta trabalho do módulo e da verificação. Quando o alvo já processa lotes grandes eficientemente, a vantagem pode diminuir. Uma política proposta ajusta horizonte por domínio e carga, mas precisa de limites e períodos de avaliação para não reagir a ruído de poucos pedidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011.

USO AVANÇADO — Saídas especializadas longas
Cenário: Um alvo é usado repetidamente no mesmo domínio.
Estratégia: Treine ou selecione proponente compatível, valide correção do algoritmo e meça aceitação por posição. Compare com o alvo sozinho sob a mesma chegada de pedidos.
Papel do modelo pequeno: Um alvo 15–30B pode usar um auxiliar barato; a relação de custo importa mais que o rótulo do método.
Aceite proposto: Reduzir latência de respostas completas sem degradar distribuição-alvo ou capacidade útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011.

USO AVANÇADO — Mudança de adapter
Cenário: O serviço troca comportamento especializado durante o dia.
Estratégia: Mantenha métricas por adapter e desative especulação quando a configuração não foi validada. Se houver proponente próprio, trate-o como artefato dependente.
Papel do modelo pequeno: Um 8–14B pode necessitar menos investimento que um módulo específico por tarefa.
Aceite proposto: Detectar queda de aceitação e comparar fallback com execução normal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em alvos 3–7B, custo auxiliar pode consumir a economia; medir antes de treinar um proponente.
8–14B: Domínio repetitivo e respostas longas podem justificar estudo, sem garantia por porte.
15–30B: A memória adicional do proponente compete com KV e concorrência do alvo.
Requisitos de treino/runtime: EAGLE requer módulo treinado e interface compatível; runtime precisa verificar candidatos corretamente.
Não aplicar quando: Não chamar todos os EAGLE de predição de características idêntica nem prometer ganho a partir de taxa de aceitação.

## T128:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: EAGLE é recurso documentado.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

V4B-C007 — Meta / Experimentos EAGLE para Llama
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores apresentam otimizações de treinamento e inferência de EAGLE para Llama em condições descritas como production scale.
Mecanismo documentado: Atenção em árvore, verificação em múltiplas rodadas e otimizações de execução do proponente/target.
Correspondência com esta base: O trabalho estuda EAGLE explicitamente.
Transferência proposta para modelo pequeno: Proposta: avaliar a viabilidade de treinamento de um draft compatível com um alvo 8–30B antes de investigar grandes lotes.
Limite: A página aberta não identifica implantação comercial específica; production scale não é convertido em production_documented. Ganhos em Llama grande e múltiplas H100 não são transferidos ao ambiente do usuário.
Fontes: V4B-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T128:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T128 → T080 [complements]
Como combinar: Lookahead adaptativo pode controlar o trabalho proposto.
Interface: Aceitação por posição e duração de cada fase.
Condição: Política não modifica a regra correta de confirmação.
Aceite proposto: Comparar horizonte adaptativo com opções fixas em carga aberta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T128 → T086 [complements]
Como combinar: Quantização KV pode alterar custo e concordância quando aplicada ao sistema.
Interface: Precisões e estados dos dois caminhos.
Condição: Par completo revalidado após mudança.
Aceite proposto: Testar qualidade e desempenho isolando cada intervenção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S038, V3B-S001, V4B-S007, V4B-S029, V4B-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir 'production scale' em pesquisa com implantação operacional identificada.
- Rejeitar uso de características de alvo incompatível, mesmo se dimensões coincidem.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O ganho esperado é executar o alvo mais eficientemente. Se a verificação preserva sua distribuição, EAGLE não torna o alvo mais competente que ele próprio nem prova equivalência a fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T080, T132

## Fontes primárias associadas

### B-S038 — EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

[https://arxiv.org/abs/2503.01840](https://arxiv.org/abs/2503.01840)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EAGLE-3 usa fusão de características de múltiplas camadas para predição direta de tokens; não equivale ao EAGLE original.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S007 — Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions

[https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/](https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Engenharia de EAGLE para Llama, incluindo atenção em árvore e grandes lotes.

Limite: Production scale descreve escala de experimento; página não identifica implantação comercial específica suficiente para contagem de produção.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T129 — MTP — Multi-Token Prediction

**Nome canônico:** MTP — Multi-Token Prediction  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T129  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-token prediction; predição de múltiplos tokens

## T129:C01 — conceito

Objetivo ou arquitetura que treina o modelo para predizer vários tokens futuros, em vez de apenas o próximo. Algumas implementações usam cabeças auxiliares sobre um tronco compartilhado e podem apoiar especulação na inferência. O treinamento MTP e o algoritmo de aceitação de tokens são componentes distintos.

Como funciona:
- Definir alvos em múltiplas posições futuras durante o treino.
- Otimizar cabeças ou módulos que compartilham parte da representação.
- Na inferência compatível, usar previsões adicionais como candidatos e aplicar verificação apropriada.

## T129:C02 — aplicacao

Quando usar:
- Checkpoint já fornece módulos MTP e runtime suporta sua utilização.
- Pesquisa de treinamento quer comparar eficiência de aprendizagem e geração.

Quando não usar:
- Esperar criar cabeças úteis apenas ligando uma flag em modelo que não as possui.

Implementação proposta:
- Inspecionar configuração e pesos auxiliares disponibilizados com o modelo.
- Comparar modo normal e modo MTP com mesma tarefa e amostragem.
- Registrar política de verificação e limites de número de tokens futuros.

Aplicação LAI proposta:
Proposta LAI: verificar suporte concreto do checkpoint antes de planejar ganho MTP; considerar como atributo na escolha de modelos e runtimes.

## T129:C03 — riscos_validacao

Armadilhas:
- Predizer vários tokens não garante que todos serão aceitos ou produzidos numa única passagem útil.
- Módulos ausentes ou incompatíveis não podem ser substituídos por mera configuração.

Métricas sugeridas:
- Aceitação de cada posição futura e custo incremental do módulo.
- Qualidade de tarefa, latência final e memória adicional.

Testes propostos:
- Desabilitar módulos auxiliares e obter uma referência de geração convencional.
- Forçar baixa concordância e verificar que a implementação não aceita previsões sem o controle exigido.

## T129:C04 — perguntas_proveniencia

Pergunta: MTP e speculative decoding são sinônimos?
Resposta: Não. MTP produz previsões; especulação define como candidatos são usados e verificados.

Pergunta: MTP pode melhorar treinamento?
Resposta: É uma hipótese investigada com resultados em modelos específicos; não garante ganho para todo checkpoint.

Pergunta: MTP exige usar todas as cabeças no serviço?
Resposta: Não necessariamente; o objetivo auxiliar e o uso acelerado na inferência são decisões distintas.

Pergunta: Previsão futura já conhece o token intermediário amostrado?
Resposta: Não por definição. Examine o condicionamento da arquitetura antes de tratá-la como uma cadeia autoregressiva comum.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T129:C05 — mecanismo_avancado

Prever posições futuras com cabeças auxiliares modifica o objetivo de treinamento. Cabeças que partem de uma representação compartilhada não produzem automaticamente a mesma fatoração autoregressiva de gerar um token e condicionar o próximo nele. Usá-las como propostas exige um procedimento de verificação apropriado. Também é possível usar o objetivo apenas como supervisão auxiliar e manter um caminho convencional na implantação.

Condição de contorno:
Um checkpoint treinado somente para próximo token não ganha cabeças úteis apenas por habilitar uma opção de execução.

Contrato proposto:
- Entradas: Arquitetura com cabeças compatíveis, alvos deslocados e política de uso na inferência.
- Saídas: Perdas auxiliares no treino ou propostas verificáveis durante geração.
- Estado: Pesos das cabeças, alinhamento dos alvos e estados compartilhados.
- Invariante: Cada cabeça é supervisionada pela posição futura correta, sem acesso indevido ao alvo.

Compromissos de projeto:
- Supervisão adicional pode mudar representações e exige controlar comparações de treinamento.
- Mais candidatos por passo elevam potencial de amortização e trabalho de verificação.

## T129:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar em uma posição os rótulos de uma cabeça e comparar com a indexação correta. Esperar perda e aceitação anormais; verificar também fronteiras e padding de exemplos.

Plano de avaliação proposto:
Plano proposto: separar experimento de qualidade do treinamento e experimento de velocidade na inferência. Controlar dados, orçamento e arquitetura; medir métricas de tarefa, custo das cabeças e tokens confirmados, evitando atribuir todo ganho ao paralelismo de saída.

Comparações:
- T079 (complements): Cabeças futuras podem fornecer candidatos, mas a regra especulativa determina sua confirmação exata.

Afirmação rastreável:
O trabalho de multi-token prediction treina cabeças independentes sobre um tronco compartilhado para prever vários tokens futuros.
Suporte: direct; fontes: B-S039
Limite: O resultado não implica que previsões simultâneas possam ser publicadas sem verificação preservando a distribuição original.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T129:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou supervisão auxiliar e proposta especulativa. O aprofundamento analisa transferência entre treino e serving, qualidade por distância futura e custo de manter cabeças que podem não ser usadas.

Objetivo e implantação
Um modelo pode ter sido treinado com alvos futuros sem disponibilizar todas as cabeças na exportação. Inspecione artefato e runtime antes de planejar MTP na inferência. Uma descrição do treinamento não comprova que a implantação usa geração de múltiplos tokens por passo ou que o checkpoint público inclui os componentes necessários.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

Distância da previsão
Quanto mais distante o token previsto, maior pode ser a incerteza sem observar as escolhas intermediárias. Meça acerto e aceitação por horizonte, categoria e configuração de amostragem. Uma média agregada pode esconder uma primeira cabeça útil e demais posições que só acrescentam custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

Compartilhamento de computação
Cabeças auxiliares podem reaproveitar representações, mas ainda exigem operações e estado. Quantifique memória e tempo adicionais e confirme se o backend executa de modo eficiente. A alternativa de draft externo possui outro custo e outra flexibilidade; a comparação depende da implementação concreta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

USO AVANÇADO — Escolha de checkpoint
Cenário: Dois modelos semelhantes diferem em suporte MTP.
Estratégia: Compare qualidade do caminho convencional, disponibilidade das cabeças e benefício da verificação. Não escolha só pelo número de tokens que o material promocional diz prever.
Papel do modelo pequeno: Um 15–30B pode ser candidato quando respostas longas tornam a economia relevante.
Aceite proposto: Aceitar pela latência completa, memória e qualidade no mesmo domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

USO AVANÇADO — Pesquisa de treinamento
Cenário: Há controle sobre um modelo especializado.
Estratégia: Adicione objetivos futuros com alinhamento rigoroso e avalie se melhoram representação ou serving. Separe efeito do treinamento do efeito de executar as cabeças na geração.
Papel do modelo pequeno: Um 3–7B pode servir como escala de experimento antes de investimento maior.
Aceite proposto: Ablacionar objetivo auxiliar e modo de inferência em comparações distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: O benefício pode estar no treinamento, mesmo sem aceleração em serving; não misturar as conclusões.
8–14B: Use horizonte curto inicialmente e registre retornos decrescentes por posição.
15–30B: Inclua estados auxiliares no orçamento e na transferência entre workers, quando presentes.
Requisitos de treino/runtime: Requer arquitetura e pesos compatíveis, além de verificação apropriada na inferência. Não é um flag que cria cabeças treinadas.
Não aplicar quando: Não emitir previsões independentes como se fossem a mesma fatoração autoregressiva do alvo.

## T129:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: MTP faz parte da pesquisa/treino do modelo; a fonte não comprova que a especulação MTP esteja ativa em toda implantação online.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: MTP é recurso documentado para modelos compatíveis.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T129:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T129 → T079 [feeds]
Como combinar: Cabeças MTP podem produzir candidatos para verificação especulativa.
Interface: Propostas e informações exigidas pelo algoritmo.
Condição: Runtime suporta o checkpoint e a regra de confirmação.
Aceite proposto: Comparar distribuição e medir tokens confirmados por rodada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S039, V4B-S011, V4D-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T129 → T102 [complements]
Como combinar: Separar fases pode exigir transferir estados auxiliares junto ao KV.
Interface: Manifesto de estados por sequência.
Condição: Destino conhece todos os componentes necessários.
Aceite proposto: Testar retomada sem perda ou mistura de cabeças e posições.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S039, V4B-S011, V4D-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar se as cabeças existem no artefato entregue, não somente no paper.
- Separar disponibilidade do recurso em TensorRT-LLM de adoção por um produto específico.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
MTP não permite inferir qualidade geral a partir de quantos tokens são propostos. Compare a resposta do modelo e o custo de produzi-la; melhoria de treinamento e aceleração são hipóteses diferentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T128, T132

## Fontes primárias associadas

### B-S039 — Better & Faster Large Language Models via Multi-token Prediction

[https://arxiv.org/abs/2404.19737](https://arxiv.org/abs/2404.19737)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetivo de treino prevê múltiplos tokens com cabeças auxiliares sobre tronco compartilhado.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

### V4D-S008 — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesquisa sobre RL de raciocínio e transferência de capacidades a modelos menores.

Limite: Pesquisa e benchmarks, não evidência de implantação de cada variante. Registro atual é v2, revisado em 2026-01-04; comparação histórica não define fronteira de novembro de 2026.

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

# T130 — N-Gram Speculative Decoding

**Nome canônico:** N-Gram Speculative Decoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T130  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ngram speculation; especulação por n-gramas

## T130:C01 — conceito

Gera candidatos de continuação buscando sequências de tokens repetidas no prompt ou em um pool de histórico permitido. Dispensa um modelo neural auxiliar para a proposta, mas o modelo alvo ainda verifica os candidatos. Favorece padrões repetitivos, como transformações de texto e código.

Como funciona:
- Indexar n-gramas e continuações observadas em tokens.
- Localizar correspondência para o final da sequência atual.
- Propor alguns tokens seguintes e submeter a verificação do alvo.

## T130:C02 — aplicacao

Quando usar:
- Saída reutiliza trechos do contexto ou padrões recorrentes.
- Memória ou complexidade não justificam carregar um draft neural.

Quando não usar:
- Conteúdo pouco repetitivo gera candidatos ruins e overhead maior que a economia.

Implementação proposta:
- Começar com pool privado por requisição e limites de tamanho.
- Ajustar tamanho da chave e quantidade de candidatos com avaliação de custo líquido.
- Preservar a identificação do tokenizer e da política de amostragem no experimento.

Aplicação LAI proposta:
Proposta LAI: candidato inicial para tarefas repetitivas do modelo local por não exigir treino de draft; validar separadamente conversa aberta e edição de código.

## T130:C03 — riscos_validacao

Armadilhas:
- Comparar texto decodificado em vez de tokens pode produzir correspondências inválidas.
- Pools compartilhados guardam conteúdo e precisam respeitar escopo de acesso e retenção.

Métricas sugeridas:
- Taxa de correspondência, comprimento aceito e custo de lookup.
- Latência por batch e memória de índices no host.

Testes propostos:
- Comparar textos repetitivos e aleatórios, exigindo ganho real no primeiro e degradação limitada no segundo.
- Inserir padrões ambíguos e confirmar que o alvo rejeita continuações inadequadas.

## T130:C04 — perguntas_proveniencia

Pergunta: A resposta armazenada é devolvida diretamente?
Resposta: Não. Ela pode fornecer candidatos; o alvo precisa verificá-los.

Pergunta: N-gram é busca semântica?
Resposta: Não. Trabalha principalmente com padrões exatos de tokens, não equivalência de significado.

Pergunta: Correspondência exata dispensa o alvo?
Resposta: Não. O padrão pode ter surgido em outro contexto e a próxima distribuição pode ser diferente.

Pergunta: Pode funcionar sem um segundo modelo?
Resposta: Sim. O proponente pode ser uma estrutura de tokens na CPU; ainda existem custo de busca e verificação.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T130:C05 — mecanismo_avancado

O tamanho da chave controla especificidade do padrão: correspondências curtas ocorrem mais, mas podem propor continuações ambíguas; longas têm menos cobertura. O comprimento da continuação controla trabalho adicional de verificação. Ambos precisam ser avaliados conjuntamente com concorrência. A consulta deve operar em token IDs compatíveis com o alvo, pois coincidência de caracteres após decodificação não garante a mesma segmentação.

Condição de contorno:
Em texto pouco repetitivo, manutenção do dicionário e verificação de candidatos podem custar mais que os passos economizados.

Contrato proposto:
- Entradas: Histórico permitido de tokens, comprimentos de chave e proposta, política para múltiplas ocorrências.
- Saídas: Continuação candidata e sua origem no índice.
- Estado: Pares de padrões, frequência ou ordem das ocorrências e limites de memória.
- Invariante: Correspondência serve apenas para propor; confirmação continua dependente do modelo alvo.

Compromissos de projeto:
- Chaves longas aumentam precisão de padrão e reduzem frequência de hits.
- Dicionários grandes ampliam cobertura e podem piorar localidade na CPU.

## T130:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir o mesmo n-grama com continuações conflitantes e inserir mudança de tokenização. Esperar seleção determinável pela política e rejeição de índices incompatíveis.

Plano de avaliação proposto:
Plano proposto: comparar geração sem propostas e diferentes pares de comprimentos na mesma carga. Medir lookup, atualização, verificação, tokens confirmados e latência por concorrência; escolher pelo tempo total e não apenas pelo comprimento aceito.

Comparações:
- T131 (alternative): Estruturas de sufixos suportam padrões variáveis e outra organização das continuações históricas.

Afirmação rastreável:
A implementação documentada de N-Gram constrói padrões chave-continuação e verifica no alvo as propostas encontradas.
Suporte: direct; fontes: B-S041
Limite: O custo e as configurações eficientes descritos no artigo dependem da carga; não são defaults universais.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T130:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou comprimentos de chave e continuação. Esta camada usa o caso de produção do Hiring Assistant para delimitar padrões favoráveis e propõe controles de proveniência e de custo do índice.

Repetição que interessa
N-gramas são particularmente plausíveis quando a saída reaproveita sequências do prompt ou do histórico permitido. O relato do LinkedIn descreve esse perfil em saídas estruturadas do Hiring Assistant. Isso não autoriza extrapolar para raciocínio aberto, tradução livre ou textos com pouca repetição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

Origem e escopo
Defina de onde propostas podem vir: prompt atual, tokens confirmados ou memória compartilhada autorizada. Índices entre usuários exigem isolamento e regras de retenção. Mesmo com verificação pelo alvo, consultar um índice privado pode expor padrões ou ampliar canais de informação; a arquitetura deve limitar acesso desde a busca.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

Custo de busca
Um proponente sem rede neural ainda consome CPU, memória e sincronização. Meça tempo por consulta e atualização, especialmente com contextos grandes e concorrência. Uma chave curta pode produzir muitas ocorrências; a política para escolher continuação precisa ser determinística ou explicitamente amostrada e reprodutível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

USO AVANÇADO — Extração estruturada com cópia
Cenário: A resposta reutiliza nomes e trechos da entrada.
Estratégia: Teste n-gramas no prompt atual, mantendo o verificador do alvo e a gramática quando suportada. Compare diferentes comprimentos sem ajustar ao conjunto final de avaliação.
Papel do modelo pequeno: Um 8–14B pode executar extração especializada com pouco custo adicional de proponente.
Aceite proposto: Medir aceitação, CPU, latência e validade semântica da extração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

USO AVANÇADO — Reescrita com baixa alteração
Cenário: O usuário pede correções pontuais em um texto.
Estratégia: Use a entrada como fonte de candidatos e teste casos em que a continuação mais frequente precisa ser alterada. A verificação deve rejeitar a cópia incorreta.
Papel do modelo pequeno: Um 3–7B pode ser adequado a tarefas locais estreitas, sujeito à qualidade-base.
Aceite proposto: Confirmar alterações obrigatórias e ausência de cópia indevida apesar de alta repetição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Custo de busca pode ser relevante frente a um alvo barato; manter índice restrito ao pedido simplifica.
8–14B: Boa hipótese para formatos repetitivos e respostas longas, sem ganho presumido.
15–30B: Em alvos maiores, verificação pode amortizar mais trabalho, mas concorrência continua determinante.
Requisitos de treino/runtime: Runtime de especulação com proponente de tokens; não requer treinar um draft neural.
Não aplicar quando: Não descrever preservação da distribuição como garantia de texto idêntico em todas as sementes e implementações.

## T130:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O proponente escolhido usa correspondências por n-gramas, sem modelo auxiliar.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T130:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T130 → T079 [feeds]
Como combinar: O LinkedIn usa propostas n-gram verificadas pelo alvo no Hiring Assistant.
Interface: Sequência candidata e estado do alvo.
Condição: Regra correta de aceitação e configuração compatível.
Aceite proposto: Comparar execução especulativa com o alvo sem proponente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S001. Casos: V4B-C001.

2. T130 → T196 [complements]
Como combinar: Restrições estruturais precisam ser consideradas no caminho de verificação.
Interface: Estado de gramática e prefixo confirmado.
Condição: Implementação suporta a combinação sem aceitar tokens proibidos.
Aceite proposto: Testar fronteiras de strings, delimitadores e rejeição de candidatos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S041, V4B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar índice compartilhado sem domínio de acesso explícito.
- Relatar taxa de aceitação com denominador correto e custo do proponente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Especulação n-gram pode acelerar uma tarefa em que o modelo já é competente. A repetição da entrada facilita proposta, mas não garante que o conteúdo copiado seja a resposta certa.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T131, T132

## Fontes primárias associadas

### B-S041 — N-Gram Speculative Decoding in TensorRT LLM

[https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog07_NGram_performance_Analysis_And_Auto_Enablement.html](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog07_NGram_performance_Analysis_And_Auto_Enablement.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Propostas a partir de n-gramas, pools privados ou compartilhados e verificação pelo modelo alvo.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T131 — Suffix Decoding

**Nome canônico:** SuffixDecoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T131  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** SuffixDecoding; decodificação por sufixos

## T131:C01 — conceito

SuffixDecoding propõe continuações a partir de padrões encontrados em árvores de sufixos de tokens do prompt e de gerações anteriores. É especulação sem pesos auxiliares. Não equivale a cache de respostas: o modelo alvo continua verificando o trecho candidato antes de aceitá-lo.

Como funciona:
- Manter estrutura de sufixos com sequências de tokens observadas.
- Buscar padrões que correspondam ao final da geração atual e selecionar continuações.
- Verificar no alvo, atualizar o histórico permitido e controlar retenção da estrutura.

## T131:C02 — aplicacao

Quando usar:
- Workflows iterativos repetem trechos de código, instruções ou tentativas.
- Há implementação compatível e custo de lookup pequeno para a carga.

Quando não usar:
- A estrutura cresce sem limite ou a carga não oferece repetição suficiente.

Implementação proposta:
- Definir limites de tokens armazenados e isolamento por domínio antes de habilitar pool compartilhado.
- Comparar com n-gramas simples e geração convencional no mesmo workload.
- Medir custo no host e na verificação sob diferentes níveis de concorrência.

Aplicação LAI proposta:
Proposta LAI: avaliar em ciclos de edição e verificação da Helena; manter a árvore como acelerador descartável, sem promovê-la a memória factual.

## T131:C03 — riscos_validacao

Armadilhas:
- Uma árvore grande pode consumir CPU e memória e anular o ganho da GPU.
- Histórico de outro domínio pode elevar candidatos ruins; compartilhamento exige política explícita.

Métricas sugeridas:
- Comprimento médio aceito, tempo de busca e atualização.
- Memória da árvore, throughput e p95 com concorrência crescente.

Testes propostos:
- Executar ciclos repetitivos e carga inédita; aceitar a técnica apenas onde houver benefício líquido.
- Evictar históricos e verificar continuidade correta, sem depender da estrutura para verdade ou persistência da missão.

## T131:C04 — perguntas_proveniencia

Pergunta: SuffixDecoding é memória episódica?
Resposta: Não. Armazena padrões úteis para propor tokens, sem avaliar se uma experiência foi correta.

Pergunta: Precisa treinar um modelo auxiliar?
Resposta: O método descrito é model-free na proposta; ainda depende de implementação e verificação no alvo.

Pergunta: O índice torna a resposta uma cópia obrigatória?
Resposta: Não. Ele fornece candidatos; o alvo deve rejeitar continuações incompatíveis com seu contexto atual.

Pergunta: Sem pesos adicionais significa custo zero?
Resposta: Não. Estruturas, contagens, consultas, sincronização e atualização consomem memória e tempo de CPU.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T131:C05 — mecanismo_avancado

Uma árvore de sufixos pode organizar continuações de múltiplas sequências, mas busca rápida não torna atualização gratuita. A implementação descrita pela Snowflake mantém informações de frequência para selecionar filhos, expondo uma troca entre tempo de consulta, atualização e memória. Sob alta concorrência, o proponente na CPU pode limitar o sistema mesmo quando a GPU verifica candidatos eficientemente.

Condição de contorno:
Históricos pouco repetitivos ou manutenção pesada da estrutura reduzem o benefício, independentemente da ausência de pesos adicionais.

Contrato proposto:
- Entradas: Tokens confirmados, histórico autorizado ao índice, limite de retenção e orçamento de proposta.
- Saídas: Continuação candidata com origem e comprimento explícitos.
- Estado: Árvores locais/compartilhadas, contagens e política de remoção de sequências.
- Invariante: Atualizações e remoções preservam contagens e não deixam referências a sequências ausentes.

Compromissos de projeto:
- Reter mais sequências amplia cobertura e custo de memória.
- Pré-organizar filhos acelera escolha e acrescenta manutenção quando contagens mudam.

## T131:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover uma sequência muito frequente enquanto outras usam seus padrões e inserir continuações novas. Esperar consistência de referências e contagens, com verificação normal dos candidatos restantes.

Plano de avaliação proposto:
Plano proposto: comparar N-Gram e sufixos na mesma mistura repetitiva e não repetitiva. Medir tempo CPU de atualização/consulta, memória, verificação e latência total por concorrência; aceitar benefício sem esconder custo do proponente.

Comparações:
- T103 (distinct_from): Uma trie de prefixos indexa ancestralidade KV; a estrutura de sufixos encontra padrões para propor novos tokens.

Afirmação rastreável:
O relato técnico da Snowflake descreve árvores de sufixos e estruturas auxiliares para reduzir custo de selecionar continuações.
Suporte: direct; fontes: B-S040
Limite: Os ganhos relatados pertencem às cargas avaliadas; não garantem superioridade em toda tarefa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T131:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou atualização de árvores e gargalo de CPU. A nova camada considera envelhecimento de padrões, compartilhamento controlado e avaliação da adaptação a mudanças de domínio.

Memória de padrões
Frequências antigas podem favorecer continuações que deixaram de ser comuns. Uma política proposta limita retenção por idade ou quantidade de tokens e compara seu efeito com índice só da requisição. O objetivo é evitar que histórico volumoso aumente custo e reduza relevância sem melhorar aceitação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

Compartilhamento e isolamento
Árvores locais e compartilhadas têm propriedades diferentes. Um índice compartilhado pode aproveitar repetição entre pedidos, mas exige separar domínios de acesso e versões de tokenização. O verificador do alvo não substitui a política de quais dados podem participar da proposta; metadados de origem precisam acompanhar o índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

Medição da contribuição
Compare contra n-gram simples e contra nenhum proponente. Separe custo de construção, atualização, consulta e verificação, incluindo aquecimento do índice. Se a avaliação começa com um índice preenchido por exemplos do teste, o resultado não representa uma implantação sem esse conhecimento prévio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

USO AVANÇADO — Geração de código repetitiva
Cenário: Muitos pedidos seguem APIs e padrões semelhantes.
Estratégia: Use histórico autorizado e versionado, limite retenção e avalie mudanças de biblioteca. O alvo verifica propostas, e compilação ou testes avaliam a tarefa depois.
Papel do modelo pequeno: Um 8–14B pode produzir alterações locais com repertório repetitivo.
Aceite proposto: Medir latência e correção executável, incluindo APIs raras e mudanças de versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

USO AVANÇADO — Lotes com documentos padronizados
Cenário: Saídas compartilham trechos e estruturas.
Estratégia: Construa um índice a partir de dados permitidos, mantenha um controle frio e teste deriva no padrão. Evite transformar o índice em repositório invisível de informações sensíveis.
Papel do modelo pequeno: Um 15–30B pode aproveitar repetição quando o custo de verificação justifica a estrutura.
Aceite proposto: Comparar ganho líquido depois de incluir manutenção de CPU e memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma árvore sofisticada pode ser desnecessária para poucos pedidos e alvos baratos.
8–14B: Repetição entre tarefas pode justificar estudo, com limites claros de retenção.
15–30B: Em alta concorrência, CPU e sincronização podem limitar o sistema antes da GPU.
Requisitos de treino/runtime: Runtime e algoritmo de confirmação corretos; não exige atualização dos pesos do alvo.
Não aplicar quando: Não tratar benchmark de Suffix Decoding como prova de implantação nem assumir que frequência equivale a correção.

## T131:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C023 — Snowflake / Suffix Decoding
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: pesquisa sobre LLM.
Uso observado: A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.
Mecanismo documentado: Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.
Correspondência com esta base: O mecanismo é suffix decoding.
Transferência proposta para modelo pequeno: Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.
Limite: Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.
Fontes: B-S040.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fonte primária de Suffix Decoding e métricas de runtime consultadas. O caso selecionado é pesquisa; implantação específica de bigtech não foi confirmada neste recorte.
Consultas registradas: V4B-Q001, V4B-Q018.

## T131:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T131 → T130 [alternative]
Como combinar: N-gram simples é um baseline que ajuda a justificar a árvore de sufixos.
Interface: Mesmo histórico permitido e política de verificação.
Condição: Orçamentos de memória e CPU comparáveis.
Aceite proposto: Comparar ganho líquido e sensibilidade à mudança de domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S040, V3B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T131 → T080 [complements]
Como combinar: O horizonte pode reagir à aceitação e ao custo de consulta.
Interface: Propostas por posição e duração da rodada.
Condição: Ajuste não usa dados futuros nem altera a distribuição-alvo.
Aceite proposto: Medir adaptação após mudança controlada na repetição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S040, V3B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Eliminar referências a sequências removidas e corrigir contagens relacionadas.
- Separar aquecimento legítimo de vazamento do conjunto de avaliação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve avaliar o gerador completo na tarefa. A árvore melhora proposta de continuações; não adiciona compreensão geral nem transforma cópia provável em verdade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T130, T103

## Fontes primárias associadas

### B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM

[https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvores de sufixos sobre tokens anteriores produzem candidatos especulativos sem modelo auxiliar.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T132 — Draft-Model Speculation

**Nome canônico:** Draft-Model Speculation  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T132  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** draft model speculative decoding; especulação com modelo auxiliar

## T132:C01 — conceito

Variante de speculative decoding em que um modelo menor ou mais rápido gera os candidatos. Diferentemente de n-gramas, exige pesos e recursos do assistente. A decisão econômica depende do custo do draft, de sua concordância com o alvo e do trabalho adicional de verificação.

Como funciona:
- Executar o draft sobre o prefixo compatível e produzir uma curta continuação.
- Avaliar a continuação em paralelo com o alvo.
- Aceitar o trecho válido e corrigir rejeições conforme o algoritmo escolhido.

## T132:C02 — aplicacao

Quando usar:
- Alvo é caro por token e há assistente barato com boa concordância.
- Há memória suficiente para pesos, estados e buffers de ambos.

Quando não usar:
- O assistente compete tanto pelos mesmos recursos que o alvo perde mais tempo do que economiza.

Implementação proposta:
- Validar compatibilidade de tokenização; métodos com tokenizers diferentes exigem tratamento específico.
- Comparar vários comprimentos e registrar custo separado do draft e do alvo.
- Manter a mesma carga, amostragem e critério de qualidade do baseline.

Aplicação LAI proposta:
Proposta LAI: não carregar um segundo modelo na GPU principal antes de medir a folga de memória e comparar com especulação por padrões sem modelo.

## T132:C03 — riscos_validacao

Armadilhas:
- Modelo pequeno competente em geral pode discordar bastante do alvo específico.
- Compartilhar a mesma GPU pode alterar ocupação e memória de maneira desfavorável.

Métricas sugeridas:
- Custo por token proposto e aceito e frequência de rejeições.
- Tempo total por resposta e memória adicional de ambos os modelos.

Testes propostos:
- Usar casos com alta e baixa concordância e confirmar que o ganho previsto corresponde à latência real.
- Verificar correção da amostragem no modo implementado, sem supor equivalência apenas porque as respostas parecem boas.

## T132:C04 — perguntas_proveniencia

Pergunta: O melhor draft é sempre o menor?
Resposta: Não. Precisa equilibrar custo e concordância; pequeno demais pode gerar rejeições frequentes.

Pergunta: É uma técnica independente da especulação?
Resposta: É uma implementação da família T079; o proponente aqui é explicitamente outro modelo.

Pergunta: Qual o limite quando α tende a um?
Resposta: A expectativa tende a γ+1; isso ainda precisa ser comparado ao custo de produzir e verificar a rodada.

Pergunta: Dois modelos da mesma família bastam?
Resposta: Não. É necessário verificar tokenização, configuração, custo e concordância; parentesco nominal não constitui contrato de compatibilidade.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T132:C05 — mecanismo_avancado

Um draft externo precisa ser barato em relação ao alvo e suficientemente próximo de suas distribuições. Sob hipóteses idealizadas de aceitação independente α, γ propostas rendem em média (1−α^(γ+1))/(1−α) tokens confirmados por rodada, contando o token adicional. A duração inclui γ passos do draft e a verificação; aumentar γ não compensa automaticamente baixa concordância ou um proponente caro.

Condição de contorno:
A independência e a taxa constante são aproximações analíticas; aceitação real varia com prefixo, domínio e política de amostragem.

Contrato proposto:
- Entradas: Par de modelos, alinhamento de tokens, horizonte e configurações de amostragem.
- Saídas: Candidatos com probabilidades necessárias e continuação confirmada pelo alvo.
- Estado: Caches separados e correspondência exata entre prefixos dos dois modelos.
- Invariante: Probabilidades usadas na correção correspondem às propostas efetivamente amostradas.

Compromissos de projeto:
- Draft maior pode elevar concordância e consumir o ganho de tempo.
- Tokenizadores diferentes exigem alinhamento adicional e restringem algoritmos aplicáveis.

## T132:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar um draft barato que concorda em prosa e diverge em código, depois alterar filtros de amostragem apenas nele. Esperar custos e aceitação distintos, sem perder a correção matemática da distribuição alvo.

Plano de avaliação proposto:
Plano proposto: comparar pares de modelos e horizontes com mesma carga e recursos explicitados. Medir tempo do draft, verificação, aceitação por posição e latência total; substituir estimativas idealizadas por medições antes de dimensionar produção.

Comparações:
- T080 (complements): Adaptar o horizonte responde ao custo e à concordância observados do par.

Afirmação rastreável:
A análise de speculative decoding relaciona aceitação, horizonte e custo relativo do draft ao trabalho amortizado.
Suporte: direct; fontes: V3B-S001
Limite: A expressão idealizada não prevê automaticamente velocidade com batching, comunicação ou aceitação correlacionada.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T132:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 forneceu o modelo de custo e a condição probabilística. O aprofundamento analisa alinhamento entre distribuições, vida útil dos dois caches e seleção de pares sem confundir tamanho com economia.

Compatibilidade probabilística
Tokenização, filtros e temperatura afetam a distribuição de proposta e alvo. O algoritmo precisa usar probabilidades correspondentes ao que realmente foi amostrado, incluindo transformações aplicáveis. Alinhamento de texto entre tokenizers diferentes não basta para usar uma correção desenhada para o mesmo vocabulário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S001, V4B-S029, V4D-S003.

Dois estados, uma história
Draft e alvo possuem caches distintos, mas devem representar o mesmo prefixo confirmado. Quando parte da proposta é rejeitada, estado provisório precisa ser descartado ou corrigido. Cancelamento e retomada devem manter cursores separados de tokens propostos, verificados e emitidos; publicar cedo quebra a garantia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S001, V4B-S029, V4D-S003.

Escolha do par
Um draft menor pode ser rápido e divergir muito do alvo; outro ligeiramente maior pode aceitar mais e custar demais. Compare tempo do draft, verificação e trabalho confirmado por rodada sob carga. A documentação atual do Phi Silica descreve draft na NPU, sem provar que a mesma estratégia se aplica ao caminho GPU.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S001, V4B-S029, V4D-S003.

USO AVANÇADO — Alvo especializado estável
Cenário: O mesmo modelo maior atende um domínio recorrente.
Estratégia: Avalie pares de draft e alvo, começando por compatibilidade de tokens. Ajuste horizonte em dados separados e inclua memória extra na comparação de capacidade.
Papel do modelo pequeno: Um alvo 15–30B com draft barato pode ser hipótese útil para respostas longas.
Aceite proposto: Reduzir tempo completo mantendo o contrato de distribuição e custo aceitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S001, V4B-S029, V4D-S003.

USO AVANÇADO — Serving local com energia limitada
Cenário: A latência importa junto com consumo e memória.
Estratégia: Meça o sistema com e sem draft no backend realmente disponível. Ociosiade menor da unidade de cálculo não garante menor energia total; registre duração e recursos adicionais.
Papel do modelo pequeno: Alvos 3–7B podem não amortizar outro modelo; verificar antes de adotar.
Aceite proposto: Escolher por orçamento real, sem importar ganhos de NPU, GPU ou modelo diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S001, V4B-S029, V4D-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: O alvo já barato pode tornar especulação redundante; a comparação precisa incluir carga baixa.
8–14B: Pares próximos em comportamento podem ser estudados, sem presumir que família igual garante aceitação.
15–30B: Memória do draft pode reduzir concorrência do alvo e anular vantagem por pedido.
Requisitos de treino/runtime: Dois modelos compatíveis e runtime que implemente verificação/correção. Treinar um draft próprio é opcional e separado.
Não aplicar quando: Não prometer texto idêntico em qualquer execução; a preservação pretendida é da distribuição sob as hipóteses do algoritmo.

## T132:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: A API explica o modelo de rascunho menor verificado pelo principal na NPU. Escopo: capacidade NPU da documentação consultada em 2026-11-05; não é inferida para GPU ou para a versão histórica de 2024.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4B-C007 — Meta / Experimentos EAGLE para Llama
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores apresentam otimizações de treinamento e inferência de EAGLE para Llama em condições descritas como production scale.
Mecanismo documentado: Atenção em árvore, verificação em múltiplas rodadas e otimizações de execução do proponente/target.
Correspondência com esta base: Há componente de draft aprendido, com acoplamento específico que difere de qualquer modelo auxiliar genérico.
Transferência proposta para modelo pequeno: Proposta: avaliar a viabilidade de treinamento de um draft compatível com um alvo 8–30B antes de investigar grandes lotes.
Limite: A página aberta não identifica implantação comercial específica; production scale não é convertido em production_documented. Ganhos em Llama grande e múltiplas H100 não são transferidos ao ambiente do usuário.
Fontes: V4B-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T132:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T132 → T080 [complements]
Como combinar: Lookahead regula quanto trabalho o draft antecipa.
Interface: Aceitação por posição e custo da rodada.
Condição: Estimativas suficientemente estáveis.
Aceite proposto: Comparar com horizontes fixos sob mudança de carga.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S001, V4B-S029, V4D-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T132 → T079 [feeds]
Como combinar: Draft externo é uma forma de construir candidatos para especulação.
Interface: Tokens e probabilidades necessárias à confirmação.
Condição: Caches e distribuição consistente.
Aceite proposto: Testar rejeição parcial, bônus e rollback de estado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S001, V4B-S029, V4D-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não enviar tokens provisórios ao usuário como confirmados.
- Revalidar o par após mudar quantização, adapter ou parâmetros de geração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Com verificação correta, o draft acelera o alvo sem elevar sua capacidade. A comparação com fronteira deve usar qualidade do alvo e custo do sistema de dois modelos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T080, T128, T130

## Fontes primárias associadas

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

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4B-S007 — Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions

[https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/](https://ai.meta.com/research/publications/efficient-speculative-decoding-for-llama-at-scale-challenges-and-solutions/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Engenharia de EAGLE para Llama, incluindo atenção em árvore e grandes lotes.

Limite: Production scale descreve escala de experimento; página não identifica implantação comercial específica suficiente para contagem de produção.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

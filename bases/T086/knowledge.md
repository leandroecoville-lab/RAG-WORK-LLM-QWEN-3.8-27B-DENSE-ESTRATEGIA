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

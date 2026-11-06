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

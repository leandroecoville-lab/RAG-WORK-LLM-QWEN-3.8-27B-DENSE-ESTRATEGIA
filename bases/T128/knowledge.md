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

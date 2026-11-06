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

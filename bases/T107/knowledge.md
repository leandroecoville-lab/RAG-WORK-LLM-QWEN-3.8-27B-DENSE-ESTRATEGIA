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

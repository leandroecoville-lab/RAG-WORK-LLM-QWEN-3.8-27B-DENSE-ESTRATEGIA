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

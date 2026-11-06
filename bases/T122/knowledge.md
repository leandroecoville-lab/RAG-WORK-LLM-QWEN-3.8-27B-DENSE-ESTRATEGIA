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

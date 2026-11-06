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

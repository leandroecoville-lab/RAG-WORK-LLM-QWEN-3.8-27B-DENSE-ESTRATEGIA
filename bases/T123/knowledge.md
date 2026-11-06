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

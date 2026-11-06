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

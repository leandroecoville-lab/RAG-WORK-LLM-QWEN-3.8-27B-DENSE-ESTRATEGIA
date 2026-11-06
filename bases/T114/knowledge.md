# T114 — Online Softmax

**Nome canônico:** Online Softmax  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T114  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** softmax incremental; normalização online

## T114:C01 — conceito

Cálculo incremental e numericamente estável do normalizador de softmax, útil quando scores chegam em blocos. Mantém máximo e soma reescalada em vez de exigir todas as posições simultaneamente. É uma peça algorítmica usada por implementações eficientes, não uma aproximação obrigatória da distribuição.

Como funciona:
- Guardar máximo corrente m e soma l dos exponenciais reescalados.
- Ao receber novo bloco, atualizar m e reescalar a soma anterior para o novo máximo.
- Acrescentar contribuições do bloco e normalizar os acumuladores ao final.

## T114:C02 — aplicacao

Quando usar:
- Atenção fundida calcula scores por partes.
- Uma operação precisa reduzir passes ou armazenamento de intermediários.

Quando não usar:
- Somar exponenciais brutos sem controle de escala e chamar isso de implementação estável.

Implementação proposta:
- Especificar dtype dos acumuladores e política para posições mascaradas.
- Construir referência em maior precisão com valores extremos.
- Se também acumular valores da atenção, aplicar o mesmo reescalonamento ao numerador.

Aplicação LAI proposta:
Proposta LAI: usar para compreender por que kernels eficientes preservam atenção com menos memória; não é função que a aplicação precisa reimplementar.

## T114:C03 — riscos_validacao

Armadilhas:
- Combinar blocos com máximos diferentes sem reescalar produz resultado errado.
- Linha totalmente mascarada exige tratamento explícito para evitar NaN.

Métricas sugeridas:
- Erro absoluto e relativo contra referência e ocorrência de NaN.
- Número de leituras/escritas e tempo da operação fundida.

Testes propostos:
- Testar scores muito grandes, muito pequenos, repetidos e blocos vazios/mascarados.
- Mudar tamanho e ordem de agrupamento de blocos e verificar consistência dentro da tolerância numérica.

## T114:C04 — perguntas_proveniencia

Pergunta: Online Softmax elimina a normalização?
Resposta: Não. Computa o normalizador de maneira incremental com reescalonamento.

Pergunta: A saída é bit a bit igual?
Resposta: Não é garantia geral em ponto flutuante; o algoritmo é matematicamente equivalente sob suas condições.

Pergunta: Pode normalizar cada tile e somar?
Resposta: Somente se conservar e aplicar as massas relativas corretas; somar distribuições locais sem pesos produz outra distribuição.

Pergunta: Por que guardar o máximo?
Resposta: Subtrair uma referência evita exponenciais excessivas e permite reescalar blocos quando surge um score maior.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T114:C05 — mecanismo_avancado

Para blocos A e B, mantenha máximo m e soma l de exp(score−m). A combinação usa m=max(mA,mB) e l=exp(mA−m)·lA+exp(mB−m)·lB. O numerador ponderado pelos valores exige a mesma reescala antes da soma. Combinar médias locais diretamente é incorreto: blocos com massas de probabilidade diferentes não devem receber pesos iguais.

Condição de contorno:
Linhas totalmente mascaradas precisam de regra explícita, pois operações com máximos negativos infinitos podem gerar formas indefinidas.

Contrato proposto:
- Entradas: Scores em blocos, máscara e valores quando houver atenção ponderada.
- Saídas: Normalizador estável e resultado equivalente à redução global especificada.
- Estado: Máximo, soma reescalada e numerador parcial por linha.
- Invariante: Todas as parcelas são expressas na mesma referência exponencial antes de serem combinadas.

Compromissos de projeto:
- Acumulação em maior precisão reduz erro e ocupa mais recursos.
- Ordem de blocos preserva álgebra real, mas pode alterar arredondamento finito.

## T114:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: combinar blocos com máximos muito diferentes e substituir a reescala por média de saídas locais. A versão defeituosa deve divergir da referência; testar também linha vazia.

Plano de avaliação proposto:
Plano proposto: usar referência de alta precisão, permutar ordens e variar amplitudes dos scores. Medir erro absoluto/relativo e presença de valores não finitos; definir tolerância segundo dtype e uso, sem exigir igualdade bit a bit entre reduções distintas.

Comparações:
- T101 (complements): Estados de normalização podem combinar contribuições recebidas de diferentes partições do contexto.

Afirmação rastreável:
O cálculo online do normalizador busca computar o softmax clássico com menos acessos à memória.
Suporte: direct; fontes: B-S028
Limite: A estabilidade numérica não torna arbitrariamente pequena a perda de precisão de qualquer dtype.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T114:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 deu a regra de combinação estável. O aprofundamento trata identidade de redução, máscaras extremas, precisão acumulada e uso dessa operação em paralelismo.

Identidade e linhas vazias
A implementação precisa representar um bloco sem chaves válidas sem produzir operações indefinidas entre infinitos. Defina explicitamente estado vazio, transição para a primeira contribuição válida e comportamento de linha inteiramente mascarada. Retornar zero, erro ou outro valor deve seguir o contrato da operação, não surgir por acidente numérico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

Ordem de redução
A combinação é matematicamente associativa sob aritmética exata, mas arredondamentos tornam ordens diferentes numericamente distintas. Particionamento, tile e topologia podem mudar a ordem sem mudar a fórmula. Compare tolerâncias por dtype e comprimento; exigir igualdade bit a bit pode rejeitar uma implementação correta ou ocultar tolerâncias mal escolhidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

Normalizador e diagnóstico
Log-sum-exp e estatísticas parciais ajudam a investigar saturação e divergências, mas não são confiança factual da resposta. Um token pode receber probabilidade alta dentro de uma distribuição equivocada. Mantenha métricas numéricas separadas de métricas de qualidade do modelo e da decisão de encaminhar uma tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

USO AVANÇADO — Redução distribuída de atenção
Cenário: Blocos de KV residem em partições diferentes.
Estratégia: Combine máximos, massas e numeradores na mesma referência exponencial. Preserve posições e máscaras globais, incluindo partições sem contribuição válida.
Papel do modelo pequeno: Um modelo 15–30B com contexto longo pode usar o mecanismo se a comunicação compensar.
Aceite proposto: Comparar com referência não particionada e testar partições vazias ou desbalanceadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

USO AVANÇADO — Diagnóstico de NaNs
Cenário: Uma otimização falha apenas em entradas extremas.
Estratégia: Construa scores controlados com grande amplitude, mascaramento e comprimentos variados. Localize se a falha nasce na projeção, na exponencial ou na combinação.
Papel do modelo pequeno: Modelos pequenos permitem reproduzir o defeito com tensores sintéticos sem expor dados privados.
Aceite proposto: Eliminar não finitos sem alterar silenciosamente escala ou máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S028, B-S027, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Útil como operação interna de kernels; não precisa ser exposto como configuração de produto.
8–14B: A extensão do contexto e dtype determinam sensibilidade, não apenas os parâmetros totais.
15–30B: Reduções distribuídas exigem verificar comunicação e precisão acumulada conjuntamente.
Requisitos de treino/runtime: Runtime/kernel; pode participar de treinamento e inferência. Precisão dos acumuladores deve ser explicitada.
Não aplicar quando: Não combinar médias locais com pesos iguais nem tratar softmax como verificador de verdade.

## T114:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020, V4B-Q005.

## T114:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T114 → T101 [feeds]
Como combinar: A redução de estados parciais permite agregar atenção distribuída.
Interface: Tripla de estatísticas e identidade da consulta.
Condição: Todos os blocos representam a mesma consulta e escala.
Aceite proposto: Comparar diferentes ordens de comunicação com referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S028, B-S027, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T114 → T113 [complements]
Como combinar: Tiles usam a redução para manter saída e normalização incrementalmente.
Interface: Estado parcial por linha.
Condição: Padding excluído antes das estatísticas.
Aceite proposto: Testar bordas, máscaras e sequências com comprimentos díspares.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S028, B-S027, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar overflow nos scores de erro na redução; a estabilização não corrige tudo que ocorreu antes.
- Evitar clamps silenciosos que mudam probabilidades sem registro.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Essa técnica protege execução numérica e memória, sem acrescentar conhecimento. Um serviço pequeno deve demonstrar qualidade por testes externos, mesmo que seu softmax seja perfeitamente estável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T113

## Fontes primárias associadas

### B-S028 — Online normalizer calculation for softmax

[https://arxiv.org/abs/1805.02867](https://arxiv.org/abs/1805.02867)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cálculo online do normalizador de softmax com menos acessos à memória.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S027 — Fused Attention

[https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html](https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de referência de atenção em blocos com kernel fundido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

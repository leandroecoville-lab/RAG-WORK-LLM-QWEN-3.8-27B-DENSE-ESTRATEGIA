# T098 — Memory-Efficient Attention

**Nome canônico:** Memory-Efficient Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T098  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção eficiente em memória

## T098:C01 — conceito

Nome de família e de implementações que reduzem memória temporária no cálculo de atenção. Pode incluir kernels fundidos e processamento por blocos. O termo isolado não identifica uma única versão, nem informa se há aproximação, suporte a GQA ou alteração de padrão.

Como funciona:
- Evitar guardar intermediários de tamanho proporcional à matriz completa quando possível.
- Escolher kernel segundo forma, dtype, máscara e hardware.
- Manter fallback explícito quando a implementação otimizada não suporta a entrada.

## T098:C02 — aplicacao

Quando usar:
- Memória temporária da atenção limita o tamanho de entrada ou lote.
- Framework oferece implementação otimizada testada para o caso.

Quando não usar:
- Assumir que a configuração solicitada foi respeitada sem observar dispatch e profiler.

Implementação proposta:
- Registrar nome e versão do backend efetivo junto da configuração de atenção.
- Testar máscara, dropout, precisão e número de cabeças usados pelo modelo.
- Separar memória temporária de atenção e memória persistente de KV na medição.

Aplicação LAI proposta:
Proposta LAI: documentar o kernel efetivo dentro do inventário de runtime, evitando registrar o mesmo ganho como Memory-Efficient Attention e FlashAttention independentes.

## T098:C03 — riscos_validacao

Armadilhas:
- Solicitar mapas completos de atenção pode obrigar materialização de intermediários.
- Mudança de backend pode alterar ligeiramente valores numéricos e determinismo.

Métricas sugeridas:
- Memória de pico além dos pesos e KV.
- Latência por forma e frequência de fallback ao backend matemático.

Testes propostos:
- Comparar saída com referência e cobrir máscaras vazias, padding e comprimentos pequenos.
- Forçar uma forma não suportada e verificar diagnóstico ou fallback correto.

## T098:C04 — perguntas_proveniencia

Pergunta: É outro algoritmo além de FlashAttention?
Resposta: Pode ser uma implementação diferente ou apenas um rótulo amplo; é necessário identificar o backend.

Pergunta: Diminui a memória dos pesos?
Resposta: Não diretamente. O foco é o cálculo de atenção e seus intermediários.

Pergunta: Menor pico de memória prova mesma função?
Resposta: Não. A implementação pode ter mudado precisão, máscara ou conexões; compare a operação e seus resultados.

Pergunta: Por que registrar fallback?
Resposta: Sem isso, uma configuração aparentemente otimizada pode executar outro kernel e invalidar a interpretação de desempenho.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T098:C05 — mecanismo_avancado

A escolha de backend faz parte do comportamento operacional: um dispatcher pode selecionar caminhos distintos conforme forma, máscara, dtype e dispositivo. A memória economizada precisa ser atribuída à eliminação de intermediários, à aproximação ou à alteração de precisão, porque essas decisões têm garantias diferentes. Na API funcional documentada do PyTorch, dropout depende do argumento fornecido, mesmo quando o módulo chamador está em avaliação.

Condição de contorno:
Comparações entre implementações perdem sentido se uma delas aplica dropout, máscara ou escala diferentes sem registro.

Contrato proposto:
- Entradas: Tensores, semântica explícita de máscara, escala, dropout e backends permitidos.
- Saídas: Saída e identificação observável da implementação escolhida.
- Estado: Configuração de despacho, compilação e temporários necessários.
- Invariante: Troca de backend preserva a operação contratada dentro da tolerância numérica definida.

Compromissos de projeto:
- Fallback amplia cobertura e pode alterar bruscamente memória e latência.
- Precisão de acumulação maior melhora estabilidade com possível custo de execução.

## T098:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: chamar o caminho funcional com módulo em avaliação e dropout não zero; depois corrigir o argumento. Esperar variabilidade no primeiro caso e consistência compatível com o backend no segundo.

Plano de avaliação proposto:
Plano proposto: usar formas representativas e limites de especialização, fixando máscaras e precisão. Medir pico de memória, fallback e erro numérico; comparar prefill e decode separadamente e aprovar somente o caminho realmente despachado.

Comparações:
- T090 (complements): FlashAttention pode ser um backend eficiente, mas o rótulo amplo não especifica qual algoritmo foi executado.

Afirmação rastreável:
A documentação funcional do PyTorch exige dropout_p igual a zero para desativar dropout durante avaliação.
Suporte: direct; fontes: B-S017
Limite: O detalhe é específico da API consultada; outras interfaces podem administrar esse argumento automaticamente.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T098:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 advertiu sobre dispatch e dropout. A expansão organiza uma camada de negociação de capacidades, um fallback explícito e uma matriz de testes de semântica, para que memory-efficient seja uma propriedade medida da execução completa.

Negociação antes de servir
Construa uma tabela de recursos exigidos pelo modelo e oferecidos por cada backend: GQA, máscaras, offsets, gradientes e formatos numéricos. Rejeite combinações impossíveis no carregamento. Um fallback aceitável deve ser explícito e observado, pois usar um caminho denso pode ultrapassar memória apesar de produzir resultados corretos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

Medição de pico e vida útil
Registre quando temporários são alocados e liberados em relação a KV, logits e comunicação. Economizar memória em uma operação não garante redução do pico global se outro buffer cresce ao mesmo tempo. Compare o perfil temporal, especialmente quando compilação, grafos ou múltiplas streams mantêm artefatos residentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

Semântica de máscaras
Use testes pequenos com resultados inspecionáveis para confirmar convenções de máscara, causalidade e escala. APIs distintas podem interpretar um booleano de modo diferente. Uma máscara válida por tipo pode inverter permissões sem erro; compare também atenção permitida em sequências unitárias, padding e fronteiras de documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

USO AVANÇADO — Backend portátil
Cenário: O mesmo produto precisa executar em CPU e diferentes GPUs.
Estratégia: Defina contrato de atenção independente do fornecedor, selecione implementação por capacidade e mantenha referência lenta para testes. Capture o backend efetivo nos logs. Não prometa números iguais entre dispositivos nem o mesmo conjunto de formatos.
Papel do modelo pequeno: Um 3–7B pode ter execução local simples; maiores modelos precisam de perfis de memória específicos.
Aceite proposto: Exigir ausência de fallback silencioso e qualidade consistente no conjunto de compatibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

USO AVANÇADO — Treino com margem apertada
Cenário: Um ajuste fino falha por pico de memória intermitente.
Estratégia: Meça vida útil de buffers e experimente atenção eficiente, checkpointing e limites de batch separadamente. Procure o pico verdadeiro antes de reduzir a tarefa. Se o fallback materializar matriz densa, trate-o como erro de configuração operacional.
Papel do modelo pequeno: Um 8–30B com adaptadores ainda precisa acomodar ativações e buffers da base.
Aceite proposto: Aprovar por redução do pico completo e estabilidade de passos com comprimentos extremos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S017, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, portabilidade e previsibilidade podem valer mais que um kernel especializado para um único acelerador.
8–14B: Em 8–14B, combinar métricas de pico com distribuição de contextos permite evitar OOMs esporádicos.
15–30B: Em 15–30B, avaliar buffers transitórios e comunicação, que podem consumir a margem liberada.
Requisitos de treino/runtime: Troca de implementação é runtime quando preserva a operação; aproximações ou máscaras novas mudam o contrato.
Não aplicar quando: Não escolher backend apenas pelo nome nem assumir que modo de avaliação desliga dropout em toda API funcional.

## T098:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Interface eficiente de atenção com caminhos especializados.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T098:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T098 → T090 [alternative]
Como combinar: Selecionar FlashAttention quando ele cobrir todos os requisitos e vencer na carga real.
Interface: Contrato de atenção, shapes e precisão.
Condição: Semântica é preservada e o kernel está disponível.
Aceite proposto: Comparar saída, pico global e tempo end-to-end.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S017, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T098 → T193 [complements]
Como combinar: Bloquear configuração incompatível antes que uma requisição alcance o acelerador.
Interface: Matriz de capacidades e manifesto do checkpoint.
Condição: Validação conhece os recursos obrigatórios.
Aceite proposto: Injetar combinações inválidas e exigir erro legível sem execução parcial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S017, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar convenções de máscara com casos mínimos de verdade conhecida.
- Registrar fallback e alocação de temporários em produção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar uma tarefa especializada em diferentes runtimes com a fronteira. Economia de memória pode viabilizar execução local; não transforma compatibilidade de API em equivalência de competência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T093, T113

## Fontes primárias associadas

### B-S017 — torch.nn.functional.scaled_dot_product_attention

[https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de implementações de atenção, máscaras e suporte dependente de backend.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

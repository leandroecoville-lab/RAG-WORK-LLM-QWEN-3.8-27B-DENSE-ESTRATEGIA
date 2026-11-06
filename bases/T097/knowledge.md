# T097 — Block-Sparse Attention

**Nome canônico:** Block-Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T097  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa por blocos

## T097:C01 — conceito

Atenção esparsa organizada em blocos de posições, permitindo pular regiões inteiras da matriz. A granularidade facilita kernels regulares, mas pode computar pares desnecessários dentro de um bloco mantido. Não se confunde com blocos de armazenamento KV usados por PagedAttention.

Como funciona:
- Particionar a matriz lógica em tiles e selecionar quais são atendidos.
- Executar cálculo somente nos tiles presentes, respeitando a máscara causal.
- Normalizar considerando todos os blocos selecionados para cada consulta.

## T097:C02 — aplicacao

Quando usar:
- Documentos com estrutura em segmentos ou dependências previsíveis.
- Backend possui kernels eficientes para o padrão de blocos.

Quando não usar:
- Usar uma matriz quase densa ou blocos muito pequenos que tornem o overhead dominante.

Implementação proposta:
- Escolher bloco conforme formas do kernel e padrões de acesso, não apenas limites de parágrafo.
- Registrar a máscara lógica e reproduzir o experimento com densidade controlada.
- Comparar com referência densa mascarada para validar semântica antes de medir velocidade.

Aplicação LAI proposta:
Proposta LAI: estudar para um modelo ou kernel que já suporte a técnica; priorizar ajustes de serving mais simples quando não houver justificativa arquitetural.

## T097:C03 — riscos_validacao

Armadilhas:
- Permitir um bloco parcialmente futuro sem máscara interna cria vazamento causal.
- Um bloco removido pode conter uma informação crítica isolada.

Métricas sugeridas:
- Percentual de blocos ativos e pares computados dentro deles.
- Tempo de atenção, acerto de tarefa e overhead de construir a máscara.

Testes propostos:
- Comparar saída com atenção densa usando a mesma máscara exata.
- Inserir tokens futuros em blocos de fronteira e confirmar que não afetam saídas anteriores.

## T097:C04 — perguntas_proveniencia

Pergunta: Blocos do KV tornam atenção esparsa?
Resposta: Não. Paginação pode armazenar atenção densa; sparsity define quais interações são calculadas.

Pergunta: Qual tamanho de bloco é melhor?
Resposta: Depende do kernel e padrão; mede-se equilíbrio entre trabalho redundante e overhead.

Pergunta: Mudar máscara sempre exige recompilar?
Resposta: Não necessariamente; mudar metadados e recompilar código são operações distintas, mas os metadados precisam representar o novo padrão.

Pergunta: Por que testar fronteiras de documentos?
Resposta: Um bloco parcialmente válido pode conter posições de documentos diferentes; marcá-lo como completo cria vazamento de contexto.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T097:C05 — mecanismo_avancado

A representação em blocos distingue regiões completamente excluídas, completamente presentes e parcialmente mascaradas. Essa classificação permite pular blocos e evitar testes individuais onde toda conexão é válida. O custo de construir a estrutura também importa: uma máscara que muda por exemplo ou camada precisa ser atualizada, enquanto uma máscara estável pode amortizar sua construção entre chamadas compatíveis.

Condição de contorno:
Esparsidade por elemento pode deixar quase todos os blocos parcialmente ocupados, produzindo pouca economia na granularidade escolhida.

Contrato proposto:
- Entradas: Predicado de conectividade, forma, tamanho de bloco e tensores de atenção.
- Saídas: Metadados de blocos e saída equivalente à máscara declarada.
- Estado: Versão do padrão, índices presentes e classificação de blocos parciais.
- Invariante: Reutilizar metadados somente quando a conectividade e as dimensões continuam compatíveis.

Compromissos de projeto:
- Blocos maiores reduzem metadados e podem desperdiçar cálculo dentro de blocos parciais.
- Construir padrões dinâmicos pode consumir o tempo economizado na atenção.

## T097:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reutilizar propositalmente uma máscara de documentos após trocar suas fronteiras. Esperar invalidação; comparar saída com referência que proíbe atenção entre documentos distintos.

Plano de avaliação proposto:
Plano proposto: medir construção e execução separadamente, variando densidade, regularidade e frequência de mudança. Usar máscara densa equivalente como controle; aprovar pelo tempo total amortizado e equivalência, não apenas pela fração de elementos removidos.

Comparações:
- T096 (specializes): Organiza as conexões esparsas em unidades adequadas aos kernels.

Afirmação rastreável:
FlexAttention usa BlockMask para identificar blocos puláveis e distinguir blocos completos dos parcialmente mascarados.
Suporte: direct; fontes: V3B-S008
Limite: A API documentada pode evoluir; o princípio não garante ganho para padrões arbitrários.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T097:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 classificou blocos presentes, ausentes e parciais. Aqui a estratégia avalia alinhamento documental, amortização de metadados e empacotamento, distinguindo economia no kernel de uma mudança semântica no que cada token pode consultar.

Alinhamento com documentos
Ao empacotar exemplos, mantenha fronteiras documentais independentes do tamanho físico do bloco. Um bloco pode atravessar duas sequências sem autorizar conexões entre elas; a máscara parcial deve preservar isolamento. Avalie o custo dos blocos de fronteira e compare com layouts que reduzem essas regiões parcialmente ocupadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

Reuso seguro de metadados
Armazene a máscara compilada somente quando forma e conectividade forem idênticas. Um template de mesma largura pode ter limites documentais diferentes. A chave precisa representar esses limites e versões do padrão; caso contrário, um cache de metadados rápido pode criar uma ligação que a tarefa nunca autorizou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

Planejamento de granularidade
Escolha tamanho de bloco em conjunto com distribuição de comprimentos e regularidade do padrão. Reduzir blocos pode revelar mais esparsidade, mas aumentar overhead de índices e scheduling. Faça comparação com o mesmo predicado de conectividade para isolar granularidade; mudar máscara e bloco ao mesmo tempo impede explicar o resultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

USO AVANÇADO — Treino com exemplos empacotados
Cenário: Muitos textos pequenos são combinados para ocupar melhor o acelerador.
Estratégia: Construa máscara por documento e comprimentos reais, compile padrões recorrentes e valide gradientes contra exemplos separados. Só depois ajuste granularidade e packing. Exclua qualquer ganho obtido por permitir atenção entre exemplos independentes.
Papel do modelo pequeno: Um 3–14B em ajuste fino pode reduzir desperdício sem aprender vazamento entre amostras.
Aceite proposto: Aceitar com isolamento comprovado, gradientes consistentes e menor custo por token útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

USO AVANÇADO — Inferência de estrutura modular
Cenário: Um documento contém grupos que podem atender a poucos outros grupos.
Estratégia: Codifique relações permitidas em blocos e preserve uma referência densa com a mesma máscara lógica. Meça custo de construção para cada nova estrutura; só mantenha cache quando houver revisitas suficientes.
Papel do modelo pequeno: Um 15–30B compatível pode explorar padrões regulares, mediante validação de qualidade e suporte.
Aceite proposto: Comparar tempo total por documento e falhas nas referências que cruzam blocos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S008, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preferir padrões simples que não adicionem um seletor mais caro que a atenção economizada.
8–14B: Em 8–14B, packing e máscaras documentais oferecem um problema concreto para avaliar granularidade.
15–30B: Em 15–30B, testar layouts produzidos por paralelismo e sua compatibilidade com o backend.
Requisitos de treino/runtime: Requer kernel que pule blocos; mudança do padrão de atenção exige pesos compatíveis ou adaptação validada.
Não aplicar quando: Não confundir blocos de computação esparsa com páginas físicas de cache KV.

## T097:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Máscaras por blocos representam esparsidade explorável pelo kernel.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T097:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T097 → T096 [complements]
Como combinar: Materializar um padrão esparso em representação que permita omitir trabalho.
Interface: Predicado de conexões, índices e blocos parciais.
Condição: A representação corresponde exatamente à máscara pretendida.
Aceite proposto: Comparar saída com referência densa mascarada e contar blocos processados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S008, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T097 → T090 [complements]
Como combinar: Usar execução em tiles para blocos presentes, preservando normalização sobre o conjunto permitido.
Interface: Blocos QKV e acumuladores de softmax.
Condição: Backend combina corretamente esparsidade e kernel fundido.
Aceite proposto: Testar linhas com poucos blocos e diferentes ordens de processamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S008, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Incluir documentos de comprimento não múltiplo do bloco.
- Invalidar metadados quando mudar qualquer fronteira de sequência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar capacidade e qualidade em documentos estruturados com a fronteira. A implementação pode reduzir custo de relações autorizadas; não demonstra que eliminar outras relações preserve qualquer tarefa aberta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T093, T096, T113

## Fontes primárias associadas

### B-S016 — Generating Long Sequences with Sparse Transformers

[https://arxiv.org/abs/1904.10509](https://arxiv.org/abs/1904.10509)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fatorações esparsas da atenção e kernels para sequências longas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S010 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

[https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atenção exata com blocos e menor tráfego entre memória da GPU e SRAM.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S008 — FlexAttention: The Flexibility of PyTorch with the Performance of FlashAttention

[https://pytorch.org/blog/flexattention/](https://pytorch.org/blog/flexattention/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: BlockMask, blocos completos/parciais e custo de construção da máscara.

Limite: Artigo oficial técnico; APIs e recomendações de compilação devem ser conferidas na versão instalada.

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

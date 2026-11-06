# T113 — FlashAttention Tiling

**Nome canônico:** FlashAttention Tiling  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T113  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** blocagem de FlashAttention

## T113:C01 — conceito

Decomposição em blocos usada dentro de implementações de FlashAttention para manter dados próximos do processamento e evitar a matriz completa em memória global. É um componente do algoritmo, não outra capacidade independente de recuperação ou compressão de conhecimento.

Como funciona:
- Escolher blocos de consultas e de chaves/valores que se ajustem aos recursos do kernel.
- Atualizar acumuladores e normalização enquanto percorre blocos.
- Gravar resultados consolidados em vez de intermediários completos de todos os pares.

## T113:C02 — aplicacao

Quando usar:
- Desenvolvimento ou análise de kernels de atenção.
- Diagnóstico de ocupação, tráfego de memória e limite de registradores.

Quando não usar:
- Alterar tamanho de bloco sem considerar dimensão de cabeça, dtype, máscara e recursos da GPU.

Implementação proposta:
- Usar implementação de referência e testes numéricos antes de autotuning.
- Varrer poucos tiles candidatos em formas representativas e separar custo de compilação.
- Registrar registradores, memória compartilhada e eventuais spills no profiler.

Aplicação LAI proposta:
Proposta LAI: manter como conhecimento para auditoria de performance; preferir kernels mantidos pelo runtime a patches locais sem necessidade comprovada.

## T113:C03 — riscos_validacao

Armadilhas:
- Tile grande pode exceder recursos e reduzir ocupação ou causar spills.
- Tile pequeno pode aumentar leitura redundante e número de iterações.

Métricas sugeridas:
- Bytes globais movimentados, ocupação e tempo de execução.
- Memória compartilhada, registradores por thread e erro numérico.

Testes propostos:
- Testar comprimentos que não são múltiplos do bloco e validar a máscara de fronteira.
- Comparar todas as configurações de tile com uma referência para evitar aceitar um ganho incorreto.

## T113:C04 — perguntas_proveniencia

Pergunta: Tiling é chunking de documento?
Resposta: Não. Divide operações numéricas dentro do kernel; o conteúdo lógico do prompt permanece igual.

Pergunta: Posso somar o ganho ao de FlashAttention?
Resposta: Não automaticamente. Tiling é parte do mecanismo que já produz aquele ganho.

Pergunta: Tiling torna a atenção esparsa?
Resposta: Não por si só. Todos os blocos permitidos ainda podem ser visitados; sparsity exige excluir conexões.

Pergunta: Por que testar strides não contíguos?
Resposta: Um kernel que pressupõe layout incorreto pode ler endereços errados mesmo com shapes aparentemente compatíveis.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T113:C05 — mecanismo_avancado

Os tiles de consulta e de chave podem ter tamanhos diferentes porque seus papéis no reúso são distintos. O acumulador de saída e estatísticas de normalização precisam sobreviver ao percurso dos blocos KV. Nas bordas, posições físicas extras devem ser mascaradas sem afetar máximos e somas. A disposição dos dados também influencia coalescência e pressão de registradores, além do simples número de operações.

Condição de contorno:
Um tile que cabe nominalmente em memória compartilhada pode executar mal por registradores, sincronização ou baixa ocupação.

Contrato proposto:
- Entradas: Formas QKV, strides, máscara e dimensões dos tiles.
- Saídas: Blocos de saída consolidados e estatísticas necessárias ao backward quando aplicável.
- Estado: Acumuladores persistentes no kernel e buffers temporários com limites válidos.
- Invariante: Padding de tile nunca entra no normalizador nem contribui para a saída.

Compromissos de projeto:
- Tiles maiores aumentam reúso e podem reduzir paralelismo residente.
- Layouts especializados melhoram acesso e podem exigir conversões antes da atenção.

## T113:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar sequências com comprimento um acima e um abaixo do múltiplo do tile, preenchendo padding com valores extremos. Esperar saída independente desses valores inválidos.

Plano de avaliação proposto:
Plano proposto: comparar configurações com entradas, precisão e máscara fixas. Medir duração incluindo conversão de layout, memória temporária e correção nas bordas; selecionar por famílias de formas, evitando assumir um tile ótimo para todo serviço.

Comparações:
- T114 (complements): A normalização incremental permite combinar contribuições dos tiles sem armazenar todos os scores.

Afirmação rastreável:
O tutorial oficial de atenção fundida do Triton percorre blocos KV enquanto atualiza acumuladores de saída e normalização.
Suporte: direct; fontes: B-S027
Limite: O exemplo é uma implementação didática otimizada; configurações adequadas dependem de dispositivo e versão.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T113:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou tiles e acumuladores. Esta camada liga a escolha de tile ao regime de execução, aos limites de compilação e à validação de formas que não aparecem nos casos ideais.

Tile dependente da fase
Prefill oferece muitas consultas; decode frequentemente possui poucas consultas e KV crescente. Um tamanho favorável ao primeiro pode deixar pouca ocupação no segundo. Selecione variantes por forma e dtype, considerando cabeças agrupadas e comprimentos reais, em vez de fixar uma configuração por número de parâmetros do modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

Reúso versus recursos locais
Aumentar tile pode reduzir leituras repetidas e elevar uso de registradores ou memória compartilhada. Esse consumo pode reduzir blocos residentes e causar spills. O resultado é uma curva de compromisso; a melhor configuração não se deduz somente de quantos bytes deixam de ir para a memória global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

Compilação e variedade
Formas variáveis podem produzir múltiplas especializações e custo de compilação. Defina classes de comprimento e um caminho correto para casos raros. O aquecimento precisa cobrir classes relevantes; uma medida que exclui todo custo de compilação não descreve pedidos ocasionais nem atualização frequente do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Serviço com duas fases dominantes
Cenário: Documentos longos geram respostas curtas.
Estratégia: Escolha variantes para prefill e decode separadamente e acompanhe transição entre elas. Evite otimizar decode quase inexistente enquanto prefill ocupa a maior parte do pedido.
Papel do modelo pequeno: Um 8–14B pode oferecer leitura especializada com uma política de kernels adequada às formas.
Aceite proposto: Reduzir tempo da fase dominante mantendo logits dentro da tolerância definida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Auditoria de kernel customizado
Cenário: Uma implementação promete economia superior ao backend padrão.
Estratégia: Teste comprimentos não múltiplos, masks, strides e grupos KV. Compare com referência simples e depois avalie carga representativa.
Papel do modelo pequeno: Um 3–7B facilita exploração, mas os testes devem incluir dimensões reais do checkpoint alvo.
Aceite proposto: Nenhum ganho é aceito antes de passar bordas e equivalência numérica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S027, V3B-S006, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Overhead de lançamento e compilação pode superar economia em sequências curtas.
8–14B: Varie contexto e lote para encontrar pontos de transição entre variantes.
15–30B: Considere competição por recursos locais com comunicação e outros kernels, quando presentes.
Requisitos de treino/runtime: Otimização de runtime, sem treino se a operação for preservada. Backend e GPU precisam suportar a variante.
Não aplicar quando: Não tratar tiling como sparse attention: todos os pares permitidos podem continuar sendo calculados.

## T113:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q020, V4B-Q005.

## T113:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T113 → T114 [requires]
Como combinar: Estatísticas de softmax permitem combinar tiles sem materializar a matriz inteira.
Interface: Máximos, somas e numeradores parciais.
Condição: Mesma máscara e escala em todas as parcelas.
Aceite proposto: Comparar combinação em ordens diferentes sob tolerância numérica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S027, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T113 → T107 [complements]
Como combinar: Profiling verifica se maior tile reduz tráfego sem criar spills ou baixa ocupação.
Interface: Contadores e tempo por forma.
Condição: Medições do mesmo kernel e dispositivo.
Aceite proposto: Demonstrar efeito no tempo do pedido, além do microbenchmark.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S027, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar linhas totalmente mascaradas conforme a semântica declarada do backend.
- Fixar versão do compilador e registrar seleção efetiva de kernel.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Tiling não muda a capacidade cognitiva do modelo. Na comparação com fronteira, seu efeito aparece no custo e na latência de uma tarefa cuja qualidade já foi medida separadamente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T114, T097

## Fontes primárias associadas

### B-S027 — Fused Attention

[https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html](https://triton-lang.org/main/getting-started/tutorials/06-fused-attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de referência de atenção em blocos com kernel fundido.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S006 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning — full text

[https://arxiv.org/html/2307.08691v1](https://arxiv.org/html/2307.08691v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento entre blocos e warps, custo de operações não matriciais.

Limite: Texto técnico consultado; velocidade depende de formas, dtype e arquitetura do dispositivo.

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

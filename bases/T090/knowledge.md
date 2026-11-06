# T090 — FlashAttention

**Nome canônico:** FlashAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T090  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção com otimização de IO

## T090:C01 — conceito

Algoritmo de atenção exata que reorganiza cálculo e acesso à memória para evitar materializar toda a matriz de atenção na memória global. Usa blocos e estados intermediários compactos. Na versão densa, continua calculando as interações exigidas pela atenção; economia de memória não transforma automaticamente o custo aritmético quadrático em linear.

Como funciona:
- Carregar blocos de consultas, chaves e valores em memória mais próxima do processamento.
- Acumular resultados com normalização estável sem guardar todos os scores globais.
- Escrever a saída consolidada e apenas os intermediários necessários.

## T090:C02 — aplicacao

Quando usar:
- Atenção ocupa parcela relevante do custo com sequências longas.
- Backend e dimensões do modelo são suportados pelo kernel.

Quando não usar:
- Esperar ganho relevante quando o gargalo dominante está em rede, ferramentas ou outras camadas.

Implementação proposta:
- Confirmar pelo profiler qual kernel foi escolhido; não confiar apenas na flag.
- Comparar com atenção de referência usando mesma máscara e precisão.
- Medir prefill, decode e memória de pico separadamente para o tamanho real da carga.

Aplicação LAI proposta:
Proposta LAI: verificar se o runtime já usa atenção otimizada antes de propor uma segunda instalação; medir contribuição no tempo total da missão.

## T090:C03 — riscos_validacao

Armadilhas:
- Exato matematicamente não significa bit a bit igual, devido à ordem das operações em ponto flutuante.
- Pedir todos os pesos de atenção pode exigir outro caminho e eliminar parte da economia.

Métricas sugeridas:
- Tempo de kernel e bytes de memória global movimentados.
- Memória de pico e diferença numérica da saída contra referência.

Testes propostos:
- Cobrir máscaras causais, padding e comprimentos não múltiplos do bloco; exigir erro numérico limitado.
- Verificar que entradas não suportadas falham claramente ou usam fallback conhecido.

## T090:C04 — perguntas_proveniencia

Pergunta: FlashAttention é atenção esparsa?
Resposta: A versão densa original é exata e não remove pares de tokens; variantes esparsas são uma extensão distinta.

Pergunta: Dobra automaticamente a velocidade?
Resposta: Não. O ganho depende do kernel, formas, hardware e parcela da atenção no custo total.

Pergunta: Cabe menos matriz intermediária significa menos cache KV?
Resposta: Não necessariamente. Intermediários de atenção e estados persistentes KV são parcelas diferentes.

Pergunta: Pode validar apenas perplexidade?
Resposta: Não. Compare também saídas e máscaras em casos controlados; qualidade agregada pode ocultar um erro de fronteira.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T090:C05 — mecanismo_avancado

A economia central aparece quando a matriz de probabilidades de atenção deixa de ser gravada integralmente na memória externa. Isso reduz intermediários e tráfego, mas não transforma atenção densa em uma operação linear no comprimento. No treinamento, estratégias de recomputação podem reconstruir intermediários no backward; na inferência, o benefício depende da forma das consultas, especialmente da diferença entre prefill com muitas consultas e decode com poucas.

Condição de contorno:
Exatidão algorítmica permite diferenças de ponto flutuante decorrentes da ordem das reduções; não implica identidade bit a bit.

Contrato proposto:
- Entradas: Q, K, V, máscara, escala e regra de dropout explicitamente definidas.
- Saídas: Saída equivalente à atenção especificada e, quando aplicável, gradientes.
- Estado: Acumuladores de normalização e blocos temporários, sem matriz global persistente.
- Invariante: Toda posição permitida participa da normalização; nenhuma posição proibida contribui.

Compromissos de projeto:
- Menos tráfego externo pode exigir recomputar valores no backward.
- Um kernel rápido em prefill pode não ser o melhor para consultas unitárias.

## T090:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar com referência de alta precisão em logits extremos, máscara causal e comprimentos não múltiplos do tile. Esperar ausência de vazamento futuro e erros compatíveis com o dtype escolhido.

Plano de avaliação proposto:
Plano proposto: controlar forma, máscara, dtype e dropout; medir memória intermediária, tráfego e duração separada de forward e backward. Aprovar pela equivalência numérica e benefício no caminho efetivamente utilizado, incluindo custos de despacho.

Comparações:
- T096 (distinct_from): Sparsity muda quais interações existem; FlashAttention pode executar a atenção densa original.

Afirmação rastreável:
FlashAttention reduz acessos entre memória externa e memória próxima ao processamento por uma execução consciente de IO.
Suporte: direct; fontes: B-S010
Limite: O artigo não garante aceleração universal nem remove o custo aritmético quadrático da atenção densa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T090:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou economia de intermediários e diferença prefill/decode. A nova camada trata seleção de backend como contrato de compatibilidade, validação numérica e atribuição causal de ganhos, evitando avaliar um kernel isolado e prometer desempenho de serviço.

Contrato completo do operador
Liste máscara causal, offsets, comprimentos variáveis, dimensão de cabeça, dtype e política de dropout antes de trocar backend. Verifique se o executor selecionou o kernel esperado ou fez fallback. Uma API com o mesmo nome pode escolher caminhos diferentes conforme a forma; registre essa decisão no ensaio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

Equivalência útil à tarefa
Compare saídas e, no treinamento, gradientes com uma referência apropriada. Pequenas diferenças numéricas são esperadas por ordem de redução; o limite aceitável depende da precisão e do uso. Além do erro tensorial, teste se classificações ou campos sensíveis mudam, sobretudo perto de empates entre tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

Benefício além do kernel
Separe tempo de atenção de tokenização, projeções, comunicação e sampling. O ganho total é limitado pela parcela otimizada. Quando a memória liberada permitir lote maior, faça um segundo experimento: o primeiro mede troca de kernel, o segundo mede a nova configuração de serviço, preservando atribuição clara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

USO AVANÇADO — Prefill de documentos extensos
Cenário: O processamento de entrada domina o tempo inicial.
Estratégia: Escolha um backend compatível, aqueça compilação e varie comprimentos reais. Preserve o mesmo padrão de atenção. Depois avalie se memória liberada pode servir mais pedidos sem piorar a cauda do decode.
Papel do modelo pequeno: Um 3–30B de atenção densa pode aproveitar a implementação sem alterar pesos, quando suportado.
Aceite proposto: Aceitar somente com erro dentro da tolerância e ganho end-to-end, incluindo fallback.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

USO AVANÇADO — Ajuste fino com contexto longo
Cenário: Ativações de atenção limitam o microbatch.
Estratégia: Valide backward, máscaras de padding e fronteiras entre exemplos empacotados. Aumente microbatch somente após comparar gradientes com a configuração original. Meça memória no pico do treino inteiro, não apenas durante atenção.
Papel do modelo pequeno: Um 8–14B com adaptadores pode ganhar margem de ativações, sem reduzir a memória da base automaticamente.
Aceite proposto: Exigir estabilidade de treinamento e ausência de atenção entre exemplos independentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S010, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, outros operadores podem dominar; confirmar que atenção ocupa parcela relevante antes de otimizar.
8–14B: Em 8–14B, ganhos de memória podem facilitar contexto ou microbatch, avaliados separadamente.
15–30B: Em 15–30B, verificar coexistência com quantização, paralelismo e kernels de decode específicos.
Requisitos de treino/runtime: Troca de kernel é runtime quando semântica é preservada; suporte ao backward e arquitetura precisa ser confirmado.
Não aplicar quando: Não usar uma máscara esparsa nova como se fosse apenas substituição exata de implementação.

## T090:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C018 — PyTorch / FlexAttention para inferência
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: As publicações documentam recursos utilizáveis de FlexAttention, incluindo atenção em decode, GQA, cache paginado e backend FlashAttention-4 para hardware especificado.
Mecanismo documentado: Modificações de scores e máscaras são compiladas para caminhos especializados; comportamento e elegibilidade dependem do backend.
Correspondência com esta base: Relaciona implementação da família FlashAttention; FA4 não prova adoção específica de FA1, FA2 ou FA3.
Transferência proposta para modelo pequeno: Proposta: executar equivalência de máscara e logits para o checkpoint 3–30B e depois avaliar formas reais de prefill/decode.
Limite: Disponibilidade documentada não demonstra implantação de bigtech nem suporte ao dispositivo local. Não transportar resultados de kernels entre arquiteturas de GPU.
Fontes: V4B-S017, V4B-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T090:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T090 → T107 [complements]
Como combinar: Medir quanto tráfego e tempo de atenção representam no caminho crítico.
Interface: Perfil por operador e bytes de intermediários.
Condição: Formas e precisão são idênticas na comparação.
Aceite proposto: Relacionar ganho local ao limite de ganho total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S010, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T090 → T115 [complements]
Como combinar: Combinar redução de intermediários com recomputação seletiva no treinamento.
Interface: Política de checkpoint e operadores de atenção recompostos.
Condição: Backward e RNG são preservados.
Aceite proposto: Comparar memória de pico e tempo por passo com gradientes equivalentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S010, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar fallback de backend como resultado, não excluí-lo.
- Testar padding, offsets causais e sequências de comprimento extremo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo de uma tarefa com fronteira mantendo qualidade fixa. FlashAttention melhora execução de atenção existente; não amplia o conhecimento nem transforma contexto numericamente suportado em compreensão confiável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T091, T092, T097, T098, T113, T114

## Fontes primárias associadas

### B-S010 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

[https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atenção exata com blocos e menor tráfego entre memória da GPU e SRAM.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

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

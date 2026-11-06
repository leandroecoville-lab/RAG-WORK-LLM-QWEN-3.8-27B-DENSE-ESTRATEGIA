# T096 — Sparse Attention

**Nome canônico:** Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T096  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa

## T096:C01 — conceito

Família de padrões que calcula atenção apenas sobre parte dos pares possíveis de posições. A seleção pode ser local, fixa, por blocos ou dependente do conteúdo. Economia aritmética teórica só vira menor tempo quando o kernel evita efetivamente o trabalho omitido.

Como funciona:
- Definir uma conectividade esparsa entre consultas e chaves.
- Calcular e normalizar scores apenas sobre posições permitidas.
- Propagar informação pelas conexões restantes e pela profundidade do modelo.

## T096:C02 — aplicacao

Quando usar:
- Sequências longas permitem explorar estrutura de dependências.
- Existe checkpoint ou procedimento validado para o padrão escolhido.

Quando não usar:
- Aplicar máscara esparsa em kernel que ainda calcula toda a matriz e esperar aceleração automática.

Implementação proposta:
- Especificar padrão, densidade, limites de conexão e necessidade de treinamento.
- Comparar tempo real e qualidade contra atenção densa no mesmo regime.
- Avaliar casos em que a informação importante está em posições raras ou distantes.

Aplicação LAI proposta:
Proposta LAI: tratar atenção esparsa como escolha de arquitetura ou backend especializado, não como otimização universal que a Helena ativa por prompt.

## T096:C03 — riscos_validacao

Armadilhas:
- Remover conexões pode eliminar a única rota útil para uma evidência.
- Operações irregulares podem perder eficiência apesar de fazerem menos multiplicações.

Métricas sugeridas:
- Densidade de pares atendidos e tempo de kernel.
- Acerto por distância e tipo de dependência no documento.

Testes propostos:
- Construir tarefa com evidência distante e medir falhas conforme a densidade diminui.
- Perfil de execução deve mostrar trabalho reduzido, não apenas valores mascarados depois do cálculo.

## T096:C04 — perguntas_proveniencia

Pergunta: Sparse Attention é sinônimo de FlashAttention?
Resposta: Não. A primeira reduz conectividade; a versão densa de FlashAttention reorganiza a mesma atenção.

Pergunta: Menos FLOPs garante menor latência?
Resposta: Não. Acesso irregular, seleção e overhead podem anular a economia.

Pergunta: Muitos pesos próximos de zero bastam para acelerar?
Resposta: Não se o kernel ainda calcula todos os scores e executa a mesma redução densa.

Pergunta: O resultado esparso pode ser exato?
Resposta: Sim em relação à máscara declarada; isso não o torna idêntico à atenção original sem essa máscara.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T096:C05 — mecanismo_avancado

Esparsidade tem dois significados que precisam ser separados: pesos de atenção pequenos após softmax e conexões deliberadamente ausentes antes da normalização. Apenas o segundo define um padrão de cálculo que pode dispensar operações. Zerar valores depois de calcular a matriz densa não recupera o custo já pago. Além disso, normalizar sobre um subconjunto produz outra distribuição, salvo casos especiais de contribuição originalmente nula.

Condição de contorno:
Um padrão com poucas conexões pode executar lentamente se sua irregularidade impedir agrupamento eficiente ou exigir seleção cara.

Contrato proposto:
- Entradas: Padrão permitido, tensores QKV, máscara causal e regra para linhas sem conexões.
- Saídas: Saída normalizada apenas sobre posições admitidas pelo padrão.
- Estado: Índices ou estrutura do padrão e metadados necessários ao kernel.
- Invariante: A exclusão ocorre antes da normalização e respeita as restrições causais.

Compromissos de projeto:
- Conectividade menor economiza trabalho e restringe rotas de informação.
- Padrões regulares favorecem kernels, mas podem representar pior dependências específicas.

## T096:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: excluir uma chave com score dominante e comparar referência densa mascarada com kernel esparso. Também criar linha totalmente excluída e exigir comportamento definido, sem NaNs silenciosos.

Plano de avaliação proposto:
Plano proposto: comparar kernel esparso com máscara densa equivalente para correção, depois avaliar contra modelo de conectividade completa para qualidade. Medir custo de seleção, execução e tarefa final; aprovar somente a troca explicitamente escolhida.

Comparações:
- T090 (distinct_from): Atenção exata eficiente em IO pode preservar todas as conexões; sparsity seleciona quais permanecem.

Afirmação rastreável:
Longformer combina atenção local e global para oferecer uma estrutura esparsa de conexões.
Suporte: direct; fontes: B-S015
Limite: A fonte sustenta esse padrão específico, não a preservação de qualidade para qualquer poda.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T096:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu conexões ausentes de pesos pequenos. O novo desenho exige escolher um grafo de comunicação adequado à tarefa, contabilizar o seletor e avaliar adaptação dos pesos, tornando explícito quando esparsidade é arquitetura e quando é aproximação experimental.

Cobertura do grafo
Analise se o padrão permite que dependências relevantes se encontrem ao longo das camadas. Um grafo conectado teoricamente pode ainda exigir muitos passos ou comprimir informação em poucos intermediários. Crie testes de ponte entre seções e compare padrões com o mesmo número aproximado de conexões, evitando avaliar somente tamanho de contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

Custo antes da atenção
Inclua construção de índices, seleção, ordenação e movimentação de dados na medição. Um padrão barato no papel pode produzir acessos irregulares ou gastar muito para decidir o que ignorar. Registre economia efetiva de operações e bytes separadamente, usando o mesmo kernel denso como referência sem alterar outras otimizações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

Adaptação e regressão
Se a máscara não faz parte do treinamento original, trate a mudança como nova variante do modelo. Compare sem adaptação e com treino adicional quando houver recursos e dados autorizados. Preserve um conjunto de tarefas com dependências raras para impedir que a redução média de custo esconda perda sistemática de informação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

USO AVANÇADO — Documentos com estrutura previsível
Cenário: Seções possuem vínculos locais e algumas referências globais conhecidas.
Estratégia: Desenhe uma máscara por blocos/seções, preserve conexões de referência e verifique ausência de acesso futuro. Use um protótipo para medir viabilidade antes de treinar. Se precisar construir matriz densa para escolher conexões, contabilize esse custo integral.
Papel do modelo pequeno: Um 3–14B pode ser adaptado ao domínio, mas não recebe a capacidade apenas por trocar uma flag.
Aceite proposto: Aceitar por qualidade em dependências cruzadas e redução end-to-end, incluindo construção da máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

USO AVANÇADO — Pesquisa de contexto extenso
Cenário: O objetivo é explorar arquitetura dentro de orçamento limitado.
Estratégia: Compare padrões local, global e conteúdo-dependente com dados e compute controlados. Registre custo de treino e inferência. Não apresentar um único checkpoint melhor em um benchmark como superioridade causal de toda a família esparsa.
Papel do modelo pequeno: Um 15–30B pode ser candidato experimental se treino e kernels forem viáveis.
Aceite proposto: Exigir avaliações fora do domínio de ajuste e relatório das relações que deixaram de ser recuperadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, B-S016, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, a capacidade representacional menor recomenda padrões simples e tarefas delimitadas antes de seleção complexa.
8–14B: Em 8–14B, investigar padrões estruturados com kernels regulares e avaliação de longo alcance.
15–30B: Em 15–30B, incluir custo de treinamento/adaptação e integração distribuída no orçamento de projeto.
Requisitos de treino/runtime: Arquitetura esparsa normalmente exige pesos compatíveis; esparsificação pós-treino é aproximação a validar.
Não aplicar quando: Não zerar scores após cálculo denso e apresentar isso como economia aritmética de sparse attention.

## T096:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T096:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T096 → T097 [complements]
Como combinar: Organizar conectividade em blocos para que o executor possa pular regiões inteiras.
Interface: Máscara lógica e índices de blocos presentes.
Condição: Padrão mantém esparsidade também na granularidade física.
Aceite proposto: Comparar conexões úteis, blocos processados e tempo total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, B-S016, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T096 → T110 [complements]
Como combinar: Adicionar canais globais limitados para dependências que a vizinhança não cobre.
Interface: Posições globais e regra de seleção.
Condição: Causalidade e treinamento autorizam essas conexões.
Aceite proposto: Testar relações distantes e crescimento do custo ao aumentar globais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, B-S016, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Relatar custo do seletor e casos sem ganho real.
- Não confundir conectividade teórica com recuperação fiel de detalhes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve abranger tarefas locais e globais, mantendo transparência sobre treino adicional. Esparsidade pode ampliar contexto viável; não garante compreensão equivalente do conteúdo removido.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T097, T111, T112

## Fontes primárias associadas

### B-S016 — Generating Long Sequences with Sparse Transformers

[https://arxiv.org/abs/1904.10509](https://arxiv.org/abs/1904.10509)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fatorações esparsas da atenção e kernels para sequências longas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

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

# T111 — Dynamic Sparse Attention

**Nome canônico:** Dynamic Sparse Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T111  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção esparsa dinâmica

## T111:C01 — conceito

Família de atenção esparsa cuja seleção de posições depende do conteúdo ou do estado da execução. Em vez de uma máscara fixa, um roteador ou seletor decide quais interações calcular. Routing Transformer é uma referência específica, não a definição de todas as variantes.

Como funciona:
- Produzir sinais de seleção a partir de consultas, chaves ou representações compactas.
- Escolher grupos ou posições relevantes para cada consulta.
- Calcular atenção somente no conjunto selecionado e contabilizar custo de seleção.

## T111:C02 — aplicacao

Quando usar:
- Conteúdo relevante muda muito entre entradas longas.
- Há método validado cujo seletor é mais barato que a atenção evitada.

Quando não usar:
- Seletor precisa calcular todos os scores caros para descobrir quais scores deveria evitar.

Implementação proposta:
- Definir orçamento de posições e política para incluir conexões essenciais.
- Comparar com máscara fixa de igual custo para demonstrar valor do dinamismo.
- Avaliar seleção fora da distribuição de treino e o efeito de entradas adversas.

Aplicação LAI proposta:
Proposta LAI: tratar como pesquisa ou backend especializado; primeiro exigir ganho demonstrado sobre mecanismos estáticos mais simples.

## T111:C03 — riscos_validacao

Armadilhas:
- Erros de seleção retiram evidências antes de o modelo poder usá-las.
- Agrupamentos desequilibrados podem gerar picos de memória e trabalho.

Métricas sugeridas:
- Tempo do seletor, densidade e equilíbrio de grupos.
- Recall de posições úteis e qualidade final frente à atenção de referência.

Testes propostos:
- Inserir uma evidência rara mas decisiva e verificar se o seletor a preserva.
- Medir custo total em entradas repetitivas e aleatórias, incluindo o roteamento.

## T111:C04 — perguntas_proveniencia

Pergunta: É o mesmo que escolher documentos por RAG?
Resposta: Não. Opera nas conexões internas de atenção, embora ambos selecionem informação.

Pergunta: Exige sempre retreinar?
Resposta: Depende da variante; modelos com roteador aprendido e métodos de poda em inferência têm requisitos distintos.

Pergunta: Top-k após scores densos elimina O(n²)?
Resposta: Não o custo de produzir esses scores; é necessário examinar onde a seleção realmente acontece.

Pergunta: Mais confiança do roteador prova relevância?
Resposta: Não. Compare candidatos selecionados com evidência necessária e avalie falhas por mudança de domínio.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T111:C05 — mecanismo_avancado

O custo de selecionar conexões integra o orçamento da atenção. Um seletor que calcula todos os produtos QK antes de escolher top-k pode economizar armazenamento posterior sem eliminar o cálculo denso inicial. Roteamento por agrupamentos procura evitar essa etapa, mas enfrenta grupos desequilibrados e seleção instável: pequenas alterações de representação podem mover uma chave entre conjuntos e mudar abruptamente o contexto consultado.

Condição de contorno:
A seleção baseada em conteúdo pode perder uma evidência importante sem produzir erro de execução ou sinal explícito de baixa confiança.

Contrato proposto:
- Entradas: Representações para seleção, capacidade dos grupos e restrições causais.
- Saídas: Conjunto de conexões selecionadas e atenção normalizada nesse conjunto.
- Estado: Centroides ou índice, alocações de grupos e metadados de capacidade.
- Invariante: A seleção e a atenção usam posições compatíveis e não introduzem acesso futuro.

Compromissos de projeto:
- Seleção adaptativa pode encontrar dependências distantes e custa computação própria.
- Limitar capacidade controla memória e pode descartar candidatos relevantes.

## T111:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar um grupo muito popular e colocar evidência rara em sua fronteira. Perturbar levemente a consulta e verificar estabilidade, candidatos perdidos e comportamento ao exceder capacidade.

Plano de avaliação proposto:
Plano proposto: comparar padrão fixo, seleção dinâmica e referência densa com o mesmo orçamento declarado. Separar tempo de roteamento e atenção; medir cobertura da evidência, qualidade e distribuição de tamanhos de grupos.

Comparações:
- T097 (complements): Seleção dinâmica pode produzir blocos, mas o custo de construir seus metadados precisa ser contabilizado.

Afirmação rastreável:
Routing Transformer aprende padrões esparsos dependentes do conteúdo usando um módulo baseado em k-means online.
Suporte: direct; fontes: B-S025
Limite: Essa realização não define todas as técnicas de atenção dinâmica nem garante seleção ótima.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T111:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou custo de seleção e instabilidade dos grupos. Esta camada acrescenta distribuição do orçamento de conexões, sinais de omissão e avaliação separada do seletor e do operador de atenção.

Orçamento por consulta
Dar o mesmo número de conexões a cada consulta pode desperdiçar trabalho em regiões previsíveis e faltar em relações difíceis. Uma política adaptativa precisa estimar dificuldade sem calcular a atenção densa inteira. Defina um limite máximo e contabilize custo do estimador, roteamento, ordenação e padding, não apenas dos produtos finalmente selecionados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

Omissão versus cálculo
Uma resposta pode falhar porque a chave relevante não foi selecionada ou porque o modelo não usou corretamente uma chave acessível. Em um conjunto pequeno, compare conexões selecionadas com uma referência densa e meça cobertura da evidência anotada. Esse diagnóstico orienta aumentar orçamento, mudar seletor ou revisar treinamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

Robustez de distribuição
Agrupamentos aprendidos em textos comuns podem se comportar diferente em código, números ou documentos multilíngues. Teste desequilíbrio, grupos vazios e concentração adversarial de tokens. Uma política de capacidade deve declarar se descarta, reroteia ou amplia processamento quando um grupo excede o limite; essas escolhas alteram custo e semântica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

USO AVANÇADO — Leitura longa especializada
Cenário: O domínio possui dependências recorrentes que podem ser aprendidas.
Estratégia: Treine ou adapte um seletor compatível, mantenha uma amostra densa de controle e compare qualidade por tipo de relação. Use fallback quando sinais operacionais mostram saturação.
Papel do modelo pequeno: Um 8–14B pode explorar sparsity treinada em tarefas bem delimitadas.
Aceite proposto: O seletor deve manter cobertura de evidência enquanto reduz trabalho total medido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

USO AVANÇADO — Investigação de latência irregular
Cenário: Poucos pedidos geram picos apesar de tamanho semelhante.
Estratégia: Correlacione distribuição de grupos, quantidade de conexões e temporários. Separe desbalanceamento do seletor de problemas do kernel ou da fila.
Papel do modelo pequeno: Um 15–30B exige orçamento por dispositivo, inclusive para grupos excepcionais.
Aceite proposto: Reproduzir os picos com entradas controladas e confirmar a causa antes de alterar a máscara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S025, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma implementação dinâmica pode custar mais que atenção densa otimizada em sequências pequenas.
8–14B: O benefício depende de contexto longo e seletor barato, não somente do porte do modelo.
15–30B: Considere memória de índices e buffers, além da matriz de atenção evitada.
Requisitos de treino/runtime: Seleção arquitetural geralmente exige treinamento; substituir arbitrariamente a atenção de um checkpoint é aproximação a validar.
Não aplicar quando: Não apresentar redução de conexões como aceleração se o seletor ou padding dominam o tempo.

## T111:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T111:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T111 → T097 [feeds]
Como combinar: Conexões selecionadas são convertidas em blocos processáveis.
Interface: Índices, ocupação e máscaras de borda.
Condição: A conversão não amplia indevidamente o campo visível.
Aceite proposto: Comparar lista lógica e máscara realmente executada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S025, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T111 → T107 [complements]
Como combinar: Profiling mede seleção, movimentação e computação conjuntamente.
Interface: Tempo por fase e bytes transportados.
Condição: Mesmo conjunto de consultas e contexto.
Aceite proposto: Confirmar redução no caminho crítico, não apenas em FLOPs estimados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S025, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Incluir casos raros em que uma única chave distante determina a resposta.
- Registrar descartes por capacidade como intervenção semântica, não detalhe invisível.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare com fronteira em documentos com evidência marcada e dependências variadas. Sparsity pode economizar execução e simultaneamente perder relações; a avaliação deve tornar essa troca visível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T096, T097, T112

## Fontes primárias associadas

### B-S025 — Efficient Content-Based Sparse Attention with Routing Transformers

[https://arxiv.org/abs/2003.05997](https://arxiv.org/abs/2003.05997)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento esparso dependente do conteúdo com agrupamento online.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

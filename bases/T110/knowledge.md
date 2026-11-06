# T110 — Global Token Attention

**Nome canônico:** Global Token Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T110  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção em tokens globais

## T110:C01 — conceito

Padrão em que algumas posições selecionadas têm conexões de alcance amplo, complementando atenção local. No Longformer, tokens definidos conforme a tarefa participam de atenção global. Isso difere de dar atenção plena a todos os pares e de declarar uma instrução prioritária no prompt.

Como funciona:
- Selecionar posições especiais que precisam reunir ou distribuir informação.
- Adicionar conexões globais à máscara local de acordo com a arquitetura.
- Manter limites causais quando o modelo for um decoder autorregressivo.

## T110:C02 — aplicacao

Quando usar:
- Arquitetura foi treinada com tokens globais para classificação, pergunta ou estrutura documental.
- Poucos pontos de agregação podem conectar segmentos distantes.

Quando não usar:
- Marcar arbitrariamente tokens como globais em um checkpoint sem implementação ou treino correspondente.

Implementação proposta:
- Definir regra de seleção dependente da tarefa e manter seu número limitado.
- Avaliar posições de perguntas, títulos ou marcadores com um conjunto separado.
- Inspecionar máscara para impedir que uma conexão global burle causalidade.

Aplicação LAI proposta:
Proposta LAI: estudar como escolha de arquitetura; não confundir com inserir palavras especiais que supostamente aumentariam a atenção do Qwen por instrução.

## T110:C03 — riscos_validacao

Armadilhas:
- Muitos tokens globais aproximam o custo da atenção densa.
- Um token global pode virar gargalo de representação e não preservar todos os detalhes.

Métricas sugeridas:
- Quantidade de tokens globais e custo adicional por sequência.
- Acerto em dependências entre segmentos e sensibilidade à seleção de posições.

Testes propostos:
- Comparar apenas atenção local com local mais posições globais em tarefa de evidência distante.
- No modo causal, perturbar futuro e verificar ausência de influência em saídas anteriores.

## T110:C04 — perguntas_proveniencia

Pergunta: Token global significa maior prioridade de instrução?
Resposta: Não. Descreve conexões de atenção da arquitetura, não autoridade de uma mensagem.

Pergunta: Todo modelo permite isso por máscara?
Resposta: Não. Há requisitos de arquitetura, implementação e treinamento.

Pergunta: Token global é uma instrução prioritária?
Resposta: Não. Global descreve conexões de atenção, enquanto prioridade de instruções depende de treinamento e comportamento do sistema.

Pergunta: Uma camada permite todos trocarem informação via global?
Resposta: As atualizações usam estados da camada anterior; reunir e redistribuir informação pode exigir etapas sucessivas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T110:C05 — mecanismo_avancado

Um token global pode reunir informação distante e distribuí-la em camadas seguintes, encurtando caminhos no grafo de atenção. Isso não torna automaticamente todos os pares diretamente conectados na mesma camada. Com n tokens, janela de alcance w e g posições globais, o número de conexões pode ser modelado por O(nw+ng), conforme a máscara. Se g cresce proporcionalmente a n, a economia pode desaparecer.

Condição de contorno:
A interpretação bidirecional típica de encoders não pode ser transplantada para geração causal permitindo acesso a informação futura.

Contrato proposto:
- Entradas: Posições globais selecionadas, máscara local, direção permitida e tensores do modelo.
- Saídas: Representações que combinam caminhos locais e globais autorizados.
- Estado: Identidade das posições globais e regra de seleção específica da tarefa.
- Invariante: A seleção global nunca elimina restrições causais ou documentais exigidas.

Compromissos de projeto:
- Mais posições globais ampliam conectividade e custo.
- Escolhas fixas simplificam execução, mas podem concentrar informação em poucos estados.

## T110:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: marcar como global uma posição futura num decoder e perturbar seu conteúdo. A implementação causal correta deve impedir influência sobre logits anteriores.

Plano de avaliação proposto:
Plano proposto: comparar diferentes seleções globais com custo e treinamento controlados. Medir qualidade por distância da evidência, memória e tempo; usar referência mascarada para verificar conectividade antes de atribuir ganhos ao mecanismo.

Comparações:
- T109 (complements): Conexões globais acrescentam rotas longas a uma base local.

Afirmação rastreável:
Longformer usa atenção global motivada pela tarefa junto da janela local.
Suporte: direct; fontes: B-S015
Limite: A relação de complexidade é uma modelagem da conectividade; não prevê tempo de kernel nem garante transmissão fiel de fatos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T110:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou caminhos e complexidade dos tokens globais. Esta camada examina seleção de posições, capacidade de agregação e avaliação de gargalos que permanecem mesmo com conectividade ampla.

Seleção orientada à tarefa
Escolher posições globais é uma decisão de representação: pergunta, delimitadores ou resumos podem ter papéis diferentes. Defina a regra antes da avaliação e teste mudanças na posição dos fatos. Escolher globais depois de conhecer a resposta produz uma vantagem artificial que não estará disponível durante uso real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

Gargalo de agregação
Poucos tokens globais precisam condensar muitas relações. Acesso ao documento inteiro não garante retenção de todos os detalhes: largura e treinamento limitam o que é transmitido. Aumentar posições globais pode reduzir esse gargalo, mas acrescenta computação e memória; procure um compromisso medido na tarefa concreta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

Direção e causalidade
Em geração autoregressiva, uma posição global também deve obedecer à disponibilidade temporal. Uma máscara bidirecional de encoder não pode ser transferida diretamente para decoder. Para streaming, especifique quando um resumo global é atualizado e se tokens posteriores dependem de sua versão antiga ou nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

USO AVANÇADO — Pergunta sobre documento longo
Cenário: Uma arquitetura compatível precisa relacionar seções distantes.
Estratégia: Designe a pergunta e marcadores estruturais como candidatos globais, mantendo a seleção independente da resposta. Compare com recuperação segmentada sob o mesmo orçamento.
Papel do modelo pequeno: Um 8–14B treinado para o padrão pode executar leitura especializada com menos conexões que atenção densa.
Aceite proposto: Testar resposta, localização da evidência e resistência a trechos irrelevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

USO AVANÇADO — Síntese de fluxo delimitado
Cenário: Eventos locais precisam alimentar um estado resumido.
Estratégia: Use posições de agregação apenas na arquitetura que permita atualizá-las corretamente; fora dela, implemente resumo externo explícito, sem apresentar essa alternativa como o mesmo mecanismo.
Papel do modelo pequeno: Um 3–7B pode manter sínteses de domínio estreito apoiadas em registros originais.
Aceite proposto: Medir quais fatos deixam de sobreviver quando aumenta o número de eventos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucos globais podem virar gargalo severo; comece com tarefas de baixa entropia e evidência curta.
8–14B: Explore seleção estrutural e número de globais separadamente, evitando trocar vários fatores ao mesmo tempo.
15–30B: Maior capacidade não elimina crescimento de custo quando a quantidade de globais acompanha o contexto.
Requisitos de treino/runtime: Exige modelo e máscara compatíveis; adicionar um token especial ao prompt de um LLM comum não cria atenção global arquitetural.
Não aplicar quando: Não prometer cobertura integral apenas porque existe um caminho no grafo de atenção.

## T110:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T110:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T110 → T109 [complements]
Como combinar: Conexões globais suplementam vizinhanças locais na arquitetura prevista.
Interface: Máscaras por camada e posições selecionadas.
Condição: Treinamento e inferência compartilham semântica.
Aceite proposto: Testar fronteiras, causalidade e relações distantes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T110 → T097 [complements]
Como combinar: Blocos podem representar o padrão misto e evitar materialização densa.
Interface: Metadados de blocos locais e globais.
Condição: Granularidade não introduz conexões proibidas.
Aceite proposto: Comparar máscara realizada com a máscara de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não selecionar tokens globais usando rótulos ou informação da resposta.
- Registrar crescimento do número de conexões quando aumentar a quantidade de globais.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve avaliar relações distantes e detalhes omitidos, não somente tamanho aceito de entrada. Conectividade e compreensão são propriedades distintas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T109, T096

## Fontes primárias associadas

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

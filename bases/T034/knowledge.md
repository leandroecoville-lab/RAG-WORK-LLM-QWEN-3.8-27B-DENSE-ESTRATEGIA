# T034 — Agentic Chunking

**Nome canônico:** Agentic Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T034  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação por agente

## T034:C01 — conceito

Rótulo amplo para usar uma LLM ou um agente na definição de unidades de conhecimento, fronteiras ou agrupamentos durante a ingestão. Não designa um algoritmo universal. Precisa distinguir seleção de trechos originais de geração de novas proposições, pois a segunda pode introduzir informação falsa.

Como funciona:
- Fornecer unidades iniciais e um contrato de segmentação.
- Solicitar fronteiras ou agrupamentos com referências à origem.
- Validar cobertura, tamanho e fidelidade antes de indexar.

Nota de nomenclatura: Termo descritivo sem implementação única identificada; fontes fornecem os conceitos de segmentação relacionados, não validam um método exclusivo.

## T034:C02 — aplicacao

Quando usar:
- Acervos heterogêneos cujo layout não fornece boa estrutura.
- Prototipagem de unidades conceituais difíceis de obter com regras simples.

Quando não usar:
- Não adotar sem controle de custo e verificação quando ingestão determinística já atende às perguntas.

Implementação proposta:
- Proposta: pedir offsets ou IDs existentes, evitando reescrita livre da fonte.
- Validar que cada unidade citada pertence ao documento e que não há lacunas.
- Separar proposições geradas das passagens originais no índice.

Aplicação LAI proposta:
Proposta LAI: reservar para bases teóricas complexas em experimento isolado; manter divisão estrutural como comparação de menor custo.

## T034:C03 — riscos_validacao

Armadilhas:
- A LLM pode agrupar fatos incompatíveis ou criar uma conexão inexistente.
- Resultados variáveis dificultam reproduzir atualizações e depurar recuperação.

Métricas sugeridas:
- Cobertura e fidelidade dos trechos.
- Custo por documento e ganho de recall frente ao splitter convencional.

Testes propostos:
- Executar duas vezes o mesmo documento e medir estabilidade.
- Inserir instrução maliciosa no texto e exigir que seja tratada como dado, sem mudar o segmentador.

## T034:C04 — perguntas_proveniencia

Pergunta: Usar um agente para dividir texto torna o RAG melhor?
Resposta: Não automaticamente. O ganho depende de perguntas reais, e a ingestão pode ficar mais cara e menos previsível.

Pergunta: Posso indexar fatos reescritos como originais?
Resposta: Não. Marque-os como derivados e mantenha as fontes correspondentes.

Pergunta: Toda proposição precisa repetir o nome da entidade?
Resposta: Precisa ser interpretável na recuperação. Uma referência estruturada pode cumprir esse papel sem repetir texto, desde que o leitor a resolva.

Pergunta: Como atualizar uma proposição após correção da fonte?
Resposta: Recalcule as derivadas dependentes da revisão alterada. Similaridade de texto não basta para detectar quais relações ficaram inválidas.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T034:C05 — mecanismo_avancado

Há duas decisões distintas sob esse rótulo: escolher fronteiras entre segmentos existentes e produzir proposições independentes. A segunda resolve pronomes e combina contexto, mas cria texto novo. Sua validação deve verificar sustentação e escopo: sujeito, quantificador, modalidade e condição temporal. Uma proposição curta pode ter boa recuperabilidade e ainda inverter a conclusão por remover uma palavra como “pode”.

Condição de contorno:
A extração proposicional é arriscada quando interpretação depende de ironia, discordância entre participantes ou condições distribuídas em várias partes do documento.

Contrato proposto:
- Entradas: Segmentos identificados, contexto necessário e contrato indicando seleção literal ou derivação.
- Saídas: Grupos de offsets ou proposições marcadas como derivadas, cada uma ligada às evidências.
- Estado: Modelo, instrução, revisões documentais e resultados de verificações de sustentação.
- Invariante: Uma reescrita nunca recebe automaticamente o mesmo status de uma afirmação literal da fonte.

Compromissos de projeto:
- Proposições autocontidas facilitam localização de fatos específicos, mas aumentam tamanho do índice e custo de ingestão.
- Verificação adicional reduz erros de derivação; pode anular a economia obtida na geração final.

## T034:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: apresentar falas contraditórias de dois autores e uma hipótese condicional. A extração deve preservar atribuição, discordância e modalidade, sem fundi-las numa afirmação categórica.

Plano de avaliação proposto:
Avaliação proposta: comparar chunks estruturais, fronteiras escolhidas por modelo e proposições derivadas com mesmo corpus. Medir recall, fidelidade por proposição, expansão do índice e custo de atualização; inspecionar separadamente erros de atribuição e negação.

Comparações:
- T033 (alternative): Estrutura formal fornece fronteiras sem exigir que um modelo reconstrua cada afirmação.
- T054 (complements): Proposições validadas podem alimentar memória semântica, mantendo proveniência e grau de confirmação.

Afirmação rastreável:
Dense X Retrieval investiga proposições autocontidas como unidade de recuperação, comparando granularidades de indexação.
Suporte: related; fontes: V3A-S012
Limite: A fonte sustenta uma abordagem proposicional, não padroniza todos os métodos chamados Agentic Chunking.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T034:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou fronteiras e proposições. Aqui decisões do agente sobre segmentação ficam sujeitas a estabilidade e custo de revisão.

Projeto e decomposição
O agente deve escolher entre fronteiras candidatas produzidas por regras, não inventar livremente texto derivado. Isso limita variação e preserva alinhamento com origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

Controle adaptativo
Registre justificativa de fronteira por dependência: mudança de assunto, entidade ou escopo. Repetir a segmentação com pequena edição deve modificar apenas regiões justificáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

Validação contrafactual
Compare splitter determinístico e agente com orçamento de chamadas igualado por corpus. Meça recuperação, estabilidade de IDs, custo de ingestão e taxa de fronteiras que separam condição e consequência. Unidade de avaliação: documento segmentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

USO AVANÇADO — Documentos heterogêneos
Cenário: Seções misturam FAQ e narrativa.
Estratégia: Classificar região e selecionar política de divisão específica; usar julgamento do agente somente em fronteiras ambíguas.
Papel do modelo pequeno: 3–7B classifica tipos; 8–14B decide bordas.
Aceite proposto: Nenhuma condição essencial deve ficar sem referência ao trecho dependente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

USO AVANÇADO — Notas de pesquisa
Cenário: Uma observação interrompe tópico e retorna depois.
Estratégia: Criar segmentos por unidade argumentativa e relações de continuidade; não fundir trechos distantes sem registrar origem.
Papel do modelo pequeno: 15–30B identifica dependências complexas.
Aceite proposto: Cada segmento deve ser reconstruível a partir de intervalos explícitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de região com conjunto fechado de políticas.
8–14B: Árbitro de poucas fronteiras ambíguas, com justificativa curta.
15–30B: Analista de continuidade argumentativa em documentos difíceis.
Requisitos de treino/runtime: Candidatos de fronteira, alinhamento por offsets e orçamento de ingestão; decisão estocástica precisa versão registrada.
Não aplicar quando: Conteúdo é homogêneo e splitter simples tem qualidade equivalente com custo muito menor.

## T034:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q022.

## T034:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T034 → T033 [requires]
Como combinar: Detectar estruturas antes da escolha pelo agente.
Interface: Blocos protegidos e cortes permitidos.
Condição: Agente não poder romper unidade obrigatória.
Aceite proposto: Testar tabela e bloco de código que parecem mudar de tema.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S012, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T034 → T072 [feeds]
Como combinar: Versionar decisões de segmentação.
Interface: Modelo, prompt, fronteiras e revisão documental.
Condição: Reindexação preservar histórico de referência.
Aceite proposto: Repetir ingestão e medir mudança injustificada de IDs.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S012, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar reescrita de texto de simples chunking.
- Comparar fronteiras com origem, não só com fluência dos segmentos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar benefício marginal sobre regras; usar modelo maior na ingestão só se o ganho persistir na leitura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T011, T033, T195

## Fontes primárias associadas

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S041 — Semantic splitter

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de parsers semânticos e janelas de sentenças.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S012 — Dense X Retrieval: What Retrieval Granularity Should We Use?

[https://arxiv.org/abs/2312.06648](https://arxiv.org/abs/2312.06648)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Granularidade de recuperação e proposições autossuficientes como unidades de indexação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

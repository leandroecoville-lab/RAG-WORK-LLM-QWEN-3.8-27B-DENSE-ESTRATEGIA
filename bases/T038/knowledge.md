# T038 — Selective Context Pruning

**Nome canônico:** Selective Context Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda seletiva de contexto; Selective Context

## T038:C01 — conceito

Poda seletiva de contexto com base em uma medida de importância ou informação. É uma especialização de Context Pruning; Selective Context é também o nome de uma proposta de pesquisa sobre remoção de redundância. O critério concreto de seleção deve ser declarado, sem tratar todo texto previsível como dispensável.

Como funciona:
- Dividir o contexto em unidades selecionáveis.
- Atribuir pontuações segundo o método escolhido.
- Remover unidades abaixo do orçamento preservando dependências obrigatórias.

Nota de nomenclatura: Entrada mantida como variante do conceito geral T018; o método científico específico deve ser citado pelo título da fonte.

## T038:C02 — aplicacao

Quando usar:
- Entradas com passagens repetidas e baixa densidade informativa.
- Experimentos controlados de redução de prompt.

Quando não usar:
- Não excluir automaticamente frases comuns que expressem negação ou restrição essencial.

Implementação proposta:
- Proposta: registrar o seletor usado e os trechos removidos.
- Criar lista de invariantes que não podem desaparecer.
- Comparar poda por informação, por relevância e por regras em perguntas independentes.

Aplicação LAI proposta:
Proposta LAI: empregar inicialmente como opção de seleção auditável em documentação; não usar para descartar autorização, identificação de cliente ou decisão vigente.

## T038:C03 — riscos_validacao

Armadilhas:
- Previsibilidade estatística não equivale a inutilidade para a tarefa.
- Pontuação local pode ignorar relações entre frases distantes.

Métricas sugeridas:
- Retenção de invariantes e perda de qualidade.
- Razão de compressão e latência total.

Testes propostos:
- Inserir uma restrição em frase comum e exigir sua preservação.
- Avaliar casos em que a resposta depende de dois trechos cuja utilidade aparece somente em conjunto.

## T038:C04 — perguntas_proveniencia

Pergunta: Selective Context e qualquer poda seletiva são sinônimos exatos?
Resposta: Não. Um é uma proposta específica; o outro é um rótulo geral para várias políticas.

Pergunta: Um seletor pode ser usado sem treinamento?
Resposta: Sim. Há regras e escores que não exigem treinar o gerador, mas ainda precisam de avaliação.

Pergunta: Somar surpresa favorece unidades longas?
Resposta: Pode favorecer: a soma cresce com o número de tokens. A comparação precisa declarar agregação, tamanho e limiar utilizados.

Pergunta: LLMLingua-2 aplica exatamente o mesmo critério?
Resposta: Não. Formula retenção como classificação de tokens com aprendizado supervisionado e informação bidirecional; não é apenas outro limiar sobre surpresa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T038:C05 — mecanismo_avancado

No método Selective Context, a informação de um token é sua surpresa sob um modelo: I(x) = −log₂ P(x | prefixo), em bits. Pontuações podem ser agregadas em unidades lexicais antes do descarte. Isso mede improbabilidade contextual, não valor causal para a resposta. Uma condição previsível pode ter baixo escore, enquanto um erro de digitação raro recebe pontuação elevada.

Condição de contorno:
A transferência falha quando o modelo que estima probabilidades trata linguagem técnica ou idioma de forma muito diferente do gerador que lerá o resultado.

Contrato proposto:
- Entradas: Texto tokenizado, modelo de pontuação, unidade selecionável e orçamento de retenção.
- Saídas: Máscara de seleção com offsets, pontuações e motivos de preservação obrigatória.
- Estado: Tokenizer, definição de agregação, limiar e contexto usado no cálculo das probabilidades.
- Invariante: Uma unidade removida por baixa surpresa não é declarada semanticamente dispensável sem avaliação da tarefa.

Compromissos de projeto:
- Unidades maiores preservam sintaxe e tornam a seleção menos granular.
- Pontuação probabilística dispensa treinar o gerador, mas acrescenta inferência e pode privilegiar ruído incomum.

## T038:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma restrição frequente junto de códigos aleatórios sem utilidade. A avaliação deve revelar se a política prefere o ruído; regras obrigatórias precisam impedir a perda da restrição.

Plano de avaliação proposto:
Avaliação proposta: comparar surpresa, seleção por relevância e LLMLingua-2 sob o mesmo orçamento final. Medir retenção de condições, resposta sustentada, custo do seletor e degradação por idioma; controlar o tamanho das unidades para não atribuir seu efeito ao escore.

Comparações:
- T018 (specializes): O registro preserva a associação ao conceito geral de poda, detalhando um critério informacional específico.
- T020 (distinct_from): Um seletor treinado com rótulos de retenção aprende outra função; surpresa não equivale a probabilidade de relevância.

Afirmação rastreável:
Selective Context calcula auto-informação com um modelo causal e usa unidades lexicais para reduzir conteúdo considerado redundante.
Suporte: direct; fontes: A-S016
Limite: A interpretação como importância operacional é uma hipótese adicional; o artigo não transforma previsibilidade em garantia de inutilidade.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T038:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou surprisal e alias de poda. Aqui a seleção é estratificada por função textual para evitar viés contra unidades previsíveis.

Projeto e decomposição
Negações, unidades e operadores podem ser previsíveis linguisticamente e decisivos semanticamente. Separe seleção de tokens livres e proteção de classes funcionais relevantes à tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

Controle adaptativo
Calibre dentro de tipos de conteúdo, evitando que código, nomes raros ou OCR dominem score por surpresa. Alta perplexidade pode sinalizar ruído, não valor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

Validação contrafactual
Compare seleção global e estratificada com mesmo número de tokens. Meça perda de relação, erro em negação e excesso de ruído preservado; o alvo é utilidade do leitor, não surpresa média. Unidade de avaliação: bloco selecionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

USO AVANÇADO — Especificação com fórmulas
Cenário: Símbolos curtos mudam condições.
Estratégia: Proteger operadores e unidades, selecionar explicação por relevância e verificar fórmula completa após compressão.
Papel do modelo pequeno: 3–7B lê estrutura validada.
Aceite proposto: Expressão resultante deve manter equivalência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

USO AVANÇADO — Texto com OCR imperfeito
Cenário: Ruído recebe score elevado.
Estratégia: Detectar regiões suspeitas, conferir imagem ou original e impedir que a seleção priorize lixo por raridade.
Papel do modelo pequeno: 8–14B interpreta trecho corrigido.
Aceite proposto: Não aumentar taxa de erro por preservar caracteres corrompidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de spans com operadores protegidos por regras.
8–14B: Classificador de conteúdo útil versus ruído antes da seleção.
15–30B: Revisor de relações complexas quando poda por token for insuficiente.
Requisitos de treino/runtime: Tags funcionais e amostra de validação por tipo; manter relação com T018 como especialização, não algoritmo universal novo.
Não aplicar quando: Proteções ocupam quase toda janela ou linguagem comprimida fica ilegível para o consumidor.

## T038:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Seleção de tokens pertence à família; mecanismo específico depende da versão.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T038:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T038 → T018 [complements]
Como combinar: Usar estratos como política específica de poda.
Interface: Token, classe funcional, dependência e score.
Condição: Poda preservar fechamento das relações.
Aceite proposto: Testar frase previsível cuja negação muda a decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V3A-S001, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T038 → T195 [complements]
Como combinar: Verificar expressão ou código após seleção.
Interface: Representação original e selecionada.
Condição: Existir propriedade executável adequada.
Aceite proposto: Detectar mudança de operador apesar de formato válido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V3A-S001, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar raridade como sinônimo de importância.
- Não tratar LLMLingua-2 e Selective Context como mesmo estimador.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar preservação de relações com tokens iguais; score do compressor não mede compreensão do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T018, T039

## Fontes primárias associadas

### A-S016 — Compressing Context to Enhance Inference Efficiency of Large Language Models

[https://aclanthology.org/2023.emnlp-main.391/](https://aclanthology.org/2023.emnlp-main.391/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Selective Context: remoção de redundância no contexto de entrada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S027 — LLMLingua Prompt Compression — Prompt flow

[https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração documentada de compressor e contrato de entrada/saída; não comprova carga real.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

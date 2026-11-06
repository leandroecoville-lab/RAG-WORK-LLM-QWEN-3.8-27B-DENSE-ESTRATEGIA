# R005 — LLMLingua

**Nome canônico:** LLMLingua — compressão de prompts em múltiplas etapas  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** LLM Lingua; compressor de prompt; prompt compression LLMLingua

## R005:C01 — conceito

Método de compressão de prompts que combina controle de orçamento e seleção iterativa de conteúdo. O texto comprimido continua sendo fornecido ao modelo alvo. A ficha usa o artigo original como referência e distingue LongLLMLingua, uma extensão voltada a cenários de contexto longo.

Como funciona:
- Definir quanto contexto pode ser preservado no orçamento.
- Avaliar conteúdo e aplicar compressão em etapas para reduzir redundância.
- Executar o modelo alvo com o resultado comprimido e comparar a tarefa final.

Nota de nomenclatura: LLMLingua pode designar uma família de ferramentas. As variantes têm mecanismos e requisitos próprios; esta ficha não trata todas como um único algoritmo.

## R005:C02 — aplicacao

Quando usar:
- Prompts extensos e repetitivos cujo custo de processamento domina o fluxo.
- Tarefas com conjunto de avaliação que permita detectar perda de informação relevante.

Quando não usar:
- Quando cada caractere de um contrato, código ou registro precisa ser preservado literalmente sem perda.

Implementação proposta:
- Proposta: fixar versão do compressor, tokenizer e modelo alvo.
- Experimentar razões de compressão conservadoras antes de elevar a redução.
- Comparar qualidade, latência total e custo, incluindo o compressor e a recuperação das fontes originais.

Aplicação LAI proposta:
Proposta LAI: experimentar em históricos repetitivos e documentos recuperados; manter instruções obrigatórias e campos exatos fora de uma compressão destrutiva.

## R005:C03 — riscos_validacao

Armadilhas:
- Uma pequena exclusão pode remover negação, unidade, condição ou nome decisivo.
- A redução de tokens não garante menor latência se o compressor custar mais que o prefill economizado.

Métricas sugeridas:
- Razão entre tokens antes e depois, medida pelo tokenizer do destino.
- Variação de acurácia e tempo completo da chamada, incluindo compressão.

Testes propostos:
- Proposta: incluir pares que diferem apenas por uma negação e verificar que a resposta mantém a distinção.
- Comparar prompts originais e comprimidos em dados reservados, sem aceitar economia acompanhada de erro crítico.

## R005:C04 — perguntas_proveniencia

Pergunta: LLMLingua é Context Distillation?
Resposta: Não são equivalentes. Aqui a redução é aplicada ao texto enviado; a destilação paramétrica treina comportamento nos pesos ou adaptadores.

Pergunta: Posso adotar a maior razão publicada?
Resposta: Não automaticamente. O limite aceitável depende de tarefa, idioma, modelo e custo dos erros.

Pergunta: O gerador precisa ler texto perfeitamente gramatical?
Resposta: Nem sempre, mas a tarefa precisa conservar sentido suficiente. Aparência estranha não prova perda, e texto fluente não prova fidelidade.

Pergunta: A taxa configurada é a economia final da aplicação?
Resposta: Não. Some compressor, reprocessamento, overhead e possíveis releituras. O custo líquido depende do uso real e da qualidade preservada.

Escopo das fontes:
A-S015 sustenta os componentes do método original; A-S018 identifica LongLLMLingua. Não foram reproduzidos seus benchmarks nem afirmados ganhos específicos para o Qwen.

## R005:C05 — mecanismo_avancado

O LLMLingua original combina controle de orçamento, compressão iterativa de tokens e alinhamento de distribuição entre modelos. O repositório atual reúne variantes com mecanismos diferentes: LongLLMLingua condiciona a tarefa de contexto longo, enquanto LLMLingua-2 usa classificação aprendida de tokens. Reproduzir um resultado exige registrar variante, checkpoint e configuração; citar apenas o nome do pacote não identifica o método executado.

Condição de contorno:
A redução de tokens pode deixar de compensar quando o custo do compressor domina ou quando detalhes removidos provocam novas buscas e geração adicional.

Contrato proposto:
- Entradas: Prompt estruturado, orçamento, variante escolhida e trechos que não podem ser comprimidos.
- Saídas: Texto reduzido, métricas de tamanho e referências ao original para validar conteúdo preservado.
- Estado: Checkpoint do compressor, tokenizer, parâmetros e versões do gerador consumidor.
- Invariante: Preservar uma palavra ou símbolo não é tratado como garantia de preservar a relação lógica da frase.

Compromissos de projeto:
- Compressão extrativa conserva partes do original e pode quebrar relações entre elas.
- Seções protegidas reduzem risco de perder contratos e limitam a compressão máxima alcançável.

## R005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: proteger os tokens de uma condição, mas permitir remoção da ligação entre condição e consequência. A verificação deve detectar a mudança semântica apesar de todas as palavras protegidas continuarem presentes.

Plano de avaliação proposto:
Avaliação proposta: comparar prompt integral, seleção por passagem e variante específica do LLMLingua com mesmo gerador. Medir sustentação, preservação de exceções, custo do compressor e latência total; incluir taxas de compressão graduais, sem presumir um ganho fixo.

Comparações:
- T037 (complements): Condicionamento à pergunta é relevante em variantes apropriadas, mas não define todos os métodos do pacote.
- R006 (distinct_from): LLMLingua entrega contexto reduzido ao gerador; PRISM transfere comportamento para adaptadores treinados.

Afirmação rastreável:
O artigo original descreve compressão coarse-to-fine; o repositório distingue variantes e documenta preservação de tokens e seções.
Suporte: direct; fontes: A-S015, V3A-S044
Limite: Opções de uma variante não devem ser atribuídas automaticamente às demais; a pesquisa não executou o pacote.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciou variantes LLMLingua. Aqui a seleção de variante depende do consumidor e do perfil de carga, com teste de robustez de leitura.

Projeto e decomposição
Escolha entre compressão orientada à consulta e independente da tarefa conforme reutilização prevista. Um corpus consultado de muitas formas pode não amortizar recompressão específica por pergunta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

Controle adaptativo
Avalie legibilidade funcional para cada leitor 3–30B. O fato de um modelo grande interpretar tokens selecionados não prova que um modelo menor preserve relações, negações e referências.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

Validação contrafactual
Compare variantes com taxa efetiva e custo completo, incluindo compressor, leitura e expansão de recuperação. Meça qualidade por tipo de informação, não apenas compressão média. Unidade de avaliação: pipeline compressor-leitor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

USO AVANÇADO — RAG local de baixa latência
Cenário: Documentos retornados são redundantes.
Estratégia: Usar compressor leve após recuperação, proteger campos decisivos e encaminhar original quando teste de suporte falhar.
Papel do modelo pequeno: 3–7B lê pacote conservador.
Aceite proposto: Não reduzir latência sacrificando unidade, negação ou fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

USO AVANÇADO — Análise recorrente de dossiê
Cenário: Várias perguntas usam o mesmo material.
Estratégia: Comparar representação geral reutilizada com compressão por pergunta; manter original e medir custo acumulado por sessão.
Papel do modelo pequeno: 8–14B integra; 15–30B audita casos difíceis.
Aceite proposto: Escolher variante por custo por resposta aceita, não por taxa anunciada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de compressão moderada com relações explícitas e recuperação de fallback.
8–14B: Leitor de texto mais denso após validação de fidelidade contextual.
15–30B: Professor ou auditor de preservação, sem presumir comportamento igual entre modelos.
Requisitos de treino/runtime: Versão exata da biblioteca e compressor, tokenizer do leitor e dados próprios de avaliação; integração Prompt flow é disponibilidade.
Não aplicar quando: Compressão custa mais que leitura ou produz texto que o consumidor não interpreta com confiabilidade.

## R005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Integração do projeto identificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Variante da família, distinta do original.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## R005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R005 → T037 [complements]
Como combinar: Condicionar seleção à pergunta quando variante suportar.
Interface: Pergunta, trechos e taxa efetiva.
Condição: Objetivo permanecer estável durante reuso.
Aceite proposto: Trocar pergunta e testar perda de evidência relevante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028, V3A-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R005 → T042 [requires]
Como combinar: Contar contexto final e reserva do consumidor.
Interface: Tokens após compressão, metadados e saída prevista.
Condição: Contagem usar protocolo do leitor.
Aceite proposto: Comparar taxa solicitada e redução efetiva em tokens.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028, V3A-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar integração em biblioteca de produção comprovada.
- Não transportar ganhos publicados para todo modelo pequeno.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar pipeline completo com leitura integral; compressor eficiente pode piorar um consumidor menos robusto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T020, T037, T018

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S018 — LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression

[https://arxiv.org/abs/2310.06839](https://arxiv.org/abs/2310.06839)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão voltada à informação relevante em contextos longos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S044 — LLMLingua official implementation

[https://github.com/microsoft/LLMLingua](https://github.com/microsoft/LLMLingua)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenciação das variantes LLMLingua, LongLLMLingua e LLMLingua-2; opções de preservação e compressão estruturada documentadas no README.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V4A-S027 — LLMLingua Prompt Compression — Prompt flow

[https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração documentada de compressor e contrato de entrada/saída; não comprova carga real.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

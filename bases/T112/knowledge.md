# T112 — Retrieval-Based Attention

**Nome canônico:** Retrieval-Based Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T112  
**Data da curadoria:** 2026-11-05

## T112:C01 — conceito

Termo amplo para mecanismos em que recuperação seleciona representações consultadas pela atenção. Pode designar memória interna recuperável ou arquiteturas como RETRO, que usam trechos externos com cross-attention. É necessário identificar a variante; anexar documentos ao prompt por RAG não equivale a modificar a atenção.

Como funciona:
- Construir consulta e recuperar candidatos de um índice de representações.
- Codificar ou preparar os candidatos para o mecanismo de atenção.
- Combinar a informação recuperada com os estados do modelo no ponto previsto pela arquitetura.

Nota de nomenclatura: RETRO é exemplo documentado. O registro não identifica toda a família com uma implementação específica.

## T112:C02 — aplicacao

Quando usar:
- Modelo e runtime foram projetados para integrar recuperação internamente.
- Pesquisa compara memória recuperável com ampliar parâmetros ou contexto.

Quando não usar:
- Presumir que qualquer checkpoint aceita cross-attention adicional sem treino e novos pesos.

Implementação proposta:
- Especificar se a memória é externa, KV interno ou blocos codificados.
- Versionar retriever, corpus e modelo conjuntamente para reproduzir resultados.
- Comparar com RAG textual convencional antes de adotar integração mais profunda.

Aplicação LAI proposta:
Proposta LAI: começar pelo RAG externo deste pacote; tratar atenção baseada em recuperação como opção arquitetural que exige integração e avaliação próprias.

## T112:C03 — riscos_validacao

Armadilhas:
- Erro do retriever pode excluir informações necessárias antes da geração.
- Atualizar o índice pode mudar a distribuição dos conteúdos vistos pela arquitetura treinada.

Métricas sugeridas:
- Recall dos candidatos e latência de recuperação.
- Qualidade final, custo de atenção adicional e sensibilidade a corpus desatualizado.

Testes propostos:
- Retirar a evidência correta do índice e verificar comportamento de abstinência ou degradação explícita.
- Trocar o corpus mantendo modelo fixo e medir impacto em tarefas previamente corretas.

## T112:C04 — perguntas_proveniencia

Pergunta: RETRO é igual a colocar texto recuperado no prompt?
Resposta: Não. Sua arquitetura inclui recuperação, codificação e cross-attention por trechos.

Pergunta: O nome descreve um único algoritmo?
Resposta: Não. É uma família; cada implementação deve informar o que recupera e onde usa a informação.

Pergunta: Mudar o banco atualiza os pesos?
Resposta: Não. Atualiza memória externa; o modelo ainda depende de suas capacidades treinadas de utilizar o material recuperado.

Pergunta: Boa recuperação garante resposta correta?
Resposta: Não. O conteúdo pode ser mal interpretado, e o índice também pode conter evidência conflitante ou desatualizada.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T112:C05 — mecanismo_avancado

Recuperar conteúdo para uma camada de atenção requer compatibilidade entre índice, codificador e mecanismo que consome seus estados. Atualizar somente os documentos pode mudar distribuição e latência; atualizar embeddings sem reconstruir o índice pode quebrar a correspondência geométrica. No RETRO, recuperação externa participa de uma arquitetura com codificação e cross-attention por trechos, portanto não equivale a anexar texto a um modelo convencional.

Condição de contorno:
A recuperação pode falhar mesmo quando a cross-attention é correta; o modelo não consegue atender a candidatos que o índice deixou de fornecer.

Contrato proposto:
- Entradas: Consulta de recuperação, índice versionado, candidatos e codificador compatível.
- Saídas: Representações externas e sua integração nos pontos previstos da arquitetura.
- Estado: Versões de corpus, embeddings, índice e política de atualização.
- Invariante: Cada candidato mantém proveniência e correspondência com a versão usada para codificá-lo.

Compromissos de projeto:
- Memória externa amplia conteúdo acessível e adiciona consulta, codificação e transporte.
- Mais candidatos aumentam cobertura e custo, podendo introduzir material irrelevante.

## T112:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o codificador das consultas mantendo o índice antigo e inserir documentos duplicados. Esperar detecção de incompatibilidade e avaliação explícita da perda de cobertura.

Plano de avaliação proposto:
Plano proposto: separar qualidade de recuperação da utilização pelo modelo. Controlar corpus e versões; medir recall de evidência, latência por etapa e qualidade final com candidatos corretos e incorretos; aprovar pelo benefício total com proveniência preservada.

Comparações:
- T111 (distinct_from): Selecionar estados internos e recuperar trechos externos têm diferentes identidades, custos e atualizações.

Afirmação rastreável:
RETRO combina recuperador congelado, codificador diferenciável e cross-attention por trechos.
Suporte: direct; fontes: B-S026
Limite: O artigo apresenta uma arquitetura treinada para essa integração, não uma função universal disponível em qualquer checkpoint.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T112:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu compatibilidade de índice e cross-attention. O aprofundamento separa atualizações de conhecimento, atualizações da arquitetura e requisitos de avaliação que detectam dependência indevida do banco recuperado.

Conhecimento versionado
Mudar o banco externo pode modificar respostas sem mudar pesos. Registre a versão do índice junto à versão do modelo e preserve snapshots para reproduzir erros. Uma retirada de documento precisa impedir sua recuperação futura; a presença de informação semelhante nos pesos é outro problema, não resolvido pela remoção do índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

Contaminação de avaliação
Recuperação sobre corpus que contém respostas de teste pode inflar resultados sem demonstrar generalização. Deduplicate exemplos e vizinhos próximos por origem, não só por igualdade literal. Registre quais trechos foram recuperados e diferencie conhecimento disponível legitimamente de vazamento do conjunto usado para medir capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

Alternativa externa
Antes de treinar atenção com recuperação, compare um RAG textual no checkpoint existente. A arquitetura integrada pode oferecer vantagens específicas, mas exige acoplamento de codificador, treino e runtime. A decisão deve considerar atualização do acervo, custo de manutenção e possibilidade de inspecionar evidências, além da métrica principal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

USO AVANÇADO — Acervo técnico mutável
Cenário: Manuais mudam com frequência e o modelo precisa consultar detalhes.
Estratégia: Construa primeiro uma referência com recuperação textual, meça falhas e só investigue integração arquitetural quando houver hipótese clara sobre a limitação encontrada.
Papel do modelo pequeno: Um 3–7B pode executar o baseline de domínio; não se presume que suporte RETRO.
Aceite proposto: Comparar atualização de fatos, latência de busca e qualidade em versões históricas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

USO AVANÇADO — Pesquisa de modelo especializado
Cenário: Há orçamento para treinar uma arquitetura que consome vizinhos.
Estratégia: Controle corpus, codificador e frequência de recuperação. Faça ablação sem vizinhos, com vizinhos relevantes e com vizinhos errados para medir dependência.
Papel do modelo pequeno: Um 8–14B pode ser objeto de pesquisa controlada; porte isolado não define custo do treinamento.
Aceite proposto: A melhora deve sobreviver à remoção de duplicatas e a mudanças de distribuição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S026, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: RAG textual costuma ser uma hipótese inicial operacional mais simples; medir antes de redesenhar o modelo.
8–14B: Arquiteturas de recuperação podem ser estudadas com treino específico e corpus governado.
15–30B: O custo do codificador e de buscas repetidas pode dominar mesmo quando o gerador é maior.
Requisitos de treino/runtime: RETRO exige pesos e runtime específicos; Qwen ou outro decoder convencional não recebe essa arquitetura por configuração.
Não aplicar quando: Não apresentar cross-attention de recuperação como funcionalidade genérica de qualquer endpoint.

## T112:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C025 — Google DeepMind / RETRO
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: O trabalho avalia um modelo treinado para consumir trechos recuperados por uma arquitetura específica de atenção.
Mecanismo documentado: Codificação de vizinhos recuperados e cross-attention por trechos fazem parte da função treinada.
Correspondência com esta base: Recuperação participa da arquitetura de atenção.
Transferência proposta para modelo pequeno: Proposta: estudar custo e benefício de arquitetura treinada versus RAG externo antes de escolher uma intervenção em 3–30B.
Limite: Pesquisa não comprova produto implantado. Alterar um checkpoint convencional para reproduzir RETRO requer treinamento e compatibilidade; não é uma opção intercambiável de serving.
Fontes: B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T112:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T112 → T009 [alternative]
Como combinar: Comparar recuperação textual e integração arquitetural sob o mesmo corpus.
Interface: Consultas, evidências e versões do índice.
Condição: Protocolos de teste evitam vazamento e igualam acesso a conhecimento.
Aceite proposto: Medir resposta correta com evidência e custo de atualizar o acervo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S026, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T112 → T177 [requires]
Como combinar: Arquitetura integrada precisa aprender a consumir os estados externos.
Interface: Pesos do codificador, módulos de atenção e dados de treino.
Condição: Objetivo e entrada refletem uso posterior.
Aceite proposto: Ablacionar recuperação e verificar comportamento com ausência de vizinhos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S026, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir acesso ao documento correto com uso correto da informação.
- Manter logs de proveniência sem expor conteúdo protegido a usuários não autorizados.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação deve igualar acesso ao acervo e considerar atualizações. Um modelo especializado pode vencer numa coleção específica sem possuir conhecimento ou capacidade geral equivalentes aos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T067, T096, T111

## Fontes primárias associadas

### B-S026 — Improving language models by retrieving from trillions of tokens

[https://arxiv.org/abs/2112.04426](https://arxiv.org/abs/2112.04426)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RETRO combina recuperação, codificador e cross-attention por trechos.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

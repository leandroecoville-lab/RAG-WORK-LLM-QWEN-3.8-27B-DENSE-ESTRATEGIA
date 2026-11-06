# T018 — Context Pruning

**Nome canônico:** Context Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de contexto

## T018:C01 — conceito

Remove unidades de contexto consideradas dispensáveis antes da inferência. Pode usar regras, relevância, dependências ou modelos. Diferentemente de uma síntese abstrativa, a poda extrativa mantém o texto dos trechos escolhidos; ainda assim pode eliminar premissas essenciais.

Como funciona:
- Separar contexto em unidades com origem identificada.
- Atribuir elegibilidade e prioridade sem remover campos obrigatórios.
- Selecionar unidades dentro do orçamento e registrar descartes.

## T018:C02 — aplicacao

Quando usar:
- Documentos recuperados com muito ruído.
- Histórico que contém saídas repetidas ou superadas.

Quando não usar:
- Não usar apenas similaridade lexical quando a resposta depende de exceções ou condições indiretas.

Implementação proposta:
- Proposta: proteger negações, números, restrições e pares de chamada/resultado.
- Combinar relevância à pergunta com fechamento de dependências.
- Manter índice do que foi removido para permitir recuperação posterior.

Aplicação LAI proposta:
Proposta LAI: começar removendo duplicatas e logs já resolvidos; decisões atuais e evidências de autorização devem obedecer regras determinísticas de preservação.

## T018:C03 — riscos_validacao

Armadilhas:
- Uma premissa útil pode parecer pouco semelhante à pergunta.
- Remover trechos intermediários pode alterar a leitura de uma sequência causal ou temporal.

Métricas sugeridas:
- Tokens removidos e cobertura de evidência crítica.
- Qualidade final em comparação com contexto integral.

Testes propostos:
- Plantar uma exceção relevante em um parágrafo de baixa similaridade.
- Comparar explicação e resposta antes e depois da poda em casos negativos.

## T018:C04 — perguntas_proveniencia

Pergunta: Poda extrativa é sempre fiel?
Resposta: O texto preservado é original, mas a combinação de trechos pode omitir qualificações e induzir erro.

Pergunta: Posso podar depois do resultado da busca?
Resposta: Sim. Esse é um ponto comum, desde que o processo retenha evidências suficientes para a pergunta.

Pergunta: Uma frase irrelevante à pergunta pode ser necessária?
Resposta: Sim. Ela pode definir quem é o sujeito, qual unidade está em uso ou quando a regra vale. Relevância direta e suporte são funções distintas.

Pergunta: Como auditar o seletor?
Resposta: Guarde a máscara de seleção e os offsets. Assim é possível localizar exatamente o que foi removido e investigar uma resposta incorreta.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T018:C05 — mecanismo_avancado

A seleção independente de frases pode conservar uma conclusão e remover a condição que a limita. Uma poda orientada por dependências trata definição, unidade, negação e referente como parte da evidência necessária. O orçamento deve ser aplicado depois desse fechamento: escolher os trechos mais pontuados e descobrir tarde que suas dependências não cabem produz contexto incoerente.

Condição de contorno:
O critério de relevância deixa de ser suficiente quando as unidades selecionadas dependem de elementos com baixa pontuação isolada.

Contrato proposto:
- Entradas: Blocos identificados, orçamento e critérios de relevância e dependência.
- Saídas: Subconjunto literal acompanhado dos trechos de suporte necessários.
- Estado: Mapa de seleção, pontuações e localização do conteúdo retirado.
- Invariante: A poda não transforma uma afirmação condicional em regra incondicional por remoção silenciosa.

Compromissos de projeto:
- Poda por bloco mantém mais contexto e reduz economia em relação a tokens isolados.
- Critérios aprendidos capturam padrões, mas podem falhar em exceções raras e fora de domínio.

## T018:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atribuir alta relevância a um resultado e baixa relevância à frase que informa sua unidade e exceção. O seletor deve manter suporte suficiente ou indicar que o orçamento não permite resposta confiável.

Plano de avaliação proposto:
Avaliação proposta: comparar ranking independente e seleção com dependências no mesmo orçamento. Medir conservação de condições, respostas apoiadas, tokens e custo do seletor; avaliar também casos em que a ausência de informação exige abstenção.

Comparações:
- T038 (complements): Selective Context acrescenta critérios específicos de seleção à família de poda.
- T006 (specializes): Poda é compressão por remoção; não sintetiza necessariamente um texto novo.

Afirmação rastreável:
Selective Context reduz entrada removendo redundância, enquanto LLMLingua-2 aprende seleção de tokens com contexto bidirecional.
Suporte: direct; fontes: A-S016, V3A-S001
Limite: Os métodos não oferecem garantia universal de preservação de toda dependência semântica.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T018:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou dependências na poda. Aqui o novo critério é medir valor marginal dos blocos com ablações e controlar deriva da política.

Projeto e decomposição
Remova blocos candidatos individualmente em validação e observe quais decisões mudam. Atribua importância pelo efeito na tarefa, separando evidência redundante de condição rara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

Controle adaptativo
Aprenda política de poda por família de pergunta e congele sua versão durante avaliação. Feedback de uso pode criar viés se só forem observadas respostas que passaram pelo filtro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

Validação contrafactual
Compare poda baseada em comprimento, score e efeito contrafactual. Meça perda de requisitos raros e ganho de custo, incluindo expansão de recuperação. Unidade de avaliação: pacote de evidências. Uma ablação deve remover um bloco redundante e outra deve remover uma condição rara do mesmo tamanho. Se a política atribuir valor semelhante aos dois, o score não representa utilidade da tarefa. Registre quais respostas mudaram e se houve recuperação posterior; avaliação apenas sobre tokens removidos esconderia perda de capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

USO AVANÇADO — Dossiê com duplicatas
Cenário: Muitos textos repetem o mesmo anúncio.
Estratégia: Reter origem primária e versões que adicionam condição nova; não remover discordância por parecer redundante.
Papel do modelo pequeno: 3–7B detecta duplicação com verificação de campos.
Aceite proposto: Manter todas as condições únicas relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

USO AVANÇADO — Assistência técnica
Cenário: Logs comuns escondem uma exceção.
Estratégia: Proteger códigos de erro e mudança de estado; podar mensagens repetidas e recuperar bloco completo se diagnóstico permanecer ambíguo.
Papel do modelo pequeno: 8–14B interpreta conjunto reduzido.
Aceite proposto: Causa escolhida deve persistir no teste com log integral.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de blocos elegíveis para remoção, sob regras determinísticas.
8–14B: Leitor que sinaliza requisito perdido e pede expansão.
15–30B: Avaliador de conflitos entre blocos antes da poda final.
Requisitos de treino/runtime: Amostras de ablação e rastreamento de blocos descartados; não usar respostas de avaliação como treino.
Não aplicar quando: Não existe forma de recuperar conteúdo removido e omissão tem custo alto.

## T018:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Seleção aprendida especializa poda de contexto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T018:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T018 → T039 [feeds]
Como combinar: Transformar valor marginal em prioridade da janela.
Interface: block_id, ganho observado e dependências.
Condição: Estimativa válida para a família de tarefa.
Aceite proposto: Verificar estabilidade em novas fontes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T018 → T044 [complements]
Como combinar: Reabrir bloco quando surgir lacuna concreta.
Interface: Requisito faltante e referência descartada.
Condição: Política registrar o descarte.
Aceite proposto: Comparar recuperação dirigida com reinserção integral.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Conservar casos rejeitados para avaliar viés de seleção.
- Não usar frequência de acesso como único valor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perda causada pela poda em leitores pequenos e fronteira; tolerância à informação incompleta varia.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T038, T039

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T016 — Tool Result Truncation

**Nome canônico:** Tool Result Truncation  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de saída de ferramenta

## T016:C01 — conceito

Limita a quantidade de uma saída de ferramenta inserida no contexto. Deve preservar o resultado completo fora da chamada e indicar a truncagem. Uma amostra de log não autoriza concluir que o trecho omitido contém ou não contém determinado fato.

Como funciona:
- Receber a saída integral e guardar metadados de tamanho.
- Selecionar partes pertinentes dentro do orçamento.
- Retornar indicador de conteúdo parcial e forma de obter continuação.

## T016:C02 — aplicacao

Quando usar:
- Logs extensos, consultas com muitas linhas e arquivos volumosos.
- Inspeção inicial que será seguida por busca direcionada.

Quando não usar:
- Não truncar silenciosamente resultados usados para afirmar cobertura completa ou ausência de erro.

Implementação proposta:
- Proposta: exigir campos truncated, total_size e artifact_ref no contrato.
- Priorizar cabeçalho, erros e intervalos pedidos, evitando corte cego no final.
- Permitir leitura por offset ou filtro e distinguir zero resultados de saída omitida.

Aplicação LAI proposta:
Proposta LAI: resumir saídas extensas da auditoria com links para o original; manter contagem de registros para que a Helena saiba o que ainda não viu.

## T016:C03 — riscos_validacao

Armadilhas:
- O erro decisivo pode estar fora da amostra.
- Cortar JSON ou uma linha de tabela pode produzir interpretação incorreta.

Métricas sugeridas:
- Fração omitida e número de leituras adicionais.
- Taxa de decisões incorretas causadas por resultado parcial.

Testes propostos:
- Colocar falha no meio de um log grande e recuperá-la com busca.
- Testar uma saída cortada no meio de JSON e exigir formato estruturado válido ou conteúdo bruto marcado.

## T016:C04 — perguntas_proveniencia

Pergunta: Truncar é a mesma coisa que resumir?
Resposta: Não. Truncar remove partes; resumir reescreve conteúdo. Ambos podem perder informação de maneiras diferentes.

Pergunta: Posso declarar não há erros após ler os primeiros resultados?
Resposta: Só se a ferramenta verificou todo o conjunto e retornou esse resultado de forma explícita.

Pergunta: Truncar e resumir são equivalentes?
Resposta: Não. Truncar retém uma parte literal; resumir produz outra representação. Ambos podem perder informação, mas têm riscos e testes de fidelidade diferentes.

Pergunta: O marcador de truncamento deve ficar só no log?
Resposta: Não. Quem toma a decisão precisa conhecer a cobertura. O marcador deve acompanhar o trecho entregue ao consumidor.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T016:C05 — mecanismo_avancado

A política de truncamento precisa preservar sinais de estado independentes do corpo: código de saída, paginação, contagem quando disponível e existência de erro. Cortar apenas pelo começo pode remover o diagnóstico final; guardar começo e fim pode omitir o único erro intermediário. Portanto, uma saída parcial exige contrato de cobertura e caminho para leitura direcionada do restante.

Condição de contorno:
Se o consumidor precisa provar ausência de ocorrências no conjunto inteiro, uma amostra truncada não fornece evidência suficiente, por maior que pareça.

Contrato proposto:
- Entradas: Resultado completo, limite de apresentação e metadados confiáveis da ferramenta.
- Saídas: Trecho parcial identificado e referência recuperável ao original.
- Estado: Artefato completo, regiões exibidas e versão do seletor de trechos.
- Invariante: Conteúdo omitido nunca é descrito como examinado apenas porque a ferramenta terminou sem erro de transporte.

Compromissos de projeto:
- Limites rígidos protegem contexto, mas podem esconder o sinal mais importante.
- Seleção orientada por erros preserva diagnóstico e exige conhecer o formato, sem substituir o original.

## T016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar uma ocorrência relevante somente no meio omitido de um log. O agente deve reconhecer cobertura parcial e recuperar essa região antes de concluir ausência de problema.

Plano de avaliação proposto:
Avaliação proposta: comparar prefixo, início e fim, e seleção estruturada com igual orçamento. Medir diagnósticos preservados, releituras, falsos relatos de ausência e custo total; manter o original disponível em todas as variantes.

Comparações:
- T214 (distinct_from): Pruning pode selecionar campos ou regiões por relevância; truncamento aplica um limite de apresentação.
- T215 (distinct_from): Masking substitui observações antigas por marcadores; truncamento também pode ocorrer no primeiro recebimento.

Afirmação rastreável:
MCP separa a referência de um recurso da operação que lê seu conteúdo.
Suporte: related; fontes: V3A-S019
Limite: Isso apoia externalização do original; o protocolo de truncamento descrito é uma proposta editorial.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu parcial, erro e vazio. Aqui a saída truncada é uma projeção orientada pela pergunta, com caminho mensurável de recuperação.

Projeto e decomposição
Escolha projeção por tipo de resultado: amostra estratificada para exploração, agregação para contagem e linhas exatas para diagnóstico. Cortar os primeiros caracteres raramente é contrato suficiente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Controle adaptativo
Preserve total de itens, filtros, ordenação e cursor. O modelo decide se a projeção responde à pergunta ou solicita leitura adicional com campos definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Validação contrafactual
Compare prefixo simples e projeções orientadas à tarefa. Meça conclusões corretas sobre o conjunto e custo das leituras adicionais. Unidade de avaliação: resultado de ferramenta. Para validar projeções, use conjunto cuja exceção aparece no final e outro com distribuição desigual entre categorias. Prefixo simples deve falhar de modo observável; amostra estratificada pode localizar a exceção, mas ainda não prova sua frequência. Contagens e conclusões exaustivas precisam vir da consulta completa, com filtro e ordenação registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Busca com muitos resultados
Cenário: A pergunta pede exceções raras.
Estratégia: Calcular contagens em código, devolver grupos e abrir amostras das categorias suspeitas. Não inferir ausência pela amostra.
Papel do modelo pequeno: 3–7B classifica categorias.
Aceite proposto: Contagem final deve vir da consulta completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Falha de compilação volumosa
Cenário: Logs contêm cascata de erros.
Estratégia: Retornar primeiros erros por arquivo e resumo de frequências; preservar log integral para buscar causa anterior.
Papel do modelo pequeno: 8–14B prioriza diagnóstico.
Aceite proposto: Patch deve ser validado contra execução posterior, não resumo do log.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de schema e contagens calculadas, sem estimar totais pela amostra.
8–14B: Investigador que pede intervalos adicionais com hipótese explícita.
15–30B: Correlacionador de múltiplos logs por identificadores de operação.
Requisitos de treino/runtime: Ferramenta de projeção determinística e armazenamento do resultado completo quando necessário.
Não aplicar quando: O corte remove a única evidência disponível ou a tarefa exige exaustividade sem cursor.

## T016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T016 → T238 [complements]
Como combinar: Abrir intervalos do artefato integral.
Interface: artifact_id, versão, intervalo e total.
Condição: Leitura manter ordenação e revisão.
Aceite proposto: Reconstituir trecho omitido sem trocar a origem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T016 → T042 [requires]
Como combinar: Limitar projeção pelo orçamento real.
Interface: Tokens estimados, reserva e esquema de resposta.
Condição: Medir após serializar metadados.
Aceite proposto: Testar resultado cujo cabeçalho sozinho excede a cota.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar amostra de resultado completo.
- Propagar erro da ferramenta sem convertê-lo em conjunto vazio.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar diagnóstico e decisões sobre conjuntos grandes; concisão isolada não basta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T043, T066

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

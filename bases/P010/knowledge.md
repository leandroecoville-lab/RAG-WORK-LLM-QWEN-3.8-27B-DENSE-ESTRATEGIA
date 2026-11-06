# P010 — Routing Engine

**Nome canônico:** Routing Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P010  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de roteamento de modelos

## P010:C01 — conceito

Routing Engine é um nome editorial proposto para escolher uma rota de execução compatível com a tarefa e seu orçamento. Pode decidir modelo, endpoint e alternativa elegível. RouteLLM e cascatas fornecem fundamentos relacionados; não demonstram que este componente exista na LAI nem que um roteador aprendido supere uma política simples no acervo do usuário.

Como funciona:
- Eliminar rotas incompatíveis com tamanho de contexto, ferramentas, formato exigido e disponibilidade operacional.
- Entre as rotas elegíveis, considerar estimativas de qualidade, custo, latência e capacidade observada.
- Registrar a razão da escolha e os critérios para escalonamento ou fallback, sem formar ciclos de tentativas.

## P010:C02 — aplicacao

Quando usar:
- Cargas heterogêneas em que modelos ou serviços têm custos e desempenhos diferentes mensuráveis.

Quando não usar:
- Quando não há avaliação representativa para sustentar alegações de qualidade equivalente entre rotas.

Implementação proposta:
- Proposta: começar com uma política determinística baseada em capacidades e classes de tarefa, versionando cada decisão.
- Construir comparação offline com um baseline único antes de adotar roteamento aprendido ou limiares mais complexos.
- Se uma resposta falhar na verificação, permitir escalonamento com orçamento restante e transferir evidências suficientes para a nova rota.

Aplicação LAI proposta:
Proposta LAI: P010 escolhe a rota; P009 executa; P012 devolve sinais verificáveis de aceitação; P016 avalia a política em dados separados.

## P010:C03 — riscos_validacao

Armadilhas:
- Confiança declarada pelo próprio modelo não equivale a probabilidade calibrada de acerto.
- Um fallback mais barato pode perder suporte a ferramentas ou truncar o contexto.
- Rotear sem contabilizar tentativas anteriores pode aumentar custo total apesar de reduzir o preço por chamada.

Métricas sugeridas:
- Qualidade por classe de tarefa, custo por resultado aceito, latência final e taxa de escalonamento.

Testes propostos:
- Aceite proposto: tornar o endpoint preferido indisponível e exigir uma alternativa com as mesmas capacidades obrigatórias.
- Comparar política e baseline em conjunto separado por projeto ou período, incluindo perguntas difíceis e casos sem rota elegível.

## P010:C04 — perguntas_proveniencia

Pergunta: Modelo barato deve receber automaticamente toda tarefa curta?
Resposta: Não. Tamanho é apenas um sinal; uma tarefa curta pode exigir capacidade específica ou verificação rigorosa.

Pergunta: Como julgar economia real de uma rota?
Resposta: Pelo custo total até um resultado aceito, incluindo respostas rejeitadas, reruns, ferramentas e escalonamentos.

Pergunta: Qual objetivo otimizar?
Resposta: Custo e tempo para uma tarefa aceita, preservando requisitos e limites de erro.

Pergunta: Como impedir loops de fallback?
Resposta: Registre rotas visitadas, orçamento global, deadline e motivo final quando não resta opção válida.

Escopo das fontes:
Fontes sustentam roteamento, calibração e avaliação; política LAI e limiares exigem validação própria.

## P010:C05 — mecanismo_avancado

Routing Engine propõe escolher uma rota sob restrições de capacidade, orçamento, qualidade e disponibilidade. A decisão deve guardar quais candidatos foram elegíveis e por que um foi selecionado. Uma estimativa de dificuldade ou confiança precisa ser calibrada no domínio; um número alto emitido pelo próprio modelo não basta. Fallback deve consumir um orçamento global e preservar requisitos, evitando alternância infinita entre provedores que falham da mesma forma.

Condição de contorno:
Uma rota mais barata por chamada pode aumentar custo total se produzir mais respostas rejeitadas ou exigir escalonamento frequente. A métrica principal precisa considerar resultado aceito.

Contrato proposto:
- Entradas: Tarefa, capacidades exigidas, orçamento restante, deadline, saúde dos candidatos e versão da política de roteamento.
- Saídas: Rota escolhida ou impossibilidade explícita, justificativa, limite de tentativas e critério de escalonamento.
- Estado: Histórico de desempenho por tipo de tarefa, calibração, custos e tentativas já consumidas na operação.
- Invariante: Nenhuma troca de rota pode relaxar silenciosamente um requisito obrigatório nem reiniciar o orçamento de retries.

Compromissos de projeto:
- Um classificador adicional custa latência e pode compensar quando evita uso excessivo de modelos caros.
- Cascatas economizam em casos simples, mas acumulam custo e atraso quando a maioria exige escalonamento.

## P010:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: tornar indisponível a rota preferida e oferecer fallback sem a capacidade requerida; exigir rejeição clara, sem apresentar saída degradada como equivalente.

Plano de avaliação proposto:
Comparar roteador com uma rota fixa forte e outra econômica no mesmo conjunto reservado. Medir custo por tarefa aceita, erro, latência de cauda, taxa de escalonamento e calibração. Incluir períodos de indisponibilidade simulada.

Comparações:
- T133 (specializes): É um componente proposto para escolher modelos.
- T203 (complements): Roteamento por correção pode fornecer sinal de aceitação ou escalonamento.

Afirmação rastreável:
Pesquisas de roteamento e cascatas estudam trocas entre custo e qualidade; calibração exige avaliação.
Suporte: related; fontes: C-S001, C-S002, C-S050
Limite: O contrato aqui não reproduz um algoritmo específico nem promete ganhos dos artigos no domínio do usuário.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P010:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o roteador proposto com seleção sob restrições, aprendizado sem viés de sobreviventes e separação entre dificuldade estimada e falha de infraestrutura.

Elegibilidade antes do ranking
Proposta: filtrar modelos por contrato de ferramenta, tamanho de entrada, prazo e requisitos de dados antes de prever qualidade/custo. Um candidato barato porém incapaz do formato não é uma rota válida. Registrar o conjunto excluído ajuda a explicar decisões e detectar configurações desatualizadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

Feedback com censura
Guardar resultado de todas as tentativas, inclusive timeout, abstenção e escalada. Avaliar apenas tarefas aceitas pelo modelo pequeno cria seleção favorável. Amostras controladas em shadow, sem efeitos duplicados, podem estimar o desempenho das rotas não escolhidas; isso ainda exige desenho experimental adequado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

Razão de escalada
Separar erro estrutural, evidência insuficiente, tarefa fora do domínio e indisponibilidade. Cada razão sugere uma ação diferente: reparar contexto, trocar ferramenta, usar modelo maior ou aguardar capacidade. Trocar modelo para qualquer erro pode apenas repetir a falha compartilhada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

USO AVANÇADO — Extração de contratos com exceções
Cenário: Maioria dos documentos segue padrões; poucos exigem interpretação difícil.
Estratégia: Extrair com modelo pequeno, verificar campos e escalar apenas os casos de ambiguidade definidos.
Papel do modelo pequeno: 3–14B atende o fluxo comum com evidência por campo.
Aceite proposto: Medir cobertura, erro residual e custo total, incluindo casos escalados e revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

USO AVANÇADO — Serviço sob fila longa
Cenário: A rota habitual ultrapassa o prazo disponível.
Estratégia: Escolher somente alternativa que preserve requisito; caso contrário adiar ou recusar explicitamente.
Papel do modelo pequeno: Classificador pequeno estima tipo de tarefa; fila/deadline vêm da telemetria.
Aceite proposto: Nenhuma mudança silenciosa de qualidade contratada e p95 dentro do limite declarado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S050, V4C-S011, V4C-S012, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: tarefas estáveis e classificação de rota com calibração local.
8–14B: 8–14B: rota principal de tarefas especializadas com ferramentas e validação.
15–30B: 15–30B: escalada intermediária avaliada contra o custo de fronteira ou revisão humana.
Requisitos de treino/runtime: Calibrar usando resultados reais da política e controlar mudança de distribuição.
Não aplicar quando: Não usar autoconfiança verbal do modelo como probabilidade calibrada de sucesso.

## P010:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C013 — Uber / GenAI Gateway
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A Uber relata equipes internas utilizando o gateway para consultas a modelos externos e hospedados internamente.
Mecanismo documentado: Adaptadores expõem uma interface comum e integram autenticação, política de dados, métricas e atribuição de custos.
Correspondência com esta base: O gateway é referência para infraestrutura de rotas, não valida o motor editorial completo.
Transferência proposta para modelo pequeno: Proposta: centralizar adapters de 3–30B e registrar capacidades reais de cada endpoint; separar seleção do modelo da tradução de protocolos e da medição do custo por tarefa aceita.
Limite: Interface compatível não torna modelos semanticamente equivalentes. Não mapear automaticamente disponibilidade de múltiplos fornecedores a cascata ou fallback comprovado.
Fontes: V4C-S012.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Seleção por resultado é referência para o roteador editorial.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C012 — Amazon Web Services / Amazon Bedrock Intelligent Prompt Routing
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação disponibiliza um endpoint de roteamento que prevê qualidade e escolhe entre dois modelos compatíveis da mesma família.
Mecanismo documentado: Configuração define modelos, critério e fallback; resposta informa o modelo usado. A página é documentação de produto, não relato de implantação de um cliente.
Correspondência com esta base: O serviço oferece referência para um componente editorial de roteamento.
Transferência proposta para modelo pequeno: Proposta: comparar um roteador local 3–30B com regras simples, rotas fixas e escalonamento após validação. Rejeitar candidatos sem capacidade necessária antes de estimar qualidade.
Limite: Classificado como operational_product. Não conta para dez casos comprovados em produção; lista de modelos e regiões muda. Exemplos com modelos maiores não validam as bandas pequenas.
Fontes: V4C-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P010 é proposta. Bedrock oferece recurso de roteamento; relatos Uber têm escopos próprios e não comprovam automaticamente roteamento dinâmico por dificuldade.
Consultas registradas: V4C-Q008, V4C-Q009.

## P010:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P010 → T133 [complements]
Como combinar: Implementar a política de escolha como decisão rastreável.
Interface: Candidatos elegíveis, scores, motivo e orçamento.
Condição: Existe heterogeneidade real de tarefas e modelos.
Aceite proposto: Reproduzir a decisão a partir de entradas e versão da política.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V4C-S011, V4C-S012, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P010 → T203 [complements]
Como combinar: Usar verificação de correção para orientar nova rota.
Interface: Critério falho, evidência e tentativas anteriores.
Condição: Há verificador útil e escalada permitida.
Aceite proposto: A escalada reduz erro medido sem exceder orçamento de tarefa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S050, V4C-S011, V4C-S012, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não treinar o roteador somente em sucessos publicados.
- Não contar economia por chamada ignorando retries e professor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar política completa contra modelo único nos mesmos pedidos, incluindo seleção e abstinência. Medir não inferioridade por subgrupo, custo por aceite e cauda de latência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T136, T198, T203, P009, P012, P016

## Fontes primárias associadas

### C-S001 — RouteLLM: Learning to Route LLMs with Preference Data

[https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteadores aprendidos escolhem entre modelos considerando qualidade e custo; resultados dependem do conjunto de tarefas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S002 — FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

[https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cascatas de modelos e decisões de encaminhamento podem ser otimizadas sob orçamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

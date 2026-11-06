# P016 — Evaluation Engine

**Nome canônico:** Evaluation Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de avaliação de versões

## P016:C01 — conceito

Evaluation Engine é um nome editorial proposto para comparar versões do sistema em conjuntos de tarefas e monitorar regressões. Sua unidade é a avaliação agregada de comportamento, enquanto P012 verifica um resultado concreto durante o fluxo. As fontes apoiam boas práticas de avaliação; não confirmam um motor LAI implementado nem resultados de benchmark deste pacote.

Como funciona:
- Definir objetivos, conjunto de casos, critérios de sucesso e métricas antes de comparar candidatos.
- Executar baseline e versão candidata sob condições documentadas, preservando entradas, saídas, custos e versões.
- Analisar desempenho por classe de tarefa e revisar divergências com avaliação humana ou oráculos adequados.

## P016:C02 — aplicacao

Quando usar:
- Mudanças em recuperação, prompts, roteamento, modelos e políticas de memória que podem introduzir regressões.

Quando não usar:
- Para apresentar perguntas produzidas a partir das próprias fichas como teste independente de cobertura ou generalização.

Implementação proposta:
- Proposta: separar desenvolvimento, ajuste e teste; evitar vazamento de documentos ou tarefas quase duplicadas entre divisões.
- Avaliar recuperação e resposta separadamente: recuperar o documento certo não implica responder corretamente, e uma resposta memorizada pode esconder recuperação ruim.
- Calibrar avaliadores automáticos contra rótulos revisados e apresentar tamanho da amostra, variabilidade e condições de medição.

Aplicação LAI proposta:
Proposta LAI: versionar datasets e critérios com os artefatos, alimentando decisões de P010 e P017; as duas QAs de cada ficha permanecem material didático.

## P016:C03 — riscos_validacao

Armadilhas:
- Uma média global pode ocultar regressões graves em tarefas raras.
- O julgador pode preferir respostas longas ou compartilhar o mesmo erro do produtor.
- Escolher o melhor limiar repetidamente sobre o teste transforma esse conjunto em material de ajuste.

Métricas sugeridas:
- Qualidade por estrato, recall de evidências, correção funcional, custo por sucesso e latências sob carga definida.

Testes propostos:
- Aceite proposto: inserir uma regressão conhecida em apenas uma classe e exigir sua identificação no relatório.
- Reservar um conjunto externo às fichas e verificar que alterações de limiares não o utilizem como treinamento.

## P016:C04 — perguntas_proveniencia

Pergunta: As QAs deste RAG comprovam sua qualidade?
Resposta: Não. Elas ajudam ensino e checagem interna, mas foram escritas a partir do conteúdo; um benchmark independente precisa de casos separados.

Pergunta: Como distinguir melhoria de custo de perda de qualidade?
Resposta: Comparar custo por resultado aceito sob os mesmos critérios e reportar a qualidade por classe, incluindo falhas e tentativas adicionais.

Pergunta: Posso chamar 100% de busca por nome de qualidade geral?
Resposta: Não. É um teste de cobertura literal, diferente de perguntas descritivas e de respostas corretas.

Pergunta: O que fazer após ver falhas na reserva?
Resposta: Registrar a primeira rodada; usar esses casos para desenvolvimento futuro e criar outra reserva antes do próximo ajuste.

Escopo das fontes:
Fontes apoiam avaliação e calibração; datasets, limiares e resultados LAI continuam pendentes de execução.

## P016:C05 — mecanismo_avancado

Evaluation Engine propõe manter avaliações separadas de recuperação, montagem de contexto, geração e execução. Um resultado de Hit@k indica presença de um alvo entre candidatos, sem provar que a resposta final usa a evidência corretamente. Consultas usadas para ajustar ranking pertencem ao desenvolvimento. Um conjunto reservado deve ser congelado antes da mudança avaliada e identificado por hash; após inspecionar falhas, ele perde o papel de reserva intocada para a próxima rodada.

Condição de contorno:
Um pequeno conjunto editorial pode revelar regressões, mas não representa automaticamente a distribuição de produção. Métricas agregadas podem esconder falhas em categorias raras ou importantes.

Contrato proposto:
- Entradas: Corpus e configuração identificados, consultas, critérios ou referências, partições e protocolo definido antes da execução.
- Saídas: Resultados por caso, agregações, falhas, artefatos de configuração e limites da interpretação.
- Estado: Versões de datasets, histórico de alterações, primeiras execuções reservadas e registros de decisões de ajuste.
- Invariante: Não alterar respostas esperadas depois de observar falhas para melhorar o score da mesma rodada; correções exigem nova versão justificada.

Compromissos de projeto:
- Casos sintéticos permitem cobertura dirigida, mas precisam ser complementados por exemplos reais autorizados.
- Juízes automáticos ampliam escala; custo, viés e correlação com o gerador precisam de controles próprios.

## P016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: mudar um documento, um parâmetro de ranking e uma referência esperada; verificar que cada alteração muda a identidade da avaliação e impede comparação sem qualificação.

Plano de avaliação proposto:
Executar baseline e candidato com mesmos dados, preservar rankings completos e examinar ganhos e regressões. Para geração, adicionar respostas reais e avaliação de suporte por evidência. Não inferir qualidade de geração a partir do teste lexical offline.

Comparações:
- T199 (complements): Aprendizagem por avaliação usa resultados sem contaminar a reserva.
- T205 (complements): Equivalência semântica pode ser uma dimensão específica do protocolo.

Afirmação rastreável:
A avaliação de RAG distingue qualidade de recuperação, fidelidade ao contexto e resposta.
Suporte: related; fontes: V3D-S002
Limite: O motor proposto não é implementação do Ragas; os testes deste pacote medem apenas os componentes efetivamente executados.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegeu conjunto reservado e separou recuperação de resposta. Esta proposta acrescenta diagnóstico causal, avaliação de seletores e governança das versões promovidas. Nenhum benchmark reservado foi consultado para escrever estas estratégias.

Métricas em camadas
Avalie entrada, recuperação, contexto, geração e ação separadamente, mantendo um resultado de tarefa final. Isso permite localizar se a falha veio de documento ausente, interpretação ou execução. Uma métrica intermediária não substitui sucesso de ponta a ponta; melhoria local pode piorar custo ou qualidade global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

Seleção também é sistema
Roteadores, juízes e políticas de parada precisam de avaliação própria. Meça se o conjunto contém solução correta e se o seletor a escolhe; registre abstenções e casos rejeitados. A precisão dos resultados aceitos deve ser acompanhada de cobertura e custo dos descartados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

Promoção reproduzível
Cada rodada registra hashes de dados, corpus, modelo e configuração, além das mudanças propostas. Mantenha desenvolvimento, calibração e aceitação separados. Depois que falhas de um conjunto reservado orientam alterações, ele passa a ser dado de desenvolvimento para versões futuras; a governança deve reconhecer essa mudança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

USO AVANÇADO — Escolher modelo 3–30B
Cenário: Há candidatos com custos e habilidades diferentes.
Estratégia: Defina tarefas e critérios antes da comparação, use ferramentas equivalentes e avalie por categoria. Inclua casos desconhecidos, abstinência e tempo completo.
Papel do modelo pequeno: Um modelo pequeno pode ser escolhido na região de competência demonstrada.
Aceite proposto: Qualidade suficiente, cobertura e custo por resultado correto dentro do objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

USO AVANÇADO — Validar otimização de runtime
Cenário: Cache ou quantização promete mais capacidade.
Estratégia: Compare semântica e qualidade primeiro, depois prefill, decode, fila e memória em carga representativa. Separe efeito do algoritmo de diferenças de modelo e template.
Papel do modelo pequeno: O porte orienta orçamento, mas não substitui ensaio do checkpoint real.
Aceite proposto: Nenhuma regressão relevante escondida por tokens por segundo ou média global.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Testes de domínio e contratos fechados ajudam a identificar onde o 3–7B é útil.
8–14B: Para 8–14B, examine ganhos de especialização e falhas fora da distribuição.
15–30B: Para 15–30B, inclua custo de infraestrutura e vantagem marginal frente a opções menores.
Requisitos de treino/runtime: Proposta de avaliação, não execução realizada. Requer dados, critérios, instrumentação e ambiente adequados.
Não aplicar quando: Não ajustar ranking às consultas reservadas nem alterar gabarito depois de ver falha para melhorar o score.

## P016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Avaliação local pode inspirar a proposta LAI; o produto editorial não foi implantado.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: O scorer inspira avaliação de artefatos da proposta editorial.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011, V4B-Q012.

## P016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P016 → T198 [feeds]
Como combinar: Calibração precisa de dados e métricas independentes na avaliação.
Interface: Evento de sucesso, score e divisão dos dados.
Condição: Amostra representa o caminho de uso.
Aceite proposto: Relatar confiabilidade e cobertura por categoria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P016 → T203 [feeds]
Como combinar: A avaliação mede roteamento completo, incluindo tentativas e escalonamento.
Interface: Decisões, contrafactuais amostrados e custos.
Condição: Comparações têm acesso equivalente a ferramentas e evidências.
Aceite proposto: Aceitar política pelo resultado final, não pela confiança prevista.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P016 → P017 [complements]
Como combinar: Destilação proposta usa avaliação para promover ou rejeitar aluno.
Interface: Checkpoint, dados e contrato de uso.
Condição: Teste final não participa do treino ou seleção.
Aceite proposto: Medir generalização e regressões depois da transferência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S002, C-S048, C-S050, V4B-S026, V3B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transformar percentuais relativos de preferência em multiplicadores de inteligência.
- Preservar resultados por caso e limitações, não somente um score composto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O engine proposto deve sustentar comparações delimitadas com fronteira. Um conjunto finito de tarefas não comprova supremacia universal; nenhuma medição inexistente deve ser apresentada como resultado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T195, T198, T200, T205, P007, P010, P012, P017

## Fontes primárias associadas

### V2C-S004 — Evaluation best practices

[https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evals específicas da tarefa, objetivos, datasets, métricas, comparação, acompanhamento contínuo e calibração com julgamento humano.

Limite: Orientação metodológica, sem benchmark do pacote. As QA redigidas nas fichas são material didático, não teste independente.

### C-S048 — Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

[https://arxiv.org/abs/2305.01210](https://arxiv.org/abs/2305.01210)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: EvalPlus examina limitações de testes e avaliação de correção funcional de código gerado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S050 — On Calibration of Modern Neural Networks

[https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração relaciona probabilidades previstas à frequência de acerto; temperatura de calibração não é temperatura de geração.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S002 — Ragas: Automated Evaluation of Retrieval Augmented Generation

[https://arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Avaliar recuperação, fidelidade ao contexto e geração são dimensões distintas de um sistema RAG.

Limite: Página do artigo e abstract consultados, versão revisada indicada em 2025-04-28. Este pacote não executa Ragas nem afirma avaliação real de geração.

### V4B-S026 — Automated Unit Test Improvement using Large Language Models at Meta

[https://arxiv.org/abs/2402.09171](https://arxiv.org/abs/2402.09171)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Autores relatam implantação de TestGen-LLM em test-a-thons e recomendações aceitas para produção, com filtros de build, estabilidade e cobertura.

Limite: Alegação de produção vem do relato explícito dos autores sobre deployment, não do fato de ser paper; cobertura não prova correção geral.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

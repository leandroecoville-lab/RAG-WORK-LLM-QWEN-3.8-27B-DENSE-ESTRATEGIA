# T044 — Progressive Context Expansion

**Nome canônico:** Progressive Context Expansion  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T044  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** expansão progressiva de contexto

## T044:C01 — conceito

Começa com contexto suficiente para orientar a tarefa e amplia a informação conforme surgem lacunas verificáveis. É o movimento complementar ao carregamento progressivo: a expansão precisa ter motivo, orçamento e condição de parada, não apenas adicionar cada vez mais texto.

Como funciona:
- Iniciar com objetivo, estado e evidência de maior valor.
- Identificar lacunas ou referências que precisam ser abertas.
- Buscar detalhe adicional e revisar a suficiência do contexto.

## T044:C02 — aplicacao

Quando usar:
- Perguntas cuja profundidade necessária não é conhecida antecipadamente.
- Análise de incidentes que começa por sintomas e segue dependências.

Quando não usar:
- Não reduzir a entrada inicial a ponto de ocultar restrições obrigatórias ou identidade da tarefa.

Implementação proposta:
- Proposta: manter lista explícita de perguntas não respondidas.
- Abrir fontes por referência exata antes de expandir semanticamente quando possível.
- Limitar rodadas e encerrar com lacunas declaradas se nenhuma nova evidência surgir.

Aplicação LAI proposta:
Proposta LAI: usar índice, ficha técnica e fonte original como níveis sucessivos; informações obrigatórias continuam carregadas desde o começo.

## T044:C03 — riscos_validacao

Armadilhas:
- Expansão pode virar loop de busca sem progresso.
- Um modelo confiante pode não perceber que faltam premissas.

Métricas sugeridas:
- Ganho de cobertura por rodada.
- Tokens e chamadas extras até evidência suficiente.

Testes propostos:
- Criar uma pergunta que exige abrir um documento citado e conferir a expansão.
- Fornecer buscas repetidas sem informação nova e exigir parada controlada.

## T044:C04 — perguntas_proveniencia

Pergunta: Mais contexto sempre melhora a resposta?
Resposta: Não. A expansão deve resolver uma lacuna identificada, pois dados extras também introduzem ruído.

Pergunta: Quem decide que a evidência é suficiente?
Resposta: Uma política de cobertura e verificação, auxiliada pelo modelo; confiança textual isolada não basta.

Pergunta: Como estimar o valor da próxima busca?
Resposta: Use o tipo de lacuna, custo e histórico de tentativas. É uma heurística operacional que precisa ser comparada com expansão fixa.

Pergunta: Quando expandir o documento em vez da coleção?
Resposta: Quando a lacuna é local, como uma definição ou ressalva próxima. Ausência de identidade ou fonte independente pode exigir busca mais ampla.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T044:C05 — mecanismo_avancado

A expansão pode escolher entre abrir uma referência exata, aumentar a região de um documento ou iniciar nova busca. Essas ações têm custos e riscos diferentes. Uma política útil associa cada ação a uma lacuna: identidade ambígua, premissa ausente ou contradição. O progresso é redução verificável dessa lacuna, não crescimento de tokens nem confiança retórica do modelo após mais leitura.

Condição de contorno:
Um agente pode permanecer confiante apesar de uma premissa falsa; gatilhos baseados apenas em incerteza do gerador não detectam todos os casos que precisam expandir.

Contrato proposto:
- Entradas: Lista de lacunas, contexto atual, referências disponíveis e orçamento restante de busca e leitura.
- Saídas: Nova evidência vinculada à lacuna ou registro de tentativa sem resolução.
- Estado: Consultas já feitas, fontes abertas, versões e razões de parada.
- Invariante: Repetir a mesma evidência não conta como confirmação independente nem como ganho de cobertura.

Compromissos de projeto:
- Expansão sob demanda evita leitura desnecessária e acrescenta latência sequencial.
- Abrir fontes vizinhas conserva escopo; novas buscas ampliam cobertura e aumentam risco de desvio temático.

## T044:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer evidência que responde metade de uma comparação e resultados repetidos para a outra metade. O agente deve identificar cobertura parcial e parar após esgotar a política, sem completar por analogia.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação única, expansão fixa e expansão por lacunas com orçamento máximo igual. Medir cobertura incremental, custo por lacuna resolvida e encerramentos justificados; incluir casos de alta confiança com premissa ausente.

Comparações:
- T014 (complements): Carregamento progressivo define níveis disponíveis; expansão escolhe quando percorrê-los por necessidade concreta.
- T067 (complements): Recuperação ativa oferece gatilhos e consultas durante a geração, compondo uma política de expansão.

Afirmação rastreável:
FLARE antecipa a continuação textual e usa baixa confiança em tokens para acionar recuperação e regeneração.
Suporte: direct; fontes: V3A-S010
Limite: É um mecanismo específico de acionamento; confiança do modelo não equivale a uma prova geral de suficiência da evidência.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T044:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 expandiu por lacuna. Aqui a ordem de abertura considera valor esperado de informação e custo de verificar hipóteses.

Projeto e decomposição
Associe cada abertura a uma decisão que pode mudar. Abrir mais documentos sem hipótese de utilidade aumenta contexto e latência sem necessariamente reduzir incerteza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

Controle adaptativo
Escolha primeiro a fonte com maior poder de discriminar alternativas, respeitando autoridade e custo. Se o resultado não mudar as opções, revise a hipótese antes de repetir busca semelhante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

Validação contrafactual
Compare expansão por top-k e por lacuna discriminante. Meça decisões alteradas por abertura, leituras redundantes e tempo até evidência suficiente; incluir fontes indisponíveis. Unidade de avaliação: sequência de aberturas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

USO AVANÇADO — Diagnóstico de erro
Cenário: Duas causas levam a correções diferentes.
Estratégia: Abrir o log ou configuração que distingue causas, depois carregar código correspondente; não ler todo o repositório antecipadamente.
Papel do modelo pequeno: 8–14B escolhe teste discriminante.
Aceite proposto: Cada expansão deve reduzir alternativas ou justificar insuficiência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

USO AVANÇADO — Consulta de política
Cenário: Uma exceção pode mudar a regra.
Estratégia: Abrir seção de exceções antes de resposta conclusiva, mantendo versão e escopo da regra principal.
Papel do modelo pequeno: 3–7B identifica condição; 15–30B integra.
Aceite proposto: Não afirmar regra absoluta sem verificar exceção aplicável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Detector de campo obrigatório ausente e seletor de referência exata.
8–14B: Planejador de uma abertura discriminante por vez.
15–30B: Coordenador de hipóteses múltiplas com limite de custo.
Requisitos de treino/runtime: Representação de lacunas e alternativas, referências estáveis e contabilização por abertura.
Não aplicar quando: O acervo não contém informação discriminante ou o sistema não consegue avaliar progresso.

## T044:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Busca sob demanda relacionada à expansão.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T044:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T044 → T078 [feeds]
Como combinar: Transformar falta semântica explícita em evento de carga.
Interface: Campo ausente, decisão afetada e candidatos.
Condição: Rótulo de falta ter critério verificável.
Aceite proposto: Recuperar conteúdo irrelevante e impedir encerramento falso da lacuna.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T044 → T218 [complements]
Como combinar: Detectar repetição de expansões sem progresso.
Interface: Referências visitadas e alternativas restantes.
Condição: Equivalência de buscas ser observável.
Aceite proposto: Repetir consultas parafraseadas e exigir mudança de estratégia.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar volume lido como progresso.
- Parar quando nenhuma abertura plausível puder alterar a decisão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar resolução de hipóteses com custo de leitura; modelos maiores podem escolher aberturas melhores, exigindo medição local.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T026, T067, T078

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S010 — Active Retrieval Augmented Generation

[https://arxiv.org/abs/2305.06983](https://arxiv.org/abs/2305.06983)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: FLARE usa previsão da próxima sentença e sinais de confiança para decidir consultas e regeneração.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

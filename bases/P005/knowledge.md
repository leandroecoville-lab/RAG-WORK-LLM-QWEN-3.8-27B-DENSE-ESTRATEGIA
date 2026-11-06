# P005 — Context & Memory Controller

**Nome canônico:** Context & Memory Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador proposto de contexto e memória

## P005:C01 — conceito

Context & Memory Controller é um nome editorial proposto para coordenar políticas entre contexto ativo e memória persistente. Decidiria quando recuperar, resumir, promover ou reconciliar informações, delegando armazenamento e montagem a outros componentes. Essas fronteiras são escolhas arquiteturais propostas; as fontes não atestam um controlador LAI implementado nem uma taxonomia padronizada com esse nome.

Como funciona:
- Observar eventos da tarefa, ocupação da janela e candidatos a memória com suas evidências.
- Distinguir decisões vigentes, hipóteses, resultados confirmados e conteúdo temporário antes de escolher o destino.
- Emitir comandos versionados para montagem de contexto e atualização de memória, preservando a origem das decisões.

## P005:C02 — aplicacao

Quando usar:
- Fluxos com múltiplos agentes ou sessões em que resumos, decisões e recuperação precisam seguir a mesma política.

Quando não usar:
- Como escritor irrestrito capaz de transformar qualquer saída fluente em fato persistente confirmado.

Implementação proposta:
- Proposta: definir regras de promoção por tipo; uma preferência declarada, uma inferência e um resultado de ferramenta exigem evidências distintas.
- Associar cada decisão de política à versão do estado observado e recusar atualização quando essa base já tiver mudado.
- Ao compactar, solicitar resumo com referências; ao encontrar conflito, registrar versões concorrentes e aplicar reconciliação explícita.

Aplicação LAI proposta:
Proposta LAI: estabelecer P005 como coordenador de política; P004 persiste, P007 recupera, P002 administra a janela e P001 monta a entrada.

## P005:C03 — riscos_validacao

Armadilhas:
- Dois controladores independentes podem promover conclusões incompatíveis ou alternar continuamente versões.
- Ausência no resumo não significa revogação de uma decisão; exclusão e supersessão precisam de eventos próprios.
- Políticas excessivamente agressivas acumulam erros como se fossem conhecimento consolidado.

Métricas sugeridas:
- Promoções corrigidas posteriormente, conflitos pendentes, decisões sem origem e custo de recuperação por etapa útil.

Testes propostos:
- Aceite proposto: inserir hipótese posteriormente refutada e verificar que ela não permanece como fato ativo.
- Rodar duas propostas sobre a mesma versão e exigir resolução do conflito; testar redução de contexto preservando uma obrigação vigente.

## P005:C04 — perguntas_proveniencia

Pergunta: Quem decide o que vira memória reutilizável?
Resposta: Nesta arquitetura proposta, a política do controlador, aplicando critérios de evidência e escopo; o runtime executa a persistência.

Pergunta: Uma decisão que desapareceu do resumo deixa de valer?
Resposta: Não automaticamente. Deve existir revogação, supersessão ou condição de validade verificável no registro persistente.

Pergunta: Qual regra diferencia memória de contexto?
Resposta: Uma informação pode ser útil agora sem merecer persistência, ou ser durável sem precisar ocupar a janela atual.

Pergunta: O que registrar em cada decisão?
Resposta: Identidade, versão da política, origem, motivo e revisão dos dados usados para permitir auditoria.

Escopo das fontes:
Fontes apoiam memória seletiva e persistência; autoridade, regras de promoção e fronteiras são desenho editorial proposto.

## P005:C05 — mecanismo_avancado

Context & Memory Controller é proposto como coordenador entre o que pode ser lido, o que cabe no próximo turno e o que merece persistência. Uma resposta recém-gerada não deve virar fato durável só porque apareceu no diálogo. A admissão de memórias precisa distinguir observação, inferência e instrução, além de registrar fonte e validade. A admissão no contexto tem objetivo diferente: selecionar informação útil para a tarefa atual dentro de um orçamento.

Condição de contorno:
Unificar políticas não exige um único banco ou processo. Centralização excessiva pode criar gargalo e misturar decisões de relevância com regras de autorização.

Contrato proposto:
- Entradas: Tarefa, identidade, candidatos de leitura, propostas de gravação, limites de contexto e políticas de retenção.
- Saídas: Decisões justificadas de admitir, adiar, rejeitar ou revisar, com manifesto do contexto e da memória afetada.
- Estado: Versão das políticas, pendências de validação, referências de origem e métricas de pressão por sessão.
- Invariante: Uma decisão de relevância não pode ampliar permissão; conteúdo inferido precisa continuar identificado como inferência ao ser persistido.

Compromissos de projeto:
- Coordenação reduz divergências de política, mas exige interfaces claras para não concentrar toda execução em um componente.
- Validar promoção de memória custa tempo; aceitar tudo acelera escrita e pode acumular conclusões incorretas.

## P005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: recuperar documento sem autorização, gerar hipótese plausível e tentar promovê-la como fato confirmado; exigir bloqueio de escopo e preservação explícita da natureza inferida.

Plano de avaliação proposto:
Comparar gravação irrestrita e admissão por proveniência em tarefas com correções e fontes conflitantes. Medir fatos indevidamente promovidos, utilidade no turno seguinte, custo e atrasos. Separar falhas de autorização de falhas de relevância.

Comparações:
- P001 (complements): A montagem de contexto consome decisões de admissão.
- P004 (complements): O runtime de memória recebe gravações e consultas autorizadas.

Afirmação rastreável:
Persistência de sessão e armazenamento durável entre sessões têm escopos distintos na documentação de memória.
Suporte: related; fontes: V3D-S016
Limite: O controlador unificado é proposta própria e precisa de implementação e avaliação específicas.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou políticas de contexto e memória. Aqui Context & Memory Controller é proposto com regras de precedência e filas de decisões revisáveis.

Projeto e decomposição
Defina precedência entre elegibilidade, validade, utilidade e custo. Informação muito relevante mas revogada não deve vencer seleção; relevância não amplia permissão nem confirma verdade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

Controle adaptativo
Separe caminho rápido de leitura e caminho de manutenção. Promoção, reconciliação e consolidação podem ter fila própria, evitando que cada pergunta reavalie todo o acervo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

Validação contrafactual
Compare controlador único irrestrito e políticas tipadas com decisões registradas. Meça promoção indevida, bloqueios desnecessários e custo por consulta; centralização lógica não exige processo monolítico. Unidade de avaliação: decisão de política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

USO AVANÇADO — Memória com correções
Cenário: Nova evidência contradiz regra ativa.
Estratégia: Suspender uso da regra afetada, preservar evidência e enviar reconciliação à fila prioritária; liberar somente após decisão explícita.
Papel do modelo pequeno: 8–14B propõe reconciliação.
Aceite proposto: Nenhuma projeção pode continuar aplicando regra suspensa como vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

USO AVANÇADO — Carga alta de observações
Cenário: Nem tudo merece memória durável.
Estratégia: Admitir observações em camada temporária, consolidar por tipo e promover somente candidatos úteis e sustentados.
Papel do modelo pequeno: 3–7B classifica; 15–30B integra.
Aceite proposto: Taxa de fatos sem origem promovidos deve ser medida e bloqueada pelo critério local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V3A-S032, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e elegibilidade básica com regras externas.
8–14B: Revisor de suporte e conflitos locais antes de atualização.
15–30B: Planejador de manutenção complexa entre conjuntos de memória.
Requisitos de treino/runtime: Tabela de políticas, estados de decisão e trilha de motivos; nomes e fronteiras do controlador são proposta editorial.
Não aplicar quando: O controlador pode escrever irrestritamente ou a política mistura autorização e relevância numa pontuação única.

## P005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## P005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P005 → T071 [requires]
Como combinar: Aplicar promoção por tipo de candidato.
Interface: Fonte, tipo, escopo e critério de aceite.
Condição: Evidência satisfizer critério específico.
Aceite proposto: Propor hipótese como fato e exigir rejeição identificável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P005 → P004 [feeds]
Como combinar: Emitir comandos de memória com pré-condições.
Interface: Comando, revisão-base e decisão de política.
Condição: Runtime validar conflito antes de confirmar.
Aceite proposto: Mudar estado durante decisão e impedir sobrescrita.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P005 → P001 [feeds]
Como combinar: Informar quais evidências são elegíveis.
Interface: IDs, validade, prioridade e motivos de exclusão.
Condição: Builder não reintroduzir conteúdo suspenso.
Aceite proposto: Recuperar fato revogado com score alto e impedir inclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V3A-S032, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar ausência no resumo como revogação.
- Não promover saída fluente sem origem verificável.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade das decisões de admissão e correção; política bem definida reduz erro acumulado, sem garantir raciocínio de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T058, T069, T071, T075, P001, P002, P004, P007

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T075 — Memory Reconciliation

**Nome canônico:** Memory Reconciliation  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T075  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reconciliação de memória

## T075:C01 — conceito

Reconcilia registros duplicados, divergentes ou temporariamente incompatíveis. O objetivo é determinar o que pode ser apresentado como vigente e o que permanece em disputa. Similaridade textual não basta para resolver autoridade, identidade ou tempo.

Como funciona:
- Detectar afirmações que se referem à mesma entidade e propriedade.
- Comparar origem, validade, versão e evidência.
- Criar resolução explícita ou manter conflito pendente sem apagar as fontes.

## T075:C02 — aplicacao

Quando usar:
- Ingestão de vários sistemas sobre a mesma entidade.
- Correções tardias e memórias produzidas por múltiplos agentes.

Quando não usar:
- Não escolher automaticamente o texto mais recente quando uma fonte antiga é a autoridade aplicável.

Implementação proposta:
- Proposta: separar duplicata exata, atualização temporal e contradição real.
- Definir prioridades de fontes por domínio e campo.
- Invalidar sínteses dependentes quando a resolução alterar o conhecimento vigente.

Aplicação LAI proposta:
Proposta LAI: decisões atuais de Leandro devem ter validade e origem explícitas; informações históricas permanecem rastreáveis e não substituem automaticamente a decisão vigente.

## T075:C03 — riscos_validacao

Armadilhas:
- Entidades homônimas podem ser fundidas indevidamente.
- Uma maioria de cópias pode vencer uma fonte primária se independência não for considerada.

Métricas sugeridas:
- Conflitos detectados e resoluções corretas.
- Tempo de propagação de correções e taxa de fusões indevidas.

Testes propostos:
- Apresentar duas informações válidas em períodos diferentes e evitar falso conflito.
- Apresentar duas fontes incompatíveis sem autoridade suficiente e exigir incerteza explícita.

## T075:C04 — perguntas_proveniencia

Pergunta: Reconciliar significa apagar a versão perdedora?
Resposta: Não necessariamente. Manter o histórico ajuda a explicar por que a conclusão mudou.

Pergunta: Um modelo pode resolver todos os conflitos?
Resposta: Não. Alguns exigem fonte adicional ou decisão autorizada; o sistema deve representar esse bloqueio.

Pergunta: A memória mais recente deve sempre vencer?
Resposta: Não. Ela pode ser uma cópia atrasada, hipótese ou erro. Compare autoridade, validade, identidade e evidências antes de decidir.

Pergunta: Posso repetir usando uma nova chave de operação?
Resposta: Uma nova chave pode representar outra ação e duplicar o efeito. Reutilize identidade conforme o contrato do provedor e investigue o resultado anterior.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T075:C05 — mecanismo_avancado

Reconciliação envolve observações incompletas, além de contradições textuais. Uma operação externa pode ter sido aplicada enquanto sua confirmação se perdeu; o estado local fica desconhecido, não fracassado. A reconciliação busca recibo ou estado remoto usando identidade estável da operação, registra o resultado observado e só então decide continuidade. Para conhecimento, a mesma disciplina separa correção temporal, disputa de fonte e simples duplicação.

Condição de contorno:
Sem identificador correlacionável ou interface de consulta do serviço, pode ser impossível determinar automaticamente se um efeito ocorreu; a incerteza deve permanecer explícita.

Contrato proposto:
- Entradas: Registros divergentes, identidades, versões, tempos e observações de fontes autoritativas.
- Saídas: Estado reconciliado ou disputa persistente, com justificativa e evidências da decisão.
- Estado: Tentativas, chaves de operação, revisões corrigidas e derivados que precisam invalidação.
- Invariante: Ausência de confirmação local nunca é convertida automaticamente em prova de não execução externa.

Compromissos de projeto:
- Consultar a fonte autoritativa reduz duplicação e acrescenta latência e dependência de disponibilidade.
- Resolução automática acelera convergência e precisa ser limitada quando autoridade ou identidade permanecem ambíguas.

## T075:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: simular sucesso remoto seguido de perda da resposta e reinício local. A reconciliação deve consultar o efeito pela identidade conhecida, evitando reenviar cegamente ou compensar algo cujo resultado ainda não foi confirmado.

Plano de avaliação proposto:
Avaliação proposta: comparar última escrita vence e reconciliação por identidade e evidência em duplicatas, atualizações e resultados incertos. Medir convergência correta, efeitos duplicados, conflitos preservados e tempo; incluir fontes indisponíveis e recibos atrasados.

Comparações:
- T065 (complements): Transações protegem estado local; reconciliação observa o que ocorreu fora dessa fronteira.
- T058 (complements): Consolidações dependentes devem ser reavaliadas quando a reconciliação muda o conhecimento vigente.

Afirmação rastreável:
A documentação de tolerância a falhas do LangGraph orienta tratar confirmação perdida como resultado desconhecido e consultar o provedor.
Suporte: direct; fontes: V3A-S030
Limite: Isso não fornece uma solução automática para qualquer serviço; deduplicação e consulta dependem das garantias da API externa.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T075:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou ACK perdido. Aqui reconciliação separa conflito epistemológico, conflito de versão e efeito externo incerto.

Projeto e decomposição
Cada classe exige evidência diferente. Versões concorrentes pedem regra de atualização; afirmações contraditórias pedem fontes; efeito externo incerto pede consulta ao sistema que executou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

Controle adaptativo
Não resolva tudo por última escrita ou votação. Uma correção tardia pode ser mais válida que relato recente; várias cópias da mesma origem não constituem consenso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

Validação contrafactual
Compare reconciliador genérico e rotas tipadas. Meça duplicação de efeitos, perda de correções e conflitos encerrados sem evidência; incluir estado explicitamente inconclusivo. Unidade de avaliação: conflito ou operação incerta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

USO AVANÇADO — Memórias contraditórias
Cenário: Agentes registram fatos incompatíveis.
Estratégia: Agrupar pelo mesmo sujeito e escopo, comparar fontes e preservar alternativas quando não houver critério decisivo.
Papel do modelo pequeno: 8–14B explica conflito.
Aceite proposto: Não escolher fato apenas por formulação mais confiante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

USO AVANÇADO — Operação sem recibo
Cenário: A chamada externa pode ter concluído.
Estratégia: Consultar por identificador estável; se status não for determinável, suspender retry e registrar resolução necessária. Compensação também é novo efeito controlado.
Papel do modelo pequeno: 3–7B classifica status; controlador decide.
Aceite proposto: Nenhum reenvio cego pode criar efeito duplicado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S006, V4A-S011, V2A-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipos de conflito e estados observados.
8–14B: Reconciliador de afirmações com fontes e escopos explícitos.
15–30B: Planejador de resolução complexa, mantendo efeitos sob protocolo determinístico.
Requisitos de treino/runtime: Identidade de operação, versões e evidência externa consultável; registrar desconhecido como estado válido.
Não aplicar quando: A aplicação exige conclusão definitiva sem acesso a informação que decide o conflito.

## T075:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C007 — Amazon / Dynamo em serviços Amazon
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores descrevem adoção de Dynamo por serviços centrais da Amazon.
Mecanismo documentado: Versionamento de objetos e resolução de conflitos assistida pela aplicação.
Correspondência com esta base: Conflitos de objetos são resolvidos pela aplicação; não confirma reconciliação de efeitos LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Apresentar versões concorrentes ao reconciliador pequeno sem permitir que ele descarte evidência sozinho.
Limite: Dynamo histórico não equivale a todos os produtos DynamoDB; particionamento por hash não é CAS. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S006.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: Detecção de versões divergentes fundamenta reconciliação de estado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q006, V4A-Q007.

## T075:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T075 → T243 [requires]
Como combinar: Tratar efeitos incertos pelo protocolo do serviço.
Interface: operation_id, consulta de status e recibos.
Condição: Serviço oferecer mecanismo ou intervenção definida.
Aceite proposto: Simular efeito concluído com resposta perdida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S006, V4A-S011, V2A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T075 → T056 [complements]
Como combinar: Separar recência do relato e validade do fato.
Interface: Tempos de validade, registro e fonte.
Condição: Escopos temporais serem comparáveis.
Aceite proposto: Inserir correção tardia e impedir vitória automática do último relato.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S006, V4A-S011, V2A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter timeout em falha confirmada.
- Não executar compensação antes de saber qual efeito ocorreu.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar resolução correta e preservação de incerteza; eloquência não resolve estado externo desconhecido.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T054, T056, T058, T072

## Fontes primárias associadas

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S035 — Graphiti: Build Real-Time Knowledge Graphs for AI Agents

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grafo temporal de entidades, relações e episódios com rastreabilidade.

Limite: README consultado; sem auditoria de código, teste de escala ou confirmação de promessas comerciais.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S006 — Dynamo: Amazon’s highly available key-value store

[https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso em serviços Amazon; versões de objetos e resolução de conflitos pela aplicação.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

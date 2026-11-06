# T071 — Memory Promotion

**Nome canônico:** Memory Promotion  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T071  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** promoção de memória

## T071:C01 — conceito

Processo de admitir informação em uma categoria de maior reutilização ou confiança, por exemplo de observação para fato candidato, de episódios para procedimento e de procedimento para skill. A promoção é uma decisão de qualidade; mover um arquivo de pasta não comprova aprendizado.

Como funciona:
- Definir destino, requisitos e evidências necessárias.
- Verificar origem, repetibilidade e limites de aplicação.
- Registrar decisão de promoção com versão e possibilidade de reversão.

Nota de nomenclatura: Política arquitetural proposta; não existe limiar universal de evidência aplicável a toda memória.

## T071:C02 — aplicacao

Quando usar:
- Agentes que transformam experiências em conhecimento reutilizável.
- Curadoria de skills a partir de resultados de execução.

Quando não usar:
- Não promover por número de repetições quando todas derivam da mesma afirmação inicial.

Implementação proposta:
- Proposta: estabelecer critérios diferentes para fato, regra e procedimento.
- Exigir testes novos para procedimentos e evidência independente quando cabível.
- Manter dependências para rebaixar ou invalidar uma memória se suas fontes mudarem.

Aplicação LAI proposta:
Proposta LAI: promover episódios da Helena a procedimentos somente após validação fora do caso original; hipóteses continuam utilizáveis como hipóteses.

## T071:C03 — riscos_validacao

Armadilhas:
- A autoconfirmação pode promover erros com aparência de consenso.
- Critérios rígidos demais podem impedir reutilização útil de hipóteses claramente rotuladas.

Métricas sugeridas:
- Precisão das memórias promovidas em tarefas posteriores.
- Taxa de reversão e tempo até detectar generalização errada.

Testes propostos:
- Apresentar cinco cópias do mesmo relato e não tratá-las como cinco confirmações.
- Invalidar a evidência de uma skill e exigir revisão de seu status.

## T071:C04 — perguntas_proveniencia

Pergunta: Promoção precisa alterar pesos?
Resposta: Não. Pode mudar estado editorial e disponibilidade de uma memória externa.

Pergunta: É possível reverter uma promoção?
Resposta: O desenho deve permitir: correções e novos resultados podem exigir rebaixar confiança ou retirar um procedimento de uso.

Pergunta: Toda hipótese precisa ser promovida para ser útil?
Resposta: Não. Pode orientar investigação com seu status explícito. O erro é tratá-la como premissa confirmada sem a mudança de evidência necessária.

Pergunta: Como rebaixar um procedimento sem apagar aprendizado?
Resposta: Preserve histórico e motivo, suspenda recomendação no escopo afetado e mantenha acesso aos casos que ainda explicam quando ele funcionou.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T071:C05 — mecanismo_avancado

Promover memória altera sua autoridade de uso, não apenas seu endereço. Um fato candidato pode ser útil para busca exploratória antes de ser aceito como premissa operacional. Um procedimento testado em ambiente específico pode ser recomendado apenas naquele escopo. A decisão de promoção deve registrar critérios satisfeitos e dependências; quando uma fonte é corrigida, o sistema precisa reavaliar a promoção e os consumidores derivados.

Condição de contorno:
A promoção é frágil quando validação usa os mesmos casos que originaram a regra ou quando uma revisão bem escrita substitui evidência de aplicabilidade.

Contrato proposto:
- Entradas: Memória candidata, evidências, escopo pretendido e critérios proporcionais à consequência do uso.
- Saídas: Status de promoção com justificativa, limites e pendências de validação.
- Estado: Histórico de decisões, revisores ou verificadores, dependências e condições de rebaixamento.
- Invariante: Aumento de autoridade exige evidência adequada; frequência de repetição ou consenso entre cópias não basta.

Compromissos de projeto:
- Critérios explícitos reduzem propagação de erros e acrescentam tempo até reutilização ampla.
- Manter candidatos acessíveis favorece descoberta e exige que o leitor respeite seus estados de incerteza.

## T071:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: promover uma regra apoiada por duas notas que derivam da mesma origem, depois corrigir essa origem. A política deve reconhecer dependência comum e reavaliar a regra promovida.

Plano de avaliação proposto:
Avaliação proposta: comparar promoção imediata e promoção com validação independente em casos novos. Medir falsos conhecimentos aceitos, utilidade perdida por bloqueio, tempo de revisão e propagação de correções; separar fatos, hipóteses e procedimentos.

Comparações:
- T058 (distinct_from): Consolidação produz uma representação; promoção decide quais usos e grau de confiança ela pode receber.
- T055 (complements): Procedimentos podem ser promovidos para reutilização sob pré-condições verificadas e versões compatíveis.

Afirmação rastreável:
PROV-DM permite registrar derivação e responsabilidade de entidades, fornecendo estrutura para rastrear a origem de memórias candidatas.
Suporte: related; fontes: V3A-S037
Limite: Os critérios de promoção são proposta editorial; o padrão de proveniência não certifica conteúdo nem prescreve aprovação de memórias.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T071:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou promoção e mudança de pasta. Aqui promoção exige período de uso observado e critérios diferentes por tipo de memória.

Projeto e decomposição
Crie estados candidato, validado para escopo e ativo. Preferência explícita pode ter caminho curto; regra inferida de episódios precisa de suporte e teste de transferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

Controle adaptativo
Antes de promoção ampla, usar candidato em modo de comparação sem alterar decisões reais. Registrar quando ele ajudaria, conflitaria ou ampliaria incorretamente o escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

Validação contrafactual
Compare admissão imediata e promoção por evidência. Meça falsos fatos ativos, utilidade futura e tempo até corrigir promoção indevida; mais candidatos aprovados não indica melhor aprendizado. Unidade de avaliação: candidato promovido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

USO AVANÇADO — Preferência declarada
Cenário: Usuário define padrão para um projeto.
Estratégia: Registrar fonte explícita, escopo e condição de revisão; recuperar em tarefa elegível e evitar generalização para outros projetos.
Papel do modelo pequeno: 3–7B extrai declaração.
Aceite proposto: Escopo armazenado deve corresponder ao pedido literal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

USO AVANÇADO — Regra operacional inferida
Cenário: Vários incidentes sugerem recomendação.
Estratégia: Consolidar evidências independentes, testar em caso novo e promover apenas condições verificadas. Manter exceções junto da regra.
Papel do modelo pequeno: 15–30B compara casos.
Aceite proposto: Regra deve recusar aplicação fora das condições validadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S037, V4A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de candidatos explícitos com tipo e origem.
8–14B: Revisor de suporte local e compatibilidade de escopo.
15–30B: Analista de abstrações entre episódios, com validação externa.
Requisitos de treino/runtime: Estados de promoção, critérios por tipo e caminho de revogação; autoridade não deriva do texto produzido pelo modelo.
Não aplicar quando: Não há fonte para o candidato ou o único suporte é repetição da mesma inferência.

## T071:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C018 — OpenAI / ChatGPT Memory
Evidência: produto/recurso disponível; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Produto documenta memórias salvas e uso de histórico para personalização.
Mecanismo documentado: Informações selecionadas podem atravessar conversas com controles próprios.
Correspondência com esta base: Seleção do que lembrar não prova política de promoção desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Criar memória externa pequena de preferências explícitas e testar correções e escopo.
Limite: Comportamento varia por conta; fonte não revela algoritmo nem prova precisão permanente. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S017.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q013, V4A-Q023.

## T071:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T071 → T058 [requires]
Como combinar: Receber candidato consolidado com divergências preservadas.
Interface: Proposição, fontes, exceções e limites.
Condição: Consolidação não apagar evidência contrária.
Aceite proposto: Testar candidato aparentemente consensual derivado de uma única origem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S037, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T071 → T075 [complements]
Como combinar: Revisar promoção após evidência nova.
Interface: Memória ativa, correção e dependentes.
Condição: Revogação alcançar projeções e resumos.
Aceite proposto: Corrigir regra e verificar que uso futuro deixa de aplicá-la.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S037, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover conclusão pelo grau de confiança verbal.
- Não interpretar frequência de uso como confirmação independente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de memórias ativas no futuro; promoção controlada reduz erro acumulado sem tornar o modelo infalível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T048, T055, T058, T204

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

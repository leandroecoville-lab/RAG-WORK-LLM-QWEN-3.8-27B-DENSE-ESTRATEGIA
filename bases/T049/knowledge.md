# T049 — Episodic Memory

**Nome canônico:** Episodic Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T049  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória episódica

## T049:C01 — conceito

Registra experiências situadas: objetivo, contexto, ações, resultados, tempo e evidências. Permite recuperar casos anteriores para orientar novas tarefas. Um episódio mostra o que ocorreu em determinadas condições; não prova sozinho uma regra geral nem garante que a mesma ação funcionará novamente.

Como funciona:
- Delimitar uma experiência e identificar participantes, ambiente e versão.
- Registrar sequência e resultados com evidências.
- Indexar por problema, condições e desfecho para recuperação futura.

## T049:C02 — aplicacao

Quando usar:
- Aprender procedimentos a partir de incidentes ou missões concluídas.
- Retomar casos semelhantes com contexto operacional verificável.

Quando não usar:
- Não reduzir uma experiência a uma frase de sucesso sem guardar condições e falhas.

Implementação proposta:
- Proposta: separar observações, ações propostas, ações executadas e resultados validados.
- Manter um resumo do episódio e referências ao log completo.
- Recuperar casos contrastantes, incluindo tentativas malsucedidas, para evitar confirmação seletiva.

Aplicação LAI proposta:
Proposta LAI: armazenar auditorias e correções da Helena como episódios verificáveis antes de promover seus aprendizados a skills.

## T049:C03 — riscos_validacao

Armadilhas:
- Relato do agente pode confundir intenção com execução.
- Um caso de outra versão pode induzir uma correção incompatível.

Métricas sugeridas:
- Recall de episódios relevantes e diversidade de resultados.
- Melhoria em tarefas novas comparada à execução sem memória.

Testes propostos:
- Buscar um incidente conhecido sem mencionar seu ID.
- Alterar versão do ambiente e exigir que a solução antiga seja revalidada.

## T049:C04 — perguntas_proveniencia

Pergunta: Episódio é a conversa inteira?
Resposta: Pode conter conversa, mas deve ter fronteiras, objetivo e resultado. Um histórico bruto não fornece automaticamente essa estrutura.

Pergunta: Uma correção que funcionou vira regra?
Resposta: Vira evidência de um caso. Generalização exige condições de aplicação e novas avaliações.

Pergunta: Qual é a unidade correta de episódio?
Resposta: A menor sequência que conserva objetivo, condições e desfecho interpretável. Pode atravessar sessões; uma sessão pode conter vários episódios.

Pergunta: Casos incompletos devem entrar no índice?
Resposta: Podem ser úteis, desde que a incompletude seja recuperável como campo. O leitor não deve interpretar ausência de resultado como resultado negativo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T049:C05 — mecanismo_avancado

Um episódio precisa preservar o que o agente sabia no momento da decisão. Acrescentar a solução descoberta depois à descrição inicial cria retrospectiva enganosa e ensina um procedimento impossível de reproduzir. Resultados também podem ser censurados: uma tarefa interrompida não é necessariamente fracasso, e sucesso sem verificação pode ser apenas ausência de erro observado. Esses estados devem sobreviver à síntese do caso.

Condição de contorno:
Casos históricos deixam de orientar bem quando foram selecionados somente por sucesso ou quando as condições anteriores à ação não podem ser reconstruídas.

Contrato proposto:
- Entradas: Sequência do episódio, evidências disponíveis por etapa e observações posteriores separadas.
- Saídas: Caso recuperável com contexto inicial, decisões, desfecho e limitações de observação.
- Estado: Versões do ambiente, fronteiras do episódio, participantes e proveniência dos resultados.
- Invariante: Informação conhecida depois não aparece como premissa disponível antes de sua observação.

Compromissos de projeto:
- Episódios completos melhoram análise de sequência e aumentam o custo de leitura.
- Resumos favorecem busca por problema e podem esconder tentativas malsucedidas que explicam o desfecho.

## T049:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: registrar uma tarefa encerrada antes da validação e adicionar a conclusão em data posterior. A consulta histórica deve distinguir resultado desconhecido naquele instante de resultado posteriormente confirmado.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação por objetivo e por condições iniciais usando casos positivos, negativos e interrompidos. Medir adequação da analogia, reconstrução temporal e confusão entre intenção e efeito; avaliar transferência entre versões separadamente.

Comparações:
- T070 (complements): O episodic store fornece armazenamento e índices; memória episódica define a unidade de experiência e sua interpretação.
- T057 (distinct_from): Uma sequência lembrada pode sugerir hipótese, mas não identifica por si só o efeito de uma intervenção.

Afirmação rastreável:
Generative Agents mantém experiências em um fluxo de memória e usa sua recuperação para orientar comportamento.
Suporte: direct; fontes: A-S008
Limite: A avaliação de plausibilidade em simulação não demonstra validade causal nem qualidade de procedimentos de produção.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T049:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou episódios e vazamento retrospectivo. Aqui recuperação usa semelhança de condições e resultados negativos para evitar transferência superficial.

Projeto e decomposição
Indexe condições iniciais, ação, resultado e fatores desconhecidos separadamente. Episódios com narrativa parecida podem exigir ações opostas quando uma pré-condição muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

Controle adaptativo
Recupere exemplos de sucesso e falha com condições próximas. Ausência de falhas no histórico pode refletir seleção de registros, não prova de segurança do procedimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

Validação contrafactual
Compare recuperação por texto integral e por condições estruturadas. Meça recomendações transferidas indevidamente, cobertura de falhas e qualidade em episódios com resultado ainda pendente. Unidade de avaliação: episódio completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

USO AVANÇADO — Diagnóstico recorrente
Cenário: Sintomas semelhantes tiveram causas diferentes.
Estratégia: Recuperar episódios por ambiente e versão, comparar testes discriminantes e evitar repetir ação que falhou nas mesmas condições.
Papel do modelo pequeno: 8–14B compara episódios.
Aceite proposto: Recomendação deve explicar condição compartilhada e diferença que pode invalidar transferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

USO AVANÇADO — Aprendizado de projeto
Cenário: Uma decisão anterior parece reutilizável.
Estratégia: Carregar contexto da escolha e alternativas rejeitadas; testar se restrições atuais ainda coincidem antes de aplicar.
Papel do modelo pequeno: 15–30B integra experiências.
Aceite proposto: Não usar resultado posterior que ainda não era conhecido na data avaliada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008, V3A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de condições, ações e resultados explícitos.
8–14B: Comparador de poucos episódios com esquema comum.
15–30B: Planejador de testes para adaptar experiência a contexto parcialmente diferente.
Requisitos de treino/runtime: Registro de episódios com estados pendente/concluído e documentação das condições observadas.
Não aplicar quando: Histórico registra somente casos bem-sucedidos ou omite condições que determinam o resultado.

## T049:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Experiências recuperáveis integram a arquitetura.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q008, V4A-Q023.

## T049:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T049 → T070 [requires]
Como combinar: Buscar episódios por campos e não apenas similaridade.
Interface: Condições, tempo, ação e estado do resultado.
Condição: Store permitir filtros e paginação verificável.
Aceite proposto: Recuperar também falha rara com mesmas pré-condições.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T049 → T055 [feeds]
Como combinar: Transformar experiência em procedimento candidato.
Interface: Episódios de suporte, limites e exceções.
Condição: Transferência validada antes de uso geral.
Aceite proposto: Aplicar a contexto com pré-condição ausente e exigir recusa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008, V3A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar correlação entre ação e resultado como causalidade.
- Não transformar resultado desconhecido em falha.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar transferência correta de experiência, não plausibilidade da narrativa recuperada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T058, T070, T071, T181

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

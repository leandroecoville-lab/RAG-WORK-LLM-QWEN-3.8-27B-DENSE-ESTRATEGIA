# T039 — Importance-Aware Window

**Nome canônico:** Importance-Aware Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T039  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela orientada à importância

## T039:C01 — conceito

Janela de contexto que prioriza unidades pelo valor esperado para a tarefa, em vez de manter apenas as mais recentes. Importância pode combinar obrigatoriedade, relevância, impacto e recência. Esses critérios são decisões de engenharia; um escore de LLM não é uma medida objetiva de verdade.

Como funciona:
- Classificar unidades por papel e obrigatoriedade.
- Pontuar conteúdo opcional e considerar dependências.
- Escolher conjunto que caiba no orçamento preservando o essencial.

Nota de nomenclatura: Nome descritivo de uma política de seleção, não algoritmo universal ou benchmark estabelecido.

## T039:C02 — aplicacao

Quando usar:
- Missões longas com decisões antigas ainda relevantes.
- Histórico volumoso com poucos marcos decisivos.

Quando não usar:
- Não deixar permissões e restrições críticas dependerem exclusivamente de um escore probabilístico.

Implementação proposta:
- Proposta: separar conteúdo fixado por regra de conteúdo elegível a ranking.
- Registrar justificativa curta de inclusão e origem.
- Reavaliar importância quando objetivo ou estado da missão mudar.

Aplicação LAI proposta:
Proposta LAI: fixar decisões vigentes e evidências operacionais da Helena; usar ranking somente para material complementar e casos semelhantes.

## T039:C03 — riscos_validacao

Armadilhas:
- Autoavaliação do modelo pode dar peso excessivo à própria hipótese.
- A importância muda com o problema e não deve ser congelada para sempre.

Métricas sugeridas:
- Recall de fatos críticos antigos.
- Tokens usados por evidência efetivamente aproveitada na resposta.

Testes propostos:
- Colocar uma decisão antiga indispensável entre muitos eventos recentes.
- Alterar o objetivo e verificar que a seleção muda sem apagar o histórico.

## T039:C04 — perguntas_proveniencia

Pergunta: Importante significa verdadeiro?
Resposta: Não. Uma hipótese muito relevante ainda pode ser falsa e precisa manter seu status.

Pergunta: Preciso usar embeddings para medir importância?
Resposta: Não. Regras de domínio, tipo de evento e dependências podem ser mais apropriados para certos campos.

Pergunta: É adequado normalizar todos os escores juntos?
Resposta: Depende do significado e da distribuição de cada critério. Normalização por candidatos pode mudar prioridades quando novos itens entram.

Pergunta: Como evitar que uma memória acessada domine para sempre?
Resposta: Separe frequência de acesso, validade e novidade. Faça avaliações com fatos antigos pouco acessados que continuam necessários à tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T039:C05 — mecanismo_avancado

Selecionar por importância pode ser formulado como alocação de orçamento: maximizar utilidade estimada de unidades com custos em tokens. Entretanto, a utilidade raramente é aditiva. Uma definição e sua exceção podem ser úteis apenas juntas; dois exemplos quase idênticos competem pelo mesmo benefício. O seletor deve considerar dependências e redundância, além de pontuações individuais, para evitar escolher um conjunto aparentemente forte e logicamente incompleto.

Condição de contorno:
Quando a função de utilidade é mal calibrada, otimizar o ranking apenas torna mais consistente uma seleção equivocada de conteúdo.

Contrato proposto:
- Entradas: Unidades com custo, origem, status, dependências e escores separados por critério.
- Saídas: Conjunto selecionado e relatório das restrições preservadas e dependências não atendidas.
- Estado: Modelo de importância, pesos, histórico de acesso e orçamento efetivo da chamada.
- Invariante: Prioridade de leitura não altera confiança factual, autorização ou validade temporal de uma memória.

Compromissos de projeto:
- Escores combinados permitem adaptação, mas tornam difícil explicar qual critério excluiu uma evidência.
- Atualizar importância por acesso favorece continuidade e pode criar ciclos em que apenas lembranças já populares permanecem visíveis.

## T039:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma conclusão relevante e uma ressalva de baixo escore cuja remoção muda seu alcance. A seleção deve conservar a dependência ou recusar a conclusão isolada.

Plano de avaliação proposto:
Avaliação proposta: comparar recência, ranking individual e seleção com dependências sob orçamento igual. Medir cobertura de pares necessários, diversidade, custo de seleção e persistência de erros autorreforçados; testar mudança explícita de objetivo.

Comparações:
- T018 (complements): A poda executa a exclusão; importância fornece um dos critérios para decidir quais unidades podem sair.
- T040 (complements): O estado da tarefa fornece dependências obrigatórias que um ranking de importância sozinho pode desconhecer.

Afirmação rastreável:
Generative Agents combina critérios de recuperação para escolher memórias pertinentes ao comportamento simulado.
Suporte: related; fontes: A-S008
Limite: A evidência apoia seleção multifatorial em uma arquitetura específica, não uma função universal de importância operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T039:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 formulou valor não aditivo. Aqui prioridades da janela incluem custo de reconstrução e risco de esquecimento de obrigações.

Projeto e decomposição
Calcule prioridade por necessidade imediata, custo de reabrir e impacto de omissão. Conteúdo fácil de recuperar pode sair antes de uma decisão rara que exige vários passos para reconstruir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

Controle adaptativo
Use envelhecimento de prioridades para impedir que informação sempre citada monopolize janela. Fixação precisa de condição de liberação, ou a política deixa de administrar recursos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

Validação contrafactual
Compare prioridade por recência, frequência e custo de reconstrução. Meça retomadas, leituras adicionais e obrigações perdidas; manter iguais os limites de janela e saída. Unidade de avaliação: janela de execução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

USO AVANÇADO — Diagnóstico longo
Cenário: Uma hipótese depende de evidência antiga cara.
Estratégia: Fixar evidência até testar a hipótese; liberar após registrar resultado e referência, não após mero número de turnos.
Papel do modelo pequeno: 8–14B gerencia hipóteses locais.
Aceite proposto: Não repetir investigação porque a evidência decisiva foi removida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

USO AVANÇADO — Projeto com várias frentes
Cenário: Assuntos recentes competem com decisão crítica.
Estratégia: Reservar espaço para contratos ativos e mover detalhes reabríveis; revisar prioridades quando a tarefa mudar.
Papel do modelo pequeno: 3–7B classifica blocos; 15–30B integra.
Aceite proposto: Decisão deve manter restrições mesmo com ruído recente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e recuperabilidade de blocos.
8–14B: Controlador de hipóteses com liberação explícita de conteúdo fixado.
15–30B: Planejador entre frentes com custos de reconstrução diferentes.
Requisitos de treino/runtime: Metadados de dependência, custo de leitura e estados de obrigação; limites devem ser aplicados em código.
Não aplicar quando: Todos os blocos são declarados indispensáveis sem possibilidade de decompor a tarefa.

## T039:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T039:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T039 → T074 [feeds]
Como combinar: Usar prioridade para escolher conteúdo removível.
Interface: Valor, custo de recarga e condição de fixação.
Condição: Evicção não destruir única cópia durável.
Aceite proposto: Medir recargas e repetição de trabalho.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T039 → T040 [requires]
Como combinar: Recalcular importância após mudança de fase.
Interface: Estado atual, objetivo e contratos ativos.
Condição: Mudança de estado ser confirmada.
Aceite proposto: Cancelar hipótese e verificar liberação do bloco fixado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não premiar acesso causado pelo próprio ranking sem correção.
- Preservar conteúdo raro exigido por obrigação ativa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade com igual janela; mais tokens de alta prioridade não significam raciocínio melhor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T018, T040, T048

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

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

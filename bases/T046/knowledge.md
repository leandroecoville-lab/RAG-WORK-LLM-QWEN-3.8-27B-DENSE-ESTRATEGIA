# T046 — Dynamic Few-Shot Selection

**Nome canônico:** Dynamic Few-Shot Selection  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T046  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** seleção dinâmica de demonstrações

## T046:C01 — conceito

Escolhe exemplos de demonstração para cada consulta, conforme similaridade, diversidade, dificuldade e orçamento. Adapta o comportamento mostrado ao modelo sem atualizar pesos. Os exemplos devem ensinar a tarefa e não vazar a resposta do conjunto de avaliação.

Como funciona:
- Manter banco de exemplos com entrada, saída validada e metadados.
- Selecionar exemplos relevantes para a nova tarefa.
- Limitar redundância e compor prompt com ordem controlada.

## T046:C02 — aplicacao

Quando usar:
- Muitas classes ou formatos de solicitação.
- Tarefas em que exemplos estáticos ocupam contexto sem ajudar a pergunta atual.

Quando não usar:
- Não selecionar demonstrações com saídas não verificadas apenas porque se parecem semanticamente com a consulta.

Implementação proposta:
- Proposta: indexar exemplos por tarefa, versão de schema e idioma.
- Aplicar diversidade ou cotas para incluir exceções úteis.
- Separar exemplos de treino, desenvolvimento e teste por origem documental.

Aplicação LAI proposta:
Proposta LAI: selecionar exemplos de extração e ferramentas já aprovados conforme a missão, preservando casos de erro e ausência de dados.

## T046:C03 — riscos_validacao

Armadilhas:
- Exemplos quase idênticos reduzem cobertura de comportamentos.
- Mudança de schema pode tornar demonstrações antigas nocivas.

Métricas sugeridas:
- Qualidade por classe e orçamento de exemplos.
- Ganho sobre seleção fixa e aleatória com mesmo número de tokens.

Testes propostos:
- Consultar uma classe rara e verificar presença de uma demonstração válida.
- Alterar schema de saída e impedir seleção de exemplos incompatíveis.

## T046:C04 — perguntas_proveniencia

Pergunta: Isso é fine-tuning?
Resposta: Não. Os exemplos entram no contexto de cada chamada; os parâmetros do modelo permanecem iguais.

Pergunta: O exemplo mais parecido é sempre o melhor?
Resposta: Não. Diversidade e cobertura de exceções podem ser mais úteis que repetição de um caso quase idêntico.

Pergunta: É preciso recuperar entrada e saída juntas?
Resposta: A busca pode usar a entrada, mas a demonstração final precisa de saída validada e compatível. Não busque por uma resposta de teste desconhecida.

Pergunta: Mais diversidade sempre ajuda?
Resposta: Não. Exemplos desconectados podem confundir a tarefa. Compare diversidade condicionada ao objetivo com similaridade pura usando o mesmo orçamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T046:C05 — mecanismo_avancado

A seleção dinâmica altera a distribuição das demonstrações vista a cada pergunta. Buscar vizinhos muito semelhantes pode concentrar uma classe e induzir o modelo a tratá-la como resposta padrão. A ordem também é parte do experimento: manter exemplos selecionados e variar sua sequência pode modificar resultados. Um banco de exemplos precisa registrar origem para que duplicatas de um mesmo documento não atravessem as divisões de avaliação.

Condição de contorno:
Similaridade de superfície é insuficiente quando exemplos parecidos exigem decisões diferentes por uma exceção, versão de schema ou condição negativa.

Contrato proposto:
- Entradas: Consulta, exemplos validados, origem documental e política de cobertura por tarefa.
- Saídas: Demonstrações elegíveis com ordem, orçamento e justificativa de seleção registrados.
- Estado: Encoder, banco versionado, divisões por origem e histórico de revisão das saídas.
- Invariante: Exemplos de avaliação e suas variantes derivadas não entram no banco usado para avaliá-los.

Compromissos de projeto:
- Vizinhos semânticos aproximam a demonstração da pergunta e podem reduzir diversidade de decisões.
- Controlar classe, dificuldade e ordem melhora diagnóstico, mas torna a seleção mais complexa e menos puramente baseada em distância.

## T046:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar vizinhos quase idênticos com rótulos distintos por uma única condição. O seletor deve conservar exemplos que mostrem a fronteira, sem escolher todos de uma classe.

Plano de avaliação proposto:
Avaliação proposta: comparar exemplos fixos, aleatórios e recuperados com tokens equivalentes. Variar ordem separadamente, medir desempenho por classe e estabilidade, e fazer divisão por documento ou origem; não atribuir ganho de quantidade ao algoritmo de seleção.

Comparações:
- T019 (complements): Poda reduz o conjunto de demonstrações; seleção dinâmica determina quais são úteis para a consulta atual.
- T005 (distinct_from): Uma demonstração orienta comportamento, enquanto uma resposta em cache tenta reutilizar um resultado já produzido.

Afirmação rastreável:
Pesquisas sobre exemplos em contexto investigam seleção por similaridade e mostram sensibilidade à ordem das demonstrações.
Suporte: direct; fontes: V3A-S016, V3A-S017
Limite: Os resultados dependem de modelos e tarefas estudados; uma ordenação favorável não transfere automaticamente para outro modelo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T046:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou viés e vazamento. Aqui seleção de exemplos é orientada por necessidade de habilidade e custo de interferência.

Projeto e decomposição
Recupere exemplos pelo tipo de transformação necessário, não apenas pelo assunto. Uma pergunta sobre finanças pode precisar de exemplo de extração temporal, não de narrativa financeira.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

Controle adaptativo
Separe exemplos de formato, decisão e exceção. Escolher vários exemplos da mesma função pode reforçar estilo e deixar a dificuldade real sem demonstração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

Validação contrafactual
Compare similaridade semântica e cobertura de habilidades com orçamento igual. Meça erros de transferência de entidade, rótulo e valor dos exemplos para o caso novo. Unidade de avaliação: consulta com demonstrações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

USO AVANÇADO — Extração variável
Cenário: Documentos diferem em layout e ambiguidade.
Estratégia: Selecionar um exemplo de formato e outro da exceção relevante; substituir nomes e valores somente quando isso não alterar o mecanismo demonstrado.
Papel do modelo pequeno: 3–7B aprende formato local.
Aceite proposto: Não copiar valores do exemplo para a saída real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

USO AVANÇADO — Tarefas com ferramentas
Cenário: Modelo confunde ordem de operações.
Estratégia: Selecionar demonstração com a mesma dependência entre chamadas, preservando diferenças de schema da ferramenta atual.
Papel do modelo pequeno: 8–14B planeja sequência curta.
Aceite proposto: Argumentos e versão devem vir do caso atual, não da demonstração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucas demonstrações contrastivas por habilidade fechada.
8–14B: Exemplos de sequência e tratamento de insuficiência.
15–30B: Demonstrações de integração de evidências sem depender de nomes do domínio.
Requisitos de treino/runtime: Banco de exemplos com metadados de habilidade e origem; particionar avaliação por fonte para evitar quase duplicatas.
Não aplicar quando: Exemplos disponíveis são contraditórios ou incompatíveis com o protocolo atual.

## T046:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q016.

## T046:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T046 → T019 [complements]
Como combinar: Remover demonstrações redundantes após selecionar habilidades.
Interface: Lista de exemplos, função e custo de tokens.
Condição: Todas as habilidades necessárias continuarem cobertas.
Aceite proposto: Excluir exemplo e testar fronteira que ele representava.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T046 → T036 [requires]
Como combinar: Extrair necessidade de habilidade da consulta.
Interface: Transformação, restrições e formato esperado.
Condição: Análise não depender da resposta desconhecida.
Aceite proposto: Testar assunto parecido com habilidade diferente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não selecionar pelo gabarito de avaliação.
- Não usar exemplos antigos de ferramenta como contrato atual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar transferência de habilidade em casos novos; mais exemplos semelhantes podem aumentar cópia indevida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T019, T155, T204

## Fontes primárias associadas

### A-S031 — SemanticSimilarityExampleSelector

[https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector](https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Seleção de exemplos por similaridade semântica.

Limite: Resultado de busca e módulo oficial consultados; abertura direta rejeitada por content-type text/markdown.

### V3A-S016 — What Makes Good In-Context Examples for GPT-3?

[https://arxiv.org/abs/2101.06804](https://arxiv.org/abs/2101.06804)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de demonstrações por recuperação de exemplos semelhantes; comportamento depende do conjunto e do modelo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S017 — Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity

[https://aclanthology.org/2022.acl-long.556/](https://aclanthology.org/2022.acl-long.556/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sensibilidade à ordem de demonstrações e não transferência automática de uma boa permutação entre modelos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

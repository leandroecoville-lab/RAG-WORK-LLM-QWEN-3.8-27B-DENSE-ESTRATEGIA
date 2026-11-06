# R007 — SADA

**Nome canônico:** SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** State-Aligned Distillation Adapters; adaptadores com alinhamento de estados

## R007:C01 — conceito

Pesquisa sobre conversão de contexto em adaptadores que procura preservar estados internos relevantes do modelo com contexto completo. O trabalho identifica divergência de estados entre o modelo com adaptador e o modelo de referência e propõe alinhamento para reduzir essa diferença.

Como funciona:
- Escolher representações internas adequadas para informar o mapeamento contexto-parâmetros.
- Usar a saída do bloco de atenção como interface de representação.
- Treinar com sinal de alinhamento entre os estados do modelo com adaptador e os do modelo com contexto completo.

Nota de nomenclatura: SADA está desambiguado pelo título completo da publicação; o nome sozinho não define compatibilidade com outros modelos.

## R007:C02 — aplicacao

Quando usar:
- Pesquisa que disponha de acesso às ativações e ao treinamento do modelo.
- Comparações controladas de retenção de contexto explícito versus compressão em parâmetros.

Quando não usar:
- Como recurso ativável apenas por prompt em uma API fechada sem acesso aos estados internos.

Implementação proposta:
- Proposta: verificar implementação, checkpoints e tarefas usadas no trabalho antes de portar a arquitetura.
- Reproduzir um caso pequeno medindo estados internos e desempenho final simultaneamente.
- Comparar com contexto completo e adaptação sem alinhamento, incluindo casos em que manter o texto é necessário.

Aplicação LAI proposta:
Proposta LAI: tratar como experimento de pesquisa posterior à memória externa e à destilação convencional, com critérios próprios de compatibilidade e ganho.

## R007:C03 — riscos_validacao

Armadilhas:
- Estados mais próximos não garantem resposta correta em toda tarefa.
- Mudar arquitetura ou tokenizer pode invalidar o mapeamento e exigir novo treinamento.

Métricas sugeridas:
- Qualidade da tarefa e divergência de representações por camada.
- Custo de produzir adaptadores, memória usada e latência total por contexto.

Testes propostos:
- Proposta: fazer ablação do alinhamento mantendo dados e orçamento constantes.
- Incluir perguntas que dependem de detalhes exatos para medir perdas ocultas pela média de desempenho.

## R007:C04 — perguntas_proveniencia

Pergunta: SADA é um banco de memória textual?
Resposta: Não. A referência identificada trata mapeamento de contexto em adaptadores e alinhamento de representações.

Pergunta: Alinhar estados torna a compressão sem perda?
Resposta: Não há garantia geral. É necessário medir tarefas e casos em que detalhes do contexto precisam permanecer explícitos.

Pergunta: Por que comparar estados e respostas separadamente?
Resposta: Divergência interna ajuda diagnosticar o mecanismo, mas a utilidade final depende da tarefa. Uma melhora em uma medida não substitui a outra.

Pergunta: O método equivale a resumir texto num arquivo?
Resposta: Não. Ele produz parâmetros de adaptação por uma interface neural treinada. Persistir um resumo externo opera em outro nível do sistema.

Escopo das fontes:
A-S012 sustenta a proposta de interface de estados e alinhamento. Não houve auditoria do código nem reprodução dos experimentos.

## R007:C05 — mecanismo_avancado

SADA aborda a diferença entre reproduzir uma resposta final e preservar estados internos próximos aos obtidos com contexto completo. Atribui divergência em camadas profundas à seleção de entrada inadequada e à supervisão insuficiente. Usa a saída do bloco de atenção como interface e alinhamento de estados na destilação. Isso exige acesso aos componentes internos; uma comparação apenas textual não reproduz o mecanismo proposto.

Condição de contorno:
Estados internos semelhantes não garantem por si só resposta correta, e a interface aprendida pode perder validade quando mudam backbone, camadas ou distribuição do contexto.

Contrato proposto:
- Entradas: Modelo compatível, contexto professor, representações internas selecionadas e mecanismo de geração de adaptadores.
- Saídas: Pesos temporários e avaliação da geração junto de medidas de divergência interna.
- Estado: Versões de camadas, treinamento, interface de features e configuração de leitura do adaptador.
- Invariante: Um adaptador é vinculado ao modelo e contexto de origem; não é tratado como memória universal intercambiável.

Compromissos de projeto:
- Comprimir contexto em parâmetros pode reduzir custo de inferência e exige computação para produzir e aplicar adaptadores.
- Alinhar estados oferece sinal de treinamento adicional e aumenta acesso necessário à arquitetura e custo de adaptação.

## R007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o backbone ou a interface de camada mantendo o mapeamento treinado. Verifique divergência interna e qualidade da saída, sem aceitar compatibilidade apenas porque os tensores têm dimensões iguais.

Plano de avaliação proposto:
Avaliação proposta: comparar contexto explícito, adaptação sem alinhamento e SADA com backbone fixo. Medir saída sustentada, distância de estados por camada, memória e latência incluindo geração do adaptador; incluir situações em que reter texto explícito é preferível.

Comparações:
- R006 (distinct_from): PRISM diagnostica componentes dominantes; SADA trata seleção de interface e supervisão de estados na parametrização do contexto.
- T052 (complements): O método depende de representações internas compatíveis, dentro da família ampla de contexto latente.

Afirmação rastreável:
SADA propõe attention-block output como interface e state-alignment distillation para reduzir divergência de estados frente ao modelo com contexto completo.
Suporte: direct; fontes: A-S012
Limite: Esta ficha refere-se ao artigo de Gao e coautores na ACL 2026; nenhuma garantia é transferida a trabalhos homônimos ou modelos arbitrários.

Nota de pesquisa:
Identificação reconferida em 2026-11-05: SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters, Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan e Zhou Xiao, https://aclanthology.org/2026.acl-long.1046/. Escopo coincide com a v2. Link de código consta na publicação, mas não houve instalação nem execução; contratos e avaliações são propostas.

## R007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 identificou SADA e interface de estados. Aqui adapters derivados de contexto recebem isolamento, expiração e avaliação funcional por sessão.

Projeto e decomposição
Preserve identidade: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters. A proposta exige relacionar adapter ao contexto que o produziu, ao modelo-base e à interface de estados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

Controle adaptativo
Se o contexto muda ou pertence a outro escopo, o adapter anterior não pode ser reutilizado por semelhança. Cache de adapter precisa de identidade exata e condições de validade, não apenas nome da tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

Validação contrafactual
Compare erro de alinhamento interno e qualidade final separadamente. Teste contexto correto, trocado e revogado; estados próximos podem produzir resposta errada ou conservar informação que já deveria ser desconsiderada. Unidade de avaliação: adapter e contexto de origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

USO AVANÇADO — Contexto recorrente especializado
Cenário: Muitas chamadas usam o mesmo material estável.
Estratégia: Avaliar custo de criar adapter e reutilizá-lo, mantendo caminho de leitura textual para mudanças e auditoria.
Papel do modelo pequeno: 15–30B modelo aberto experimental.
Aceite proposto: Amortização deve incluir geração, troca e invalidação do adapter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

USO AVANÇADO — Sessões isoladas
Cenário: Cada tarefa contém informações próprias.
Estratégia: Associar adapter a sessão e contexto, impedir carga cruzada e verificar limpeza ao trocar tarefa.
Papel do modelo pequeno: 8–14B somente se arquitetura adaptada.
Aceite proposto: Nenhuma saída pode usar conteúdo de contexto de outra sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Baseline textual ou aluno experimental restrito, sem compatibilidade presumida.
8–14B: Consumidor adaptado apenas com acesso a estados e treinamento validado.
15–30B: Alvo de pesquisa com instrumentação de camadas e análise de custo.
Requisitos de treino/runtime: Modelo aberto compatível, acesso aos estados, treino e versionamento; a pesquisa não é API universal para modelos fechados.
Não aplicar quando: Não há controle da interface neural ou o contexto muda antes de amortizar adaptação.

## R007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C033 — Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan, Zhou Xiao / SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda adaptação de contexto por alinhamento de estados.
Mecanismo documentado: Distilação aproxima estados em interface de blocos de atenção usando adapters.
Correspondência com esta base: Título e autores fixam escopo da sigla.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar modelo aberto em faixa permitida com instrumentação de estados e teste funcional separado.
Limite: Nenhuma produção bigtech exata estabelecida; alinhamento interno não garante resposta correta. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Não foi estabelecida implantação bigtech exata do SADA identificado. A transferência a 3–30B permanece proposta dependente de arquitetura, treino e avaliação.
Consultas registradas: V4A-Q017, V4A-Q024.

## R007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R007 → T052 [requires]
Como combinar: Fixar significado da representação alinhada.
Interface: Camada, tensor, máscara e versão do modelo.
Condição: Interface coincidir com o treinamento.
Aceite proposto: Trocar camada de leitura e medir falha funcional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S012, V3A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R007 → T031 [complements]
Como combinar: Invalidar adapter quando contexto ou escopo mudar.
Interface: Context_digest, session_id e validade.
Condição: Relação com contexto de origem ser verificável.
Aceite proposto: Revogar contexto e impedir carregamento do adapter antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S012, V3A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir SADA com siglas homônimas.
- Não usar alinhamento de estados como prova suficiente de correção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefa e modelo-base fixos com contexto textual; não prometer equivalência geral ao professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T052, T179, T182, R006

## Fontes primárias associadas

### A-S012 — SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters

[https://aclanthology.org/2026.acl-long.1046/](https://aclanthology.org/2026.acl-long.1046/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapeamento contexto-parâmetros e alinhamento de estados para adaptadores.

Limite: Leitura do resumo e metadados; código não auditado e resultados não reproduzidos.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

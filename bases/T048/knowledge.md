# T048 — Memory Management

**Nome canônico:** Memory Management  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T048  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gestão de memória

## T048:C01 — conceito

Conjunto de políticas para escrever, organizar, recuperar, corrigir, promover, compactar e remover informação de memória. Controla o ciclo de vida e a qualidade do acervo. Não é apenas escolher um banco de dados ou aumentar a quantidade armazenada.

Como funciona:
- Aplicar critérios de admissão e metadados na escrita.
- Escolher o que recuperar e em qual nível de detalhe.
- Reconciliar mudanças, expiração e uso do espaço disponível.

## T048:C02 — aplicacao

Quando usar:
- Agentes persistentes com fontes mutáveis.
- Múltiplas missões compartilham fatos e procedimentos.

Quando não usar:
- Não automatizar promoção de hipótese para fato somente com base na confiança textual do modelo.

Implementação proposta:
- Proposta: definir políticas separadas para eventos, fatos e skills.
- Registrar decisões de promoção, invalidação e remoção.
- Manter mecanismos de reconstrução e indicadores de memórias conflitantes ou sem fonte.

Aplicação LAI proposta:
Proposta LAI: centralizar regras de memória sob a orquestração da Helena, com autorização por domínio e testes de recuperação antes de declarar autoaprendizagem.

## T048:C03 — riscos_validacao

Armadilhas:
- Políticas de retenção podem apagar dados necessários para auditar decisões.
- Memória excessiva e mal indexada pode piorar seleção e custo.

Métricas sugeridas:
- Precisão da recuperação e taxa de obsolescência.
- Crescimento, latência e número de conflitos não resolvidos.

Testes propostos:
- Ingerir duplicatas e confirmar consolidação sem perder fontes.
- Revogar um fato e verificar propagação aos resumos e procedimentos dependentes.

## T048:C04 — perguntas_proveniencia

Pergunta: Gerenciar memória exige uma LLM?
Resposta: Não em todas as etapas. Integridade, versões, acesso e expiração podem ser determinísticos.

Pergunta: Qual é o melhor sinal de memória útil?
Resposta: Melhoria comprovada na execução de novas tarefas, com origem e validade das informações utilizadas.

Pergunta: É preciso apagar uma memória para esquecer seu uso?
Resposta: Não. Pode removê-la da seleção ativa, reduzir prioridade ou arquivar o índice, preservando o registro quando necessário.

Pergunta: Qual custo precisa entrar na decisão?
Resposta: Escrita, manutenção, indexação, recuperação, releitura e correção. Otimizar somente tokens da próxima resposta pode aumentar o custo total.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T048:C05 — mecanismo_avancado

Gerenciar memória envolve decisões acopladas: admitir tudo aumenta custo de recuperação, enquanto consolidar cedo pode apagar contexto antes que seu valor seja conhecido. Políticas devem distinguir validade factual, prioridade de leitura e retenção física. Uma memória pouco acessada pode continuar verdadeira e obrigatória; outra muito frequente pode estar obsoleta. Confundir essas dimensões transforma estatísticas de uso em decisões incorretas sobre conhecimento.

Condição de contorno:
Uma política uniforme costuma falhar quando o mesmo store contém preferências, evidência histórica, resultados transitórios e procedimentos com ciclos de atualização diferentes.

Contrato proposto:
- Entradas: Eventos de criação, acesso, correção e pressão de capacidade, com classe da memória.
- Saídas: Decisões de admissão, reorganização, revisão ou descarte, cada uma com motivo rastreável.
- Estado: Políticas versionadas, dependências entre derivados e fontes e fila de manutenção pendente.
- Invariante: Reduzir prioridade de recuperação não equivale a invalidar a afirmação nem autoriza apagar sua única evidência.

Compromissos de projeto:
- Automatizar organização reduz manutenção manual e introduz erros que podem se propagar entre notas.
- Políticas por classe preservam semântica de retenção e aumentam o número de contratos a operar.

## T048:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: marcar como raramente acessada uma regra ainda vigente e como popular uma regra revogada. A manutenção deve conservar a primeira e impedir que frequência restaure a validade da segunda.

Plano de avaliação proposto:
Avaliação proposta: comparar política fixa, recência e política por classes em uma sequência com mudanças. Medir qualidade posterior, custo de manutenção, atrasos de correção e perdas irreversíveis; contar consultas extras geradas por memória descartada cedo.

Comparações:
- T074 (complements): Eviction é uma operação de capacidade dentro de um ciclo de vida mais amplo.
- T058 (complements): Consolidação reorganiza conteúdo; a gestão decide quando e sob quais invariantes executar essa transformação.

Afirmação rastreável:
MemoryBank usa atualização inspirada em esquecimento e reforço; A-MEM permite que novas notas alterem representações de memórias anteriores.
Suporte: direct; fontes: V3A-S036, V3A-S034
Limite: São políticas de pesquisa distintas, sem prova de que uma imitação do esquecimento humano seja ótima para memória operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T048:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu ciclo de vida. Aqui gestão de memória usa orçamentos separados por tipo e mede custo de qualidade do acervo.

Projeto e decomposição
Separe orçamento de evidências, fatos, episódios e procedimentos. Remover detalhe episódico antigo pode ser aceitável; remover evidência de uma regra ativa pode quebrar auditabilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

Controle adaptativo
Crie fila de manutenção com prioridade por impacto: memória sem fonte, conflito ativo, índice atrasado e candidato redundante exigem tratamentos distintos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

Validação contrafactual
Compare políticas sob crescimento contínuo do acervo. Meça utilidade por consulta, registros inválidos recuperados e tempo de manutenção; custo de indexação e reparo entra junto com armazenamento. Unidade de avaliação: coleção de memórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

USO AVANÇADO — Assistente de múltiplos projetos
Cenário: Memórias competem por espaço.
Estratégia: Aplicar quotas por projeto e tipo, mantendo referências a evidências de decisões ativas. Evitar que projeto muito acessado elimine histórico necessário de outro.
Papel do modelo pequeno: 3–7B classifica tipo; regras aplicam quotas.
Aceite proposto: Nenhuma remoção pode quebrar decisão ainda ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

USO AVANÇADO — Acervo com correções frequentes
Cenário: Índices e resumos ficam atrasados.
Estratégia: Priorizar reparo de objetos usados em tarefas pendentes e suspender promoção quando manutenção estiver atrasada demais.
Papel do modelo pequeno: 8–14B identifica dependências afetadas.
Aceite proposto: Consulta sensível deve detectar projeção desatualizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S032, V4A-S010, V4A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo, duplicação e estado de manutenção.
8–14B: Revisor de conflitos e propostas de consolidação locais.
15–30B: Planejador de manutenção entre coleções com dependências complexas.
Requisitos de treino/runtime: Inventário por tipo, métricas de consulta e dependências; ações irreversíveis exigem política explícita do sistema.
Não aplicar quando: A mesma operação mistura relevância, retenção e exclusão sem estados separados.

## T048:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C009 — Meta / CacheLib em serviços Facebook
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Artigo de operadores relata adoção desde 2017 por múltiplos serviços.
Mecanismo documentado: Engine comum para desenvolvimento e operação de caches de dados e armazenamento.
Correspondência com esta base: Ciclo de vida físico inspira gestão, sem avaliar utilidade semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar política determinística de residência e estimativa de utilidade proposta pelo modelo.
Limite: Não afirma cache semântico, resumo, verdade da memória ou taxa de acerto de LLM. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q013, V4A-Q023.

## T048:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T048 → T058 [feeds]
Como combinar: Encaminhar redundâncias para consolidação verificável.
Interface: Conjunto candidato, dependências e escopo.
Condição: Consolidação preservar evidência e divergência.
Aceite proposto: Comparar respostas antes e depois da manutenção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S032, V4A-S010, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T048 → T074 [complements]
Como combinar: Gerenciar residência sem apagar memória canônica.
Interface: Objeto, custo de recarga e estado de retenção.
Condição: Evicção e exclusão terem operações distintas.
Aceite proposto: Remover da janela e recuperar da origem durável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S032, V4A-S010, V4A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar tamanho do acervo como indicador de aprendizado.
- Não deixar manutenção apagar a única origem de uma conclusão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade da memória sob crescimento e correção; armazenamento maior não garante respostas melhores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T058, T071, T074, T075

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S036 — MemoryBank: Enhancing Large Language Models with Long-Term Memory

[https://arxiv.org/abs/2305.10250](https://arxiv.org/abs/2305.10250)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória recuperável e política de atualização inspirada em esquecimento e reforço por tempo e significância.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S034 — A-MEM: Agentic Memory for LLM Agents

[https://arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Notas estruturadas, conexão entre memórias e evolução das representações de notas anteriores.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S017 — Memory in ChatGPT

[https://help.openai.com/en/articles/8590148-memory-in-chatgpt](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias salvas e histórico como fontes distintas de personalização e controles.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

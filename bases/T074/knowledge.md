# T074 — Memory Eviction

**Nome canônico:** Memory Eviction  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T074  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** expulsão de memória; descarregamento de memória

## T074:C01 — conceito

Remove informação de uma camada de memória quando ela excede orçamento ou deixa de ser útil. É essencial declarar se a remoção ocorre só do contexto ativo, de um cache ou do armazenamento durável. Essas operações têm consequências muito diferentes.

Como funciona:
- Definir camada, limite e unidades elegíveis.
- Escolher itens por recência, uso, validade ou prioridade.
- Preservar referências ou realizar descarte conforme a política aplicável.

## T074:C02 — aplicacao

Quando usar:
- Contexto ativo e caches com capacidade limitada.
- Acervos com material redundante ou vencido.

Quando não usar:
- Não apagar a única evidência de uma decisão sem considerar retenção e dependências.

Implementação proposta:
- Proposta: fixar objetivos e restrições vigentes contra expulsão automática.
- Distinguir arquivamento, invalidação e exclusão definitiva.
- Registrar o motivo e verificar se objetos expulsos ainda são referenciados por memórias ativas.

Aplicação LAI proposta:
Proposta LAI: começar por expulsar detalhes do contexto ativo para arquivo; exclusão durável exige política própria, não apenas escore de relevância.

## T074:C03 — riscos_validacao

Armadilhas:
- Um item pouco usado pode tornar-se crítico em uma tarefa rara.
- Remover memória repetidamente recuperada causa thrashing e aumenta latência.

Métricas sugeridas:
- Taxa de recarregamento após expulsão.
- Falhas por informação removida e uso do orçamento.

Testes propostos:
- Expulsar um detalhe do contexto e recuperá-lo por referência quando necessário.
- Tentar apagar evidência ainda usada por uma decisão e exigir tratamento de dependência.

## T074:C04 — perguntas_proveniencia

Pergunta: Eviction significa esquecimento permanente?
Resposta: Depende da camada. Em contexto ou cache pode significar apenas descarregar algo recuperável.

Pergunta: É igual a KV Cache Eviction?
Resposta: Não. KV cache contém estados de inferência; memória de agente pode conter fatos, arquivos e episódios.

Pergunta: Noeviction elimina risco de perda?
Resposta: Evita expulsão automática por essa política, mas novas escritas podem falhar. O aplicativo precisa detectar e tratar a falha, além de garantir persistência.

Pergunta: Devo conservar tudo que é caro de reconstruir?
Resposta: É um critério forte, mas deve ser combinado com validade, uso esperado e retenção. A decisão não pode depender só de frequência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T074:C05 — mecanismo_avancado

Eviction por pressão de capacidade e expiração por tempo são mecanismos diferentes. No Redis, LRU e LFU usam aproximações; a frequência pode decair para acompanhar mudanças de acesso. Esses critérios preveem reutilização, não importância factual. Se uma camada contém a única cópia de uma memória necessária, tratá-la como cache converte uma otimização de desempenho em perda de conhecimento.

Condição de contorno:
A política falha quando assume que todo objeto removido pode ser reconstruído, mas fontes, operações ou artefatos originais já não estão disponíveis.

Contrato proposto:
- Entradas: Ocupação, acessos, classe da memória, custo de reconstrução e referências ainda ativas.
- Saídas: Objetos elegíveis removidos da camada e registro de destino ou possibilidade de reconstrução.
- Estado: Contadores, prioridade, TTL quando aplicável e vínculos com a cópia autoritativa.
- Invariante: Eviction de cache não apaga a única evidência de um fato sem uma política de retenção separada.

Compromissos de projeto:
- LRU acompanha recência e pode expulsar itens raros caros de recuperar.
- LFU preserva itens frequentes e precisa adaptar-se quando o padrão muda; ambas exigem avaliar misses e custo de reconstrução.

## T074:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar duas coleções maiores que a capacidade e manter uma evidência crítica pouco acessada. A política deve expor thrashing e impedir que a evidência autoritativa seja tratada como cópia descartável.

Plano de avaliação proposto:
Avaliação proposta: comparar LRU, LFU e política por classe com a mesma capacidade. Medir hit rate, latência de misses, custo de recomputação e perdas irrecuperáveis; separar expulsões por capacidade de expiração e invalidação.

Comparações:
- T031 (distinct_from): Invalidação remove elegibilidade por mudança de estado; eviction libera capacidade mesmo para conteúdo ainda válido.
- T048 (complements): Gestão de memória decide quais classes podem ser descartadas e sob quais condições.

Afirmação rastreável:
Redis documenta LRU aproximado, LFU com contadores probabilísticos e política noeviction que pode rejeitar novas escritas.
Suporte: direct; fontes: V3A-S039
Limite: Essas políticas controlam recursos do store; não definem a relevância ou verdade das memórias de um agente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T074:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu expiração e capacidade. Aqui evicção usa custo de reconstituição e dependências ativas para reduzir trabalho repetido.

Projeto e decomposição
Calcule custo de recarga, reconstrução e verificação. Dois blocos do mesmo tamanho podem ter custos muito diferentes se um vem de arquivo local e outro de investigação longa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

Controle adaptativo
Evite evictar fragmentos de um conjunto necessário em breve. A unidade de substituição pode ser grupo de dependências, desde que a reserva não torne toda memória permanentemente fixa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

Validação contrafactual
Compare LRU, LFU e política por custo de reconstrução. Meça latência total, trabalho repetido e falhas de disponibilidade após evicção; hit rate isolado pode favorecer objetos baratos. Unidade de avaliação: decisão de evicção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

USO AVANÇADO — Agente local com pouca memória
Cenário: Contexto alterna entre módulos.
Estratégia: Manter contratos caros de reconstruir e remover logs reabríveis; liberar grupo quando a fase encerrar.
Papel do modelo pequeno: 3–7B classifica recuperabilidade.
Aceite proposto: Nenhum bloco removido pode ser a única cópia de uma decisão ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

USO AVANÇADO — Cache de artefatos derivados
Cenário: Resumos grandes competem com extrações pequenas.
Estratégia: Priorizar valor por custo evitado e demanda prevista, usando tamanho e tempo de reconstrução medidos.
Papel do modelo pequeno: 8–14B sugere categorias; código aplica política.
Aceite proposto: Reduzir custo de recarga sem aumentar respostas obsoletas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S039, V4A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e disponibilidade de origem.
8–14B: Avaliador de dependências de curto prazo por fase.
15–30B: Planejador de reorganização quando conjunto ativo exceder capacidade.
Requisitos de treino/runtime: Medição de custo, referência à cópia canônica e condição de liberação de conteúdo fixado.
Não aplicar quando: Evicção é usada para apagar histórico ou a origem não pode ser recuperada confiavelmente.

## T074:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C009 — Meta / CacheLib em serviços Facebook
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Artigo de operadores relata adoção desde 2017 por múltiplos serviços.
Mecanismo documentado: Engine comum para desenvolvimento e operação de caches de dados e armazenamento.
Correspondência com esta base: Gerência de cache é família relacionada à evicção de memória externa.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar política determinística de residência e estimativa de utilidade proposta pelo modelo.
Limite: Não afirma cache semântico, resumo, verdade da memória ou taxa de acerto de LLM. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q007.

## T074:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T074 → T039 [requires]
Como combinar: Receber prioridade e custo de reconstrução.
Interface: Objeto, valor, dependências e condição de fixação.
Condição: Estimativas atualizadas pela fase atual.
Aceite proposto: Comparar recargas após mudança de objetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S039, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T074 → T063 [complements]
Como combinar: Acionar recarga identificada quando bloco voltar a ser necessário.
Interface: Referência, revisão e status de residência.
Condição: Evicção não invalidar identidade do conteúdo.
Aceite proposto: Evictar e recarregar verificando mesmos bytes e escopo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S039, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apagar metadados de versão necessários à reconciliação.
- Não tratar conteúdo pouco acessado como dispensável sem verificar obrigações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo útil e continuidade sob memória limitada; evicção sofisticada pode ser pior que LRU em carga simples.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T048, T062, T105

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

### V3A-S039 — Redis Key eviction

[https://redis.io/docs/latest/develop/reference/eviction/](https://redis.io/docs/latest/develop/reference/eviction/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Políticas de eviction, noeviction, LRU aproximado, LFU probabilístico e distinção entre expiração e pressão de capacidade.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T056 — Bitemporal Memory

**Nome canônico:** Bitemporal Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T056  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória bitemporal; valid time e system time

## T056:C01 — conceito

Registra dois eixos: quando um fato vale no domínio e quando o sistema o conheceu ou registrou. Permite responder tanto o que hoje sabemos sobre o passado quanto o que acreditávamos naquele momento. Bitemporalidade é independente do número de camadas de memória.

Como funciona:
- Armazenar intervalo de validade e intervalo de registro.
- Inserir correções sem apagar a história de conhecimento.
- Consultar com os dois tempos declarados.

## T056:C02 — aplicacao

Quando usar:
- Dados atrasados, correções retroativas e auditoria.
- Avaliação histórica que não pode usar informação conhecida somente depois.

Quando não usar:
- Não confundir data de ingestão com data em que o fato passou a valer.

Implementação proposta:
- Proposta: usar intervalos consistentes, preferencialmente semiabertos, e timezone explícito.
- Distinguir tempo do evento, validade de negócio e registro quando não coincidem.
- Na recuperação, aplicar filtros temporais antes de apresentar os fatos à LLM.

Aplicação LAI proposta:
Proposta LAI: avaliar decisões antigas da Helena usando somente dados disponíveis na data da decisão; manter correções posteriores em uma visão distinta.

## T056:C03 — riscos_validacao

Armadilhas:
- Misturar os eixos introduz vazamento de futuro em backtests.
- Correções podem criar sobreposições de validade sem resolução clara.

Métricas sugeridas:
- Correção de consultas as-of nos dois eixos.
- Quantidade de conflitos de intervalo e registros sem tempo confiável.

Testes propostos:
- Registrar hoje um fato válido desde ontem e comparar duas consultas históricas.
- Executar replay com corte de conhecimento e impedir uso da correção futura.

## T056:C04 — perguntas_proveniencia

Pergunta: Dois timestamps tornam qualquer memória bitemporal?
Resposta: Não. Os tempos precisam representar e suportar consultas de validade e conhecimento, com semântica definida.

Pergunta: Bitemporal significa cinco camadas?
Resposta: Não. Camadas organizam tipos de memória; bitemporalidade descreve eixos temporais dos registros.

Pergunta: Tempo do evento é sempre valid-time?
Resposta: Não. O evento pode informar uma alteração que só valerá depois, ou corrigir uma validade passada. A semântica vem do domínio.

Pergunta: Qual perspectiva usar para auditoria de uma decisão?
Resposta: A informação conhecida na hora da decisão, com validade adequada à pergunta. Uma análise retrospectiva corrigida responde a outra questão e deve ser identificada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T056:C05 — mecanismo_avancado

Consultar memória bitemporal exige fixar a perspectiva de conhecimento e a validade de domínio em todas as relações usadas. Uma consulta pode filtrar corretamente o fato principal e ainda juntar uma entidade pela versão atual, introduzindo informação futura. A base de leitura também precisa ser consistente entre consultas sucessivas: “agora” e “último estado processado” podem mudar enquanto um relatório está sendo montado.

Condição de contorno:
Dois timestamps numa linha não bastam se as operações não preservam intervalos históricos ou se consultas e joins ignoram um dos eixos temporais.

Contrato proposto:
- Entradas: Instante de conhecimento, instante ou intervalo de validade e entidades a consultar.
- Saídas: Fatos e relações válidos sob a mesma perspectiva, com limites temporais explícitos.
- Estado: Revisões bitemporais, base de leitura e política para correções recebidas tardiamente.
- Invariante: Nenhuma evidência posterior ao limite de conhecimento entra silenciosamente numa reconstrução histórica.

Compromissos de projeto:
- Dois eixos permitem auditoria e correção retroativa, aumentando armazenamento e complexidade das consultas.
- Fixar uma base de leitura melhora consistência e pode apresentar um estado ligeiramente anterior às atualizações em curso.

## T056:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir hoje um fato válido no mês passado e mudar também sua entidade associada. A consulta “como sabíamos antes” deve usar versões antigas em ambos os lados da relação.

Plano de avaliação proposto:
Avaliação proposta: comparar consulta atual, por validade e bitemporal em dados com chegada tardia. Medir correção das junções, intervalos sobrepostos indevidos e vazamento temporal; repetir relatórios com base fixa durante atualizações concorrentes.

Comparações:
- T009 (complements): RAG temporal precisa recuperar fatos segundo a perspectiva temporal correta antes de gerar texto.
- T077 (complements): Relações de um grafo podem carregar os dois eixos para reconstrução histórica consistente.

Afirmação rastreável:
XTDB distingue filtros de valid-time e system-time e uma base de consulta composta por snapshot e clock time.
Suporte: direct; fontes: A-S032, V3A-S042
Limite: Os nomes e recursos pertencem ao XTDB consultado; outra implementação precisa definir seus próprios contratos equivalentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T056:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 cuidou de joins temporais. Aqui bitemporalidade suporta auditoria de decisões e comparação justa de políticas sob informação disponível.

Projeto e decomposição
Defina consulta de auditoria com dois instantes: quando o fato valeu e o que o sistema sabia ao decidir. Misturar essas perspectivas pode punir uma decisão por informação que chegou depois.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

Controle adaptativo
Correções retroativas devem gerar nova versão de conhecimento e permitir recalcular projeções sem apagar a resposta histórica. O resultado recalculado precisa ser rotulado como reavaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

Validação contrafactual
Compare política original e nova usando o mesmo corte de conhecimento. Meça diferenças atribuíveis à política versus dados tardios; testar fatos com validade futura declarada e observação atrasada. Unidade de avaliação: decisão histórica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

USO AVANÇADO — Explicação de decisão
Cenário: Usuário pergunta por que recomendação mudou.
Estratégia: Recuperar evidências conhecidas em cada data, mostrar qual correção alterou o entendimento e separar erro anterior de informação nova.
Papel do modelo pequeno: 8–14B explica duas perspectivas.
Aceite proposto: Cada justificativa deve usar somente fatos disponíveis naquele corte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

USO AVANÇADO — Avaliação de memória
Cenário: Nova política de consolidação parece melhor.
Estratégia: Reprocessar histórico com cortes consistentes, sem entregar ao modelo correções futuras; comparar erros evitados e antecipações indevidas.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra auditoria.
Aceite proposto: Não contabilizar vantagem causada por vazamento temporal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S032, V3A-S042.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de datas com rótulos de validade e registro separados.
8–14B: Leitor de consultas temporais já executadas por banco.
15–30B: Explicador de mudanças de decisão entre perspectivas históricas.
Requisitos de treino/runtime: Banco ou camada que preserve ambos os tempos, política de intervalos e identificação de correções.
Não aplicar quando: Datas são inferidas sem fonte ou aplicação só armazena último valor e tenta reconstruir passado por suposição.

## T056:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q025.

## T056:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T056 → T077 [complements]
Como combinar: Aplicar cortes temporais às relações do grafo.
Interface: Aresta, valid_time, recorded_time e perspectiva.
Condição: Todos os elos respeitarem corte comum.
Aceite proposto: Consultar caminho com elo conhecido apenas posteriormente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S032, V3A-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T056 → T059 [feeds]
Como combinar: Registrar correção como evento interpretável.
Interface: Evento, tempos, origem e versão do esquema.
Condição: Replay preservar distinção dos dois tempos.
Aceite proposto: Reproduzir decisão histórica sem incorporar correção futura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S032, V3A-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar timestamp de ingestão como data do fato.
- Não apresentar reavaliação atual como resposta que existia no passado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência temporal das justificativas; nenhum porte de modelo corrige retrospectivamente um histórico inexistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T054, T072, T077

## Fontes primárias associadas

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S042 — XTDB SQL Queries

[https://docs.xtdb.com/reference/main/sql/queries.html](https://docs.xtdb.com/reference/main/sql/queries.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Filtros temporais por tabela e basis de leitura; snapshot e clock time como dimensões do contexto de consulta.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

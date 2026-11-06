# T077 — Temporal Knowledge Graphs

**Nome canônico:** Temporal Knowledge Graphs  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T077  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** grafos de conhecimento temporais

## T077:C01 — conceito

Grafos em que entidades ou relações têm validade temporal e, quando necessário, histórico de registro. Permitem perguntar quais relações valiam em determinado momento e como mudaram. Um timestamp de criação isolado não fornece toda essa semântica.

Como funciona:
- Modelar entidades e relações com intervalos e proveniência.
- Registrar mudanças sem confundir correção com evento novo.
- Aplicar filtros temporais durante busca e travessia.

## T077:C02 — aplicacao

Quando usar:
- Dependências e fatos que mudam com versões ou períodos.
- Auditoria de relações históricas entre sistemas e decisões.

Quando não usar:
- Não misturar relações de épocas diferentes em um caminho apresentado como simultaneamente válido.

Implementação proposta:
- Proposta: definir se cada consulta usa tempo de validade, de conhecimento ou ambos.
- Exigir interseção temporal coerente ao compor caminhos.
- Manter evidências e estado de verificação nas arestas, não somente data.

Aplicação LAI proposta:
Proposta LAI: representar qual software consumia qual schema em cada versão; verificar intervalos antes de recomendar compatibilidade.

## T077:C03 — riscos_validacao

Armadilhas:
- Relações antigas podem aparecer em respostas atuais por falta de filtro.
- Expansões do grafo podem combinar versões incompatíveis.

Métricas sugeridas:
- Precisão de consultas históricas e atuais.
- Arestas sem validade e caminhos temporalmente inconsistentes.

Testes propostos:
- Criar uma dependência substituída e consultar antes e depois da mudança.
- Registrar correção tardia e comparar o que era conhecido em duas datas.

## T077:C04 — perguntas_proveniencia

Pergunta: Temporal graph é sempre bitemporal?
Resposta: Não. Pode registrar um único eixo. Bitemporalidade exige distinguir validade e conhecimento ou registro.

Pergunta: Preciso usar um produto específico?
Resposta: Não. Graphiti é uma referência de implementação, mas a modelagem temporal pode existir em outras tecnologias.

Pergunta: Um timestamp de criação resolve validade?
Resposta: Não. Ele indica registro ou criação do objeto. O fato pode ter começado antes, valer depois ou não ter ocorrência confirmada.

Pergunta: Um caminho temporal é causal?
Resposta: Não. Compatibilidade de tempos permite compor relações segundo a consulta; causalidade ainda exige hipóteses e evidências adicionais de identificação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T077:C05 — mecanismo_avancado

A semântica de um caminho temporal depende da pergunta. Para relações simultâneas, os intervalos das arestas precisam ter interseção: com intervalos semiabertos, o maior início deve ser menor que o menor fim. Para uma trajetória ao longo do tempo, pode ser necessário apenas respeitar a ordem dos eventos. Além disso, promessa atual sobre evento futuro não equivale a ocorrência futura já confirmada.

Condição de contorno:
Aplicar a mesma regra temporal a toda consulta pode excluir trajetórias válidas ou produzir relações simultâneas que nunca coexistiram.

Contrato proposto:
- Entradas: Entidades, arestas com validade e origem, perspectiva de conhecimento e tipo de consulta temporal.
- Saídas: Caminhos ou relações com intervalos compatíveis e evidências que distinguem planos de fatos ocorridos.
- Estado: Histórico de invalidação, referência temporal dos episódios e regras de interpretação dos campos.
- Invariante: O sistema não transforma intenção, prazo ou promessa em evidência de que o evento descrito aconteceu.

Compromissos de projeto:
- Arestas temporais permitem reconstrução precisa e aumentam complexidade de filtros e junções.
- Preservar relações invalidadas facilita auditoria e exige que consultas atuais excluam as versões inadequadas.

## T077:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar uma promessa hoje para uma entrega futura e depois registrar cancelamento. A consulta sobre compromissos deve reconhecer a promessa; a consulta sobre entregas realizadas não pode contar essa ocorrência.

Plano de avaliação proposto:
Avaliação proposta: comparar consultas de snapshot e trajetórias ordenadas em dados com intervalos não sobrepostos. Medir coerência temporal, atualização após cancelamento e recuperação de proveniência; incluir fatos descobertos tardiamente para testar o eixo de conhecimento.

Comparações:
- T056 (complements): Bitemporalidade acrescenta a perspectiva do que era conhecido às relações válidas no domínio.
- T051 (specializes): O grafo temporal especializa a representação relacional com regras explícitas de validade e evolução.

Afirmação rastreável:
EntityEdge no Graphiti diferencia valid_at, invalid_at, expired_at e reference_time e documenta tratamento específico para planos futuros.
Suporte: direct; fontes: V3A-S043
Limite: Os nomes e interpretações são da revisão consultada; não constituem padrão universal para todo grafo temporal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T077:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu intervalos e jornadas temporais. Aqui grafos temporais modelam incerteza de datas e respostas condicionadas à resolução disponível.

Projeto e decomposição
Represente datas aproximadas como intervalos ou limites, sem inventar dia exato. Relação que vale em algum ponto do mês não prova simultaneidade com outra relação de data desconhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

Controle adaptativo
Separe tempo do evento, validade da relação e momento de conhecimento. Caminhos precisam declarar se buscam coexistência, sequência possível ou sequência comprovada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

Validação contrafactual
Compare datas pontuais imputadas e intervalos explícitos. Meça relações temporais falsas, respostas inconclusivas corretas e vazamento de conhecimento futuro; ordem temporal não implica causalidade. Unidade de avaliação: caminho temporal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

USO AVANÇADO — Histórico de responsabilidades
Cenário: Documentos informam mudanças com datas incompletas.
Estratégia: Construir relações com intervalos sustentados e responder quem podia ser responsável, distinguindo certeza de possibilidade.
Papel do modelo pequeno: 3–7B extrai datas; banco calcula.
Aceite proposto: Não afirmar responsável único quando intervalos permitem alternativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

USO AVANÇADO — Rastreio de dependências
Cenário: É preciso explicar cadeia de mudanças.
Estratégia: Consultar sequência de eventos com ordenação confirmada e marcar trechos cuja ordem não é decidível.
Papel do modelo pequeno: 8–14B explica caminho.
Aceite proposto: Cada salto temporal deve respeitar relações de ordem observadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S035, V3A-S043, A-S032.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de expressões temporais com indicação de precisão.
8–14B: Leitor de caminhos já filtrados por lógica temporal.
15–30B: Analista de alternativas quando intervalos e perspectivas produzem múltiplas histórias possíveis.
Requisitos de treino/runtime: Álgebra temporal, campos de precisão e identidade de relações; LLM não deve decidir sozinho interseções de intervalos.
Não aplicar quando: A aplicação exige cronologia exata a partir de fontes que só fornecem datas aproximadas.

## T077:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Tempo lógico orienta processamento; não é grafo temporal de conhecimento.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q015, V4A-Q025.

## T077:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T077 → T056 [requires]
Como combinar: Aplicar perspectiva de conhecimento ao grafo.
Interface: Validade, registro e instante da pergunta.
Condição: Consulta declarar os dois tempos.
Aceite proposto: Adicionar descoberta posterior e impedir alteração da história conhecida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S035, V3A-S043, A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T077 → T057 [conflicts]
Como combinar: Evitar converter sequência em causa.
Interface: Caminho temporal e hipótese causal separada.
Condição: Causalidade exigir identificação adicional.
Aceite proposto: Apresentar eventos ordenados sem mecanismo e exigir ressalva causal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S035, V3A-S043, A-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não preencher data desconhecida com data de ingestão.
- Não confundir plano futuro com evento ocorrido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar raciocínio temporal sobre intervalos; modelos maiores também podem inventar precisão se schema não preservar incerteza.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T029, T051, T056, T072

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

### V3A-S043 — Graphiti EntityEdge implementation

[https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py](https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campos valid_at, invalid_at, expired_at, reference_time, episódios e contrato temporal das relações; código lido, não executado.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V3A-S035 — Zep: A Temporal Knowledge Graph Architecture for Agent Memory

[https://arxiv.org/abs/2501.13956](https://arxiv.org/abs/2501.13956)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura temporal Graphiti para integração de conversas e dados estruturados com relações históricas.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

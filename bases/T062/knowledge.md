# T062 — Hierarchical Memory

**Nome canônico:** Hierarchical Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T062  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória hierárquica

## T062:C01 — conceito

Organiza memória em níveis com diferentes papéis, custos e graus de detalhe: contexto ativo, estado, episódios, fatos, procedimentos e arquivos originais. Essa organização é uma decisão arquitetural; não existe obrigação universal de ter cinco ou seis níveis.

Como funciona:
- Definir responsabilidade e critérios de admissão de cada nível.
- Mover ou recuperar informação conforme necessidade da tarefa.
- Preservar ligações entre sínteses e fontes originais.

## T062:C02 — aplicacao

Quando usar:
- Agentes que precisam operar por longos períodos com contexto limitado.
- Acervos que combinam fatos, experiências e procedimentos.

Quando não usar:
- Não confundir múltiplas pastas com uma hierarquia funcional sem política de acesso e atualização.

Implementação proposta:
- Proposta: separar contexto ativo de armazenamento durável.
- Declarar quais dados são autoritativos e quais são projeções.
- Avaliar promoção, invalidação e recuperação em todos os níveis, sem depender somente de resumos.

Aplicação LAI proposta:
Proposta LAI: combinar estado da missão, episódios, conhecimento e skills com fontes originais; escolher o número de camadas por necessidade, não por rótulo.

## T062:C03 — riscos_validacao

Armadilhas:
- Uma correção na fonte pode não alcançar o resumo ativo.
- Muitos níveis aumentam complexidade e latência de recuperação.

Métricas sugeridas:
- Tempo e precisão para chegar à evidência original.
- Consistência entre níveis após mudanças.

Testes propostos:
- Corrigir um fato e verificar propagação às memórias derivadas.
- Recuperar uma informação antiga sem carregar o acervo inteiro.

## T062:C04 — perguntas_proveniencia

Pergunta: Hierarquia é sempre do recente para o antigo?
Resposta: Não. Pode refletir função, abstração, persistência ou custo de acesso.

Pergunta: Ela amplia fisicamente a janela da LLM?
Resposta: Não. Gerencia o que entra na janela e mantém o restante recuperável fora dela.

Pergunta: Toda camada precisa de uma cópia do fato?
Resposta: Não. Pode conter apenas índice ou referência. Cópias e resumos criam obrigações adicionais de atualização e controle de versão.

Pergunta: Como decidir onde manter um item?
Resposta: Considere custo de acesso, frequência, criticidade e capacidade de reconstrução. Frequência alta não autoriza ignorar validade ou proveniência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T062:C05 — mecanismo_avancado

Há duas hierarquias diferentes: níveis de armazenamento com latência distinta e níveis de abstração com detalhe distinto. Um resumo pode estar no armazenamento lento, e um trecho original pode permanecer ativo; misturar essas dimensões dificulta políticas de atualização. Para cada passagem entre níveis, declare se ocorre cópia, seleção ou transformação, e qual versão continua sendo a referência quando as representações divergem.

Condição de contorno:
Adicionar camadas pode piorar o sistema quando buscas atravessam muitos níveis, os índices não representam exceções ou a atualização de derivados fica atrasada.

Contrato proposto:
- Entradas: Memórias classificadas por função, custo de acesso, detalhe e origem autoritativa.
- Saídas: Representações distribuídas em níveis com vínculos explícitos e caminhos de recuperação.
- Estado: Políticas de promoção, invalidação, retenção e posição de atualização de cada projeção.
- Invariante: Uma correção na origem torna detectável a obsolescência de qualquer derivado que ainda não foi reconstruído.

Compromissos de projeto:
- Hierarquias reduzem leitura recorrente e acrescentam decisões de roteamento que podem falhar.
- Mais níveis favorecem especialização e ampliam custo de coerência, observabilidade e recuperação de falhas.

## T062:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir uma exceção no registro original enquanto um resumo superior continua ativo. A consulta deve detectar a revisão pendente ou reabrir a origem, sem usar o resumo antigo como vigente.

Plano de avaliação proposto:
Avaliação proposta: comparar store único e hierarquia com carga de leituras e correções controlada. Medir latência por nível, fontes abertas, atraso de invalidação e respostas obsoletas; incluir tarefas que precisam de detalhe ausente no índice superior.

Comparações:
- T008 (complements): Resumos hierárquicos organizam abstração; memória hierárquica também pode organizar custo e persistência.
- T063 (complements): Gerência virtual de contexto é uma aplicação de níveis de memória orientada à janela ativa limitada.

Afirmação rastreável:
MemGPT organiza níveis de memória para mover informação entre armazenamento externo e contexto limitado.
Suporte: related; fontes: A-S009
Limite: A fonte sustenta essa arquitetura específica; não exige número fixo de camadas nem valida todas as taxonomias de memória.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T062:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou armazenamento e abstração. Aqui hierarquia é otimizada por custo de movimento e localidade de tarefa.

Projeto e decomposição
Meça quanto custa mover e interpretar cada unidade entre arquivo, índice e janela. Um resumo curto pode ser barato de carregar e caro de desambiguar; latência física não é custo total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

Controle adaptativo
Promova residência temporária por fase da tarefa, não por popularidade global. Múltiplas tarefas concorrentes podem ter conjuntos de trabalho distintos e competir por níveis rápidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

Validação contrafactual
Compare política estática, por recência e por fase. Meça recargas, latência de leitura e decisões erradas por usar abstração inadequada; separar nível físico do nível semântico na telemetria. Unidade de avaliação: trajetória de acessos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

USO AVANÇADO — Projeto com módulos ativos
Cenário: Somente parte do repositório muda.
Estratégia: Manter contratos dos módulos ativos na janela, descritores no nível intermediário e originais externos; rebaixar após encerrar fase.
Papel do modelo pequeno: 3–7B usa contratos; 8–14B abre detalhe.
Aceite proposto: Mudança de módulo deve carregar versão correta antes de agir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

USO AVANÇADO — Pesquisa em acervo extenso
Cenário: Consulta alterna visão geral e detalhe.
Estratégia: Usar síntese para navegação e originais para afirmações precisas; contabilizar custo de expandir cada nível.
Papel do modelo pequeno: 15–30B integra níveis.
Aceite proposto: Detalhe factual deve continuar verificável no original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V3A-S039.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de nível intermediário explícito com referências simples.
8–14B: Controlador de expansão entre poucos níveis por necessidade.
15–30B: Integrador global que decide quais detalhes precisam subir à janela.
Requisitos de treino/runtime: Catálogo de níveis, custo de recarga e dependências; não pressupor equivalência entre RAM, contexto e resumo.
Não aplicar quando: Custo de movimentar níveis excede benefício ou a abstração perde informação indispensável sem recuperação.

## T062:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Hierarquia de KV é analogia de camadas de memória, não memória semântica do agente.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T062:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T062 → T074 [complements]
Como combinar: Escolher residência por fase e custo de retorno.
Interface: Objeto, nível, custo e condição de fixação.
Condição: Evicção não alterar retenção canônica.
Aceite proposto: Medir oscilações entre os mesmos dois níveis.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T062 → T008 [complements]
Como combinar: Criar abstrações para navegação, separadas da localização física.
Interface: Resumo, nível semântico e referências.
Condição: Originais permanecerem disponíveis.
Aceite proposto: Comparar resposta detalhada com resumo e com folha.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V3A-S039. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar disco de memória semântica apenas por ser durável.
- Não usar resumo como substituto literal da evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo total de acesso e leitura; mais níveis podem aumentar complexidade sem melhorar respostas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T047, T048, T050, T063, T071

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S039 — Redis Key eviction

[https://redis.io/docs/latest/develop/reference/eviction/](https://redis.io/docs/latest/develop/reference/eviction/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Políticas de eviction, noeviction, LRU aproximado, LFU probabilístico e distinção entre expiração e pressão de capacidade.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

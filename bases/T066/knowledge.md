# T066 — Memory Resolver / Reference Resolver

**Nome canônico:** Memory Resolver / Reference Resolver  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T066  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** resolvedor de memória; resolvedor de referências

## T066:C01 — conceito

Resolve um identificador de memória ou artefato para a versão e o conteúdo corretos. Centraliza validação de acesso, integridade, existência e leitura parcial. Não deve interpretar um caminho recebido como autorização para acessar qualquer arquivo.

Como funciona:
- Receber referência com escopo e versão.
- Verificar autorização e localizar o objeto.
- Entregar conteúdo ou intervalo com metadados de completude.

## T066:C02 — aplicacao

Quando usar:
- Arquiteturas que passam referências entre agentes.
- Memórias externas em múltiplos armazenamentos.

Quando não usar:
- Não aceitar URLs ou caminhos arbitrários sem regras de resolução e escopo.

Implementação proposta:
- Proposta: definir formato de ID e schema de resposta.
- Distinguir not_found, forbidden, stale_version e partial.
- Validar hash quando exigido e retornar meios de continuar leitura de um objeto grande.

Aplicação LAI proposta:
Proposta LAI: construir um resolvedor comum para evidências e estado da Helena, usando referências estáveis em relatórios e checkpoints.

## T066:C03 — riscos_validacao

Armadilhas:
- Um alias como latest pode mudar entre etapas.
- Erro genérico pode ser confundido com memória inexistente, induzindo recriação indevida.

Métricas sugeridas:
- Referências resolvidas na versão pedida.
- Tempo de resolução e taxa de conteúdo parcial mal interpretado.

Testes propostos:
- Tentar resolver ID de outro namespace e exigir rejeição.
- Pedir versão antiga existente e retornar exatamente aquela versão ou erro explícito.

## T066:C04 — perguntas_proveniencia

Pergunta: O resolvedor também decide relevância?
Resposta: Pode integrar-se à busca, mas sua função principal é obter o objeto exato pedido com garantias de identidade e acesso.

Pergunta: Posso retornar só texto?
Resposta: Metadados de versão, origem e completude ajudam a evitar interpretações incorretas e devem acompanhar o texto.

Pergunta: Um recurso encontrado já foi lido?
Resposta: Não. Descoberta fornece metadados ou referência. A resposta deve distinguir recurso listado, conteúdo aberto e conteúdo parcialmente consumido.

Pergunta: Posso recuperar por similaridade após not_found?
Resposta: Pode iniciar outra busca, mas devolva candidatos como alternativas. Não finja que um registro parecido é a versão exata que estava referenciada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T066:C05 — mecanismo_avancado

Resolver uma memória envolve transformar um nome lógico em uma versão concreta e depois obter seus bytes. Essas etapas podem observar estados diferentes se o alias mudar entre consultas. Uma resolução reproduzível devolve a versão efetiva junto do conteúdo e mantém leituras parciais ancoradas nela. Busca semântica pode sugerir outro registro quando a referência falha, mas não deve substituir silenciosamente a identidade originalmente solicitada.

Condição de contorno:
O resolvedor não consegue garantir disponibilidade de objetos apagados ou comprovar autoria apenas por encontrar bytes cujo hash corresponde ao identificador.

Contrato proposto:
- Entradas: Referência, versão ou política de alias, escopo de acesso e faixa de leitura desejada.
- Saídas: Conteúdo identificado, versão efetiva, integridade verificável e status explícito de completude.
- Estado: Mapeamento de aliases, revisões de acesso, referências já resolvidas e cursores vinculados à versão.
- Invariante: Todas as partes de uma leitura compõem a mesma revisão, salvo solicitação explícita de atualização.

Compromissos de projeto:
- Fixar versão favorece reprodução e pode impedir acesso à informação mais recente.
- Resolver aliases automaticamente simplifica uso e exige tornar visível a revisão realmente consultada.

## T066:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar latest entre duas páginas de leitura. O resolvedor deve manter o objeto original ou invalidar o cursor, evitando entregar um documento composto de versões diferentes.

Plano de avaliação proposto:
Avaliação proposta: comparar referências versionadas e aliases mutáveis sob atualizações concorrentes. Medir leituras mistas, erros corretamente classificados, latência e recuperação de conteúdo; testar ausência, acesso negado e corrupção como estados distintos.

Comparações:
- T015 (complements): O uso de referências depende de um componente que consiga materializar conteúdo com identidade e escopo conhecidos.
- T061 (complements): Endereçamento por conteúdo oferece verificação de identidade para objetos resolvidos, sem garantir disponibilidade.

Afirmação rastreável:
MCP Resources define recursos identificados por URI e operações de leitura; IPFS distingue identificação por conteúdo de localização.
Suporte: related; fontes: V3A-S019, V3A-S038
Limite: Imutabilidade de versão, autorização e cursores consistentes são contratos adicionais da implementação proposta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T066:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu resolução pinada. Aqui referências são resolvidas em duas fases para distinguir identidade, disponibilidade e conteúdo efetivamente lido.

Projeto e decomposição
Primeiro resolver identidade e versão; depois abrir o recorte e verificar integridade. Um recurso encontrado pode estar indisponível, parcial ou exigir conversão que altera offsets.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

Controle adaptativo
Use alias apenas para descoberta. Ao iniciar tarefa dependente, fixe revisão e registre atualização detectada; seguir alias latest silenciosamente pode misturar evidências de momentos diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

Validação contrafactual
Compare resolução direta e fallback semântico em referências quebradas. Meça substituições indevidas, falsos sucessos e tempo de recuperação; fallback deve retornar candidato, não fingir identidade exata. Unidade de avaliação: resolução de referência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

USO AVANÇADO — Handoff entre agentes
Cenário: Referências viajam sem conteúdo integral.
Estratégia: Resolver cada artefato, verificar recortes e construir lista de faltas antes de aceitar tarefa. Pedir substituição explícita quando origem sumiu.
Papel do modelo pequeno: 3–7B interpreta manifesto.
Aceite proposto: Nenhuma referência ausente pode aparecer como evidência lida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

USO AVANÇADO — Documentação renomeada
Cenário: Caminhos mudam entre versões.
Estratégia: Usar mapa de renomeação e digest para confirmar continuidade; se conteúdo divergir, tratar como nova versão e reavaliar conclusão.
Papel do modelo pequeno: 8–14B compara significado.
Aceite proposto: Alias novo não pode ocultar alteração material.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V3A-S038.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de referências estruturadas com erro tipado.
8–14B: Revisor de candidatos de substituição e diferenças locais.
15–30B: Integrador de evidências quando múltiplas resoluções produzem versões incompatíveis.
Requisitos de treino/runtime: Registry de aliases, versões e estados de abertura; integridade e autorização são verificações distintas.
Não aplicar quando: Identidade só pode ser aproximada e a tarefa exige documento exato.

## T066:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C013 — Google / Knowledge Graph na busca Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Anúncio relata início da implantação a usuários da busca.
Mecanismo documentado: Entidades e relações permitem desambiguação e apresentação de fatos relacionados.
Correspondência com esta base: Desambiguação de entidades inspira resolução, sem contrato de versão desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Fazer 3–7B propor entidades candidatas e confirmar identidade com chaves estruturadas.
Limite: Não comprova Microsoft GraphRAG, causalidade, bitemporalidade ou arquitetura LLM de 2012. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S018.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q019.

## T066:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T066 → T015 [requires]
Como combinar: Receber referência com seletor e revisão.
Interface: URI, versão, intervalo e tipo esperado.
Condição: Produtor declarar se conteúdo foi realmente aberto.
Aceite proposto: Testar referência correta com seletor inválido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V3A-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T066 → T072 [feeds]
Como combinar: Fixar conjunto resolvido numa revisão de trabalho.
Interface: Manifesto de recursos e revisões observadas.
Condição: Tarefa não misturar latest de momentos diferentes.
Aceite proposto: Atualizar alias durante carga e detectar incompatibilidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V3A-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir nome parecido com mesmo objeto.
- Não apresentar resultado parcial como abertura integral.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar integridade de citações e custo de resolução; modelo maior não torna alias ambíguo uma identidade comprovada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T053, T061, T067

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V4A-S018 — Introducing the Knowledge Graph: things, not strings

[https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação gradual de entidades e relações na busca Google; não é GraphRAG moderno.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T007 — Response Caching por Hash

**Nome canônico:** Response Caching por Hash  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** exact response cache; cache exato por hash

## T007:C01 — conceito

Cache de resposta por identidade exata de uma requisição normalizada. Um hash funciona como endereço compacto de todos os fatores que alteram a resposta. Não reconhece paráfrases e não verifica a verdade do conteúdo armazenado.

Como funciona:
- Construir representação canônica da requisição e de suas dependências.
- Calcular hash criptográfico e procurar entrada válida no mesmo escopo.
- Retornar a resposta ou executar e gravar o resultado com política de expiração.

Nota de nomenclatura: Padrão de engenharia formado por cache exato e endereçamento por conteúdo; não é um algoritmo específico de LLM.

## T007:C02 — aplicacao

Quando usar:
- Transformações repetidas sobre o mesmo documento e versão.
- Consultas determinísticas de custo alto e dados estáveis.

Quando não usar:
- Evitar reutilização quando estado externo relevante não faz parte da chave ou das condições de validade.

Implementação proposta:
- Proposta: hashear modelo, parâmetros, prompt, fontes, schemas e namespace.
- Manter a requisição canônica ou sua descrição para auditar colisões lógicas.
- Não armazenar respostas incompletas, erros transitórios ou saídas sem validação mínima.

Aplicação LAI proposta:
Proposta LAI: cachear extrações técnicas verificadas por hash de arquivo e versão de schema; manter namespaces separados para evitar mistura entre contextos.

## T007:C03 — riscos_validacao

Armadilhas:
- Omitir a versão de uma fonte torna a chave semanticamente incompleta.
- Normalizar excessivamente pode tornar iguais entradas que significam coisas diferentes.

Métricas sugeridas:
- Acertos corretos e acertos indevidos.
- Tempo economizado e tamanho do armazenamento.

Testes propostos:
- Mudar um único campo decisivo e exigir uma chave diferente.
- Permutar campos de JSON sem alterar significado e verificar normalização estável.

## T007:C04 — perguntas_proveniencia

Pergunta: SHA-256 elimina todos os erros de cache?
Resposta: Não. Um bom hash não corrige uma chave que deixou de fora informação relevante.

Pergunta: Como tratar temperatura maior que zero?
Resposta: Reutilizar fixa uma amostra anterior; documente esse comportamento ou desative cache quando diversidade for necessária.

Pergunta: SHA-256 elimina todo risco de cache incorreto?
Resposta: Não. Um hash forte não corrige uma chave incompleta nem uma resposta originalmente errada; colisão de projeto costuma ser mais relevante que colisão criptográfica.

Pergunta: Cache de resposta pode repetir uma ferramenta de escrita?
Resposta: Reutilizar texto não equivale a executar nem confirmar um efeito. Operações de escrita precisam de identidade e reconciliação próprias, separadas deste cache.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T007:C05 — mecanismo_avancado

A chave deve representar a requisição efetiva, não apenas o texto visível da pergunta. Modelo, parâmetros, instruções, escopo e revisão das fontes podem alterar a resposta. Canonicalização resolve diferenças de serialização, como ordem de propriedades, mas não decide que duas instruções significam a mesma coisa. Normalizar arrays, tipos ou espaços significativos indevidamente cria colisões semânticas mesmo com hash criptográfico correto.

Condição de contorno:
Requisições dependentes de relógio, aleatoriedade desejada ou estado externo mutável não são reutilizáveis sem incorporar uma fronteira válida desses fatores.

Contrato proposto:
- Entradas: Envelope completo do pedido e versão da regra de canonicalização.
- Saídas: Chave, resposta elegível e metadados da execução que a originou.
- Estado: Entradas associadas à revisão das dependências e ao escopo de acesso.
- Invariante: Pedidos distintos em um fator que muda o resultado não recebem deliberadamente a mesma identidade.

Compromissos de projeto:
- Chaves completas diminuem hits, mas reduzem reutilização incorreta.
- Canonicalização acrescenta trabalho e exige tratamento rigoroso de números, Unicode e campos opcionais.

## T007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: enviar objetos com propriedades em ordem diferente e depois mudar um parâmetro relevante. Os primeiros devem compartilhar a identidade definida; a alteração de parâmetro deve produzir outra chave.

Plano de avaliação proposto:
Avaliação proposta: comparar identidade de bytes e envelope canonicalizado com casos equivalentes e distintos. Medir hits corretos, colisões de significado, tempo de chaveamento e recuperação após mudança de política.

Comparações:
- T005 (alternative): Cache semântico busca equivalência aproximada; o hash depende de equivalência explicitamente definida.
- T061 (complements): Endereçamento por conteúdo pode armazenar os artefatos associados à resposta.

Afirmação rastreável:
RFC 8785 define representação JSON determinística apropriada a operações reproduzíveis de hashing.
Suporte: direct; fontes: V3A-S006
Limite: A especificação não define quais campos de uma requisição de LLM são semanticamente obrigatórios.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu identidade canônica da requisição. Aqui o cache ganha admissão por valor econômico e separação entre resultado calculado e apresentação.

Projeto e decomposição
Cacheie artefatos determinísticos antes da resposta linguística: extração validada, conjunto de candidatos ou tabela calculada. Isso mantém reutilização quando muda apenas o estilo solicitado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

Controle adaptativo
Use política de admissão que considere custo evitado e frequência prevista. Respostas enormes consultadas uma vez podem expulsar pequenos resultados caros e recorrentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

Validação contrafactual
Compare cache de resposta, cache intermediário e execução integral. Inclua tempo de serialização, transferência e verificação de dependências. Unidade de avaliação: requisição versionada. Teste duas apresentações do mesmo resultado calculado e uma terceira com configuração de cálculo diferente. As primeiras podem reutilizar o artefato intermediário, enquanto a terceira deve provocar recomputação. Medir esse padrão separa economia legítima de uma chave insuficiente. Avalie também quando transferir o artefato custa mais do que refazer uma computação pequena.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

USO AVANÇADO — Reformatação recorrente
Cenário: O mesmo relatório precisa formatos diferentes.
Estratégia: Reusar tabela validada e gerar apresentação por pedido; invalidar se qualquer fonte mudar.
Papel do modelo pequeno: 3–7B formata sem recalcular fatos.
Aceite proposto: Valores devem coincidir com artefato canônico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

USO AVANÇADO — Validação repetida
Cenário: Vários agentes verificam o mesmo arquivo.
Estratégia: Reusar laudo por hash do conteúdo, versão do validador e configuração. Resultado parcial não entra no cache.
Papel do modelo pequeno: Modelo pequeno interpreta laudo; código verifica identidade.
Aceite proposto: Arquivo alterado precisa provocar miss.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Formatador sobre resultado exato previamente validado.
8–14B: Explicador de laudos e diagnósticos cacheados por revisão.
15–30B: Sintetizador de múltiplos artefatos sem reutilizar conclusão incompatível.
Requisitos de treino/runtime: Armazenamento por chave e estatísticas de custo; separar conteúdo, configuração e versão do produtor.
Não aplicar quando: Resultado depende de estado externo não representado na chave.

## T007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q011.

## T007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T007 → T061 [complements]
Como combinar: Endereçar artefatos reutilizáveis pelo conteúdo.
Interface: Digest, codec e versão do formato.
Condição: Bytes e interpretação forem estáveis.
Aceite proposto: Alterar configuração e verificar nova identidade lógica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S006, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T007 → T150 [complements]
Como combinar: Unificar computações simultâneas da mesma chave.
Interface: Chave completa e promessa de resultado.
Condição: Cancelamento de cliente não apagar trabalho compartilhado.
Aceite proposto: Executar pedidos concorrentes e contar computações reais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S006, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não armazenar falha transitória como resultado definitivo.
- Conservar fonte e idade do artefato cacheado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar trabalho evitado com corretude idêntica; cache não deve ser creditado como capacidade cognitiva.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T031, T061, T157

## Fontes primárias associadas

### A-S005 — LLM Caching

[https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/](https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico com embeddings, limiar de distância, TTL e filtros de acesso.

Limite: Documentação consultada da versão 0.10.0, não afirma ser a versão corrente do pacote.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S006 — RFC 8785: JSON Canonicalization Scheme (JCS)

[https://www.rfc-editor.org/rfc/rfc8785.html](https://www.rfc-editor.org/rfc/rfc8785.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Serialização JSON determinística para hashing e assinatura; preservação de conteúdo e restrições do formato. Caching é aplicação editorial. 

Limite: RFC informativo, não norma IETF Standards Track. Não fornece autorização, semântica de equivalência de pedidos nem veracidade do conteúdo.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

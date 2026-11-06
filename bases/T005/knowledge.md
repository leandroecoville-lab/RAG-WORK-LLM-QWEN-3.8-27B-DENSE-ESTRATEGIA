# T005 — Semantic Caching

**Nome canônico:** Semantic Caching  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cache semântico

## T005:C01 — conceito

Armazena perguntas ou representações de contexto e respostas anteriores para reutilizar uma resposta quando uma nova consulta for semanticamente equivalente dentro de um escopo permitido. Similaridade vetorial é um sinal de proximidade, não uma prova de que a resposta continua correta.

Como funciona:
- Aplicar filtros de identidade, versão e escopo antes da busca.
- Comparar embedding da pergunta com entradas válidas do cache.
- Aceitar somente candidatos que satisfaçam limiar e condições de reutilização.

## T005:C02 — aplicacao

Quando usar:
- Perguntas frequentes sobre conteúdo estável.
- Variações de redação que realmente pedem o mesmo fato.

Quando não usar:
- Não reutilizar indiscriminadamente resultados de saldos, permissões, horários ou estados mutáveis.

Implementação proposta:
- Proposta: incluir versão documental e do modelo na chave lógica.
- Calibrar limiar com pares equivalentes e pares parecidos com respostas diferentes.
- Invalidar entradas por mudança da fonte e registrar por que cada acerto foi aceito.

Aplicação LAI proposta:
Proposta LAI: começar por FAQs técnicas estáveis e segmentadas; só expandir após medir falsos acertos no vocabulário real da empresa.

## T005:C03 — riscos_validacao

Armadilhas:
- Perguntas sobre clientes distintos podem ser quase idênticas.
- Negação, data ou unidade numérica podem inverter a resposta apesar da alta similaridade.

Métricas sugeridas:
- Precisão dos acertos do cache, não apenas taxa de acertos.
- Tempo e custo poupados após custo de busca e manutenção.

Testes propostos:
- Testar pares que diferem só por não, data, tenant ou valor.
- Alterar a política fonte e verificar que respostas antigas não são retornadas.

## T005:C04 — perguntas_proveniencia

Pergunta: Um embedding muito parecido garante mesma resposta?
Resposta: Não. Os detalhes decisivos podem ter pouco peso no vetor; use filtros e avaliação de equivalência.

Pergunta: Cache semântico substitui RAG?
Resposta: Não. Ele reaproveita respostas; RAG recupera evidência para construir uma resposta nova.

Pergunta: Posso copiar um limiar entre modelos de embedding?
Resposta: Não com confiança. Distribuições e métricas mudam; recalibre usando pares relevantes ao domínio e declare a unidade da distância.

Pergunta: Um hit frequente deve renovar a validade?
Resposta: A frequência pode justificar permanência em memória, mas não atualidade factual. Renovar TTL sem validar dependências pode perpetuar uma resposta obsoleta.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T005:C05 — mecanismo_avancado

O erro mais caro costuma ser aceitar uma pergunta próxima cuja resposta difere em um pequeno detalhe: negação, unidade, data ou identidade. A decisão precisa combinar similaridade com condições exatas de elegibilidade. Embeddings de versões diferentes também não devem compartilhar a mesma comparação apenas por terem dimensões iguais; o espaço vetorial faz parte do contrato.

Condição de contorno:
O cache deixa de ser confiável quando a resposta depende de estado pessoal ou temporal ausente da chave e dos filtros, mesmo que a distância seja muito pequena.

Contrato proposto:
- Entradas: Consulta, escopo autorizado, versão das fontes e identificador do embedding.
- Saídas: Hit elegível com origem e validade, ou miss que segue para geração.
- Estado: Índice vetorial segregado por versões compatíveis e metadados de dependência.
- Invariante: Proximidade vetorial nunca sobrepõe uma incompatibilidade de escopo ou versão.

Compromissos de projeto:
- Limiar permissivo eleva reutilização e também falsos acertos.
- Filtros mais estritos reduzem cobertura, mas evitam compartilhar respostas entre contextos diferentes.

## T005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas consultas quase iguais que mudem apenas o sujeito ou a validade temporal. A resposta armazenada deve ser recusada quando esses campos alterarem a resposta correta.

Plano de avaliação proposto:
Avaliação proposta: comparar cache exato, cache semântico e execução sem cache. Usar pares equivalentes e quase equivalentes criados para o domínio; medir precisão dos hits, cobertura e custo. Escolher limiar pela tolerância real ao falso acerto.

Comparações:
- T031 (complements): Respostas reutilizáveis precisam de uma regra explícita de validade e invalidação.
- T007 (alternative): Identidade exata evita a decisão de equivalência semântica, mas perde paráfrases.

Afirmação rastreável:
RedisVL SemanticCache expõe distância, filtros, vetorizador e TTL como controles distintos.
Suporte: direct; fontes: V3A-S007
Limite: Esses controles não demonstram automaticamente equivalência semântica ou correção da resposta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou falsos hits e filtros. A camada nova é admissão seletiva de respostas e cache de artefatos parciais verificáveis.

Projeto e decomposição
Diferencie cache da resposta completa e cache de evidências recuperadas. Perguntas similares podem compartilhar documentos sem compartilhar conclusão. Priorize reuso de candidatos quando pequenas mudanças alterarem o resultado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

Controle adaptativo
Admitir uma resposta exige fonte vigente e estabilidade do domínio. Registre quais atributos tornam a equivalência inválida, como versão, unidade e finalidade. Um classificador pode sugerir hit; regras fechadas confirmam elegibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

Validação contrafactual
Construa pares mínimos que mudam somente um atributo decisivo. Compare taxa de aceitação errada e custo evitado, não apenas similaridade média. Unidade de avaliação: família de consultas. Separe validação de admissão e validação de reutilização. Uma resposta pode ter sido correta quando entrou no cache e inadequada para a consulta atual. Teste pares com mesma intenção geral, mas população, unidade ou versão diferente, e registre em qual filtro o hit foi recusado. Isso permite reduzir custo sem esconder falsos acertos no agregado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

USO AVANÇADO — Suporte com perguntas recorrentes
Cenário: Usuários reformulam dúvida sobre uma versão.
Estratégia: Buscar candidato, validar versão e pré-condições, reutilizar resposta apenas se o contrato continuar equivalente.
Papel do modelo pequeno: 3–7B extrai atributos para filtros.
Aceite proposto: Nenhum hit em versão incompatível no conjunto de validação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

USO AVANÇADO — Pesquisa repetida com novo critério
Cenário: Consultas variam o julgamento solicitado.
Estratégia: Reusar trechos elegíveis e gerar nova conclusão; não devolver resposta anterior quando muda o critério de comparação.
Papel do modelo pequeno: 8–14B reinterpreta evidências existentes.
Aceite proposto: Citação atual e conclusão sensível à mudança do critério.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de atributos que alimenta chave de elegibilidade.
8–14B: Verificador de equivalência contextual em candidatos curtos.
15–30B: Leitor de evidências cacheadas para síntese de critérios múltiplos.
Requisitos de treino/runtime: Índice vetorial, metadados de dependência e caminho de bypass; calibrar limiar por domínio.
Não aplicar quando: Respostas variam por identidade, tempo ou estado que o cache não consegue verificar.

## T005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C017 — Microsoft / API Management semantic response cache
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Política disponível busca respostas em cache externo por proximidade.
Mecanismo documentado: Embedding, limiar e particionamento de cache por expressões.
Correspondência com esta base: Retorno de resposta por similaridade semântica explicitado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Aceitar somente domínio estável e validar pares quase iguais com entidades ou negações diferentes.
Limite: Não comprova implantação nem taxa de falsos acertos; limiares do serviço não são probabilidades. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q012.

## T005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T005 → T031 [requires]
Como combinar: Revogar itens derivados quando a base muda.
Interface: dependency_ids, revisão e lista de respostas afetadas.
Condição: Dependências registradas no momento de admissão.
Aceite proposto: Alterar fonte e medir sobrevivência indevida de hits.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S016, V3A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T005 → T205 [complements]
Como combinar: Testar equivalência antes de reutilizar resposta.
Interface: Par de pedidos e atributos relevantes.
Condição: Verificação mais barata que refazer e validada no domínio.
Aceite proposto: Incluir negações e quantificadores quase iguais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S016, V3A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar resposta cuja origem não pode ser reaberta.
- Separar falha do cache de ausência de candidato.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo por resposta correta com reexecução completa; mais hits podem piorar o sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T007, T031, T205

## Fontes primárias associadas

### A-S005 — LLM Caching

[https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/](https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico com embeddings, limiar de distância, TTL e filtros de acesso.

Limite: Documentação consultada da versão 0.10.0, não afirma ser a versão corrente do pacote.

### V3A-S007 — RedisVL LLM Cache API

[https://redis.io/docs/latest/develop/ai/redisvl/api/cache/](https://redis.io/docs/latest/develop/ai/redisvl/api/cache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: SemanticCache com filtros, distância, vetorizador e TTL; diferenças de capacidades entre implementações.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S016 — Get cached responses of large language model API requests

[https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy](https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico por proximidade vetorial, limiar e particionamento vary-by.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

# T031 — Semantic Cache Invalidation

**Nome canônico:** Semantic Cache Invalidation  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T031  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** invalidação de cache semântico

## T031:C01 — conceito

Define quando uma resposta reutilizável por similaridade deixa de ser válida. A proximidade semântica da pergunta pode permanecer alta enquanto fontes, políticas ou contexto mudam. Por isso, expiração e dependências são condições adicionais à busca vetorial.

Como funciona:
- Registrar fontes e versões usadas em cada resposta cacheada.
- Detectar alteração, expiração ou mudança de escopo.
- Remover ou tornar inelegíveis entradas afetadas antes da próxima reutilização.

## T031:C02 — aplicacao

Quando usar:
- FAQs cuja documentação é atualizada.
- Caches de consultas condicionadas a versão de produto ou contrato.

Quando não usar:
- Não depender somente de TTL quando uma mudança exige invalidação imediata.

Implementação proposta:
- Proposta: manter vetor de dependências ou geração do índice na entrada.
- Combinar expiração temporal com invalidação por evento.
- Em caso de falha na propagação, preferir recomputar a resposta a servir uma entrada de validade desconhecida.

Aplicação LAI proposta:
Proposta LAI: vincular respostas técnicas a hashes de contratos e snapshots de repositórios; decisões comerciais mutáveis não devem depender só de similaridade.

## T031:C03 — riscos_validacao

Armadilhas:
- Invalidação parcial pode deixar respostas antigas em réplicas.
- A mesma pergunta pode mudar de resposta por contexto não registrado na dependência.

Métricas sugeridas:
- Tempo entre mudança da fonte e rejeição do cache.
- Taxa de respostas obsoletas e recomputações desnecessárias.

Testes propostos:
- Atualizar uma regra e consultar uma paráfrase da pergunta antiga.
- Simular atraso no evento de invalidação e exigir checagem de versão.

## T031:C04 — perguntas_proveniencia

Pergunta: Um TTL curto resolve tudo?
Resposta: Não. Ainda existe uma janela de obsolescência e TTL curto pode anular a economia do cache.

Pergunta: Preciso refazer todos os embeddings após mudar uma resposta?
Resposta: Não necessariamente. A política deve distinguir atualização de resposta, metadados e representação vetorial.

Pergunta: Um cache negativo pode ser reutilizado?
Resposta: Somente se a ausência observada tiver escopo e validade definidos. Falha de recuperação ou indisponibilidade não equivale a inexistência do fato.

Pergunta: Como tratar uma entrada acessada durante invalidação?
Resposta: Defina o contrato de consistência. Para exigência forte, verifique versão ou época no caminho de leitura; apenas apagar em segundo plano deixa uma janela de reutilização.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T031:C05 — mecanismo_avancado

Uma resposta pode ficar inválida por mudança na fonte, no direito de acesso, na política ou no modelo de interpretação. TTL limita idade, mas não acompanha necessariamente essas mudanças. Um desenho por dependências registra quais revisões sustentam cada entrada e verifica sua elegibilidade no hit; invalidação por evento e expiração podem coexistir como controles de problemas diferentes.

Condição de contorno:
Se não é possível identificar dependências ou sua versão vigente, o cache não pode prometer atualização imediata somente ajustando o limiar semântico.

Contrato proposto:
- Entradas: Entrada candidata, revisões das dependências e contexto atual de acesso.
- Saídas: Decisão de servir, revalidar ou remover a entrada, com motivo.
- Estado: Índice de dependências, época de política e prazo de retenção.
- Invariante: Um hit semelhante não ignora revogação ou revisão incompatível conhecida no momento da leitura.

Compromissos de projeto:
- Invalidação precisa exige metadados e coordenação entre serviços.
- Expiração ampla simplifica operação, mas provoca misses e ainda permite obsolescência até o vencimento.

## T031:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: armazenar uma resposta e corrigir a fonte antes de vencer o TTL. A próxima consulta equivalente deve rejeitar ou revalidar a entrada, sem esperar a expiração para reconhecer a correção.

Plano de avaliação proposto:
Avaliação proposta: comparar TTL isolado, versão por namespace e dependências explícitas. Variar frequência de mudanças e reutilização; medir respostas obsoletas, tempo de propagação, misses evitáveis e custo de revalidação.

Comparações:
- T005 (complements): A invalidação decide elegibilidade; a similaridade só localiza uma resposta candidata.
- T072 (complements): Versões de memória e fonte permitem detectar dependências incompatíveis.

Afirmação rastreável:
RedisVL oferece controles separados de TTL, filtros e exclusão de entradas de cache.
Suporte: direct; fontes: V3A-S007
Limite: A rastreabilidade das dependências e sua propagação são responsabilidades adicionais da aplicação.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T031:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciou TTL e invalidação. Aqui a estratégia usa granularidade de dependências e prazo de frescor observável por resposta.

Projeto e decomposição
Associe cada resposta às entidades, fontes e versões que poderiam alterá-la. Dependência apenas no documento inteiro provoca invalidação excessiva; dependência estreita demais deixa resposta antiga ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

Controle adaptativo
Defina frescor por classe de dado e meça atraso entre correção confirmada e último hit obsoleto. A verificação deve consultar o caminho visto pelo cliente, incluindo réplicas e índices.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

Validação contrafactual
Compare invalidação por documento, por entidade e TTL. Injete atualização e preenchimento atrasado para medir sobrevivência indevida; hit rate não é métrica de consistência. Unidade de avaliação: resposta derivada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

USO AVANÇADO — FAQ com políticas alteradas
Cenário: Uma cláusula muda várias respostas.
Estratégia: Publicar nova revisão, revogar respostas dependentes e verificar réplicas antes de liberar reutilização para cláusula sensível.
Papel do modelo pequeno: 3–7B identifica candidatos afetados; código confirma vínculos.
Aceite proposto: Nenhum hit antigo após o prazo de frescor definido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

USO AVANÇADO — Cache de busca derivada
Cenário: Índice recebe correções assíncronas.
Estratégia: Marcar resultados por revisão da projeção e desviar consultas sensíveis para origem quando o atraso exceder o limite.
Papel do modelo pequeno: 8–14B responde com evidência elegível.
Aceite proposto: Resposta deve informar insuficiência em vez de citar projeção revogada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de entidades para construir dependências candidatas.
8–14B: Revisor de alcance semântico de uma alteração e seus efeitos.
15–30B: Analista de conflitos entre versões quando regras de invalidação não bastarem.
Requisitos de treino/runtime: Eventos de atualização, versões monotônicas por objeto e monitoramento do caminho de leitura; LLM não controla sozinho a coerência.
Não aplicar quando: Não é possível saber a origem da resposta ou detectar atualizações relevantes.

## T031:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: Invalidação de cache convencional, não proximidade semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

V4A-C017 — Microsoft / API Management semantic response cache
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Política disponível busca respostas em cache externo por proximidade.
Mecanismo documentado: Embedding, limiar e particionamento de cache por expressões.
Correspondência com esta base: Particionamento protege escopo, mas política de invalidação completa é desenho adicional.
Transferência proposta para modelo pequeno: Proposta de engenharia: Aceitar somente domínio estável e validar pares quase iguais com entidades ou negações diferentes.
Limite: Não comprova implantação nem taxa de falsos acertos; limiares do serviço não são probabilidades. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q007, V4A-Q012.

## T031:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T031 → T007 [requires]
Como combinar: Guardar dependências junto ao item cacheado.
Interface: Chave, origem, revisão e estado de revogação.
Condição: Admissão ocorrer com proveniência completa.
Aceite proposto: Alterar entidade e localizar todos os itens afetados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S011, V4A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T031 → T075 [complements]
Como combinar: Reconciliar preenchimento atrasado com versão atual.
Interface: Versão observada, versão vigente e operação pendente.
Condição: Regra impedir regressão de versão.
Aceite proposto: Reproduzir chegada de valor antigo após invalidar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S011, V4A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apagar a única informação de versão durante evicção.
- Não interpretar ausência temporária como exclusão definitiva.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar exposição a resposta obsoleta; modelos maiores também erram quando recebem cache inconsistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T007, T072

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

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S016 — Get cached responses of large language model API requests

[https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy](https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico por proximidade vetorial, limiar e particionamento vary-by.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.

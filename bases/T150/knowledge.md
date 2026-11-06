# T150 — Request Coalescing / Singleflight

**Nome canônico:** Request Coalescing / Singleflight  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T150  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** coalescência de solicitações; singleflight

## T150:C01 — conceito

Coalescência faz solicitações concorrentes equivalentes compartilhar uma execução já em andamento. Singleflight é uma implementação conhecida desse padrão. Difere de cache persistente: o foco é evitar trabalho duplicado simultâneo, ainda que o resultado não seja guardado depois.

Como funciona:
- Derivar chave que identifica operação e entradas equivalentes.
- O primeiro solicitante inicia a execução; os demais aguardam o mesmo trabalho.
- Distribuir resultado ou erro e liberar a entrada em andamento.

## T150:C02 — aplicacao

Quando usar:
- Muitas consultas simultâneas ao mesmo recurso.
- Expiração de cache que provoca várias recomputações idênticas.

Quando não usar:
- Ações com intenção diferente, dados privados distintos ou respostas dependentes do solicitante.

Implementação proposta:
- Incluir tenant, autorização e versão relevante na chave.
- Definir cancelamento por assinante sem cancelar indevidamente os demais.
- Limitar tempo de vida e remover registros órfãos após falha.

Aplicação LAI proposta:
Proposta: coalescer carregamento de documentos e consultas repetidas de especialistas da Helena quando o contrato comprovar equivalência.

## T150:C03 — riscos_validacao

Armadilhas:
- Chave incompleta pode compartilhar resposta entre clientes.
- Uma execução lenta cria fila de espera para todos os solicitantes daquela chave.

Métricas sugeridas:
- Número de operações reais por solicitações equivalentes.
- Latência dos seguidores e economia de chamadas.

Testes propostos:
- Disparar várias leituras idênticas e exigir uma execução real em andamento.
- Repetir com tenants distintos e conferir que nunca compartilham resposta.

## T150:C04 — perguntas_proveniencia

Pergunta: Singleflight garante uma execução para sempre?
Resposta: Não. Suprime duplicatas concorrentes dentro do escopo implementado.

Pergunta: Substitui idempotência?
Resposta: Não. Uma nova tentativa futura ainda pode repetir efeito e precisa de proteção própria.

Pergunta: Coalescer erros equivale a cache negativo?
Resposta: Não. O erro é compartilhado entre aguardantes da chamada ativa; guardá-lo depois exige política adicional de expiração.

Pergunta: A chave pode ser só o nome do documento?
Resposta: Não se revisão, escopo ou parâmetros alterarem a leitura; a chave deve representar equivalência real do resultado.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T150:C05 — mecanismo_avancado

A equivalência de solicitações precisa incluir mais que o texto visível: versão do recurso, parâmetros efetivos, identidade de escopo e nível de consistência podem mudar o resultado. Singleflight distribui inclusive o mesmo erro aos aguardantes; se todos repetirem imediatamente, forma-se uma nova rajada. No código Go consultado, Forget libera futuras chamadas da espera pela execução anterior, sem cancelá-la; isso permite coexistência de trabalhos para a mesma chave.

Condição de contorno:
Coalescer operações com efeitos diferentes ou dados de escopos distintos viola a semântica, mesmo quando os argumentos aparentam igualdade.

Contrato proposto:
- Entradas: Chave de equivalência completa, função de leitura e deadline de cada interessado.
- Saídas: Resultado compartilhado, erro e indicação de participação na execução comum.
- Estado: Execução líder, aguardantes e ciclo de vida da chave.
- Invariante: Cancelar um aguardante não cancela implicitamente trabalho ainda necessário aos demais.

Compromissos de projeto:
- Compartilhar reduz trabalho repetido e acopla a latência dos aguardantes ao líder.
- Esquecer uma chave destrava novas tentativas e pode duplicar carga enquanto a chamada anterior termina.

## T150:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: cancelar um aguardante, manter outro e chamar Forget enquanto a operação está ativa; verificar separadamente resultado compartilhado e possibilidade de nova execução.

Plano de avaliação proposto:
Comparar sem coalescência e com coalescência sob rajadas de chaves populares e falhas. Medir execuções físicas por intenção de leitura, espera, erros compartilhados e memória retida. Separar efeitos de cache posterior e compartilhamento apenas em andamento.

Comparações:
- T157 (distinct_from): Hash de prefixo localiza estado de inferência; singleflight coordena uma execução ativa por chave.
- T162 (distinct_from): Idempotência limita efeito lógico; coalescência não a garante entre processos ou após término.

Afirmação rastreável:
A implementação Go documenta que Forget permite novas chamadas sem esperar pela chamada anterior.
Suporte: direct; fontes: V3C-S011
Limite: Essa semântica é da implementação inspecionada, não uma propriedade universal de todos os coalescedores.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T150:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou equivalência de chave e comportamento de Forget. A camada nova trata ciclo de vida dos aguardantes, publicação por versão e limites da coalescência em gerações probabilísticas.

Dono e consumidores distintos
Uma execução compartilhada tem uma identidade própria; cada consumidor mantém prazo e cancelamento independentes. A saída de um aguardante não deve cancelar a operação enquanto outros ainda precisam dela. Quando ninguém resta, a política pode cancelar o produtor, mas precisa confirmar o que já consumiu ou realizou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V4C-S022.

Publicação vinculada à versão
Se o recurso mudar durante a execução, o resultado antigo não deve preencher a chave da nova revisão. Registre versão observada e versão solicitada, publicando apenas no espaço correspondente. Invalidação de cache e fim do singleflight são eventos distintos: excluir uma entrada não interrompe necessariamente trabalho em andamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V3C-S037.

Probabilidade e privacidade
Duas inferências com o mesmo texto podem esperar diversidade ou contextos privados diferentes. Compartilhe somente quando contrato, fontes, identidade de escopo e política de amostragem permitirem o mesmo resultado. A redução de chamadas não justifica colapsar tentativas deliberadamente independentes usadas para avaliação ou busca de alternativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V3C-S017.

USO AVANÇADO — Busca documental após cache miss
Cenário: Muitos agentes solicitam o mesmo documento versionado.
Estratégia: Use uma busca compartilhada por documento, revisão e escopo. Distribua o resultado e seu estado aos aguardantes; erros recebem uma política comum de espera para impedir que todos reiniciem simultaneamente a chamada que acabou de falhar.
Papel do modelo pequeno: 3–7B consome trechos já recuperados; coalescência fica no cliente determinístico.
Aceite proposto: Proposta: medir chamadas à origem, espera por consumidor e contaminação entre versões durante rajadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S022, V3C-S011.

USO AVANÇADO — Inferência repetitiva de classificação
Cenário: Vários workflows pedem a mesma classificação sobre entrada imutável.
Estratégia: Fixe template, revisão do modelo e schema antes de compartilhar. Se a tarefa exige múltiplas amostras, inclua identidade da amostra e evite coalescência entre elas. Guarde a decisão de compartilhamento para auditar economias reais.
Papel do modelo pequeno: 3–14B pode atender classes fechadas; 15–30B não muda o requisito de equivalência.
Aceite proposto: Proposta: comparar resultado e custo com execução independente, incluindo cancelamento de parte dos consumidores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S011, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: classificador determinístico ou quase determinístico em domínio fechado, com revisão fixada.
8–14B: Proposta: extrações repetidas de fontes imutáveis sob contrato idêntico.
15–30B: Proposta: tarefas mais caras com evidência compartilhável, sem colapsar exploração de hipóteses diferentes.
Requisitos de treino/runtime: Requer gestão de aguardantes, timeout próprio e chave completa; singleflight local não coordena automaticamente réplicas.
Não aplicar quando: Não usar para ações de negócio distintas, inferência privada incompatível ou amostras que deveriam ser independentes.

## T150:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C022 — Cloudflare / CDN — request collapsing
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A documentação descreve cache lock para solicitações simultâneas do mesmo asset em um data center.
Mecanismo documentado: A primeira solicitação busca a origem; as demais aguardam e recebem a resposta compartilhada. O escopo é por localização, não exclusão global de todas as chamadas.
Correspondência com esta base: Há coalescência explícita de solicitações simultâneas por chave de asset.
Transferência proposta para modelo pequeno: Proposta: coalescer leitura idêntica de documentos ou inferência determinística com escopo e versões iguais, separando cancelamento de um consumidor do trabalho compartilhado.
Limite: Operational_product: documentação de comportamento do serviço sem deployment específico de cliente. Cache HTTP não demonstra equivalência de respostas probabilísticas de LLM.
Fontes: V4C-S022.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Cloudflare documenta request collapsing como recurso; não foi promovido a caso identificado de cliente nem a prova de coalescência LLM em produção.
Consultas registradas: V4C-Q009, V4C-Q017.

## T150:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T150 → T137 [complements]
Como combinar: Uma execução compartilhada consome uma reserva de produtor, conservando custos de entrega aos consumidores.
Interface: Chave, participantes e reserva de execução.
Condição: Cancelar um consumidor não liquida a reserva de todos.
Aceite proposto: Testar entradas e saídas concorrentes sem saldo duplicado ou perdido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T150 → T171 [complements]
Como combinar: Coalescência protege misses enquanto cache reaproveita resultados ou cálculo já armazenado.
Interface: Estado ativo, resultado publicado e versão de cache.
Condição: As políticas de expiração são separadas.
Aceite proposto: Alterar recurso durante a chamada e impedir publicação na revisão errada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S022, V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Diferenciar entrega duplicada de intenção nova que tem parâmetros iguais.
- Não apresentar uma exclusão local por chave como garantia distribuída de exatamente uma vez.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare redução de chamadas e equivalência de resultado em tarefas fixas, contra modelos locais e fronteira. A técnica economiza execução repetida, sem melhorar competência do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T007, T162

## Fontes primárias associadas

### C-S015 — singleflight package

[https://pkg.go.dev/golang.org/x/sync/singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas simultâneas de mesma chave compartilham a execução em andamento e seu resultado.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S011 — golang/sync — singleflight implementation

[https://github.com/golang/sync/blob/master/singleflight/singleflight.go](https://github.com/golang/sync/blob/master/singleflight/singleflight.go)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro de chamadas em curso por chave; Forget permite nova chamada sem aguardar a chamada anterior.

Limite: Branch master pode mudar; semântica inspecionada não constitui cache durável ou deduplicação de efeitos entre processos.

### V4C-S022 — Default Cache Behavior — Request collapsing

[https://developers.cloudflare.com/cache/concepts/default-cache-behavior/](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache lock colapsa requisições simultâneas pelo mesmo asset em um data center e distribui a resposta aos aguardantes.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S017 — Transformers — Utilities for generation

[https://huggingface.co/docs/transformers/internal/generation_utils](https://huggingface.co/docs/transformers/internal/generation_utils)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TemperatureLogitsWarper e filtros top-k/top-p transformam logits e distribuição de amostragem.

Limite: Parâmetros e ordem de aplicação variam por backend; não garantem factualidade ou determinismo entre ambientes.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
